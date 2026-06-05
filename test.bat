@echo off
title Uni-API - Test

if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting backend for testing...
start "Uni-API Backend" venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level error
timeout /t 3 /nobreak >nul

echo Running integration tests...
echo.
venv\Scripts\python.exe tests\test_integration.py

echo.
echo Tests finished. Cleaning up...
taskkill /FI "WINDOWTITLE eq Uni-API Backend*" /F >nul 2>&1

pause