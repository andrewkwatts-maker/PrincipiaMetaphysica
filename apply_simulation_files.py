#!/usr/bin/env python3
"""
Apply simulation_file updates to config.py manually
"""
import re

# Mappings from batch_add_simulation_files.py
FORMULAS_TO_UPDATE = {
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

with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check current state
current_count = len(re.findall(r'simulation_file=', content))
print(f"Current simulation_file count: {current_count}")

# Find which formulas need updating
for formula_name, sim_file in FORMULAS_TO_UPDATE.items():
    pattern = rf'{formula_name}\s*=\s*Formula\('
    match = re.search(pattern, content)
    if match:
        # Find the formula block
        start = match.start()
        pos = match.end()
        depth = 1
        while pos < len(content) and depth > 0:
            if content[pos] == '(':
                depth += 1
            elif content[pos] == ')':
                depth -= 1
            pos += 1

        formula_block = content[start:pos]
        has_sim_file = 'simulation_file=' in formula_block
        print(f"{formula_name}: {'HAS' if has_sim_file else 'NEEDS'} simulation_file")
    else:
        print(f"{formula_name}: NOT FOUND")

print(f"\nTarget: Add {len(FORMULAS_TO_UPDATE)} simulation_file assignments")
