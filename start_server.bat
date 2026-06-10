@echo off
cd /d "%~dp0"
echo ============================================================
echo  STEP 1 of 2: Starting the WeCom AI Gateway server
echo.
echo  Keep this window OPEN. Closing it stops the server.
echo  When you see "Application startup complete", it is ready.
echo ============================================================
call .venv\Scripts\activate.bat
python -m uvicorn gateway:app --host 0.0.0.0 --port 8000
echo.
echo The server has stopped. Press any key to close this window.
pause >nul
