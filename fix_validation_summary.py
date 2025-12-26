#!/usr/bin/env python3
"""
Fix validation_summary in theory_output.json
Converts from simplified array format to full object format with metadata
"""

import json
from pathlib import Path

# Load theory_output.json
theory_path = Path(__file__).parent / "theory_output.json"
with open(theory_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get current validation_summary and simulations
old_validation_summary = data.get('validation_summary', [])
simulations = data.get('simulations', {})

print(f"Current validation entries: {len(old_validation_summary)}")
print(f"Available simulations: {len(simulations)}")

# Create enhanced validation_summary
new_validation_summary = []

# Mapping from validation names to simulation keys and metadata
validation_mapping = {
    "Proton Decay": {
        "id": "proton_decay",
        "sim_key": "proton_decay",
        "bound_type": "lower"
    },
    "Neutrino Masses": {
        "id": "neutrino_masses",
        "sim_key": "neutrino_masses",
        "bound_type": "central"
    },
    "Higgs Mass": {
        "id": "higgs_mass",
        "sim_key": "higgs_mass",
        "bound_type": "central"
    },
    "KK Graviton": {
        "id": "kk_graviton",
        "sim_key": "kk_graviton",
        "bound_type": "lower"
    },
    "DT Splitting": {
        "id": "doublet_triplet",
        "sim_key": "doublet_triplet",
        "bound_type": "central"
    },
    "Breaking Chain": {
        "id": "breaking_chain",
        "sim_key": "breaking_chain",
        "bound_type": "central"
    },
    "Fermion Chirality": {
        "id": "fermion_chirality",
        "sim_key": "fermion_chirality",
        "bound_type": "central"
    },
    "Pneuma Stability": {
        "id": "pneuma_stability",
        "sim_key": "pneuma_stability",
        "bound_type": "check"
    },
    "Hebrew Physics": {
        "id": "hebrew_physics",
        "sim_key": "hebrew_physics",
        "bound_type": "check"
    },
    "KK Spectrum (v14.2)": {
        "id": "kk_spectrum_v14_2",
        "sim_key": "kk_spectrum_v14_2",
        "bound_type": "check"
    },
    "Yukawa Textures": {
        "id": "yukawa_textures",
        "sim_key": "yukawa_textures",
        "bound_type": "check"
    },
    "CP Phase": {
        "id": "cp_phase",
        "sim_key": "cp_phase",
        "bound_type": "central"
    },
    "G2 Ricci-Flatness": {
        "id": "g2_ricci",
        "sim_key": "g2_ricci",
        "bound_type": "check"
    },
    "Yukawa Overlaps": {
        "id": "yukawa_overlaps",
        "sim_key": "yukawa_overlaps",
        "bound_type": "check"
    },
    "Asymptotic Safety": {
        "id": "asymptotic_safety",
        "sim_key": "asymptotic_safety",
        "bound_type": "check"
    },
    "Moduli Racetrack (v15.0)": {
        "id": "moduli_racetrack_v15_0",
        "sim_key": "moduli_racetrack_v15_0",
        "bound_type": "check"
    },
    "G2 Metric+Perturbation (v15.0)": {
        "id": "g2_metric_pert_v15_0",
        "sim_key": "g2_metric_pert_v15_0",
        "bound_type": "check"
    },
    "Yukawa 7D MC (v15.0)": {
        "id": "yukawa_7d_mc_v15_0",
        "sim_key": "yukawa_7d_mc_v15_0",
        "bound_type": "check"
    },
    "Pneuma-Vielbein Bridge (v15.1)": {
        "id": "pneuma_vielbein_v15_1",
        "sim_key": "pneuma_vielbein_v15_1",
        "bound_type": "check"
    },
    "Multi-Sector Sampling (v16.0)": {
        "id": "multi_sector_v16_0",
        "sim_key": "multi_sector_v16_0",
        "bound_type": "check"
    },
    "Microtubule-PM Coupling (v15.2)": {
        "id": "microtubule_pm_v15_2",
        "sim_key": "microtubule_pm_v15_2",
        "bound_type": "check"
    },
    "Lattice Dispersion (v16.0)": {
        "id": "lattice_dispersion_v16_0",
        "sim_key": "lattice_dispersion_v16_0",
        "bound_type": "check"
    },
    "Evolutionary Orchestration (v16.1)": {
        "id": "evo_orch_v16_1",
        "sim_key": "evo_orch_v16_1",
        "bound_type": "check"
    },
    "Subleading Dispersion (v16.1)": {
        "id": "subleading_disp_v16_1",
        "sim_key": "subleading_disp_v16_1",
        "bound_type": "check"
    },
    "PMNS Geometric (v14.1)": {
        "id": "pmns_geometric_v14_1",
        "sim_key": "pmns_geometric_v14_1",
        "bound_type": "check"
    },
    "Pneuma Potential (v14.1)": {
        "id": "pneuma_potential_v14_1",
        "sim_key": "pneuma_potential_v14_1",
        "bound_type": "check"
    },
    "G2 Landscape (v14.1)": {
        "id": "g2_landscape_v14_1",
        "sim_key": "g2_landscape_v14_1",
        "bound_type": "check"
    },
    "Superpartner Bounds (v14.1)": {
        "id": "superpartner_v14_1",
        "sim_key": "superpartner_v14_1",
        "bound_type": "lower"
    },
    "LQG Timescale (v14.1)": {
        "id": "lqg_timescale_v14_1",
        "sim_key": "lqg_timescale_v14_1",
        "bound_type": "check"
    },
    "Mirror Dark Matter (v15.3)": {
        "id": "mirror_dm_v15_3",
        "sim_key": "mirror_dm_v15_3",
        "bound_type": "check"
    },
    "Landscape Selection (v15.4)": {
        "id": "landscape_sel_v15_4",
        "sim_key": "landscape_sel_v15_4",
        "bound_type": "check"
    },
    "Virasoro Anomaly (v12.8)": {
        "id": "virasoro_v12_8",
        "sim_key": "virasoro_v12_8",
        "bound_type": "check"
    },
    "Sp(2,R) Gauge Fixing (v13.0)": {
        "id": "sp2r_gauge_v13_0",
        "sim_key": "sp2r_gauge_v13_0",
        "bound_type": "check"
    },
    "Orientation Sum (v12.8)": {
        "id": "orientation_sum_v12_8",
        "sim_key": "orientation_sum_v12_8",
        "bound_type": "check"
    },
    "Zero Modes (v12.8)": {
        "id": "zero_modes_v12_8",
        "sim_key": "zero_modes_v12_8",
        "bound_type": "check"
    }
}

# Process each validation entry
for name, status in old_validation_summary:
    mapping = validation_mapping.get(name, {})
    sim_key = mapping.get('sim_key')

    # Get simulation data if available
    sim_data = simulations.get(sim_key, {}) if sim_key else {}

    # Build enhanced entry
    entry = {
        "id": mapping.get('id', name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('.', '_')),
        "name": name,
        "status": status
    }

    # Extract values from simulation data
    if sim_data:
        entry["computed"] = sim_data.get('computed')
        entry["experimental"] = sim_data.get('experimental')
        entry["bound_type"] = sim_data.get('bound_type', mapping.get('bound_type'))
        entry["sigma"] = sim_data.get('sigma')
        entry["ratio"] = sim_data.get('ratio')
        entry["units"] = sim_data.get('units')
        entry["source"] = sim_data.get('source')
        entry["notes"] = sim_data.get('notes')
    else:
        # No simulation data available
        entry["computed"] = None
        entry["experimental"] = None
        entry["bound_type"] = mapping.get('bound_type')
        entry["sigma"] = None
        entry["ratio"] = None
        entry["units"] = None
        entry["source"] = None
        entry["notes"] = "No simulation data available" if status == "ERROR" else None

    new_validation_summary.append(entry)

# Show some examples
print("\nExample entries:")
for i, entry in enumerate(new_validation_summary[:3]):
    print(f"\n{i+1}. {entry['name']}:")
    print(json.dumps(entry, indent=2))

print(f"\n\nTotal new entries: {len(new_validation_summary)}")

# Save to a temporary file first for review
output_path = Path(__file__).parent / "validation_summary_enhanced.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(new_validation_summary, f, indent=2)

print(f"\nEnhanced validation summary saved to: {output_path}")
print("\nReview this file before applying to theory_output.json")
