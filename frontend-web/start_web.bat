@echo off
echo ================================================
echo Chemical Equipment Parameter Visualizer
echo Web Frontend Startup
echo ================================================
echo.

cd /d "%~dp0"

echo Checking Node.js installation...
node --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo Checking npm installation...
npm --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed
    pause
    exit /b 1
)

echo.
echo Checking node_modules...
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed
)

echo.
echo ================================================
echo Web frontend starting...
echo Application will open at: http://localhost:3000
echo.
echo Make sure the backend server is running!
echo Press Ctrl+C to stop the server
echo ================================================
echo.

call npm start
