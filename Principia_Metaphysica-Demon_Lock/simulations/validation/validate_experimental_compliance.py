"""
Validate Experimental Value Compliance
========================================

Audits all simulation files to ensure parameters have experimental values
or explicit no_experimental_value=True flags.

Usage:
    python -m simulations.validation.validate_experimental_compliance

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import os
import sys
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

# Add parent paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@dataclass
class ParameterIssue:
    """An issue found with a parameter definition."""
    file: str
    param_path: str
    issue_type: str
    message: str


class ExperimentalComplianceValidator:
    """Validates experimental value compliance across simulation files."""

    SIMULATION_DIR = Path(__file__).parent.parent / "v16"
    VALID_SOURCES = [
        "PDG2024", "PDG 2024", "CODATA2018", "CODATA 2022",
        "NuFIT6.0", "NuFIT 6.0", "NuFIT",
        "DESI2025", "DESI 2025", "DESI_2025", "DESI DR2",
        "Planck2018", "Planck 2018",
        "Super-K", "Super-Kamiokande", "Hyper-K",
        "LHC", "ATLAS", "CMS",
        "geometric", "topological", "theory"  # For no_experimental_value cases
    ]

    def __init__(self):
        self.issues: List[ParameterIssue] = []
        self.params_checked = 0
        self.params_compliant = 0
        self.params_missing_experimental = 0

    def validate_all(self) -> Dict[str, Any]:
        """Validate all simulation files."""
        results = {
            "total_files": 0,
            "total_params": 0,
            "compliant_params": 0,
            "missing_experimental": 0,
            "issues": [],
            "files_checked": []
        }

        # Find all simulation Python files
        for py_file in self.SIMULATION_DIR.rglob("*.py"):
            if py_file.name.startswith("__"):
                continue
            if "test" in py_file.name.lower():
                continue

            results["total_files"] += 1
            results["files_checked"].append(str(py_file.relative_to(self.SIMULATION_DIR)))

            file_issues = self._validate_file(py_file)
            results["issues"].extend(file_issues)

        results["total_params"] = self.params_checked
        results["compliant_params"] = self.params_compliant
        results["missing_experimental"] = self.params_missing_experimental

        return results

    def _validate_file(self, filepath: Path) -> List[Dict[str, str]]:
        """Validate a single simulation file."""
        issues = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST to find Parameter instantiations
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Check if it's a Parameter() call
                    if self._is_parameter_call(node):
                        param_issues = self._validate_parameter(node, filepath)
                        issues.extend(param_issues)

        except Exception as e:
            issues.append({
                "file": str(filepath),
                "param_path": "N/A",
                "issue_type": "parse_error",
                "message": f"Could not parse file: {e}"
            })

        return issues

    def _is_parameter_call(self, node: ast.Call) -> bool:
        """Check if a Call node is a Parameter() instantiation."""
        if isinstance(node.func, ast.Name):
            return node.func.id == "Parameter"
        if isinstance(node.func, ast.Attribute):
            return node.func.attr == "Parameter"
        return False

    def _validate_parameter(self, node: ast.Call, filepath: Path) -> List[Dict[str, str]]:
        """Validate a Parameter instantiation."""
        issues = []
        self.params_checked += 1

        # Extract keyword arguments
        kwargs = {}
        for kw in node.keywords:
            try:
                kwargs[kw.arg] = ast.literal_eval(kw.value)
            except:
                # Handle non-literal values
                if isinstance(kw.value, ast.Constant):
                    kwargs[kw.arg] = kw.value.value
                elif isinstance(kw.value, ast.Name):
                    kwargs[kw.arg] = f"<{kw.value.id}>"
                else:
                    kwargs[kw.arg] = "<complex>"

        param_path = kwargs.get('path', '<unknown>')
        status = kwargs.get('status', '<unknown>')

        # Check experimental value compliance
        has_experimental_bound = kwargs.get('experimental_bound') is not None
        has_bound_source = kwargs.get('bound_source') is not None
        no_experimental_value = kwargs.get('no_experimental_value', False)

        # ESTABLISHED params should have experimental values
        if status == "ESTABLISHED":
            if not has_experimental_bound or not has_bound_source:
                issues.append({
                    "file": str(filepath.relative_to(self.SIMULATION_DIR)),
                    "param_path": param_path,
                    "issue_type": "missing_experimental",
                    "message": "ESTABLISHED param must have experimental_bound and bound_source"
                })
                self.params_missing_experimental += 1
            else:
                self.params_compliant += 1

        # PREDICTED/DERIVED params should either have experimental bound OR no_experimental_value=True
        elif status in ("PREDICTED", "DERIVED"):
            if not has_experimental_bound and not no_experimental_value:
                issues.append({
                    "file": str(filepath.relative_to(self.SIMULATION_DIR)),
                    "param_path": param_path,
                    "issue_type": "missing_experimental_or_flag",
                    "message": "PREDICTED/DERIVED param needs experimental_bound OR no_experimental_value=True"
                })
                self.params_missing_experimental += 1
            elif has_experimental_bound and not has_bound_source:
                issues.append({
                    "file": str(filepath.relative_to(self.SIMULATION_DIR)),
                    "param_path": param_path,
                    "issue_type": "missing_bound_source",
                    "message": "Has experimental_bound but missing bound_source"
                })
                self.params_missing_experimental += 1
            else:
                self.params_compliant += 1

        # GEOMETRIC params typically don't have experimental values
        elif status == "GEOMETRIC":
            if no_experimental_value or not has_experimental_bound:
                self.params_compliant += 1
            else:
                self.params_compliant += 1  # Having experimental is fine for GEOMETRIC

        # CALIBRATED params should have experimental reference
        elif status == "CALIBRATED":
            if not has_experimental_bound and not no_experimental_value:
                issues.append({
                    "file": str(filepath.relative_to(self.SIMULATION_DIR)),
                    "param_path": param_path,
                    "issue_type": "calibrated_needs_reference",
                    "message": "CALIBRATED param should reference experimental value it's calibrated to"
                })
                self.params_missing_experimental += 1
            else:
                self.params_compliant += 1
        else:
            self.params_compliant += 1

        # Validate bound_source format
        if has_bound_source:
            source = kwargs.get('bound_source', '')
            if not any(valid in source for valid in self.VALID_SOURCES):
                issues.append({
                    "file": str(filepath.relative_to(self.SIMULATION_DIR)),
                    "param_path": param_path,
                    "issue_type": "unknown_source",
                    "message": f"Unrecognized bound_source: {source}"
                })

        return issues

    def print_report(self, results: Dict[str, Any]) -> None:
        """Print a formatted validation report."""
        print("=" * 70)
        print("EXPERIMENTAL VALUE COMPLIANCE REPORT")
        print("=" * 70)
        print(f"\nFiles checked: {results['total_files']}")
        print(f"Parameters checked: {results['total_params']}")
        print(f"Compliant parameters: {results['compliant_params']}")
        print(f"Missing experimental: {results['missing_experimental']}")

        if results['issues']:
            print(f"\n{'='*70}")
            print(f"ISSUES FOUND: {len(results['issues'])}")
            print("=" * 70)

            # Group by file
            by_file = {}
            for issue in results['issues']:
                f = issue['file']
                if f not in by_file:
                    by_file[f] = []
                by_file[f].append(issue)

            for file, file_issues in sorted(by_file.items()):
                print(f"\n{file}:")
                for issue in file_issues:
                    print(f"  [{issue['issue_type']}] {issue['param_path']}")
                    print(f"    {issue['message']}")
        else:
            print("\n[OK] All parameters are compliant!")

        compliance_rate = (results['compliant_params'] / max(results['total_params'], 1)) * 100
        print(f"\nCompliance Rate: {compliance_rate:.1f}%")


def main():
    """Run the validation."""
    validator = ExperimentalComplianceValidator()
    results = validator.validate_all()
    validator.print_report(results)

    # Exit with error code if issues found
    if results['issues']:
        sys.exit(1)


if __name__ == "__main__":
    main()
