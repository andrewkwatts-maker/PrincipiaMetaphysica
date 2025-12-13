#!/usr/bin/env python3
"""
Validate PM Paths for Firebase Upload
======================================

Checks that all data-pm-value paths used in HTML files exist in theory_output.json

Usage:
    python validate_pm_paths.py

Returns:
    Exit code 0 if all paths found
    Exit code 1 if any paths missing
"""

import json
import re
import glob
import sys
from pathlib import Path

# HTML PM paths that must exist in theory_output.json
REQUIRED_PATHS = [
    'dark_energy.w0_PM',
    'dimensions.D_after_sp2r',
    'dimensions.D_bulk',
    'neutrino_mass.delta_m_sq',  # MISSING - needs fix
    'pmns_matrix.theta_23',
    'proton_decay.M_GUT',
    'proton_decay.alpha_GUT_inv',
    'topology.b3',
    'topology.chi_eff',
    'topology.n_gen',
    'v10_2_all_fermions.gauge_bosons_derived.Z_mass_GeV',  # MISSING - needs fix
    'v11_final_observables.higgs_mass.m_h_GeV',
    'v11_final_observables.proton_lifetime.tau_p_years',
    'v12_6_geometric_derivations.vev_pneuma.v_EW',
    'v12_final_values.kk_graviton.m1_TeV',
    'validation.exact_matches',
    'validation.predictions_within_1sigma',
    'validation.total_predictions'
]

def check_path(data, path):
    """Check if a dotted path exists in nested dict"""
    parts = path.split('.')
    current = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current

def main():
    print("=" * 80)
    print("PM PATH VALIDATION FOR FIREBASE UPLOAD")
    print("=" * 80)

    # Load theory_output.json
    try:
        with open('theory_output.json', 'r') as f:
            data = json.load(f)
        print(f"\n[OK] Loaded theory_output.json (version {data.get('meta', {}).get('version', 'unknown')})")
    except FileNotFoundError:
        print("\n[ERROR] theory_output.json not found!")
        print("  Run: python run_all_simulations.py")
        return 1
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON in theory_output.json: {e}")
        return 1

    # Check all required paths
    print(f"\nChecking {len(REQUIRED_PATHS)} required PM paths...")
    print("-" * 80)

    missing = []
    found = []

    for path in sorted(REQUIRED_PATHS):
        exists, value = check_path(data, path)
        if exists:
            found.append((path, value))
            # Truncate long values
            value_str = str(value)
            if len(value_str) > 60:
                value_str = value_str[:60] + "..."
            print(f"  [OK] {path}")
            print(f"       = {value_str}")
        else:
            missing.append(path)
            print(f"  [MISSING] {path}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Found:   {len(found)}/{len(REQUIRED_PATHS)} ({len(found)/len(REQUIRED_PATHS)*100:.1f}%)")
    print(f"Missing: {len(missing)}/{len(REQUIRED_PATHS)} ({len(missing)/len(REQUIRED_PATHS)*100:.1f}%)")

    if missing:
        print("\n" + "=" * 80)
        print("MISSING PATHS - ACTION REQUIRED")
        print("=" * 80)
        for path in missing:
            print(f"  [X] {path}")

            # Provide hints for known missing paths
            if path == 'neutrino_mass.delta_m_sq':
                print("    HINT: Data exists in v10_1_neutrino_masses.delta_m21_sq_eV2")
                print("    FIX: Add neutrino_mass section in run_all_simulations.py")
            elif path == 'v10_2_all_fermions.gauge_bosons_derived.Z_mass_GeV':
                print("    HINT: Add gauge_bosons_derived subsection")
                print("    FIX: Add to v10_2_all_fermions in run_all_simulations.py")

        print("\n" + "=" * 80)
        print("NEXT STEPS:")
        print("=" * 80)
        print("1. Review PM_VALUE_AUDIT_REPORT.md for detailed fixes")
        print("2. Apply fixes to run_all_simulations.py")
        print("3. Re-run: python run_all_simulations.py")
        print("4. Re-validate: python validate_pm_paths.py")
        print("=" * 80)

        return 1  # Exit with error code
    else:
        print("\n" + "=" * 80)
        print("[SUCCESS] ALL PM PATHS VALIDATED - READY FOR FIREBASE UPLOAD")
        print("=" * 80)
        return 0  # Success

if __name__ == '__main__':
    sys.exit(main())
