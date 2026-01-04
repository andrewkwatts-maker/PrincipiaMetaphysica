@echo off
REM Script to replace auth-guard.js with enhanced version
REM Location: h:/Github/PrincipiaMetaphysica/replace-auth-guard.bat

echo ========================================
echo Auth-Guard.js Enhancement Replacement
echo ========================================
echo.

REM Check if enhanced version exists
if not exist "js\auth-guard-ENHANCED.js" (
    echo ERROR: Enhanced version not found at js\auth-guard-ENHANCED.js
    echo Please ensure the enhanced file exists before running this script.
    pause
    exit /b 1
)

REM Create backup if not already exists
if not exist "js\auth-guard.js.backup" (
    echo Creating backup: js\auth-guard.js.backup
    copy "js\auth-guard.js" "js\auth-guard.js.backup"
    if errorlevel 1 (
        echo ERROR: Failed to create backup
        pause
        exit /b 1
    )
    echo Backup created successfully
) else (
    echo Backup already exists: js\auth-guard.js.backup
)

echo.
echo Ready to replace auth-guard.js with enhanced version.
echo.
set /p CONFIRM=Are you sure you want to continue? (Y/N):

if /i not "%CONFIRM%"=="Y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo Replacing file...
copy /Y "js\auth-guard-ENHANCED.js" "js\auth-guard.js"
if errorlevel 1 (
    echo ERROR: Failed to replace file
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: auth-guard.js has been updated!
echo ========================================
echo.
echo Changes:
echo  - Firebase data loading enhanced
echo  - PM value population added
echo  - Tooltip system integrated
echo  - Loading states implemented
echo  - Error handling improved
echo.
echo Backup location: js\auth-guard.js.backup
echo.
echo Next steps:
echo  1. Test the updated auth-guard.js
echo  2. Check browser console for proper logging
echo  3. Verify PM values populate after login
echo  4. Verify tooltips work on hover
echo.
pause
