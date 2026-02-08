@echo off
echo ================================================
echo Chemical Equipment Parameter Visualizer
echo Backend Server Startup
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
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ================================================
echo Backend server starting...
echo Server will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

python manage.py runserver
