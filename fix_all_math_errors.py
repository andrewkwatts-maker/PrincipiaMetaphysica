#!/usr/bin/env python3
"""Fix all Math input errors throughout the paper."""

import re

# Read the file
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing Math input errors...")

# Fix 1: Replace \t\t\text{ with \text{ (double tab before \text)
count1 = len(re.findall(r'\\t\\t\\text\{', content))
content = re.sub(r'\\t\\t\\text\{', r'\\text{', content)
print(f"Fixed {count1} instances of \\t\\t\\text{{")

# Fix 2: Replace \t\t\times with \times (double tab before \times)
count2 = len(re.findall(r'\\t\\t\\times', content))
content = re.sub(r'\\t\\t\\times', r'\\times', content)
print(f"Fixed {count2} instances of \\t\\t\\times")

# Fix 3: Replace \f\f\frac with \frac (double f before \frac)
count3 = len(re.findall(r'\\f\\f\\frac', content))
content = re.sub(r'\\f\\f\\frac', r'\\frac', content)
print(f"Fixed {count3} instances of \\f\\f\\frac")

# Fix 4: Replace pprox with \approx (missing backslash)
count4 = len(re.findall(r'([^\\])approx', content))
content = re.sub(r'([^\\])approx', r'\1\\approx', content)
print(f"Fixed {count4} instances of missing backslash before approx")

# Fix 5: Replace constra\int with constraint (broken word)
count5 = len(re.findall(r'constra\\int', content))
content = re.sub(r'constra\\int', r'constraint', content)
print(f"Fixed {count5} instances of constra\\int")

# Fix 6: Replace <\strong> with </strong> (broken closing tag)
count6 = len(re.findall(r'<\\strong>', content))
content = re.sub(r'<\\strong>', r'</strong>', content)
print(f"Fixed {count6} instances of <\\strong>")

# Fix 7: Replace <\sub> with </sub> (broken closing tag)
count7 = len(re.findall(r'<\\sub>', content))
content = re.sub(r'<\\sub>', r'</sub>', content)
print(f"Fixed {count7} instances of <\\sub>")

# Write the fixed content
with open(r'h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
    f.write(content)

total_fixes = count1 + count2 + count3 + count4 + count5 + count6 + count7
print(f"\nTotal fixes: {total_fixes}")
print("All Math input errors fixed!")
