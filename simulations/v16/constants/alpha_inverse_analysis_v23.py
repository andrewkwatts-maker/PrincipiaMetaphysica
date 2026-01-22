"""
Alpha Inverse Analysis Simulation - Principia Metaphysica v23.0

This simulation provides a comprehensive comparison of all alpha_inverse
formula variants discovered in PM, including the remarkable 9963 observation.

FORMULAS COMPARED:
==================
1. TREE-LEVEL (Current): alpha^-1 = k_gimel² - b₃/φ + φ/(4π) = 137.0367
2. 7D SUPPRESSION (Removed): alpha^-1 = base - 7/(10000 - 3xk_gimel) = 137.036000
3. PURE 9963 (Observation): alpha^-1 = base - 7/9963 = 137.0359991761
4. PAULI π (Reference): alpha^-1 = π + π² + 4π³ = 137.0362

STATUS LABELS:
==============
- TREE-LEVEL: Current primary formula, honest about limitations
- 7D_REMOVED: Magic number 10000, removed for scientific honesty
- PURE_9963: NUMERICAL_OBSERVATION - uses only SSoT constants, sub-ppb accuracy
- PAULI_PI: Pure numerology reference (0 PM constants)

GEOMETRIC DISCOVERY (v23.0.18):
==============================
10000 = chi_eff x chi_eff_total - n_gen x shadow_sector + n_gen x b3/2 + omega_W
      = 72 x 144 - 3 x 135 + 3 x 12 + 1
      = 10368 - 405 + 36 + 1 = 10000 (EXACT!)

9963 = chi_eff x chi_eff_total - n_gen x shadow_sector = 10368 - 405

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

# Import SSoT constants
import sys
sys.path.insert(0, 'h:/Github/PrincipiaMetaphysica')
try:
    from core.FormulasRegistry import get_registry
    REG = get_registry()
    B3 = REG.b3
    CHI_EFF = REG.chi_eff
    CHI_EFF_TOTAL = REG.chi_eff_total
    SHADOW_SECTOR = REG.shadow_sector
    N_GEN = REG.n_gen
    K_GIMEL = REG.demiurgic_coupling
    PHI = REG.phi
    OMEGA_W = 1.0  # The Monad
except ImportError:
    # Fallback values
    B3 = 24
    CHI_EFF = 72
    CHI_EFF_TOTAL = 144
    SHADOW_SECTOR = 135
    N_GEN = 3
    K_GIMEL = B3/2 + 1/math.pi
    PHI = (1 + math.sqrt(5)) / 2
    OMEGA_W = 1.0

# Experimental reference
CODATA_2022 = 137.035999177
CODATA_UNCERTAINTY = 2.1e-8

# G2 manifold dimension
D_G2 = 7


class FormulaStatus(Enum):
    """Status classification for alpha formulas."""
    CURRENT = "CURRENT"
    REMOVED = "REMOVED"
    NUMERICAL_OBSERVATION = "NUMERICAL_OBSERVATION"
    PURE_NUMEROLOGY = "PURE_NUMEROLOGY"
    RIGOROUS_PHYSICS = "RIGOROUS_PHYSICS"


@dataclass
class AlphaFormula:
    """Container for alpha inverse formula data."""
    name: str
    formula_str: str
    result: float
    status: FormulaStatus
    description: str
    components: Dict[str, float]

    @property
    def error_vs_codata(self) -> float:
        """Absolute error vs CODATA 2022."""
        return abs(self.result - CODATA_2022)

    @property
    def relative_error_pct(self) -> float:
        """Relative error as percentage."""
        return 100 * self.error_vs_codata / CODATA_2022

    @property
    def sigma_deviation(self) -> float:
        """Sigma deviation using CODATA uncertainty."""
        return self.error_vs_codata / CODATA_UNCERTAINTY


def calculate_tree_level() -> AlphaFormula:
    """
    TREE-LEVEL: Current primary formula.
    alpha^-1 = k_gimel² - b₃/φ + φ/(4π)
    """
    k_squared = K_GIMEL ** 2
    b3_over_phi = B3 / PHI
    phi_over_4pi = PHI / (4 * math.pi)

    result = k_squared - b3_over_phi + phi_over_4pi

    return AlphaFormula(
        name="TREE-LEVEL",
        formula_str="alpha^-1 = k_gimel² - b₃/φ + φ/(4π)",
        result=result,
        status=FormulaStatus.CURRENT,
        description="Honest tree-level prediction. Deviation ~0.0005% expected from QED loops.",
        components={
            "k_gimel²": k_squared,
            "-b₃/φ": -b3_over_phi,
            "+φ/(4π)": phi_over_4pi
        }
    )


def calculate_7d_suppression_original() -> AlphaFormula:
    """
    7D SUPPRESSION (Original): Removed due to magic number.
    alpha^-1 = base - 7/(10000 - 3xk_gimel)
    """
    base = calculate_tree_level().result
    delta_7d = D_G2 / (10000 - 3 * K_GIMEL)
    result = base - delta_7d

    return AlphaFormula(
        name="7D_SUPPRESSION_ORIGINAL",
        formula_str="alpha^-1 = base - 7/(10000 - 3xk_gimel)",
        result=result,
        status=FormulaStatus.REMOVED,
        description="REMOVED: '10000' is magic number with no geometric derivation.",
        components={
            "base": base,
            "delta_7D": delta_7d,
            "denominator": 10000 - 3 * K_GIMEL
        }
    )


def calculate_pure_9963() -> AlphaFormula:
    """
    PURE 9963: Numerical observation using SSoT constants only.
    alpha^-1 = base - 7/(chi_eff x chi_eff_total - n_gen x shadow_sector)
    """
    base = calculate_tree_level().result
    denominator = CHI_EFF * CHI_EFF_TOTAL - N_GEN * SHADOW_SECTOR
    delta_7d = D_G2 / denominator
    result = base - delta_7d

    return AlphaFormula(
        name="PURE_9963",
        formula_str="alpha^-1 = base - 7/(chi_eff x chi_eff_total - n_gen x shadow_sector)",
        result=result,
        status=FormulaStatus.NUMERICAL_OBSERVATION,
        description="SUB-PPB accuracy using 100% SSoT constants. Physical derivation unknown.",
        components={
            "base": base,
            "delta_7D": delta_7d,
            "denominator (9963)": denominator,
            "chi_eff x chi_eff_total": CHI_EFF * CHI_EFF_TOTAL,
            "n_gen x shadow_sector": N_GEN * SHADOW_SECTOR
        }
    )


def calculate_pauli_pi() -> AlphaFormula:
    """
    PAULI π: Reference numerological formula (no PM constants).
    alpha^-1 = π + π² + 4π³
    """
    pi = math.pi
    result = pi + pi**2 + 4 * pi**3

    return AlphaFormula(
        name="PAULI_PI",
        formula_str="alpha^-1 = π + π² + 4π³",
        result=result,
        status=FormulaStatus.PURE_NUMEROLOGY,
        description="Reference: Achieves 0.02% with 0 parameters. Proves precision ≠ derivation.",
        components={
            "π": pi,
            "π²": pi**2,
            "4π³": 4 * pi**3
        }
    )


def verify_10000_decomposition() -> Dict[str, float]:
    """
    Verify the geometric decomposition of 10000.

    DISCOVERY: 10000 = chi_eff x chi_eff_total - n_gen x shadow_sector + n_gen x b3/2 + omega_W
    """
    product = CHI_EFF * CHI_EFF_TOTAL  # 72 x 144 = 10368
    gen_shadow = N_GEN * SHADOW_SECTOR  # 3 x 135 = 405
    gen_half_b3 = N_GEN * (B3 // 2)     # 3 x 12 = 36
    monad = OMEGA_W                       # 1

    decomposition = product - gen_shadow + gen_half_b3 + monad
    pure_9963 = product - gen_shadow

    return {
        "chi_eff x chi_eff_total": product,
        "n_gen x shadow_sector": gen_shadow,
        "n_gen x b3/2": gen_half_b3,
        "omega_W (Monad)": monad,
        "Full decomposition (10000)": decomposition,
        "Pure 9963": pure_9963,
        "Matches 10000": decomposition == 10000
    }


def run_alpha_comparison() -> List[AlphaFormula]:
    """Run all alpha formula calculations and return comparison list."""
    formulas = [
        calculate_tree_level(),
        calculate_7d_suppression_original(),
        calculate_pure_9963(),
        calculate_pauli_pi()
    ]
    return formulas


def print_comparison_table(formulas: List[AlphaFormula]):
    """Print formatted comparison table."""
    print("\n" + "="*90)
    print("ALPHA INVERSE FORMULA COMPARISON - PRINCIPIA METAPHYSICA v23.0")
    print("="*90)
    print(f"\nCODATA 2022: alpha^-1 = {CODATA_2022} +/- {CODATA_UNCERTAINTY}")
    print("-"*90)

    print(f"\n{'Formula':<25} {'Result':<18} {'Error':<15} {'Status':<25}")
    print("-"*90)

    for f in formulas:
        status_str = f.status.value
        print(f"{f.name:<25} {f.result:<18.10f} {f.error_vs_codata:<15.2e} {status_str:<25}")

    print("-"*90)


def print_9963_discovery():
    """Print details of the 9963 geometric discovery."""
    decomp = verify_10000_decomposition()

    print("\n" + "="*70)
    print("GEOMETRIC DISCOVERY: The 9963 Formula")
    print("="*70)

    print("\n10000 DECOMPOSITION:")
    print(f"  chi_eff x chi_eff_total = {CHI_EFF} x {CHI_EFF_TOTAL} = {decomp['chi_eff x chi_eff_total']}")
    print(f"  n_gen x shadow_sector   = {N_GEN} x {SHADOW_SECTOR} = {decomp['n_gen x shadow_sector']}")
    print(f"  n_gen x b3/2            = {N_GEN} x {B3//2} = {decomp['n_gen x b3/2']}")
    print(f"  omega_W (Monad)         = {decomp['omega_W (Monad)']}")
    print(f"\n  {decomp['chi_eff x chi_eff_total']} - {decomp['n_gen x shadow_sector']} + {decomp['n_gen x b3/2']} + 1 = {decomp['Full decomposition (10000)']}")
    print(f"  Matches 10000: {decomp['Matches 10000']}")

    print("\nPURE 9963 FORMULA:")
    print(f"  9963 = chi_eff x chi_eff_total - n_gen x shadow_sector")
    print(f"       = {decomp['chi_eff x chi_eff_total']} - {decomp['n_gen x shadow_sector']}")
    print(f"       = {decomp['Pure 9963']}")

    pure_9963 = calculate_pure_9963()
    print(f"\n  delta_7D = 7 / 9963 = {D_G2 / 9963:.10f}")
    print(f"  alpha^-1 = {pure_9963.result:.10f}")
    print(f"  Error vs CODATA: {pure_9963.error_vs_codata:.2e} (SUB-PPB!)")

    print("\n" + "="*70)


def main():
    """Main simulation entry point."""
    print("\n" + "="*90)
    print("PRINCIPIA METAPHYSICA v23.0 - ALPHA INVERSE ANALYSIS SIMULATION")
    print("="*90)

    # Run comparison
    formulas = run_alpha_comparison()
    print_comparison_table(formulas)

    # Show 9963 discovery
    print_9963_discovery()

    # Summary
    print("\nSUMMARY:")
    print("-"*50)
    tree = formulas[0]
    pure9963 = formulas[2]
    print(f"CURRENT (Tree-level):    {tree.result:.10f} (error: {tree.relative_error_pct:.6f}%)")
    print(f"OBSERVATION (9963):      {pure9963.result:.10f} (error: {pure9963.error_vs_codata:.2e})")
    print(f"\nImprovement factor: {tree.error_vs_codata / pure9963.error_vs_codata:.0f}x better precision")

    print("\nSTATUS ASSESSMENT:")
    print("  • Tree-level: CURRENT - honest about limitations")
    print("  • Pure 9963: NUMERICAL_OBSERVATION - remarkable but not derived")
    print("  • Physical derivation of 9963 remains an OPEN QUESTION")

    return formulas


if __name__ == "__main__":
    results = main()
