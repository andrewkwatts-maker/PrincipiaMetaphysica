# Root Directory Structure

**Clean as of:** December 3, 2025
**Goal:** Minimal root with only simulation/config/docs essentials

---

## Root Directory Files

### Core System (4 files)
- **config.py** - Single source of truth for all parameters
- **run_all_simulations.py** - Orchestrates all simulations
- **generate_enhanced_constants.py** - Generates theory-constants-enhanced.js
- **validate_pm_values.py** - Validates PM.* references in HTML

### Documentation (11 files)
- **README.md** - Project overview
- **ARCHITECTURE.md** - System architecture
- **CONFIG_README.md** - Configuration documentation
- **BUILD_README.md** - Build instructions
- **SimulateTheory_README.md** - Simulation pipeline
- **ENHANCED_CONSTANTS_README.md** - Constants system
- **SINGLE_SOURCE_OF_TRUTH.md** - Validation report
- **V7_PUBLICATION_SUMMARY.md** - v7.0 summary
- **VALIDATION_COMPLETE.md** - Final validation report
- **CLEANUP_SUMMARY.md** - Cleanup documentation
- **ROOT_STRUCTURE.md** - This file

### Website Entry Points (5 files)
- **index.html** - Homepage
- **principia-metaphysica-paper.html** - Main paper
- **beginners-guide.html** - Beginner's guide
- **references.html** - References page
- **philosophical-implications.html** - Philosophy section
- **visualization-index.html** - Visualizations

### Build & Data (2 files)
- **build.bat** - Build script
- **theory_output.json** - Simulation results
- **CNAME** - GitHub Pages domain

---

## Subdirectories

### simulations/
Simulation modules that compute theoretical values:
- proton_decay_rg_hybrid.py
- pmns_full_matrix.py
- wz_evolution_desi_dr2.py
- gauge_unification_merged.py
- asymptotic_safety_gauge.py
- threshold_corrections.py

### utils/
Utility scripts:
- plot_wz_evolution.py
- validation_modules.py

### sections/
Website section pages (cosmology, fermion-sector, etc.)

### foundations/
Educational foundation pages (physics concepts)

### diagrams/
Theory diagrams and visualizations

### components/
Reusable HTML components

### css/
Stylesheets (pm-tooltip.css, styles.css, etc.)

### js/
JavaScript (pm-tooltip-system.js, etc.)

### theory-constants-enhanced.js
Enhanced constants with metadata (20KB)

### analysis/
Analysis results and plots:
- plots/ - PNG visualizations (7 files: wz_evolution, RG flows, KK spectrum, etc.)

### docs/
Documentation pages:
- PAPER_2T_UPDATE_SECTION.html
- computational-appendices.html
- beginners-guide-printable.html

### tests/
Test pages:
- test-tooltip-system.html

### scripts/
Build and utility scripts

### images/
Static images

---

## Files Removed (Clean Sweep)

### Old Parameter Files (7 files)
✗ theory_parameters_v6.1.csv
✗ theory_parameters_v6.4.csv
✗ theory_parameters_v6.5.csv
✗ extra_dim_tuning_grid.csv
✗ magic_number_fix_instructions.json
✗ v65_cleanup_tasks.json
✗ Alpha4,5 Definitions.txt

### Old Rumination Folders (57 files deleted)
✗ abstract-resolutions/ - 28 MD files (theoretical explorations, CY4 constructions, w0 derivations)
✗ peer-reviews/ - 5 MD files (fresh-* review documents)
✗ solutions/ - 23 MD files + 1 HTML file (old resolution attempts)
✗ analysis/*.md - 6 MD files (kept analysis/plots/ with PNGs)

### Moved to Subfolders
- PNG files → analysis/plots/
- Simulation scripts → simulations/
- Utility scripts → utils/
- Test pages → tests/
- Documentation → docs/
- Styles → css/

---

## Import Structure

### run_all_simulations.py
```python
import config  # From root
from simulations.proton_decay_rg_hybrid import run_proton_decay_calculation
from simulations.pmns_full_matrix import run_pmns_calculation
from simulations.wz_evolution_desi_dr2 import run_wz_analysis
```

### generate_enhanced_constants.py
```python
import config  # From root
# Reads theory_output.json from root
# Generates theory-constants-enhanced.js in root
```

### validate_pm_values.py
```python
# Standalone validator
# Reads theory-constants-enhanced.js from root
# Scans all HTML files
```

---

## Workflow

### 1. Update Parameters
```bash
vim config.py
```

### 2. Run Simulations
```bash
python run_all_simulations.py
# Outputs: theory_output.json
```

### 3. Generate Enhanced Constants
```bash
python generate_enhanced_constants.py
# Outputs: theory-constants-enhanced.js (20KB)
```

### 4. Validate
```bash
python validate_pm_values.py
# Validates all 198 PM.* references
```

### 5. Build Website
```bash
build.bat
# Processes all HTML files
```

---

## Benefits of Clean Root

✅ **Clear purpose** - Every root file has active role
✅ **Easy navigation** - Core files immediately visible
✅ **No clutter** - No old versions or temporary files
✅ **Organized** - Related files in subfolders
✅ **Maintainable** - Clear structure for future updates

---

## Maintenance Guidelines

### Keep in Root
- Core system files (config, orchestrator, generator, validator)
- Essential documentation (README, architecture, etc.)
- Main website entry points (index, paper, guide)
- Build artifacts (theory_output.json, theory-constants-enhanced.js)

### Move to Subfolders
- Simulation modules → simulations/
- Utilities → utils/
- Test pages → tests/
- Analysis results → analysis/
- Documentation pages → docs/
- Styles → css/
- Scripts → js/
- Images → images/ or diagrams/

### Delete Immediately
- Old version files (v6.x)
- Temporary files (.log, .tmp)
- Deprecated scripts
- Duplicate documentation

---

**Copyright (c) 2025 Andrew Keith Watts. All rights reserved.**
