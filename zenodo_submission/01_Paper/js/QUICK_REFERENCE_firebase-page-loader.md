# Firebase Page Loader - Quick Reference

## Import

```javascript
import { loadPageFromFirebase, populatePMValues, clearPageCache, refreshPageData } from './firebase-page-loader.js';
```

## Load Page

```javascript
const result = await loadPageFromFirebase('fermion-sector');
if (result.success) {
  console.log('Loaded:', result.fromCache ? 'from cache' : 'from Firebase');
}
```

## HTML Patterns

### Pattern 1: Category + Parameter
```html
<span class="pm-value" data-category="proton_decay" data-param="M_GUT" data-format="display"></span>
<span class="pm-value" data-category="pmns_matrix" data-param="theta_23" data-format="fixed:2"></span>
```

### Pattern 2: Nested Path
```html
<span class="pm-value" data-pm-value="v12_7_pure_geometric.vev_pure.v_GeV" data-format="fixed:3"></span>
<span class="pm-value" data-pm-value="v12_7_pure_geometric.flux_stab_pure.m_h_GeV" data-format="fixed:2"></span>
```

## Common Formats

| Format | Example |
|--------|---------|
| `display` | Pre-formatted (e.g., "2.12×10¹⁶") |
| `fixed:2` | 42.30 |
| `fixed:3` | 246.220 |
| `scientific:2` | 1.23e+16 |
| `percent:1` | 85.3% |

## Events

```javascript
// Page loaded
window.addEventListener('pm-page-loaded', (e) => {
  console.log('Page:', e.detail.pageId);
});

// Tooltips ready
window.addEventListener('pm-tooltips-ready', () => {
  console.log('Tooltips active');
});
```

## Cache Management

```javascript
// Clear all caches
clearPageCache();

// Refresh bypassing cache
await refreshPageData('page-id');
```

## Common Examples

### Proton Decay
```html
<span class="pm-value" data-category="proton_decay" data-param="M_GUT" data-format="display"></span> GeV
```

### PMNS Angles
```html
θ₂₃ = <span class="pm-value" data-category="pmns_matrix" data-param="theta_23" data-format="fixed:2"></span>°
```

### Gauge Coupling
```html
1/α_GUT = <span class="pm-value" data-category="gauge_unification" data-param="alpha_GUT_inv" data-format="fixed:2"></span>
```

### Nested Path (VEV)
```html
v = <span class="pm-value" data-pm-value="v12_7_pure_geometric.vev_pure.v_GeV" data-format="fixed:3"></span> GeV
```

## Test Page

Open: `h:/Github/PrincipiaMetaphysica/test-firebase-page-loader.html`

## Full Documentation

See: `h:/Github/PrincipiaMetaphysica/js/README-firebase-page-loader.md`
