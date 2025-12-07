import os
import re
from pathlib import Path

# Pattern to match numerical uncertainties like "5.0 ± 1.5" or "5.0 +/- 1.5"
uncertainty_pattern = re.compile(
    r'\d+\.?\d*\s*[±+]/?[-−]\s*\d+\.?\d*'
)

foundations_dir = Path(r'H:\Github\PrincipiaMetaphysica\foundations')

print("Scanning foundations directory for numerical uncertainties...\n")

files_with_uncertainties = []
total_matches = 0

for html_file in foundations_dir.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    matches = []
    for i, line in enumerate(lines, 1):
        if uncertainty_pattern.search(line):
            matches.append((i, line.strip()))

    if matches:
        files_with_uncertainties.append(html_file.name)
        total_matches += len(matches)
        print(f"\n{html_file.name}:")
        print(f"  Found {len(matches)} numerical uncertainty pattern(s)")
        for line_num, line_content in matches:
            # Show a snippet of the line
            snippet = line_content[:120] + '...' if len(line_content) > 120 else line_content
            print(f"    Line {line_num}: {snippet}")

print(f"\n{'='*70}")
print(f"SUMMARY:")
print(f"  Files with numerical uncertainties: {len(files_with_uncertainties)}")
print(f"  Total matches: {total_matches}")
if files_with_uncertainties:
    print(f"  Files: {', '.join(files_with_uncertainties)}")
else:
    print("  No numerical uncertainty patterns found in foundations directory!")
print(f"{'='*70}")
