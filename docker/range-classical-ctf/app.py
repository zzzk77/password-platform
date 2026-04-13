from flask import Flask, request, jsonify, render_template
import yaml

app = Flask(__name__)

# 加载配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 凯撒密码加密
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

# 凯撒密码解密
def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# 栅栏密码加密
def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    return ''.join([''.join(row) for row in fence])

# 栅栏密码解密
def rail_fence_decrypt(ciphertext, rails):
    fence = [[''] * len(ciphertext) for _ in range(rails)]
    rail = 0
    direction = 1
    
    # 标记栅栏位置
    for i in range(len(ciphertext)):
        fence[rail][i] = 'x'
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    # 填充栅栏
    index = 0
    for i in range(rails):
        for j in range(len(ciphertext)):
            if fence[i][j] == 'x':
                fence[i][j] = ciphertext[index]
                index += 1
    
    # 读取解密结果
    result = []
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    return ''.join(result)

# 简单替换密码（固定映射）
substitution_map = {
    'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R', 'E': 'T',
    'F': 'Y', 'G': 'U', 'H': 'I', 'I': 'O', 'J': 'P',
    'K': 'A', 'L': 'S', 'M': 'D', 'N': 'F', 'O': 'G',
    'P': 'H', 'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z',
    'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B', 'Y': 'N', 'Z': 'M'
}

# 简单替换密码加密
def substitution_encrypt(text):
    result = ""
    for char in text:
        if char.isalpha():
            upper = char.isupper()
            char = char.upper()
            if char in substitution_map:
                result += substitution_map[char] if upper else substitution_map[char].lower()
            else:
                result += char
        else:
            result += char
    return result

# 简单替换密码解密
def substitution_decrypt(text):
    reverse_map = {v: k for k, v in substitution_map.items()}
    result = ""
    for char in text:
        if char.isalpha():
            upper = char.isupper()
            char = char.upper()
            if char in reverse_map:
                result += reverse_map[char] if upper else reverse_map[char].lower()
            else:
                result += char
        else:
            result += char
    return result

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

# 凯撒密码加密端点
@app.route('/caesar/encrypt', methods=['POST'])
def caesar_encrypt_endpoint():
    data = request.json.get('data', '')
    shift = request.json.get('shift', 3)
    encrypted = caesar_encrypt(data, shift)
    return jsonify({
        'status': 'success',
        'encrypted': encrypted,
        'algorithm': 'Caesar Cipher',
        'shift': shift
    })

# 凯撒密码解密端点
@app.route('/caesar/decrypt', methods=['POST'])
def caesar_decrypt_endpoint():
    data = request.json.get('data', '')
    shift = request.json.get('shift', 3)
    decrypted = caesar_decrypt(data, shift)
    return jsonify({
        'status': 'success',
        'decrypted': decrypted,
        'algorithm': 'Caesar Cipher',
        'shift': shift
    })

# 栅栏密码加密端点
@app.route('/rail-fence/encrypt', methods=['POST'])
def rail_fence_encrypt_endpoint():
    data = request.json.get('data', '')
    rails = request.json.get('rails', 2)
    encrypted = rail_fence_encrypt(data, rails)
    return jsonify({
        'status': 'success',
        'encrypted': encrypted,
        'algorithm': 'Rail Fence Cipher',
        'rails': rails
    })

# 栅栏密码解密端点
@app.route('/rail-fence/decrypt', methods=['POST'])
def rail_fence_decrypt_endpoint():
    data = request.json.get('data', '')
    rails = request.json.get('rails', 2)
    decrypted = rail_fence_decrypt(data, rails)
    return jsonify({
        'status': 'success',
        'decrypted': decrypted,
        'algorithm': 'Rail Fence Cipher',
        'rails': rails
    })

# 替换密码加密端点
@app.route('/substitution/encrypt', methods=['POST'])
def substitution_encrypt_endpoint():
    data = request.json.get('data', '')
    encrypted = substitution_encrypt(data)
    return jsonify({
        'status': 'success',
        'encrypted': encrypted,
        'algorithm': 'Substitution Cipher'
    })

# 替换密码解密端点
@app.route('/substitution/decrypt', methods=['POST'])
def substitution_decrypt_endpoint():
    data = request.json.get('data', '')
    decrypted = substitution_decrypt(data)
    return jsonify({
        'status': 'success',
        'decrypted': decrypted,
        'algorithm': 'Substitution Cipher'
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