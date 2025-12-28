#!/usr/bin/env python3
"""
Test script for v16 Pneuma simulations.

This script verifies that the v16 Pneuma mechanism integrates properly
with the PMRegistry and SimulationBase infrastructure.
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(_current_dir)
_project_root = os.path.dirname(_simulations_dir)
sys.path.insert(0, _project_root)

from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics
from simulations.v16.pneuma import PneumaMechanismV16


def test_pneuma_v16():
    """Test Pneuma mechanism v16.0."""
    print("=" * 70)
    print(" TEST: Pneuma Mechanism v16.0")
    print("=" * 70)
    print()

    # Create registry
    registry = PMRegistry()

    # Load established physics
    print("Loading established physics...")
    EstablishedPhysics.load_into_registry(registry)

    # Add topology parameters
    print("Setting topology parameters...")
    registry.set_param("topology.CHI_EFF", 144, source="TCS_187", status="ESTABLISHED")
    registry.set_param("topology.B3", 24, source="TCS_187", status="ESTABLISHED")

    # Create simulation
    sim = PneumaMechanismV16()

    # Verify metadata
    print()
    print("Simulation Metadata:")
    print(f"  ID: {sim.metadata.id}")
    print(f"  Version: {sim.metadata.version}")
    print(f"  Domain: {sim.metadata.domain}")
    print(f"  Section: {sim.metadata.section_id}")

    # Verify inputs
    print()
    print("Required Inputs:")
    for inp in sim.required_inputs:
        has = registry.has_param(inp)
        status = "OK" if has else "MISSING"
        print(f"  {inp}: {status}")

    # Run simulation
    print()
    print("Running simulation...")
    results = sim.execute(registry, verbose=False)

    # Verify outputs
    print()
    print("Outputs:")
    for param_path in sim.output_params:
        if registry.has_param(param_path):
            value = registry.get_param(param_path)
            print(f"  {param_path} = {value}")
        else:
            print(f"  {param_path} = MISSING")

    # Verify formulas
    print()
    print("Formulas:")
    formulas = sim.get_formulas()
    for formula in formulas:
        print(f"  {formula.id} ({formula.label}): {formula.description}")

    # Verify section content
    print()
    print("Section Content:")
    section = sim.get_section_content()
    if section:
        print(f"  Section {section.section_id}: {section.title}")
        print(f"  Blocks: {len(section.content_blocks)}")
        print(f"  Formula refs: {len(section.formula_refs)}")
        print(f"  Param refs: {len(section.param_refs)}")

    # Verify parameter definitions
    print()
    print("Parameter Definitions:")
    params = sim.get_output_param_definitions()
    for param in params:
        print(f"  {param.path}: {param.name} ({param.units})")

    # Validation checks
    print()
    print("=" * 70)
    print(" VALIDATION CHECKS")
    print("=" * 70)

    checks = []

    # Check 1: All outputs injected
    all_injected = all(registry.has_param(p) for p in sim.output_params)
    checks.append(("All outputs injected", all_injected))

    # Check 2: Lagrangian valid
    lagrangian_valid = registry.get_param("pneuma.lagrangian_valid")
    checks.append(("Lagrangian valid", lagrangian_valid))

    # Check 3: VEV positive and finite
    vev = registry.get_param("pneuma.vev")
    vev_ok = vev > 0 and vev < 100
    checks.append(("VEV reasonable", vev_ok))

    # Check 4: Mass scale in reasonable range
    mass_scale = registry.get_param("pneuma.mass_scale")
    mass_ok = 1e16 < mass_scale < 1e19
    checks.append(("Mass scale reasonable", mass_ok))

    # Print results
    for check_name, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"  {check_name}: {status}")

    # Overall result
    print()
    all_passed = all(passed for _, passed in checks)
    if all_passed:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED")
        return 1

    print("=" * 70)
    return 0


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    exit_code = test_pneuma_v16()
    sys.exit(exit_code)
