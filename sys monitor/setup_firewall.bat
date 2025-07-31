@echo off
echo ========================================
echo    System Monitor - Firewall Setup
echo ========================================
echo.
echo This script will configure Windows Firewall
echo to allow the System Monitor server on port 5000
echo.
echo Please run this as Administrator!
echo.
pause

echo.
echo Adding firewall rule for System Monitor Server...
netsh advfirewall firewall add rule name="System Monitor Server" dir=in action=allow protocol=TCP localport=5000

if %errorlevel% equ 0 (
    echo.
    echo ✅ Firewall rule added successfully!
    echo.
    echo Your server can now accept connections from other PCs.
    echo Server IP: 192.168.209.126
    echo Server Port: 5000
    echo.
    echo Other PCs can connect using:
    echo http://192.168.209.126:5000
    echo.
) else (
    echo.
    echo ❌ Failed to add firewall rule.
    echo Please run this script as Administrator!
    echo.
)

pause 