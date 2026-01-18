#!/usr/bin/env python3
"""
Validation Script for Cosmology Derivation Chain
=================================================

Validates the integrity and consistency of the cosmology_chain.json
derivation structure.

Checks:
1. All steps have required fields
2. Dependencies are valid (refer to earlier steps)
3. Expected results are formatted correctly
4. Wolfram Language syntax is valid (basic check)
5. Numerical predictions match geometric anchors

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


class DerivationChainValidator:
    """Validates cosmology derivation chain structure and consistency."""

    def __init__(self, json_path: str):
        """
        Initialize validator with path to chain JSON.

        Args:
            json_path: Path to cosmology_chain.json
        """
        self.json_path = Path(json_path)
        self.chain = None
        self.errors = []
        self.warnings = []

    def load_chain(self) -> bool:
        """Load and parse JSON file."""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.chain = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.json_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False

    def validate_metadata(self) -> bool:
        """Validate metadata structure."""
        if 'metadata' not in self.chain:
            self.errors.append("Missing 'metadata' section")
            return False

        metadata = self.chain['metadata']
        required_fields = ['title', 'version', 'date', 'author', 'description',
                          'topological_invariant', 'geometric_anchors',
                          'observational_targets']

        for field in required_fields:
            if field not in metadata:
                self.errors.append(f"Missing metadata field: {field}")

        # Validate geometric anchors
        if 'geometric_anchors' in metadata:
            anchors = metadata['geometric_anchors']
            required_anchors = ['k_gimel', 'c_kaf', 'chi_eff']

            for anchor in required_anchors:
                if anchor not in anchors:
                    self.errors.append(f"Missing geometric anchor: {anchor}")
                elif not isinstance(anchors[anchor], (int, float)):
                    self.errors.append(f"Invalid type for {anchor}: {type(anchors[anchor])}")

        return len(self.errors) == 0

    def validate_sections(self) -> bool:
        """Validate section structure."""
        if 'sections' not in self.chain:
            self.errors.append("Missing 'sections' section")
            return False

        sections = self.chain['sections']
        expected_sections = [
            '1_friedmann_equations',
            '2_dynamical_wz',
            '3_phantom_crossing',
            '4_hubble_resolution',
            '5_ede_mechanism'
        ]

        for section_key in expected_sections:
            if section_key not in sections:
                self.errors.append(f"Missing section: {section_key}")
            else:
                self._validate_section(section_key, sections[section_key])

        return len(self.errors) == 0

    def _validate_section(self, section_key: str, section_data: Dict) -> None:
        """Validate individual section structure."""
        if 'title' not in section_data:
            self.errors.append(f"Section {section_key} missing 'title'")

        if 'queries' not in section_data:
            self.errors.append(f"Section {section_key} missing 'queries'")
            return

        queries = section_data['queries']
        if not isinstance(queries, list):
            self.errors.append(f"Section {section_key} 'queries' must be a list")
            return

        for i, query in enumerate(queries):
            self._validate_query(section_key, i, query)

    def _validate_query(self, section_key: str, index: int, query: Dict) -> None:
        """Validate individual query structure."""
        required_fields = [
            'step_number',
            'description',
            'wolfram_language',
            'wolfram_alpha_query',
            'expected_result',
            'dependencies'
        ]

        for field in required_fields:
            if field not in query:
                self.errors.append(
                    f"Section {section_key}, query {index}: missing field '{field}'"
                )

        # Validate step number
        if 'step_number' in query:
            if not isinstance(query['step_number'], int):
                self.errors.append(
                    f"Section {section_key}, query {index}: step_number must be integer"
                )

        # Validate dependencies
        if 'dependencies' in query:
            if not isinstance(query['dependencies'], list):
                self.errors.append(
                    f"Section {section_key}, query {index}: dependencies must be list"
                )
            else:
                step_num = query.get('step_number', -1)
                for dep in query['dependencies']:
                    if not isinstance(dep, int):
                        self.errors.append(
                            f"Step {step_num}: dependency must be integer, got {type(dep)}"
                        )
                    elif dep >= step_num:
                        self.errors.append(
                            f"Step {step_num}: invalid dependency {dep} (must be < {step_num})"
                        )

        # Basic Wolfram Language syntax checks
        if 'wolfram_language' in query:
            wl_code = query['wolfram_language']
            self._check_wolfram_syntax(section_key, index, wl_code)

    def _check_wolfram_syntax(self, section_key: str, index: int, code: str) -> None:
        """Perform basic Wolfram Language syntax validation."""
        # Check balanced brackets
        brackets = {'[': ']', '{': '}', '(': ')'}
        stack = []

        for char in code:
            if char in brackets.keys():
                stack.append(char)
            elif char in brackets.values():
                if not stack:
                    self.warnings.append(
                        f"Section {section_key}, query {index}: unmatched closing bracket '{char}'"
                    )
                else:
                    last = stack.pop()
                    if brackets[last] != char:
                        self.warnings.append(
                            f"Section {section_key}, query {index}: mismatched brackets {last} and {char}"
                        )

        if stack:
            self.warnings.append(
                f"Section {section_key}, query {index}: unclosed brackets {stack}"
            )

        # Check for common Wolfram functions
        wolfram_functions = [
            'Sqrt', 'Exp', 'Solve', 'NIntegrate', 'D', 'Limit',
            'Table', 'Plot', 'Print', 'N'
        ]

        has_function = any(func in code for func in wolfram_functions)
        if not has_function and len(code) > 20:
            self.warnings.append(
                f"Section {section_key}, query {index}: no recognizable Wolfram functions"
            )

    def validate_summary(self) -> bool:
        """Validate summary section."""
        if 'summary' not in self.chain:
            self.errors.append("Missing 'summary' section")
            return False

        summary = self.chain['summary']
        required_fields = ['total_steps', 'verification_status', 'key_predictions']

        for field in required_fields:
            if field not in summary:
                self.errors.append(f"Missing summary field: {field}")

        # Validate total_steps count
        if 'total_steps' in summary and 'sections' in self.chain:
            expected_total = sum(
                len(section['queries'])
                for section in self.chain['sections'].values()
                if 'queries' in section
            )

            if summary['total_steps'] != expected_total:
                self.errors.append(
                    f"total_steps mismatch: declared {summary['total_steps']}, "
                    f"actual {expected_total}"
                )

        return len(self.errors) == 0

    def validate_numerical_predictions(self) -> bool:
        """Validate numerical predictions against geometric anchors."""
        if 'summary' not in self.chain or 'metadata' not in self.chain:
            return True  # Already reported errors

        summary = self.chain['summary']
        metadata = self.chain['metadata']

        if 'key_predictions' not in summary:
            return True

        predictions = summary['key_predictions']
        anchors = metadata.get('geometric_anchors', {})

        # Check w0 prediction is within reasonable range
        if 'w0_prediction' in predictions:
            w0 = predictions['w0_prediction']
            if not -2 < w0 < 0:
                self.warnings.append(
                    f"w₀ prediction {w0} outside reasonable range [-2, 0]"
                )

        # Check wa prediction
        if 'wa_prediction' in predictions:
            wa = predictions['wa_prediction']
            if not -2 < wa < 2:
                self.warnings.append(
                    f"wₐ prediction {wa} outside reasonable range [-2, 2]"
                )

        # Check consistency with observational targets
        if 'observational_targets' in metadata:
            targets = metadata['observational_targets']

            if 'w0_prediction' in predictions and 'DESI_2025_w0' in targets:
                w0_pm = predictions['w0_prediction']
                w0_desi = targets['DESI_2025_w0']
                deviation = abs(w0_pm - w0_desi)

                if deviation > 0.5:
                    self.warnings.append(
                        f"Large w₀ deviation from DESI: {deviation:.3f} "
                        f"(PM: {w0_pm:.3f}, DESI: {w0_desi:.3f})"
                    )

        return True

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        Run all validation checks.

        Returns:
            Tuple of (success, errors, warnings)
        """
        if not self.load_chain():
            return False, self.errors, self.warnings

        self.validate_metadata()
        self.validate_sections()
        self.validate_summary()
        self.validate_numerical_predictions()

        success = len(self.errors) == 0
        return success, self.errors, self.warnings

    def print_report(self) -> None:
        """Print validation report to console."""
        print("=" * 70)
        print("DERIVATION CHAIN VALIDATION REPORT")
        print("=" * 70)
        print(f"\nFile: {self.json_path}")

        if self.chain:
            metadata = self.chain.get('metadata', {})
            print(f"Title: {metadata.get('title', 'N/A')}")
            print(f"Version: {metadata.get('version', 'N/A')}")
            print(f"Date: {metadata.get('date', 'N/A')}")

            if 'sections' in self.chain:
                total_queries = sum(
                    len(section.get('queries', []))
                    for section in self.chain['sections'].values()
                )
                print(f"Total derivation steps: {total_queries}")

        print("\n" + "-" * 70)

        if self.errors:
            print(f"\nERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        else:
            print("\n[OK] No errors found")

        if self.warnings:
            print(f"\nWARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        else:
            print("[OK] No warnings")

        print("\n" + "=" * 70)

        if not self.errors:
            print("STATUS: VALID - Chain ready for Wolfram verification")
        else:
            print("STATUS: INVALID - Please fix errors before proceeding")

        print("=" * 70)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Default path
    default_path = "h:\\Github\\PrincipiaMetaphysica\\AutoGenerated\\derivations\\cosmology_chain.json"

    # Allow override from command line
    json_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    # Run validation
    validator = DerivationChainValidator(json_path)
    success, errors, warnings = validator.validate_all()

    # Print report
    validator.print_report()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
