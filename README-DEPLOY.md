# 密码虚拟攻防平台 - 一键部署指南

## 🚀 快速开始

### 环境要求
- Linux 服务器 (Ubuntu 20.04+ / CentOS 7+)
- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 内存
- 至少 10GB 磁盘空间

### 一键部署

```bash
# 1. 上传项目到服务器
scp -r ./密码虚拟攻防平台 user@your-server:/home/user/

# 2. SSH 登录服务器
ssh user@your-server

# 3. 进入项目目录
cd 密码虚拟攻防平台

# 4. 赋予执行权限
chmod +x deploy.sh

# 5. 一键部署
./deploy.sh
```

### Windows PowerShell

```powershell
# 进入项目目录
cd .\密码虚拟攻防平台\

# 一键部署
.\start-docker.bat
```

## 📍 部署后访问

部署完成后，访问服务器 IP 或域名：

| 服务 | 地址 |
|------|------|
| **主平台** | http://服务器IP/ |
| **攻击端** | http://服务器IP/attack/ |
| **防御端** | http://服务器IP/defense/ |
| **CTF靶场** | http://服务器IP/ctf/ |
| **通信靶场** | http://服务器IP/comm/ |
| **破解靶场** | http://服务器IP/crack/ |

## 📋 常用运维命令

```bash
# 查看服务状态
docker compose ps

# 查看实时日志
docker compose logs -f

# 重启所有服务
docker compose restart

# 停止所有服务
docker compose down

# 更新并重新部署
git pull && ./deploy.sh
```

## 🔧 自定义配置

### 修改端口
编辑 `docker-compose.yml` 中的端口映射：

```yaml
nginx:
  ports:
    - "8080:80"  # 修改为 8080 端口
```

### 修改域名
编辑 `nginx/deploy.conf`，将 `server_name localhost;` 改为你的域名：

```nginx
server_name your-domain.com;
```

### SSL/HTTPS 配置
编辑 `nginx/deploy.conf`：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # ... 其余配置
}
```

## 🐛 故障排查

### 端口冲突
```bash
# 查看端口占用
netstat -tlnp | grep :80

# 修改 docker-compose.yml 中的端口
```

### 容器启动失败
```bash
# 查看详细日志
docker compose logs [服务名]

# 常见问题:
# - 4000端口被占用: 停止本地后端服务
# - 构建失败: 检查Dockerfile和网络
```

### 前端无法访问API
```bash
# 检查后端是否正常运行
docker compose logs backend

# 检查API连通性
curl http://localhost/api/settings
```

## 📊 系统架构

```
                    ┌─────────────┐
                    │   用户浏览器  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Nginx     │
                    │   (端口80)   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
   │  前端    │       │  后端    │       │  靶场    │
   │3001/3002│       │ (4000)  │       │8081-8083│
   └─────────┘       └─────────┘       └─────────┘
```

## 🔐 安全建议

1. **修改默认端口** - 避免使用默认端口
2. **配置防火墙** - 只开放 80/443 端口
3. **启用 HTTPS** - 使用 Let's Encrypt 免费证书
4. **定期更新** - 保持 Docker 镜像最新
5. **限制资源** - 为容器设置资源限制
