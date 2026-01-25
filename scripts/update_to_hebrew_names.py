#!/usr/bin/env python3
"""
Update to Hebrew Names Script
=============================
Systematically updates code to use the new Hebrew naming scheme.

IMPORTANT: This script only updates USAGES (e.g., reg.b3 → reg.elder_vessels)
It does NOT change:
- Variable declarations (self._b3 = 24 stays)
- Property definitions (def b3(self) stays)
- Aliases (the backward compatibility layer)

Usage: python scripts/update_to_hebrew_names.py [--dry-run] [--apply]
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Project root
ROOT = Path(__file__).parent.parent

# Directories to process (simulation code, not core registry)
PROCESS_DIRS = [
    "simulations",
    "tests",
]

# Files to skip (FormulasRegistry defines the aliases)
SKIP_FILES = {
    "FormulasRegistry.py",
    "find_old_names.py",
    "apply_hebrew_renames.py",
    "update_to_hebrew_names.py",
    "add_gnostic_naming.py",
}

# Mapping: old_name -> new_name
# Only for USAGES like reg.old_name or self.old_name
USAGE_RENAMES = {
    # Topological Invariants
    "watts_constant": "monad_unity",
    "decad": "residual_key",
    "b3": "elder_vessels",
    "horos": "horos_limit",
    "chi_eff": "mephorash_chi",  # Be careful not to match chi_eff_total/chi_eff_sector
    "shadow_sector": "demiurgic_gates",
    "christ_constant": "logos_joint",
    "delta_jc": "logos_joint",
    "odowd_bulk_pressure": "sophian_pressure",
    "sterile_sector": "sophian_pressure",
    "roots_total": "nitzotzin_roots",
    # Central Sampler
    "reid_invariant": "nitsot_par",
    "central_pair": "reid_pair",
    "central_pair_weight": "watts_weight",
    "central_activation_threshold": "gnosis_threshold",
}

# Patterns to match for replacement (only registry property access)
# ONLY match: reg.old_name, registry.old_name, REGISTRY.old_name, _SSOT.old_name
# Do NOT match: self.old_name (local attribute) or general .old_name
def create_patterns():
    """Create regex patterns for each old name - ONLY registry access."""
    patterns = {}

    # Prefixes that indicate registry/SSoT access
    registry_prefixes = r'(?:reg|registry|REGISTRY|_SSOT|_registry|self\.reg|self\.registry|self\._registry)'

    for old_name, new_name in USAGE_RENAMES.items():
        # Match registry_prefix.old_name followed by non-word char or end
        if old_name == "chi_eff":
            # Special case: only match .chi_eff not followed by _ or alphanumeric
            pattern = rf'({registry_prefixes})\.chi_eff(?!_|[a-zA-Z0-9])'
            replacement = rf'\1.{new_name}'
        else:
            pattern = rf'({registry_prefixes})\.{old_name}(?![a-zA-Z0-9_])'
            replacement = rf'\1.{new_name}'
        patterns[old_name] = (re.compile(pattern), replacement)
    return patterns


def should_skip_file(filepath: Path) -> bool:
    """Check if file should be skipped."""
    return filepath.name in SKIP_FILES


def process_file(filepath: Path, patterns: Dict, dry_run: bool = True) -> List[Tuple[int, str, str]]:
    """
    Process a single file for replacements.

    Returns list of (line_num, old_line, new_line) tuples for changes made.
    """
    changes = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return changes

    new_lines = []
    for i, line in enumerate(lines, 1):
        new_line = line
        for old_name, (pattern, replacement) in patterns.items():
            if pattern.search(new_line):
                new_line = pattern.sub(replacement, new_line)

        if new_line != line:
            changes.append((i, line.rstrip(), new_line.rstrip()))
        new_lines.append(new_line)

    if changes and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return changes


def main():
    parser = argparse.ArgumentParser(description='Update code to use Hebrew names')
    parser.add_argument('--apply', action='store_true', help='Actually apply changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all changes')
    args = parser.parse_args()

    dry_run = not args.apply
    patterns = create_patterns()

    print("=" * 80)
    print(" UPDATE TO HEBREW NAMES")
    print("=" * 80)
    if dry_run:
        print(" MODE: DRY RUN (use --apply to make changes)")
    else:
        print(" MODE: APPLYING CHANGES")
    print("=" * 80)

    total_files = 0
    total_changes = 0

    for dir_name in PROCESS_DIRS:
        dir_path = ROOT / dir_name
        if not dir_path.exists():
            continue

        for root, dirs, files in os.walk(dir_path):
            # Skip __pycache__ and similar
            dirs[:] = [d for d in dirs if not d.startswith('__')]

            for file in files:
                if not file.endswith('.py'):
                    continue

                filepath = Path(root) / file
                if should_skip_file(filepath):
                    continue

                changes = process_file(filepath, patterns, dry_run)

                if changes:
                    total_files += 1
                    total_changes += len(changes)

                    rel_path = filepath.relative_to(ROOT)
                    print(f"\n  {rel_path} ({len(changes)} changes)")

                    if args.verbose:
                        for line_num, old_line, new_line in changes[:5]:
                            # ASCII-safe output
                            safe_old = old_line[:60].encode('ascii', 'replace').decode('ascii')
                            safe_new = new_line[:60].encode('ascii', 'replace').decode('ascii')
                            print(f"    L{line_num}:")
                            print(f"      - {safe_old}...")
                            print(f"      + {safe_new}...")
                        if len(changes) > 5:
                            print(f"    ... and {len(changes) - 5} more")

    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    print(f"  Files modified:  {total_files}")
    print(f"  Total changes:   {total_changes}")

    if dry_run:
        print("\n  Run with --apply to make these changes.")
    else:
        print("\n  Changes applied successfully!")
        print("  Run simulations to verify: python run_all_simulations.py --skip-guard")


if __name__ == "__main__":
    main()
