@echo off
REM Upload Formula Database to Firebase
REM This script installs dependencies and uploads formulas to Firestore

echo ===============================================================
echo PRINCIPIA METAPHYSICA - UPLOAD FORMULA DATABASE
echo ===============================================================
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Check if serviceAccountKey.json exists
if not exist scripts\serviceAccountKey.json (
    echo ERROR: scripts\serviceAccountKey.json not found
    echo.
    echo Download from Firebase Console:
    echo   1. Go to https://console.firebase.google.com/
    echo   2. Select project: principia-metaphysica
    echo   3. Project Settings ^> Service Accounts
    echo   4. Generate New Private Key
    echo   5. Save as scripts\serviceAccountKey.json
    echo.
    pause
    exit /b 1
)

REM Run the upload script
echo Uploading formulas to Firebase...
echo.
node scripts/upload-formula-database.js %*

if errorlevel 1 (
    echo.
    echo ERROR: Upload failed
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo UPLOAD COMPLETE
echo ===============================================================
pause
