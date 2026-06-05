@echo off
title Uni-API - Setup

echo ======================================
echo   Uni-API Setup
echo ======================================
echo.

if not exist "venv" (
    echo [1/3] Creating Python virtual environment...
    python -m venv venv
) else (
    echo [1/3] Virtual environment already exists, skipping
)

echo [2/3] Installing backend dependencies...
call venv\Scripts\python.exe -m pip install -r backend\requirements.txt -q

echo [3/3] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ======================================
echo   Setup complete!
echo ======================================
echo.
echo Run the application:  start.bat
echo Run tests:            test.bat
echo.
echo On first run, open http://localhost:3000/setup to create an admin account.
echo.
pause