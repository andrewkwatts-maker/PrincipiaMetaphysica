#!/usr/bin/env python3
"""
Add experimental values to parameter metadata in theory_output.json

This script enriches the parameter metadata with:
- experimentalValue: measured value from established physics
- experimentalSource: citation (PDG 2024, NuFIT 6.0, DESI DR2, etc.)
- experimentalUncertainty: measurement uncertainty

This allows the website to show computed vs experimental comparison.
"""

import json
import sys
from pathlib import Path

# Parameter key to experimental value mapping
# Format: (value, uncertainty, source)
EXPERIMENTAL_VALUES = {
    # PDG 2024 - Particle masses
    "pdg.m_higgs": (125.10, 0.14, "PDG 2024"),
    "pdg.m_electron": (0.0005109989461, 0.0000000000031, "PDG 2024"),
    "pdg.m_muon": (0.1056583745, 0.0000000024, "PDG 2024"),
    "pdg.m_tau": (1.77686, 0.00012, "PDG 2024"),
    "pdg.m_up": (2.16e-3, 0.49e-3, "PDG 2024 (MS-bar, 2 GeV)"),
    "pdg.m_down": (4.67e-3, 0.48e-3, "PDG 2024 (MS-bar, 2 GeV)"),
    "pdg.m_strange": (0.093, 0.011, "PDG 2024 (MS-bar, 2 GeV)"),
    "pdg.m_charm": (1.27, 0.02, "PDG 2024 (MS-bar)"),
    "pdg.m_bottom": (4.18, 0.03, "PDG 2024 (MS-bar)"),
    "pdg.m_top": (172.76, 0.30, "PDG 2024"),

    # PDG 2024 - Gauge couplings and masses
    "pdg.alpha_s_MZ": (0.1180, 0.0010, "PDG 2024"),
    "pdg.sin2_theta_W": (0.23121, 0.00004, "PDG 2024"),
    "pdg.m_W": (80.377, 0.012, "PDG 2024"),
    "pdg.m_Z": (91.1876, 0.0021, "PDG 2024"),

    # NuFIT 6.0 (2024) - Neutrino mixing angles
    "nufit.theta_12": (33.41, 0.75, "NuFIT 6.0 (2024)"),
    "nufit.theta_23": (45.0, 1.0, "NuFIT 6.0 (2024)"),
    "nufit.theta_13": (8.54, 0.12, "NuFIT 6.0 (2024)"),
    "nufit.delta_CP": (194.0, 25.0, "NuFIT 6.0 (2024)"),

    # NuFIT 6.0 - Neutrino mass splittings
    "nufit.delta_m21_sq": (7.42e-5, 0.21e-5, "NuFIT 6.0 (2024) [eV^2]"),
    "nufit.delta_m31_sq": (2.517e-3, 0.026e-3, "NuFIT 6.0 (2024) [eV^2, NO]"),

    # DESI DR2 2024 - Dark energy
    "desi.w0": (-0.827, 0.063, "DESI DR2 2024"),
    "desi.wa": (-0.75, 0.30, "DESI DR2 2024"),

    # DESI + Planck - Cosmological parameters
    "desi.H0": (68.52, 0.62, "DESI+CMB 2024 [km/s/Mpc]"),
    "desi.Omega_m": (0.3080, 0.0076, "DESI+CMB 2024"),
    "desi.sigma8": (0.812, 0.012, "DESI+CMB 2024"),

    # Planck 2018
    "planck.S8": (0.834, 0.016, "Planck 2018"),

    # Super-Kamiokande - Proton decay bound
    "bounds.tau_proton_lower": (1.67e34, 0, "Super-Kamiokande 2017 (90% CL lower bound)"),

    # Neutrino mass sum
    "bounds.sum_m_nu_upper": (0.12, 0, "Planck+BAO 2018 (95% CL upper bound)"),

    # Additional established constants
    "constants.M_PLANCK": (2.435e18, 3e15, "PDG 2024 (Reduced Planck mass)"),
    "constants.alpha_em": (7.2973525693e-3, 1.1e-12, "CODATA 2018"),
    "constants.m_proton": (0.938272088, 0.000000001, "PDG 2024"),

    # Higgs VEV
    "higgs.vev": (246.22, 0.0, "PDG 2024 (from Fermi constant)"),

    # CKM matrix elements (PDG 2024)
    "ckm.V_us": (0.2243, 0.0005, "PDG 2024"),
    "ckm.V_cb": (0.0422, 0.0008, "PDG 2024"),
    "ckm.V_ub": (0.00382, 0.00024, "PDG 2024"),
    "ckm.V_td": (0.0086, 0.0002, "PDG 2024"),
    "ckm.V_ts": (0.0415, 0.0010, "PDG 2024"),
    "ckm.V_tb": (0.999, 0.000029, "PDG 2024"),
    "ckm.jarlskog_invariant": (3.08e-5, 0.15e-5, "PDG 2024"),
}


def add_experimental_values_to_theory_output(theory_path: Path, output_path: Path = None):
    """
    Add experimental values to parameters in theory_output.json

    Args:
        theory_path: Path to theory_output.json
        output_path: Path to write updated file (default: overwrite theory_path)
    """
    if output_path is None:
        output_path = theory_path

    print(f"Loading theory_output.json from: {theory_path}")
    with open(theory_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'parameters' not in data:
        print("ERROR: No 'parameters' field found in theory_output.json")
        sys.exit(1)

    parameters = data['parameters']
    total_params = len(parameters)
    updated_count = 0

    print(f"\nProcessing {total_params} parameters...")
    print("-" * 80)

    # Add experimental values to matching parameters
    for param_key in parameters:
        if param_key in EXPERIMENTAL_VALUES:
            exp_value, exp_uncertainty, exp_source = EXPERIMENTAL_VALUES[param_key]

            # Get current parameter data
            param_data = parameters[param_key]
            computed_value = param_data.get('value', None)

            # Add experimental metadata
            param_data['experimentalValue'] = exp_value
            param_data['experimentalUncertainty'] = exp_uncertainty
            param_data['experimentalSource'] = exp_source

            # Calculate deviation if both values exist
            if computed_value is not None and exp_value != 0:
                # Relative deviation
                deviation = abs(computed_value - exp_value) / abs(exp_value)
                param_data['relativeDeviation'] = deviation

                # Sigma deviation (if uncertainty > 0)
                if exp_uncertainty > 0:
                    sigma_dev = abs(computed_value - exp_value) / exp_uncertainty
                    param_data['sigmaDeviation'] = sigma_dev

                # Order of magnitude agreement
                import math
                if exp_value != 0 and computed_value != 0:
                    oom_diff = abs(math.log10(abs(computed_value)) - math.log10(abs(exp_value)))
                    param_data['oomAgreement'] = oom_diff < 1.0  # Within 1 OOM
                    param_data['oomDifference'] = oom_diff

            updated_count += 1

            # Print summary
            status = "OK"
            if computed_value is not None:
                if 'sigmaDeviation' in param_data:
                    sigma = param_data['sigmaDeviation']
                    if sigma < 1.0:
                        status_str = f"OK {sigma:.2f}sig"
                    elif sigma < 3.0:
                        status_str = f"~  {sigma:.2f}sig"
                    else:
                        status_str = f"X  {sigma:.2f}sig"
                else:
                    status_str = "OK"
            else:
                status_str = "~  (no computed value)"

            print(f"{status_str:20s} {param_key:35s} | exp={exp_value:12.6g} +/- {exp_uncertainty:10.6g} | {exp_source}")

    print("-" * 80)
    print(f"\nUpdated {updated_count}/{total_params} parameters with experimental values")

    # Write updated data
    print(f"\nWriting updated theory_output.json to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("OK Done!")

    # Print summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    # Count parameters by agreement
    excellent = 0  # < 1sig
    good = 0       # 1-3sig
    poor = 0       # > 3sig
    no_comparison = 0

    for param_key in parameters:
        param_data = parameters[param_key]
        if 'experimentalValue' in param_data:
            if 'sigmaDeviation' in param_data:
                sigma = param_data['sigmaDeviation']
                if sigma < 1.0:
                    excellent += 1
                elif sigma < 3.0:
                    good += 1
                else:
                    poor += 1
            else:
                no_comparison += 1

    total_with_exp = excellent + good + poor + no_comparison

    print(f"Parameters with experimental values: {total_with_exp}")
    print(f"  - Excellent agreement (< 1sig):      {excellent:3d} ({100*excellent/total_with_exp:.1f}%)")
    print(f"  - Good agreement (1-3sig):           {good:3d} ({100*good/total_with_exp:.1f}%)")
    print(f"  - Poor agreement (> 3sig):           {poor:3d} ({100*poor/total_with_exp:.1f}%)")
    print(f"  - No computed value:               {no_comparison:3d}")
    print("=" * 80)


if __name__ == "__main__":
    # Paths
    repo_root = Path(__file__).parent
    theory_path = repo_root / "AutoGenerated" / "theory_output.json"

    if not theory_path.exists():
        print(f"ERROR: theory_output.json not found at: {theory_path}")
        sys.exit(1)

    # Run the update
    add_experimental_values_to_theory_output(theory_path)

    print("\nOK Experimental values added to theory_output.json")
    print("  The parameters table on the website will now show experimental comparisons.")
