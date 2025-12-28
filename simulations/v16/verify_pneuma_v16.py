#!/usr/bin/env python3
"""
Verification script for Pneuma v16 upgrade.

Checks that all components are properly installed and functional.
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(_current_dir)
_project_root = os.path.dirname(_simulations_dir)
sys.path.insert(0, _project_root)


def verify_files():
    """Verify all required files exist."""
    print("=" * 70)
    print(" FILE VERIFICATION")
    print("=" * 70)

    base_dir = os.path.join(_simulations_dir, "v16", "pneuma")

    files = [
        "__init__.py",
        "pneuma_mechanism_v16_0.py",
        "README.md",
    ]

    all_exist = True
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        exists = os.path.exists(filepath)
        status = "OK" if exists else "MISSING"
        print(f"  {filename}: {status}")
        if exists:
            size = os.path.getsize(filepath)
            print(f"    Size: {size} bytes")
        all_exist = all_exist and exists

    return all_exist


def verify_imports():
    """Verify module imports work."""
    print()
    print("=" * 70)
    print(" IMPORT VERIFICATION")
    print("=" * 70)

    try:
        from simulations.v16.pneuma import PneumaMechanismV16
        print("  PneumaMechanismV16: OK")

        from simulations.base import PMRegistry, SimulationBase
        print("  PMRegistry: OK")
        print("  SimulationBase: OK")

        from simulations.base.established import EstablishedPhysics
        print("  EstablishedPhysics: OK")

        return True
    except ImportError as e:
        print(f"  Import error: {e}")
        return False


def verify_simulation():
    """Verify simulation runs correctly."""
    print()
    print("=" * 70)
    print(" SIMULATION VERIFICATION")
    print("=" * 70)

    try:
        from simulations.base import PMRegistry
        from simulations.base.established import EstablishedPhysics
        from simulations.v16.pneuma import PneumaMechanismV16

        # Create registry
        registry = PMRegistry()
        EstablishedPhysics.load_into_registry(registry)
        registry.set_param("topology.CHI_EFF", 144, source="TCS_187")
        registry.set_param("topology.B3", 24, source="TCS_187")

        # Run simulation
        sim = PneumaMechanismV16()
        results = sim.execute(registry, verbose=False)

        # Check outputs
        expected_outputs = [
            "pneuma.coupling",
            "pneuma.flow_parameter",
            "pneuma.lagrangian_valid",
            "pneuma.vev",
            "pneuma.mass_scale",
        ]

        all_present = True
        for param in expected_outputs:
            if registry.has_param(param):
                value = registry.get_param(param)
                print(f"  {param}: {value}")
            else:
                print(f"  {param}: MISSING")
                all_present = False

        # Verify formulas
        formulas = sim.get_formulas()
        print(f"\n  Formulas: {len(formulas)}")
        for formula in formulas:
            print(f"    - {formula.id}: {formula.label}")

        # Verify section content
        section = sim.get_section_content()
        print(f"\n  Section Content:")
        print(f"    Section: {section.section_id}")
        print(f"    Title: {section.title}")
        print(f"    Blocks: {len(section.content_blocks)}")

        return all_present and results["pneuma.lagrangian_valid"]

    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_interface():
    """Verify SimulationBase interface implementation."""
    print()
    print("=" * 70)
    print(" INTERFACE VERIFICATION")
    print("=" * 70)

    try:
        from simulations.v16.pneuma import PneumaMechanismV16
        from simulations.base import SimulationBase

        sim = PneumaMechanismV16()

        # Check it's a subclass
        is_subclass = isinstance(sim, SimulationBase)
        print(f"  Is SimulationBase subclass: {is_subclass}")

        # Check required properties
        properties = [
            "metadata",
            "required_inputs",
            "output_params",
            "output_formulas",
        ]

        all_implemented = True
        for prop in properties:
            has_prop = hasattr(sim, prop)
            print(f"  Has {prop}: {has_prop}")
            all_implemented = all_implemented and has_prop

        # Check required methods
        methods = [
            "run",
            "get_section_content",
            "get_formulas",
            "get_output_param_definitions",
        ]

        for method in methods:
            has_method = hasattr(sim, method) and callable(getattr(sim, method))
            print(f"  Has {method}(): {has_method}")
            all_implemented = all_implemented and has_method

        return is_subclass and all_implemented

    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    """Run all verification checks."""
    print()
    print("=" * 70)
    print(" PNEUMA V16 VERIFICATION")
    print("=" * 70)
    print()

    checks = []

    # Run verifications
    files_ok = verify_files()
    checks.append(("Files exist", files_ok))

    imports_ok = verify_imports()
    checks.append(("Imports work", imports_ok))

    interface_ok = verify_interface()
    checks.append(("Interface implemented", interface_ok))

    simulation_ok = verify_simulation()
    checks.append(("Simulation runs", simulation_ok))

    # Summary
    print()
    print("=" * 70)
    print(" VERIFICATION SUMMARY")
    print("=" * 70)

    for check_name, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"  {check_name}: {status}")

    all_passed = all(passed for _, passed in checks)

    print()
    if all_passed:
        print("ALL VERIFICATIONS PASSED")
        print()
        print("Pneuma v16 upgrade successful!")
        return 0
    else:
        print("SOME VERIFICATIONS FAILED")
        return 1


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    exit_code = main()
    sys.exit(exit_code)
