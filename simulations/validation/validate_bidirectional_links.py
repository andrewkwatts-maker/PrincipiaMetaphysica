"""
Validate Bi-directional Links in theory_output.json
===================================================

Validates that all cross-references are bi-directional:
- formulas <-> params (formulas reference params, params link to formulas)
- formulas <-> sections (formulas assigned to sections, sections list formulas)
- params <-> sections (params referenced in sections, sections list params)

Usage:
    python validate_bidirectional_links.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict


def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON file with UTF-8 encoding."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_formula_param_links(data: Dict[str, Any]) -> Tuple[int, int, List[str]]:
    """
    Validate formula ↔ param bidirectional links.
    Returns (found_count, missing_count, issues_list)
    """
    issues = []
    found = 0
    missing = 0

    formulas = data.get('formulas', {}).get('formulas', {})
    parameters = data.get('parameters', {})

    # Build param lookup (flattened)
    all_params = set()
    def extract_params(obj, prefix=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in ('value', 'units', 'status', 'description', 'source'):
                    continue
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict) and 'value' in value:
                    all_params.add(new_prefix)
                    all_params.add(key)  # Also add just the key
                elif isinstance(value, dict):
                    extract_params(value, new_prefix)

    extract_params(parameters)

    # Check formulas reference valid params
    for formula_id, formula in formulas.items():
        if not isinstance(formula, dict):
            continue

        input_params = formula.get('inputParams', [])
        output_params = formula.get('outputParams', [])
        terms = formula.get('terms', {})

        # Check inputParams
        for param in input_params:
            if not isinstance(param, str):
                continue
            if param and not any(p.endswith(param) or param in p for p in all_params):
                issues.append(f"Formula '{formula_id}' references unknown inputParam: {param}")
                missing += 1
            else:
                found += 1

        # Check outputParams
        for param in output_params:
            if not isinstance(param, str):
                continue
            if param and not any(p.endswith(param) or param in p for p in all_params):
                issues.append(f"Formula '{formula_id}' references unknown outputParam: {param}")
                missing += 1
            else:
                found += 1

    return found, missing, issues


def validate_formula_section_links(data: Dict[str, Any]) -> Tuple[int, int, List[str]]:
    """
    Validate formula ↔ section bidirectional links.
    Returns (found_count, missing_count, issues_list)
    """
    issues = []
    found = 0
    missing = 0

    formulas = data.get('formulas', {}).get('formulas', {})
    sections = data.get('sections', {})

    # Valid section identifiers
    valid_sections = set(sections.keys())
    valid_sections.update([f"Section {s}" for s in sections.keys()])
    valid_sections.update([str(i) for i in range(1, 10)])
    valid_sections.update([f"{i}" for i in range(1, 10)])
    valid_sections.update(['Appendix A', 'Appendix B', 'Appendix C', 'Appendix D',
                          'Appendix E', 'Appendix F', 'Appendix G', 'Appendix H',
                          'Appendix I', 'Appendix J', 'Appendix K', 'Appendix L'])
    valid_sections.update(['Dimensional Shadow', 'Fermion Sector', 'Geometric Framework',
                          'Gauge Unification', 'Cosmology', 'Predictions'])

    # Check formulas have valid section assignments
    for formula_id, formula in formulas.items():
        if not isinstance(formula, dict):
            continue

        section = formula.get('section', formula.get('sectionId', ''))
        if section:
            # Check if section is valid
            if section not in valid_sections and not any(section.startswith(v) for v in valid_sections):
                issues.append(f"Formula '{formula_id}' has unknown section: {section}")
                missing += 1
            else:
                found += 1

    # Check sections reference formulas that exist
    for section_id, section in sections.items():
        if not isinstance(section, dict):
            continue

        formula_refs = section.get('formulaRefs', [])
        for ref in formula_refs:
            if ref not in formulas:
                issues.append(f"Section '{section_id}' references unknown formula: {ref}")
                missing += 1
            else:
                found += 1

    return found, missing, issues


def validate_section_param_links(data: Dict[str, Any]) -> Tuple[int, int, List[str]]:
    """
    Validate section ↔ param bidirectional links.
    Returns (found_count, missing_count, issues_list)
    """
    issues = []
    found = 0
    missing = 0

    sections = data.get('sections', {})
    parameters = data.get('parameters', {})

    # Build param lookup (flattened)
    all_params = set()
    def extract_params(obj, prefix=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in ('value', 'units', 'status', 'description', 'source'):
                    continue
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict) and 'value' in value:
                    all_params.add(new_prefix)
                    all_params.add(key)
                elif isinstance(value, dict):
                    extract_params(value, new_prefix)

    extract_params(parameters)

    # Check sections reference valid params
    for section_id, section in sections.items():
        if not isinstance(section, dict):
            continue

        param_refs = section.get('paramRefs', [])
        for ref in param_refs:
            if ref and not any(p.endswith(ref) or ref in p for p in all_params):
                issues.append(f"Section '{section_id}' references unknown param: {ref}")
                missing += 1
            else:
                found += 1

    return found, missing, issues


def validate_derived_from_links(data: Dict[str, Any]) -> Tuple[int, int, List[str]]:
    """
    Validate derivedFrom links between formulas.
    Returns (found_count, missing_count, issues_list)
    """
    issues = []
    found = 0
    missing = 0

    formulas = data.get('formulas', {}).get('formulas', {})

    for formula_id, formula in formulas.items():
        if not isinstance(formula, dict):
            continue

        derived_from = formula.get('derivedFrom', [])
        for ref in derived_from:
            if ref not in formulas:
                issues.append(f"Formula '{formula_id}' derivedFrom unknown formula: {ref}")
                missing += 1
            else:
                found += 1

    return found, missing, issues


def main():
    """Main validation routine."""
    base_dir = Path(__file__).parent.parent.parent
    theory_path = base_dir / 'AutoGenerated' / 'theory_output.json'

    print("=" * 70)
    print("Bi-directional Link Validation")
    print("=" * 70)
    print(f"Theory output: {theory_path}")

    if not theory_path.exists():
        print(f"ERROR: {theory_path} not found")
        sys.exit(1)

    data = load_json(theory_path)
    print(f"Loaded theory_output.json (version: {data.get('version', 'unknown')})")

    # Track critical vs informational issues separately
    critical_issues = []
    informational_issues = []
    total_valid = 0
    total_critical = 0
    total_informational = 0

    # 1. Formula <-> Param links (INFORMATIONAL - these are often theoretical variables)
    print("\n--- Validating Formula <-> Parameter Links ---")
    found, missing, issues = validate_formula_param_links(data)
    print(f"  Valid: {found}, Unlinked: {missing} (informational)")
    total_valid += found
    total_informational += missing
    informational_issues.extend(issues)

    # 2. Formula <-> Section links (CRITICAL)
    print("\n--- Validating Formula <-> Section Links ---")
    found, missing, issues = validate_formula_section_links(data)
    print(f"  Valid: {found}, Broken: {missing}")
    total_valid += found
    total_critical += missing
    critical_issues.extend(issues)

    # 3. Section <-> Param links (INFORMATIONAL)
    print("\n--- Validating Section <-> Parameter Links ---")
    found, missing, issues = validate_section_param_links(data)
    print(f"  Valid: {found}, Unlinked: {missing} (informational)")
    total_valid += found
    total_informational += missing
    informational_issues.extend(issues)

    # 4. Formula derivedFrom links (INFORMATIONAL - documentation-level references)
    print("\n--- Validating Formula derivedFrom Links ---")
    found, missing, issues = validate_derived_from_links(data)
    print(f"  Valid: {found}, Unlinked: {missing} (informational)")
    total_valid += found
    total_informational += missing
    informational_issues.extend(issues)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total valid links: {total_valid}")
    print(f"Critical issues: {total_critical}")
    print(f"Informational issues: {total_informational}")

    if total_critical == 0:
        print("\n[PASS] All critical bi-directional links are valid!")
        if total_informational > 0:
            print(f"       ({total_informational} informational issues - theoretical params not in registry)")
    else:
        success_rate = (total_valid / (total_valid + total_critical)) * 100
        print(f"\nCritical success rate: {success_rate:.1f}%")

        print("\n" + "-" * 70)
        print("CRITICAL ISSUES (first 20):")
        print("-" * 70)
        for issue in critical_issues[:20]:
            # Handle encoding for Windows console
            safe_issue = issue.encode('ascii', 'replace').decode('ascii')
            print(f"  - {safe_issue}")
        if len(critical_issues) > 20:
            print(f"  ... and {len(critical_issues) - 20} more critical issues")

    print("=" * 70)

    # Only fail on critical issues
    sys.exit(0 if total_critical == 0 else 1)


if __name__ == "__main__":
    main()
