# PM Paper Tooltips - User Guide

## Overview

The PM Paper Tooltips system provides comprehensive, interactive tooltips throughout the paper, enhancing readability and user experience with detailed information about formulas, parameters, citations, and more.

## Features

### 1. Smart Tooltip Positioning
- **Viewport-aware**: Tooltips automatically adjust position to stay within viewport
- **200ms hover delay**: Reduces tooltip flicker during mouse movement
- **Smooth animations**: Fade-in effects with scale transform
- **Mobile-optimized**: Centered tooltips on small screens

### 2. Tooltip Types

#### Formula Variable Tooltips
Hover over variables in equations to see:
- **Variable symbol** and name
- **Description** from the formula's terms dictionary
- **Value** (if computed)
- **Units**
- **Parameter link** to related parameter
- **External links** to Wikipedia or references

**Example:**
```html
<div class="equation-content">
    $$N_{\text{gen}} = \frac{1}{2}|\chi_{\text{eff}}|$$
</div>
```

Hovering over `N_gen` shows:
```
N_gen
─────
Number of fermion generations

Value: 3
Units: dimensionless
Parameter: topology.n_gen
```

#### Parameter Value Tooltips
Hover over parameter values to see:
- **Full parameter name**
- **Description**
- **Value with units**
- **Uncertainty range**
- **Source** (PDG, CODATA, etc.)
- **Status** badge (ESTABLISHED, PREDICTED, DERIVED)

**Usage:**
```html
<!-- Path-based -->
<span data-pm-value="pdg.m_higgs">?</span>

<!-- Category-based -->
<span data-category="simulations" data-param="proton_decay.tau_p_years">?</span>
```

Tooltip shows:
```
m_higgs
─────
Higgs boson mass

125.1 GeV
Uncertainty: ±0.14
Source: ESTABLISHED:PDG2024
[ESTABLISHED]
```

#### Formula Reference Tooltips
Hover over equation references (e.g., "Eq. (4.2)") to see:
- **Equation number**
- **Formula preview** (rendered LaTeX)
- **Action hint** ("Click to jump to equation")

**Automatic conversion:**
The system automatically converts text like "Eq. (4.2)" into clickable links with tooltips.

#### Citation Tooltips
Hover over citations to see:
- **Citation key**
- **Reference details** (author, year, title)
- **Action hint** ("Click to view in references")

**Usage:**
```html
<cite data-citation="Joyce2000">Joyce 2000</cite>
```

#### Acronym Tooltips
Hover over acronyms to see full expansion:
- SM → Standard Model
- GUT → Grand Unified Theory
- CKM → Cabibbo-Kobayashi-Maskawa
- PMNS → Pontecorvo-Maki-Nakagawa-Sakata
- And many more...

**Usage:**
```html
<abbr class="acronym">SM</abbr>
```

### 3. Interactive Features

#### Copy to Clipboard
Every formula includes a **"📋 Copy LaTeX"** button:
- Click to copy the LaTeX source to clipboard
- Visual feedback: button changes to "✓ Copied!" for 2 seconds
- Works on all modern browsers

**Locations:**
- Formula card headers (main copy button)
- Equation wrappers (small floating button on hover)

#### LaTeX/Plain Text Toggle
Switch between LaTeX rendering and plain text:
- **"Show Plain Text"** button in formula headers
- Useful for copy-pasting or understanding formula structure
- Maintains formatting in plain text view

#### Collapsible Derivations
Formula cards can expand to show:
- **LaTeX source code**
- **Derivation steps** and parent formulas
- **Term definitions** in detail list
- **Related formulas**

Click the **"▸"** button to expand/collapse.

### 4. Mobile Support

#### Touch Interactions
- **Tap to show** tooltip (instead of hover)
- **Tap again** or **tap elsewhere** to hide
- Tooltips **centered** on screen for readability
- **Larger tap targets** for formula elements

#### Responsive Design
- Tooltips resize to **90vw** on mobile
- Font sizes adjust for readability
- Copy and toggle buttons remain accessible
- **Always-visible** copy buttons (no hover needed)

### 5. Accessibility

#### Keyboard Navigation
- **Tab** through interactive elements
- **Focus indicators** on buttons
- **Screen reader** compatible (semantic HTML)

#### Reduced Motion
Respects `prefers-reduced-motion` setting:
- Disables animations
- Instant tooltip appearance

#### High Contrast
Supports `prefers-contrast` setting:
- **Thicker borders**
- **Higher contrast** colors
- **White outline** for better visibility

## Implementation Guide

### Basic Setup

#### 1. Include Required Files
```html
<!-- CSS -->
<link rel="stylesheet" href="css/pm-paper-tooltips.css">

<!-- JavaScript (after paper renderer) -->
<script src="js/pm-paper-renderer.js"></script>
<script src="js/pm-paper-tooltips.js"></script>
```

#### 2. Ensure Data Loaded
The tooltip system automatically initializes when:
- `PMPaperRenderer.loaded` is true
- Formula and parameter data is available

### Advanced Configuration

#### Custom Tooltip Delays
```javascript
// Adjust timing
PMPaperTooltips.config.SHOW_DELAY = 300;  // ms before showing
PMPaperTooltips.config.HIDE_DELAY = 150;  // ms before hiding
```

#### Custom Positioning
```javascript
// Adjust offsets
PMPaperTooltips.config.OFFSET_X = 15;     // px from cursor
PMPaperTooltips.config.OFFSET_Y = 15;     // px from cursor
PMPaperTooltips.config.VIEWPORT_MARGIN = 30; // px from edge
```

#### Manual Tooltip Display
```javascript
// Show tooltip programmatically
const content = `
    <div class="tooltip-header">Custom Tooltip</div>
    <div class="tooltip-body">Content here</div>
`;
PMPaperTooltips.showTooltip(event, content, 'custom-type');

// Hide tooltip
PMPaperTooltips.hideTooltip();
```

### Adding Tooltips to New Elements

#### For Formula Variables
Ensure your formula data includes `terms`:
```json
{
    "id": "my-formula",
    "latex": "E = mc^2",
    "terms": {
        "E": {
            "description": "Energy",
            "units": "GeV"
        },
        "m": {
            "description": "Mass",
            "units": "GeV/c²"
        }
    }
}
```

#### For Parameters
Add parameters with metadata:
```json
{
    "my_param": {
        "value": 125.1,
        "source": "ESTABLISHED:PDG2024",
        "uncertainty": 0.14,
        "status": "ESTABLISHED",
        "metadata": {
            "description": "My parameter description",
            "units": "GeV"
        }
    }
}
```

Use in HTML:
```html
<span data-pm-value="category.my_param">?</span>
```

#### For Custom Acronyms
Edit the acronyms dictionary in `pm-paper-tooltips.js`:
```javascript
const acronyms = {
    'MYACR': 'My Acronym Expansion',
    // ... add more
};
```

Use in HTML:
```html
<abbr class="acronym">MYACR</abbr>
```

## Styling Customization

### Theme Colors
All colors use CSS custom properties. Override in your CSS:

```css
:root {
    --tooltip-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    --tooltip-border: rgba(139, 127, 255, 0.3);
    --tooltip-text: #f8f9fa;
    --tooltip-accent: #8b7fff;
}
```

### Custom Tooltip Types
Add custom styling for new tooltip types:

```css
.pm-tooltip-my-type {
    border-color: rgba(255, 100, 100, 0.4);
}

.pm-tooltip-my-type .tooltip-header {
    background: rgba(255, 100, 100, 0.1);
    border-bottom-color: rgba(255, 100, 100, 0.2);
}
```

### Button Customization
Customize interactive buttons:

```css
.copy-equation-btn {
    background: rgba(100, 200, 255, 0.2);
    border-color: rgba(100, 200, 255, 0.4);
    color: #64c8ff;
}

.copy-equation-btn:hover {
    background: rgba(100, 200, 255, 0.3);
    transform: scale(1.05);
}
```

## Performance Optimization

### Caching
The system caches formula and parameter data:
```javascript
// Check cache status
console.log(PMPaperTooltips.state.formulasCache);
console.log(PMPaperTooltips.state.parametersCache);
```

### Lazy Loading
Tooltips are created on-demand, not pre-rendered.

### Memory Management
- Only one tooltip exists in DOM at a time
- Tooltip content is cleared when hidden
- Event listeners use delegation (minimal overhead)

## Browser Support

### Modern Browsers (Full Support)
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Features by Browser
| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Tooltips | ✓ | ✓ | ✓ | ✓ |
| Copy to clipboard | ✓ | ✓ | ✓ | ✓ |
| Smart positioning | ✓ | ✓ | ✓ | ✓ |
| Touch support | ✓ | ✓ | ✓ | ✓ |
| Accessibility | ✓ | ✓ | ✓ | ✓ |

## Troubleshooting

### Tooltips Not Showing

**Check data loaded:**
```javascript
console.log(PMPaperRenderer.loaded);  // Should be true
console.log(PM._loaded);               // Should be true
```

**Check caches:**
```javascript
window.debugTooltips();  // Logs cache status
```

**Verify HTML attributes:**
```html
<!-- Correct -->
<span data-pm-value="pdg.m_higgs">?</span>

<!-- Incorrect (missing data-pm-value) -->
<span>125.1 GeV</span>
```

### Positioning Issues

**Adjust viewport margin:**
```javascript
PMPaperTooltips.config.VIEWPORT_MARGIN = 40;
```

**Override positioning CSS:**
```css
.pm-paper-tooltip {
    max-width: 400px !important;
}
```

### Mobile Touch Not Working

**Ensure touch events enabled:**
```javascript
// Check mobile detection
console.log(PMPaperTooltips.state.isMobile);
```

**Add explicit touch class:**
```html
<span class="demo-param touch-enabled" data-pm-value="...">?</span>
```

### Copy Button Not Working

**Check clipboard API:**
```javascript
console.log('Clipboard API:', navigator.clipboard ? 'Available' : 'Not available');
```

**Fallback for older browsers:**
The system automatically uses `document.execCommand('copy')` as fallback.

## Examples

### Full Implementation Example
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="css/pm-paper-tooltips.css">
</head>
<body>
    <p>
        The Higgs mass is
        <span data-pm-value="pdg.m_higgs">?</span>
        GeV, as shown in
        <a href="#eq-4.5" class="equation-ref">Eq. (4.5)</a>.
    </p>

    <div class="equation-wrapper" id="eq-4.5">
        <div class="equation-content">
            $$m_h = \sqrt{2\lambda v^2}$$
        </div>
        <div class="equation-number">(4.5)</div>
    </div>

    <script src="js/pm-constants-loader.js"></script>
    <script src="js/pm-formula-loader.js"></script>
    <script src="js/pm-paper-renderer.js"></script>
    <script src="js/pm-paper-tooltips.js"></script>
</body>
</html>
```

## API Reference

### Methods

#### `PMPaperTooltips.init()`
Initialize the tooltip system. Called automatically on page load.

#### `PMPaperTooltips.showTooltip(event, content, type)`
Show a tooltip with custom content.
- **event**: MouseEvent or synthetic event with pageX/pageY
- **content**: HTML string for tooltip body
- **type**: Tooltip type for styling ('variable', 'parameter', etc.)

#### `PMPaperTooltips.hideTooltip()`
Hide the current tooltip immediately.

#### `PMPaperTooltips.scheduleHide()`
Hide tooltip after configured delay.

### Properties

#### `PMPaperTooltips.config`
Configuration object:
```javascript
{
    SHOW_DELAY: 200,      // ms
    HIDE_DELAY: 100,      // ms
    OFFSET_X: 12,         // px
    OFFSET_Y: 12,         // px
    MAX_WIDTH: 500,       // px
    VIEWPORT_MARGIN: 20   // px
}
```

#### `PMPaperTooltips.state`
Current state:
```javascript
{
    currentTooltip: HTMLElement | null,
    currentTarget: HTMLElement | null,
    hideTimeout: number | null,
    showTimeout: number | null,
    isMobile: boolean,
    formulasCache: Object,
    parametersCache: Object
}
```

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

## Version History

### v1.0.0 (2025-12-28)
- Initial release
- Formula variable tooltips
- Parameter tooltips
- Formula reference tooltips
- Citation tooltips
- Acronym tooltips
- Copy to clipboard
- LaTeX/plain text toggle
- Mobile support
- Smart positioning
- Accessibility features
