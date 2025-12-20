#!/usr/bin/env python3
"""
Config.py Usage Validator - Single Source of Truth Enforcement

Scans simulation files for hardcoded parameter values that should be imported
from config.py instead.

Usage:
    python scripts/validate_config_usage.py
    python scripts/validate_config_usage.py --fix  # Auto-generate fix suggestions

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

# Critical parameters that must come from config.py
CRITICAL_PARAMS = {
    'M_GUT': {
        'pattern': r'M_GUT\s*=\s*([0-9.]+e[0-9]+|[0-9.]+)',
        'config_import': 'from config import GaugeUnificationParameters',
        'config_usage': 'M_GUT = GaugeUnificationParameters.M_GUT  # 2.118e16 GeV',
        'expected_value': '2.118e16',
    },
    'M_PLANCK': {
        'pattern': r'M_PLANCK\s*=\s*([0-9.]+e[0-9]+|[0-9.]+)',
        'config_import': 'from config import PhenomenologyParameters',
        'config_usage': 'M_PLANCK = PhenomenologyParameters.M_PLANCK_REDUCED  # 2.435e18 GeV',
        'expected_value': '2.435e18',
    },
    'SHADOW_KUF': {
        'pattern': r'alpha[_]?4\s*=\s*(0\.576[0-9]+)',
        'config_import': 'from config import SharedDimensionsParameters',
        'config_usage': 'SHADOW_KUF = SharedDimensionsParameters.SHADOW_KUF  # 0.576152',
        'expected_value': '0.576152',
    },
    'SHADOW_CHET': {
        'pattern': r'alpha[_]?5\s*=\s*(0\.576[0-9]+)',
        'config_import': 'from config import SharedDimensionsParameters',
        'config_usage': 'SHADOW_CHET = SharedDimensionsParameters.SHADOW_CHET  # 0.576152',
        'expected_value': '0.576152',
    },
    'THETA_23': {
        'pattern': r'[Tt]heta[_]?23\s*=\s*(45\.0*)',
        'config_import': 'from config import NeutrinoParameters',
        'config_usage': 'THETA_23 = NeutrinoParameters.THETA_23  # 45.0 degrees',
        'expected_value': '45.0',
    },
    'ALPHA_GUT': {
        'pattern': r'alpha[_]?[Gg][Uu][Tt]\s*=\s*1\s*/\s*([0-9.]+)',
        'config_import': 'from config import GaugeUnificationParameters',
        'config_usage': 'ALPHA_GUT = GaugeUnificationParameters.ALPHA_GUT  # 1/23.54',
        'expected_value': '1/23.54',
    },
}

# Acceptable exceptions (geometry-derived constants, not phenomenological)
ACCEPTABLE_HARDCODED = [
    'Omega',  # Intersection numbers (pure geometry)
    'phi',    # Wilson phases (geometry-derived)
    'b2', 'b3',  # Betti numbers (topology)
    'chi_eff',   # Euler characteristic (topology)
    'T_omega',   # Torsion class (if deriving it)
]


class ConfigValidator:
    """Validates config.py usage across simulation files."""

    def __init__(self, simulations_dir='simulations'):
        self.simulations_dir = Path(simulations_dir)
        self.violations = defaultdict(list)
        self.files_checked = 0
        self.files_with_violations = 0

    def check_file(self, filepath):
        """Check a single file for hardcoded parameters."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return

        self.files_checked += 1

        # Check if file imports config
        imports_config = bool(re.search(r'import config|from config import', content))

        # Check for hardcoded values
        file_violations = []
        for param_name, param_info in CRITICAL_PARAMS.items():
            matches = re.finditer(param_info['pattern'], content, re.MULTILINE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                matched_value = match.group(1) if match.groups() else match.group(0)

                # Check if this is in a comment explaining the config value
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_end = content.find('\n', match.end())
                line = content[line_start:line_end]

                # Skip if it's a comment reference to config
                if 'config.' in line or '#' in line[:match.start() - line_start]:
                    continue

                file_violations.append({
                    'param': param_name,
                    'line': line_num,
                    'value': matched_value,
                    'imports_config': imports_config,
                })

        if file_violations:
            self.files_with_violations += 1
            self.violations[str(filepath)] = file_violations

    def scan_simulations(self):
        """Scan all Python files in simulations directory."""
        py_files = sorted(self.simulations_dir.glob('*.py'))
        print(f"Scanning {len(py_files)} files in {self.simulations_dir}...\n")

        for py_file in py_files:
            self.check_file(py_file)

    def print_report(self, verbose=False):
        """Print validation report."""
        print("=" * 80)
        print("CONFIG.PY USAGE VALIDATION REPORT")
        print("=" * 80)
        print()

        print(f"Files checked: {self.files_checked}")
        print(f"Files with violations: {self.files_with_violations}")
        print(f"Total violations: {sum(len(v) for v in self.violations.values())}")
        print()

        if not self.violations:
            print("SUCCESS: All files properly import from config.py!")
            return True

        print("VIOLATIONS FOUND:")
        print()

        # Group by parameter type
        param_counts = defaultdict(int)
        for file_violations in self.violations.values():
            for violation in file_violations:
                param_counts[violation['param']] += 1

        print("By Parameter Type:")
        for param, count in sorted(param_counts.items(), key=lambda x: -x[1]):
            print(f"  {param}: {count} instances")
        print()

        # Detailed violations
        print("Detailed Violations:")
        print("-" * 80)

        for filepath, file_violations in sorted(self.violations.items()):
            rel_path = Path(filepath).relative_to(Path.cwd()) if Path(filepath).is_absolute() else filepath
            print(f"\n{rel_path}:")

            imports_config = file_violations[0]['imports_config']
            print(f"  Imports config: {'Yes' if imports_config else 'No'}")

            for violation in file_violations:
                param = violation['param']
                print(f"    Line {violation['line']}: {param} = {violation['value']}")

                if verbose:
                    param_info = CRITICAL_PARAMS[param]
                    print(f"      → Fix: {param_info['config_usage']}")

        return False

    def generate_fixes(self):
        """Generate suggested fixes for all violations."""
        print("\n" + "=" * 80)
        print("SUGGESTED FIXES")
        print("=" * 80)

        for filepath, file_violations in sorted(self.violations.items()):
            rel_path = Path(filepath).relative_to(Path.cwd()) if Path(filepath).is_absolute() else filepath
            print(f"\n### {rel_path}")

            # Collect unique imports needed
            imports_needed = set()
            replacements = []

            for violation in file_violations:
                param = violation['param']
                param_info = CRITICAL_PARAMS[param]
                imports_needed.add(param_info['config_import'])
                replacements.append(param_info['config_usage'])

            print("\nAdd these imports at the top:")
            for imp in sorted(imports_needed):
                print(f"  {imp}")

            print("\nReplace hardcoded values with:")
            for repl in replacements:
                print(f"  {repl}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate config.py usage')
    parser.add_argument('--simulations', default='simulations',
                        help='Path to simulations directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed fix suggestions')
    parser.add_argument('--fix', action='store_true',
                        help='Generate fix suggestions')

    args = parser.parse_args()

    validator = ConfigValidator(args.simulations)
    validator.scan_simulations()

    success = validator.print_report(verbose=args.verbose)

    if args.fix and not success:
        validator.generate_fixes()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
