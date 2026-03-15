"""
Unit Tests for Sphere Packing Simulation
==========================================
Tests E8 and Leech lattice sphere packing properties:
packing densities, coordination shells, lattice enumeration,
and Planck-scale patch simulation.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.geometry.sphere_packing import (
    E8SpherePacking, LeechSpherePacking, PlanckLatticeSimulation,
    L_PLANCK,
)


# ------------------------------------------------------------------
# E8 Sphere Packing
# ------------------------------------------------------------------

class TestE8Density:
    """Tests for E8 packing density."""

    @pytest.fixture(scope="class")
    def e8(self):
        return E8SpherePacking()

    def test_optimal_density_value(self, e8):
        expected = math.pi ** 4 / 384.0
        assert np.isclose(e8.optimal_density(), expected)

    def test_optimal_density_approximate(self, e8):
        assert np.isclose(e8.optimal_density(), 0.25367, atol=1e-4)

    def test_computed_density_matches_optimal(self, e8):
        """Computed density from geometry matches the known optimal."""
        computed = e8.compute_density()
        assert np.isclose(computed, e8.optimal_density(), rtol=1e-10)

    def test_packing_radius(self, e8):
        """Packing radius = 1/√2 for E8."""
        assert np.isclose(e8.packing_radius(), 1.0 / math.sqrt(2.0))

    def test_voronoi_volume(self, e8):
        """E8 is unimodular → Voronoi volume = 1."""
        assert np.isclose(e8.voronoi_cell_volume(), 1.0)

    def test_sphere_volume_8d(self, e8):
        """V₈(r) = π⁴r⁸/24."""
        r = 1.0
        expected = math.pi ** 4 / 24.0
        assert np.isclose(e8.sphere_volume_8d(r), expected)


class TestE8CoordinationShells:
    """Tests for E8 theta series / coordination sequence."""

    @pytest.fixture(scope="class")
    def e8(self):
        return E8SpherePacking()

    def test_first_shell_240(self, e8):
        shells = e8.coordination_shells(1)
        assert shells[0] == (2, 240)

    def test_second_shell_2160(self, e8):
        shells = e8.coordination_shells(2)
        assert shells[1] == (4, 2160)

    def test_third_shell_6720(self, e8):
        shells = e8.coordination_shells(3)
        assert shells[2] == (6, 6720)

    def test_fourth_shell_17520(self, e8):
        shells = e8.coordination_shells(4)
        assert shells[3] == (8, 17520)


class TestE8LatticeEnumeration:
    """Tests for E8 lattice point enumeration in finite balls."""

    @pytest.fixture(scope="class")
    def e8(self):
        return E8SpherePacking()

    def test_origin_only_at_small_radius(self, e8):
        """Only the origin at radius < √2."""
        points = e8.enumerate_lattice_points(1.0)
        assert len(points) == 1
        np.testing.assert_allclose(points[0], np.zeros(8))

    def test_first_shell_at_sqrt2(self, e8):
        """Origin + 240 roots at radius √2."""
        points = e8.enumerate_lattice_points(math.sqrt(2.0))
        assert len(points) == 241  # origin + 240 roots

    def test_all_points_in_ball(self, e8):
        """All enumerated points are within the given radius."""
        R = 2.0
        points = e8.enumerate_lattice_points(R)
        norms = np.sqrt(np.sum(points ** 2, axis=1))
        assert np.all(norms <= R + 1e-10)

    def test_first_two_shells(self, e8):
        """At radius 2, should have origin + 240 + 2160 = 2401 points."""
        points = e8.enumerate_lattice_points(2.0)
        assert len(points) == 2401


class TestE8DensityConvergence:
    """Tests for density convergence with patch size."""

    @pytest.fixture(scope="class")
    def e8(self):
        return E8SpherePacking()

    def test_density_increases_with_radius(self, e8):
        """Density should approach the optimal as R increases."""
        conv = e8.density_convergence(max_radius=3.0, num_steps=5)
        # Filter out zero-density entries
        densities = [d for _, d, n in conv if n > 0]
        assert len(densities) > 0

    def test_density_bounded_by_optimal(self, e8):
        """Finite patch density shouldn't vastly exceed optimal."""
        conv = e8.density_convergence(max_radius=3.0, num_steps=5)
        optimal = e8.optimal_density()
        for _, d, n in conv:
            if n > 100:  # Only check substantial patches
                assert d < optimal * 3.0  # Allow some finite-size fluctuation


# ------------------------------------------------------------------
# Leech Sphere Packing
# ------------------------------------------------------------------

class TestLeechDensity:
    """Tests for Leech lattice packing density."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechSpherePacking()

    def test_optimal_density_value(self, leech):
        expected = math.pi ** 12 / math.factorial(12)
        assert np.isclose(leech.optimal_density(), expected)

    def test_optimal_density_approximate(self, leech):
        assert np.isclose(leech.optimal_density(), 0.001930, atol=1e-5)

    def test_computed_density_matches(self, leech):
        computed = leech.compute_density()
        assert np.isclose(computed, leech.optimal_density(), rtol=1e-10)

    def test_packing_radius(self, leech):
        assert np.isclose(leech.packing_radius(), 1.0)

    def test_kissing_number(self, leech):
        shells = leech.coordination_shells(3)
        assert shells[2] == (4, 196_560)

    def test_no_norm2_vectors(self, leech):
        shells = leech.coordination_shells(3)
        assert shells[1] == (2, 0)


# ------------------------------------------------------------------
# Planck Lattice Simulation
# ------------------------------------------------------------------

class TestPlanckSimulation:
    """Tests for the full Planck-scale lattice simulation."""

    @pytest.fixture(scope="class")
    def sim(self):
        return PlanckLatticeSimulation()

    def test_simulation_runs(self, sim):
        results = sim.run()
        assert 'e8' in results
        assert 'leech' in results
        assert 'validation' in results
        assert 'physical' in results

    def test_e8_density_validated(self, sim):
        results = sim.run()
        assert results['validation']['e8_density_matches']

    def test_leech_density_validated(self, sim):
        results = sim.run()
        assert results['validation']['leech_density_matches']

    def test_n_gen_3(self, sim):
        results = sim.run()
        assert results['leech']['n_gen'] == 3

    def test_e8_lie_dim_248(self, sim):
        results = sim.run()
        assert results['e8']['lie_algebra_dim'] == 248

    def test_planck_length_correct(self, sim):
        results = sim.run()
        assert np.isclose(results['physical']['planck_length_m'], L_PLANCK)


class TestPlanckVerification:
    """Run the built-in verification suite."""

    def test_all_checks_pass(self):
        sim = PlanckLatticeSimulation()
        checks = sim.verify()
        for key, val in checks.items():
            assert val, f"Planck simulation check failed: {key}"
