#!/usr/bin/env python3
"""
Bulk Hebrew Rename Script v23.2
===============================
Systematically renames Hebrew properties across the codebase with validation.

Usage:
    python scripts/bulk_hebrew_rename.py --dry-run           # Preview changes
    python scripts/bulk_hebrew_rename.py --apply             # Apply changes
    python scripts/bulk_hebrew_rename.py --apply --dir simulations  # Apply to specific dir
    python scripts/bulk_hebrew_rename.py --validate          # Validate after changes

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Project root
ROOT = Path(__file__).parent.parent

# v23.2 Rename mappings: old_name -> (new_name, value, symbol, hebrew)
RENAMES = {
    # Property renames - Registry access patterns
    "elder_vessels": ("governing_elder_kad", 24, r"\mathcal{E}_{\text{כד}}", "Kad"),
    "elders": ("governing_elder_kad", 24, r"\mathcal{E}_{\text{כד}}", "Kad"),
    "demiurgic_gates": ("demiurgic_Yetts", 135, "Yd", "Kalah"),
    "ennoia_chi": ("qedem_chi_sum", 144, "chi_Q", "Qedem"),
    "bridge_effective": ("Echad_Prime", 13, "Yud-Gimel", "Echad"),
    "bridge_local": ("Dodecad_Anchors", 12, "Bet-Yod", "Dodecad"),
    "Dodecad_Anchor": ("Dodecad_Anchors", 12, "Bet-Yod", "Dodecad"),
}

# Files to skip (core definitions)
SKIP_FILES = {
    "FormulasRegistry.py",  # Will be updated manually
    "bulk_hebrew_rename.py",
    "find_old_names.py",
    "update_to_hebrew_names.py",
}

# Directories to skip
SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "Principia_Metaphysica-Demon_Lock",
    "Principia_Metaphysica-Demon_Lock_FULL",
}

# TODO file path
TODO_FILE = ROOT / "docs" / "Updates" / "HEBREW_RENAME_TODO.md"


def create_patterns() -> Dict[str, Tuple[re.Pattern, str]]:
    """Create regex patterns for each rename."""
    patterns = {}

    # Registry access prefixes
    registry_prefixes = r'(?:reg|registry|REGISTRY|_SSOT|_registry|_REG|self\.reg|self\.registry|self\._registry|self\.)'

    for old_name, (new_name, value, symbol, hebrew) in RENAMES.items():
        # Pattern 1: Registry property access (e.g., reg.elder_vessels)
        pattern1 = rf'({registry_prefixes})\.{old_name}(?![a-zA-Z0-9_])'
        replacement1 = rf'\1.{new_name}'
        patterns[f"{old_name}_prop"] = (re.compile(pattern1), replacement1)

        # Pattern 2: String references (e.g., "elder_vessels" in dicts)
        pattern2 = rf'(["\'])({old_name})(["\'])'
        replacement2 = rf'\1{new_name}\3'
        patterns[f"{old_name}_str"] = (re.compile(pattern2), replacement2)

    return patterns


def should_skip_file(filepath: Path) -> bool:
    """Check if file should be skipped."""
    return filepath.name in SKIP_FILES


def should_skip_dir(dirpath: Path) -> bool:
    """Check if directory should be skipped."""
    return any(skip in str(dirpath) for skip in SKIP_DIRS)


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
        print(f"  [ERROR] Could not read {filepath}: {e}")
        return changes

    new_lines = []
    for i, line in enumerate(lines, 1):
        new_line = line
        for pattern_name, (pattern, replacement) in patterns.items():
            new_line = pattern.sub(replacement, new_line)

        if new_line != line:
            changes.append((i, line.rstrip(), new_line.rstrip()))
        new_lines.append(new_line)

    if changes and not dry_run:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"  [ERROR] Could not write {filepath}: {e}")
            return []

    return changes


def update_todo_file(rename_name: str, status: str):
    """Update the TODO tracking file."""
    if not TODO_FILE.exists():
        return

    try:
        content = TODO_FILE.read_text(encoding='utf-8')

        # Update status checkbox
        old_pattern = rf'\| `{rename_name}` \|.*?\| \[ \] PENDING \|'
        new_status = f'| `{rename_name}` |.*| [x] {status} |'

        # Simple update - mark as done
        content = content.replace(f'| `{rename_name}` |', f'| `{rename_name}` |')

        # Add to validation log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n{timestamp} - Renamed {rename_name} - {status}"

        if "## Validation Log" in content:
            content = content.replace("```\n[timestamp]", f"```\n{log_entry}\n[timestamp]")

        TODO_FILE.write_text(content, encoding='utf-8')
    except Exception as e:
        print(f"  [WARNING] Could not update TODO file: {e}")


def run_rename(target_dir: Optional[str] = None, dry_run: bool = True, verbose: bool = False):
    """Run the rename operation."""
    patterns = create_patterns()

    # Determine directories to process
    if target_dir:
        process_dirs = [ROOT / target_dir]
    else:
        process_dirs = [
            ROOT / "simulations",
            ROOT / "core",
            ROOT / "scripts",
            ROOT / "tests",
            ROOT / "docs",
            ROOT / "Pages",
        ]

    print("=" * 80)
    print(" BULK HEBREW RENAME v23.2")
    print("=" * 80)
    print(f" MODE: {'DRY RUN' if dry_run else 'APPLYING CHANGES'}")
    print(f" Target: {target_dir or 'ALL directories'}")
    print("=" * 80)

    total_files = 0
    total_changes = 0

    for base_dir in process_dirs:
        if not base_dir.exists():
            continue

        for root, dirs, files in os.walk(base_dir):
            root_path = Path(root)

            # Skip excluded directories
            dirs[:] = [d for d in dirs if not should_skip_dir(root_path / d)]

            for filename in files:
                if not filename.endswith(('.py', '.md', '.html', '.json', '.txt')):
                    continue

                filepath = root_path / filename

                if should_skip_file(filepath):
                    continue

                changes = process_file(filepath, patterns, dry_run)

                if changes:
                    total_files += 1
                    total_changes += len(changes)

                    rel_path = filepath.relative_to(ROOT)
                    print(f"\n  {rel_path} ({len(changes)} changes)")

                    if verbose:
                        for line_num, old_line, new_line in changes[:5]:
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

        # Update TODO file
        for old_name in RENAMES.keys():
            update_todo_file(old_name, "COMPLETE")

    return total_files, total_changes


def validate_renames():
    """Validate that renames were applied correctly."""
    print("=" * 80)
    print(" VALIDATING RENAMES")
    print("=" * 80)

    # Check for remaining old names
    old_names_found = {}

    for old_name in RENAMES.keys():
        count = 0
        for ext in ['*.py', '*.md', '*.html']:
            for filepath in ROOT.rglob(ext):
                if should_skip_dir(filepath.parent):
                    continue
                if should_skip_file(filepath):
                    continue
                try:
                    content = filepath.read_text(encoding='utf-8', errors='ignore')
                    occurrences = len(re.findall(rf'\b{old_name}\b', content))
                    if occurrences > 0:
                        count += occurrences
                except:
                    pass

        if count > 0:
            old_names_found[old_name] = count
            print(f"  [WARNING] {old_name}: {count} occurrences remaining")
        else:
            print(f"  [OK] {old_name}: fully renamed")

    if old_names_found:
        print(f"\n  Total old names remaining: {sum(old_names_found.values())}")
    else:
        print("\n  All renames validated successfully!")

    return len(old_names_found) == 0


def main():
    parser = argparse.ArgumentParser(description="Bulk Hebrew rename script")
    parser.add_argument('--apply', action='store_true', help='Apply changes (default: dry run)')
    parser.add_argument('--dir', type=str, help='Target specific directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed changes')
    parser.add_argument('--validate', action='store_true', help='Validate renames were applied')

    args = parser.parse_args()

    if args.validate:
        success = validate_renames()
        sys.exit(0 if success else 1)

    dry_run = not args.apply
    run_rename(target_dir=args.dir, dry_run=dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
