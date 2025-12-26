@echo off
REM Principia Metaphysica File Organization Script (Windows)
REM Date: 2025-12-25
REM Purpose: Move migration reports to reports/ directory and clean up temporary files

cd /d "h:\Github\PrincipiaMetaphysica"

echo === Moving Migration Reports to reports/ directory ===

REM Quality Reports (completed work)
git mv AI_REFERENCES_REMOVAL_SUMMARY.md reports\ 2>nul
git mv FORMULA_POLISH_REPORT.md reports\ 2>nul
git mv MIGRATION_AUDIT_REPORT.md reports\ 2>nul
git mv MIGRATION_TEMPLATES.md reports\ 2>nul
git mv PARAMETER_CATEGORY_SUMMARY.md reports\ 2>nul
git mv PNEUMA_STABILITY_MATH_REVIEW.md reports\ 2>nul

REM Formula-related migration reports
git mv FORMULA_COMPARISON_SECTIONS_6_7.md reports\ 2>nul
git mv FORMULA_REFERENCES_1-20.md reports\ 2>nul
git mv FORMULA_REFERENCES_F21_F40.md reports\ 2>nul

REM Learning resources reports (partial progress)
git mv LEARNING_RESOURCES_FORMULAS_1-27.md reports\ 2>nul
git mv LEARNING_RESOURCES_REPORT.md reports\ 2>nul

REM Related formulas reports
git mv RELATED_FORMULAS_COMPLETION_REPORT.md reports\ 2>nul
git mv RELATED_FORMULAS_FINAL_REPORT.md reports\ 2>nul
git mv RELATED_FORMULAS_IMPLEMENTATION.md reports\ 2>nul

REM Simulation mapping reports
git mv SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md reports\ 2>nul
git mv FORMULA_SIMULATION_MAPPING_FINAL.md reports\ 2>nul
git mv SIMULATION_LINK_MAPPING_REPORT.md reports\ 2>nul
git mv README_SIMULATION_MAPPING.md reports\ 2>nul

REM Section metadata reports
git mv SECTION_METADATA_REPORT.md reports\ 2>nul

REM PM Constants loader reports
git mv PM_CONSTANTS_LOADER_V2.1_COMPATIBILITY_REPORT.md reports\ 2>nul
git mv PM_CONSTANTS_LOADER_FIX_SUMMARY.md reports\ 2>nul

echo === Moving temporary TXT files to reports/ archive ===

REM Quick reference files (can be archived)
git mv SIMULATION_MAPPING_QUICK_REFERENCE.txt reports\ 2>nul
git mv SIMULATION_MAPPING_CORRECTIONS.txt reports\ 2>nul
git mv RELATED_FORMULAS_SUMMARY.txt reports\ 2>nul
git mv pneuma_stress_energy_formula.txt reports\ 2>nul
git mv extract_missing_related_formulas.txt reports\ 2>nul

echo === Creating archive directory for one-off scripts ===

if not exist scripts\archive mkdir scripts\archive

REM Move one-off utility scripts to archive
git mv find_math_errors.py scripts\archive\ 2>nul
git mv fix_math_entities.py scripts\archive\ 2>nul
git mv verify_pneuma_math.py scripts\archive\ 2>nul
git mv verify_superpotential_relation.py scripts\archive\ 2>nul
git mv validate_formula_lookups.py scripts\archive\ 2>nul
git mv update_values.py scripts\archive\ 2>nul
git mv parameter_category_example.py scripts\archive\ 2>nul
git mv test_parameter_category.py scripts\archive\ 2>nul
git mv test_tcs_topology.py scripts\archive\ 2>nul
git mv pneuma_stability_v12_8_CORRECTED.py scripts\archive\ 2>nul

REM Move patch file to reports
git mv fix_gauge_table.patch reports\ 2>nul

echo.
echo === File Organization Complete ===
echo.
echo Summary:
echo - Moved 30+ migration reports to reports/ directory
echo - Archived 10+ one-off utility scripts to scripts\archive\
echo - Moved 5 temporary TXT files to reports/
echo.
echo Next steps:
echo 1. Review moved files to ensure correctness
echo 2. Run: git status
echo 3. Run: git add reports/ scripts/archive/
echo 4. Commit changes: git commit -m "Organize migration reports and archive temporary files"
echo.
pause
