# PM Constants Loader - Quick Reference Guide

**Version:** 2.1.0 (100% Compatible)
**File:** `h:\Github\PrincipiaMetaphysica\js\pm-constants-loader.js`

## Quick Start

### 1. Include the Script
```html
<script src="js/pm-constants-loader.js"></script>
```

### 2. Use Data Attributes
```html
<!-- Simple value -->
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>

<!-- With formatting -->
<span data-pm-value="parameters.dark_energy.w0" data-format="fixed:4"></span>

<!-- Category + param style -->
<span data-category="topology" data-param="n_gen"></span>
```

## All Patterns

### Pattern 1: data-pm-value (Recommended)
```html
<!-- Direct path to value -->
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>
<span data-pm-value="parameters.topology.CHI_EFF"></span>
<span data-pm-value="dimensions.D_BULK"></span>
```

**When to use:** You know the exact path in theory_output.json

---

### Pattern 2: data-category + data-param
```html
<!-- Category and parameter -->
<span data-category="topology" data-param="n_gen"></span>
<span data-category="dark_energy" data-param="w0"></span>
<span data-category="proton_decay" data-param="tau_p_years"></span>
```

**When to use:** More readable, automatically tries multiple path strategies

**Tries these paths in order:**
1. `simulations.[category].[param]`
2. `parameters.[category].[param]`
3. `[category].[param]`
4. `PM.[category].[param]` (flat access)

---

### Pattern 3: data-category + data-param + data-field
```html
<!-- Extract specific field from nested object -->
<span data-category="neutrino"
      data-param="pmns_angles.theta_12"
      data-field="experimental"></span>
```

**When to use:** You need a specific sub-field from an object

---

### Pattern 4: data-stat-id
```html
<!-- Statistics -->
<span data-stat-id="total_parameters"></span>
<span data-stat-id="within_1sigma"></span>

<!-- Also supports dotted paths -->
<span data-stat-id="simulations.proton_decay.tau_p_years"></span>
```

**When to use:** Displaying statistics or validation data

**Tries these sources in order:**
1. `PM_STATS.[id]` (if pm-validation-stats.js loaded)
2. `statistics.[id]` in theory_output.json
3. Dotted path via `PM.get(id)`
4. `validation_summary` array (by name or id)

---

### Pattern 5: data-formula-id
```html
<!-- Auto-fills with formula HTML -->
<div data-formula-id="proton-lifetime"></div>
<div data-formula-id="generation-number"></div>
```

**When to use:** Displaying formulas from the formula database

---

## Formatting

### Available Formats

```html
<!-- Scientific notation (N decimals) -->
<span data-pm-value="..." data-format="scientific:2"></span>
<!-- Output: 8.15e+34 -->

<!-- Fixed decimals -->
<span data-pm-value="..." data-format="fixed:4"></span>
<!-- Output: -0.8528 -->

<!-- Percentage -->
<span data-pm-value="..." data-format="percent"></span>
<!-- Output: 96.6% -->

<!-- Integer -->
<span data-pm-value="..." data-format="integer"></span>
<!-- Output: 144 -->

<!-- Auto (default - intelligent formatting) -->
<span data-pm-value="..."></span>
<!-- Output: Auto-formats based on magnitude -->
```

---

## Common Use Cases

### 1. Dimension Constants
```html
<span data-pm-value="dimensions.D_BULK"></span>           <!-- 26 -->
<span data-pm-value="dimensions.D_AFTER_SP2R"></span>     <!-- 13 -->
<span data-pm-value="dimensions.D_G2"></span>             <!-- 7 -->
<span data-pm-value="dimensions.D_OBSERVABLE"></span>     <!-- 4 -->
```

### 2. Simulation Results
```html
<!-- Proton decay -->
<span data-category="proton_decay" data-param="tau_p_years"></span>

<!-- Neutrino masses -->
<span data-category="neutrino_masses" data-param="m1_eV"></span>

<!-- Dark energy -->
<span data-category="dark_energy" data-param="w0" data-format="fixed:4"></span>
```

### 3. Topology Parameters
```html
<span data-category="topology" data-param="n_gen"></span>        <!-- 3 -->
<span data-category="topology" data-param="chi_eff"></span>      <!-- 144 -->
<span data-category="topology" data-param="B3"></span>           <!-- 24 -->
```

### 4. Validation Statistics
```html
<span data-stat-id="total_parameters"></span>
<span data-stat-id="within_1sigma"></span>
<span data-stat-id="within_2sigma"></span>
<span data-stat-id="success_rate_1sigma"></span>
```

### 5. Nested Values
```html
<!-- Higgs mass -->
<span data-category="simulations"
      data-param="higgs_mass.m_h_GeV"></span>

<!-- PMNS angle with specific field -->
<span data-category="neutrino"
      data-param="pmns_angles.theta_12"
      data-field="predicted"></span>
```

---

## JavaScript API

### Basic Usage
```javascript
// Get value by path
const value = PM.get('simulations.proton_decay.tau_p_years');
console.log(value);  // 8.15e+34

// Get simulation data (shorthand)
const tau_p = PM.simulation('proton_decay.tau_p_years');

// Direct access (flat)
const tau_p = PM.proton_decay.tau_p_years;
```

### Advanced Usage
```javascript
// Get formula
const formula = PM.formula('proton-lifetime');
console.log(formula.html);

// Get all formulas
const allFormulas = PM.formulas;

// Get statistics
const stats = PM.statistics;
console.log(stats.total_parameters);

// Check if loaded
if (PM._loaded) {
    console.log('Data is ready');
}

// Manually refresh DOM
PM.updateDOM();

// Format value
const formatted = PM.formatValue(8.15e34, 'scientific:2');
console.log(formatted);  // "8.15e+34"
```

### Dimensions
```javascript
PM.dimensions.D_BULK          // 26
PM.dimensions.D_AFTER_SP2R    // 13
PM.dimensions.D_G2            // 7
PM.dimensions.D_OBSERVABLE    // 4
```

---

## Error Handling

### Success State
```html
<!-- Element shows value -->
<span class="pm-loaded">8.15e+34</span>
```

### Loading State
```html
<!-- Element shows loading -->
<span class="pm-loading">...</span>
```

### Error State
```html
<!-- Element shows error -->
<span class="pm-error" title="ERROR: Path not found...">?</span>
```

**To debug errors:**
1. Check browser console for detailed error messages
2. Hover over "?" to see tooltip with attempted paths
3. Verify `theory_output.json` exists and is accessible
4. Run: `python run_all_simulations.py --export` to regenerate data

---

## CSS Styling

### Default Classes

```css
/* Loaded successfully */
.pm-loaded {
    /* Your styles */
}

/* Loading... */
.pm-loading {
    /* Your styles */
}

/* Error occurred */
.pm-error {
    /* Your styles */
    cursor: help;  /* Show tooltip on hover */
}

/* Formula auto-filled */
.pm-formula-auto {
    /* Your styles */
}
```

---

## Troubleshooting

### Problem: Shows "?"
**Solutions:**
1. Check console for error message
2. Hover over "?" for tooltip showing tried paths
3. Verify path exists in theory_output.json
4. Check for typos in data attributes
5. Ensure theory_output.json is up to date

### Problem: Shows "..."
**Solutions:**
1. Check if theory_output.json exists
2. Check browser console for fetch errors
3. Ensure file path is correct
4. Check browser network tab for 404 errors

### Problem: Wrong value shown
**Solutions:**
1. Clear browser cache
2. Regenerate theory_output.json: `python run_all_simulations.py --export`
3. Hard refresh page (Ctrl+Shift+R)

---

## Testing

**Test file:** `test-pm-constants-compatibility.html`

```bash
# Open in browser
start test-pm-constants-compatibility.html

# Check results
# - Should show 100% pass rate
# - Check console for detailed test results
# - Hover over failed tests for error details
```

---

## Best Practices

### 1. Use data-pm-value for clarity
```html
<!-- Good: Clear and explicit -->
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>

<!-- Also good: More concise -->
<span data-category="proton_decay" data-param="tau_p_years"></span>
```

### 2. Always specify format for numbers
```html
<!-- Good: Clear formatting intent -->
<span data-pm-value="parameters.dark_energy.w0" data-format="fixed:4"></span>

<!-- Less good: Relies on auto-formatting -->
<span data-pm-value="parameters.dark_energy.w0"></span>
```

### 3. Use semantic HTML
```html
<!-- Good: Screen reader friendly -->
<p>Proton lifetime: <span data-pm-value="..."></span> years</p>

<!-- Less good: No context -->
<div data-pm-value="..."></div>
```

### 4. Check for errors in development
```javascript
// Enable verbose logging
PM.load().then(() => {
    console.log('PM loaded:', PM.version);
    console.log('Simulations:', Object.keys(PM.simulations || {}));
});
```

---

## Version Compatibility

**v2.1.0 (Current)**
- 100% compatibility with all patterns
- Enhanced error reporting
- data-field support
- 4 path resolution strategies
- Full backward compatibility

**v2.0.0**
- 95% compatibility
- Basic patterns supported
- Limited error reporting

**Migration from v2.0.0 → v2.1.0**
- No breaking changes
- Drop-in replacement
- Automatic improvements

---

## Support

**Documentation:**
- Full report: `PM_CONSTANTS_LOADER_V2.1_COMPATIBILITY_REPORT.md`
- This guide: `js/PM_CONSTANTS_QUICK_REFERENCE.md`

**Testing:**
- Test suite: `test-pm-constants-compatibility.html`

**Console Commands:**
```javascript
// Check version
console.log(PM.version);

// Check loaded status
console.log(PM._loaded);

// Get all simulation keys
console.log(Object.keys(PM).filter(k => !k.startsWith('_')));

// Debug specific path
console.log(PM.get('simulations.proton_decay.tau_p_years'));
```

---

**Last Updated:** 2025-12-25
**Version:** 2.1.0
**Status:** Production Ready - 100% Compatible
