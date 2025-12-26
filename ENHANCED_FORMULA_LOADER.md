# Enhanced PM Formula Loader

## Overview

The `pm-formula-loader.js` has been enhanced with a rich, interactive formula component that provides:

- **Title and subtitle** display with equation numbers and categories
- **Plain text toggle** for viewing formulas in ASCII format
- **Expandable info panel** with inputs, outputs, derivation, and terms
- **Hover effects** for interactive formula cards
- **Compact mode** for grid layouts
- **Automatic styling** injection (no external CSS required)

## Features

### 1. Rich Formula Cards

Each formula is now rendered as a beautiful, interactive card with:

- **Header Section**
  - Equation number (e.g., "Eq. 4.2")
  - Title (auto-generated from formula ID)
  - Category badge (THEORY, DERIVED, PREDICTIONS)
  - Description/subtitle

- **Display Section**
  - LaTeX formula (rendered with MathJax)
  - Plain text toggle button
  - Collapsible plain text view

- **Expandable Details**
  - Input parameters (📥)
  - Output parameters (📤)
  - Derived from formulas (🔗)
  - Term definitions (📖)
  - Section reference (📑)

### 2. Interactive Features

- **Hover effects** - Cards glow with purple accent on hover
- **Expandable panels** - Click "More Info" to reveal detailed information
- **Plain text toggle** - Click to show/hide ASCII representation
- **Smooth animations** - All transitions are smooth and polished

### 3. Customization Options

The `render()` method accepts these options:

```javascript
PMFormulaLoader.render(element, formulaId, {
    showTitle: true,      // Show header with title and category
    showPlainText: true,  // Show plain text toggle button
    expandable: true,     // Enable expandable info panel
    interactive: true,    // Enable hover effects
    compact: false        // Use compact spacing
});
```

## Usage

### Basic Usage (Auto-render)

Simply add a `data-formula-id` attribute to any element:

```html
<div data-formula-id="generation-number"></div>
```

The formula will be automatically rendered when the page loads.

### Custom Options via Data Attributes

Control rendering options using data attributes:

```html
<!-- Compact mode -->
<div data-formula-id="fine-structure-constant" data-compact="true"></div>

<!-- No title, non-interactive -->
<div data-formula-id="proton-electron-mass-ratio"
     data-show-title="false"
     data-interactive="false"></div>

<!-- Minimal version -->
<div data-formula-id="weak-mixing-angle"
     data-show-title="false"
     data-show-plaintext="false"
     data-expandable="false"></div>
```

### Manual Rendering

Use JavaScript to render formulas programmatically:

```javascript
// Wait for formulas to load
await PMFormulaLoader.load();

// Render with options
const element = document.getElementById('my-formula');
PMFormulaLoader.render(element, 'generation-number', {
    showTitle: true,
    showPlainText: true,
    expandable: true,
    interactive: true,
    compact: false
});
```

### Grid Layouts

Create responsive formula grids:

```html
<div class="formula-grid">
    <div data-formula-id="generation-number" data-compact="true"></div>
    <div data-formula-id="fine-structure-constant" data-compact="true"></div>
    <div data-formula-id="proton-electron-mass-ratio" data-compact="true"></div>
    <div data-formula-id="vacuum-energy-density" data-compact="true"></div>
</div>

<style>
.formula-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
}
</style>
```

## Styling

Styles are automatically injected into the page when the first formula is rendered. No external CSS file is required.

### Color Scheme

The component uses a dark theme with purple accents:

- **Primary accent**: `#8b7fff` (purple)
- **Background**: `rgba(255, 255, 255, 0.03)` (subtle white overlay)
- **Borders**: `rgba(255, 255, 255, 0.1)` (subtle white borders)
- **Text**: `#f8f9fa` (light gray)
- **Code blocks**: `#a3e635` (lime green)

### Custom Styling

You can override the default styles using CSS:

```css
/* Customize card background */
.pm-formula-card {
    background: rgba(0, 100, 200, 0.1) !important;
}

/* Customize hover effect */
.pm-formula-card.interactive:hover {
    border-color: rgba(0, 200, 255, 0.5) !important;
    box-shadow: 0 4px 20px rgba(0, 200, 255, 0.2) !important;
}

/* Customize title color */
.pm-formula-title {
    color: #00ccff !important;
}
```

## API Reference

### PMFormulaLoader.render(element, formulaId, options)

Renders a formula into a DOM element with full interactive features.

**Parameters:**
- `element` (HTMLElement) - Target element to render into
- `formulaId` (string) - Formula ID from theory_output.json
- `options` (Object, optional) - Rendering options

**Options:**
- `showTitle` (boolean, default: true) - Show header with title and category
- `showPlainText` (boolean, default: true) - Show plain text toggle button
- `expandable` (boolean, default: true) - Enable expandable info panel
- `interactive` (boolean, default: true) - Enable hover effects
- `compact` (boolean, default: false) - Use compact spacing

**Returns:**
- `boolean` - True if rendered successfully, false otherwise

**Example:**
```javascript
PMFormulaLoader.render(document.getElementById('target'), 'generation-number', {
    showTitle: true,
    showPlainText: true,
    expandable: true,
    interactive: true,
    compact: false
});
```

### PMFormulaLoader.renderAll()

Automatically renders all elements with `data-formula-id` or `data-id` attributes.

Called automatically on page load. Can be called manually to render dynamically added elements.

**Example:**
```javascript
// Add new formula element
const div = document.createElement('div');
div.setAttribute('data-formula-id', 'fine-structure-constant');
document.body.appendChild(div);

// Render it
PMFormulaLoader.renderAll();
```

### PMFormulaLoader._ensureStyles()

Ensures formula styles are loaded (called automatically by render()).

**Note:** This is a private method and should not be called directly.

## Data Attributes

### Available Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `data-formula-id` | string | required | Formula ID to render |
| `data-show-title` | boolean | true | Show header section |
| `data-show-plaintext` | boolean | true | Show plain text toggle |
| `data-expandable` | boolean | true | Enable expandable panel |
| `data-interactive` | boolean | true | Enable hover effects |
| `data-compact` | boolean | false | Use compact spacing |

### Examples

```html
<!-- Full featured (default) -->
<div data-formula-id="generation-number"></div>

<!-- Compact mode -->
<div data-formula-id="generation-number" data-compact="true"></div>

<!-- No title -->
<div data-formula-id="generation-number" data-show-title="false"></div>

<!-- No plain text -->
<div data-formula-id="generation-number" data-show-plaintext="false"></div>

<!-- No expandable panel -->
<div data-formula-id="generation-number" data-expandable="false"></div>

<!-- Non-interactive -->
<div data-formula-id="generation-number" data-interactive="false"></div>

<!-- Minimal (just the formula) -->
<div data-formula-id="generation-number"
     data-show-title="false"
     data-show-plaintext="false"
     data-expandable="false"></div>
```

## Testing

A test page is available at `test-enhanced-formulas.html` demonstrating:

1. Default configuration with full features
2. Compact mode
3. No title, non-interactive mode
4. Grid layout with multiple formulas
5. Manual rendering with custom options

To test:

1. Ensure `theory_output.json` exists in the project root
2. Run a local web server (e.g., `python -m http.server 8000`)
3. Open `http://localhost:8000/test-enhanced-formulas.html`

## Browser Compatibility

- **Modern browsers** (Chrome, Firefox, Safari, Edge) - Full support
- **MathJax required** for LaTeX rendering
- **JavaScript required** for interactive features

## Performance

- Styles are injected once (cached check via `#pm-formula-styles`)
- MathJax rendering is batched and asynchronous
- Hover effects use CSS transitions (hardware accelerated)
- No external CSS dependencies

## Migration from Old Version

The enhanced version is **backward compatible**. Existing usage will continue to work:

```javascript
// Old usage still works
PMFormulaLoader.render(element, formulaId);
PMFormulaLoader.render(element, formulaId, { showLabel: true });
```

New options are optional and default to enabled for the best experience.

## Future Enhancements

Potential future additions:

- [ ] Dark/light theme toggle
- [ ] Copy formula to clipboard
- [ ] Formula search/filter
- [ ] Export formula as image
- [ ] Link to related formulas
- [ ] Formula comparison view
- [ ] Custom color schemes
- [ ] Animation presets

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
