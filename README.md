# 密码虚拟攻防平台 - Docker部署指南

## 项目简介

密码虚拟攻防平台是一个用于密码学教学和实践的Web平台，包含攻击端、防御端和多个靶场环境。

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐
│   攻击端前端     │    │   防御端前端     │
│  (Port: 3001)   │    │  (Port: 3002)   │
└─────────────────┘    └─────────────────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌─────────────────┐
         │    后端服务      │
         │  (Port: 4000)   │
         └─────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌─────────┐   ┌─────────┐   ┌─────────┐
│ 靶场1   │   │ 靶场2   │   │ 靶场3   │
│(8081)   │   │(8082)   │   │(8083)   │
└─────────┘   └─────────┘   └─────────┘
```

## 服务说明

### 前端服务
- **攻击端**: http://localhost:3001
- **防御端**: http://localhost:3002

### 后端服务
- **后端API**: http://localhost:4000

### 靶场服务
- **CTF入门密码题靶场**: http://localhost:8081
- **古典密码通信系统靶场**: http://localhost:8082
- **古典密码破解挑战靶场**: http://localhost:8083

## 快速启动

### Windows用户
双击运行 `start-docker.bat` 文件，自动构建并启动所有服务。

### 手动启动
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止所有服务
docker-compose down
```

## 环境要求

- Docker Desktop 20.10+
- Docker Compose 2.0+
- 至少4GB可用内存
- 至少10GB可用磁盘空间

## 靶场Flag说明

### CTF入门密码题靶场 (Port: 8081)
- 凯撒密码: `flag{3}`
- 栅栏密码: `flag{2}`
- 简单替换密码: `flag{QWE}`

### 古典密码通信系统靶场 (Port: 8082)
- 维吉尼亚密码: `flag{SECRET}`
- Playfair密码: `flag{PLAYFAIR}`
- 混合密码系统: `flag{caesar+rail}`

### 古典密码破解挑战靶场 (Port: 8083)
- 凯撒密码破解: `flag{3}`
- 栅栏密码破解: `flag{2}`
- 维吉尼亚密码破解: `flag{SECRET}`
- 频率分析挑战: `flag{frequency}`

## 故障排除

### 端口冲突
如果端口被占用，可以修改 `docker-compose.yml` 文件中的端口映射。

### 镜像构建失败
如果镜像构建失败，请检查网络连接，确保可以访问Docker Hub。

### 服务无法访问
1. 检查Docker服务是否正常运行
2. 检查防火墙设置
3. 查看容器日志: `docker-compose logs [服务名]`

## 开发说明

### 项目结构
```
密码虚拟攻防平台/
├── attack/              # 攻击端前端代码
├── defense/             # 防御端前端代码
├── shared/              # 共享代码
├── docker/              # 靶场服务
│   ├── range-classical-ctf/
│   ├── range-classical-communication/
│   └── range-classical-crack/
├── simple-server.js     # 后端服务
├── docker-compose.yml   # Docker编排文件
├── Dockerfile.backend   # 后端Dockerfile
├── Dockerfile.frontend  # 前端Dockerfile
├── start-docker.bat     # 启动脚本
└── stop-docker.bat      # 停止脚本
```

### 本地开发
如果不使用Docker，可以分别启动各个服务：

1. 启动后端服务:
```bash
npm install
node simple-server.js
```

2. 启动前端服务:
```bash
npm run dev:attack  # 攻击端
npm run dev:defense # 防御端
```

3. 启动靶场服务:
```bash
cd docker/range-classical-ctf
pip install -r requirements.txt
python app.py
```

## 许可证

MIT License
