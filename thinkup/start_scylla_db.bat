@echo off
echo Starting Local Infrastructure (ScyllaDB + MinIO)...
cd platform-backend
docker-compose down
docker-compose up -d
if %errorlevel% neq 0 (
    echo Docker startup failed. Please ensure Docker Desktop is running.
    pause
    exit /b %errorlevel%
)

echo Waiting for services to be ready...
timeout /t 10

echo Initializing Database Tables...
python init_local_db.py

echo Initializing S3 Buckets...
python init_local_s3.py

echo Infrastructure is ready!
echo ScyllaDB: http://localhost:8000
echo MinIO Console: http://localhost:9001 (User: local, Pass: localpassword)
pause