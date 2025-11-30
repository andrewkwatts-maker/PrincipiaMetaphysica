#!/usr/bin/env python3
"""
Add complete copyright attribution to all files.
Ensures Andrew K Watts owns all intellectual property with AI tools credited as assistants.
"""

import os
import re
from pathlib import Path

# Copyright headers
HTML_COPYRIGHT = """<!--
    Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

    This is the intellectual property of Andrew Keith Watts. Unauthorized
    reproduction, distribution, or modification of this code, in whole or in part,
    without the express written permission of Andrew Keith Watts is strictly prohibited.

    For inquiries, please contact AndrewKWatts@Gmail.com
-->
"""

PYTHON_COPYRIGHT = """#!/usr/bin/env python3
\"\"\"
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
\"\"\"

"""

# Correct footer with Andrew K Watts ownership and AI attribution
CORRECT_FOOTER = '''    <footer>
        <p>
            <strong>Principia Metaphysica</strong><br>
            &copy; 2025 Andrew Keith Watts. All rights reserved.
        </p>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">
            This project was developed with the assistance of AI tools including Claude (Anthropic),
            Grok (xAI), and Gemini (Google).
        </p>
    </footer>'''

repo_root = Path(r'h:\Github\PrincipiaMetaphysica')

def add_html_copyright():
    """Add copyright headers to HTML files that are missing them."""

    # Find HTML files in components and solutions directories
    html_files = (
        list((repo_root / 'components').glob('*.html')) +
        list((repo_root / 'solutions').glob('*.html'))
    )

    updated = []

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already has copyright
            if 'Copyright (c) 2025 Andrew Keith Watts' in content:
                continue

            # Add copyright after DOCTYPE
            if '<!DOCTYPE html>' in content:
                content = content.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n' + HTML_COPYRIGHT, 1)
            elif '<html' in content:
                # Some files might not have DOCTYPE
                content = HTML_COPYRIGHT + '\n' + content
            else:
                print(f"Warning: Cannot add copyright to {filepath.name} - no DOCTYPE or html tag")
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            updated.append(filepath.name)

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")

    return updated

def add_html_footer():
    """Add or fix footer attribution in HTML files."""

    # Find HTML files that need footer updates
    html_files = (
        list((repo_root / 'components').glob('*.html')) +
        list((repo_root / 'solutions').glob('*.html'))
    )

    updated = []

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if file has a footer
            if '<footer>' not in content:
                continue

            # Extract and check footer
            footer_match = re.search(r'<footer>.*?</footer>', content, re.DOTALL)
            if not footer_match:
                continue

            old_footer = footer_match.group(0)

            # Check if footer needs updating
            needs_update = False

            # Missing Andrew K Watts copyright
            if '&copy; 2025 Andrew Keith Watts' not in old_footer and '© 2025 Andrew Keith Watts' not in old_footer:
                needs_update = True

            # Check AI attribution
            has_claude = 'Claude' in old_footer or 'Anthropic' in old_footer
            has_grok = 'Grok' in old_footer or 'xAI' in old_footer
            has_gemini = 'Gemini' in old_footer or 'Google' in old_footer

            # If any AI mentioned, all three must be mentioned
            if (has_claude or has_grok or has_gemini) and not (has_claude and has_grok and has_gemini):
                needs_update = True

            # Remove problematic "Generated with" language
            if 'Generated with' in old_footer or 'Co-Authored-By' in old_footer:
                needs_update = True

            if needs_update:
                content = content.replace(old_footer, CORRECT_FOOTER)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                updated.append(filepath.name)

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")

    return updated

def add_python_copyright():
    """Add copyright headers to Python files."""

    py_files = [
        'add_foundation_links.py',
        'add_foundation_links_printable.py',
        'add_theory_links_to_foundations.py',
        'asymptotic_safety_gauge.py',
        'config.py',
        'gauge_unification_merged.py',
        'generate_js_constants.py',
        'remove_v65_references.py',
        'scan_v6_references.py',
        'simplify_paper_abstract.py',
        'SimulateTheory.py',
        'threshold_corrections.py',
        'update_footer_copyright.py',
        'update_paper_to_current_framework.py',
        'validation_modules.py'
    ]

    updated = []

    for filename in py_files:
        filepath = repo_root / filename

        if not filepath.exists():
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already has copyright
            if 'Copyright (c) 2025 Andrew Keith Watts' in content:
                continue

            # Remove shebang if present, we'll re-add it
            lines = content.split('\n')
            if lines[0].startswith('#!'):
                shebang = lines[0]
                content = '\n'.join(lines[1:])
            else:
                shebang = None

            # Add copyright
            if shebang:
                new_content = shebang + '\n' + PYTHON_COPYRIGHT + content.lstrip()
            else:
                new_content = PYTHON_COPYRIGHT + content.lstrip()

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            updated.append(filename)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return updated

def main():
    print("Adding copyright attribution to all files...\n")

    print("1. Adding copyright headers to HTML files...")
    html_headers = add_html_copyright()
    if html_headers:
        print(f"   Updated {len(html_headers)} files:")
        for name in html_headers:
            print(f"     - {name}")
    else:
        print("   All HTML files already have copyright headers")

    print("\n2. Updating HTML footers...")
    html_footers = add_html_footer()
    if html_footers:
        print(f"   Updated {len(html_footers)} files:")
        for name in html_footers:
            print(f"     - {name}")
    else:
        print("   All HTML footers already correct")

    print("\n3. Adding copyright headers to Python files...")
    py_headers = add_python_copyright()
    if py_headers:
        print(f"   Updated {len(py_headers)} files:")
        for name in py_headers:
            print(f"     - {name}")
    else:
        print("   All Python files already have copyright headers")

    total = len(html_headers) + len(html_footers) + len(py_headers)
    print(f"\nTotal files updated: {total}")
    print("\nAll intellectual property is now correctly attributed to Andrew K Watts.")
    print("AI tools (Claude, Grok, Gemini) are credited as development assistants.")

if __name__ == '__main__':
    main()
