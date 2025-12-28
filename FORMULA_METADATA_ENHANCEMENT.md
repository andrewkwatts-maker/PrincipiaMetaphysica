# Formula Metadata Display Enhancement

**Principia Metaphysica - Scientific Rigor in Paper Rendering**

## Overview

Enhanced the paper rendering system to display complete formula metadata with scientific rigor. Each formula now shows comprehensive information including derivations, input/output parameters, experimental comparisons, and interactive tooltips.

## What Was Changed

### 1. Enhanced `pm-paper-renderer.js`

#### Expanded `renderEquation()` Function

The core equation rendering function now displays:

- **LaTeX Equation** - Main mathematical display with MathJax
- **Equation Number** - Right-aligned label (e.g., "(2.3)")
- **Plain Text Fallback** - Unicode representation for accessibility
- **Terms Dictionary** - Inline "where X is..., Y represents..." format
- **Description** - Context about what the formula computes
- **Expandable Metadata Panel** with:
  - 📥 **Input Parameters** - Color-coded chips with links
  - 📤 **Output Parameters** - What the formula computes
  - 🔬 **Derivation Steps** - Numbered step-by-step derivation
  - 📚 **References** - Academic citations
  - 📊 **Category Badge** - ESTABLISHED, THEORY, DERIVED, PREDICTION
  - 🎯 **Value Comparison** - Theory vs Experiment with σ deviation
  - 📝 **Notes** - Additional scientific context

#### New Helper Functions

- `formatScientificValue(value)` - Formats numbers with proper scientific notation
- `getCategoryBadge(category)` - Returns styled category badges
- `showEquationTooltip(event)` - Shows preview on equation reference hover
- `hideEquationTooltip(event)` - Cleans up tooltip

#### Enhanced Equation References

The `processEquationReferences()` function now:
- Converts "Eq. (4.2)" to clickable links
- Adds hover tooltips with formula preview
- Shows LaTeX and description on hover
- Smooth animations and positioning

### 2. New CSS File: `formula-metadata.css`

Complete styling for scientific formula display:

#### Main Sections

1. **Equation Wrapper** - Container with subtle gradient and border
2. **Equation Display** - LaTeX with right-aligned equation number
3. **Plain Text** - Monospace fallback for copying
4. **Terms Section** - Italic variables with definitions
5. **Metadata Panel** - Expandable with smooth animations
6. **Parameter Lists** - Color-coded chips (blue=input, orange=output)
7. **Derivation Steps** - Numbered with green accents
8. **References** - Purple-accented citation list
9. **Category Badges** - Color-coded by formula type
10. **Value Comparison** - Theory vs experiment with deviation status
11. **Equation Tooltips** - Frosted glass preview on hover

#### Color Coding

- **Input Parameters**: Blue (`rgba(59, 130, 246, ...)`)
- **Output Parameters**: Orange (`rgba(251, 146, 60, ...)`)
- **Derivation**: Green (`rgba(74, 222, 128, ...)`)
- **References**: Purple (`rgba(168, 85, 247, ...)`)
- **Values**: Green (`rgba(34, 197, 94, ...)`)
- **Notes**: Yellow (`rgba(255, 212, 59, ...)`)

#### Typography

- **Variables**: Italic Times New Roman (proper math typography)
- **Code/Parameters**: Source Code Pro or Fira Code monospace
- **Units**: Italic, lighter weight
- **Numbers**: Bold for emphasis in value comparisons

### 3. Test File: `test-formula-metadata.html`

Standalone demonstration showing:
- Three-generation formula with complete metadata
- Euler characteristic with terms dictionary
- Interactive equation cross-references
- Hover tooltip functionality

## Usage

### In Paper Sections

Formulas automatically render with metadata when loaded from `theory_output.json`:

```json
{
  "type": "equation",
  "formulaId": "three-generations",
  "label": "(2.3)"
}
```

### Required Formula Structure

Formulas in `formulas.json` should include:

```json
{
  "three-generations": {
    "id": "three-generations",
    "label": "(2.3)",
    "latex": "n_{\\text{gen}} = \\frac{\\chi_{\\text{eff}}}{48}",
    "plain_text": "n_gen = χ_eff / 48",
    "category": "THEORY",
    "description": "Number of fermion generations from index theorem",
    "input_params": ["topology.chi_eff"],
    "output_params": ["topology.n_gen"],
    "derivation": {
      "steps": [
        "Step 1: ...",
        "Step 2: ..."
      ],
      "references": [
        "Author (Year) Title"
      ]
    },
    "terms": {
      "n_gen": {
        "description": "the number of fermion generations",
        "symbol": "n_{\\text{gen}}"
      }
    },
    "computed_value": 3,
    "experimental_value": 3,
    "sigma_deviation": 0,
    "units": "dimensionless",
    "notes": "Additional context..."
  }
}
```

### CSS Integration

Include in your HTML:

```html
<link rel="stylesheet" href="css/formula-metadata.css">
```

## Scientific Features

### 1. Proper Math Typography

- Variables in italic (e.g., *n*, *χ*)
- Units in upright (e.g., GeV, eV)
- Numbers with proper formatting
- Subscripts and superscripts properly styled

### 2. Experimental Comparison

Shows theory vs experiment with:
- **Computed Value**: From theoretical calculation
- **Experimental Value**: From measurements
- **σ Deviation**: Agreement in standard deviations
- **Color Coding**: Green (< 1σ), Yellow (1-2σ), Orange (> 2σ)

### 3. Derivation Transparency

- Numbered steps showing logical progression
- References to academic literature
- Parent formula citations
- Methodological notes

### 4. Interactive References

- Hover over "Eq. (2.3)" shows preview tooltip
- Click jumps to equation
- Smooth animations and positioning
- MathJax typesetting in tooltips

### 5. Accessibility

- Plain text fallback for screen readers
- Keyboard navigation support
- High contrast color schemes
- Semantic HTML structure

## Responsive Design

### Desktop (> 768px)
- Two-column parameter display
- Full metadata panel
- Tooltip positioning optimized

### Tablet (768px - 480px)
- Single column layout
- Stacked value comparisons
- Adjusted padding and spacing

### Mobile (< 480px)
- Full-width parameters
- Vertical layout for all sections
- Touch-optimized button sizes

## Print Styles

When printing:
- Metadata panels auto-expand
- Black and white borders
- No interactive elements
- Page break avoidance

## Future Enhancements

1. **Parameter Linking**: Click parameter chips to jump to parameter definitions
2. **Formula Network Graph**: Visualize derivation dependencies
3. **Citation Export**: Copy BibTeX or citations
4. **Compare View**: Side-by-side formula comparison
5. **Search Integration**: Search within derivations and notes
6. **Version History**: Track formula refinements over time

## Files Modified

1. `js/pm-paper-renderer.js` - Enhanced equation rendering
2. `css/formula-metadata.css` - Complete metadata styling (NEW)
3. `test-formula-metadata.html` - Test demonstration (NEW)

## Testing

Open `test-formula-metadata.html` in a browser to see:
- Complete metadata display
- Expandable panels
- Hover tooltips
- Color-coded sections
- Value comparisons
- Interactive references

## Notes

- Maintains backward compatibility
- Graceful degradation if metadata missing
- Works with existing formula loader
- Integrates with MathJax v3
- No breaking changes to existing code

---

**Copyright © 2025-2026 Andrew Keith Watts. All rights reserved.**
