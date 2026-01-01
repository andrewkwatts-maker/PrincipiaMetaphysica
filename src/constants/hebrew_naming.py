#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Hebrew Letter Naming Conventions
================================================================

DOI: 10.5281/zenodo.18079602

This module defines the Hebrew letter naming conventions for the
fundamental geometric constants of the 288-24-4 architecture.

HEBREW LETTER SYMBOLISM:

    י (Yod) - The 288 Ancestral Roots
    --------------------------------
    Yod is the smallest letter, yet contains all others.
    The 288 roots are the ancestral basis from which all
    physical constants descend.

    Notation: Yod₁ through Yod₂₈₈ (or Y₁ - Y₂₈₈)

    ן (Nun Sofit) - The 24 Torsion Pins
    ------------------------------------
    Nun Sofit (final Nun) represents completion and descent.
    The 24 pins are the "final form" through which the 288
    roots descend into 4D spacetime.

    The 12/12 split: Shadow-A (ן₁-ן₁₂) and Shadow-B (ן₁₃-ן₂₄)

    Notation: Nun₁ through Nun₂₄ (or N₁ - N₂₄)

    ד (Dalet) - The 4 Spacetime Dimensions
    ---------------------------------------
    Dalet means "door" - the gateway from higher dimensions
    to our observable 4D spacetime.

    Notation: Dalet₁ through Dalet₄ (or D₁ - D₄)
    Represents: [t, x, y, z] or [time, space, space, space]

THE PROJECTION HIERARCHY:
    Yod (288) → Nun (24) → Dalet (4)

    288 ancestral roots project through 24 torsion pins
    into 4 spacetime dimensions.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


# ============================================================================
# HEBREW LETTER CONSTANTS
# ============================================================================

# The Hebrew letters
YOD = "י"      # Yod - 288 roots
NUN_SOFIT = "ן"  # Nun Sofit - 24 pins
DALET = "ד"    # Dalet - 4 dimensions


@dataclass
class HebrewConstant:
    """A constant with Hebrew letter notation."""
    hebrew: str
    name: str
    value: int
    description: str
    notation_range: str


# The three fundamental Hebrew constants
HEBREW_YOD = HebrewConstant(
    hebrew=YOD,
    name="Yod",
    value=288,
    description="The 288 Ancestral Roots - the primordial basis from which all constants descend",
    notation_range="Yod₁ - Yod₂₈₈ (Y₁ - Y₂₈₈)"
)

HEBREW_NUN = HebrewConstant(
    hebrew=NUN_SOFIT,
    name="Nun Sofit",
    value=24,
    description="The 24 Torsion Pins - the final form through which roots descend to 4D",
    notation_range="Nun₁ - Nun₂₄ (N₁ - N₂₄)"
)

HEBREW_DALET = HebrewConstant(
    hebrew=DALET,
    name="Dalet",
    value=4,
    description="The 4 Spacetime Dimensions - the door to observable reality",
    notation_range="Dalet₁ - Dalet₄ (D₁ - D₄)"
)


# ============================================================================
# GEOMETRIC CONSTANTS WITH HEBREW NOTATION
# ============================================================================

class GeometricConstants:
    """
    The fundamental geometric constants with Hebrew letter notation.

    The 288-24-4 Architecture:
        Yod (288) = Total ancestral roots
        Nun (24) = Torsion pins = 12 + 12 shadow split
        Dalet (4) = Spacetime dimensions
    """

    # Primary constants
    YOD_TOTAL = 288          # Total Yod (ancestral roots)
    YOD_ACTIVE = 125         # Active Yod (observable nodes)
    YOD_HIDDEN = 163         # Hidden Yod (bulk supports)

    NUN_TOTAL = 24           # Total Nun (torsion pins)
    NUN_SHADOW_A = 12        # Shadow-A pins (ן₁-ן₁₂)
    NUN_SHADOW_B = 12        # Shadow-B pins (ן₁₃-ן₂₄)

    DALET_TOTAL = 4          # Total Dalet (spacetime dimensions)
    NUN_PER_DALET = 6        # Pins per dimension (24/4 = 6)

    # Derived constants
    SO24_GENERATORS = 276    # SO(24) generators = YOD - TAX
    MANIFOLD_TAX = 12        # Tax = NUN_SHADOW_A = 12

    @classmethod
    def get_torsion_pattern(cls) -> List[int]:
        """Return the [6,6,6,6] torsion pattern (Nun per Dalet)."""
        return [cls.NUN_PER_DALET] * cls.DALET_TOTAL

    @classmethod
    def verify_closure(cls) -> Dict[str, Any]:
        """
        Verify the closure equations.

        Returns:
            Dictionary with verification results
        """
        # Structural closure: SO(24) + Nun - Tax = Yod
        structural_lhs = cls.SO24_GENERATORS + cls.NUN_TOTAL - cls.MANIFOLD_TAX
        structural_ok = structural_lhs == cls.YOD_TOTAL

        # Partition closure: Active + Hidden = Yod
        partition_lhs = cls.YOD_ACTIVE + cls.YOD_HIDDEN
        partition_ok = partition_lhs == cls.YOD_TOTAL

        # Torsion closure: Shadow-A + Shadow-B = Nun
        torsion_lhs = cls.NUN_SHADOW_A + cls.NUN_SHADOW_B
        torsion_ok = torsion_lhs == cls.NUN_TOTAL

        return {
            "structural": {
                "equation": f"SO(24) + {NUN_SOFIT} - Tax = {YOD}",
                "calculation": f"{cls.SO24_GENERATORS} + {cls.NUN_TOTAL} - {cls.MANIFOLD_TAX} = {structural_lhs}",
                "passed": structural_ok
            },
            "partition": {
                "equation": f"Active + Hidden = {YOD}",
                "calculation": f"{cls.YOD_ACTIVE} + {cls.YOD_HIDDEN} = {partition_lhs}",
                "passed": partition_ok
            },
            "torsion": {
                "equation": f"Shadow-A + Shadow-B = {NUN_SOFIT}",
                "calculation": f"{cls.NUN_SHADOW_A} + {cls.NUN_SHADOW_B} = {torsion_lhs}",
                "passed": torsion_ok
            },
            "all_passed": structural_ok and partition_ok and torsion_ok
        }


# ============================================================================
# ROOT NOTATION HELPERS
# ============================================================================

def yod_notation(index: int) -> str:
    """
    Get Yod notation for a root index (1-288).

    Args:
        index: Root index (1 to 288)

    Returns:
        String like "Yod₁" or "Y₁"
    """
    if not 1 <= index <= 288:
        raise ValueError(f"Yod index must be 1-288, got {index}")
    return f"Yod₍{index}₎"


def nun_notation(index: int) -> str:
    """
    Get Nun notation for a pin index (1-24).

    Args:
        index: Pin index (1 to 24)

    Returns:
        String like "Nun₁" or "N₁"
    """
    if not 1 <= index <= 24:
        raise ValueError(f"Nun index must be 1-24, got {index}")
    return f"Nun₍{index}₎"


def dalet_notation(index: int) -> str:
    """
    Get Dalet notation for a dimension index (1-4).

    Args:
        index: Dimension index (1 to 4)

    Returns:
        String like "Dalet₁" or "D₁"
    """
    if not 1 <= index <= 4:
        raise ValueError(f"Dalet index must be 1-4, got {index}")
    dim_names = ["t", "x", "y", "z"]
    return f"Dalet₍{index}₎ ({dim_names[index-1]})"


def get_shadow_designation(pin_index: int) -> str:
    """
    Get shadow designation for a pin.

    Pins 1-12 are Shadow-A (ן₁-ן₁₂)
    Pins 13-24 are Shadow-B (ן₁₃-ן₂₄)

    Args:
        pin_index: Pin index (1 to 24)

    Returns:
        "Shadow-A" or "Shadow-B"
    """
    if not 1 <= pin_index <= 24:
        raise ValueError(f"Pin index must be 1-24, got {pin_index}")
    return "Shadow-A" if pin_index <= 12 else "Shadow-B"


# ============================================================================
# SUMMARY DISPLAY
# ============================================================================

def print_hebrew_summary():
    """Print a summary of the Hebrew letter naming conventions."""
    print("=" * 70)
    print("PRINCIPIA METAPHYSICA v16.2 - Hebrew Letter Naming Conventions")
    print("=" * 70)

    print(f"\n{YOD} (Yod) - The 288 Ancestral Roots")
    print("-" * 40)
    print(f"  Total: {GeometricConstants.YOD_TOTAL}")
    print(f"  Active (observable): {GeometricConstants.YOD_ACTIVE}")
    print(f"  Hidden (bulk supports): {GeometricConstants.YOD_HIDDEN}")
    print(f"  Notation: Yod₁ - Yod₂₈₈")

    print(f"\n{NUN_SOFIT} (Nun Sofit) - The 24 Torsion Pins")
    print("-" * 40)
    print(f"  Total: {GeometricConstants.NUN_TOTAL}")
    print(f"  Shadow-A: {GeometricConstants.NUN_SHADOW_A} (Nun₁ - Nun₁₂)")
    print(f"  Shadow-B: {GeometricConstants.NUN_SHADOW_B} (Nun₁₃ - Nun₂₄)")
    print(f"  Notation: Nun₁ - Nun₂₄")

    print(f"\n{DALET} (Dalet) - The 4 Spacetime Dimensions")
    print("-" * 40)
    print(f"  Total: {GeometricConstants.DALET_TOTAL}")
    print(f"  Pins per dimension: {GeometricConstants.NUN_PER_DALET}")
    print(f"  Pattern: {GeometricConstants.get_torsion_pattern()}")
    print(f"  Notation: Dalet₁ (t), Dalet₂ (x), Dalet₃ (y), Dalet₄ (z)")

    print("\n" + "=" * 70)
    print("PROJECTION HIERARCHY")
    print("-" * 70)
    print(f"  {YOD} (288) → {NUN_SOFIT} (24) → {DALET} (4)")
    print("  288 ancestral roots → 24 torsion pins → 4 spacetime dimensions")

    print("\n" + "=" * 70)
    print("CLOSURE VERIFICATION")
    print("-" * 70)
    closure = GeometricConstants.verify_closure()
    for name, data in closure.items():
        if name != "all_passed":
            status = "✓" if data["passed"] else "✗"
            print(f"  {status} {data['equation']}: {data['calculation']}")
    print(f"\n  All Closures: {'VERIFIED' if closure['all_passed'] else 'FAILED'}")
    print("=" * 70)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print_hebrew_summary()
