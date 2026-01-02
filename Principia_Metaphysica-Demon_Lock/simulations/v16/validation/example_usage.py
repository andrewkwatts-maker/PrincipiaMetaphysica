#!/usr/bin/env python3
"""
Example usage of RigorousValidatorV16_1

This script demonstrates how to integrate the rigorous validator into
the PM simulation pipeline.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import sys
import os
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
sys.path.insert(0, _simulations_root)

from simulations.base import PMRegistry
from simulations.v16.validation import RigorousValidatorV16_1


def main():
    """
    Main example demonstrating validator usage.
    """
    print("\n" + "="*80)
    print("RIGOROUS VALIDATOR v16.1 - EXAMPLE USAGE")
    print("="*80)

    # Step 1: Create registry
    print("\n[1] Creating PMRegistry...")
    registry = PMRegistry.get_instance()

    # Step 2: Populate with predictions from other simulations
    # (In real usage, these would come from neutrino_mixing_v16_0 and dark_energy_v16_0)
    print("[2] Loading predictions into registry...")

    # Neutrino predictions (from neutrino_mixing_v16_0)
    registry.set_param("neutrino.theta_12_pred", 33.59,
                      source="neutrino_mixing_v16_0", status="PREDICTED",
                      metadata={"units": "degrees", "description": "Solar mixing angle"})

    registry.set_param("neutrino.theta_13_pred", 8.33,
                      source="neutrino_mixing_v16_0", status="PREDICTED",
                      metadata={"units": "degrees", "description": "Reactor mixing angle"})

    registry.set_param("neutrino.theta_23_pred", 45.75,
                      source="neutrino_mixing_v16_0", status="PREDICTED",
                      metadata={"units": "degrees", "description": "Atmospheric mixing angle"})

    registry.set_param("neutrino.delta_CP_pred", 232.5,
                      source="neutrino_mixing_v16_0", status="PREDICTED",
                      metadata={"units": "degrees", "description": "CP-violating phase"})

    # Dark energy predictions (from dark_energy_v16_0)
    registry.set_param("cosmology.w0_derived", -11/13,
                      source="dark_energy_v16_0", status="PREDICTED",
                      metadata={"units": "dimensionless", "description": "Dark energy EoS"})

    registry.set_param("cosmology.wa_derived", 0.288,
                      source="dark_energy_v16_0", status="PREDICTED",
                      metadata={"units": "dimensionless", "description": "Evolution parameter"})

    # Cosmology predictions (if available)
    registry.set_param("cosmology.Omega_m", 0.310,
                      source="cosmology_sim", status="PREDICTED",
                      metadata={"units": "dimensionless", "description": "Matter density"})

    registry.set_param("cosmology.H0", 68.5,
                      source="cosmology_sim", status="PREDICTED",
                      metadata={"units": "km/s/Mpc", "description": "Hubble constant"})

    # Step 3: Create and execute validator
    print("[3] Creating validator...")
    validator = RigorousValidatorV16_1()

    print("[4] Executing validation...")
    results = validator.execute(registry, verbose=True)

    # Step 4: Display results
    print("\n" + "="*80)
    print("VALIDATION RESULTS SUMMARY")
    print("="*80)
    print(f"\nOverall Status: {results['validation.overall_status']}")
    print(f"Total Checks: {results['validation.total_checks']}")
    print(f"  ✓ PASS: {results['validation.pass_count']} ({100*results['validation.pass_count']/results['validation.total_checks']:.1f}%)")
    print(f"  ⚠ TENSION: {results['validation.tension_count']} ({100*results['validation.tension_count']/results['validation.total_checks']:.1f}%)")

    print(f"\nSector Breakdown:")
    print(f"  Neutrino: {results['validation.neutrino_status']}")
    print(f"  Dark Energy: {results['validation.dark_energy_status']}")
    print(f"  Cosmology: {results['validation.cosmology_status']}")

    # Step 5: Display detailed validation entries
    print("\n" + "="*80)
    print("DETAILED VALIDATION ENTRIES")
    print("="*80)

    for i, entry in enumerate(validator.validation_entries, 1):
        status_icon = "✓" if entry.status == "PASS" else "⚠"
        print(f"\n[{i}] {status_icon} {entry.param_name}")
        print(f"    PM Prediction: {entry.pm_value:.4f}")
        print(f"    Experimental: {entry.exp_value:.4f} ± {entry.exp_uncertainty:.4f} ({entry.source})")
        print(f"    Deviation: {entry.sigma_deviation:.2f}σ")
        print(f"    Status: {entry.status}")
        if entry.notes:
            print(f"    Notes: {entry.notes}")

    # Step 6: Access section content
    print("\n" + "="*80)
    print("SECTION CONTENT (for paper)")
    print("="*80)
    section = validator.get_section_content()
    if section:
        print(f"\nSection ID: {section.section_id}.{section.subsection_id}")
        print(f"Title: {section.title}")
        print(f"Abstract: {section.abstract[:200]}...")
        print(f"Content Blocks: {len(section.content_blocks)}")
        print(f"Formula Refs: {section.formula_refs}")

    # Step 7: Access formulas
    print("\n" + "="*80)
    print("FORMULAS")
    print("="*80)
    for formula in validator.get_formulas():
        print(f"\n{formula.id} ({formula.label}): {formula.description}")
        print(f"  LaTeX: {formula.latex[:80]}...")

    print("\n" + "="*80)
    print("EXAMPLE COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
