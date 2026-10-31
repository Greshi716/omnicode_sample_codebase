@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run deploy.bat first.
    pause
    exit /b 1
)

echo Running OmniCode Diagnostic Evaluation Benchmark...
".venv\Scripts\python.exe" eval\run_eval.py
pause
