#!/usr/bin/env python3
"""Fix the Math input errors in section 6.2a of the paper."""

import re

# Read the file
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the broken formulas in section 6.2a
# The issue is that backslashes have been replaced with tab characters or corrupted

# Fix line 1922: Main equation - use raw string properly
content = re.sub(
    r'\$\$m_t = y_t [^\$]*\$\$',
    r'$$m_t = y_t \\times \\frac{v_{\\text{EW}}}{\\sqrt{2}} = 172.7 \\text{ GeV}$$',
    content,
    count=1
)

# Fix the derivation steps - find the section and replace
section_pattern = r'(<h3 class="subsection-title">6\.2a Top Quark Mass</h3>.*?<h3 class="subsection-title">6\.2b)'

def fix_section(match):
    section = match.group(0)

    # Fix VEV line - match any characters including tabs
    section = re.sub(
        r'VEV from Section 5\.6: \$v_\{[^\$]*\} = 173\.97\$ GeV',
        r'VEV from Section 5.6: $v_{\\text{EW}} = 173.97$ GeV',
        section
    )

    # Fix mass formula line
    section = re.sub(
        r'Mass formula: \$m_t = y_t [^\$]*\$',
        r'Mass formula: $m_t = y_t \\times v / \\sqrt{2}$',
        section
    )

    # Fix approx line
    section = re.sub(
        r'yields \$y_t [^\$]*1\.0\$',
        r'yields $y_t \\approx 1.0$',
        section
    )

    # Fix result line
    section = re.sub(
        r'Result: \$m_t = 1\.0 [^\$]*= 172\.7\$ GeV',
        r'Result: $m_t = 1.0 \\times 173.97 / \\sqrt{2} = 172.7$ GeV',
        section
    )

    return section

content = re.sub(section_pattern, fix_section, content, flags=re.DOTALL)

# Write the fixed content
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed section 6.2a!")
