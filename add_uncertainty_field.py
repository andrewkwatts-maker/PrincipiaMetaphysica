#!/usr/bin/env python3
"""
Add missing 'uncertainty' fields to Parameter definitions.
"""

import re
from pathlib import Path

# Map of parameter paths to uncertainties
UNCERTAINTIES = {
    # NuFIT 6.0
    "neutrino.theta_12_pred": 0.75,
    "neutrino.theta_13_pred": 0.11,
    "neutrino.theta_23_pred": 1.5,
    "neutrino.delta_CP_pred": 28.0,

    # DESI 2024
    "cosmology.w0_derived": 0.067,
    "cosmology.H0": 0.62,
    "cosmology.Omega_m": 0.005,
    "desi.w0": 0.067,
    "desi.wa": 0.21,
    "desi.Omega_m": 0.005,
    "desi.sigma8": 0.011,

    # Planck 2018
    "planck.S8": 0.013,
    "cosmology.s8_pm_predicted": 0.020,  # KiDS-1000 uncertainty

    # PDG 2024
    "pdg.alpha_s_MZ": 0.001,
    "pdg.sin2_theta_W": 0.00004,
    "pdg.m_Z": 0.0021,

    # CODATA 2022
    "electromagnetic.alpha_inv": 0.000000021,
    "fermion.mass_ratio_proton_electron": 0.00000011,

    # Proton decay - no uncertainty on lower bound
    "proton_decay.tau_p_years": None,
    "bounds.tau_proton_lower": None,
}

def process_file(file_path: Path):
    """Add uncertainty field to parameters that are missing it."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Pattern: Find Parameter blocks with experimental_bound but no uncertainty
    # Look for experimental_bound followed by bound_type, but NOT followed by uncertainty
    pattern = r'(experimental_bound=([^,\n]+),\s*\n\s*bound_type="([^"]+)",\s*\n\s*bound_source="([^"]+)")'

    def add_uncertainty(match):
        full_match = match.group(0)
        exp_value = match.group(2)
        bound_type = match.group(3)
        bound_source = match.group(4)

        # Check if uncertainty already present right after
        lookahead_pos = match.end()
        next_chars = content[lookahead_pos:lookahead_pos+100]

        if 'uncertainty=' in next_chars:
            return full_match  # Already has uncertainty

        # Try to find which parameter this is by looking back
        lookback = content[max(0, match.start()-500):match.start()]
        path_match = re.search(r'path="([^"]+)"', lookback)

        uncertainty_value = None
        if path_match:
            param_path = path_match.group(1)
            for key, unc in UNCERTAINTIES.items():
                if key in param_path or param_path in key:
                    uncertainty_value = unc
                    break

        # Add uncertainty field
        return full_match + f',\n                uncertainty={uncertainty_value}'

    content = re.sub(pattern, add_uncertainty, content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all v16 simulation files."""
    v16_dir = Path("h:/Github/PrincipiaMetaphysica/simulations/v16")

    py_files = [
        f for f in v16_dir.rglob("*.py")
        if f.name != "__init__.py" and "test_" not in f.name
    ]

    modified = 0
    for py_file in sorted(py_files):
        try:
            if process_file(py_file):
                print(f"[OK] Updated: {py_file.name}")
                modified += 1
            else:
                print(f"  Skip: {py_file.name}")
        except Exception as e:
            print(f"[ERROR] {py_file.name}: {e}")

    print(f"\nModified {modified}/{len(py_files)} files")

if __name__ == "__main__":
    main()
