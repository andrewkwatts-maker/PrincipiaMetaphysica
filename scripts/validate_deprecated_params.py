#!/usr/bin/env python3
"""
Deprecated Parameter Reference Validator

Scans HTML, JS, and Python files for references to deprecated PM param paths
and suggests replacements based on config/deprecated_params.json.

This script is READ-ONLY - it does not modify any files.

Usage:
    python scripts/validate_deprecated_params.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import os
import re
import sys
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPRECATED_CONFIG = os.path.join(PROJECT_ROOT, "config", "deprecated_params.json")

# Directories to scan
SCAN_DIRS = [
    os.path.join(PROJECT_ROOT, "Pages"),
    os.path.join(PROJECT_ROOT, "js"),
    os.path.join(PROJECT_ROOT, "simulations"),
]

# File extensions to scan
SCAN_EXTENSIONS = ['.html', '.js', '.py']


def load_deprecated_params() -> Dict[str, Dict[str, str]]:
    """Load deprecated params config."""
    if not os.path.exists(DEPRECATED_CONFIG):
        print(f"Warning: {DEPRECATED_CONFIG} not found")
        return {}

    with open(DEPRECATED_CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)

    deprecated = {}
    for item in config.get('deprecated_params', []):
        old_path = item.get('old_path', '')
        if old_path:
            deprecated[old_path] = {
                'new_path': item.get('new_path', ''),
                'reason': item.get('reason', ''),
                'deprecated_in': item.get('deprecated_in', '')
            }

    return deprecated


def scan_file(filepath: str, deprecated: Dict[str, Dict[str, str]]) -> List[Tuple[int, str, str, Dict]]:
    """
    Scan a file for deprecated param references.

    Returns list of (line_number, line_content, deprecated_path, replacement_info)
    """
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return []

    for i, line in enumerate(lines, 1):
        for old_path, info in deprecated.items():
            # Look for the path in various contexts
            patterns = [
                rf'["\']({re.escape(old_path)})["\']',  # String literal
                rf'data-pm-value=["\']({re.escape(old_path)})["\']',  # HTML attribute
                rf'PM\.get\(["\']({re.escape(old_path)})["\']',  # PM.get() call
                rf'get_param\(["\']({re.escape(old_path)})["\']',  # Python get_param
                rf'registry\.get\(["\']({re.escape(old_path)})["\']',  # Registry get
            ]

            for pattern in patterns:
                if re.search(pattern, line):
                    findings.append((i, line.strip(), old_path, info))
                    break  # Only report once per line per path

    return findings


def scan_directory(dirpath: str, deprecated: Dict[str, Dict[str, str]]) -> Dict[str, List[Tuple]]:
    """Scan a directory for deprecated param references."""
    results = {}

    if not os.path.exists(dirpath):
        return results

    for root, dirs, files in os.walk(dirpath):
        # Skip hidden and common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in SCAN_EXTENSIONS:
                continue

            filepath = os.path.join(root, filename)
            findings = scan_file(filepath, deprecated)

            if findings:
                rel_path = os.path.relpath(filepath, PROJECT_ROOT)
                results[rel_path] = findings

    return results


def main():
    """Main entry point."""
    print("=" * 70)
    print("Deprecated Parameter Reference Validator")
    print("=" * 70)

    # Load deprecated params
    deprecated = load_deprecated_params()
    if not deprecated:
        print("\nNo deprecated params configured. Exiting.")
        return 0

    print(f"\nLoaded {len(deprecated)} deprecated param paths from config")

    # Scan directories
    all_findings = {}
    for dirpath in SCAN_DIRS:
        if os.path.exists(dirpath):
            findings = scan_directory(dirpath, deprecated)
            all_findings.update(findings)

    # Report findings
    print("\n" + "-" * 70)
    print("SCAN RESULTS")
    print("-" * 70)

    total_findings = 0
    for filepath, findings in sorted(all_findings.items()):
        print(f"\n{filepath}:")
        for line_num, line_content, old_path, info in findings:
            print(f"  Line {line_num}: {old_path}")
            print(f"    Replace with: {info['new_path']}")
            print(f"    Reason: {info['reason']}")
            if len(line_content) < 80:
                print(f"    Context: {line_content}")
            total_findings += 1

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if total_findings > 0:
        print(f"\n[WARN] Found {total_findings} deprecated param references in {len(all_findings)} files")
        print("\nRecommended actions:")
        print("1. Update the references to use the new param paths")
        print("2. Run simulations to verify changes")
        print("3. Test affected pages/functionality")
        return 1
    else:
        print("\n[PASS] No deprecated param references found")
        return 0


if __name__ == "__main__":
    sys.exit(main())
