#!/usr/bin/env python3
"""
Validation script for fermion mass calculations in full_fermion_matrices_v10_2.py

This script verifies that:
1. All quark masses are non-zero and match PDG values
2. All lepton masses are non-zero and match PDG values (no NaN)
3. Errors are within acceptable thresholds
"""

import sys
import numpy as np
from simulations.full_fermion_matrices_v10_2 import derive_all_fermion_matrices

# PDG 2025 reference values (in GeV)
PDG_VALUES = {
    'quarks_up': {'u': 2.2e-3, 'c': 1.27, 't': 172.7},
    'quarks_down': {'d': 4.7e-3, 's': 95e-3, 'b': 4.18},
    'leptons': {'e': 0.511e-3, 'mu': 105.66e-3, 'tau': 1.777}
}

# Error thresholds
QUARK_ERROR_THRESHOLD = 2.0  # 2% for quarks
LEPTON_ERROR_THRESHOLD = 0.5  # 0.5% for leptons

def validate_masses():
    """Run validation checks on fermion masses"""
    print("="*70)
    print("FERMION MASS VALIDATION")
    print("="*70)
    print()

    # Run the simulation
    result = derive_all_fermion_matrices()

    mu = result['mu']
    md = result['md']
    me = result['me']

    # Check for zeros or NaNs
    print("1. Checking for zeros and NaNs...")
    all_masses = np.concatenate([mu, md, me])
    if np.any(all_masses == 0):
        print("   FAIL: Some masses are zero!")
        print(f"   Quark masses (up): {mu}")
        print(f"   Quark masses (down): {md}")
        print(f"   Lepton masses: {me}")
        return False

    if np.any(np.isnan(all_masses)):
        print("   FAIL: Some masses are NaN!")
        print(f"   Quark masses (up): {mu}")
        print(f"   Quark masses (down): {md}")
        print(f"   Lepton masses: {me}")
        return False

    print("   PASS: All masses are non-zero and non-NaN")
    print()

    # Check up-type quarks
    print("2. Validating up-type quark masses...")
    quark_names = ['u', 'c', 't']
    pdg_up = np.array([PDG_VALUES['quarks_up'][q] for q in quark_names])
    errors_up = np.abs((mu - pdg_up) / pdg_up * 100)

    all_pass = True
    for i, name in enumerate(quark_names):
        status = "PASS" if errors_up[i] < QUARK_ERROR_THRESHOLD else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"   {name}: {mu[i]*1e3:.2f} MeV (PDG: {pdg_up[i]*1e3:.2f} MeV) - Error: {errors_up[i]:.2f}% [{status}]")

    if not all_pass:
        return False
    print()

    # Check down-type quarks
    print("3. Validating down-type quark masses...")
    quark_names = ['d', 's', 'b']
    pdg_down = np.array([PDG_VALUES['quarks_down'][q] for q in quark_names])
    errors_down = np.abs((md - pdg_down) / pdg_down * 100)

    all_pass = True
    for i, name in enumerate(quark_names):
        status = "PASS" if errors_down[i] < QUARK_ERROR_THRESHOLD else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"   {name}: {md[i]*1e3:.2f} MeV (PDG: {pdg_down[i]*1e3:.2f} MeV) - Error: {errors_down[i]:.2f}% [{status}]")

    if not all_pass:
        return False
    print()

    # Check leptons
    print("4. Validating charged lepton masses...")
    lepton_names = ['e', 'mu', 'tau']
    pdg_leptons = np.array([PDG_VALUES['leptons'][l] for l in lepton_names])
    errors_leptons = np.abs((me - pdg_leptons) / pdg_leptons * 100)

    all_pass = True
    for i, name in enumerate(lepton_names):
        status = "PASS" if errors_leptons[i] < LEPTON_ERROR_THRESHOLD else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"   {name}: {me[i]*1e3:.3f} MeV (PDG: {pdg_leptons[i]*1e3:.3f} MeV) - Error: {errors_leptons[i]:.3f}% [{status}]")

    if not all_pass:
        return False
    print()

    print("="*70)
    print("ALL VALIDATION CHECKS PASSED!")
    print("="*70)
    return True

if __name__ == "__main__":
    success = validate_masses()
    sys.exit(0 if success else 1)
