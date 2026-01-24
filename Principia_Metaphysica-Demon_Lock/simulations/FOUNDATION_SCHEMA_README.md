# Foundation Schema System

A comprehensive schema and template system for managing theoretical foundations in the Principia Metaphysica framework.

## Overview

The Foundation Schema system provides:

- **Structured data models** for foundations and formulas
- **Validation functions** ensuring data integrity
- **Template generators** for HTML and JSON output
- **Utility functions** for working with theory_output.json
- **Command-line tools** for managing foundations
- **Category system** for organizing foundations by domain

## Files

```
simulations/
├── foundation_schema.py      # Core schema definitions and utilities
├── foundation_manager.py     # CLI tool for foundation management
└── FOUNDATION_SCHEMA_README.md  # This file

test_foundation_schema.py     # Test suite
```

## Quick Start

### 1. Create a Foundation

```python
from foundation_schema import FoundationEntry, FormulaEntry, CATEGORY_QUANTUM

# Create formulas
formula = FormulaEntry(
    id="schrodinger-eq",
    label="Schrödinger Equation",
    plain_text="iℏ ∂ψ/∂t = Ĥψ",
    latex=r"i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi",
    validated=True,
    description="Time-dependent Schrödinger equation"
)

# Create foundation
foundation = FoundationEntry(
    id="quantum-mechanics",
    title="Quantum Mechanics",
    category=CATEGORY_QUANTUM,
    year_established=1925,
    badge_type="established",
    main_equation="iℏ ∂ψ/∂t = Ĥψ",
    main_equation_latex=r"i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi",
    summary="Fundamental framework for quantum phenomena...",
    key_properties=[
        "Wave-particle duality",
        "Uncertainty principle",
        "Quantum superposition"
    ],
    pm_connection="The Pneuma field exhibits quantum behavior...",
    formulas=[formula],
    references=["Schrödinger (1926)"],
    tags=["quantum", "wave-function"]
)

# Validate
is_valid, errors = foundation.validate()
print(f"Valid: {is_valid}")
```

### 2. Generate Templates

```python
from foundation_schema import generate_html_template, generate_json_template

# Generate HTML
html = generate_html_template(foundation)
with open('foundation.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Generate JSON
json_str = generate_json_template(foundation)
with open('foundation.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
```

### 3. Work with theory_output.json

```python
from foundation_schema import (
    load_foundations_from_theory_output,
    save_foundations_to_theory_output,
    get_foundation_by_id
)

# Load foundations
foundations = load_foundations_from_theory_output('theory_output.json')

# Add new foundation
foundations.append(foundation)

# Save back
save_foundations_to_theory_output(foundations, 'theory_output.json', merge=True)

# Retrieve specific foundation
qm = get_foundation_by_id(foundations, 'quantum-mechanics')
```

## Command-Line Tool

The `foundation_manager.py` script provides a CLI for foundation management.

### List Foundations

```bash
# List all foundations
python simulations/foundation_manager.py list

# List by category
python simulations/foundation_manager.py list --category quantum
```

### Show Foundation Details

```bash
python simulations/foundation_manager.py show yang-mills-theory
```

### Validate Foundations

```bash
python simulations/foundation_manager.py validate
```

### Generate Reports

```bash
python simulations/foundation_manager.py report
```

### Export Foundations

```bash
# Export to HTML files
python simulations/foundation_manager.py export-html --output-dir output/foundations

# Export to JSON
python simulations/foundation_manager.py export-json --output-file foundations.json
```

### Add Example Foundation

```bash
python simulations/foundation_manager.py add-example
```

### Custom theory_output.json Path

```bash
python simulations/foundation_manager.py --theory-output custom_path.json list
```

## Data Schema

### FoundationEntry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | Unique identifier (alphanumeric, hyphens, underscores) |
| `title` | str | Yes | Foundation title |
| `category` | str | Yes | Category (see Categories below) |
| `year_established` | int | Yes | Year the theory was established (1600-2030) |
| `badge_type` | str | Yes | Badge type: "established" or "novel" |
| `main_equation` | str | Yes | Main equation (plain text) |
| `main_equation_latex` | str | No | LaTeX representation of main equation |
| `summary` | str | Yes | Brief summary of the foundation |
| `key_properties` | List[str] | Yes | List of key properties (min 1) |
| `pm_connection` | str | Yes | Connection to Principia Metaphysica |
| `formulas` | List[FormulaEntry] | No | Related formulas |
| `references` | List[str] | No | Academic references |
| `tags` | List[str] | No | Searchable tags |

### FormulaEntry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | Unique identifier |
| `label` | str | Yes | Formula label/name |
| `plain_text` | str | Yes | Plain text representation |
| `latex` | str | No | LaTeX representation |
| `validated` | bool | No | Whether formula is validated (default: False) |
| `description` | str | No | Description of the formula |

## Categories

Available foundation categories:

| Constant | Value | Description |
|----------|-------|-------------|
| `CATEGORY_GEOMETRY` | "geometry" | Geometric foundations |
| `CATEGORY_ALGEBRA` | "algebra" | Algebraic structures |
| `CATEGORY_THERMODYNAMICS` | "thermodynamics" | Thermodynamic principles |
| `CATEGORY_GRAVITY` | "gravity" | Gravitational theories |
| `CATEGORY_QUANTUM` | "quantum" | Quantum mechanics |
| `CATEGORY_TOPOLOGY` | "topology" | Topological concepts |
| `CATEGORY_GUT` | "grand-unification" | Grand Unified Theories |
| `CATEGORY_GAUGE` | "gauge-theory" | Gauge theories |
| `CATEGORY_SYMMETRY` | "symmetry" | Symmetry principles |
| `CATEGORY_INFORMATION` | "information-theory" | Information theory |

## Badge Types

| Constant | Value | Description |
|----------|-------|-------------|
| `BADGE_ESTABLISHED` | "established" | Established theoretical foundation |
| `BADGE_NOVEL` | "novel" | Novel contribution from PM |

## Validation

All entries are validated for:

- **Required fields**: No empty strings or None values
- **ID format**: Alphanumeric characters, hyphens, and underscores only
- **Category**: Must be from VALID_CATEGORIES
- **Badge type**: Must be from VALID_BADGE_TYPES
- **Year**: Must be between 1600 and 2030
- **Key properties**: Must have at least one entry
- **Formulas**: Each formula must pass its own validation

```python
is_valid, errors = foundation.validate()
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

## HTML Template Structure

Generated HTML follows this structure:

```html
<section class="foundation-entry" id="{id}" data-category="{category}">
  <div class="foundation-header">
    <h3>{title}</h3>
    <span class="badge badge-{badge_type}">{BADGE_TYPE}</span>
    <span class="year-badge">{year}</span>
  </div>

  <div class="main-equation" data-latex="{latex}">
    {main_equation}
  </div>

  <div class="foundation-summary">
    <p>{summary}</p>
  </div>

  <div class="key-properties">
    <h4>Key Properties</h4>
    <ul>
      <li>{property_1}</li>
      <!-- ... -->
    </ul>
  </div>

  <div class="pm-connection">
    <h4>Connection to Principia Metaphysica</h4>
    <p>{pm_connection}</p>
  </div>

  <h4>Related Formulas</h4>
  <ul class="formula-list">
    <li id="{formula_id}" data-latex="{latex}">
      <strong>{label}:</strong> {plain_text}
      <br><em>{description}</em>
    </li>
    <!-- ... -->
  </ul>
</section>
```

## JSON Template Structure

```json
{
  "id": "foundation-id",
  "title": "Foundation Title",
  "category": "category-name",
  "year_established": 1900,
  "badge_type": "established",
  "main_equation": "E = mc²",
  "main_equation_latex": "E = mc^2",
  "summary": "Foundation summary...",
  "key_properties": [
    "Property 1",
    "Property 2"
  ],
  "pm_connection": "Connection to PM...",
  "formulas": [
    {
      "id": "formula-id",
      "label": "Formula Label",
      "plain_text": "f(x) = x²",
      "latex": "f(x) = x^2",
      "validated": true,
      "description": "Description..."
    }
  ],
  "references": [
    "Author (Year). Title."
  ],
  "tags": [
    "tag1",
    "tag2"
  ]
}
```

## Helper Functions

### Filtering and Retrieval

```python
from foundation_schema import get_foundations_by_category, get_foundation_by_id

# Get all quantum foundations
quantum_foundations = get_foundations_by_category(foundations, CATEGORY_QUANTUM)

# Get specific foundation
foundation = get_foundation_by_id(foundations, 'yang-mills-theory')

# Get formula from foundation
formula = foundation.get_formula_by_id('gauge-covariant-derivative')
```

### Validation Reports

```python
from foundation_schema import validate_all_foundations

report = validate_all_foundations(foundations)
print(f"Valid: {report['valid']}/{report['total']}")

if report['invalid'] > 0:
    for error_info in report['errors']:
        print(f"\n{error_info['id']}: {error_info['title']}")
        for error in error_info['errors']:
            print(f"  - {error}")
```

### HTML Extraction (Beta)

```python
from foundation_schema import extract_foundation_from_html

# Extract from HTML content
html_content = """
<section data-category="quantum">
  <h2>Quantum Mechanics (1925)</h2>
  <div class="equation">iℏ ∂ψ/∂t = Ĥψ</div>
  <p class="summary">Fundamental framework...</p>
  <ul>
    <li>Wave-particle duality</li>
    <li>Uncertainty principle</li>
  </ul>
</section>
"""

foundation = extract_foundation_from_html(html_content, 'quantum-mechanics')
```

**Note**: HTML extraction is a basic parser and may need customization for specific HTML structures.

## Integration with theory_output.json

### Expected Structure

The schema expects `theory_output.json` to have a `foundations` array:

```json
{
  "foundations": [
    {
      "id": "foundation-1",
      "title": "...",
      ...
    },
    {
      "id": "foundation-2",
      "title": "...",
      ...
    }
  ],
  "other_data": {
    ...
  }
}
```

### Loading Behavior

- If `foundations` key doesn't exist, returns empty list
- File parsing errors are caught and reported
- Missing files trigger a warning but don't crash

### Saving Behavior

- Default behavior is to **merge** with existing data
- Only the `foundations` array is replaced
- Other top-level keys in theory_output.json are preserved
- Set `merge=False` to overwrite entire file (use with caution)

## Best Practices

### 1. Use Consistent IDs

```python
# Good: descriptive, hyphen-separated
id="yang-mills-theory"
id="schrodinger-equation"

# Bad: spaces, special characters
id="Yang Mills Theory"  # Has spaces
id="yang_mills/theory"  # Has slash
```

### 2. Provide LaTeX When Available

```python
# Always provide LaTeX for mathematical equations
main_equation="∇×E = -∂B/∂t",
main_equation_latex=r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}"
```

### 3. Write Clear PM Connections

```python
# Good: specific connection
pm_connection="The Pneuma Lagrangian incorporates Yang-Mills gauge structure through its SU(3)×SU(2)×U(1) symmetry, while extending it with topological and consciousness coupling terms."

# Bad: vague connection
pm_connection="This is related to PM."
```

### 4. Validate Before Saving

```python
# Always validate before saving
is_valid, errors = foundation.validate()
if is_valid:
    foundations.append(foundation)
    save_foundations_to_theory_output(foundations, 'theory_output.json')
else:
    print("Validation failed:", errors)
```

### 5. Use Tags for Searchability

```python
# Good: multiple relevant tags
tags=["gauge-theory", "standard-model", "non-abelian", "qcd"]

# Bad: no tags
tags=[]
```

## Testing

Run the test suite:

```bash
python test_foundation_schema.py
```

Test coverage includes:
- Formula creation and validation
- Foundation creation and validation
- Invalid entry rejection
- Template generation
- Validation reports
- Dictionary conversion

## Example: Complete Workflow

```python
from foundation_schema import (
    FoundationEntry,
    FormulaEntry,
    CATEGORY_GRAVITY,
    generate_html_template,
    load_foundations_from_theory_output,
    save_foundations_to_theory_output,
    validate_all_foundations
)

# 1. Create formulas
einstein_eq = FormulaEntry(
    id="einstein-field-eq",
    label="Einstein Field Equations",
    plain_text="Gμν = 8πG Tμν",
    latex=r"G_{\mu\nu} = 8\pi G T_{\mu\nu}",
    validated=True,
    description="Relates spacetime curvature to energy-momentum"
)

# 2. Create foundation
general_relativity = FoundationEntry(
    id="general-relativity",
    title="General Relativity",
    category=CATEGORY_GRAVITY,
    year_established=1915,
    badge_type="established",
    main_equation="Gμν = 8πG Tμν",
    main_equation_latex=r"G_{\mu\nu} = 8\pi G T_{\mu\nu}",
    summary="Einstein's theory of gravitation as curved spacetime geometry.",
    key_properties=[
        "Equivalence principle",
        "Geodesic motion",
        "Gravitational time dilation",
        "Frame-dragging effects"
    ],
    pm_connection="PM extends GR by incorporating topological defects and consciousness-matter coupling through the Pneuma field, providing a mechanism for dark energy and cosmic structure formation.",
    formulas=[einstein_eq],
    references=[
        "Einstein, A. (1915). Die Feldgleichungen der Gravitation. Sitzungsberichte der Preussischen Akademie der Wissenschaften, 844-847."
    ],
    tags=["gravity", "spacetime", "relativity", "einstein"]
)

# 3. Validate
is_valid, errors = general_relativity.validate()
print(f"Valid: {is_valid}")

# 4. Load existing foundations
foundations = load_foundations_from_theory_output('theory_output.json')

# 5. Add new foundation
foundations.append(general_relativity)

# 6. Validate all
report = validate_all_foundations(foundations)
print(f"Valid foundations: {report['valid']}/{report['total']}")

# 7. Save
if report['invalid'] == 0:
    save_foundations_to_theory_output(foundations, 'theory_output.json')
    print("Saved successfully!")
else:
    print("Fix errors before saving:")
    for error in report['errors']:
        print(f"  {error}")

# 8. Generate HTML for documentation
html = generate_html_template(general_relativity)
with open('general-relativity.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## Error Handling

The schema includes comprehensive error handling:

```python
# Validation errors
is_valid, errors = foundation.validate()
# Returns: (False, ['Foundation ID cannot be empty', ...])

# File loading errors
foundations = load_foundations_from_theory_output('missing.json')
# Prints warning, returns []

# Saving errors
success = save_foundations_to_theory_output(foundations, '/invalid/path.json')
# Prints error, returns False
```

## Future Enhancements

Potential improvements:

1. **Enhanced HTML Extraction**: More sophisticated HTML parsing for various formats
2. **Formula Validation**: Mathematical syntax checking for formulas
3. **Cross-References**: Link foundations that depend on each other
4. **Search Functionality**: Full-text search across foundations
5. **Version Control**: Track changes to foundations over time
6. **Export Formats**: PDF, Markdown, Wiki syntax
7. **Import from Sources**: BibTeX, arXiv, standard formats

## Contributing

When adding new foundations:

1. Use the schema structure defined in `foundation_schema.py`
2. Validate before committing
3. Provide LaTeX for mathematical content
4. Include clear PM connections
5. Add relevant references and tags
6. Test with `test_foundation_schema.py`

## License

Part of the Principia Metaphysica project.

---

**Last Updated**: 2025-12-26
**Version**: 1.0.0
