#!/usr/bin/env python3
"""
Atomically fix theta_13 values in HTML files.

This script uses atomic file operations to safely update the files
even if they're being monitored by file watchers.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def atomic_replace_in_file(filepath, replacements):
    """
    Atomically replace strings in a file.

    Creates a temp file, makes changes, then atomically moves it.
    This avoids issues with file watchers and concurrent modifications.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"SKIP: {filepath} does not exist")
        return 0

    # Read the original file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply replacements
    original_content = content
    changes_made = 0

    for old, new, description in replacements:
        count = content.count(old)
        if count > 0:
            print(f"  • {description}")
            print(f"    Found {count} occurrence(s)")
            content = content.replace(old, new)
            changes_made += count

    if changes_made == 0:
        print(f"  No changes needed in {filepath.name}")
        return 0

    # Write to temporary file in same directory
    # (same directory ensures atomic move is possible)
    temp_fd, temp_path = tempfile.mkstemp(
        dir=filepath.parent,
        prefix='.tmp_',
        suffix='.html',
        text=True
    )

    try:
        # Write new content to temp file
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            f.write(content)

        # Preserve file permissions
        shutil.copystat(filepath, temp_path)

        # Atomic move (replaces original file)
        # On Windows, need to remove destination first
        if os.name == 'nt':
            try:
                os.replace(temp_path, filepath)
            except OSError:
                # Fallback for older Windows
                os.remove(filepath)
                shutil.move(temp_path, filepath)
        else:
            os.replace(temp_path, filepath)

        print(f"  ✓ Updated {filepath.name} ({changes_made} changes)")
        return changes_made

    except Exception as e:
        # Clean up temp file on error
        try:
            os.remove(temp_path)
        except:
            pass
        raise e

def main():
    """Main function."""
    base_dir = Path(__file__).parent

    print("=" * 70)
    print("THETA_13 FIX - Atomic File Updates")
    print("=" * 70)
    print()
    print("Changing theta_13 from 8.57° (calibrated) to 8.65° (derived)")
    print("Based on v14.1 pure geometric derivation")
    print()

    total_changes = 0

    # 1. Fix principia-metaphysica-paper.html
    print("[1/3] principia-metaphysica-paper.html")
    paper_html = base_dir / "principia-metaphysica-paper.html"
    paper_replacements = [
        (
            "                <tr>\n" +
            "                    <td>$\\theta_{13}$</td>\n" +
            "                    <td>8.57&deg;</td>\n" +
            "                    <td>$8.57 \\pm 0.12$&deg;</td>\n" +
            "                    <td>CALIBRATED</td>\n" +
            "                </tr>",
            "                <tr>\n" +
            "                    <td>$\\theta_{13}$</td>\n" +
            "                    <td>8.65&deg;</td>\n" +
            "                    <td>$8.57 \\pm 0.12$&deg;</td>\n" +
            "                    <td>DERIVED</td>\n" +
            "                </tr>",
            "Table row: 8.57° CALIBRATED → 8.65° DERIVED"
        )
    ]
    total_changes += atomic_replace_in_file(paper_html, paper_replacements)
    print()

    # 2. Fix beginners-guide.html
    print("[2/3] beginners-guide.html")
    beginners_html = base_dir / "beginners-guide.html"
    beginners_replacements = [
        (
            "θ<sub>13</sub> = 8.57°",
            "θ<sub>13</sub> = 8.65°",
            "PMNS values description"
        )
    ]
    total_changes += atomic_replace_in_file(beginners_html, beginners_replacements)
    print()

    # 3. Fix principia-metaphysica-paper-old.html (optional)
    print("[3/3] principia-metaphysica-paper-old.html (optional)")
    old_paper_html = base_dir / "principia-metaphysica-paper-old.html"
    old_paper_replacements = [
        (
            "$\\theta_{13} = 8.57^\\circ$",
            "$\\theta_{13} = 8.65^\\circ$",
            "Constraint description"
        ),
        (
            "\\(\\theta_{13} = 8.57°\\) calibrated to NuFIT",
            "\\(\\theta_{13} = 8.65°\\) derived from G₂ topology",
            "Derivation method note"
        )
    ]
    total_changes += atomic_replace_in_file(old_paper_html, old_paper_replacements)
    print()

    # Summary
    print("=" * 70)
    print(f"COMPLETE: {total_changes} total changes made")
    print("=" * 70)
    print()

    if total_changes > 0:
        print("VERIFY CHANGES:")
        print("  grep -n '8\\.65.*theta' *.html")
        print("  grep -n 'DERIVED' *.html | grep theta_13")
        print()
        print("ENSURE EXPERIMENTAL VALUES UNCHANGED:")
        print("  grep -n '8\\.57.*0\\.12' *.html  # Should show NuFIT experimental values")

    return 0 if total_changes > 0 else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nAborted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
