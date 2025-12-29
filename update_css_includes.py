#!/usr/bin/env python3
"""
Update all HTML pages to include the new UX consistency CSS files.

This script adds:
- pm-header.css
- pm-ux-consistency.css
- mobile-responsive.css

To pages that don't already have them.
"""

import os
import re
from pathlib import Path

# CSS files to add
CSS_FILES = [
    'pm-header.css',
    'pm-ux-consistency.css',
    'mobile-responsive.css'
]

def update_html_file(filepath):
    """Update a single HTML file with new CSS includes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'pm-ux-consistency.css' in content:
        print(f"[OK] {filepath.name} - Already updated")
        return False

    # Find the last stylesheet link
    last_css_pattern = r'(<link[^>]*rel=["\']stylesheet["\'][^>]*>)'
    matches = list(re.finditer(last_css_pattern, content))

    if not matches:
        print(f"[SKIP] {filepath.name} - No stylesheet links found")
        return False

    # Get the last match
    last_match = matches[-1]
    insert_pos = last_match.end()

    # Determine the path prefix (../ for pages/, ./ for root)
    if 'pages' in str(filepath):
        prefix = '../css/'
    else:
        prefix = 'css/'

    # Build the CSS includes to add
    css_includes = []

    # Check which files are missing
    for css_file in CSS_FILES:
        if css_file not in content:
            css_includes.append(f'    <link rel="stylesheet" href="{prefix}{css_file}">')

    if not css_includes:
        print(f"[OK] {filepath.name} - All CSS files already present")
        return False

    # Insert the new CSS includes
    new_content = (
        content[:insert_pos] +
        '\n' + '\n'.join(css_includes) +
        content[insert_pos:]
    )

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[UPDATED] {filepath.name} - Added {len(css_includes)} CSS file(s)")
    return True

def main():
    """Update all HTML files in the project."""
    root_dir = Path(__file__).parent

    # Files to update
    html_files = []

    # Root HTML files
    html_files.extend(root_dir.glob('*.html'))

    # Pages directory
    pages_dir = root_dir / 'pages'
    if pages_dir.exists():
        html_files.extend(pages_dir.glob('*.html'))

    print("Updating HTML files with new CSS includes...\n")
    print("=" * 60)

    updated_count = 0
    for filepath in sorted(html_files):
        # Skip test files
        if 'test' in filepath.name.lower():
            print(f"[SKIP] {filepath.name} - Skipping test file")
            continue

        if update_html_file(filepath):
            updated_count += 1

    print("=" * 60)
    print(f"\n[DONE] Complete! Updated {updated_count} file(s)")

if __name__ == '__main__':
    main()
