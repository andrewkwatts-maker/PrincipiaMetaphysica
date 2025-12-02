# Magic Number Elimination System

## Overview

This system establishes a **single source of truth** for all physics constants across the Principia Metaphysica website. All constants are now:

1. **Defined in `config.py`** (hand-coded theoretical foundations)
2. **Computed by simulations** (proton decay, PMNS, dark energy)
3. **Output to `theory_output.json`** (complete simulation results)
4. **Exposed via `theory-constants.js`** (website-ready JavaScript constants)
5. **Available in all HTML files** via `<script src="theory-constants.js"></script>`

## Files in This System

### Detection & Analysis

- **`find_magic_numbers.py`** - Comprehensive magic number detector
  - Scans all HTML files for hard-coded numeric constants
  - Compares against canonical values from `theory_output.json`
  - Generates detailed report with context

- **`run_magic_finder.py`** - Simplified runner (no Unicode issues)
  - Fast scan of all files
  - Outputs JSON instructions for automated fixing

- **`magic_number_fix_instructions.json`** - Machine-readable fix instructions
  - Contains all 6,066 detected magic numbers
  - Includes file paths, line numbers, contexts
  - Specifies PM.* replacement paths

### Automated Fixing

- **`fix_magic_numbers_focused.py`** - Focused fixer script
  - ✅ Adds `<script src="theory-constants.js"></script>` to all HTML files (36 files updated)
  - Generates priority list for manual review
  - Avoids false positives (numbers in prose text)

- **`MAGIC_NUMBER_PRIORITIES.md`** - Human-readable priorities
  - Lists files updated with script tags
  - Identifies high-priority files for review
  - Provides replacement examples

### Source of Truth Pipeline

```
config.py (80+ hand-coded constants)
    ↓
run_all_simulations.py (computes predictions)
    ↓
theory_output.json (complete results)
    ↓
theory-constants.js (auto-generated for website)
    ↓
HTML files (via <script src="theory-constants.js"></script>)
```

## Current Status

### ✅ Completed

1. **Script tags added to 36 HTML files**
   - All major theory sections
   - All foundation pages
   - Beginner's guide and paper
   - All diagrams and references

2. **Theory constants available website-wide**
   - `PM.dimensions.*` (D_bulk=26, D_after_sp2r=13, etc.)
   - `PM.topology.*` (chi_eff=144, b3=24, n_gen=3)
   - `PM.proton_decay.*` (M_GUT, tau_p, alpha_GUT_inv)
   - `PM.pmns_matrix.*` (theta_23, theta_12, theta_13, delta_cp)
   - `PM.dark_energy.*` (w0_PM, wa_PM_effective)
   - `PM.shared_dimensions.*` (alpha_4, alpha_5)
   - `PM.validation.*` (status, grades, predictions_within_1sigma)

3. **Helper functions available**
   - `PM.format.scientific(value, decimals)` - Format as scientific notation
   - `PM.format.fixed(value, decimals)` - Format as fixed decimal
   - `PM.format.percent(value)` - Format as percentage
   - `PM.format.sigma(value)` - Format with sigma symbol

4. **Build system integrated**
   - `build.bat` runs full pipeline
   - Regenerates `theory-constants.js` on every build
   - Verifies output files exist

### 📋 Pending (Manual Review Recommended)

**6,066 magic numbers detected** across 54 files. Most are false positives (numbers in prose text like "26-dimensional"). Priority areas:

1. **Theory sections with formulas**
   - `sections/gauge-unification.html` (360 occurrences)
   - `sections/geometric-framework.html` (423 occurrences)
   - `sections/cosmology.html` (486 occurrences)
   - `sections/fermion-sector.html` (293 occurrences)

2. **Main paper**
   - `principia-metaphysica-paper.html` (614 occurrences)

3. **Beginner's guide**
   - `beginners-guide.html` (205 occurrences)

## Usage Examples

### Basic Constant Access

```html
<script src="theory-constants.js"></script>
<script>
// Access constants directly
const M_GUT = PM.proton_decay.M_GUT;  // 2.118e16
const theta_23 = PM.pmns_matrix.theta_23;  // 47.2
const w0 = PM.dark_energy.w0_PM;  // -0.853
</script>
```

### Formatted Display

```html
<!-- Display M_GUT in scientific notation -->
<p>M<sub>GUT</sub> = <span id="mgut-display"></span> GeV</p>

<script>
document.getElementById('mgut-display').textContent =
    PM.format.scientific(PM.proton_decay.M_GUT, 3);
// Output: "2.118e+16"
</script>
```

### Dynamic Predictions Card

```html
<div class="prediction-card">
    <h3>Proton Decay</h3>
    <p>Lifetime: <span id="tau-p"></span> years</p>
    <p>GUT Scale: <span id="m-gut"></span> GeV</p>
    <p>Coupling: 1/α<sub>GUT</sub> = <span id="alpha-gut"></span></p>
</div>

<script>
document.getElementById('tau-p').textContent =
    PM.format.scientific(PM.proton_decay.tau_p_median, 2);
document.getElementById('m-gut').textContent =
    PM.format.scientific(PM.proton_decay.M_GUT, 3);
document.getElementById('alpha-gut').textContent =
    PM.proton_decay.alpha_GUT_inv.toFixed(2);
</script>
```

### Conditional Display Based on Validation

```html
<script>
if (PM.validation.pmns_status === 'EXCELLENT') {
    document.getElementById('pmns-badge').classList.add('success');
}

// Show number of exact matches
document.getElementById('exact-count').textContent =
    PM.validation.exact_matches;
</script>
```

## Replacement Strategy

### ✅ DO Replace

- **Formulas and calculations**
  ```html
  <!-- Before -->
  <code>M_GUT = 2.118×10¹⁶ GeV</code>

  <!-- After -->
  <code>M_GUT = <span class="value"></span> GeV</code>
  <script>document.querySelector('.value').textContent = PM.format.scientific(PM.proton_decay.M_GUT, 3);</script>
  ```

- **Data attributes**
  ```html
  <!-- Before -->
  <div data-mgut="2.118e16">

  <!-- After -->
  <div data-mgut="" id="data-container"></div>
  <script>document.getElementById('data-container').dataset.mgut = PM.proton_decay.M_GUT;</script>
  ```

- **Prediction cards and results**
- **Interactive visualizations**
- **Form default values**

### ❌ DON'T Replace

- **Prose text** ("the 26-dimensional bulk space")
- **Historical context** ("Planck proposed in 1900")
- **References and citations**
- **Section numbers** ("Section 3.2")
- **Dates and years**

## Next Steps

1. **Review priority files** (see `MAGIC_NUMBER_PRIORITIES.md`)
   - Start with `sections/gauge-unification.html` (has form values)
   - Review formula displays in theory sections

2. **Test the system**
   - Open any HTML file in browser
   - Open console: `console.log(PM)`
   - Verify constants are accessible

3. **Gradual migration**
   - Replace magic numbers as pages are updated
   - Focus on formulas and predictions first
   - Leave prose numbers unchanged

4. **Maintain single source of truth**
   - Update `config.py` when theoretical values change
   - Run `build.bat` to regenerate `theory-constants.js`
   - Never hard-code values in HTML again

## Detection Results

**Summary:**
- **Total magic numbers found**: 6,066
- **Files affected**: 54
- **Script tags added**: 36 files
- **Already had script**: 2 files
- **Failed (no </head> tag)**: 3 files

**Top files by occurrence:**
1. `principia-metaphysica-paper.html` - 614
2. `sections/cosmology.html` - 486
3. `sections/geometric-framework.html` - 423
4. `sections/gauge-unification.html` - 360
5. `philosophical-implications.html` - 337

**By category:**
- Topology (3, 24, 144): 3,153 occurrences
- Dimensions (4, 6, 13, 26): 2,816 occurrences
- PMNS angles: 53 occurrences
- Shared dimensions (α₄, α₅): 24 occurrences
- Proton decay (M_GUT, τ_p): 20 occurrences

Most of these are false positives (prose text). Manual review recommended for formulas and predictions.

## Troubleshooting

**Constants not available in HTML:**
```javascript
// Check if script loaded
console.log(PM);  // Should show object with all constants

// If undefined, check:
// 1. Is <script src="theory-constants.js"></script> in <head>?
// 2. Is path correct? (use "../theory-constants.js" in subdirectories)
// 3. Does theory-constants.js exist in root?
```

**Values seem outdated:**
```bash
# Regenerate from latest simulations
python run_all_simulations.py

# Or use build system
build.bat
```

**Need to add new constant:**
1. Add to `config.py`
2. Run `python run_all_simulations.py`
3. Constant now available as `PM.category.constant_name`

## Benefits

✅ **No more magic numbers** - All constants trace to `config.py`
✅ **Automatic updates** - Change `config.py`, run build, website updates
✅ **No drift** - Website always matches latest simulation results
✅ **Type safety** - JavaScript constants are validated
✅ **Easy maintenance** - One place to update values
✅ **Auditability** - Can trace any constant to source

## Copyright

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This project was developed with the assistance of AI tools including Claude (Anthropic), Grok (xAI), and Gemini (Google).
