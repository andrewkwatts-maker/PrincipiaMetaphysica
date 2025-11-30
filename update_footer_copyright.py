#!/usr/bin/env python3
"""Update footer copyright with AI attribution in all HTML files"""

import os
import glob
import re

# New footer with AI attribution
new_footer = '''    <footer>
        <p>
            <strong>Principia Metaphysica</strong><br>
            &copy; 2025 Andrew Keith Watts. All rights reserved.
        </p>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">
            This project was developed with the assistance of AI tools including Claude (Anthropic),
            Grok (xAI), and Gemini (Google).
        </p>
    </footer>'''

# Find all HTML files
html_files = []
html_files.extend(glob.glob('*.html'))
html_files.extend(glob.glob('foundations/*.html'))
html_files.extend(glob.glob('sections/*.html'))
html_files.extend(glob.glob('diagrams/*.html'))

# Process each file
updated_count = 0

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find and replace the footer
        # Match footer with various content patterns
        footer_pattern = r'<footer>.*?</footer>'

        if re.search(footer_pattern, content, re.DOTALL):
            # Replace with new footer
            content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)

            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            updated_count += 1
            print(f"Updated footer in: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"\nDone! Updated {updated_count} files with AI attribution in footer")
