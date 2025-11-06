@echo off
echo ========================================
echo   Smart Campus Connect - DEMO MODE
echo ========================================
echo.
echo Starting Backend Server...
echo.
cd src\backend
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload"
timeout /t 3 >nul
echo.
echo Starting Frontend Server...
echo.
cd ..\frontend
start "Frontend Server" cmd /k "npm run dev"
echo.
echo ========================================
echo   Servers Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo DEMO CREDENTIALS:
echo   Admin:   admin@demo.com / admin123
echo   Teacher: teacher@demo.com / admin123
echo   Student: student@demo.com / admin123
echo.
echo Press any key to close this window...
pause >nul
