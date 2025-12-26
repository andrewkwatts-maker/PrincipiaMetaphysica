# File Organization Summary

**Date:** 2025-12-25
**Purpose:** Organize migration reports and archive temporary files

## Overview

This document summarizes the file organization that will be performed by running the `ORGANIZE_FILES_COMMANDS.bat` script.

---

## Files to Move to `reports/` (30+ Markdown Files)

### Quality & Audit Reports (6 files)
- `AI_REFERENCES_REMOVAL_SUMMARY.md`
- `FORMULA_POLISH_REPORT.md`
- `MIGRATION_AUDIT_REPORT.md`
- `MIGRATION_TEMPLATES.md`
- `PARAMETER_CATEGORY_SUMMARY.md`
- `PNEUMA_STABILITY_MATH_REVIEW.md`

### Formula-Related Reports (5 files)
- `FORMULA_COMPARISON_SECTIONS_6_7.md`
- `FORMULA_REFERENCES_1-20.md`
- `FORMULA_REFERENCES_F21_F40.md`
- `FORMULA_SIMULATION_MAPPING_FINAL.md`
- `FORMULA_REFERENCES_ADDED_SUMMARY.md`

### Learning Resources Reports (5 files)
- `LEARNING_RESOURCES_FORMULAS_1-27.md`
- `LEARNING_RESOURCES_REPORT.md`
- `LEARNING_RESOURCES_ADDITIONS.md`
- `LEARNING_RESOURCES_UPDATE_SUMMARY.md`
- `LEARNING_RESOURCES_VERIFICATION.md`

### Related Formulas Reports (3 files)
- `RELATED_FORMULAS_COMPLETION_REPORT.md`
- `RELATED_FORMULAS_FINAL_REPORT.md`
- `RELATED_FORMULAS_IMPLEMENTATION.md`

### Simulation Mapping Reports (5 files)
- `SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md`
- `SIMULATION_LINK_MAPPING_REPORT.md`
- `README_SIMULATION_MAPPING.md`
- `SIMULATION_FILE_UPDATE_STATUS.md`
- `SIMULATION_FILE_ASSIGNMENT_GUIDE.md`

### Section Metadata Reports (1 file)
- `SECTION_METADATA_REPORT.md`

### PM Constants Loader Reports (2 files)
- `PM_CONSTANTS_LOADER_V2.1_COMPATIBILITY_REPORT.md`
- `PM_CONSTANTS_LOADER_FIX_SUMMARY.md`

### Temporary TXT Files (5 files)
- `pneuma_stress_energy_formula.txt`
- `extract_missing_related_formulas.txt`
- `SIMULATION_MAPPING_QUICK_REFERENCE.txt`
- `SIMULATION_MAPPING_CORRECTIONS.txt`
- `RELATED_FORMULAS_SUMMARY.txt`

### Patch Files (1 file)
- `fix_gauge_table.patch`

---

## Files to Move to `scripts/archive/` (16 Python Files)

### Math & Validation Scripts (4 files)
- `find_math_errors.py`
- `fix_math_entities.py`
- `verify_pneuma_math.py`
- `verify_superpotential_relation.py`

### Formula & Binding Validation Scripts (3 files)
- `validate_formula_lookups.py`
- `validate_pm_bindings.py`
- `validate_bindings_final.py`

### Update & Category Scripts (2 files)
- `update_values.py`
- `parameter_category_example.py`

### Test Scripts (2 files)
- `test_parameter_category.py`
- `test_tcs_topology.py`

### Simulation Scripts (1 file)
- `pneuma_stability_v12_8_CORRECTED.py`

### Mojibake & Encoding Fix Scripts (3 files)
- `fix_mojibake_comprehensive.py`
- `fix_emdash.py`
- `fix_appendix_p.py`

### Missing Sections Script (1 file)
- `find_missing_sections.py`

---

## Directory Structure Created

```
scripts/
  └── archive/      (created if doesn't exist)
```

---

## How to Run

### Option 1: Run the Batch Script
```cmd
cd h:\Github\PrincipiaMetaphysica
ORGANIZE_FILES_COMMANDS.bat
```

### Option 2: Run Individual Commands
If you prefer to run commands individually or the batch script has issues, use the commands listed in `ORGANIZE_FILES_COMMANDS.bat`.

---

## Post-Organization Steps

1. **Verify the moves:**
   ```cmd
   git status
   ```

2. **Check that files are in the correct locations:**
   ```cmd
   dir reports\*.md
   dir scripts\archive\*.py
   ```

3. **Commit the changes:**
   ```cmd
   git commit -m "Organize migration reports and archive temporary files"
   ```

---

## Notes

- All moves use `git mv` to preserve file history
- No files are deleted, only moved
- The script is idempotent - you can run it multiple times safely (already moved files will just show errors but won't break anything)
- Files already in the reports/ directory are not affected
