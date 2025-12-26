# Citation System Guide

## Overview

The Principia Metaphysica citation system provides dynamic, interactive citations that link to the references database. Citations are loaded from `AUTO_GENERATED/json/references.json` and provide hover tooltips with full reference details.

## Quick Start

### 1. Include Required Files

Add these to your HTML `<head>`:

```html
<link rel="stylesheet" href="../css/pm-citations.css">
<script src="../js/pm-citations.js"></script>
```

### 2. Add Citations in Your Content

Use the `<cite>` element with a `data-ref` attribute:

```html
<p>
    The F-theory index theorem<cite data-ref="vafa1996"></cite> predicts
    three generations of fermions.
</p>
```

### 3. The System Automatically:

- Loads references from `AUTO_GENERATED/json/references.json`
- Replaces citations with numbered superscripts: [1], [2], etc.
- Adds hover tooltips showing full reference details
- Enables click-to-scroll to the references section
- Generates a formatted references list (if container exists)

## Usage Examples

### Basic Citation

```html
<p>
    M-theory compactifications<cite data-ref="acharya2001_chiral"></cite>
    provide a natural framework for chiral fermions.
</p>
```

### Multiple Citations

```html
<p>
    The generation number is predicted by string theory
    <cite data-ref="vafa1996"></cite><cite data-ref="acharya2001_chiral"></cite>.
</p>
```

### Within Complex HTML

```html
<p>
    The <strong>TCS G₂ manifold<cite data-ref="corti2015"></cite></strong>
    with b₃ = 24 provides the correct topology.
</p>
```

## Citation Features

### Interactive Tooltips

When hovering over a citation, users see:
- Full title
- Authors
- Year
- arXiv ID (if available)
- DOI (if available)
- Description

### Click Navigation

Clicking a citation:
1. Scrolls to the reference in the references section
2. Highlights the reference with an animation
3. If not on the references page, navigates to `references.html#ref-{id}`

### Automatic Numbering

Citations are numbered sequentially in order of appearance:
- First unique reference → [1]
- Second unique reference → [2]
- Same reference cited again → same number

## References Section

### Auto-Generate References List

To display a formatted references list, add a container:

```html
<div id="references-container"></div>
```

The system will populate it with all cited references in citation order.

### Custom Container ID

If using a different ID:

```javascript
PMCitations.generateReferencesList('my-custom-id');
```

## Reference Data Format

References in `AUTO_GENERATED/json/references.json`:

```json
{
  "vafa1996": {
    "id": "vafa1996",
    "title": "Evidence for F-Theory",
    "authors": "Vafa, C.",
    "year": 1996,
    "arxiv": "hep-th/9602022",
    "doi": "",
    "description": "F-theory index theorem: n_gen = χ/24 for D3-branes on CY4",
    "citedByFormulas": ["generation-number"],
    "citedByParams": []
  }
}
```

## JavaScript API

### Manual Initialization

```javascript
// Initialize citation system
await PMCitations.init();

// Refresh citations (after dynamic content loads)
PMCitations.refresh();

// Get citation mapping
const citationMap = PMCitations.getCitationMap();

// Get raw references data
const references = PMCitations.getReferencesData();
```

### Re-processing Citations

If you dynamically load content:

```javascript
// Load your dynamic content
document.getElementById('content').innerHTML = newContent;

// Refresh citations
PMCitations.refresh();
```

## CSS Customization

### Citation Link Styling

```css
cite.citation {
    color: var(--accent-primary);
    font-weight: 600;
    vertical-align: super;
}

cite.citation:hover {
    color: var(--accent-secondary);
    transform: scale(1.1);
}
```

### Tooltip Styling

```css
.pm-citation-tooltip {
    max-width: 400px;
    padding: 1rem;
    background: var(--bg-card);
    border-radius: 8px;
}
```

### References List Styling

```css
.ref-item {
    padding: 1.5rem;
    background: var(--bg-secondary);
    border-left: 3px solid var(--accent-primary);
}
```

## Best Practices

### 1. Verify Reference IDs

Ensure your `data-ref` values match IDs in `references.json`:

```html
<!-- Correct -->
<cite data-ref="vafa1996"></cite>

<!-- Wrong - typo in ID -->
<cite data-ref="vafa_1996"></cite>
```

### 2. Place Citations Naturally

```html
<!-- Good: After the claim -->
The theory predicts three generations<cite data-ref="vafa1996"></cite>.

<!-- Also good: After a phrase -->
Using F-theory<cite data-ref="vafa1996"></cite>, we derive...
```

### 3. Group Multiple Citations

```html
<!-- Multiple citations together -->
This is supported by string theory
<cite data-ref="vafa1996"></cite><cite data-ref="acharya2001_chiral"></cite>.

<!-- Not recommended: Separating with spaces -->
<cite data-ref="vafa1996"></cite> <cite data-ref="acharya2001_chiral"></cite>
```

### 4. Console Debugging

The system logs useful information:

```
References loaded successfully: 50 references
Processed 12 citations
```

Check for warnings about missing references:

```
Warning: Reference not found: unknown_ref
```

## Troubleshooting

### Citations Show [?]

**Problem**: Citation displays `[?]` with red color

**Causes**:
1. Reference ID doesn't exist in `references.json`
2. Typo in `data-ref` attribute
3. References file not loaded

**Solution**: Check console for warnings, verify ID in `references.json`

### Tooltips Not Showing

**Problem**: Hover shows nothing

**Causes**:
1. `pm-citations.css` not loaded
2. JavaScript errors preventing tooltip creation

**Solution**: Check browser console, verify CSS file is included

### Citations Not Numbered

**Problem**: Citations still show `data-ref` value

**Causes**:
1. `pm-citations.js` not loaded
2. Script loaded before DOM ready
3. Path to `references.json` incorrect

**Solution**: Check script order, verify file paths, check console

### References List Empty

**Problem**: `references-container` remains empty

**Causes**:
1. Container ID doesn't match (default: `references-container`)
2. No citations processed yet
3. Called before references loaded

**Solution**: Verify container ID, ensure citations exist on page

## Examples in Production

### Section File (fermion-sector.html)

```html
<head>
    <link href="../css/pm-citations.css" rel="stylesheet"/>
    <script src="../js/pm-citations.js"></script>
</head>
<body>
    <p>
        M-theory on G₂ manifolds<cite data-ref="acharya1998"></cite>
        naturally produces SO(10) gauge symmetry.
    </p>
</body>
```

### Test File

See `test-citations.html` for a complete working example.

## Integration with Other Systems

### Works With PM Tooltip System

The citation system coexists with the PM tooltip system:

```html
<!-- Citations with superscript numbers -->
<cite data-ref="vafa1996"></cite>

<!-- PM values with hover tooltips -->
<span class="pm-value" data-category="topology" data-param="b3"></span>
```

Both systems use independent tooltip implementations.

### Dynamic Content

For SPAs or dynamically loaded content:

```javascript
// After loading new content
fetch('/api/section')
    .then(response => response.text())
    .then(html => {
        document.getElementById('content').innerHTML = html;
        PMCitations.refresh(); // Re-process new citations
    });
```

## Future Enhancements

Potential improvements:

1. **Citation Styles**: Support multiple citation formats (APA, MLA, Chicago)
2. **BibTeX Export**: Generate BibTeX from cited references
3. **Bibliography Management**: Filter references by section/category
4. **Search Integration**: Link citations to search results
5. **Citation Analytics**: Track which references are most cited

## License

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

---

**Questions or Issues?**

Contact: AndrewKWatts@Gmail.com
