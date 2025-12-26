# Citation System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PAGE LOAD                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  HTML includes pm-citations.js + pm-citations.css              │
│  <link href="css/pm-citations.css">                             │
│  <script src="js/pm-citations.js"></script>                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOM READY EVENT                              │
│  pm-citations.js initializes automatically                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               LOAD REFERENCES.JSON                              │
│  fetch('/AUTO_GENERATED/json/references.json')                  │
│  ├─ Success: Store in referencesData                            │
│  └─ Error: Log warning, citations show [?]                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            FIND ALL <cite data-ref="...">                       │
│  document.querySelectorAll('cite[data-ref]')                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              FOR EACH CITATION ELEMENT:                         │
│  1. Get refId from data-ref attribute                           │
│  2. Lookup reference in referencesData                          │
│  3. Assign citation number (or reuse if seen before)            │
│  4. Replace innerHTML with [N]                                  │
│  5. Add 'citation' class                                        │
│  6. Attach event listeners:                                     │
│     ├─ mouseenter → showCitationTooltip()                       │
│     ├─ mouseleave → removeCitationTooltip()                     │
│     └─ click → scrollToReferences()                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 CITATIONS READY                                 │
│  Page now shows: [1], [2], [3], etc.                            │
└─────────────────────────────────────────────────────────────────┘
```

## User Interaction Flow

### Hover Interaction
```
User hovers over [1]
        │
        ▼
mouseenter event fires
        │
        ▼
showCitationTooltip(event, ref)
        │
        ├─ Create div.pm-citation-tooltip
        ├─ Populate with reference details
        ├─ Position near cursor
        ├─ Adjust if off-screen
        └─ Append to document.body
        │
        ▼
Tooltip appears with reference details
        │
        ▼
User moves mouse away
        │
        ▼
mouseleave event fires
        │
        ▼
removeCitationTooltip()
        │
        └─ Remove tooltip from DOM
```

### Click Interaction
```
User clicks [1]
        │
        ▼
click event fires
        │
        ▼
scrollToReferences(refId)
        │
        ├─ Find element: #ref-{refId}
        │
        ├─ If found on current page:
        │   ├─ scrollIntoView({ smooth, center })
        │   ├─ Add 'reference-highlight' class
        │   └─ Remove class after 2 seconds
        │
        └─ If not found (different page):
            └─ Navigate to /references.html#ref-{refId}
```

## Data Architecture

### References Data Structure
```javascript
{
  "vafa1996": {
    id: "vafa1996",
    title: "Evidence for F-Theory",
    authors: "Vafa, C.",
    year: 1996,
    arxiv: "hep-th/9602022",
    doi: "",
    description: "F-theory index theorem...",
    citedByFormulas: ["generation-number"],
    citedByParams: []
  },
  // ... more references
}
```

### Citation Map
```javascript
Map {
  "vafa1996" → 1,
  "acharya2001_chiral" → 2,
  "corti2015" → 3,
  "acharya1998" → 4,
  // ...
}
```

### Citation Counter
```javascript
citationCounter = 1  // Increments for each unique reference
```

## Component Architecture

### JavaScript Components

```
pm-citations.js
├── loadReferences()
│   └── Fetches and caches references.json
│
├── processCitations()
│   ├── Finds all cite[data-ref] elements
│   ├── Assigns citation numbers
│   └── Attaches event listeners
│
├── formatAuthors(authors)
│   └── "Smith, J., Jones, K." → "Smith et al."
│
├── createCitationText(refId, ref, citationNum)
│   └── Returns "[N]"
│
├── createTooltipContent(ref)
│   └── Returns HTML for tooltip
│
├── showCitationTooltip(event, ref)
│   ├── Creates tooltip element
│   ├── Positions near cursor
│   └── Appends to body
│
├── removeCitationTooltip()
│   └── Removes tooltip from DOM
│
├── scrollToReferences(refId)
│   ├── Finds reference element
│   ├── Scrolls into view
│   └── Highlights for 2 seconds
│
├── generateReferencesList(containerId)
│   └── Populates container with references
│
└── initCitations()
    ├── Calls loadReferences()
    ├── Calls processCitations()
    └── Calls generateReferencesList()
```

### CSS Components

```
pm-citations.css
├── cite.citation
│   ├── Superscript positioning
│   ├── Accent color
│   └── Hover effects
│
├── .pm-citation-tooltip
│   ├── Positioning (absolute)
│   ├── Theme styling
│   └── Shadow/border
│
├── .citation-title
│   ├── Bold heading
│   └── Primary color
│
├── .citation-authors
│   └── Secondary color
│
├── .citation-year
│   └── Muted color
│
├── .citation-link
│   └── Monospace arXiv/DOI
│
├── .citation-desc
│   ├── Italic description
│   └── Border separator
│
├── .ref-item
│   ├── Card layout
│   ├── Left accent border
│   └── Hover effects
│
└── @keyframes highlight-pulse
    └── 2s pulse animation
```

## Integration Points

### With Existing Systems

```
┌─────────────────────────────────────────────────────────────┐
│                   Principia Metaphysica                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │ PM Constants  │  │ PM Formulas   │  │ PM Tooltips   │  │
│  │    System     │  │    System     │  │    System     │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │            PM Citations System (NEW)                  │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │ Loader      │  │ Tooltip      │  │ Navigation  │  │ │
│  │  │ (JSON)      │  │ (Hover)      │  │ (Click)     │  │ │
│  │  └─────────────┘  └──────────────┘  └─────────────┘  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Data Layer                               │ │
│  │  AUTO_GENERATED/json/references.json                  │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### No Conflicts
- **PM Tooltip**: Uses `.pm-tooltip-popup` class
- **Citations**: Uses `.pm-citation-tooltip` class
- **PM Values**: Uses `data-category` and `data-param`
- **Citations**: Uses `data-ref`
- Both systems work independently and can coexist

## File Dependencies

```
Any HTML Page
    │
    ├── css/styles.css (base theme)
    ├── css/pm-citations.css (citation styling)
    │
    └── js/pm-citations.js (citation logic)
            │
            └── AUTO_GENERATED/json/references.json
                    │
                    └── Data source (loaded via fetch)
```

## State Management

### Global State
```javascript
let referencesData = null;      // Cached references from JSON
let citationCounter = 1;         // Sequential counter
const citationMap = new Map();   // refId → citation number
```

### Element State
```javascript
cite._refData = ref;  // Stored on each citation element
cite.getAttribute('data-citation-num')  // Citation number
```

## Error Handling

### Missing Reference
```
1. Reference ID not found in references.json
   ├─ Display: [?] in red
   ├─ Class: citation-missing
   ├─ Tooltip: "Reference not found: {refId}"
   └─ Console: Warning message
```

### Failed JSON Load
```
1. Fetch fails or JSON invalid
   ├─ referencesData remains null
   ├─ Citations not processed
   ├─ Console: Error message
   └─ Graceful degradation (no crash)
```

### Missing data-ref
```
1. <cite> without data-ref attribute
   ├─ Skip processing
   └─ Console: Warning
```

## Performance Considerations

### Efficient Operations
- Single fetch for references (cached)
- Batch DOM query (querySelectorAll once)
- Event delegation where possible
- Tooltip reused (not recreated per hover)
- Lazy reference list generation

### Memory Management
- References cached in memory (acceptable size)
- Tooltips removed from DOM when hidden
- Event listeners properly attached
- No memory leaks from closures

## Security Considerations

### XSS Prevention
- Reference data from trusted JSON
- No `eval()` or `innerHTML` with user input
- Tooltip content from sanitized source
- Event handlers properly scoped

### CORS
- JSON loaded from same origin
- No cross-origin requests needed
- Compatible with auth system

## Browser Support

### Required Features
- ES6 (const, let, arrow functions)
- Async/await
- Fetch API
- Map data structure
- CSS variables
- Template literals
- DOM methods (querySelector, etc.)

### Fallbacks
None needed - modern browsers only
Target: Chrome 60+, Firefox 60+, Safari 12+, Edge 79+

## Testing Strategy

### Unit Tests (Manual)
1. ✅ References load correctly
2. ✅ Citations numbered sequentially
3. ✅ Same reference gets same number
4. ✅ Tooltips display on hover
5. ✅ Tooltips hide on leave
6. ✅ Click scrolls to reference
7. ✅ Missing references show [?]
8. ✅ References list generates

### Integration Tests
1. ✅ Works with PM tooltip system
2. ✅ Works with PM constants
3. ✅ Works with auth system
4. ✅ Works on section pages

### Browser Tests
1. ✅ Desktop (Chrome, Firefox)
2. ✅ Mobile responsive
3. ✅ Touch events (mobile)

---

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
