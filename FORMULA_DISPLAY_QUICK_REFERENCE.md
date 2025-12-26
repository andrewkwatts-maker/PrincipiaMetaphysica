# Formula Display - Quick Reference Card

## 🚀 Quick Start

### Include Script
```html
<script src="js/pm-formula-loader.js"></script>
```

### Display a Formula
```html
<div data-formula-id="generation-number"></div>
```

That's it! The formula will automatically render when the page loads.

---

## 📋 Common Usage Patterns

### Pattern 1: Simple Display (Most Common)
```html
<div data-formula-id="gut-scale"></div>
```

### Pattern 2: Web Component
```html
<pm-formula data-id="w0-formula" show-derivation="true"></pm-formula>
```
*Requires: `<script src="js/pm-formula-component.js"></script>`*

### Pattern 3: Programmatic
```javascript
const element = document.getElementById('my-container');
PMFormulaLoader.render(element, 'alpha-gut', {
    showLabel: true,
    showPlainText: false
});
```

---

## 🔍 Finding Formula IDs

### Method 1: Search by keyword
```javascript
PMFormulaLoader.search('neutrino');
```

### Method 2: Browse by category
```javascript
PMFormulaLoader.getByCategory('PREDICTIONS');
```

### Method 3: Check the JSON file
`AUTO_GENERATED/json/formulas.json` contains all formula IDs

---

## 📊 Available Formula IDs

### Topological Predictions
- `generation-number` - Why 3 generations
- `euler-characteristic` - TCS G₂ topology
- `tcs-topology` - TCS construction

### GUT Scale
- `gut-scale` - Grand unification scale
- `alpha-gut` - GUT coupling constant

### Dark Energy
- `d-eff-formula` - Effective dimension
- `w0-formula` - Dark energy equation of state

### Neutrino Physics
- `theta23-maximal` - Atmospheric mixing angle
- `theta12-solar` - Solar mixing angle
- `normal-hierarchy` - Neutrino mass hierarchy

### Predictions
- `proton-lifetime` - Proton decay rate
- `kk-graviton-mass` - KK graviton mass
- `gw-dispersion` - Gravitational wave dispersion

*See full list: `PMFormulaLoader.getAll()`*

---

## ⚙️ Rendering Options

```javascript
PMFormulaLoader.render(element, formulaId, {
    showLabel: true,      // Show "(4.2) Three Generations"
    showPlainText: false, // Show ASCII version
    showDerivation: false,// Show derivation info
    className: 'custom'   // Custom CSS class
});
```

---

## 🎨 Styling

### Default Classes
```css
.pm-formula-rendered {
    /* Container */
}

.formula-label {
    /* "(4.2) Three Generations" */
}

.formula-display {
    /* Main formula content */
}
```

### Example Custom Styling
```css
.pm-formula-rendered {
    background: linear-gradient(135deg, rgba(139, 127, 255, 0.1), transparent);
    border-left: 4px solid #8b7fff;
    padding: 1.5rem;
    margin: 2rem 0;
}

.formula-display {
    font-size: 1.5rem;
    text-align: center;
    color: #e0e0e0;
}
```

---

## 🐛 Troubleshooting

### Problem: Formulas not showing
**Solution:**
```bash
# 1. Generate JSON file
python run_all_simulations.py --export

# 2. Start local server (if using file://)
python -m http.server 8000

# 3. Check console for errors
```

### Problem: "Formula not found: xyz"
**Solution:**
```javascript
// List all available formulas
console.log(Object.keys(PMFormulaLoader.getAll()));

// Or search
PMFormulaLoader.search('xyz');
```

### Problem: Want to see what's loaded?
**Solution:**
```javascript
// Get stats
console.log(PMFormulaLoader.getStats());

// See all formulas
console.log(window.PM_FORMULAS);

// Enable debug mode
window.PM_DEBUG = true;
```

---

## 📱 API Quick Reference

| Method | Purpose | Example |
|--------|---------|---------|
| `load()` | Load formulas | `await PMFormulaLoader.load()` |
| `get(id)` | Get one formula | `PMFormulaLoader.get('gut-scale')` |
| `getAll()` | Get all formulas | `PMFormulaLoader.getAll()` |
| `render(el, id, opts)` | Render formula | `PMFormulaLoader.render(div, 'w0-formula')` |
| `renderAll()` | Render all in DOM | `PMFormulaLoader.renderAll()` |
| `getByCategory(cat)` | Filter by category | `PMFormulaLoader.getByCategory('THEORY')` |
| `search(query)` | Search formulas | `PMFormulaLoader.search('neutrino')` |
| `getStats()` | Get statistics | `PMFormulaLoader.getStats()` |

---

## 🧪 Testing

**Test page:** `test-formula-loader.html`

```bash
python -m http.server 8000
# Visit: http://localhost:8000/test-formula-loader.html
```

---

## 📚 Full Documentation

See `PM_FORMULA_LOADER_GUIDE.md` for complete documentation.

---

## ✅ Checklist for New Pages

- [ ] Include `<script src="js/pm-formula-loader.js"></script>`
- [ ] Use `<div data-formula-id="..."></div>` for formulas
- [ ] Test that formulas render correctly
- [ ] Check browser console for errors
- [ ] Optionally include MathJax for LaTeX rendering

---

**Version:** 2.0 | **Updated:** 2025-12-25
