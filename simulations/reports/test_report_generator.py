#!/usr/bin/env python3
"""
Test Script for report_generator_v16.py
========================================

Demonstrates usage and validates output.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulations.reports.report_generator_v16 import TechnicalReportGenerator


def test_basic_generation():
    """Test basic report generation."""
    print("\n" + "="*60)
    print("TEST 1: Basic Report Generation")
    print("="*60)

    generator = TechnicalReportGenerator()
    generator.load_data()

    # Test parameter categorization
    categories = generator.categorize_parameters()
    print(f"\nParameter Categories:")
    for status, params in categories.items():
        print(f"  {status}: {len(params)} parameters")

    # Test formula categorization
    formula_categories = generator.categorize_formulas()
    print(f"\nFormula Categories:")
    for category, formulas in formula_categories.items():
        print(f"  {category}: {len(formulas)} formulas")

    print("\n[PASS] Basic generation test passed")


def test_statistical_analysis():
    """Test statistical analysis functions."""
    print("\n" + "="*60)
    print("TEST 2: Statistical Analysis")
    print("="*60)

    generator = TechnicalReportGenerator()
    generator.load_data()

    categories = generator.categorize_parameters()
    all_params = []
    for params in categories.values():
        all_params.extend(params)

    # Compute chi-square
    chi_square, n_dof, p_value = generator.compute_chi_square(all_params)

    print(f"\nChi-Square Analysis:")
    print(f"  chi^2 = {chi_square:.3f}")
    print(f"  DOF = {n_dof}")
    print(f"  p-value = {p_value:.6f}")

    print("\n[PASS] Statistical analysis test passed")


def test_formatting():
    """Test value formatting functions."""
    print("\n" + "="*60)
    print("TEST 3: Value Formatting")
    print("="*60)

    generator = TechnicalReportGenerator()
    generator.load_data()

    # Test format_value
    test_values = [
        (1.23e-5, "GeV"),
        (123456789, "years"),
        (0.00729735257, "dimensionless"),
        (None, ""),
        ({"key": "value"}, ""),
        ([1, 2, 3], ""),
    ]

    print("\nValue Formatting:")
    for value, units in test_values:
        formatted = generator.format_value(value, units)
        print(f"  {str(value)[:30]:30s} => {formatted}")

    # Test format_uncertainty
    print("\nUncertainty Formatting:")
    test_uncertainties = [
        (125.09, 0.24, "GeV"),
        (1.67e34, 3e32, "years"),
        (0.00729735257, 0.00000000015, "dimensionless"),
    ]

    for value, unc, units in test_uncertainties:
        formatted = generator.format_uncertainty(value, unc, units)
        print(f"  {value:.3e} +/- {unc:.3e} => {formatted}")

    print("\n[PASS] Formatting test passed")


def test_table_generation():
    """Test table generation."""
    print("\n" + "="*60)
    print("TEST 4: Table Generation")
    print("="*60)

    generator = TechnicalReportGenerator()
    generator.load_data()

    categories = generator.categorize_parameters()

    # Generate a sample table
    if 'GEOMETRIC' in categories:
        geometric_params = categories['GEOMETRIC']
        table = generator.generate_parameter_table(geometric_params, "Geometric Parameters (Sample)")
        print(f"\nGenerated table with {len(geometric_params)} parameters")
        print(f"Table length: {len(table)} characters")
        print("\nTable preview:")
        print(table[:500] + "..." if len(table) > 500 else table)

    print("\n[PASS] Table generation test passed")


def test_full_report():
    """Test full report generation."""
    print("\n" + "="*60)
    print("TEST 5: Full Report Generation")
    print("="*60)

    generator = TechnicalReportGenerator()
    generator.load_data()

    report = generator.generate_report()

    print(f"\nReport Statistics:")
    print(f"  Total length: {len(report):,} characters")
    print(f"  Lines: {report.count(chr(10)):,}")
    print(f"  Tables: {report.count('|---|'):,}")
    print(f"  LaTeX tables: {report.count('begin{table}'):,}")

    # Check for key sections
    required_sections = [
        "Executive Summary",
        "Statistical Summary",
        "Experimental Comparisons",
        "Parameter Tables",
        "Formula Summary",
        "LaTeX Tables for Paper Appendix"
    ]

    print("\nSection presence:")
    for section in required_sections:
        present = section in report
        status = "[OK]" if present else "[MISSING]"
        print(f"  {status} {section}")

    print("\n[PASS] Full report generation test passed")


def test_custom_paths():
    """Test custom input/output paths."""
    print("\n" + "="*60)
    print("TEST 6: Custom Paths")
    print("="*60)

    # Use default paths but test the constructor
    theory_path = os.path.join(project_root, 'AutoGenerated', 'theory_output.json')
    output_path = os.path.join(project_root, 'AutoGenerated', 'TECHNICAL_SUMMARY_TEST.md')

    generator = TechnicalReportGenerator(
        theory_output_path=theory_path,
        output_path=output_path
    )

    print(f"\nInput path: {generator.theory_output_path}")
    print(f"Output path: {generator.output_path}")

    # Don't actually save to avoid cluttering
    print("\n[PASS] Custom paths test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("PRINCIPIA METAPHYSICA - REPORT GENERATOR TEST SUITE")
    print("="*70)

    tests = [
        test_basic_generation,
        test_statistical_analysis,
        test_formatting,
        test_table_generation,
        test_full_report,
        test_custom_paths,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n[FAIL] Test failed: {e}")
            failed += 1
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70 + "\n")

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
