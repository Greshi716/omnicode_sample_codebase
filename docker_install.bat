@echo off
setlocal

cd /d "%~dp0"

echo =====================================================================
echo           OmniCode Consumer Sample App - Docker Installer
echo =====================================================================
echo.

if exist "..\Project\docker_install.bat" (
    echo [+] Redirecting to Unified Docker Installer in Base Framework...
    call "..\Project\docker_install.bat"
    exit /b %ERRORLEVEL%
)

echo [1/3] Checking Docker installation...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed or not in PATH.
    pause
    exit /b 1
)

echo [2/3] Checking Docker daemon...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker daemon is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [3/3] Launching Sample App containers via Docker Compose...
docker compose up -d --build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker compose failed.
    pause
    exit /b 1
)

echo.
echo =====================================================================
echo  SUCCESS: Sample App Docker container is running!
echo  Port: http://localhost:8080
echo  To view logs: docker compose logs -f
echo  To stop:      docker compose down
echo =====================================================================
echo.
pause
