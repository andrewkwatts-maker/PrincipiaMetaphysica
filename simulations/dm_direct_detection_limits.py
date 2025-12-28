#!/usr/bin/env python3
"""
Dark Matter Direct Detection Limits
=====================================

Calculates the scattering cross-section of Mirror Dark Matter with
Standard Model nucleons. Checks predictions against LZ/XENONnT 2024-2025
sensitivity limits.

Since PM dark matter resides in a mirror sector, the coupling to SM
nucleons is suppressed by the portal (Pneuma) coupling, making direct
detection challenging but providing a clear falsifiability criterion.

References:
- LZ Collaboration (2023) "First Dark Matter Search Results from LUX-ZEPLIN"
- XENON Collaboration (2023) "First Dark Matter Search with Nuclear Recoils"
- Foot (2004) "Mirror dark matter: Cosmology, galaxy structure and direct detection"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple


class DMDetectionLimits:
    """
    Calculates the scattering cross-section of Mirror Dark Matter
    with Standard Model nucleons.

    In the PM framework, mirror DM couples to SM via the Pneuma portal,
    giving suppressed but potentially detectable signals.
    """

    # Physical constants
    m_nucleon = 0.938272  # Nucleon mass (GeV)
    G_F = 1.166e-5        # Fermi constant (GeV^-2)
    hbar_c2 = 3.894e-28   # Conversion factor (GeV^-2 to cm^2)

    # Experimental limits (approximate, 2024-2025)
    LIMITS = {
        "LZ_2023": {
            "mass_GeV": [10, 30, 50, 100, 300, 1000],
            "sigma_cm2": [1e-44, 5e-48, 1e-48, 1.5e-48, 3e-48, 1e-47]
        },
        "XENONnT_2023": {
            "mass_GeV": [10, 30, 50, 100, 300, 1000],
            "sigma_cm2": [2e-44, 8e-48, 2e-48, 2.5e-48, 5e-48, 2e-47]
        }
    }

    def __init__(self, g_pm_coupling: float = 1.0e-11):
        """
        Initialize DM detection calculator.

        Args:
            g_pm_coupling: Pneuma portal coupling (dimensionless)
                          This is the mixing between SM and mirror sectors.
                          PM prediction: ~10^-11 from G2 cycle separation.
        """
        self.g_mix = g_pm_coupling

    def calculate_sigma_si(
        self,
        m_dm_gev: float,
        form_factor: float = 1.0
    ) -> float:
        """
        Calculate Spin-Independent scattering cross-section.

        In mirror models: sigma_SI ~ (g_mix^2 * mu^2) / pi
        where mu is the reduced mass.

        Args:
            m_dm_gev: Dark matter particle mass in GeV
            form_factor: Nuclear form factor (default: 1)

        Returns:
            Cross-section in cm^2
        """
        # Reduced mass
        mu = (m_dm_gev * self.m_nucleon) / (m_dm_gev + self.m_nucleon)

        # Portal scattering amplitude
        # |M|^2 ~ g_mix^4 * mu^2 / (m_mediator^2)^2
        # For Pneuma-mediated: m_mediator ~ M_Planck / sqrt(chi_eff) ~ 2e17 GeV

        m_mediator = 2e17  # GeV (Pneuma mass scale)

        # Cross-section in natural units (GeV^-2)
        sigma_nat = (self.g_mix**4 * mu**2) / (np.pi * m_mediator**4)

        # Apply form factor
        sigma_nat *= form_factor**2

        # Convert to cm^2
        sigma_cm2 = sigma_nat * self.hbar_c2

        return sigma_cm2

    def calculate_sigma_sd(
        self,
        m_dm_gev: float,
        spin_factor: float = 1.0
    ) -> float:
        """
        Calculate Spin-Dependent scattering cross-section.

        Generally smaller than SI for scalar portal coupling.

        Args:
            m_dm_gev: Dark matter mass in GeV
            spin_factor: Nuclear spin structure factor

        Returns:
            SD cross-section in cm^2
        """
        # SD is typically suppressed by ~100 relative to SI for scalar portals
        sigma_si = self.calculate_sigma_si(m_dm_gev)
        sigma_sd = sigma_si * 0.01 * spin_factor

        return sigma_sd

    def get_experimental_limit(
        self,
        m_dm_gev: float,
        experiment: str = "LZ_2023"
    ) -> float:
        """
        Get experimental upper limit on cross-section at given mass.

        Args:
            m_dm_gev: Dark matter mass in GeV
            experiment: Experiment name ("LZ_2023", "XENONnT_2023")

        Returns:
            Upper limit on cross-section (cm^2)
        """
        if experiment not in self.LIMITS:
            raise ValueError(f"Unknown experiment: {experiment}")

        limits = self.LIMITS[experiment]
        masses = np.array(limits["mass_GeV"])
        sigmas = np.array(limits["sigma_cm2"])

        # Log-log interpolation
        log_m = np.log10(masses)
        log_s = np.log10(sigmas)

        limit = 10**np.interp(np.log10(m_dm_gev), log_m, log_s)

        return limit

    def is_excluded(
        self,
        m_dm_gev: float,
        sigma_cm2: float,
        experiment: str = "LZ_2023"
    ) -> bool:
        """
        Check if a point is excluded by current experiments.

        Args:
            m_dm_gev: Dark matter mass
            sigma_cm2: Predicted cross-section
            experiment: Experiment to compare against

        Returns:
            True if excluded (sigma > limit)
        """
        limit = self.get_experimental_limit(m_dm_gev, experiment)
        return sigma_cm2 > limit

    def analyze_pm_prediction(
        self,
        m_dm_range: Tuple[float, float] = (10, 1000),
        n_points: int = 50
    ) -> Dict[str, Any]:
        """
        Full analysis of PM dark matter detection prospects.

        Args:
            m_dm_range: Mass range to scan (GeV)
            n_points: Number of mass points

        Returns:
            Complete detection analysis
        """
        masses = np.logspace(np.log10(m_dm_range[0]), np.log10(m_dm_range[1]), n_points)
        sigmas = np.array([self.calculate_sigma_si(m) for m in masses])

        # Check against limits
        lz_limits = np.array([self.get_experimental_limit(m, "LZ_2023") for m in masses])
        xenon_limits = np.array([self.get_experimental_limit(m, "XENONnT_2023") for m in masses])

        # Find where PM prediction intersects limits
        ratio_lz = sigmas / lz_limits
        ratio_xenon = sigmas / xenon_limits

        # Characteristic mass and cross-section
        m_best = 100  # GeV (typical WIMP mass)
        sigma_best = self.calculate_sigma_si(m_best)

        # Detection prospects
        if np.max(ratio_lz) > 1:
            detection_status = "EXCLUDED"
            comment = "PM prediction already excluded by LZ"
        elif np.max(ratio_lz) > 0.1:
            detection_status = "TESTABLE"
            comment = "PM prediction within reach of next-generation experiments"
        elif np.max(ratio_lz) > 0.001:
            detection_status = "CHALLENGING"
            comment = "PM prediction requires significant detector improvements"
        else:
            detection_status = "BEYOND_REACH"
            comment = "PM coupling too weak for foreseeable direct detection"

        return {
            "portal_coupling": self.g_mix,
            "mass_range_GeV": m_dm_range,

            "sigma_at_100GeV_cm2": float(sigma_best),
            "lz_limit_at_100GeV_cm2": float(self.get_experimental_limit(100, "LZ_2023")),
            "ratio_to_lz_limit": float(sigma_best / self.get_experimental_limit(100, "LZ_2023")),

            "detection_status": detection_status,
            "comment": comment,

            "n_points_above_lz": int(np.sum(ratio_lz > 1)),
            "n_points_above_10pct_lz": int(np.sum(ratio_lz > 0.1)),

            "alternative_detection": (
                "Mirror DM may be better detected via: "
                "(1) Mirror photon emission, "
                "(2) Gravitational effects, "
                "(3) Self-interacting DM signatures"
            )
        }

    def derive_portal_coupling(
        self,
        chi_eff: int = 144,
        b3: int = 24,
        d_over_R: float = 0.12
    ) -> float:
        """
        Derive portal coupling from G2 geometry.

        The coupling between SM and mirror sectors is exponentially
        suppressed by cycle separation on the G2 manifold.

        Args:
            chi_eff: Effective Euler characteristic
            b3: Third Betti number
            d_over_R: Cycle separation ratio

        Returns:
            Portal coupling strength
        """
        # Base coupling from topology
        base_coupling = 1 / chi_eff  # ~ 1/144

        # Exponential suppression from cycle separation
        suppression = np.exp(-2 * np.pi * d_over_R * chi_eff / b3)

        # Total portal coupling
        g_portal = base_coupling * suppression

        return g_portal


if __name__ == "__main__":
    print("=" * 60)
    print("DARK MATTER DIRECT DETECTION ANALYSIS")
    print("Mirror Sector DM via Pneuma Portal")
    print("=" * 60)

    # Derive portal coupling from G2 geometry
    dm = DMDetectionLimits()
    g_derived = dm.derive_portal_coupling()
    print(f"\n1. G2-DERIVED PORTAL COUPLING:")
    print(f"   g_portal = {g_derived:.2e}")

    # Use derived coupling
    dm = DMDetectionLimits(g_pm_coupling=g_derived)

    print("\n2. CROSS-SECTION PREDICTIONS:")
    for m in [10, 50, 100, 500, 1000]:
        sigma = dm.calculate_sigma_si(m)
        limit = dm.get_experimental_limit(m, "LZ_2023")
        ratio = sigma / limit
        status = "EXCLUDED" if ratio > 1 else "OK"
        print(f"   m = {m:4d} GeV: sigma = {sigma:.2e} cm^2, limit = {limit:.2e} cm^2 ({status})")

    print("\n3. FULL ANALYSIS:")
    analysis = dm.analyze_pm_prediction()
    print(f"   Status: {analysis['detection_status']}")
    print(f"   Ratio to LZ: {analysis['ratio_to_lz_limit']:.2e}")
    print(f"   {analysis['comment']}")
    print(f"\n   Alternative: {analysis['alternative_detection']}")
