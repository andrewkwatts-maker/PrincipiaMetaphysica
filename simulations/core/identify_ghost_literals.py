"""
Ghost Literal Hunter v17.2 - Identifies hardcoded constants that bypass SSoT
============================================================================
Scans Python files for hardcoded numeric literals that should be derived
from FormulasRegistry.

TARGET_LITERALS are DERIVED values that MUST come from the registry:
- 144 (chi_eff_total/pressure_divisor = B3^2/4)
- 163 (sterile_sector = (7*B3)-5)
- 288 (roots_total = shadow + christ)
- 71.55 / 71.549 (h0_local from O'Dowd formula)
- 576 (manifold_area = B3^2)
- 0.9583 (tzimtzum_pressure = 23/24)
- 0.6819 (sophian_drag)

EXCLUDED values (experimental constants from external sources):
- 137.036 (alpha inverse - from CODATA/PDG, not derived)

Usage:
    python core/identify_ghost_literals.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import os
import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any


class GhostLiteralHunter(ast.NodeVisitor):
    """
    AST visitor that identifies hardcoded numeric literals.

    This hunter finds DERIVED values that should come from FormulasRegistry
    but are instead hardcoded as magic numbers (Ghost Literals).
    """

    # DERIVED values that MUST come from FormulasRegistry SSoT
    TARGET_LITERALS = {
        144,      # chi_eff_total/pressure_divisor = B3^2/4
        163,      # sterile_sector = (7*B3)-5
        288,      # roots_total = shadow + christ
        71.549,   # h0_local (partial match)
        71.55,    # h0_local (rounded)
        576,      # manifold_area = B3^2
        0.9583,   # tzimtzum_pressure = 23/24
        0.6819,   # sophian_drag
    }

    # Experimental values from external sources - these are ALLOWED hardcoded
    EXPERIMENTAL_VALUES = {
        137.036,  # alpha inverse (CODATA/PDG)
        137.035999,  # Source: CODATA 2022 fine structure constant inverse (1/α = 137.035999...)
    }

    # Files/directories to exclude from scanning
    EXCLUDED_PATHS = {
        'Principia_Metaphysica-Demon_Lock',
        'Principia_Metaphysica-Demon_Lock_FULL',
        '__pycache__',
        '.git',
        'archived',
        'deprecated',
        'venv',
        '.venv',
    }

    # Prefixes for archived version directories (pattern matching)
    ARCHIVED_PREFIXES = (
        'Principia_Metaphysica_v',  # Matches: Principia_Metaphysica_v16_2_20260102_FULL etc.
    )

    # Test files where hardcoded values are EXPECTED (test fixtures)
    TEST_FIXTURE_FILES = {
        'test_value_context_audit.py',  # Defines KNOWN_DERIVED_VALUES as fixtures
        'test_sterility_audit.py',  # Tests against known values
        'test_physics_invariants.py',  # Validation test fixtures
        'test_core.py',  # Core tests with expected values
        'brane_alignment_audit.py',  # Test validation
        'omega_unwinding_test.py',  # Test validation
        'run_all_sterile_audits.py',  # Meta-audit orchestrator
        'topology_gap_check.py',  # Test validation
    }

    # SSoT source files where hardcoded values are the DEFINITION (not ghosts)
    SSOT_SOURCE_FILES = {
        'FormulasRegistry.py',  # THE source of truth - defines the values
        'identify_ghost_literals.py',  # Defines TARGET_LITERALS for hunting
        'verify_sterility_report.py',  # IndependentGeometricValidator uses raw seeds intentionally
    }

    def __init__(self, filename: str):
        self.filename = filename
        self.findings: List[Dict[str, Any]] = []

    def visit_Num(self, node: ast.Num) -> None:
        """Visit numeric literals (Python 3.7 and earlier)."""
        self._check_literal(node.n, node.lineno, node.col_offset)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        """Visit constant literals (Python 3.8+)."""
        if isinstance(node.value, (int, float)):
            self._check_literal(node.value, node.lineno, node.col_offset)
        self.generic_visit(node)

    def _check_literal(self, value: Any, lineno: int, col_offset: int) -> None:
        """Check if a numeric literal is a Ghost Literal."""
        # Skip experimental values (allowed hardcoded)
        for exp_val in self.EXPERIMENTAL_VALUES:
            if abs(value - exp_val) < 0.001:
                return

        # Check against target literals
        for target in self.TARGET_LITERALS:
            # Use tolerance for floating point comparison
            if isinstance(value, float) and isinstance(target, float):
                if abs(value - target) < 0.01:
                    self.findings.append({
                        'file': self.filename,
                        'line': lineno,
                        'column': col_offset,
                        'value': value,
                        'target': target,
                        'type': 'float_ghost'
                    })
            elif value == target:
                self.findings.append({
                    'file': self.filename,
                    'line': lineno,
                    'column': col_offset,
                    'value': value,
                    'target': target,
                    'type': 'exact_ghost'
                })


def scan_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Scan a single Python file for Ghost Literals.

    Args:
        filepath: Path to the Python file

    Returns:
        List of findings (Ghost Literal occurrences)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        hunter = GhostLiteralHunter(filepath)
        hunter.visit(tree)
        return hunter.findings
    except SyntaxError as e:
        print(f"  [WARN] Syntax error in {filepath}: {e}")
        return []
    except Exception as e:
        print(f"  [WARN] Could not parse {filepath}: {e}")
        return []


def should_exclude(path: str) -> bool:
    """Check if a path should be excluded from scanning."""
    path_parts = Path(path).parts
    for excluded in GhostLiteralHunter.EXCLUDED_PATHS:
        if excluded in path_parts:
            return True
    # Check for archived version prefixes
    for part in path_parts:
        for prefix in GhostLiteralHunter.ARCHIVED_PREFIXES:
            if part.startswith(prefix):
                return True
    return False


def is_test_fixture(filepath: str) -> bool:
    """Check if file is a test fixture where hardcoded values are expected."""
    filename = Path(filepath).name
    return filename in GhostLiteralHunter.TEST_FIXTURE_FILES


def is_ssot_source(filepath: str) -> bool:
    """Check if file is a SSoT source where values are DEFINED (not ghosts)."""
    filename = Path(filepath).name
    return filename in GhostLiteralHunter.SSOT_SOURCE_FILES


def scan_repository(root_dir: str = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Scan all Python files in the repository for Ghost Literals.

    Args:
        root_dir: Root directory to scan (defaults to project root)

    Returns:
        Dictionary mapping file paths to their findings
    """
    if root_dir is None:
        root_dir = str(Path(__file__).parent.parent)

    all_findings: Dict[str, List[Dict[str, Any]]] = {}
    files_scanned = 0

    print(f"\n{'='*70}")
    print(" GHOST LITERAL HUNTER v17.2 - Scanning for hardcoded constants")
    print(f"{'='*70}")
    print(f" Root: {root_dir}")
    print(f" Targets: {sorted(GhostLiteralHunter.TARGET_LITERALS)}")
    print(f"{'-'*70}")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded directories
        if should_exclude(dirpath):
            continue

        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)

                # Skip if path contains excluded directories
                if should_exclude(filepath):
                    continue

                # Skip test fixtures (where hardcoded values are expected)
                if is_test_fixture(filepath):
                    continue

                # Skip SSoT source files (where values are DEFINED)
                if is_ssot_source(filepath):
                    continue

                findings = scan_file(filepath)
                files_scanned += 1

                if findings:
                    rel_path = os.path.relpath(filepath, root_dir)
                    all_findings[rel_path] = findings

    print(f"\n Files scanned: {files_scanned}")
    print(f" Files with Ghost Literals: {len(all_findings)}")

    return all_findings


def print_report(findings: Dict[str, List[Dict[str, Any]]]) -> None:
    """Print a formatted report of Ghost Literal findings."""
    if not findings:
        print(f"\n{'='*70}")
        print(" VERDICT: NO GHOST LITERALS DETECTED")
        print(" All DERIVED values are sourced from FormulasRegistry SSoT")
        print(f"{'='*70}\n")
        return

    total_ghosts = sum(len(f) for f in findings.values())

    print(f"\n{'='*70}")
    print(f" WARNING: {total_ghosts} GHOST LITERALS DETECTED")
    print(f"{'='*70}")

    for filepath, file_findings in sorted(findings.items()):
        print(f"\n [{len(file_findings)}] {filepath}")
        for finding in file_findings:
            print(f"     Line {finding['line']}: {finding['value']} "
                  f"(should be registry.{_get_registry_name(finding['target'])})")

    print(f"\n{'-'*70}")
    print(" These values should be imported from FormulasRegistry:")
    print("   from simulations.core.FormulasRegistry import get_registry")
    print("   _REG = get_registry()")
    print("   # Then use: _REG.mephorash_chi, _REG.barbelo_modulus, etc.")
    print(f"{'='*70}\n")


def _get_registry_name(value: Any) -> str:
    """Map a target value to its FormulasRegistry property name."""
    mapping = {
        144: 'chi_eff_total',  # Also: pressure_divisor, roots_per_sector
        163: 'sterile_sector',
        288: 'roots_total',
        71.55: 'h0_local',
        71.549: 'h0_local',
        576: 'manifold_area_bulk',
        0.9583: 'tzimtzum_pressure',
        0.6819: 'sophian_drag',
    }
    return mapping.get(value, 'UNKNOWN')


def write_json_report(findings: Dict[str, List[Dict[str, Any]]], output_path: Path) -> None:
    """Write findings to a JSON file for tracking."""
    import json
    from datetime import datetime

    report = {
        "timestamp": datetime.now().isoformat() + "Z",
        "total_files": len(findings),
        "total_ghosts": sum(len(f) for f in findings.values()),
        "targets": sorted([float(t) if isinstance(t, float) else t
                         for t in GhostLiteralHunter.TARGET_LITERALS]),
        "findings": findings
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f" JSON report: {output_path}")


def main():
    """Run the Ghost Literal Hunter."""
    # Get project root
    project_root = Path(__file__).parent.parent

    # Scan repository
    findings = scan_repository(str(project_root))

    # Print report
    print_report(findings)

    # Write JSON report for tracking
    json_path = project_root / "AutoGenerated" / "ghost_literal_report.json"
    write_json_report(findings, json_path)

    # Return exit code based on findings
    if findings:
        total = sum(len(f) for f in findings.values())
        print(f"Exit code: 1 ({total} Ghost Literals found)")
        return 1
    else:
        print("Exit code: 0 (Clean)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
