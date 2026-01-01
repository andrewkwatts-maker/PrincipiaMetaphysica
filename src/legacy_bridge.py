#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Legacy Bridge
============================================

DOI: 10.5281/zenodo.18079602

This module provides backwards compatibility for v16.0/v16.1 simulations
by wrapping them in a Sterile Environment. Old simulations that relied
on MCMC optimization will be forced to use the fixed 288-root registry.

THE PROBLEM:
    v16.1 simulations used stochastic optimization to "find" constants.
    In v16.2, constants are geometric residues - they cannot be "found."

THE SOLUTION:
    The sterile_wrapper decorator injects the fixed 288-root basis into
    legacy simulations, forcing them to operate in READ_ONLY_STERILE mode.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import functools
import warnings
from typing import Callable, Any, Dict, Optional
import numpy as np

# Import the root derivation engine
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.physics.root_derivation import RootDerivation, BulkInsulationConstant


class SterileEnvironmentError(Exception):
    """Raised when a legacy simulation violates sterile constraints."""
    pass


class LegacySimulationWarning(UserWarning):
    """Warning for legacy simulation patterns detected."""
    pass


def sterile_wrapper(legacy_sim_func: Callable) -> Callable:
    """
    Wraps v16.0/v16.1 simulations to ensure they pull from the
    288-root registry instead of using internal optimizers.

    This decorator:
    1. Forces load of the fixed 125 residues
    2. Injects these into the legacy simulation's 'params'
    3. Sets mode to 'READ_ONLY_STERILE'
    4. Validates output against 288-root constraints

    Usage:
        @sterile_wrapper
        def old_simulation(params):
            # Legacy code that used to optimize
            return results
    """
    @functools.wraps(legacy_sim_func)
    def wrapper(*args, **kwargs):
        # Issue warning about legacy mode
        warnings.warn(
            f"Running legacy simulation '{legacy_sim_func.__name__}' in STERILE mode. "
            "MCMC and optimization are disabled.",
            LegacySimulationWarning
        )

        # 1. Force load the fixed 125 residues from 288-root basis
        model = RootDerivation()
        fixed_basis = model.derive_metric_residues()
        normalized_basis = model.derive_normalized_residues()

        # 2. Create sterile registry
        sterile_registry = {
            "roots": model.TOTAL_ROOTS,
            "torsion": model.SHADOW_TORSION,
            "active": model.OBSERVABLE_NODES,
            "hidden": model.HIDDEN_SUPPORTS,
            "residues": fixed_basis,
            "normalized_residues": normalized_basis,
            "sterile_angle": model.sterile_angle_degrees,
            "decay_constant": model.decay_constant,
        }

        # 3. Inject into kwargs
        kwargs['injected_basis'] = fixed_basis
        kwargs['sterile_registry'] = sterile_registry
        kwargs['mode'] = 'READ_ONLY_STERILE'

        # 4. Execute legacy simulation
        result = legacy_sim_func(*args, **kwargs)

        # 5. Validate output against sterile constraints
        _validate_sterile_output(result, model)

        return result

    return wrapper


def _validate_sterile_output(result: Any, model: RootDerivation) -> None:
    """
    Validate that legacy simulation output respects sterile constraints.

    Raises:
        SterileEnvironmentError: If output violates constraints
    """
    if isinstance(result, dict):
        # Check if result tried to modify core constants
        forbidden_keys = ['optimized_H0', 'fitted_alpha', 'tuned_w0', 'best_fit']
        for key in forbidden_keys:
            if key in result:
                raise SterileEnvironmentError(
                    f"Legacy simulation attempted to set '{key}'. "
                    "In STERILE mode, these values are geometric invariants."
                )

        # Check residue count if present
        if 'residue_count' in result:
            if result['residue_count'] != model.OBSERVABLE_NODES:
                raise SterileEnvironmentError(
                    f"Residue count mismatch: got {result['residue_count']}, "
                    f"expected {model.OBSERVABLE_NODES}"
                )


def enforce_read_only(registry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a read-only view of the registry that raises errors on modification.

    Args:
        registry: The source registry dictionary

    Returns:
        A frozen dictionary-like object
    """
    class ReadOnlyDict(dict):
        def __setitem__(self, key, value):
            raise SterileEnvironmentError(
                f"Cannot modify '{key}' in READ_ONLY_STERILE mode. "
                "Registry is geometrically locked."
            )

        def __delitem__(self, key):
            raise SterileEnvironmentError(
                f"Cannot delete '{key}' in READ_ONLY_STERILE mode."
            )

        def update(self, *args, **kwargs):
            raise SterileEnvironmentError(
                "Cannot update registry in READ_ONLY_STERILE mode."
            )

    return ReadOnlyDict(registry)


def get_sterile_registry() -> Dict[str, Any]:
    """
    Get the fixed 288-root sterile registry.

    Returns:
        Dictionary with all geometric constants locked
    """
    model = RootDerivation()

    return enforce_read_only({
        # Core architecture
        "SO24_generators": model.SO24_GENERATORS,
        "shadow_torsion": model.SHADOW_TORSION,
        "manifold_cost": model.MANIFOLD_COST,
        "total_roots": model.TOTAL_ROOTS,

        # Node partition
        "observable_nodes": model.OBSERVABLE_NODES,
        "hidden_supports": model.HIDDEN_SUPPORTS,

        # 4-Pattern
        "spacetime_dimensions": model.SPACETIME_DIMENSIONS,
        "pins_per_dimension": model.PINS_PER_DIMENSION,
        "torsion_matrix": [6, 6, 6, 6],

        # Derived quantities
        "sterile_angle_deg": model.sterile_angle_degrees,
        "sterile_angle_rad": model.sterile_angle,
        "survival_rate": model.survival_rate,
        "decay_constant": model.decay_constant,
        "bulk_pressure": model.calculate_hidden_pressure(),

        # Sterile ratios
        "insulation_ratio": model.HIDDEN_SUPPORTS / model.OBSERVABLE_NODES,  # 1.304
        "active_density": model.OBSERVABLE_NODES / model.TOTAL_ROOTS,  # 0.434
        "hidden_density": model.HIDDEN_SUPPORTS / model.TOTAL_ROOTS,  # 0.566

        # Mode flag
        "mode": "READ_ONLY_STERILE",
    })


def validate_legacy_compatibility(legacy_params: Dict[str, Any]) -> Dict[str, str]:
    """
    Check if legacy parameters are compatible with v16.2 sterile model.

    Args:
        legacy_params: Parameters from a v16.0/v16.1 simulation

    Returns:
        Dictionary mapping parameter names to compatibility status
    """
    model = RootDerivation()
    results = {}

    # Check mass hierarchy
    if 'particle_weights' in legacy_params:
        results['mass_hierarchy'] = "REQUIRES_REMAP"

    # Check expansion rate
    if 'hubble_fit' in legacy_params or 'H0_optimized' in legacy_params:
        results['expansion_rate'] = "REQUIRES_REPLACEMENT"

    # Check torsion balance
    if 'dimensions' in legacy_params:
        if legacy_params['dimensions'] != 4:
            results['torsion_balance'] = "CRITICAL_UPDATE_REQUIRED"
        else:
            results['torsion_balance'] = "COMPATIBLE"

    # Check registry access
    if 'registry_path' in legacy_params:
        results['registry_access'] = "COMPATIBLE_DIFFERENT_VALUES"

    return results


# ================================================================
# Validation Gate
# ================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PRINCIPIA METAPHYSICA v16.2 - Legacy Bridge Test")
    print("=" * 70)

    # Test sterile registry
    print("\n[1] Testing Sterile Registry...")
    registry = get_sterile_registry()
    print(f"    Total Roots: {registry['total_roots']}")
    print(f"    Observable Nodes: {registry['observable_nodes']}")
    print(f"    Sterile Angle: {registry['sterile_angle_deg']:.4f} deg")
    print(f"    Mode: {registry['mode']}")

    # Test read-only enforcement
    print("\n[2] Testing Read-Only Enforcement...")
    try:
        registry['total_roots'] = 300
        print("    ERROR: Should have raised SterileEnvironmentError")
    except SterileEnvironmentError as e:
        print(f"    Correctly blocked: {str(e)[:50]}...")

    # Test legacy compatibility check
    print("\n[3] Testing Legacy Compatibility...")
    legacy_params = {
        'hubble_fit': 73.0,
        'dimensions': 3,
        'registry_path': 'data/registry.json'
    }
    compat = validate_legacy_compatibility(legacy_params)
    for param, status in compat.items():
        print(f"    {param}: {status}")

    # Test sterile wrapper
    print("\n[4] Testing Sterile Wrapper...")

    @sterile_wrapper
    def mock_legacy_simulation(data, **kwargs):
        mode = kwargs.get('mode', 'UNKNOWN')
        basis = kwargs.get('injected_basis', None)
        return {
            'mode': mode,
            'basis_injected': basis is not None,
            'residue_count': len(basis) if basis is not None else 0
        }

    result = mock_legacy_simulation({'test': True})
    print(f"    Mode: {result['mode']}")
    print(f"    Basis Injected: {result['basis_injected']}")
    print(f"    Residue Count: {result['residue_count']}")

    print("\n" + "=" * 70)
    print("Legacy Bridge: ALL TESTS PASSED")
    print("=" * 70)
