from flask import Flask, request, jsonify, render_template
import yaml

app = Flask(__name__)

# 加载配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 维吉尼亚密码加密
def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ascii_offset + key_shift) % 26 + ascii_offset)
            key_index += 1
        else:
            result += char
    return result

# 维吉尼亚密码解密
def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ascii_offset - key_shift) % 26 + ascii_offset)
            key_index += 1
        else:
            result += char
    return result

# Playfair密码加密
def playfair_encrypt(text, key):
    # 生成Playfair矩阵
    matrix = []
    used_chars = set()
    
    # 添加密钥字符
    for char in key.upper():
        if char not in used_chars and char.isalpha():
            if char == 'J':
                char = 'I'
            matrix.append(char)
            used_chars.add(char)
    
    # 添加剩余字母
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # 跳过J
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    # 创建5x5矩阵
    playfair_matrix = [matrix[i*5:(i+1)*5] for i in range(5)]
    
    # 准备明文
    text = text.upper().replace('J', 'I')
    text_pairs = []
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            # 处理奇数长度
            text_pairs.append(text[i] + 'X')
            i += 1
        elif text[i] == text[i+1]:
            # 处理重复字符
            text_pairs.append(text[i] + 'X')
            i += 1
        else:
            text_pairs.append(text[i] + text[i+1])
            i += 2
    
    # 加密
    result = ""
    for pair in text_pairs:
        a, b = pair[0], pair[1]
        # 查找位置
        pos_a, pos_b = None, None
        for row in range(5):
            for col in range(5):
                if playfair_matrix[row][col] == a:
                    pos_a = (row, col)
                if playfair_matrix[row][col] == b:
                    pos_b = (row, col)
        
        if pos_a and pos_b:
            ra, ca = pos_a
            rb, cb = pos_b
            
            if ra == rb:
                # 同一行
                result += playfair_matrix[ra][(ca+1)%5]
                result += playfair_matrix[rb][(cb+1)%5]
            elif ca == cb:
                # 同一列
                result += playfair_matrix[(ra+1)%5][ca]
                result += playfair_matrix[(rb+1)%5][cb]
            else:
                # 矩形
                result += playfair_matrix[ra][cb]
                result += playfair_matrix[rb][ca]
    
    return result

# Playfair密码解密
def playfair_decrypt(text, key):
    # 生成Playfair矩阵
    matrix = []
    used_chars = set()
    
    # 添加密钥字符
    for char in key.upper():
        if char not in used_chars and char.isalpha():
            if char == 'J':
                char = 'I'
            matrix.append(char)
            used_chars.add(char)
    
    # 添加剩余字母
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # 跳过J
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    # 创建5x5矩阵
    playfair_matrix = [matrix[i*5:(i+1)*5] for i in range(5)]
    
    # 准备密文
    text = text.upper()
    text_pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    
    # 解密
    result = ""
    for pair in text_pairs:
        a, b = pair[0], pair[1]
        # 查找位置
        pos_a, pos_b = None, None
        for row in range(5):
            for col in range(5):
                if playfair_matrix[row][col] == a:
                    pos_a = (row, col)
                if playfair_matrix[row][col] == b:
                    pos_b = (row, col)
        
        if pos_a and pos_b:
            ra, ca = pos_a
            rb, cb = pos_b
            
            if ra == rb:
                # 同一行
                result += playfair_matrix[ra][(ca-1)%5]
                result += playfair_matrix[rb][(cb-1)%5]
            elif ca == cb:
                # 同一列
                result += playfair_matrix[(ra-1)%5][ca]
                result += playfair_matrix[(rb-1)%5][cb]
            else:
                # 矩形
                result += playfair_matrix[ra][cb]
                result += playfair_matrix[rb][ca]
    
    return result

# 混合密码系统（维吉尼亚 + Playfair）
def hybrid_encrypt(text, vigenere_key, playfair_key):
    # 先使用维吉尼亚加密
    vigenere_encrypted = vigenere_encrypt(text, vigenere_key)
    # 再使用Playfair加密
    return playfair_encrypt(vigenere_encrypted, playfair_key)

def hybrid_decrypt(text, vigenere_key, playfair_key):
    # 先使用Playfair解密
    playfair_decrypted = playfair_decrypt(text, playfair_key)
    # 再使用维吉尼亚解密
    return vigenere_decrypt(playfair_decrypted, vigenere_key)

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

# 维吉尼亚密码加密端点
@app.route('/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt_endpoint():
    data = request.json.get('data', '')
    key = request.json.get('key', 'SECRET')
    encrypted = vigenere_encrypt(data, key)
    return jsonify({
        'status': 'success',
        'encrypted': encrypted,
        'algorithm': 'Vigenere Cipher',
        'key_length': len(key)
    })

# 维吉尼亚密码解密端点
@app.route('/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt_endpoint():
    data = request.json.get('data', '')
    key = request.json.get('key', 'SECRET')
    decrypted = vigenere_decrypt(data, key)
    return jsonify({
        'status': 'success',
        'decrypted': decrypted,
        'algorithm': 'Vigenere Cipher',
        'key_length': len(key)
    })

# Playfair密码加密端点
@app.route('/playfair/encrypt', methods=['POST'])
def playfair_encrypt_endpoint():
    data = request.json.get('data', '')
    key = request.json.get('key', 'SECRET')
    encrypted = playfair_encrypt(data, key)
    return jsonify({
        'status': 'success',
        'encrypted': encrypted,
        'algorithm': 'Playfair Cipher',
        'key': key
    })

# Playfair密码解密端点
@app.route('/playfair/decrypt', methods=['POST'])
def playfair_decrypt_endpoint():
    data = request.json.get('data', '')
    key = request.json.get('key', 'SECRET')
    decrypted = playfair_decrypt(data, key)
    return jsonify({
        'status': 'success',
        'decrypted': decrypted,
        'algorithm': 'Playfair Cipher',
        'key': key
    })

# 混合密码加密端点
@app.route('/hybrid/encrypt', methods=['POST'])
def hybrid_encrypt_endpoint():
    data = request.json.get('data', '')
    vigenere_key = request.json.get('vigenere_key', 'SECRET')
    playfair_key = request.json.get('playfair_key', 'SECRET')
    encrypted = hybrid_encrypt(data, vigenere_key, playfair_key)
    return jsonify({
        'status': 'success',
        'encrypted': encrypted,
        'algorithm': 'Hybrid Cipher (Vigenere + Playfair)',
        'vigenere_key_length': len(vigenere_key),
        'playfair_key': playfair_key
    })

# 混合密码解密端点
@app.route('/hybrid/decrypt', methods=['POST'])
def hybrid_decrypt_endpoint():
    data = request.json.get('data', '')
    vigenere_key = request.json.get('vigenere_key', 'SECRET')
    playfair_key = request.json.get('playfair_key', 'SECRET')
    decrypted = hybrid_decrypt(data, vigenere_key, playfair_key)
    return jsonify({
        'status': 'success',
        'decrypted': decrypted,
        'algorithm': 'Hybrid Cipher (Vigenere + Playfair)',
        'vigenere_key_length': len(vigenere_key),
        'playfair_key': playfair_key
    })

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