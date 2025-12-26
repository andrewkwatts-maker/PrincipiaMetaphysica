#!/usr/bin/env python3
"""Verify sections metadata updates"""

import json
import sys

def verify_sections(theory_output_path):
    """Verify sections metadata completeness"""

    with open(theory_output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sections = data.get('sections', {})

    print("=== SECTIONS METADATA VERIFICATION ===\n")

    total_sections = len(sections)
    complete_sections = 0

    for section_id, section in sections.items():
        print(f"Section {section_id}: {section.get('title', 'Unnamed')}")

        # Check required fields
        has_order = 'order' in section
        has_category = 'category' in section
        has_description = 'description' in section
        has_formulas = len(section.get('formulaRefs', [])) > 0
        has_params = len(section.get('paramRefs', [])) > 0

        print(f"  Order: {'YES' if has_order else 'NO'} - {section.get('order', 'N/A')}")
        print(f"  Category: {'YES' if has_category else 'NO'} - {section.get('category', 'N/A')}")
        print(f"  Description: {'YES' if has_description else 'NO'}")
        print(f"  Formula refs: {len(section.get('formulaRefs', []))} formulas")
        print(f"  Param refs: {len(section.get('paramRefs', []))} parameters")

        is_complete = all([has_order, has_category, has_description, has_formulas, has_params])

        if is_complete:
            complete_sections += 1
            print(f"  Status: COMPLETE")
        else:
            print(f"  Status: INCOMPLETE")

        print()

    # Summary
    completeness_pct = (complete_sections / total_sections * 100) if total_sections > 0 else 0

    print("=== SUMMARY ===")
    print(f"Total sections: {total_sections}")
    print(f"Complete sections: {complete_sections}")
    print(f"Incomplete sections: {total_sections - complete_sections}")
    print(f"Completeness: {completeness_pct:.1f}%")

    # Category breakdown
    print("\n=== CATEGORY BREAKDOWN ===")
    categories = {}
    for section in sections.values():
        cat = section.get('category', 'uncategorized')
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} sections")

    # Formula and parameter stats
    print("\n=== CROSS-REFERENCE STATS ===")
    total_formula_refs = sum(len(s.get('formulaRefs', [])) for s in sections.values())
    total_param_refs = sum(len(s.get('paramRefs', [])) for s in sections.values())
    avg_formulas = total_formula_refs / total_sections if total_sections > 0 else 0
    avg_params = total_param_refs / total_sections if total_sections > 0 else 0

    print(f"  Total formula references: {total_formula_refs}")
    print(f"  Total parameter references: {total_param_refs}")
    print(f"  Average formulas per section: {avg_formulas:.1f}")
    print(f"  Average parameters per section: {avg_params:.1f}")

    return completeness_pct == 100

if __name__ == '__main__':
    theory_output_path = r'h:\Github\PrincipiaMetaphysica\theory_output.json'
    success = verify_sections(theory_output_path)
    sys.exit(0 if success else 1)
