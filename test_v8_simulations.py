#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

Test runner for v8.0 simulations - Validates all new modules
"""

import sys
import os

# Suppress Unicode errors in console output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simulations'))
sys.path.insert(0, os.path.dirname(__file__))

import json

def test_kk_spectrum():
    """Test KK spectrum calculation"""
    print("\n" + "=" * 70)
    print("TESTING: KK Spectrum Full Calculation")
    print("=" * 70)

    from kk_spectrum_full import run_kk_spectrum
    results = run_kk_spectrum()

    print(f"\nRESULTS:")
    print(f"  m1 = {results['m1']/1e3:.2f} TeV")
    print(f"  m2 = {results['m2']/1e3:.2f} TeV")
    print(f"  m3 = {results['m3']/1e3:.2f} TeV")
    print(f"  sigma(m1) = {results['sigma_m1_fb']:.3f} fb")
    print(f"  Discovery potential: {results['discovery_significance_sigma']:.1f} sigma")
    print(f"  BR(gg) = {results['branching_ratios']['gg']*100:.1f}%")

    return results

def test_mass_ordering():
    """Test neutrino mass ordering calculation"""
    print("\n" + "=" * 70)
    print("TESTING: Neutrino Mass Ordering")
    print("=" * 70)

    from neutrino_mass_ordering import run_mass_ordering
    results = run_mass_ordering()

    print(f"\nRESULTS:")
    print(f"  Predicted: {results['ordering_predicted']}")
    print(f"  P(IH) = {results['prob_IH_mean']*100:.1f}% +/- {results['prob_IH_std']*100:.1f}%")
    print(f"  Confidence: {results['confidence_level']*100:.1f}%")

    return results

def test_proton_channels():
    """Test proton decay branching ratios"""
    print("\n" + "=" * 70)
    print("TESTING: Proton Decay Channels")
    print("=" * 70)

    from proton_decay_channels import run_proton_channels
    results = run_proton_channels()

    print(f"\nRESULTS:")
    print(f"  BR(e+pi0) = {results['BR_epi0_mean']*100:.1f}% +/- {results['BR_epi0_std']*100:.1f}%")
    print(f"  BR(K+nu) = {results['BR_Knu_mean']*100:.1f}% +/- {results['BR_Knu_std']*100:.1f}%")
    print(f"  All channels consistent: {results['all_consistent']}")

    return results

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("PRINCIPIA METAPHYSICA v8.0 - SIMULATION VALIDATION")
    print("=" * 70)

    results_all = {}

    try:
        results_all['kk_spectrum'] = test_kk_spectrum()
    except Exception as e:
        print(f"\nERROR in KK spectrum: {e}")
        import traceback
        traceback.print_exc()

    try:
        results_all['mass_ordering'] = test_mass_ordering()
    except Exception as e:
        print(f"\nERROR in mass ordering: {e}")
        import traceback
        traceback.print_exc()

    try:
        results_all['proton_channels'] = test_proton_channels()
    except Exception as e:
        print(f"\nERROR in proton channels: {e}")
        import traceback
        traceback.print_exc()

    # Save results
    with open('v8_test_results.json', 'w') as f:
        # Convert numpy arrays to lists for JSON
        def convert(obj):
            if hasattr(obj, 'tolist'):
                return obj.tolist()
            return obj

        json.dump(results_all, f, indent=2, default=convert)

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE - Results saved to v8_test_results.json")
    print("=" * 70)

if __name__ == "__main__":
    main()
