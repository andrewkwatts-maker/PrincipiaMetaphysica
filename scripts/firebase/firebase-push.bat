@echo off
REM ============================================================
REM Principia Metaphysica - Firebase Push Updates
REM ============================================================
REM
REM Validates and pushes simulation updates to Firebase.
REM
REM BEFORE RUNNING:
REM 1. Run simulations: python simulations/run_all_simulations.py
REM 2. Review theory_output.json
REM
REM This script will:
REM - Show diff between local and remote
REM - Validate all OOM values are within 1 OOM tolerance
REM - Confirm values are better than or equal to previous
REM - Ask for confirmation before pushing
REM
REM Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
REM ============================================================

echo.
echo ============================================================
echo  PRINCIPIA METAPHYSICA - FIREBASE PUSH UPDATES
echo ============================================================
echo.

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js not found
    pause
    exit /b 1
)

REM Check dependencies
if not exist "node_modules\firebase-admin" (
    echo Installing dependencies...
    call npm install firebase-admin
    echo.
)

REM Check for service account
if not exist "scripts\serviceAccountKey.json" (
    echo ERROR: scripts\serviceAccountKey.json not found
    echo Download from Firebase Console ^> Service Accounts
    pause
    exit /b 1
)

REM Check for theory_output.json
if not exist "theory_output.json" (
    echo ERROR: theory_output.json not found
    echo.
    echo Run simulations first:
    echo   python simulations/run_all_simulations.py
    echo.
    pause
    exit /b 1
)

REM First show diff
echo Step 1: Analyzing changes...
echo.
node scripts\firebase-diff.js

if %ERRORLEVEL% neq 0 (
    echo.
    echo ============================================================
    echo  WARNING: Some validations failed
    echo ============================================================
    echo.
    echo Review the issues above before pushing.
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" (
        echo Push cancelled.
        pause
        exit /b 0
    )
)

REM Push updates
echo.
echo Step 2: Pushing updates...
echo.
node scripts\firebase-push-updates.js

pause
