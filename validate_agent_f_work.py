#!/usr/bin/env python3
"""
Validation script for Agent F's work
Tests all fixes and improvements
"""

import re
from pathlib import Path

def test_equation_labels():
    """Verify all equation labels are sequential (no PM values)"""
    file_path = Path('H:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html')

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for PM values in equation labels
    pattern = r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="([^"]+)"'
    matches = re.findall(pattern, content, re.DOTALL)

    if matches:
        print(f"[FAIL] Found {len(matches)} equation labels with PM values:")
        for match in matches[:10]:
            print(f"  - {match}")
        return False
    else:
        print("[PASS] All equation labels are sequential (no PM values)")
        return True

def test_cross_references():
    """Verify cross-references use static format"""
    file_path = Path('H:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html')

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for the fixed cross-references
    if '[→ Eq. (2.10)]' in content:
        print("[PASS] Planck derivation cross-reference: [-> Eq. (2.10)]")
        planck_ok = True
    else:
        print("[FAIL] Planck derivation cross-reference not found")
        planck_ok = False

    if '§3.1]' in content:
        print("[PASS] Hodge derivation cross-reference: [-> Section 3.1]")
        hodge_ok = True
    else:
        print("[FAIL] Hodge derivation cross-reference not found")
        hodge_ok = False

    return planck_ok and hodge_ok

def test_formula_database():
    """Verify formula database has all expected formulas"""
    from formula_definitions import ALL_FORMULAS, FORMULA_CATEGORIES, CALABI_YAU, G2_MANIFOLDS

    total_formulas = len(ALL_FORMULAS)
    total_categories = len(FORMULA_CATEGORIES)

    print(f"[INFO] Total formulas: {total_formulas}")
    print(f"[INFO] Total categories: {total_categories}")

    # Check new formulas
    expected_calabi_yau = {'ricci_flat', 'euler_characteristic', 'mirror_symmetry'}
    actual_calabi_yau = set(CALABI_YAU.keys())

    expected_g2 = {'g2_holonomy_conditions', 'flux_dressed_euler', 'tcs_gluing',
                   'm_gut_from_torsion', 'v9_factorization'}
    actual_g2 = set(G2_MANIFOLDS.keys())

    calabi_ok = expected_calabi_yau == actual_calabi_yau
    g2_ok = expected_g2 == actual_g2

    if calabi_ok:
        print(f"[PASS] Calabi-Yau formulas: {len(CALABI_YAU)} formulas added")
    else:
        print(f"[FAIL] Calabi-Yau formulas mismatch")
        print(f"  Expected: {expected_calabi_yau}")
        print(f"  Actual: {actual_calabi_yau}")

    if g2_ok:
        print(f"[PASS] G2 manifold formulas: {len(G2_MANIFOLDS)} formulas added")
    else:
        print(f"[FAIL] G2 manifold formulas mismatch")
        print(f"  Expected: {expected_g2}")
        print(f"  Actual: {actual_g2}")

    return calabi_ok and g2_ok

def test_validation_rules():
    """Verify validation rules are documented"""
    file_path = Path('H:/Github/PrincipiaMetaphysica/sections_content.py')

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_rules = [
        'Section Numbers: ALWAYS STATIC',
        'Equation Labels: ALWAYS SEQUENTIAL',
        'Cross-References: ALWAYS STATIC',
        'Physics Constants: ONLY USE PM VALUES',
        'Abstract Content: CENTRALIZED'
    ]

    all_found = True
    for rule in required_rules:
        if rule in content:
            print(f"[PASS] Validation rule documented: {rule}")
        else:
            print(f"[FAIL] Validation rule missing: {rule}")
            all_found = False

    return all_found

def test_abstract_centralization():
    """Verify abstract is in sections_content.py"""
    file_path = Path('H:/Github/PrincipiaMetaphysica/sections_content.py')

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '"abstract": {' in content:
        print("[PASS] Abstract section found in sections_content.py")
        return True
    else:
        print("[FAIL] Abstract section not found in sections_content.py")
        return False

def main():
    print("=" * 80)
    print("AGENT F WORK VALIDATION")
    print("=" * 80)
    print()

    results = {
        'Equation Labels': test_equation_labels(),
        'Cross-References': test_cross_references(),
        'Formula Database': test_formula_database(),
        'Validation Rules': test_validation_rules(),
        'Abstract Centralization': test_abstract_centralization()
    }

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total = len(results)
    passed = sum(results.values())

    for test_name, passed_test in results.items():
        status = "[PASS]" if passed_test else "[FAIL]"
        print(f"{status} {test_name}")

    print()
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n*** ALL TESTS PASSED ***")
        print("Agent F work is complete and validated!")
        return True
    else:
        print(f"\n!!! {total - passed} TEST(S) FAILED !!!")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
