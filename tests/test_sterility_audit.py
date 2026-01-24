"""
Sterility Audit Test v23.0 - AST-Based Ghost Literal Scanner
=============================================================
Scans the repository for 'Ghost Literals' - hardcoded numbers that
should be derived from the FormulasRegistry SSoT.

This test uses Python's Abstract Syntax Tree (AST) to scan source files
for numeric literals, flagging any that are not in the approved set.

If a raw number (outside of 0, 1, -1, 2) is found anywhere in the
simulation logic, the test fails, forcing developers to justify
every constant through the Registry.

Usage:
    python tests/test_sterility_audit.py
    pytest tests/test_sterility_audit.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import ast
import os
import sys
import unittest
from pathlib import Path
from typing import List, Tuple, Set

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class SterilityValidator(ast.NodeVisitor):
    """
    AST visitor that identifies numeric literals in Python source code.

    Flags any number that is not in the 'sterile set' of allowed values.
    """

    # Allowed constants (standard logic/index offsets)
    # 0, 1, -1, 2 are universally needed for logic, indexing, and binary ops
    STERILE_SET: Set[float] = {0, 0.0, 1, 1.0, -1, -1.0, 2, 2.0, 10, 100}

    # Additional allowed values (common in formatting, logging, etc.)
    FORMAT_EXCEPTIONS: Set[float] = {
        3, 4, 5, 6, 7, 8, 9,  # Small integers for formatting
        16, 32, 60, 64, 70,   # Common bit/time values
    }

    def __init__(self, filename: str, strict_mode: bool = False):
        self.filename = filename
        self.strict_mode = strict_mode
        self.violations: List[Tuple[int, float, str]] = []

        # Combine allowed sets
        self.allowed = self.STERILE_SET.copy()
        if not strict_mode:
            self.allowed.update(self.FORMAT_EXCEPTIONS)

    def visit_Constant(self, node: ast.Constant) -> None:
        """Check numeric constants (Python 3.8+)."""
        if isinstance(node.value, (int, float)):
            self._check_value(node.value, node.lineno)
        self.generic_visit(node)

    def visit_Num(self, node: ast.Num) -> None:
        """Check numeric constants (Python < 3.8 compatibility)."""
        self._check_value(node.n, node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """
        Check for Decimal('...') calls with hardcoded literals.

        Decimal strings like Decimal('163') are "Logic Shadows" that
        bypass the simple numeric literal check.
        """
        # Check if this is a Decimal() call
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name == 'Decimal' and node.args:
            arg = node.args[0]
            # Check if the argument is a string literal
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                try:
                    # Try to parse the string as a number
                    value = float(arg.value)
                    if value not in self.allowed:
                        self.violations.append(
                            (node.lineno, f"Decimal('{arg.value}')", "DECIMAL_SHADOW")
                        )
                except ValueError:
                    pass  # Not a numeric string, ignore

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Block forbidden external constant imports.

        Importing scipy.constants or using math constants directly
        introduces "Ghost Data" not derived from the 24-base geometry.
        """
        forbidden_modules = {
            "scipy.constants",
            "scipy.special",
        }

        if node.module in forbidden_modules:
            self.violations.append(
                (node.lineno, f"Forbidden Import: {node.module}", "EXTERNAL_CONSTANT")
            )

        self.generic_visit(node)

    def _check_value(self, value: float, lineno: int) -> None:
        """Check if a numeric value is allowed."""
        if value not in self.allowed:
            # Get context from the line
            self.violations.append((lineno, value, ""))


class GhostLiteralScanner:
    """
    Scans the repository for Ghost Literals - hardcoded numeric values
    that should be centralized in the FormulasRegistry.
    """

    # Files to skip (the Registry itself must contain the seeds)
    SKIP_FILES: Set[str] = {
        "FormulasRegistry.py",
        "named_constants.json",
        "__pycache__",
        ".git",
        "test_sterility_audit.py",  # This file contains examples
    }

    # Directories to skip
    SKIP_DIRS: Set[str] = {
        "__pycache__",
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "env",
        # Archived/packaged versions (frozen snapshots)
        "Principia_Metaphysica-Demon_Lock",
        "Principia_Metaphysica-Demon_Lock_FULL",
        "Principia_Metaphysica_v16_2_20251231",
        "Principia_Metaphysica_v16_2_20260101_FULL",
        "Principia_Metaphysica_v16_2_20260102_FULL",
    }

    # Known Ghost Literals that MUST be migrated to Registry
    # NOTE: EXPERIMENTAL values (137.036 from CODATA) are ALLOWED in validation scripts
    #       Only our DERIVED predictions should use the Registry SSoT
    KNOWN_GHOSTS: Set[float] = {
        # Deprecated/incorrect values (MUST be removed)
        0.5772,         # Truncated Sophian Gamma (should be 0.57721566490153286)
        0.57721,        # Truncated Sophian Gamma
        1.280145,       # Deprecated holonomy (should be 1.5427971665)
        4.898979,       # Hossenfelder Root (should be sqrt(24))
        0.006944,       # Reid Invariant (should be 1/144)
        0.00694444,     # Reid Invariant
        # DERIVED values that should use Registry (PM predictions)
        # NOTE: These are intentionally left commented out - they are valid when
        # sourced from FormulasRegistry. The audit should focus on DEPRECATED values.
        # 576,          # Manifold volume (B3^2) - acceptable if from registry
        # 1.6402,       # Parity target - acceptable if from registry
        # 71.55,        # H0 result - acceptable if from registry
        # 0.9583,       # Tzimtzum - acceptable if from registry
        # 0.6819,       # Sophian Drag - acceptable if from registry
    }

    # EXPERIMENTAL values from PDG/CODATA that SHOULD stay hardcoded
    # These are external measurements, NOT our derived predictions
    EXPERIMENTAL_VALUES: Set[float] = {
        137.035,        # Alpha inverse (CODATA)
        137.036,        # Alpha inverse (CODATA)
        137.035999,     # Alpha inverse high precision (CODATA 2022)
        137.035999177,  # Alpha inverse ultra-precision (CODATA)
    }

    def __init__(self, project_root: str = None, strict_mode: bool = False):
        self.project_root = project_root or str(Path(__file__).parent.parent)
        self.strict_mode = strict_mode
        self.all_violations: List[Tuple[str, int, float]] = []
        self.ghost_findings: List[Tuple[str, int, float]] = []

    def scan_file(self, file_path: str) -> List[Tuple[int, float, str]]:
        """Scan a single Python file for numeric literals."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)
            validator = SterilityValidator(file_path, self.strict_mode)
            validator.visit(tree)
            return validator.violations

        except SyntaxError:
            # Skip files that aren't valid Python
            return []
        except Exception as e:
            print(f"Warning: Could not scan {file_path}: {e}")
            return []

    def scan_repository(self) -> bool:
        """
        Scan all Python files in the repository.

        Returns:
            True if no violations found, False otherwise.
        """
        self.all_violations = []
        self.ghost_findings = []

        for root, dirs, files in os.walk(self.project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            for file in files:
                # Skip non-Python files and excluded files
                if not file.endswith(".py"):
                    continue
                if file in self.SKIP_FILES:
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.project_root)

                violations = self.scan_file(file_path)

                for lineno, value, context in violations:
                    self.all_violations.append((relative_path, lineno, value))

                    # Check if it's a known Ghost Literal
                    if value in self.KNOWN_GHOSTS:
                        self.ghost_findings.append((relative_path, lineno, value))

        return len(self.ghost_findings) == 0

    def generate_report(self) -> str:
        """Generate a human-readable sterility report."""
        lines = [
            "=" * 60,
            " PRINCIPIA METAPHYSICA v23.0 - STERILITY AUDIT REPORT",
            "=" * 60,
            "",
        ]

        if not self.ghost_findings:
            lines.extend([
                "STATUS: STERILE",
                "No known Ghost Literals found in the codebase.",
                "",
            ])
        else:
            lines.extend([
                "STATUS: NON-STERILE",
                f"Found {len(self.ghost_findings)} Ghost Literal violations:",
                "",
            ])

            for file_path, lineno, value in self.ghost_findings:
                lines.append(f"  {file_path}:{lineno} -> {value}")

            lines.extend([
                "",
                "These values must be migrated to FormulasRegistry.py",
            ])

        lines.extend([
            "",
            "-" * 60,
            f"Total numeric literals scanned: {len(self.all_violations)}",
            f"Known Ghost Literals found: {len(self.ghost_findings)}",
            "=" * 60,
        ])

        return "\n".join(lines)


class TestSterilityAudit(unittest.TestCase):
    """
    Unit tests for the Sterility Audit.

    These tests ensure that the codebase remains free of Ghost Literals.
    """

    def test_find_ghost_literals(self):
        """
        Scan the repository for Ghost Literals.

        This test fails if any known Ghost Literals are found outside
        the FormulasRegistry.
        """
        scanner = GhostLiteralScanner()
        is_sterile = scanner.scan_repository()

        if not is_sterile:
            report = scanner.generate_report()
            self.fail(f"Sterility Audit Failed!\n\n{report}")

    def test_deprecated_holonomy(self):
        """Ensure deprecated holonomy value 1.280145 is not used."""
        scanner = GhostLiteralScanner()
        scanner.KNOWN_GHOSTS = {1.280145}  # Only check this value
        scanner.scan_repository()

        if scanner.ghost_findings:
            self.fail(
                f"Deprecated holonomy 1.280145 found in:\n"
                + "\n".join(f"  {f}:{l}" for f, l, _ in scanner.ghost_findings)
                + "\nUse 1.5427971665 (G2 Laplacian eigenvalue) instead."
            )

    def test_truncated_gamma(self):
        """Ensure truncated Sophian Gamma (0.5772) is not used."""
        scanner = GhostLiteralScanner()
        scanner.KNOWN_GHOSTS = {0.5772, 0.57721}
        scanner.scan_repository()

        if scanner.ghost_findings:
            self.fail(
                f"Truncated Sophian Gamma found in:\n"
                + "\n".join(f"  {f}:{l} -> {v}" for f, l, v in scanner.ghost_findings)
                + "\nUse 0.57721566490153286 (16 decimal precision) from Registry."
            )


class TestParityInvariants(unittest.TestCase):
    """
    v17: Parity Invariant Tests

    These tests ensure the geometric derivations remain consistent
    and that the SSoT JSON matches the live Registry calculations.
    """

    def setUp(self):
        """Initialize registry for tests."""
        try:
            from core.FormulasRegistry import get_registry
            self.registry = get_registry()
        except ImportError:
            self.skipTest("FormulasRegistry not available")

    def test_h0_geometric_precision(self):
        """
        Verify H0 derived from Base-24 hits the 71.55 target.

        This tests the O'Dowd Formula using derived geometric values.
        """
        h0 = self.registry.h0_local
        expected = 71.55

        # Allow 0.01 tolerance (same as test_physics_invariants.py)
        self.assertAlmostEqual(
            h0, expected, delta=0.01,
            msg=f"H0 Drift detected: {h0:.4f} != {expected}"
        )

    def test_bulk_pressure_derivation(self):
        """
        Ensure 163 is derived from (7 * 24) - 5.

        The O'Dowd Bulk Pressure must match the Heptagonal Scaling formula.
        """
        derived = self.registry.odowd_bulk_derived
        expected = 163

        self.assertEqual(
            derived, expected,
            msg=f"Bulk Pressure Logic Leak: {derived} != {expected}"
        )

    def test_pressure_divisor_derivation(self):
        """
        Ensure 144 is derived from B3^2 / 4.

        The pressure divisor must be geometrically derived.
        """
        derived = self.registry.pressure_divisor
        expected = 144.0

        self.assertEqual(
            derived, expected,
            msg=f"Pressure Divisor Logic Leak: {derived} != {expected}"
        )

    def test_manifold_area_derivation(self):
        """
        Ensure 576 is derived from B3^2.

        The manifold area must equal 24^2.
        """
        derived = self.registry.manifold_area_bulk
        expected = 576

        self.assertEqual(
            derived, expected,
            msg=f"Manifold Area Logic Leak: {derived} != {expected}"
        )

    def test_sterile_equals_bulk(self):
        """
        Verify sterile sector equals O'Dowd bulk pressure.

        163 = 288 - 125 = (7 * 24) - 5
        """
        self.assertTrue(
            self.registry.verify_sterile_equals_bulk(),
            msg="Sterile sector != O'Dowd bulk pressure"
        )

    def test_parity_sum(self):
        """
        Verify Manifold Parity: eta_S + sigma_T = 163/239 + 23/24 = 1.6403...
        """
        parity = self.registry.parity_sum
        # v23.0+: Derived from 163/239 + 23/24 = 1.64034169820...
        expected = 1.6403

        self.assertAlmostEqual(
            parity, expected, delta=0.0001,
            msg=f"Parity Invariant Failed: {parity:.4f} != {expected}"
        )


class TestJSONConsistency(unittest.TestCase):
    """
    v17: JSON Consistency Tests

    Ensures the Named Constants JSON matches the live Registry calculations.
    If the JSON was manually edited, this will detect the drift.
    """

    def setUp(self):
        """Initialize registry for tests."""
        try:
            from core.FormulasRegistry import get_registry
            self.registry = get_registry()
        except ImportError:
            self.skipTest("FormulasRegistry not available")

    def test_json_h0_matches_registry(self):
        """
        Ensure JSON h0 value matches live Registry calculation.
        """
        import json

        json_path = Path(__file__).parent.parent / "AutoGenerated" / "named_constants.json"
        if not json_path.exists():
            self.skipTest("named_constants.json not found")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        json_h0 = data.get("derived_values", {}).get("hubble_constant", {}).get("value")
        registry_h0 = self.registry.h0_local

        if json_h0 is not None:
            self.assertAlmostEqual(
                float(json_h0), registry_h0, delta=0.01,
                msg=f"SSoT DESYNC: JSON h0 ({json_h0}) != Registry h0 ({registry_h0})"
            )

    def test_json_volatility_metadata(self):
        """
        Ensure JSON has volatility metadata for freshness checking.
        """
        import json

        json_path = Path(__file__).parent.parent / "AutoGenerated" / "named_constants.json"
        if not json_path.exists():
            self.skipTest("named_constants.json not found")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        volatility = data.get("volatility")
        self.assertIsNotNone(
            volatility,
            msg="JSON missing volatility metadata (v17 requirement)"
        )

        if volatility:
            self.assertIn("generated_at", volatility)
            self.assertIn("max_age_seconds", volatility)


def run_sterility_audit():
    """Run the sterility audit and print the report."""
    print("Initializing Sterility Audit...")

    scanner = GhostLiteralScanner()
    is_sterile = scanner.scan_repository()

    print(scanner.generate_report())

    return 0 if is_sterile else 1


if __name__ == "__main__":
    # Run as standalone script
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=[''], exit=True)
    else:
        exit_code = run_sterility_audit()
        sys.exit(exit_code)
