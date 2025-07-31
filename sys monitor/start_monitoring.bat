@echo off
title System Monitor - Auto Client
echo ========================================
echo    System Monitor Auto Client
echo ========================================
echo.
echo This will automatically:
echo 1. Install required packages
echo 2. Test connection to server
echo 3. Start monitoring this PC
echo.
echo Server: 192.168.209.126:5000
echo.
echo Press any key to start...
pause

echo.
echo Starting auto client...
python auto_client.py

echo.
echo Monitoring stopped.
pause 