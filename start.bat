@echo off
title ComplaintIQ - Starting...
color 0A

echo.
echo  ========================================
echo    ComplaintIQ - AI Complaint Center
echo  ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install Python 3.11+
    pause
    exit /b 1
)

:: Setup backend venv if not exists
if not exist "backend\venv" (
    echo  [SETUP] Creating virtual environment...
    python -m venv backend\venv
    echo  [SETUP] Installing dependencies...
    backend\venv\Scripts\pip install -r backend\requirements.txt --quiet
)

:: Check if .env exists
if not exist "backend\.env" (
    copy "backend\.env.example" "backend\.env" >nul
    echo  [WARN] Created backend\.env from example. Add your OPENAI_API_KEY!
)

echo  [1/2] Starting Backend  --^> http://localhost:8000
echo  [2/2] Starting Frontend --^> http://localhost:5500
echo.
echo  API Docs : http://localhost:8000/docs
echo  App      : http://localhost:5500
echo.
echo  Press Ctrl+C in each window to stop.
echo  ========================================
echo.

:: Start backend in new window
start "ComplaintIQ Backend" cmd /k "cd /d "%~dp0backend" && venv\Scripts\activate && uvicorn main:app --reload --port 8000 --host 0.0.0.0"

:: Small delay
timeout /t 2 /nobreak >nul

:: Start frontend in new window
start "ComplaintIQ Frontend" cmd /k "cd /d "%~dp0frontend" && python -m http.server 5500"

:: Open browser
timeout /t 3 /nobreak >nul
start http://localhost:5500

echo  Both servers started! Browser opening...
echo  Close the two server windows to stop.
pause
