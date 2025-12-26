"""
Test script for the foundation schema system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simulations'))

from foundation_schema import (
    FoundationEntry,
    FormulaEntry,
    create_example_foundation,
    validate_all_foundations,
    generate_html_template,
    generate_json_template,
    CATEGORY_GEOMETRY,
    CATEGORY_GAUGE,
    CATEGORY_QUANTUM,
)


def test_formula_creation():
    """Test creating and validating a formula."""
    print("Testing FormulaEntry creation...")

    formula = FormulaEntry(
        id="test-formula",
        label="Test Formula",
        plain_text="E = mc^2",
        latex=r"E = mc^2",
        validated=True
    )

    is_valid, errors = formula.validate()
    assert is_valid, f"Formula validation failed: {errors}"
    print("  PASSED: FormulaEntry creation and validation")

    # Test invalid formula
    invalid_formula = FormulaEntry(
        id="",  # Empty ID
        label="Test",
        plain_text="Test"
    )
    is_valid, errors = invalid_formula.validate()
    assert not is_valid, "Expected validation to fail for empty ID"
    print(f"  PASSED: Invalid formula correctly rejected: {errors[0]}")


def test_foundation_creation():
    """Test creating and validating a foundation."""
    print("\nTesting FoundationEntry creation...")

    foundation = FoundationEntry(
        id="test-foundation",
        title="Test Foundation",
        category=CATEGORY_GEOMETRY,
        year_established=1915,
        badge_type="established",
        main_equation="G_μν = 8πG T_μν",
        main_equation_latex=r"G_{\mu\nu} = 8\pi G T_{\mu\nu}",
        summary="Test summary",
        key_properties=["Property 1", "Property 2"],
        pm_connection="Test connection"
    )

    is_valid, errors = foundation.validate()
    assert is_valid, f"Foundation validation failed: {errors}"
    print("  PASSED: FoundationEntry creation and validation")

    # Test with formulas
    formula = FormulaEntry(
        id="ricci-tensor",
        label="Ricci Tensor",
        plain_text="R_μν = R^ρ_μρν",
        validated=True
    )
    foundation.add_formula(formula)
    assert len(foundation.formulas) == 1
    print(f"  PASSED: Added formula to foundation (total: {len(foundation.formulas)})")

    # Retrieve formula
    retrieved = foundation.get_formula_by_id("ricci-tensor")
    assert retrieved is not None
    assert retrieved.id == "ricci-tensor"
    print("  PASSED: Retrieved formula by ID")


def test_invalid_foundation():
    """Test that invalid foundations are properly rejected."""
    print("\nTesting invalid foundation rejection...")

    # Missing required fields
    invalid_foundation = FoundationEntry(
        id="",  # Empty ID
        title="Test",
        category="invalid-category",  # Invalid category
        year_established=999,  # Unrealistic year
        badge_type="invalid-badge",  # Invalid badge type
        main_equation="",  # Empty equation
        main_equation_latex=None,
        summary="",  # Empty summary
        key_properties=[],  # Empty list
        pm_connection=""  # Empty connection
    )

    is_valid, errors = invalid_foundation.validate()
    assert not is_valid, "Expected validation to fail"
    print(f"  PASSED: Invalid foundation rejected with {len(errors)} errors")
    for i, error in enumerate(errors[:3], 1):
        print(f"    {i}. {error}")


def test_example_foundation():
    """Test the example foundation."""
    print("\nTesting example foundation...")

    foundation = create_example_foundation()

    is_valid, errors = foundation.validate()
    assert is_valid, f"Example foundation validation failed: {errors}"
    print("  PASSED: Example foundation is valid")
    print(f"    ID: {foundation.id}")
    print(f"    Title: {foundation.title}")
    print(f"    Category: {foundation.category}")
    print(f"    Year: {foundation.year_established}")
    print(f"    Formulas: {len(foundation.formulas)}")
    print(f"    References: {len(foundation.references)}")
    print(f"    Tags: {', '.join(foundation.tags)}")


def test_template_generation():
    """Test template generation."""
    print("\nTesting template generation...")

    foundation = create_example_foundation()

    # Test HTML template
    html = generate_html_template(foundation)
    assert len(html) > 0
    assert foundation.id in html
    assert foundation.title in html
    print(f"  PASSED: HTML template generated ({len(html)} chars)")

    # Test JSON template
    json_str = generate_json_template(foundation)
    assert len(json_str) > 0
    assert foundation.id in json_str
    print(f"  PASSED: JSON template generated ({len(json_str)} chars)")


def test_validation_report():
    """Test the validation report function."""
    print("\nTesting validation report...")

    # Create mix of valid and invalid foundations
    valid1 = create_example_foundation()
    valid1.id = "valid-1"

    valid2 = create_example_foundation()
    valid2.id = "valid-2"
    valid2.title = "Another Valid Foundation"

    invalid = FoundationEntry(
        id="",
        title="Invalid",
        category="bad-category",
        year_established=1800,
        badge_type="established",
        main_equation="test",
        main_equation_latex=None,
        summary="test",
        key_properties=["test"],
        pm_connection="test"
    )

    foundations = [valid1, valid2, invalid]
    report = validate_all_foundations(foundations)

    assert report['total'] == 3
    assert report['valid'] == 2
    assert report['invalid'] == 1
    print(f"  PASSED: Validation report correct")
    print(f"    Total: {report['total']}")
    print(f"    Valid: {report['valid']}")
    print(f"    Invalid: {report['invalid']}")


def test_to_dict_conversion():
    """Test dictionary conversion."""
    print("\nTesting dictionary conversion...")

    foundation = create_example_foundation()
    data = foundation.to_dict()

    assert isinstance(data, dict)
    assert data['id'] == foundation.id
    assert data['title'] == foundation.title
    assert data['category'] == foundation.category
    assert len(data['formulas']) == len(foundation.formulas)
    print("  PASSED: to_dict() conversion")
    print(f"    Keys: {', '.join(list(data.keys())[:5])}...")


def main():
    """Run all tests."""
    print("=" * 70)
    print("Foundation Schema Test Suite")
    print("=" * 70)

    try:
        test_formula_creation()
        test_foundation_creation()
        test_invalid_foundation()
        test_example_foundation()
        test_template_generation()
        test_validation_report()
        test_to_dict_conversion()

        print("\n" + "=" * 70)
        print("All tests PASSED!")
        print("=" * 70)

    except AssertionError as e:
        print(f"\n\nTEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
