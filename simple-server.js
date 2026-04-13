// 简化版后端服务
import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';

const app = express();
const PORT = 4000;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 模拟数据
let users = [];
let emailCodes = new Map();

// 生成6位数字验证码
function generateCode() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

// 邮箱格式校验
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// 生成token
function generateToken(userId) {
  const payload = { userId, ts: Date.now() };
  return Buffer.from(JSON.stringify(payload)).toString('base64');
}

// 邮件发送功能暂时禁用

// 发送邮箱验证码接口
app.post('/api/users/send-code', async (req, res) => {
  const { email, type = 'register' } = req.body;

  if (!email || !isValidEmail(email)) {
    return res.status(400).json({ message: '请输入有效的邮箱地址' });
  }

  // 注册时检查邮箱是否已被使用
  if (type === 'register') {
    const existingUser = users.find(user => user.email === email);
    if (existingUser) {
      return res.status(409).json({ message: '该邮箱已被注册' });
    }
  }

  // 重置密码时检查邮箱是否存在
  if (type === 'reset') {
    const existingUser = users.find(user => user.email === email);
    if (!existingUser) {
      return res.status(404).json({ message: '该邮箱未注册' });
    }
  }

  const code = generateCode();
  emailCodes.set(email, {
    code,
    type,
    expireAt: Date.now() + 5 * 60 * 1000 // 5分钟过期
  });

  // 开发环境：直接输出验证码到终端
  console.log(`[邮箱验证码] ${email} 的验证码: ${code} (类型: ${type})`);
  
  // 模拟邮件发送成功
  const success = true;

  if (success) {
    res.json({
      message: '验证码已发送到您的邮箱（开发环境：请查看终端输出）',
      // 开发环境返回验证码，生产环境去掉
      code: process.env.NODE_ENV === 'production' ? undefined : code
    });
  } else {
    res.status(500).json({ message: '发送验证码失败，请稍后重试' });
  }
});

// 验证邮箱验证码接口
app.post('/api/users/verify-code', (req, res) => {
  const { email, code, type = 'register' } = req.body;

  if (!email || !code) {
    return res.status(400).json({ message: '请输入邮箱和验证码' });
  }

  const codeData = emailCodes.get(email);
  if (!codeData) {
    return res.status(400).json({ message: '验证码已过期或不存在' });
  }

  if (codeData.type !== type) {
    return res.status(400).json({ message: '验证码类型不匹配' });
  }

  if (codeData.expireAt < Date.now()) {
    emailCodes.delete(email);
    return res.status(400).json({ message: '验证码已过期' });
  }

  if (codeData.code !== code) {
    return res.status(400).json({ message: '验证码错误' });
  }

  // 验证码验证成功
  emailCodes.delete(email);
  res.json({ message: '验证码验证成功' });
});

// 用户注册接口
app.post('/api/users/register', (req, res) => {
  const { username, email, password, role = 'user' } = req.body;

  if (!username || !email || !password) {
    return res.status(400).json({ message: '请输入用户名、邮箱和密码' });
  }

  if (!isValidEmail(email)) {
    return res.status(400).json({ message: '请输入有效的邮箱地址' });
  }

  // 检查用户名是否已存在
  const existingUser = users.find(user => user.username === username);
  if (existingUser) {
    return res.status(409).json({ message: '用户名已存在' });
  }

  // 检查邮箱是否已存在
  const existingEmail = users.find(user => user.email === email);
  if (existingEmail) {
    return res.status(409).json({ message: '邮箱已被注册' });
  }

  // 创建新用户
  const newUser = {
    id: users.length + 1,
    username,
    email,
    password, // 实际应用中应该加密
    role,
    nickname: username,
    avatar: '',
    allowedRoles: ['user']
  };

  users.push(newUser);
  const token = generateToken(newUser.id);

  res.json({
    message: '注册成功',
    user: {
      id: newUser.id,
      username: newUser.username,
      email: newUser.email,
      role: newUser.role,
      nickname: newUser.nickname,
      avatar: newUser.avatar
    },
    token
  });
});

// 用户登录接口
app.post('/api/users/login', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ message: '请输入用户名和密码' });
  }

  const user = users.find(u => u.username === username && u.password === password);
  if (!user) {
    return res.status(401).json({ message: '用户名或密码错误' });
  }

  const token = generateToken(user.id);

  res.json({
    message: '登录成功',
    user: {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      nickname: user.nickname,
      avatar: user.avatar
    },
    token
  });
});

// 忘记密码接口
app.post('/api/users/forgot-password', (req, res) => {
  const { email, code, newPassword } = req.body;

  if (!email || !code || !newPassword) {
    return res.status(400).json({ message: '请输入邮箱、验证码和新密码' });
  }

  const codeData = emailCodes.get(email);
  if (!codeData || codeData.type !== 'reset' || codeData.expireAt < Date.now()) {
    return res.status(400).json({ message: '验证码已过期或不存在' });
  }

  if (codeData.code !== code) {
    return res.status(400).json({ message: '验证码错误' });
  }

  const user = users.find(u => u.email === email);
  if (!user) {
    return res.status(404).json({ message: '用户不存在' });
  }

  // 更新密码
  user.password = newPassword;
  emailCodes.delete(email);

  res.json({ message: '密码重置成功' });
});

// 模拟攻击场景数据
const attackScenarios = [
  {
    id: 1,
    name: 'CTF入门密码题',
    description: '测试凯撒密码、栅栏密码等古典密码的破解方法，适合CTF入门。',
    difficulty: '简单',
    successRate: 90,
    type: '古典密码加密'
  },
  {
    id: 2,
    name: '古典密码通信系统',
    description: '模拟二战时期的密码通信系统，测试维吉尼亚密码、Playfair密码等古典密码的加密方法。',
    difficulty: '中等',
    successRate: 75,
    type: '古典密码加密'
  },
  {
    id: 3,
    name: '古典密码破解挑战',
    description: '提供多种古典密码的密文，挑战破解能力，包括频率分析、暴力破解等方法。',
    difficulty: '困难',
    successRate: 60,
    type: '古典密码加密'
  }
];

// 模拟防御措施数据
const defenseMeasures = [
  {
    id: 1,
    name: '密码复杂度要求',
    description: '设置密码长度、复杂度要求，防止弱密码被破解。',
    effectiveness: 85
  },
  {
    id: 2,
    name: '双因素认证',
    description: '启用双因素认证，增加账户安全性。',
    effectiveness: 95
  },
  {
    id: 3,
    name: '定期密码更换',
    description: '强制用户定期更换密码，减少密码被破解的风险。',
    effectiveness: 70
  }
];

// 模拟靶场数据
const ranges = [
  {
    id: 1,
    name: 'CTF入门密码题',
    type: '古典密码加密',
    description: '测试凯撒密码、栅栏密码等古典密码的破解方法，适合CTF入门。',
    difficulty: 1,
    port: 8081,
    url: 'http://localhost:8081',
    status: '运行中'
  },
  {
    id: 2,
    name: '古典密码通信系统',
    type: '古典密码加密',
    description: '模拟二战时期的密码通信系统，测试维吉尼亚密码、Playfair密码等古典密码的加密方法。',
    difficulty: 2,
    port: 8082,
    url: 'http://localhost:8082',
    status: '运行中'
  },
  {
    id: 3,
    name: '古典密码破解挑战',
    type: '古典密码加密',
    description: '提供多种古典密码的密文，挑战破解能力，包括频率分析、暴力破解等方法。',
    difficulty: 3,
    port: 8083,
    url: 'http://localhost:8083',
    status: '运行中'
  }
];

// 模拟场景数据
const scenes = [
  {
    id: 1,
    name: 'CTF入门密码题',
    type: '古典密码加密',
    description: '测试凯撒密码、栅栏密码等古典密码的破解方法，适合CTF入门。',
    difficulty: 1,
    status: '已部署',
    successCount: 156,
    topology: {
      nodes: [
        { id: 1, name: '靶场入口', type: 'entry' },
        { id: 2, name: '密码分析', type: 'analysis' },
        { id: 3, name: 'flag提交', type: 'submit' }
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 }
      ]
    }
  },
  {
    id: 2,
    name: '古典密码通信系统',
    type: '古典密码加密',
    description: '模拟二战时期的密码通信系统，测试维吉尼亚密码、Playfair密码等古典密码的加密方法。',
    difficulty: 2,
    status: '已部署',
    successCount: 89,
    topology: {
      nodes: [
        { id: 1, name: '靶场入口', type: 'entry' },
        { id: 2, name: '加密分析', type: 'analysis' },
        { id: 3, name: '密钥破解', type: 'crack' },
        { id: 4, name: 'flag提交', type: 'submit' }
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
        { source: 3, target: 4 }
      ]
    }
  },
  {
    id: 3,
    name: '古典密码破解挑战',
    type: '古典密码加密',
    description: '提供多种古典密码的密文，挑战破解能力，包括频率分析、暴力破解等方法。',
    difficulty: 3,
    status: '已部署',
    successCount: 45,
    topology: {
      nodes: [
        { id: 1, name: '靶场入口', type: 'entry' },
        { id: 2, name: '密文分析', type: 'analysis' },
        { id: 3, name: '频率分析', type: 'frequency' },
        { id: 4, name: '暴力破解', type: 'brute' },
        { id: 5, name: 'flag提交', type: 'submit' }
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
        { source: 3, target: 4 },
        { source: 4, target: 5 }
      ]
    }
  }
];

// API路由
app.get('/api/attack/scenarios', (req, res) => {
  res.json(attackScenarios);
});

app.get('/api/defense/measures', (req, res) => {
  res.json(defenseMeasures);
});

app.get('/api/ranges', (req, res) => {
  res.json(ranges);
});

app.get('/api/ranges/:id', (req, res) => {
  const { id } = req.params;
  const range = ranges.find(r => r.id == id);
  if (range) {
    res.json(range);
  } else {
    res.status(404).json({ message: '靶场不存在' });
  }
});

app.post('/api/ranges/:id/start', (req, res) => {
  const { id } = req.params;
  const range = ranges.find(r => r.id == id);
  if (range) {
    range.status = '运行中';
    res.json({ message: '靶场启动成功', range });
  } else {
    res.status(404).json({ message: '靶场不存在' });
  }
});

app.post('/api/ranges/:id/stop', (req, res) => {
  const { id } = req.params;
  const range = ranges.find(r => r.id == id);
  if (range) {
    range.status = '已停止';
    res.json({ message: '靶场停止成功', range });
  } else {
    res.status(404).json({ message: '靶场不存在' });
  }
});

app.get('/api/scenes', (req, res) => {
  res.json(scenes);
});

app.post('/api/flag/submit', (req, res) => {
  const { flag, targetId } = req.body;
  // 简单的flag验证逻辑
  if (flag && targetId) {
    res.json({
      success: true,
      message: 'Flag提交成功！',
      score: 100
    });
  } else {
    res.json({
      success: false,
      message: 'Flag提交失败，请检查输入。'
    });
  }
});

// 启动服务
app.listen(PORT, () => {
  console.log(`简化版后端服务运行在 http://localhost:${PORT}`);
  // 初始化用户数据
  users = [
    {
      id: 1,
      username: 'admin',
      email: 'admin@example.com',
      password: 'admin123',
      role: 'admin',
      nickname: '系统管理员',
      avatar: '',
      allowedRoles: ['admin', 'attacker', 'defender', 'guest']
    },
    {
      id: 2,
      username: 'attacker',
      email: 'attacker@example.com',
      password: 'attack123',
      role: 'attacker',
      nickname: '红队队员',
      avatar: '',
      allowedRoles: ['attacker', 'guest']
    },
    {
      id: 3,
      username: 'defender',
      email: 'defender@example.com',
      password: 'defense123',
      role: 'defender',
      nickname: '蓝队队员',
      avatar: '',
      allowedRoles: ['defender', 'guest']
    },
    {
      id: 4,
      username: 'guest',
      email: 'guest@example.com',
      password: 'guest123',
      role: 'guest',
      nickname: '访客',
      avatar: '',
      allowedRoles: ['guest']
    }
  ];
});