#!/usr/bin/env python3
"""
fix_auth_loading_state.py - Update all HTML pages with auth-loading state

This script:
1. Changes body class from "not-authenticated" to "auth-loading"
2. Removes inline onclick handlers from header login buttons
3. Reports changes made

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
from pathlib import Path


def fix_auth_loading_state(file_path: Path) -> bool:
    """Fix auth loading state in a single HTML file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # 1. Change body class from not-authenticated to auth-loading
        content = re.sub(
            r'<body class="not-authenticated"',
            '<body class="auth-loading"',
            content
        )

        # 2. Remove onclick handler from header login button
        content = re.sub(
            r'(<button[^>]*id="header-login-btn"[^>]*)\s*onclick="[^"]*"([^>]*>)',
            r'\1\2',
            content
        )

        # Also handle reverse attribute order
        content = re.sub(
            r'(<button[^>]*)\s*onclick="[^"]*"([^>]*id="header-login-btn"[^>]*>)',
            r'\1\2',
            content
        )

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    project_root = Path(__file__).parent.parent

    # Find all HTML files with not-authenticated class
    html_files = []
    for pattern in ['*.html', 'sections/*.html', 'foundations/*.html',
                    'docs/*.html', 'diagrams/*.html', 'components/*.html',
                    'tests/*.html']:
        html_files.extend(project_root.glob(pattern))

    # Exclude node_modules and examples
    html_files = [f for f in html_files
                  if 'node_modules' not in str(f)
                  and 'examples' not in str(f)]

    modified_count = 0
    for file_path in sorted(set(html_files)):
        if fix_auth_loading_state(file_path):
            print(f"UPDATED: {file_path.relative_to(project_root)}")
            modified_count += 1

    print(f"\n{'='*60}")
    print(f"Total files modified: {modified_count}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
