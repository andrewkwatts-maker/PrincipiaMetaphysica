# PM Formula Loader - Quick Reference Card

## Installation

```html
<!-- Include MathJax -->
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<!-- Include PM Formula Loader -->
<script src="js/pm-formula-loader.js"></script>
```

---

## Basic Usage

### Auto-render (Recommended)

```html
<!-- Formulas render automatically on page load -->
<div data-formula-id="generation-number"></div>
<div data-formula-id="fine-structure-constant"></div>
<div data-formula-id="proton-electron-mass-ratio"></div>
```

### Manual Render

```javascript
await PMFormulaLoader.load();
PMFormulaLoader.render(element, 'generation-number');
```

---

## Options

### Via JavaScript

```javascript
PMFormulaLoader.render(element, formulaId, {
    showTitle: true,        // Show header with title/category
    showPlainText: true,    // Show plain text toggle
    expandable: true,       // Enable expandable panel
    interactive: true,      // Enable hover effects
    compact: false          // Use compact spacing
});
```

### Via Data Attributes

```html
<div data-formula-id="generation-number"
     data-show-title="true"
     data-show-plaintext="true"
     data-expandable="true"
     data-interactive="true"
     data-compact="false"></div>
```

---

## Common Patterns

### Grid Layout

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1.5rem;">
    <div data-formula-id="generation-number" data-compact="true"></div>
    <div data-formula-id="fine-structure-constant" data-compact="true"></div>
    <div data-formula-id="proton-electron-mass-ratio" data-compact="true"></div>
</div>
```

### Minimal Display

```html
<div data-formula-id="generation-number"
     data-show-title="false"
     data-show-plaintext="false"
     data-expandable="false"></div>
```

### Non-Interactive

```html
<div data-formula-id="generation-number"
     data-interactive="false"></div>
```

### Compact Mode

```html
<div data-formula-id="generation-number"
     data-compact="true"></div>
```

---

## API Methods

### Load Formulas

```javascript
await PMFormulaLoader.load();
// Returns: true if loaded successfully
```

### Get Formula

```javascript
const formula = PMFormulaLoader.get('generation-number');
// Returns: Formula object or null
```

### Get All Formulas

```javascript
const formulas = PMFormulaLoader.getAll();
// Returns: Object with all formulas keyed by ID
```

### Get by Category

```javascript
const theoryFormulas = PMFormulaLoader.getByCategory('THEORY');
// Returns: Array of formulas in category
```

### Get by Section

```javascript
const section4Formulas = PMFormulaLoader.getBySection('4');
// Returns: Array of formulas in section
```

### Search

```javascript
const results = PMFormulaLoader.search('generation');
// Returns: Array of matching formulas
```

### Get Stats

```javascript
const stats = PMFormulaLoader.getStats();
// Returns: { loaded, version, total, categories, ... }
```

### Render Single

```javascript
PMFormulaLoader.render(element, 'generation-number', options);
// Returns: true if successful
```

### Render All

```javascript
PMFormulaLoader.renderAll();
// Renders all elements with data-formula-id
```

---

## Data Attributes Reference

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `data-formula-id` | string | required | Formula ID to render |
| `data-show-title` | boolean | true | Show header section |
| `data-show-plaintext` | boolean | true | Show plain text toggle |
| `data-expandable` | boolean | true | Enable expandable panel |
| `data-interactive` | boolean | true | Enable hover effects |
| `data-compact` | boolean | false | Use compact spacing |

---

## Formula Object Structure

```javascript
{
    id: "generation-number",
    equationNumber: "Eq. 4.1",
    category: "THEORY",
    description: "Number of fermion generations",
    latex: "N_g = 3",
    plainText: "N_g = 3",
    inputParams: [],
    outputParams: ["N_g"],
    derivedFrom: [],
    terms: {
        "N_g": "Number of fermion generations"
    },
    section: "4.1 Generation Number"
}
```

---

## CSS Classes

### Container Classes

- `.pm-formula-container` - Wrapper element
- `.pm-formula-card` - Card container
- `.pm-formula-card.interactive` - Interactive hover effects
- `.pm-formula-card.compact` - Compact spacing
- `.pm-formula-card.expanded` - Expanded state

### Header Classes

- `.pm-formula-header` - Header section
- `.pm-formula-title-row` - Title row flex container
- `.pm-formula-eq-num` - Equation number
- `.pm-formula-title` - Formula title
- `.pm-formula-category` - Category badge
- `.pm-formula-subtitle` - Description text

### Display Classes

- `.pm-formula-display` - Display section
- `.pm-formula-latex` - LaTeX formula
- `.pm-formula-plaintext` - Plain text container
- `.pm-plaintext-toggle` - Toggle button
- `.pm-plaintext-code` - Plain text code block

### Details Classes

- `.pm-formula-expandable` - Expandable section
- `.pm-expand-btn` - Expand button
- `.pm-formula-details` - Details panel
- `.pm-formula-params` - Parameters section
- `.pm-formula-derived` - Derivation section
- `.pm-formula-terms` - Terms section
- `.pm-formula-section` - Section reference

### Utility Classes

- `.pm-formula-error` - Error message
- `.pm-formula-link` - Formula link

---

## Color Variables

```css
/* Primary Colors */
--pm-purple: #8b7fff;
--pm-purple-light: #a394ff;
--pm-text: #f8f9fa;
--pm-code: #a3e635;

/* Backgrounds */
--pm-card-bg: rgba(255, 255, 255, 0.03);
--pm-header-bg: rgba(139, 127, 255, 0.05);
--pm-details-bg: rgba(0, 0, 0, 0.2);
--pm-code-bg: rgba(0, 0, 0, 0.3);

/* Borders */
--pm-border: rgba(255, 255, 255, 0.1);
--pm-border-hover: rgba(139, 127, 255, 0.4);

/* Shadows */
--pm-shadow-hover: 0 4px 20px rgba(139, 127, 255, 0.15);
```

---

## Examples

### Simple Formula

```html
<div data-formula-id="generation-number"></div>
```

### Compact Grid

```html
<div class="formula-grid">
    <div data-formula-id="generation-number" data-compact="true"></div>
    <div data-formula-id="fine-structure-constant" data-compact="true"></div>
</div>
```

### Custom Styling

```html
<style>
.custom-formula .pm-formula-card {
    background: rgba(0, 100, 200, 0.1);
    border-color: rgba(0, 200, 255, 0.3);
}
</style>

<div class="custom-formula" data-formula-id="generation-number"></div>
```

### Manual Rendering

```javascript
// Wait for DOM and formulas
document.addEventListener('DOMContentLoaded', async () => {
    await PMFormulaLoader.load();

    // Render specific formula
    const target = document.getElementById('my-formula');
    PMFormulaLoader.render(target, 'generation-number', {
        showTitle: true,
        compact: false
    });

    // Log stats
    console.log(PMFormulaLoader.getStats());
});
```

---

## Troubleshooting

### Formulas Not Rendering

1. Check `theory_output.json` exists
2. Run local web server (file:// may not work)
3. Check browser console for errors
4. Verify formula ID is correct

### MathJax Not Working

1. Ensure MathJax is loaded before formulas
2. Check MathJax CDN is accessible
3. Wait for MathJax to initialize

### Styles Not Applied

1. Styles auto-inject on first render
2. Check for `#pm-formula-styles` in `<head>`
3. Override with `!important` if needed

### Performance Issues

1. Use `data-compact="true"` for grids
2. Limit expanded panels (close when not needed)
3. Consider lazy loading for many formulas

---

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+
- ❌ IE11 (not supported)

---

## Dependencies

- **MathJax 3.x** (required for LaTeX rendering)
- **Modern JavaScript** (ES6+)
- **No CSS framework** required
- **No jQuery** required

---

## File Size

- **JavaScript**: ~31 KB (uncompressed)
- **Auto-injected CSS**: ~8 KB
- **Total overhead**: ~39 KB
- **Minified**: ~20 KB (estimated)

---

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

---

## Support

For issues or questions:
1. Check `ENHANCED_FORMULA_LOADER.md` for detailed docs
2. See `test-enhanced-formulas.html` for examples
3. Review `FORMULA_LOADER_COMPARISON.md` for migration

---

## Version

- **Enhanced Version**: 2.0
- **File**: `js/pm-formula-loader.js`
- **Lines**: 775
- **Last Updated**: 2025-12-26
