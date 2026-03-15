"""
Unit Tests for Lattice Connections
====================================
Tests the mathematical connections between E8, Leech, G2, bridges,
and four-face structure — verifying the complete derivation chain.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.algebra.octonions import OctonionAlgebra, FANO_TRIPLES
from simulations.PM.algebra.e8_root_system import E8RootSystem
from simulations.PM.algebra.leech_lattice import LeechLattice
from simulations.PM.geometry.g2_differential import G2DifferentialGeometry, G2_TRIPLES
from simulations.PM.geometry.bridge_geometry import BridgeSystem
from simulations.PM.geometry.four_face_structure import FourFaceG2Structure
from simulations.PM.algebra.lattice_bridge import LatticeBridgeConnector


# ------------------------------------------------------------------
# Octonion Algebra
# ------------------------------------------------------------------

class TestOctonionAlgebra:
    """Tests for octonion algebra connecting E8 to G2."""

    @pytest.fixture(scope="class")
    def octonions(self):
        return OctonionAlgebra()

    def test_seven_triples(self, octonions):
        assert len(FANO_TRIPLES) == 7

    def test_structure_constants_shape(self, octonions):
        C = octonions.structure_constants
        assert C.shape == (7, 7, 7)

    def test_structure_constants_antisymmetric(self, octonions):
        C = octonions.structure_constants
        # C_{ijk} = -C_{jik}
        assert np.allclose(C, -np.transpose(C, (1, 0, 2)))
        # C_{ijk} = -C_{ikj}
        assert np.allclose(C, -np.transpose(C, (0, 2, 1)))

    def test_fano_triples_match_g2(self, octonions):
        """Fano plane triples must match G2_TRIPLES from g2_differential.py."""
        g2_indices = [(i, j, k) for (i, j, k, s) in G2_TRIPLES]
        for triple in FANO_TRIPLES:
            assert triple in g2_indices, f"Fano triple {triple} not in G2_TRIPLES"

    def test_structure_constants_match_g2_phi(self, octonions):
        """Geometric structure constants must equal the standard G2 3-form φ_{ijk}."""
        C = octonions.structure_constants
        phi = G2DifferentialGeometry._standard_phi()
        assert np.allclose(C, phi)

    def test_multiplication_constants_differ_by_one_sign(self, octonions):
        """Multiplication constants differ from geometric by sign on triple (1,3,5)."""
        C_geom = octonions.structure_constants
        C_mult = octonions.multiplication_constants
        # They should differ only where indices involve the (1,3,5) triple
        diff = C_mult - C_geom
        # The nonzero diff entries are at the 6 permutations of (1,3,5)
        num_diff = np.sum(np.abs(diff) > 0.5)
        assert num_diff == 6  # 3 cyclic + 3 anti-cyclic permutations

    def test_g2_structure_as_3form(self, octonions):
        phi = octonions.g2_structure_as_3form()
        standard = G2DifferentialGeometry._standard_phi()
        assert np.allclose(phi, standard)

    def test_norm_multiplicative(self, octonions):
        """Octonion norm is multiplicative: |ab|² = |a|²|b|²."""
        rng = np.random.RandomState(42)
        for _ in range(10):
            a = rng.randn(8)
            b = rng.randn(8)
            ab = octonions.multiply(a, b)
            assert np.isclose(
                octonions.norm_squared(ab),
                octonions.norm_squared(a) * octonions.norm_squared(b),
                rtol=1e-10
            )

    def test_alternative(self, octonions):
        """Octonions are alternative: a(ab) = a²b, (ab)b = ab²."""
        rng = np.random.RandomState(42)
        a = rng.randn(8)
        b = rng.randn(8)
        a2 = octonions.multiply(a, a)
        b2 = octonions.multiply(b, b)
        assert np.allclose(
            octonions.multiply(a, octonions.multiply(a, b)),
            octonions.multiply(a2, b), atol=1e-10
        )
        assert np.allclose(
            octonions.multiply(octonions.multiply(a, b), b),
            octonions.multiply(a, b2), atol=1e-10
        )

    def test_not_associative(self, octonions):
        """Octonions are NOT associative in general."""
        rng = np.random.RandomState(42)
        a, b, c = rng.randn(8), rng.randn(8), rng.randn(8)
        lhs = octonions.multiply(octonions.multiply(a, b), c)
        rhs = octonions.multiply(a, octonions.multiply(b, c))
        assert not np.allclose(lhs, rhs, atol=1e-10)

    def test_conjugate_norm(self, octonions):
        """x · x̄ = |x|² (real part only)."""
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
        xx_bar = octonions.multiply(x, octonions.conjugate(x))
        assert np.isclose(xx_bar[0], octonions.norm_squared(x))
        assert np.allclose(xx_bar[1:], 0, atol=1e-10)

    def test_project_to_imaginary(self, octonions):
        v = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        proj = OctonionAlgebra.project_to_imaginary(v)
        assert proj.shape == (7,)
        np.testing.assert_array_equal(proj, v[1:])

    def test_embed_imaginary(self, octonions):
        v = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
        embedded = OctonionAlgebra.embed_imaginary(v)
        assert embedded.shape == (8,)
        assert embedded[0] == 0.0
        np.testing.assert_array_equal(embedded[1:], v)

    def test_verify(self, octonions):
        checks = octonions.verify()
        for key, val in checks.items():
            if key != 'not_associative':  # This is True = good
                assert val, f"Octonion verification failed: {key}"


# ------------------------------------------------------------------
# E8 → G2 via Octonions
# ------------------------------------------------------------------

class TestE8ToG2:
    """Tests for E8 root projection to Im(O) and G2 derivation."""

    @pytest.fixture(scope="class")
    def e8(self):
        return E8RootSystem()

    def test_projection_shape(self, e8):
        proj = e8.project_to_imaginary_octonions()
        assert proj.shape == (240, 7)

    def test_projected_norms_bounded(self, e8):
        """Projected norms ≤ original norm² = 2."""
        proj = e8.project_to_imaginary_octonions()
        norms_sq = np.sum(proj ** 2, axis=1)
        assert np.all(norms_sq <= 2.0 + 1e-10)

    def test_g2_from_e8_produces_valid_g2(self, e8):
        g2 = G2DifferentialGeometry.from_e8(e8)
        verify = g2.verify()
        for key, val in verify.items():
            if key != 'hodge_max_error':
                assert val, f"G2 from E8 failed: {key}"

    def test_g2_from_e8_matches_standard(self, e8):
        """G2 from E8 must produce the same metric as default G2."""
        g2_e8 = G2DifferentialGeometry.from_e8(e8)
        g2_std = G2DifferentialGeometry()
        np.testing.assert_allclose(g2_e8.compute_metric(), g2_std.compute_metric())

    def test_g2_e8_compatibility(self, e8):
        g2 = G2DifferentialGeometry.from_e8(e8)
        compat = g2.verify_e8_compatibility(e8)
        assert compat['projection_shape']  # True if shape == (240, 7)
        assert compat['norms_bounded']
        assert compat['metric_is_identity']
        assert compat['phi_well_defined']
        assert compat['structure_constants_match_phi']

    def test_g2_invariant_check(self, e8):
        checks = e8.g2_invariant_check()
        assert checks['norms_bounded']
        assert checks['phi_acts_on_projections']
        assert checks['phi_gives_flat_metric']

    def test_e8_sublattice_basis_shapes(self, e8):
        for idx in range(3):
            basis = e8.e8_sublattice_basis(idx)
            assert basis.shape == (8, 24)

    def test_e8_sublattice_orthogonal(self, e8):
        """Sublattice bases are in disjoint coordinate blocks."""
        for i in range(3):
            for j in range(i + 1, 3):
                bi = e8.e8_sublattice_basis(i)
                bj = e8.e8_sublattice_basis(j)
                overlap = np.sum(bi * bj)
                assert abs(overlap) < 1e-10


# ------------------------------------------------------------------
# Leech → E8 Triple Decomposition
# ------------------------------------------------------------------

class TestLeechE8Decomposition:
    """Tests for Leech lattice decomposition into E8 blocks."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=False)

    def test_e8_triple_dimensions(self, leech):
        result = leech.decompose_e8_triple()
        assert result['dimensions'] == [8, 8, 8]
        assert result['total_dim'] == 24

    def test_e8_triple_orthogonal(self, leech):
        result = leech.decompose_e8_triple()
        assert result['orthogonal']

    def test_e8_triple_each_is_e8(self, leech):
        result = leech.decompose_e8_triple()
        assert result['each_is_e8']

    def test_e8_triple_spans_R24(self, leech):
        result = leech.decompose_e8_triple()
        assert result['spans_R24']

    def test_e8_pair_480_roots(self, leech):
        result = leech.extract_e8_pair()
        assert result['num_roots'] == 480

    def test_e8_pair_all_norm2(self, leech):
        result = leech.extract_e8_pair()
        assert result['all_norm2']

    def test_e8_pair_remaining_8d(self, leech):
        result = leech.extract_e8_pair()
        assert result['remaining_dim'] == 8

    def test_e8_pair_heterotic(self, leech):
        result = leech.extract_e8_pair()
        assert result['heterotic_compatible']


# ------------------------------------------------------------------
# Leech → 12 Bridge Pairs
# ------------------------------------------------------------------

class TestLeechToBridges:
    """Tests for Leech decomposition into 12 bridge pairs."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=False)

    def test_12_bridge_pairs(self, leech):
        result = leech.decompose_bridge_pairs()
        assert result['num_bridges'] == 12

    def test_bridge_dim_24(self, leech):
        result = leech.decompose_bridge_pairs()
        assert result['total_dim'] == 24

    def test_bridge_moduli_shape(self, leech):
        result = leech.decompose_bridge_pairs()
        assert result['moduli'].shape == (12, 3)

    def test_bridge_moduli_valid(self, leech):
        """All L1 > 0, L2 > 0, 0 < θ < π."""
        result = leech.decompose_bridge_pairs()
        moduli = result['moduli']
        assert np.all(moduli[:, 0] > 0)  # L1
        assert np.all(moduli[:, 1] > 0)  # L2
        assert np.all(moduli[:, 2] > 0)  # theta
        assert np.all(moduli[:, 2] < math.pi)  # theta

    def test_bridge_system_from_leech(self, leech):
        system = BridgeSystem.from_leech_decomposition(leech)
        assert len(system.bridges) == 12

    def test_bridge_system_signature(self, leech):
        system = BridgeSystem.from_leech_decomposition(leech)
        sig = system.metric_signature()
        assert sig == (26, 1)

    def test_bridge_system_27d(self, leech):
        system = BridgeSystem.from_leech_decomposition(leech)
        assert system.total_bridge_dimensions + 3 == 27

    def test_verify_leech_origin(self, leech):
        system = BridgeSystem.from_leech_decomposition(leech)
        checks = system.verify_leech_origin(leech)
        for key, val in checks.items():
            assert val, f"Leech origin check failed: {key}"

    def test_e8_grouping(self, leech):
        result = leech.decompose_bridge_pairs()
        grouping = result['e8_grouping']
        assert grouping[0] == [0, 1, 2, 3]
        assert grouping[1] == [4, 5, 6, 7]
        assert grouping[2] == [8, 9, 10, 11]


# ------------------------------------------------------------------
# Four-Face Grouping
# ------------------------------------------------------------------

class TestFourFaceGrouping:
    """Tests for 4 faces × 3 bridges grouping."""

    @pytest.fixture(scope="class")
    def leech(self):
        return LeechLattice(compute_minimal=False)

    def test_four_faces(self, leech):
        result = leech.four_face_grouping()
        assert result['num_faces'] == 4

    def test_three_bridges_per_face(self, leech):
        result = leech.four_face_grouping()
        assert result['bridges_per_face'] == 3

    def test_all_bridges_covered(self, leech):
        result = leech.four_face_grouping()
        assert result['all_bridges_covered']

    def test_no_duplicate_bridges(self, leech):
        result = leech.four_face_grouping()
        assert result['no_duplicates']

    def test_faces_cross_e8_copies(self, leech):
        """Each face has one bridge from each E8 copy."""
        result = leech.four_face_grouping()
        assert result['cross_e8']

    def test_n_gen_consistent(self, leech):
        result = leech.four_face_grouping()
        assert result['n_gen_consistent']

    def test_h11_consistent(self, leech):
        result = leech.four_face_grouping()
        assert result['h11_consistent']

    def test_face_assignments(self, leech):
        """Face i = {bridge i, bridge i+4, bridge i+8}."""
        result = leech.four_face_grouping()
        faces = result['faces']
        assert faces[0] == [0, 4, 8]
        assert faces[1] == [1, 5, 9]
        assert faces[2] == [2, 6, 10]
        assert faces[3] == [3, 7, 11]

    def test_face_moduli_from_bridges(self, leech):
        decomp = leech.decompose_bridge_pairs()
        grouping = leech.four_face_grouping()
        face_moduli = FourFaceG2Structure.compute_face_moduli_from_bridges(
            decomp['moduli'], grouping['faces']
        )
        assert len(face_moduli) == 4
        assert all(T > 0 for T in face_moduli)

    def test_leakage_from_lattice(self, leech):
        decomp = leech.decompose_bridge_pairs()
        grouping = leech.four_face_grouping()
        alpha_leak = FourFaceG2Structure.compute_leakage_from_lattice(
            decomp['moduli'], grouping['faces']
        )
        expected = 1.0 / math.sqrt(6.0)
        assert np.isclose(alpha_leak, expected)


# ------------------------------------------------------------------
# Full Derivation Chain
# ------------------------------------------------------------------

class TestFullChain:
    """Tests for the complete LatticeBridgeConnector derivation chain."""

    @pytest.fixture(scope="class")
    def connector(self):
        c = LatticeBridgeConnector()
        c.derive_all()
        return c

    def test_chain_runs(self, connector):
        assert connector._results is not None

    def test_chain_valid(self, connector):
        assert connector._results['chain_valid']

    def test_e8_valid(self, connector):
        assert connector._results['e8']['valid']

    def test_octonions_valid(self, connector):
        assert connector._results['octonions']['valid']

    def test_g2_from_e8_compatible(self, connector):
        assert connector._results['g2_from_e8']['e8_compatible']

    def test_e8_triple(self, connector):
        r = connector._results['e8_triple']
        assert r['orthogonal']
        assert r['each_is_e8']
        assert r['spans_R24']

    def test_e8_pair(self, connector):
        r = connector._results['e8_pair']
        assert r['num_roots'] == 480
        assert r['all_norm2']

    def test_bridge_decomposition(self, connector):
        r = connector._results['bridge_decomposition']
        assert r['num_bridges'] == 12
        assert r['total_dim'] == 24

    def test_bridges_from_leech(self, connector):
        r = connector._results['bridges_from_leech']
        assert r['signature_26_1']
        assert r['moduli_valid']

    def test_four_faces(self, connector):
        r = connector._results['four_faces']
        assert r['num_faces'] == 4
        assert r['bridges_per_face'] == 3
        assert r['cross_e8']

    def test_alpha_leak(self, connector):
        r = connector._results['face_moduli']
        assert r['alpha_leak_matches']

    def test_verify_chain(self, connector):
        checks = connector.verify_chain()
        for key, val in checks.items():
            assert val, f"Chain verification failed: {key}"

    def test_summary(self, connector):
        s = connector.summary()
        assert "Chain valid: True" in s
