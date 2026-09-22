@echo off
title CipherMind Launcher
cd /d "%~dp0"

echo ============================================
echo   CipherMind - Setup and Launch
echo ============================================

REM 1. Check for .env file
if not exist ".env" (
    echo No .env file found.
    echo Creating one from .env.example ...
    copy .env.example .env >nul
    echo.
    echo IMPORTANT: Open the new .env file and add your
    echo HF_API_TOKEN and GROQ_API_KEY_1 before continuing.
    echo.
    pause
)

REM 2. Create virtual environment if missing
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM 3. Install dependencies
echo Installing dependencies (first run only, may take a few minutes)...
pip install -q -r requirements.txt

REM 4. Open the browser after a short delay, then start the server
echo Starting CipherMind server...
start /b cmd /c "timeout /t 3 /nobreak >nul & start "" http://127.0.0.1:8000"
python -m uvicorn main:app --host 127.0.0.1 --port 8000

pause
