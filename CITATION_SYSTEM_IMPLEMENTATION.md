# Citation System Implementation Summary

## Overview

A complete, dynamic citation system has been implemented for Principia Metaphysica that loads references from `AUTO_GENERATED/json/references.json` and provides interactive citations with hover tooltips and click-to-navigate functionality.

## Files Created

### 1. JavaScript Loader
**File**: `h:\Github\PrincipiaMetaphysica\js\pm-citations.js` (10KB)

**Features**:
- Dynamically loads references from JSON
- Processes all `<cite data-ref="...">` elements
- Assigns sequential citation numbers [1], [2], etc.
- Creates hover tooltips with full reference details
- Enables click navigation to references section
- Auto-generates formatted references list
- Provides public API for dynamic content

**Key Functions**:
```javascript
PMCitations.init()           // Initialize system
PMCitations.refresh()        // Re-process citations
PMCitations.getCitationMap() // Get citation numbers
PMCitations.getReferencesData() // Get raw references
```

### 2. CSS Styling
**File**: `h:\Github\PrincipiaMetaphysica\css\pm-citations.css` (5KB)

**Features**:
- Superscript citation numbers with hover effects
- Beautiful tooltip design matching site theme
- Formatted references list with hover highlights
- Smooth scroll animations
- Responsive mobile design
- Color-coded missing citations

**Key Styles**:
- `.citation` - Superscript citation links
- `.pm-citation-tooltip` - Hover tooltip popup
- `.ref-item` - Reference list entries
- `.reference-highlight` - Scroll animation

### 3. Demo Page
**File**: `h:\Github\PrincipiaMetaphysica\test-citations.html` (4KB)

**Purpose**: Demonstrates complete citation system functionality

**Includes**:
- Multiple citation examples
- Tooltip demonstrations
- References auto-generation
- Usage instructions
- Console logging for debugging

### 4. Documentation
**File**: `h:\Github\PrincipiaMetaphysica\js\CITATION_SYSTEM_GUIDE.md` (8KB)

**Contents**:
- Quick start guide
- Usage examples
- API documentation
- Troubleshooting guide
- Best practices
- Integration examples

## Updated Files

### Section File Updated
**File**: `h:\Github\PrincipiaMetaphysica\sections\fermion-sector.html`

**Changes**:
1. Added CSS include: `<link href="../css/pm-citations.css" rel="stylesheet"/>`
2. Added JS include: `<script src="../js/pm-citations.js"></script>`
3. Added 3 citations demonstrating the system:
   - Line 344: `<cite data-ref="acharya1998"></cite>` (SO(10) from M-theory)
   - Line 1054: `<cite data-ref="vafa1996"></cite><cite data-ref="acharya2001_chiral"></cite>` (three generations)
   - Line 3395: `<cite data-ref="corti2015"></cite>` (TCS G₂ manifold)

## How It Works

### 1. HTML Usage
```html
<p>
    F-theory predicts three generations<cite data-ref="vafa1996"></cite>.
</p>
```

### 2. System Processing
1. JavaScript loads on page load
2. Fetches `AUTO_GENERATED/json/references.json`
3. Finds all `<cite data-ref="...">` elements
4. Replaces with numbered citations: `[1]`, `[2]`, etc.
5. Attaches hover and click event listeners

### 3. User Interaction
- **Hover**: Shows tooltip with full reference details
- **Click**: Scrolls to reference in references section
- **Visual**: Superscript numbers with color effects

### 4. Auto-Generated References List
```html
<div id="references-container"></div>
```
System automatically populates with formatted references.

## Citation Features

### Interactive Tooltips
Display on hover:
- Full title
- Authors
- Publication year
- arXiv ID (if available)
- DOI (if available)
- Description/context

### Smart Numbering
- First occurrence: Gets next available number
- Repeat citations: Use same number
- Sequential ordering: [1], [2], [3], etc.
- Missing references: Show [?] in red

### Navigation
- Click citation → scroll to reference
- Smooth scroll animation
- Highlight reference for 2 seconds
- Cross-page navigation support

## Integration

### Required Includes
```html
<head>
    <link rel="stylesheet" href="css/pm-citations.css">
    <script src="js/pm-citations.js"></script>
</head>
```

### Works With Existing Systems
- **PM Tooltip System**: Independent implementation
- **PM Constants**: No conflicts
- **Formula System**: Compatible
- **Auth System**: Works on protected pages

## Data Source

### References JSON
**Location**: `AUTO_GENERATED/json/references.json`

**Format**:
```json
{
  "vafa1996": {
    "id": "vafa1996",
    "title": "Evidence for F-Theory",
    "authors": "Vafa, C.",
    "year": 1996,
    "arxiv": "hep-th/9602022",
    "doi": "",
    "description": "F-theory index theorem...",
    "citedByFormulas": ["generation-number"],
    "citedByParams": []
  }
}
```

### Dynamic Loading
- Fetched asynchronously on page load
- Cached in memory
- Available to all citation elements
- No hardcoded references

## Visual Design

### Citation Appearance
- Superscript numbers in accent color
- Hover: Scale up + color change
- Cursor: Pointer (indicates clickable)
- Missing: Red [?] with help cursor

### Tooltip Design
- Max width: 400px
- Dark theme matching site
- Rounded corners (8px)
- Drop shadow for depth
- Positioned near cursor
- Auto-adjusts if off-screen

### References List
- Card-based layout
- Left border in accent color
- Hover effect: Color shift
- Sequential numbering
- Grouped information
- Linked arXiv/DOI

## Testing

### Test File
**Location**: `h:\Github\PrincipiaMetaphysica\test-citations.html`

**Test Coverage**:
- Single citations
- Multiple citations in sequence
- Same reference cited multiple times
- Citations within complex HTML
- Tooltip display
- Click navigation
- References list generation

### Console Logging
System logs helpful information:
```
References loaded successfully: 50 references
Processed 12 citations
```

Warnings for issues:
```
Warning: Reference not found: unknown_id
```

## Example Usage in Production

### fermion-sector.html
Three citations added:

1. **M-theory SO(10)**:
```html
whose isometries give rise to the SO(10) gauge group<cite data-ref="acharya1998"></cite>.
```

2. **Three Generations**:
```html
into three generations of Standard Model fermions<cite data-ref="vafa1996"></cite><cite data-ref="acharya2001_chiral"></cite>:
```

3. **TCS G₂ Manifold**:
```html
TCS G₂ manifold<cite data-ref="corti2015"></cite>
```

## API Examples

### Basic Usage
```javascript
// Auto-initialized on page load
// Citations processed automatically
```

### Dynamic Content
```javascript
// Load new content
document.getElementById('content').innerHTML = newHTML;

// Refresh citations
PMCitations.refresh();
```

### Access Data
```javascript
// Get citation mapping
const map = PMCitations.getCitationMap();
// Map: vafa1996 → 1, acharya1998 → 2, etc.

// Get all references
const refs = PMCitations.getReferencesData();
```

## Browser Compatibility

- Modern browsers (ES6+ required)
- Async/await support needed
- Fetch API required
- CSS variables supported
- Mobile responsive

## Performance

- Lazy loads references on demand
- Efficient DOM queries
- Event delegation where possible
- Tooltip reused (not recreated)
- Minimal memory footprint

## Future Enhancements

Potential additions:
1. Citation style formats (APA, MLA, Chicago)
2. BibTeX export functionality
3. Citation search/filter
4. Analytics (most cited)
5. Inline reference mode option
6. PDF export with bibliography

## Summary

A complete, production-ready citation system that:
- ✅ Dynamically loads from references.json
- ✅ Uses data attributes (not hardcoded)
- ✅ Provides interactive tooltips
- ✅ Enables click navigation
- ✅ Auto-generates references list
- ✅ Integrates seamlessly with existing systems
- ✅ Includes comprehensive documentation
- ✅ Demonstrates working examples

## Files Summary

| File | Size | Purpose |
|------|------|---------|
| js/pm-citations.js | 10KB | JavaScript loader and processor |
| css/pm-citations.css | 5KB | Visual styling |
| test-citations.html | 4KB | Demo and testing |
| js/CITATION_SYSTEM_GUIDE.md | 8KB | User documentation |
| sections/fermion-sector.html | Updated | Production example |

**Total New Code**: ~27KB
**Lines of Code**: ~600
**Time to Implement**: Complete and tested

---

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
