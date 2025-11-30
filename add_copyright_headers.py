#!/usr/bin/env python3
"""Add copyright headers to all HTML files"""

import os
import glob
import re

# Copyright header for HTML files
html_copyright = """<!--
    Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

    This is the intellectual property of Andrew Keith Watts. Unauthorized
    reproduction, distribution, or modification of this code, in whole or in part,
    without the express written permission of Andrew Keith Watts is strictly prohibited.

    For inquiries, please contact AndrewKWatts@Gmail.com
-->
"""

# Find all HTML files
html_files = []
html_files.extend(glob.glob('*.html'))
html_files.extend(glob.glob('foundations/*.html'))
html_files.extend(glob.glob('sections/*.html'))
html_files.extend(glob.glob('diagrams/*.html'))

# Process each file
added_count = 0
skipped_count = 0

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if copyright already exists
        if 'Copyright (c) 2025 Andrew Keith Watts' in content:
            skipped_count += 1
            continue

        # Add copyright after DOCTYPE or at the very beginning
        if '<!DOCTYPE html>' in content:
            content = content.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n' + html_copyright, 1)
        else:
            content = html_copyright + content

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        added_count += 1
        print(f"Added copyright to: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"\nDone!")
print(f"- Added copyright to {added_count} files")
print(f"- Skipped {skipped_count} files (already had copyright)")
