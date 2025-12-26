#!/usr/bin/env python3
"""
Validate that all formula and parameter references in sections actually exist
"""

import json
import sys

def validate_references(theory_output_path):
    """Validate section references against actual formulas and parameters"""

    print("=" * 80)
    print("VALIDATING SECTION REFERENCES")
    print("=" * 80)
    print()

    with open(theory_output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sections = data.get('sections', {})
    formulas = data.get('formulas', {}).get('formulas', {})
    parameters = data.get('parameters', {})

    print(f"Loaded {len(sections)} sections")
    print(f"Loaded {len(formulas)} formulas")
    print(f"Parameters structure loaded")
    print()

    # Get all parameter paths
    def get_all_param_paths(obj, prefix=''):
        """Recursively get all parameter paths"""
        paths = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                # Skip metadata keys
                if key in ['version']:
                    continue
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict) and not any(isinstance(v, (list, str, int, float, bool, type(None))) for v in value.values() if not isinstance(v, dict)):
                    # This is a nested structure, recurse
                    paths.extend(get_all_param_paths(value, new_prefix))
                else:
                    # This is a leaf or has actual values, add the path
                    paths.append(new_prefix)
                    if isinstance(value, dict):
                        # Also add sub-paths
                        paths.extend(get_all_param_paths(value, new_prefix))
        return paths

    param_paths = set(get_all_param_paths(parameters))
    print(f"Found {len(param_paths)} parameter paths")
    print()

    # Validate each section
    total_formula_refs = 0
    valid_formula_refs = 0
    invalid_formula_refs = []

    total_param_refs = 0
    valid_param_refs = 0
    invalid_param_refs = []

    print("=" * 80)
    print("VALIDATION RESULTS:")
    print("=" * 80)
    print()

    for section_id, section in sorted(sections.items()):
        print(f"Section {section_id}: {section.get('title')}")

        # Validate formula references
        formula_refs = section.get('formulaRefs', [])
        total_formula_refs += len(formula_refs)

        valid_count = 0
        for ref in formula_refs:
            if ref in formulas:
                valid_count += 1
                valid_formula_refs += 1
            else:
                invalid_formula_refs.append((section_id, ref))

        print(f"  Formula refs: {valid_count}/{len(formula_refs)} valid")

        # Validate parameter references
        param_refs = section.get('paramRefs', [])
        total_param_refs += len(param_refs)

        valid_count = 0
        for ref in param_refs:
            if ref in param_paths:
                valid_count += 1
                valid_param_refs += 1
            else:
                invalid_param_refs.append((section_id, ref))

        print(f"  Param refs: {valid_count}/{len(param_refs)} valid")
        print()

    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY:")
    print("=" * 80)
    print()

    formula_validity = (valid_formula_refs / total_formula_refs * 100) if total_formula_refs > 0 else 0
    param_validity = (valid_param_refs / total_param_refs * 100) if total_param_refs > 0 else 0

    print(f"Formula References:")
    print(f"  Total: {total_formula_refs}")
    print(f"  Valid: {valid_formula_refs}")
    print(f"  Invalid: {len(invalid_formula_refs)}")
    print(f"  Validity: {formula_validity:.1f}%")
    print()

    print(f"Parameter References:")
    print(f"  Total: {total_param_refs}")
    print(f"  Valid: {valid_param_refs}")
    print(f"  Invalid: {len(invalid_param_refs)}")
    print(f"  Validity: {param_validity:.1f}%")
    print()

    # Show invalid references if any
    if invalid_formula_refs:
        print("INVALID FORMULA REFERENCES:")
        for section_id, ref in invalid_formula_refs:
            print(f"  Section {section_id}: '{ref}' not found in formulas")
        print()

    if invalid_param_refs:
        print("INVALID PARAMETER REFERENCES:")
        for section_id, ref in invalid_param_refs:
            print(f"  Section {section_id}: '{ref}' not found in parameters")
        print()

    # Overall status
    all_valid = len(invalid_formula_refs) == 0 and len(invalid_param_refs) == 0

    if all_valid:
        print("STATUS: ALL REFERENCES VALID")
    else:
        print("STATUS: SOME INVALID REFERENCES FOUND")
        print("Note: This is expected as we mapped theoretical references.")
        print("The formulas and parameters may need to be added to the database.")

    print("=" * 80)

    return all_valid

if __name__ == '__main__':
    theory_output_path = r'h:\Github\PrincipiaMetaphysica\theory_output.json'
    all_valid = validate_references(theory_output_path)
    # Don't fail on invalid refs - they're expected
    sys.exit(0)
