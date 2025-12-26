# Principia Metaphysica: Standardized Template Schemas
## Single Source of Truth Migration Plan

**Version:** 1.0
**Date:** 2025-12-25
**Purpose:** Define standard metadata templates for Parameters, Formulas, and Sections

---

## 1. THREE-LEVEL DISPLAY ARCHITECTURE

All templates support three display levels:

| Level | Name | Paper Use | Website Use |
|-------|------|-----------|-------------|
| **L1** | Display | Inline value/formula | Compact inline |
| **L2** | Hover | N/A (footnote) | Tooltip on hover |
| **L3** | Expandable | Appendix/footnote | Accordion sections |

---

## 2. PARAMETER TEMPLATE

```python
@dataclass
class ParameterMetadata:
    """Complete metadata for any physical parameter."""

    # === LEVEL 1: DISPLAY (Always shown) ===
    id: str                              # Unique kebab-case ID (e.g., "higgs-mass")
    value: float                         # Numerical value
    units: str                           # Physical units (e.g., "GeV", "years")
    symbol: str                          # LaTeX/Unicode symbol (e.g., "m_H")
    display_value: str                   # Formatted display (e.g., "125.10 GeV")
    status: str                          # GEOMETRIC | DERIVED | CALIBRATED | INPUT | PREDICTED

    # === LEVEL 2: HOVER (Tooltip content) ===
    title: str                           # Human-readable name
    description: str                     # One-line description
    oom: float                           # Order of magnitude (log10 of value)
    uncertainty: Optional[float]         # Absolute uncertainty
    uncertainty_percent: Optional[float] # Relative uncertainty (%)

    # Experimental comparison
    experimental_value: Optional[float]
    experimental_error: Optional[float]
    experimental_source: str             # "PDG 2024", "NuFIT 6.0", etc.
    sigma_deviation: Optional[float]     # Deviation in sigma

    # === LEVEL 3: EXPANDABLE (Detailed sections) ===
    long_description: str                # Multi-paragraph explanation
    derivation: str                      # How it's computed
    derivation_formula_ids: List[str]    # Formula IDs used in derivation
    simulation_file: str                 # Source simulation

    # Bidirectional references
    used_in_formulas: List[str]          # Formula IDs that use this param
    depends_on_params: List[str]         # Param IDs this depends on
    section_refs: List[str]              # Section IDs where discussed

    # Documentation
    references: List[str]                # Citation IDs
    notes: str                           # Additional context
    website_only_notes: str              # Extra content for website (not paper)

    # Testability
    testable: bool
    testable_by: str                     # "HL-LHC", "Hyper-K", etc.
    testable_year: Optional[int]         # Expected year

    # Metadata
    version_introduced: str              # PM version (e.g., "v14.1")
    last_updated: str                    # Date string
```

---

## 3. FORMULA TEMPLATE

```python
@dataclass
class FormulaMetadata:
    """Complete metadata for any formula."""

    # === LEVEL 1: DISPLAY (Always shown) ===
    id: str                              # Unique kebab-case ID
    label: str                           # Equation label (e.g., "(2.6)")
    category: str                        # ESTABLISHED | THEORY | DERIVED | PREDICTIONS
    status: str                          # "EXACT MATCH", "TESTABLE", etc.

    # Representations
    latex: str                           # LaTeX for paper
    html: str                            # HTML for website
    plain_text: str                      # Plain text fallback

    # Computed result (if applicable)
    computed_value: Optional[float]
    computed_units: str

    # === LEVEL 2: HOVER (Term-level tooltips) ===
    terms: Dict[str, TermMetadata]       # Hoverable term definitions

    # Quick info
    short_description: str               # One-line summary
    section_ref: str                     # Primary section

    # === LEVEL 3: EXPANDABLE (Detailed sections) ===
    long_description: str                # Full explanation

    # Derivation chain
    derivation: DerivationMetadata       # Steps, assumptions, etc.

    # Sub-components (for complex formulas)
    components: List[FormulaComponent]   # Numerator, denominator, etc.

    # Experimental comparison
    experimental_value: Optional[float]
    experimental_error: Optional[float]
    experimental_source: str
    sigma_deviation: Optional[float]

    # Bidirectional references
    parent_formulas: List[str]           # Formulas this derives from
    child_formulas: List[str]            # Formulas derived from this
    uses_params: List[str]               # Parameter IDs used
    outputs_params: List[str]            # Parameter IDs this computes

    # Documentation
    references: List[str]                # Citation IDs
    learning_resources: List[LearningResource]
    simulation_file: str
    notes: str
    website_only_notes: str

    # Metadata
    attribution: str                     # "Principia Metaphysica"
    version_introduced: str
    last_updated: str

@dataclass
class TermMetadata:
    """Metadata for individual terms within a formula."""
    symbol: str                          # Display symbol
    name: str                            # Human name
    description: str                     # What it means

    # Display
    units: Optional[str]
    value: Optional[str]
    oom: Optional[float]

    # References
    param_id: Optional[str]              # Link to parameter
    formula_id: Optional[str]            # Link to defining formula
    link: Optional[str]                  # URL reference

@dataclass
class FormulaComponent:
    """Sub-component of a complex formula."""
    id: str                              # e.g., "numerator", "suppression-factor"
    label: str                           # Display label
    latex: str
    html: str
    description: str
    is_dominant: bool                    # Is this the main contribution?
    order_of_magnitude: Optional[float]

@dataclass
class DerivationMetadata:
    """Complete derivation information."""
    method: str                          # "geometric", "algebraic", "numerical"
    steps: List[DerivationStep]
    assumptions: List[str]
    approximations: List[str]
    parent_formulas: List[str]
    established_physics: List[str]
    verification_page: Optional[str]
    comments: str
    difficulty: str                      # "beginner", "intermediate", "advanced"

@dataclass
class DerivationStep:
    """Single step in derivation."""
    content: str                         # Step description
    level: str                           # "conceptual", "mathematical", "computational"
    formula_refs: List[str]              # Formula IDs referenced
    param_refs: List[str]                # Parameter IDs referenced
    assumptions: List[str]
    error_estimate: Optional[float]
    reference: Optional[str]
```

---

## 4. SECTION TEMPLATE

```python
@dataclass
class SectionMetadata:
    """Complete metadata for paper/website sections."""

    # === IDENTIFICATION ===
    id: str                              # Section ID (e.g., "2", "2.1", "A")
    title: str                           # Section title
    type: str                            # "section" | "subsection" | "appendix"
    parent_id: Optional[str]             # Parent section ID (for subsections)

    # === ABSTRACT ===
    abstract: str                        # Section summary (2-3 sentences)

    # === CONTENT BLOCKS ===
    content_blocks: List[ContentBlock]   # Ordered content

    # === APPENDICES ===
    appendices: List[AppendixMetadata]   # Associated appendices

    # === REFERENCES ===
    formula_refs: List[str]              # All formulas in this section
    param_refs: List[str]                # All parameters in this section
    figure_refs: List[str]               # Figure IDs
    table_refs: List[str]                # Table IDs
    citation_refs: List[str]             # Citations used

    # === NAVIGATION ===
    prev_section: Optional[str]
    next_section: Optional[str]
    subsections: List[str]               # Child section IDs

    # === METADATA ===
    paper_line_start: int                # Line number in main paper
    paper_line_end: int
    section_file: Optional[str]          # Corresponding sections/*.html
    website_only_content: List[ContentBlock]  # Extra for website

    # === DISPLAY ===
    beginner_summary: str                # Simplified explanation for website
    key_takeaways: List[str]             # Bullet points
    learning_objectives: List[str]       # What reader will learn

@dataclass
class ContentBlock:
    """Single block of content within a section."""
    type: str                            # "text" | "formula" | "param" | "figure" |
                                         # "table" | "callout" | "grid" | "panel"

    # For type="text"
    text: Optional[str]                  # Markdown/HTML text

    # For type="formula"
    formula_id: Optional[str]            # Reference to formula
    show_derivation: bool = False
    show_terms: bool = True

    # For type="param"
    param_id: Optional[str]              # Reference to parameter
    display_mode: str = "inline"         # "inline" | "card" | "full"

    # For type="figure"
    figure_id: Optional[str]
    caption: Optional[str]
    alt_text: Optional[str]

    # For type="table"
    table_id: Optional[str]
    columns: List[str]
    rows: List[List[str]]                # Can contain param_refs/formula_refs

    # For type="callout"
    callout_type: str = "info"           # "info" | "warning" | "derivation" | "example"
    title: Optional[str]
    content: List[ContentBlock]          # Nested blocks

    # For type="grid" or "panel"
    columns: int = 2
    children: List[ContentBlock]         # Nested blocks

    # Visibility
    paper_only: bool = False             # Only show in paper
    website_only: bool = False           # Only show on website
    expandable: bool = False             # Wrapped in accordion on website

@dataclass
class AppendixMetadata:
    """Appendix associated with a section."""
    id: str                              # Appendix letter/number
    title: str
    content_blocks: List[ContentBlock]
    simulation_code: Optional[str]       # Python simulation code
    simulation_file: str                 # File path
```

---

## 5. SECTION STRUCTURE FOR PAPER

Based on paper analysis, the sections are:

```json
{
  "sections": [
    {"id": "1", "title": "Introduction", "type": "section"},
    {"id": "2", "title": "The 26-Dimensional Bulk Spacetime", "type": "section"},
    {"id": "3", "title": "Reduction to the 13-Dimensional Shadow", "type": "section"},
    {"id": "4", "title": "Compactification on the TCS G₂ Manifold", "type": "section"},
    {"id": "5", "title": "Gauge Unification and the Standard Model", "type": "section"},
    {"id": "6", "title": "Fermion Sector and Mixing Angles", "type": "section"},
    {"id": "7", "title": "Cosmology and Dark Energy", "type": "section"},
    {"id": "8", "title": "Predictions and Testability", "type": "section"},
    {"id": "9", "title": "Discussion and Transparency", "type": "section"}
  ],
  "appendices": [
    {"id": "A", "title": "Virasoro Anomaly Cancellation", "parent_section": "2"},
    {"id": "B", "title": "Generation Number Derivation", "parent_section": "4"},
    {"id": "C", "title": "Atmospheric Mixing Angle Derivation", "parent_section": "6"},
    {"id": "D", "title": "Dark Energy Equation of State", "parent_section": "7"},
    {"id": "E", "title": "Proton Decay Calculation", "parent_section": "5"},
    {"id": "F", "title": "Dimensional Decomposition", "parent_section": "3"},
    {"id": "G", "title": "Effective Torsion from Flux Quantization", "parent_section": "4"},
    {"id": "H", "title": "Proton Decay Branching Ratio", "parent_section": "5"},
    {"id": "I", "title": "Gravitational Wave Dispersion", "parent_section": "7"},
    {"id": "J", "title": "Monte Carlo Error Propagation", "parent_section": "8"},
    {"id": "K", "title": "Transparency Statement", "parent_section": "9"},
    {"id": "L", "title": "Complete PM Values Summary", "parent_section": "8"},
    {"id": "M", "title": "Speculative Extensions - Consciousness", "parent_section": "9"},
    {"id": "N", "title": "G₂ Topology Landscape", "parent_section": "4"}
  ]
}
```

---

## 6. RENDERING APPROACH

### 6.1 Single Renderer Per Type

```javascript
// Section Renderer
function renderSection(sectionId, options = {}) {
    const { format = 'html', level = 'full' } = options;
    // format: 'html' (website) | 'latex' (paper)
    // level: 'display' | 'full' | 'summary'
}

// Formula Renderer
function renderFormula(formulaId, options = {}) {
    const { format = 'html', showTerms = true, showDerivation = false } = options;
}

// Parameter Renderer
function renderParam(paramId, options = {}) {
    const { format = 'html', mode = 'inline' } = options;
    // mode: 'inline' | 'card' | 'full'
}
```

### 6.2 Nested Rendering

```html
<!-- Section contains formulas -->
<pm-section section-id="2.1">
  <!-- Auto-renders content_blocks including: -->
  <pm-formula formula-id="master-action-26d"></pm-formula>
  <pm-param param-id="d-bulk" mode="card"></pm-param>
</pm-section>

<!-- Formula contains params -->
<pm-formula formula-id="generation-number">
  <!-- Terms auto-link to params via param_id -->
</pm-formula>
```

---

## 7. AGENT TASK ASSIGNMENTS

### 7.1 Parameter Agents (8 agents)

| Agent | Focus | Parameter Classes |
|-------|-------|-------------------|
| P1 | Dimensional & Fundamental | FundamentalConstants, DimensionalStructure |
| P2 | Topology | TCSTopologyParameters, G2SpinorGeometryParameters |
| P3 | Gauge & GUT | GaugeUnificationParameters, XYGaugeBosonParameters |
| P4 | Proton Decay | GeometricProtonDecayParameters, DoubletTripletSplittingParameters |
| P5 | Neutrino & PMNS | NeutrinoParameters, SeesawParameters, NeutrinoMassMatrix |
| P6 | Dark Energy & Cosmology | PhenomenologyParameters, MultiTimeParameters, LandscapeParameters |
| P7 | Pneuma & Moduli | PneumaRacetrackParameters, ModuliParameters, MashiachStabilization |
| P8 | Mirror & Higgs | MirrorSectorParameters, HiggsMassParameters, KKGravitonParameters |

### 7.2 Formula Agents (8 agents)

| Agent | Focus | Section Coverage |
|-------|-------|------------------|
| F1 | Section 2 | Master action, Virasoro, Pneuma, racetrack |
| F2 | Section 3 | Sp(2,R), primordial spinor, reduction |
| F3 | Section 4 | TCS topology, generation number, torsion |
| F4 | Section 5 | GUT scale, coupling, proton decay, breaking chain |
| F5 | Section 6 | PMNS angles, Yukawa, masses, CP phase |
| F6 | Section 7 | Dark energy w₀/wₐ, thermal time, effective dimension |
| F7 | Section 8 | KK graviton, predictions, testability |
| F8 | Appendices | All appendix formulas A-N |

### 7.3 Section Agents (8 agents)

| Agent | Focus | Sections |
|-------|-------|----------|
| S1 | Sections 1-2 | Introduction, 26D Bulk |
| S2 | Section 3 | 13D Shadow Reduction |
| S3 | Section 4 | TCS G₂ Compactification |
| S4 | Section 5 | Gauge Unification |
| S5 | Section 6 | Fermion Sector |
| S6 | Section 7 | Cosmology |
| S7 | Sections 8-9 | Predictions, Discussion |
| S8 | Appendices | All 14 appendices A-N |

---

## 8. VALIDATION CHECKLIST

Each agent must verify:

1. **Copy accuracy**: Content matches paper exactly (not paraphrased)
2. **ID consistency**: All formula_id/param_id references exist
3. **Bidirectional links**: If A references B, B should reference A
4. **Simulation match**: Computed values match simulation output
5. **Unit consistency**: Units are in standard format
6. **OOM present**: Every numerical parameter has order of magnitude
7. **Status correct**: GEOMETRIC/DERIVED/CALIBRATED matches derivation

---

## 9. TODO MARKERS

For content that doesn't fit templates, add:

```html
<!-- TODO:MIGRATE: [description of content] -->
<!-- Reason: [why it doesn't fit template] -->
```

Or in JSON:
```json
{
  "todos": [
    {
      "location": "section_2.content_blocks[5]",
      "description": "Complex SVG diagram needs separate handling",
      "priority": "medium"
    }
  ]
}
```

---

## 10. FILE OUTPUTS

After migration, theory_output.json will contain:

```json
{
  "version": "17.0",
  "generated": "2025-12-25T...",

  "parameters": {
    "higgs-mass": { /* ParameterMetadata */ },
    "m-gut": { /* ParameterMetadata */ },
    ...
  },

  "formulas": {
    "master-action-26d": { /* FormulaMetadata */ },
    "generation-number": { /* FormulaMetadata */ },
    ...
  },

  "sections": {
    "1": { /* SectionMetadata */ },
    "2": { /* SectionMetadata */ },
    ...
    "A": { /* AppendixMetadata */ },
    ...
  },

  "simulations": { /* existing simulation results */ },
  "statistics": { /* validation statistics */ },

  "todos": [ /* non-standardizable content */ ]
}
```
