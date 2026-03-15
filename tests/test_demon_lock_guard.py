"""
Unit Tests for DemonLockGuard - Parameter Integrity Enforcement
===============================================================
Tests the guard rail validator that prevents parameter contamination.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations" / "core"))

from simulations.core.demon_lock_guard import DemonLockGuard
from simulations.core.FormulasRegistry import get_registry


@pytest.fixture
def guard():
    """Create a DemonLockGuard instance without JSON."""
    return DemonLockGuard(registry=get_registry())


class TestGuardInitialization:
    """Tests for guard initialization."""

    def test_guard_creates_with_registry(self, guard):
        """Guard initializes with a registry."""
        assert guard.registry is not None

    def test_guard_starts_with_no_violations(self, guard):
        """Fresh guard has no violations."""
        assert len(guard.violations) == 0

    def test_guard_starts_with_no_warnings(self, guard):
        """Fresh guard has no warnings."""
        assert len(guard.warnings) == 0

    def test_guard_has_parity_tolerance(self, guard):
        """Guard defines a parity tolerance."""
        assert guard.PARITY_TOLERANCE > 0
        assert guard.PARITY_TOLERANCE < 0.01


class TestExpectedParitySum:
    """Tests for the expected parity sum derivation."""

    def test_parity_sum_is_derived(self, guard):
        """Parity sum comes from registry, not hardcoded."""
        expected = guard.registry.parity_sum
        assert guard.EXPECTED_PARITY_SUM == expected

    def test_parity_sum_reasonable_range(self, guard):
        """Parity sum should be in a reasonable range (> 1, < 2)."""
        assert 1.0 < guard.EXPECTED_PARITY_SUM < 2.0


class TestJsonLoading:
    """Tests for JSON manifest loading."""

    def test_load_nonexistent_file(self, guard):
        """Loading a nonexistent JSON file records a violation."""
        result = guard.load_json("/nonexistent/path/constants.json")
        assert result is False
        assert len(guard.violations) > 0
        assert "not found" in guard.violations[0].lower() or "CRITICAL" in guard.violations[0]

    def test_data_empty_before_load(self, guard):
        """Data dict is empty before any JSON is loaded."""
        assert guard.data == {}
