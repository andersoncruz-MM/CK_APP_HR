@echo off
echo ============================================
echo   Chicken Kitchen HR Forms - Web App
echo   Opening http://localhost:8080/web/
echo   Press Ctrl+C to stop the server
echo ============================================
echo.
cd /d "%~dp0"
start http://localhost:8080/web/
python -m http.server 8080
