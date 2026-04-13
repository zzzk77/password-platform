from flask import Flask, request, jsonify, render_template
import yaml
from Crypto.Cipher import DES
import binascii

app = Flask(__name__)

# 加载配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# DES弱密钥列表
DES_WEAK_KEYS = [
    b'\x01\x01\x01\x01\x01\x01\x01\x01',
    b'\xFE\xFE\xFE\xFE\xFE\xFE\xFE\xFE',
    b'\xE0\xE0\xE0\xE0\xF1\xF1\xF1\xF1',
    b'\x1F\x1F\x1F\x1F\x0E\x0E\x0E\x0E',
]

# DES半弱密钥对
DES_SEMI_WEAK_PAIRS = [
    (b'\x01\xFE\x01\xFE\x01\xFE\x01\xFE', b'\xFE\x01\xFE\x01\xFE\x01\xFE\x01'),
    (b'\x1F\xE0\x1F\xE0\x0E\xF1\x0E\xF1', b'\xE0\x1F\xE0\x1F\xF1\x0E\xF1\x0E'),
    (b'\x01\xE0\x01\xE0\x01\xF1\x01\xF1', b'\xE0\x01\xE0\x01\xF1\x01\xF1\x01'),
    (b'\x1F\xFE\x1F\xFE\x0E\xFE\x0E\xFE', b'\xFE\x1F\xFE\x1F\xFE\x0E\xFE\x0E'),
    (b'\x01\x1F\x01\x1F\x01\x0E\x01\x0E', b'\x1F\x01\x1F\x01\x0E\x01\x0E\x01'),
    (b'\xE0\xFE\xE0\xFE\xF1\xFE\xF1\xFE', b'\xFE\xE0\xFE\xE0\xFE\xF1\xFE\xF1'),
]

def pad_des(text):
    """PKCS5填充"""
    if isinstance(text, str):
        text = text.encode('utf-8')
    pad_len = 8 - (len(text) % 8)
    return text + bytes([pad_len] * pad_len)

def unpad_des(data):
    """PKCS5去填充"""
    pad_len = data[-1]
    return data[:-pad_len]

def des_encrypt(key, plaintext, mode='ECB'):
    """DES加密"""
    if isinstance(key, str):
        key = binascii.unhexlify(key)
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    plaintext = pad_des(plaintext)
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    else:
        cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(plaintext)

def des_decrypt(key, ciphertext, mode='ECB'):
    """DES解密"""
    if isinstance(key, str):
        key = binascii.unhexlify(key)
    if isinstance(ciphertext, str):
        ciphertext = binascii.unhexlify(ciphertext)
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    else:
        cipher = DES.new(key, DES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad_des(decrypted)

def is_weak_key(key_bytes):
    """检查是否为弱密钥"""
    return key_bytes in DES_WEAK_KEYS

# 获取挑战信息
@app.route('/challenges', methods=['GET'])
def get_challenges():
    challenges = []
    for challenge in config['challenges']:
        challenges.append({
            'name': challenge['name'],
            'description': challenge['description']
        })
    return jsonify({
        'status': 'success',
        'challenges': challenges,
        'target': config['name']
    })

# DES加密端点
@app.route('/des/encrypt', methods=['POST'])
def des_encrypt_endpoint():
    data = request.json.get('data', '')
    key_hex = request.json.get('key', '0101010101010101')
    mode = request.json.get('mode', 'ECB')
    
    try:
        key = binascii.unhexlify(key_hex)
        encrypted = des_encrypt(key, data, mode)
        encrypted_hex = binascii.hexlify(encrypted).decode('utf-8').upper()
        
        is_weak = is_weak_key(key)
        
        return jsonify({
            'status': 'success',
            'encrypted': encrypted_hex,
            'algorithm': 'DES-' + mode,
            'key': key_hex,
            'is_weak_key': is_weak,
            'weak_key_warning': '⚠️ 检测到弱密钥！该密钥不安全，加密两次等于无加密。' if is_weak else None
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# DES解密端点
@app.route('/des/decrypt', methods=['POST'])
def des_decrypt_endpoint():
    data_hex = request.json.get('data', '')
    key_hex = request.json.get('key', '0101010101010101')
    mode = request.json.get('mode', 'ECB')
    
    try:
        key = binascii.unhexlify(key_hex)
        ciphertext = binascii.unhexlify(data_hex)
        decrypted = des_decrypt(key, ciphertext, mode)
        
        return jsonify({
            'status': 'success',
            'decrypted': decrypted.decode('utf-8', errors='replace'),
            'algorithm': 'DES-' + mode,
            'key': key_hex
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# 二次加密验证端点（弱密钥特性）
@app.route('/des/double-encrypt', methods=['POST'])
def des_double_encrypt_endpoint():
    data = request.json.get('data', '')
    key_hex = request.json.get('key', '0101010101010101')
    
    try:
        key = binascii.unhexlify(key_hex)
        # 第一次加密
        first_encrypted = des_encrypt(key, data)
        first_hex = binascii.hexlify(first_encrypted).decode('utf-8').upper()
        # 第二次加密
        second_encrypted = des_encrypt(key, first_encrypted)
        second_hex = binascii.hexlify(second_encrypted).decode('utf-8').upper()
        
        is_weak = is_weak_key(key)
        
        return jsonify({
            'status': 'success',
            'original': data,
            'first_encrypted': first_hex,
            'second_encrypted': second_hex,
            'is_weak_key': is_weak,
            'double_encrypt_equals_original': data == unpad_des(second_encrypted).decode('utf-8', errors='replace') if second_encrypted else False,
            'explanation': '弱密钥特性：E_K(E_K(M)) = M，加密两次还原明文！' if is_weak else '非弱密钥，二次加密不会还原明文。'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# ECB模式分析端点
@app.route('/des/ecb-analyze', methods=['POST'])
def des_ecb_analyze():
    data = request.json.get('data', '')
    key_hex = request.json.get('key', '0101010101010101')
    
    try:
        key = binascii.unhexlify(key_hex)
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data
        
        data_bytes = pad_des(data_bytes)
        cipher = DES.new(key, DES.MODE_ECB)
        encrypted = cipher.encrypt(data_bytes)
        
        # 分析每个8字节块的密文
        blocks = []
        for i in range(0, len(encrypted), 8):
            block = encrypted[i:i+8]
            block_hex = binascii.hexlify(block).decode('utf-8').upper()
            blocks.append(block_hex)
        
        # 检测重复块
        unique_blocks = set(blocks)
        has_duplicates = len(unique_blocks) < len(blocks)
        
        return jsonify({
            'status': 'success',
            'total_blocks': len(blocks),
            'unique_blocks': len(unique_blocks),
            'has_duplicate_blocks': has_duplicates,
            'blocks': blocks,
            'warning': '⚠️ ECB模式警告：检测到重复密文块！相同明文产生相同密文，存在信息泄露风险！' if has_duplicates else '未检测到重复密文块。',
            'explanation': 'ECB模式下，相同的8字节明文块总是产生相同的8字节密文块。攻击者可以通过比较密文块来推断明文的结构信息。'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# 密钥空间计算端点
@app.route('/des/keyspace', methods=['GET'])
def des_keyspace():
    return jsonify({
        'status': 'success',
        'standard_des': {
            'key_bits': 64,
            'effective_bits': 56,
            'keyspace': '2^56 = 72,057,594,037,927,936',
            'explanation': '标准DES密钥64位，其中8位为校验位，有效密钥长度56位'
        },
        'weak_key_reduced': {
            'description': '某些实现忽略每个字节最高有效位',
            'effective_bits': 48,
            'keyspace': '2^48 = 281,474,976,710,656',
            'explanation': '每个字节8位 - 1位校验位 - 1位被忽略 = 6位有效，8×6=48位',
            'reduction_factor': '2^56 / 2^48 = 256倍缩减'
        },
        'weak_keys': {
            'count': 4,
            'keys': ['0101010101010101', 'FEFEFEFEFEFEFEFE', 'E0E0E0E0F1F1F1F1', '1F1F1F1F0E0E0E0E'],
            'explanation': '弱密钥特征：E_K(E_K(M)) = M，加密两次等于无加密'
        },
        'semi_weak_keys': {
            'count': 6,
            'pairs': 6,
            'explanation': '半弱密钥对：E_K1(E_K2(M)) = M，用K1加密后可用K2解密'
        }
    })

# 弱密钥检测端点
@app.route('/des/check-weak-key', methods=['POST'])
def check_weak_key():
    key_hex = request.json.get('key', '')
    
    try:
        key = binascii.unhexlify(key_hex)
        
        is_weak = key in DES_WEAK_KEYS
        is_semi_weak = False
        semi_weak_partner = None
        
        for pair in DES_SEMI_WEAK_PAIRS:
            if key == pair[0]:
                is_semi_weak = True
                semi_weak_partner = binascii.hexlify(pair[1]).decode('utf-8').upper()
                break
            elif key == pair[1]:
                is_semi_weak = True
                semi_weak_partner = binascii.hexlify(pair[0]).decode('utf-8').upper()
                break
        
        return jsonify({
            'status': 'success',
            'key': key_hex,
            'is_weak_key': is_weak,
            'is_semi_weak_key': is_semi_weak,
            'semi_weak_partner': semi_weak_partner,
            'risk_level': 'CRITICAL' if is_weak else ('HIGH' if is_semi_weak else 'NORMAL'),
            'recommendation': '立即更换密钥！弱密钥可被瞬间破解。' if is_weak else ('建议更换密钥，半弱密钥对存在相互解密风险。' if is_semi_weak else '密钥安全性正常。')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# 提交flag验证
@app.route('/submit-flag', methods=['POST'])
def submit_flag():
    challenge_name = request.json.get('challenge', '')
    flag = request.json.get('flag', '')
    
    for challenge in config['challenges']:
        if challenge['name'] == challenge_name:
            if flag == challenge['flag']:
                return jsonify({
                    'status': 'success',
                    'message': 'Flag正确！挑战完成！',
                    'challenge': challenge_name
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Flag错误，请重试！',
                    'challenge': challenge_name
                }), 400
    
    return jsonify({
        'status': 'error',
        'message': '挑战不存在！',
        'challenge': challenge_name
    }), 404

# 根路径，显示HTML页面
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 健康检查
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'name': config['name'],
        'type': config['type'],
        'difficulty': config['difficulty']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['port'], debug=False)
