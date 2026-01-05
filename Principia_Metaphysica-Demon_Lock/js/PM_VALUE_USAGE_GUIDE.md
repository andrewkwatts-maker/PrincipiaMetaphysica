# PM Value Elements - Usage Guide

## Overview

The `pm-constants-loader.js` (v2.2.0) provides dynamic data loading for Principia Metaphysica HTML documents. It automatically populates elements with values from `theory_output.json`.

## Features (v2.2.0)

✅ **Case-insensitive path resolution** - `dimensions.d_bulk` works even though JSON has `D_BULK`
✅ **Automatic parameter aliasing** - Legacy names map to current JSON structure
✅ **Auto-initialization** - Loads on DOMContentLoaded automatically
✅ **MutationObserver** - Auto-updates when new elements are added dynamically
✅ **Fallback display** - Shows "..." while loading, "?" for missing values
✅ **Enhanced error reporting** - Hover over "?" to see detailed error messages

## Supported Attribute Formats

### 1. `data-pm-value` (Recommended)

Direct path to value in theory_output.json:

```html
<span class="pm-value" data-pm-value="simulations.proton_decay.tau_p_years"></span>
<span class="pm-value" data-pm-value="parameters.topology.CHI_EFF"></span>
<span class="pm-value" data-pm-value="dimensions.D_bulk"></span>
```

### 2. `data-category` + `data-param`

Alternative format for category-based lookup:

```html
<span data-category="simulations" data-param="proton_decay.tau_p_years"></span>
<span data-category="topology" data-param="CHI_EFF"></span>
```

### 3. Formatting with `data-format`

Control number formatting:

```html
<!-- Scientific notation with 2 decimals -->
<span data-pm-value="simulations.proton_decay.tau_p_years" data-format="scientific:2"></span>
<!-- Output: 8.15e+34 -->

<!-- Fixed decimals -->
<span data-pm-value="parameters.dark_energy.d_eff" data-format="fixed:3"></span>
<!-- Output: 12.576 -->

<!-- Integer -->
<span data-pm-value="parameters.topology.CHI_EFF" data-format="integer"></span>
<!-- Output: 144 -->

<!-- Percent -->
<span data-pm-value="some.ratio" data-format="percent"></span>
<!-- Output: 75.0% -->
```

## Parameter Aliases (Automatic Mapping)

The loader automatically resolves these legacy/alternate names:

| HTML Attribute | Maps To | Notes |
|----------------|---------|-------|
| `dimensions.d_bulk` | `parameters.dimensions.D_BULK` | Case-insensitive |
| `dimensions.d_after_sp2r` | `parameters.dimensions.D_AFTER_SP2R` | Case-insensitive |
| `dimensions.d_observable` | `parameters.dimensions.D_OBSERVABLE` | Case-insensitive |
| `dimensions.d_g2` | `parameters.dimensions.D_INTERNAL` | Alternate name |
| `parameters.topology.b2` | `parameters.topology.B2` | Case mapping |
| `parameters.topology.b3` | `parameters.topology.B3` | Case mapping |
| `parameters.topology.h11` | `parameters.topology.HODGE_H11` | Naming convention |
| `parameters.topology.h31` | `parameters.topology.HODGE_H31` | Naming convention |
| `parameters.topology.nu` | `parameters.topology.n_gen` | Alternate name |
| `parameters.gauge.m_ps` | `simulations.breaking_chain.m_ps` | Different location |
| `validation.total_predictions` | `statistics.total_parameters` | Section rename |
| `validation.exact_matches` | `statistics.exact_matches` | Section rename |
| `validation.predictions_within_1sigma` | `statistics.within_1sigma` | Section rename |

## Case-Insensitive Lookups

The loader tries multiple strategies to find values:

1. **Exact path** - Try path as written
2. **Alias mapping** - Check if path has an alias
3. **Case-insensitive** - Match ignoring case
4. **Built-in dimensions** - Fallback to hardcoded dimension values

This means all of these work:

```html
<span data-pm-value="dimensions.D_BULK"></span>       <!-- Exact -->
<span data-pm-value="dimensions.d_bulk"></span>       <!-- Lowercase -->
<span data-pm-value="dimensions.D_Bulk"></span>       <!-- Mixed case -->
<span data-pm-value="DIMENSIONS.D_BULK"></span>       <!-- All caps -->
```

## Error Handling

### Loading States

- **Loading:** Element shows `...` while data loads
- **Success:** Element shows value, gets `pm-loaded` class
- **Error:** Element shows `?`, gets `pm-error` class

### Debug Mode

Enable detailed console logging:

```html
<script>
window.PM_DEBUG = true;  // Enable before pm-constants-loader.js loads
</script>
```

With debug mode enabled, you'll see:
- Exact paths tried for each failed lookup
- Detailed error messages in console
- All attempted strategies for finding values

### Error Tooltips

Hover over any `?` to see:
- The path that was requested
- All paths that were tried
- Suggestions for fixing the issue

## MutationObserver (Auto-Refresh)

The loader automatically detects when new elements are added to the DOM and updates them:

```javascript
// This will automatically populate when added
const newElement = document.createElement('span');
newElement.setAttribute('data-pm-value', 'simulations.proton_decay.tau_p_years');
document.body.appendChild(newElement);
// No need to call PM.updateDOM() manually!
```

## Manual Control

### Programmatic Access

```javascript
// Get a value
const value = window.PM.get('simulations.proton_decay.tau_p_years');

// Get simulation data
const protonData = window.PM.simulation('proton_decay');

// Get formula
const formula = window.PM.formula('proton-lifetime');

// Get statistics
const stats = window.PM.statistics;

// Format a value
const formatted = window.PM.formatValue(8.15e34, 'scientific:2');
```

### Manual Refresh

```javascript
// Force update all elements
window.PM.updateDOM();

// Reload data from JSON
window.PM.refresh();
```

## Common Paths

### Dimensions
- `dimensions.D_bulk` → 26
- `dimensions.D_after_sp2r` → 13
- `dimensions.D_observable` → 4
- `dimensions.D_G2` → 7

### Topology
- `parameters.topology.CHI_EFF` → 144
- `parameters.topology.B2` → 4
- `parameters.topology.B3` → 24
- `parameters.topology.n_gen` → 3

### Gauge
- `parameters.gauge.M_GUT` → 2.118e+16 GeV
- `simulations.breaking_chain.m_ps` → 1.2e+12 GeV

### Dark Energy
- `parameters.dark_energy.d_eff` → 12.576
- `parameters.dark_energy.alpha_T` → 0.5
- `parameters.dark_energy.w0` → -0.8528
- `parameters.dark_energy.wa` → -0.75

### Simulations
- `simulations.proton_decay.tau_p_years` → 8.15e+34 years
- `simulations.proton_decay.suppression_factor` → 2.125
- `simulations.higgs_mass.m_h_GeV` → 125.1 GeV
- `simulations.neutrino_masses.sum_masses_eV` → 0.06 eV

### Statistics
- `statistics.total_parameters` → 3
- `statistics.exact_matches` → 0
- `statistics.within_1sigma` → 2
- `statistics.mean_sigma` → 1.27

## Testing

Open `test-pm-value-fix.html` in a browser to test all features:

```bash
# Start local server
python -m http.server 8000

# Open browser
http://localhost:8000/test-pm-value-fix.html
```

Check browser console for detailed load report.

## Troubleshooting

### Values show "?"

1. Check browser console for errors
2. Enable `window.PM_DEBUG = true` for details
3. Verify `theory_output.json` exists and is accessible
4. Check the path spelling and case
5. Hover over "?" for suggested paths

### Data not loading

1. Ensure `theory_output.json` exists in project root
2. Run: `python run_all_simulations.py --export`
3. If using `file://` protocol, start a local server instead
4. Check browser console for fetch errors

### Case sensitivity issues

All paths are now case-insensitive in v2.2.0. If you still see issues:
- Check for typos in the path
- Verify the parameter exists in `theory_output.json`
- Enable debug mode to see all attempted paths

## Version History

### v2.2.0 (Current)
- ✅ Case-insensitive path resolution
- ✅ Parameter aliasing for legacy names
- ✅ MutationObserver for dynamic content
- ✅ Enhanced error reporting with tooltips
- ✅ Summary statistics in console

### v2.1.0
- ✅ Multi-strategy path resolution
- ✅ Support for data-category format
- ✅ Auto-initialization

### v2.0.0
- ✅ Initial dynamic loader
- ✅ data-pm-value support
