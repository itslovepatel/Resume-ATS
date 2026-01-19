@echo off
echo ========================================
echo   Starting ATS Resume Analyzer
echo ========================================
echo.

REM Start Backend
echo [INFO] Starting Backend Server...
start "ATS Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo [INFO] Starting Frontend Server...
start "ATS Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo [INFO] Servers starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

start http://localhost:3000

echo.
echo Press any key to stop both servers...
pause >nul
taskkill /FI "WINDOWTITLE eq ATS Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq ATS Frontend*" /F >nul 2>&1
