# Firebase Page Loader Module

**File:** `h:/Github/PrincipiaMetaphysica/js/firebase-page-loader.js`

## Overview

A comprehensive JavaScript module that loads page content from Firebase Firestore and dynamically populates PM (Principia Metaphysica) values from centralized theory constants. This module provides the infrastructure for dynamic content management, automatic value population, and seamless integration with the authentication and tooltip systems.

## Features

### 1. **Firebase Data Loading**
- Loads page content from Firestore `pages` collection
- Fetches theory constants from `theory_constants/current` document
- Parallel loading for optimal performance
- Comprehensive error handling with fallback mechanisms

### 2. **Dynamic PM Value Population**
- Finds and populates all `.pm-value` elements automatically
- Supports two patterns:
  - `data-category` + `data-param` (e.g., `data-category="proton_decay" data-param="M_GUT"`)
  - `data-pm-value` for nested paths (e.g., `data-pm-value="v12_7_pure_geometric.vev_pure.v_GeV"`)
- Handles nested object paths with dot notation
- Multiple format options (scientific, fixed, percent, etc.)

### 3. **Session Storage Caching**
- Automatic caching in sessionStorage
- 5-minute TTL (time-to-live)
- Cache versioning for automatic invalidation
- Per-page cache management

### 4. **Tooltip Integration**
- Automatic tooltip initialization after data loads
- Works with existing PM tooltip system
- Dispatches events for custom integrations

### 5. **Fallback Support**
- Falls back to static `theory-constants-enhanced.js` if Firebase fails
- Graceful degradation for offline scenarios
- Maintains functionality without Firebase connection

## Installation

### Prerequisites

Ensure Firebase is configured in your project:

```javascript
// firebase-config.js must be available
import { db } from './firebase-config.js';
```

### Import the Module

```javascript
import { loadPageFromFirebase, populatePMValues, clearPageCache, refreshPageData } from './firebase-page-loader.js';
```

## API Reference

### Functions

#### `loadPageFromFirebase(pageId)`

Loads page content from Firebase and populates all PM values.

**Parameters:**
- `pageId` (string): Page identifier (e.g., 'index', 'fermion-sector', 'gauge-unification')

**Returns:**
- `Promise<Object>`: Result object with:
  - `success` (boolean): Whether load succeeded
  - `data` (Object): Loaded data (pmData and pageContent)
  - `fromCache` (boolean): Whether data came from cache
  - `error` (string): Error message if failed

**Example:**
```javascript
const result = await loadPageFromFirebase('fermion-sector');

if (result.success) {
  console.log('Page loaded!', result.data);
  console.log('From cache:', result.fromCache);
} else {
  console.error('Load failed:', result.error);
}
```

#### `populatePMValues(pmData)`

Populates all `.pm-value` elements with data from PM object.

**Parameters:**
- `pmData` (Object): PM theory constants object

**Returns:**
- `number`: Count of elements populated

**Example:**
```javascript
const count = populatePMValues(window.PM);
console.log(`Populated ${count} PM values`);
```

#### `refreshPageData(pageId)`

Refreshes page data from Firebase, bypassing cache.

**Parameters:**
- `pageId` (string): Page identifier

**Returns:**
- `Promise<Object>`: Result object (same as loadPageFromFirebase)

**Example:**
```javascript
const result = await refreshPageData('index');
console.log('Data refreshed:', result);
```

#### `clearPageCache()`

Clears all cached page data from sessionStorage.

**Returns:**
- `void`

**Example:**
```javascript
clearPageCache();
console.log('All page caches cleared');
```

## HTML Usage Patterns

### Pattern 1: Category + Parameter

Use `data-category` and `data-param` attributes for standard PM object structure:

```html
<span class="pm-value"
      data-category="proton_decay"
      data-param="M_GUT"
      data-format="display"></span>

<span class="pm-value"
      data-category="pmns_matrix"
      data-param="theta_23"
      data-format="fixed:2"></span>

<span class="pm-value"
      data-category="gauge_unification"
      data-param="alpha_GUT_inv"
      data-format="fixed:2"></span>
```

**Data Structure:**
```javascript
PM.proton_decay.M_GUT = { value: 2.118e16, display: "2.12×10¹⁶", unit: "GeV" }
PM.pmns_matrix.theta_23 = { value: 42.3, unit: "°" }
PM.gauge_unification.alpha_GUT_inv = { value: 24.54 }
```

### Pattern 2: Nested Path

Use `data-pm-value` for nested object paths:

```html
<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.vev_pure.v_GeV"
      data-format="fixed:3"></span>

<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.flux_stab_pure.m_h_GeV"
      data-format="fixed:2"></span>

<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.proton_lifetime_predicted.tau_p_years"
      data-format="scientific:2"></span>
```

**Data Structure:**
```javascript
PM.v12_7_pure_geometric.vev_pure.v_GeV = { value: 246.220 }
PM.v12_7_pure_geometric.flux_stab_pure.m_h_GeV = { value: 125.25 }
PM.v12_7_pure_geometric.proton_lifetime_predicted.tau_p_years = { value: 1.23e35 }
```

### Accessing Nested Fields

Use `data-field` to access specific fields within objects:

```html
<span class="pm-value"
      data-category="pmns_matrix"
      data-param="theta_12"
      data-field="experimental_value"
      data-format="fixed:2"></span>
```

**Data Structure:**
```javascript
PM.pmns_matrix.theta_12 = {
  value: 33.82,
  experimental_value: 33.41,
  error: 0.41,
  unit: "°"
}
```

## Format Specifications

The `data-format` attribute supports these formats:

| Format | Description | Example Output |
|--------|-------------|----------------|
| `scientific:N` | Scientific notation with N decimals | `1.23e+16` |
| `fixed:N` | Fixed decimals (N places) | `24.54` |
| `percent:N` | Percentage with N decimals | `85.3%` |
| `sigma:N` | Sigma notation | `2.46σ` |
| `eV:N` | Electron volts | `125.25 eV` |
| `GeV:N` | Giga electron volts | `246.220 GeV` |
| `TeV:N` | Tera electron volts | `2.12 TeV` |
| `years:N` | Years in scientific notation | `1.23e+35 years` |
| `display` | Pre-formatted display string | `2.12×10¹⁶` |

**Examples:**

```html
<!-- Scientific notation with 2 decimals -->
<span class="pm-value"
      data-category="proton_decay"
      data-param="tau_p_median"
      data-format="scientific:2"></span>
<!-- Output: 1.23e+35 -->

<!-- Fixed decimals (3 places) -->
<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.vev_pure.v_GeV"
      data-format="fixed:3"></span>
<!-- Output: 246.220 -->

<!-- Display format (use pre-formatted string) -->
<span class="pm-value"
      data-category="proton_decay"
      data-param="M_GUT"
      data-format="display"></span>
<!-- Output: 2.12×10¹⁶ (from obj.display) -->
```

## Events

### `pm-page-loaded`

Dispatched when page data has been successfully loaded and populated.

**Event Detail:**
```javascript
{
  pageId: string,          // Page identifier
  pmData: Object,          // PM theory constants
  pageContent: Object|null, // Page content from Firestore
  timestamp: number,       // Load timestamp
  fallback: boolean        // Whether fallback was used (optional)
}
```

**Usage:**
```javascript
window.addEventListener('pm-page-loaded', (event) => {
  const { pageId, pmData, pageContent, timestamp } = event.detail;

  console.log(`Page ${pageId} loaded at ${timestamp}`);
  console.log('PM Data:', pmData);
  console.log('Page Content:', pageContent);

  // Custom initialization here
  initializeCustomComponents();
});
```

### `pm-tooltips-ready`

Dispatched when tooltips have been initialized and are active.

**Usage:**
```javascript
window.addEventListener('pm-tooltips-ready', () => {
  console.log('Tooltips are now active');
  // Enable features that depend on tooltips
});
```

## Integration with auth-guard.js

To integrate with the authentication guard system:

### Step 1: Add Import

```javascript
import { loadPageFromFirebase } from './firebase-page-loader.js';
```

### Step 2: Update Authentication Handler

Replace the data loading section in `handleAuthenticated()`:

```javascript
async function handleAuthenticated(user) {
  // ... existing code ...

  // Initialize data from Firestore
  try {
    await initializeData();

    if (currentPageId) {
      // Use the new firebase-page-loader module
      const result = await loadPageFromFirebase(currentPageId);

      if (result.success) {
        console.log(`Page loaded successfully: ${currentPageId}${result.fromCache ? ' (from cache)' : ''}`);
      } else {
        console.warn('Page load failed, using fallback');
      }

      // Load legacy data for backward compatibility
      const pageData = await loadAllPageData(currentPageId);
      window.dispatchEvent(new CustomEvent('pm-data-ready', { detail: pageData }));
    }
  } catch (error) {
    console.error('Error initializing data:', error);
  }
}
```

## Session Storage Cache

### Cache Structure

```
Key: pm_firebase_cache_{pageId}
Value: {
  version: "1.0",
  timestamp: 1234567890,
  pmData: { ... },
  pageContent: { ... }
}
```

### Cache Behavior

- **TTL:** 5 minutes
- **Scope:** Per browser tab/window (sessionStorage)
- **Versioning:** Cache automatically invalidated when version changes
- **Automatic Cleanup:** Invalid/expired caches removed on access

### Cache Management

```javascript
// Clear all caches
clearPageCache();

// Refresh bypassing cache
await refreshPageData('fermion-sector');

// Check if data came from cache
const result = await loadPageFromFirebase('index');
if (result.fromCache) {
  console.log('Loaded from cache');
}
```

## Error Handling

### Firebase Connection Errors

If Firebase is unavailable, the module:

1. Logs error to console
2. Attempts to load static `theory-constants-enhanced.js`
3. Populates values with static PM object
4. Dispatches `pm-page-loaded` event with `fallback: true`

```javascript
// Firebase fails → fallback to static
const result = await loadPageFromFirebase('index');
// result.success may be false, but values still populate from static PM
```

### Missing Data

If a PM value is not found:

1. Logs warning to console
2. Skips the element (doesn't populate)
3. Element retains original content

```html
<!-- If PM.nonexistent.param doesn't exist -->
<span class="pm-value"
      data-category="nonexistent"
      data-param="param">Fallback text</span>
<!-- Element keeps "Fallback text" -->
```

### Invalid Format

If format specification is invalid:

1. Logs warning to console
2. Returns string representation of value

```javascript
// Invalid format → returns value.toString()
formatPMValue(42.5, 'invalid:format') // "42.5"
```

## Testing

### Test Page

A comprehensive test page is available:

```
h:/Github/PrincipiaMetaphysica/test-firebase-page-loader.html
```

**Features:**
- Test all PM value patterns
- Test all format specifications
- Event logging
- Cache management controls
- Manual populate testing

### Running Tests

1. Open `test-firebase-page-loader.html` in browser
2. Click "Load Test Page" to fetch from Firebase
3. Verify all PM values populate correctly
4. Test cache by clicking "Load" again (should show "from cache")
5. Test refresh with "Refresh (Bypass Cache)"
6. Clear cache and verify reload

### Expected Results

| Test Case | Expected Output |
|-----------|----------------|
| M_GUT (display) | `2.12×10¹⁶ GeV` |
| α_GUT (fixed:4) | `0.0408` |
| θ₂₃ (fixed:2) | `42.30°` |
| 1/α_GUT (fixed:2) | `24.54` |
| VEV (fixed:3) | `246.220 GeV` |
| Higgs mass (fixed:2) | `125.25 GeV` |
| Proton lifetime (scientific:2) | `1.23e+35 years` |
| w₀ (fixed:4) | `-0.8528` |

## Performance Optimization

### Parallel Loading

Theory constants and page content load in parallel:

```javascript
const [pmData, pageContent] = await Promise.all([
  loadTheoryConstants(),
  loadPageContent(pageId)
]);
```

### Batch DOM Updates

All PM values populated in single DOM pass:

```javascript
const elements = document.querySelectorAll('.pm-value, [data-category][data-param], [data-pm-value]');
elements.forEach(el => {
  // Populate each element
});
```

### Lazy Tooltip Initialization

Tooltips initialize after DOM population complete:

```javascript
await new Promise(resolve => setTimeout(resolve, 100));
initializeTooltips();
```

## Backward Compatibility

The module maintains full backward compatibility:

| Feature | Compatibility |
|---------|---------------|
| Existing `.pm-value` elements | ✓ Fully supported |
| Static PM object | ✓ Used as fallback |
| `pm-data-ready` event | ✓ Still dispatched |
| Legacy `loadAllPageData()` | ✓ Can run in parallel |
| Existing tooltip system | ✓ Automatically integrated |

## Migration Guide

### Migrating Existing Pages

1. **Add data attributes** to existing `.pm-value` elements:
   ```html
   <!-- Before -->
   <span class="pm-value">2.12×10¹⁶</span>

   <!-- After -->
   <span class="pm-value"
         data-category="proton_decay"
         data-param="M_GUT"
         data-format="display"></span>
   ```

2. **Remove hardcoded values** from HTML:
   ```html
   <!-- Elements now start empty -->
   <span class="pm-value"
         data-category="pmns_matrix"
         data-param="theta_23"
         data-format="fixed:2"></span>
   ```

3. **Let module populate** dynamically:
   - Values populate automatically after `loadPageFromFirebase()` call
   - No manual initialization needed

4. **Test fallback** by disabling Firebase:
   - Ensure static `theory-constants-enhanced.js` loads
   - Verify values still populate

### No Changes Required For

- Pages already using `.pm-value` pattern with data attributes
- Pages using static PM object as fallback
- Existing event listeners (`pm-data-ready`, `pm-tooltips-ready`)

## Troubleshooting

### Values Not Populating

**Check:**
1. Firebase connection working?
2. `theory_constants/current` document exists in Firestore?
3. Data attributes correct? (`data-category` and `data-param` or `data-pm-value`)
4. PM object structure matches expected format?
5. Console errors logged?

**Debug:**
```javascript
// Check PM object loaded
console.log('PM object:', window.PM);

// Manually populate
import { populatePMValues } from './firebase-page-loader.js';
const count = populatePMValues(window.PM);
console.log(`Populated ${count} values`);
```

### Cache Issues

**Clear cache:**
```javascript
clearPageCache();
```

**Bypass cache:**
```javascript
await refreshPageData('page-id');
```

**Check cache:**
```javascript
const cacheKey = 'pm_firebase_cache_index';
const cached = sessionStorage.getItem(cacheKey);
console.log('Cached data:', JSON.parse(cached));
```

### Tooltip Not Working

**Check:**
1. Tooltip system loaded? (`pm-tooltip-system.js`)
2. `initPMTooltips()` or `setupPMTooltipSystem()` function exists?
3. `pm-tooltips-ready` event fired?

**Debug:**
```javascript
window.addEventListener('pm-tooltips-ready', () => {
  console.log('Tooltips initialized!');
});
```

## Advanced Usage

### Custom Formatters

Add custom format handlers:

```javascript
// Extend formatPMValue function
function customFormat(value, format) {
  if (format === 'custom:log10') {
    return Math.log10(value).toFixed(2);
  }
  // Fall back to default
  return formatPMValue(value, format);
}
```

### Dynamic Page Content Injection

Use page content from Firestore:

```javascript
const result = await loadPageFromFirebase('dynamic-page');
if (result.data.pageContent) {
  // Page content automatically injected to #main-content
  console.log('Dynamic content loaded');
}
```

### Event-Based Workflows

Chain multiple operations:

```javascript
let pmDataLoaded = false;
let tooltipsReady = false;

window.addEventListener('pm-page-loaded', () => {
  pmDataLoaded = true;
  checkReady();
});

window.addEventListener('pm-tooltips-ready', () => {
  tooltipsReady = true;
  checkReady();
});

function checkReady() {
  if (pmDataLoaded && tooltipsReady) {
    console.log('Page fully initialized!');
    startApplication();
  }
}
```

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

## Related Files

- `h:/Github/PrincipiaMetaphysica/js/firebase-page-loader.js` - Main module
- `h:/Github/PrincipiaMetaphysica/js/firebase-page-loader-integration.md` - Integration guide
- `h:/Github/PrincipiaMetaphysica/test-firebase-page-loader.html` - Test page
- `h:/Github/PrincipiaMetaphysica/js/auth-guard.js` - Authentication integration
- `h:/Github/PrincipiaMetaphysica/js/firebase-data.js` - Firebase data module
- `h:/Github/PrincipiaMetaphysica/js/pm-tooltip-system.js` - Tooltip system
