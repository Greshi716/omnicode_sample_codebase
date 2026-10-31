@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run deploy.bat first.
    pause
    exit /b 1
)

echo Starting OmniCode Web UI at http://localhost:5000/ ...
start "" http://localhost:5000/
".venv\Scripts\python.exe" main.py --ui 5000
pause
