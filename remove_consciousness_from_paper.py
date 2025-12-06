"""
Remove consciousness and fringe concepts from principia-metaphysica-paper.html

Keep the paper focused on mathematics, physics, and geometric proofs only.
Consciousness discussion will remain on the website (philosophical-implications.html).

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re

filepath = "h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove Section 7.5 from table of contents
# Find the TOC entry and remove it
toc_pattern = r'<li>\s*<a href="#philosophical_implications">\s*7\.5.*?</a>\s*</li>'
content = re.sub(toc_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

# Also handle the broader multi-line pattern
toc_pattern2 = r'<li>\s*<a href="#philosophical_implications">\s*7\.5 Speculative.*?Hidden Variables\s*</a>\s*<ul>.*?</ul>\s*</li>'
content = re.sub(toc_pattern2, '', content, flags=re.DOTALL | re.IGNORECASE)

# Alternative simpler approach - just remove lines containing the TOC entry
lines = content.split('\n')
new_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue

    # Skip TOC entry for 7.5
    if '7.5 Speculative: Consciousness' in line or '7.5 Speculative' in line:
        # Skip this line and potentially next few lines if they're part of the same entry
        skip_next = 0
        continue

    new_lines.append(line)

content = '\n'.join(new_lines)

# Find the start and end of Section 7.5
# Start: <h3 id="philosophical_implications">
# End: <h3 id="asymptotic_safety">

# Pattern to match entire Section 7.5
section_pattern = r'<h3 id="philosophical_implications">.*?(?=<h3 id="asymptotic_safety">)'

# Remove the entire section
content = re.sub(section_pattern, '', content, flags=re.DOTALL)

# Renumber Section 7.6 to 7.5
content = content.replace('7.6 Asymptotic Safety', '7.5 Asymptotic Safety')
content = content.replace('id="asymptotic_safety"', 'id="asymptotic_safety"')  # Keep ID same
content = content.replace('(7.6)', '(7.5)')  # Equation number
content = content.replace('Eq. 7.6', 'Eq. 7.5')

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"OK: Removed Section 7.5 (Consciousness & Hidden Variables) from {filepath}")
print("Renumbered Section 7.6 -> 7.5 (Asymptotic Safety)")
print("\nConsciousness discussion remains available on:")
print("  - philosophical-implications.html")
print("  - sections/thermal-time.html (speculative section)")
print("\nThe paper now focuses purely on mathematics, physics, and geometric proofs.")
