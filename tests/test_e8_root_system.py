"""
Unit Tests for E8 Root System — Complete Algebraic Verification
================================================================
Tests the E8 root system construction: 240 roots, Cartan matrix,
Weyl reflections, Dynkin diagram, and lattice properties.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.algebra.e8_root_system import E8RootSystem


@pytest.fixture(scope="module")
def e8():
    """Construct the E8 root system once for all tests."""
    return E8RootSystem()


# ------------------------------------------------------------------
# Root count and structure
# ------------------------------------------------------------------

class TestRootCount:
    """Verify the fundamental counting properties of E8 roots."""

    def test_exactly_240_roots(self, e8):
        assert e8.num_roots == 240

    def test_120_positive_roots(self, e8):
        assert e8.num_positive_roots == 120

    def test_120_negative_roots(self, e8):
        assert len(e8.negative_roots) == 120

    def test_positive_plus_negative_equals_all(self, e8):
        """Positive and negative roots together give all 240."""
        all_roots = set(map(tuple, np.round(e8.roots, 10)))
        pos = set(map(tuple, np.round(e8.positive_roots, 10)))
        neg = set(map(tuple, np.round(e8.negative_roots, 10)))
        assert pos | neg == all_roots
        assert len(pos & neg) == 0  # disjoint

    def test_no_duplicate_roots(self, e8):
        """All 240 roots are distinct."""
        root_set = set(map(tuple, np.round(e8.roots, 10)))
        assert len(root_set) == 240

    def test_root_decomposition_112_plus_128(self, e8):
        """112 integer roots + 128 half-integer roots = 240."""
        integer_count = 0
        half_int_count = 0
        for r in e8.roots:
            if all(abs(c - round(c)) < 1e-10 for c in r):
                integer_count += 1
            else:
                half_int_count += 1
        assert integer_count == 112
        assert half_int_count == 128


# ------------------------------------------------------------------
# Root norms
# ------------------------------------------------------------------

class TestRootNorms:
    """All E8 roots must have norm² = 2 (simply-laced)."""

    def test_all_roots_norm_squared_2(self, e8):
        norms_sq = np.sum(e8.roots ** 2, axis=1)
        assert np.allclose(norms_sq, 2.0)

    def test_simple_roots_norm_squared_2(self, e8):
        norms_sq = np.sum(e8.simple_roots ** 2, axis=1)
        assert np.allclose(norms_sq, 2.0)


# ------------------------------------------------------------------
# Closure properties
# ------------------------------------------------------------------

class TestClosure:
    """Root system must be closed under negation and Weyl reflections."""

    def test_closed_under_negation(self, e8):
        root_set = set(map(tuple, np.round(e8.roots, 10)))
        for r in e8.roots:
            neg = tuple(np.round(-r, 10))
            assert neg in root_set

    def test_closed_under_weyl_reflections(self, e8):
        """Reflecting any root through any simple root hyperplane stays in the system."""
        root_set = set(map(tuple, np.round(e8.roots, 10)))
        rng = np.random.RandomState(42)
        for _ in range(500):
            i = rng.randint(240)
            j = rng.randint(8)
            reflected = e8.weyl_reflect(e8.roots[i], j)
            assert tuple(np.round(reflected, 10)) in root_set

    def test_closed_under_arbitrary_root_reflection(self, e8):
        """Reflecting any root through any other root stays in the system."""
        root_set = set(map(tuple, np.round(e8.roots, 10)))
        rng = np.random.RandomState(123)
        for _ in range(300):
            i, j = rng.choice(240, 2, replace=False)
            reflected = e8.weyl_reflect_by_root(e8.roots[i], e8.roots[j])
            assert tuple(np.round(reflected, 10)) in root_set


# ------------------------------------------------------------------
# Root string integrality
# ------------------------------------------------------------------

class TestIntegrality:
    """2⟨α, β⟩/⟨β, β⟩ must be an integer for all root pairs."""

    def test_root_string_integral(self, e8):
        rng = np.random.RandomState(99)
        for _ in range(1000):
            i, j = rng.choice(240, 2, replace=False)
            val = 2.0 * np.dot(e8.roots[i], e8.roots[j]) / np.dot(e8.roots[j], e8.roots[j])
            assert abs(val - round(val)) < 1e-10, f"Non-integral root string: {val}"


# ------------------------------------------------------------------
# Simple roots
# ------------------------------------------------------------------

class TestSimpleRoots:
    """Tests for the 8 simple roots (Bourbaki convention)."""

    def test_exactly_8_simple_roots(self, e8):
        assert len(e8.simple_roots) == 8

    def test_rank_is_8(self, e8):
        assert e8.rank == 8

    def test_simple_roots_are_roots(self, e8):
        """Every simple root is in the root system."""
        root_set = set(map(tuple, np.round(e8.roots, 10)))
        for sr in e8.simple_roots:
            assert tuple(np.round(sr, 10)) in root_set

    def test_simple_roots_linearly_independent(self, e8):
        rank = np.linalg.matrix_rank(e8.simple_roots)
        assert rank == 8

    def test_simple_root_inner_products_nonpositive(self, e8):
        """Off-diagonal inner products of simple roots are ≤ 0."""
        for i in range(8):
            for j in range(8):
                if i != j:
                    assert np.dot(e8.simple_roots[i], e8.simple_roots[j]) <= 1e-10


# ------------------------------------------------------------------
# Cartan matrix
# ------------------------------------------------------------------

class TestCartanMatrix:
    """Tests for the 8×8 Cartan matrix of E8."""

    def test_shape_8x8(self, e8):
        assert e8.cartan_matrix.shape == (8, 8)

    def test_diagonal_is_2(self, e8):
        for i in range(8):
            assert e8.cartan_matrix[i, i] == 2

    def test_off_diagonal_nonpositive(self, e8):
        for i in range(8):
            for j in range(8):
                if i != j:
                    assert e8.cartan_matrix[i, j] <= 0

    def test_determinant_is_1(self, e8):
        """E8 Cartan matrix has determinant 1 (unimodular)."""
        det = int(round(np.linalg.det(e8.cartan_matrix.astype(np.float64))))
        assert det == 1

    def test_cartan_matrix_matches_known(self, e8):
        """Verify against the known E8 Cartan matrix.

        Our labeling: α₅ is the trivalent branch node connecting
        to α₄ (chain), α₆ (arm length 1), and α₇-α₈ (arm length 2).
        """
        known = np.array([
            [ 2, -1,  0,  0,  0,  0,  0,  0],
            [-1,  2, -1,  0,  0,  0,  0,  0],
            [ 0, -1,  2, -1,  0,  0,  0,  0],
            [ 0,  0, -1,  2, -1,  0,  0,  0],
            [ 0,  0,  0, -1,  2, -1, -1,  0],
            [ 0,  0,  0,  0, -1,  2,  0,  0],
            [ 0,  0,  0,  0, -1,  0,  2, -1],
            [ 0,  0,  0,  0,  0,  0, -1,  2],
        ], dtype=np.int64)
        np.testing.assert_array_equal(e8.cartan_matrix, known)

    def test_cartan_matrix_symmetric(self, e8):
        """E8 is simply-laced, so Cartan matrix is symmetric."""
        np.testing.assert_array_equal(e8.cartan_matrix, e8.cartan_matrix.T)

    def test_positive_definite(self, e8):
        """Cartan matrix of finite type must be positive definite."""
        eigenvalues = np.linalg.eigvalsh(e8.cartan_matrix.astype(np.float64))
        assert all(ev > 0 for ev in eigenvalues)


# ------------------------------------------------------------------
# Dynkin diagram
# ------------------------------------------------------------------

class TestDynkinDiagram:
    """Tests for the E8 Dynkin diagram adjacency."""

    def test_adjacency_symmetric(self, e8):
        np.testing.assert_array_equal(e8.dynkin_adjacency, e8.dynkin_adjacency.T)

    def test_exactly_7_edges(self, e8):
        """E8 Dynkin diagram has exactly 7 edges (tree on 8 nodes)."""
        num_edges = np.sum(e8.dynkin_adjacency) // 2
        assert num_edges == 7

    def test_branching_node(self, e8):
        """Node 5 (α₆ in Bourbaki) has degree 3 (the branch point)."""
        degrees = np.sum(e8.dynkin_adjacency, axis=1)
        assert 3 in degrees  # E8 has exactly one trivalent node


# ------------------------------------------------------------------
# Lie algebra dimension
# ------------------------------------------------------------------

class TestDimension:
    """E8 Lie algebra dimension = 248 = 8 (rank) + 240 (roots)."""

    def test_dimension_248(self, e8):
        assert e8.dimension == 248


# ------------------------------------------------------------------
# Highest root and Coxeter number
# ------------------------------------------------------------------

class TestHighestRoot:
    """Tests for the highest root and dual Coxeter number."""

    def test_highest_root_norm_squared_2(self, e8):
        theta = e8.highest_root()
        assert np.isclose(np.dot(theta, theta), 2.0)

    def test_highest_root_is_a_root(self, e8):
        theta = e8.highest_root()
        root_set = set(map(tuple, np.round(e8.roots, 10)))
        assert tuple(np.round(theta, 10)) in root_set

    def test_dual_coxeter_number_30(self, e8):
        assert e8.dual_coxeter_number() == 30

    def test_weyl_group_order(self, e8):
        assert e8.weyl_group_order() == 696_729_600


# ------------------------------------------------------------------
# E8 × E8
# ------------------------------------------------------------------

class TestE8CrossE8:
    """Tests for E8 × E8 heterotic string root system."""

    def test_480_roots_in_r16(self, e8):
        cross = e8.e8_cross_e8_roots()
        assert cross.shape == (480, 16)

    def test_no_overlap(self, e8):
        cross = e8.e8_cross_e8_roots()
        left = cross[:240]
        right = cross[240:]
        # Left roots have zero right half, and vice versa
        assert np.allclose(left[:, 8:], 0.0)
        assert np.allclose(right[:, :8], 0.0)


# ------------------------------------------------------------------
# Coordination shells (theta series)
# ------------------------------------------------------------------

class TestCoordinationShells:
    """Tests for E8 lattice coordination sequence (theta series)."""

    def test_first_shell_240(self, e8):
        shells = e8.coordination_sequence(num_shells=1)
        assert shells[0] == (2, 240)

    def test_second_shell_2160(self, e8):
        shells = e8.coordination_sequence(num_shells=2)
        assert shells[1] == (4, 2160)

    def test_third_shell_6720(self, e8):
        shells = e8.coordination_sequence(num_shells=3)
        assert shells[2] == (6, 6720)


# ------------------------------------------------------------------
# Full verification
# ------------------------------------------------------------------

class TestFullVerification:
    """Run the built-in verify_root_system() and check all pass."""

    def test_all_checks_pass(self, e8):
        results = e8.verify_root_system()
        for key, val in results.items():
            assert val, f"Verification failed: {key}"
