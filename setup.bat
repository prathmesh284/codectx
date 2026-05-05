@echo off
REM Setup script for CodeCtx on Windows
REM Creates venv, installs dependencies, and initializes configuration

echo.
echo ================================================
echo CodeCtx Setup for Windows
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found: 
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install requirements
echo [4/5] Installing dependencies...
pip install -q --upgrade pip setuptools wheel
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Copy .env.example if .env doesn't exist
echo [5/5] Setting up configuration...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo Configuration template created: .env
    )
)
echo.

REM Initialize CodeCtx config
echo Initializing CodeCtx configuration...
python -c "from codectx.config_manager import get_config_manager; cm = get_config_manager(); print('✓ Config initialized')"
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Edit .env if needed (optional)
echo   2. Run: codectx .
echo.
echo To activate venv in future sessions:
echo   Windows: venv\Scripts\activate
echo   macOS/Linux: source venv/bin/activate
echo.
pause
