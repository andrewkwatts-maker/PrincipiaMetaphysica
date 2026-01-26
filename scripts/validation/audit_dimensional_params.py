#!/usr/bin/env python3
"""
Dimensional Parameter Usage Auditor
====================================

Scans all simulation files to find:
1. Hardcoded dimensional values (26, 13, 7, 6, 4, 24, 12, 5, 3)
2. Division/multiplication patterns that should use named params
3. Legacy param names that should be updated to semantic names

5-Level Chain:
- Level 0 (ANCESTRAL): 26D (24,2) - D_ancestral_*
- Level 1 (SHADOW): 13D (12,1) - D_shadow_*
- Level 2 (G2): 7D (7,0) - D_G2_*
- Level 3 (EXTERNAL): 6D (5,1) - D_external_*
- Level 4 (VISIBLE): 4D (3,1) - D_visible_*

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# Dimensional values and their semantic names
DIMENSIONAL_VALUES = {
    # Total dimensions
    26: ("D_ancestral_total", "Level 0: Ancestral"),
    13: ("D_shadow_total", "Level 1: Shadow"),
    7: ("D_G2_total", "Level 2: G2"),
    6: ("D_external_total", "Level 3: External"),
    4: ("D_visible_total", "Level 4: Visible"),
    # Spatial dimensions
    24: ("D_ancestral_space", "Level 0: Ancestral space"),
    12: ("D_shadow_space", "Level 1: Shadow space"),
    5: ("D_external_space", "Level 3: External space"),
    3: ("D_visible_space", "Level 4: Visible space"),
    # Temporal dimensions
    2: ("D_ancestral_time", "Level 0: Ancestral time (2T)"),
    1: ("D_shadow_time/D_external_time/D_visible_time", "Various time dims"),
    0: ("D_G2_time", "Level 2: G2 time (Riemannian)"),
}

# Legacy names that should be updated
LEGACY_NAMES = {
    "D_brane_total": "D_shadow_total",
    "D_brane_space": "D_shadow_space",
    "D_brane_time": "D_shadow_time",
    "D_compact_G2": "D_G2_total",
    "D_compact_external": "D_external_total",
    "D_external_6": "D_external_total",
}

# Patterns that suggest dimensional operations needing named params
SUSPICIOUS_PATTERNS = [
    (r'/\s*2\b', "Division by 2 - consider D_ancestral_time or sector split"),
    (r'\*\s*2\b', "Multiplication by 2 - consider 2*D_shadow_total relation"),
    (r'/\s*24\b', "Division by 24 - consider D_ancestral_space or b3"),
    (r'/\s*13\b', "Division by 13 - consider D_shadow_total"),
    (r'/\s*7\b', "Division by 7 - consider D_G2_total"),
    (r'/\s*6\b', "Division by 6 - consider D_external_total"),
    (r'/\s*4\b', "Division by 4 - consider D_visible_total"),
    (r'26\s*-\s*13', "26-13 calculation - use D_ancestral_total - D_shadow_total"),
    (r'13\s*-\s*7', "13-7 calculation - use D_shadow_total - D_G2_total"),
    (r'13\s*-\s*6', "13-6 calculation - use D_shadow_total - D_external_total"),
    (r'6\s*-\s*4', "6-4 calculation - use D_external_total - D_visible_total"),
]


class DimensionalParamAuditor:
    """Audits dimensional parameter usage across the codebase."""

    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        self.findings: Dict[str, List[Tuple[int, str, str]]] = defaultdict(list)
        self.summary: Dict[str, int] = defaultdict(int)

    def scan_file(self, filepath: Path) -> None:
        """Scan a single file for dimensional param issues."""
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            print(f"  [WARN] Cannot read {filepath}: {e}")
            return

        rel_path = str(filepath.relative_to(self.base_path))

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue

            # Check for hardcoded dimensional values
            for value, (param_name, description) in DIMENSIONAL_VALUES.items():
                # Only flag standalone numbers, not part of larger numbers
                pattern = rf'\b{value}\b'
                if re.search(pattern, line):
                    # Skip if it's already using the param name
                    if param_name.split('/')[0] in line:
                        continue
                    # Skip string literals
                    if re.search(rf'["\'][^"\']*{value}[^"\']*["\']', line):
                        continue
                    self.findings[rel_path].append(
                        (line_num, f"Hardcoded {value}", f"{description} -> use {param_name}")
                    )
                    self.summary[f"hardcoded_{value}"] += 1

            # Check for legacy names
            for legacy, semantic in LEGACY_NAMES.items():
                if legacy in line and semantic not in line:
                    self.findings[rel_path].append(
                        (line_num, f"Legacy name: {legacy}", f"Consider updating to {semantic}")
                    )
                    self.summary["legacy_names"] += 1

            # Check for suspicious patterns
            for pattern, description in SUSPICIOUS_PATTERNS:
                if re.search(pattern, line):
                    # Skip if it looks like it's already using proper params
                    if "D_" in line or "b3" in line or "chi_eff" in line:
                        continue
                    self.findings[rel_path].append(
                        (line_num, "Suspicious pattern", description)
                    )
                    self.summary["suspicious_patterns"] += 1

    def scan_directory(self, subdir: str = "simulations") -> None:
        """Scan all Python files in a directory."""
        scan_path = self.base_path / subdir
        if not scan_path.exists():
            print(f"[WARN] Directory not found: {scan_path}")
            return

        py_files = list(scan_path.rglob("*.py"))
        print(f"\nScanning {len(py_files)} Python files in {subdir}/...")

        for filepath in py_files:
            self.scan_file(filepath)

    def print_report(self) -> None:
        """Print the audit report."""
        print("\n" + "=" * 70)
        print("DIMENSIONAL PARAMETER USAGE AUDIT REPORT")
        print("=" * 70)

        # Summary
        print("\nSUMMARY:")
        print("-" * 40)
        total_issues = sum(self.summary.values())
        print(f"Total potential issues: {total_issues}")
        for category, count in sorted(self.summary.items()):
            print(f"  {category}: {count}")

        # Detailed findings by file
        if self.findings:
            print("\nDETAILED FINDINGS BY FILE:")
            print("-" * 40)
            for filepath, issues in sorted(self.findings.items()):
                if len(issues) > 0:
                    print(f"\n{filepath} ({len(issues)} issues):")
                    for line_num, issue_type, suggestion in issues[:10]:  # Limit output
                        print(f"  Line {line_num}: [{issue_type}] {suggestion}")
                    if len(issues) > 10:
                        print(f"  ... and {len(issues) - 10} more")

        print("\n" + "=" * 70)

    def get_files_needing_review(self) -> List[str]:
        """Get list of files with issues that need manual review."""
        return [f for f, issues in self.findings.items() if len(issues) > 5]


def main():
    """Main entry point."""
    auditor = DimensionalParamAuditor()

    # Scan key directories
    auditor.scan_directory("simulations")
    auditor.scan_directory("core")

    # Print report
    auditor.print_report()

    # List files needing review
    files_needing_review = auditor.get_files_needing_review()
    if files_needing_review:
        print("\nFILES REQUIRING DETAILED REVIEW:")
        for f in files_needing_review:
            print(f"  - {f}")

    return 0 if sum(auditor.summary.values()) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
