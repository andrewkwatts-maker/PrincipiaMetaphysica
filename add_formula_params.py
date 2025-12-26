#!/usr/bin/env python3
"""
Add input_params and output_params to Formula definitions in config.py.

This ensures the Single Source of Truth - params are defined where formulas are created.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re

# Mapping of formula IDs to their input/output params (using category.param_id format)
FORMULA_PARAMS = {
    'generation-number': {
        'input_params': ['topology.CHI_EFF'],
        'output_params': ['topology.n_gen']
    },
    'gut-scale': {
        'input_params': ['dimensions.D_EFFECTIVE'],
        'output_params': ['gauge.M_GUT']
    },
    'dark-energy-w0': {
        'input_params': ['dark_energy.d_eff'],
        'output_params': ['dark_energy.w0']
    },
    'proton-lifetime': {
        'input_params': ['gauge.M_GUT', 'gauge.ALPHA_GUT'],
        'output_params': ['proton_decay.tau_p_years']
    },
    'theta23-maximal': {
        'input_params': [],
        'output_params': ['pmns.theta_23']
    },
    'kk-graviton': {
        'input_params': ['dimensions.D_EFFECTIVE'],
        'output_params': ['kk_spectrum.m1_TeV']
    },
    'sp2r-constraints': {
        'input_params': ['dimensions.D_BULK'],
        'output_params': ['dimensions.D_EFFECTIVE']
    },
    'racetrack-superpotential': {
        'input_params': ['gauge.M_GUT'],
        'output_params': ['pneuma.VEV']
    },
    'bekenstein-hawking': {
        'input_params': [],
        'output_params': []
    },
    'reduction-cascade': {
        'input_params': ['dimensions.D_BULK'],
        'output_params': ['dimensions.D_EFFECTIVE']
    },
    'hidden-variables': {
        'input_params': ['dimensions.D_SHARED_EXTRAS'],
        'output_params': []
    },
    'division-algebra': {
        'input_params': [],
        'output_params': []
    },
    'dirac-pneuma': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'so10-breaking': {
        'input_params': ['gauge.M_GUT'],
        'output_params': []
    },
    'doublet-triplet': {
        'input_params': ['gauge.M_GUT', 'pneuma.VEV'],
        'output_params': []
    },
    'ckm-elements': {
        'input_params': [],
        'output_params': []
    },
    'yukawa-instanton': {
        'input_params': ['gauge.M_GUT'],
        'output_params': []
    },
    'friedmann-constraint': {
        'input_params': ['dark_energy.w0', 'dark_energy.wa'],
        'output_params': []
    },
    'de-sitter-attractor': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'kms-condition': {
        'input_params': [],
        'output_params': []
    },
    'gw-dispersion': {
        'input_params': ['kk_spectrum.m1_TeV'],
        'output_params': []
    },
    'vacuum-minimization': {
        'input_params': ['pneuma.VEV', 'gauge.M_GUT'],
        'output_params': []
    },
    'pati-salam-chain': {
        'input_params': ['gauge.M_GUT'],
        'output_params': []
    },
    'higgs-potential': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'rg-running-couplings': {
        'input_params': ['gauge.ALPHA_GUT', 'gauge.M_GUT'],
        'output_params': []
    },
    'attractor-potential': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'effective-euler': {
        'input_params': ['topology.B2', 'topology.B3'],
        'output_params': ['topology.CHI_EFF']
    },
    'tcs-topology': {
        'input_params': [],
        'output_params': ['topology.B2', 'topology.B3']
    },
    'flux-quantization': {
        'input_params': ['topology.CHI_EFF'],
        'output_params': ['topology.n_flux']
    },
    'dark-energy-wa': {
        'input_params': ['dark_energy.w0'],
        'output_params': ['dark_energy.wa']
    },
    'higgs-vev': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'higgs-mass': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'top-quark-mass': {
        'input_params': ['pneuma.VEV'],
        'output_params': []
    },
    'seesaw-mechanism': {
        'input_params': ['gauge.M_GUT'],
        'output_params': ['neutrino.mass_spectrum']
    },
    'primordial-spinor-13d': {
        'input_params': ['dimensions.D_EFFECTIVE'],
        'output_params': []
    },
    'mirror-dm-ratio': {
        'input_params': [],
        'output_params': ['mirror_sector.dm_baryon_ratio']
    },
    'neutrino-mass-21': {
        'input_params': ['neutrino.seesaw'],
        'output_params': ['neutrino.mass_splittings']
    },
    'neutrino-mass-31': {
        'input_params': ['neutrino.seesaw'],
        'output_params': ['neutrino.mass_splittings']
    },
    'master-action-26d': {
        'input_params': [],
        'output_params': ['dimensions.D_BULK']
    },
    'virasoro-anomaly': {
        'input_params': ['dimensions.D_BULK'],
        'output_params': []
    },
    'pneuma-vev': {
        'input_params': [],
        'output_params': ['pneuma.VEV']
    },
    'effective-torsion': {
        'input_params': ['topology.CHI_EFF'],
        'output_params': []
    },
}


def add_params_to_formulas():
    """Add input_params and output_params to Formula definitions in config.py."""

    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    for formula_id, params in FORMULA_PARAMS.items():
        input_params = params['input_params']
        output_params = params['output_params']

        # Skip if both empty
        if not input_params and not output_params:
            continue

        # Find the formula definition
        # Look for id="formula-id" pattern
        pattern = rf'(id="{formula_id}",\n)'

        if pattern in content or re.search(pattern, content):
            # Build the param strings
            param_lines = []
            if input_params:
                param_lines.append(f'        input_params={input_params!r},')
            if output_params:
                param_lines.append(f'        output_params={output_params!r},')

            param_str = '\n'.join(param_lines) + '\n'

            # Check if already has input_params or output_params
            # Find the formula block and check
            formula_pattern = rf'id="{formula_id}".*?(?=\n\s+\w+\s*=\s*Formula\(|\nALL_FORMULAS|\Z)'
            formula_match = re.search(formula_pattern, content, re.DOTALL)

            if formula_match:
                formula_text = formula_match.group()
                if 'input_params=' not in formula_text and 'output_params=' not in formula_text:
                    # Add after id line
                    replacement = f'id="{formula_id}",\n{param_str}'
                    content = re.sub(rf'id="{formula_id}",\n', replacement, content)
                    changes += 1
                    print(f"  Added params to: {formula_id}")

    if changes > 0:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nUpdated {changes} formula definitions")
    else:
        print("\nNo changes needed")


if __name__ == '__main__':
    print("=" * 60)
    print("ADDING INPUT/OUTPUT PARAMS TO FORMULA DEFINITIONS")
    print("=" * 60)
    add_params_to_formulas()
