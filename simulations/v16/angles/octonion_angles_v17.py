"""
Principia Metaphysica - Octonion Angle Computations v17.2

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Computes key angles derived from octonionic structure:
- Primary Golden Angle: arctan(1/phi) ~ 31.72 degrees
- Large Golden Angle: 360/phi^2 ~ 137.51 degrees (near 1/alpha!)
- Triality Cycle Angle: 120 degrees
- Fano Plane Base Angle: 360/7 ~ 51.43 degrees
- G2 Embedding Angles from division algebra descent
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class OctonionAnglesResult:
    """Results from octonion angles computation."""

    primary_golden_deg: float
    large_golden_deg: float
    triality_cycle_deg: float
    g2_calibration_deg: float
    fano_base_deg: float

    phi: float
    large_golden_near_alpha: str
    status: str


class OctonionAngles:
    """
    Octonion-derived angles for division algebra and G2 geometry.

    The octonions are the largest normed division algebra (8D).
    G2 = Aut(O) preserves octonionic multiplication.
    These angles link octonionic structure to physical parameters.
    """

    def __init__(self):
        self.PHI = (1 + np.sqrt(5)) / 2  # Golden ratio ~ 1.618

    def compute_primary_golden(self) -> Dict[str, float]:
        """
        Primary octonionic golden angle: arctan(1/phi) ~ 31.72 degrees
        """
        theta_rad = np.arctan(1 / self.PHI)
        theta_deg = np.degrees(theta_rad)

        return {
            'theta_rad': theta_rad,
            'theta_deg': theta_deg,
            'formula': 'arctan(1/phi)',
            'interpretation': 'Base for many residues and mixing angles'
        }

    def compute_large_golden(self) -> Dict[str, Any]:
        """
        Large golden angle: 360/phi^2 ~ 137.51 degrees

        Strikingly close to 1/alpha ~ 137.036!
        This is the phyllotaxis angle (optimal packing in nature).
        """
        theta_deg = 360 / (self.PHI ** 2)
        supplement = 360 - theta_deg

        return {
            'theta_deg': theta_deg,
            'supplement_deg': supplement,
            'formula': '360 / phi^2',
            'alpha_inverse': 137.036,
            'difference': abs(theta_deg - 137.036),
            'interpretation': 'Geometric near-match to 1/alpha (refined with sterile terms)'
        }

    def compute_triality_cycle(self) -> Dict[str, float]:
        """
        Triality cycle angle: 120 degrees

        G2's outer automorphism cycles three representations.
        This 3-fold symmetry appears in many places.
        """
        return {
            'theta_deg': 120.0,
            'fold': 3,
            'formula': '360 / 3',
            'interpretation': 'G2 outer automorphism cycles (1, 7, 7) reps'
        }

    def compute_g2_calibration(self) -> Dict[str, float]:
        """
        G2 3-form calibration angle: arccos(1/3) ~ 70.53 degrees

        From associative 3-form normalization in G2 geometry.
        """
        cos_val = 1/3
        theta_rad = np.arccos(cos_val)
        theta_deg = np.degrees(theta_rad)

        return {
            'cos_val': cos_val,
            'theta_rad': theta_rad,
            'theta_deg': theta_deg,
            'formula': 'arccos(1/3)',
            'interpretation': 'Calibration angle from 3-form phi'
        }

    def compute_fano_plane_base(self) -> Dict[str, float]:
        """
        Fano plane base angle: 360/7 ~ 51.43 degrees

        The Fano plane is the projective plane over F_2.
        It encodes octonionic multiplication (7 lines, 7 points).
        """
        theta_deg = 360 / 7

        return {
            'theta_deg': theta_deg,
            'formula': '360 / 7',
            'lines': 7,
            'points': 7,
            'interpretation': 'Projective angles in octonion multiplication diagram'
        }

    def compute_all_angles(self) -> OctonionAnglesResult:
        """Compute all octonion angles."""
        primary = self.compute_primary_golden()
        large = self.compute_large_golden()
        triality = self.compute_triality_cycle()
        g2_cal = self.compute_g2_calibration()
        fano = self.compute_fano_plane_base()

        return OctonionAnglesResult(
            primary_golden_deg=primary['theta_deg'],
            large_golden_deg=large['theta_deg'],
            triality_cycle_deg=triality['theta_deg'],
            g2_calibration_deg=g2_cal['theta_deg'],
            fano_base_deg=fano['theta_deg'],
            phi=self.PHI,
            large_golden_near_alpha=f"{large['theta_deg']:.4f} vs 1/alpha = 137.036",
            status='COMPUTED'
        )

    def run_demonstration(self) -> Dict[str, Any]:
        """Run octonion angles demonstration."""
        print("=" * 60)
        print("Octonion Angle Computations")
        print("=" * 60)

        print(f"\nGolden Ratio phi = {self.PHI:.12f}")

        primary = self.compute_primary_golden()
        print(f"\n1. Primary Golden Angle:")
        print(f"   {primary['formula']} = {primary['theta_deg']:.6f} degrees")

        large = self.compute_large_golden()
        print(f"\n2. Large Golden Angle:")
        print(f"   {large['formula']} = {large['theta_deg']:.6f} degrees")
        print(f"   Note: 1/alpha = {large['alpha_inverse']}")
        print(f"   Difference: {large['difference']:.4f} degrees")

        triality = self.compute_triality_cycle()
        print(f"\n3. Triality Cycle Angle:")
        print(f"   {triality['theta_deg']:.2f} degrees ({triality['interpretation']})")

        g2_cal = self.compute_g2_calibration()
        print(f"\n4. G2 Calibration Angle:")
        print(f"   {g2_cal['formula']} = {g2_cal['theta_deg']:.6f} degrees")

        fano = self.compute_fano_plane_base()
        print(f"\n5. Fano Plane Base Angle:")
        print(f"   {fano['formula']} = {fano['theta_deg']:.6f} degrees")

        print("\n" + "=" * 60)
        print("Large Golden Angle's proximity to 1/alpha is refined")
        print("in the theory via sterile and torsion residues.")
        print("=" * 60)

        return {
            'primary': primary,
            'large': large,
            'triality': triality,
            'g2_cal': g2_cal,
            'fano': fano,
            'result': self.compute_all_angles()
        }


def run_octonion_demo():
    """Run octonion angles demonstration."""
    angles = OctonionAngles()
    return angles.run_demonstration()


if __name__ == '__main__':
    run_octonion_demo()
