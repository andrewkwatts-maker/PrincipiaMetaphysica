# Academic Formula Rendering System

## Overview

The PM Paper Renderer now supports **academic paper-style formula rendering** that automatically formats equations with:

- Equation numbers at the right margin
- Parameter definitions below the formula
- Brief discussion of the formula's role
- Derivation references and citations
- Automatic cross-referencing in text

## Features

### 1. **Standard Academic Format**

Formulas are rendered in the traditional physics paper format:

```
                n_gen = χ_eff/48 = 144/48 = 3                    (4.2)

where n_gen is the number of fermion generations and χ_eff = 144
is the effective Euler characteristic of the G₂ manifold. This
result follows from the index theorem applied to the TCS construction
[see Section 2.3, Eq. (2.7)].
```

### 2. **Automatic Cross-References**

Text like "From Eq. (4.2), we obtain..." is automatically converted to clickable links that navigate to the equation.

### 3. **Metadata-Driven Content**

All formula information is pulled from `theory_output.json`:

```json
{
  "id": "generation-number",
  "label": "(4.2) Three Generations",
  "latex": "n_{gen} = \\frac{\\chi_{eff}}{48} = \\frac{144}{48} = 3",
  "description": "Number of fermion generations derived from TCS #187 Euler characteristic",
  "terms": {
    "n_gen": {
      "name": "Number of Generations",
      "description": "Number of fermion families - exactly 3 from topology"
    },
    "χ_eff": {
      "name": "Effective Euler Characteristic",
      "description": "χ_eff = 144 from TCS #187 construction"
    }
  },
  "derivation": {
    "parentFormulas": ["tcs-euler-characteristic"],
    "note": "See Section 2.3 for detailed derivation"
  }
}
```

## Usage

### In Section Content Blocks

Simply include a formula block in your section's `contentBlocks`:

```json
{
  "type": "formula",
  "label": "generation-number",
  "latex": "n_{gen} = \\frac{\\chi_{eff}}{48} = 3"
}
```

The renderer will automatically:
1. Look up the full formula metadata using the `label` as the formula ID
2. Extract the equation number from the label (e.g., "(4.2)")
3. Pull terms and descriptions from the formula metadata
4. Render in academic paper style with all components

### Formula Metadata Structure

#### Required Fields

- `id`: Unique identifier (kebab-case)
- `label`: Display label with equation number, e.g., "(4.2) Three Generations"
- `latex`: LaTeX equation code

#### Optional Fields

- `description`: Brief explanation of the formula's role
- `terms`: Object mapping symbols to definitions
- `derivation.parentFormulas`: Array of parent formula IDs
- `derivation.note`: Custom derivation note
- `section`: Section reference (e.g., "Section 4")

### Cross-References in Text

The system automatically converts equation references in text to links:

**Pattern Recognition:**
- `Eq. (4.2)` → Links to `#eq-4.2`
- `equation (4.2)` → Links to `#eq-4.2`
- `(4.2)` → Links to `#eq-4.2` (when preceded by equation-related text)

**Example:**

```json
{
  "type": "text",
  "content": "From Eq. (4.2), we obtain the three-generation structure. This follows from equation (2.7) via the index theorem."
}
```

Renders as text with clickable links to the equations.

## Implementation Details

### New Functions in `pm-paper-renderer.js`

#### `renderEquation(block)`

Main function that renders formulas in academic style.

**Parameters:**
- `block`: Formula content block with `type: 'formula'` or `type: 'equation'`

**Returns:**
- HTML string with complete academic-style equation

**Features:**
- Extracts equation number from label
- Pulls formula metadata from global formulas collection
- Renders with equation number at right margin
- Adds parameter definitions from `terms`
- Includes description/discussion
- Shows derivation references

#### `extractEquationNumber(label)`

Extracts equation number from formula label.

**Examples:**
- `"(4.2) Three Generations"` → `"4.2"`
- `"Eq. 4.2"` → `"4.2"`

#### `renderTermsDefinition(terms)`

Renders parameter definitions as inline text.

**Input:**
```json
{
  "n_gen": { "description": "number of fermion generations" },
  "χ_eff": { "description": "effective Euler characteristic" }
}
```

**Output:**
```
where n_gen is number of fermion generations, χ_eff is effective Euler characteristic
```

#### `formatFormulaReference(formula)`

Formats formula reference for citations.

**Output Examples:**
- `[Section 2.3, Eq. (2.7)]`
- `[Eq. (4.2)]`
- `[Section 4]`

#### `processEquationReferences(container)`

Post-processes text content to convert equation references to links.

**Features:**
- Scans all text nodes for equation patterns
- Skips code blocks and existing links
- Creates anchor links to `#eq-{number}`
- Preserves original text formatting

### CSS Styling

The system includes comprehensive CSS for academic formatting:

```css
/* Main equation wrapper */
.equation-wrapper.academic-equation {
  margin: 1.75rem 0;
  padding: 0.75rem 0;
}

/* Equation line with number at right */
.equation-line {
  display: flex;
  justify-content: space-between;
}

/* Centered equation content */
.equation-line .equation-content {
  flex: 1;
  text-align: center;
}

/* Equation number at right margin */
.equation-line .equation-number {
  flex-shrink: 0;
  padding-left: 1rem;
  color: #666;
}

/* Parameter definitions */
.equation-terms {
  margin: 0.75rem 0;
  color: #333;
}

/* Discussion text */
.equation-discussion {
  margin: 0.75rem 0;
  color: #333;
}

/* Derivation references */
.equation-derivation {
  margin: 0.5rem 0;
  color: #666;
  font-style: italic;
}

/* Cross-reference links */
.equation-ref {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

/* Highlight on navigation */
.equation-wrapper.academic-equation:target {
  background: rgba(102, 126, 234, 0.08);
  border-left: 3px solid #8b7fff;
}
```

## Best Practices

### 1. **Equation Numbering**

Use consistent numbering scheme:
- Section-based: `(4.2)` = Section 4, Equation 2
- Always use parentheses: `(4.2)` not `4.2`

### 2. **Parameter Definitions**

Write clear, concise definitions:
```json
"terms": {
  "m_h": {
    "description": "Higgs boson mass in GeV"
  }
}
```

Avoid redundant prefixes like "is the" - the renderer adds those.

### 3. **Derivation Notes**

Be specific about references:
```json
"derivation": {
  "parentFormulas": ["higgs-vev", "tcs-topology"],
  "note": "Derived using moduli stabilization conditions from Section 5.2"
}
```

### 4. **Formula IDs**

Use descriptive kebab-case IDs:
- ✅ `generation-number`, `higgs-mass`, `proton-lifetime`
- ❌ `eq42`, `formula1`, `x`

### 5. **Cross-References**

Always use standard formats:
- ✅ `"From Eq. (4.2), we see..."`
- ✅ `"This follows from equation (2.7)"`
- ❌ `"From eq 4.2"` (missing period and parentheses)

## Example: Complete Formula

### In theory_output.json

```json
{
  "id": "generation-number",
  "label": "(4.2) Three Generations",
  "latex": "n_{gen} = \\frac{\\chi_{eff}}{48} = \\frac{144}{48} = 3",
  "category": "TOPOLOGY",
  "description": "This result follows from the index theorem applied to the TCS construction with effective Euler characteristic χ_eff = 144.",
  "terms": {
    "n_gen": {
      "description": "number of fermion generations"
    },
    "χ_eff": {
      "description": "effective Euler characteristic of the G₂ manifold"
    },
    "48": {
      "description": "divisor from G₂ index theorem (2× F-theory's 24)"
    }
  },
  "derivation": {
    "parentFormulas": ["tcs-euler-characteristic"],
    "note": "See Section 2.3, Eq. (2.7) for the TCS construction details"
  },
  "section": "Section 4"
}
```

### In Section Content

```json
{
  "type": "text",
  "content": "The topology directly determines the number of generations:"
},
{
  "type": "formula",
  "label": "generation-number"
},
{
  "type": "text",
  "content": "From Eq. (4.2), we obtain exactly three generations with no free parameters."
}
```

### Rendered Output

```
The topology directly determines the number of generations:

                n_gen = χ_eff/48 = 144/48 = 3                    (4.2)

where n_gen is number of fermion generations, χ_eff is effective
Euler characteristic of the G₂ manifold, 48 is divisor from G₂
index theorem (2× F-theory's 24). This result follows from the
index theorem applied to the TCS construction with effective Euler
characteristic χ_eff = 144.

Derived from [Section 2.3, Eq. (2.7)]
See Section 2.3, Eq. (2.7) for the TCS construction details

From Eq. (4.2), we obtain exactly three generations with no free
parameters.
```

*(With "Eq. (4.2)" as a clickable link)*

## Testing

Use the test file to verify the rendering:

```bash
# Open in browser
open test-academic-formulas.html
```

The test page demonstrates:
1. Formula loaded from theory_output.json
2. Manual formula with custom parameters
3. Formula with derivation references
4. Cross-reference link generation

## Migration Guide

### From Old Format

**Before:**
```json
{
  "type": "equation",
  "latex": "n_{gen} = 3",
  "label": "Three Generations"
}
```

**After:**
```json
{
  "type": "formula",
  "label": "generation-number"
}
```

*With formula metadata in theory_output.json formulas section*

### Adding Metadata

For each formula in your sections:

1. Create entry in `formulas.formulas` with ID matching the label
2. Add `label` with equation number: `"(4.2) Title"`
3. Fill in `description`, `terms`, `derivation`
4. Update section content blocks to reference by ID

## Files Modified

- `h:\Github\PrincipiaMetaphysica\js\pm-paper-renderer.js`
  - Added `renderEquation()` function
  - Added `extractEquationNumber()` helper
  - Added `renderTermsDefinition()` helper
  - Added `formatFormulaReference()` helper
  - Added `processEquationReferences()` for cross-links
  - Updated `renderContentBlock()` to use new rendering
  - Exported new functions in API

- `h:\Github\PrincipiaMetaphysica\paper.html`
  - Added comprehensive CSS for academic equations
  - Added styles for cross-reference links
  - Added highlight effect for targeted equations

## Future Enhancements

Potential improvements for future versions:

1. **Automatic equation numbering** - Generate numbers based on section order
2. **Equation index** - Generate "List of Equations" section automatically
3. **LaTeX output** - Export to proper LaTeX format for journal submission
4. **Bibliography integration** - Link formulas to bibliography entries
5. **Interactive derivations** - Expand/collapse derivation steps
6. **Parameter tooltips** - Hover over symbols to see definitions

## Support

For questions or issues with the academic formula rendering system:

1. Check this documentation
2. Review test-academic-formulas.html examples
3. Inspect browser console for errors
4. Verify formula metadata structure in theory_output.json

---

**Version:** 1.0.0
**Last Updated:** 2025-12-28
**Author:** Claude (Anthropic)
**Copyright:** Andrew Keith Watts, 2025-2026
