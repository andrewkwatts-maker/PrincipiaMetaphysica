"""
Bridge Geometry and (2,0) Field Sampling
==========================================
Implements the 12 bridge pair geometry B_i^{2,0} for the 27D spacetime
M^{27}(24,1,2). Each bridge is a 2D surface with complex structure,
moduli stabilization via racetrack superpotential, KK spectrum,
and sampler data fields S^{2,0}.

Dimensional Architecture:
  M^{27}(24,1,2) = T¹ ×_fiber (⊕_{i=1}^{12} B_i^{2,0}) ⊕ S^{2,0}
  - 24 = 12 bridge pairs × 2D each
  - 1  = timelike fiber T¹
  - 2  = sampler data fields S^{2,0}
  - Total: 24 + 1 + 2 = 27D, signature (26,1)

Mathematical Objects:
  - 12 bridge manifolds B_i (2D tori with complex structure τ_i)
  - Racetrack superpotential W = Σ A_j exp(−a_j T_i)
  - KK spectrum: m_n = n/R_i per bridge
  - Laplacian eigenmodes on T² (sampler fields)
  - Full 27D metric assembly

References:
  - Kachru, Kallosh, Linde, Trivedi (2003) "de Sitter Vacua in String Theory"
  - Denef, Douglas, Florea (2004) "Statistics of Flux Vacua"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
from scipy.optimize import minimize
from typing import Optional, List, Tuple
import math


class BridgeManifold:
    """A single 2D bridge manifold B_i = T² with complex structure τ_i.

    Each bridge is a flat 2-torus parametrized by:
      - L₁, L₂: side lengths
      - θ: angle between basis vectors (determines τ)
      - Complex structure τ = L₂/L₁ · exp(iθ)

    The bridge metric is:
      ds² = L₁²(dx¹)² + 2L₁L₂cos(θ) dx¹dx² + L₂²(dx²)²
    """

    def __init__(self, L1: float = 1.0, L2: float = 1.0, theta: float = math.pi / 2,
                 bridge_index: int = 0):
        self.L1 = L1
        self.L2 = L2
        self.theta = theta
        self.index = bridge_index

    @property
    def complex_structure(self) -> complex:
        """Complex structure τ = (L₂/L₁) · exp(iθ)."""
        return (self.L2 / self.L1) * np.exp(1j * self.theta)

    @property
    def area(self) -> float:
        """Area of the torus = L₁ L₂ sin(θ)."""
        return self.L1 * self.L2 * math.sin(self.theta)

    @property
    def metric_2d(self) -> np.ndarray:
        """2×2 metric tensor of the bridge."""
        g = np.array([
            [self.L1 ** 2, self.L1 * self.L2 * math.cos(self.theta)],
            [self.L1 * self.L2 * math.cos(self.theta), self.L2 ** 2]
        ], dtype=np.float64)
        return g

    def laplacian_eigenvalues(self, max_mode: int = 5) -> np.ndarray:
        """Eigenvalues of the scalar Laplacian on T².

        λ_{m,n} = (2π)² (m²/L₁² + n²/L₂² − 2mn cos(θ)/(L₁L₂)) / sin²(θ)

        For orthogonal torus (θ=π/2):
        λ_{m,n} = (2π)² (m²/L₁² + n²/L₂²)

        Returns:
            Sorted array of eigenvalues (with multiplicities)
        """
        eigenvalues = set()
        sin2 = math.sin(self.theta) ** 2

        for m in range(-max_mode, max_mode + 1):
            for n in range(-max_mode, max_mode + 1):
                if m == 0 and n == 0:
                    eigenvalues.add(0.0)
                    continue
                lam = (4 * math.pi ** 2 / sin2) * (
                    m ** 2 / self.L1 ** 2
                    + n ** 2 / self.L2 ** 2
                    - 2 * m * n * math.cos(self.theta) / (self.L1 * self.L2)
                )
                eigenvalues.add(round(lam, 10))

        return np.array(sorted(eigenvalues))

    def kk_masses(self, num_modes: int = 10) -> np.ndarray:
        """KK masses from compactification on this bridge.

        m_n = √(λ_n) where λ_n are Laplacian eigenvalues.
        """
        evals = self.laplacian_eigenvalues(max_mode=num_modes)
        # Skip zero mode
        positive = evals[evals > 1e-10]
        return np.sqrt(positive)


class BridgeSystem:
    """System of 12 bridge manifolds forming the 24D bridge sector.

    M^{27}(24,1,2) = T¹ ×_fiber (⊕_{i=1}^{12} B_i^{2,0}) ⊕ S^{2,0}
    """

    def __init__(self, moduli: Optional[np.ndarray] = None):
        """Initialize 12 bridge manifolds.

        Args:
            moduli: (12, 3) array of [L1, L2, theta] per bridge.
                   If None, uses default symmetric configuration.
        """
        if moduli is None:
            # Default: all bridges identical with L1=L2=1, θ=π/2
            moduli = np.column_stack([
                np.ones(12),           # L1
                np.ones(12),           # L2
                np.full(12, math.pi / 2)  # theta
            ])

        self._source = 'default'
        self.bridges = []
        for i in range(12):
            self.bridges.append(BridgeManifold(
                L1=moduli[i, 0],
                L2=moduli[i, 1],
                theta=moduli[i, 2],
                bridge_index=i
            ))

    # ------------------------------------------------------------------
    # Leech lattice connection
    # ------------------------------------------------------------------

    @classmethod
    def from_leech_decomposition(cls, leech) -> 'BridgeSystem':
        """Construct bridge system from Leech lattice sublattice decomposition.

        Derives bridge moduli (L1, L2, θ) from the Leech lattice's
        12 two-dimensional sublattice decomposition. Each 2D coordinate
        pair in Λ₂₄ corresponds to one bridge torus T².

        This replaces the default symmetric configuration with
        moduli derived from the Leech generator matrix structure.

        Args:
            leech: LeechLattice instance

        Returns:
            BridgeSystem with lattice-derived moduli
        """
        decomp = leech.decompose_bridge_pairs()
        moduli = decomp['moduli']

        instance = cls(moduli=moduli)
        instance._source = 'leech'
        instance._leech_source = leech
        instance._bridge_decomposition = decomp
        return instance

    @classmethod
    def from_lattice(cls) -> 'BridgeSystem':
        """Construct bridge system from Leech lattice (primary path).

        Attempts to build bridge moduli from the Leech lattice
        decomposition. Falls back to the default symmetric
        configuration if the lattice module is unavailable.

        Returns:
            BridgeSystem with _source set to 'leech' or 'default'
        """
        try:
            from simulations.PM.algebra.leech_lattice import LeechLattice
            leech = LeechLattice(compute_minimal=False)
            instance = cls.from_leech_decomposition(leech)
            # _source already set to 'leech' by from_leech_decomposition
            return instance
        except (ImportError, Exception):
            instance = cls()
            instance._source = 'default'
            return instance

    def verify_leech_origin(self, leech) -> dict:
        """Verify bridge system consistency with Leech lattice origin.

        Args:
            leech: LeechLattice instance

        Returns:
            Dict with verification results
        """
        checks = {}

        # Total bridge dimensions match Leech dimension
        checks['dim_matches_leech'] = self.total_bridge_dimensions == leech.dimension

        # 12 bridges = 24D / 2D per bridge
        checks['bridge_count'] = len(self.bridges) == leech.dimension // 2

        # Signature still (26,1)
        sig = self.metric_signature()
        checks['signature_26_1'] = sig == (26, 1)

        # All bridge areas positive
        checks['all_areas_positive'] = all(b.area > 0 for b in self.bridges)

        # All bridge moduli valid
        checks['moduli_valid'] = all(
            b.L1 > 0 and b.L2 > 0 and 0 < b.theta < math.pi
            for b in self.bridges
        )

        return checks

    @property
    def total_bridge_dimensions(self) -> int:
        """Total dimensions from bridges: 12 × 2 = 24."""
        return len(self.bridges) * 2

    # ------------------------------------------------------------------
    # Moduli stabilization
    # ------------------------------------------------------------------

    def racetrack_potential(self, moduli_flat: np.ndarray) -> float:
        """Racetrack superpotential for moduli stabilization.

        W = Σᵢ (Aᵢ exp(−aᵢ Tᵢ) + Bᵢ exp(−bᵢ Tᵢ))

        where Tᵢ = area(Bᵢ) + i·axion is the complexified Kähler modulus.

        The scalar potential is V = e^K (|DW|² − 3|W|²) in N=1 SUGRA.

        For simplicity, we minimize |W|² as a proxy for finding
        a stable vacuum.

        Args:
            moduli_flat: Flattened moduli array (L1_1, L2_1, θ_1, ..., L1_12, L2_12, θ_12)
        """
        moduli = moduli_flat.reshape(12, 3)

        # Racetrack parameters (from instanton counting)
        A = np.ones(12) * 1.0
        B = np.ones(12) * (-0.5)
        a = np.ones(12) * (2 * math.pi / 24)  # from b₃ = 24
        b = np.ones(12) * (2 * math.pi / 12)  # from b₃/2

        W = 0.0
        for i in range(12):
            L1, L2, theta = moduli[i]
            if theta <= 0 or theta >= math.pi:
                return 1e10  # Invalid angle
            if L1 <= 0 or L2 <= 0:
                return 1e10  # Invalid lengths
            T = L1 * L2 * math.sin(theta)  # Area (real part of Kähler modulus)
            W += A[i] * math.exp(-a[i] * T) + B[i] * math.exp(-b[i] * T)

        return W ** 2

    def stabilize_moduli(self) -> Tuple[np.ndarray, float]:
        """Find stable moduli configuration via racetrack potential minimization.

        Returns:
            (optimized_moduli, potential_value) tuple
        """
        # Initial guess: symmetric configuration
        x0 = np.column_stack([
            np.ones(12) * 2.0,
            np.ones(12) * 2.0,
            np.full(12, math.pi / 2)
        ]).ravel()

        # Bounds: L > 0.1, 0.1 < θ < π-0.1
        bounds = []
        for _ in range(12):
            bounds.extend([
                (0.1, 10.0),       # L1
                (0.1, 10.0),       # L2
                (0.1, math.pi - 0.1),  # theta
            ])

        result = minimize(
            self.racetrack_potential,
            x0,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': 1000}
        )

        optimized_moduli = result.x.reshape(12, 3)
        return optimized_moduli, result.fun

    # ------------------------------------------------------------------
    # KK spectrum
    # ------------------------------------------------------------------

    def combined_kk_spectrum(self, num_modes: int = 5) -> np.ndarray:
        """Combined KK spectrum from all 12 bridges.

        Each bridge contributes its own tower of KK masses.
        """
        all_masses = []
        for bridge in self.bridges:
            masses = bridge.kk_masses(num_modes)
            all_masses.extend(masses)
        return np.sort(all_masses)

    def lightest_kk_mass(self, num_modes: int = 3) -> float:
        """Lightest KK mass from any bridge."""
        spectrum = self.combined_kk_spectrum(num_modes)
        return float(spectrum[0]) if len(spectrum) > 0 else float('inf')

    # ------------------------------------------------------------------
    # Coupling matrix
    # ------------------------------------------------------------------

    def coupling_matrix(self) -> np.ndarray:
        """12×12 bridge coupling matrix.

        C_{ij} = ∫ dA × overlap between bridge i and bridge j modes.
        For non-overlapping bridges: C = diag(areas).
        """
        areas = np.array([b.area for b in self.bridges])
        return np.diag(areas)

    # ------------------------------------------------------------------
    # 27D metric
    # ------------------------------------------------------------------

    def assemble_27d_metric(self) -> np.ndarray:
        """Assemble the full 27D metric.

        ds² = −dt² + Σ_{i=1}^{12} ds²_i + ds²_S

        Structure:
          - Index 0: time (signature −1)
          - Indices 1-24: 12 bridge pairs (2 each)
          - Indices 25-26: sampler fields S^{2,0}

        Returns:
            (27, 27) metric tensor
        """
        g = np.zeros((27, 27), dtype=np.float64)

        # Time component: g_{00} = -1
        g[0, 0] = -1.0

        # Bridge components: indices 1-24
        for i, bridge in enumerate(self.bridges):
            g_bridge = bridge.metric_2d
            row = 1 + 2 * i
            g[row:row + 2, row:row + 2] = g_bridge

        # Sampler field components: indices 25-26
        g[25, 25] = 1.0
        g[26, 26] = 1.0

        return g

    def metric_signature(self) -> Tuple[int, int]:
        """Compute the metric signature (p, q) where p = positive, q = negative eigenvalues."""
        g = self.assemble_27d_metric()
        eigvals = np.linalg.eigvalsh(g)
        p = int(np.sum(eigvals > 1e-10))
        q = int(np.sum(eigvals < -1e-10))
        return (p, q)

    # ------------------------------------------------------------------
    # Sampler fields
    # ------------------------------------------------------------------

    def sampler_field_modes(self, bridge_index: int = 0,
                            max_mode: int = 5) -> np.ndarray:
        """Compute sampler field S^{2,0} modes on a bridge.

        The sampler fields are Laplacian eigenmodes on T² bridges,
        providing the data for the 2 extra sampler dimensions.

        Returns:
            Array of eigenvalues for the bridge Laplacian
        """
        return self.bridges[bridge_index].laplacian_eigenvalues(max_mode)

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verify(self) -> dict:
        """Verify bridge geometry properties."""
        results = {}

        # Dimension count: 12×2 + 1 + 2 = 27
        results['total_dim_27'] = self.total_bridge_dimensions + 3 == 27

        # Metric signature (26, 1)
        sig = self.metric_signature()
        results['signature_26_1'] = sig == (26, 1)

        # All bridge areas positive
        results['all_areas_positive'] = all(b.area > 0 for b in self.bridges)

        # Coupling matrix symmetric and positive semi-definite
        C = self.coupling_matrix()
        results['coupling_symmetric'] = bool(np.allclose(C, C.T))
        eigvals_C = np.linalg.eigvalsh(C)
        results['coupling_psd'] = bool(np.all(eigvals_C >= -1e-10))

        # KK masses exist
        spectrum = self.combined_kk_spectrum(3)
        results['kk_spectrum_nonempty'] = len(spectrum) > 0

        # Moduli stabilization
        opt_moduli, pot_val = self.stabilize_moduli()
        results['moduli_stabilized'] = pot_val < 1.0  # Small potential at minimum
        results['moduli_positive'] = bool(np.all(opt_moduli[:, :2] > 0))

        # Metric determinant (should be negative for Lorentzian)
        g = self.assemble_27d_metric()
        det_g = np.linalg.det(g)
        results['metric_det_negative'] = det_g < 0

        return results

    def __repr__(self):
        return f"BridgeSystem(bridges={len(self.bridges)}, dim={self.total_bridge_dimensions + 3})"
