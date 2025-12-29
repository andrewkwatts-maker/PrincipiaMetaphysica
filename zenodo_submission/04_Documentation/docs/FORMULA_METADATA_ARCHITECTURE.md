# Formula Metadata Display Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FORMULA METADATA SYSTEM                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────────┐ ┌──────────┐ ┌────────────┐
        │   Data Layer │ │  Render  │ │   Style    │
        │              │ │  Layer   │ │   Layer    │
        │ formulas.json│ │ pm-paper │ │  formula-  │
        │              │ │ -renderer│ │  metadata  │
        └──────────────┘ └──────────┘ └────────────┘
                │             │             │
                └─────────────┼─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Browser Display │
                    │  (with MathJax)  │
                    └──────────────────┘
```

## Data Flow

```
1. LOAD: formulas.json → PMFormulaLoader/PaperRenderer._data
   │
   ├─ Parse JSON structure
   ├─ Cache in memory
   └─ Index by formula ID

2. RENDER: renderEquation(block) → HTML string
   │
   ├─ Extract formulaId from block
   ├─ Fetch formula from _data.formulas.formulas[formulaId]
   ├─ Build HTML structure:
   │  │
   │  ├─ Equation line (LaTeX + number)
   │  ├─ Plain text fallback
   │  ├─ Terms definitions
   │  ├─ Description
   │  └─ Metadata panel (expandable):
   │     │
   │     ├─ Input parameters
   │     ├─ Output parameters
   │     ├─ Derivation steps
   │     ├─ References
   │     ├─ Category badge
   │     ├─ Value comparison
   │     └─ Notes
   │
   └─ Return HTML

3. TYPESET: MathJax.typesetPromise([element])
   │
   └─ Render LaTeX → SVG/MathML

4. INTERACT: User interactions
   │
   ├─ Click "Show metadata" → Toggle .expanded class
   ├─ Hover equation reference → Show tooltip
   └─ Click equation reference → Scroll to equation
```

## Component Hierarchy

```
<div class="equation-wrapper academic-equation">
  │
  ├─ <div class="equation-line">
  │   ├─ <div class="equation-content">$$LaTeX$$</div>
  │   └─ <div class="equation-number">(2.3)</div>
  │
  ├─ <div class="equation-plaintext">Plain text</div>
  │
  ├─ <div class="equation-terms">
  │   └─ <div class="terms-intro">where ...</div>
  │
  ├─ <div class="equation-discussion">
  │   └─ <p>Description</p>
  │
  └─ <div class="equation-metadata-panel">
      │
      ├─ <button class="metadata-toggle">
      │   ├─ <span class="toggle-icon">▸</span>
      │   └─ <span class="toggle-text">Show...</span>
      │
      └─ <div class="metadata-content">
          │
          ├─ <div class="metadata-section metadata-inputs">
          │   ├─ <h5>📥 Input Parameters</h5>
          │   └─ <ul class="param-list">
          │       └─ <li class="param-item">
          │           └─ <code class="param-link">param</code>
          │
          ├─ <div class="metadata-section metadata-outputs">
          │   └─ [Same structure as inputs]
          │
          ├─ <div class="metadata-section metadata-derivation">
          │   ├─ <h5>🔬 Derivation</h5>
          │   └─ <ol class="derivation-steps">
          │       └─ <li class="derivation-step">Step N</li>
          │
          ├─ <div class="metadata-section metadata-references">
          │   ├─ <h5>📚 References</h5>
          │   └─ <ul class="reference-list">
          │       └─ <li class="reference-item">Citation</li>
          │
          ├─ <div class="metadata-section metadata-category">
          │   ├─ <h5>📊 Category</h5>
          │   └─ <div class="category-badge">
          │       ├─ <span class="badge">THEORY</span>
          │       └─ <p class="badge-desc">Description</p>
          │
          ├─ <div class="metadata-section metadata-values">
          │   ├─ <h5>🎯 Values</h5>
          │   └─ <div class="value-comparison">
          │       ├─ <div class="value-item value-computed">
          │       ├─ <div class="value-item value-experimental">
          │       └─ <div class="value-item value-deviation">
          │
          └─ <div class="metadata-section metadata-notes">
              ├─ <h5>📝 Notes</h5>
              └─ <p class="metadata-notes-text">Notes</p>
```

## CSS Class Naming Convention

```
Component Prefix Pattern:
  equation-*         → Main equation elements
  metadata-*         → Metadata panel elements
  param-*           → Parameter-related
  value-*           → Value comparison
  derivation-*      → Derivation steps
  reference-*       → Citation references
  badge-*           → Category badges
  tooltip-*         → Hover tooltips
```

## Function Call Graph

```
renderPaper(containerId)
  │
  ├─ loadTheoryData()
  │   └─ fetch(theory_output.json)
  │
  ├─ renderAllSections(container, sections)
  │   └─ renderSection(section)
  │       └─ renderSubsection(subsection)
  │           └─ renderContentBlock(block)
  │               └─ if block.type === 'equation':
  │                   renderEquation(block) ◄─── CORE FUNCTION
  │                     │
  │                     ├─ extractEquationNumber(label)
  │                     ├─ renderTermsDefinition(terms)
  │                     ├─ formatScientificValue(value)
  │                     ├─ getCategoryBadge(category)
  │                     └─ escapeHtml(text)
  │
  ├─ processFormulas(container)
  ├─ processParameters(container)
  ├─ processEquationReferences(container)
  │   └─ for each equation reference:
  │       ├─ addEventListener('mouseenter', showEquationTooltip)
  │       └─ addEventListener('mouseleave', hideEquationTooltip)
  │
  └─ MathJax.typesetPromise([container])
```

## Styling Cascade

```
Base Styles (formula-metadata.css)
  │
  ├─ .equation-wrapper             [Container]
  │   └─ .academic-equation         [Modifier]
  │
  ├─ .equation-line                 [Display]
  │   ├─ .equation-content          [LaTeX]
  │   └─ .equation-number           [Label]
  │
  ├─ .equation-plaintext            [Fallback]
  ├─ .equation-terms                [Definitions]
  ├─ .equation-discussion           [Description]
  │
  └─ .equation-metadata-panel       [Expandable]
      │
      ├─ .metadata-toggle           [Button]
      │   ├─ .toggle-icon           [▸ Arrow]
      │   └─ .toggle-text           [Label]
      │
      └─ .metadata-content          [Panel content]
          │
          ├─ .metadata-section      [Base section]
          │   ├─ .metadata-inputs   [Input params]
          │   ├─ .metadata-outputs  [Output params]
          │   ├─ .metadata-derivation [Steps]
          │   ├─ .metadata-references [Citations]
          │   ├─ .metadata-category   [Badge]
          │   ├─ .metadata-values     [Comparison]
          │   └─ .metadata-notes      [Context]
          │
          └─ Color coding applied via section classes
```

## State Management

```
Formula States:
  │
  ├─ LOADING
  │   └─ Fetch formulas.json
  │       └─ Parse → _data.formulas.formulas
  │
  ├─ LOADED
  │   └─ Render equations
  │       └─ Build HTML
  │           └─ Append to DOM
  │
  ├─ TYPESET
  │   └─ MathJax processing
  │       └─ LaTeX → SVG/MathML
  │
  └─ INTERACTIVE
      ├─ Panel collapsed (default)
      │   └─ Click toggle → EXPANDED
      │
      └─ Panel expanded
          └─ Click toggle → COLLAPSED

Reference States:
  │
  ├─ IDLE
  │   └─ Default link appearance
  │
  ├─ HOVER
  │   └─ Show tooltip
  │       ├─ Position near mouse
  │       ├─ Load formula preview
  │       └─ Typeset LaTeX
  │
  └─ CLICK
      └─ Scroll to equation
          └─ Highlight briefly (future)
```

## Event Flow

```
User Interactions:
  │
  ├─ Click "Show metadata" button
  │   │
  │   ├─ Event: onclick
  │   ├─ Target: .metadata-toggle
  │   ├─ Action: Toggle .expanded on parent .equation-metadata-panel
  │   └─ CSS: Slide down animation
  │
  ├─ Hover equation reference "Eq. (2.3)"
  │   │
  │   ├─ Event: mouseenter
  │   ├─ Target: .equation-ref
  │   ├─ Action: showEquationTooltip(event)
  │   │   ├─ Get equation number
  │   │   ├─ Find equation element
  │   │   ├─ Get formula data
  │   │   ├─ Create tooltip element
  │   │   ├─ Position near cursor
  │   │   └─ Typeset with MathJax
  │   └─ CSS: Fade in animation
  │
  └─ Click equation reference
      │
      ├─ Event: click
      ├─ Target: <a href="#eq-2.3">
      ├─ Action: Browser scroll to anchor
      └─ CSS: Smooth scroll behavior
```

## Responsive Breakpoints

```
Desktop (> 768px)
  │
  ├─ Full two-column parameter display
  ├─ Large equation numbers
  ├─ Side-by-side value comparison
  └─ Full tooltip width (400px)

Tablet (768px - 480px)
  │
  ├─ Single column parameters
  ├─ Stacked value comparison
  ├─ Reduced padding
  └─ Smaller tooltip (300px)

Mobile (< 480px)
  │
  ├─ Full-width parameters
  ├─ Vertical all layouts
  ├─ Touch-optimized buttons
  └─ Compact metadata sections

Print
  │
  ├─ Auto-expand all panels
  ├─ Black borders only
  ├─ No interactive elements
  └─ Page break avoidance
```

## Integration Points

```
External Dependencies:
  │
  ├─ MathJax v3
  │   ├─ LaTeX rendering
  │   ├─ SVG output
  │   └─ typesetPromise()
  │
  ├─ theory_output.json / formulas.json
  │   ├─ Formula metadata
  │   ├─ Section content
  │   └─ Parameter definitions
  │
  └─ PM Global Object (optional)
      ├─ PM.formula(id)
      ├─ PM.get(path)
      └─ PM.parameter(id)

Internal Dependencies:
  │
  ├─ pm-formula-loader.js
  │   └─ PMFormulaLoader.load()
  │
  └─ pm-paper-renderer.js
      ├─ renderPaper()
      ├─ renderSection()
      └─ renderEquation() ◄─── ENHANCED
```

## Performance Optimization

```
Optimization Strategy:
  │
  ├─ Lazy Loading
  │   ├─ Load formulas on demand
  │   └─ Render visible sections first
  │
  ├─ Caching
  │   ├─ localStorage for formulas
  │   ├─ MathJax output cache
  │   └─ Section HTML cache
  │
  ├─ Batching
  │   ├─ Single MathJax typeset call
  │   └─ Bulk DOM updates
  │
  └─ CSS Optimization
      ├─ GPU-accelerated transforms
      ├─ will-change hints
      └─ contain: paint
```

## Accessibility Tree

```
Semantic Structure:
  │
  ├─ <div role="region" aria-label="Equation 2.3">
  │   │
  │   ├─ Math content (MathML/SVG)
  │   │   └─ aria-label="n_gen equals chi_eff divided by 48"
  │   │
  │   ├─ Plain text alternative
  │   │   └─ visually-hidden for screen readers
  │   │
  │   └─ <button aria-expanded="false">
  │       └─ aria-controls="metadata-panel-2.3"
  │
  └─ <div id="metadata-panel-2.3" aria-hidden="true">
      └─ Metadata sections with proper headings
```

## Error Handling

```
Error Recovery:
  │
  ├─ Formula not found
  │   └─ Display formulaId with "not found" message
  │
  ├─ Invalid LaTeX
  │   └─ Fall back to plain text
  │
  ├─ Missing metadata
  │   └─ Gracefully skip section
  │
  ├─ MathJax fails
  │   └─ Show raw LaTeX in code block
  │
  └─ Tooltip positioning off-screen
      └─ Adjust to viewport bounds
```

---

**Architecture Version:** 1.0
**Last Updated:** 2025-12-28
