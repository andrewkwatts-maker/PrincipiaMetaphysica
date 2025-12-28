#!/usr/bin/env python3
"""
Principia Metaphysica Framework Initialization
===============================================

Proper initialization order for the PM simulation framework:

1. GEOMETRIC: Load geometric anchors from b₃ = 24
2. ESTABLISHED: Load experimental values from PDG, NuFIT, etc.
3. SIMULATIONS: Run v16 simulations using both GEOMETRIC and ESTABLISHED inputs

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from simulations.base import PMRegistry
from simulations.geometric_anchors_v16_1 import GeometricAnchors


def initialize_framework(verbose: bool = True) -> PMRegistry:
    """
    Initialize the Principia Metaphysica simulation framework.

    This function sets up the PMRegistry with:
    1. GEOMETRIC parameters from b₃ = 24
    2. ESTABLISHED parameters from experiments (if available)

    Args:
        verbose: If True, print initialization status

    Returns:
        Initialized PMRegistry instance
    """
    if verbose:
        print("=" * 70)
        print("INITIALIZING PRINCIPIA METAPHYSICA FRAMEWORK")
        print("=" * 70)
        print()

    # Get singleton registry
    registry = PMRegistry.get_instance()

    # Step 1: Load geometric anchors (FUNDAMENTAL - from topology)
    if verbose:
        print("Step 1: Loading GEOMETRIC anchors from b3 = 24...")
        print("-" * 70)

    anchors = GeometricAnchors(b3=24)
    anchors.register_anchors()

    if verbose:
        print(f"  [OK] Registered 13 GEOMETRIC parameters")
        print()

    # Step 2: Load established physics (EXPERIMENTAL - from measurements)
    if verbose:
        print("Step 2: Loading ESTABLISHED physics from experiments...")
        print("-" * 70)

    try:
        from simulations.base.established import EstablishedPhysics
        EstablishedPhysics.load_into_registry(registry)

        if verbose:
            # Count ESTABLISHED parameters
            all_params = registry.export_parameters()
            established_count = sum(1 for p in all_params.values() if p['status'] == 'ESTABLISHED')
            print(f"  [OK] Registered {established_count} ESTABLISHED parameters")
            print()

    except ImportError as e:
        if verbose:
            print(f"  [WARN] EstablishedPhysics not available: {e}")
            print("  Continuing with GEOMETRIC parameters only...")
            print()

    # Step 3: Verify initialization
    if verbose:
        print("Step 3: Verifying framework initialization...")
        print("-" * 70)

        all_params = registry.export_parameters()

        # Count by status
        status_counts = {}
        for param in all_params.values():
            status = param['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        for status, count in sorted(status_counts.items()):
            print(f"  {status:12s}: {count:3d} parameters")

        print()
        print("-" * 70)
        print(f"Total parameters loaded: {len(all_params)}")
        print()

        # Show some key geometric parameters
        print("Key GEOMETRIC parameters:")
        print("-" * 70)

        key_params = [
            "geometry.b3",
            "geometry.n_generations",
            "geometry.k_gimel",
            "geometry.alpha_gut",
            "geometry.chi_eff",
        ]

        for param_path in key_params:
            if registry.has_param(param_path):
                value = registry.get_param(param_path)
                if isinstance(value, float):
                    print(f"  {param_path:30s} = {value:12.6f}")
                else:
                    print(f"  {param_path:30s} = {value:12}")

        print()

    if verbose:
        print("=" * 70)
        print("FRAMEWORK INITIALIZATION COMPLETE")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Run v16 simulations: python -m simulations.v16.gauge")
        print("  2. Access parameters: registry.get_param('geometry.k_gimel')")
        print("  3. Export results: registry.export_parameters()")
        print()

    return registry


if __name__ == "__main__":
    # Initialize framework with verbose output
    registry = initialize_framework(verbose=True)

    # Example: Access a geometric parameter
    print("Example usage:")
    print("-" * 70)
    k_gimel = registry.get_param("geometry.k_gimel")
    alpha_gut = registry.get_param("geometry.alpha_gut")
    n_gen = registry.get_param("geometry.n_generations")

    print(f"Warp factor k_gimel = {k_gimel:.6f}")
    print(f"GUT coupling alpha_GUT = {alpha_gut:.6f}")
    print(f"Number of generations = {n_gen}")
    print()

    # Show provenance
    entry = registry.get_entry("geometry.k_gimel")
    print(f"Provenance for geometry.k_gimel:")
    print(f"  Source: {entry.source}")
    print(f"  Status: {entry.status}")
    print(f"  Timestamp: {entry.timestamp}")
    print(f"  Metadata: {entry.metadata}")
    print()
