@echo off
cd /d "%~dp0"
echo ============================================================
echo  STEP 2 of 2: Opening a Cloudflare Tunnel
echo.
echo  This gives the server a PUBLIC https address that WeCom
echo  can reach. Look below for a line like:
echo      https://something-random.trycloudflare.com
echo  That is the address to give to WeCom.
echo.
echo  Keep this window OPEN. Closing it shuts the tunnel.
echo ============================================================

set CLOUDFLARED=cloudflared
if exist "%~dp0cloudflared.exe" set CLOUDFLARED=%~dp0cloudflared.exe

where %CLOUDFLARED% >nul 2>nul
if errorlevel 1 if not exist "%~dp0cloudflared.exe" (
    echo.
    echo PROBLEM: the program "cloudflared" is not installed yet.
    echo.
    echo How to fix - choose ONE:
    echo   A. Open PowerShell and run:  winget install Cloudflare.cloudflared
    echo   B. Download "cloudflared-windows-amd64.exe" from
    echo      https://github.com/cloudflare/cloudflared/releases/latest
    echo      rename it to cloudflared.exe and put it in this folder.
    echo.
    echo Then double-click this file again.
    pause
    exit /b 1
)

%CLOUDFLARED% tunnel --url http://127.0.0.1:8000
echo.
echo The tunnel has stopped. Press any key to close this window.
pause >nul
