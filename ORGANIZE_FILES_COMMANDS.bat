@echo off
REM === File Organization Commands ===
REM Generated: 2025-12-25
REM Run this script to organize all migration files

cd /d "h:\Github\PrincipiaMetaphysica"

echo.
echo === Creating archive directory ===
if not exist scripts\archive mkdir scripts\archive

echo.
echo === Moving Migration Reports (MD files) to reports/ ===

REM Quality Reports
git mv AI_REFERENCES_REMOVAL_SUMMARY.md reports/
git mv FORMULA_POLISH_REPORT.md reports/
git mv MIGRATION_AUDIT_REPORT.md reports/
git mv MIGRATION_TEMPLATES.md reports/
git mv PARAMETER_CATEGORY_SUMMARY.md reports/
git mv PNEUMA_STABILITY_MATH_REVIEW.md reports/

REM Formula-related migration reports
git mv FORMULA_COMPARISON_SECTIONS_6_7.md reports/
git mv FORMULA_REFERENCES_1-20.md reports/
git mv FORMULA_REFERENCES_F21_F40.md reports/
git mv FORMULA_SIMULATION_MAPPING_FINAL.md reports/
git mv FORMULA_REFERENCES_ADDED_SUMMARY.md reports/

REM Learning resources reports
git mv LEARNING_RESOURCES_FORMULAS_1-27.md reports/
git mv LEARNING_RESOURCES_REPORT.md reports/
git mv LEARNING_RESOURCES_ADDITIONS.md reports/
git mv LEARNING_RESOURCES_UPDATE_SUMMARY.md reports/
git mv LEARNING_RESOURCES_VERIFICATION.md reports/

REM Related formulas reports
git mv RELATED_FORMULAS_COMPLETION_REPORT.md reports/
git mv RELATED_FORMULAS_FINAL_REPORT.md reports/
git mv RELATED_FORMULAS_IMPLEMENTATION.md reports/

REM Simulation mapping reports
git mv SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md reports/
git mv SIMULATION_LINK_MAPPING_REPORT.md reports/
git mv README_SIMULATION_MAPPING.md reports/
git mv SIMULATION_FILE_UPDATE_STATUS.md reports/
git mv SIMULATION_FILE_ASSIGNMENT_GUIDE.md reports/

REM Section metadata reports
git mv SECTION_METADATA_REPORT.md reports/

REM PM Constants loader reports
git mv PM_CONSTANTS_LOADER_V2.1_COMPATIBILITY_REPORT.md reports/
git mv PM_CONSTANTS_LOADER_FIX_SUMMARY.md reports/

echo.
echo === Moving temporary TXT files to reports/ ===

git mv pneuma_stress_energy_formula.txt reports/
git mv extract_missing_related_formulas.txt reports/
git mv SIMULATION_MAPPING_QUICK_REFERENCE.txt reports/
git mv SIMULATION_MAPPING_CORRECTIONS.txt reports/
git mv RELATED_FORMULAS_SUMMARY.txt reports/

echo.
echo === Moving one-off scripts to scripts/archive/ ===

REM Utility scripts
git mv find_math_errors.py scripts/archive/
git mv fix_math_entities.py scripts/archive/
git mv verify_pneuma_math.py scripts/archive/
git mv verify_superpotential_relation.py scripts/archive/
git mv validate_formula_lookups.py scripts/archive/
git mv update_values.py scripts/archive/
git mv parameter_category_example.py scripts/archive/
git mv test_parameter_category.py scripts/archive/
git mv test_tcs_topology.py scripts/archive/
git mv pneuma_stability_v12_8_CORRECTED.py scripts/archive/

REM Additional utility scripts found
git mv find_missing_sections.py scripts/archive/
git mv validate_pm_bindings.py scripts/archive/
git mv validate_bindings_final.py scripts/archive/
git mv fix_mojibake_comprehensive.py scripts/archive/
git mv fix_emdash.py scripts/archive/
git mv fix_appendix_p.py scripts/archive/

REM Move patch file to reports
git mv fix_gauge_table.patch reports/

echo.
echo === File Organization Complete ===
echo.
echo Files moved:
echo   - 30+ migration reports to reports/
echo   - 5 temporary TXT files to reports/
echo   - 16 one-off utility scripts to scripts/archive/
echo   - 1 patch file to reports/
echo.
echo Next steps:
echo   1. Review moved files: git status
echo   2. Verify everything looks correct
echo   3. Commit changes: git commit -m "Organize migration reports and archive temporary files"
echo.
pause
