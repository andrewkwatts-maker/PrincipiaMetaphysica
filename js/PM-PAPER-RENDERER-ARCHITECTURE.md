# PM Paper Renderer - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRINCIPIA METAPHYSICA                        │
│                   Dynamic Paper Renderer v1.0                    │
└─────────────────────────────────────────────────────────────────┘

                              DATA SOURCES
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│  theory_output.json                 sections/*.html               │
│  ─────────────────                 ─────────────────             │
│  • version                          • introduction.html           │
│  • metadata                         • geometric-framework.html    │
│  • sections                         • fermion-sector.html         │
│  • formulas                         • cosmology.html              │
│  • parameters                       • predictions.html            │
│  • simulations                      • conclusion.html             │
│  • statistics                       • ...                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │  LOADER LAYER        │
                    └──────────────────────┘
                               ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐    ┌────────────────┐    ┌────────────────┐
│ PM Constants  │    │ PM Formula     │    │ PM Paper       │
│ Loader        │    │ Loader         │    │ Renderer       │
├───────────────┤    ├────────────────┤    ├────────────────┤
│ • PM.get()    │    │ • PM.formula() │    │ • renderPaper()│
│ • PM.data     │    │ • getAll()     │    │ • renderSec()  │
│ • updateDOM() │    │ • getBy...()   │    │ • process...() │
└───────────────┘    └────────────────┘    └────────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │  RENDERING ENGINE    │
                    └──────────────────────┘
                               ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐    ┌────────────────┐    ┌────────────────┐
│ Title/Meta    │    │ Table of       │    │ Sections       │
│ Renderer      │    │ Contents       │    │ Renderer       │
│               │    │                │    │                │
│ • Title       │    │ • TOC list     │    │ • Load HTML    │
│ • Subtitle    │    │ • Section links│    │ • Process      │
│ • Author      │    │ • Subsections  │    │ • Content      │
│ • Date/Ver    │    │                │    │ • Formulas     │
│               │    │                │    │ • Parameters   │
└───────────────┘    └────────────────┘    └────────────────┘
                                                   ↓
                                    ┌──────────────────────┐
                                    │  CONTENT PROCESSORS  │
                                    └──────────────────────┘
                                           ↓
                    ┌──────────────────────┴─────────────────────┐
                    ↓                      ↓                      ↓
            ┌───────────────┐    ┌────────────────┐    ┌────────────────┐
            │ Formula       │    │ Parameter      │    │ Content Block  │
            │ Processor     │    │ Processor      │    │ Renderer       │
            ├───────────────┤    ├────────────────┤    ├────────────────┤
            │ • Find refs   │    │ • Find refs    │    │ • Paragraph    │
            │ • Lookup ID   │    │ • Lookup path  │    │ • Heading      │
            │ • Insert HTML │    │ • Format value │    │ • Formula      │
            │               │    │ • Insert text  │    │ • Equation     │
            │               │    │                │    │ • List         │
            │               │    │                │    │ • Code         │
            │               │    │                │    │ • Quote        │
            └───────────────┘    └────────────────┘    └────────────────┘
                                           ↓
                                    ┌──────────────────────┐
                                    │  MATHJAX INTEGRATION │
                                    └──────────────────────┘
                                           ↓
                                    MathJax.typesetPromise()
                                           ↓
                                    ┌──────────────────────┐
                                    │  RENDERED OUTPUT     │
                                    └──────────────────────┘
```

## Data Flow Sequence

```
1. PAGE LOAD
   └─> Load pm-constants-loader.js
       └─> Load pm-formula-loader.js
           └─> Load pm-paper-renderer.js

2. INITIALIZATION
   └─> PMPaperRenderer.renderPaper('container', options)
       │
       ├─> loadTheoryData()
       │   └─> Fetch theory_output.json
       │       └─> Parse JSON
       │           └─> Store in PaperRenderer._data
       │
       ├─> renderTitle(metadata)
       │   └─> Create .paper-title-section
       │       └─> Insert title, subtitle, author, date
       │
       ├─> renderAbstractSection(abstract)
       │   └─> Create .paper-abstract
       │       └─> Insert abstract text
       │
       ├─> renderTableOfContents(sections)
       │   └─> Create .paper-toc
       │       ├─> Sort sections by order
       │       └─> Create TOC links
       │
       └─> renderAllSections(sections)
           └─> For each section:
               ├─> renderSection(section)
               │   ├─> Create section header
               │   ├─> Load section HTML file
               │   │   └─> loadSectionFile(sectionFile)
               │   │       ├─> Fetch HTML file
               │   │       ├─> Parse with DOMParser
               │   │       ├─> Extract <body> content
               │   │       └─> Cache result
               │   │
               │   ├─> processFormulas(content)
               │   │   └─> Find [data-formula-id]
               │   │       └─> PM.formula(id)
               │   │           └─> Insert formula.html
               │   │
               │   ├─> processParameters(content)
               │   │   └─> Find [data-pm-value]
               │   │       └─> PM.get(path)
               │   │           └─> formatValue()
               │   │               └─> Insert text
               │   │
               │   └─> Append to container
               │
               └─> MathJax.typesetPromise([container])

3. COMPLETION
   └─> Return success/failure boolean
```

## Component Responsibilities

### PM Constants Loader (pm-constants-loader.js)
```
ROLE: Load and manage parameter values
PROVIDES:
  • PM.get(path) - Get any parameter value
  • PM.simulation(path) - Get simulation data
  • PM.dimensions - Dimension constants
  • PM.updateDOM() - Update all data-pm-value elements
DEPENDS ON:
  • theory_output.json
```

### PM Formula Loader (pm-formula-loader.js)
```
ROLE: Load and manage formulas
PROVIDES:
  • PM.formula(id) - Get formula by ID
  • PMFormulaLoader.get(id) - Get formula object
  • PMFormulaLoader.getByCategory(cat) - Get formulas by category
  • PMFormulaLoader.search(query) - Search formulas
DEPENDS ON:
  • theory_output.json (formulas section)
  • PM Constants Loader (optional)
```

### PM Paper Renderer (pm-paper-renderer.js)
```
ROLE: Build complete paper from sections
PROVIDES:
  • PMPaperRenderer.renderPaper(id, opts) - Render full paper
  • PMPaperRenderer.renderSection(section, opts) - Render section
  • PMPaperRenderer.renderFormula(id) - Get formula HTML
  • PMPaperRenderer.processFormulas(el) - Process formula refs
  • PMPaperRenderer.processParameters(el) - Process param refs
  • PMPaperRenderer.typesetMathJax(el) - Trigger MathJax
DEPENDS ON:
  • PM Constants Loader (for PM.get())
  • PM Formula Loader (for PM.formula())
  • theory_output.json
  • sections/*.html files
  • MathJax (optional)
```

## File Loading Strategy

```
theory_output.json lookup paths (tried in order):
  1. ./theory_output.json
  2. AUTO_GENERATED/theory_output.json
  3. ../theory_output.json
  4. ../AUTO_GENERATED/theory_output.json
  5. ../../theory_output.json
  6. ../../AUTO_GENERATED/theory_output.json

Section HTML file lookup paths (tried in order):
  1. {sectionFile}
  2. ../{sectionFile}
  3. ../../{sectionFile}
```

## Caching Strategy

```
┌─────────────────────────────────────┐
│         CACHING LAYERS              │
├─────────────────────────────────────┤
│                                     │
│  1. Session Storage Cache           │
│     └─> theory_output.json          │
│         (Fast reload on same page)  │
│                                     │
│  2. In-Memory Cache                 │
│     └─> Section HTML files          │
│         (PaperRenderer._sectionsCache)│
│                                     │
│  3. Browser Cache                   │
│     └─> All static files            │
│         (Controlled by server)      │
│                                     │
└─────────────────────────────────────┘
```

## Error Handling Flow

```
┌─────────────────────────────────────┐
│         ERROR SCENARIOS             │
├─────────────────────────────────────┤
│                                     │
│  1. theory_output.json not found    │
│     └─> Try fallback paths          │
│         └─> Try individual JSONs    │
│             └─> Show error          │
│                                     │
│  2. Section HTML file not found     │
│     └─> Log warning                 │
│         └─> Render without content  │
│             └─> Show abstract only  │
│                                     │
│  3. Formula ID not found            │
│     └─> Show "?" in element         │
│         └─> Add error class         │
│             └─> Add tooltip         │
│                                     │
│  4. Parameter path not found        │
│     └─> Try alias mappings          │
│         └─> Try alternate paths     │
│             └─> Show "?"            │
│                                     │
│  5. MathJax not available           │
│     └─> Render without typesetting  │
│         └─> Raw LaTeX visible       │
│                                     │
└─────────────────────────────────────┘
```

## State Management

```
PaperRenderer Object:
  ._data         → theory_output.json parsed data
  ._loaded       → boolean, is data loaded?
  ._loading      → Promise of load operation
  ._sectionsCache → Map<filePath, htmlContent>
  ._debug        → boolean, debug mode enabled?
```

## Integration Points

```
┌──────────────────────────────────────────────────────────┐
│                   EXTERNAL DEPENDENCIES                   │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Required:                                                │
│  • Fetch API (for loading JSON/HTML)                      │
│  • DOMParser (for parsing HTML)                           │
│  • Promise support (ES6+)                                 │
│                                                           │
│  Optional:                                                │
│  • MathJax v3 (for formula typesetting)                   │
│  • PM Constants Loader (for parameter values)             │
│  • PM Formula Loader (for formula data)                   │
│  • MutationObserver (for auto-updates)                    │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Performance Characteristics

```
Operation                    Time Complexity    Space Complexity
─────────────────────────────────────────────────────────────
Load theory_output.json      O(1) + network     O(n) data size
Render paper                 O(n) sections      O(n) DOM nodes
Process formulas             O(m) formula refs  O(1) per formula
Process parameters           O(p) param refs    O(1) per param
Load section HTML            O(1) + network     O(s) section size
MathJax typesetting          O(f) formulas      Varies
```

## Browser Support Matrix

```
Feature                 Chrome  Firefox  Safari  Edge
────────────────────────────────────────────────────
Fetch API                 ✓       ✓       ✓      ✓
DOMParser                 ✓       ✓       ✓      ✓
ES6 Promises              ✓       ✓       ✓      ✓
async/await               ✓       ✓       ✓      ✓
Template literals         ✓       ✓       ✓      ✓
Arrow functions           ✓       ✓       ✓      ✓
const/let                 ✓       ✓       ✓      ✓
Map/Set                   ✓       ✓       ✓      ✓
sessionStorage            ✓       ✓       ✓      ✓
MutationObserver          ✓       ✓       ✓      ✓

Minimum Version:          49      52      10     79
```

## Version History

```
v1.0.0 (2025-12-26)
├─ Initial release
├─ Dynamic paper rendering
├─ Section HTML loading
├─ Formula processing
├─ Parameter processing
├─ MathJax integration
├─ Comprehensive error handling
├─ Session caching
└─ Debug mode
```

## Future Architecture Extensions

```
Planned Features:
├─ Progressive section loading (lazy load on scroll)
├─ Search integration (full-text search across paper)
├─ Version comparison (diff between paper versions)
├─ Annotation system (user comments on sections)
├─ Export functionality (PDF, Word, Markdown)
├─ Print optimization (special print CSS)
└─ Mobile responsive (adaptive layout)
```

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
