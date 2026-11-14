@echo off
setlocal enabledelayedexpansion
title CardioPredict AI - Stopping Application...

echo ================================================================
echo       CARDIOPREDICT AI: STOPPING WEB APPLICATION ^& API
echo ================================================================
echo.

set "STOPPED=0"

REM Stop by Port 5000 PID via netstat
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo [INFO] Found server running on PID %%a. Terminating...
    taskkill /F /PID %%a >nul 2>&1
    set "STOPPED=1"
)

REM Fallback via PowerShell TCP connection check
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }" >nul 2>&1

REM Stop by window title if the command window is still open
taskkill /FI "WINDOWTITLE eq CardioPredict_AI_Server*" /F >nul 2>&1

if "!STOPPED!"=="1" (
    echo [SUCCESS] CardioPredict AI server has been stopped.
) else (
    echo [INFO] No running CardioPredict AI server detected on port 5000.
)

echo.
echo ================================================================
echo                   SERVER SHUTDOWN COMPLETE
echo ================================================================
echo.
timeout /t 3 /nobreak >nul
