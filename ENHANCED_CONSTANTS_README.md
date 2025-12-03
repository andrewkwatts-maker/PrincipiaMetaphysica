# Enhanced Theory Constants System

**Version 7.0** - December 2025

## Overview

The Principia Metaphysica website now uses a **single source of truth** architecture for all physical constants and theoretical predictions. Every numerical value is:

1. **Defined once** in `config.py`
2. **Computed** by simulation scripts in `simulations/`
3. **Exported** to `theory_output.json`
4. **Enhanced** with metadata in `theory-constants-enhanced.js`
5. **Displayed** dynamically in HTML with hover tooltips

## Architecture

```
config.py
  ↓
run_all_simulations.py
  ↓
theory_output.json
  ↓
generate_enhanced_constants.py
  ↓
theory-constants-enhanced.js
  ↓
HTML pages (.pm-value elements)
  ↓
User sees value + hover tooltip
```

## Files

### Core System
- **`config.py`**: Single source of truth for all parameters
- **`run_all_simulations.py`**: Orchestrates all simulations
- **`generate_enhanced_constants.py`**: Creates enhanced JS constants with metadata
- **`theory-constants-enhanced.js`**: JavaScript constants with full metadata (auto-generated)

### Tooltip System
- **`js/pm-tooltip-system.js`**: JavaScript to populate values and show tooltips
- **`css/pm-tooltip.css`**: Styling for hoverable values and tooltips

### Utilities
- **`fix_all_magic_numbers.py`**: Script to replace hard-coded values with PM.* references
- **`test-tooltip-system.html`**: Test page to verify hover functionality

## Usage in HTML

### 1. Add Script Tags

```html
<head>
  ...
  <link rel="stylesheet" href="css/pm-tooltip.css">
  <script src="theory-constants-enhanced.js"></script>
  <script src="js/pm-tooltip-system.js"></script>
</head>
```

### 2. Use PM Values

Replace hard-coded numbers:
```html
<!-- OLD (magic number) -->
<p>The proton lifetime is 3.84×10³⁴ years</p>

<!-- NEW (dynamic with tooltip) -->
<p>The proton lifetime is <span class="pm-value"
     data-category="proton_decay"
     data-param="tau_p_median"
     data-format="display"></span> years</p>
```

### 3. Format Options

- **`display`**: Use pre-formatted display string (e.g., "3.84×10³⁴")
- **`fixed:2`**: Format as decimal with 2 places (e.g., "47.20")
- **`fixed:3`**: Format as decimal with 3 places (e.g., "0.177")
- **`scientific:2`**: Scientific notation (e.g., "2.12e+16")
- **`percent`**: Percentage format (e.g., "95.3%")

## Enhanced Metadata Structure

Each constant includes:

```javascript
PM.proton_decay.tau_p_median = {
    value: 3.764188689612127e+34,
    unit: "years",
    display: "3.84×10³⁴",
    uncertainty_lower: 2.479137899634815e+34,
    uncertainty_upper: 5.509450111901326e+34,
    uncertainty_oom: 0.177,
    confidence_level: "68%",
    formula: "τ_p = 3.82×10³³ × (M_GUT/10¹⁶)⁴ × (0.03/α_GUT)²",
    derivation: "Monte Carlo (1000 samples) with 3-loop RG + KK thresholds",
    source: "simulation:proton_decay_rg_hybrid",
    experimental_bound: 1.67e+34,
    experimental_source: "Super-K 2024",
    agreement: "2.3× above bound",
    testable: "Hyper-K 2030s",
    references: ["PDG 2024", "PM Section 4.2a"]
}
```

## Hover Tooltip Features

When hovering over any `.pm-value` element, users see:

- **Value & Unit**: "3.84×10³⁴ years"
- **Formula**: Mathematical expression
- **Derivation**: Physical explanation (e.g., "Monte Carlo with 3-loop RG")
- **Uncertainty**: Error bars or confidence intervals
- **Experimental Comparison**: Measured value and agreement (σ deviation)
- **Testability**: Future experiments (e.g., "Hyper-K 2030s")
- **Source**: Traceability (config parameter or simulation)
- **References**: Citations

## Available Constants

### Dimensions
- `PM.dimensions.D_bulk` = 26
- `PM.dimensions.D_after_sp2r` = 13
- `PM.dimensions.D_G2` = 7
- `PM.dimensions.D_eff` = 12.589

### Topology
- `PM.topology.chi_eff` = 144
- `PM.topology.b3` = 24
- `PM.topology.n_gen` = 3

### Proton Decay
- `PM.proton_decay.M_GUT` = 2.118×10¹⁶ GeV
- `PM.proton_decay.tau_p_median` = 3.84×10³⁴ years
- `PM.proton_decay.uncertainty_oom` = 0.177

### Gauge Unification
- `PM.gauge_unification.alpha_GUT_inv` = 23.54
- `PM.gauge_unification.unification_precision` = 0.953

### Dark Energy
- `PM.dark_energy.w0_PM` = -0.8528
- `PM.dark_energy.w0_DESI_central` = -0.83
- `PM.dark_energy.w0_DESI_error` = 0.06
- `PM.dark_energy.w0_sigma` = 0.38

### PMNS Matrix
- `PM.pmns_matrix.theta_23` = 47.20°
- `PM.pmns_matrix.theta_12` = 33.59°
- `PM.pmns_matrix.theta_13` = 8.57°
- `PM.pmns_matrix.delta_CP` = 235.0°
- `PM.pmns_matrix.avg_sigma` = 0.09

## Implementation Summary (v7.0)

### Files Updated (198 magic numbers → PM.* references)
1. **principia-metaphysica-paper.html** - 86 replacements
2. **sections/cosmology.html** - 27 replacements
3. **sections/gauge-unification.html** - 12 replacements
4. **sections/fermion-sector.html** - 38 replacements
5. **sections/predictions.html** - 35 replacements

### Benefits

✅ **Single Source of Truth**: Change config.py → regenerate → entire website updates
✅ **Traceability**: Every value traced to config or simulation
✅ **Educational**: Hover to see formula, derivation, uncertainty, experimental comparison
✅ **Maintainability**: No scattered magic numbers across 54 HTML files
✅ **Validation**: Verify all values come from simulations, not hand-typed

## Workflow

### To Update a Value:

1. **Edit config.py**:
   ```python
   class ProtonDecayParameters:
       M_GUT = 2.2e16  # New value
   ```

2. **Run simulations**:
   ```bash
   python run_all_simulations.py
   ```

3. **Regenerate enhanced constants**:
   ```bash
   python generate_enhanced_constants.py
   ```

4. **Verify** - Open any HTML page, values update automatically!

### To Add a New Constant:

1. Add to `config.py`
2. Add to appropriate simulation in `simulations/`
3. Export in `run_all_simulations.py`
4. Add enhanced metadata in `generate_enhanced_constants.py`
5. Use in HTML with `<span class="pm-value" ...>`

## Testing

Open `test-tooltip-system.html` in a browser to verify:
- Values populate correctly
- Tooltips appear on hover
- Formatting is correct
- Console shows no errors

## Copyright

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This system was developed with the assistance of AI tools including Claude (Anthropic), Grok (xAI), and Gemini (Google).
