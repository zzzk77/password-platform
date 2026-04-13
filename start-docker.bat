@echo off
echo ========================================
echo 密码虚拟攻防平台 - Docker启动脚本
echo ========================================
echo.

echo [1/3] 停止并删除旧容器...
docker-compose down

echo.
echo [2/3] 构建镜像...
docker-compose build

echo.
echo [3/3] 启动服务...
docker-compose up -d

echo.
echo ========================================
echo 服务启动完成！
echo ========================================
echo.
echo 访问地址：
echo   - 攻击端: http://localhost:3001
echo   - 防御端: http://localhost:3002
echo   - 后端API: http://localhost:4000
echo   - CTF入门密码题靶场: http://localhost:8081
echo   - 古典密码通信系统靶场: http://localhost:8082
echo   - 古典密码破解挑战靶场: http://localhost:8083
echo.
echo 按任意键退出...
pause >nul
