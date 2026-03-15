"""
Unit Tests for FormulasRegistry - Core Infrastructure
=====================================================
Tests the Single Source of Truth (SSoT) for correctness of
Ten Pillar Seeds, derived quantities, and precision context.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
from decimal import getcontext, ROUND_HALF_EVEN
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.core.FormulasRegistry import FormulasRegistry, get_registry, lock_geometric_context


@pytest.fixture(scope="module")
def registry():
    """Get the singleton FormulasRegistry instance."""
    return get_registry()


class TestPrecisionContext:
    """Tests for the geometric precision context."""

    def test_precision_is_64_digits(self):
        lock_geometric_context()
        ctx = getcontext()
        assert ctx.prec == 64

    def test_rounding_mode(self):
        lock_geometric_context()
        ctx = getcontext()
        assert ctx.rounding == ROUND_HALF_EVEN


class TestTenPillarSeeds:
    """Tests for the Ten Pillar Seeds - the ONLY hardcoded inputs."""

    def test_b3_equals_24(self, registry):
        """Third Betti number b3 (elder_kads) must be 24."""
        assert registry.elder_kads == 24

    def test_golden_ratio(self, registry):
        """Golden ratio phi = (1 + sqrt(5)) / 2."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        assert registry._phi == pytest.approx(expected, rel=1e-15)

    def test_demiurgic_coupling(self, registry):
        """kappa_Delta = B3/2 + 1/pi = 12.318..."""
        expected = 24 / 2 + 1 / math.pi
        assert registry.demiurgic_coupling == pytest.approx(expected, rel=1e-12)

    def test_tzimtzum_pressure(self, registry):
        """sigma_T = 23/24."""
        assert registry._tzimtzum_pressure == pytest.approx(23.0 / 24.0, rel=1e-15)

    def test_sophian_drag(self, registry):
        """eta_S = 163/239 (derived from b3)."""
        expected = 163.0 / 239.0
        assert registry._sophian_drag == pytest.approx(expected, rel=1e-12)

    def test_odowd_bulk_pressure(self, registry):
        """O'Dowd Bulk Pressure = 163."""
        assert registry._odowd_bulk_pressure == 163

    def test_penrose_hameroff_bridge(self, registry):
        """Penrose-Hameroff Bridge = 13."""
        assert registry._penrose_hameroff_bridge == 13

    def test_hossenfelder_root(self, registry):
        """Hossenfelder Root = sqrt(24)."""
        assert registry._hossenfelder_root == pytest.approx(math.sqrt(24), rel=1e-15)


class TestDerivedQuantities:
    """Tests for quantities derived from the Ten Pillar Seeds."""

    def test_parity_sum(self, registry):
        """Parity sum = sophian_drag + tzimtzum_pressure."""
        expected = 163.0 / 239.0 + 23.0 / 24.0
        assert registry.parity_sum == pytest.approx(expected, rel=1e-12)

    def test_n_gen_equals_3(self, registry):
        """Number of fermion generations must be 3."""
        assert registry.n_gen == 3

    def test_chi_eff_positive(self, registry):
        """Effective Euler characteristic must be positive."""
        assert registry.chi_eff > 0


class TestSingleton:
    """Tests that the registry is a proper singleton."""

    def test_get_registry_returns_same_instance(self):
        """Multiple calls to get_registry() return the same object."""
        r1 = get_registry()
        r2 = get_registry()
        assert r1 is r2

    def test_registry_has_required_attributes(self, registry):
        """Registry exposes all required seed attributes."""
        required = ['elder_kads', 'demiurgic_coupling', 'parity_sum', 'n_gen', 'chi_eff']
        for attr in required:
            assert hasattr(registry, attr), f"Registry missing attribute: {attr}"


class TestLegacyAliases:
    """Tests that legacy accessor names still work."""

    def test_b3_property(self, registry):
        """b3 property should equal elder_kads."""
        assert registry.b3 == registry.elder_kads
