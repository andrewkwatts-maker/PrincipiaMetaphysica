"""
Principia Metaphysica - Bazien Angles Analysis v17.2

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Analysis of Bazien Angles in the Master Action:
- Sterile Angle: arcsin(125/288) ~ 25.72 degrees (projection bottleneck)
- Golden Angle: arctan(1/phi) ~ 31.72 degrees (octonionic base)
- Shadow Projection Angle (related to fine-structure residue)
- Related mixing/projection angles (Cabibbo precursor, weak mixing base)

These angles govern brane-node overlaps, spectral residues, and parameter
locking in the Pneuma Lagrangian during SpR(2) -> G2 -> CY3 descent.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

from core.FormulasRegistry import get_registry

_REG = get_registry()


@dataclass
class BazienAnglesResult:
    """Results from Bazien angles computation."""

    sterile_angle_deg: float
    golden_angle_deg: float
    shadow_projection_deg: float
    cabibbo_precursor_deg: float
    weak_bulk_precursor_deg: float

    sterile_sin: float
    status: str


class BazienAngles:
    """
    Bazien angles from shadow brane intersection and parameter locking.

    These angles arise in the 25D -> 13D -> 7D -> 4D dimensional descent,
    governing which ancestral roots project to observable residues.
    """

    def __init__(self):
        self.NUM_RESIDUES = _REG.sophian_registry  # Observable spectral residues (125)
        self.ANC_ROOTS = _REG.nitzotzin_roots  # Ancestral root basis (288)
        self.B3 = _REG.elder_kads  # Third Betti number (24)
        self.PHI = (1 + np.sqrt(5)) / 2  # Golden ratio

    def compute_sterile_angle(self) -> Dict[str, float]:
        """
        Primary Bazien angle: shadow brane intersection.
        arcsin(125/288) ~ 25.72 degrees
        """
        sin_theta = self.NUM_RESIDUES / self.ANC_ROOTS
        theta_rad = np.arcsin(sin_theta)
        theta_deg = np.degrees(theta_rad)

        return {
            'sin_theta': sin_theta,
            'theta_rad': theta_rad,
            'theta_deg': theta_deg,
            'interpretation': f'{self.NUM_RESIDUES}/{self.ANC_ROOTS} ~ {sin_theta:.4f} projection fraction'
        }

    def compute_golden_angle(self) -> Dict[str, float]:
        """
        Octonionic golden angle: arctan(1/phi) ~ 31.72 degrees
        """
        theta_rad = np.arctan(1 / self.PHI)
        theta_deg = np.degrees(theta_rad)

        return {
            'theta_rad': theta_rad,
            'theta_deg': theta_deg,
            'phi': self.PHI,
            'interpretation': 'Base angle for many residues (octonionic/G2)'
        }

    def compute_shadow_projection(self) -> Dict[str, float]:
        """
        Shadow projection angle (heuristic from residue tables).
        Approximately sterile + golden/4
        """
        sterile = self.compute_sterile_angle()['theta_deg']
        golden = self.compute_golden_angle()['theta_deg']
        shadow = sterile + golden / 4

        return {
            'theta_deg': shadow,
            'formula': 'theta_sterile + theta_golden / 4',
            'interpretation': 'Shadow brane overlap enhancement'
        }

    def compute_cabibbo_precursor(self) -> Dict[str, float]:
        """
        Cabibbo angle precursor: golden / 2.5 ~ 12.69 degrees
        """
        golden = self.compute_golden_angle()['theta_deg']
        cabibbo = golden / 2.5

        return {
            'theta_deg': cabibbo,
            'formula': 'theta_golden / 2.5',
            'observed_cabibbo': 13.0,
            'interpretation': 'Small mixing base from 3D cycle suppression'
        }

    def compute_weak_bulk_precursor(self) -> Dict[str, float]:
        """
        Weak mixing bulk precursor: sin^2(theta_W) ~ 0.25 at GUT scale
        """
        sin2_bulk = 0.25
        theta_rad = np.arcsin(np.sqrt(sin2_bulk))
        theta_deg = np.degrees(theta_rad)

        return {
            'sin2_theta': sin2_bulk,
            'theta_deg': theta_deg,
            'interpretation': 'Unified value before torsion thinning'
        }

    def compute_all_angles(self) -> BazienAnglesResult:
        """
        Compute all Bazien angles.
        """
        sterile = self.compute_sterile_angle()
        golden = self.compute_golden_angle()
        shadow = self.compute_shadow_projection()
        cabibbo = self.compute_cabibbo_precursor()
        weak = self.compute_weak_bulk_precursor()

        return BazienAnglesResult(
            sterile_angle_deg=sterile['theta_deg'],
            golden_angle_deg=golden['theta_deg'],
            shadow_projection_deg=shadow['theta_deg'],
            cabibbo_precursor_deg=cabibbo['theta_deg'],
            weak_bulk_precursor_deg=weak['theta_deg'],
            sterile_sin=sterile['sin_theta'],
            status='COMPUTED'
        )

    def run_demonstration(self) -> Dict[str, Any]:
        """Run Bazien angles demonstration."""
        print("=" * 60)
        print("Bazien Angles Analysis")
        print("=" * 60)

        sterile = self.compute_sterile_angle()
        print(f"\n1. Sterile Angle theta_sterile:")
        print(f"   arcsin({self.NUM_RESIDUES}/{self.ANC_ROOTS}) = {sterile['theta_deg']:.4f} degrees")
        print(f"   Projection bottleneck: {sterile['interpretation']}")

        golden = self.compute_golden_angle()
        print(f"\n2. Golden Angle theta_g:")
        print(f"   arctan(1/phi) = {golden['theta_deg']:.4f} degrees")
        print(f"   Octonionic base for residues")

        shadow = self.compute_shadow_projection()
        print(f"\n3. Shadow Projection Angle:")
        print(f"   {shadow['formula']} = {shadow['theta_deg']:.4f} degrees")

        cabibbo = self.compute_cabibbo_precursor()
        print(f"\n4. Cabibbo Precursor:")
        print(f"   {cabibbo['formula']} = {cabibbo['theta_deg']:.4f} degrees")
        print(f"   Observed Cabibbo angle: ~{cabibbo['observed_cabibbo']} degrees")

        weak = self.compute_weak_bulk_precursor()
        print(f"\n5. Weak Mixing Bulk Precursor:")
        print(f"   sin^2(theta_W) = {weak['sin2_theta']} -> {weak['theta_deg']:.4f} degrees")

        print("\n" + "=" * 60)

        return {
            'sterile': sterile,
            'golden': golden,
            'shadow': shadow,
            'cabibbo': cabibbo,
            'weak': weak,
            'result': self.compute_all_angles()
        }


def run_bazien_demo():
    """Run Bazien angles demonstration."""
    angles = BazienAngles()
    return angles.run_demonstration()


if __name__ == '__main__':
    run_bazien_demo()
