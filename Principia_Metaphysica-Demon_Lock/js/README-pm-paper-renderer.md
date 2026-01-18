# PM Paper Renderer

Dynamic paper rendering system for Principia Metaphysica. Builds the complete paper from `theory_output.json` sections, formulas, and parameters.

## Features

- **Dynamic Loading**: Loads all sections from `theory_output.json`
- **Formula Integration**: Automatically renders formulas using `data-formula-id` references
- **Parameter Population**: Uses `PM.get()` for dynamic parameter values
- **Section Loading**: Loads individual section HTML files
- **MathJax Coordination**: Triggers MathJax typesetting after rendering
- **Flexible Options**: Control what gets rendered (sections, formulas, parameters, TOC, etc.)

## Installation

```html
<!-- MathJax Configuration -->
<script>
    MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']]
        }
    };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<!-- PM Loaders (in order) -->
<script src="js/pm-constants-loader.js"></script>
<script src="js/pm-formula-loader.js"></script>
<script src="js/pm-paper-renderer.js"></script>
```

## Basic Usage

### HTML Container

```html
<div id="paper-container"></div>
```

### JavaScript

```javascript
// Simple rendering
await PMPaperRenderer.renderPaper('paper-container');

// With options
await PMPaperRenderer.renderPaper('paper-container', {
    loadSections: true,      // Load section HTML files
    loadFormulas: true,      // Process formula references
    loadParameters: true,    // Process parameter references
    renderAbstract: true,    // Render abstract section
    renderTOC: true,         // Render table of contents
    debug: false             // Enable debug logging
});
```

## API Reference

### `renderPaper(containerId, options)`

Renders the complete paper into a container.

**Parameters:**
- `containerId` (string): ID of the container element
- `options` (object): Rendering options
  - `loadSections` (boolean): Load section HTML files (default: true)
  - `loadFormulas` (boolean): Process formula references (default: true)
  - `loadParameters` (boolean): Process parameter references (default: true)
  - `renderAbstract` (boolean): Render abstract section (default: true)
  - `renderTOC` (boolean): Render table of contents (default: true)
  - `debug` (boolean): Enable debug logging (default: false)

**Returns:** `Promise<boolean>` - True if rendered successfully

**Example:**
```javascript
const success = await PMPaperRenderer.renderPaper('paper-container', {
    loadSections: true,
    renderTOC: true
});

if (success) {
    console.log('Paper rendered successfully!');
}
```

### `renderSection(section, options)`

Renders a single section with subsections.

**Parameters:**
- `section` (object): Section data from theory_output.json
- `options` (object): Rendering options
  - `loadFormulas` (boolean): Process formulas (default: true)
  - `loadParameters` (boolean): Process parameters (default: true)

**Returns:** `Promise<HTMLElement>` - Rendered section element

**Example:**
```javascript
const sectionData = PMPaperRenderer.data.sections['1'];
const sectionEl = await PMPaperRenderer.renderSection(sectionData, {
    loadFormulas: true,
    loadParameters: true
});
document.body.appendChild(sectionEl);
```

### `renderFormula(formulaId)`

Looks up and returns formula HTML/LaTeX.

**Parameters:**
- `formulaId` (string): Formula ID (e.g., 'generation-number')

**Returns:** `string|null` - HTML/LaTeX string or null if not found

**Example:**
```javascript
const formulaHtml = PMPaperRenderer.renderFormula('generation-number');
console.log(formulaHtml); // '<span>ν = ½|χ|</span>'
```

### `processFormulas(container)`

Processes all formula references in a container.

**Parameters:**
- `container` (HTMLElement): Container element to process

**Example:**
```javascript
const div = document.getElementById('content');
PMPaperRenderer.processFormulas(div);
```

### `processParameters(container)`

Processes all parameter references in a container.

**Parameters:**
- `container` (HTMLElement): Container element to process

**Example:**
```javascript
const div = document.getElementById('content');
PMPaperRenderer.processParameters(div);
```

### `typesetMathJax(element)`

Triggers MathJax typesetting on a specific element.

**Parameters:**
- `element` (HTMLElement): Element to typeset

**Example:**
```javascript
const section = document.getElementById('section-1');
PMPaperRenderer.typesetMathJax(section);
```

## Data Attributes

The renderer recognizes and processes several data attributes:

### Formula References

```html
<!-- Empty element - will be filled with formula content -->
<div data-formula-id="generation-number"></div>

<!-- Element with existing content - will be preserved, but formula data added as tooltip -->
<div data-formula-id="proton-lifetime">
    Custom content here
</div>
```

### Parameter References

```html
<!-- Simple path-based reference -->
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>

<!-- Category + param reference -->
<span data-category="simulations" data-param="proton_decay.tau_p_years"></span>

<!-- With formatting -->
<span data-pm-value="simulations.higgs_mass.m_h_GeV" data-format="fixed:2"></span>
```

**Supported formats:**
- `scientific:N` - Scientific notation with N decimals
- `fixed:N` - Fixed-point notation with N decimals
- `percent` - Multiply by 100 and add %
- `integer` - Round to integer

## Data Structure

The renderer expects `theory_output.json` with the following structure:

```json
{
  "version": "14.1",
  "metadata": {
    "title": "Principia Metaphysica",
    "subtitle": "A Unified Theory of Physics",
    "author": "Andrew Keith Watts",
    "date": "2025",
    "version": "14.1"
  },
  "sections": {
    "1": {
      "id": "1",
      "title": "Introduction",
      "abstract": "Section abstract...",
      "sectionFile": "sections/introduction.html",
      "subsections": [],
      "contentBlocks": [],
      "keyTakeaways": ["Point 1", "Point 2"],
      "order": 1
    }
  },
  "formulas": {
    "formulas": {
      "generation-number": {
        "id": "generation-number",
        "label": "(3.1) Generation Number",
        "html": "<span>ν = ½|χ|</span>",
        "latex": "\\nu = \\frac{1}{2}|\\chi|",
        "description": "Number of generations"
      }
    }
  },
  "parameters": { ... },
  "simulations": { ... }
}
```

## Section HTML Files

Section HTML files should be complete HTML documents. The renderer extracts content from the `<body>` tag:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Section 1: Introduction</title>
</head>
<body>
    <div class="section-content">
        <h3>Overview</h3>
        <p>Content with <span data-pm-value="parameters.topology.n_gen"></span> generations.</p>

        <div data-formula-id="generation-number"></div>
    </div>
</body>
</html>
```

## CSS Styling

The renderer adds these CSS classes:

### Container Classes
- `.pm-paper-container` - Main container
- `.paper-title-section` - Title and metadata
- `.paper-abstract` - Abstract section
- `.paper-toc` - Table of contents
- `.paper-sections` - Sections container
- `.paper-section` - Individual section

### Section Classes
- `.section-header` - Section header
- `.section-title` - Section title
- `.section-number` - Section number badge
- `.section-abstract` - Section abstract
- `.section-content` - Section content
- `.section-takeaways` - Key takeaways

### State Classes
- `.pm-loaded` - Successfully loaded value/formula
- `.pm-loading` - Loading state
- `.pm-error` - Error state
- `.pm-formula-loaded` - Formula loaded successfully

### Content Block Classes
- `.content-blocks` - Content blocks container
- `.content-block` - Individual block
- `.content-block-{type}` - Type-specific block (paragraph, heading, formula, etc.)
- `.formula-block` - Formula display block
- `.equation-block` - Equation display block

## Examples

### Example 1: Full Paper with Custom Styling

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Paper</title>
    <script src="js/pm-constants-loader.js"></script>
    <script src="js/pm-formula-loader.js"></script>
    <script src="js/pm-paper-renderer.js"></script>

    <style>
        .pm-paper-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            font-family: Georgia, serif;
        }

        .paper-title {
            font-size: 3rem;
            text-align: center;
            margin-bottom: 2rem;
        }

        .section-title {
            font-size: 2rem;
            margin-top: 3rem;
            border-bottom: 2px solid #333;
            padding-bottom: 0.5rem;
        }
    </style>
</head>
<body>
    <div id="paper"></div>

    <script>
        window.addEventListener('load', async () => {
            await PMPaperRenderer.renderPaper('paper', {
                loadSections: true,
                renderTOC: true,
                debug: true
            });
        });
    </script>
</body>
</html>
```

### Example 2: Single Section Rendering

```javascript
// Load specific section
const section2 = PMPaperRenderer.data.sections['2'];
const container = document.getElementById('section-container');

const sectionEl = await PMPaperRenderer.renderSection(section2);
container.appendChild(sectionEl);

// Trigger MathJax
PMPaperRenderer.typesetMathJax(sectionEl);
```

### Example 3: Custom Content with Formula References

```html
<div id="custom-content">
    <h2>My Custom Section</h2>
    <p>The generation number is given by:</p>
    <div data-formula-id="generation-number"></div>

    <p>With value: <span data-pm-value="parameters.topology.n_gen"></span></p>
</div>

<script>
    // Process formulas and parameters in custom content
    const container = document.getElementById('custom-content');
    PMPaperRenderer.processFormulas(container);
    PMPaperRenderer.processParameters(container);
    PMPaperRenderer.typesetMathJax(container);
</script>
```

## Integration with Existing Code

The PM Paper Renderer integrates seamlessly with:

- **pm-constants-loader.js**: Uses `PM.get()` for parameter values
- **pm-formula-loader.js**: Uses `PM.formula()` for formula lookups
- **MathJax**: Automatically triggers typesetting after rendering

## Troubleshooting

### Formulas not rendering

1. Check that `pm-formula-loader.js` is loaded before `pm-paper-renderer.js`
2. Verify `theory_output.json` exists and contains formulas
3. Check browser console for errors
4. Enable debug mode: `renderPaper('container', { debug: true })`

### Parameters showing "?"

1. Check that `pm-constants-loader.js` is loaded
2. Verify the parameter path is correct
3. Check `theory_output.json` contains the parameter
4. Hover over "?" for detailed error message

### Sections not loading

1. Verify section HTML files exist in the `sections/` directory
2. Check `sectionFile` paths in `theory_output.json`
3. Ensure you're running from a web server (not `file://`)
4. Enable debug mode to see fetch attempts

### MathJax not typesetting

1. Ensure MathJax is loaded before rendering
2. Check MathJax configuration
3. Verify elements don't have `mathjax-ignore` class
4. Manually trigger: `PMPaperRenderer.typesetMathJax(element)`

## Performance

- **Caching**: Section HTML files are cached after first load
- **Async Loading**: All sections load in parallel
- **Lazy Typesetting**: MathJax only processes rendered elements
- **Efficient Processing**: Only processes elements with data attributes

## Browser Compatibility

- Modern browsers with ES6 support
- Fetch API required
- MutationObserver support recommended
- Tested on Chrome, Firefox, Safari, Edge

## Version History

### v1.0.0 (2025-12-26)
- Initial release
- Dynamic paper rendering from theory_output.json
- Formula and parameter processing
- Section HTML file loading
- MathJax integration
- Comprehensive API

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

## Support

For issues or questions, please contact: AndrewKWatts@Gmail.com
