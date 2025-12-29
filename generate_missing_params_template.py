#!/usr/bin/env python3
"""
Generate template JSON for missing parameters.
This helps quickly add the missing parameters to theory_output.json
"""

import json

# Missing parameters identified by validation
missing_params = {
    "topology.h11": {
        "value": None,  # To be filled
        "unit": "dimensionless",
        "description": "Hodge number h^{1,1} - number of Kahler moduli",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.h21": {
        "value": None,
        "unit": "dimensionless",
        "description": "Hodge number h^{2,1} - number of complex structure moduli",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.h31": {
        "value": None,
        "unit": "dimensionless",
        "description": "Hodge number h^{3,1}",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.D_eff": {
        "value": None,
        "unit": "dimensionless",
        "description": "Effective spacetime dimension",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.M_KK": {
        "value": None,
        "unit": "GeV",
        "description": "Kaluza-Klein mass scale",
        "status": "DERIVED",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": ["topology.R_compactification"]
    },
    "topology.R_compactification": {
        "value": None,
        "unit": "meters",
        "description": "Compactification radius",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.cycle_separation": {
        "value": None,
        "unit": "dimensionless",
        "description": "Geometric separation between cycles",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.cycle_separations": {
        "values": None,
        "unit": "dimensionless",
        "description": "Array of cycle separations for different generations",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": None,
        "derivedFrom": []
    },
    "topology.HODGE_H11": {
        "value": None,
        "unit": "dimensionless",
        "description": "Hodge number H^{1,1} (uppercase variant)",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": "topology-constraint",
        "derivedFrom": []
    },
    "topology.HODGE_H31": {
        "value": None,
        "unit": "dimensionless",
        "description": "Hodge number H^{3,1} (uppercase variant)",
        "status": "GEOMETRIC",
        "classification": "GEOMETRIC",
        "formulaRef": "topology-constraint",
        "derivedFrom": []
    },
    "neutrino.m1": {
        "value": None,
        "unit": "eV",
        "description": "Neutrino mass eigenstate 1",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "neutrino-mass-spectrum",
        "derivedFrom": ["nufit.delta_m21_sq", "nufit.delta_m31_sq"]
    },
    "neutrino.m2": {
        "value": None,
        "unit": "eV",
        "description": "Neutrino mass eigenstate 2",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "neutrino-mass-spectrum",
        "derivedFrom": ["nufit.delta_m21_sq", "nufit.delta_m31_sq"]
    },
    "neutrino.m3": {
        "value": None,
        "unit": "eV",
        "description": "Neutrino mass eigenstate 3",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "neutrino-mass-spectrum",
        "derivedFrom": ["nufit.delta_m21_sq", "nufit.delta_m31_sq"]
    },
    "neutrino.theta_12": {
        "value": None,
        "unit": "radians",
        "description": "Neutrino mixing angle theta_12 (derived from geometric theory)",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "tribimaximal-mixing-derivation",
        "derivedFrom": ["topology.cycle_separations"]
    },
    "neutrino.theta_13": {
        "value": None,
        "unit": "radians",
        "description": "Neutrino mixing angle theta_13 (derived from geometric theory)",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "tribimaximal-mixing-derivation",
        "derivedFrom": ["topology.cycle_separations"]
    },
    "neutrino.theta_23": {
        "value": None,
        "unit": "radians",
        "description": "Neutrino mixing angle theta_23 (derived from geometric theory)",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "tribimaximal-mixing-derivation",
        "derivedFrom": ["topology.cycle_separations"]
    },
    "fermions.yukawa_top_GUT": {
        "value": None,
        "unit": "dimensionless",
        "description": "Top quark Yukawa coupling at GUT scale",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "yukawa-rg-equation",
        "derivedFrom": ["pdg.yukawa_top", "gauge.g_gut"]
    },
    "fermions.m_top_MSbar": {
        "value": None,
        "unit": "GeV",
        "description": "Top quark mass in MSbar scheme",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "mass-running-equation",
        "derivedFrom": ["pdg.m_top_pole"]
    },
    "fermions.yukawa_hierarchy": {
        "value": None,
        "unit": "dimensionless",
        "description": "Yukawa coupling hierarchy pattern",
        "status": "DERIVED",
        "classification": "GEOMETRIC",
        "formulaRef": "yukawa-hierarchy-derivation",
        "derivedFrom": ["topology.cycle_separations"]
    },
    "fermions.proton_mass": {
        "value": 0.938272088,
        "unit": "GeV",
        "description": "Proton mass (PDG value)",
        "status": "ESTABLISHED",
        "classification": "ESTABLISHED",
        "formulaRef": None,
        "derivedFrom": []
    },
    "proton_decay.d_over_R": {
        "value": None,
        "unit": "dimensionless",
        "description": "Ratio of cycle separation to compactification radius",
        "status": "DERIVED",
        "classification": "GEOMETRIC",
        "formulaRef": "cycle-separation-suppression",
        "derivedFrom": ["topology.cycle_separation", "topology.R_compactification"]
    },
    "proton_decay.gamma_p": {
        "value": None,
        "unit": "1/s",
        "description": "Proton decay rate",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "proton-decay-rate",
        "derivedFrom": ["mass_scales.M_GUT", "gauge.alpha_GUT"]
    },
    "proton_decay.geometric_suppression": {
        "value": None,
        "unit": "dimensionless",
        "description": "Geometric suppression factor for proton decay",
        "status": "DERIVED",
        "classification": "GEOMETRIC",
        "formulaRef": "geometric-suppression-factor",
        "derivedFrom": ["topology.cycle_separation"]
    },
    "pdg.yukawa_top": {
        "value": None,
        "unit": "dimensionless",
        "description": "Top quark Yukawa coupling at electroweak scale",
        "status": "ESTABLISHED",
        "classification": "ESTABLISHED",
        "formulaRef": None,
        "derivedFrom": []
    },
    "pdg.m_top_pole": {
        "value": 172.69,
        "unit": "GeV",
        "description": "Top quark pole mass (PDG 2024)",
        "status": "ESTABLISHED",
        "classification": "ESTABLISHED",
        "formulaRef": None,
        "derivedFrom": []
    },
    "pdg.higgs_quartic": {
        "value": None,
        "unit": "dimensionless",
        "description": "Higgs quartic coupling lambda",
        "status": "ESTABLISHED",
        "classification": "ESTABLISHED",
        "formulaRef": None,
        "derivedFrom": []
    },
    "higgs.dt_splitting_ratio": {
        "value": None,
        "unit": "dimensionless",
        "description": "Doublet-triplet splitting ratio",
        "status": "DERIVED",
        "classification": "GEOMETRIC",
        "formulaRef": "doublet-triplet-splitting",
        "derivedFrom": ["topology.cycle_separation"]
    },
    "higgs.m_h": {
        "value": None,
        "unit": "GeV",
        "description": "Higgs boson mass (derived from theory)",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "higgs-mass-derivation",
        "derivedFrom": ["topology.M_KK", "pdg.higgs_quartic"]
    },
    "gauge.alpha_GUT": {
        "value": None,
        "unit": "dimensionless",
        "description": "Unified gauge coupling at GUT scale",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": None,
        "derivedFrom": ["gauge.g_gut"]
    },
    "mass_scales.M_GUT": {
        "value": None,
        "unit": "GeV",
        "description": "Grand Unified Theory scale",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": None,
        "derivedFrom": ["gauge.g_gut"]
    },
    "methods.n_kk_modes": {
        "value": None,
        "unit": "dimensionless",
        "description": "Number of Kaluza-Klein modes included in calculation",
        "status": "DERIVED",
        "classification": "DERIVED",
        "formulaRef": "kk-threshold-correction",
        "derivedFrom": ["topology.M_KK"]
    }
}

def main():
    print("=" * 80)
    print("MISSING PARAMETERS TEMPLATE")
    print("=" * 80)
    print()
    print("The following JSON can be added to theory_output.json parameters section:")
    print()
    print(json.dumps(missing_params, indent=2))
    print()
    print("=" * 80)
    print(f"Total missing parameters: {len(missing_params)}")
    print("=" * 80)
    print()
    print("Note: Values marked as None need to be calculated or filled in.")
    print("Parameters with 'value' field should have scalar values.")
    print("Parameters with 'values' field should have array values.")

if __name__ == '__main__':
    main()
