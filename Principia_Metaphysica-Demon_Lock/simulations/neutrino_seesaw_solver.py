#!/usr/bin/env python3
"""
Neutrino Seesaw Solver - Type-I Seesaw Mechanism
=================================================

Calculates the physical neutrino masses using the Type-I Seesaw mechanism.
Checks predictions against the cosmological bound sum(m_nu) < 0.12 eV.

This addresses the "Observational Fit" gap by deriving neutrino masses
from the G2 Yukawa couplings and testing against Planck/CMB constraints.

The seesaw formula: m_nu = -m_D^T * M_R^(-1) * m_D

References:
- Minkowski (1977) "mu -> e gamma at rate one out of 10^9 muon decays?"
- Yanagida (1979) "Horizontal symmetry and masses of neutrinos"
- Gell-Mann, Ramond, Slansky (1979) in Supergravity
- NuFIT 6.0 (2024) for experimental mass splittings

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple


class NeutrinoSeesawSolver:
    """
    Solves the Type-I Seesaw Equation for light neutrino masses.

    m_nu = -m_D^T * M_R^(-1) * m_D

    where:
    - m_D = Y_nu * v / sqrt(2) is the Dirac mass matrix
    - M_R is the right-handed Majorana mass matrix
    """

    def __init__(self, v_higgs: float = 246.0):
        """
        Initialize seesaw solver.

        Args:
            v_higgs: Higgs VEV in GeV (default: 246 GeV)
        """
        self.v = v_higgs
        self.v_yukawa = v_higgs / np.sqrt(2)  # 174 GeV

        # Experimental constraints (NuFIT 6.0, NO)
        self.delta_m21_sq = 7.42e-5  # eV^2 (solar)
        self.delta_m31_sq = 2.510e-3  # eV^2 (atmospheric, NO)
        self.sum_nu_bound = 0.12  # eV (Planck 2018)

    def solve_masses(
        self,
        yukawa_matrix: np.ndarray,
        M_majorana: np.ndarray
    ) -> Dict[str, Any]:
        """
        Solve the seesaw equation for light neutrino masses.

        Args:
            yukawa_matrix: 3x3 Dirac Yukawa coupling matrix
            M_majorana: 3x3 right-handed Majorana mass matrix (GeV)

        Returns:
            Dictionary with mass eigenvalues and analysis
        """
        Y = np.array(yukawa_matrix, dtype=complex)
        M_R = np.array(M_majorana, dtype=complex)

        # Dirac Mass Matrix: m_D = Y * v / sqrt(2)
        m_D = Y * self.v_yukawa

        # Inverse of heavy Majorana matrix
        M_R_inv = np.linalg.inv(M_R)

        # Seesaw Formula: m_light = -m_D^T * M_R^(-1) * m_D
        # Note: For Hermitian case, this gives real eigenvalues
        m_light = -np.dot(np.transpose(m_D), np.dot(M_R_inv, m_D))

        # Diagonalize to get mass eigenvalues
        eigenvalues, eigenvectors = np.linalg.eigh(m_light)

        # Convert to eV (from GeV)
        masses_eV = np.abs(eigenvalues) * 1e9
        masses_eV = np.sort(masses_eV)  # Order: m1 < m2 < m3 (NO)

        # Calculate mass splittings
        delta_m21_sq_pred = masses_eV[1]**2 - masses_eV[0]**2
        delta_m31_sq_pred = masses_eV[2]**2 - masses_eV[0]**2

        # Sum of masses
        sum_masses = np.sum(masses_eV)

        # Determine ordering
        if masses_eV[2] > masses_eV[1] > masses_eV[0]:
            ordering = "Normal"
        else:
            ordering = "Inverted"

        # Check against cosmological bound
        passes_cosmo = sum_masses < self.sum_nu_bound

        # Check against oscillation data
        solar_check = abs(delta_m21_sq_pred - self.delta_m21_sq) / self.delta_m21_sq < 0.1
        atm_check = abs(delta_m31_sq_pred - self.delta_m31_sq) / self.delta_m31_sq < 0.1

        return {
            "m1_eV": float(masses_eV[0]),
            "m2_eV": float(masses_eV[1]),
            "m3_eV": float(masses_eV[2]),
            "sum_m_nu_eV": float(sum_masses),
            "ordering": ordering,

            "delta_m21_sq_pred": float(delta_m21_sq_pred),
            "delta_m31_sq_pred": float(delta_m31_sq_pred),
            "delta_m21_sq_exp": self.delta_m21_sq,
            "delta_m31_sq_exp": self.delta_m31_sq,

            "passes_cosmological_bound": passes_cosmo,
            "cosmo_bound_eV": self.sum_nu_bound,
            "solar_splitting_check": solar_check,
            "atmospheric_splitting_check": atm_check,

            "M_R_scale_GeV": float(np.abs(M_R[0, 0])),
            "status": "PASS" if (passes_cosmo and solar_check and atm_check) else "CHECK"
        }

    def derive_yukawas_from_g2(
        self,
        epsilon: float = 0.2257,
        chi_eff: int = 144,
        b3: int = 24
    ) -> np.ndarray:
        """
        Derive neutrino Yukawa matrix from G2 geometry.

        Uses the same hierarchical structure as charged fermions,
        but with additional suppression from right-handed neutrino location.

        Args:
            epsilon: Cabibbo angle (Wolfenstein parameter)
            chi_eff: Effective Euler characteristic
            b3: Third Betti number

        Returns:
            3x3 Yukawa matrix
        """
        # Base scale from G2 geometry
        base_yukawa = np.sqrt(b3 / chi_eff)  # ~ 0.41

        # Hierarchical suppression from cycle distances
        # Neutrino Yukawas are much smaller due to RH neutrino localization
        suppression = epsilon**3  # Additional suppression

        # Yukawa texture (Froggatt-Nielsen like)
        Y_nu = np.array([
            [epsilon**6, epsilon**5, epsilon**3],
            [epsilon**5, epsilon**4, epsilon**2],
            [epsilon**3, epsilon**2, 1.0]
        ]) * base_yukawa * suppression

        return Y_nu

    def derive_majorana_from_g2(
        self,
        M_GUT: float = 2.1e16,
        chi_eff: int = 144  # Derived: b3^2/4 = 24^2/4 = 576/4 = 144
    ) -> np.ndarray:
        """
        Derive right-handed Majorana mass matrix from G2 geometry.

        The RH neutrino mass is set by the GUT scale with geometric factors.

        Args:
            M_GUT: GUT scale in GeV
            chi_eff: Effective Euler characteristic (b3^2/4 = 144)

        Returns:
            3x3 Majorana mass matrix
        """
        # Base scale related to GUT
        M_scale = M_GUT / np.sqrt(chi_eff)  # ~ 1.75e15 GeV

        # Hierarchical structure (simpler than Dirac sector)
        M_R = np.diag([
            M_scale * 0.01,   # Lightest RH neutrino
            M_scale * 0.1,    # Middle RH neutrino
            M_scale * 1.0     # Heaviest RH neutrino
        ])

        return M_R

    def run_g2_seesaw(self) -> Dict[str, Any]:
        """
        Complete seesaw calculation with G2-derived inputs.

        Returns:
            Full seesaw analysis with G2 geometry inputs
        """
        # Derive Yukawas from G2
        Y_nu = self.derive_yukawas_from_g2()

        # Derive Majorana masses from G2/GUT
        M_R = self.derive_majorana_from_g2()

        # Solve seesaw
        result = self.solve_masses(Y_nu, M_R)

        # Add derivation info
        result["yukawa_source"] = "G2_geometry"
        result["majorana_source"] = "G2_GUT_scale"
        result["Y_nu_max"] = float(np.max(np.abs(Y_nu)))
        result["Y_nu_min"] = float(np.min(np.abs(Y_nu[Y_nu != 0])))

        return result


class ExtendedSeesawSolver(NeutrinoSeesawSolver):
    """
    Extended seesaw with Type-I + Type-II contributions.

    Includes both the standard seesaw and a triplet Higgs contribution
    that could arise from extended gauge sectors.
    """

    def __init__(self, v_higgs: float = 246.0, v_triplet: float = 0.1):
        """
        Initialize extended seesaw.

        Args:
            v_higgs: Standard Higgs VEV (GeV)
            v_triplet: Triplet Higgs VEV (eV scale for Type-II)
        """
        super().__init__(v_higgs)
        self.v_T = v_triplet * 1e-9  # Convert eV to GeV

    def solve_extended(
        self,
        yukawa_matrix: np.ndarray,
        M_majorana: np.ndarray,
        triplet_coupling: np.ndarray
    ) -> Dict[str, Any]:
        """
        Solve extended seesaw with Type-I + Type-II.

        m_nu = m_II + m_I = f * v_T - m_D^T M_R^(-1) m_D

        Args:
            yukawa_matrix: Dirac Yukawa (3x3)
            M_majorana: RH Majorana mass (3x3)
            triplet_coupling: Triplet Yukawa f (3x3)

        Returns:
            Extended seesaw results
        """
        # Type-I contribution
        type1_result = self.solve_masses(yukawa_matrix, M_majorana)

        # Type-II contribution
        f = np.array(triplet_coupling, dtype=complex)
        m_II = f * self.v_T * 1e9  # Convert to eV

        # Combined mass matrix
        m_I_eV = np.array([type1_result["m1_eV"], type1_result["m2_eV"], type1_result["m3_eV"]])

        # Simple addition (assuming diagonal dominance)
        m_total = m_I_eV + np.diag(m_II).real
        sum_total = np.sum(np.abs(m_total))

        return {
            "type1_contribution": type1_result,
            "type2_vev_eV": self.v_T * 1e9,
            "combined_sum_eV": float(sum_total),
            "passes_bound": sum_total < self.sum_nu_bound
        }


if __name__ == "__main__":
    print("=" * 60)
    print("NEUTRINO SEESAW SOLVER")
    print("Type-I Seesaw with G2 Geometry")
    print("=" * 60)

    solver = NeutrinoSeesawSolver()

    print("\n1. G2-DERIVED SEESAW:")
    result = solver.run_g2_seesaw()

    print(f"\n   Neutrino Masses:")
    print(f"   m1 = {result['m1_eV']:.5f} eV")
    print(f"   m2 = {result['m2_eV']:.5f} eV")
    print(f"   m3 = {result['m3_eV']:.5f} eV")
    print(f"   Sum = {result['sum_m_nu_eV']:.5f} eV (bound < {result['cosmo_bound_eV']} eV)")

    print(f"\n   Mass Splittings:")
    print(f"   Delta m21^2 = {result['delta_m21_sq_pred']:.2e} eV^2 (exp: {result['delta_m21_sq_exp']:.2e})")
    print(f"   Delta m31^2 = {result['delta_m31_sq_pred']:.2e} eV^2 (exp: {result['delta_m31_sq_exp']:.2e})")

    print(f"\n   Ordering: {result['ordering']}")
    print(f"   Cosmological check: {'PASS' if result['passes_cosmological_bound'] else 'FAIL'}")
    print(f"   Status: {result['status']}")

    print("\n2. EXAMPLE WITH EXPLICIT INPUTS:")
    # Example with explicit Yukawas
    Y_ex = np.array([
        [1e-6, 0, 0],
        [0, 2e-6, 0],
        [0, 0, 5e-6]
    ])
    M_R_ex = np.eye(3) * 1e14  # 10^14 GeV

    result_ex = solver.solve_masses(Y_ex, M_R_ex)
    print(f"   m1 = {result_ex['m1_eV']:.5f} eV")
    print(f"   m2 = {result_ex['m2_eV']:.5f} eV")
    print(f"   m3 = {result_ex['m3_eV']:.5f} eV")
    print(f"   Sum = {result_ex['sum_m_nu_eV']:.5f} eV")
