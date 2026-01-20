#!/usr/bin/env python3
"""
Example: Integration of Covariance Analysis in PM Workflow
============================================================

This example demonstrates how the covariance matrix analysis integrates
with the full Principia Metaphysica simulation pipeline.

Workflow:
1. Run physics simulations (neutrino, cosmology, etc.)
2. Predictions are stored in PMRegistry
3. Covariance analysis reads predictions from registry
4. Statistical validation computed with proper correlations
5. Results written back to registry and exported

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import sys
import os
from pathlib import Path

# Add simulations to path
_simulations_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(_simulations_root))

from simulations.base import PMRegistry
from simulations.v16.statistics import RigorCovarianceV16_1


def run_full_validation_workflow(verbose: bool = True):
    """
    Demonstrate full validation workflow.

    In a real scenario, the predictions would come from actual physics
    simulations. Here we use placeholder values for demonstration.

    Args:
        verbose: Whether to print detailed output

    Returns:
        Dictionary with validation results
    """
    if verbose:
        print("=" * 75)
        print("PM v16.1 - FULL VALIDATION WORKFLOW EXAMPLE")
        print("=" * 75)

    # Step 1: Initialize registry
    if verbose:
        print("\n[1] Initializing PMRegistry...")
    registry = PMRegistry.get_instance()

    # Step 2: Simulate running physics modules (normally these would be actual sims)
    if verbose:
        print("\n[2] Running physics simulations...")

    # Neutrino mixing simulation (placeholder)
    if verbose:
        print("    - Running neutrino_mixing_v16_0...")
    registry.set_param(
        "neutrino.theta_12_pred",
        33.59,  # Example: PM prediction for solar angle
        source="neutrino_mixing_v16_0",
        status="PREDICTED",
        metadata={"units": "degrees", "description": "Solar mixing angle from G2 geometry"}
    )
    registry.set_param(
        "neutrino.theta_13_pred",
        8.33,  # Example: PM prediction for reactor angle
        source="neutrino_mixing_v16_0",
        status="PREDICTED",
        metadata={"units": "degrees", "description": "Reactor mixing angle from G2 geometry"}
    )
    registry.set_param(
        "neutrino.theta_23_pred",
        42.75,  # Example: PM prediction for atmospheric angle
        source="neutrino_mixing_v16_0",
        status="PREDICTED",
        metadata={"units": "degrees", "description": "Atmospheric mixing angle from G2 geometry"}
    )
    registry.set_param(
        "neutrino.delta_CP_pred",
        232.5,  # Example: PM prediction for CP phase
        source="neutrino_mixing_v16_0",
        status="PREDICTED",
        metadata={"units": "degrees", "description": "CP-violating phase from G2 geometry"}
    )

    # Dark energy simulation (placeholder)
    if verbose:
        print("    - Running dark_energy_v16_0...")
    registry.set_param(
        "cosmology.w0_derived",
        -11/13,  # PM prediction: w0 = -11/13 ≈ -0.846
        source="dark_energy_v16_0",
        status="PREDICTED",
        metadata={"units": "dimensionless", "description": "Dark energy EoS at z=0 from pneuma mechanism"}
    )
    registry.set_param(
        "cosmology.wa_derived",
        0.288,  # Example: PM prediction for time evolution
        source="dark_energy_v16_0",
        status="PREDICTED",
        metadata={"units": "dimensionless", "description": "Dark energy evolution parameter"}
    )

    # Cosmology simulation (placeholder)
    if verbose:
        print("    - Running cosmology_parameters_v16_0...")
    registry.set_param(
        "cosmology.Omega_m",
        0.310,  # Example: PM prediction for matter density
        source="cosmology_parameters_v16_0",
        status="PREDICTED",
        metadata={"units": "dimensionless", "description": "Matter density parameter"}
    )
    registry.set_param(
        "cosmology.H0",
        68.5,  # Example: PM prediction for Hubble constant
        source="cosmology_parameters_v16_0",
        status="PREDICTED",
        metadata={"units": "km/s/Mpc", "description": "Hubble constant"}
    )

    # Step 3: Run covariance analysis
    if verbose:
        print("\n[3] Running rigorous covariance analysis...")
    cov_sim = RigorCovarianceV16_1()
    results = cov_sim.execute(registry, verbose=False)

    # Step 4: Display results
    if verbose:
        print("\n[4] Validation Results:")
        print("-" * 75)

        # Neutrino sector
        print(f"\nNeutrino Sector (NuFIT 6.0):")
        print(f"  χ² = {results['statistics.neutrino_chi_square']:.2f}")
        print(f"  ndof = {results['statistics.neutrino_ndof']}")
        print(f"  χ²/ndof = {results['statistics.neutrino_chi_square']/results['statistics.neutrino_ndof']:.2f}")
        print(f"  p-value = {results['statistics.neutrino_p_value']:.4f}")
        print(f"  Status: {results['statistics.neutrino_status']}")

        # Cosmology sector
        print(f"\nCosmology Sector (DESI 2025):")
        print(f"  χ² = {results['statistics.cosmology_chi_square']:.2f}")
        print(f"  ndof = {results['statistics.cosmology_ndof']}")
        print(f"  χ²/ndof = {results['statistics.cosmology_chi_square']/results['statistics.cosmology_ndof']:.2f}")
        print(f"  p-value = {results['statistics.cosmology_p_value']:.4f}")
        print(f"  Status: {results['statistics.cosmology_status']}")

        # Combined
        print(f"\nCombined Analysis:")
        print(f"  χ² = {results['statistics.combined_chi_square']:.2f}")
        print(f"  ndof = {results['statistics.combined_ndof']}")
        print(f"  χ²/ndof = {results['statistics.combined_chi_square']/results['statistics.combined_ndof']:.2f}")
        print(f"  p-value = {results['statistics.combined_p_value']:.4f}")
        print(f"  Status: {results['statistics.combined_status']}")

    # Step 5: Interpretation
    if verbose:
        print("\n[5] Interpretation:")
        print("-" * 75)

        neu_status = results['statistics.neutrino_status']
        cos_status = results['statistics.cosmology_status']
        combined_status = results['statistics.combined_status']

        if neu_status in ['EXCELLENT', 'GOOD']:
            print("  ✓ Neutrino sector: Predictions agree well with NuFIT 6.0 data")
        else:
            print("  ⚠ Neutrino sector: Some tensions present, require investigation")

        if cos_status in ['EXCELLENT', 'GOOD']:
            print("  ✓ Cosmology sector: Predictions agree well with DESI 2025 data")
        else:
            print("  ⚠ Cosmology sector: Tensions present")
            print("    Note: This is expected for the test values used here.")
            print("    PM predicts w0 = -11/13 ≈ -0.846, while DESI finds -0.727 ± 0.067")

        print(f"\n  Overall assessment: {combined_status}")

        if combined_status in ['EXCELLENT', 'GOOD', 'ACCEPTABLE']:
            print("  → PM v16.1 provides statistically acceptable fits to data")
        elif combined_status == 'MARGINAL':
            print("  → Marginal fit; some refinements may improve agreement")
        else:
            print("  → Significant tensions; review predictions or consider systematics")

    # Step 6: Export results (optional)
    if verbose:
        print("\n[6] Export options:")
        print("    - registry.export_parameters() → all parameters with metadata")
        print("    - registry.export_sections() → section content for paper")
        print("    - cov_sim.get_section_content() → Appendix A.S content")

    print("\n" + "=" * 75)
    print("WORKFLOW COMPLETE")
    print("=" * 75)

    return results


def demonstrate_parameter_pulls(verbose: bool = True):
    """
    Demonstrate how to access individual parameter pulls.

    Pulls show how far each parameter deviates from experiment
    in units of its uncertainty, accounting for correlations.
    """
    if verbose:
        print("\n" + "=" * 75)
        print("PARAMETER PULLS DEMONSTRATION")
        print("=" * 75)

    # Initialize and run
    registry = PMRegistry.get_instance()

    # Set predictions (same as above)
    registry.set_param("neutrino.theta_12_pred", 33.59, source="test", status="PREDICTED")
    registry.set_param("neutrino.theta_13_pred", 8.33, source="test", status="PREDICTED")
    registry.set_param("neutrino.theta_23_pred", 42.75, source="test", status="PREDICTED")
    registry.set_param("neutrino.delta_CP_pred", 232.5, source="test", status="PREDICTED")

    registry.set_param("cosmology.w0_derived", -11/13, source="test", status="PREDICTED")
    registry.set_param("cosmology.wa_derived", 0.288, source="test", status="PREDICTED")
    registry.set_param("cosmology.Omega_m", 0.310, source="test", status="PREDICTED")
    registry.set_param("cosmology.H0", 68.5, source="test", status="PREDICTED")

    # Run analysis
    cov_sim = RigorCovarianceV16_1()
    cov_sim.execute(registry, verbose=False)

    # Access results
    neu_result = cov_sim.neutrino_result
    cos_result = cov_sim.cosmology_result

    if verbose:
        print("\nNeutrino Parameter Pulls:")
        print("-" * 75)
        for i, param_name in enumerate(neu_result.covariance_data.parameter_names):
            pred = neu_result.predictions[i]
            obs = neu_result.observations[i]
            pull = neu_result.pulls[i]
            print(f"  {param_name:12s}: {pred:7.2f} vs {obs:7.2f} (pull = {pull:+5.2f}σ)")

        print("\nCosmology Parameter Pulls:")
        print("-" * 75)
        for i, param_name in enumerate(cos_result.covariance_data.parameter_names):
            pred = cos_result.predictions[i]
            obs = cos_result.observations[i]
            pull = cos_result.pulls[i]
            print(f"  {param_name:12s}: {pred:7.4f} vs {obs:7.4f} (pull = {pull:+5.2f}σ)")

        print("\nNote: Pulls are marginalized (accounting for correlations with other params)")
        print("      A large pull in one parameter can be compensated by correlations.")

    print("\n" + "=" * 75)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Run full workflow
    results = run_full_validation_workflow(verbose=True)

    # Demonstrate parameter pulls
    demonstrate_parameter_pulls(verbose=True)
