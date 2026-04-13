#!/bin/bash

# ============================================
# 密码虚拟攻防平台 - 一键部署脚本
# ============================================

set -e

echo "========================================"
echo "   密码虚拟攻防平台 - 一键部署"
echo "========================================"

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose 未安装"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 清理旧容器
echo ""
echo "🧹 清理旧容器..."
docker compose down --remove-orphans 2>/dev/null || true

# 构建并启动
echo ""
echo "🔨 构建镜像..."
docker compose build --no-cache

echo ""
echo "🚀 启动服务..."
docker compose up -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 15

# 检查服务状态
echo ""
echo "📊 服务状态:"
docker compose ps

echo ""
echo "========================================"
echo "   ✅ 部署完成！"
echo "========================================"
echo ""
echo "📍 访问地址:"
echo "   主平台:   http://localhost/"
echo "   防御端:   http://localhost/defense/"
echo "   CTF靶场:  http://localhost/ctf/"
echo "   通信靶场: http://localhost/comm/"
echo "   破解靶场: http://localhost/crack/"
echo ""
echo "📋 运维命令:"
echo "   查看日志: docker compose logs -f"
echo "   停止服务: docker compose down"
echo "   重启服务: docker compose restart"
echo ""
