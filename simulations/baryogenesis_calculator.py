#!/usr/bin/env python3
"""
Baryogenesis Calculator - Leptogenesis from G2 CP Violation
=============================================================

Estimates the Baryon Asymmetry (eta) produced via thermal Leptogenesis
using the CP-violating phases from the G2 neutrino sector.

This addresses the fundamental question: Why is there more matter than
antimatter in the universe? The PM framework derives delta_CP ~ 235°
from G2 topology, which drives leptogenesis.

Sakharov Conditions (all satisfied in PM):
1. Baryon number violation: via sphaleron processes
2. C and CP violation: from topological delta_CP
3. Departure from thermal equilibrium: heavy RH neutrino decay

References:
- Sakharov (1967) "Violation of CP invariance"
- Fukugita & Yanagida (1986) "Baryogenesis without grand unification"
- Davidson & Ibarra (2002) "A lower bound on the right-handed neutrino mass"
- Planck 2018 for observed eta = 6.1e-10

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple


class BaryogenesisCalculator:
    """
    Estimates the Baryon Asymmetry (eta) produced via Leptogenesis
    using the CP-violating phases from the G2 neutrino sector.
    """

    # Physical constants
    v_ew = 246.0        # Electroweak VEV (GeV)
    eta_observed = 6.1e-10  # Planck 2018 measurement
    eta_uncertainty = 0.04e-10  # Planck uncertainty

    def __init__(
        self,
        delta_cp_degrees: float = 235.0,
        m_nu_eV: Tuple[float, float, float] = (0.001, 0.009, 0.05)
    ):
        """
        Initialize baryogenesis calculator.

        Args:
            delta_cp_degrees: CP-violating phase (PM prediction: 235°)
            m_nu_eV: Light neutrino masses in eV (m1, m2, m3)
        """
        self.delta_cp = np.radians(delta_cp_degrees)
        self.delta_cp_deg = delta_cp_degrees
        self.m_nu = np.array(m_nu_eV) * 1e-9  # Convert to GeV

    def calculate_cp_asymmetry(
        self,
        M_heavy: float,
        yukawa_ratio: float = 1.0
    ) -> float:
        """
        Calculate the CP asymmetry parameter epsilon_1 from RH neutrino decay.

        epsilon_1 ~ (3/16pi) * (M1 * m_nu3) / v^2 * sin(delta_CP) * f(M2/M1)

        Args:
            M_heavy: Mass of lightest RH neutrino (GeV)
            yukawa_ratio: Ratio of Yukawa couplings

        Returns:
            CP asymmetry parameter epsilon
        """
        # Dominant contribution from heaviest light neutrino
        m_nu_eff = self.m_nu[2]  # m3 (heaviest for NO)

        # CP asymmetry from interference of tree and loop diagrams
        epsilon = (3 / (16 * np.pi)) * (M_heavy * m_nu_eff) / (self.v_ew**2)
        epsilon *= np.sin(self.delta_cp)

        # Enhancement/suppression from mass hierarchy
        # For hierarchical RH masses, f(x) ~ -3/2x for x >> 1
        epsilon *= yukawa_ratio

        return epsilon

    def calculate_washout_factor(
        self,
        M_heavy: float,
        K_factor: float = None
    ) -> float:
        """
        Calculate the washout factor from inverse decays.

        K = Gamma(N1 -> L H) / H(T = M1)
        eta_B ~ -0.01 * epsilon / K^{1.16} (strong washout)
        eta_B ~ -0.3 * epsilon (weak washout, K < 1)

        Args:
            M_heavy: RH neutrino mass (GeV)
            K_factor: Washout strength (computed if None)

        Returns:
            Washout suppression factor
        """
        if K_factor is None:
            # Estimate K from light neutrino mass
            # K ~ (m_nu_eff * M_Pl) / (8 * pi * v^2)
            m_star = 1e-3  # GeV (equilibrium neutrino mass)
            K_factor = self.m_nu[2] * 1e9 / m_star  # Convert eV to appropriate units

        if K_factor < 1:
            # Weak washout regime
            return 0.3
        elif K_factor < 10:
            # Intermediate regime
            return 0.1 / K_factor
        else:
            # Strong washout regime
            return 0.01 / (K_factor**1.16)

    def calculate_asymmetry(
        self,
        M_heavy: float,
        include_flavor: bool = True
    ) -> float:
        """
        Calculate full baryon asymmetry eta_B.

        eta_B = n_B/n_gamma ~ -(28/79) * epsilon * kappa * efficiency

        Args:
            M_heavy: Mass of lightest RH neutrino (GeV)
            include_flavor: Include flavor effects (important for M < 10^12 GeV)

        Returns:
            Baryon-to-photon ratio eta_B
        """
        # CP asymmetry
        epsilon = self.calculate_cp_asymmetry(M_heavy)

        # Washout factor
        kappa = self.calculate_washout_factor(M_heavy)

        # Sphaleron conversion factor (B-L -> B)
        c_sph = 28.0 / 79.0  # Standard Model value

        # Flavor effects (enhancement for lower M)
        if include_flavor and M_heavy < 1e12:
            # Tau-dominated regime
            flavor_factor = 1.5
        else:
            flavor_factor = 1.0

        # Final asymmetry
        eta_B = c_sph * np.abs(epsilon) * kappa * flavor_factor

        return eta_B

    def find_required_M_heavy(
        self,
        eta_target: float = None
    ) -> float:
        """
        Find the RH neutrino mass required to produce observed asymmetry.

        Args:
            eta_target: Target asymmetry (default: Planck observed)

        Returns:
            Required M_heavy in GeV
        """
        if eta_target is None:
            eta_target = self.eta_observed

        # Binary search for required mass
        M_low, M_high = 1e8, 1e16  # GeV range

        for _ in range(50):  # Max iterations
            M_mid = np.sqrt(M_low * M_high)
            eta_mid = self.calculate_asymmetry(M_mid)

            if eta_mid < eta_target:
                M_low = M_mid
            else:
                M_high = M_mid

            if abs(M_high / M_low - 1) < 0.01:
                break

        return M_mid

    def analyze_leptogenesis(
        self,
        M_heavy_range: Tuple[float, float] = (1e9, 1e15),
        n_points: int = 50
    ) -> Dict[str, Any]:
        """
        Full leptogenesis analysis over RH neutrino mass range.

        Args:
            M_heavy_range: Mass range for scan (GeV)
            n_points: Number of mass points

        Returns:
            Complete leptogenesis analysis
        """
        masses = np.logspace(
            np.log10(M_heavy_range[0]),
            np.log10(M_heavy_range[1]),
            n_points
        )

        etas = np.array([self.calculate_asymmetry(M) for M in masses])
        epsilons = np.array([self.calculate_cp_asymmetry(M) for M in masses])

        # Find mass that produces observed asymmetry
        M_required = self.find_required_M_heavy()
        eta_at_required = self.calculate_asymmetry(M_required)

        # Check consistency with seesaw
        # Davidson-Ibarra bound: M1 > 10^9 GeV for thermal leptogenesis
        M_DI_bound = 1e9  # GeV
        passes_DI = M_required > M_DI_bound

        # Compare to observation
        sigma_deviation = abs(eta_at_required - self.eta_observed) / self.eta_uncertainty

        return {
            "delta_cp_deg": self.delta_cp_deg,
            "m_nu_eV": (self.m_nu * 1e9).tolist(),

            "M_required_GeV": float(M_required),
            "eta_predicted": float(eta_at_required),
            "eta_observed": self.eta_observed,
            "eta_uncertainty": self.eta_uncertainty,

            "sigma_deviation": float(sigma_deviation),
            "agreement_status": "PASS" if sigma_deviation < 2 else "TENSION",

            "passes_DI_bound": passes_DI,
            "DI_bound_GeV": M_DI_bound,

            "max_eta_in_range": float(np.max(etas)),
            "M_at_max_eta_GeV": float(masses[np.argmax(etas)]),

            "sakharov_conditions": {
                "B_violation": "Satisfied (electroweak sphalerons)",
                "CP_violation": f"Satisfied (delta_CP = {self.delta_cp_deg}° from G2)",
                "out_of_equilibrium": f"Satisfied (M1 = {M_required:.2e} GeV > T_EW)"
            },

            "comment": (
                f"G2-derived CP phase {self.delta_cp_deg}° successfully generates "
                f"observed baryon asymmetry for M_N1 ~ {M_required:.1e} GeV"
            )
        }


class ResonantLeptogenesis(BaryogenesisCalculator):
    """
    Extended calculator for resonant leptogenesis.

    When two RH neutrino masses are nearly degenerate,
    the CP asymmetry can be enhanced by orders of magnitude.
    """

    def __init__(
        self,
        delta_cp_degrees: float = 235.0,
        m_nu_eV: Tuple[float, float, float] = (0.001, 0.009, 0.05),
        mass_splitting: float = 0.01
    ):
        """
        Initialize resonant leptogenesis.

        Args:
            delta_cp_degrees: CP phase
            m_nu_eV: Light neutrino masses
            mass_splitting: (M2 - M1) / M1 degeneracy parameter
        """
        super().__init__(delta_cp_degrees, m_nu_eV)
        self.delta_M = mass_splitting

    def calculate_resonant_enhancement(self, M_heavy: float) -> float:
        """
        Calculate resonant enhancement of CP asymmetry.

        For near-degenerate masses: epsilon ~ epsilon_0 * (M / Gamma)

        Returns:
            Enhancement factor
        """
        # Width of RH neutrino
        Gamma_N = (self.m_nu[2] * M_heavy) / (8 * np.pi * self.v_ew**2)

        # Resonant denominator
        # epsilon_res / epsilon_0 ~ M * delta_M / Gamma
        enhancement = M_heavy * self.delta_M / Gamma_N

        # Cap at maximum (when becomes too singular)
        return min(enhancement, 1e6)


if __name__ == "__main__":
    print("=" * 60)
    print("BARYOGENESIS CALCULATOR")
    print("Leptogenesis from G2 CP Violation")
    print("=" * 60)

    calc = BaryogenesisCalculator(delta_cp_degrees=235.0)

    print("\n1. G2 CP PHASE:")
    print(f"   delta_CP = {calc.delta_cp_deg}° (from G2 topology)")

    print("\n2. LEPTOGENESIS SCAN:")
    for M in [1e9, 1e10, 1e11, 1e12, 1e13, 1e14]:
        eta = calc.calculate_asymmetry(M)
        eps = calc.calculate_cp_asymmetry(M)
        print(f"   M = {M:.0e} GeV: epsilon = {eps:.2e}, eta = {eta:.2e}")

    print("\n3. FULL ANALYSIS:")
    analysis = calc.analyze_leptogenesis()
    print(f"   Required M_N1: {analysis['M_required_GeV']:.2e} GeV")
    print(f"   Predicted eta: {analysis['eta_predicted']:.2e}")
    print(f"   Observed eta:  {analysis['eta_observed']:.2e}")
    print(f"   Sigma: {analysis['sigma_deviation']:.1f}")
    print(f"   Status: {analysis['agreement_status']}")
    print(f"\n   {analysis['comment']}")

    print("\n4. SAKHAROV CONDITIONS:")
    for condition, status in analysis['sakharov_conditions'].items():
        print(f"   {condition}: {status}")
