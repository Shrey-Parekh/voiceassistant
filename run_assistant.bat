@echo off
echo ========================================
echo    AI Voice Assistant Launcher
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found! Checking dependencies...
echo.

echo Installing/updating required packages...
pip install -r requirements.txt

echo.
echo ========================================
echo Starting AI Voice Assistant...
echo ========================================
echo.
echo Say "quit" or "goodbye" to exit
echo Continuous listening mode enabled
echo.
echo Press any key to start...
pause >nul

python voice_assistant.py

echo.
echo Assistant stopped. Press any key to exit...
pause >nul
