@echo off
echo ============================================
echo   Chicken Kitchen HR - Web Application
echo   http://localhost:8000
echo   Press Ctrl+C to stop
echo ============================================
echo.

cd /d "%~dp0"

REM Load .env variables
if exist .env (
    for /f "tokens=1,2 delims==" %%a in (.env) do (
        if not "%%a"=="" if not "%%a"=="#" set "%%a=%%b"
    )
)

start http://localhost:8000
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
