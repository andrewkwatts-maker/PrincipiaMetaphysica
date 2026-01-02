#!/usr/bin/env python3
"""
Vacuum Stability Monitor - Coleman-De Luccia Instanton Analysis
================================================================

Estimates the lifetime of the universe in the PM model using
Coleman-De Luccia instanton calculations. Checks if our local
minimum (the PM vacuum) is long-lived against tunneling.

This addresses the "Stability" gap by verifying that the racetrack
potential doesn't allow dangerous vacuum decay.

References:
- Coleman (1977) "Fate of the false vacuum: Semiclassical theory"
- Coleman & De Luccia (1980) "Gravitational effects on and of vacuum decay"
- Espinosa et al. (2015) "The cosmological Higgs dam instability"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from scipy.optimize import minimize_scalar


class VacuumStabilityMonitor:
    """
    Estimates Vacuum Decay Probability via Coleman-De Luccia instantons.
    Checks if the local minimum (our universe) is long-lived.
    """

    # Physical constants
    MP = 2.435e18           # Reduced Planck Mass (GeV)
    age_universe = 13.8e9   # Age of universe (years)
    hubble_volume = 4e80    # Current Hubble volume (GeV^-4)

    def __init__(self):
        """Initialize vacuum stability monitor."""
        pass

    def calculate_tunneling_action(
        self,
        V_true: float,
        V_false: float,
        barrier_height: float,
        barrier_width: float
    ) -> float:
        """
        Calculate the bounce action B for vacuum tunneling.

        Uses thin-wall approximation:
        B ≈ 27 * pi^2 * sigma^4 / (2 * epsilon^3)

        where sigma is wall tension and epsilon is energy difference.

        For thick walls (typical in moduli potentials), corrections apply.

        Args:
            V_true: True vacuum energy density (GeV^4)
            V_false: False vacuum energy density (GeV^4) - our vacuum
            barrier_height: Height of potential barrier (GeV^4)
            barrier_width: Width of barrier in field space (GeV)

        Returns:
            Dimensionless bounce action B
        """
        epsilon = V_false - V_true  # Energy difference

        if epsilon <= 0:
            return float('inf')  # Stable - true vacuum is higher or equal

        # Domain wall tension (simplified)
        # sigma ~ sqrt(barrier_height) * barrier_width
        sigma = np.sqrt(barrier_height) * barrier_width

        # Thin-wall bounce action
        if epsilon < 1e-100:
            return float('inf')

        B = (27 * np.pi**2 * sigma**4) / (2 * epsilon**3)

        # Gravitational corrections (important for Planck-scale physics)
        # These reduce the action, making tunneling easier
        grav_correction = 1 - (3 * sigma**2) / (self.MP**2 * np.sqrt(epsilon))

        if grav_correction > 0:
            B *= grav_correction

        return B

    def estimate_lifetime(self, action_B: float) -> Dict[str, Any]:
        """
        Estimate vacuum lifetime from bounce action.

        Decay rate per unit volume: Gamma/V ~ mu^4 * exp(-B)
        Lifetime ~ 1 / (Gamma/V * V_hubble)

        Args:
            action_B: Dimensionless bounce action

        Returns:
            Lifetime analysis dictionary
        """
        if action_B > 1000:
            return {
                "lifetime_years": "> 10^100",
                "lifetime_hubble": "> 10^90",
                "stable": True,
                "stability_class": "ABSOLUTELY_STABLE",
                "comment": "Vacuum is stable on all cosmological timescales"
            }

        if action_B > 400:
            return {
                "lifetime_years": f"~ 10^{action_B/2.3:.0f}",
                "lifetime_hubble": f"~ 10^{(action_B - 90)/2.3:.0f}",
                "stable": True,
                "stability_class": "METASTABLE_SAFE",
                "comment": "Vacuum is metastable but lifetime >> age of universe"
            }

        # Calculate numerical lifetime
        # Gamma/V ~ MP^4 * exp(-B)
        log_lifetime = action_B - 4 * np.log(self.MP / 1e9) - np.log(self.hubble_volume)
        lifetime_years = self.age_universe * np.exp(log_lifetime - 23)  # Rough conversion

        if lifetime_years > 1e20:
            stability = "METASTABLE_SAFE"
            stable = True
            comment = "Vacuum is metastable but safe"
        elif lifetime_years > self.age_universe:
            stability = "METASTABLE_MARGINAL"
            stable = True
            comment = "Vacuum is marginally safe"
        else:
            stability = "UNSTABLE"
            stable = False
            comment = "Vacuum could decay before now - problematic!"

        return {
            "lifetime_years": f"{lifetime_years:.2e}",
            "lifetime_hubble": f"{lifetime_years / self.age_universe:.2e} Hubble times",
            "stable": stable,
            "stability_class": stability,
            "comment": comment
        }

    def analyze_racetrack_potential(
        self,
        N_flux: int = 24,
        a: float = None,
        b: float = None,
        A: float = 1.0,
        B: float = 1.03,
        T_min: float = 9.865
    ) -> Dict[str, Any]:
        """
        Analyze stability of racetrack superpotential vacuum.

        W = A * exp(-a*T) + B * exp(-b*T)

        Args:
            N_flux: Flux quantum number (24 for TCS G2)
            a, b: Instanton coefficients (derived from N_flux if None)
            A, B: Prefactors
            T_min: Location of stabilized modulus

        Returns:
            Stability analysis for racetrack vacuum
        """
        if a is None:
            a = 2 * np.pi / N_flux
        if b is None:
            b = 2 * np.pi / (N_flux - 1)

        def W(T):
            """Superpotential."""
            return A * np.exp(-a * T) + B * np.exp(-b * T)

        def V(T):
            """
            Scalar potential (simplified F-term).
            V ~ exp(K) * |D_T W|^2 with K ~ -3 ln(2*Re(T))
            """
            K = -3 * np.log(2 * T)
            dW = -a * A * np.exp(-a * T) - b * B * np.exp(-b * T)
            dK = -3 / (2 * T)
            D_W = dW + dK * W(T)

            # Kahler metric K_TT ~ 3/(2T)^2
            K_TT_inv = (2 * T)**2 / 3

            V_F = np.exp(K) * (K_TT_inv * np.abs(D_W)**2 - 3 * np.abs(W(T))**2)
            return V_F

        # Find minimum
        result = minimize_scalar(V, bounds=(1, 50), method='bounded')
        T_computed_min = result.x
        V_min = V(T_computed_min)

        # Find barrier (local maximum between minima)
        # Check for runaway or additional minima
        T_scan = np.linspace(0.5, 100, 1000)
        V_scan = np.array([V(t) for t in T_scan])

        # Find local maxima (potential barriers)
        barriers = []
        for i in range(1, len(V_scan) - 1):
            if V_scan[i] > V_scan[i-1] and V_scan[i] > V_scan[i+1]:
                barriers.append((T_scan[i], V_scan[i]))

        # Asymptotic behavior (T -> infinity)
        V_asymp = V(100)  # Large T limit

        # Calculate tunneling action if barriers exist
        if barriers and len(barriers) > 0:
            barrier_T, barrier_V = barriers[0]
            V_barrier = barrier_V
            barrier_width = abs(barrier_T - T_computed_min)

            # Estimate lower vacuum (could be runaway or SUSY)
            V_true = min(V_asymp, 0)  # Conservative: assume AdS or SUSY minimum

            action_B = self.calculate_tunneling_action(
                V_true=V_true,
                V_false=V_min,
                barrier_height=V_barrier - V_min,
                barrier_width=barrier_width
            )
        else:
            # No barrier found - check if runaway
            if V_asymp < V_min:
                action_B = 100  # Some barrier exists from curvature
            else:
                action_B = float('inf')  # True minimum

        lifetime = self.estimate_lifetime(action_B)

        return {
            "N_flux": N_flux,
            "a": a,
            "b": b,
            "T_min_computed": float(T_computed_min),
            "T_min_input": T_min,
            "V_min": float(V_min),
            "n_barriers": len(barriers),
            "V_asymptotic": float(V_asymp),
            "bounce_action": float(action_B) if action_B != float('inf') else "infinite",
            "lifetime": lifetime,
            "status": lifetime["stability_class"]
        }

    def check_higgs_stability(
        self,
        m_h: float = 125.1,  # Higgs mass (PDG)
        m_t: float = 172.69,
        alpha_s: float = 0.1179
    ) -> Dict[str, Any]:
        """
        Check electroweak vacuum stability from Higgs potential.

        The SM Higgs potential may become unstable at high scales.
        PM framework modifies this through G2 couplings.

        Args:
            m_h: Higgs mass (GeV)
            m_t: Top quark mass (GeV)
            alpha_s: Strong coupling at M_Z

        Returns:
            Higgs vacuum stability analysis
        """
        # Critical top mass for stability (rough estimate)
        m_t_crit = 171.4 + 0.5 * (m_h - 125.1) - 0.3 * (alpha_s - 0.1179) / 0.001  # Higgs mass (PDG)

        # Instability scale (where lambda becomes negative)
        # Rough estimate from SM RG running
        log_Lambda_I = 17 + 3 * (m_h - 125.1) - 2 * (m_t - 172.69)  # Higgs mass (PDG)
        Lambda_I = 10**log_Lambda_I  # GeV

        if m_t < m_t_crit:
            status = "STABLE"
            comment = "Electroweak vacuum is absolutely stable"
        elif Lambda_I > 1e18:
            status = "METASTABLE_SAFE"
            comment = f"Metastable with instability scale ~ {Lambda_I:.1e} GeV"
        else:
            status = "METASTABLE_TENSION"
            comment = f"Instability scale {Lambda_I:.1e} GeV is below Planck scale"

        return {
            "m_higgs_GeV": m_h,
            "m_top_GeV": m_t,
            "m_top_critical": float(m_t_crit),
            "instability_scale_GeV": float(Lambda_I),
            "status": status,
            "comment": comment
        }


if __name__ == "__main__":
    print("=" * 60)
    print("VACUUM STABILITY MONITOR")
    print("Coleman-De Luccia Analysis")
    print("=" * 60)

    monitor = VacuumStabilityMonitor()

    print("\n1. RACETRACK POTENTIAL STABILITY:")
    racetrack = monitor.analyze_racetrack_potential(
        N_flux=24,
        T_min=9.865
    )
    print(f"   N_flux = {racetrack['N_flux']}")
    print(f"   T_min = {racetrack['T_min_computed']:.3f}")
    print(f"   V_min = {racetrack['V_min']:.2e}")
    print(f"   Barriers found: {racetrack['n_barriers']}")
    print(f"   Bounce action: {racetrack['bounce_action']}")
    print(f"   Stability: {racetrack['status']}")
    print(f"   {racetrack['lifetime']['comment']}")

    print("\n2. HIGGS VACUUM STABILITY:")
    higgs = monitor.check_higgs_stability(
        m_h=125.1,  # Higgs mass (PDG)
        m_t=172.69
    )
    print(f"   m_H = {higgs['m_higgs_GeV']} GeV")
    print(f"   m_t = {higgs['m_top_GeV']} GeV")
    print(f"   m_t critical = {higgs['m_top_critical']:.2f} GeV")
    print(f"   Instability scale: {higgs['instability_scale_GeV']:.2e} GeV")
    print(f"   Status: {higgs['status']}")
    print(f"   {higgs['comment']}")

    print("\n3. GENERIC TUNNELING EXAMPLE:")
    # Example: metastable dS vacuum
    V_our = -1.0e-120  # Cosmological constant scale
    V_lower = -2.0e-120  # Hypothetical lower vacuum

    B = monitor.calculate_tunneling_action(
        V_true=V_lower,
        V_false=V_our,
        barrier_height=1e-118,
        barrier_width=1e-2 * monitor.MP
    )
    lifetime = monitor.estimate_lifetime(B)

    print(f"   Bounce action B = {B:.2e}")
    print(f"   Stability: {lifetime['stability_class']}")
    print(f"   {lifetime['comment']}")
