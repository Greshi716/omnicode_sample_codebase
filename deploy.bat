@echo off
setlocal enabledelayedexpansion

echo =====================================================================
echo        OmniCode Consumer Sample App - Automated Deployment
echo =====================================================================
echo.

cd /d "%~dp0"

:: 1. Locate Base Framework
echo [1/5] Locating OmniCode Base Framework...
set "CORE_PATH="

if defined OMNICODE_CORE_PATH (
    if exist "%OMNICODE_CORE_PATH%\omnicode_core" (
        set "CORE_PATH=%OMNICODE_CORE_PATH%"
    )
)

if not defined CORE_PATH (
    if exist "..\Project\omnicode_core" (
        set "CORE_PATH=..\Project"
    )
)

if not defined CORE_PATH (
    echo [ERROR] Could not locate the Base Framework repo.
    echo Please ensure the base project is in a sibling folder named 'Project'
    echo or set the OMNICODE_CORE_PATH environment variable.
    pause
    exit /b 1
)

echo [+] Located Base Framework at: %CORE_PATH%

:: 2. Detect Python
echo.
echo [2/5] Checking Python installation...
set "PY_CMD="

py -3.12 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=py -3.12"
    goto :FOUND_PYTHON
)

python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
    goto :FOUND_PYTHON
)

echo [!] Python 3.12 was not found on PATH.
echo [*] Attempting to install Python 3.12 via winget...
winget install --id Python.Python.3.12 -e --source winget
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python. Please install Python 3.12 manually and rerun.
    pause
    exit /b 1
)
set "PY_CMD=py -3.12"

:FOUND_PYTHON
echo [+] Using Python: %PY_CMD%

:: 3. Create Virtual Environment
echo.
echo [3/5] Setting up virtual environment (.venv)...
if not exist ".venv\Scripts\python.exe" (
    echo [*] Creating virtualenv in .venv...
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [+] Existing .venv detected.
)

set "VENV_PY=.venv\Scripts\python.exe"
set "VENV_PIP=.venv\Scripts\pip.exe"

:: 4. Install omnicode-core from Base and Consumer Dependencies
echo.
echo [4/5] Installing dependencies and linking omnicode-core library...
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel --quiet
"%VENV_PIP%" install -e "%CORE_PATH%" --quiet
"%VENV_PIP%" install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)
echo [+] Dependencies installed and omnicode-core linked.

:: Setup .env if missing
if not exist ".env" (
    echo [*] Creating default .env configuration...
    echo # Consumer App Environment Configuration > .env
    echo OMNICODE_CORE_PATH=!CORE_PATH! >> .env
    echo ANTHROPIC_API_KEY= >> .env
    echo [+] Created .env file.
)

:: 5. Run the 3-Bug Benchmark Evaluation
echo.
echo [5/5] Running the 3-Bug Benchmark Evaluation...
"%VENV_PY%" eval\run_eval.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Benchmark runner finished with non-zero code.
)

echo.
echo =====================================================================
echo  SUCCESS: OmniCode Consumer App is deployed and evaluated!
echo  Location: %~dp0
echo  Virtualenv: %~dp0.venv
echo =====================================================================
echo.
pause
