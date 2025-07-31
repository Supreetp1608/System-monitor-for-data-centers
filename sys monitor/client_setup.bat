@echo off
title System Monitor Client Setup
echo ========================================
echo    System Monitor Client Setup
echo ========================================
echo.
echo This will start monitoring this PC and send
echo data to the central server.
echo.
echo Server IP: 192.168.209.126
echo Server Port: 5000
echo.
echo Press any key to start monitoring...
pause

echo.
echo Installing required packages...
pip install psutil requests

echo.
echo Starting system monitor...
python monitor_client.py --server http://192.168.209.126:5000

echo.
echo Monitoring stopped.
pause 