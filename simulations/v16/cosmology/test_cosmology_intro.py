"""
Test script for Cosmological Framework Introduction v16.0
==========================================================

Validates that the simulation follows the v16 schema exactly.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from cosmology_intro_v16_0 import CosmologyIntroV16, export_cosmology_intro_v16
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics


def test_schema_compliance():
    """Test that simulation follows v16 schema."""
    print("\n" + "="*70)
    print(" TESTING COSMOLOGY INTRO V16.0 SCHEMA COMPLIANCE")
    print("="*70)

    sim = CosmologyIntroV16()

    # Test 1: Metadata
    print("\n[TEST 1] Metadata...")
    metadata = sim.metadata
    assert metadata.id == "cosmology_intro_v16_0"
    assert metadata.version == "16.0"
    assert metadata.domain == "cosmology"
    assert metadata.section_id == "5"
    assert metadata.subsection_id == "5.1"
    print("  ✓ All metadata fields present and correct")

    # Test 2: Required inputs
    print("\n[TEST 2] Required inputs...")
    inputs = sim.required_inputs
    assert len(inputs) == 3
    assert "desi.H0" in inputs
    assert "desi.Omega_m" in inputs
    assert "desi.w0" in inputs
    print(f"  ✓ {len(inputs)} required inputs specified")

    # Test 3: Output params
    print("\n[TEST 3] Output parameters...")
    outputs = sim.output_params
    assert len(outputs) == 6
    print(f"  ✓ {len(outputs)} output parameters specified")

    # Test 4: Output formulas
    print("\n[TEST 4] Output formulas...")
    formulas = sim.output_formulas
    assert len(formulas) == 5
    print(f"  ✓ {len(formulas)} output formulas specified")

    # Test 5: Section content (must not be None/empty)
    print("\n[TEST 5] Section content...")
    section = sim.get_section_content()
    assert section is not None, "get_section_content() returned None!"
    assert len(section.content_blocks) > 0, "Section has no content blocks!"
    assert section.title != "", "Section title is empty!"
    print(f"  ✓ Section has {len(section.content_blocks)} content blocks")

    # Test 6: Formulas (must not be empty)
    print("\n[TEST 6] Formulas...")
    formula_list = sim.get_formulas()
    assert formula_list is not None, "get_formulas() returned None!"
    assert len(formula_list) > 0, "get_formulas() returned empty list!"
    for formula in formula_list:
        assert formula.latex != "", f"Formula {formula.id} has empty LaTeX!"
        assert formula.description != "", f"Formula {formula.id} has empty description!"
    print(f"  ✓ {len(formula_list)} formulas with complete metadata")

    # Test 7: Parameter definitions (must not be empty)
    print("\n[TEST 7] Parameter definitions...")
    param_defs = sim.get_output_param_definitions()
    assert param_defs is not None, "get_output_param_definitions() returned None!"
    assert len(param_defs) > 0, "get_output_param_definitions() returned empty list!"
    for param in param_defs:
        assert param.name != "", f"Parameter {param.path} has empty name!"
        assert param.units != "", f"Parameter {param.path} has empty units!"
        assert param.status != "", f"Parameter {param.path} has empty status!"
    print(f"  ✓ {len(param_defs)} parameter definitions with complete metadata")

    # Test 8: Beginner explanation (must not be None/empty)
    print("\n[TEST 8] Beginner explanation...")
    beginner = sim.get_beginner_explanation()
    assert beginner is not None, "get_beginner_explanation() returned None!"
    assert "icon" in beginner and beginner["icon"] != ""
    assert "title" in beginner and beginner["title"] != ""
    assert "simpleExplanation" in beginner and beginner["simpleExplanation"] != ""
    assert "analogy" in beginner and beginner["analogy"] != ""
    assert "keyTakeaway" in beginner and beginner["keyTakeaway"] != ""
    assert "technicalDetail" in beginner and beginner["technicalDetail"] != ""
    assert "prediction" in beginner and beginner["prediction"] != ""
    print(f"  ✓ Complete beginner explanation with all 7 fields")

    # Test 9: Run method (must return results)
    print("\n[TEST 9] Run method...")
    registry = PMRegistry.get_instance()
    EstablishedPhysics.load_into_registry(registry)
    results = sim.run(registry)
    assert results is not None, "run() returned None!"
    assert len(results) > 0, "run() returned empty results!"
    # Check all output params are in results
    for param_path in sim.output_params:
        assert param_path in results, f"Output param {param_path} not in results!"
    print(f"  ✓ run() returned {len(results)} computed parameters")

    # Test 10: Validate computed values
    print("\n[TEST 10] Validate computed values...")
    assert 60 < results["cosmology.H0_theory"] < 80, "H0 out of range!"
    assert 0.6 < results["cosmology.Omega_Lambda"] < 0.8, "Omega_Lambda out of range!"
    assert 0.99 < results["cosmology.Omega_total"] < 1.01, "Omega_total not flat!"
    assert 4.5 < results["cosmology.D_eff_cosmology"] < 5.0, "D_eff out of range!"
    assert 13.0 < results["cosmology.age_universe_Gyr"] < 15.0, "Age out of range!"
    print(f"  ✓ All computed values within expected ranges")

    print("\n" + "="*70)
    print(" ALL SCHEMA COMPLIANCE TESTS PASSED!")
    print("="*70)
    print("\nThis simulation will NOT fail schema validation.")
    print("All required methods return non-None, non-empty values.")


if __name__ == "__main__":
    test_schema_compliance()

    # Also run the full simulation
    print("\n" + "="*70)
    print(" RUNNING FULL SIMULATION")
    print("="*70)
    results = export_cosmology_intro_v16()

    print("\n" + "="*70)
    print(" SIMULATION COMPLETE")
    print("="*70)
    print(f"  Version: {results['version']}")
    print(f"  Domain: {results['domain']}")
    print(f"  Section: {results['section']}")
    print(f"  Status: {results['status']}")
