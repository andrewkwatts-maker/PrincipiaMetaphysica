#!/usr/bin/env python3
"""
Batch add simulation_file assignments to config.py formulas.
Based on SIMULATION_MAPPING_CORRECTIONS.txt

This script uses a safer string replacement method that finds unique context
around each formula and adds the simulation_file parameter.
"""

import sys
import os

# Mapping: formula_name → (simulation_file, unique_context_before_closing_paren)
# Format: {formula_name: (simulation_file, context_string)}
FORMULAS_TO_UPDATE = {
    'EFFECTIVE_DIMENSION': (
        'simulations/derive_d_eff_v12_8.py',
        '        computed_value=12.576,\n        related_formulas=["dark-energy-w0"]\n    )'
    ),
    'FRIEDMANN_CONSTRAINT': (
        'simulations/wz_evolution_desi_dr2.py',
        '        related_formulas=["dark-energy-w0", "dark-energy-wa"]\n    )'
    ),
    'DE_SITTER_ATTRACTOR': (
        'simulations/attractor_scalar_v12_8.py',
        '        notes="Ensures cosmic acceleration approaches de Sitter exponentially",\n        related_formulas=["attractor-potential", "dark-energy-wa"]\n    )'
    ),
    'GUT_SCALE': (
        'simulations/gauge_unification_precision_v12_4.py',
        None  # Will search for pattern
    ),
    'KAPPA_GUT_COEFFICIENT': (
        'simulations/gauge_unification_precision_v12_4.py',
        None
    ),
    'PLANCK_MASS_DERIVATION': (
        'simulations/gauge_unification_precision_v12_4.py',
        None
    ),
    'PROTON_LIFETIME': (
        'simulations/proton_decay_geometric_v13_0.py',
        None
    ),
    'DOUBLET_TRIPLET': (
        'simulations/doublet_triplet_splitting_v14_0.py',
        None
    ),
    'THETA23_MAXIMAL': (
        'simulations/derive_theta23_g2_v12_8.py',
        None
    ),
    'SEESAW_MECHANISM': (
        'simulations/neutrino_mass_matrix_final_v12_7.py',
        None
    ),
    'CKM_ELEMENTS': (
        'simulations/ckm_cp_rigor.py',
        None
    ),
    'HIGGS_VEV': (
        'simulations/derive_vev_pneuma.py',
        None
    ),
    'HIGGS_MASS': (
        'simulations/higgs_mass_v12_4_moduli_stabilization.py',
        None
    ),
    'HIGGS_POTENTIAL': (
        'simulations/pneuma_full_potential_v14_1.py',
        None
    ),
    'HIGGS_QUARTIC': (
        'simulations/higgs_yukawa_rg_v12_4.py',
        None
    ),
    'TOP_QUARK_MASS': (
        'simulations/higgs_yukawa_rg_v12_4.py',
        None
    ),
    'BOTTOM_QUARK_MASS': (
        'simulations/higgs_yukawa_rg_v12_4.py',
        None
    ),
    'TAU_LEPTON_MASS': (
        'simulations/higgs_yukawa_rg_v12_4.py',
        None
    ),
    'YUKAWA_INSTANTON': (
        'simulations/g2_yukawa_overlap_integrals_v15_0.py',
        None
    ),
    'GW_DISPERSION_COEFF': (
        'simulations/gw_dispersion_v12_8.py',
        None
    ),
    'GW_DISPERSION_ALT': (
        'simulations/gw_dispersion_v12_8.py',
        None
    ),
    'KK_GRAVITON': (
        'simulations/kk_spectrum_full.py',
        None
    ),
    'VIRASORO_ANOMALY': (
        'simulations/virasoro_anomaly_v12_8.py',
        None
    ),
    'SP2R_CONSTRAINTS': (
        'simulations/sp2r_gauge_fixing_validation_v13_0.py',
        None
    ),
    'REDUCTION_CASCADE': (
        'simulations/dim_decomp_v12_8.py',
        None
    ),
    'PRIMORDIAL_SPINOR_13D': (
        'simulations/g2_spinor_geometry_validation_v13_0.py',
        None
    ),
    'EFFECTIVE_EULER': (
        'simulations/g2_landscape_scanner_v14_1.py',
        None
    ),
    'FLUX_QUANTIZATION': (
        'simulations/flux_stabilization_full_v12_7.py',
        None
    ),
    'EFFECTIVE_TORSION': (
        'simulations/torsion_effective_v12_8.py',
        None
    ),
    'EFFECTIVE_TORSION_SPINOR': (
        'simulations/torsion_spinor_fraction_v12_8.py',
        None
    ),
    'GHOST_COEFFICIENT': (
        'simulations/virasoro_anomaly_v12_8.py',
        None
    ),
    'MIRROR_DM_RATIO': (
        'simulations/mirror_dark_matter_abundance_v15_3.py',
        None
    ),
    'MIRROR_TEMP_RATIO': (
        'simulations/mirror_dark_matter_abundance_v15_3.py',
        None
    ),
    'SO10_BREAKING': (
        'simulations/breaking_chain_geometric_v14_1.py',
        None
    ),
    'PATI_SALAM_CHAIN': (
        'simulations/breaking_chain_geometric_v14_1.py',
        None
    ),
}


def find_formula_block(content, formula_name):
    """Find the start and end of a formula definition."""
    import re

    # Find where the formula starts
    pattern = rf'^\s+{formula_name}\s*=\s*Formula\('
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return None, None

    start = match.start()

    # Find the matching closing parenthesis
    pos = match.end()
    depth = 1  # We're already inside the Formula(

    while pos < len(content) and depth > 0:
        if content[pos] == '(':
            depth += 1
        elif content[pos] == ')':
            depth -= 1
        pos += 1

    if depth != 0:
        return None, None

    end = pos
    return start, end


def add_simulation_file(content, formula_name, simulation_file):
    """Add simulation_file to a formula."""
    start, end = find_formula_block(content, formula_name)

    if start is None:
        print(f"  ERROR: Could not find formula {formula_name}")
        return content, False

    formula_block = content[start:end]

    # Check if simulation_file already exists
    if 'simulation_file=' in formula_block:
        print(f"  SKIP: {formula_name} already has simulation_file")
        return content, False

    # Find the last line before the closing )
    # Work backwards from the end
    lines = formula_block.split('\n')

    # The last line should be just whitespace + )
    if lines[-1].strip() == ')':
        # Good, insert before this line
        # Add comma to previous line if needed
        if lines[-2].strip() and not lines[-2].rstrip().endswith(','):
            lines[-2] = lines[-2] + ','

        # Insert the new line
        indent = '        '  # Standard indentation for Formula parameters
        new_line = f'{indent}simulation_file="{simulation_file}"'
        lines.insert(-1, new_line)

        new_formula_block = '\n'.join(lines)
        new_content = content[:start] + new_formula_block + content[end:]

        print(f"  SUCCESS: Added simulation_file to {formula_name}")
        return new_content, True
    else:
        print(f"  ERROR: Unexpected format for {formula_name}")
        return content, False


def main():
    if not os.path.exists('config.py'):
        print("ERROR: config.py not found in current directory")
        sys.exit(1)

    print("=" * 80)
    print("Adding simulation_file assignments to config.py")
    print("=" * 80)
    print(f"\nTotal formulas to update: {len(FORMULAS_TO_UPDATE)}")
    print()

    # Read config.py
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    successful = 0
    skipped = 0
    failed = 0

    # Process each formula
    for formula_name, (simulation_file, _) in sorted(FORMULAS_TO_UPDATE.items()):
        print(f"Processing {formula_name}...")
        content, success = add_simulation_file(content, formula_name, simulation_file)
        if success:
            successful += 1
        elif 'already has simulation_file' in str(success):
            skipped += 1
        else:
            failed += 1

    # Write the updated content
    if content != original_content:
        # Create backup
        import shutil
        shutil.copy2('config.py', 'config.py.backup')
        print(f"\nCreated backup: config.py.backup")

        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)

        print("\n" + "=" * 80)
        print("✓ Successfully updated config.py")
        print(f"  Added: {successful} formulas")
        print(f"  Skipped: {skipped} formulas")
        print(f"  Failed: {failed} formulas")
        print("=" * 80)

        # Verify
        import re
        count = len(re.findall(r'simulation_file=', content))
        print(f"\nVerification: {count} formulas now have simulation_file assignments")
    else:
        print("\n" + "=" * 80)
        print("No changes needed - all formulas already have simulation_file")
        print("=" * 80)


if __name__ == '__main__':
    main()
