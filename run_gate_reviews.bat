@echo off
echo ============================================================
echo  PRINCIPIA METAPHYSICA - Gate/Certificate Review Orchestrator
echo ============================================================
echo.
echo  This script cycles through all 70+ gates and certificates,
echo  reviewing one every 39 minutes using Claude Code.
echo.
echo  Branch: GateCertReviews (never touches main)
echo  Estimated runtime: ~45 hours for full cycle
echo.
echo  Press Ctrl+C at any time to stop. Progress is saved.
echo.
echo  Options:
echo    --list           List all gates in the queue
echo    --dry-run        Generate prompts without invoking Claude
echo    --single C001-B3 Review a single gate
echo    --start-at N     Resume from gate index N
echo    --interval M     Minutes between reviews (default 39)
echo.
echo ============================================================
echo.

REM Check that Claude CLI is available
where claude >nul 2>nul
if errorlevel 1 (
    echo ERROR: 'claude' CLI not found in PATH!
    echo Install: npm install -g @anthropic-ai/claude-code
    pause
    exit /b 1
)

REM Check Python
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: 'python' not found in PATH!
    pause
    exit /b 1
)

REM Run the orchestrator with all passed arguments
python scripts\gate_review_orchestrator.py %*

echo.
echo ============================================================
echo  Gate review session complete.
echo  Check scripts\gate_review_logs\ for all prompts and responses.
echo ============================================================
pause
