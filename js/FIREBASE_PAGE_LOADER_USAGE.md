# Firebase Page Loader - Usage Guide

## Overview

The `firebase-page-loader.js` module provides a comprehensive solution for loading page content and PM theory constants from Firebase Firestore. It features intelligent caching, automatic value population, and event-driven architecture.

**Location:** `h:/Github/PrincipiaMetaphysica/js/firebase-page-loader.js`

## Key Features

1. **Loads theory constants** from `theory_constants/current` document
2. **Loads page content** from `pages/{pageId}` collection
3. **Populates PM values** dynamically on the page
4. **Session caching** (5-minute TTL) to reduce Firestore calls
5. **Nested path support** (e.g., `vev_pure.v_GeV`)
6. **Event-driven** architecture for other scripts to hook into
7. **Automatic value formatting** (scientific notation, precision)
8. **Error handling** with fallback mechanisms

## Installation

### 1. Import Firebase Configuration

Make sure Firebase is initialized first:

```html
<script type="module" src="/js/firebase-config.js"></script>
```

### 2. Import the Page Loader

```html
<script type="module">
  import { initPageFromFirebase } from '/js/firebase-page-loader.js';

  // Initialize after DOM is ready
  document.addEventListener('DOMContentLoaded', async () => {
    await initPageFromFirebase('index');
  });
</script>
```

## Basic Usage

### Initialize a Page

```javascript
import { initPageFromFirebase } from '/js/firebase-page-loader.js';

// Call this after authentication succeeds
const pmData = await initPageFromFirebase('fermion-sector');

// PM data is now available globally as window.PM
console.log(window.PM);
```

### Integration with Auth Guard

The module works seamlessly with `auth-guard.js`:

```javascript
import { setupAuthGuard } from '/js/auth-guard.js';
import { initPageFromFirebase } from '/js/firebase-page-loader.js';

// Set up auth guard
setupAuthGuard('fermion-sector');

// Listen for authentication
window.addEventListener('pm-data-ready', (event) => {
  console.log('PM data loaded:', event.detail.pmData);
  console.log('Page content:', event.detail.pageContent);
  console.log('Page ID:', event.detail.pageId);
});
```

## HTML Markup for PM Values

### Method 1: Simple Category + Parameter

```html
<span class="pm-value"
      data-category="v12_7_pure_geometric"
      data-param="vev_pure">
  Loading...
</span>
```

### Method 2: Nested Parameters

```html
<span class="pm-value"
      data-category="v12_7_pure_geometric"
      data-param="vev_pure.v_GeV">
  Loading...
</span>
```

### Method 3: Deep Nesting

```html
<span class="pm-value"
      data-category="fermions"
      data-param="electron.mass.value">
  Loading...
</span>
```

## API Reference

### Primary Functions

#### `initPageFromFirebase(pageId)`

Initialize page with Firebase data.

**Parameters:**
- `pageId` (string): Page identifier (e.g., 'index', 'fermion-sector')

**Returns:** `Promise<Object>` - PM data object

**Example:**
```javascript
const pmData = await initPageFromFirebase('fermion-sector');
```

**Side Effects:**
- Sets `window.PM` to theory constants
- Sets `window.PageContent` to page content (if available)
- Dispatches `pm-data-ready` event
- Populates all `.pm-value` elements on page

---

#### `loadTheoryConstants()`

Load theory constants from Firestore with caching.

**Returns:** `Promise<Object>` - Theory constants object

**Example:**
```javascript
import { loadTheoryConstants } from '/js/firebase-page-loader.js';

const pmData = await loadTheoryConstants();
console.log(pmData.v12_7_pure_geometric);
```

**Caching:**
- 5-minute TTL
- Automatic cache invalidation
- Logs cache hits to console

---

#### `loadPageContent(pageId)`

Load page-specific content from Firestore.

**Parameters:**
- `pageId` (string): Page identifier

**Returns:** `Promise<Object|null>` - Page content or null if not found

**Example:**
```javascript
import { loadPageContent } from '/js/firebase-page-loader.js';

const pageData = await loadPageContent('fermion-sector');
if (pageData) {
  console.log('Title:', pageData.title);
  console.log('Description:', pageData.description);
}
```

---

#### `populatePMValues(pmData)`

Populate all `.pm-value` elements on the page.

**Parameters:**
- `pmData` (Object): PM theory constants object

**Returns:** `number` - Count of populated elements

**Example:**
```javascript
import { populatePMValues } from '/js/firebase-page-loader.js';

const count = populatePMValues(window.PM);
console.log(`Populated ${count} values`);
```

---

### Cache Management Functions

#### `clearCache()`

Clear all cached data (forces fresh Firestore fetch).

**Example:**
```javascript
import { clearCache } from '/js/firebase-page-loader.js';

clearCache();
```

---

#### `refreshPageData(pageId)`

Clear cache and reload page data.

**Parameters:**
- `pageId` (string): Page identifier

**Returns:** `Promise<Object>` - Fresh PM data

**Example:**
```javascript
import { refreshPageData } from '/js/firebase-page-loader.js';

const freshData = await refreshPageData('fermion-sector');
```

---

#### `getCacheStatus()`

Get cache status for debugging.

**Returns:** `Object` with properties:
- `hasTheoryConstants` (boolean)
- `pageContentCount` (number)
- `cacheAge` (number|null) - milliseconds since cache update
- `ttl` (number) - cache TTL in milliseconds

**Example:**
```javascript
import { getCacheStatus } from '/js/firebase-page-loader.js';

const status = getCacheStatus();
console.log('Cache status:', status);
// {
//   hasTheoryConstants: true,
//   pageContentCount: 2,
//   cacheAge: 45000,
//   ttl: 300000
// }
```

## Events

### `pm-data-ready`

Dispatched when page data is successfully loaded.

**Event Detail:**
```javascript
{
  pmData: Object,      // Theory constants
  pageContent: Object, // Page content (or null)
  pageId: string       // Page identifier
}
```

**Example:**
```javascript
window.addEventListener('pm-data-ready', (event) => {
  const { pmData, pageContent, pageId } = event.detail;
  console.log(`Data ready for ${pageId}`);

  // Initialize tooltips or other UI
  initializeTooltips(pmData);
});
```

---

### `pm-data-error`

Dispatched when data loading fails.

**Event Detail:**
```javascript
{
  error: string,  // Error message
  pageId: string  // Page identifier
}
```

**Example:**
```javascript
window.addEventListener('pm-data-error', (event) => {
  console.error(`Error loading ${event.detail.pageId}:`, event.detail.error);

  // Show error message to user
  showErrorNotification(event.detail.error);
});
```

## Value Formatting

The module automatically formats numeric values:

### Formatting Rules

1. **Large numbers** (≥ 1e6): Scientific notation with 4 decimals
   - `1234567.89` → `1.2346e+6`

2. **Small numbers** (< 0.01 and ≠ 0): Scientific notation with 4 decimals
   - `0.00123` → `1.2300e-3`

3. **Regular numbers**: 6 significant figures
   - `123.456789` → `123.457`

4. **Strings**: Returned as-is
   - `"Standard Model"` → `"Standard Model"`

### Custom Formatting (Future)

To use custom formatting, you can extend the `formatValue` function or handle it in your own code:

```javascript
// Get raw value without formatting
const category = 'v12_7_pure_geometric';
const param = 'vev_pure.v_GeV';
const rawValue = window.PM[category].vev_pure.v_GeV;

// Apply custom formatting
const formatted = rawValue.toFixed(2) + ' GeV';
```

## Firestore Data Structure

### Theory Constants Document

**Path:** `theory_constants/current`

**Structure:**
```javascript
{
  v12_7_pure_geometric: {
    vev_pure: {
      v_GeV: 246.22,
      v_MeV: 246220,
      description: "VEV from pure geometric computation"
    },
    // ... more parameters
  },
  fermions: {
    electron: {
      mass: {
        value: 0.511,
        unit: "MeV",
        uncertainty: 0.001
      }
    }
  },
  // ... more categories
}
```

### Page Content Document

**Path:** `pages/{pageId}`

**Structure:**
```javascript
{
  title: "Fermion Sector Analysis",
  description: "Detailed analysis of fermion masses...",
  sections: [
    {
      heading: "Introduction",
      content: "..."
    }
  ],
  metadata: {
    lastUpdated: "2025-12-13",
    author: "Andrew K Watts"
  }
}
```

## Performance Considerations

### Caching Strategy

- **5-minute TTL**: Balances freshness vs. performance
- **Session-based**: Cache cleared on page refresh
- **Granular**: Theory constants and page content cached separately

### Load Optimization

```javascript
// Good: Parallel loading
Promise.all([
  loadTheoryConstants(),
  loadPageContent('index')
]).then(([pmData, pageContent]) => {
  // Both loaded simultaneously
});

// Bad: Sequential loading
const pmData = await loadTheoryConstants();
const pageContent = await loadPageContent('index');
```

### Firestore Reads

- **First visit**: 1-2 reads (theory constants + page content)
- **Cached**: 0 reads
- **After 5 minutes**: 1-2 reads (cache refresh)

## Troubleshooting

### Values Not Populating

**Symptom:** PM values show "Loading..." or empty

**Causes:**
1. Missing `data-category` or `data-param` attributes
2. Incorrect category/param path
3. Firebase not initialized
4. Data not in Firestore

**Solution:**
```javascript
// Check if PM data loaded
console.log('PM data:', window.PM);

// Check cache status
import { getCacheStatus } from '/js/firebase-page-loader.js';
console.log('Cache:', getCacheStatus());

// Verify element attributes
const el = document.querySelector('.pm-value');
console.log('Category:', el.getAttribute('data-category'));
console.log('Param:', el.getAttribute('data-param'));
```

---

### Cache Not Working

**Symptom:** Multiple Firestore reads for same page

**Causes:**
1. Cache TTL expired (> 5 minutes)
2. Cache manually cleared
3. Page refreshed

**Solution:**
```javascript
// Check cache age
import { getCacheStatus } from '/js/firebase-page-loader.js';
const status = getCacheStatus();
console.log('Cache age (ms):', status.cacheAge);
console.log('TTL (ms):', status.ttl);

// Extend TTL if needed (edit cache.CACHE_TTL in source)
```

---

### Event Not Firing

**Symptom:** `pm-data-ready` event listener not called

**Causes:**
1. Listener added after event dispatched
2. Error during data loading

**Solution:**
```javascript
// Add listener before initializing
window.addEventListener('pm-data-ready', (event) => {
  console.log('Data ready!', event.detail);
});

// Also listen for errors
window.addEventListener('pm-data-error', (event) => {
  console.error('Data error!', event.detail);
});

// Then initialize
await initPageFromFirebase('index');
```

## Example: Complete Page Setup

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Fermion Sector - Principia Metaphysica</title>
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
  <div id="main-content">
    <h1>Fermion Sector Analysis</h1>

    <p>
      The electron mass is
      <span class="pm-value"
            data-category="fermions"
            data-param="electron.mass.value">
        Loading...
      </span> MeV.
    </p>

    <p>
      The VEV is
      <span class="pm-value"
            data-category="v12_7_pure_geometric"
            data-param="vev_pure.v_GeV">
        Loading...
      </span> GeV.
    </p>
  </div>

  <script type="module">
    import { initPageFromFirebase } from '/js/firebase-page-loader.js';
    import { setupAuthGuard } from '/js/auth-guard.js';

    // Set up authentication guard
    setupAuthGuard('fermion-sector');

    // Listen for data ready
    window.addEventListener('pm-data-ready', (event) => {
      console.log('Page initialized!');
      console.log('PM data:', event.detail.pmData);

      // Initialize tooltips, charts, etc.
      initializePageFeatures();
    });

    // Listen for errors
    window.addEventListener('pm-data-error', (event) => {
      console.error('Failed to load data:', event.detail.error);
      showErrorMessage('Unable to load page data. Please refresh.');
    });

    // Helper functions
    function initializePageFeatures() {
      // Initialize tooltips
      if (window.setupPMTooltipSystem) {
        window.setupPMTooltipSystem();
      }

      // Initialize charts, etc.
      // ...
    }

    function showErrorMessage(message) {
      alert(message);
    }
  </script>
</body>
</html>
```

## Migration from Old System

If you're migrating from the old `firebase-data.js` system:

### Old Code
```javascript
import { loadAllPageData } from '/js/firebase-data.js';

const data = await loadAllPageData('index');
window.PM = data.PM;
```

### New Code
```javascript
import { initPageFromFirebase } from '/js/firebase-page-loader.js';

await initPageFromFirebase('index');
// window.PM is set automatically
```

### Key Differences

1. **Simpler API**: One function instead of multiple
2. **Automatic population**: No need to manually populate PM values
3. **Event-driven**: Use events instead of return values
4. **Better caching**: Session-based with configurable TTL
5. **Error handling**: Dedicated error events

## Best Practices

1. **Initialize early**: Call `initPageFromFirebase()` as soon as authentication succeeds
2. **Use events**: Listen to `pm-data-ready` for initialization tasks
3. **Handle errors**: Always listen to `pm-data-error` event
4. **Cache wisely**: Don't clear cache unnecessarily
5. **Nested paths**: Use dot notation for nested values (`vev_pure.v_GeV`)
6. **Consistent naming**: Use consistent `pageId` across system
7. **Check console**: Module logs all operations to console

## Security Considerations

1. **Firebase Rules**: Ensure Firestore security rules protect data
2. **Authentication**: Always use with auth-guard.js
3. **API Keys**: Firebase config is public (this is normal)
4. **Data Validation**: Validate data from Firestore before use

## Support

For issues or questions:
1. Check console for error messages
2. Use `getCacheStatus()` for debugging
3. Verify Firestore data structure
4. Check Firebase Console for read counts

---

**Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.**
