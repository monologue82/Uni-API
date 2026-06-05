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

echo Starting backend...
start "Uni-API Backend" cmd /c "cd /d backend && ..\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info"

echo Starting frontend...
start "Uni-API Frontend" cmd /c "cd frontend && npx vite"

echo.
echo Both services started. Close this window to stop.
pause

taskkill /FI "WINDOWTITLE eq Uni-API Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Uni-API Frontend*" /F >nul 2>&1