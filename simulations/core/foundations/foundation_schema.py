"""
Foundation Configuration Schema and Template System

This module provides a structured schema for managing theoretical foundations
in the Principia Metaphysica framework. It includes:
- Data classes for foundation entries and formulas
- Validation functions for required fields
- Helper functions to convert HTML content to structured data
- Category constants for organizing foundations
- Template generation and extraction utilities
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Tuple
import json
import re
from pathlib import Path

# ============================================================================
# Foundation Categories
# ============================================================================

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

VALID_CATEGORIES = {
    CATEGORY_GEOMETRY,
    CATEGORY_ALGEBRA,
    CATEGORY_THERMODYNAMICS,
    CATEGORY_GRAVITY,
    CATEGORY_QUANTUM,
    CATEGORY_TOPOLOGY,
    CATEGORY_GUT,
    CATEGORY_GAUGE,
    CATEGORY_SYMMETRY,
    CATEGORY_INFORMATION,
}

# Badge types for visual distinction
BADGE_ESTABLISHED = "established"
BADGE_NOVEL = "novel"

VALID_BADGE_TYPES = {BADGE_ESTABLISHED, BADGE_NOVEL}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class FormulaEntry:
    """Represents a single formula within a foundation entry."""

    id: str
    label: str
    plain_text: str
    latex: Optional[str] = None
    validated: bool = False
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the formula entry.

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        if not self.id or not self.id.strip():
            errors.append("Formula ID cannot be empty")

        if not self.label or not self.label.strip():
            errors.append("Formula label cannot be empty")

        if not self.plain_text or not self.plain_text.strip():
            errors.append("Formula plain_text cannot be empty")

        # Check for valid ID format (alphanumeric, hyphens, underscores)
        if self.id and not re.match(r'^[a-zA-Z0-9_-]+$', self.id):
            errors.append(f"Formula ID '{self.id}' contains invalid characters")

        return (len(errors) == 0, errors)

    def __str__(self) -> str:
        return f"Formula({self.id}: {self.label})"


@dataclass
class FoundationEntry:
    """Represents a theoretical foundation in the PM framework."""

    id: str
    title: str
    category: str
    year_established: int
    badge_type: str  # "established" or "novel"
    main_equation: str
    main_equation_latex: Optional[str]
    summary: str
    key_properties: List[str]
    pm_connection: str
    formulas: List[FormulaEntry] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        data = asdict(self)
        # Convert formula objects to dicts
        data['formulas'] = [f.to_dict() for f in self.formulas]
        return data

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the foundation entry.

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Required field validation
        if not self.id or not self.id.strip():
            errors.append("Foundation ID cannot be empty")

        if not self.title or not self.title.strip():
            errors.append("Foundation title cannot be empty")

        if not self.category:
            errors.append("Category cannot be empty")
        elif self.category not in VALID_CATEGORIES:
            errors.append(f"Invalid category '{self.category}'. Must be one of: {', '.join(VALID_CATEGORIES)}")

        if not self.badge_type:
            errors.append("Badge type cannot be empty")
        elif self.badge_type not in VALID_BADGE_TYPES:
            errors.append(f"Invalid badge type '{self.badge_type}'. Must be one of: {', '.join(VALID_BADGE_TYPES)}")

        if self.year_established < 1600 or self.year_established > 2030:
            errors.append(f"Year established ({self.year_established}) seems unrealistic")

        if not self.main_equation or not self.main_equation.strip():
            errors.append("Main equation cannot be empty")

        if not self.summary or not self.summary.strip():
            errors.append("Summary cannot be empty")

        if not self.pm_connection or not self.pm_connection.strip():
            errors.append("PM connection cannot be empty")

        if not self.key_properties:
            errors.append("Key properties list cannot be empty")

        # Check for valid ID format
        if self.id and not re.match(r'^[a-zA-Z0-9_-]+$', self.id):
            errors.append(f"Foundation ID '{self.id}' contains invalid characters")

        # Validate formulas
        for i, formula in enumerate(self.formulas):
            is_valid, formula_errors = formula.validate()
            if not is_valid:
                errors.append(f"Formula {i} validation failed: {'; '.join(formula_errors)}")

        return (len(errors) == 0, errors)

    def add_formula(self, formula: FormulaEntry) -> None:
        """Add a formula to this foundation entry."""
        self.formulas.append(formula)

    def get_formula_by_id(self, formula_id: str) -> Optional[FormulaEntry]:
        """Retrieve a formula by its ID."""
        for formula in self.formulas:
            if formula.id == formula_id:
                return formula
        return None

    def __str__(self) -> str:
        return f"FoundationEntry({self.id}: {self.title} [{self.category}])"


# ============================================================================
# HTML Extraction Utilities
# ============================================================================

def extract_text_from_html(html_content: str) -> str:
    """
    Extract plain text from HTML content.

    Args:
        html_content: HTML string

    Returns:
        Plain text with HTML tags removed
    """
    # Remove script and style elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#8217;', "'")

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


def extract_latex_from_html(html_content: str) -> Optional[str]:
    """
    Extract LaTeX from HTML content (looks for data-latex or similar attributes).

    Args:
        html_content: HTML string

    Returns:
        LaTeX string if found, None otherwise
    """
    # Look for data-latex attribute
    match = re.search(r'data-latex=["\']([^"\']+)["\']', html_content)
    if match:
        return match.group(1)

    # Look for LaTeX within delimiters
    match = re.search(r'\$\$([^$]+)\$\$', html_content)
    if match:
        return match.group(1).strip()

    match = re.search(r'\\\[([^\]]+)\\\]', html_content)
    if match:
        return match.group(1).strip()

    return None


def extract_foundation_from_html(html_content: str, foundation_id: str) -> Optional[FoundationEntry]:
    """
    Extract a foundation entry from HTML content.

    This is a basic parser that looks for common patterns in foundation HTML sections.

    Args:
        html_content: HTML string containing foundation data
        foundation_id: ID to assign to the foundation

    Returns:
        FoundationEntry if extraction successful, None otherwise
    """
    # This is a template function - actual implementation would depend on
    # the specific HTML structure of foundation sections

    # Extract title
    title_match = re.search(r'<h[23]>(.*?)</h[23]>', html_content, re.IGNORECASE)
    if not title_match:
        return None
    title = extract_text_from_html(title_match.group(1))

    # Extract category from class or data attribute
    category_match = re.search(r'data-category=["\']([^"\']+)["\']', html_content)
    category = category_match.group(1) if category_match else CATEGORY_QUANTUM

    # Extract year
    year_match = re.search(r'(\d{4})', html_content)
    year = int(year_match.group(1)) if year_match else 1900

    # Extract badge type
    badge_match = re.search(r'badge-(\w+)', html_content)
    badge_type = badge_match.group(1) if badge_match else BADGE_ESTABLISHED

    # Extract main equation
    equation_match = re.search(r'<div[^>]*class=["\'][^"\']*equation[^"\']*["\'][^>]*>(.*?)</div>',
                               html_content, re.DOTALL | re.IGNORECASE)
    main_equation = extract_text_from_html(equation_match.group(1)) if equation_match else ""
    main_equation_latex = extract_latex_from_html(equation_match.group(1)) if equation_match else None

    # Extract summary
    summary_match = re.search(r'<p[^>]*class=["\'][^"\']*summary[^"\']*["\'][^>]*>(.*?)</p>',
                              html_content, re.DOTALL | re.IGNORECASE)
    summary = extract_text_from_html(summary_match.group(1)) if summary_match else ""

    # Extract key properties (look for list items)
    properties = []
    property_matches = re.finditer(r'<li[^>]*>(.*?)</li>', html_content, re.DOTALL | re.IGNORECASE)
    for match in property_matches:
        prop_text = extract_text_from_html(match.group(1))
        if prop_text:
            properties.append(prop_text)

    # Extract PM connection
    pm_match = re.search(r'<div[^>]*class=["\'][^"\']*pm-connection[^"\']*["\'][^>]*>(.*?)</div>',
                         html_content, re.DOTALL | re.IGNORECASE)
    pm_connection = extract_text_from_html(pm_match.group(1)) if pm_match else ""

    return FoundationEntry(
        id=foundation_id,
        title=title,
        category=category,
        year_established=year,
        badge_type=badge_type,
        main_equation=main_equation,
        main_equation_latex=main_equation_latex,
        summary=summary,
        key_properties=properties if properties else ["No properties extracted"],
        pm_connection=pm_connection if pm_connection else "Connection to be documented"
    )


# ============================================================================
# Template Generation
# ============================================================================

def generate_html_template(foundation: FoundationEntry) -> str:
    """
    Generate an HTML template for a foundation entry.

    Args:
        foundation: FoundationEntry to convert to HTML

    Returns:
        HTML string
    """
    formulas_html = ""
    if foundation.formulas:
        formulas_html = "<h4>Related Formulas</h4>\n<ul class='formula-list'>\n"
        for formula in foundation.formulas:
            latex_attr = f' data-latex="{formula.latex}"' if formula.latex else ''
            formulas_html += f'  <li id="{formula.id}"{latex_attr}>\n'
            formulas_html += f'    <strong>{formula.label}:</strong> {formula.plain_text}\n'
            if formula.description:
                formulas_html += f'    <br><em>{formula.description}</em>\n'
            formulas_html += '  </li>\n'
        formulas_html += "</ul>\n"

    properties_html = "\n".join(f"  <li>{prop}</li>" for prop in foundation.key_properties)

    latex_attr = f' data-latex="{foundation.main_equation_latex}"' if foundation.main_equation_latex else ''

    template = f"""<section class="foundation-entry" id="{foundation.id}" data-category="{foundation.category}">
  <div class="foundation-header">
    <h3>{foundation.title}</h3>
    <span class="badge badge-{foundation.badge_type}">{foundation.badge_type.upper()}</span>
    <span class="year-badge">{foundation.year_established}</span>
  </div>

  <div class="main-equation"{latex_attr}>
    {foundation.main_equation}
  </div>

  <div class="foundation-summary">
    <p>{foundation.summary}</p>
  </div>

  <div class="key-properties">
    <h4>Key Properties</h4>
    <ul>
{properties_html}
    </ul>
  </div>

  <div class="pm-connection">
    <h4>Connection to Principia Metaphysica</h4>
    <p>{foundation.pm_connection}</p>
  </div>

  {formulas_html}
</section>
"""
    return template


def generate_json_template(foundation: FoundationEntry) -> str:
    """
    Generate a JSON template for a foundation entry.

    Args:
        foundation: FoundationEntry to convert to JSON

    Returns:
        JSON string (formatted)
    """
    return json.dumps(foundation.to_dict(), indent=2, ensure_ascii=False)


# ============================================================================
# Theory Output Integration
# ============================================================================

def load_foundations_from_theory_output(filepath: str) -> List[FoundationEntry]:
    """
    Load foundation entries from theory_output.json.

    Args:
        filepath: Path to theory_output.json

    Returns:
        List of FoundationEntry objects
    """
    foundations = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Ensure data is a dictionary
        if not isinstance(data, dict):
            print(f"Warning: {filepath} does not contain a JSON object")
            return foundations

        # Look for foundations in various possible locations
        foundation_data = data.get('foundations', [])

        if not isinstance(foundation_data, list):
            print(f"Warning: 'foundations' is not a list in {filepath}")
            return foundations

        for item in foundation_data:
            if not isinstance(item, dict):
                print(f"Warning: Skipping non-dict item in foundations")
                continue

            # Convert formula dicts back to FormulaEntry objects
            formulas = []
            for f_data in item.get('formulas', []):
                formulas.append(FormulaEntry(**f_data))

            item['formulas'] = formulas
            foundation = FoundationEntry(**item)
            foundations.append(foundation)

    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except (TypeError, KeyError) as e:
        print(f"Error loading foundation data: {e}")
    except Exception as e:
        print(f"Error loading foundations: {e}")

    return foundations


def save_foundations_to_theory_output(foundations: List[FoundationEntry],
                                     filepath: str,
                                     merge: bool = True) -> bool:
    """
    Save foundation entries to theory_output.json.

    Args:
        foundations: List of FoundationEntry objects
        filepath: Path to theory_output.json
        merge: If True, merge with existing data; if False, overwrite

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing data if merging
        existing_data = {}
        if merge and Path(filepath).exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

        # Convert foundations to dicts
        foundation_dicts = [f.to_dict() for f in foundations]

        # Update or set foundations
        existing_data['foundations'] = foundation_dicts

        # Save back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error saving foundations: {e}")
        return False


def get_foundations_by_category(foundations: List[FoundationEntry],
                                category: str) -> List[FoundationEntry]:
    """
    Filter foundations by category.

    Args:
        foundations: List of FoundationEntry objects
        category: Category to filter by

    Returns:
        List of matching FoundationEntry objects
    """
    return [f for f in foundations if f.category == category]


def get_foundation_by_id(foundations: List[FoundationEntry],
                        foundation_id: str) -> Optional[FoundationEntry]:
    """
    Retrieve a foundation by its ID.

    Args:
        foundations: List of FoundationEntry objects
        foundation_id: ID to search for

    Returns:
        FoundationEntry if found, None otherwise
    """
    for foundation in foundations:
        if foundation.id == foundation_id:
            return foundation
    return None


def validate_all_foundations(foundations: List[FoundationEntry]) -> Dict[str, Any]:
    """
    Validate all foundations and return a report.

    Args:
        foundations: List of FoundationEntry objects

    Returns:
        Dictionary with validation results
    """
    results = {
        'total': len(foundations),
        'valid': 0,
        'invalid': 0,
        'errors': []
    }

    for foundation in foundations:
        is_valid, errors = foundation.validate()
        if is_valid:
            results['valid'] += 1
        else:
            results['invalid'] += 1
            results['errors'].append({
                'id': foundation.id,
                'title': foundation.title,
                'errors': errors
            })

    return results


# ============================================================================
# Example Usage
# ============================================================================

def create_example_foundation() -> FoundationEntry:
    """Create an example foundation entry for demonstration."""

    # Create example formulas
    formula1 = FormulaEntry(
        id="gauge-covariant-derivative",
        label="Gauge Covariant Derivative",
        plain_text="D_μ = ∂_μ - ig A_μ^a T^a",
        latex=r"D_\mu = \partial_\mu - ig A_\mu^a T^a",
        validated=True,
        description="Covariant derivative in gauge theory"
    )

    formula2 = FormulaEntry(
        id="field-strength-tensor",
        label="Field Strength Tensor",
        plain_text="F_μν = ∂_μ A_ν - ∂_ν A_μ + ig[A_μ, A_ν]",
        latex=r"F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + ig[A_\mu, A_\nu]",
        validated=True,
        description="Non-abelian field strength tensor"
    )

    # Create foundation entry
    foundation = FoundationEntry(
        id="yang-mills-theory",
        title="Yang-Mills Gauge Theory",
        category=CATEGORY_GAUGE,
        year_established=1954,
        badge_type=BADGE_ESTABLISHED,
        main_equation="L_YM = -¼ F_μν^a F^{μν,a}",
        main_equation_latex=r"\mathcal{L}_{YM} = -\frac{1}{4} F_{\mu\nu}^a F^{\mu\nu,a}",
        summary="Yang-Mills theory generalizes Maxwell's electromagnetism to non-abelian gauge groups, forming the foundation for the Standard Model gauge interactions.",
        key_properties=[
            "Non-abelian gauge symmetry under SU(N) transformations",
            "Self-interacting gauge bosons due to group structure",
            "Asymptotic freedom at high energies",
            "Confinement at low energies (for QCD)"
        ],
        pm_connection="The Pneuma Lagrangian incorporates Yang-Mills gauge structure through its SU(3)×SU(2)×U(1) symmetry, while extending it with topological and consciousness coupling terms.",
        formulas=[formula1, formula2],
        references=[
            "Yang, C. N., & Mills, R. L. (1954). Conservation of Isotopic Spin and Isotopic Gauge Invariance. Physical Review, 96(1), 191.",
            "Gross, D. J., & Wilczek, F. (1973). Ultraviolet Behavior of Non-Abelian Gauge Theories. Physical Review Letters, 30(26), 1343."
        ],
        tags=["gauge-theory", "standard-model", "non-abelian", "qcd"]
    )

    return foundation


if __name__ == "__main__":
    # Demonstration of the schema system
    print("Foundation Schema and Template System")
    print("=" * 60)

    # Create example foundation
    example = create_example_foundation()

    # Validate
    is_valid, errors = example.validate()
    print(f"\nValidation: {'PASSED' if is_valid else 'FAILED'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

    # Display
    print(f"\n{example}")
    print(f"Category: {example.category}")
    print(f"Formulas: {len(example.formulas)}")

    # Generate templates
    print("\n" + "=" * 60)
    print("HTML Template:")
    print("=" * 60)
    print(generate_html_template(example))

    print("\n" + "=" * 60)
    print("JSON Template:")
    print("=" * 60)
    print(generate_json_template(example))

    # Demonstrate category filtering
    foundations = [example]
    gauge_foundations = get_foundations_by_category(foundations, CATEGORY_GAUGE)
    print(f"\nFoundations in GAUGE category: {len(gauge_foundations)}")
