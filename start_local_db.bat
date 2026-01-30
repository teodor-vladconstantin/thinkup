@echo off
echo Starting Local Database (Moto)...
start /B python -m moto.server -p 8000
echo Database started on port 8000.
echo.
echo Initializing tables...
cd platform-backend
python init_local_db.py
cd ..
echo Done.
pause