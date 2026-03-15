"""
Unit Tests for G2 Differential Geometry — Real Computation Verification
========================================================================
Tests the G2 3-form, Hitchin metric derivation, Hodge star, torsion
classes, curvature, and representation decomposition.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.geometry.g2_differential import G2DifferentialGeometry


@pytest.fixture(scope="module")
def g2():
    """Standard flat G2 geometry."""
    return G2DifferentialGeometry()


# ------------------------------------------------------------------
# 3-form structure
# ------------------------------------------------------------------

class TestThreeForm:
    """Tests for the associative 3-form φ."""

    def test_phi_shape(self, g2):
        assert g2.phi.shape == (7, 7, 7)

    def test_phi_antisymmetric(self, g2):
        """φ must be totally antisymmetric."""
        phi = g2.phi
        for i in range(7):
            for j in range(7):
                for k in range(7):
                    assert np.isclose(phi[i, j, k], -phi[j, i, k])
                    assert np.isclose(phi[i, j, k], -phi[i, k, j])
                    assert np.isclose(phi[i, j, k], phi[j, k, i])

    def test_phi_has_7_nonzero_triples(self, g2):
        """Standard φ has exactly 7 independent nonzero components."""
        phi = g2.phi
        count = 0
        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    if abs(phi[i, j, k]) > 1e-10:
                        count += 1
        assert count == 7

    def test_phi_norm_squared(self, g2):
        """||φ||² = 7 for the standard G2 form."""
        # Each of 7 triples contributes 3! = 6 nonzero entries of magnitude 1
        norm_sq = np.sum(g2.phi ** 2) / 6.0  # divide by 3! for normalization
        assert np.isclose(norm_sq, 7.0)


# ------------------------------------------------------------------
# Metric from 3-form
# ------------------------------------------------------------------

class TestMetric:
    """Tests for the Hitchin-derived metric."""

    def test_metric_shape(self, g2):
        assert g2.metric.shape == (7, 7)

    def test_metric_symmetric(self, g2):
        g = g2.metric
        np.testing.assert_allclose(g, g.T, atol=1e-10)

    def test_metric_positive_definite(self, g2):
        eigvals = np.linalg.eigvalsh(g2.metric)
        assert np.all(eigvals > 0)

    def test_standard_metric_is_identity(self, g2):
        """For standard φ₀, the derived metric is proportional to I₇."""
        g = g2.metric
        # Normalize
        scale = g[0, 0]
        g_normalized = g / scale
        np.testing.assert_allclose(g_normalized, np.eye(7), atol=1e-8)

    def test_metric_determinant_positive(self, g2):
        assert np.linalg.det(g2.metric) > 0


# ------------------------------------------------------------------
# Hodge star
# ------------------------------------------------------------------

class TestHodgeStar:
    """Tests for the Hodge dual ∗φ."""

    def test_star_phi_shape(self, g2):
        assert g2.star_phi.shape == (7, 7, 7, 7)

    def test_star_phi_antisymmetric(self, g2):
        """∗φ must be totally antisymmetric."""
        sp = g2.star_phi
        # Check a few swaps
        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    for l in range(k + 1, 7):
                        val = sp[i, j, k, l]
                        assert np.isclose(val, -sp[j, i, k, l])
                        assert np.isclose(val, -sp[i, k, j, l])
                        assert np.isclose(val, -sp[i, j, l, k])

    def test_star_phi_has_7_nonzero_quads(self, g2):
        """∗φ should have 7 independent nonzero components."""
        sp = g2.star_phi
        count = 0
        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    for l in range(k + 1, 7):
                        if abs(sp[i, j, k, l]) > 1e-10:
                            count += 1
        assert count == 7

    def test_hodge_involution(self, g2):
        """∗(∗φ) = φ (Hodge star is an involution on Ω³ in 7D)."""
        result = g2.check_hodge_involution()
        assert result['holds'], f"Hodge involution failed: max_error={result['max_error']}"


# ------------------------------------------------------------------
# Exterior derivatives
# ------------------------------------------------------------------

class TestExteriorDerivatives:
    """Tests for dφ and d∗φ."""

    def test_d_phi_zero(self, g2):
        """dφ = 0 for standard G2 (constant coefficients)."""
        d_phi = g2.compute_d_phi()
        assert np.allclose(d_phi, 0.0)

    def test_d_star_phi_zero(self, g2):
        """d∗φ = 0 for standard G2."""
        d_star = g2.compute_d_star_phi()
        assert np.allclose(d_star, 0.0)


# ------------------------------------------------------------------
# Torsion classes
# ------------------------------------------------------------------

class TestTorsionClasses:
    """Tests for the Fernández-Gray torsion decomposition."""

    def test_standard_is_torsion_free(self, g2):
        torsion = g2.compute_torsion_classes()
        assert torsion['torsion_free']

    def test_tau0_zero(self, g2):
        torsion = g2.compute_torsion_classes()
        assert abs(torsion['tau0']) < 1e-10

    def test_tau1_zero(self, g2):
        torsion = g2.compute_torsion_classes()
        assert np.allclose(torsion['tau1'], 0.0)

    def test_d_phi_norm_zero(self, g2):
        torsion = g2.compute_torsion_classes()
        assert torsion['dφ_norm'] < 1e-10

    def test_d_star_phi_norm_zero(self, g2):
        torsion = g2.compute_torsion_classes()
        assert torsion['d∗φ_norm'] < 1e-10


# ------------------------------------------------------------------
# Curvature
# ------------------------------------------------------------------

class TestCurvature:
    """Tests for curvature tensors."""

    def test_ricci_flat(self, g2):
        """G2 holonomy implies Ricci-flatness."""
        Ric = g2.compute_ricci()
        assert np.allclose(Ric, 0.0)

    def test_scalar_curvature_zero(self, g2):
        assert abs(g2.compute_scalar_curvature()) < 1e-10

    def test_riemann_zero_flat(self, g2):
        """Flat G2 has zero Riemann tensor."""
        R = g2.compute_riemann()
        assert np.allclose(R, 0.0)

    def test_christoffel_zero_flat(self, g2):
        """Flat metric has zero Christoffel symbols."""
        Gamma = g2.compute_christoffel()
        assert np.allclose(Gamma, 0.0)


# ------------------------------------------------------------------
# Representation decomposition
# ------------------------------------------------------------------

class TestRepresentationDecomposition:
    """Tests for Λ²(R⁷) = g₂ ⊕ R⁷."""

    def test_total_dimension_21(self, g2):
        decomp = g2.lambda2_decomposition()
        assert decomp['total_dim'] == 21

    def test_g2_dimension_14(self, g2):
        decomp = g2.lambda2_decomposition()
        assert decomp['g2_dim'] == 14

    def test_standard_dimension_7(self, g2):
        decomp = g2.lambda2_decomposition()
        assert decomp['standard_dim'] == 7

    def test_decomposition_valid(self, g2):
        decomp = g2.lambda2_decomposition()
        assert decomp['decomposition_valid']


# ------------------------------------------------------------------
# Perturbed G2
# ------------------------------------------------------------------

class TestPerturbedG2:
    """Tests for perturbed G2 structure (nonzero torsion)."""

    @pytest.fixture(scope="class")
    def perturbed(self):
        phi = G2DifferentialGeometry.perturbed_phi(epsilon=0.05, seed=42)
        return G2DifferentialGeometry(phi=phi)

    def test_perturbed_metric_still_positive_definite(self, perturbed):
        g = perturbed.compute_metric()
        eigvals = np.linalg.eigvalsh(g)
        assert np.all(eigvals > 0)

    def test_perturbed_metric_not_identity(self, perturbed):
        """Perturbed metric should deviate from identity."""
        g = perturbed.compute_metric()
        scale = g[0, 0]
        diff = np.max(np.abs(g / scale - np.eye(7)))
        assert diff > 1e-5  # Should be noticeably different


# ------------------------------------------------------------------
# Full verification
# ------------------------------------------------------------------

class TestFullVerification:
    """Run the built-in verify() suite."""

    def test_all_checks_pass(self, g2):
        results = g2.verify()
        for key, val in results.items():
            if key == 'hodge_max_error':
                continue  # This is a float, not a boolean
            assert val, f"G2 verification failed: {key}"
