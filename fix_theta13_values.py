#!/usr/bin/env python3
"""
Fix theta_13 neutrino mixing angle values in HTML files.

Changes theta_13 from calibrated 8.57° to geometrically derived 8.65°
based on v14.1 pure geometric derivation.
"""

import re
import sys
from pathlib import Path

def fix_file(filepath, replacements, dry_run=False):
    """Apply replacements to a file."""
    print(f"\nProcessing: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        for old, new, description in replacements:
            count = content.count(old)
            if count > 0:
                print(f"  {description}: {count} occurrence(s)")
                content = content.replace(old, new)
                changes_made += count

        if changes_made > 0:
            if dry_run:
                print(f"  [DRY RUN] Would make {changes_made} change(s)")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Made {changes_made} change(s)")
        else:
            print("  No changes needed")

        return changes_made

    except Exception as e:
        print(f"  ERROR: {e}")
        return 0

def main():
    """Main function."""
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("=" * 70)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 70)

    base_dir = Path(__file__).parent

    # Fix principia-metaphysica-paper.html
    # This replaces the CALIBRATED row with DERIVED and 8.65°
    paper_html = base_dir / "principia-metaphysica-paper.html"
    paper_replacements = [
        (
            """                <tr>
                    <td>$\\theta_{13}$</td>
                    <td>8.57&deg;</td>
                    <td>$8.57 \\pm 0.12$&deg;</td>
                    <td>CALIBRATED</td>
                </tr>""",
            """                <tr>
                    <td>$\\theta_{13}$</td>
                    <td>8.65&deg;</td>
                    <td>$8.57 \\pm 0.12$&deg;</td>
                    <td>DERIVED</td>
                </tr>""",
            "Update theta_13 table row (CALIBRATED -> DERIVED, 8.57 -> 8.65)"
        )
    ]

    # Fix beginners-guide.html
    beginners_html = base_dir / "beginners-guide.html"
    beginners_replacements = [
        (
            "θ<sub>13</sub> = 8.57°",
            "θ<sub>13</sub> = 8.65°",
            "Update theta_13 value in PMNS description"
        )
    ]

    # Fix principia-metaphysica-paper-old.html (optional)
    old_paper_html = base_dir / "principia-metaphysica-paper-old.html"
    old_paper_replacements = [
        (
            "$\\theta_{13} = 8.57^\\circ$",
            "$\\theta_{13} = 8.65^\\circ$",
            "Update theta_13 in old paper (constraint description)"
        ),
        (
            "\\(\\theta_{13} = 8.57°\\) calibrated to NuFIT",
            "\\(\\theta_{13} = 8.65°\\) derived from G₂ topology",
            "Update theta_13 calibration note to derivation note"
        )
    ]

    total_changes = 0

    # Process each file
    if paper_html.exists():
        total_changes += fix_file(paper_html, paper_replacements, dry_run)
    else:
        print(f"WARNING: {paper_html} not found")

    if beginners_html.exists():
        total_changes += fix_file(beginners_html, beginners_replacements, dry_run)
    else:
        print(f"WARNING: {beginners_html} not found")

    if old_paper_html.exists():
        total_changes += fix_file(old_paper_html, old_paper_replacements, dry_run)
    else:
        print(f"INFO: {old_paper_html} not found (optional file)")

    print("\n" + "=" * 70)
    if dry_run:
        print(f"DRY RUN COMPLETE: Would make {total_changes} total change(s)")
        print("Run without --dry-run to apply changes")
    else:
        print(f"COMPLETE: Made {total_changes} total change(s)")
    print("=" * 70)

    # Verification suggestions
    print("\nVERIFICATION COMMANDS:")
    print("  grep -n '8\\.57' *.html | grep -i theta")
    print("  grep -n '8\\.65' *.html | grep -i theta")
    print("  grep -n 'CALIBRATED' *.html | grep -i theta")

if __name__ == '__main__':
    main()
