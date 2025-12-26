#!/usr/bin/env python3
"""
Script to find all formulas in config.py missing section metadata.
"""

import sys
sys.path.insert(0, r'h:\Github\PrincipiaMetaphysica')

from config import Formulas

# Get all formulas
formulas = Formulas.get_all_formulas()

missing_sections = []
has_sections = []

for formula in formulas:
    if hasattr(formula, 'section') and formula.section:
        has_sections.append({
            'id': formula.id,
            'label': formula.label,
            'section': formula.section
        })
    else:
        missing_sections.append({
            'id': formula.id,
            'label': formula.label,
            'description': formula.description
        })

print("=" * 80)
print(f"FORMULA SECTION AUDIT")
print("=" * 80)
print(f"Total formulas: {len(formulas)}")
print(f"With section: {len(has_sections)}")
print(f"Missing section: {len(missing_sections)}")
print(f"Completion: {len(has_sections)}/{len(formulas)} ({100*len(has_sections)/len(formulas):.1f}%)")
print("=" * 80)

if missing_sections:
    print("\nFORMULAS MISSING SECTION METADATA:")
    print("-" * 80)
    for i, formula in enumerate(missing_sections, 1):
        print(f"\n{i}. {formula['label']}")
        print(f"   ID: {formula['id']}")
        print(f"   Description: {formula['description']}")

print("\n" + "=" * 80)
print(f"\nFormulas WITH section metadata (sample):")
print("-" * 80)
for formula in has_sections[:5]:
    print(f"{formula['label']} -> Section {formula['section']}")
