# Foundation Configuration Schema System - Implementation Summary

## Overview

A complete foundation configuration schema and template system has been created for the Principia Metaphysica project. This system provides structured data management, validation, and template generation for theoretical foundations.

## Files Created

### Core System Files

1. **`simulations/foundation_schema.py`** (632 lines)
   - Core schema definitions (`FoundationEntry`, `FormulaEntry` dataclasses)
   - Validation functions with comprehensive error reporting
   - HTML and JSON template generators
   - Integration with theory_output.json
   - Helper functions for filtering, retrieval, and validation
   - Category and badge type constants
   - Example foundation creation

2. **`simulations/foundation_manager.py`** (399 lines)
   - Command-line interface for foundation management
   - Commands: list, show, validate, report, export-html, export-json, add-example
   - Manager class with load/save operations
   - Report generation with statistics
   - Export functionality to multiple formats

3. **`test_foundation_schema.py`** (152 lines)
   - Comprehensive test suite
   - Tests for formula and foundation creation
   - Validation testing (valid and invalid cases)
   - Template generation testing
   - Dictionary conversion testing
   - All tests passing

4. **`simulations/foundation_example.py`** (296 lines)
   - Complete working examples
   - Three example foundations:
     - Riemannian Geometry (established, 1854)
     - Quantum Field Theory (established, 1948)
     - TCS Topology (novel, 2024)
   - Demonstrates full workflow from creation to export

### Documentation Files

5. **`simulations/FOUNDATION_SCHEMA_README.md`** (681 lines)
   - Complete reference documentation
   - Data schema specifications
   - API reference for all functions
   - HTML and JSON template structure
   - Integration guide for theory_output.json
   - Best practices and examples
   - Error handling guide

6. **`simulations/FOUNDATION_QUICK_START.md`** (240 lines)
   - 5-minute tutorial
   - Quick reference for common tasks
   - Command cheat sheet
   - Troubleshooting guide
   - Minimal examples for quick implementation

7. **`FOUNDATION_SYSTEM_SUMMARY.md`** (This file)
   - High-level overview
   - Implementation details
   - Usage examples
   - Feature summary

## Data Schema

### FoundationEntry Structure

```python
@dataclass
class FoundationEntry:
    # Core identification
    id: str                              # Unique identifier
    title: str                           # Display title
    category: str                        # Category from VALID_CATEGORIES

    # Temporal and classification
    year_established: int                # Year (1600-2030)
    badge_type: str                      # "established" or "novel"

    # Mathematical content
    main_equation: str                   # Plain text equation
    main_equation_latex: Optional[str]   # LaTeX representation

    # Descriptive content
    summary: str                         # Brief summary
    key_properties: List[str]            # Key characteristics
    pm_connection: str                   # Link to PM theory

    # Related content
    formulas: List[FormulaEntry]         # Associated formulas
    references: List[str]                # Citations
    tags: List[str]                      # Search tags
```

### FormulaEntry Structure

```python
@dataclass
class FormulaEntry:
    id: str                              # Unique identifier
    label: str                           # Display label
    plain_text: str                      # Plain text representation
    latex: Optional[str]                 # LaTeX representation
    validated: bool                      # Validation status
    description: Optional[str]           # Optional description
```

## Categories

10 foundation categories are supported:

- **geometry** - Geometric foundations (Riemannian geometry, differential geometry)
- **algebra** - Algebraic structures (Lie algebras, group theory)
- **thermodynamics** - Thermodynamic principles
- **gravity** - Gravitational theories (GR, modified gravity)
- **quantum** - Quantum mechanics and QFT
- **topology** - Topological concepts (TCS, homology)
- **grand-unification** - GUT theories
- **gauge-theory** - Gauge field theories
- **symmetry** - Symmetry principles
- **information-theory** - Information theoretic foundations

## Command-Line Interface

### Available Commands

```bash
# List operations
python simulations/foundation_manager.py list
python simulations/foundation_manager.py list --category quantum

# Details and validation
python simulations/foundation_manager.py show <foundation-id>
python simulations/foundation_manager.py validate

# Reports and statistics
python simulations/foundation_manager.py report

# Export operations
python simulations/foundation_manager.py export-html --output-dir output/foundations
python simulations/foundation_manager.py export-json --output-file foundations.json

# Example data
python simulations/foundation_manager.py add-example
```

### Current Statistics

After running the example script:

```
Total Foundations: 4

By Category:
  gauge-theory: 1 (Yang-Mills)
  geometry: 1 (Riemannian)
  quantum: 1 (QFT)
  topology: 1 (TCS)

By Badge Type:
  established: 3
  novel: 1

By Time Period:
  Pre-1900: 1
  1900-1950: 1
  1950-2000: 1
  Post-2000: 1

Total Formulas: 9
Average Formulas per Foundation: 2.2
```

## Features

### 1. Comprehensive Validation

- Required field checking
- Type validation
- Format validation (IDs, years, categories)
- Nested formula validation
- Detailed error reporting

Example:
```python
is_valid, errors = foundation.validate()
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

### 2. Template Generation

**HTML Template**:
- Semantic structure with proper classes
- LaTeX data attributes for rendering
- Organized sections (header, equation, summary, properties, PM connection, formulas)
- Badge system for visual distinction

**JSON Template**:
- Clean, structured format
- Full data preservation
- Easy import/export

### 3. Integration with theory_output.json

- Loads from existing `foundations` array
- Merges with existing data
- Preserves other top-level keys
- Error handling for missing/malformed data

### 4. Helper Functions

```python
# Filtering
get_foundations_by_category(foundations, "quantum")

# Retrieval
get_foundation_by_id(foundations, "yang-mills-theory")

# Validation reporting
report = validate_all_foundations(foundations)
# Returns: {'total': 4, 'valid': 4, 'invalid': 0, 'errors': []}
```

### 5. HTML Extraction (Beta)

Basic HTML parsing to extract foundation data from HTML sections:

```python
foundation = extract_foundation_from_html(html_content, "foundation-id")
```

## Example Foundations Included

### 1. Yang-Mills Gauge Theory (Example)
- Category: gauge-theory
- Year: 1954
- Badge: established
- Formulas: 2 (gauge covariant derivative, field strength tensor)
- Tags: gauge-theory, standard-model, non-abelian, qcd

### 2. Riemannian Geometry
- Category: geometry
- Year: 1854
- Badge: established
- Formulas: 3 (metric tensor, Christoffel symbols, Riemann tensor)
- Tags: geometry, manifolds, curvature, general-relativity

### 3. Quantum Field Theory
- Category: quantum
- Year: 1948
- Badge: established
- Formulas: 2 (QFT Lagrangian, fermion propagator)
- Tags: quantum, field-theory, standard-model, particle-physics

### 4. Topological Cycle Separation (TCS)
- Category: topology
- Year: 2024
- Badge: **novel** (PM contribution)
- Formulas: 2 (TCS cycle condition, consciousness coupling)
- Tags: topology, pm-novel, tcs, fermion-generations, dark-energy, consciousness

## Usage Workflow

### 1. Create a Foundation

```python
from foundation_schema import FoundationEntry, FormulaEntry, CATEGORY_QUANTUM

# Create formulas
formula = FormulaEntry(
    id="schrodinger-eq",
    label="Schrödinger Equation",
    plain_text="iℏ ∂ψ/∂t = Ĥψ",
    latex=r"i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi",
    validated=True
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
    summary="Fundamental framework for quantum phenomena",
    key_properties=["Wave-particle duality", "Uncertainty principle"],
    pm_connection="The Pneuma field exhibits quantum behavior...",
    formulas=[formula],
    tags=["quantum", "wave-function"]
)
```

### 2. Validate

```python
is_valid, errors = foundation.validate()
if is_valid:
    print("Valid!")
else:
    print("Errors:", errors)
```

### 3. Save to theory_output.json

```python
from foundation_schema import (
    load_foundations_from_theory_output,
    save_foundations_to_theory_output
)

foundations = load_foundations_from_theory_output('theory_output.json')
foundations.append(foundation)
save_foundations_to_theory_output(foundations, 'theory_output.json')
```

### 4. Generate Templates

```python
from foundation_schema import generate_html_template, generate_json_template

html = generate_html_template(foundation)
json_str = generate_json_template(foundation)
```

## Testing

All tests passing:

```bash
python test_foundation_schema.py
```

Test coverage:
- Formula creation and validation
- Foundation creation and validation
- Invalid entry rejection
- Example foundation validation
- Template generation (HTML and JSON)
- Validation reporting
- Dictionary conversion

## Generated Output Files

Running the example script creates:

1. **theory_output.json** - Updated with foundations array
2. **output/tcs-topology-foundation.html** - Example HTML template
3. **output/tcs-topology-foundation.json** - Example JSON template

## Integration Points

### With theory_output.json

The system integrates seamlessly with the existing theory_output.json structure:

```json
{
  "version": "14.1",
  "config_source": "config.py",
  "simulations": {
    ...existing simulation data...
  },
  "foundations": [
    {
      "id": "yang-mills-theory",
      "title": "Yang-Mills Gauge Theory",
      ...
    }
  ]
}
```

### With HTML Documentation

Generated HTML templates use semantic classes for easy styling:

```css
.foundation-entry { }
.foundation-header { }
.badge-established { }
.badge-novel { }
.main-equation { }
.key-properties { }
.pm-connection { }
.formula-list { }
```

## Best Practices

1. **Always validate before saving**
   - Use `foundation.validate()` to catch errors early

2. **Provide LaTeX for mathematical content**
   - Enables proper rendering in documentation
   - Stored in `data-latex` attributes

3. **Write clear PM connections**
   - Explain specific relationships to PM theory
   - Be concrete and detailed

4. **Use descriptive IDs**
   - Use hyphens: `yang-mills-theory`
   - Avoid spaces and special characters

5. **Include comprehensive references**
   - Original papers
   - Standard textbooks
   - Review articles

6. **Tag appropriately**
   - Use multiple tags for searchability
   - Include both general and specific tags

## Future Enhancements

Potential improvements identified in documentation:

1. Enhanced HTML extraction for various formats
2. Mathematical syntax validation for formulas
3. Cross-reference system between foundations
4. Full-text search functionality
5. Version control for foundation changes
6. Additional export formats (PDF, Markdown, Wiki)
7. Import from standard formats (BibTeX, arXiv)

## Quick Reference

### Most Common Operations

```python
# Create
foundation = FoundationEntry(...)

# Validate
is_valid, errors = foundation.validate()

# Load
foundations = load_foundations_from_theory_output('theory_output.json')

# Filter
quantum_foundations = get_foundations_by_category(foundations, "quantum")

# Retrieve
foundation = get_foundation_by_id(foundations, "yang-mills-theory")

# Save
save_foundations_to_theory_output(foundations, 'theory_output.json')

# Generate templates
html = generate_html_template(foundation)
json_str = generate_json_template(foundation)
```

### Most Common CLI Commands

```bash
# List and explore
python simulations/foundation_manager.py list
python simulations/foundation_manager.py show <id>

# Validate and report
python simulations/foundation_manager.py validate
python simulations/foundation_manager.py report

# Export
python simulations/foundation_manager.py export-html
python simulations/foundation_manager.py export-json
```

## Summary

The Foundation Configuration Schema System provides:

- **Structured data management** for theoretical foundations
- **Comprehensive validation** ensuring data integrity
- **Template generation** for HTML and JSON output
- **Command-line tools** for easy management
- **Integration** with existing theory_output.json
- **Complete documentation** for all use cases
- **Working examples** demonstrating best practices

The system is production-ready and has been tested with 4 example foundations covering established theories (Yang-Mills, Riemannian Geometry, QFT) and novel PM contributions (TCS Topology).

---

**Implementation Date**: 2025-12-26
**Total Lines of Code**: ~2,200
**Test Status**: All tests passing
**Documentation**: Complete
