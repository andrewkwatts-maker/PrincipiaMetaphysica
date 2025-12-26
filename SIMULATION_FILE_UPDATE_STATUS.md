# Simulation File Assignment Update Status

**Date**: December 25, 2025
**Task**: Add missing `simulation_file` assignments to 35 formulas in config.py

## Summary

Based on `SIMULATION_MAPPING_CORRECTIONS.txt`, 35 formulas are missing `simulation_file` assignments.

## Progress

### Completed (1/35)
- [x] DARK_ENERGY_W0 → `simulations/wz_evolution_desi_dr2.py`

### Remaining (34/35)

#### Cosmology (4)
- [ ] EFFECTIVE_DIMENSION → `simulations/derive_d_eff_v12_8.py`
- [ ] FRIEDMANN_CONSTRAINT → `simulations/wz_evolution_desi_dr2.py`
- [ ] DE_SITTER_ATTRACTOR → `simulations/attractor_scalar_v12_8.py`

#### Gauge/GUT (3)
- [ ] GUT_SCALE → `simulations/gauge_unification_precision_v12_4.py`
- [ ] KAPPA_GUT_COEFFICIENT → `simulations/gauge_unification_precision_v12_4.py`
- [ ] PLANCK_MASS_DERIVATION → `simulations/gauge_unification_precision_v12_4.py`

#### Proton Decay (2)
- [ ] PROTON_LIFETIME → `simulations/proton_decay_geometric_v13_0.py`
- [ ] DOUBLET_TRIPLET → `simulations/doublet_triplet_splitting_v14_0.py`

#### Neutrino (3)
- [ ] THETA23_MAXIMAL → `simulations/derive_theta23_g2_v12_8.py`
- [ ] SEESAW_MECHANISM → `simulations/neutrino_mass_matrix_final_v12_7.py`
- [ ] CKM_ELEMENTS → `simulations/ckm_cp_rigor.py`

#### Higgs/Yukawa (8)
- [ ] HIGGS_VEV → `simulations/derive_vev_pneuma.py`
- [ ] HIGGS_MASS → `simulations/higgs_mass_v12_4_moduli_stabilization.py`
- [ ] HIGGS_POTENTIAL → `simulations/pneuma_full_potential_v14_1.py`
- [ ] HIGGS_QUARTIC → `simulations/higgs_yukawa_rg_v12_4.py`
- [ ] TOP_QUARK_MASS → `simulations/higgs_yukawa_rg_v12_4.py`
- [ ] BOTTOM_QUARK_MASS → `simulations/higgs_yukawa_rg_v12_4.py`
- [ ] TAU_LEPTON_MASS → `simulations/higgs_yukawa_rg_v12_4.py`
- [ ] YUKAWA_INSTANTON → `simulations/g2_yukawa_overlap_integrals_v15_0.py`

#### Gravitational Waves (2)
- [ ] GW_DISPERSION_COEFF → `simulations/gw_dispersion_v12_8.py`
- [ ] GW_DISPERSION_ALT → `simulations/gw_dispersion_v12_8.py`

#### Geometric Framework (7)
- [ ] KK_GRAVITON → `simulations/kk_spectrum_full.py`
- [ ] VIRASORO_ANOMALY → `simulations/virasoro_anomaly_v12_8.py`
- [ ] SP2R_CONSTRAINTS → `simulations/sp2r_gauge_fixing_validation_v13_0.py`
- [ ] REDUCTION_CASCADE → `simulations/dim_decomp_v12_8.py`
- [ ] PRIMORDIAL_SPINOR_13D → `simulations/g2_spinor_geometry_validation_v13_0.py`
- [ ] EFFECTIVE_EULER → `simulations/g2_landscape_scanner_v14_1.py`
- [ ] FLUX_QUANTIZATION → `simulations/flux_stabilization_full_v12_7.py`

#### Torsion (2)
- [ ] EFFECTIVE_TORSION → `simulations/torsion_effective_v12_8.py`
- [ ] EFFECTIVE_TORSION_SPINOR → `simulations/torsion_spinor_fraction_v12_8.py`

#### Other (3)
- [ ] GHOST_COEFFICIENT → `simulations/virasoro_anomaly_v12_8.py`
- [ ] MIRROR_DM_RATIO → `simulations/mirror_dark_matter_abundance_v15_3.py`
- [ ] MIRROR_TEMP_RATIO → `simulations/mirror_dark_matter_abundance_v15_3.py`
- [ ] SO10_BREAKING → `simulations/breaking_chain_geometric_v14_1.py`
- [ ] PATI_SALAM_CHAIN → `simulations/breaking_chain_geometric_v14_1.py`

## Implementation Method

A Python script `add_simulation_files.py` has been created to automate the updates.

To complete the task, run:
```bash
python add_simulation_files.py
```

This will:
1. Read config.py
2. Find each formula definition
3. Add `simulation_file="path/to/simulation.py"` before the closing parenthesis
4. Write the updated config.py

## Verification

After running the script, verify with:
```bash
python -c "
import re
with open('config.py', 'r') as f:
    content = f.read()
count = len(re.findall(r'simulation_file=', content))
print(f'Total formulas with simulation_file: {count}')
print(f'Expected: 55 (19 existing + 35 new + 1 DARK_ENERGY_W0 manually added)')
"
```

Expected result: **55 formulas** with `simulation_file` assignments (100% coverage).
