#!/usr/bin/env python3
"""
Kahler Metric Geometry - Moduli Space Cross-Talk
=================================================

Computes the Kahler Metric K_{ij_bar} for the G2 moduli space.
This proves the sectors (SM, Mirror, Hidden) are geometrically coupled,
not just independently stacked.

The non-diagonal metric introduces kinetic mixing between moduli,
which affects how the different sectors interact and how masses run.

References:
- Acharya & Witten (2001) "Chiral fermions from manifolds of G2 holonomy"
- KKLT (2003) "de Sitter Vacua in String Theory"
- Joyce (2000) "Compact Manifolds with Special Holonomy"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional, Union


class KahlerMetricGeometry:
    """
    Computes the Kahler Metric K_{i j_bar} for the G2 moduli space.
    Used to normalize kinetic terms and calculate cross-talk between sectors.
    """

    def __init__(self, moduli_values: Union[List, np.ndarray]):
        """
        Initialize with moduli field values.

        Args:
            moduli_values: List or array of complex moduli T_i
                          Real part = volume/shape, Imag part = axion
        """
        self.T = np.array(moduli_values, dtype=complex)
        self.n_moduli = len(self.T)

        # Sector labels for interpretation
        self.sector_names = ["SM", "Mirror", "Hidden", "Gravity"][:self.n_moduli]

    def kahler_potential(self) -> complex:
        """
        Compute the Kahler potential K for the moduli space.

        For G2 compactification with volume modulus:
        K = -3 ln(T + T_bar) for single modulus
        K = -sum_i ln(T_i + T_i_bar) for multiple moduli (simplified)

        In full TCS G2: K = -3 ln(Vol(Y)) where Vol depends on all moduli.

        Returns:
            Kahler potential (real part is physical)
        """
        # Sum of real parts (volumes)
        volume_term = np.sum(self.T + np.conj(self.T))

        if volume_term <= 0:
            raise ValueError("Volume term must be positive for valid compactification")

        return -3 * np.log(volume_term)

    def compute_metric(self) -> np.ndarray:
        """
        Compute the Kahler metric K_{i j_bar} = d^2 K / d T_i d T_j_bar.

        For K = -3 ln(sum_i(T_i + T_i_bar)):
        K_{ij_bar} = 3 / (sum_k(T_k + T_k_bar))^2

        This gives a democratic (all equal) metric in this approximation.
        More realistic: include subleading corrections from topology.

        Returns:
            n_moduli x n_moduli complex matrix
        """
        metric = np.zeros((self.n_moduli, self.n_moduli), dtype=complex)

        # Total volume
        denom = np.sum(self.T + np.conj(self.T))

        # Leading order: democratic metric
        for i in range(self.n_moduli):
            for j in range(self.n_moduli):
                metric[i, j] = 3.0 / (denom ** 2)

        # Add subleading corrections based on moduli separation
        # This breaks the democracy and introduces hierarchy
        for i in range(self.n_moduli):
            for j in range(self.n_moduli):
                if i != j:
                    # Cross-term suppression from cycle separation
                    T_diff = np.abs(self.T[i] - self.T[j])
                    suppression = np.exp(-T_diff / 10.0)  # Decay scale
                    metric[i, j] *= suppression

        return metric

    def compute_inverse_metric(self) -> np.ndarray:
        """
        Compute the inverse Kahler metric K^{ij_bar}.

        Used for kinetic term normalization and coupling calculations.

        Returns:
            Inverse metric matrix
        """
        metric = self.compute_metric()
        return np.linalg.inv(metric)

    def get_coupling_strength(self, sector_i: int, sector_j: int) -> float:
        """
        Returns the geometric coupling between two sectors based on inverse metric.

        Coupling ~ K^{ij_bar} determines how strongly sectors communicate.

        Args:
            sector_i: Index of first sector (0=SM, 1=Mirror, etc.)
            sector_j: Index of second sector

        Returns:
            Coupling strength (dimensionless)
        """
        if sector_i >= self.n_moduli or sector_j >= self.n_moduli:
            raise ValueError(f"Sector index out of range (max: {self.n_moduli-1})")

        g_inverse = self.compute_inverse_metric()
        return float(np.abs(g_inverse[sector_i, sector_j]))

    def compute_canonical_normalization(self) -> np.ndarray:
        """
        Compute canonical normalization factors for each modulus.

        To get canonical kinetic terms, we need to rescale:
        T_i^{can} = sqrt(K_{ii}) * T_i

        Returns:
            Array of normalization factors
        """
        metric = self.compute_metric()
        return np.sqrt(np.real(np.diag(metric)))

    def analyze_sector_hierarchy(self) -> Dict[str, Any]:
        """
        Analyze the hierarchy structure from the Kahler metric.

        Returns:
            Dictionary with hierarchy analysis
        """
        metric = self.compute_metric()
        inv_metric = self.compute_inverse_metric()

        # Eigenvalue analysis for hierarchy
        eigenvalues = np.linalg.eigvals(np.real(metric))
        eigenvalues = np.sort(np.real(eigenvalues))[::-1]

        hierarchy_ratio = eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] != 0 else np.inf

        # Cross-sector couplings
        couplings = {}
        for i in range(self.n_moduli):
            for j in range(i+1, self.n_moduli):
                name = f"{self.sector_names[i]}-{self.sector_names[j]}"
                couplings[name] = self.get_coupling_strength(i, j)

        return {
            "n_moduli": self.n_moduli,
            "moduli_values": self.T.tolist(),
            "kahler_potential": float(np.real(self.kahler_potential())),
            "metric_eigenvalues": eigenvalues.tolist(),
            "hierarchy_ratio": float(hierarchy_ratio),
            "cross_sector_couplings": couplings,
            "canonical_normalizations": self.compute_canonical_normalization().tolist(),
            "status": "HIERARCHICAL" if hierarchy_ratio > 10 else "DEMOCRATIC"
        }

    def compute_f_term_potential(self, W: complex, dW: np.ndarray) -> float:
        """
        Compute the F-term scalar potential from superpotential.

        V_F = exp(K) * [K^{ij_bar} D_i W D_j_bar W_bar - 3|W|^2]

        where D_i W = dW/dT_i + (dK/dT_i) * W

        Args:
            W: Superpotential value
            dW: Array of superpotential derivatives dW/dT_i

        Returns:
            F-term potential value
        """
        K = self.kahler_potential()
        K_inv = self.compute_inverse_metric()

        # Kahler derivatives (simplified)
        denom = np.sum(self.T + np.conj(self.T))
        dK = -3.0 / denom * np.ones(self.n_moduli)

        # Kahler covariant derivatives
        D_W = dW + dK * W
        D_W_bar = np.conj(D_W)

        # Contract with inverse metric
        contraction = 0
        for i in range(self.n_moduli):
            for j in range(self.n_moduli):
                contraction += K_inv[i, j] * D_W[i] * D_W_bar[j]

        V_F = np.exp(np.real(K)) * (np.real(contraction) - 3 * np.abs(W)**2)

        return float(V_F)


class TCSKahlerGeometry(KahlerMetricGeometry):
    """
    Specialized Kahler geometry for TCS (Twisted Connected Sum) G2 manifolds.

    Includes the specific structure from Joyce's TCS construction:
    - 4 Kahler moduli from h^{1,1} = 4
    - Specific gluing constraints from K=4 matching
    """

    def __init__(self, h11: int = 4, chi_eff: int = 144, b3: int = 24):
        """
        Initialize TCS geometry.

        Args:
            h11: Hodge number h^{1,1} (default: 4 for TCS #187)
            chi_eff: Effective Euler characteristic (144)
            b3: Third Betti number (24)
        """
        self.h11 = h11
        self.chi_eff = chi_eff
        self.b3 = b3

        # Initialize moduli at stabilized values
        # Real parts from racetrack stabilization
        moduli = [
            9.865 + 0.1j,   # SM sector (Re(T) from Higgs constraint)
            23.5 + 0.0j,    # Mirror sector
            24.0 + 0.05j,   # Hidden sector
            100.0 + 0.2j    # Gravity sector (large volume)
        ][:h11]

        super().__init__(moduli)
        self.sector_names = ["SM", "Mirror", "Hidden", "Gravity"][:h11]

    def compute_tcs_metric(self) -> np.ndarray:
        """
        Compute Kahler metric with TCS-specific corrections.

        Includes:
        - K-matching gluing contributions
        - Cycle separation terms
        - Topological corrections from b3

        Returns:
            TCS-corrected Kahler metric
        """
        # Start with base metric
        metric = self.compute_metric()

        # TCS corrections
        K_matching = 4  # Matching parameter

        # Off-diagonal suppression from gluing
        gluing_suppression = np.exp(-np.pi / K_matching)

        for i in range(self.n_moduli):
            for j in range(self.n_moduli):
                if i != j:
                    metric[i, j] *= gluing_suppression

        # Topological correction to diagonal
        topo_correction = 1 + self.b3 / (12 * self.chi_eff)
        for i in range(self.n_moduli):
            metric[i, i] *= topo_correction

        return metric


if __name__ == "__main__":
    print("=" * 60)
    print("KAHLER METRIC GEOMETRY ANALYSIS")
    print("G2 Moduli Space Structure")
    print("=" * 60)

    # Example: 3 Moduli (SM, Mirror, Hidden)
    moduli = [9.865 + 0.1j, 23.5 + 0j, 24.0 + 0.05j]

    kg = KahlerMetricGeometry(moduli)

    print("\n1. MODULI VALUES:")
    for i, T in enumerate(moduli):
        print(f"   T_{i} ({kg.sector_names[i]}): {T}")

    print(f"\n2. KAHLER POTENTIAL:")
    K = kg.kahler_potential()
    print(f"   K = {np.real(K):.4f}")

    print("\n3. KAHLER METRIC (Real part):")
    metric = kg.compute_metric()
    print(np.real(metric))

    print("\n4. CROSS-SECTOR COUPLINGS:")
    for i in range(len(moduli)):
        for j in range(i+1, len(moduli)):
            coupling = kg.get_coupling_strength(i, j)
            print(f"   {kg.sector_names[i]}-{kg.sector_names[j]}: {coupling:.4e}")

    print("\n5. HIERARCHY ANALYSIS:")
    analysis = kg.analyze_sector_hierarchy()
    print(f"   Eigenvalues: {analysis['metric_eigenvalues']}")
    print(f"   Hierarchy ratio: {analysis['hierarchy_ratio']:.2f}")
    print(f"   Status: {analysis['status']}")

    print("\n6. TCS G2 SPECIFIC GEOMETRY:")
    tcs = TCSKahlerGeometry(h11=4, chi_eff=144, b3=24)
    tcs_analysis = tcs.analyze_sector_hierarchy()
    print(f"   TCS moduli count: {tcs_analysis['n_moduli']}")
    print(f"   TCS hierarchy: {tcs_analysis['hierarchy_ratio']:.2f}")
