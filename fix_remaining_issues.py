#!/usr/bin/env python3
"""Fix remaining LaTeX issues in section 6.2a."""

import re

# Read the file
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing remaining LaTeX issues...")

# Fix 1: \timesv → \times v
count1 = content.count(r'\timesv')
content = content.replace(r'\timesv', r'\times v')
print(f"Fixed {count1} instances of \\timesv")

# Fix 2: pprox → \approx (anywhere in the doc)
count2 = len(re.findall(r'([^\\\w])pprox', content))
content = re.sub(r'([^\\\w])pprox', r'\1\\approx', content)
print(f"Fixed {count2} instances of pprox")

# Fix 3: \times followed immediately by a digit (add space)
count3 = len(re.findall(r'\\times(\d)', content))
content = re.sub(r'\\times(\d)', r'\\times \1', content)
print(f"Fixed {count3} instances of \\timesNUMBER")

# Fix 4: Add space between \times and \frac if missing
count4 = content.count(r'\times\frac')
content = content.replace(r'\times\frac', r'\times \frac')
print(f"Fixed {count4} instances of \\times\\frac")

# Write the fixed content
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
    f.write(content)

total_fixes = count1 + count2 + count3 + count4
print(f"\nTotal fixes: {total_fixes}")
print("All remaining issues fixed!")
