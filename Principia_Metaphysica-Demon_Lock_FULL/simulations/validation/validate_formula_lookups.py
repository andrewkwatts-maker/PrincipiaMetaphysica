#!/usr/bin/env python3
"""
Validate Formula and Parameter Lookups
=======================================

This script validates that all formula and parameter references in HTML files
are valid and match entries in config.py / theory_output.json.

Usage:
    python validate_formula_lookups.py [--fix] [--verbose]

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Add parent to path for config import
sys.path.insert(0, str(Path(__file__).parent))

from config import CoreFormulas, FundamentalConstants, PhenomenologyParameters


def load_theory_output() -> Dict:
    """Load theory_output.json"""
    theory_path = Path(__file__).parent / "theory_output.json"
    if not theory_path.exists():
        print("WARNING: theory_output.json not found. Run: python run_all_simulations.py --export")
        return {}
    with open(theory_path) as f:
        return json.load(f)


def get_valid_formula_ids() -> Set[str]:
    """Get all valid formula IDs from CoreFormulas"""
    formulas = CoreFormulas.get_all_formulas()
    return {f.id for f in formulas}


def get_valid_parameter_ids() -> Dict[str, str]:
    """Get all valid parameter IDs from config classes"""
    params = {}

    # FundamentalConstants
    for attr in dir(FundamentalConstants):
        if not attr.startswith('_') and attr.isupper():
            params[f"fundamental.{attr}"] = str(getattr(FundamentalConstants, attr))

    # PhenomenologyParameters
    for attr in dir(PhenomenologyParameters):
        if not attr.startswith('_') and attr.isupper():
            params[f"phenomenology.{attr}"] = str(getattr(PhenomenologyParameters, attr))

    return params


def find_html_files() -> List[Path]:
    """Find all HTML files to validate"""
    root = Path(__file__).parent
    html_files = []

    # Main pages
    for pattern in ["*.html", "sections/*.html"]:
        html_files.extend(root.glob(pattern))

    return sorted(html_files)


def validate_formula_references(html_content: str, valid_ids: Set[str]) -> List[Tuple[int, str, str]]:
    """
    Find formula references in HTML and check if they're valid.

    Returns list of (line_number, reference, status) tuples.
    """
    issues = []

    # Patterns to find formula references
    patterns = [
        r'data-formula-id="([^"]+)"',
        r'formula-id="([^"]+)"',
        r'<pm-formula\s+formula-id="([^"]+)"',
    ]

    lines = html_content.split('\n')
    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for formula_id in matches:
                if formula_id not in valid_ids:
                    issues.append((line_num, formula_id, "INVALID - not in CoreFormulas"))

    return issues


def validate_stat_references(html_content: str, theory_data: Dict) -> List[Tuple[int, str, str]]:
    """
    Find data-stat-id references and check if they resolve.
    Checks both theory_output.json AND pm-validation-stats.js defaults.

    Returns list of (line_number, reference, status) tuples.
    """
    issues = []

    # PM_STATS keys from pm-validation-stats.js (these are always available)
    pm_stats_keys = {
        'total_parameters', 'geometric_count', 'derived_count', 'calibrated_count',
        'phenomenological_count', 'exact_count', 'total_validations', 'testable_predictions',
        'within_1sigma', 'within_2sigma', 'within_3sigma', 'exact_matches', 'mean_sigma',
        'max_sigma', 'validations_passed', 'validations_failed',
        # Computed properties from getters
        'success_rate_1sigma', 'success_rate_2sigma', 'success_rate_3sigma',
        'exact_match_rate', 'validation_success_rate', 'geometric_fraction',
        'exact_fraction', 'derived_fraction', 'validation_summary',
        'validation_summary_percent', 'calibration_statement', 'geometric_percentage',
        'summary_short', 'summary_full', 'transparency_statement'
    }

    pattern = r'data-stat-id="([^"]+)"'

    lines = html_content.split('\n')
    for line_num, line in enumerate(lines, 1):
        matches = re.findall(pattern, line)
        for stat_id in matches:
            # First check if it's a PM_STATS key (handled by pm-validation-stats.js)
            if stat_id in pm_stats_keys:
                continue  # Valid - handled by PM_STATS

            # Then check if it's in theory_data.statistics
            if 'statistics' in theory_data and stat_id in theory_data['statistics']:
                continue  # Valid - in statistics section

            # Try to resolve the stat_id as a dotted path in theory_data
            parts = stat_id.split('.')
            value = theory_data
            resolved = True
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    resolved = False
                    break

            if not resolved:
                issues.append((line_num, stat_id, "INVALID - path not found in theory_output.json or PM_STATS"))

    return issues


def find_placeholder_references(html_content: str) -> List[Tuple[int, str]]:
    """
    Find placeholder references like [v12_6_geometric_derivations.vev_pneuma.v_EW]
    that should be replaced with dynamic lookups.
    """
    placeholders = []

    pattern = r'\[([a-z0-9_]+\.[a-z0-9_.]+)\]'

    lines = html_content.split('\n')
    for line_num, line in enumerate(lines, 1):
        matches = re.findall(pattern, line, re.IGNORECASE)
        for placeholder in matches:
            # Skip common false positives
            if placeholder.startswith('http') or placeholder.startswith('mailto'):
                continue
            placeholders.append((line_num, placeholder))

    return placeholders


def find_hardcoded_values(html_content: str) -> List[Tuple[int, str, str]]:
    """
    Find likely hardcoded numerical values that should be dynamic.
    """
    hardcoded = []

    # Known values that should be dynamic
    known_values = {
        "2.118": "M_GUT",
        "10^16": "M_GUT",
        "8.15×10^34": "proton_lifetime",
        "8.15e34": "proton_lifetime",
        "0.8528": "dark_energy_w0",
        "-0.8528": "dark_energy_w0",
        "23.54": "alpha_GUT_inv",
        "1/23.54": "alpha_GUT_inv",
        "0.23121": "sin2_theta_W",
        "172.7": "top_quark_mass",
        "125.1": "higgs_mass",
        "5.0 TeV": "kk_graviton_mass",
        "4.5 TeV": "kk_graviton_mass",
        "7.42×10^-5": "dm2_21",
        "2.515×10^-3": "dm2_31",
    }

    lines = html_content.split('\n')
    for line_num, line in enumerate(lines, 1):
        for value, param in known_values.items():
            if value in line:
                # Skip if it's in a comment or script
                if '<!--' in line or '<script' in line.lower():
                    continue
                hardcoded.append((line_num, value, f"Should be: data-stat-id=\"{param}\""))

    return hardcoded


def validate_file(filepath: Path, valid_formula_ids: Set[str], theory_data: Dict, verbose: bool = False) -> Dict:
    """Validate a single HTML file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return {"file": str(filepath), "error": str(e)}

    results = {
        "file": str(filepath.name),
        "formula_issues": validate_formula_references(content, valid_formula_ids),
        "stat_issues": validate_stat_references(content, theory_data),
        "placeholders": find_placeholder_references(content),
        "hardcoded": find_hardcoded_values(content),
    }

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate formula and parameter lookups")
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all details')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix issues (not implemented)')
    args = parser.parse_args()

    print("=" * 70)
    print(" FORMULA & PARAMETER LOOKUP VALIDATION")
    print("=" * 70)
    print()

    # Load data
    valid_formula_ids = get_valid_formula_ids()
    print(f"Valid formula IDs: {len(valid_formula_ids)}")

    theory_data = load_theory_output()
    print(f"Theory output loaded: {'Yes' if theory_data else 'No'}")
    print()

    # Find and validate HTML files
    html_files = find_html_files()
    print(f"HTML files to validate: {len(html_files)}")
    print()

    total_issues = 0
    total_placeholders = 0
    total_hardcoded = 0

    for filepath in html_files:
        results = validate_file(filepath, valid_formula_ids, theory_data, args.verbose)

        if "error" in results:
            print(f"ERROR reading {results['file']}: {results['error']}")
            continue

        formula_issues = results["formula_issues"]
        stat_issues = results["stat_issues"]
        placeholders = results["placeholders"]
        hardcoded = results["hardcoded"]

        has_issues = formula_issues or stat_issues or placeholders or hardcoded

        if has_issues or args.verbose:
            print(f"--- {results['file']} ---")

            if formula_issues:
                print(f"  Formula Issues ({len(formula_issues)}):")
                for line, ref, status in formula_issues:
                    print(f"    Line {line}: {ref} - {status}")
                total_issues += len(formula_issues)

            if stat_issues:
                print(f"  Stat ID Issues ({len(stat_issues)}):")
                for line, ref, status in stat_issues:
                    print(f"    Line {line}: {ref} - {status}")
                total_issues += len(stat_issues)

            if placeholders:
                print(f"  Placeholder References ({len(placeholders)}):")
                for line, ref in placeholders[:5]:  # Limit output
                    print(f"    Line {line}: [{ref}]")
                if len(placeholders) > 5:
                    print(f"    ... and {len(placeholders) - 5} more")
                total_placeholders += len(placeholders)

            if hardcoded and args.verbose:
                print(f"  Hardcoded Values ({len(hardcoded)}):")
                for line, value, suggestion in hardcoded[:5]:
                    print(f"    Line {line}: {value} - {suggestion}")
                if len(hardcoded) > 5:
                    print(f"    ... and {len(hardcoded) - 5} more")
                total_hardcoded += len(hardcoded)

            print()

    # Summary
    print("=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    print(f"  Total formula/stat issues: {total_issues}")
    print(f"  Total placeholder refs:    {total_placeholders}")
    print(f"  Total hardcoded values:    {total_hardcoded}")
    print()

    if total_issues == 0 and total_placeholders == 0:
        print("  STATUS: ALL LOOKUPS VALID")
        return 0
    else:
        print("  STATUS: ISSUES FOUND - Review and fix")
        return 1


if __name__ == "__main__":
    sys.exit(main())
