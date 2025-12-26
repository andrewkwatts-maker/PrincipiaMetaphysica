# PM Formula Loader - Complete Guide

## Overview

The PM Formula Loader system provides a unified way to display formulas from the Principia Metaphysica theory across the website. It automatically loads formula data from `AUTO_GENERATED/json/formulas.json` and renders them with proper formatting.

## Updated Features (v2.0)

### What's New
- ✅ Loads from `AUTO_GENERATED/json/formulas.json` (primary) or `theory_output.json` (fallback)
- ✅ Automatic DOM rendering with `data-formula-id` attribute
- ✅ Support for `<pm-formula data-id="...">` elements
- ✅ Manual rendering API: `PMFormulaLoader.render(element, formulaId, options)`
- ✅ MathJax integration (auto-triggers typesetting after rendering)
- ✅ Error handling with helpful messages for missing formulas
- ✅ Prevents double-rendering with `.pm-formula-rendered` class

## Installation

### 1. Include the Script

Add to your HTML `<head>` or before closing `</body>`:

```html
<script src="js/pm-formula-loader.js"></script>
```

Optional: Include the web component for advanced features:
```html
<script src="js/pm-formula-component.js"></script>
```

### 2. The loader auto-initializes on page load

No additional JavaScript needed! The loader will:
1. Auto-detect and load `AUTO_GENERATED/json/formulas.json`
2. Merge with `FORMULA_REGISTRY` if present
3. Render all formulas with `data-formula-id` or `data-id` attributes

## Usage

### Method 1: Simple div with data-formula-id (Recommended)

```html
<div data-formula-id="generation-number"></div>
```

This automatically renders:
- Formula label (if available)
- HTML/LaTeX formula
- Styled container with proper formatting

### Method 2: pm-formula element with data-id

```html
<pm-formula data-id="gut-scale"></pm-formula>
```

### Method 3: pm-formula web component (Advanced)

Requires `pm-formula-component.js`:

```html
<pm-formula formula-id="generation-number" show-derivation="true"></pm-formula>
```

**Attributes:**
- `formula-id` or `data-id`: Formula ID to display
- `show-label`: Show formula label (default: true)
- `show-derivation`: Show derivation chain (default: false)

### Method 4: Manual Rendering via JavaScript

```javascript
// Wait for loader to be ready
await PMFormulaLoader.load();

// Render into a specific element
const element = document.getElementById('my-formula-container');
PMFormulaLoader.render(element, 'w0-formula', {
    showLabel: true,
    showPlainText: true,
    showDerivation: false,
    className: 'my-custom-class'
});
```

## API Reference

### PMFormulaLoader.load()

Load formulas from JSON file.

```javascript
await PMFormulaLoader.load();
// or with custom path:
await PMFormulaLoader.load('path/to/formulas.json');
```

**Returns:** `Promise<boolean>` - true if loaded successfully

### PMFormulaLoader.get(id)

Get formula data by ID.

```javascript
const formula = PMFormulaLoader.get('generation-number');
console.log(formula.html);      // HTML representation
console.log(formula.latex);     // LaTeX representation
console.log(formula.plainText); // Plain text representation
console.log(formula.label);     // Formula label
```

**Returns:** `Object|null` - Formula object or null if not found

### PMFormulaLoader.render(element, formulaId, options)

Render a formula into a DOM element.

```javascript
PMFormulaLoader.render(
    document.getElementById('target'),
    'gut-scale',
    {
        showLabel: true,        // Show formula label
        showPlainText: false,   // Show plain text version
        showDerivation: false,  // Show derivation info
        className: 'custom-class' // Custom CSS class
    }
);
```

**Parameters:**
- `element` (HTMLElement): Target element
- `formulaId` (string): Formula ID
- `options` (Object): Rendering options

**Returns:** `boolean` - true if rendered successfully

### PMFormulaLoader.renderAll()

Render all formulas with `data-formula-id` or `data-id` attributes.

```javascript
PMFormulaLoader.renderAll();
```

Auto-called after loading, but can be manually triggered if new elements are added dynamically.

### PMFormulaLoader.getAll()

Get all loaded formulas.

```javascript
const allFormulas = PMFormulaLoader.getAll();
console.log(Object.keys(allFormulas)); // Array of formula IDs
```

**Returns:** `Object` - All formulas keyed by ID

### PMFormulaLoader.getByCategory(category)

Get formulas by category.

```javascript
const theoryFormulas = PMFormulaLoader.getByCategory('THEORY');
const predictions = PMFormulaLoader.getByCategory('PREDICTIONS');
```

**Parameters:**
- `category` (string): Category name (THEORY, DERIVED, PREDICTIONS, ESTABLISHED)

**Returns:** `Array` - Array of formula objects

### PMFormulaLoader.getBySection(section)

Get formulas by section number.

```javascript
const section4Formulas = PMFormulaLoader.getBySection('4');
const section5_3 = PMFormulaLoader.getBySection('5.3');
```

**Parameters:**
- `section` (string): Section number

**Returns:** `Array` - Array of formula objects

### PMFormulaLoader.search(query)

Search formulas by description or label.

```javascript
const results = PMFormulaLoader.search('neutrino');
results.forEach(f => console.log(f.label, f.description));
```

**Parameters:**
- `query` (string): Search query

**Returns:** `Array` - Matching formulas

### PMFormulaLoader.getStats()

Get statistics about loaded formulas.

```javascript
const stats = PMFormulaLoader.getStats();
console.log(`Loaded ${stats.total} formulas (v${stats.version})`);
console.log(stats.categories); // { THEORY: 12, DERIVED: 25, ... }
```

**Returns:** `Object` - Statistics object

## Formula Data Structure

Each formula in the JSON has this structure:

```json
{
  "generation-number": {
    "id": "generation-number",
    "label": "(4.2) Three Generations",
    "html": "n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3",
    "latex": "n_{gen} = \\frac{\\chi_{eff}}{48} = \\frac{144}{48} = 3",
    "plainText": "n_gen = χ_eff/48 = 144/48 = 3",
    "category": "DERIVED",
    "description": "Number of fermion generations from G₂ topology",
    "section": "4",
    "computedValue": 3,
    "experimentalValue": 3,
    "sigmaDeviation": 0.0
  }
}
```

## Styling

The rendered formulas have these CSS classes:

- `.pm-formula-rendered` - Container div (default)
- `.formula-label` - Formula label
- `.formula-display` - Main formula display
- `.formula-plaintext` - Plain text version
- `.formula-derivation` - Derivation info

You can customize styling in your CSS:

```css
.pm-formula-rendered {
    background: rgba(139, 127, 255, 0.05);
    border: 1px solid rgba(139, 127, 255, 0.2);
    border-radius: 8px;
    padding: 1rem;
}

.formula-display {
    font-family: 'Times New Roman', serif;
    font-size: 1.3rem;
    text-align: center;
}
```

## MathJax Integration

The loader automatically triggers MathJax typesetting after rendering formulas:

```javascript
// Supports both MathJax v2 and v3
// No additional configuration needed
```

Make sure MathJax is loaded before the formulas if you want LaTeX rendering:

```html
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script src="js/pm-formula-loader.js"></script>
```

## Error Handling

### Missing Formula

If a formula ID doesn't exist, an error message is displayed:

```html
<div data-formula-id="non-existent"></div>
```

Renders:
```
Formula not found: non-existent
Available formulas: generation-number, gut-scale, w0-formula...
```

### Loading Failures

If the JSON file can't be loaded, detailed error messages appear in the console:

```
PMFormulaLoader: Failed to load formulas!
  Tried paths: ['AUTO_GENERATED/json/formulas.json', ...]

  SOLUTIONS:
  1. Run: python run_all_simulations.py --export
  2. Check that AUTO_GENERATED/json/formulas.json exists
  3. If using file:// protocol, run a local web server
```

## Debugging

Enable verbose logging:

```javascript
window.PM_DEBUG = true;
```

Check loaded formulas:

```javascript
console.log(window.PM_FORMULAS); // All loaded formulas
console.log(PMFormulaLoader.getStats()); // Statistics
```

## Examples

### Example 1: Simple Formula Display

```html
<h2>Why 3 Generations?</h2>
<div data-formula-id="generation-number"></div>
<p>This formula derives the number of fermion generations from G₂ topology.</p>
```

### Example 2: Multiple Formulas

```html
<h2>Grand Unification</h2>
<div data-formula-id="gut-scale"></div>
<div data-formula-id="alpha-gut"></div>
```

### Example 3: Dynamic Rendering

```javascript
async function displayFormula(formulaId) {
    await PMFormulaLoader.load();

    const container = document.createElement('div');
    PMFormulaLoader.render(container, formulaId, { showDerivation: true });

    document.body.appendChild(container);
}

displayFormula('w0-formula');
```

### Example 4: Formula Gallery

```javascript
async function createFormulaGallery(category) {
    await PMFormulaLoader.load();

    const formulas = PMFormulaLoader.getByCategory(category);
    const gallery = document.getElementById('formula-gallery');

    formulas.forEach(f => {
        const div = document.createElement('div');
        PMFormulaLoader.render(div, f.id, {
            showLabel: true,
            showPlainText: true
        });
        gallery.appendChild(div);
    });
}

createFormulaGallery('PREDICTIONS');
```

## Migration from Old System

### Old (formula-database.js):
```javascript
const formula = FORMULA_DATABASE['generation-number'];
element.innerHTML = formula.html;
```

### New (pm-formula-loader.js):
```html
<!-- Automatic rendering -->
<div data-formula-id="generation-number"></div>

<!-- Or programmatic -->
<script>
const formula = PMFormulaLoader.get('generation-number');
PMFormulaLoader.render(element, 'generation-number');
</script>
```

## Troubleshooting

### Formulas not rendering?

1. Check console for errors
2. Verify `AUTO_GENERATED/json/formulas.json` exists
3. Run `python run_all_simulations.py --export` to regenerate
4. Check that script is loaded: `<script src="js/pm-formula-loader.js"></script>`

### Using file:// protocol?

Start a local web server:
```bash
python -m http.server 8000
# Then visit: http://localhost:8000
```

### Want to see what's loaded?

```javascript
console.log(PMFormulaLoader.getStats());
console.log(Object.keys(PMFormulaLoader.getAll()));
```

## Testing

A test page is available at `test-formula-loader.html` to verify functionality:

```bash
python -m http.server 8000
# Visit: http://localhost:8000/test-formula-loader.html
```

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
