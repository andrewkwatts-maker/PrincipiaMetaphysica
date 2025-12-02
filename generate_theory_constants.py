#!/usr/bin/env python3
"""
Generate theory-constants.js from config.py
============================================

This script ensures single source of truth for all theoretical constants.
All values on the website are generated from config.py, eliminating magic numbers.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import config

def generate_javascript_constants():
    """
    Generate JavaScript constants file from config.py

    Returns:
        dict with all constants organized by category
    """

    constants = {
        # Meta information
        'meta': {
            'version': '6.5',
            'last_updated': '2025-12-03',
            'description': 'Principia Metaphysica - Single Source of Truth for all theoretical constants'
        },

        # Fundamental Dimensions
        'dimensions': {
            'D_bulk': config.FundamentalConstants.D_BULK,
            'D_after_sp2r': config.FundamentalConstants.D_AFTER_SP2R,
            'D_internal': config.FundamentalConstants.D_INTERNAL,
            'D_effective': config.FundamentalConstants.D_EFFECTIVE,
            'D_common': config.FundamentalConstants.D_COMMON,
            'D_shared_extras': config.FundamentalConstants.D_SHARED_EXTRAS,
            'D_observable_brane': config.FundamentalConstants.D_OBSERVABLE_BRANE,
            'D_shadow_brane': config.FundamentalConstants.D_SHADOW_BRANE,
            'n_branes': config.FundamentalConstants.N_BRANES,
            'n_shadow_branes': config.FundamentalConstants.N_SHADOW_BRANES
        },

        # G2 Topology
        'topology': {
            'b2': 4,  # h^{1,1} Hodge number
            'b3': 24,  # h^{2,1} Hodge number
            'chi_eff': config.FundamentalConstants.euler_characteristic_effective(),
            'nu': 24,  # Crowley-Nordenstram invariant
            'n_gen': config.FundamentalConstants.fermion_generations(),
            'h_11': config.FundamentalConstants.HODGE_H11,
            'h_21': config.FundamentalConstants.HODGE_H21,
            'h_31': config.FundamentalConstants.HODGE_H31
        },

        # Shared Dimensions Parameters
        'shared_dimensions': {
            'alpha_4': config.SharedDimensionsParameters.ALPHA_4,
            'alpha_5': config.SharedDimensionsParameters.ALPHA_5,
            'd_eff': config.SharedDimensionsParameters.D_EFF,
            'w0_prediction': config.SharedDimensionsParameters.W_0_PREDICTION,
            'R_shared_y': config.SharedDimensionsParameters.R_SHARED_Y,
            'R_shared_z': config.SharedDimensionsParameters.R_SHARED_Z,
            'M_KK_central': config.SharedDimensionsParameters.M_KK_CENTRAL
        },

        # Energy Scales
        'scales': {
            'M_Planck': config.PhenomenologyParameters.M_PLANCK,
            'M_star': config.PhenomenologyParameters.M_STAR,
            'M_GUT': config.GaugeUnificationParameters.M_GUT,
            'M_GUT_error': config.GaugeUnificationParameters.M_GUT_ERROR,
            'M_KK': config.V61Predictions.M_KK_CENTRAL
        },

        # Gauge Unification
        'gauge': {
            'M_GUT': config.GaugeUnificationParameters.M_GUT,
            'M_GUT_error': config.GaugeUnificationParameters.M_GUT_ERROR,
            'alpha_GUT': config.GaugeUnificationParameters.ALPHA_GUT,
            'alpha_GUT_inv': config.GaugeUnificationParameters.ALPHA_GUT_INV
        },

        # Proton Decay
        'proton_decay': {
            'tau_p': config.PhenomenologyParameters.TAU_PROTON,
            'tau_p_lower_68': config.PhenomenologyParameters.TAU_PROTON_LOWER_68,
            'tau_p_upper_68': config.PhenomenologyParameters.TAU_PROTON_UPPER_68,
            'tau_p_uncertainty_oom': config.PhenomenologyParameters.TAU_PROTON_UNCERTAINTY_OOM,
            'tau_p_super_k_bound': config.PhenomenologyParameters.TAU_PROTON_SUPER_K_BOUND
        },

        # Dark Energy
        'dark_energy': {
            'w0': config.SharedDimensionsParameters.W_0_PREDICTION,
            'w0_desi_dr2': config.PhenomenologyParameters.W0_DESI_DR2,
            'w0_desi_error': config.PhenomenologyParameters.W0_DESI_ERROR,
            'wa_evolution': config.PhenomenologyParameters.WA_EVOLUTION,
            'wa_error': config.PhenomenologyParameters.WA_ERROR,
            'wa_desi_significance': config.PhenomenologyParameters.WA_DESI_SIGNIFICANCE
        },

        # Neutrino Sector (PMNS Matrix)
        'neutrino': {
            'theta_23': config.NeutrinoParameters.THETA_23,
            'theta_23_error': config.NeutrinoParameters.THETA_23_ERROR,
            'theta_23_nufit': config.NeutrinoParameters.THETA_23_NUFIT,
            'theta_23_nufit_error': config.NeutrinoParameters.THETA_23_NUFIT_ERROR,

            'theta_12': config.NeutrinoParameters.THETA_12,
            'theta_12_error': config.NeutrinoParameters.THETA_12_ERROR,
            'theta_12_nufit': config.NeutrinoParameters.THETA_12_NUFIT,
            'theta_12_nufit_error': config.NeutrinoParameters.THETA_12_NUFIT_ERROR,

            'theta_13': config.NeutrinoParameters.THETA_13,
            'theta_13_error': config.NeutrinoParameters.THETA_13_ERROR,
            'theta_13_nufit': config.NeutrinoParameters.THETA_13_NUFIT,
            'theta_13_nufit_error': config.NeutrinoParameters.THETA_13_NUFIT_ERROR,

            'delta_cp': config.NeutrinoParameters.DELTA_CP,
            'delta_cp_error': config.NeutrinoParameters.DELTA_CP_ERROR,
            'delta_cp_nufit': config.NeutrinoParameters.DELTA_CP_NUFIT,
            'delta_cp_nufit_error': config.NeutrinoParameters.DELTA_CP_NUFIT_ERROR,

            'average_deviation_sigma': config.NeutrinoParameters.PMNS_AVERAGE_DEVIATION_SIGMA,
            'hierarchy_prediction': config.NeutrinoParameters.HIERARCHY_PREDICTION
        },

        # Cosmology
        'cosmology': {
            'Omega_lambda': config.PhenomenologyParameters.OMEGA_LAMBDA,
            'Omega_matter': config.PhenomenologyParameters.OMEGA_MATTER,
            'Omega_baryon': config.PhenomenologyParameters.OMEGA_BARYON,
            'H0': config.PhenomenologyParameters.H0,
            'alpha_T_canonical': config.ThermalTimeParameters.ALPHA_T_CANONICAL
        },

        # Thermal Time
        'thermal_time': {
            'alpha_T_canonical': config.ThermalTimeParameters.ALPHA_T_CANONICAL,
            'alpha_T_z0': config.ThermalTimeParameters.ALPHA_T_Z0,
            'alpha_T_z1': config.ThermalTimeParameters.ALPHA_T_Z1,
            'alpha_T_z2': config.ThermalTimeParameters.ALPHA_T_Z2,
            'alpha_T_high_z': config.ThermalTimeParameters.ALPHA_T_HIGH_Z
        },

        # Predictions (v6.1)
        'predictions': {
            'M_KK_central': config.V61Predictions.M_KK_CENTRAL,
            'M_KK_min': config.V61Predictions.M_KK_MIN,
            'M_KK_max': config.V61Predictions.M_KK_MAX,
            'Delta_N_eff_central': config.V61Predictions.DELTA_N_EFF_CENTRAL
        }
    }

    return constants

def write_javascript_file(constants, output_path='theory-constants.js'):
    """
    Write constants to JavaScript file

    Args:
        constants: dict of constants
        output_path: output file path
    """

    js_content = """/**
 * Principia Metaphysica - Theory Constants
 * =========================================
 *
 * AUTO-GENERATED from config.py - DO NOT EDIT MANUALLY
 *
 * Single source of truth for all theoretical constants used across the website.
 * Generated by: generate_theory_constants.py
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

const PM = """

    # Add the JSON data
    js_content += json.dumps(constants, indent=2)

    # Add export statement
    js_content += """;\n\n// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PM;
}
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Generated {output_path} with {len(constants)} categories")

    # Print summary
    total_constants = sum(len(v) if isinstance(v, dict) else 1 for v in constants.values())
    print(f"Total constants: {total_constants}")

    return output_path

def write_python_summary(constants, output_path='theory_constants_summary.txt'):
    """
    Write human-readable summary

    Args:
        constants: dict of constants
        output_path: output file path
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("PRINCIPIA METAPHYSICA - THEORY CONSTANTS SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write("Generated from config.py\n")
        f.write(f"Version: {constants['meta']['version']}\n")
        f.write(f"Last Updated: {constants['meta']['last_updated']}\n\n")

        for category, values in constants.items():
            if category == 'meta':
                continue

            f.write(f"\n{category.upper().replace('_', ' ')}\n")
            f.write("-" * 70 + "\n")

            if isinstance(values, dict):
                for key, value in values.items():
                    if isinstance(value, float):
                        f.write(f"  {key}: {value:.6e}\n")
                    else:
                        f.write(f"  {key}: {value}\n")
            else:
                f.write(f"  {values}\n")

    print(f"Generated {output_path}")

    return output_path

if __name__ == '__main__':
    print("=" * 70)
    print("GENERATING THEORY CONSTANTS FROM CONFIG.PY")
    print("=" * 70)

    # Generate constants
    constants = generate_javascript_constants()

    # Write JavaScript file
    js_file = write_javascript_file(constants)

    # Write summary
    summary_file = write_python_summary(constants)

    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nJavaScript constants: {js_file}")
    print(f"Summary file: {summary_file}")
    print("\nNext steps:")
    print("1. Include theory-constants.js in all HTML files")
    print("2. Replace magic numbers with PM.category.constant")
    print("3. Run validation to ensure consistency")
