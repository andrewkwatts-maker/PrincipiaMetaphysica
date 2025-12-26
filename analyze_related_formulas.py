#!/usr/bin/env python3
"""
Analyze which formulas in config.py are missing related_formulas metadata.
"""

import sys
sys.path.insert(0, 'H:\\Github\\PrincipiaMetaphysica')

from config import CoreFormulas

def analyze_formulas():
    """Identify formulas without related_formulas."""
    all_formulas = CoreFormulas.get_all_formulas()

    formulas_with_related = []
    formulas_without_related = []

    for formula in all_formulas:
        if formula.related_formulas and len(formula.related_formulas) > 0:
            formulas_with_related.append({
                'id': formula.id,
                'name': formula.label,
                'category': formula.category,
                'section': formula.section,
                'related': formula.related_formulas,
                'derivation_parents': formula.derivation.parent_formulas if formula.derivation else []
            })
        else:
            formulas_without_related.append({
                'id': formula.id,
                'name': formula.label,
                'category': formula.category,
                'section': formula.section,
                'derivation_parents': formula.derivation.parent_formulas if formula.derivation else []
            })

    print("=" * 80)
    print("FORMULAS WITHOUT related_formulas METADATA")
    print("=" * 80)
    print(f"\nTotal: {len(formulas_without_related)} formulas missing related_formulas")
    print(f"Completion: {len(formulas_with_related)}/{len(all_formulas)} ({100*len(formulas_with_related)/len(all_formulas):.1f}%)\n")

    for i, f in enumerate(formulas_without_related, 1):
        print(f"\n{i}. ID: {f['id']}")
        print(f"   Name: {f['name']}")
        print(f"   Category: {f['category']}")
        print(f"   Section: {f['section']}")
        if f['derivation_parents']:
            print(f"   Derivation Parents: {', '.join(f['derivation_parents'])}")

    print("\n" + "=" * 80)
    print("FORMULAS WITH related_formulas (for reference)")
    print("=" * 80)
    print(f"\nTotal: {len(formulas_with_related)} formulas with related_formulas\n")

    for i, f in enumerate(formulas_with_related, 1):
        print(f"\n{i}. ID: {f['id']}")
        print(f"   Related: {', '.join(f['related'])}")

    return formulas_without_related, formulas_with_related

if __name__ == "__main__":
    formulas_without, formulas_with = analyze_formulas()
