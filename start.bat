@echo off
setlocal enabledelayedexpansion
title CardioPredict AI - Starting Application...

echo ================================================================
echo       CARDIOPREDICT AI: STARTING WEB APPLICATION ^& API
echo ================================================================
echo.

REM Navigate to project root directory
cd /d "%~dp0"

REM Determine Python executable (venv or system python)
set "PYTHON_CMD=python"
if exist "venv\Scripts\python.exe" (
    set "PYTHON_CMD=venv\Scripts\python.exe"
    echo [INFO] Using virtual environment Python: venv\Scripts\python.exe
) else (
    echo [INFO] Using system Python: python
)

REM Check if Python is available
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

REM Check if port 5000 is currently occupied, terminate previous instance if found
echo [INFO] Checking if port 5000 is already in use...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo [INFO] Freeing port 5000 by terminating process PID %%a...
    taskkill /F /PID %%a >nul 2>&1
)

echo [INFO] Launching server in dedicated console window...
start "CardioPredict_AI_Server" %PYTHON_CMD% run.py

echo [INFO] Waiting for server to initialize...
timeout /t 3 /nobreak >nul

echo [INFO] Launching default web browser at http://127.0.0.1:5000 ...
start http://127.0.0.1:5000

echo.
echo ================================================================
echo   CardioPredict AI is now RUNNING!
echo   Web Portal: http://127.0.0.1:5000
echo   REST API:   http://127.0.0.1:5000/api/predict
echo.
echo   To STOP the server at any time:
echo   - Double-click 'stop.bat', or
echo   - Close the 'CardioPredict_AI_Server' window.
echo ================================================================
echo.
timeout /t 4 /nobreak >nul
