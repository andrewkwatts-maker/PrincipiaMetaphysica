#!/usr/bin/env python3
"""
Principia Metaphysica - Comprehensive Validation Suite
=======================================================

Comprehensive validation suite for CI/CD pipeline that:
1. Runs all simulations via run_all_simulations.py
2. Runs all pytest tests
3. Validates theory_output.json structure
4. Checks all experimental data files are valid JSON
5. Verifies all formulas have proper metadata
6. Checks all parameters have proper provenance
7. Generates a validation report

Exit codes:
- 0: All validations passed
- 1: One or more validations failed

Usage:
    python simulations/validate_all.py [--skip-simulations] [--skip-tests] [--verbose]

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime
import traceback


class ValidationReport:
    """Tracks validation results and generates reports."""

    def __init__(self):
        self.sections: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.now()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_section(self, name: str, passed: bool, details: Dict[str, Any],
                   errors: List[str] = None, warnings: List[str] = None):
        """Add a validation section result."""
        self.sections[name] = {
            "passed": passed,
            "details": details,
            "errors": errors or [],
            "warnings": warnings or []
        }
        if errors:
            self.errors.extend(errors)
        if warnings:
            self.warnings.extend(warnings)

    def all_passed(self) -> bool:
        """Check if all sections passed."""
        return all(section["passed"] for section in self.sections.values())

    def generate_summary(self) -> str:
        """Generate a text summary of the validation."""
        duration = (datetime.now() - self.start_time).total_seconds()

        lines = [
            "=" * 80,
            "PRINCIPIA METAPHYSICA - VALIDATION SUITE SUMMARY",
            "=" * 80,
            f"Timestamp: {datetime.now().isoformat()}",
            f"Duration: {duration:.2f}s",
            "",
            "RESULTS:",
            "-" * 80
        ]

        for name, result in self.sections.items():
            status = "PASS" if result["passed"] else "FAIL"
            lines.append(f"  [{status}] {name}")
            if result["errors"]:
                for error in result["errors"]:
                    lines.append(f"         ERROR: {error}")
            if result["warnings"]:
                for warning in result["warnings"]:
                    lines.append(f"         WARNING: {warning}")

        lines.append("")
        lines.append("-" * 80)

        total = len(self.sections)
        passed = sum(1 for s in self.sections.values() if s["passed"])
        failed = total - passed

        lines.append(f"Total Checks: {total}")
        lines.append(f"Passed: {passed}")
        lines.append(f"Failed: {failed}")
        lines.append(f"Success Rate: {100.0 * passed / total:.1f}%")

        if self.warnings:
            lines.append(f"\nWarnings: {len(self.warnings)}")

        lines.append("")
        lines.append("=" * 80)

        if self.all_passed():
            lines.append("STATUS: ALL VALIDATIONS PASSED")
        else:
            lines.append(f"STATUS: {failed} VALIDATION(S) FAILED")

        lines.append("=" * 80)

        return "\n".join(lines)

    def save_json(self, output_path: Path):
        """Save the validation report as JSON."""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "all_passed": self.all_passed(),
            "sections": self.sections,
            "summary": {
                "total_checks": len(self.sections),
                "passed": sum(1 for s in self.sections.values() if s["passed"]),
                "failed": sum(1 for s in self.sections.values() if not s["passed"]),
                "warnings": len(self.warnings)
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)


class ComprehensiveValidator:
    """Main validation orchestrator."""

    def __init__(self, project_root: Path, verbose: bool = True,
                 skip_simulations: bool = False, skip_tests: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.skip_simulations = skip_simulations
        self.skip_tests = skip_tests
        self.report = ValidationReport()

    def log(self, message: str):
        """Print log message if verbose."""
        if self.verbose:
            print(message)

    def validate_all(self) -> bool:
        """Run all validations and return overall success status."""
        self.log("=" * 80)
        self.log("PRINCIPIA METAPHYSICA - COMPREHENSIVE VALIDATION SUITE")
        self.log("=" * 80)
        self.log("")

        # 1. Run simulations
        if not self.skip_simulations:
            self.validate_simulations()
        else:
            self.log("[SKIPPED] Simulations (--skip-simulations)")

        # 2. Run pytest tests
        if not self.skip_tests:
            self.validate_pytest_tests()
        else:
            self.log("[SKIPPED] Pytest tests (--skip-tests)")

        # 3. Validate theory_output.json structure
        self.validate_theory_output_structure()

        # 4. Validate experimental data files
        self.validate_experimental_data_files()

        # 5. Validate formula metadata
        self.validate_formula_metadata()

        # 6. Validate parameter provenance
        self.validate_parameter_provenance()

        # 7. Validate JSON files in AutoGenerated
        self.validate_autogenerated_json_files()

        # Generate report
        self.log("")
        self.log(self.report.generate_summary())

        # Save JSON report
        report_path = self.project_root / "simulations" / "validation_report.json"
        self.report.save_json(report_path)
        self.log(f"\nDetailed report saved to: {report_path}")

        return self.report.all_passed()

    def validate_simulations(self) -> None:
        """Run all simulations via run_all_simulations.py."""
        self.log("\n[1/7] Running all simulations...")
        self.log("-" * 80)

        run_script = self.project_root / "simulations" / "run_all_simulations.py"

        if not run_script.exists():
            self.report.add_section(
                "Simulations",
                False,
                {"script": str(run_script)},
                errors=["run_all_simulations.py not found"]
            )
            return

        try:
            result = subprocess.run(
                [sys.executable, str(run_script), "--quiet"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            passed = result.returncode == 0

            details = {
                "exit_code": result.returncode,
                "stdout_lines": len(result.stdout.splitlines()),
                "stderr_lines": len(result.stderr.splitlines())
            }

            errors = []
            if not passed:
                errors.append(f"Simulations failed with exit code {result.returncode}")
                if result.stderr:
                    errors.append(f"stderr: {result.stderr[:500]}")

            self.report.add_section("Simulations", passed, details, errors)

            if passed:
                self.log("[OK] All simulations passed")
            else:
                self.log(f"[FAIL] Simulations failed with exit code {result.returncode}")

        except subprocess.TimeoutExpired:
            self.report.add_section(
                "Simulations",
                False,
                {"timeout": "300s"},
                errors=["Simulations timed out after 300 seconds"]
            )
            self.log("[FAIL] Simulations timed out")
        except Exception as e:
            self.report.add_section(
                "Simulations",
                False,
                {"exception": str(e)},
                errors=[f"Exception running simulations: {e}"]
            )
            self.log(f"[FAIL] Exception: {e}")

    def validate_pytest_tests(self) -> None:
        """Run all pytest tests."""
        self.log("\n[2/7] Running pytest tests...")
        self.log("-" * 80)

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )

            # pytest returns 0 if all tests pass, non-zero otherwise
            passed = result.returncode == 0

            # Parse output to get test counts
            output = result.stdout + result.stderr
            details = {
                "exit_code": result.returncode,
                "output_preview": output[:500] if output else "No output"
            }

            errors = []
            warnings = []

            if not passed:
                errors.append(f"Pytest failed with exit code {result.returncode}")
                # Try to extract failure info
                if "FAILED" in output:
                    failed_tests = [line for line in output.splitlines() if "FAILED" in line]
                    errors.extend(failed_tests[:5])  # First 5 failures

            # Check for warnings
            if "warning" in output.lower():
                warnings.append("Pytest generated warnings (see output)")

            self.report.add_section("Pytest Tests", passed, details, errors, warnings)

            if passed:
                self.log("[OK] All pytest tests passed")
            else:
                self.log(f"[FAIL] Pytest tests failed")

        except subprocess.TimeoutExpired:
            self.report.add_section(
                "Pytest Tests",
                False,
                {"timeout": "120s"},
                errors=["Pytest tests timed out after 120 seconds"]
            )
            self.log("[FAIL] Pytest tests timed out")
        except FileNotFoundError:
            self.report.add_section(
                "Pytest Tests",
                False,
                {},
                errors=["pytest not installed. Run: pip install pytest"]
            )
            self.log("[FAIL] pytest not installed")
        except Exception as e:
            self.report.add_section(
                "Pytest Tests",
                False,
                {"exception": str(e)},
                errors=[f"Exception running pytest: {e}"]
            )
            self.log(f"[FAIL] Exception: {e}")

    def validate_theory_output_structure(self) -> None:
        """Validate theory_output.json has required structure."""
        self.log("\n[3/7] Validating theory_output.json structure...")
        self.log("-" * 80)

        theory_output_path = self.project_root / "AutoGenerated" / "theory_output.json"

        if not theory_output_path.exists():
            self.report.add_section(
                "Theory Output Structure",
                False,
                {"path": str(theory_output_path)},
                errors=["theory_output.json not found"]
            )
            self.log("[FAIL] theory_output.json not found")
            return

        try:
            with open(theory_output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check required top-level keys
            required_keys = [
                "metadata", "derivation_logic", "parameter_classification",
                "parameters", "formulas", "sections", "provenance", "validation"
            ]

            missing_keys = [key for key in required_keys if key not in data]

            # Validate metadata structure
            metadata_errors = []
            if "metadata" in data:
                meta = data["metadata"]
                required_meta = ["version", "timestamp", "git"]
                metadata_errors = [f"metadata.{key} missing" for key in required_meta if key not in meta]

            # Count elements
            details = {
                "file_size_kb": theory_output_path.stat().st_size / 1024,
                "parameters_count": len(data.get("parameters", {})),
                "formulas_count": len(data.get("formulas", {})),
                "sections_count": len(data.get("sections", {})),
                "provenance_entries": len(data.get("provenance", {}))
            }

            errors = []
            if missing_keys:
                errors.append(f"Missing top-level keys: {', '.join(missing_keys)}")
            errors.extend(metadata_errors)

            passed = len(errors) == 0

            self.report.add_section("Theory Output Structure", passed, details, errors)

            if passed:
                self.log(f"[OK] Valid structure with {details['parameters_count']} params, "
                        f"{details['formulas_count']} formulas, {details['sections_count']} sections")
            else:
                self.log(f"[FAIL] Invalid structure")

        except json.JSONDecodeError as e:
            self.report.add_section(
                "Theory Output Structure",
                False,
                {"path": str(theory_output_path)},
                errors=[f"Invalid JSON: {e}"]
            )
            self.log(f"[FAIL] Invalid JSON: {e}")
        except Exception as e:
            self.report.add_section(
                "Theory Output Structure",
                False,
                {"exception": str(e)},
                errors=[f"Exception: {e}"]
            )
            self.log(f"[FAIL] Exception: {e}")

    def validate_experimental_data_files(self) -> None:
        """Validate all experimental data JSON files."""
        self.log("\n[4/7] Validating experimental data files...")
        self.log("-" * 80)

        data_dir = self.project_root / "simulations" / "data" / "experimental"

        if not data_dir.exists():
            self.report.add_section(
                "Experimental Data Files",
                False,
                {"path": str(data_dir)},
                errors=["Experimental data directory not found"]
            )
            self.log("[FAIL] Experimental data directory not found")
            return

        # Find all JSON files
        json_files = list(data_dir.glob("*.json"))

        if not json_files:
            self.report.add_section(
                "Experimental Data Files",
                False,
                {"path": str(data_dir)},
                warnings=["No experimental data JSON files found"]
            )
            self.log("[WARN] No experimental data files found")
            return

        errors = []
        valid_files = []
        invalid_files = []

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                valid_files.append(json_file.name)
            except json.JSONDecodeError as e:
                invalid_files.append(json_file.name)
                errors.append(f"{json_file.name}: Invalid JSON - {e}")
            except Exception as e:
                invalid_files.append(json_file.name)
                errors.append(f"{json_file.name}: {e}")

        passed = len(invalid_files) == 0

        details = {
            "total_files": len(json_files),
            "valid_files": len(valid_files),
            "invalid_files": len(invalid_files),
            "files": [f.name for f in json_files]
        }

        self.report.add_section("Experimental Data Files", passed, details, errors)

        if passed:
            self.log(f"[OK] All {len(valid_files)} experimental data files are valid JSON")
        else:
            self.log(f"[FAIL] {len(invalid_files)} invalid files")

    def validate_formula_metadata(self) -> None:
        """Validate that all formulas have proper metadata."""
        self.log("\n[5/7] Validating formula metadata...")
        self.log("-" * 80)

        theory_output_path = self.project_root / "AutoGenerated" / "theory_output.json"

        if not theory_output_path.exists():
            self.report.add_section(
                "Formula Metadata",
                False,
                {},
                errors=["theory_output.json not found"]
            )
            self.log("[FAIL] theory_output.json not found")
            return

        try:
            with open(theory_output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            formulas = data.get("formulas", {})

            if not formulas:
                self.report.add_section(
                    "Formula Metadata",
                    False,
                    {},
                    errors=["No formulas found in theory_output.json"]
                )
                self.log("[FAIL] No formulas found")
                return

            # Required fields for each formula
            required_fields = ["latex", "category"]
            recommended_fields = ["description", "domain"]

            errors = []
            warnings = []
            formulas_with_issues = []

            for formula_id, formula_data in formulas.items():
                missing_required = [f for f in required_fields if f not in formula_data]
                missing_recommended = [f for f in recommended_fields if f not in formula_data]

                if missing_required:
                    errors.append(f"{formula_id}: Missing required fields: {', '.join(missing_required)}")
                    formulas_with_issues.append(formula_id)

                if missing_recommended:
                    warnings.append(f"{formula_id}: Missing recommended fields: {', '.join(missing_recommended)}")

            passed = len(errors) == 0

            details = {
                "total_formulas": len(formulas),
                "formulas_with_errors": len(formulas_with_issues),
                "formulas_with_warnings": len([w for w in warnings])
            }

            self.report.add_section("Formula Metadata", passed, details, errors, warnings)

            if passed:
                self.log(f"[OK] All {len(formulas)} formulas have required metadata")
                if warnings:
                    self.log(f"     {len(warnings)} warning(s) about recommended fields")
            else:
                self.log(f"[FAIL] {len(formulas_with_issues)} formulas missing required metadata")

        except Exception as e:
            self.report.add_section(
                "Formula Metadata",
                False,
                {"exception": str(e)},
                errors=[f"Exception: {e}"]
            )
            self.log(f"[FAIL] Exception: {e}")

    def validate_parameter_provenance(self) -> None:
        """Validate that all parameters have proper provenance tracking."""
        self.log("\n[6/7] Validating parameter provenance...")
        self.log("-" * 80)

        theory_output_path = self.project_root / "AutoGenerated" / "theory_output.json"

        if not theory_output_path.exists():
            self.report.add_section(
                "Parameter Provenance",
                False,
                {},
                errors=["theory_output.json not found"]
            )
            self.log("[FAIL] theory_output.json not found")
            return

        try:
            with open(theory_output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            parameters = data.get("parameters", {})
            provenance = data.get("provenance", {})

            if not parameters:
                self.report.add_section(
                    "Parameter Provenance",
                    False,
                    {},
                    errors=["No parameters found in theory_output.json"]
                )
                self.log("[FAIL] No parameters found")
                return

            # Check each parameter has required provenance fields
            required_fields = ["value", "source"]
            recommended_fields = ["source_simulation", "status"]

            errors = []
            warnings = []
            params_without_provenance = []
            params_missing_fields = []

            for param_id, param_data in parameters.items():
                # Check required fields
                missing_required = [f for f in required_fields if f not in param_data]
                missing_recommended = [f for f in recommended_fields if f not in param_data]

                if missing_required:
                    errors.append(f"{param_id}: Missing required fields: {', '.join(missing_required)}")
                    params_missing_fields.append(param_id)

                if missing_recommended:
                    warnings.append(f"{param_id}: Missing recommended fields: {', '.join(missing_recommended)}")

                # Check if parameter has provenance entry
                if param_id not in provenance and "established" not in param_data.get("status", "").lower():
                    params_without_provenance.append(param_id)

            if params_without_provenance:
                warnings.extend([f"{p}: No provenance entry" for p in params_without_provenance[:10]])
                if len(params_without_provenance) > 10:
                    warnings.append(f"... and {len(params_without_provenance) - 10} more")

            passed = len(errors) == 0

            details = {
                "total_parameters": len(parameters),
                "parameters_with_provenance": len(provenance),
                "parameters_missing_fields": len(params_missing_fields),
                "parameters_without_provenance": len(params_without_provenance)
            }

            self.report.add_section("Parameter Provenance", passed, details, errors, warnings)

            if passed:
                self.log(f"[OK] All {len(parameters)} parameters have required provenance")
                if warnings:
                    self.log(f"     {len(warnings)} warning(s)")
            else:
                self.log(f"[FAIL] {len(params_missing_fields)} parameters missing required fields")

        except Exception as e:
            self.report.add_section(
                "Parameter Provenance",
                False,
                {"exception": str(e)},
                errors=[f"Exception: {e}"]
            )
            self.log(f"[FAIL] Exception: {e}")

    def validate_autogenerated_json_files(self) -> None:
        """Validate all JSON files in AutoGenerated directory."""
        self.log("\n[7/7] Validating AutoGenerated JSON files...")
        self.log("-" * 80)

        autogen_dir = self.project_root / "AutoGenerated"

        if not autogen_dir.exists():
            self.report.add_section(
                "AutoGenerated JSON Files",
                False,
                {"path": str(autogen_dir)},
                errors=["AutoGenerated directory not found"]
            )
            self.log("[FAIL] AutoGenerated directory not found")
            return

        # Find all JSON files recursively
        json_files = list(autogen_dir.rglob("*.json"))

        if not json_files:
            self.report.add_section(
                "AutoGenerated JSON Files",
                False,
                {"path": str(autogen_dir)},
                warnings=["No JSON files found in AutoGenerated"]
            )
            self.log("[WARN] No JSON files found")
            return

        errors = []
        valid_files = []
        invalid_files = []

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                valid_files.append(json_file.relative_to(autogen_dir))
            except json.JSONDecodeError as e:
                invalid_files.append(json_file.relative_to(autogen_dir))
                errors.append(f"{json_file.relative_to(autogen_dir)}: Invalid JSON - {str(e)[:100]}")
            except Exception as e:
                invalid_files.append(json_file.relative_to(autogen_dir))
                errors.append(f"{json_file.relative_to(autogen_dir)}: {e}")

        passed = len(invalid_files) == 0

        details = {
            "total_files": len(json_files),
            "valid_files": len(valid_files),
            "invalid_files": len(invalid_files)
        }

        self.report.add_section("AutoGenerated JSON Files", passed, details, errors)

        if passed:
            self.log(f"[OK] All {len(valid_files)} JSON files in AutoGenerated are valid")
        else:
            self.log(f"[FAIL] {len(invalid_files)} invalid JSON files")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive validation suite for Principia Metaphysica"
    )
    parser.add_argument(
        "--skip-simulations",
        action="store_true",
        help="Skip running simulations (useful for quick checks)"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running pytest tests"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )

    args = parser.parse_args()

    # Get project root (scripts/validation/ -> scripts/ -> project root)
    project_root = Path(__file__).resolve().parent.parent.parent

    # Create validator and run
    validator = ComprehensiveValidator(
        project_root=project_root,
        verbose=not args.quiet,
        skip_simulations=args.skip_simulations,
        skip_tests=args.skip_tests
    )

    success = validator.validate_all()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
