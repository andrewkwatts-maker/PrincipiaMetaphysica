#!/usr/bin/env python3
"""
Update experimental metadata for v16 simulation parameters
===========================================================

This script adds experimental_bound, bound_type, bound_source, and uncertainty
fields to Parameter definitions in v16 simulation files.

Sources:
- PDG 2024: Particle masses, couplings, mixing angles
- DESI DR2 2024: H0, w0, wa, Omega_m
- Planck 2018: CMB parameters (S8, Omega_m)
- NuFIT 6.0 2024: Neutrino mixing angles
- Super-Kamiokande 2024: Proton lifetime lower bound
- CODATA 2022: Fundamental constants (alpha, m_p/m_e)
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

# Experimental values from established sources
EXPERIMENTAL_VALUES = {
    # CODATA 2022 - Fundamental Constants
    "constants.alpha_inv": {
        "value": 137.035999084,
        "uncertainty": 0.000000021,
        "source": "CODATA 2022",
        "bound_type": "measured"
    },
    "constants.m_p_over_m_e": {
        "value": 1836.15267343,
        "uncertainty": 0.00000011,
        "source": "CODATA 2022",
        "bound_type": "measured"
    },

    # PDG 2024 - Gauge couplings at M_Z
    "pdg.alpha_s_MZ": {
        "value": 0.1180,
        "uncertainty": 0.0010,
        "source": "PDG 2024",
        "bound_type": "measured"
    },
    "pdg.sin2_theta_W": {
        "value": 0.23121,
        "uncertainty": 0.00004,
        "source": "PDG 2024",
        "bound_type": "measured"
    },
    "pdg.m_Z": {
        "value": 91.1876,
        "uncertainty": 0.0021,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },

    # PDG 2024 - Fermion masses (GeV)
    "pdg.m_electron": {
        "value": 0.5109989461e-3,
        "uncertainty": 0.0000000031e-3,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },
    "pdg.m_muon": {
        "value": 0.1056583745,
        "uncertainty": 0.0000000024,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },
    "pdg.m_tau": {
        "value": 1.77686,
        "uncertainty": 0.00012,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },
    "pdg.m_up": {
        "value": 2.16e-3,
        "uncertainty": 0.49e-3,
        "source": "PDG 2024 MS-bar 2 GeV",
        "bound_type": "measured"
    },
    "pdg.m_down": {
        "value": 4.67e-3,
        "uncertainty": 0.48e-3,
        "source": "PDG 2024 MS-bar 2 GeV",
        "bound_type": "measured"
    },
    "pdg.m_strange": {
        "value": 93.4e-3,
        "uncertainty": 8.6e-3,
        "source": "PDG 2024 MS-bar 2 GeV",
        "bound_type": "measured"
    },
    "pdg.m_charm": {
        "value": 1.27,
        "uncertainty": 0.02,
        "source": "PDG 2024 MS-bar (GeV)",
        "bound_type": "measured"
    },
    "pdg.m_bottom": {
        "value": 4.18,
        "uncertainty": 0.03,
        "source": "PDG 2024 MS-bar (GeV)",
        "bound_type": "measured"
    },
    "pdg.m_top": {
        "value": 172.69,
        "uncertainty": 0.30,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },
    "pdg.m_proton": {
        "value": 0.938272088,
        "uncertainty": 0.000000001,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },

    # Higgs mass
    "pdg.m_higgs": {
        "value": 125.25,
        "uncertainty": 0.17,
        "source": "PDG 2024 (GeV)",
        "bound_type": "measured"
    },

    # NuFIT 6.0 2024 - Neutrino mixing angles (degrees)
    "nufit.theta_12": {
        "value": 33.41,
        "uncertainty": 0.75,
        "source": "NuFIT 6.0 (2024)",
        "bound_type": "measured"
    },
    "nufit.theta_13": {
        "value": 8.54,
        "uncertainty": 0.11,
        "source": "NuFIT 6.0 (2024)",
        "bound_type": "measured"
    },
    "nufit.theta_23": {
        "value": 49.0,
        "uncertainty": 1.5,
        "source": "NuFIT 6.0 (2024) upper octant",
        "bound_type": "measured"
    },
    "nufit.delta_CP": {
        "value": 230.0,
        "uncertainty": 28.0,
        "source": "NuFIT 6.0 (2024)",
        "bound_type": "measured"
    },

    # DESI DR2 2024 - Cosmology
    "desi.H0": {
        "value": 68.52,
        "uncertainty": 0.62,
        "source": "DESI 2024 BAO+CMB (km/s/Mpc)",
        "bound_type": "measured"
    },
    "desi.w0": {
        "value": -0.727,
        "uncertainty": 0.067,
        "source": "DESI 2024 BAO+CMB+PantheonPlus",
        "bound_type": "measured"
    },
    "desi.wa": {
        "value": -0.27,
        "uncertainty": 0.21,
        "source": "DESI 2024 BAO+CMB+PantheonPlus",
        "bound_type": "measured"
    },
    "desi.Omega_m": {
        "value": 0.3069,
        "uncertainty": 0.0050,
        "source": "DESI 2024",
        "bound_type": "measured"
    },
    "desi.sigma8": {
        "value": 0.827,
        "uncertainty": 0.011,
        "source": "DESI 2024",
        "bound_type": "measured"
    },

    # Planck 2018 - CMB
    "planck.S8": {
        "value": 0.832,
        "uncertainty": 0.013,
        "source": "Planck 2018",
        "bound_type": "measured"
    },
    "planck.Omega_m": {
        "value": 0.3153,
        "uncertainty": 0.0073,
        "source": "Planck 2018",
        "bound_type": "measured"
    },

    # Super-Kamiokande 2024 - Proton decay
    "super_k.tau_proton_lower": {
        "value": 1.67e34,
        "uncertainty": None,
        "source": "Super-Kamiokande 2024 90% CL (years)",
        "bound_type": "lower"
    },
}

def add_experimental_metadata_to_parameter(param_block: str, param_path: str) -> str:
    """
    Add experimental metadata fields to a Parameter definition.

    Args:
        param_block: The full Parameter(...) block as a string
        param_path: The path identifier (e.g., "gauge.M_GUT")

    Returns:
        Updated parameter block with experimental metadata
    """
    # Check if this parameter has experimental data
    exp_data = None
    for key, data in EXPERIMENTAL_VALUES.items():
        if key in param_path or param_path in key:
            exp_data = data
            break

    if not exp_data:
        # No experimental data - mark as theoretical prediction
        if "experimental_bound=" not in param_block:
            # Add after derivation_formula if present, otherwise after description
            if "derivation_formula=" in param_block:
                param_block = param_block.replace(
                    'derivation_formula=',
                    f'experimental_bound=None,\n                bound_type="theoretical_prediction",\n                bound_source="No direct measurement",\n                uncertainty=None,\n                derivation_formula='
                )
            elif "description=" in param_block:
                param_block = re.sub(
                    r'(description=.*?",)\n',
                    r'\1\n                experimental_bound=None,\n                bound_type="theoretical_prediction",\n                bound_source="No direct measurement",\n                uncertainty=None,\n',
                    param_block,
                    count=1
                )
        return param_block

    # Has experimental data - add the fields
    if "experimental_bound=" not in param_block:
        value = exp_data["value"]
        uncertainty = exp_data["uncertainty"]
        source = exp_data["source"]
        bound_type = exp_data["bound_type"]

        # Format the new fields
        new_fields = f"""experimental_bound={value},
                bound_type="{bound_type}",
                bound_source="{source}",
                uncertainty={uncertainty},"""

        # Insert after derivation_formula if present, otherwise after description
        if "derivation_formula=" in param_block:
            param_block = param_block.replace(
                'derivation_formula=',
                f'{new_fields}\n                derivation_formula='
            )
        elif "description=" in param_block:
            param_block = re.sub(
                r'(description=.*?",)\n',
                f'\\1\n                {new_fields}\n',
                param_block,
                count=1
            )

    return param_block

def process_simulation_file(file_path: Path) -> bool:
    """
    Process a single simulation file to add experimental metadata.

    Args:
        file_path: Path to simulation file

    Returns:
        True if file was modified, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Find all Parameter blocks
        param_pattern = r'(Parameter\s*\([\s\S]*?path="([^"]+)"[\s\S]*?\))'
        matches = re.finditer(param_pattern, content)

        modifications = []
        for match in matches:
            param_block = match.group(1)
            param_path = match.group(2)

            updated_block = add_experimental_metadata_to_parameter(param_block, param_path)

            if updated_block != param_block:
                modifications.append((param_block, updated_block))

        # Apply modifications
        for old, new in modifications:
            content = content.replace(old, new, 1)

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated: {file_path.name}")
            return True
        else:
            print(f"  No changes: {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] Error processing {file_path.name}: {e}")
        return False

def main():
    """Main entry point."""
    print("=" * 70)
    print(" UPDATING EXPERIMENTAL METADATA IN V16 SIMULATIONS")
    print("=" * 70)
    print()

    # Find all v16 simulation files
    v16_dir = Path("simulations/v16")
    if not v16_dir.exists():
        v16_dir = Path("h:/Github/PrincipiaMetaphysica/simulations/v16")

    if not v16_dir.exists():
        print(f"ERROR: Cannot find v16 directory at {v16_dir}")
        return

    # Get all Python files (excluding __init__.py)
    py_files = [
        f for f in v16_dir.rglob("*.py")
        if f.name != "__init__.py" and "test_" not in f.name
    ]

    print(f"Found {len(py_files)} simulation files to process\n")

    # Process each file
    modified_count = 0
    for py_file in sorted(py_files):
        if process_simulation_file(py_file):
            modified_count += 1

    print()
    print("=" * 70)
    print(f" COMPLETE: Modified {modified_count}/{len(py_files)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
