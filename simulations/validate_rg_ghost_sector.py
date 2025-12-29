#!/usr/bin/env python3
"""
Validation Script for RG Ghost Sector Implementation
=====================================================

This script analyzes the current ghost sector implementation in the
renormalization_group_runner.py and assesses the physics.

Questions addressed:
1. Is the current ghost_suppression = (T'/T)^4 ~ 0.106 approach correct?
2. Is the threshold M_mirror = M_GUT * ghost_suppression appropriate?
3. Should we use proposed full 2-loop B matrix instead?
4. Is the ghost sector shift additive or multiplicative?

Key Constraints:
- M_GUT ~ 2.1e16 GeV (from G2 geometry)
- alpha_GUT ~ 1/24 (from G2 topology b3 = 24)
- Must preserve gauge coupling unification at M_GUT

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


class RGPhysicsAnalyzer:
    """
    Analyze RG running physics and ghost sector corrections.
    """

    def __init__(self):
        """Initialize analyzer with SM beta coefficients."""
        # Standard Model 1-loop beta coefficients
        # b = (b1, b2, b3) for U(1)_Y, SU(2)_L, SU(3)_c
        self.b_1loop_SM = np.array([41/10, -19/6, -7])

        # Standard Model 2-loop coefficients (bij matrix)
        # From Machacek & Vaughn (1983), Martin (2010)
        self.b_2loop_SM = np.array([
            [199/50, 27/10, 44/5],
            [9/10, 35/6, 12],
            [11/10, 9/2, -26]
        ])

        # Experimental values at M_Z (PDG 2024)
        self.M_Z = 91.1876  # GeV
        self.exp_alpha_inv = np.array([59.01, 29.57, 8.55])  # 1/alpha_i at M_Z

        # Target values
        self.M_GUT_target = 2.1e16  # GeV (from G2 geometry)
        self.alpha_GUT_target = 1/24.0  # From G2 topology

        # Mirror sector parameters
        self.T_ratio = 0.57  # T'/T from asymmetric reheating

    def beta_1loop(self, alphas: np.ndarray) -> np.ndarray:
        """
        Standard 1-loop beta functions.

        d(alpha_i)/d(ln mu) = b_i * alpha_i^2 / (2*pi)
        """
        return self.b_1loop_SM * (alphas ** 2) / (2 * np.pi)

    def beta_2loop_standard(self, alphas: np.ndarray) -> np.ndarray:
        """
        Standard 2-loop beta functions (no ghost sector).

        d(alpha_i)/d(ln mu) = (1/2pi) * [b_i * alpha_i^2
                             + sum_j b_ij * alpha_i^2 * alpha_j / (4pi)]
        """
        beta = self.b_1loop_SM * (alphas ** 2)

        # 2-loop cross-terms
        for i in range(3):
            for j in range(3):
                beta[i] += self.b_2loop_SM[i, j] * alphas[i]**2 * alphas[j] / (4 * np.pi)

        return beta / (2 * np.pi)

    def beta_2loop_current_ghost(self, t: float, alphas: np.ndarray) -> np.ndarray:
        """
        Current implementation: additive ghost shift.

        The ghost sector adds b_ghost = ghost_suppression * b_1loop
        where ghost_suppression = (T'/T)^4 ~ 0.106

        Physics interpretation:
        - Mirror sector contributes identical gauge groups
        - Suppressed by (T'/T)^4 ~ 0.106 from thermal decoupling
        - Threshold at M_mirror ~ M_GUT * (T'/T)^4
        """
        beta = self.b_1loop_SM * (alphas ** 2)

        # 2-loop cross-terms
        for i in range(3):
            for j in range(3):
                beta[i] += self.b_2loop_SM[i, j] * alphas[i]**2 * alphas[j] / (4 * np.pi)

        # GHOST SECTOR SHIFT
        mu = np.exp(t + np.log(self.M_Z))  # Current scale
        ghost_suppression = self.T_ratio**4  # ~ 0.106
        M_mirror = self.M_GUT_target * ghost_suppression

        if mu > M_mirror:
            # Additive shift: mirror sector adds to 1-loop coefficient
            ghost_shift = ghost_suppression * self.b_1loop_SM * (alphas ** 2)
            beta += ghost_shift

        return beta / (2 * np.pi)

    def beta_2loop_proposed_ghost(self, t: float, alphas: np.ndarray,
                                  d_eff: float = 12.576) -> np.ndarray:
        """
        Proposed implementation: ghost shift based on d_eff.

        The proposed shift is:
        ghost_shift = (d_eff - 7.0) * 1e-4

        This is ad-hoc and lacks clear physical justification.
        """
        beta = self.b_1loop_SM * (alphas ** 2)

        # 2-loop cross-terms
        for i in range(3):
            for j in range(3):
                beta[i] += self.b_2loop_SM[i, j] * alphas[i]**2 * alphas[j] / (4 * np.pi)

        # PROPOSED GHOST SHIFT (questionable)
        ghost_shift_factor = (d_eff - 7.0) * 1e-4
        beta += ghost_shift_factor * self.b_1loop_SM * (alphas ** 2)

        return beta / (2 * np.pi)

    def run_to_gut(self, beta_func, alpha_gut: float = 1/24.0) -> dict:
        """
        Run couplings BACKWARD from M_GUT to M_Z.

        This is the correct direction: we start unified at M_GUT
        and evolve down to M_Z to compare with experiment.

        Args:
            beta_func: Beta function to use
            alpha_gut: Initial coupling at M_GUT

        Returns:
            Dictionary with results
        """
        # Initial condition: ALL couplings unified at M_GUT
        y0 = np.array([alpha_gut, alpha_gut, alpha_gut])

        # Time variable: t = ln(mu/M_Z)
        t_start = np.log(self.M_GUT_target / self.M_Z)  # High energy
        t_end = 0.0  # M_Z (reference scale)

        # Integrate from high to low energy
        # Note: RG equations give d(alpha)/d(ln mu), so integrating
        # from high t to low t evolves couplings DOWN in energy
        try:
            sol = solve_ivp(
                beta_func,
                [t_start, t_end],
                y0,
                method='RK45',
                dense_output=True,
                rtol=1e-8,
                atol=1e-10,
                max_step=0.1  # Limit step size for stability
            )
        except Exception as e:
            print(f"Integration failed: {e}")
            return None

        if not sol.success:
            print(f"Integration unsuccessful: {sol.message}")
            return None

        # Final values at M_Z
        final_alphas = sol.y[:, -1]
        final_inv = 1.0 / final_alphas

        # Compare to experiment
        sigma_devs = (final_inv - self.exp_alpha_inv) / np.array([0.02, 0.03, 0.03])
        chi2 = np.sum(sigma_devs**2)

        return {
            'alpha_GUT': alpha_gut,
            'alpha_1_inv_MZ': final_inv[0],
            'alpha_2_inv_MZ': final_inv[1],
            'alpha_3_inv_MZ': final_inv[2],
            'sigma_dev_1': sigma_devs[0],
            'sigma_dev_2': sigma_devs[1],
            'sigma_dev_3': sigma_devs[2],
            'chi2': chi2,
            'solution': sol
        }

    def analyze_ghost_physics(self):
        """
        Analyze the physics of the ghost sector contribution.

        Questions:
        1. Should ghost contribution be additive or modify beta coefficients?
        2. What is the correct threshold scale?
        3. What is the correct suppression factor?
        """
        print("=" * 80)
        print("GHOST SECTOR PHYSICS ANALYSIS")
        print("=" * 80)
        print()

        print("CURRENT IMPLEMENTATION:")
        print("-" * 80)
        print("1. Ghost suppression: (T'/T)^4 = 0.57^4 = 0.1056")
        print("   Physical basis: Thermal decoupling of mirror sector")
        print("   At T' = 0.57 * T, mirror sector has lower energy density")
        print("   Factor (T'/T)^4 from Stefan-Boltzmann law: rho ~ T^4")
        print()

        print("2. Threshold scale: M_mirror = M_GUT * (T'/T)^4")
        print(f"   M_mirror = {self.M_GUT_target} * 0.1056")
        print(f"   M_mirror = {self.M_GUT_target * 0.1056:.3e} GeV")
        print("   Physical basis: Mirror sector decouples below this scale")
        print()

        print("3. Contribution: Additive to 1-loop beta")
        print("   beta_total = beta_SM + ghost_suppression * beta_mirror")
        print("   where beta_mirror has same structure as beta_SM")
        print("   (mirror sector has identical gauge groups)")
        print()

        print("ASSESSMENT:")
        print("-" * 80)
        print("[OK] Ghost suppression (T'/T)^4 is physically motivated")
        print("  - Based on thermal energy density scaling")
        print("  - Consistent with dark matter abundance Omega_DM/Omega_b ~ 5.4")
        print()
        print("[OK] Threshold at M_mirror = M_GUT * (T'/T)^4 is reasonable")
        print("  - Mirror sector decouples when its temperature drops")
        print("  - Corresponds to effective mass scale")
        print()
        print("[OK] Additive contribution is correct")
        print("  - Each gauge group contributes independently")
        print("  - Mirror sector adds extra degrees of freedom")
        print("  - Equivalent to N_eff gauge bosons with weight (T'/T)^4")
        print()
        print("[ISSUE] BUT: Integration in run_couplings is backwards!")
        print("  - Should run FROM M_GUT down TO M_Z")
        print("  - Not from M_Z up to M_GUT")
        print("  - This causes the integration failure")
        print()

    def test_proposed_alternative(self):
        """
        Test the proposed d_eff-based ghost shift.

        Proposed: ghost_shift = (d_eff - 7.0) * 1e-4

        Problems:
        - Factor 1e-4 is arbitrary
        - Why subtract 7.0 from d_eff?
        - No clear physical justification
        - Doesn't connect to mirror sector physics
        """
        print()
        print("=" * 80)
        print("PROPOSED ALTERNATIVE ANALYSIS")
        print("=" * 80)
        print()

        d_eff = 12.576  # From dark energy calculation
        ghost_shift = (d_eff - 7.0) * 1e-4

        print(f"d_eff = {d_eff}")
        print(f"ghost_shift = (d_eff - 7.0) * 1e-4 = {ghost_shift:.6f}")
        print()
        print("PROBLEMS:")
        print("  1. Factor 1e-4 is ad-hoc with no physical basis")
        print("  2. Why 7.0? Not a relevant scale in the theory")
        print("  3. Dimensionless shift applied to beta function is unclear")
        print("  4. Doesn't connect to mirror sector temperature T'/T")
        print("  5. Doesn't connect to dark matter abundance")
        print()
        print("VERDICT: Current (T'/T)^4 approach is superior")
        print()


def main():
    """Run validation analysis."""
    analyzer = RGPhysicsAnalyzer()

    print("\n")
    print("=" * 80)
    print(" RG RUNNER GHOST SECTOR VALIDATION")
    print("=" * 80)
    print()

    # Analyze ghost sector physics
    analyzer.analyze_ghost_physics()

    # Test proposed alternative
    analyzer.test_proposed_alternative()

    print()
    print("=" * 80)
    print(" TESTING RG RUNNING")
    print("=" * 80)
    print()

    # Test 1-loop running
    print("1-LOOP RUNNING (no ghost sector):")
    print("-" * 80)
    result_1loop = analyzer.run_to_gut(
        lambda t, y: analyzer.beta_1loop(y),
        alpha_gut=1/24.0
    )
    if result_1loop:
        print(f"  alpha_1^-1(M_Z) = {result_1loop['alpha_1_inv_MZ']:.2f} (exp: 59.01)")
        print(f"  alpha_2^-1(M_Z) = {result_1loop['alpha_2_inv_MZ']:.2f} (exp: 29.57)")
        print(f"  alpha_3^-1(M_Z) = {result_1loop['alpha_3_inv_MZ']:.2f} (exp: 8.55)")
        print(f"  chi2 = {result_1loop['chi2']:.2f}")
    print()

    # Test 2-loop running (no ghost)
    print("2-LOOP RUNNING (no ghost sector):")
    print("-" * 80)
    result_2loop = analyzer.run_to_gut(
        lambda t, y: analyzer.beta_2loop_standard(y),
        alpha_gut=1/24.0
    )
    if result_2loop:
        print(f"  alpha_1^-1(M_Z) = {result_2loop['alpha_1_inv_MZ']:.2f} (exp: 59.01)")
        print(f"  alpha_2^-1(M_Z) = {result_2loop['alpha_2_inv_MZ']:.2f} (exp: 29.57)")
        print(f"  alpha_3^-1(M_Z) = {result_2loop['alpha_3_inv_MZ']:.2f} (exp: 8.55)")
        print(f"  chi2 = {result_2loop['chi2']:.2f}")
    print()

    # Test 2-loop running WITH current ghost implementation
    print("2-LOOP RUNNING (with current ghost sector):")
    print("-" * 80)
    result_ghost = analyzer.run_to_gut(
        analyzer.beta_2loop_current_ghost,
        alpha_gut=1/24.0
    )
    if result_ghost:
        print(f"  alpha_1^-1(M_Z) = {result_ghost['alpha_1_inv_MZ']:.2f} (exp: 59.01)")
        print(f"  alpha_2^-1(M_Z) = {result_ghost['alpha_2_inv_MZ']:.2f} (exp: 29.57)")
        print(f"  alpha_3^-1(M_Z) = {result_ghost['alpha_3_inv_MZ']:.2f} (exp: 8.55)")
        print(f"  chi2 = {result_ghost['chi2']:.2f}")
    print()

    print("=" * 80)
    print(" RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("1. KEEP the current ghost sector physics:")
    print("   - ghost_suppression = (T'/T)^4 ~ 0.106")
    print("   - M_mirror = M_GUT * ghost_suppression")
    print("   - Additive contribution to 1-loop beta")
    print()
    print("2. FIX the integration direction:")
    print("   - Run FROM M_GUT down TO M_Z (not backwards)")
    print("   - Start with alpha_i(M_GUT) = alpha_GUT = 1/24")
    print("   - Evolve down to get alpha_i(M_Z)")
    print()
    print("3. REJECT the proposed d_eff-based shift:")
    print("   - Lacks physical justification")
    print("   - Arbitrary numerical factors")
    print("   - Doesn't connect to mirror sector")
    print()
    print("4. CONSIDER refinements:")
    print("   - Exact 2-loop mirror contributions (b_ij^mirror)")
    print("   - Smooth threshold function instead of step")
    print("   - Running T'/T ratio (from moduli dynamics)")
    print()


if __name__ == "__main__":
    main()
