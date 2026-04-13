from flask import Flask, request, jsonify, render_template
import yaml
import collections

app = Flask(__name__)

# 加载配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 凯撒密码解密
def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

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

# 频率分析
def frequency_analysis(text):
    # 统计字母频率
    frequency = collections.defaultdict(int)
    total_chars = 0
    
    for char in text:
        if char.isalpha():
            frequency[char.upper()] += 1
            total_chars += 1
    
    # 计算频率百分比
    frequency_percent = {}
    for char, count in frequency.items():
        frequency_percent[char] = (count / total_chars) * 100 if total_chars > 0 else 0
    
    # 按频率排序
    sorted_frequency = sorted(frequency_percent.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'total_chars': total_chars,
        'frequency': frequency,
        'frequency_percent': frequency_percent,
        'sorted_frequency': sorted_frequency
    }

# 获取挑战目标列表
@app.route('/targets', methods=['GET'])
def get_targets():
    targets = []
    for target in config['targets']:
        targets.append({
            'id': target['id'],
            'name': target['name'],
            'ciphertext': target['ciphertext']
        })
    return jsonify({
        'status': 'success',
        'targets': targets,
        'target': config['name']
    })

# 获取单个挑战目标详情
@app.route('/targets/<int:target_id>', methods=['GET'])
def get_target(target_id):
    for target in config['targets']:
        if target['id'] == target_id:
            return jsonify({
                'status': 'success',
                'target': {
                    'id': target['id'],
                    'name': target['name'],
                    'ciphertext': target['ciphertext']
                }
            })
    return jsonify({
        'status': 'error',
        'message': '目标不存在！'
    }), 404

# 频率分析工具
@app.route('/tools/frequency', methods=['POST'])
def frequency_tool():
    text = request.json.get('text', '')
    analysis = frequency_analysis(text)
    return jsonify({
        'status': 'success',
        'analysis': analysis
    })

# 凯撒密码破解工具
@app.route('/tools/caesar-crack', methods=['POST'])
def caesar_crack_tool():
    text = request.json.get('text', '')
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        results.append({
            'shift': shift,
            'decrypted': decrypted
        })
    return jsonify({
        'status': 'success',
        'results': results
    })

# 栅栏密码破解工具
@app.route('/tools/rail-fence-crack', methods=['POST'])
def rail_fence_crack_tool():
    text = request.json.get('text', '')
    results = []
    for rails in range(2, 6):  # 尝试2-5轨
        decrypted = rail_fence_decrypt(text, rails)
        results.append({
            'rails': rails,
            'decrypted': decrypted
        })
    return jsonify({
        'status': 'success',
        'results': results
    })

# 提交明文验证
@app.route('/submit-plaintext', methods=['POST'])
def submit_plaintext():
    target_id = request.json.get('target_id')
    plaintext = request.json.get('plaintext', '').upper()
    
    for target in config['targets']:
        if target['id'] == target_id:
            expected_plaintext = target['plaintext'].upper()
            if plaintext == expected_plaintext:
                return jsonify({
                    'status': 'success',
                    'message': '明文正确！',
                    'target': target['name']
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': '明文错误，请重试！',
                    'target': target['name']
                }), 400
    
    return jsonify({
        'status': 'error',
        'message': '目标不存在！'
    }), 404

# 提交flag验证
@app.route('/submit-flag', methods=['POST'])
def submit_flag():
    target_id = request.json.get('target_id')
    flag = request.json.get('flag', '')
    
    for target in config['targets']:
        if target['id'] == target_id:
            if flag == target['flag']:
                return jsonify({
                    'status': 'success',
                    'message': 'Flag正确！挑战完成！',
                    'target': target['name']
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Flag错误，请重试！',
                    'target': target['name']
                }), 400
    
    return jsonify({
        'status': 'error',
        'message': '目标不存在！'
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