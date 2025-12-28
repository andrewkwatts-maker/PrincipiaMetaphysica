@echo off
REM ============================================================
REM Principia Metaphysica - Firebase Status Check
REM ============================================================
REM
REM Checks sync status between local files and Firebase.
REM Shows what needs to be uploaded or downloaded.
REM
REM Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
REM ============================================================

echo.
echo ============================================================
echo  PRINCIPIA METAPHYSICA - FIREBASE STATUS
echo ============================================================
echo.

where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js not found
    pause
    exit /b 1
)

if not exist "node_modules\firebase-admin" (
    echo Installing dependencies...
    call npm install firebase-admin cheerio
    echo.
)

node scripts\firebase-check-status.js

pause
