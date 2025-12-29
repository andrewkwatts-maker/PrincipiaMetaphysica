@echo off
REM Start local web server for testing Principia Metaphysica
REM Copyright (c) 2025 Andrew Keith Watts

echo ========================================
echo Principia Metaphysica - Local Server
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.x
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Starting local web server on port 8000...
echo.
echo Open your browser to:
echo   - Main site: http://localhost:8000/
echo   - References: http://localhost:8000/Pages/references.html
echo   - Test page: http://localhost:8000/test_references_page.html
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8000
