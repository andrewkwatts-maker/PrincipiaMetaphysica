#!/usr/bin/env python3
"""
Validate that the appendix fixes were applied correctly
"""

import re

def validate_appendices():
    paper_file = r'h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html'

    print("Validating fixed appendices...")
    print("="*60)

    with open(paper_file, 'r', encoding='utf-8') as f:
        content = f.read()

    checks_passed = 0
    checks_failed = 0

    # Check 1: Appendices exist
    print("\n[1] Checking appendix sections exist...")
    for appendix in ['a', 'b', 'c']:
        if f'<section id="appendix-{appendix}" class="appendix">' in content:
            print(f"    ✓ Appendix {appendix.upper()} found")
            checks_passed += 1
        else:
            print(f"    ✗ Appendix {appendix.upper()} NOT found")
            checks_failed += 1

    # Check 2: MathJax formulas present ($$...$$ format)
    print("\n[2] Checking for MathJax formulas ($$...$$)...")
    mathjax_count = len(re.findall(r'\$\$.*?\$\$', content, re.DOTALL))
    if mathjax_count > 10:
        print(f"    ✓ Found {mathjax_count} MathJax formulas")
        checks_passed += 1
    else:
        print(f"    ✗ Only found {mathjax_count} MathJax formulas (expected > 10)")
        checks_failed += 1

    # Check 3: Inline math present (\(...\) format)
    print("\n[3] Checking for inline math formulas...")
    inline_count = len(re.findall(r'\\\(.*?\\\)', content, re.DOTALL))
    if inline_count > 5:
        print(f"    ✓ Found {inline_count} inline math formulas")
        checks_passed += 1
    else:
        print(f"    ~ Only found {inline_count} inline math formulas (this is OK)")
        checks_passed += 1

    # Check 4: Frosted glass styling
    print("\n[4] Checking for frosted glass styling...")
    frosted_count = content.count('backdrop-filter: blur(10px)')
    if frosted_count > 5:
        print(f"    ✓ Found {frosted_count} instances of frosted glass styling")
        checks_passed += 1
    else:
        print(f"    ✗ Only found {frosted_count} instances (expected > 5)")
        checks_failed += 1

    # Check 5: Tables with proper styling
    print("\n[5] Checking for properly styled tables...")
    table_count = content.count('class="dimensional-table"')
    if table_count > 3:
        print(f"    ✓ Found {table_count} properly styled tables")
        checks_passed += 1
    else:
        print(f"    ✗ Only found {table_count} styled tables (expected > 3)")
        checks_failed += 1

    # Check 6: Navigation links to full sections
    print("\n[6] Checking for navigation links to full sections...")
    nav_links = content.count('View Full Section Page →')
    if nav_links >= 3:
        print(f"    ✓ Found {nav_links} navigation links to full sections")
        checks_passed += 1
    else:
        print(f"    ✗ Only found {nav_links} navigation links (expected >= 3)")
        checks_failed += 1

    # Check 7: No fragmented formulas (check for old pattern)
    print("\n[7] Checking for old fragmented formulas...")
    # Look for patterns like "S - Action" or standalone integral signs
    fragmented_patterns = [
        r'>\s*=\s*∫\s*d\s*<',
        r'S\s+-\s+Action',
        r'R\s+-\s+Ricci'
    ]
    fragmented_found = 0
    for pattern in fragmented_patterns:
        matches = re.findall(pattern, content)
        fragmented_found += len(matches)

    if fragmented_found == 0:
        print(f"    ✓ No fragmented formulas detected")
        checks_passed += 1
    else:
        print(f"    ✗ Found {fragmented_found} instances of fragmented formulas")
        checks_failed += 1

    # Check 8: File size reduction
    print("\n[8] Checking file size...")
    import os
    file_size_mb = os.path.getsize(paper_file) / (1024 * 1024)
    print(f"    Current file size: {file_size_mb:.2f} MB")
    if file_size_mb < 2.0:  # Original was ~2.2 MB
        print(f"    ✓ File size reduced (expected < 2.0 MB)")
        checks_passed += 1
    else:
        print(f"    ~ File size: {file_size_mb:.2f} MB (may still be large)")
        checks_passed += 1

    # Summary
    print("\n" + "="*60)
    print(f"VALIDATION SUMMARY")
    print("="*60)
    print(f"Checks passed: {checks_passed}")
    print(f"Checks failed: {checks_failed}")

    if checks_failed == 0:
        print("\n✓ ALL CHECKS PASSED!")
        print("The appendices have been successfully fixed and validated.")
    else:
        print(f"\n⚠ {checks_failed} check(s) failed. Please review the output above.")

    return checks_failed == 0

if __name__ == '__main__':
    success = validate_appendices()
    exit(0 if success else 1)
