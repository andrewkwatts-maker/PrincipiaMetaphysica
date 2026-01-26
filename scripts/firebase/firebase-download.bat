@echo off
REM ============================================================
REM Principia Metaphysica - Firebase Database Download
REM ============================================================
REM
REM Downloads all data from Firebase Firestore to local files
REM for viewing and backup.
REM
REM Output: firebase-backup/ folder
REM
REM Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
REM ============================================================

echo.
echo ============================================================
echo  PRINCIPIA METAPHYSICA - FIREBASE DOWNLOAD
echo ============================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if firebase-admin is installed
if not exist "node_modules\firebase-admin" (
    echo Installing firebase-admin...
    call npm install firebase-admin
    echo.
)

REM Check for service account key
if not exist "scripts\serviceAccountKey.json" (
    echo ERROR: scripts\serviceAccountKey.json not found
    echo.
    echo Please download your service account key:
    echo 1. Go to Firebase Console
    echo 2. Project Settings ^> Service Accounts
    echo 3. Generate New Private Key
    echo 4. Save as scripts\serviceAccountKey.json
    echo.
    pause
    exit /b 1
)

REM Run download script
echo Running download...
echo.
node scripts\firebase-download.js

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo  Download complete! Check firebase-backup\ folder
    echo ============================================================
    echo.

    REM Open backup folder
    if exist "firebase-backup" (
        explorer firebase-backup
    )
) else (
    echo.
    echo Download failed. Check errors above.
)

pause
