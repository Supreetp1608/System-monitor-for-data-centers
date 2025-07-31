@echo off
title System Monitor Server
echo ========================================
echo    System Monitor Server
echo ========================================
echo.
echo Starting server...
echo Dashboard will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the server
python server/app.py

echo.
echo Server stopped.
pause 