"""
Unit Tests for Leech Lattice Λ₂₄ — Golay Code and Lattice Verification
========================================================================
Tests the extended Golay code construction, Leech lattice properties,
theta series, and minimal vector enumeration.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.algebra.leech_lattice import GolayCode, LeechLattice


# ------------------------------------------------------------------
# Golay Code Tests
# ------------------------------------------------------------------

class TestGolayCodeStructure:
    """Verify the [24, 12, 8] extended binary Golay code."""

    @pytest.fixture(scope="class")
    def golay(self):
        return GolayCode()

    def test_generator_matrix_shape(self, golay):
        assert golay.generator_matrix.shape == (12, 24)

    def test_generator_left_half_identity(self, golay):
        """Left 12 columns of generator are I₁₂."""
        np.testing.assert_array_equal(
            golay.generator_matrix[:, :12],
            np.eye(12, dtype=np.uint8)
        )

    def test_exactly_4096_codewords(self, golay):
        cw = golay.enumerate_codewords()
        assert len(cw) == 4096

    def test_zero_codeword_present(self, golay):
        cw = golay.enumerate_codewords()
        assert any(np.all(c == 0) for c in cw)

    def test_all_ones_codeword_present(self, golay):
        cw = golay.enumerate_codewords()
        assert any(np.all(c == 1) for c in cw)

    def test_all_codewords_binary(self, golay):
        cw = golay.enumerate_codewords()
        assert np.all((cw == 0) | (cw == 1))

    def test_closed_under_addition_mod2(self, golay):
        """Sum of any two codewords (mod 2) is a codeword."""
        cw = golay.enumerate_codewords()
        cw_set = set(map(tuple, cw))
        rng = np.random.RandomState(42)
        for _ in range(500):
            i, j = rng.choice(4096, 2)
            s = tuple((cw[i] + cw[j]) % 2)
            assert s in cw_set


class TestGolayMinDistance:
    """Verify minimum Hamming distance = 8."""

    @pytest.fixture(scope="class")
    def golay(self):
        return GolayCode()

    def test_min_distance_8(self, golay):
        assert golay.min_distance() == 8

    def test_no_low_weight_codewords(self, golay):
        """No nonzero codewords with weight < 8."""
        wd = golay.weight_distribution()
        for w in range(1, 8):
            assert wd.get(w, 0) == 0


class TestGolayWeightDistribution:
    """Verify the known weight distribution of C₂₄."""

    @pytest.fixture(scope="class")
    def golay(self):
        return GolayCode()

    def test_weight_0_count(self, golay):
        wd = golay.weight_distribution()
        assert wd[0] == 1

    def test_weight_8_count_759(self, golay):
        """759 octads (weight-8 codewords)."""
        wd = golay.weight_distribution()
        assert wd[8] == 759

    def test_weight_12_count_2576(self, golay):
        """2576 dodecads (weight-12 codewords)."""
        wd = golay.weight_distribution()
        assert wd[12] == 2576

    def test_weight_16_count_759(self, golay):
        """759 hexadecads (complements of octads)."""
        wd = golay.weight_distribution()
        assert wd[16] == 759

    def test_weight_24_count_1(self, golay):
        """Exactly one weight-24 codeword (all ones)."""
        wd = golay.weight_distribution()
        assert wd[24] == 1

    def test_total_weight_distribution(self, golay):
        """Total counts sum to 4096."""
        wd = golay.weight_distribution()
        assert sum(wd.values()) == 4096

    def test_symmetric_distribution(self, golay):
        """Weight distribution is symmetric: A_w = A_{24-w}."""
        wd = golay.weight_distribution()
        for w in range(25):
            assert wd.get(w, 0) == wd.get(24 - w, 0)

    def test_golay_verify_all_pass(self, golay):
        results = golay.verify()
        for key, val in results.items():
            assert val, f"Golay verification failed: {key}"


# ------------------------------------------------------------------
# Leech Lattice Tests
# ------------------------------------------------------------------

class TestLeechLatticeBasic:
    """Basic Leech lattice properties without full enumeration."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=False)

    def test_dimension_24(self, leech):
        assert leech.dimension == 24

    def test_kissing_number_196560(self, leech):
        assert leech.kissing_number == 196_560

    def test_n_gen_equals_3(self, leech):
        assert leech.n_gen_from_lattice() == 3

    def test_covering_radius_sqrt2(self, leech):
        assert np.isclose(leech.covering_radius(), np.sqrt(2.0))

    def test_automorphism_group_order(self, leech):
        assert leech.automorphism_group_order() == 8_315_553_613_086_720_000


class TestLeechThetaSeries:
    """Verify theta series coefficients."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=False)

    def test_no_norm2_vectors(self, leech):
        """Defining property: no vectors of norm² = 2."""
        theta = leech.theta_series_coefficients(3)
        assert theta[1] == (2, 0)

    def test_origin_count(self, leech):
        theta = leech.theta_series_coefficients(1)
        assert theta[0] == (0, 1)

    def test_kissing_number_from_theta(self, leech):
        theta = leech.theta_series_coefficients(3)
        assert theta[2] == (4, 196_560)

    def test_second_shell(self, leech):
        theta = leech.theta_series_coefficients(4)
        assert theta[3] == (6, 16_773_120)

    def test_third_shell(self, leech):
        theta = leech.theta_series_coefficients(5)
        assert theta[4] == (8, 398_034_000)


class TestLeechPackingDensity:
    """Verify packing density = π¹² / 12!."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=False)

    def test_packing_density_value(self, leech):
        expected = math.pi ** 12 / math.factorial(12)
        assert np.isclose(leech.packing_density(), expected)

    def test_packing_density_approximate(self, leech):
        """Packing density ≈ 0.001930."""
        assert np.isclose(leech.packing_density(), 0.001930, atol=1e-5)


class TestLeechMinimalVectors:
    """Tests with actual minimal vector enumeration."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=True)

    def test_computed_vectors_exist(self, leech):
        assert leech.computed_vectors_count > 0

    def test_octad_vectors_count(self, leech):
        """Should have 97,152 vectors from octads + 1,104 from diagonals = 98,256."""
        # Octad type: 759 octads × 128 sign patterns = 97,152
        # Diagonal type: C(24,2) × 4 = 1,104
        expected = 97_152 + 1_104
        assert leech.computed_vectors_count == expected

    def test_all_computed_vectors_norm_32(self, leech):
        """All computed vectors have norm² = 32 (integer coords)."""
        norms_sq = np.sum(leech.minimal_vectors ** 2, axis=1)
        assert np.allclose(norms_sq, 32.0)

    def test_no_duplicate_vectors(self, leech):
        """All computed vectors are distinct."""
        vecs = set(map(tuple, leech.minimal_vectors.astype(int)))
        assert len(vecs) == leech.computed_vectors_count

    def test_closed_under_negation(self, leech):
        """For every computed vector v, -v is also computed."""
        vec_set = set(map(tuple, leech.minimal_vectors.astype(int)))
        for v in leech.minimal_vectors:
            neg = tuple((-v).astype(int))
            assert neg in vec_set


class TestLeechVerification:
    """Run the built-in verification suite."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=True)

    def test_all_checks_pass(self, leech):
        results = leech.verify()
        for key, val in results.items():
            if key == 'computed_count':
                continue  # This is an info field, not a boolean check
            assert val, f"Leech verification failed: {key}"
