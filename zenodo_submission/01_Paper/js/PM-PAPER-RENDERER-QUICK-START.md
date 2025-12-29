# PM Paper Renderer - Quick Start Guide

## Installation (3 lines)

```html
<script src="js/pm-constants-loader.js"></script>
<script src="js/pm-formula-loader.js"></script>
<script src="js/pm-paper-renderer.js"></script>
```

## Basic Usage (2 lines)

```javascript
// Render entire paper
await PMPaperRenderer.renderPaper('paper-container');
```

## Complete Minimal Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Paper</title>

    <!-- MathJax -->
    <script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>

    <!-- PM Loaders -->
    <script src="js/pm-constants-loader.js"></script>
    <script src="js/pm-formula-loader.js"></script>
    <script src="js/pm-paper-renderer.js"></script>
</head>
<body>
    <div id="paper"></div>

    <script>
        window.addEventListener('load', async () => {
            await PMPaperRenderer.renderPaper('paper');
        });
    </script>
</body>
</html>
```

## Common Tasks

### Render Paper with Options
```javascript
await PMPaperRenderer.renderPaper('container', {
    loadSections: true,      // Load section HTML files
    loadFormulas: true,      // Process formulas
    loadParameters: true,    // Process parameters
    renderAbstract: true,    // Show abstract
    renderTOC: true,         // Show table of contents
    debug: false             // Debug logging
});
```

### Render Single Section
```javascript
const section = PMPaperRenderer.data.sections['2'];
const sectionEl = await PMPaperRenderer.renderSection(section);
document.getElementById('container').appendChild(sectionEl);
```

### Get Formula HTML
```javascript
const html = PMPaperRenderer.renderFormula('generation-number');
```

### Process Existing Content
```javascript
const div = document.getElementById('my-content');
PMPaperRenderer.processFormulas(div);
PMPaperRenderer.processParameters(div);
PMPaperRenderer.typesetMathJax(div);
```

## Data Attributes

### Formulas
```html
<div data-formula-id="generation-number"></div>
```

### Parameters
```html
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>
<span data-pm-value="parameters.topology.n_gen" data-format="fixed:2"></span>
```

### Format Options
- `scientific:2` → 1.23e+10
- `fixed:2` → 123.45
- `percent` → 12.3%
- `integer` → 123

## API Quick Reference

| Function | Purpose |
|----------|---------|
| `renderPaper(id, opts)` | Render complete paper |
| `renderSection(section, opts)` | Render single section |
| `renderFormula(id)` | Get formula HTML |
| `processFormulas(el)` | Process formula refs in element |
| `processParameters(el)` | Process param refs in element |
| `typesetMathJax(el)` | Trigger MathJax on element |

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `PMPaperRenderer.data` | Object | theory_output.json data |
| `PMPaperRenderer.loaded` | Boolean | Is data loaded? |

## Debugging

### Enable Debug Mode
```javascript
await PMPaperRenderer.renderPaper('container', { debug: true });
```

### Check Data
```javascript
console.log(PMPaperRenderer.data);           // All data
console.log(PMPaperRenderer.data.sections);  // All sections
console.log(PMPaperRenderer.loaded);         // Is loaded?
```

### Test Formula Lookup
```javascript
console.log(PM.formula('generation-number'));
```

### Test Parameter Lookup
```javascript
console.log(PM.get('parameters.topology.n_gen'));
```

## Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Could not load theory_output.json" | Run from web server, not file:// |
| Formulas showing "?" | Check formula ID exists in theory_output.json |
| Parameters showing "?" | Check parameter path, hover for details |
| MathJax not rendering | Ensure MathJax loads before rendering |
| Sections not loading | Check section files exist in sections/ |

## File Structure

```
project/
├── theory_output.json          # Main data file
├── js/
│   ├── pm-constants-loader.js  # Parameter loader
│   ├── pm-formula-loader.js    # Formula loader
│   └── pm-paper-renderer.js    # Paper renderer
└── sections/
    ├── introduction.html        # Section 1
    ├── geometric-framework.html # Section 2
    └── ...
```

## CSS Classes Added

- `.pm-paper-container` - Main container
- `.paper-section` - Each section
- `.section-title` - Section title
- `.section-number` - Section number badge
- `.paper-toc` - Table of contents
- `.pm-loaded` - Successfully loaded value
- `.pm-error` - Error loading value

## Example Styling

```css
.pm-paper-container {
    max-width: 900px;
    margin: 0 auto;
    font-family: Georgia, serif;
}

.section-title {
    font-size: 2rem;
    color: #8b7fff;
}

.pm-loaded {
    color: #8b7fff;
    font-weight: 600;
}

.pm-error {
    color: #ff4444;
}
```

## Testing

### Test Files Provided
- `test-paper-renderer.html` - Interactive test page
- `examples/dynamic-paper-example.html` - Complete example

### Manual Test
1. Open `test-paper-renderer.html`
2. Click "Render Full Paper"
3. Verify sections appear
4. Check formulas render
5. Verify parameters populate

## Next Steps

1. See `js/README-pm-paper-renderer.md` for full documentation
2. Check `examples/dynamic-paper-example.html` for complete example
3. Review `PM_PAPER_RENDERER_SUMMARY.md` for implementation details

## Version

Version 1.0.0 - Released 2025-12-26

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
