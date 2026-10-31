@echo off
setlocal

cd /d "%~dp0"

echo =====================================================================
echo         OmniCode Consumer Sample App - Docker Installer
echo =====================================================================
echo.

echo [1/3] Checking Docker installation...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed or not in PATH.
    echo Please install Docker Desktop and rerun.
    pause
    exit /b 1
)

echo [2/3] Checking Docker daemon status...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker daemon is not running. Please start Docker Desktop.
    pause
    exit /b 1
)
echo [+] Docker daemon is running.

echo.
echo [3/3] Building and starting Sample App & PostgreSQL containers...
docker compose up -d --build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker compose build/start failed.
    pause
    exit /b 1
)

echo.
echo =====================================================================
echo  SUCCESS: Consumer Sample App Docker Stack is deployed!
echo =====================================================================
echo  - Spring Boot Service: http://localhost:8080
echo  - PostgreSQL Database: localhost:5432 (library_db)
echo  - View logs:          docker compose logs -f
echo  - Stop stack:         docker compose down
echo =====================================================================
echo.
pause
