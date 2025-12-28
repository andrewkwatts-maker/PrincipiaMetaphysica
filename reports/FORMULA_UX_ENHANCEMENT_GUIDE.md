# Formula UX Enhancement Guide

## Overview

The `Formula` dataclass in `config.py` has been enhanced to support rich interactive UX rendering, matching the capabilities demonstrated in `index.html`. This enables formulas to display with hoverable variables, info panels, expandable sections, and derivation chains.

## Enhanced Dataclasses

### 1. `FormulaTerm` (Enhanced)

Added `contribution` field to describe how each term contributes to the formula.

```python
@dataclass
class FormulaTerm:
    name: str                           # Display name (e.g., "S<sub>26D</sub> - Master Action")
    description: str                    # What the variable represents
    link: Optional[str] = None          # URL to learn more
    symbol: Optional[str] = None        # Unicode symbol for display
    value: Optional[str] = None         # Numerical value if applicable
    units: Optional[str] = None         # Physical units
    oom: Optional[float] = None         # Order of magnitude (log10)
    param_id: Optional[str] = None      # Link to parameter ID
    formula_id: Optional[str] = None    # Link to defining formula ID
    contribution: Optional[str] = None  # How it contributes to the formula (NEW)
```

**Usage Example:**
```python
term = FormulaTerm(
    symbol="S_26D",
    name="S<sub>26D</sub> - Master Action",
    description="The total 26-dimensional action",
    units="Dimensionless (natural units)",
    contribution="This is the fundamental action from which all physics emerges.",
    link="paper.html#framework"
)
```

### 2. `FormulaInfoItem` (New)

Displays key facts about the formula in an info grid panel.

```python
@dataclass
class FormulaInfoItem:
    title: str          # Grid item title (e.g., "Full Bulk")
    content: str        # Grid item content (e.g., "26D with signature (24,2)")
    link: Optional[str] = None  # URL to learn more
```

**Usage Example:**
```python
info_grid = [
    FormulaInfoItem(
        title="Full Bulk",
        content="26D with signature (24,2)",
        link="paper.html#section-2"
    ),
    FormulaInfoItem(
        title="Gauge Group",
        content="SO(10) ⊃ G_SM",
        link="paper.html#section-3"
    )
]
```

### 3. `FormulaSubComponent` (New)

Represents clickable sub-components in the expandable formula section.

```python
@dataclass
class FormulaSubComponent:
    symbol: str                         # HTML/Unicode symbol
    name: str                          # Component name
    description: str                   # Brief description
    link: Optional[str] = None         # URL to learn more
    badge: Optional[str] = None        # Badge text (e.g., "Established")
    badge_type: str = "established"    # established, theory, mathematics
```

**Usage Example:**
```python
sub_components = [
    FormulaSubComponent(
        symbol="M<sub>*</sub><sup>11</sup>R<sub>13</sub>",
        name="13D Einstein-Hilbert Term",
        description="13D gravity with reduced Planck mass M*",
        link="foundations/einstein-hilbert-action.html",
        badge="Established",
        badge_type="established"
    ),
    FormulaSubComponent(
        symbol="Γ<sup>M</sup>",
        name="13D Gamma Matrices",
        description="64×64 matrices from Clifford algebra Cl(12,1)",
        link="foundations/dirac-equation.html",
        badge="Clifford Algebra",
        badge_type="established"
    )
]
```

### 4. `FormulaDerivationStep` (New)

Represents a single step in the derivation chain showing the path to established physics.

```python
@dataclass
class FormulaDerivationStep:
    title: str                         # e.g., "Dirac Equation (1928)"
    link: Optional[str] = None         # URL to learn more
    badge: Optional[str] = None        # Badge text (e.g., "Established")
    badge_type: str = "established"    # established, theory, mathematics
```

**Usage Example:**
```python
derivation_chain = [
    FormulaDerivationStep(
        title="Dirac Equation (1928)",
        link="foundations/dirac-equation.html",
        badge="Established",
        badge_type="established"
    ),
    FormulaDerivationStep(
        title="Einstein-Hilbert Action (1915)",
        link="foundations/einstein-hilbert-action.html",
        badge="Established",
        badge_type="established"
    )
]
```

## Enhanced Formula Class

### New Fields in `Formula`

```python
@dataclass
class Formula:
    # ... existing required fields ...

    # === RICH UX RENDERING (for interactive formulas like index.html) ===
    # Interactive HTML display
    html_interactive: Optional[str] = None  # HTML with formula-var spans for hover tooltips

    # Info panel (formula meaning and context)
    info_title: Optional[str] = None        # e.g., "Unified 26-dimensional Action Principle"
    info_meaning: Optional[str] = None      # Long description of what the formula means
    info_grid: List[FormulaInfoItem] = field(default_factory=list)  # Key facts grid
    use_cases: List[str] = field(default_factory=list)  # What emerges from this formula

    # Expandable section
    expansion_title: Optional[str] = None   # Plain text LaTeX as section title
    sub_components: List[FormulaSubComponent] = field(default_factory=list)  # Clickable components
    derivation_chain: List[FormulaDerivationStep] = field(default_factory=list)  # Path to established physics
```

### Complete Usage Example

```python
from config import (
    Formula,
    FormulaTerm,
    FormulaInfoItem,
    FormulaSubComponent,
    FormulaDerivationStep,
    FormulaCategory
)

# Create interactive formula with all rich UX features
master_action = Formula(
    # Required fields
    id="master-action",
    label="(1.1) Master Action",
    html="S<sub>26D</sub> = ∫ d<sup>26</sup>X √|G<sub>(24,2)</sub>| [...]",
    latex=r"S_{26D} = \int d^{26}X \sqrt{|G_{(24,2)}|} [...]",
    plain_text="S_26D = ∫ d^26X √|G_(24,2)| [...]",
    category=FormulaCategory.THEORY,
    description="The unified 26-dimensional action principle",

    # Interactive HTML with hoverable variables
    html_interactive='''
        <a class="formula-var" href="paper.html#framework">
            S<sub>26D</sub>
            <div class="var-tooltip">
                <div class="var-name">S<sub>26D</sub> - Master Action</div>
                <div class="var-description">The total 26-dimensional action</div>
                <div class="var-units">Dimensionless</div>
            </div>
        </a>
    ''',

    # Info panel
    info_title="Unified 26-dimensional Action Principle",
    info_meaning="This single 26D action with signature (24,2) encodes ALL of physics through dimensional reduction.",
    info_grid=[
        FormulaInfoItem(
            title="Full Bulk",
            content="26D with signature (24,2)",
            link="paper.html#section-2"
        ),
        FormulaInfoItem(
            title="Effective Shadow",
            content="13D with signature (12,1)",
            link="paper.html#section-2"
        )
    ],
    use_cases=[
        "Einstein gravity + cosmological dynamics",
        "Standard Model gauge interactions",
        "Three generations of fermions"
    ],

    # Expandable section
    expansion_title="S_26D → S_13D → S_4D",
    sub_components=[
        FormulaSubComponent(
            symbol="M<sub>*</sub><sup>11</sup>R<sub>13</sub>",
            name="13D Einstein-Hilbert Term",
            description="13D gravity term",
            link="foundations/einstein-hilbert-action.html",
            badge="Established"
        )
    ],
    derivation_chain=[
        FormulaDerivationStep(
            title="Dirac Equation (1928)",
            link="foundations/dirac-equation.html",
            badge="Established"
        ),
        FormulaDerivationStep(
            title="Einstein-Hilbert Action (1915)",
            link="foundations/einstein-hilbert-action.html",
            badge="Established"
        )
    ]
)

# Export to JSON for theory_output.json
formula_data = master_action.to_dict()
```

## JSON Output Structure

When exported via `to_dict()`, the enhanced formula produces:

```json
{
  "id": "master-action",
  "label": "(1.1) Master Action",
  "html": "S<sub>26D</sub> = ...",
  "latex": "S_{26D} = ...",
  "plainText": "S_26D = ...",
  "category": "THEORY",
  "description": "The unified 26-dimensional action principle",

  "htmlInteractive": "<a class=\"formula-var\" ...>",

  "infoTitle": "Unified 26-dimensional Action Principle",
  "infoMeaning": "This single 26D action...",
  "infoGrid": [
    {
      "title": "Full Bulk",
      "content": "26D with signature (24,2)",
      "link": "paper.html#section-2"
    }
  ],
  "useCases": [
    "Einstein gravity + cosmological dynamics",
    "Standard Model gauge interactions"
  ],

  "expansionTitle": "S_26D → S_13D → S_4D",
  "subComponents": [
    {
      "symbol": "M<sub>*</sub><sup>11</sup>R<sub>13</sub>",
      "name": "13D Einstein-Hilbert Term",
      "description": "13D gravity term",
      "link": "foundations/einstein-hilbert-action.html",
      "badge": "Established",
      "badgeType": "established"
    }
  ],
  "derivationChain": [
    {
      "title": "Dirac Equation (1928)",
      "link": "foundations/dirac-equation.html",
      "badge": "Established",
      "badgeType": "established"
    }
  ]
}
```

## Frontend Integration

The enhanced Formula structure integrates seamlessly with the interactive formula display in `index.html`:

### 1. Variable Tooltips
- Use `FormulaTerm` with `contribution` field
- Render as `<a class="formula-var">` with nested `<div class="var-tooltip">`

### 2. Info Panel
- `info_title` → Formula heading
- `info_meaning` → Description paragraph
- `info_grid` → Grid of key facts
- `use_cases` → "What Emerges" list

### 3. Expandable Section
- `expansion_title` → Section header
- `sub_components` → Clickable component cards
- `derivation_chain` → Chain of derivation steps

## Migration Path

To upgrade existing formulas:

1. **Add interactive HTML**: Convert existing `html` field to include `formula-var` spans
2. **Add info panel**: Populate `info_title`, `info_meaning`, and `info_grid`
3. **Add use cases**: List what physics emerges from the formula
4. **Add components**: Break down formula into sub-components
5. **Add derivation**: Trace path back to established physics

## Testing

Run the test script to verify the enhancement works:

```bash
python test_formula_enhancements.py
```

Expected output:
```
SUCCESS: All enhanced Formula fields work correctly!

Formula ID: master-action
Info Title: Unified 26-dimensional Action Principle
Info Grid Items: 3
Use Cases: 4
Sub-Components: 2
Derivation Chain Steps: 3
```

## Benefits

1. **Rich Interactive Display**: Formulas can now show detailed tooltips, expandable sections, and derivation chains
2. **Educational Value**: Users can explore sub-components and trace formulas back to established physics
3. **Backward Compatibility**: All new fields are optional; existing formulas work unchanged
4. **Type Safety**: All fields are properly typed with dataclasses
5. **JSON Export**: Clean serialization to `theory_output.json` for frontend consumption

## Next Steps

1. **Populate Existing Formulas**: Enhance the 109 formulas in `theory_output.json` with rich UX fields
2. **Update Renderers**: Ensure `js/formula-loader.js` and section renderers consume these new fields
3. **Create Templates**: Build reusable templates for common formula patterns
4. **Document Patterns**: Establish conventions for info grids, use cases, and derivation chains
