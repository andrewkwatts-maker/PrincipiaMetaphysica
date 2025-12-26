#!/usr/bin/env python3
"""Fix tab character corruption in LaTeX formulas."""

import re

# Read the file
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing tab character corruption in LaTeX...")

# Fix 1: Replace tab + "imes" with \times
count1 = len(re.findall(r'\times', content))
content = re.sub(r'\times', r'\\times', content)
print(f"Fixed {count1} instances of tab+imes to \\times")

# Fix 2: Replace tab + "ext{" with \text{
count2 = len(re.findall(r'\text\{', content))
content = re.sub(r'\text\{', r'\\text{', content)
print(f"Fixed {count2} instances of tab+ext to \\text")

# Fix 3: Replace "rac{" with \frac{
count3 = len(re.findall(r'rac\{', content))
content = re.sub(r'rac\{', r'\\frac{', content)
print(f"Fixed {count3} instances of rac to \\frac")

# Fix 4: Replace " pprox" with \approx (space before pprox)
count4 = len(re.findall(r' pprox', content))
content = re.sub(r' pprox', r' \\approx', content)
print(f"Fixed {count4} instances of pprox to \\approx")

# Write the fixed content
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
    f.write(content)

total_fixes = count1 + count2 + count3 + count4
print(f"\nTotal fixes: {total_fixes}")
print("Tab corruption fixed!")
