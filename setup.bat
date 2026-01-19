@echo off
echo ========================================
echo   ATS Resume Analyzer - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

echo [INFO] Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt -q

cd ..

echo.
echo [INFO] Setting up Frontend...
cd frontend

REM Install npm dependencies
echo [INFO] Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload --port 8000
echo.
echo 2. Start Frontend (Terminal 2):
echo    cd frontend
echo    npm run dev
echo.
echo Then open http://localhost:3000 in your browser.
echo.
pause
