@echo off
setlocal enabledelayedexpansion

set "ip1=192.168.5.3"
set "ip2=192.168.5.4"

:connect_ip
cls
echo Please select the phone to connect:
echo 1. Phone 1 - %ip1%
echo 2. Phone 2 - %ip2%
set /p choice="Enter 1 or 2: "

if "!choice!"=="1" (
    set "ip=!ip1!"
) else if "!choice!"=="2" (
    set "ip=!ip2!"
) else (
    echo Invalid choice, please select again.
    pause
    goto connect_ip
)

echo Trying to connect to phone via IP !ip!...
adb connect !ip!:5555

:: 检查是否连接成功
adb devices | findstr /C:"!ip!:5555" | findstr /C:"device" >nul
if errorlevel 1 (
    echo [!] IP connection failed. 
    echo [?] Is the phone connected via USB? 
    echo [*] Attempting to reset TCP mode via USB...
    
    :: 在这里加入 tcpip 命令
    adb tcpip 5555
    timeout /t 2 >nul
    
    :: 再次尝试连接
    adb connect !ip!:5555
)

:: 再次检查
adb devices | findstr /C:"!ip!:5555" | findstr /C:"device" >nul
if errorlevel 1 (
    echo [X] Still cannot connect. Please check:
    echo     1. Phone and PC are on the same Wi-Fi.
    echo     2. USB Debugging is ON.
    pause
    exit /b
)

echo Connection successful! Launching scrcpy...
scrcpy --tcpip=!ip!:5555 --turn-screen-off

pause
goto connect_ip
