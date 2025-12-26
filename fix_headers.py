#!/usr/bin/env python3
"""
Fix HTML headers to be consistent across all pages.
Uses the header from index.html as the reference.
"""

import re
import os
from pathlib import Path

# Define the correct header templates for different page types

# For root-level pages (references.html, etc.)
ROOT_HEADER_TEMPLATE = '''    <header>
        <div class="header-content">
            <div class="site-title" style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">Principia Metaphysica</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="sections/index.html">Sections</a></li>
                    <li><a href="foundations/index.html">Foundations</a></li>
                    <li><a href="references.html">References</a></li>
                    <li class="user-controls-nav">
                        <div class="user-controls">
                            <img id="user-avatar" src="/images/default-avatar.svg" alt="User">
                            <span id="user-email"></span>
                            <button id="logout-btn">Logout</button>
                        </div>
                        <button id="header-login-btn" class="header-login-btn">
                            <img src="/images/google-icon.svg" alt="G" class="google-icon-small">
                            Login
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
    </header>'''

# For sections/*.html pages
SECTIONS_HEADER_TEMPLATE = '''    <header>
        <div class="header-content">
            <div class="site-title" style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">Principia Metaphysica</div>
            <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="index.html">Sections</a></li>
                    <li><a href="../foundations/index.html">Foundations</a></li>
                    <li><a href="../references.html">References</a></li>
                    <li class="user-controls-nav">
                        <div class="user-controls">
                            <img id="user-avatar" src="/images/default-avatar.svg" alt="User">
                            <span id="user-email"></span>
                            <button id="logout-btn">Logout</button>
                        </div>
                        <button id="header-login-btn" class="header-login-btn">
                            <img src="/images/google-icon.svg" alt="G" class="google-icon-small">
                            Login
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
    </header>'''

# For foundations/*.html pages
FOUNDATIONS_HEADER_TEMPLATE = '''    <header>
        <div class="header-content">
            <div class="site-title" style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">Principia Metaphysica</div>
            <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../sections/index.html">Sections</a></li>
                    <li><a href="index.html">Foundations</a></li>
                    <li><a href="../references.html">References</a></li>
                    <li class="user-controls-nav">
                        <div class="user-controls">
                            <img id="user-avatar" src="/images/default-avatar.svg" alt="User">
                            <span id="user-email"></span>
                            <button id="logout-btn">Logout</button>
                        </div>
                        <button id="header-login-btn" class="header-login-btn">
                            <img src="/images/google-icon.svg" alt="G" class="google-icon-small">
                            Login
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
    </header>'''


def fix_header(file_path, header_template):
    """Replace the header in a file with the correct template."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the entire header block (including broken ones with user-controls outside)
    # This matches from <header> to </header> including any user-controls divs that might be outside
    pattern = r'<header>.*?</header>(?:\s*<div class="user-controls">.*?</div>)?'

    # Check if a header exists
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Replace the header
        new_content = re.sub(pattern, header_template, content, count=1, flags=re.DOTALL)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    return False


def main():
    base_dir = Path('h:/Github/PrincipiaMetaphysica')

    # Fix root-level HTML files (except index.html and principia-metaphysica-paper.html)
    root_files = [
        'references.html',
        'simulations.html',
        'beginners-guide.html',
        'appendices.html',
        'visualization-index.html',
        'ancient-numerology.html',
        'mystical-nomenclature-archive.html',
        'philosophical-implications.html',
    ]

    print("Fixing root-level files...")
    for filename in root_files:
        file_path = base_dir / filename
        if file_path.exists():
            if fix_header(file_path, ROOT_HEADER_TEMPLATE):
                print(f"  ✓ Fixed {filename}")
            else:
                print(f"  - No header found in {filename}")

    # Fix sections/*.html files
    sections_dir = base_dir / 'sections'
    print("\nFixing sections/*.html files...")
    for file_path in sections_dir.glob('*.html'):
        if fix_header(file_path, SECTIONS_HEADER_TEMPLATE):
            print(f"  ✓ Fixed {file_path.name}")
        else:
            print(f"  - No header found in {file_path.name}")

    # Fix foundations/*.html files
    foundations_dir = base_dir / 'foundations'
    print("\nFixing foundations/*.html files...")
    for file_path in foundations_dir.glob('*.html'):
        if fix_header(file_path, FOUNDATIONS_HEADER_TEMPLATE):
            print(f"  ✓ Fixed {file_path.name}")
        else:
            print(f"  - No header found in {file_path.name}")

    print("\nDone!")


if __name__ == '__main__':
    main()
