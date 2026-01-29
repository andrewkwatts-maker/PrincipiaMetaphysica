@echo off
REM ============================================================
REM Principia Metaphysica - Full Simulation to Firebase Pipeline
REM ============================================================
REM
REM Complete pipeline:
REM 1. Run all simulations
REM 2. Generate theory_output.json
REM 3. Generate theory-constants-enhanced.js
REM 4. Show diff with Firebase
REM 5. Validate OOM constraints
REM 6. Push to Firebase (with confirmation)
REM
REM Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
REM ============================================================

echo.
echo ============================================================
echo  PRINCIPIA METAPHYSICA - FULL PIPELINE
echo ============================================================
echo.
echo This will:
echo   1. Run all simulations
echo   2. Generate updated constants
echo   3. Validate against Firebase
echo   4. Push updates (with your confirmation)
echo.
echo ============================================================
echo.

set /p CONTINUE="Continue? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo Cancelled.
    exit /b 0
)

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js not found
    pause
    exit /b 1
)

REM Install npm dependencies if needed
if not exist "node_modules\firebase-admin" (
    echo Installing Node.js dependencies...
    call npm install firebase-admin cheerio
    echo.
)

REM ============================================================
REM Step 1: Run Simulations
REM ============================================================
echo.
echo ============================================================
echo  STEP 1: Running Simulations
echo ============================================================
echo.

python simulations/run_all_simulations.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Simulations failed
    pause
    exit /b 1
)

echo.
echo Simulations complete!

REM ============================================================
REM Step 2: Generate Enhanced Constants
REM ============================================================
echo.
echo ============================================================
echo  STEP 2: Generating Enhanced Constants
echo ============================================================
echo.

if exist "generate_enhanced_constants.py" (
    python generate_enhanced_constants.py
) else (
    echo Skipping - generate_enhanced_constants.py not found
)

REM ============================================================
REM Step 3: Check Firebase Status
REM ============================================================
echo.
echo ============================================================
echo  STEP 3: Checking Firebase Status
echo ============================================================
echo.

if exist "scripts\serviceAccountKey.json" (
    node scripts\firebase-check-status.js
) else (
    echo WARNING: Firebase not configured
    echo Place serviceAccountKey.json in scripts\ folder to enable sync
    echo.
    echo Simulations complete. Manual Firebase upload required.
    pause
    exit /b 0
)

REM ============================================================
REM Step 4: Show Diff and Validate
REM ============================================================
echo.
echo ============================================================
echo  STEP 4: Validating Changes
echo ============================================================
echo.

node scripts\firebase-diff.js

if %ERRORLEVEL% neq 0 (
    echo.
    echo ============================================================
    echo  WARNING: Validation issues detected
    echo ============================================================
    echo.
    echo Review the issues above carefully.
    echo.
    set /p FORCEPUSH="Push anyway? (y/n): "
    if /i not "%FORCEPUSH%"=="y" (
        echo.
        echo Push cancelled. Review and fix issues before pushing.
        pause
        exit /b 0
    )
)

REM ============================================================
REM Step 5: Push to Firebase
REM ============================================================
echo.
echo ============================================================
echo  STEP 5: Push to Firebase
echo ============================================================
echo.

node scripts\firebase-push-updates.js

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo  PIPELINE COMPLETE!
    echo ============================================================
    echo.
    echo Summary:
    echo   - Simulations: COMPLETE
    echo   - Constants: GENERATED
    echo   - Validation: PASSED
    echo   - Firebase: UPDATED
    echo.
    echo The website will now reflect the latest simulation results.
    echo.
) else (
    echo.
    echo Pipeline completed with errors. Check logs above.
)

pause
