#!/usr/bin/env python3
"""
Test Suite for G2 Geometry v16.0
=================================

Comprehensive tests for g2_geometry_v16_0 simulation.

Run with: python simulations/v16/geometric/test_g2_geometry_v16.py
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from simulations.v16.geometric import G2GeometryV16
from simulations.base import PMRegistry


def test_metadata():
    """Test simulation metadata."""
    print("\n" + "="*70)
    print("TEST: Metadata")
    print("="*70)

    sim = G2GeometryV16()
    metadata = sim.metadata

    assert metadata.id == "g2_geometry_v16_0", f"Expected id='g2_geometry_v16_0', got '{metadata.id}'"
    assert metadata.version == "16.0", f"Expected version='16.0', got '{metadata.version}'"
    assert metadata.domain == "geometric", f"Expected domain='geometric', got '{metadata.domain}'"
    assert metadata.section_id == "2", f"Expected section_id='2', got '{metadata.section_id}'"

    print("✓ id:", metadata.id)
    print("✓ version:", metadata.version)
    print("✓ domain:", metadata.domain)
    print("✓ title:", metadata.title)
    print("✓ section_id:", metadata.section_id)
    print("\n[PASS] Metadata test")


def test_no_dependencies():
    """Test that this is a root simulation with no dependencies."""
    print("\n" + "="*70)
    print("TEST: Root Simulation (No Dependencies)")
    print("="*70)

    sim = G2GeometryV16()
    inputs = sim.required_inputs

    assert len(inputs) == 0, f"Root simulation should have 0 inputs, got {len(inputs)}: {inputs}"

    print("✓ required_inputs:", inputs)
    print("\n[PASS] No dependencies test")


def test_outputs():
    """Test output parameter and formula lists."""
    print("\n" + "="*70)
    print("TEST: Outputs")
    print("="*70)

    sim = G2GeometryV16()
    params = sim.output_params
    formulas = sim.output_formulas

    expected_params = [
        "topology.b2",
        "topology.b3",
        "topology.CHI_EFF",
        "topology.n_gen",
        "topology.K_MATCHING",
        "topology.d_over_R"
    ]

    expected_formulas = [
        "g2-holonomy",
        "euler-characteristic",
        "betti-numbers",
        "three-generations",
        "cycle-matching"
    ]

    assert params == expected_params, f"Parameter list mismatch"
    assert formulas == expected_formulas, f"Formula list mismatch"

    print("✓ output_params:", len(params))
    for p in params:
        print(f"  - {p}")

    print("✓ output_formulas:", len(formulas))
    for f in formulas:
        print(f"  - {f}")

    print("\n[PASS] Outputs test")


def test_computation():
    """Test the run() method computes correct values."""
    print("\n" + "="*70)
    print("TEST: Computation")
    print("="*70)

    PMRegistry.reset_instance()
    registry = PMRegistry.get_instance()
    sim = G2GeometryV16()

    results = sim.run(registry)

    # Check all expected outputs present
    assert "topology.b2" in results
    assert "topology.b3" in results
    assert "topology.CHI_EFF" in results
    assert "topology.n_gen" in results
    assert "topology.K_MATCHING" in results
    assert "topology.d_over_R" in results

    # Check values
    assert results["topology.b2"] == 4, f"Expected b2=4, got {results['topology.b2']}"
    assert results["topology.b3"] == 24, f"Expected b3=24, got {results['topology.b3']}"
    assert results["topology.CHI_EFF"] == 144, f"Expected CHI_EFF=144, got {results['topology.CHI_EFF']}"
    assert results["topology.n_gen"] == 3, f"Expected n_gen=3, got {results['topology.n_gen']}"
    assert results["topology.K_MATCHING"] == 4, f"Expected K_MATCHING=4, got {results['topology.K_MATCHING']}"
    assert results["topology.d_over_R"] == 0.12, f"Expected d_over_R=0.12, got {results['topology.d_over_R']}"

    # Check holonomy validation
    assert results["_holonomy_valid"] == True, "G2 holonomy validation should pass"

    print("✓ b2 =", results["topology.b2"])
    print("✓ b3 =", results["topology.b3"])
    print("✓ CHI_EFF =", results["topology.CHI_EFF"])
    print("✓ n_gen =", results["topology.n_gen"])
    print("✓ K_MATCHING =", results["topology.K_MATCHING"])
    print("✓ d_over_R =", results["topology.d_over_R"])
    print("✓ G2 holonomy valid:", results["_holonomy_valid"])

    print("\n[PASS] Computation test")


def test_registry_integration():
    """Test integration with PMRegistry."""
    print("\n" + "="*70)
    print("TEST: PMRegistry Integration")
    print("="*70)

    PMRegistry.reset_instance()
    registry = PMRegistry.get_instance()
    sim = G2GeometryV16()

    # Execute simulation
    results = sim.execute(registry, verbose=False)

    # Check all parameters injected
    for param_path in sim.output_params:
        assert registry.has_param(param_path), f"Parameter {param_path} not in registry"
        entry = registry.get_entry(param_path)
        assert entry.status == "GEOMETRIC", f"Expected status=GEOMETRIC for {param_path}, got {entry.status}"
        assert entry.source == "g2_geometry_v16_0", f"Expected source=g2_geometry_v16_0, got {entry.source}"

    # Check all formulas injected
    for formula_id in sim.output_formulas:
        assert registry.has_formula(formula_id), f"Formula {formula_id} not in registry"
        formula = registry.get_formula(formula_id)
        assert formula.category == "THEORY", f"Expected category=THEORY for {formula_id}, got {formula.category}"

    print("✓ All parameters injected with status=GEOMETRIC")
    print("✓ All formulas injected with category=THEORY")
    print("✓ Provenance tracked")

    # Check specific values
    assert registry.get_param("topology.b3") == 24
    assert registry.get_param("topology.CHI_EFF") == 144
    assert registry.get_param("topology.n_gen") == 3

    print("✓ Values correct in registry")

    print("\n[PASS] Registry integration test")


def test_formulas():
    """Test formula definitions."""
    print("\n" + "="*70)
    print("TEST: Formula Definitions")
    print("="*70)

    sim = G2GeometryV16()
    formulas = sim.get_formulas()

    assert len(formulas) == 5, f"Expected 5 formulas, got {len(formulas)}"

    for formula in formulas:
        # Check all required fields present
        assert formula.id, "Formula must have id"
        assert formula.label, "Formula must have label"
        assert formula.latex, "Formula must have latex"
        assert formula.plain_text, "Formula must have plain_text"
        assert formula.category == "THEORY", f"All formulas should be THEORY, got {formula.category}"
        assert formula.description, "Formula must have description"

        # Check derivation exists
        assert formula.derivation is not None, f"Formula {formula.id} missing derivation"
        assert "steps" in formula.derivation, f"Formula {formula.id} missing derivation steps"

        print(f"✓ {formula.id}: {formula.label} ({formula.category})")

    print("\n[PASS] Formula definitions test")


def test_parameters():
    """Test parameter definitions."""
    print("\n" + "="*70)
    print("TEST: Parameter Definitions")
    print("="*70)

    sim = G2GeometryV16()
    params = sim.get_output_param_definitions()

    assert len(params) == 6, f"Expected 6 parameter definitions, got {len(params)}"

    for param in params:
        # Check all required fields
        assert param.path, "Parameter must have path"
        assert param.name, "Parameter must have name"
        assert param.units, "Parameter must have units"
        assert param.status == "GEOMETRIC", f"All params should be GEOMETRIC, got {param.status}"
        assert param.description, "Parameter must have description"

        print(f"✓ {param.path}: {param.name} ({param.status}, {param.units})")

    # Check n_gen has experimental bound
    n_gen_param = next((p for p in params if p.path == "topology.n_gen"), None)
    assert n_gen_param is not None, "n_gen parameter not found"
    assert n_gen_param.experimental_bound == 3.0, "n_gen should have experimental bound of 3.0"
    assert n_gen_param.bound_type == "measured", "n_gen bound should be 'measured'"

    print("✓ topology.n_gen has experimental bound")

    print("\n[PASS] Parameter definitions test")


def test_section_content():
    """Test section content generation."""
    print("\n" + "="*70)
    print("TEST: Section Content Generation")
    print("="*70)

    sim = G2GeometryV16()
    section = sim.get_section_content()

    assert section is not None, "Section content should not be None"
    assert section.section_id == "2", f"Expected section_id='2', got '{section.section_id}'"
    assert section.title, "Section must have title"
    assert section.abstract, "Section must have abstract"
    assert len(section.content_blocks) > 0, "Section must have content blocks"
    assert len(section.formula_refs) > 0, "Section must reference formulas"
    assert len(section.param_refs) > 0, "Section must reference parameters"

    print("✓ Section ID:", section.section_id)
    print("✓ Title:", section.title)
    print("✓ Content blocks:", len(section.content_blocks))
    print("✓ Formula refs:", len(section.formula_refs))
    print("✓ Param refs:", len(section.param_refs))

    # Check content block types
    block_types = [block.type for block in section.content_blocks]
    assert "paragraph" in block_types, "Should have paragraph blocks"
    assert "formula" in block_types, "Should have formula blocks"

    print("✓ Block types:", set(block_types))

    print("\n[PASS] Section content test")


def test_generation_count():
    """Test that n_gen = 3 matches Standard Model."""
    print("\n" + "="*70)
    print("TEST: Three Generations Prediction")
    print("="*70)

    PMRegistry.reset_instance()
    registry = PMRegistry.get_instance()
    sim = G2GeometryV16()

    results = sim.execute(registry, verbose=False)
    n_gen = results["topology.n_gen"]

    assert n_gen == 3, f"Predicted n_gen={n_gen}, but Standard Model has exactly 3 generations"

    print("✓ n_gen = χ_eff / 48")
    print("✓ n_gen = 144 / 48")
    print("✓ n_gen = 3")
    print("✓ Matches Standard Model observation")

    print("\n[PASS] Three generations test")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print(" G2 GEOMETRY v16.0 TEST SUITE")
    print("="*70)

    tests = [
        test_metadata,
        test_no_dependencies,
        test_outputs,
        test_computation,
        test_registry_integration,
        test_formulas,
        test_parameters,
        test_section_content,
        test_generation_count,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"\n[ERROR] {test.__name__}: {e}")
            failed += 1

    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("\n✓ ALL TESTS PASSED")
        print("="*70)
        return 0
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        print("="*70)
        return 1


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    exit_code = run_all_tests()
    sys.exit(exit_code)
