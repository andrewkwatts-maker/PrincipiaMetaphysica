#!/usr/bin/env python3
"""
Find Old Names Script
=====================
Identifies all locations of parameter names that need to be renamed.

Usage: python scripts/find_old_names.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Project root
ROOT = Path(__file__).parent.parent

# Directories to skip
SKIP_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    'Principia_Metaphysica-Demon_Lock', 'Principia_Metaphysica-Demon_Lock_FULL',
    '.claude'
}

# File extensions to search
EXTENSIONS = {'.py', '.js', '.html', '.md', '.json', '.txt'}

# Old name -> New name mapping (from user's final table)
RENAMES = {
    # TOPOLOGICAL INVARIANTS
    'watts_constant': 'monad_unity',
    'decad': 'residual_key',
    # 'syzygy_gap': 'syzygy_gap',  # Same - no change
    'b3': 'elder_vessels',
    'horos': 'horos_limit',
    'chi_eff': 'mephorash_chi',
    'shadow_sector': 'demiurgic_gates',
    'christ_constant': 'logos_joint',
    'delta_jc': 'logos_joint',
    'odowd_bulk_pressure': 'barbelo_modulus',
    'sterile_sector': 'barbelo_modulus',  # Same value (163)
    'roots_total': 'nitzotzin_roots',
    'visible_sector': 'sophian_modulus',
    'sophian_registry': 'sophian_modulus',  # v23.2.29 update

    # CENTRAL SAMPLER
    'central_pair': 'reid_pair',
    'central_pair_weight': 'watts_weight',
    'central_activation_threshold': 'gnosis_threshold',
}

# Gnostic name updates (for GNOSTIC_MAP)
GNOSTIC_UPDATES = {
    'The Monad': 'The Monad',  # Same
    'The Pleroma': 'Elder Vessels',
    'The Sophia': 'Sophia Pressure',  # For 163
    'The Demiurge': 'Shem HaMephorash',  # For chi_eff=72
    'The Christos': 'Logos Joint',
    'The Barbelo': 'Sophia Pressure',
    'The Ennoia': 'Nitzotzin Roots',
    'The Decad': 'The Hand',
    'The Horos': 'The Boundary',
}


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    parts = path.parts
    return any(skip in parts for skip in SKIP_DIRS)


def find_occurrences(old_name: str) -> dict:
    """Find all occurrences of old_name in the codebase."""
    results = defaultdict(list)

    # Patterns to match
    patterns = [
        rf'\b{old_name}\b',  # Exact word match
        rf'"{old_name}"',     # In quotes
        rf"'{old_name}'",     # In single quotes
        rf'\.{old_name}\b',   # As property access
        rf'self\._{old_name}',  # As private attribute
        rf'self\.{old_name}',   # As public attribute
    ]

    combined_pattern = '|'.join(patterns)
    regex = re.compile(combined_pattern)

    for root, dirs, files in os.walk(ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            filepath = Path(root) / file

            if filepath.suffix not in EXTENSIONS:
                continue

            if should_skip(filepath):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        rel_path = filepath.relative_to(ROOT)
                        results[str(rel_path)].append((i, line.strip()[:100]))
            except Exception as e:
                pass

    return results


def main():
    print("=" * 80)
    print(" PARAMETER RENAME SEARCH REPORT")
    print("=" * 80)

    total_files = 0
    total_occurrences = 0

    for old_name, new_name in RENAMES.items():
        print(f"\n{'-' * 80}")
        print(f" {old_name} -> {new_name}")
        print(f"{'-' * 80}")

        results = find_occurrences(old_name)

        if not results:
            print("  No occurrences found.")
            continue

        file_count = len(results)
        occurrence_count = sum(len(locs) for locs in results.values())
        total_files += file_count
        total_occurrences += occurrence_count

        print(f"  Found in {file_count} files ({occurrence_count} occurrences):\n")

        for filepath, locations in sorted(results.items()):
            print(f"  [FILE] {filepath} ({len(locations)} occurrences)")
            for line_num, content in locations[:3]:  # Show first 3
                # ASCII-safe output
                safe_content = content[:70].encode('ascii', 'replace').decode('ascii')
                print(f"      L{line_num}: {safe_content}...")
            if len(locations) > 3:
                print(f"      ... and {len(locations) - 3} more")

    print(f"\n{'=' * 80}")
    print(f" SUMMARY")
    print(f"{'=' * 80}")
    print(f"  Total unique old names: {len(RENAMES)}")
    print(f"  Total files affected:   {total_files}")
    print(f"  Total occurrences:      {total_occurrences}")
    print(f"{'=' * 80}")

    # Write detailed report
    report_path = ROOT / "docs" / "Updates" / "PARAMETER_RENAME_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Parameter Rename Report\n\n")
        f.write("## Proposed Renames\n\n")
        f.write("| Old Name | New Name | Gematria | Hebrew |\n")
        f.write("|----------|----------|----------|--------|\n")

        gematria_map = {
            'monad_unity': ('1', 'א (Aleph)'),
            'residual_key': ('10', 'י (Yod)'),
            'elder_vessels': ('24', 'כד (Kad)'),
            'horos_limit': ('27', 'כז (Kaz)'),
            'mephorash_chi': ('72', 'עב (Av)'),
            'demiurgic_gates': ('135', 'קלה (Kalah)'),
            'logos_joint': ('153', 'קנג'),
            'barbelo_modulus': ('163', 'צ (Tsade)'),
            'nitzotzin_roots': ('288', 'רפח'),
            'reid_pair': ('200', 'ר (Resh)'),
            'watts_weight': ('~261', 'רϕ'),
            'gnosis_threshold': ('9', 'ט (Tet)'),
        }

        for old, new in RENAMES.items():
            gem, heb = gematria_map.get(new, ('', ''))
            f.write(f"| `{old}` | `{new}` | {gem} | {heb} |\n")

        f.write("\n## Occurrences by File\n\n")

        for old_name, new_name in RENAMES.items():
            results = find_occurrences(old_name)
            if results:
                f.write(f"\n### `{old_name}` → `{new_name}`\n\n")
                for filepath, locations in sorted(results.items()):
                    f.write(f"- **{filepath}** ({len(locations)} occurrences)\n")

    print(f"\n  Detailed report saved to: {report_path}")


if __name__ == "__main__":
    main()
