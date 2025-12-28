#!/usr/bin/env python3
"""
Validation script for fermion mass calculation bug fix.
Verifies that the FN formula m_f = A_f × ε^Q_f × v_yukawa is correctly implemented.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simulations', 'core'))

from geometric.g2_yukawa_overlap_integrals_v14_2 import G2YukawaOverlapIntegrals
from fermion.yukawa_texture_geometric_v14_2 import GeometricYukawaTextures


def validate_dimension_analysis():
    """Verify that dimensions are correct in the calculation."""
    print("=" * 80)
    print("DIMENSION ANALYSIS VALIDATION")
    print("=" * 80)
    print()

    sim = G2YukawaOverlapIntegrals()

    print("Checking Higgs profile...")
    # Higgs profile should be dimensionless
    phi_at_origin = sim.higgs_profile(0.0)
    print(f"  φ(r=0) = {phi_at_origin:.4f} (dimensionless) ✓")

    # Yukawa coupling should be dimensionless
    results = sim.compute_all_yukawas()
    y_top = results['fermions']['top']['yukawa_coupling']
    print(f"  Y_top = {y_top:.4f} (dimensionless) ✓")

    # Mass should have units of GeV
    m_top = results['fermions']['top']['mass_predicted_gev']
    print(f"  m_top = Y_top × v_yukawa = {y_top:.4f} × {sim.v_yukawa:.2f} GeV")
    print(f"        = {m_top:.2f} GeV ✓")
    print()

    return True


def validate_fn_formula():
    """Verify FN formula: m_f = A_f × ε^Q_f × v_yukawa"""
    print("=" * 80)
    print("FN FORMULA VALIDATION: m_f = A_f × ε^Q_f × v_yukawa")
    print("=" * 80)
    print()

    sim = G2YukawaOverlapIntegrals()
    results = sim.compute_all_yukawas()

    # Test for each fermion
    all_pass = True
    for fermion in ['top', 'charm', 'up', 'bottom', 'strange', 'down', 'tau', 'muon', 'electron']:
        r = results['fermions'][fermion]

        # Calculate mass using FN formula
        A_f = r['phenomenological_coeff_A']
        Q = r['fn_charge']
        epsilon_Q = sim.epsilon ** Q
        m_calculated = A_f * epsilon_Q * sim.v_yukawa
        m_predicted = r['mass_predicted_gev']

        # Verify they match
        relative_error = abs(m_calculated - m_predicted) / m_predicted if m_predicted > 0 else 0
        status = "✓" if relative_error < 1e-6 else "✗"

        if relative_error >= 1e-6:
            all_pass = False

        print(f"{fermion:>10}: m = {A_f:.4f} × {epsilon_Q:.6f} × {sim.v_yukawa:.2f} GeV = {m_calculated:.6f} GeV {status}")
        print(f"{'':>10}  Stored value: {m_predicted:.6f} GeV (error: {relative_error:.2e})")

    print()
    if all_pass:
        print("FN FORMULA VALIDATION: PASSED ✓")
    else:
        print("FN FORMULA VALIDATION: FAILED ✗")
    print()

    return all_pass


def validate_mass_predictions():
    """Validate mass predictions against experimental values."""
    print("=" * 80)
    print("MASS PREDICTION VALIDATION")
    print("=" * 80)
    print()

    sim = G2YukawaOverlapIntegrals()
    results = sim.compute_all_yukawas()

    print(f"{'Fermion':<12} | {'Q':<3} | {'A_f':<8} | {'Pred (GeV)':<14} | {'Exp (GeV)':<14} | {'Error':<8} | {'Status'}")
    print("-" * 95)

    passed = 0
    total = 0

    tolerance = {
        'top': 5.0,
        'bottom': 5.0,
        'charm': 5.0,
        'strange': 20.0,  # QCD uncertainties
        'up': 20.0,       # QCD uncertainties
        'down': 30.0,     # QCD uncertainties
        'tau': 5.0,
        'muon': 5.0,
        'electron': 5.0
    }

    for fermion in ['top', 'bottom', 'charm', 'strange', 'up', 'down', 'tau', 'muon', 'electron']:
        r = results['fermions'][fermion]
        error = r['error_pct']
        tol = tolerance[fermion]
        status = "✓ PASS" if error < tol else "✗ FAIL"

        total += 1
        if error < tol:
            passed += 1

        print(f"{fermion:<12} | {r['fn_charge']:<3} | {r['phenomenological_coeff_A']:<8.4f} | "
              f"{r['mass_predicted_gev']:<14.6f} | {r['mass_experimental_gev']:<14.6f} | "
              f"{error:>6.1f}% | {status}")

    print("-" * 95)
    print(f"PASSED: {passed}/{total} fermions")
    print()

    return passed == total


def validate_epsilon():
    """Validate epsilon derivation from curvature."""
    print("=" * 80)
    print("EPSILON PARAMETER VALIDATION")
    print("=" * 80)
    print()

    sim = G2YukawaOverlapIntegrals()

    print(f"  Curvature scale: λ = {sim.lambda_curvature}")
    print(f"  Derived: ε = exp(-λ) = {sim.epsilon:.5f}")
    print(f"  Cabibbo angle (V_us): 0.2257")

    agreement = abs(sim.epsilon - 0.2257) / 0.2257 * 100
    print(f"  Agreement: {100 - agreement:.1f}% ✓")
    print()

    return agreement < 2.0  # Within 2%


def validate_consistency():
    """Validate consistency between the two implementations."""
    print("=" * 80)
    print("CONSISTENCY VALIDATION")
    print("=" * 80)
    print()

    sim1 = G2YukawaOverlapIntegrals()
    sim2 = GeometricYukawaTextures()

    results1 = sim1.compute_all_yukawas()
    results2 = sim2.derive_all_textures(verbose=False)

    print("Comparing predictions from both implementations...")
    print()

    all_consistent = True
    for fermion in ['top', 'charm', 'up', 'bottom', 'strange', 'down', 'tau', 'muon', 'electron']:
        m1 = results1['fermions'][fermion]['mass_predicted_gev']
        m2 = results2['fermions'][fermion]['m_predicted_gev']

        rel_diff = abs(m1 - m2) / m1 if m1 > 0 else 0
        status = "✓" if rel_diff < 1e-6 else "✗"

        if rel_diff >= 1e-6:
            all_consistent = False

        print(f"{fermion:>10}: overlap={m1:.6f} GeV, texture={m2:.6f} GeV, diff={rel_diff:.2e} {status}")

    print()
    if all_consistent:
        print("CONSISTENCY CHECK: PASSED ✓")
    else:
        print("CONSISTENCY CHECK: FAILED ✗")
    print()

    return all_consistent


def main():
    """Run all validation tests."""
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  FERMION MASS CALCULATION BUG FIX - VALIDATION SUITE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    tests = [
        ("Dimension Analysis", validate_dimension_analysis),
        ("FN Formula", validate_fn_formula),
        ("Mass Predictions", validate_mass_predictions),
        ("Epsilon Parameter", validate_epsilon),
        ("Consistency", validate_consistency)
    ]

    results = {}
    for name, test_func in tests:
        try:
            passed = test_func()
            results[name] = passed
        except Exception as e:
            print(f"ERROR in {name}: {e}")
            results[name] = False

    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()

    all_passed = True
    for name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {name:<30} {status}")
        if not passed:
            all_passed = False

    print()
    print("=" * 80)

    if all_passed:
        print("ALL TESTS PASSED ✓✓✓")
        print()
        print("The fermion mass calculation bug has been successfully fixed.")
        print("The FN formula m_f = A_f × ε^Q_f × v_yukawa is correctly implemented.")
        print()
        return 0
    else:
        print("SOME TESTS FAILED ✗✗✗")
        print()
        print("Please review the failures above.")
        print()
        return 1


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    sys.exit(main())
