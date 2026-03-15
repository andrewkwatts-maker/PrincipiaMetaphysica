"""
Unit Tests for Bridge Geometry and (2,0) Field Sampling
=========================================================
Tests the 12 bridge pair system, 27D metric assembly,
moduli stabilization, KK spectrum, and sampler fields.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.geometry.bridge_geometry import BridgeManifold, BridgeSystem


# ------------------------------------------------------------------
# Single Bridge Manifold
# ------------------------------------------------------------------

class TestBridgeManifold:
    """Tests for a single 2D bridge B_i = T²."""

    @pytest.fixture(scope="class")
    def bridge(self):
        return BridgeManifold(L1=1.0, L2=1.0, theta=math.pi / 2)

    def test_metric_shape(self, bridge):
        assert bridge.metric_2d.shape == (2, 2)

    def test_metric_symmetric(self, bridge):
        g = bridge.metric_2d
        np.testing.assert_allclose(g, g.T)

    def test_metric_positive_definite(self, bridge):
        eigvals = np.linalg.eigvalsh(bridge.metric_2d)
        assert np.all(eigvals > 0)

    def test_orthogonal_metric_is_identity(self, bridge):
        """Orthogonal torus with L1=L2=1: metric ≈ I₂."""
        np.testing.assert_allclose(bridge.metric_2d, np.eye(2), atol=1e-15)

    def test_area(self, bridge):
        assert np.isclose(bridge.area, 1.0)

    def test_complex_structure(self, bridge):
        """τ = i for square torus."""
        assert np.isclose(bridge.complex_structure, 1j)


class TestBridgeLaplacian:
    """Tests for Laplacian eigenvalues on T²."""

    @pytest.fixture(scope="class")
    def bridge(self):
        return BridgeManifold(L1=1.0, L2=1.0, theta=math.pi / 2)

    def test_zero_eigenvalue(self, bridge):
        evals = bridge.laplacian_eigenvalues(max_mode=3)
        assert evals[0] == 0.0

    def test_first_nonzero_eigenvalue(self, bridge):
        """For square torus L1=L2=1: λ_{1,0} = (2π)²."""
        evals = bridge.laplacian_eigenvalues(max_mode=3)
        first_nonzero = evals[evals > 1e-10][0]
        assert np.isclose(first_nonzero, 4 * math.pi ** 2, rtol=1e-10)

    def test_eigenvalues_nonnegative(self, bridge):
        evals = bridge.laplacian_eigenvalues(max_mode=3)
        assert np.all(evals >= -1e-10)

    def test_kk_masses_positive(self, bridge):
        masses = bridge.kk_masses(num_modes=3)
        assert np.all(masses > 0)

    def test_kk_first_mass(self, bridge):
        """First KK mass = 2π for unit square torus."""
        masses = bridge.kk_masses(num_modes=3)
        assert np.isclose(masses[0], 2 * math.pi, rtol=1e-10)


class TestBridgeScaling:
    """Tests for scaling behavior with different moduli."""

    def test_area_scales(self):
        b = BridgeManifold(L1=2.0, L2=3.0, theta=math.pi / 2)
        assert np.isclose(b.area, 6.0)

    def test_kk_mass_inversely_scales(self):
        """KK mass ∝ 1/L."""
        b1 = BridgeManifold(L1=1.0, L2=1.0, theta=math.pi / 2)
        b2 = BridgeManifold(L1=2.0, L2=2.0, theta=math.pi / 2)
        m1 = b1.kk_masses(3)[0]
        m2 = b2.kk_masses(3)[0]
        assert np.isclose(m1 / m2, 2.0, rtol=1e-10)

    def test_non_orthogonal_torus(self):
        """Non-orthogonal torus has smaller area."""
        b = BridgeManifold(L1=1.0, L2=1.0, theta=math.pi / 3)
        assert b.area < 1.0  # sin(π/3) ≈ 0.866


# ------------------------------------------------------------------
# Bridge System (12 bridges)
# ------------------------------------------------------------------

class TestBridgeSystem:
    """Tests for the 12-bridge system."""

    @pytest.fixture(scope="class")
    def system(self):
        return BridgeSystem()

    def test_12_bridges(self, system):
        assert len(system.bridges) == 12

    def test_bridge_dimensions_24(self, system):
        assert system.total_bridge_dimensions == 24

    def test_total_dimensions_27(self, system):
        """24 (bridges) + 1 (time) + 2 (sampler) = 27."""
        assert system.total_bridge_dimensions + 3 == 27


class TestMetric27D:
    """Tests for the full 27D metric."""

    @pytest.fixture(scope="class")
    def system(self):
        return BridgeSystem()

    def test_metric_shape(self, system):
        g = system.assemble_27d_metric()
        assert g.shape == (27, 27)

    def test_metric_symmetric(self, system):
        g = system.assemble_27d_metric()
        np.testing.assert_allclose(g, g.T)

    def test_signature_26_1(self, system):
        """Metric should have signature (26, 1) — Lorentzian."""
        sig = system.metric_signature()
        assert sig == (26, 1)

    def test_time_component_negative(self, system):
        g = system.assemble_27d_metric()
        assert g[0, 0] == -1.0

    def test_bridge_blocks_positive(self, system):
        """Each 2×2 bridge block is positive definite."""
        g = system.assemble_27d_metric()
        for i in range(12):
            block = g[1 + 2 * i:3 + 2 * i, 1 + 2 * i:3 + 2 * i]
            eigvals = np.linalg.eigvalsh(block)
            assert np.all(eigvals > 0)

    def test_sampler_fields_positive(self, system):
        g = system.assemble_27d_metric()
        assert g[25, 25] == 1.0
        assert g[26, 26] == 1.0

    def test_metric_determinant_negative(self, system):
        """Lorentzian metric has negative determinant."""
        g = system.assemble_27d_metric()
        assert np.linalg.det(g) < 0


# ------------------------------------------------------------------
# Moduli Stabilization
# ------------------------------------------------------------------

class TestModuliStabilization:
    """Tests for racetrack moduli stabilization."""

    @pytest.fixture(scope="class")
    def system(self):
        return BridgeSystem()

    def test_potential_finite(self, system):
        """Potential at default moduli is finite."""
        x0 = np.column_stack([
            np.ones(12) * 2.0, np.ones(12) * 2.0, np.full(12, math.pi / 2)
        ]).ravel()
        V = system.racetrack_potential(x0)
        assert np.isfinite(V)

    def test_stabilization_converges(self, system):
        opt, V = system.stabilize_moduli()
        assert V < 1.0  # Small potential

    def test_stabilized_moduli_positive(self, system):
        opt, _ = system.stabilize_moduli()
        assert np.all(opt[:, :2] > 0)  # L1, L2 > 0

    def test_stabilized_angles_valid(self, system):
        opt, _ = system.stabilize_moduli()
        assert np.all(opt[:, 2] > 0)      # θ > 0
        assert np.all(opt[:, 2] < math.pi) # θ < π


# ------------------------------------------------------------------
# KK Spectrum
# ------------------------------------------------------------------

class TestKKSpectrum:
    """Tests for Kaluza-Klein mass spectrum."""

    @pytest.fixture(scope="class")
    def system(self):
        return BridgeSystem()

    def test_kk_spectrum_nonempty(self, system):
        spectrum = system.combined_kk_spectrum(3)
        assert len(spectrum) > 0

    def test_kk_masses_positive(self, system):
        spectrum = system.combined_kk_spectrum(3)
        assert np.all(spectrum > 0)

    def test_kk_masses_sorted(self, system):
        spectrum = system.combined_kk_spectrum(3)
        assert np.all(np.diff(spectrum) >= -1e-10)

    def test_lightest_kk_mass(self, system):
        m = system.lightest_kk_mass(3)
        assert m > 0


# ------------------------------------------------------------------
# Coupling Matrix
# ------------------------------------------------------------------

class TestCouplingMatrix:
    """Tests for bridge coupling matrix."""

    @pytest.fixture(scope="class")
    def system(self):
        return BridgeSystem()

    def test_shape_12x12(self, system):
        C = system.coupling_matrix()
        assert C.shape == (12, 12)

    def test_symmetric(self, system):
        C = system.coupling_matrix()
        np.testing.assert_allclose(C, C.T)

    def test_positive_semi_definite(self, system):
        C = system.coupling_matrix()
        eigvals = np.linalg.eigvalsh(C)
        assert np.all(eigvals >= -1e-10)


# ------------------------------------------------------------------
# Sampler Fields
# ------------------------------------------------------------------

class TestSamplerFields:
    """Tests for S^{2,0} sampler data fields."""

    @pytest.fixture(scope="class")
    def system(self):
        return BridgeSystem()

    def test_sampler_modes_exist(self, system):
        modes = system.sampler_field_modes(bridge_index=0, max_mode=3)
        assert len(modes) > 0

    def test_zero_mode_present(self, system):
        modes = system.sampler_field_modes(bridge_index=0, max_mode=3)
        assert modes[0] == 0.0


# ------------------------------------------------------------------
# Full Verification
# ------------------------------------------------------------------

class TestFullVerification:
    """Run the built-in verification suite."""

    def test_all_checks_pass(self):
        system = BridgeSystem()
        results = system.verify()
        for key, val in results.items():
            assert val, f"Bridge verification failed: {key}"
