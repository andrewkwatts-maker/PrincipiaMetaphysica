# PM Formula Renderer - Complete Guide

## Overview

The PM Formula Renderer (`pm-formula-renderer.js`) provides a rich UX system for displaying mathematical formulas from the Principia Metaphysica theory. It supports multiple rendering modes from simple inline display to full interactive pages.

## Installation

### 1. Include Dependencies

```html
<!-- Load in this order -->
<script src="theory-constants-enhanced.js"></script>
<script src="js/pm-formula-loader.js"></script>
<script src="js/formula-registry.js"></script>
<script src="js/pm-formula-renderer.js"></script>
```

### 2. CSS Requirements

The renderer uses CSS classes from `css/styles.css`:
- `.interactive-formula`
- `.formula-display`
- `.formula-var`
- `.var-tooltip`
- `.formula-info`
- `.formula-info-grid`
- `.formula-info-item`
- `.sub-components`
- `.derivation-chain`
- `.expandable-formula`

## API Reference

### Core Methods

#### 1. `renderInteractive(formulaId, container, options)`

Renders an interactive formula with hoverable variables and tooltips.

**Parameters:**
- `formulaId` (string): Formula identifier (e.g., 'master-action-26d')
- `container` (string|HTMLElement): Container ID or DOM element
- `options` (Object):
  - `showHint` (boolean): Show "Hover for details" hint (default: true)
  - `large` (boolean): Use large font size (default: false)

**Example:**
```javascript
PMFormulaRenderer.renderInteractive('master-action-26d', 'formula-container', {
    showHint: true,
    large: true
});
```

**HTML Output:**
```html
<div class="interactive-formula">
    <span class="formula-hint">Hover for details</span>
    <div class="formula-display large">
        <a class="formula-var" href="...">S<sub>26D</sub>
            <div class="var-tooltip">
                <div class="var-name">26D Master Action</div>
                <div class="var-description">...</div>
            </div>
        </a>
        ...
    </div>
</div>
```

---

#### 2. `renderInfoPanel(formulaId, container)`

Renders a formula information panel with title, description, metadata grid, and use cases.

**Parameters:**
- `formulaId` (string): Formula identifier
- `container` (string|HTMLElement): Container ID or DOM element

**Example:**
```javascript
PMFormulaRenderer.renderInfoPanel('master-action-26d', 'info-panel');
```

**Required Formula Properties:**
```javascript
{
    label: "Master 26D Action",
    description: "Fundamental action principle...",
    infoGrid: [
        {
            title: "Full Bulk",
            content: "26D with signature (24,2)",
            link: "paper.html#section-2"
        },
        {
            title: "Gauge Group",
            content: "SO(10) ⊃ SU(3)×SU(2)×U(1)",
            link: "paper.html#section-3"
        }
    ],
    useCases: [
        {
            text: "Einstein gravity + cosmological dynamics",
            link: "paper.html#section-6"
        },
        {
            text: "SO(10) GUT → Standard Model",
            link: "paper.html#section-3"
        }
    ]
}
```

**HTML Output:**
```html
<div class="formula-info">
    <div class="formula-title">Master 26D Action</div>
    <div class="formula-meaning">Fundamental action principle...</div>
    <div class="formula-info-grid">
        <div class="formula-info-item">
            <a href="...">
                <h5>Full Bulk</h5>
                <p>26D with signature (24,2)</p>
            </a>
        </div>
        ...
    </div>
    <div class="use-cases">
        <h5>What Emerges</h5>
        <ul>
            <li><a href="...">Einstein gravity + cosmological dynamics</a></li>
            ...
        </ul>
    </div>
</div>
```

---

#### 3. `renderExpandable(formulaId, container, options)`

Renders a collapsible section with sub-components grid and derivation chain.

**Parameters:**
- `formulaId` (string): Formula identifier
- `container` (string|HTMLElement): Container ID or DOM element
- `options` (Object):
  - `headerText` (string): Header label (default: 'Dimensional Reduction')
  - `expanded` (boolean): Initially expanded (default: false)

**Example:**
```javascript
PMFormulaRenderer.renderExpandable('master-action-26d', 'expandable', {
    headerText: 'Master Action Breakdown',
    expanded: false
});
```

**Required Formula Properties:**
```javascript
{
    plainText: "S = ∫ d²⁶X √|G_(24,2)| [...]",
    subComponents: [
        {
            symbol: "M²₂₆R₂₆",
            name: "Einstein-Hilbert Term",
            description: "26D gravity with signature (24,2)",
            link: "foundations/einstein-hilbert-action.html",
            badge: "Established",
            badgeClass: "established"
        },
        ...
    ],
    derivation: {
        parentFormulas: ['spacetime-26d'],
        establishedPhysics: ['einstein-hilbert', 'clifford-algebra'],
        steps: [...]
    }
}
```

**HTML Output:**
```html
<div class="expandable-formula">
    <div class="formula-header">
        <div class="formula-main">
            <span>▼ Master Action Breakdown:</span>
            S = ∫ d²⁶X √|G_(24,2)| [...]
        </div>
        <button class="expand-btn">▼</button>
    </div>
    <div class="formula-expansion">
        <div class="sub-components">
            <a class="sub-component" href="...">
                <div class="component-symbol">M²₂₆R₂₆</div>
                <div class="component-name">Einstein-Hilbert Term</div>
                <div class="component-description">...</div>
                <span class="foundation-badge established">Established</span>
            </a>
            ...
        </div>
        <div class="derivation-chain">
            <div class="chain-title">Derivation Path to Established Physics</div>
            <div class="chain-step">
                <span class="step-arrow">→</span>
                <a href="...">Einstein-Hilbert Action (1915)</a>
                <span class="foundation-badge established">Established</span>
            </div>
            ...
        </div>
    </div>
</div>
```

---

#### 4. `renderPlainText(formulaId, container)`

Renders monospace plain text version (good for AI processing and accessibility).

**Example:**
```javascript
PMFormulaRenderer.renderPlainText('generation-number', 'plain-text');
```

**HTML Output:**
```html
<div class="formula-plain-text">
    <div>Three Generations Formula</div>
    <code>n_gen = χ_eff/48 = 144/48 = 3</code>
</div>
```

---

#### 5. `renderFull(formulaId, container, options)`

Renders complete formula display with all components.

**Parameters:**
- `formulaId` (string): Formula identifier
- `container` (string|HTMLElement): Container ID or DOM element
- `options` (Object):
  - `showInteractive` (boolean): Show interactive display (default: true)
  - `showInfoPanel` (boolean): Show info panel (default: true)
  - `showExpandable` (boolean): Show expandable section (default: false)
  - `showPlainText` (boolean): Show plain text version (default: true)
  - `interactiveOptions` (Object): Options for interactive renderer
  - `expandableOptions` (Object): Options for expandable renderer

**Example:**
```javascript
PMFormulaRenderer.renderFull('generation-number', 'full-display', {
    showInteractive: true,
    showInfoPanel: true,
    showExpandable: true,
    showPlainText: true,
    interactiveOptions: { large: true },
    expandableOptions: { expanded: false }
});
```

---

#### 6. `renderBatch(formulas, options)`

Batch render multiple formulas.

**Parameters:**
- `formulas` (Array): Array of formula IDs
- `options` (Object):
  - `containerSelector` (string): CSS selector for containers (default: '.formula-container')
  - `renderMode` (string): 'interactive' | 'full' | 'plain' (default: 'interactive')

**Example:**
```javascript
// HTML
<div class="formula-slot"></div>
<div class="formula-slot"></div>
<div class="formula-slot"></div>

// JavaScript
PMFormulaRenderer.renderBatch(
    ['generation-number', 'gut-scale', 'w0-formula'],
    {
        containerSelector: '.formula-slot',
        renderMode: 'interactive'
    }
);
```

---

## Formula Data Structure

Formulas are loaded from `PM.formulas` (via `pm-formula-loader.js`) or `FORMULA_REGISTRY` (via `formula-registry.js`).

### Complete Formula Object

```javascript
{
    // Core properties
    id: "generation-number",
    html: "n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3",
    latex: "n_{gen} = \\frac{\\chi_{eff}}{48} = 3",
    plainText: "n_gen = χ_eff/48 = 144/48 = 3",
    label: "(2.6) Three Generations Formula",
    category: "DERIVED",
    description: "Topological derivation of exactly 3 fermion generations",

    // Interactive rendering
    terms: {
        "n<sub>gen</sub>": {
            name: "Number of Generations",
            description: "= 3 (electron/muon/tau families)",
            units: "dimensionless",
            contribution: "Topologically required from G₂ manifold",
            link: "sections.html#2#generations"
        },
        "χ<sub>eff</sub>": {
            name: "Effective Euler Characteristic",
            description: "= 144 from flux-dressed TCS G₂ topology",
            link: "sections.html#2#euler-char"
        }
    },

    // Info panel
    infoGrid: [
        {
            title: "Topology Source",
            content: "G₂ manifold with χ_eff = 144",
            link: "sections.html#2"
        },
        {
            title: "Agreement",
            content: "EXACT (observed = 3)",
            link: "sections/validation.html"
        }
    ],

    useCases: [
        {
            text: "Explains why nature has exactly 3 fermion families",
            link: "sections/fermion-sector.html"
        }
    ],

    // Expandable section
    subComponents: [
        {
            symbol: "χ_eff",
            name: "Euler Characteristic",
            description: "Topological invariant = 144",
            link: "sections/topology.html",
            badge: "Geometric",
            badgeClass: "derived"
        },
        {
            symbol: "48",
            name: "Index Divisor",
            description: "= 24 × 2 from F-theory + two-time",
            link: "sections/index-theorem.html",
            badge: "Established",
            badgeClass: "established"
        }
    ],

    // Derivation chain
    derivation: {
        parentFormulas: ["spacetime-26d", "clifford-26d"],
        establishedPhysics: ["f-theory-index"],
        steps: [
            "F-theory generation formula: n_gen = χ/24",
            "PM two-time framework doubles divisor: n_gen = χ_eff/48",
            "G₂ manifold with χ_eff = 144: n_gen = 144/48 = 3"
        ],
        verificationPage: "sections.html#2"
    }
}
```

---

## Usage Examples

### Example 1: Inline Formula in Paper Section

```html
<!-- In sections.html or paper.html -->
<div id="formula-display"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    PMFormulaRenderer.renderInteractive('generation-number', 'formula-display', {
        showHint: true,
        large: false
    });
});
</script>
```

### Example 2: Standalone Formula Page

```html
<!-- In formulas.html or individual formula page -->
<div id="formula-full"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    PMFormulaRenderer.renderFull('generation-number', 'formula-full', {
        showInteractive: true,
        showInfoPanel: true,
        showExpandable: true,
        showPlainText: true,
        interactiveOptions: { large: true }
    });
});
</script>
```

### Example 3: Formula List Page

```html
<!-- Render all formulas in a category -->
<div class="formula-list">
    <div class="formula-container" data-formula="generation-number"></div>
    <div class="formula-container" data-formula="gut-scale"></div>
    <div class="formula-container" data-formula="w0-formula"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const containers = document.querySelectorAll('.formula-container');
    containers.forEach(container => {
        const formulaId = container.dataset.formula;
        PMFormulaRenderer.renderFull(formulaId, container, {
            showInteractive: true,
            showInfoPanel: true,
            showExpandable: false,
            showPlainText: false
        });
    });
});
</script>
```

### Example 4: Dynamic Formula Loading

```javascript
// Load formula based on URL parameter
const urlParams = new URLSearchParams(window.location.search);
const formulaId = urlParams.get('id') || 'master-action-26d';

PMFormulaRenderer.renderFull(formulaId, 'main-content', {
    showInteractive: true,
    showInfoPanel: true,
    showExpandable: true,
    showPlainText: true
});
```

---

## CSS Customization

The renderer uses CSS variables from `css/styles.css`. You can customize the appearance:

```css
/* Override tooltip colors */
.var-tooltip {
    background: #1a1a2e !important;
    border-color: rgba(139, 127, 255, 0.4) !important;
}

/* Customize formula display */
.formula-display.large {
    font-size: 1.5rem !important;
}

/* Change hover effects */
.formula-var:hover {
    background: rgba(139, 127, 255, 0.4) !important;
}
```

---

## Mobile Support

The renderer includes touch support for mobile devices:

- Touch a variable to show tooltip
- Touch outside to dismiss
- Tooltips reposition for small screens
- Expandable sections work with touch

---

## Error Handling

If a formula is not found, the renderer displays an error message:

```javascript
PMFormulaRenderer.renderInteractive('non-existent-id', 'container');
// Displays: "Error: Formula not found: non-existent-id"
```

---

## Integration with Existing Systems

### With pm-formula-component.js

The renderer complements the `<pm-formula>` web component:

```html
<!-- Web component (shadow DOM) -->
<pm-formula formula-id="generation-number"></pm-formula>

<!-- Renderer (light DOM, more flexible) -->
<div id="formula-display"></div>
<script>
PMFormulaRenderer.renderFull('generation-number', 'formula-display');
</script>
```

### With pm-formula-loader.js

The renderer automatically uses formulas loaded by `PMFormulaLoader`:

```javascript
// Load from JSON
PMFormulaLoader.loadFromJSON('theory_output.json');

// Render loaded formula
PMFormulaRenderer.renderInteractive('custom-formula-id', 'container');
```

---

## Performance Tips

1. **Batch rendering**: Use `renderBatch()` for multiple formulas
2. **Lazy loading**: Only render formulas when they enter viewport
3. **Cache formulas**: Store `getFormula()` results to avoid repeated lookups

---

## Testing

Use `test-formula-renderer.html` to test all rendering modes:

```bash
# Open in browser
open test-formula-renderer.html
```

---

## API Summary

| Method | Purpose | Use Case |
|--------|---------|----------|
| `renderInteractive()` | Hoverable formula | Inline in paper sections |
| `renderInfoPanel()` | Metadata & use cases | Formula details page |
| `renderExpandable()` | Collapsible details | Complex formula breakdown |
| `renderPlainText()` | ASCII version | AI processing, accessibility |
| `renderFull()` | Complete display | Standalone formula pages |
| `renderBatch()` | Multiple formulas | Formula lists, catalogs |

---

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
