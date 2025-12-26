# Simulation File Mapping - Complete Documentation Index

**Project**: Principia Metaphysica - Formula Simulation Link Completion
**Date**: December 25, 2025
**Status**: Analysis Complete, Ready for Implementation

---

## Quick Start

### What Was Done
Complete analysis and mapping of all 55 formulas in `config.py` to their corresponding simulation validation files. Identified 36 formulas missing simulation links and 6 with incorrect paths.

### What You Need
1. Read the **Executive Summary** for overview
2. Use the **Final Mapping** for implementation
3. Reference the **CSV file** for programmatic updates

---

## Documentation Files

### 1. Executive Summary (START HERE)
**File**: `SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md`
**Purpose**: High-level overview, outcomes, next steps
**Audience**: Project leads, stakeholders
**Contents**:
- Current state and problem definition
- Solution overview and deliverables
- Key findings and corrections needed
- Implementation guide and priorities
- Success criteria and metrics

### 2. Final Mapping (IMPLEMENTATION GUIDE)
**File**: `FORMULA_SIMULATION_MAPPING_FINAL.md`
**Purpose**: Complete formula → simulation mapping with full details
**Audience**: Developers implementing changes
**Contents**:
- All 55 formulas organized by category
- Simulation file assignments (NEW, UPDATE, ASSIGNED)
- Justifications for each mapping
- File existence corrections
- Implementation checklist

### 3. Detailed Report (REFERENCE)
**File**: `SIMULATION_LINK_MAPPING_REPORT.md`
**Purpose**: In-depth analysis and supporting information
**Audience**: Technical reviewers, documentation
**Contents**:
- Formulas WITH simulation files (19)
- Formulas WITHOUT simulation files (36)
- All available simulation files (82+)
- Proposed mappings with justifications
- Next steps and verification plan

### 4. Quick Reference (LOOKUP)
**File**: `SIMULATION_MAPPING_QUICK_REFERENCE.txt`
**Purpose**: Fast lookup by category, priority-based
**Audience**: Developers during implementation
**Contents**:
- Formulas grouped by physics category
- Priority classifications (HIGH, MEDIUM, LOW)
- File validation checklist
- Implementation priority list
- Quick action items

### 5. Corrections List (CRITICAL FIXES)
**File**: `SIMULATION_MAPPING_CORRECTIONS.txt`
**Purpose**: File name corrections and verified mappings
**Audience**: Developers fixing existing assignments
**Contents**:
- Incorrect → Correct file name mappings
- Files that don't exist and alternatives
- Updated assignments (6 formulas)
- Copy-paste ready corrected paths
- Items marked for update

### 6. CSV Mapping (PROGRAMMATIC)
**File**: `formula_simulation_mapping.csv`
**Purpose**: Machine-readable mapping for automated updates
**Audience**: Scripts, automation tools
**Format**:
```csv
formula_name,formula_id,simulation_file,status,action
DARK_ENERGY_W0,dark-energy-w0,simulations/wz_evolution_desi_dr2.py,NEW,ADD
```
**Columns**:
- `formula_name`: Variable name in config.py
- `formula_id`: Formula ID string
- `simulation_file`: Full path to simulation
- `status`: NEW | UPDATE | ASSIGNED
- `action`: ADD | CHANGE_FROM:old_path | NO_CHANGE

---

## File Selection Guide

### For Quick Implementation
→ Use **CSV file** + **Quick Reference**
- CSV provides machine-readable list
- Quick Reference shows priorities

### For Understanding Rationale
→ Read **Final Mapping** + **Executive Summary**
- Final Mapping explains each choice
- Executive Summary provides context

### For Verification
→ Check **Corrections List** + **Detailed Report**
- Corrections shows what's wrong now
- Detailed Report lists all available files

### For Complete Reference
→ Read all files in order:
1. Executive Summary (overview)
2. Final Mapping (details)
3. Corrections List (fixes needed)
4. CSV (data)

---

## Key Statistics

### Coverage
- **Before**: 19/55 formulas (35%)
- **After**: 55/55 formulas (100%)
- **Improvement**: +36 formulas (+188%)

### Actions Required
- **NEW assignments**: 36 formulas
- **UPDATE corrections**: 6 formulas
- **NO CHANGE**: 19 formulas
- **Total changes**: 42 lines in config.py

### File Corrections
- `thermal_time_cosmology_v13_8.py` → `thermal_time_v12_8.py`
- `gw_dispersion_v14_2.py` → `gw_dispersion_v12_8.py`
- `gauge_coupling_running_v14_3.py` → `gauge_unification_precision_v12_4.py`
- `clifford_algebra_spinor_v14_0.py` → `g2_spinor_geometry_validation_v13_0.py`

---

## Implementation Workflow

### Step 1: Preparation
```bash
cd h:\Github\PrincipiaMetaphysica
git status  # Ensure clean working directory
git checkout -b simulation-link-completion
```

### Step 2: Read Documentation
1. Open `SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md`
2. Review priorities and file corrections
3. Open `formula_simulation_mapping.csv` in editor

### Step 3: Update config.py

**For NEW assignments (36 formulas)**:
```python
# Add simulation_file= line to Formula(...) definition
# Example:
DARK_ENERGY_W0 = Formula(
    id="dark-energy-w0",
    label="(7.1) Dark Energy EoS",
    # ... other fields ...
    simulation_file="simulations/wz_evolution_desi_dr2.py",  # ADD THIS
)
```

**For UPDATE corrections (6 formulas)**:
```python
# Change existing simulation_file= to correct path
# Example:
# BEFORE:
simulation_file="simulations/gauge_coupling_running_v14_3.py",
# AFTER:
simulation_file="simulations/gauge_unification_precision_v12_4.py",
```

### Step 4: Verification
```bash
# Check all referenced files exist
python -c "
import config
import os
missing = []
for name, formula in vars(config.CoreFormulas).items():
    if hasattr(formula, 'simulation_file') and formula.simulation_file:
        if not os.path.exists(formula.simulation_file):
            missing.append(f'{name}: {formula.simulation_file}')
if missing:
    print('MISSING FILES:')
    for m in missing: print(f'  {m}')
else:
    print('✓ All simulation files exist!')
"
```

### Step 5: Testing
```bash
# Run all simulations to verify they work
cd simulations
for sim in *.py; do
    echo "Testing $sim..."
    python "$sim" --quiet 2>&1 | head -20
done
```

### Step 6: Export and Commit
```bash
# Regenerate theory_output.json
python export_theory.py

# Commit changes
git add config.py theory_output.json
git commit -m "Complete simulation file links for all formulas (100% coverage)

- Added simulation_file for 36 formulas previously missing links
- Corrected 6 incorrect simulation file paths
- Verified all referenced simulation files exist
- Updated theory_output.json with complete mappings

Files corrected:
- thermal_time_cosmology_v13_8.py → thermal_time_v12_8.py
- gw_dispersion_v14_2.py → gw_dispersion_v12_8.py
- gauge_coupling_running_v14_3.py → gauge_unification_precision_v12_4.py
- clifford_algebra_spinor_v14_0.py → g2_spinor_geometry_validation_v13_0.py

Coverage: 35% → 100% (19 → 55 formulas)
"
```

---

## Mapping by Physics Category

### Cosmology (7)
- Dark energy EoS, evolution
- Thermal time mechanism
- Effective dimension
- Friedmann constraint
- Attractor potential

### Gauge/GUT (8)
- GUT scale, coupling
- Weak mixing angle
- Strong coupling
- RG running
- SO(10), Pati-Salam breaking

### Proton Decay (3)
- Lifetime prediction
- Branching ratios
- Doublet-triplet splitting

### Neutrino Sector (6)
- Mass splittings (solar, atmospheric)
- Mixing angles (θ₂₃, θ₁₃)
- CP phase
- CKM matrix

### Higgs/Yukawa (9)
- Higgs VEV, mass, potential
- Yukawa couplings (top, bottom, tau)
- Instanton suppression

### Gravitational Waves (3)
- Dispersion relation
- Dispersion coefficient
- Alternative derivation

### Geometric Framework (11)
- Virasoro anomaly
- Sp(2,R) constraints
- Dimensional reduction
- Spinor geometry
- TCS topology
- Flux quantization
- Effective torsion

### Other (8)
- KK graviton mass
- Pneuma field (3)
- Mirror sector (2)
- Generation number
- Ghost coefficient

---

## Most Used Simulation Files

### Top 10 by Formula Count
1. `gauge_unification_precision_v12_4.py` - 7 formulas (gauge sector)
2. `pneuma_full_potential_v14_1.py` - 4 formulas (Pneuma field)
3. `higgs_yukawa_rg_v12_4.py` - 4 formulas (Yukawa sector)
4. `gw_dispersion_v12_8.py` - 3 formulas (GW sector)
5. `g2_landscape_scanner_v14_1.py` - 2 formulas (topology)
6. `pmns_full_matrix.py` - 2 formulas (neutrino masses)
7. `mirror_dark_matter_abundance_v15_3.py` - 2 formulas (mirror sector)
8. `attractor_scalar_v12_8.py` - 2 formulas (cosmology)
9. `wz_evolution_desi_dr2.py` - 2 formulas (dark energy)
10. Others - 1 formula each

---

## Quality Assurance

### Verification Checklist
- [x] All 55 formulas mapped
- [x] All simulation files verified to exist
- [x] File path corrections identified
- [x] CSV file generated for automation
- [x] Documentation complete and indexed
- [ ] config.py updated (PENDING)
- [ ] All simulations tested (PENDING)
- [ ] theory_output.json regenerated (PENDING)

### Validation Criteria
- Each formula has exactly ONE simulation_file
- All referenced files exist in simulations/ directory
- File paths use forward slashes (cross-platform)
- Simulation outputs match formula computed_value
- Units are consistent between formula and simulation

---

## Troubleshooting

### Problem: Simulation file doesn't exist
**Solution**: Check `SIMULATION_MAPPING_CORRECTIONS.txt` for replacement file

### Problem: Multiple simulations could validate a formula
**Solution**: Choose the most specific/relevant simulation (see justifications in Final Mapping)

### Problem: Simulation output doesn't match formula value
**Solution**:
1. Check if simulation has been updated but formula hasn't
2. Verify units match
3. Check for rounding differences
4. Review simulation derivation steps

### Problem: CSV import fails
**Solution**: Check CSV format, ensure proper quoting of paths with special characters

---

## Contact & Support

**Documentation Author**: Claude Code Analysis System
**Analysis Date**: December 25, 2025
**Project**: Principia Metaphysica v14.1+

For questions about:
- **Mapping rationale**: See `FORMULA_SIMULATION_MAPPING_FINAL.md`
- **Implementation**: See `SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md`
- **File corrections**: See `SIMULATION_MAPPING_CORRECTIONS.txt`
- **Automation**: Use `formula_simulation_mapping.csv`

---

## Appendix: All Documentation Files

```
Project Root (h:\Github\PrincipiaMetaphysica\)
├── README_SIMULATION_MAPPING.md                    ← This file
├── SIMULATION_MAPPING_EXECUTIVE_SUMMARY.md         ← Start here
├── FORMULA_SIMULATION_MAPPING_FINAL.md             ← Implementation guide
├── SIMULATION_LINK_MAPPING_REPORT.md               ← Detailed analysis
├── SIMULATION_MAPPING_QUICK_REFERENCE.txt          ← Fast lookup
├── SIMULATION_MAPPING_CORRECTIONS.txt              ← Critical fixes
└── formula_simulation_mapping.csv                  ← Machine-readable
```

**Total Documentation**: 7 files, ~15,000 words, 100% formula coverage

---

**END OF DOCUMENTATION INDEX**
