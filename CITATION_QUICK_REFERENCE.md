# Citation System - Quick Reference Card

## Setup (Add to HTML head)

```html
<link href="../css/pm-citations.css" rel="stylesheet"/>
<script src="../js/pm-citations.js"></script>
```

## Basic Usage

### Add a Citation
```html
<p>
    F-theory predicts three generations<cite data-ref="vafa1996"></cite>.
</p>
```

### Multiple Citations
```html
<p>
    String theory frameworks<cite data-ref="vafa1996"></cite><cite data-ref="acharya2001_chiral"></cite>
    support this prediction.
</p>
```

### Within Complex HTML
```html
<strong>TCS G₂ manifold<cite data-ref="corti2015"></cite></strong>
```

## References List

### Auto-Generate References
```html
<!-- Add this container anywhere on your page -->
<div id="references-container"></div>
```

System automatically populates it with all cited references.

## Common Reference IDs

| ID | Reference | Topic |
|----|-----------|-------|
| `vafa1996` | Vafa (1996) | F-theory, generation number |
| `acharya2001_chiral` | Acharya & Witten (2001) | Chiral fermions, G₂ |
| `corti2015` | Corti et al. (2015) | TCS G₂ manifolds |
| `acharya1998` | Acharya (1998) | M-theory, SO(10) |

See `AUTO_GENERATED/json/references.json` for all available references.

## What Users See

### Display
- **Before**: `<cite data-ref="vafa1996"></cite>`
- **After**: `[1]` (superscript, colored)

### Hover
Shows tooltip with:
- Title
- Authors
- Year
- arXiv/DOI
- Description

### Click
Scrolls to reference in references section

## JavaScript API

```javascript
// Manual refresh (for dynamic content)
PMCitations.refresh();

// Get citation numbers
const map = PMCitations.getCitationMap();

// Get references data
const refs = PMCitations.getReferencesData();
```

## Styling

### Customize Citation Appearance
```css
cite.citation {
    color: #8b7fff;          /* Citation color */
    font-weight: 600;        /* Citation weight */
}

cite.citation:hover {
    color: #ff7eb6;          /* Hover color */
}
```

### Customize Tooltip
```css
.pm-citation-tooltip {
    max-width: 400px;        /* Tooltip width */
    background: #1a1a2e;     /* Background */
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Citations show `[?]` | Check reference ID in `references.json` |
| No tooltips | Verify `pm-citations.css` is loaded |
| Not numbered | Check console for errors, verify `pm-citations.js` loaded |
| References empty | Ensure container ID is `references-container` |

## Console Messages

### Success
```
References loaded successfully: 50 references
Processed 12 citations
```

### Warnings
```
Warning: Reference not found: unknown_ref
Missing data-ref attribute on element
```

## File Locations

```
├── js/
│   ├── pm-citations.js           (JavaScript loader)
│   └── CITATION_SYSTEM_GUIDE.md  (Full documentation)
├── css/
│   └── pm-citations.css          (Styling)
├── AUTO_GENERATED/json/
│   └── references.json           (Data source)
└── test-citations.html           (Demo page)
```

## Examples in Production

### sections/fermion-sector.html

```html
<!-- Line 250-255: Head includes -->
<link href="../css/pm-citations.css" rel="stylesheet"/>
<script src="../js/pm-citations.js"></script>

<!-- Line 344: SO(10) citation -->
whose isometries give rise to the SO(10) gauge group<cite data-ref="acharya1998"></cite>.

<!-- Line 1054: Generation number citations -->
into three generations of Standard Model fermions<cite data-ref="vafa1996"></cite><cite data-ref="acharya2001_chiral"></cite>:

<!-- Line 3395: TCS manifold citation -->
TCS G₂ manifold<cite data-ref="corti2015"></cite>
```

## Best Practices

1. **Always verify reference IDs** before using
2. **Place citations after claims**, not in the middle of sentences
3. **Group multiple citations** together: `[1][2]` not `[1] and [2]`
4. **Use descriptive data-ref values** that match reference IDs exactly
5. **Check console** for warnings about missing references

## Key Features

- ✅ Dynamic loading from JSON (no hardcoding)
- ✅ Interactive hover tooltips
- ✅ Click navigation to references
- ✅ Auto-generated references list
- ✅ Sequential numbering
- ✅ Missing reference detection
- ✅ Mobile responsive
- ✅ Theme integration

## Support

**Documentation**: See `js/CITATION_SYSTEM_GUIDE.md` for comprehensive guide

**Architecture**: See `CITATION_SYSTEM_ARCHITECTURE.md` for system details

**Demo**: Open `test-citations.html` to see working examples

---

**Quick Test**: Open browser console and type:
```javascript
PMCitations.getCitationMap()
```
Should show citation number mappings.

---

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
