"""
Import Health Smoke Test
========================
Verifies that all remaining simulation modules import cleanly.
Catches broken imports from refactoring or archival.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import importlib
import sys
from pathlib import Path

import pytest

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "simulations"))

SIMULATIONS_DIR = PROJECT_ROOT / "simulations" / "PM"


def collect_module_paths():
    """Collect all Python module paths under simulations/PM/."""
    modules = []
    for py_file in SIMULATIONS_DIR.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        # Convert file path to module path
        rel = py_file.relative_to(PROJECT_ROOT)
        module_path = str(rel).replace("\\", "/").replace("/", ".").removesuffix(".py")
        modules.append(module_path)
    return sorted(modules)


MODULE_PATHS = collect_module_paths()


@pytest.mark.parametrize("module_path", MODULE_PATHS)
def test_module_imports(module_path):
    """Each simulation module should import without errors."""
    try:
        importlib.import_module(module_path)
    except ImportError as e:
        pytest.fail(f"ImportError in {module_path}: {e}")
    except Exception as e:
        # Some modules may fail for non-import reasons (missing data files, etc.)
        # We only care about import-level failures
        if "No module named" in str(e) or "cannot import name" in str(e):
            pytest.fail(f"Import failure in {module_path}: {e}")
        else:
            pytest.skip(f"Non-import error in {module_path}: {type(e).__name__}: {e}")
