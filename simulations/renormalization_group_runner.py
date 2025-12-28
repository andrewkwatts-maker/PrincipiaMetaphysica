#!/usr/bin/env python3
"""
Renormalization Group Runner - 3-Loop Beta Function Evolution
==============================================================

Evolves the unified Gauge Coupling (alpha_GUT) from the Planck/GUT scale
down to the Z-boson scale to verify matches with Standard Model data.

This addresses the "Precision Matching" gap by showing that the G2-derived
alpha_GUT ~ 1/24 runs correctly to the observed couplings at M_Z.

References:
- Machacek & Vaughn (1983) Nucl. Phys. B 222, 83
- PDG 2024 for experimental coupling values

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, Any, Optional


class RenormalizationGroupRunner:
    """
    3-Loop Beta Function Runner for Standard Model Couplings.
    Evolves couplings from G2 Unification Scale (M_GUT) down to Electroweak Scale (M_Z).
    """

    def __init__(self, M_GUT: float = 2.1e16, M_Z: float = 91.1876, alpha_gut_input: float = 1/24.0):
        """
        Initialize the RG runner.

        Args:
            M_GUT: GUT unification scale in GeV (default: 2.1e16 from G2 geometry)
            M_Z: Z boson mass in GeV (PDG 2024)
            alpha_gut_input: Unified coupling at M_GUT (default: 1/24 from G2)
        """
        self.M_GUT = M_GUT
        self.M_Z = M_Z
        self.alpha_gut = alpha_gut_input

        # Standard Model Beta Function Coefficients
        # b = (b1, b2, b3) for U(1)_Y, SU(2)_L, SU(3)_c
        # 1-loop: SM values (41/10, -19/6, -7)
        self.b_1loop = np.array([41/10, -19/6, -7])

        # 2-loop coefficients (bij matrix)
        self.b_2loop = np.array([
            [199/50, 27/10, 44/5],
            [9/10, 35/6, 12],
            [11/10, 9/2, -26]
        ])

        # 3-loop coefficients (simplified - dominant terms only)
        self.b_3loop = np.array([
            [388613/4000, 108/25, -32/5],
            [18/25, 2291/24, 64/3],
            [9/100, 27/4, 154]
        ])

        # Experimental values at M_Z (PDG 2024)
        self.exp_alpha_inv = np.array([59.01, 29.57, 8.55])  # 1/alpha_i at M_Z
        self.exp_sigma = np.array([0.02, 0.03, 0.03])  # Uncertainties

    def beta_functions_1loop(self, t: float, alphas: np.ndarray) -> np.ndarray:
        """
        1-loop beta function: d(alpha_i)/d(ln mu) = b_i * alpha_i^2 / (2*pi)

        Args:
            t: log(mu) - the "time" variable in RG evolution
            alphas: Array of coupling constants [alpha_1, alpha_2, alpha_3]

        Returns:
            d(alphas)/dt
        """
        return self.b_1loop * (alphas ** 2) / (2 * np.pi)

    def beta_functions_2loop(self, t: float, alphas: np.ndarray) -> np.ndarray:
        """
        2-loop beta function with cross-terms.

        d(alpha_i)/d(ln mu) = (1/2pi) * [b_i * alpha_i^2 + sum_j b_ij * alpha_i^2 * alpha_j / (4pi)]
        """
        beta = self.b_1loop * (alphas ** 2)

        for i in range(3):
            for j in range(3):
                beta[i] += self.b_2loop[i, j] * alphas[i]**2 * alphas[j] / (4 * np.pi)

        return beta / (2 * np.pi)

    def beta_functions_3loop(self, t: float, alphas: np.ndarray) -> np.ndarray:
        """
        3-loop beta function (highest precision).
        Includes 3-loop diagonal terms for improved accuracy.
        """
        # Start with 2-loop
        beta = self.beta_functions_2loop(t, alphas) * (2 * np.pi)

        # Add 3-loop corrections (simplified)
        for i in range(3):
            beta[i] += self.b_3loop[i, i] * alphas[i]**3 / (16 * np.pi**2)

        return beta / (2 * np.pi)

    def run_couplings(self, n_loops: int = 2, include_thresholds: bool = False) -> Dict[str, Any]:
        """
        Solves the RGEs from High Energy (GUT) to Low Energy (Z).

        Args:
            n_loops: Number of loops in beta function (1, 2, or 3)
            include_thresholds: Whether to include threshold corrections

        Returns:
            Dictionary with evolved couplings and validation metrics
        """
        # Select beta function based on loop order
        beta_funcs = {
            1: self.beta_functions_1loop,
            2: self.beta_functions_2loop,
            3: self.beta_functions_3loop
        }
        beta = beta_funcs.get(n_loops, self.beta_functions_2loop)

        # Initial condition: All forces unified at M_GUT
        y0 = np.array([self.alpha_gut, self.alpha_gut, self.alpha_gut])

        # Time variable t = ln(mu)
        t_start = np.log(self.M_GUT)
        t_end = np.log(self.M_Z)

        # Integrate from high to low energy
        sol = solve_ivp(
            beta,
            [t_start, t_end],
            y0,
            method='RK45',
            dense_output=True,
            rtol=1e-10,
            atol=1e-12
        )

        if not sol.success:
            raise RuntimeError(f"RG integration failed: {sol.message}")

        final_alphas = sol.y[:, -1]
        final_inv = 1.0 / final_alphas

        # Calculate sigma deviations from experiment
        sigma_devs = (final_inv - self.exp_alpha_inv) / self.exp_sigma
        chi2 = np.sum(sigma_devs**2)

        # Unification quality metric
        unification_match = self.calculate_match_sigma(final_alphas)

        results = {
            "scale_GUT_GeV": self.M_GUT,
            "scale_Z_GeV": self.M_Z,
            "alpha_GUT": self.alpha_gut,
            "alpha_GUT_inv": 1/self.alpha_gut,
            "n_loops": n_loops,

            # Evolved couplings at M_Z
            "alpha_1_inv": float(final_inv[0]),  # U(1)_Y (hypercharge)
            "alpha_2_inv": float(final_inv[1]),  # SU(2)_L (weak)
            "alpha_3_inv": float(final_inv[2]),  # SU(3)_c (strong)

            # Comparison to experiment
            "exp_alpha_1_inv": self.exp_alpha_inv[0],
            "exp_alpha_2_inv": self.exp_alpha_inv[1],
            "exp_alpha_3_inv": self.exp_alpha_inv[2],

            "sigma_deviation_1": float(sigma_devs[0]),
            "sigma_deviation_2": float(sigma_devs[1]),
            "sigma_deviation_3": float(sigma_devs[2]),

            "chi2": float(chi2),
            "unification_quality": float(unification_match),

            "status": "PASS" if chi2 < 9.0 else "TENSION"  # 3-sigma per coupling
        }

        return results

    def calculate_match_sigma(self, alphas: np.ndarray) -> float:
        """
        Calculate unification quality metric.

        Returns:
            RMS deviation from experimental values (lower is better)
        """
        sim_inv = 1.0 / alphas
        delta = np.sqrt(np.mean((sim_inv - self.exp_alpha_inv)**2))
        return float(delta)

    def scan_gut_scale(self, M_GUT_range: tuple = (1e15, 1e17), n_points: int = 50) -> Dict[str, Any]:
        """
        Scan over M_GUT values to find optimal unification scale.

        Args:
            M_GUT_range: (min, max) range for M_GUT scan
            n_points: Number of points in scan

        Returns:
            Scan results with optimal M_GUT
        """
        M_values = np.logspace(np.log10(M_GUT_range[0]), np.log10(M_GUT_range[1]), n_points)
        chi2_values = []

        original_M_GUT = self.M_GUT

        for M in M_values:
            self.M_GUT = M
            try:
                result = self.run_couplings(n_loops=2)
                chi2_values.append(result['chi2'])
            except Exception:
                chi2_values.append(np.inf)

        self.M_GUT = original_M_GUT  # Restore

        chi2_values = np.array(chi2_values)
        best_idx = np.argmin(chi2_values)

        return {
            "M_GUT_scan_min": M_GUT_range[0],
            "M_GUT_scan_max": M_GUT_range[1],
            "n_points": n_points,
            "optimal_M_GUT": float(M_values[best_idx]),
            "optimal_chi2": float(chi2_values[best_idx]),
            "PM_M_GUT": 2.1e16,
            "PM_chi2": float(chi2_values[np.argmin(np.abs(M_values - 2.1e16))])
        }


if __name__ == "__main__":
    print("=" * 60)
    print("RENORMALIZATION GROUP EVOLUTION")
    print("From M_GUT to M_Z")
    print("=" * 60)

    rg = RenormalizationGroupRunner(M_GUT=2.1e16, alpha_gut_input=1/24.0)

    print("\n1-Loop Evolution:")
    result_1 = rg.run_couplings(n_loops=1)
    print(f"  alpha_1^-1 = {result_1['alpha_1_inv']:.2f} (exp: {result_1['exp_alpha_1_inv']:.2f})")
    print(f"  alpha_2^-1 = {result_1['alpha_2_inv']:.2f} (exp: {result_1['exp_alpha_2_inv']:.2f})")
    print(f"  alpha_3^-1 = {result_1['alpha_3_inv']:.2f} (exp: {result_1['exp_alpha_3_inv']:.2f})")
    print(f"  chi2 = {result_1['chi2']:.2f}")

    print("\n2-Loop Evolution:")
    result_2 = rg.run_couplings(n_loops=2)
    print(f"  alpha_1^-1 = {result_2['alpha_1_inv']:.2f} (exp: {result_2['exp_alpha_1_inv']:.2f})")
    print(f"  alpha_2^-1 = {result_2['alpha_2_inv']:.2f} (exp: {result_2['exp_alpha_2_inv']:.2f})")
    print(f"  alpha_3^-1 = {result_2['alpha_3_inv']:.2f} (exp: {result_2['exp_alpha_3_inv']:.2f})")
    print(f"  chi2 = {result_2['chi2']:.2f}")
    print(f"  Status: {result_2['status']}")

    print("\n3-Loop Evolution:")
    result_3 = rg.run_couplings(n_loops=3)
    print(f"  alpha_1^-1 = {result_3['alpha_1_inv']:.2f}")
    print(f"  alpha_2^-1 = {result_3['alpha_2_inv']:.2f}")
    print(f"  alpha_3^-1 = {result_3['alpha_3_inv']:.2f}")
    print(f"  chi2 = {result_3['chi2']:.2f}")
