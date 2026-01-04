# PM Section Renderer - Styling Guide

## Overview

The PM Section Renderer uses CSS that matches the academic paper styling from `principia-metaphysica-paper.html` exactly. This ensures visual consistency between dynamically rendered sections and the static paper.

## CSS Files

### Primary CSS File
- **File**: `css/pm-section-paper.css`
- **Purpose**: Contains all styling for pm-section-renderer components
- **Loading**: Automatically loaded by `pm-section-renderer.js` (with inline fallback)

### Key Features
- Academic paper styling (Crimson Text serif font)
- Professional typography matching academic standards
- Responsive design for mobile/tablet/desktop
- Print-optimized styles
- Shadow DOM compatibility

## Typography

### Font Families
```css
--font-serif: 'Crimson Text', Georgia, serif;        /* Main body text */
--font-sans: 'Source Sans Pro', sans-serif;          /* Headers, labels */
--font-mono: 'Source Code Pro', monospace;           /* Code blocks */
```

### Font Sizes
- **Body text**: 11pt (1.0em)
- **Section titles (h2)**: 1.3rem
- **Subsection titles (h3)**: 1.1rem
- **Abstract**: 0.95rem
- **Code**: 0.85rem
- **Tables**: 0.9rem

### Line Heights
- **Body**: 1.7
- **Code**: 1.5

## Color Palette

### Paper Colors
```css
--bg-paper: #ffffff;          /* Paper background */
--text-dark: #1a1a1a;         /* Main text color */
--accent: #8b7fff;            /* Primary accent (purple) */
--accent-secondary: #ff7eb6;  /* Secondary accent (pink) */
--border: #e0e0e0;            /* Border color */
--code-bg: #f5f5f5;           /* Code background */
```

### Callout Box Colors
- **Info**: `rgba(96, 165, 250, 0.05)` with border `#60a5fa`
- **Warning**: `rgba(251, 191, 36, 0.05)` with border `#fbbf24`
- **Success**: `rgba(74, 222, 128, 0.05)` with border `#2e7d32`
- **Derivation**: `linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)`
- **Example**: `rgba(74, 222, 128, 0.05)` with border `#4ade80`

## Component Styles

### Section Container
```css
.pm-section {
    max-width: 850px;          /* Match paper width */
    margin: 0 auto;
    padding: 2rem 0;
    font-size: 11pt;
    line-height: 1.7;
}
```

### Section Header
```css
.section-header {
    margin-bottom: 1.5rem;
}

.section-number {
    font-size: 1.3rem;
    color: var(--accent);
    font-weight: 700;
}

.section-title {
    font-size: 1.3rem;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0.3rem;
}
```

### Abstract
```css
.section-abstract {
    background: #f8f9fa;
    padding: 20px 25px;
    border-left: 4px solid var(--accent);
    margin: 2rem 0;
}
```

### Equations
```css
.equation-block {
    margin: 1.5rem 0;
    padding: 1rem 0;
    overflow-x: auto;
}

.equation-number {
    float: right;
    color: #666;
    font-size: 0.9rem;
}
```

### Derivation Boxes
```css
.derivation-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 1.5rem 0;
}
```

### Tables
```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.9rem;
}

th, td {
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

th {
    background: #f5f5f5;
    font-weight: 600;
}
```

### Code Blocks
```css
pre {
    background: var(--code-bg);
    padding: 15px 20px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.85rem;
    line-height: 1.5;
    border-left: 3px solid var(--accent);
}

code {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.9em;
    background: #f0f0f0;
    padding: 2px 5px;
    border-radius: 3px;
}
```

### Figures
```css
.section-figure {
    text-align: center;
    margin: 2rem 0;
}

figcaption {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.5rem;
    font-style: italic;
}
```

### Lists
```css
ul, ol {
    margin-left: 2rem;
    margin-bottom: 1rem;
}

li {
    margin-bottom: 0.3rem;
}
```

## Callout Box Types

### Usage
```html
<aside class="callout callout-info">
    <h4>Title</h4>
    <p>Content...</p>
</aside>
```

### Available Types
- `.callout-info` - Blue, for informational notes
- `.callout-warning` - Amber, for warnings or cautions
- `.callout-success` - Green, for successful results
- `.callout-derivation` - Gray gradient, for mathematical derivations
- `.callout-example` - Light green, for examples
- `.callout-note` - Light gray, for general notes

## Responsive Design

### Breakpoints
- **Desktop**: > 768px (default styling)
- **Tablet**: ≤ 768px
- **Mobile**: ≤ 480px

### Mobile Optimizations (≤ 768px)
```css
.pm-section {
    padding: 1rem;
}

.section-title {
    font-size: 1.15rem;
}

table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
    font-size: 0.8rem;
}

.content-grid {
    grid-template-columns: 1fr;  /* Single column on mobile */
}
```

### Small Mobile (≤ 480px)
```css
.pm-section {
    padding: 0.5rem;
}

.section-title {
    font-size: 1.05rem;
}
```

## Print Styles

### Print Optimizations
```css
@media print {
    .pm-section {
        padding: 0;
        max-width: none;
    }

    .section-nav {
        display: none;
    }

    @page {
        size: A4;
        margin: 25mm 20mm;
    }
}
```

## Shadow DOM Integration

The CSS is loaded into the shadow root of each `<pm-section>` element, ensuring:
- **Style isolation**: Styles don't leak to/from the parent document
- **Consistency**: Same styling regardless of page context
- **Modularity**: Each section is self-contained

### CSS Parts for pm-formula
```css
pm-formula::part(container) {
    font-family: 'Crimson Text', Georgia, serif;
    color: var(--text-dark);
}

pm-formula::part(label) {
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: 600;
    color: var(--accent);
}
```

## Grid & Panel Layouts

### Content Grid
```html
<div class="content-grid" style="--columns: 2">
    <div class="grid-cell">Cell 1</div>
    <div class="grid-cell">Cell 2</div>
</div>
```

```css
.content-grid {
    display: grid;
    grid-template-columns: repeat(var(--columns, 2), 1fr);
    gap: 1.5rem;
}
```

### Content Panel
```html
<div class="content-panel">
    <h4 class="panel-title">Panel Title</h4>
    <p>Panel content...</p>
</div>
```

## Expandable Blocks

### Usage
```html
<details class="expandable-block">
    <summary>Click to expand</summary>
    <p>Hidden content...</p>
</details>
```

### Styling
```css
.expandable-block summary {
    cursor: pointer;
    color: var(--accent);
    font-weight: 600;
    padding: 0.5rem;
    background: #f8f9fa;
    border-radius: 4px;
}

.expandable-block summary:hover {
    background: #e9ecef;
}
```

## Special Elements

### Beginner Summary
```html
<details class="beginner-summary">
    <summary>Simplified Explanation</summary>
    <div class="summary-content">
        <p>Beginner-friendly explanation...</p>
    </div>
</details>
```

### Key Takeaways
```html
<div class="key-takeaways">
    <h4>Key Takeaways</h4>
    <ul>
        <li>Takeaway 1</li>
        <li>Takeaway 2</li>
    </ul>
</div>
```

### Appendices
```html
<div class="appendix" id="appendix-A">
    <h3 class="appendix-title">Appendix A: Title</h3>
    <p>Appendix content...</p>
</div>
```

### Simulation Code
```html
<details class="simulation-code">
    <summary>Simulation Code (filename.py)</summary>
    <pre><code>python code here...</code></pre>
</details>
```

## Navigation

### Section Navigation
```html
<nav class="section-nav">
    <a href="#section-1" class="nav-prev">Previous</a>
    <a href="#section-3" class="nav-next">Next</a>
</nav>
```

## Error States

### Error Display
```html
<div class="error">
    Error message here
</div>
```

```css
.error {
    color: #dc3545;
    padding: 1rem;
    background: rgba(220, 53, 69, 0.1);
    border-radius: 4px;
    border-left: 3px solid #dc3545;
}
```

## Maintenance

### Updating Styles

1. **Primary source**: Edit `css/pm-section-paper.css`
2. **Fallback**: Update inline styles in `js/pm-section-renderer.js` `getStyles()` method
3. **Testing**: Test on desktop, tablet, mobile, and print

### Syncing with Paper

To keep styles synchronized with `principia-metaphysica-paper.html`:

1. Extract styles from `<style>` tag in paper HTML
2. Copy to `css/pm-section-paper.css`
3. Adjust selectors to work in shadow DOM
4. Add `:host` rules where needed
5. Test all component types

### CSS Variables

All colors and sizes use CSS variables for easy theme adjustments:
```css
:root {
    --bg-paper: #ffffff;
    --text-dark: #1a1a1a;
    --accent: #8b7fff;
    --accent-secondary: #ff7eb6;
    --border: #e0e0e0;
    --code-bg: #f5f5f5;
}
```

## Best Practices

1. **Use semantic HTML**: Use proper heading hierarchy (h2 → h3 → h4)
2. **Consistent spacing**: Use predefined margins (1rem, 1.5rem, 2rem)
3. **Accessible colors**: Ensure sufficient contrast for readability
4. **Test responsiveness**: Check on multiple screen sizes
5. **Validate print**: Always test print preview
6. **Shadow DOM**: Remember styles are isolated - use ::part() for external styling

## Common Issues

### Issue: Styles not loading
**Solution**: Check console for CSS file path errors. Fallback inline styles should work.

### Issue: Fonts not rendering
**Solution**: Ensure Google Fonts import is present in CSS.

### Issue: Dark text on dark background
**Solution**: Verify `:host` color is set to `var(--text-dark)` not inherited from parent.

### Issue: Tables overflow on mobile
**Solution**: Use `overflow-x: auto` and `white-space: nowrap` (already in CSS).

### Issue: Print styling issues
**Solution**: Test with `@media print` styles, ensure no display:none on essential content.

## Version History

- **v1.0** (2025-12-25): Initial creation matching paper styles exactly
  - Font: Crimson Text 11pt, line-height 1.7
  - Colors: Academic palette with purple accent
  - Layouts: Tables, figures, equations, derivation boxes
  - Responsive: Desktop, tablet, mobile breakpoints
  - Print: A4 optimized with proper margins
