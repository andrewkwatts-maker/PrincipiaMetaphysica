#!/usr/bin/env python3
"""
Test script for neutrino mixing v16 simulation.

This script demonstrates the usage of the NeutrinoMixingSimulation class
and validates the SimulationBase interface implementation.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os

# Add parent to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
sys.path.insert(0, _project_root)

from simulations.base import PMRegistry
from simulations.v16.neutrino import NeutrinoMixingSimulation


def test_simulation_metadata():
    """Test that metadata is correctly defined."""
    sim = NeutrinoMixingSimulation()
    metadata = sim.metadata

    print("=" * 75)
    print("METADATA TEST")
    print("=" * 75)
    print(f"ID:          {metadata.id}")
    print(f"Version:     {metadata.version}")
    print(f"Domain:      {metadata.domain}")
    print(f"Title:       {metadata.title}")
    print(f"Section:     {metadata.section_id}.{metadata.subsection_id}")
    print(f"Description: {metadata.description[:60]}...")
    print()

    assert metadata.id == "neutrino_mixing_v16_0"
    assert metadata.version == "16.0"
    assert metadata.domain == "neutrino"
    assert metadata.section_id == "4"
    assert metadata.subsection_id == "4.5"
    print("[PASS] Metadata test passed\n")


def test_required_inputs():
    """Test that required inputs are correctly defined."""
    sim = NeutrinoMixingSimulation()
    inputs = sim.required_inputs

    print("=" * 75)
    print("REQUIRED INPUTS TEST")
    print("=" * 75)
    for inp in inputs:
        print(f"  - {inp}")
    print()

    assert "topology.b2" in inputs
    assert "topology.b3" in inputs
    assert "topology.chi_eff" in inputs
    assert "topology.n_gen" in inputs
    assert "topology.orientation_sum" in inputs
    print("[PASS] Required inputs test passed\n")


def test_output_params():
    """Test that output parameters are correctly defined."""
    sim = NeutrinoMixingSimulation()
    outputs = sim.output_params

    print("=" * 75)
    print("OUTPUT PARAMETERS TEST")
    print("=" * 75)
    for out in outputs:
        print(f"  - {out}")
    print()

    assert "neutrino.theta_12_pred" in outputs
    assert "neutrino.theta_13_pred" in outputs
    assert "neutrino.theta_23_pred" in outputs
    assert "neutrino.delta_CP_pred" in outputs
    print("[PASS] Output parameters test passed\n")


def test_formulas():
    """Test that formulas are correctly defined."""
    sim = NeutrinoMixingSimulation()
    formulas = sim.get_formulas()

    print("=" * 75)
    print("FORMULAS TEST")
    print("=" * 75)
    for formula in formulas:
        print(f"  {formula.id}: {formula.label}")
        print(f"    Category: {formula.category}")
        print(f"    Description: {formula.description[:60]}...")
        print()

    formula_ids = [f.id for f in formulas]
    assert "pmns-theta-13" in formula_ids
    assert "pmns-delta-cp" in formula_ids
    assert "pmns-theta-12" in formula_ids
    assert "pmns-theta-23" in formula_ids
    print("[PASS] Formulas test passed\n")


def test_section_content():
    """Test that section content is correctly defined."""
    sim = NeutrinoMixingSimulation()
    section = sim.get_section_content()

    print("=" * 75)
    print("SECTION CONTENT TEST")
    print("=" * 75)
    print(f"Section: {section.section_id}.{section.subsection_id}")
    print(f"Title: {section.title}")
    print(f"Abstract: {section.abstract}")
    print(f"Content blocks: {len(section.content_blocks)}")
    print(f"Formula refs: {len(section.formula_refs)}")
    print(f"Param refs: {len(section.param_refs)}")
    print()

    assert section.section_id == "4"
    assert section.subsection_id == "4.5"
    assert len(section.content_blocks) > 0
    assert len(section.formula_refs) > 0
    print("[PASS] Section content test passed\n")


def test_parameter_definitions():
    """Test that parameter definitions are correctly defined."""
    sim = NeutrinoMixingSimulation()
    params = sim.get_output_param_definitions()

    print("=" * 75)
    print("PARAMETER DEFINITIONS TEST")
    print("=" * 75)
    for param in params:
        print(f"  {param.path}")
        print(f"    Name: {param.name}")
        print(f"    Units: {param.units}")
        print(f"    Status: {param.status}")
        print(f"    Experimental bound: {param.experimental_bound} {param.units}")
        print()

    param_paths = [p.path for p in params]
    assert "neutrino.theta_12_pred" in param_paths
    assert "neutrino.theta_13_pred" in param_paths
    print("[PASS] Parameter definitions test passed\n")


def test_full_execution():
    """Test full execution of the simulation."""
    print("=" * 75)
    print("FULL EXECUTION TEST")
    print("=" * 75)

    # Create registry and set inputs
    registry = PMRegistry.get_instance()
    PMRegistry.reset_instance()  # Clear any previous state
    registry = PMRegistry.get_instance()

    # Set topological inputs (from TCS #187)
    registry.set_param("topology.b2", 4, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.b3", 24, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.n_gen", 3, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.orientation_sum", 12, source="ESTABLISHED:Sp(2,R)", status="ESTABLISHED")

    # Create and execute simulation
    sim = NeutrinoMixingSimulation()
    results = sim.execute(registry, verbose=False)

    print("\nResults:")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
    print()

    # Validate results are in reasonable ranges
    assert 30 < results["neutrino.theta_12_pred"] < 36
    assert 8 < results["neutrino.theta_13_pred"] < 10
    assert 44 < results["neutrino.theta_23_pred"] < 47
    assert 200 < results["neutrino.delta_CP_pred"] < 260

    print("[PASS] Full execution test passed\n")

    # Check registry was updated
    assert registry.has_param("neutrino.theta_12_pred")
    assert registry.has_param("neutrino.theta_13_pred")
    print("[PASS] Registry update test passed\n")


def main():
    """Run all tests."""
    print("\n")
    print("#" * 75)
    print("# NEUTRINO MIXING V16 SIMULATION TESTS")
    print("#" * 75)
    print("\n")

    test_simulation_metadata()
    test_required_inputs()
    test_output_params()
    test_formulas()
    test_section_content()
    test_parameter_definitions()
    test_full_execution()

    print("=" * 75)
    print("ALL TESTS PASSED")
    print("=" * 75)
    print()


if __name__ == "__main__":
    main()
