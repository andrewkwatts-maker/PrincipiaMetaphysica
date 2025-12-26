#!/usr/bin/env python3
"""
Add missing simulation_file assignments to formulas in config.py
Based on SIMULATION_MAPPING_CORRECTIONS.txt
"""

import re

# Mapping of formulas to simulation files that need to be ADDED
FORMULAS_TO_ADD = {
    'DARK_ENERGY_W0': 'simulations/wz_evolution_desi_dr2.py',
    'EFFECTIVE_DIMENSION': 'simulations/derive_d_eff_v12_8.py',
    'FRIEDMANN_CONSTRAINT': 'simulations/wz_evolution_desi_dr2.py',
    'DE_SITTER_ATTRACTOR': 'simulations/attractor_scalar_v12_8.py',
    'GUT_SCALE': 'simulations/gauge_unification_precision_v12_4.py',
    'KAPPA_GUT_COEFFICIENT': 'simulations/gauge_unification_precision_v12_4.py',
    'PLANCK_MASS_DERIVATION': 'simulations/gauge_unification_precision_v12_4.py',
    'PROTON_LIFETIME': 'simulations/proton_decay_geometric_v13_0.py',
    'DOUBLET_TRIPLET': 'simulations/doublet_triplet_splitting_v14_0.py',
    'THETA23_MAXIMAL': 'simulations/derive_theta23_g2_v12_8.py',
    'SEESAW_MECHANISM': 'simulations/neutrino_mass_matrix_final_v12_7.py',
    'CKM_ELEMENTS': 'simulations/ckm_cp_rigor.py',
    'HIGGS_VEV': 'simulations/derive_vev_pneuma.py',
    'HIGGS_MASS': 'simulations/higgs_mass_v12_4_moduli_stabilization.py',
    'HIGGS_POTENTIAL': 'simulations/pneuma_full_potential_v14_1.py',
    'HIGGS_QUARTIC': 'simulations/higgs_yukawa_rg_v12_4.py',
    'TOP_QUARK_MASS': 'simulations/higgs_yukawa_rg_v12_4.py',
    'BOTTOM_QUARK_MASS': 'simulations/higgs_yukawa_rg_v12_4.py',
    'TAU_LEPTON_MASS': 'simulations/higgs_yukawa_rg_v12_4.py',
    'YUKAWA_INSTANTON': 'simulations/g2_yukawa_overlap_integrals_v15_0.py',
    'GW_DISPERSION_COEFF': 'simulations/gw_dispersion_v12_8.py',
    'GW_DISPERSION_ALT': 'simulations/gw_dispersion_v12_8.py',
    'KK_GRAVITON': 'simulations/kk_spectrum_full.py',
    'VIRASORO_ANOMALY': 'simulations/virasoro_anomaly_v12_8.py',
    'SP2R_CONSTRAINTS': 'simulations/sp2r_gauge_fixing_validation_v13_0.py',
    'REDUCTION_CASCADE': 'simulations/dim_decomp_v12_8.py',
    'PRIMORDIAL_SPINOR_13D': 'simulations/g2_spinor_geometry_validation_v13_0.py',
    'EFFECTIVE_EULER': 'simulations/g2_landscape_scanner_v14_1.py',
    'FLUX_QUANTIZATION': 'simulations/flux_stabilization_full_v12_7.py',
    'EFFECTIVE_TORSION': 'simulations/torsion_effective_v12_8.py',
    'EFFECTIVE_TORSION_SPINOR': 'simulations/torsion_spinor_fraction_v12_8.py',
    'GHOST_COEFFICIENT': 'simulations/virasoro_anomaly_v12_8.py',
    'MIRROR_DM_RATIO': 'simulations/mirror_dark_matter_abundance_v15_3.py',
    'MIRROR_TEMP_RATIO': 'simulations/mirror_dark_matter_abundance_v15_3.py',
    'SO10_BREAKING': 'simulations/breaking_chain_geometric_v14_1.py',
    'PATI_SALAM_CHAIN': 'simulations/breaking_chain_geometric_v14_1.py',
}


def add_simulation_file_to_formula(content, formula_name, simulation_file):
    """
    Add simulation_file to a formula definition.
    Finds the formula block and adds simulation_file before the closing parenthesis.
    """
    # Find the formula definition
    pattern = rf'(\s+{formula_name}\s*=\s*Formula\([\s\S]*?)(\n\s+\))'

    def replace_func(match):
        formula_block = match.group(1)
        closing = match.group(2)

        # Check if simulation_file already exists
        if 'simulation_file=' in formula_block:
            print(f"  WARNING: {formula_name} already has simulation_file, skipping")
            return match.group(0)

        # Add simulation_file before the closing parenthesis
        # Find the last line before the closing parenthesis
        lines = formula_block.split('\n')

        # Add comma to the last non-empty line if it doesn't have one
        for i in range(len(lines) - 1, -1, -1):
            stripped = lines[i].strip()
            if stripped and not stripped.endswith(','):
                lines[i] = lines[i] + ','
                break

        # Reconstruct the block with the new simulation_file line
        new_block = '\n'.join(lines)
        new_line = f'\n        simulation_file="{simulation_file}"'

        return new_block + new_line + closing

    new_content, count = re.subn(pattern, replace_func, content, count=1)

    if count == 0:
        print(f"  ERROR: Could not find formula {formula_name}")
        return content, False
    else:
        print(f"  SUCCESS: Added simulation_file to {formula_name}")
        return new_content, True


def main():
    print("Adding simulation_file assignments to config.py...")
    print("=" * 80)

    # Read config.py
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    successful = 0
    failed = 0

    # Process each formula
    for formula_name, simulation_file in sorted(FORMULAS_TO_ADD.items()):
        print(f"\nProcessing {formula_name}...")
        content, success = add_simulation_file_to_formula(content, formula_name, simulation_file)
        if success:
            successful += 1
        else:
            failed += 1

    # Write the updated content
    if content != original_content:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n" + "=" * 80)
        print(f"✓ Successfully updated config.py")
        print(f"  Added: {successful} formulas")
        print(f"  Failed: {failed} formulas")
    else:
        print("\n" + "=" * 80)
        print("No changes made to config.py")


if __name__ == '__main__':
    main()
