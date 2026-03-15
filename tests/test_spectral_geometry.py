"""
Unit Tests for Spectral Geometry — Dirac Operator on Flat Tori
================================================================
Tests the Dirac operator spectrum, heat kernel, spectral zeta function,
eigenvalue symmetry, and Weyl asymptotics on flat T^d.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.geometry.spectral_geometry import FlatTorusDirac


# ------------------------------------------------------------------
# Basic structure
# ------------------------------------------------------------------

class TestDiracBasic:
    """Basic tests for Dirac operator on flat T⁷."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=7)

    def test_dimension(self, dirac):
        assert dirac.d == 7

    def test_spinor_dim_8(self, dirac):
        """Spinor dimension in 7D: 2^{⌊7/2⌋} = 2³ = 8."""
        assert dirac.spinor_dim == 8

    def test_periods_default_ones(self, dirac):
        np.testing.assert_array_equal(dirac.periods, np.ones(7))


class TestDirac3D:
    """Simpler tests on T³ for faster verification."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3, periods=np.array([1.0, 1.0, 1.0]))

    def test_spinor_dim_2(self, dirac):
        """Spinor dimension in 3D: 2^1 = 2."""
        assert dirac.spinor_dim == 2

    def test_zero_mode_exists(self, dirac):
        """n = (0,0,0) gives eigenvalue 0."""
        evals = dirac.analytic_eigenvalues(max_mode=2)
        assert np.sum(np.abs(evals) < 1e-10) >= 2  # 2 spinor components


# ------------------------------------------------------------------
# Eigenvalue structure
# ------------------------------------------------------------------

class TestEigenvalueSymmetry:
    """Tests for ±pairing of eigenvalues."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3)

    def test_eigenvalues_paired(self, dirac):
        """Eigenvalues come in ±pairs."""
        sym = dirac.check_symmetry(max_mode=2)
        assert sym['pm_paired']

    def test_equal_positive_negative(self, dirac):
        sym = dirac.check_symmetry(max_mode=2)
        assert sym['num_positive'] == sym['num_negative']

    def test_zero_modes_present(self, dirac):
        sym = dirac.check_symmetry(max_mode=2)
        assert sym['num_zero'] > 0


class TestAnalyticEigenvalues:
    """Tests for analytically known eigenvalues."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3, periods=np.array([1.0, 1.0, 1.0]))

    def test_first_nonzero_eigenvalue(self, dirac):
        """First nonzero |λ| = 2π for T³ with L=1."""
        evals = dirac.analytic_eigenvalues(max_mode=2)
        nonzero = np.abs(evals[np.abs(evals) > 1e-10])
        min_nonzero = np.min(nonzero)
        assert np.isclose(min_nonzero, 2 * math.pi, rtol=1e-10)

    def test_eigenvalue_formula(self, dirac):
        """Check λ = 2π√(n₁² + n₂² + n₃²) for specific modes."""
        # Mode (1,0,0): λ = 2π
        # Mode (1,1,0): λ = 2π√2
        # Mode (1,1,1): λ = 2π√3
        evals = set(round(abs(e), 8) for e in dirac.analytic_eigenvalues(max_mode=2)
                     if abs(e) > 1e-10)
        assert round(2 * math.pi, 8) in evals
        assert round(2 * math.pi * math.sqrt(2), 8) in evals
        assert round(2 * math.pi * math.sqrt(3), 8) in evals

    def test_different_periods(self):
        """Eigenvalues scale with period lengths."""
        d = FlatTorusDirac(dimension=3, periods=np.array([2.0, 2.0, 2.0]))
        evals = d.analytic_eigenvalues(max_mode=1)
        nonzero = np.abs(evals[np.abs(evals) > 1e-10])
        min_nonzero = np.min(nonzero)
        # λ = 2π·(1/L) = π for L=2
        assert np.isclose(min_nonzero, math.pi, rtol=1e-10)


# ------------------------------------------------------------------
# Dirac index
# ------------------------------------------------------------------

class TestDiracIndex:
    """Tests for the Dirac index on flat tori."""

    def test_index_zero_3d(self):
        d = FlatTorusDirac(dimension=3)
        assert d.dirac_index() == 0

    def test_index_zero_7d(self):
        d = FlatTorusDirac(dimension=7)
        assert d.dirac_index() == 0


# ------------------------------------------------------------------
# Heat kernel
# ------------------------------------------------------------------

class TestHeatKernel:
    """Tests for heat kernel trace K(t) = Σ exp(-λ²t)."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3)

    def test_large_t_limit(self, dirac):
        """K(t) → spinor_dim as t → ∞ (only zero modes survive)."""
        K = dirac.heat_kernel_trace(1000.0, max_mode=2)
        assert np.isclose(K, dirac.spinor_dim, atol=0.1)

    def test_K_nonnegative(self, dirac):
        """Heat kernel trace is always non-negative."""
        for t in [0.001, 0.01, 0.1, 1.0, 10.0]:
            K = dirac.heat_kernel_trace(t, max_mode=2)
            assert K >= 0

    def test_K_monotone_decreasing(self, dirac):
        """K(t) is monotonically decreasing (for positive eigenvalues)."""
        # Actually K(t) decreases from K(0)=N (total modes) to K(∞)=n_zero
        times = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
        Ks = [dirac.heat_kernel_trace(t, max_mode=2) for t in times]
        for i in range(len(Ks) - 1):
            assert Ks[i] >= Ks[i + 1] - 1e-10


class TestHeatKernelAsymptotics:
    """Tests for heat kernel asymptotic behavior."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3)

    def test_large_t_matches_zero_modes(self, dirac):
        asym = dirac.heat_kernel_asymptotics(max_mode=2)
        assert asym['large_t_matches']


# ------------------------------------------------------------------
# Spectral zeta function
# ------------------------------------------------------------------

class TestSpectralZeta:
    """Tests for spectral zeta function."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3)

    def test_zeta_positive(self, dirac):
        """ζ(s) > 0 for s > d/2."""
        z = dirac.spectral_zeta(2.0, max_mode=2)
        assert z > 0

    def test_zeta_decreasing_in_s(self, dirac):
        """ζ(s) decreases as s increases (eigenvalues > 1)."""
        z1 = dirac.spectral_zeta(2.0, max_mode=2)
        z2 = dirac.spectral_zeta(3.0, max_mode=2)
        assert z2 < z1


# ------------------------------------------------------------------
# Counting function (Weyl law)
# ------------------------------------------------------------------

class TestCountingFunction:
    """Tests for the eigenvalue counting function N(λ)."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=3)

    def test_N_zero_at_small_lambda(self, dirac):
        """N(λ) counts only zero modes for λ < 2π."""
        N = dirac.counting_function(1.0, max_mode=2)
        assert N == dirac.spinor_dim  # only zero modes

    def test_N_increases(self, dirac):
        """N(λ) is non-decreasing."""
        lambdas = [1.0, 5.0, 10.0, 20.0]
        Ns = [dirac.counting_function(l, max_mode=3) for l in lambdas]
        for i in range(len(Ns) - 1):
            assert Ns[i] <= Ns[i + 1]


# ------------------------------------------------------------------
# 7D G2 torus
# ------------------------------------------------------------------

class TestG2Torus:
    """Tests specifically for 7D torus relevant to G2 geometry."""

    @pytest.fixture(scope="class")
    def dirac(self):
        return FlatTorusDirac(dimension=7)

    def test_spinor_dim_8(self, dirac):
        assert dirac.spinor_dim == 8

    def test_eigenvalue_symmetry_7d(self, dirac):
        sym = dirac.check_symmetry(max_mode=1)
        assert sym['pm_paired']

    def test_index_zero_7d(self, dirac):
        assert dirac.dirac_index(max_mode=1) == 0

    def test_weyl_coefficient_positive(self, dirac):
        assert dirac.weyl_coefficient() > 0


# ------------------------------------------------------------------
# Full verification
# ------------------------------------------------------------------

class TestFullVerification:
    """Run the built-in verify() suite."""

    def test_verify_3d(self):
        d = FlatTorusDirac(dimension=3)
        results = d.verify(max_mode=2)
        for key, val in results.items():
            assert val, f"3D verification failed: {key}"

    def test_verify_7d(self):
        d = FlatTorusDirac(dimension=7)
        results = d.verify(max_mode=1)
        for key, val in results.items():
            assert val, f"7D verification failed: {key}"
