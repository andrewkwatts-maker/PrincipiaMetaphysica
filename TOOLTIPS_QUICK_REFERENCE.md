# PM Paper Tooltips - Quick Reference

## Setup (3 Steps)

### 1. Include Files
```html
<!-- In <head> -->
<link rel="stylesheet" href="css/pm-paper-tooltips.css">

<!-- Before </body> -->
<script src="js/pm-paper-tooltips.js"></script>
<script src="js/pm-paper-tooltips-integration.js"></script>
```

### 2. Ensure Dependencies
```html
<script src="js/pm-constants-loader.js"></script>
<script src="js/pm-formula-loader.js"></script>
<script src="js/pm-paper-renderer.js"></script>
```

### 3. Done!
Auto-enhancement handles the rest.

---

## Usage

### Parameter Tooltips
```html
<!-- Path-based -->
<span data-pm-value="pdg.m_higgs">?</span>

<!-- Category-based -->
<span data-category="simulations" data-param="proton_decay.tau_p_years">?</span>
```

**Shows:** Value, units, uncertainty, source, status

---

### Equation References
```html
<!-- Auto-converted from text -->
See Eq. (4.2) for details

<!-- Manual link -->
<a href="#eq-4.2" class="equation-ref">Eq. (4.2)</a>
```

**Shows:** Equation preview

---

### Acronyms
```html
<!-- Auto-wrapped -->
The SM predicts three generations

<!-- Manual -->
<abbr class="acronym">GUT</abbr>
```

**Shows:** Full expansion

---

### Formula Variables
```html
<!-- In equation terms -->
<i>N_gen</i>
```

**Shows:** Variable definition from terms dict

---

## Interactive Features

### Copy to Clipboard
```html
<!-- Auto-added to formulas -->
<button class="copy-equation-btn">📋 Copy LaTeX</button>
```

### LaTeX Toggle
```html
<!-- Auto-added if plain text available -->
<button class="latex-toggle-btn">Show Plain Text</button>
```

### Collapsible Details
```html
<!-- Auto-added to formula cards -->
<button class="pm-expand-btn">▸</button>
```

---

## Configuration

### Timing
```javascript
PMPaperTooltips.config.SHOW_DELAY = 300;
PMPaperTooltips.config.HIDE_DELAY = 150;
```

### Positioning
```javascript
PMPaperTooltips.config.OFFSET_X = 15;
PMPaperTooltips.config.OFFSET_Y = 15;
PMPaperTooltips.config.VIEWPORT_MARGIN = 30;
```

---

## Styling

### Colors
```css
.pm-tooltip-variable { border-color: #64ffda; }
.pm-tooltip-parameter { border-color: #8b7fff; }
.pm-tooltip-formula-ref { border-color: #ffd700; }
.pm-tooltip-citation { border-color: #ffc107; }
.pm-tooltip-acronym { border-color: #4caf50; }
```

### Custom Tooltip Type
```css
.pm-tooltip-my-type {
    border-color: rgba(255, 100, 100, 0.4);
}

.pm-tooltip-my-type .tooltip-header {
    background: rgba(255, 100, 100, 0.1);
}
```

---

## API

### Show Tooltip
```javascript
const content = `
    <div class="tooltip-header">Title</div>
    <div class="tooltip-body">Content</div>
`;
PMPaperTooltips.showTooltip(event, content, 'type');
```

### Hide Tooltip
```javascript
PMPaperTooltips.hideTooltip();
```

### Check State
```javascript
console.log(PMPaperTooltips.state.currentTooltip);
console.log(PMPaperTooltips.state.isMobile);
```

---

## Debugging

### Check Data Loaded
```javascript
console.log(PM._loaded);
console.log(PMFormulaLoader._loaded);
```

### Check Caches
```javascript
window.debugTooltips();
```

### Verbose Logging
```javascript
PMPaperTooltips.config.DEBUG = true;
```

---

## Mobile Support

### Tap to Show
- Tap element → Show tooltip
- Tap again → Hide tooltip
- Tap elsewhere → Hide tooltip

### Centered Tooltips
```css
@media (max-width: 768px) {
    .pm-paper-tooltip {
        position: fixed !important;
        left: 5vw !important;
        width: 90vw !important;
    }
}
```

---

## Troubleshooting

### Tooltips Not Showing
```javascript
// 1. Check data loaded
console.log(PMPaperTooltips.state.formulasCache);

// 2. Check HTML attributes
// ✓ <span data-pm-value="pdg.m_higgs">?</span>
// ✗ <span>125.1 GeV</span>

// 3. Check for errors
// Open browser console (F12)
```

### Wrong Position
```javascript
// Increase viewport margin
PMPaperTooltips.config.VIEWPORT_MARGIN = 40;
```

### Slow Performance
```javascript
// Check cache hit rate
console.log(PMPaperTooltips.state.formulasCache);
console.log(PMPaperTooltips.state.parametersCache);

// Both should be non-null
```

---

## Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✓ Full |
| Firefox | 88+ | ✓ Full |
| Safari | 14+ | ✓ Full |
| Edge | 90+ | ✓ Full |
| Mobile Safari | 14+ | ✓ Full |
| Chrome Mobile | 90+ | ✓ Full |

---

## File Sizes

| File | Size | Gzipped |
|------|------|---------|
| pm-paper-tooltips.js | 60 KB | ~15 KB |
| pm-paper-tooltips.css | 20 KB | ~5 KB |
| pm-paper-tooltips-integration.js | 10 KB | ~3 KB |

**Total:** ~90 KB (~23 KB gzipped)

---

## Examples

### Full Page
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
        as shown in Eq. (4.5).
    </p>

    <script src="js/pm-constants-loader.js"></script>
    <script src="js/pm-formula-loader.js"></script>
    <script src="js/pm-paper-renderer.js"></script>
    <script src="js/pm-paper-tooltips.js"></script>
    <script src="js/pm-paper-tooltips-integration.js"></script>
</body>
</html>
```

### Programmatic
```javascript
// Show custom tooltip
document.getElementById('my-button').addEventListener('click', (e) => {
    PMPaperTooltips.showTooltip(e, `
        <div class="tooltip-header">Custom</div>
        <div class="tooltip-body">Content here</div>
    `, 'custom');
});
```

---

## Cheat Sheet

### Tooltip Types
- **variable** → Formula term definitions
- **parameter** → Parameter metadata
- **formula-ref** → Equation previews
- **citation** → Reference details
- **acronym** → Abbreviation expansions

### CSS Classes
- `.pm-paper-tooltip` → Main container
- `.tooltip-header` → Header section
- `.tooltip-body` → Body section
- `.tooltip-variable` → Variable name
- `.tooltip-value-row` → Value display
- `.tooltip-status` → Status badge

### Data Attributes
- `data-pm-value` → Parameter path
- `data-category` → Parameter category
- `data-param` → Parameter name
- `data-formula-id` → Formula ID
- `data-citation` → Citation key

---

**Version:** 1.0.0
**Updated:** 2025-12-28
