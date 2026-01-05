# PM Section Styling - Quick Reference Card

## Typography
```css
Body:    'Crimson Text', 11pt, line-height: 1.7
Headers: 'Source Sans Pro', weights: 400, 600
Code:    'Source Code Pro', weights: 400, 500

h2: 1.3rem  (Section titles)
h3: 1.1rem  (Subsection titles)
h4: 1.0rem  (Callout titles)
p:  1.0rem  (Body text)
```

## Colors
```css
Text:       #1a1a1a
Accent:     #8b7fff (purple)
Secondary:  #ff7eb6 (pink)
Border:     #e0e0e0
Code BG:    #f5f5f5
Abstract:   #f8f9fa
```

## Spacing
```css
Container:  max-width: 850px, padding: 2rem 0
Margins:    1rem (small), 1.5rem (medium), 2rem (large)
Lists:      margin-left: 2rem, li margin-bottom: 0.3rem
Tables:     margin: 1.5rem 0
```

## Callout Types
```html
callout-info      → Blue   (#60a5fa)
callout-warning   → Amber  (#fbbf24)
callout-success   → Green  (#2e7d32)
callout-derivation → Gray gradient
callout-example   → Light green (#4ade80)
```

## Component Classes
```html
.section-header       - Section header container
.section-title        - h2 section title with border
.section-abstract     - Abstract box with purple border
.derivation-box       - Math derivation with gradient
.callout              - Callout base + type modifier
.section-table        - Table with header styling
.section-figure       - Figure with centered caption
.content-grid         - 2-column grid (1 on mobile)
.content-panel        - Panel with border
.expandable-block     - <details> expandable content
```

## Responsive Breakpoints
```css
Desktop:  > 768px  (default styling)
Tablet:   ≤ 768px  (reduced padding, 1-column grid)
Mobile:   ≤ 480px  (minimal padding, smaller fonts)
```

## Common Patterns

### Section Header
```html
<h2 class="section-title">1. Introduction</h2>
```

### Abstract
```html
<div class="section-abstract">
    <h2>Abstract</h2>
    <p>Abstract text...</p>
</div>
```

### Derivation Box
```html
<div class="derivation-box">
    <h4>Derivation: Title</h4>
    <p>Step 1...</p>
    <div class="equation-block">$$equation$$</div>
</div>
```

### Callout
```html
<aside class="callout callout-info">
    <h4>Note</h4>
    <p>Content...</p>
</aside>
```

### Table
```html
<table class="section-table">
    <thead><tr><th>Col 1</th></tr></thead>
    <tbody><tr><td>Data</td></tr></tbody>
</table>
```

### Code Block
```html
<pre><code>python code here</code></pre>
```

### Figure
```html
<figure class="section-figure">
    <img src="image.svg" alt="...">
    <figcaption>Figure 1: Caption</figcaption>
</figure>
```

## Files
- **CSS**: `css/pm-section-paper.css` (785 lines)
- **JS**: `js/pm-section-renderer.js` (1195 lines)
- **Test**: `test-pm-section-styling.html`
- **Docs**: `css/PM_SECTION_STYLING_GUIDE.md`

## Usage
```html
<script src="js/pm-section-renderer.js"></script>
<pm-section section-id="1"></pm-section>
```

Styles load automatically from `css/pm-section-paper.css` with inline fallback.
