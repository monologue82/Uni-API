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

echo [2.5/3] Verifying psutil (system monitoring)...
call venv\Scripts\python.exe -c "import psutil; print('  psutil', psutil.__version__)" 2>nul || (
    echo  psutil not found, installing...
    call venv\Scripts\python.exe -m pip install psutil -q
)

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