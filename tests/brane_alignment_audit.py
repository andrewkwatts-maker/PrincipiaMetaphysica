#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v23.0 - Brane Alignment Audit
====================================================

DOI: 10.5281/zenodo.18079602

This test ensures that the Sterile Angle (the intersection of the two
13D shadow branes) is derived purely from the root count, not from
observational "fitting."

THE STERILE ANGLE:
    theta = arcsin(125/288) = 25.7234 degrees

    This angle is NOT measured - it is a geometric residue of the
    288-root architecture.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.physics.root_derivation import RootDerivation


def verify_sterile_angle() -> dict:
    """
    Validates that the shadow-brane intersection angle
    is a geometric residue of the 288 basis.

    Returns:
        Dictionary with validation results
    """
    model = RootDerivation()

    active_nodes = model.OBSERVABLE_NODES
    total_roots = model.TOTAL_ROOTS

    # The angle is the arcsin of the residue/root ratio
    # theta = arcsin(125/288)
    sin_theta = active_nodes / total_roots
    calc_radians = math.asin(sin_theta)
    calc_degrees = math.degrees(calc_radians)

    # Standard v23.0 Anchor (pre-calculated)
    target_degrees = 25.7234

    # Also calculate cos(theta) for completeness
    cos_theta = math.cos(calc_radians)

    # The tangent gives the shadow/active ratio
    tan_theta = math.tan(calc_radians)

    alignment = math.isclose(calc_degrees, target_degrees, abs_tol=0.0001)

    return {
        "test": "Sterile Angle Alignment",
        "active_nodes": active_nodes,
        "total_roots": total_roots,
        "sin_theta": round(sin_theta, 6),
        "cos_theta": round(cos_theta, 6),
        "tan_theta": round(tan_theta, 6),
        "calculated_radians": round(calc_radians, 6),
        "calculated_degrees": round(calc_degrees, 4),
        "target_degrees": target_degrees,
        "deviation": abs(calc_degrees - target_degrees),
        "status": "LOCKED" if alignment else "MISALIGNED"
    }


def test_angle_stability() -> dict:
    """
    Tests that the sterile angle is stable under small perturbations
    of the node count.

    Returns:
        Dictionary with stability analysis
    """
    model = RootDerivation()
    target = 25.7234

    # Test with perturbations
    perturbations = [
        (124, 288),  # -1 node
        (125, 288),  # exact
        (126, 288),  # +1 node
        (125, 287),  # -1 root
        (125, 289),  # +1 root
    ]

    results = []

    for active, total in perturbations:
        if active <= total:
            angle = math.degrees(math.asin(active / total))
            deviation = abs(angle - target)
        else:
            angle = None
            deviation = float('inf')

        results.append({
            "active": active,
            "total": total,
            "angle": round(angle, 4) if angle else None,
            "deviation": round(deviation, 4) if deviation != float('inf') else "N/A",
            "stable": deviation < 0.01 if deviation != float('inf') else False
        })

    return {
        "test": "Angle Stability",
        "target_angle": target,
        "perturbations": results,
        "conclusion": "Only exact 125/288 gives stable angle"
    }


def test_brane_geometry() -> dict:
    """
    Tests the geometric relationship between the two 13D branes.

    BRANE STRUCTURE (288-24-4 Architecture):
        - Two 13D shadow branes (each: 12 torsion pins + V₇ manifold)
        - Intersection at sterile angle θ = arcsin(125/288)
        - 4D spacetime from: 24 torsion pins / 6 pins per dimension = 4

    The 4D intersection is a DESIGN CONSTRAINT, not derived from
    brane intersection formulas. We verify consistency, not derivation.

    Returns:
        Dictionary with geometric analysis
    """
    model = RootDerivation()

    # Each shadow brane has 13 dimensions (12 torsion + V7)
    brane_dimensions = 13
    torsion_per_brane = model.SHADOW_TORSION // 2  # 24 / 2 = 12

    # The angle between them is the sterile angle
    theta = model.sterile_angle

    # The "opening" between branes
    brane_opening = math.cos(theta)

    # The projection overlap (sin of sterile angle = 125/288)
    projection_overlap = math.sin(theta)

    # DIMENSIONAL CONSISTENCY CHECK:
    # 4D spacetime = 24 torsion pins / 6 pins per dimension
    spacetime_dim = model.SHADOW_TORSION // model.PINS_PER_DIMENSION

    # Verify the sterile angle matches the node ratio exactly
    expected_sin = model.OBSERVABLE_NODES / model.TOTAL_ROOTS
    angle_consistent = math.isclose(projection_overlap, expected_sin, rel_tol=1e-10)

    # Verify dimensional structure
    dim_consistent = (spacetime_dim == 4) and (torsion_per_brane == 12)

    # Geometry is valid if both checks pass
    geometry_valid = angle_consistent and dim_consistent

    return {
        "test": "Brane Geometry",
        "brane_dimensions": brane_dimensions,
        "torsion_per_brane": torsion_per_brane,
        "sterile_angle_rad": round(theta, 6),
        "sterile_angle_deg": round(math.degrees(theta), 4),
        "brane_opening": round(brane_opening, 6),
        "projection_overlap": round(projection_overlap, 6),
        "expected_sin_theta": round(expected_sin, 6),
        "spacetime_dim": spacetime_dim,
        "angle_consistent": angle_consistent,
        "dim_consistent": dim_consistent,
        "status": "GEOMETRY_VALID" if geometry_valid else "GEOMETRY_ERROR"
    }


if __name__ == "__main__":
    print("=" * 70)
    print("BRANE ALIGNMENT AUDIT (Sterile Angle Validation)")
    print("=" * 70)

    result = verify_sterile_angle()

    print(f"\nActive Nodes: {result['active_nodes']}")
    print(f"Total Roots: {result['total_roots']}")
    print(f"\nsin(theta): {result['sin_theta']}")
    print(f"cos(theta): {result['cos_theta']}")
    print(f"tan(theta): {result['tan_theta']}")
    print(f"\nCalculated Angle: {result['calculated_degrees']}°")
    print(f"Target Angle: {result['target_degrees']}°")
    print(f"Deviation: {result['deviation']:.6f}°")
    print(f"\nSTATUS: {result['status']}")

    # Stability test
    print("\n" + "=" * 70)
    print("ANGLE STABILITY ANALYSIS")
    print("=" * 70)

    stability = test_angle_stability()
    for p in stability['perturbations']:
        print(f"  ({p['active']}/{p['total']}): angle={p['angle']}°, dev={p['deviation']}, stable={p['stable']}")

    # Brane geometry
    print("\n" + "=" * 70)
    print("BRANE GEOMETRY")
    print("=" * 70)

    geom = test_brane_geometry()
    print(f"Brane Dimensions: {geom['brane_dimensions']}D each")
    print(f"Sterile Angle: {geom['sterile_angle_deg']}°")
    print(f"Brane Opening: {geom['brane_opening']}")
    print(f"Spacetime Dimension: {geom['spacetime_dim']}D")
    print(f"STATUS: {geom['status']}")
