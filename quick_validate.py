"""
quick_validate.py - Quick Validation Script for Principia Metaphysica
Principia Metaphysica v6.1+

A simple, fast validation script to check core theoretical consistency.
Run this before commits to ensure no breaking changes.

Usage:
    python quick_validate.py

Returns exit code 0 if all tests pass, 1 if any fail.
"""

import sys
from config import (
    FundamentalConstants as FC,
    PhenomenologyParameters as PP,
    ModuliParameters as MP,
    validate_all
)

def test_basic_constraints():
    """Test fundamental theoretical constraints."""
    print("=" * 70)
    print("QUICK VALIDATION - Principia Metaphysica v6.1+")
    print("=" * 70)
    print()

    tests_passed = 0
    tests_failed = 0

    # Test 1: Dimensional consistency
    print("[1/5] Dimensional Consistency Check")
    total_dims = FC.N_BRANES * FC.SPATIAL_DIMS + FC.TIME_DIMS
    if total_dims == FC.D_INTERNAL:
        print(f"  PASS: {FC.N_BRANES} branes × {FC.SPATIAL_DIMS} spatial + {FC.TIME_DIMS} time = {total_dims}")
        tests_passed += 1
    else:
        print(f"  FAIL: Expected {FC.D_INTERNAL}, got {total_dims}")
        tests_failed += 1
    print()

    # Test 2: Generation count
    print("[2/5] Generation Count")
    generations = FC.fermion_generations()
    if generations == 3:
        print(f"  PASS: Generations = {generations} (matches Standard Model)")
        tests_passed += 1
    else:
        print(f"  FAIL: Expected 3 generations, got {generations}")
        tests_failed += 1
    print()

    # Test 3: Swampland constraint
    print("[3/5] Swampland Constraint")
    a = MP.a_swampland()
    bound = MP.SWAMPLAND_BOUND
    if a > bound:
        print(f"  PASS: a = {a:.6f} > {bound:.6f} (de Sitter compatible)")
        tests_passed += 1
    else:
        print(f"  FAIL: a = {a:.6f} <= {bound:.6f} (swampland violation)")
        tests_failed += 1
    print()

    # Test 4: Dark energy bounds
    print("[4/5] Dark Energy Equation of State")
    w0 = -PP.w0_value()  # w0_value() returns positive -11/13, need to negate
    if -1.2 < w0 < -0.5:
        print(f"  PASS: w_0 = {w0:.6f} (within observational bounds)")
        tests_passed += 1
    else:
        print(f"  FAIL: w_0 = {w0:.6f} (outside bounds [-1.2, -0.5])")
        tests_failed += 1
    print()

    # Test 5: Pneuma dimension reduction
    print("[5/5] Pneuma Dimension Reduction")
    full_dim = FC.pneuma_dimension_full()
    reduced_dim = FC.pneuma_dimension_reduced()
    expected_ratio = 2**(FC.GAUGING_DOFS / 2) * FC.MIRRORING_FACTOR
    actual_ratio = full_dim / reduced_dim
    if abs(actual_ratio - expected_ratio) < 0.01:
        print(f"  PASS: {full_dim} / {reduced_dim} = {actual_ratio:.0f} (expected {expected_ratio:.0f})")
        tests_passed += 1
    else:
        print(f"  FAIL: Ratio mismatch")
        tests_failed += 1
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {tests_passed}/5")
    print(f"Tests failed: {tests_failed}/5")
    print()

    if tests_failed == 0:
        print("SUCCESS: All quick validation tests passed!")
        print()
        return 0
    else:
        print("FAILURE: Some tests failed. Review theoretical consistency.")
        print()
        return 1

def main():
    """Main entry point."""
    try:
        exit_code = test_basic_constraints()

        # Run full validation from config.py
        print("Running comprehensive validation from config.py...")
        all_passed, results = validate_all()

        if all_passed:
            print("Comprehensive validation: PASSED")
        else:
            print("Comprehensive validation: Some checks failed")
            print("Details:", results)
            exit_code = 1

        sys.exit(exit_code)

    except Exception as e:
        print(f"ERROR: Validation script encountered an exception:")
        print(f"  {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
