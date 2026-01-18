#!/usr/bin/env python3
"""
Script to add inputParams and outputParams to all formulas in v16 simulations.
"""

import re
import sys

# Mapping of formula IDs to their input/output parameters
# Based on run() method analysis of each simulation

FORMULA_PARAMS = {
    # g2_geometry_v16_0.py
    "g2-holonomy": {
        "inputParams": [],
        "outputParams": []
    },
    "euler-characteristic": {
        "inputParams": [],
        "outputParams": ["topology.CHI_EFF"]
    },
    "betti-numbers": {
        "inputParams": [],
        "outputParams": ["topology.b2", "topology.b3"]
    },
    "three-generations": {
        "inputParams": ["topology.CHI_EFF"],
        "outputParams": ["topology.n_gen"]
    },
    "cycle-matching": {
        "inputParams": ["topology.b2"],
        "outputParams": ["topology.K_MATCHING"]
    },

    # gauge_unification_v16_0.py
    "gut-scale": {
        "inputParams": ["pdg.alpha_s_MZ", "pdg.sin2_theta_W", "pdg.m_Z", "constants.alpha_em", "constants.M_PLANCK"],
        "outputParams": ["gauge.M_GUT"]
    },
    "gauge-coupling-unification": {
        "inputParams": ["pdg.alpha_s_MZ", "pdg.sin2_theta_W", "pdg.m_Z", "constants.alpha_em", "constants.M_PLANCK"],
        "outputParams": ["gauge.M_GUT", "gauge.ALPHA_GUT", "gauge.ALPHA_GUT_INV"]
    },
    "gauge-rg-evolution": {
        "inputParams": [],
        "outputParams": []
    },

    # fermion_generations_v16_0.py
    "generation-number": {
        "inputParams": ["topology.CHI_EFF", "topology.b3"],
        "outputParams": ["fermion.n_generations", "fermion.n_flux"]
    },
    "yukawa-texture": {
        "inputParams": ["topology.CHI_EFF"],
        "outputParams": ["fermion.yukawa_hierarchy", "fermion.epsilon_fn"]
    },
    "pneuma-chiral-filter": {
        "inputParams": [],
        "outputParams": ["fermion.chiral_filter_strength"]
    },

    # proton_decay_v16_0.py
    "cycle-separation-suppression": {
        "inputParams": ["topology.K_MATCHING"],
        "outputParams": ["proton_decay.suppression_factor", "proton_decay.d_over_R"]
    },
    "proton-lifetime": {
        "inputParams": ["gauge.M_GUT", "gauge.ALPHA_GUT", "proton_decay.suppression_factor"],
        "outputParams": ["proton_decay.tau_p_years"]
    },

    # higgs_mass_v16_0.py
    "higgs-mass": {
        "inputParams": ["higgs.vev_yukawa", "higgs.lambda_eff_pheno"],
        "outputParams": ["higgs.m_higgs_pred"]
    },
    "higgs-quartic-coupling": {
        "inputParams": ["moduli.re_t_phenomenological", "yukawa.y_top"],
        "outputParams": ["higgs.lambda_eff_pheno"]
    },
    "racetrack-potential": {
        "inputParams": ["topology.B3", "topology.CHI_EFF"],
        "outputParams": ["moduli.re_t_attractor"]
    },
    "doublet-triplet-splitting": {
        "inputParams": ["gauge.M_GUT", "higgs.vev"],
        "outputParams": ["higgs.dt_splitting_ratio"]
    },

    # neutrino_mixing_v16_0.py
    "pmns-theta-13": {
        "inputParams": ["topology.b2", "topology.b3", "topology.n_gen", "topology.CHI_EFF", "topology.orientation_sum"],
        "outputParams": ["neutrino.theta_13_pred"]
    },
    "pmns-delta-cp": {
        "inputParams": ["topology.b2", "topology.b3", "topology.n_gen"],
        "outputParams": ["neutrino.delta_CP_pred"]
    },
    "pmns-theta-12": {
        "inputParams": ["topology.b2", "topology.b3", "topology.n_gen", "topology.CHI_EFF"],
        "outputParams": ["neutrino.theta_12_pred"]
    },
    "pmns-theta-23": {
        "inputParams": ["topology.b2", "topology.n_gen"],
        "outputParams": ["neutrino.theta_23_pred"]
    },
    "neutrino-mass-spectrum": {
        "inputParams": ["topology.b2", "topology.b3", "topology.CHI_EFF"],
        "outputParams": ["neutrino.m1", "neutrino.m2", "neutrino.m3"]
    },

    # multi_sector_v16_0.py
    "dark-energy-eos": {
        "inputParams": ["topology.D_eff"],
        "outputParams": ["cosmology.w_eff"]
    },
    "moduli-potential": {
        "inputParams": ["topology.CHI_EFF"],
        "outputParams": ["cosmology.modulation_width"]
    },
    "sector-temperature-ratio": {
        "inputParams": ["topology.CHI_EFF"],
        "outputParams": ["cosmology.T_mirror_ratio"]
    },
    "dark-matter-abundance": {
        "inputParams": ["cosmology.T_mirror_ratio"],
        "outputParams": ["cosmology.Omega_DM_over_b"]
    },

    # pneuma_mechanism_v16_0.py
    "pneuma-lagrangian": {
        "inputParams": ["topology.CHI_EFF", "topology.B3"],
        "outputParams": ["pneuma.coupling"]
    },
    "pneuma-flow": {
        "inputParams": ["pneuma.flow_parameter"],
        "outputParams": ["pneuma.vev"]
    },
}


def add_params_to_formula(formula_text, formula_id):
    """Add inputParams and outputParams to a formula definition."""
    if formula_id not in FORMULA_PARAMS:
        print(f"WARNING: Unknown formula ID: {formula_id}")
        return formula_text

    params = FORMULA_PARAMS[formula_id]
    input_params = params["inputParams"]
    output_params = params["outputParams"]

    # Check if already has inputParams/outputParams
    if "inputParams=" in formula_text:
        print(f"  Formula {formula_id} already has inputParams/outputParams, skipping")
        return formula_text

    # Find where to insert (before input_params=)
    # Pattern matches: description="...",\n  input_params=
    pattern = r'(description="[^"]*",)\s*\n(\s*)(input_params=)'

    # Build the new parameters
    input_list = "[" + ", ".join(f'"{p}"' for p in input_params) + "]"
    output_list = "[" + ", ".join(f'"{p}"' for p in output_params) + "]"

    replacement = f'\\1\n\\2inputParams={input_list},\n\\2outputParams={output_list},\n\\2\\3'

    result = re.sub(pattern, replacement, formula_text)

    if result == formula_text:
        print(f"  WARNING: Could not add params to formula {formula_id}")
    else:
        print(f"  Added params to formula {formula_id}")

    return result


def process_file(filepath):
    """Process a single file and add parameters to all formulas."""
    print(f"\nProcessing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Formula( blocks and extract IDs
    formula_pattern = r'Formula\(\s*id="([^"]+)"'
    formula_ids = re.findall(formula_pattern, content)

    print(f"Found {len(formula_ids)} formulas: {formula_ids}")

    # Process each formula
    modified = content
    for formula_id in formula_ids:
        # Find the complete Formula block
        pattern = rf'(Formula\(\s*id="{formula_id}".*?(?=\)|Formula\())'
        match = re.search(pattern, modified, re.DOTALL)
        if match:
            original = match.group(0)
            updated = add_params_to_formula(original, formula_id)
            modified = modified.replace(original, updated)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(modified)

    print(f"Completed {filepath}")


def main():
    """Main function."""
    files = [
        'simulations/v21/geometric/g2_geometry_v16_0.py',
        'simulations/v21/gauge/gauge_unification_v16_0.py',
        'simulations/v21/fermion/fermion_generations_v16_0.py',
        'simulations/v21/proton/proton_decay_v16_0.py',
        'simulations/v21/higgs/higgs_mass_v16_0.py',
        'simulations/v21/neutrino/neutrino_mixing_v16_0.py',
        'simulations/v21/cosmology/multi_sector_v16_0.py',
        'simulations/v21/pneuma/pneuma_mechanism_v16_0.py',
    ]

    for filepath in files:
        try:
            process_file(filepath)
        except Exception as e:
            print(f"ERROR processing {filepath}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print("COMPLETE: Added inputParams and outputParams to all formulas")
    print("="*70)


if __name__ == "__main__":
    main()
