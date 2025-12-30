# Firebase Page Loader - Quick Start

## 1. Import the Module

```html
<script type="module">
  import { initPageFromFirebase } from '/js/firebase-page-loader.js';
</script>
```

## 2. Add PM Values to HTML

```html
<span class="pm-value"
      data-category="v12_7_pure_geometric"
      data-param="vev_pure.v_GeV">
  Loading...
</span>
```

## 3. Initialize After Auth

```javascript
// Option A: Direct initialization
await initPageFromFirebase('your-page-id');

// Option B: With auth-guard.js (recommended)
import { setupAuthGuard } from '/js/auth-guard.js';
setupAuthGuard('your-page-id');

window.addEventListener('pm-data-ready', (event) => {
  console.log('Data loaded!', event.detail.pmData);
});
```

## 4. Access PM Data

```javascript
// PM data is available globally
console.log(window.PM);

// Example: Get VEV value
const vev = window.PM.v12_7_pure_geometric.vev_pure.v_GeV;
console.log('VEV:', vev, 'GeV');
```

## Common Patterns

### Pattern 1: Simple Value
```html
<span class="pm-value"
      data-category="fundamental_scales"
      data-param="M_Planck">
  Loading...
</span>
```

### Pattern 2: Nested Value
```html
<span class="pm-value"
      data-category="fermions"
      data-param="electron.mass.value">
  Loading...
</span>
```

### Pattern 3: Deep Nesting
```html
<span class="pm-value"
      data-category="v12_7_pure_geometric"
      data-param="vev_pure.v_GeV">
  Loading...
</span>
```

## Cache Management

```javascript
import { clearCache, refreshPageData } from '/js/firebase-page-loader.js';

// Clear cache
clearCache();

// Refresh data
await refreshPageData('your-page-id');
```

## Debugging

```javascript
import { getCacheStatus } from '/js/firebase-page-loader.js';

// Check cache
console.log(getCacheStatus());

// Check PM data
console.log('PM loaded:', !!window.PM);
console.log('Categories:', Object.keys(window.PM));
```

## Events

```javascript
// Success
window.addEventListener('pm-data-ready', (event) => {
  const { pmData, pageContent, pageId } = event.detail;
  // Initialize your features here
});

// Error
window.addEventListener('pm-data-error', (event) => {
  console.error('Error:', event.detail.error);
});
```

## Complete Example

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Page</title>
</head>
<body>
  <h1>PM Theory Constants</h1>

  <p>VEV: <span class="pm-value"
                  data-category="v12_7_pure_geometric"
                  data-param="vev_pure.v_GeV">...</span> GeV</p>

  <script type="module">
    import { initPageFromFirebase } from '/js/firebase-page-loader.js';

    window.addEventListener('pm-data-ready', () => {
      console.log('Ready!');
    });

    await initPageFromFirebase('my-page');
  </script>
</body>
</html>
```

## Firestore Structure

```
theory_constants/current
  └── {
        v12_7_pure_geometric: { ... },
        fermions: { ... },
        fundamental_scales: { ... }
      }

pages/{pageId}
  └── { title, description, sections, metadata }
```

## Tips

- Use `data-category` + `data-param` for all PM values
- Use dot notation for nested paths (`vev_pure.v_GeV`)
- Always handle `pm-data-error` event
- Cache expires after 5 minutes
- Check browser console for detailed logs
- Values auto-format (scientific notation for large/small numbers)

## Files

- **Module:** `h:/Github/PrincipiaMetaphysica/js/firebase-page-loader.js`
- **Full Docs:** `h:/Github/PrincipiaMetaphysica/js/FIREBASE_PAGE_LOADER_USAGE.md`
- **Example:** `h:/Github/PrincipiaMetaphysica/js/INTEGRATION_EXAMPLE.html`

---

**Need help?** Check the full documentation or integration example.
