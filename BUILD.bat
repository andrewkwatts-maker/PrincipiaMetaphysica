@echo off
REM BUILD.bat - Principia Metaphysica Build Script
REM Regenerates JavaScript constants from config.py
REM
REM Usage: Simply run BUILD.bat after editing config.py

echo ========================================
echo Principia Metaphysica Build Script
echo Framework Version: v6.1
echo ========================================
echo.

echo [1/2] Generating JavaScript constants from config.py...
python generate_js_constants.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: JavaScript generation failed!
    echo Check config.py for syntax errors.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD COMPLETE
echo ========================================
echo.
echo JavaScript constants updated successfully!
echo HTML webpages will now use the new values.
echo.
echo Next steps:
echo   - Open HTML files to see updated values
echo   - Run SimulateTheory.py for CSV analysis (optional)
echo   - Commit changes: git add config.py js/theory-constants.js
echo.

pause
