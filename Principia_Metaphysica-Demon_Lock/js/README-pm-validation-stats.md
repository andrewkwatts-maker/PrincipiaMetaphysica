# PM Validation Statistics Module

## Overview

The `pm-validation-stats.js` module provides a comprehensive, reusable statistics system for the Principia Metaphysica framework. It complements the existing `validation-stats.js` file with a more general-purpose API.

## Files

### `pm-validation-stats.js` (NEW)
- **Purpose**: General-purpose statistics module with global `PM_STATS` object
- **Scope**: Framework-wide statistics (58 parameters, validation metrics, etc.)
- **Usage**: Any page that needs parameter counts, validation rates, or summary statistics
- **Export**: `window.PM_STATS` global object
- **Auto-updates**: DOM elements with `class="pm-stat"` or `data-stat-id` attribute

### `validation-stats.js` (EXISTING)
- **Purpose**: Index page-specific validation display
- **Scope**: Homepage hero section statistics
- **Usage**: `index.html` only
- **Export**: `window.updateValidationStats()` function
- **Depends on**: `PM` constants from `theory-constants-enhanced.js`

## Usage Examples

### HTML Usage (pm-validation-stats.js)

```html
<!-- Include the script -->
<script src="js/pm-validation-stats.js"></script>

<!-- Use data attributes to auto-populate -->
<p>Total Parameters: <span data-stat-id="total_parameters"></span></p>
<p>Success Rate: <span data-stat-id="success_rate_1sigma"></span>%</p>
<p>Validation Summary: <span data-stat-id="validation_summary_percent"></span></p>

<!-- Alternative: use class="pm-stat" -->
<span class="pm-stat" data-stat-id="geometric_count"></span>
```

### JavaScript Usage

```javascript
// Access statistics programmatically
console.log(PM_STATS.total_parameters);  // 58
console.log(PM_STATS.geometric_count);   // 56
console.log(PM_STATS.success_rate_1sigma);  // "93.8"
console.log(PM_STATS.validation_summary);  // "45/48"

// Human-readable summaries
console.log(PM_STATS.summary_short);
// "45/48 predictions within 1σ (93.8%), 12 exact matches"

console.log(PM_STATS.summary_full);
// "56/58 parameters derived from geometry (96.6%), 45/48 predictions within 1σ (93.8%), 12 exact matches, mean deviation 0.35σ"

// Refresh statistics from theory_output.json
PM_STATS.update();
```

## Available Statistics

### Parameter Counts
- `total_parameters` (58) - Total SM + cosmology parameters
- `geometric_count` (56) - Parameters derived from geometry
- `derived_count` (43) - Parameters derived from other parameters
- `calibrated_count` (2) - θ₁₃ and δ_CP
- `phenomenological_count` (0) - Phenomenological inputs
- `exact_count` (12) - Exact topological parameters

### Validation Metrics
- `total_validations` (32) - Total validation tests
- `testable_predictions` (48) - Testable predictions (excludes exact constraints)
- `within_1sigma` (45) - Predictions within 1σ
- `within_2sigma` (48) - Predictions within 2σ
- `within_3sigma` (48) - Predictions within 3σ
- `exact_matches` (12) - Exact matches (0.0σ)
- `mean_sigma` (0.35) - Mean sigma deviation
- `max_sigma` (2.70) - Maximum sigma deviation
- `validations_passed` (32) - Validation tests passed
- `validations_failed` (0) - Validation tests failed

### Computed Percentages (Getters)
- `success_rate_1sigma` - "93.8"
- `success_rate_2sigma` - "100.0"
- `success_rate_3sigma` - "100.0"
- `exact_match_rate` - "25.0"
- `validation_success_rate` - "100.0"
- `geometric_percentage` - "96.6"

### Formatted Strings (Getters)
- `geometric_fraction` - "56/58"
- `exact_fraction` - "12/58"
- `derived_fraction` - "43/58"
- `validation_summary` - "45/48"
- `validation_summary_percent` - "45/48 (93.8%)"
- `calibration_statement` - "2 calibrated, 56 geometric"
- `transparency_statement` - "2 minimal calibrations (θ₁₃, δ_CP), 56/58 parameters purely geometric"

### Human-Readable Summaries (Getters)
- `summary_short` - One-line validation summary
- `summary_full` - Comprehensive validation summary

## Dynamic Loading

The module attempts to load statistics from `theory_output.json` on initialization:

```javascript
// theory_output.json structure (optional)
{
  "version": "16.0",
  "statistics": {
    "total_parameters": 58,
    "geometric_count": 56,
    // ... other statistics
  },
  "validation_summary": [
    ["Test Name", "PASS"],
    // ...
  ],
  "simulations": {
    // ... validation data with sigma values
  }
}
```

If `theory_output.json` is unavailable or doesn't contain statistics, the module falls back to hardcoded defaults (updated as of v16.0, December 2025).

## Integration with Existing Files

### With `pm-parameter-*.js` files

```html
<!-- Load in order -->
<script src="js/pm-parameter-schema.js"></script>
<script src="js/pm-parameter-data.js"></script>
<script src="js/pm-parameter-component.js"></script>
<script src="js/pm-validation-stats.js"></script>

<!-- Now you can use both systems -->
<pm-parameter id="topology.chi_eff"></pm-parameter>
<p>Total: <span data-stat-id="total_parameters"></span> parameters</p>
```

### With `theory-constants-enhanced.js`

Both systems can coexist:

```html
<script src="theory-constants-enhanced.js"></script>
<script src="js/validation-stats.js"></script>  <!-- Index page specific -->
<script src="js/pm-validation-stats.js"></script>  <!-- General purpose -->

<script>
  // Access PM constants (detailed parameter values)
  console.log(PM.topology.chi_eff.value);  // 144

  // Access PM_STATS (high-level statistics)
  console.log(PM_STATS.total_parameters);  // 58
</script>
```

## When to Use Which?

### Use `pm-validation-stats.js` when:
- You need framework-wide statistics (parameter counts, validation rates)
- You're building a summary/abstract/overview page
- You want auto-populated statistics via data attributes
- You need programmatic access to validation metrics

### Use `validation-stats.js` when:
- You're working on the index.html homepage
- You need the specific grade calculation
- You're updating the hero section statistics

### Use `pm-parameter-*.js` when:
- You need detailed parameter values with tooltips
- You want interactive parameter cards/components
- You need full parameter metadata (formulas, references, etc.)

## Browser Compatibility

- Modern browsers (ES6+ required for getters)
- Falls back gracefully if `theory_output.json` is unavailable
- No external dependencies

## Testing

Open `test-pm-stats.html` to see all statistics in action:

```bash
# From repository root
open test-pm-stats.html
# or
python -m http.server 8000
# Then navigate to http://localhost:8000/test-pm-stats.html
```

## Version History

- **v1.0.0** (2025-12-25) - Initial release
  - 58 parameters (56 geometric, 2 calibrated)
  - 32 validations (100% pass rate)
  - 45/48 predictions within 1σ (93.8%)
  - 12 exact matches

## Future Enhancements

- [ ] Add parameter category breakdown (topological, gauge, yukawa, etc.)
- [ ] Export statistics to CSV/JSON
- [ ] Real-time updates when theory_output.json changes
- [ ] Visualization widgets (charts, progress bars)
- [ ] Integration with paper citation system

## License

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
