@echo off
echo ==================================================
echo         Password Attack & Defense Platform
echo               Quick Start Script
echo ==================================================

echo [1/4] Stopping old containers...
docker-compose down

echo [2/4] Building and starting services...
docker-compose up -d --build

echo [3/4] Waiting for database to initialize (20s)...
timeout /t 20

echo [4/4] Initializing database and seeding data...
docker exec -it padp-main-app npm run db:push
docker exec -it padp-main-app npm run db:seed

echo ==================================================
echo  Startup Complete!
echo  Frontend: http://localhost:3000
echo  Backend:  http://localhost:4000
echo  AI Service: http://localhost:5000
echo ==================================================
pause
