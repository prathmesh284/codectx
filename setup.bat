@echo off
REM Setup script for CodeCtx on Windows
REM Delegates setup to the cross-platform bootstrap.

echo.
echo ================================================
echo CodeCtx Setup for Windows
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/2] Python found:
python --version
echo.
echo [2/2] Running smart bootstrap...
python bootstrap.py
if errorlevel 1 (
    echo ERROR: Bootstrap failed
    pause
    exit /b 1
)

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Edit .env if needed (optional)
echo   2. Open a new terminal if PATH was updated
echo   3. Run: codectx .
echo.
echo Project launcher directory:
echo   %CD%\bin
echo.
pause
