# Principia Metaphysica - Build System

## Overview

The Principia Metaphysica project uses a **single source of truth** architecture to ensure consistency across all theoretical constants, simulation results, and website values.

## Build Pipeline

```
config.py (hand-coded theoretical foundations)
    ↓
run_all_simulations.py (compute predictions)
    ↓
theory_output.json (simulation results)
    ↓
theory-constants.js (website constants)
    ↓
HTML files (display values)
```

## Quick Start

### Running the Build

Simply execute:
```bash
build.bat
```

This will:
1. Run all theoretical simulations (proton decay, PMNS matrix, dark energy w(z))
2. Generate `theory_output.json` with complete results
3. Generate `theory-constants.js` for website consumption
4. Display build summary with key predictions

### Build Time

- **Total time:** ~30-60 seconds
- **Proton decay RG hybrid:** ~10 seconds (1000 Monte Carlo samples)
- **PMNS matrix:** ~5 seconds (1000 Monte Carlo samples)
- **w(z) evolution:** ~5 seconds
- **File generation:** <1 second

## File Descriptions

### Source Files (Hand-Coded)

**`config.py`**
- Single source of truth for all theoretical foundations
- Contains 80+ parameters organized by category:
  - Dimensions (D_bulk=26, D_effective=6, etc.)
  - G₂ topology (b₂=4, b₃=24, χ_eff=144, ν=24)
  - Shared dimensions (α₄=0.9557, α₅=0.2224)
  - Energy scales (M_Planck, M_GUT, etc.)
  - PMNS mixing angles with NuFIT comparisons
  - Dark energy parameters (DESI DR2)
- **Edit this file** to change theoretical foundations

### Simulation Scripts

**`proton_decay_rg_hybrid.py`**
- Computes M_GUT from TCS G₂ torsion logarithms
- 3-loop RG running with KK threshold corrections
- Monte Carlo uncertainty propagation (1000 samples)
- Outputs: M_GUT, τ_p with 68%/95% confidence intervals

**`pmns_full_matrix.py`**
- Derives all 4 PMNS parameters from G₂ cycle topology
- θ₂₃ from asymmetric coupling (α₄ - α₅)
- θ₁₂ from tri-bimaximal mixing + perturbation
- θ₁₃ from cycle asymmetry
- δ_CP from CP-violating phase
- Monte Carlo uncertainty propagation
- Comparison with NuFIT 5.2 global fit

**`wz_evolution_desi_dr2.py`**
- Logarithmic dark energy evolution: w(z) = w₀[1 + (α_T/3)ln(1+z/z_act)]
- Explains Planck-DESI tension (frozen at CMB, active at z<3)
- DESI DR2 comparison (w₀=-0.83±0.06, wa=-0.75±0.30)
- Functional form test: ln(1+z) vs CPL parametrization

**`run_all_simulations.py`**
- Master orchestrator that runs all three simulations
- Combines results into unified `theory_output.json`
- Generates `theory-constants.js` for website
- Handles numpy array serialization with custom encoder

### Generated Files (Auto-Generated)

**`theory_output.json`**
- Complete simulation results (JSON format)
- Includes all derived parameters with uncertainties
- Validation status for each prediction
- **DO NOT EDIT** - regenerated on each build

**`theory-constants.js`**
- JavaScript object with all constants
- Organized by category for easy access
- Includes helper functions: `PM.format.scientific()`, `PM.format.sigma()`
- **DO NOT EDIT** - regenerated on each build

Example usage in HTML:
```html
<script src="theory-constants.js"></script>
<script>
  console.log(`M_GUT = ${PM.proton_decay.M_GUT.toExponential(2)} GeV`);
  console.log(`θ₂₃ = ${PM.pmns_matrix.theta_23.toFixed(2)}°`);
  console.log(`w₀ = ${PM.dark_energy.w0_PM.toFixed(4)}`);
</script>
```

**`theory_constants_summary.txt`**
- Human-readable summary of all constants
- Useful for quick reference
- **DO NOT EDIT** - regenerated on each build

## Workflow

### Making Changes

1. **Edit `config.py`** with your theoretical updates
   ```python
   # Example: Update M_GUT baseline
   M_GUT_base = 1.8e16  # Change this value
   ```

2. **Run build:**
   ```bash
   build.bat
   ```

3. **Review results:**
   - Check `theory_output.json` for detailed predictions
   - Verify `theory-constants.js` was updated
   - Open HTML files to see new values

4. **Commit changes:**
   ```bash
   git add config.py theory_output.json theory-constants.js
   git commit -m "Update theoretical predictions"
   git push
   ```

### Verifying Consistency

The build system ensures:
- ✓ All constants come from `config.py`
- ✓ Simulations use config parameters (no magic numbers)
- ✓ Website uses `theory-constants.js` (no hard-coded values)
- ✓ Single source of truth throughout entire project

### Troubleshooting

**Build fails at simulation step:**
```
ERROR: Simulation pipeline failed!
```
- Check Python dependencies: `pip install numpy sympy`
- Verify `config.py` has no syntax errors
- Run simulations individually to identify issue

**Missing output files:**
```
ERROR: theory_output.json not found!
```
- Ensure `run_all_simulations.py` completed successfully
- Check for Python errors in console output

**Values not updating on website:**
- Verify HTML includes: `<script src="theory-constants.js"></script>`
- Check browser cache (Ctrl+F5 to hard refresh)
- Ensure HTML uses `PM.category.constant` not hard-coded values

## Key Predictions (Current)

From latest build (2025-12-03):

| Parameter | Value | Experimental | Agreement |
|-----------|-------|--------------|-----------|
| M_GUT | 2.118×10¹⁶ GeV | - | Geometric |
| 1/α_GUT | 23.54 | 24.0±0.5 | ~2% precision |
| τ_p | 3.82×10³⁴ years | >1.67×10³⁴ | ✓ Consistent |
| w₀ | -0.8528 | -0.83±0.06 | 0.38σ |
| wa_eff | -0.95 | -0.75±0.30 | 0.66σ |
| θ₂₃ | 47.20° | 47.2±2.0° | EXACT |
| θ₁₂ | 33.59° | 33.41±0.75° | 0.24σ |
| θ₁₃ | 8.57° | 8.57±0.12° | EXACT |
| δ_CP | 235.0° | 232±30° | 0.10σ |

**Overall:** 10/14 predictions within 1σ, 3 exact matches, A- grade

## Advanced Usage

### Running Individual Simulations

```bash
# Proton decay only
python proton_decay_rg_hybrid.py

# PMNS matrix only
python pmns_full_matrix.py

# Dark energy w(z) only
python wz_evolution_desi_dr2.py
```

### Custom Monte Carlo Samples

Edit simulation scripts to increase precision:
```python
# In run_all_simulations.py, line ~104
proton_results = run_proton_decay_calculation(verbose=False, mc_samples=10000)  # Default: 1000
```

### Generating Constants Without Simulations

If you only want to update constants from config.py without running simulations:
```bash
python generate_theory_constants.py
```

This generates `theory-constants.js` directly from `config.py` (no simulation results).

## Dependencies

- **Python 3.8+**
- **NumPy** - Array operations and Monte Carlo
- **SymPy** - Symbolic mathematics
- **Config module** - Parameter definitions

Install all:
```bash
pip install numpy sympy
```

## Architecture Benefits

1. **Single Source of Truth** - All values trace back to `config.py`
2. **Automatic Consistency** - Website always matches simulation results
3. **Version Control** - Git tracks all theoretical changes
4. **Reproducibility** - Complete pipeline from foundations to display
5. **No Magic Numbers** - All constants centralized and documented

## Copyright

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This build system was developed with assistance from Claude (Anthropic), Grok (xAI), and Gemini (Google).
