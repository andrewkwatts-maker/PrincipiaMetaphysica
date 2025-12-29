"""
Pytest Configuration for Principia Metaphysica Tests

Shared fixtures and configuration for all test modules.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# Session-level Configuration
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "requires_data: marks tests that require actual data files"
    )


# =============================================================================
# Shared Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def test_data_path():
    """Path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def simulations_path():
    """Path to simulations directory."""
    return Path(__file__).parent.parent


# =============================================================================
# Test Output Configuration
# =============================================================================

@pytest.fixture(autouse=True)
def reset_warnings():
    """Reset warnings for each test."""
    import warnings
    warnings.resetwarnings()
    yield


# =============================================================================
# Coverage Helpers
# =============================================================================

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark tests that use temp files
        if "temp_" in str(item.nodeid):
            item.add_marker(pytest.mark.integration)

        # Mark tests that require actual data files
        if "requires actual data files" in str(item.obj.__doc__ or "").lower():
            item.add_marker(pytest.mark.requires_data)
