# Firebase Page Loader Integration Guide

## Overview

The `firebase-page-loader.js` module provides comprehensive functionality for loading page content from Firebase Firestore and dynamically populating PM values from centralized theory_constants.

## Integration with auth-guard.js

To integrate the new page loader with the authentication guard, update `auth-guard.js` as follows:

### Step 1: Add Import

Add the import statement at the top of `auth-guard.js`:

```javascript
import { loadPageFromFirebase } from './firebase-page-loader.js';
```

The complete import section should look like:

```javascript
import { onAuthReady, signInWithGoogle, signOutUser, getUserInfo } from './firebase-auth.js';
import { initializeData, loadAllPageData } from './firebase-data.js';
import { loadPageFromFirebase } from './firebase-page-loader.js';
```

### Step 2: Update handleAuthenticated Function

Replace the data loading section in `handleAuthenticated()` function (lines 84-97):

**OLD CODE:**
```javascript
  // Initialize data from Firestore
  try {
    await initializeData();

    // Load page-specific data if needed
    if (currentPageId) {
      const pageData = await loadAllPageData(currentPageId);
      console.log(`[PM Auth Guard] Page data loaded for ${currentPageId}`);

      // Dispatch event for page-specific handling
      window.dispatchEvent(new CustomEvent('pm-data-ready', { detail: pageData }));
    }
  } catch (error) {
    console.error('[PM Auth Guard] Error initializing data:', error);
  }
```

**NEW CODE:**
```javascript
  // Initialize data from Firestore
  try {
    await initializeData();

    // Load page-specific data if needed
    if (currentPageId) {
      // Use the new firebase-page-loader module
      const result = await loadPageFromFirebase(currentPageId);

      if (result.success) {
        console.log(`[PM Auth Guard] Page loaded successfully for ${currentPageId}${result.fromCache ? ' (from cache)' : ''}`);
      } else {
        console.warn(`[PM Auth Guard] Page load failed, falling back to static content`);
        // loadPageFromFirebase already handles fallback internally
      }

      // Also load legacy page data for backward compatibility
      const pageData = await loadAllPageData(currentPageId);

      // Dispatch event for page-specific handling
      window.dispatchEvent(new CustomEvent('pm-data-ready', { detail: pageData }));
    }
  } catch (error) {
    console.error('[PM Auth Guard] Error initializing data:', error);
  }
```

## Usage in HTML Pages

### Pattern 1: Using data-category and data-param

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

### Pattern 2: Using data-pm-value (nested paths)

```html
<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.vev_pure.v_GeV"
      data-format="fixed:3"></span>

<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.flux_stab_pure.m_h_GeV"
      data-format="fixed:2"></span>

<span class="pm-value"
      data-pm-value="v12_7_pure_geometric.alpha_gut_pure.alpha_GUT_inv"
      data-format="fixed:2"></span>
```

## Supported Format Attributes

The `data-format` attribute supports the following values:

- `scientific:N` - Scientific notation with N decimal places (e.g., `1.23e+16`)
- `fixed:N` - Fixed decimal with N places (e.g., `24.54`)
- `percent:N` - Percentage with N decimal places (e.g., `85.3%`)
- `sigma:N` - Sigma notation (e.g., `2.46σ`)
- `eV:N` - Electron volts (e.g., `125.25 eV`)
- `GeV:N` - Giga electron volts (e.g., `246.220 GeV`)
- `TeV:N` - Tera electron volts (e.g., `2.12 TeV`)
- `years:N` - Years in scientific notation (e.g., `1.23e+35 years`)
- `display` - Use pre-formatted display string (no additional formatting)

## Events

### pm-page-loaded Event

Dispatched when page data has been successfully loaded and populated:

```javascript
window.addEventListener('pm-page-loaded', (event) => {
  const { pageId, pmData, pageContent, timestamp } = event.detail;
  console.log(`Page ${pageId} loaded at ${timestamp}`);
  console.log('PM Data:', pmData);
  console.log('Page Content:', pageContent);
});
```

### pm-tooltips-ready Event

Dispatched when tooltips have been initialized:

```javascript
window.addEventListener('pm-tooltips-ready', () => {
  console.log('Tooltips are now active');
});
```

## API Functions

### loadPageFromFirebase(pageId)

Loads page content from Firebase and populates PM values.

```javascript
import { loadPageFromFirebase } from './firebase-page-loader.js';

const result = await loadPageFromFirebase('fermion-sector');
if (result.success) {
  console.log('Page loaded:', result.data);
} else {
  console.error('Load failed:', result.error);
}
```

### populatePMValues(pmData)

Populates all `.pm-value` elements with data from PM object.

```javascript
import { populatePMValues } from './firebase-page-loader.js';

const count = populatePMValues(window.PM);
console.log(`Populated ${count} PM values`);
```

### refreshPageData(pageId)

Refreshes page data from Firebase, bypassing cache.

```javascript
import { refreshPageData } from './firebase-page-loader.js';

const result = await refreshPageData('index');
console.log('Data refreshed:', result);
```

### clearPageCache()

Clears all cached page data from sessionStorage.

```javascript
import { clearPageCache } from './firebase-page-loader.js';

clearPageCache();
console.log('Cache cleared');
```

## Testing Examples

### Example 1: Proton Decay Parameters

```html
<h3>Proton Decay Predictions</h3>
<p>
  GUT Scale: M<sub>GUT</sub> =
  <span class="pm-value"
        data-category="proton_decay"
        data-param="M_GUT"
        data-format="display"></span> GeV
</p>
<p>
  Proton Lifetime: τ<sub>p</sub> =
  <span class="pm-value"
        data-pm-value="v12_7_pure_geometric.proton_lifetime_predicted.tau_p_years"
        data-format="scientific:2"></span> years
</p>
```

### Example 2: PMNS Matrix Parameters

```html
<h3>PMNS Mixing Angles</h3>
<table>
  <tr>
    <td>θ<sub>12</sub></td>
    <td>
      <span class="pm-value"
            data-category="pmns_matrix"
            data-param="theta_12"
            data-format="fixed:2"></span>°
    </td>
  </tr>
  <tr>
    <td>θ<sub>23</sub></td>
    <td>
      <span class="pm-value"
            data-category="pmns_matrix"
            data-param="theta_23"
            data-format="fixed:2"></span>°
    </td>
  </tr>
  <tr>
    <td>θ<sub>13</sub></td>
    <td>
      <span class="pm-value"
            data-category="pmns_matrix"
            data-param="theta_13"
            data-format="fixed:2"></span>°
    </td>
  </tr>
</table>
```

### Example 3: Gauge Unification

```html
<h3>Gauge Coupling Unification</h3>
<p>
  Unified coupling at GUT scale:
  1/α<sub>GUT</sub> =
  <span class="pm-value"
        data-category="gauge_unification"
        data-param="alpha_GUT_inv"
        data-format="fixed:2"></span>
</p>
<p>
  From nested path:
  1/α<sub>GUT</sub> =
  <span class="pm-value"
        data-pm-value="v12_7_pure_geometric.alpha_gut_pure.alpha_GUT_inv"
        data-format="fixed:2"></span>
</p>
```

## Session Storage Cache

The module uses sessionStorage for caching with the following behavior:

- **Cache Key Format**: `pm_firebase_cache_{pageId}`
- **Cache Version**: `1.0` (automatically invalidated on version change)
- **Cache TTL**: 5 minutes
- **Cache Scope**: Per browser tab/window (not shared across tabs)

## Error Handling

The module includes comprehensive error handling:

1. **Firestore Connection Errors**: Falls back to static content
2. **Missing Data**: Logs warnings and skips element
3. **Invalid Format**: Logs warning and returns string representation
4. **Cache Errors**: Silently ignores and loads from Firestore

## Performance Considerations

- **Parallel Loading**: Theory constants and page content load in parallel
- **Session Caching**: Reduces Firebase reads for repeated page loads
- **Lazy Tooltip Init**: Tooltips initialize after DOM is fully populated
- **Batch Population**: All PM values populated in single DOM pass

## Backward Compatibility

The integration maintains backward compatibility:

- **Legacy loadAllPageData**: Still called for existing code
- **pm-data-ready Event**: Still dispatched for legacy listeners
- **Static Fallback**: Falls back to theory-constants-enhanced.js if Firebase fails
- **Existing Tooltip System**: Works with both old and new PM value patterns

## Migration Path

For existing pages using static PM values:

1. Add `data-category` and `data-param` attributes to existing `.pm-value` elements
2. Remove hardcoded values from HTML
3. Let `loadPageFromFirebase()` populate values dynamically
4. Test with Firebase and verify fallback to static works

No changes needed to pages that already follow the `.pm-value` pattern!
