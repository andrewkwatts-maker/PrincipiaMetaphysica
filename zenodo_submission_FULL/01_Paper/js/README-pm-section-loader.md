# PM Section Loader

**Dynamic Section Loading System for Principia Metaphysica**

Version: 1.0.0
File: `js/pm-section-loader.js`

---

## Overview

The PM Section Loader provides a dynamic system for loading, rendering, and managing paper sections in Principia Metaphysica. It integrates seamlessly with the existing PM infrastructure (`pm-constants-loader.js`, `pm-formula-loader.js`) to provide:

- Dynamic loading of section content from HTML files
- Automatic formula and parameter reference resolution
- MathJax integration for LaTeX rendering
- Section metadata from `theory_output.json`
- Caching for performance optimization

---

## Quick Start

### 1. Include Required Scripts

```html
<!-- MathJax (optional but recommended) -->
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<!-- PM Loaders -->
<script src="js/pm-constants-loader.js"></script>
<script src="js/pm-formula-loader.js"></script>
<script src="js/pm-section-loader.js"></script>
```

### 2. Load and Render Sections

#### Method 1: Auto-render with data attributes

```html
<!-- Automatically loads section 1 on page load -->
<div data-section-id="1"></div>

<!-- Load all sections -->
<div data-render-all-sections></div>
```

#### Method 2: Programmatic Loading

```javascript
// Load a single section
const section = await PMSectionLoader.loadSection('1');
PMSectionLoader.renderSection('#container', section);

// Load all sections
const sections = await PMSectionLoader.loadAllSections();
PMSectionLoader.renderAllSections('#paper-container', sections);
```

---

## API Reference

### Core Methods

#### `loadMetadata()`

Loads section metadata from `theory_output.json`.

```javascript
await PMSectionLoader.loadMetadata();
```

**Returns:** `Promise<boolean>` - True if loaded successfully

---

#### `loadSection(sectionId)`

Loads a single section's HTML content and metadata.

```javascript
const section = await PMSectionLoader.loadSection('1');
```

**Parameters:**
- `sectionId` (string): Section ID (e.g., "1", "2", "3")

**Returns:** `Promise<Object>` - Section object with:
- `id`: Section ID
- `title`: Section title
- `html`: Extracted HTML content
- `rawHTML`: Full HTML document
- `htmlPath`: Path to HTML file
- `metadata`: Section metadata from theory_output.json
- `formulaRefs`: Array of formula IDs referenced
- `paramRefs`: Array of parameter IDs referenced
- `figureRefs`: Array of figure IDs referenced
- `citationRefs`: Array of citation IDs referenced

---

#### `loadAllSections()`

Loads all sections in order.

```javascript
const sections = await PMSectionLoader.loadAllSections();
```

**Returns:** `Promise<Array>` - Array of section objects

---

#### `renderSection(container, section, options)`

Renders a section's content into a container element.

```javascript
PMSectionLoader.renderSection('#container', section, {
    processFormulas: true,
    processParams: true,
    triggerMathJax: true,
    addSectionClass: true
});
```

**Parameters:**
- `container` (HTMLElement|string): Container element or selector
- `section` (Object): Section object from `loadSection()`
- `options` (Object): Rendering options
  - `processFormulas` (boolean): Process formula references (default: true)
  - `processParams` (boolean): Process parameter references (default: true)
  - `triggerMathJax` (boolean): Trigger MathJax typesetting (default: true)
  - `addSectionClass` (boolean): Add `pm-section-rendered` class (default: true)

**Returns:** `boolean` - True if rendered successfully

---

#### `renderAllSections(container, sections, options)`

Renders all sections into a container.

```javascript
PMSectionLoader.renderAllSections('#paper', sections, {
    wrapEachSection: true,
    sectionWrapperClass: 'pm-section-wrapper'
});
```

**Parameters:**
- `container` (HTMLElement|string): Container element or selector
- `sections` (Array): Array of section objects
- `options` (Object): Rendering options
  - `wrapEachSection` (boolean): Wrap each section in a div (default: true)
  - `sectionWrapperClass` (string): CSS class for wrapper (default: 'pm-section-wrapper')
  - All options from `renderSection()`

**Returns:** `boolean` - True if rendered successfully

---

#### `renderSectionContent(section)`

Renders a section's HTML with formula/param resolution (helper method).

```javascript
const htmlContent = PMSectionLoader.renderSectionContent(section);
```

**Parameters:**
- `section` (Object): Section object

**Returns:** `string` - Rendered HTML content

---

### Utility Methods

#### `getSectionMetadata(sectionId)`

Gets metadata for a specific section.

```javascript
const metadata = PMSectionLoader.getSectionMetadata('1');
```

**Returns:** `Object|null` - Section metadata or null

---

#### `getAllMetadata()`

Gets all section metadata.

```javascript
const allMetadata = PMSectionLoader.getAllMetadata();
```

**Returns:** `Object` - All section metadata keyed by ID

---

#### `isLoaded()`

Checks if section metadata is loaded.

```javascript
const loaded = PMSectionLoader.isLoaded();
```

**Returns:** `boolean`

---

#### `clearCache()`

Clears the HTML cache (useful for development).

```javascript
PMSectionLoader.clearCache();
```

---

## Data Structure

### Section Object

When you call `loadSection()`, you get a section object with this structure:

```javascript
{
    id: "1",
    title: "Introduction",
    html: "<div>...</div>",  // Extracted content
    rawHTML: "<!DOCTYPE html>...",  // Full HTML document
    htmlPath: "sections/introduction.html",

    metadata: {
        id: "1",
        title: "Introduction",
        sectionType: "main",
        abstract: "...",
        formulaRefs: ["formula-1", "formula-2"],
        paramRefs: ["param-1", "param-2"],
        figureRefs: [],
        citationRefs: ["ref-1"],
        // ... more metadata from theory_output.json
    },

    formulaRefs: ["formula-1", "formula-2"],
    paramRefs: ["param-1", "param-2"],
    figureRefs: [],
    citationRefs: ["ref-1"]
}
```

---

## Integration with PM Ecosystem

### Formula Resolution

The section loader automatically processes elements with `data-formula-id` attributes:

```html
<!-- In section HTML -->
<div data-formula-id="generation-number"></div>

<!-- After rendering, formula is automatically populated -->
<div data-formula-id="generation-number" class="pm-formula-auto">
    $$\nu = \frac{\chi}{24}$$
</div>
```

### Parameter Resolution

Elements with `data-pm-value` or `data-category`/`data-param` attributes are automatically populated by `pm-constants-loader.js`:

```html
<!-- In section HTML -->
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>

<!-- After rendering -->
<span data-pm-value="simulations.proton_decay.tau_p_years" class="pm-loaded">
    8.15e+34
</span>
```

### MathJax Integration

After rendering, the section loader automatically triggers MathJax to typeset any LaTeX formulas:

```javascript
// MathJax v3
if (window.MathJax?.typesetPromise) {
    MathJax.typesetPromise([element]);
}

// MathJax v2
if (window.MathJax?.Hub) {
    MathJax.Hub.Queue(['Typeset', MathJax.Hub, element]);
}
```

---

## File Structure

### Section HTML Files

Section HTML files are located in `sections/` directory:

```
sections/
├── introduction.html           (Section 1)
├── geometric-framework.html    (Section 2)
├── fermion-sector.html         (Section 3)
├── gauge-unification.html      (Section 4)
├── cosmology.html              (Section 5)
└── conclusion.html             (Section 6)
```

### Section Filename Mapping

The loader automatically maps section IDs to filenames:

```javascript
{
    '1': 'introduction.html',
    '2': 'geometric-framework.html',
    '3': 'fermion-sector.html',
    '4': 'gauge-unification.html',
    '5': 'cosmology.html',
    '6': 'conclusion.html'
}
```

You can override this by specifying `sectionFile` in the section metadata in `theory_output.json`.

---

## Advanced Usage

### Custom Section Loading

```javascript
// Load section with custom processing
async function loadCustomSection(sectionId) {
    const section = await PMSectionLoader.loadSection(sectionId);

    if (section) {
        // Custom pre-processing
        section.html = section.html.replace(/PLACEHOLDER/g, 'Custom Value');

        // Render with custom options
        PMSectionLoader.renderSection('#container', section, {
            processFormulas: true,
            processParams: false,  // Skip param processing
            triggerMathJax: true
        });

        // Custom post-processing
        document.querySelector('#container').classList.add('custom-styling');
    }
}
```

### Dynamic Section Navigation

```javascript
let currentSectionId = 1;
const maxSections = 6;

async function navigateToSection(sectionId) {
    if (sectionId < 1 || sectionId > maxSections) return;

    currentSectionId = sectionId;
    const section = await PMSectionLoader.loadSection(String(sectionId));

    PMSectionLoader.renderSection('#main-content', section);

    // Update navigation state
    updateNavButtons();
    window.scrollTo(0, 0);
}

function updateNavButtons() {
    document.getElementById('prev-btn').disabled = currentSectionId <= 1;
    document.getElementById('next-btn').disabled = currentSectionId >= maxSections;
}
```

### Lazy Loading Sections

```javascript
// Intersection Observer for lazy section loading
const observer = new IntersectionObserver((entries) => {
    entries.forEach(async (entry) => {
        if (entry.isIntersecting) {
            const container = entry.target;
            const sectionId = container.getAttribute('data-section-id');

            if (sectionId && !container.classList.contains('pm-section-rendered')) {
                const section = await PMSectionLoader.loadSection(sectionId);
                PMSectionLoader.renderSection(container, section);
                observer.unobserve(container);
            }
        }
    });
}, { rootMargin: '200px' });

// Observe all section containers
document.querySelectorAll('[data-section-id]').forEach(container => {
    observer.observe(container);
});
```

---

## Debugging

### Enable Debug Mode

Set `window.PM_DEBUG = true` to enable verbose logging:

```javascript
window.PM_DEBUG = true;
```

This will log:
- Path resolution attempts
- Section loading progress
- Formula/param processing details

### Common Issues

#### 1. Section Not Found

**Error:** "Could not load HTML for section X"

**Solutions:**
- Check that the section HTML file exists in `sections/` directory
- Verify the filename mapping in `_getSectionFileName()`
- Check the browser console for attempted paths

#### 2. Formulas Not Rendering

**Solutions:**
- Ensure `pm-formula-loader.js` is loaded before `pm-section-loader.js`
- Check that `theory_output.json` contains formula definitions
- Verify MathJax is loaded and configured

#### 3. Parameters Not Populating

**Solutions:**
- Ensure `pm-constants-loader.js` is loaded
- Check that `theory_output.json` is accessible
- Verify parameter paths in `data-pm-value` attributes

---

## Testing

Use the provided test page: `test-section-loader.html`

```bash
# Start a local web server
python -m http.server 8000

# Open in browser
http://localhost:8000/test-section-loader.html
```

The test page includes:
1. Load individual sections
2. Load all sections (paper view)
3. Auto-render with data attributes
4. API examples and statistics

---

## Performance Considerations

### Caching

The section loader caches HTML content after the first load:

```javascript
// First load: fetches from server
const section1 = await PMSectionLoader.loadSection('1');

// Second load: uses cache (instant)
const section1Again = await PMSectionLoader.loadSection('1');
```

Clear cache during development:

```javascript
PMSectionLoader.clearCache();
```

### Parallel Loading

Load multiple sections in parallel for better performance:

```javascript
// Load all sections in parallel
const sectionPromises = ['1', '2', '3', '4', '5', '6'].map(id =>
    PMSectionLoader.loadSection(id)
);
const sections = await Promise.all(sectionPromises);
```

---

## Browser Compatibility

- **Modern Browsers:** Full support (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **IE 11:** Not supported (uses ES6 features)
- **Mobile:** Full support on modern mobile browsers

Required features:
- `async`/`await`
- `fetch` API
- `Promise`
- `DOMParser`
- `MutationObserver` (for auto-rendering)

---

## License

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

---

## Version History

### 1.0.0 (2025-12-26)
- Initial release
- Section loading from HTML files
- Metadata integration with theory_output.json
- Formula and parameter resolution
- MathJax integration
- Auto-rendering with data attributes
- Caching system

---

## Related Files

- `js/pm-constants-loader.js` - Parameter/constant loading
- `js/pm-formula-loader.js` - Formula loading and rendering
- `theory_output.json` - Section metadata and all data
- `sections/*.html` - Section HTML files
- `test-section-loader.html` - Test page

---

## Support

For questions or issues:
- Check the test page: `test-section-loader.html`
- Enable debug mode: `window.PM_DEBUG = true`
- Review browser console for detailed error messages
- Contact: AndrewKWatts@Gmail.com
