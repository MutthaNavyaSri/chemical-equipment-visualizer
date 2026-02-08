@echo off
echo ================================================
echo Chemical Equipment Parameter Visualizer
echo Desktop Application Startup
echo ================================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Checking virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo ================================================
echo Starting desktop application...
echo.
echo Make sure the backend server is running!
echo ================================================
echo.

python main.py

pause
