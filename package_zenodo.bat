@echo off
echo ============================================================
echo  PRINCIPIA METAPHYSICA - Package for Zenodo Submission
echo ============================================================
echo.
echo Step 1: Running all simulations to ensure fresh output...
python simulations/run_all_simulations.py --quiet
if errorlevel 1 (
    echo ERROR: Simulations failed. Fix issues before packaging.
    pause
    exit /b 1
)
echo.
echo Step 2: Creating Zenodo submission package...
python scripts\packaging\zenodo_pack.py %*
echo.
echo Done. Check zenodo_package/ for the output.
pause
