#!/usr/bin/env python3
"""
Spin(7) Outer Automorphism for Shadow Duality
==============================================

Licensed under the MIT License. See LICENSE file for details.

Implements the Z_2 outer automorphism of Spin(7) that explains the
duality between normal and mirror shadows in Principia Metaphysica.

PHYSICAL SIGNIFICANCE
=====================

The key insight connecting Spin(7) automorphism to shadow physics:

1. OUTER AUTOMORPHISM GROUP
   Out(Spin(7)) = Z_2 (order 2)

   This Z_2 swaps the vector and spinor representations:
   8_v (vector) <-> 8_s (spinor)

2. SHADOW DUALITY APPLICATION
   - Normal shadow: 8_v dominant -> quarks -> small CKM mixing
   - Mirror shadow: 8_s dominant -> sterile neutrinos -> large PMNS mixing

3. THE R_PERP CONNECTION
   The OR reduction operator R_perp (with R_perp^2 = -I) acts on bridge pairs.
   Its action on the 12 (2,0) pairs implements the Spin(7) outer automorphism,
   creating the asymmetry between shadows.

MATHEMATICAL DETAILS
====================

Spin(7) Representations:
- 8_v: vector representation (SO(7) fundamental)
- 8_s: spinor representation (unique for Spin(7) vs SO(7))
- 7: adjoint restricted from 8_v (G2 content)

The outer automorphism:
- sigma: Spin(7) -> Spin(7)
- sigma^2 = id (order 2)
- sigma(8_v) = 8_s, sigma(8_s) = 8_v
- sigma preserves 7 (adjoint)

Application to Residue Fluxes:
- Normal: F_normal = F_v (vector flux pattern)
- Mirror: F_mirror = sigma(F_normal) = F_s (spinor flux pattern)

This explains why:
- CKM ~ epsilon (small, hierarchical) - confined to G2/7D
- PMNS ~ 1 (large, democratic) - full 8D spinor structure

References:
-----------
- Yokota, I. (1990). "Exceptional Lie Groups". arXiv:0902.0431
- Harvey, R. (1990). "Spinors and Calibrations". Academic Press

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum


class SpinorType(Enum):
    """Type of Spin(7) representation."""
    VECTOR = "8_v"      # Vector representation
    SPINOR = "8_s"      # Spinor representation
    ADJOINT = "21"      # Adjoint (Spin(7) Lie algebra)
    SINGLET = "1"       # Singlet


class ShadowType(Enum):
    """Type of shadow in dual-shadow framework."""
    NORMAL = "normal"   # Vector-dominant (quarks/CKM)
    MIRROR = "mirror"   # Spinor-dominant (leptons/PMNS)


class Spin7Automorphism:
    """
    Implementation of the Z_2 outer automorphism of Spin(7).

    This automorphism swaps 8_v <-> 8_s and explains the
    normal/mirror shadow asymmetry.
    """

    def __init__(self):
        """Initialize Spin(7) automorphism structure."""
        # Dimension of representations
        self.dim = {
            SpinorType.VECTOR: 8,
            SpinorType.SPINOR: 8,
            SpinorType.ADJOINT: 21,
            SpinorType.SINGLET: 1,
        }

        # The Z_2 outer automorphism
        self.outer_automorphism_order = 2

    def apply_automorphism(self, rep_type: SpinorType) -> SpinorType:
        """
        Apply the Z_2 outer automorphism to a representation.

        The automorphism swaps 8_v <-> 8_s but preserves 21 and 1.

        Args:
            rep_type: Input representation type

        Returns:
            Image under sigma
        """
        if rep_type == SpinorType.VECTOR:
            return SpinorType.SPINOR
        elif rep_type == SpinorType.SPINOR:
            return SpinorType.VECTOR
        else:
            # Adjoint and singlet are preserved
            return rep_type

    def shadow_representation(self, shadow: ShadowType) -> SpinorType:
        """
        Get the dominant representation for a shadow type.

        Args:
            shadow: Shadow type (normal or mirror)

        Returns:
            Dominant Spin(7) representation
        """
        if shadow == ShadowType.NORMAL:
            return SpinorType.VECTOR
        else:
            return SpinorType.SPINOR

    def relate_shadows(self, shadow: ShadowType) -> ShadowType:
        """
        Apply the Z_2 to relate shadows.

        Normal <-> Mirror under the outer automorphism.

        Args:
            shadow: Input shadow type

        Returns:
            Related shadow type
        """
        if shadow == ShadowType.NORMAL:
            return ShadowType.MIRROR
        else:
            return ShadowType.NORMAL

    def decompose_under_g2(self, rep_type: SpinorType) -> Dict[str, int]:
        """
        Decompose Spin(7) representation under G2 subgroup.

        The branching rules:
        - 8_v -> 7 + 1  (vector -> G2 fundamental + singlet)
        - 8_s -> 8      (spinor stays irreducible under G2)
        - 21 -> 14 + 7  (adjoint -> G2 adjoint + fundamental)

        Args:
            rep_type: Spin(7) representation

        Returns:
            Dictionary of G2 representation content
        """
        if rep_type == SpinorType.VECTOR:
            return {"7": 1, "1": 1}  # 8 = 7 + 1
        elif rep_type == SpinorType.SPINOR:
            return {"8": 1}  # Stays as 8 under G2
        elif rep_type == SpinorType.ADJOINT:
            return {"14": 1, "7": 1}  # 21 = 14 + 7
        else:
            return {"1": 1}

    def mixing_pattern(self, shadow: ShadowType) -> str:
        """
        Describe the mixing pattern for a shadow type.

        Args:
            shadow: Shadow type

        Returns:
            Description of mixing pattern
        """
        if shadow == ShadowType.NORMAL:
            return "hierarchical (CKM-like, small mixing)"
        else:
            return "democratic (PMNS-like, large mixing)"

    def residue_symmetry(self, shadow: ShadowType) -> str:
        """
        Describe the residue flux symmetry for a shadow.

        Args:
            shadow: Shadow type

        Returns:
            Description of residue symmetry
        """
        if shadow == ShadowType.NORMAL:
            return "asymmetric (Froggatt-Nielsen hierarchy)"
        else:
            return "symmetric (tribimaximal base)"


class ShadowDualityRelation:
    """
    Relates physical properties between normal and mirror shadows
    using the Spin(7) outer automorphism.
    """

    def __init__(self):
        """Initialize shadow duality relations."""
        self.spin7 = Spin7Automorphism()

        # Physical parameters
        self.epsilon = np.exp(-1.5)  # Froggatt-Nielsen parameter
        self.phi = (1 + np.sqrt(5)) / 2  # Golden ratio

    def normal_shadow_parameters(self) -> Dict[str, float]:
        """
        Return characteristic parameters for normal shadow.

        Normal shadow (quarks/CKM):
        - Vector-dominant
        - Asymmetric residues
        - Small mixing angles
        """
        return {
            'epsilon': self.epsilon,
            'V_us': self.epsilon,                   # Cabibbo angle
            'V_cb': 0.81 * self.epsilon**2,        # ~ 0.040
            'V_ub': 0.81 * self.epsilon**3 * 0.34, # ~ 0.004
            'delta_CP': 2 * np.arctan(1/self.phi),  # ~ 63 degrees
            'mixing_type': 'hierarchical',
        }

    def mirror_shadow_parameters(self) -> Dict[str, float]:
        """
        Return characteristic parameters for mirror shadow.

        Mirror shadow (leptons/PMNS):
        - Spinor-dominant
        - Symmetric residues
        - Large mixing angles
        """
        return {
            'sin2_theta12': 0.304,  # ~ 1/3 (tribimaximal)
            'sin2_theta23': 0.573,  # ~ 1/2 (maximal)
            'sin2_theta13': 0.022,  # Small but non-zero
            'delta_CP': np.radians(230),  # Extended cycle phase
            'mixing_type': 'democratic',
        }

    def automorphism_action_on_yukawa(
        self,
        yukawa_normal: np.ndarray
    ) -> np.ndarray:
        """
        Apply the automorphism to transform Yukawa pattern.

        The Z_2 maps hierarchical (CKM) to democratic (PMNS) structure.

        Args:
            yukawa_normal: 3x3 Yukawa matrix in normal shadow

        Returns:
            Transformed Yukawa for mirror shadow
        """
        # The transformation:
        # - Makes off-diagonal elements larger
        # - Makes diagonal less dominant

        n_gen = yukawa_normal.shape[0]

        # Democratic base
        democratic = np.ones((n_gen, n_gen)) / np.sqrt(n_gen)

        # Mix with small asymmetry from original
        mixing_factor = 0.1
        yukawa_mirror = democratic + mixing_factor * (yukawa_normal - democratic)

        return yukawa_mirror

    def compare_mixing_matrices(self) -> Dict[str, np.ndarray]:
        """
        Compare CKM and PMNS structures showing the duality.

        Returns:
            Dictionary with CKM and PMNS characteristic matrices
        """
        normal = self.normal_shadow_parameters()
        mirror = self.mirror_shadow_parameters()

        # CKM-like structure (small off-diagonal)
        eps = normal['epsilon']
        ckm_like = np.array([
            [1 - eps**2/2, eps, eps**3],
            [-eps, 1 - eps**2/2, eps**2],
            [eps**3, -eps**2, 1],
        ])

        # PMNS-like structure (large off-diagonal)
        s12 = np.sqrt(mirror['sin2_theta12'])
        s23 = np.sqrt(mirror['sin2_theta23'])
        s13 = np.sqrt(mirror['sin2_theta13'])
        c12 = np.sqrt(1 - mirror['sin2_theta12'])
        c23 = np.sqrt(1 - mirror['sin2_theta23'])
        c13 = np.sqrt(1 - mirror['sin2_theta13'])

        pmns_like = np.array([
            [c12*c13, s12*c13, s13],
            [-s12*c23, c12*c23, s23*c13],
            [s12*s23, -c12*s23, c23*c13],
        ])

        return {
            'CKM': np.abs(ckm_like),
            'PMNS': np.abs(pmns_like),
        }

    def print_duality_summary(self):
        """Print a summary of the shadow duality relation."""
        print("=" * 70)
        print(" SPIN(7) OUTER AUTOMORPHISM AND SHADOW DUALITY")
        print("=" * 70)

        print("\n1. THE Z_2 OUTER AUTOMORPHISM")
        print("-" * 40)
        print("   Out(Spin(7)) = Z_2")
        print("   sigma: 8_v <-> 8_s (vector <-> spinor)")
        print("   sigma preserves: 21 (adjoint), 1 (singlet)")

        print("\n2. SHADOW CORRESPONDENCE")
        print("-" * 40)
        print("   Normal Shadow          Mirror Shadow")
        print("   8_v dominant     <->   8_s dominant")
        print("   Quarks           <->   Sterile neutrinos")
        print("   CKM mixing       <->   PMNS mixing")
        print("   Hierarchical     <->   Democratic")
        print("   Asymmetric flux  <->   Symmetric flux")

        print("\n3. PHYSICAL PARAMETERS")
        print("-" * 40)

        normal = self.normal_shadow_parameters()
        print("\n   Normal Shadow (CKM):")
        print(f"     Cabibbo angle V_us = {normal['V_us']:.4f}")
        print(f"     V_cb = {normal['V_cb']:.4f}")
        print(f"     V_ub = {normal['V_ub']:.5f}")
        print(f"     delta_CP = {np.degrees(normal['delta_CP']):.1f} deg")

        mirror = self.mirror_shadow_parameters()
        print("\n   Mirror Shadow (PMNS):")
        print(f"     sin^2(theta_12) = {mirror['sin2_theta12']:.3f}")
        print(f"     sin^2(theta_23) = {mirror['sin2_theta23']:.3f}")
        print(f"     sin^2(theta_13) = {mirror['sin2_theta13']:.4f}")
        print(f"     delta_CP = {np.degrees(mirror['delta_CP']):.0f} deg")

        print("\n4. MIXING MATRIX COMPARISON")
        print("-" * 40)

        matrices = self.compare_mixing_matrices()

        print("\n   |V_CKM| (Normal Shadow - Hierarchical):")
        ckm = matrices['CKM']
        for row in ckm:
            print("     [" + " ".join(f"{x:.4f}" for x in row) + "]")

        print("\n   |U_PMNS| (Mirror Shadow - Democratic):")
        pmns = matrices['PMNS']
        for row in pmns:
            print("     [" + " ".join(f"{x:.4f}" for x in row) + "]")

        print("\n5. KEY INSIGHT")
        print("-" * 40)
        print("""
   The Z_2 outer automorphism of Spin(7) provides the mathematical
   foundation for why quarks and leptons have such different mixing
   patterns. The vector representation (normal shadow) confines quarks
   to G2/7D giving hierarchical CKM, while the spinor representation
   (mirror shadow) allows leptons to access the full 8D structure
   giving democratic PMNS mixing.
""")


def main():
    """Demonstrate Spin(7) automorphism and shadow duality."""
    spin7 = Spin7Automorphism()

    print("=" * 70)
    print(" SPIN(7) REPRESENTATION THEORY")
    print("=" * 70)

    print("\nSpin(7) Representations:")
    for rep in SpinorType:
        dim = spin7.dim[rep]
        print(f"  {rep.value}: dimension {dim}")

    print("\nZ_2 Outer Automorphism Action:")
    for rep in SpinorType:
        image = spin7.apply_automorphism(rep)
        print(f"  sigma({rep.value}) = {image.value}")

    print("\nG2 Branching Rules:")
    for rep in [SpinorType.VECTOR, SpinorType.SPINOR, SpinorType.ADJOINT]:
        branching = spin7.decompose_under_g2(rep)
        content = " + ".join(f"{count}x{name}" for name, count in branching.items())
        print(f"  {rep.value} -> {content}")

    print("\n" + "=" * 70)

    # Shadow duality
    duality = ShadowDualityRelation()
    duality.print_duality_summary()


if __name__ == "__main__":
    main()
