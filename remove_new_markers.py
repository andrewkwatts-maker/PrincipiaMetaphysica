#!/usr/bin/env python3
"""
Remove "NEW:" markers and promotional language from section HTML files.
Present the theory as a unified whole rather than highlighting recent changes.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import os

# Files to process
section_files = [
    'sections/thermal-time.html',
    'sections/cosmology.html',
    'sections/predictions.html',
    'sections/fermion-sector.html',
    'sections/gauge-unification.html',
    'sections/geometric-framework.html'
]

def remove_new_markers(file_path):
    """Remove NEW: markers and promotional badges from HTML file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove "NEW:" prefix from headings and paragraphs
    content = re.sub(r'NEW:\s*', '', content, flags=re.IGNORECASE)

    # Remove promotional badges/boxes with "NEW" or "Major Breakthrough"
    # Match full div blocks with these terms
    content = re.sub(
        r'<div[^>]*style="[^"]*background[^"]*(?:#51cf66|green)[^"]*"[^>]*>.*?NEW.*?</div>\s*',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove "100% Geometry-Derived" promotional badges
    content = re.sub(
        r'<span[^>]*>100%\s+Geometry-Derived.*?</span>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove "Major Breakthrough" boxes
    content = re.sub(
        r'<div[^>]*class="success-box"[^>]*>.*?Major Breakthrough.*?</div>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Replace promotional language
    replacements = {
        'Major Milestone:': '',
        'Breakthrough:': '',
        '100% geometry-derived': 'geometry-derived',
        '100% Geometry-Derived': 'Geometry-Derived',
        'Zero Free Parameters': 'No Free Parameters',
        'Now includes': 'Includes',
        'now derived': 'derived',
        'Now derived': 'Derived',
        'Recent update:': '',
        'Latest:': ''
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Write back if changed
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
        return True
    else:
        print(f"No changes: {file_path}")
        return False

def main():
    """Process all section files"""
    total_updated = 0

    for file_path in section_files:
        if os.path.exists(file_path):
            if remove_new_markers(file_path):
                total_updated += 1
        else:
            print(f"File not found: {file_path}")

    print(f"\nTotal files updated: {total_updated}/{len(section_files)}")

if __name__ == '__main__':
    main()
