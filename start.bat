@echo off
title Uni-API

if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo Frontend dependencies not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo ======================================
echo   Uni-API Starting...
echo ======================================
echo.
echo   Backend:  http://localhost:8000
echo   Docs:     http://localhost:8000/docs
echo   Frontend: http://localhost:3000
echo.
echo   First time? Open http://localhost:3000/setup
echo.
echo   Press Ctrl+C to stop all services.
echo.

cd /d "%~dp0"

echo [1/2] Starting backend (4 workers)...
start /b cmd /c "cd /d backend && ..\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info"

timeout /t 3 /nobreak >nul

echo [2/2] Starting frontend...
echo.
cd frontend
call npx vite

echo.
echo Stopping services...
:: Kill uvicorn and its worker processes on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1
:: Kill any remaining vite processes
taskkill /FI "WINDOWTITLE eq *vite*" /F >nul 2>&1
echo All services stopped.