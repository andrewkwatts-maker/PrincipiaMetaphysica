@echo off
echo ============================================================
echo  PRINCIPIA METAPHYSICA - Run All Simulations
echo ============================================================
echo.
echo Running 68 simulations across 8 physics domains...
echo Target: OMEGA = 0 (sterile manifold)
echo.
python run_all_simulations.py %*
echo.
pause
