@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM Principia Metaphysica - Complete Simulation and Firebase Pipeline
REM
REM This script runs the complete pipeline:
REM 1. Clears local cache files
REM 2. Runs all Python simulations (generates theory_output.json)
REM 3. Generates theory-constants-enhanced.js
REM 4. Generates content templates
REM 5. Validates all PM paths in HTML
REM 6. Shows Firebase diff and requires confirmation
REM 7. Syncs to Firebase with version history
REM
REM Usage:
REM   clear-cache-and-run.bat        - Interactive mode (requires confirmation)
REM   clear-cache-and-run.bat --yes  - Auto-confirm all prompts
REM
REM Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo  PRINCIPIA METAPHYSICA - COMPLETE SIMULATION PIPELINE
echo ═══════════════════════════════════════════════════════════════════════════
echo  Timestamp: %date% %time%
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM Check for --yes flag
set "AUTO_CONFIRM="
if "%1"=="--yes" set "AUTO_CONFIRM=--yes"
if "%1"=="-y" set "AUTO_CONFIRM=--yes"

REM Step 1: Clear local simulation cache
echo [1/7] Clearing local cache files...
if exist "theory_output.json.bak" del /f "theory_output.json.bak"
if exist "theory_output.json" (
    copy "theory_output.json" "theory_output.json.bak" >nul
    echo       Backed up theory_output.json
)
if exist "__pycache__" rd /s /q "__pycache__"
if exist "simulations\__pycache__" rd /s /q "simulations\__pycache__"
if exist "content-templates" rd /s /q "content-templates"
echo       Cache cleared.
echo.

REM Step 2: Run simulations
echo [2/7] Running all simulations...
python run_all_simulations.py
if errorlevel 1 (
    echo       ERROR: Simulation failed!
    pause
    exit /b 1
)
echo       Simulations complete.
echo.

REM Verify theory_output.json was created
if not exist "theory_output.json" (
    echo       ERROR: theory_output.json was not created!
    pause
    exit /b 1
)

REM Step 3: Generate enhanced constants
echo [3/7] Generating theory-constants-enhanced.js...
python -c "import json; f=open('theory_output.json'); d=json.load(f); f.close(); print('const PM = ' + json.dumps(d, indent=2) + ';'); print('if (typeof module !== \"undefined\") module.exports = PM;')" > theory-constants-enhanced.js.new
if exist "theory-constants-enhanced.js.new" (
    move /y "theory-constants-enhanced.js.new" "theory-constants-enhanced.js" >nul
    echo       Generated theory-constants-enhanced.js
) else (
    echo       ERROR: Failed to generate theory-constants-enhanced.js
)
echo.

REM Step 4: Generate content templates
echo [4/7] Generating content templates...
if exist "scripts\master-pipeline.js" (
    node scripts\master-pipeline.js generate --force
    if errorlevel 1 (
        echo       WARNING: Template generation had issues
    ) else (
        echo       Content templates generated successfully.
    )
) else (
    echo       master-pipeline.js not found, creating templates manually...
    if not exist "content-templates" mkdir "content-templates"
)
echo.

REM Step 5: Validate PM paths
echo [5/7] Validating PM paths...
if exist "scripts\validate-pm-paths.js" (
    node scripts\validate-pm-paths.js
    if errorlevel 1 (
        echo       WARNING: Some PM paths are missing!
        echo       Review the output above before continuing.
        if not defined AUTO_CONFIRM (
            set /p "CONTINUE=Continue anyway? [y/N]: "
            if /i not "!CONTINUE!"=="y" (
                echo       Aborted by user.
                pause
                exit /b 1
            )
        )
    ) else (
        echo       All PM paths validated successfully.
    )
) else (
    echo       validate-pm-paths.js not found, skipping validation.
)
echo.

REM Step 6: Show Firebase diff and require confirmation
echo [6/7] Checking Firebase diff...
echo ───────────────────────────────────────────────────────────────────────────
if exist "scripts\firebase-sync-with-history.js" (
    REM The sync script will show diff and ask for confirmation
    node scripts\firebase-sync-with-history.js %AUTO_CONFIRM%
    if errorlevel 1 (
        echo       Firebase sync was cancelled or failed.
        echo       No changes were made to Firebase.
    ) else (
        echo       Firebase sync complete with version history.
    )
) else (
    echo       firebase-sync-with-history.js not found, skipping sync.
)
echo.

REM Step 7: Summary and browser cache reminder
echo [7/7] Final Summary
echo ───────────────────────────────────────────────────────────────────────────
echo.
echo   Files Updated:
if exist "theory_output.json" (
    for %%I in (theory_output.json) do echo       - theory_output.json (%%~zI bytes^)
)
if exist "theory-constants-enhanced.js" (
    for %%I in (theory-constants-enhanced.js) do echo       - theory-constants-enhanced.js (%%~zI bytes^)
)
if exist "firebase-sync-report.json" (
    echo       - firebase-sync-report.json (sync report^)
)
echo.
echo   Browser Cache:
echo       To see latest data, clear browser cache:
echo       - Press F12 ^> Application ^> Clear site data
echo       - Or run: localStorage.clear()
echo.

echo ═══════════════════════════════════════════════════════════════════════════
echo  PIPELINE COMPLETE
echo ═══════════════════════════════════════════════════════════════════════════
echo.

pause
