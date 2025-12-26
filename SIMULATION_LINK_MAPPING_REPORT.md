# Simulation File Link Mapping Report
## Principia Metaphysica Formula → Simulation Mapping

**Date**: December 25, 2025
**Analysis**: Complete formula-to-simulation mapping for config.py

---

## Executive Summary

- **Total Formulas**: 55 (estimated from CoreFormulas class)
- **Formulas with simulation_file**: 19 (35%)
- **Formulas missing simulation_file**: 36 (65%)
- **Available simulation files**: 82+

**Task**: Map the 36 formulas missing simulation_file to appropriate simulation files

---

## Current Formula Simulation Links (Already Assigned)

### 1. **GENERATION_NUMBER** → `simulations/fermion_chirality_generations_v13_0.py`
   - ID: generation-number
   - Label: (2.6) Three Generations

### 2. **MASTER_ACTION_26D** → `simulations/attractor_scalar_v12_8.py`
   - ID: master-action-26d
   - Label: (2.1) Master Action

### 3. **RACETRACK_SUPERPOTENTIAL** → `simulations/pneuma_full_potential_v14_1.py`
   - ID: racetrack-superpotential
   - Label: (2.4) Racetrack Superpotential

### 4. **PNEUMA_VEV** (first instance) → `simulations/pneuma_full_potential_v14_1.py`
   - ID: pneuma-vev
   - Label: (2.4b) Pneuma VEV

### 5. **TCS_TOPOLOGY** → `simulations/g2_landscape_scanner_v14_1.py`
   - ID: tcs-topology
   - Label: (3.5) TCS G₂ Topology

### 6. **GUT_COUPLING** → `simulations/gauge_coupling_running_v14_3.py`
   - ID: gut-coupling
   - Label: (5.1) GUT Coupling

### 7. **WEAK_MIXING_ANGLE** → `simulations/gauge_coupling_running_v14_3.py`
   - ID: weak-mixing-angle
   - Label: (6.4) Weak Mixing Angle

### 8. **STRONG_COUPLING** → `simulations/gauge_coupling_running_v14_3.py`
   - ID: strong-coupling
   - Label: (6.7) Strong Coupling

### 9. **NEUTRINO_MASS_21** → `simulations/pmns_full_matrix.py`
   - ID: neutrino-mass-21
   - Label: (6.2) Solar Mass Splitting

### 10. **NEUTRINO_MASS_31** → `simulations/pmns_full_matrix.py`
   - ID: neutrino-mass-31
   - Label: (6.3) Atmospheric Mass Splitting

### 11. **CP_PHASE_GEOMETRIC** → `simulations/pmns_theta13_delta_geometric_v14_1.py`
   - ID: cp-phase-geometric
   - Label: (6.8) CP Phase

### 12. **DARK_ENERGY_WA** → `simulations/thermal_time_cosmology_v13_8.py`
   - ID: dark-energy-wa
   - Label: (7.4) Dark Energy Evolution

### 13. **THERMAL_TIME** → `simulations/thermal_time_cosmology_v13_8.py`
   - ID: thermal-time
   - Label: (7.7) Thermal Time

### 14. **GW_DISPERSION** → `simulations/gw_dispersion_v14_2.py`
   - ID: gw-dispersion
   - Label: (I.1) GW Dispersion Relation

### 15. **PROTON_BRANCHING** → `simulations/proton_decay_geometric_v13_0.py`
   - ID: proton-branching
   - Label: (H.1) Proton Decay Branching

### 16. **ATTRACTOR_POTENTIAL** → `simulations/attractor_scalar_v12_8.py`
   - ID: attractor-potential
   - Label: (7.6) Attractor Potential

### 17. **DIRAC_PNEUMA** → `simulations/clifford_algebra_spinor_v14_0.py`
   - ID: dirac-pneuma
   - Label: (3.1) Pneuma Dirac Equation

### 18. **VACUUM_MINIMIZATION** → `simulations/pneuma_full_potential_v14_1.py`
   - ID: vacuum-minimization
   - Label: (2.8) Vacuum Minimization Condition

### 19. **RG_RUNNING_COUPLINGS** → `simulations/gauge_coupling_running_v14_3.py`
   - ID: rg-running-couplings
   - Label: (6.9) RG Running Couplings

---

## Formulas Missing Simulation Links - Proposed Mappings

### COSMOLOGY FORMULAS

#### 1. **DARK_ENERGY_W0** → `simulations/wz_evolution_desi_dr2.py`
   - ID: dark-energy-w0
   - Label: (7.1) Dark Energy EoS
   - **Justification**: wz_evolution_desi_dr2.py validates DESI DR2 dark energy predictions

#### 2. **EFFECTIVE_DIMENSION** → `simulations/derive_d_eff_v12_8.py`
   - ID: effective-dimension
   - Label: (7.1) Effective Dimension
   - **Justification**: derive_d_eff_v12_8.py explicitly derives d_eff

#### 3. **GW_DISPERSION_COEFF** → `simulations/gw_dispersion_v12_8.py`
   - ID: gw-dispersion-coeff
   - Label: (I.2) GW Dispersion Coefficient
   - **Justification**: Companion to GW_DISPERSION, same physics

#### 4. **GW_DISPERSION_ALT** → `simulations/gw_dispersion_v12_8.py`
   - ID: gw-dispersion-alt
   - Label: (I.4) GW Dispersion (Alternative)
   - **Justification**: Alternative derivation of GW dispersion

#### 5. **DE_SITTER_ATTRACTOR** → `simulations/attractor_scalar_v12_8.py`
   - ID: de-sitter-attractor
   - Label: (7.10) de Sitter Attractor
   - **Justification**: Already linked to attractor_scalar_v12_8.py

#### 6. **FRIEDMANN_CONSTRAINT** → `simulations/wz_evolution_desi_dr2.py`
   - ID: friedmann-constraint
   - Label: (7.9) Friedmann Constraint
   - **Justification**: Cosmological evolution validation

### GAUGE/GUT FORMULAS

#### 7. **GUT_SCALE** → `simulations/gauge_unification_precision_v12_4.py`
   - ID: gut-scale
   - Label: (4.2) GUT Scale
   - **Justification**: gauge_unification_precision_v12_4.py validates M_GUT

#### 8. **SO10_BREAKING** → `simulations/breaking_chain_geometric_v14_1.py`
   - ID: so10-breaking
   - Label: (5.2) SO(10) Breaking
   - **Justification**: breaking_chain_geometric validates SO(10) → Pati-Salam chain

#### 9. **PATI_SALAM_CHAIN** → `simulations/breaking_chain_geometric_v14_1.py`
   - ID: pati-salam-chain
   - Label: (5.7) Pati-Salam Breaking Chain
   - **Justification**: Geometric derivation of Pati-Salam intermediate scale

#### 10. **KAPPA_GUT_COEFFICIENT** → `simulations/gauge_unification_precision_v12_4.py`
   - ID: kappa-gut-coefficient
   - Label: (E.4) GUT Scale Coefficient
   - **Justification**: GUT scale coefficient from G₂ volume

### PROTON DECAY FORMULAS

#### 11. **PROTON_LIFETIME** → `simulations/proton_decay_geometric_v13_0.py`
   - ID: proton-lifetime
   - Label: (5.3) Proton Lifetime
   - **Justification**: Core proton decay prediction

#### 12. **DOUBLET_TRIPLET** → `simulations/doublet_triplet_splitting_v14_0.py`
   - ID: doublet-triplet
   - Label: (5.4c) Doublet-Triplet Splitting
   - **Justification**: doublet_triplet_splitting validates index theorem mechanism

### NEUTRINO/MIXING FORMULAS

#### 13. **THETA23_MAXIMAL** → `simulations/derive_theta23_g2_v12_8.py`
   - ID: theta23-maximal
   - Label: (6.1) Atmospheric Mixing
   - **Justification**: derive_theta23_g2_v12_8.py validates θ₂₃ = 45°

#### 14. **CKM_ELEMENTS** → `simulations/ckm_cp_rigor.py`
   - ID: ckm-elements
   - Label: (6.10) CKM Matrix Elements
   - **Justification**: ckm_cp_rigor.py derives CKM elements from G₂

#### 15. **SEESAW_MECHANISM** → `simulations/neutrino_mass_matrix_final_v12_7.py`
   - ID: seesaw-mechanism
   - Label: (6.10) Type-I Seesaw
   - **Justification**: Underlying mechanism for neutrino masses

### YUKAWA/HIGGS FORMULAS

#### 16. **HIGGS_VEV** → `simulations/derive_vev_pneuma.py`
   - ID: higgs-vev
   - Label: (6.5) Higgs VEV
   - **Justification**: derive_vev_pneuma.py derives Higgs VEV from Pneuma

#### 17. **TOP_QUARK_MASS** → `simulations/higgs_yukawa_rg_v12_4.py`
   - ID: top-quark-mass
   - Label: (6.6) Top Quark Mass
   - **Justification**: Yukawa coupling RG flow

#### 18. **BOTTOM_QUARK_MASS** → `simulations/higgs_yukawa_rg_v12_4.py`
   - ID: bottom-quark-mass
   - Label: Bottom Quark Mass
   - **Justification**: Yukawa RG evolution

#### 19. **TAU_LEPTON_MASS** → `simulations/higgs_yukawa_rg_v12_4.py`
   - ID: tau-lepton-mass
   - Label: Tau Lepton Mass
   - **Justification**: Third generation Yukawa

#### 20. **YUKAWA_INSTANTON** → `simulations/g2_yukawa_overlap_integrals_v15_0.py`
   - ID: yukawa-instanton
   - Label: (6.11) Yukawa Instanton Suppression
   - **Justification**: g2_yukawa_overlap_integrals validates instanton action

#### 21. **HIGGS_MASS** → `simulations/higgs_mass_v12_4_moduli_stabilization.py`
   - ID: higgs-mass
   - Label: Higgs Mass
   - **Justification**: Phenomenological input but has moduli stabilization context

#### 22. **HIGGS_POTENTIAL** → `simulations/pneuma_full_potential_v14_1.py`
   - ID: higgs-potential
   - Label: Higgs Potential
   - **Justification**: F-term potential structure

#### 23. **HIGGS_QUARTIC** → `simulations/higgs_yukawa_rg_v12_4.py`
   - ID: higgs-quartic
   - Label: Higgs Quartic Coupling
   - **Justification**: RG running of quartic

### KK/COMPACTIFICATION FORMULAS

#### 24. **KK_GRAVITON** → `simulations/kk_spectrum_full.py`
   - ID: kk-graviton-mass
   - Label: (8.1) KK Graviton Mass
   - **Justification**: kk_spectrum_full.py computes full KK tower

### GEOMETRIC/TOPOLOGY FORMULAS

#### 25. **VIRASORO_ANOMALY** → `simulations/virasoro_anomaly_v12_8.py`
   - ID: virasoro-anomaly
   - Label: (2.2) Virasoro Anomaly Cancellation
   - **Justification**: virasoro_anomaly_v12_8.py validates anomaly cancellation

#### 26. **SP2R_CONSTRAINTS** → `simulations/sp2r_gauge_fixing_validation_v13_0.py`
   - ID: sp2r-constraints
   - Label: (2.3) Sp(2,R) Constraints
   - **Justification**: sp2r_gauge_fixing validates Sp(2,R) gauge fixing

#### 27. **REDUCTION_CASCADE** → `simulations/dim_decomp_v12_8.py`
   - ID: reduction-cascade
   - Label: (3.2) Dimensional Reduction
   - **Justification**: dim_decomp validates 26→13→11→7→4 cascade

#### 28. **PRIMORDIAL_SPINOR_13D** → `simulations/g2_spinor_geometry_validation_v13_0.py`
   - ID: primordial-spinor-13d
   - Label: (3.3) Primordial Spinor
   - **Justification**: Validates G₂ spinor geometry

#### 29. **EFFECTIVE_EULER** → `simulations/g2_landscape_scanner_v14_1.py`
   - ID: effective-euler
   - Label: (3.6a) Effective Euler Characteristic
   - **Justification**: Already validates TCS topology including χ_eff

#### 30. **FLUX_QUANTIZATION** → `simulations/flux_stabilization_full_v12_7.py`
   - ID: flux-quantization
   - Label: (3.6b) Flux Quantization
   - **Justification**: flux_stabilization validates flux quantization

#### 31. **EFFECTIVE_TORSION** → `simulations/torsion_effective_v12_8.py`
   - ID: effective-torsion
   - Label: (3.6c) Effective Torsion
   - **Justification**: torsion_effective_v12_8.py derives T_ω = -1.0

#### 32. **EFFECTIVE_TORSION_SPINOR** → `simulations/torsion_spinor_fraction_v12_8.py`
   - ID: effective-torsion-spinor
   - Label: (G.3) Torsion Spinor Correction
   - **Justification**: torsion_spinor_fraction validates 7/8 spinor correction

#### 33. **GHOST_COEFFICIENT** → `simulations/virasoro_anomaly_v12_8.py`
   - ID: ghost-coefficient
   - Label: (D.1) Ghost Coefficient
   - **Justification**: Ghost contribution from Virasoro structure

### MIRROR SECTOR FORMULAS

#### 34. **MIRROR_DM_RATIO** → `simulations/mirror_dark_matter_abundance_v15_3.py`
   - ID: mirror-dm-ratio
   - Label: Mirror Dark Matter Ratio
   - **Justification**: mirror_dark_matter_abundance validates mirror sector

#### 35. **MIRROR_TEMP_RATIO** → `simulations/mirror_dark_matter_abundance_v15_3.py`
   - ID: mirror-temp-ratio
   - Label: Mirror Temperature Ratio
   - **Justification**: Mirror sector temperature evolution

### MODULI/PLANCK FORMULAS

#### 36. **PLANCK_MASS_DERIVATION** → `simulations/gauge_unification_precision_v12_4.py`
   - ID: planck-mass-derivation
   - Label: (4.5) Planck Mass from Volume
   - **Justification**: M_Pl from dimensional reduction

### THEORETICAL FRAMEWORK FORMULAS (May not need simulation)

These formulas are ESTABLISHED physics or THEORY category and may not require simulation validation:

- **BEKENSTEIN_HAWKING**: Established physics
- **SCALAR_POTENTIAL**: Theoretical framework
- **HIDDEN_VARIABLES**: Theoretical framework
- **HIERARCHY_RATIO**: Derived ratio
- **DIVISION_ALGEBRA**: Pure mathematics
- **TOMITA_TAKESAKI**: Established theorem
- **KMS_CONDITION**: Established physics

---

## Summary of Proposed Additions

### New simulation_file assignments needed:

1. DARK_ENERGY_W0 → wz_evolution_desi_dr2.py
2. EFFECTIVE_DIMENSION → derive_d_eff_v12_8.py
3. GW_DISPERSION_COEFF → gw_dispersion_v12_8.py
4. GW_DISPERSION_ALT → gw_dispersion_v12_8.py
5. DE_SITTER_ATTRACTOR → attractor_scalar_v12_8.py
6. FRIEDMANN_CONSTRAINT → wz_evolution_desi_dr2.py
7. GUT_SCALE → gauge_unification_precision_v12_4.py
8. SO10_BREAKING → breaking_chain_geometric_v14_1.py
9. PATI_SALAM_CHAIN → breaking_chain_geometric_v14_1.py
10. KAPPA_GUT_COEFFICIENT → gauge_unification_precision_v12_4.py
11. PROTON_LIFETIME → proton_decay_geometric_v13_0.py
12. DOUBLET_TRIPLET → doublet_triplet_splitting_v14_0.py
13. THETA23_MAXIMAL → derive_theta23_g2_v12_8.py
14. CKM_ELEMENTS → ckm_cp_rigor.py
15. SEESAW_MECHANISM → neutrino_mass_matrix_final_v12_7.py
16. HIGGS_VEV → derive_vev_pneuma.py
17. TOP_QUARK_MASS → higgs_yukawa_rg_v12_4.py
18. BOTTOM_QUARK_MASS → higgs_yukawa_rg_v12_4.py
19. TAU_LEPTON_MASS → higgs_yukawa_rg_v12_4.py
20. YUKAWA_INSTANTON → g2_yukawa_overlap_integrals_v15_0.py
21. HIGGS_MASS → higgs_mass_v12_4_moduli_stabilization.py
22. HIGGS_POTENTIAL → pneuma_full_potential_v14_1.py
23. HIGGS_QUARTIC → higgs_yukawa_rg_v12_4.py
24. KK_GRAVITON → kk_spectrum_full.py
25. VIRASORO_ANOMALY → virasoro_anomaly_v12_8.py
26. SP2R_CONSTRAINTS → sp2r_gauge_fixing_validation_v13_0.py
27. REDUCTION_CASCADE → dim_decomp_v12_8.py
28. PRIMORDIAL_SPINOR_13D → g2_spinor_geometry_validation_v13_0.py
29. EFFECTIVE_EULER → g2_landscape_scanner_v14_1.py
30. FLUX_QUANTIZATION → flux_stabilization_full_v12_7.py
31. EFFECTIVE_TORSION → torsion_effective_v12_8.py
32. EFFECTIVE_TORSION_SPINOR → torsion_spinor_fraction_v12_8.py
33. GHOST_COEFFICIENT → virasoro_anomaly_v12_8.py
34. MIRROR_DM_RATIO → mirror_dark_matter_abundance_v15_3.py
35. MIRROR_TEMP_RATIO → mirror_dark_matter_abundance_v15_3.py
36. PLANCK_MASS_DERIVATION → gauge_unification_precision_v12_4.py

---

## Simulation Files Referenced

All simulation files are in `h:\Github\PrincipiaMetaphysica\simulations\` directory:

- attractor_scalar_v12_8.py
- breaking_chain_geometric_v14_1.py
- ckm_cp_rigor.py
- derive_d_eff_v12_8.py
- derive_theta23_g2_v12_8.py
- derive_vev_pneuma.py
- dim_decomp_v12_8.py
- doublet_triplet_splitting_v14_0.py
- fermion_chirality_generations_v13_0.py
- flux_stabilization_full_v12_7.py
- g2_landscape_scanner_v14_1.py
- g2_spinor_geometry_validation_v13_0.py
- g2_yukawa_overlap_integrals_v15_0.py
- gauge_coupling_running_v14_3.py
- gauge_unification_precision_v12_4.py
- gw_dispersion_v12_8.py
- higgs_mass_v12_4_moduli_stabilization.py
- higgs_yukawa_rg_v12_4.py
- kk_spectrum_full.py
- mirror_dark_matter_abundance_v15_3.py
- neutrino_mass_matrix_final_v12_7.py
- pmns_full_matrix.py
- pmns_theta13_delta_geometric_v14_1.py
- pneuma_full_potential_v14_1.py
- proton_decay_geometric_v13_0.py
- sp2r_gauge_fixing_validation_v13_0.py
- thermal_time_cosmology_v13_8.py (NOTE: This file may not exist - check for alternative)
- torsion_effective_v12_8.py
- torsion_spinor_fraction_v12_8.py
- virasoro_anomaly_v12_8.py
- wz_evolution_desi_dr2.py

---

## Next Steps

1. Verify each simulation file exists and validates the claimed formula
2. Add `simulation_file="simulations/[filename]"` to each formula in config.py
3. Re-run validation to confirm 100% simulation link completion
4. Update theory_output.json with new simulation links

---

**Report Generated**: December 25, 2025
**Author**: Claude Code Analysis
**Version**: 1.0
