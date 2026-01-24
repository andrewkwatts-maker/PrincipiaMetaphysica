"""
Principia Metaphysica - Sterile Angle Derivation v17.2

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Derives the sterile angle theta from brane intersection geometry.

Formula (Appendix K):
    theta = arcsin(125/288) ~ 25.72 degrees

Where:
    - 125: Number of observable 4D residues (fundamental constants/particles)
    - 288: Total ancestral roots in higher-D symmetry architecture
    - sin(theta) ~ 0.434: Projection fraction surviving as observables

The sterile angle represents the geometric bottleneck fraction of
ancestral symmetry that manifests as the 125 observable constants.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SterileAngleResult:
    """Results from sterile angle derivation."""

    # Input values
    num_residues: int
    ancestral_roots: int

    # Computed values
    sin_theta: float
    theta_rad: float
    theta_deg: float

    # Interpretation
    projection_fraction: float
    percentage: float

    # 288 decomposition
    so24_contribution: int
    signature_adjustment: int
    torsion_factor: int

    status: str
    interpretation: str


class SterileAngleDerivation:
    """
    Sterile angle from shadow brane intersection geometry.

    The sterile angle theta is the intersection angle between
    the two 13D shadow branes during dimensional descent.

    It represents the bottleneck fraction of ancestral symmetry
    that manifests as observable 4D physics (125 residues).
    """

    def __init__(self):
        # Observable residues (fundamental constants/particles)
        self.num_residues = 125

        # Ancestral roots in higher-D symmetry
        # 288 = 276 + 24 - 12 (from Appendix H: 288-Root Basis)
        self.so24_contribution = 276
        self.pleroma = 24
        self.torsion_factor = 12

        self.ancestral_roots = self.so24_contribution + self.pleroma - self.torsion_factor

    def compute_288_decomposition(self) -> Dict[str, Any]:
        """
        Decomposition of 288 ancestral roots.

        R_ancestral = 276 + 24 - 12 = 288
        From SO(24) contributions adjusted by signature/torsion in 25D(24,1).
        """
        return {
            'so24_roots': self.so24_contribution,
            'pleroma': self.pleroma,
            'torsion': self.torsion_factor,
            'total': self.ancestral_roots,
            'formula': '276 + 24 - 12 = 288',
            'interpretation': 'SO(24) contributions with signature/torsion adjustment'
        }

    def compute_sterile_angle(self) -> Dict[str, float]:
        """
        Sterile angle theta = arcsin(125/288).
        """
        sin_theta = self.num_residues / self.ancestral_roots
        theta_rad = np.arcsin(sin_theta)
        theta_deg = np.degrees(theta_rad)

        return {
            'numerator': self.num_residues,
            'denominator': self.ancestral_roots,
            'sin_theta': sin_theta,
            'theta_rad': theta_rad,
            'theta_deg': theta_deg,
            'formula': 'arcsin(125/288)'
        }

    def compute_projection_fraction(self) -> Dict[str, float]:
        """
        Projection fraction: how much of ancestral symmetry survives.
        """
        sin_theta = self.num_residues / self.ancestral_roots
        percentage = sin_theta * 100

        return {
            'fraction': sin_theta,
            'percentage': percentage,
            'interpretation': f'{percentage:.1f}% of ancestral roots manifest as observables'
        }

    def compute_complementary_angle(self) -> Dict[str, float]:
        """
        Complementary angle (90 - theta): hidden/shadow portion.
        """
        theta_deg = np.degrees(np.arcsin(self.num_residues / self.ancestral_roots))
        complementary = 90.0 - theta_deg

        return {
            'theta_deg': theta_deg,
            'complementary_deg': complementary,
            'interpretation': f'{complementary:.2f} degrees remains hidden in shadow sector'
        }

    def compute_full_derivation(self) -> SterileAngleResult:
        """Compute full sterile angle derivation."""
        decomp = self.compute_288_decomposition()
        angle = self.compute_sterile_angle()
        proj = self.compute_projection_fraction()

        return SterileAngleResult(
            num_residues=self.num_residues,
            ancestral_roots=self.ancestral_roots,
            sin_theta=angle['sin_theta'],
            theta_rad=angle['theta_rad'],
            theta_deg=angle['theta_deg'],
            projection_fraction=proj['fraction'],
            percentage=proj['percentage'],
            so24_contribution=self.so24_contribution,
            signature_adjustment=self.pleroma,
            torsion_factor=self.torsion_factor,
            status='COMPUTED',
            interpretation='Bottleneck projection from higher-D to 4D observables'
        )

    def run_demonstration(self) -> Dict[str, Any]:
        """Run sterile angle demonstration."""
        print("=" * 60)
        print("Sterile Angle Derivation from Brane Intersection Geometry")
        print("=" * 60)

        # 288 decomposition
        decomp = self.compute_288_decomposition()
        print(f"\n1. Ancestral Roots (288-Root Basis):")
        print(f"   SO(24) contribution:    {decomp['so24_roots']}")
        print(f"   + Pleroma:              {decomp['pleroma']}")
        print(f"   - Torsion factor:       {decomp['torsion']}")
        print(f"   Total ancestral roots:  {decomp['total']}")

        # Observable residues
        print(f"\n2. Observable Residues:")
        print(f"   125 fundamental constants/particles")
        print(f"   (spectral registry nodes)")

        # Sterile angle
        angle = self.compute_sterile_angle()
        print(f"\n3. Sterile Angle Computation:")
        print(f"   sin(theta) = {angle['numerator']}/{angle['denominator']} = {angle['sin_theta']:.6f}")
        print(f"   theta = {angle['formula']} = {angle['theta_deg']:.6f} degrees")

        # Projection fraction
        proj = self.compute_projection_fraction()
        print(f"\n4. Projection Fraction:")
        print(f"   {proj['percentage']:.2f}% of ancestral symmetry manifests as observables")

        # Complementary
        comp = self.compute_complementary_angle()
        print(f"\n5. Complementary Angle:")
        print(f"   90 - {angle['theta_deg']:.2f} = {comp['complementary_deg']:.2f} degrees")
        print(f"   ({comp['interpretation']})")

        result = self.compute_full_derivation()

        print("\n" + "=" * 60)
        print("The sterile angle ensures only geometrically permitted")
        print("residues emerge, unifying alpha ~ 1/137.036 with topology.")
        print("=" * 60)

        return {
            'decomposition': decomp,
            'angle': angle,
            'projection': proj,
            'complementary': comp,
            'result': result
        }


def run_sterile_angle_demo():
    """Run sterile angle demonstration."""
    deriv = SterileAngleDerivation()
    return deriv.run_demonstration()


if __name__ == '__main__':
    run_sterile_angle_demo()
