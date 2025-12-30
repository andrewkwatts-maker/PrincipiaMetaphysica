@echo off
REM Start local web server for testing Principia Metaphysica
REM Copyright (c) 2025 Andrew Keith Watts
REM
REM This script starts a local web server with CORS headers enabled,
REM allowing the HTML pages to load JSON data files properly.

echo ============================================================
echo   PRINCIPIA METAPHYSICA - Local Server
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.x
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Starting local web server with CORS support...
echo.
echo The website will open automatically in your browser.
echo Press Ctrl+C to stop the server.
echo.

python serve.py
