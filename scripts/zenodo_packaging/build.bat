@echo off
REM ============================================================================
REM BUILD.bat - Principia Metaphysica Build Script
REM ============================================================================
REM
REM Complete build pipeline:
REM   config.py (hand-coded foundations)
REM       ↓
REM   simulations/run_all_simulations.py (compute predictions)
REM       ↓
REM   theory_output.json (simulation results)
REM       ↓
REM   theory-constants.js (website constants)
REM
REM Usage: Simply run BUILD.bat after editing config.py
REM
REM Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
REM ============================================================================

echo ========================================
echo Principia Metaphysica Build Script
echo Framework Version: v6.5
echo ========================================
echo.

REM Step 1: Run all simulations
echo [1/3] Running simulations (proton decay, PMNS, w(z))...
echo   - proton_decay_rg_hybrid.py
echo   - pmns_full_matrix.py
echo   - wz_evolution_desi_dr2.py
echo.
python simulations/run_all_simulations.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Simulation pipeline failed!
    echo Check simulation scripts for errors.
    echo.
    pause
    exit /b 1
)

echo.
echo [1/3] COMPLETE - Simulations finished successfully
echo   Output: theory_output.json
echo   Output: theory-constants.js
echo.

REM Step 2: Verify output files exist
echo [2/3] Verifying generated files...

if not exist theory_output.json (
    echo ERROR: theory_output.json not found!
    pause
    exit /b 1
)

if not exist theory-constants.js (
    echo ERROR: theory-constants.js not found!
    pause
    exit /b 1
)

echo   ✓ theory_output.json
echo   ✓ theory-constants.js
echo.

REM Step 3: Display summary
echo [3/3] Build summary...
echo.

REM Read key values from theory_output.json (if jq available, otherwise skip)
where jq >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Key predictions (from theory_output.json):
    echo.
    for /f "delims=" %%i in ('python -c "import json; f=open('theory_output.json'); d=json.load(f); print(f\"  M_GUT = {d['proton_decay']['M_GUT']:.3e} GeV\")"') do echo %%i
    for /f "delims=" %%i in ('python -c "import json; f=open('theory_output.json'); d=json.load(f); print(f\"  tau_p = {d['proton_decay']['tau_p_median']:.2e} years\")"') do echo %%i
    for /f "delims=" %%i in ('python -c "import json; f=open('theory_output.json'); d=json.load(f); print(f\"  w0 = {d['dark_energy']['w0_PM']:.4f}\")"') do echo %%i
    for /f "delims=" %%i in ('python -c "import json; f=open('theory_output.json'); d=json.load(f); print(f\"  PMNS avg deviation = {d['pmns_matrix']['average_sigma']:.2f}sigma\")"') do echo %%i
    echo.
) else (
    echo   (Install jq for detailed summary, or check theory_output.json manually)
    echo.
)

echo ========================================
echo BUILD COMPLETE ✓
echo ========================================
echo.
echo Generated files:
echo   - theory_output.json      (simulation results)
echo   - theory-constants.js     (website constants)
echo.
echo Single Source of Truth:
echo   config.py → simulations → theory-constants.js → HTML
echo.
echo HTML webpages will now use the updated values automatically.
echo Include in HTML: ^<script src="theory-constants.js"^>^</script^>
echo Access values: PM.proton_decay.tau_p_median, PM.pmns_matrix.theta_23, etc.
echo.
echo Next steps:
echo   1. Review theory_output.json for detailed results
echo   2. Open HTML files to see updated values
echo   3. Commit changes:
echo      git add config.py theory_output.json theory-constants.js
echo      git commit -m "Update theoretical predictions from simulations"
echo.

pause
