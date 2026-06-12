@echo off
REM Principia Metaphysica output-repo build script.
REM
REM This repository is an auto-generated artifact of the `metaphysica` PyPI
REM library. Every file outside the SOURCE list (README, LICENSE, CNAME,
REM _redirects, .gitignore, .gitattributes, CLAUDE.md, build.bat) is
REM regenerated on every build and your manual edits to those generated
REM files WILL be lost.
REM
REM To rebuild the static site:
REM     build.bat
REM
REM To rebuild without re-running simulations (faster — useful if you
REM only touched the templates):
REM     build.bat --skip-sims
REM
REM To rebuild without plot regeneration (fastest):
REM     build.bat --fast

setlocal
pushd "%~dp0"

echo Installing/upgrading metaphysica...
python -m pip install -U metaphysica[full] || goto :error

echo Running metaphysica.build into %CD% ...
python -c "import metaphysica; raise SystemExit(metaphysica.build(out_dir='.'))" %* || goto :error

echo.
echo Build complete. Open index.html or run:
echo     python -m metaphysica.website.serve --root .
goto :eof

:error
echo Build FAILED. See errors above.
popd
exit /b 1
