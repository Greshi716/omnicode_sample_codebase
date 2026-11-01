@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo =====================================================================
echo         OmniCode Consumer Sample App - Docker Installer
echo =====================================================================
echo.

echo [1/5] Checking Docker installation...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed or not in PATH.
    echo Please install Docker Desktop and rerun.
    pause
    exit /b 1
)

echo [2/5] Checking Docker daemon status...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker daemon is not running. Start Docker Desktop, wait for "Engine running", then rerun.
    pause
    exit /b 1
)
echo [+] Docker daemon is running.

echo [3/5] Checking the framework folder ^(..\Project^)...
if not exist "..\Project\pyproject.toml" (
    echo [ERROR] The omnicode-core framework must be next to this folder at ..\Project
    pause
    exit /b 1
)

echo [4/5] Checking .env ...
if not exist ".env" (
    copy /Y ".env.example" ".env" >nul
    echo [+] Created .env from .env.example - set POSTGRES_PASSWORD and ANTHROPIC_API_KEY in it, then rerun.
    pause
    exit /b 0
)

echo.
echo [5/5] Building and starting Sample App and PostgreSQL ^(first build downloads ~2 GB^)...
docker compose up -d --build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker compose build/start failed. Scroll up for the failing step.
    pause
    exit /b 1
)

echo [*] Waiting for the app to become healthy ^(first start indexes the codebase^)...
set /a TRIES=0
:WAIT_LOOP
set "HEALTH="
for /f "delims=" %%H in ('docker inspect --format "{{.State.Health.Status}}" sample-app-service 2^>nul') do set "HEALTH=%%H"
if "!HEALTH!"=="healthy" goto :HEALTHY
set /a TRIES+=1
if !TRIES! GEQ 60 (
    echo [ERROR] The app did not become healthy within 5 minutes. Last logs:
    docker compose logs --tail 40 app
    pause
    exit /b 1
)
timeout /t 5 /nobreak >nul
goto :WAIT_LOOP
:HEALTHY

echo.
echo =====================================================================
echo  SUCCESS: Consumer Sample App Docker Stack is running!
echo =====================================================================
echo  - Sample App Web UI:    http://localhost:8080
echo  - PostgreSQL Database:  internal container db ^(library_db^)
echo  - View logs:            docker compose logs -f app
echo  - Stop stack:           docker compose down      ^(add -v to wipe the database^)
echo =====================================================================
echo.
pause
