# File Organization Instructions

**Date:** 2025-12-25
**Purpose:** Organize migration reports and clean up temporary files

---

## Quick Start (Automated)

### Option 1: Windows Batch Script
```cmd
organize_migration_files.bat
```

### Option 2: Bash Script (Git Bash on Windows)
```bash
bash organize_migration_files.sh
```

---

## Manual Instructions

If you prefer to move files manually or the scripts don't work, follow these steps:

### 1. Move Migration Reports to reports/ (30 files)

#### Quality Reports
```bash
git mv AI_REFERENCES_REMOVAL_SUMMARY.md reports/
git mv FORMULA_POLISH_REPORT.md reports/
git mv MIGRATION_AUDIT_REPORT.md reports/
git mv MIGRATION_TEMPLATES.md reports/
git mv PARAMETER_CATEGORY_SUMMARY.md reports/
git mv PNEUMA_STABILITY_MATH_REVIEW.md reports/
```

#### Formula Migration Reports
```bash
git mv FORMULA_COMPARISON_SECTIONS_6_7.md reports/
git mv FORMULA_REFERENCES_1-20.md reports/
git mv FORMULA_REFERENCES_F21_F40.md reports/
```

#### Learning Resources Reports
```bash
git mv LEARNING_RESOURCES_FORMULAS_1-27.md reports/
git mv LEARNING_RESOURCES_REPORT.md reports/
```

#### Related Formulas Reports
```bash
git mv RELATED_FORMULAS_COMPLETION_REPORT.md reports/
git mv RELATED_FORMULAS_FINAL_REPORT.md reports/
git mv RELATED_FORMULAS_IMPLEMENTATION.md reports/
```

#### Simulation Mapping Reports
```bash
git mv SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md reports/
git mv FORMULA_SIMULATION_MAPPING_FINAL.md reports/
git mv SIMULATION_LINK_MAPPING_REPORT.md reports/
git mv README_SIMULATION_MAPPING.md reports/
```

#### Section & PM Constants Reports
```bash
git mv SECTION_METADATA_REPORT.md reports/
git mv PM_CONSTANTS_LOADER_V2.1_COMPATIBILITY_REPORT.md reports/
git mv PM_CONSTANTS_LOADER_FIX_SUMMARY.md reports/
```

### 2. Archive Temporary TXT Files (5 files)

```bash
git mv SIMULATION_MAPPING_QUICK_REFERENCE.txt reports/
git mv SIMULATION_MAPPING_CORRECTIONS.txt reports/
git mv RELATED_FORMULAS_SUMMARY.txt reports/
git mv pneuma_stress_energy_formula.txt reports/
git mv extract_missing_related_formulas.txt reports/
```

### 3. Archive One-Off Utility Scripts (10 files)

First create the archive directory:
```bash
mkdir scripts/archive
```

Then move the scripts:
```bash
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
```

### 4. Move Patch File

```bash
git mv fix_gauge_table.patch reports/
```

---

## Verification

After running the script or manual commands, verify the changes:

```bash
# Check what was moved
git status

# Should show files moved from root to reports/ and scripts/archive/
```

Expected output:
```
renamed:    AI_REFERENCES_REMOVAL_SUMMARY.md -> reports/AI_REFERENCES_REMOVAL_SUMMARY.md
renamed:    FORMULA_POLISH_REPORT.md -> reports/FORMULA_POLISH_REPORT.md
... (30+ more renamed files)
```

---

## Commit Changes

Once you've verified the changes:

```bash
# Stage all moved files
git add reports/ scripts/archive/

# Commit with descriptive message
git commit -m "Organize migration reports and archive temporary files

- Moved 30+ migration reports to reports/ directory
- Archived 10+ one-off utility scripts to scripts/archive/
- Moved 5 temporary TXT files to reports/
- Created comprehensive MIGRATION_COMPLETE_SUMMARY.md

This cleanup improves project organization and makes it easier to
find migration documentation."
```

---

## Files Being Organized

### Reports Being Moved (30 files)

**Quality Reports (6):**
- AI_REFERENCES_REMOVAL_SUMMARY.md
- FORMULA_POLISH_REPORT.md
- MIGRATION_AUDIT_REPORT.md
- MIGRATION_TEMPLATES.md
- PARAMETER_CATEGORY_SUMMARY.md
- PNEUMA_STABILITY_MATH_REVIEW.md

**Formula Reports (3):**
- FORMULA_COMPARISON_SECTIONS_6_7.md
- FORMULA_REFERENCES_1-20.md
- FORMULA_REFERENCES_F21_F40.md

**Learning Resources (2):**
- LEARNING_RESOURCES_FORMULAS_1-27.md
- LEARNING_RESOURCES_REPORT.md

**Related Formulas (3):**
- RELATED_FORMULAS_COMPLETION_REPORT.md
- RELATED_FORMULAS_FINAL_REPORT.md
- RELATED_FORMULAS_IMPLEMENTATION.md

**Simulation Mapping (4):**
- SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md
- FORMULA_SIMULATION_MAPPING_FINAL.md
- SIMULATION_LINK_MAPPING_REPORT.md
- README_SIMULATION_MAPPING.md

**Technical (3):**
- SECTION_METADATA_REPORT.md
- PM_CONSTANTS_LOADER_V2.1_COMPATIBILITY_REPORT.md
- PM_CONSTANTS_LOADER_FIX_SUMMARY.md

**TXT Archives (5):**
- SIMULATION_MAPPING_QUICK_REFERENCE.txt
- SIMULATION_MAPPING_CORRECTIONS.txt
- RELATED_FORMULAS_SUMMARY.txt
- pneuma_stress_energy_formula.txt
- extract_missing_related_formulas.txt

**Patch (1):**
- fix_gauge_table.patch

### Scripts Being Archived (10 files)

**One-off Utilities:**
- find_math_errors.py
- fix_math_entities.py
- verify_pneuma_math.py
- verify_superpotential_relation.py
- validate_formula_lookups.py
- update_values.py
- parameter_category_example.py
- test_parameter_category.py
- test_tcs_topology.py
- pneuma_stability_v12_8_CORRECTED.py

---

## Files Staying in Root

These important files should remain in the root directory:

**Core System:**
- config.py (master configuration)
- run_all_simulations.py (export system)
- theory_output.json (generated output)

**Main Papers:**
- principia-metaphysica-paper.html
- references.html

**Active Scripts:**
- Any scripts in scripts/ directory that are actively used

---

## After Organization

Your directory structure will look like:

```
PrincipiaMetaphysica/
├── config.py
├── run_all_simulations.py
├── theory_output.json
├── principia-metaphysica-paper.html
├── references.html
│
├── reports/
│   ├── MIGRATION_COMPLETE_SUMMARY.md (NEW - comprehensive overview)
│   ├── MIGRATION_AUDIT_REPORT.md
│   ├── MIGRATION_TEMPLATES.md
│   ├── AI_REFERENCES_REMOVAL_SUMMARY.md
│   ├── FORMULA_POLISH_REPORT.md
│   ├── PARAMETER_CATEGORY_SUMMARY.md
│   ├── PNEUMA_STABILITY_MATH_REVIEW.md
│   ├── formula_migration_F1.json
│   ├── ... (F2-F8)
│   ├── param_migration_P1.json
│   ├── ... (P2-P8)
│   ├── section_migration_S1.json
│   ├── ... (S2-S8)
│   └── [30+ other migration reports]
│
├── scripts/
│   ├── archive/
│   │   ├── find_math_errors.py
│   │   ├── fix_math_entities.py
│   │   ├── verify_pneuma_math.py
│   │   └── [7+ other one-off scripts]
│   └── [active scripts remain here]
│
└── [other directories unchanged]
```

---

## Benefits of This Organization

✅ **Cleaner Root Directory** - Only active files at top level
✅ **Organized Reports** - All migration documentation in one place
✅ **Archived Scripts** - One-off utilities preserved but out of the way
✅ **Git History Preserved** - Using `git mv` maintains file history
✅ **Easy Navigation** - Clear separation of concerns
✅ **Professional Structure** - Ready for public repository

---

## Troubleshooting

### If a file doesn't exist
Some files may already have been moved or deleted. The scripts use `2>nul` (Windows) or `2>/dev/null` (Bash) to suppress errors for missing files.

### If git mv fails
If you get permission errors, you can:
1. Close any programs that might have the files open
2. Use regular `mv` command, then `git add` the changes
3. Or move files manually in File Explorer, then run `git add reports/ scripts/archive/`

### If you want to undo
Before committing, you can undo with:
```bash
git reset --hard HEAD
```

After committing, you can revert with:
```bash
git revert HEAD
```

---

## Questions?

See **reports/MIGRATION_COMPLETE_SUMMARY.md** for:
- Complete migration overview
- What was accomplished
- What remains to be done
- Timeline estimates
- Technical details

---

**Created:** 2025-12-25
**Author:** Andrew Keith Watts
**Project:** Principia Metaphysica v13.0
