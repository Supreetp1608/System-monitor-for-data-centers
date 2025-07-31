@echo off
title System Monitor Client
echo ========================================
echo    System Monitor Client
echo ========================================
echo.
echo Starting system monitoring...
echo Press Ctrl+C to stop
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the client script
python client/monitor_client.py --server http://localhost:5000

echo.
echo Monitoring stopped.
pause 