# Foundation Schema - Quick Start Guide

## Installation

No installation required. Files are located in:
- `simulations/foundation_schema.py` - Core schema
- `simulations/foundation_manager.py` - CLI tool
- `simulations/foundation_example.py` - Example usage

## 5-Minute Tutorial

### 1. Run the Example

```bash
python simulations/foundation_example.py
```

This creates 3 example foundations and saves them to `theory_output.json`.

### 2. List Foundations

```bash
python simulations/foundation_manager.py list
```

Output:
```
1. [yang-mills-theory] Yang-Mills Gauge Theory
   Category: gauge-theory | Year: 1954 | Badge: established
   Formulas: 2 | Tags: gauge-theory, standard-model, non-abelian, qcd

2. [riemannian-geometry] Riemannian Geometry
   Category: geometry | Year: 1854 | Badge: established
   Formulas: 3 | Tags: geometry, manifolds, curvature, general-relativity
...
```

### 3. View a Foundation

```bash
python simulations/foundation_manager.py show tcs-topology
```

### 4. Generate Report

```bash
python simulations/foundation_manager.py report
```

Output:
```
Total Foundations: 4

By Category:
  gauge-theory: 1
  geometry: 1
  quantum: 1
  topology: 1

By Badge Type:
  established: 3
  novel: 1
...
```

### 5. Validate Foundations

```bash
python simulations/foundation_manager.py validate
```

### 6. Export

```bash
# Export to HTML
python simulations/foundation_manager.py export-html --output-dir output/foundations

# Export to JSON
python simulations/foundation_manager.py export-json --output-file foundations.json
```

## Create Your Own Foundation

### Minimal Example

```python
from foundation_schema import FoundationEntry, CATEGORY_QUANTUM, BADGE_ESTABLISHED

foundation = FoundationEntry(
    id="my-foundation",
    title="My Foundation",
    category=CATEGORY_QUANTUM,
    year_established=1900,
    badge_type=BADGE_ESTABLISHED,
    main_equation="E = mc²",
    main_equation_latex=r"E = mc^2",
    summary="Brief summary of the foundation",
    key_properties=["Property 1", "Property 2"],
    pm_connection="How this relates to PM..."
)

# Validate
is_valid, errors = foundation.validate()
print(f"Valid: {is_valid}")
```

### With Formulas

```python
from foundation_schema import FormulaEntry

# Create formula
formula = FormulaEntry(
    id="my-formula",
    label="My Formula",
    plain_text="f(x) = x²",
    latex=r"f(x) = x^2",
    validated=True,
    description="Description of formula"
)

# Add to foundation
foundation.formulas = [formula]
```

### Save to theory_output.json

```python
from foundation_schema import (
    load_foundations_from_theory_output,
    save_foundations_to_theory_output
)

# Load existing
foundations = load_foundations_from_theory_output('theory_output.json')

# Add your foundation
foundations.append(foundation)

# Save
save_foundations_to_theory_output(foundations, 'theory_output.json')
```

## Available Categories

```python
CATEGORY_GEOMETRY = "geometry"
CATEGORY_ALGEBRA = "algebra"
CATEGORY_THERMODYNAMICS = "thermodynamics"
CATEGORY_GRAVITY = "gravity"
CATEGORY_QUANTUM = "quantum"
CATEGORY_TOPOLOGY = "topology"
CATEGORY_GUT = "grand-unification"
CATEGORY_GAUGE = "gauge-theory"
CATEGORY_SYMMETRY = "symmetry"
CATEGORY_INFORMATION = "information-theory"
```

## Badge Types

```python
BADGE_ESTABLISHED = "established"  # For established theories
BADGE_NOVEL = "novel"              # For PM novel contributions
```

## Common Commands

```bash
# List all foundations
python simulations/foundation_manager.py list

# List by category
python simulations/foundation_manager.py list --category quantum

# Show details
python simulations/foundation_manager.py show <foundation-id>

# Validate all
python simulations/foundation_manager.py validate

# Generate report
python simulations/foundation_manager.py report

# Export to HTML
python simulations/foundation_manager.py export-html

# Export to JSON
python simulations/foundation_manager.py export-json

# Add example foundation
python simulations/foundation_manager.py add-example
```

## Validation Rules

Required fields:
- `id` - Unique identifier (alphanumeric, hyphens, underscores)
- `title` - Foundation title
- `category` - Valid category
- `year_established` - Between 1600 and 2030
- `badge_type` - "established" or "novel"
- `main_equation` - Main equation (plain text)
- `summary` - Brief summary
- `key_properties` - List with at least 1 item
- `pm_connection` - Connection to PM

Optional fields:
- `main_equation_latex` - LaTeX version
- `formulas` - List of FormulaEntry objects
- `references` - List of references
- `tags` - List of tags

## Tips

1. **Always validate** before saving:
   ```python
   is_valid, errors = foundation.validate()
   if not is_valid:
       print("Errors:", errors)
   ```

2. **Use LaTeX** for mathematical content:
   ```python
   main_equation="∇×E = -∂B/∂t",
   main_equation_latex=r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}"
   ```

3. **Add tags** for searchability:
   ```python
   tags=["quantum", "field-theory", "standard-model"]
   ```

4. **Write clear PM connections** that explain the relationship to Principia Metaphysica

5. **Include references** for established theories:
   ```python
   references=[
       "Author (Year). Title. Journal.",
       "Book Author (Year). Book Title. Publisher."
   ]
   ```

## Files Generated

- `theory_output.json` - Contains all foundations
- `output/foundations/*.html` - HTML templates (from export-html)
- `foundations_export.json` - JSON export (from export-json)
- `output/tcs-topology-foundation.html` - Example HTML
- `output/tcs-topology-foundation.json` - Example JSON

## Next Steps

1. Read the full documentation: `FOUNDATION_SCHEMA_README.md`
2. Run the example: `python simulations/foundation_example.py`
3. Create your own foundations
4. Validate and export

## Troubleshooting

**Problem**: Unicode encoding errors on Windows
**Solution**: This is a Windows console limitation. The data is saved correctly - only display is affected.

**Problem**: Foundation not loading from theory_output.json
**Solution**: Check that theory_output.json has a `foundations` array at the top level.

**Problem**: Validation fails
**Solution**: Read the error messages carefully. Common issues:
- Missing required fields
- Invalid category or badge_type
- Empty lists for key_properties
- ID contains invalid characters

## Support

For detailed documentation, see:
- `FOUNDATION_SCHEMA_README.md` - Full documentation
- `foundation_schema.py` - Source code with docstrings
- `foundation_example.py` - Working examples
- `test_foundation_schema.py` - Test suite

---

**Last Updated**: 2025-12-26
