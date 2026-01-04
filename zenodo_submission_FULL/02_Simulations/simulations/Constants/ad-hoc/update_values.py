#!/usr/bin/env python3
"""
Helper script to update the gauge unification values in the HTML file

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import re

file_path = r"H:\Github\PrincipiaMetaphysica\sections\gauge-unification.html"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old values with new ones
replacements = [
    (r'<td style="padding: 0\.5rem; text-align: right; color: var\(--accent-primary\);">32\.5</td>',
     r'<td style="padding: 0.5rem; text-align: right; color: var(--accent-primary);">27.0</td>'),
    (r'<td style="padding: 0\.5rem; text-align: right; color: #ff7eb6;">18\.2</td>',
     r'<td style="padding: 0.5rem; text-align: right; color: #ff7eb6;">18.0</td>'),
    (r'<td style="padding: 0\.5rem; text-align: right; color: #51cf66;">22\.8</td>',
     r'<td style="padding: 0.5rem; text-align: right; color: #51cf66;">19.4</td>'),
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated gauge unification values:")
print("  AS: 32.5 -> 27.0")
print("  TC: 18.2 -> 18.0")
print("  KK: 22.8 -> 19.4")
