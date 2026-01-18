"""
Value Context Audit v17.2 - DERIVED vs EXPERIMENTAL Value Usage Validator
==========================================================================

This script ensures that:
1. DERIVED values (from PM theory) are sourced from FormulasRegistry in simulations
2. EXPERIMENTAL values (from PDG/CODATA) are only used in validation/comparison contexts
3. Proper source attribution comments exist for experimental constants

Value Classification:
---------------------
DERIVED (must use FormulasRegistry SSoT):
    - 0.9583... (tzimtzum_pressure = 23/24)
    - 0.6819    (sophian_drag)
    - 1.6402    (parity_sum)
    - 71.55     (h0_local from O'Dowd Formula)
    - 576       (manifold_area_bulk = B3^2)
    - 144       (pressure_divisor = B3^2/4)
    - 163       (sterile_sector, odowd_bulk_pressure)
    - 288       (roots_total from E8xE8)

EXPERIMENTAL (allowed hardcoded WITH source attribution):
    - 137.036... (alpha inverse from CODATA/PDG)
    - 1836.15... (proton/electron mass ratio from CODATA)
    - 91.1876    (Z boson mass from PDG)
    - 125.10     (Higgs mass from PDG)
    - -0.957     (w0 from DESI 2025 - experimental constraint)

Usage:
    python tests/test_value_context_audit.py          # Run audit
    python tests/test_value_context_audit.py --fix    # Auto-fix simple cases
    python tests/test_value_context_audit.py --test   # Run as unit tests

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import ast
import os
import re
import sys
import unittest
from pathlib import Path
from typing import List, Tuple, Set, Dict, Optional
from dataclasses import dataclass
from enum import Enum

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class ValueType(Enum):
    """Classification of numeric constants."""
    DERIVED = "DERIVED"          # From PM theory, must use FormulasRegistry
    EXPERIMENTAL = "EXPERIMENTAL"  # From PDG/CODATA, allowed with attribution
    UNKNOWN = "UNKNOWN"          # Needs classification


class FileContext(Enum):
    """Context classification for files."""
    SIMULATION = "SIMULATION"    # Should use registry for derived values
    VALIDATION = "VALIDATION"    # Can use experimental values for comparison
    TEST = "TEST"                # Can use both for testing
    REGISTRY = "REGISTRY"        # The SSoT itself
    OTHER = "OTHER"


@dataclass
class ValueUsage:
    """Represents a usage of a numeric value in code."""
    file_path: str
    line_number: int
    value: float
    value_type: ValueType
    file_context: FileContext
    has_source_comment: bool
    source_comment: Optional[str]
    is_violation: bool
    violation_reason: Optional[str]


class ValueContextValidator(ast.NodeVisitor):
    """
    AST visitor that checks numeric value usage in context.

    Rules:
    1. DERIVED values in SIMULATION files must come from FormulasRegistry
    2. EXPERIMENTAL values must have source attribution (CODATA, PDG, DESI, etc.)
    3. DERIVED values should NOT appear as raw literals in simulation logic
    """

    # DERIVED values - must use FormulasRegistry in simulations
    DERIVED_VALUES: Dict[float, str] = {
        0.9583: "tzimtzum_pressure (23/24)",
        0.95833: "tzimtzum_pressure (23/24)",
        0.6819: "sophian_drag",
        1.6402: "parity_sum (eta_S + sigma_T)",
        71.55: "h0_local (O'Dowd Formula)",
        71.549955: "h0_local (O'Dowd Formula)",
        576: "manifold_area_bulk (B3^2)",
        576.0: "manifold_area_bulk (B3^2)",
        144: "pressure_divisor (B3^2/4)",
        144.0: "pressure_divisor (B3^2/4)",
        163: "sterile_sector / odowd_bulk_pressure",
        163.0: "sterile_sector / odowd_bulk_pressure",
        288: "roots_total (E8xE8)",
        288.0: "roots_total (E8xE8)",
        125: "visible_sector (5^3)",
        125.0: "visible_sector (5^3)",
    }

    # EXPERIMENTAL values - allowed with source attribution
    EXPERIMENTAL_VALUES: Dict[float, str] = {
        137.035: "alpha inverse (CODATA)",
        137.036: "alpha inverse (CODATA)",
        137.035999: "alpha inverse (CODATA 2022)",
        137.035999177: "alpha inverse (CODATA 2022 full)",
        1836.15: "proton/electron mass ratio (CODATA)",
        1836.152673: "proton/electron mass ratio (CODATA)",
        91.1876: "Z boson mass (PDG)",
        125.10: "Higgs mass (PDG)",
        125.1: "Higgs mass (PDG)",
        -0.957: "w0 dark energy (DESI 2025)",
        0.1180: "alpha_s at M_Z (PDG)",
        0.1182: "alpha_s at M_Z (PDG)",
        246.22: "Higgs VEV (PDG)",
    }

    # Source attribution keywords that indicate proper documentation
    SOURCE_KEYWORDS = {
        "CODATA", "PDG", "DESI", "Planck", "experimental",
        "measured", "observation", "constraint", "NuFIT"
    }

    def __init__(self, filename: str, source_lines: List[str], file_context: FileContext):
        self.filename = filename
        self.source_lines = source_lines
        self.file_context = file_context
        self.usages: List[ValueUsage] = []
        self.has_registry_import = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check for FormulasRegistry import."""
        if node.module and "FormulasRegistry" in node.module:
            self.has_registry_import = True
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Check for FormulasRegistry import."""
        for alias in node.names:
            if "FormulasRegistry" in alias.name:
                self.has_registry_import = True
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        """Check numeric constants."""
        if isinstance(node.value, (int, float)):
            self._analyze_value(node.value, node.lineno)
        self.generic_visit(node)

    def _get_line_comment(self, lineno: int) -> Optional[str]:
        """Get any comment on the same line or previous line."""
        comments = []

        # Check current line
        if 0 < lineno <= len(self.source_lines):
            line = self.source_lines[lineno - 1]
            if '#' in line:
                comments.append(line[line.index('#'):])

        # Check previous line for standalone comment
        if 0 < lineno - 1 <= len(self.source_lines):
            prev_line = self.source_lines[lineno - 2].strip()
            if prev_line.startswith('#'):
                comments.append(prev_line)

        return ' '.join(comments) if comments else None

    def _has_source_attribution(self, comment: Optional[str]) -> bool:
        """Check if comment contains source attribution."""
        if not comment:
            return False
        comment_upper = comment.upper()
        return any(kw.upper() in comment_upper for kw in self.SOURCE_KEYWORDS)

    def _line_has_derivation_context(self, lineno: int) -> bool:
        """Check if the line shows a derivation from b3/B3/24."""
        derivation_patterns = [
            r'\bb3\b', r'\bB3\b', r'\b24\b',  # Base-24 references
            r'\*\*\s*2', r'pow\s*\(',         # Squaring operations
            r'\/\s*4\b', r'\/\s*4\.0',        # Division by 4
            r'\-\s*5\b', r'\-\s*5\.0',        # Subtraction of 5
            r'7\s*\*', r'\*\s*7',             # Multiplication by 7
            r'roots', r'ROOTS',               # Roots references
            r'visible', r'sterile',           # Sector references
            r'manifold', r'bulk',             # Manifold references
        ]

        # Check current line and surrounding context (3 lines each way)
        context_lines = []
        for offset in range(-3, 4):
            check_line = lineno - 1 + offset
            if 0 <= check_line < len(self.source_lines):
                context_lines.append(self.source_lines[check_line])

        context = ' '.join(context_lines)
        return any(re.search(p, context, re.IGNORECASE) for p in derivation_patterns)

    def _analyze_value(self, value: float, lineno: int) -> None:
        """Analyze a numeric value usage."""
        # Classify the value
        if value in self.DERIVED_VALUES or abs(value) in [v for v in self.DERIVED_VALUES.keys()]:
            value_type = ValueType.DERIVED
        elif value in self.EXPERIMENTAL_VALUES:
            value_type = ValueType.EXPERIMENTAL
        else:
            return  # Skip unclassified values

        # Get comment context
        comment = self._get_line_comment(lineno)
        has_source = self._has_source_attribution(comment)
        has_derivation = self._line_has_derivation_context(lineno)

        # Determine if this is a violation
        is_violation = False
        violation_reason = None

        if value_type == ValueType.DERIVED:
            # DERIVED values in SIMULATION context should use registry OR show derivation
            if self.file_context == FileContext.SIMULATION:
                if not self.has_registry_import and not has_derivation:
                    is_violation = True
                    violation_reason = f"DERIVED value {value} ({self.DERIVED_VALUES.get(value, self.DERIVED_VALUES.get(abs(value), '?'))}) used without FormulasRegistry import or derivation context"

        elif value_type == ValueType.EXPERIMENTAL:
            # EXPERIMENTAL values should have source attribution
            if not has_source:
                # Only flag in simulation files - validation files are expected to use experimental values
                if self.file_context == FileContext.SIMULATION:
                    is_violation = True
                    violation_reason = f"EXPERIMENTAL value {value} ({self.EXPERIMENTAL_VALUES[value]}) without source attribution comment"

        usage = ValueUsage(
            file_path=self.filename,
            line_number=lineno,
            value=value,
            value_type=value_type,
            file_context=self.file_context,
            has_source_comment=has_source,
            source_comment=comment,
            is_violation=is_violation,
            violation_reason=violation_reason
        )

        self.usages.append(usage)


class ValueContextAuditor:
    """
    Scans the repository for value context violations.

    Ensures DERIVED values use FormulasRegistry and EXPERIMENTAL values
    have proper source attribution.
    """

    # Files to skip
    SKIP_FILES: Set[str] = {
        "FormulasRegistry.py",
        "named_constants.json",
        "__pycache__",
        ".git",
        "test_value_context_audit.py",
    }

    # Directories to skip
    SKIP_DIRS: Set[str] = {
        "__pycache__",
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "env",
        "Principia_Metaphysica-Demon_Lock",
        "Principia_Metaphysica-Demon_Lock_FULL",
        "Principia_Metaphysica_v16_2_20251231",
        "Principia_Metaphysica_v16_2_20260101_FULL",
        "Principia_Metaphysica_v16_2_20260102_FULL",
    }

    def __init__(self, project_root: str = None):
        self.project_root = project_root or str(Path(__file__).parent.parent)
        self.all_usages: List[ValueUsage] = []
        self.violations: List[ValueUsage] = []

    def _classify_file_context(self, file_path: str) -> FileContext:
        """Determine the context classification for a file."""
        path_lower = file_path.lower()
        filename = os.path.basename(file_path).lower()

        # Registry files
        if "formulasregistry" in filename or "registry" in filename:
            return FileContext.REGISTRY

        # Test files
        if filename.startswith("test_") or "/tests/" in path_lower or "\\tests\\" in path_lower:
            return FileContext.TEST

        # Validation files
        validation_patterns = [
            "validation", "validate", "validator", "verify",
            "established", "experimental", "sigma_validator",
            "gatekeeper", "logic_check"
        ]
        if any(p in path_lower for p in validation_patterns):
            return FileContext.VALIDATION

        # Simulation files
        simulation_patterns = [
            "simulation", "simulations/v21", "run_all",
            "geometric", "cosmology", "gauge", "neutrino",
            "predictions", "appendix"
        ]
        if any(p in path_lower for p in simulation_patterns):
            return FileContext.SIMULATION

        return FileContext.OTHER

    def scan_file(self, file_path: str) -> List[ValueUsage]:
        """Scan a single Python file for value usage."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
                source_lines = source.split('\n')

            tree = ast.parse(source)
            file_context = self._classify_file_context(file_path)
            relative_path = os.path.relpath(file_path, self.project_root)

            validator = ValueContextValidator(relative_path, source_lines, file_context)
            validator.visit(tree)

            return validator.usages

        except SyntaxError:
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
        self.all_usages = []
        self.violations = []

        for root, dirs, files in os.walk(self.project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            for file in files:
                if not file.endswith(".py"):
                    continue
                if file in self.SKIP_FILES:
                    continue

                file_path = os.path.join(root, file)
                usages = self.scan_file(file_path)

                self.all_usages.extend(usages)
                self.violations.extend([u for u in usages if u.is_violation])

        return len(self.violations) == 0

    def generate_report(self) -> str:
        """Generate a human-readable audit report."""
        lines = [
            "=" * 70,
            " PRINCIPIA METAPHYSICA v17.2 - VALUE CONTEXT AUDIT REPORT",
            "=" * 70,
            "",
        ]

        # Summary by value type
        derived_count = sum(1 for u in self.all_usages if u.value_type == ValueType.DERIVED)
        experimental_count = sum(1 for u in self.all_usages if u.value_type == ValueType.EXPERIMENTAL)

        lines.extend([
            f"Total classified value usages: {len(self.all_usages)}",
            f"  - DERIVED values: {derived_count}",
            f"  - EXPERIMENTAL values: {experimental_count}",
            "",
        ])

        if not self.violations:
            lines.extend([
                "STATUS: COMPLIANT",
                "All values are used in appropriate contexts with proper attribution.",
                "",
            ])
        else:
            lines.extend([
                "STATUS: VIOLATIONS DETECTED",
                f"Found {len(self.violations)} context violations:",
                "",
            ])

            # Group by file
            by_file: Dict[str, List[ValueUsage]] = {}
            for v in self.violations:
                if v.file_path not in by_file:
                    by_file[v.file_path] = []
                by_file[v.file_path].append(v)

            for file_path, usages in sorted(by_file.items()):
                lines.append(f"  {file_path}:")
                for u in usages:
                    lines.append(f"    Line {u.line_number}: {u.violation_reason}")
                lines.append("")

        # Recommendations
        lines.extend([
            "-" * 70,
            "RECOMMENDATIONS:",
            "",
            "For DERIVED values in simulation files:",
            "  1. Import: from core.FormulasRegistry import get_registry",
            "  2. Use: reg = get_registry(); value = reg.tzimtzum_pressure",
            "",
            "For EXPERIMENTAL values:",
            "  1. Add source comment: # CODATA 2022 / PDG 2024 / DESI 2025",
            "  2. Use descriptive variable names: ALPHA_INV_CODATA = 137.036",
            "",
            "=" * 70,
        ])

        return "\n".join(lines)

    def suggest_fixes(self) -> List[Tuple[str, int, str, str]]:
        """
        Suggest fixes for violations.

        Returns:
            List of (file_path, line_number, old_code, suggested_fix) tuples.
        """
        fixes = []

        for v in self.violations:
            if v.value_type == ValueType.DERIVED:
                # Suggest using registry
                registry_attr = self._get_registry_attribute(v.value)
                if registry_attr:
                    fixes.append((
                        v.file_path,
                        v.line_number,
                        f"{v.value}",
                        f"reg.{registry_attr}  # From FormulasRegistry SSoT"
                    ))
            elif v.value_type == ValueType.EXPERIMENTAL:
                # Suggest adding source comment
                source = ValueContextValidator.EXPERIMENTAL_VALUES.get(v.value, "external source")
                fixes.append((
                    v.file_path,
                    v.line_number,
                    f"{v.value}",
                    f"{v.value}  # {source}"
                ))

        return fixes

    def _get_registry_attribute(self, value: float) -> Optional[str]:
        """Get the FormulasRegistry attribute name for a derived value."""
        mapping = {
            0.9583: "tzimtzum_pressure",
            0.95833: "tzimtzum_pressure",
            0.6819: "sophian_drag",
            1.6402: "parity_sum",
            71.55: "h0_local",
            71.549955: "h0_local",
            576: "manifold_area_bulk",
            576.0: "manifold_area_bulk",
            144: "pressure_divisor",
            144.0: "pressure_divisor",
            163: "sterile_sector",
            163.0: "sterile_sector",
            288: "roots_total",
            288.0: "roots_total",
            125: "visible_sector",
            125.0: "visible_sector",
        }
        return mapping.get(value) or mapping.get(abs(value))


class TestValueContextAudit(unittest.TestCase):
    """Unit tests for the Value Context Audit."""

    def test_no_violations(self):
        """
        Scan repository for value context violations.

        This test fails if any violations are found.
        """
        auditor = ValueContextAuditor()
        is_compliant = auditor.scan_repository()

        if not is_compliant:
            report = auditor.generate_report()
            self.fail(f"Value Context Audit Failed!\n\n{report}")

    def test_derived_values_classification(self):
        """Ensure all key derived values are classified."""
        derived = ValueContextValidator.DERIVED_VALUES

        self.assertIn(0.9583, derived)  # tzimtzum
        self.assertIn(0.6819, derived)  # sophian
        self.assertIn(71.55, derived)   # h0
        self.assertIn(576, derived)     # manifold area
        self.assertIn(144, derived)     # pressure divisor
        self.assertIn(163, derived)     # sterile sector
        self.assertIn(288, derived)     # roots total

    def test_experimental_values_classification(self):
        """Ensure all key experimental values are classified."""
        experimental = ValueContextValidator.EXPERIMENTAL_VALUES

        self.assertIn(137.036, experimental)   # alpha inverse
        self.assertIn(91.1876, experimental)   # Z mass
        self.assertIn(125.10, experimental)    # Higgs mass


def apply_experimental_fixes(auditor: ValueContextAuditor) -> int:
    """
    Apply automatic fixes for EXPERIMENTAL value violations.

    Adds source attribution comments to experimental values.
    """
    fixed_count = 0
    files_to_fix: Dict[str, List[ValueUsage]] = {}

    # Group experimental violations by file
    for v in auditor.violations:
        if v.value_type == ValueType.EXPERIMENTAL:
            if v.file_path not in files_to_fix:
                files_to_fix[v.file_path] = []
            files_to_fix[v.file_path].append(v)

    for rel_path, usages in files_to_fix.items():
        file_path = os.path.join(auditor.project_root, rel_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Sort by line number descending to avoid offset issues
            usages.sort(key=lambda u: u.line_number, reverse=True)

            for usage in usages:
                line_idx = usage.line_number - 1
                if 0 <= line_idx < len(lines):
                    line = lines[line_idx]
                    # Get source attribution
                    source = ValueContextValidator.EXPERIMENTAL_VALUES.get(usage.value, "external")

                    # Check if line already has a comment
                    if '#' in line:
                        # Add to existing comment
                        comment_idx = line.index('#')
                        existing_comment = line[comment_idx:].rstrip()
                        if source.split('(')[1].rstrip(')').upper() not in existing_comment.upper():
                            new_line = line[:comment_idx].rstrip() + f"  # {source}\n"
                            lines[line_idx] = new_line
                            fixed_count += 1
                    else:
                        # Add new comment
                        new_line = line.rstrip() + f"  # {source}\n"
                        lines[line_idx] = new_line
                        fixed_count += 1

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            print(f"  Fixed {len(usages)} violations in {rel_path}")

        except Exception as e:
            print(f"  Error fixing {rel_path}: {e}")

    return fixed_count


def run_audit(fix_mode: bool = False) -> int:
    """Run the value context audit and print the report."""
    print("Initializing Value Context Audit...")
    print("")

    auditor = ValueContextAuditor()
    is_compliant = auditor.scan_repository()

    print(auditor.generate_report())

    if not is_compliant and fix_mode:
        print("\n" + "=" * 70)
        print(" APPLYING AUTOMATIC FIXES")
        print("=" * 70)
        print("")

        # Count violation types
        exp_violations = sum(1 for v in auditor.violations if v.value_type == ValueType.EXPERIMENTAL)
        derived_violations = sum(1 for v in auditor.violations if v.value_type == ValueType.DERIVED)

        print(f"EXPERIMENTAL violations (auto-fixable): {exp_violations}")
        print(f"DERIVED violations (manual review needed): {derived_violations}")
        print("")

        if exp_violations > 0:
            print("Applying source attribution comments...")
            fixed = apply_experimental_fixes(auditor)
            print(f"\nFixed {fixed} experimental value violations.")
            print("Re-run audit to verify fixes.")
        else:
            print("No auto-fixable violations found.")

        if derived_violations > 0:
            print("\n" + "-" * 70)
            print("MANUAL FIXES REQUIRED for DERIVED values:")
            print("")
            print("Option 1: Import FormulasRegistry")
            print("  from core.FormulasRegistry import get_registry")
            print("  reg = get_registry()")
            print("  value = reg.pressure_divisor  # instead of 144")
            print("")
            print("Option 2: Add derivation context")
            print("  pressure_divisor = B3 ** 2 // 4  # 576 / 4 = 144")

    return 0 if is_compliant else 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            unittest.main(argv=[''], exit=True)
        elif sys.argv[1] == "--fix":
            exit_code = run_audit(fix_mode=True)
            sys.exit(exit_code)

    exit_code = run_audit()
    sys.exit(exit_code)
