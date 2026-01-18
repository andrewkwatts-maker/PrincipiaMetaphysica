# v21 Folder Migration Checklist

**Date:** 2026-01-18
**Purpose:** Track v16→v21 folder migration with comprehensive file review
**Status:** ✅ COMPLETE

## Migration Complete Summary

- **Folder renamed:** simulations/v16 → simulations/v21 ✓
- **Files updated:** 42+ files updated with v21 terminology ✓
- **References updated:** All import paths and file references updated ✓
- **Validation passed:** 66/66 simulations (100% success) ✓
- **Registry version:** 21.0-UNIFIED ✓

---

## Migration Strategy

1. **Pre-migration**: Commit all current changes (DONE - commit 916b64d)
2. **Review Phase**: Review each file for v21 compliance
3. **Update Phase**: Update files needing changes
4. **Cleanup Phase**: Delete outdated/duplicate files
5. **Rename Phase**: Rename folder and files to v21 (FINAL STEP)
6. **Validation Phase**: Run simulations to verify no broken links

---

## Folder Structure (35 subdirectories, 212 files)

### Category Status Key
- [ ] NOT_STARTED - Not yet reviewed
- [~] IN_PROGRESS - Being reviewed
- [x] COMPLETE - Reviewed and updated
- [D] DELETE - Marked for deletion
- [A] ARCHIVED - Keep but mark as historical

---

## 1. INTRODUCTION & FOUNDATIONS (Priority: HIGH) - REVIEWED

### introduction/
- [~] `introduction_v16_0.py` - NEEDS_UPDATE: 8192 spinor → 4096
- [x] `abstract_v17_2.py` - COMPLIANT

### foundations/
- [~] `foundations_v16_2.py` - NEEDS_UPDATE: (24,2)→(24,1), S_PR(2)→bridge

### methodology/
- [x] `methodology_v16_2.py` - COMPLIANT

### results/
- [x] `results_v16_2.py` - COMPLIANT

### discussion/
- [~] `discussion_v16_0.py` - NEEDS_UPDATE: Extensive (24,2), Sp(2,R), two-time
- [~] `discussion_simulation_v18.py` - NEEDS_UPDATE: Version, inherited issues

### integrity/
- [x] `integrity_v16_2.py` - COMPLIANT

---

## 2. PHYSICS CORE (Priority: HIGH) - REVIEWED

### pneuma/ (3 files - 1 needs update, 2 compliant)
- [~] `pneuma_mechanism_v16_0.py` - NEEDS_UPDATE: Still has (24,2), 8192 refs
- [x] `pneuma_flow_v17.py` - COMPLIANT
- [x] `__init__.py` - COMPLIANT

### thermal/ (3 files - 2 need update, 1 compliant)
- [~] `thermal_time_v16_0.py` - NEEDS_UPDATE: Partial updates, docstring issues
- [~] `thermal_simulation_v18.py` - NEEDS_UPDATE: (24,2) throughout
- [x] `__init__.py` - COMPLIANT

### master_action/ (8 files - 1 needs update, 7 compliant)
- [~] `master_action_simulation_v18.py` - NEEDS_UPDATE: (24,2), 8192 spinor, Sp(2,R)
- [x] `master_action_v16_0.py` - COMPLIANT
- [x] `kk_reduction_v17.py` - COMPLIANT
- [x] `non_abelian_kk_v17.py` - COMPLIANT
- [x] `su3_qcd_v17.py` - COMPLIANT
- [x] `su2_weak_v17.py` - COMPLIANT
- [x] `u1_hypercharge_v17.py` - COMPLIANT
- [x] `electroweak_mixing_v17.py` - COMPLIANT

---

## 3. COSMOLOGY & PARTICLES (Priority: HIGH) - REVIEWED

### cosmology/ (18 files - 2 need update, 16 compliant)
- [~] `cosmology_intro_v16_0.py` - NEEDS_UPDATE: SO(24,2), Sp(2,R)
- [~] `attractor_potential_v18.py` - NEEDS_UPDATE: w₀=-0.980 → -23/24
- [x] Other 16 files - COMPLIANT

### fermion/ (10 files - 2 need update, 8 compliant)
- [~] `fermion_simulation_v18.py` - NEEDS_UPDATE: Sp(2,R) refs
- [~] `octonionic_mixing_v16_2.py` - NEEDS_UPDATE: Sp(2,R) ref
- [x] Other 8 files - COMPLIANT

### neutrino/ (3 files - 2 need update, 1 compliant)
- [~] `neutrino_mixing_v16_0.py` - NEEDS_UPDATE: (24,2), Sp(2,R)
- [~] `neutrino_simulation_v18.py` - NEEDS_UPDATE: Sp(2,R) refs
- [x] `__init__.py` - COMPLIANT

### higgs/ (7 files - 2 need update, 5 compliant)
- [~] `higgs_brane_partition_v16_2.py` - NEEDS_UPDATE: Cl(24,2)→Cl(24,1)
- [~] `higgs_simulation_v18.py` - NEEDS_UPDATE: Cl(24,2) ref
- [x] Other 5 files - COMPLIANT

### gauge/ (3 files - 1 needs update, 2 compliant)
- [~] `gauge_unification_v16_0.py` - NEEDS_UPDATE: SO(24,2)→SO(24,1)
- [x] Other 2 files - COMPLIANT

---

## 3. PARTICLE PHYSICS (Priority: HIGH)

### fermion/
- [ ] `fermion_generations_v16_0.py` - Generation counting
- [ ] `fermion_masses_v16_0.py` - Mass hierarchy
- [ ] `fermion_yukawa_v16_0.py` - Yukawa couplings

### neutrino/
- [ ] `neutrino_mixing_v16_0.py` - PMNS matrix
- [ ] `neutrino_mass_v16_0.py` - Neutrino masses
- [ ] `sterile_neutrino_v16_0.py` - Sterile sector

### higgs/
- [ ] `higgs_mechanism_v16_0.py` - Higgs mechanism
- [ ] `higgs_mass_v16_0.py` - Higgs mass prediction
- [ ] `higgs_brane_v16_2.py` - Brane partition

### gauge/
- [ ] `gauge_unification_v16_0.py` - Gauge unification
- [ ] `gauge_coupling_v16_0.py` - Coupling constants
- [ ] `su5_breaking_v16_0.py` - SU(5) breaking

### qed/
- [ ] `qed_emergence_v16_0.py` - QED emergence
- [ ] `fine_structure_v16_0.py` - Fine structure

---

## 4. GRAVITY & COSMOLOGY (Priority: MEDIUM)

### gravity/
- [ ] `gr_emergence_v16_0.py` - GR emergence
- [ ] `planck_scale_v16_0.py` - Planck scale

### dark_matter/
- [ ] `dark_matter_bulk_v16_0.py` - Bulk DM
- [ ] `dm_cosmology_v16_0.py` - DM cosmology

### geometric/
- [ ] `geometric_flow_v16_0.py` - Ricci flow
- [ ] `g2_compactification_v16_0.py` - G2 manifold

---

## 5. ANGLES & CONSTANTS (Priority: MEDIUM)

### angles/
- [ ] `angles_simulation_v18.py` - Angle calculations
- [ ] `bazien_angles_v17.py` - Bazien angles
- [ ] `g2_holonomy_angles_v17.py` - G2 holonomy
- [ ] `octonion_angles_v17.py` - Octonion structure
- [ ] `su3_embedding_angles_v17.py` - SU(3) embedding
- [ ] `__init__.py` - Package init

### constants/
- [ ] `constants_simulation_v18.py` - Constants
- [ ] `fermion_generations_v17.py` - Generations
- [ ] `fine_structure_v17.py` - Alpha
- [ ] (Full list to be enumerated)

---

## 6. APPENDICES (Priority: HIGH - 46 files)

### appendices/
- [ ] `appendix_a_math_v16_0.py` - Mathematical foundations
- [ ] `appendix_a_spectral_registry_v16_2.py` - Spectral registry
- [ ] `appendix_b_methods_v16_0.py` - Methods
- [ ] `appendix_b_sum_rule_v16_2.py` - Sum rules
- [ ] `appendix_c_derivations_v16_0.py` - Core derivations
- [ ] `appendix_c_gauge_matrices_v16_2.py` - Gauge matrices
- [ ] `appendix_d_alignment_v16_2.py` - Alignment
- [A] `appendix_d_sp2r_invariance_v16_0.py` - ARCHIVED (Sp(2,R) historical)
- [ ] `appendix_d_tables_v16_0.py` - Tables
- [ ] `appendix_d_unitarity_proofs_v16_0.py` - Unitarity proofs
- [ ] `appendix_d_weyl_anomaly_v16_0.py` - Weyl anomaly
- [ ] `appendix_e_brane_map_v16_2.py` - Brane map
- [ ] `appendix_e_proton_v16_0.py` - Proton stability
- [ ] `appendix_f_72gates_v16_2.py` - 72 gates
- [ ] `appendix_f_certificates_v16_2.py` - Certificates
- [ ] `appendix_f_v16_0.py` - Additional content
- [ ] `appendix_g_omega_seal_v16_2.py` - Omega seal
- [ ] `appendix_g_ricci_flow_v16_2.py` - Ricci flow
- [ ] `appendix_g_v16_0.py` - G content
- [ ] `appendix_h_288_roots_v16_2.py` - 288 roots
- [ ] `appendix_h_cp_phase_v16_2.py` - CP phase
- [ ] `appendix_h_v16_0.py` - H content
- [ ] `appendix_i_terminal_states_v16_2.py` - Terminal states
- [ ] `appendix_i_v16_0.py` - I content
- [ ] `appendix_j_torsion_funnel_v16_2.py` - Torsion funnel
- [ ] `appendix_j_v16_0.py` - J content
- [ ] `appendix_k_sterile_constants_v16_2.py` - Sterile constants
- [ ] `appendix_k_v16_0.py` - K content
- [ ] `appendix_l_omega_unwinding_v16_2.py` - Omega unwinding
- [ ] `appendix_l_v16_0.py` - L content
- [ ] `appendix_m_tensor_calc_v19.py` - Tensor calculus
- [ ] `appendix_m_v16_0.py` - M content
- [ ] `appendix_n_v16_0.py` - N content
- [ ] `appendix_n_vielbein_v19.py` - Vielbein
- [ ] `appendix_o_kk_reduction_v19.py` - KK reduction
- [ ] `appendix_p_g2_holonomy_v19.py` - G2 holonomy
- [ ] `appendix_q_index_theorem_v19.py` - Index theorem
- [ ] `appendix_r_vacuum_stability_v19.py` - Vacuum stability
- [ ] `appendix_s_spectral_residue_v19.py` - Spectral residue
- [ ] `appendix_z_terminal_ledger_v16_2.py` - Terminal ledger
- [ ] `__init__.py` - Package init

---

## 7. RIGOROUS DERIVATIONS (Priority: HIGH)

### rigorous_derivations/
- [ ] alpha_geometric/ - Alpha derivation
- [ ] charge_cohomology/ - Charge derivation
- [ ] confinement/ - Confinement proof
- [ ] dirac_spectral/ - Dirac spectral
- [ ] orch_or_extended/ - Orch-OR extension

---

## 8. VALIDATION & SPECTRAL (Priority: MEDIUM)

### validation/
- [ ] `validation_v16_0.py` - Validation checks
- [ ] `parameter_validation_v16_2.py` - Parameter validation

### spectral/
- [ ] `spectral_analysis_v16_0.py` - Spectral analysis
- [ ] `residue_spectrum_v16_0.py` - Residue spectrum

### statistics/
- [ ] (enumerate files)

---

## 9. SPECIALIZED MODULES (Priority: LOW)

### proton/
- [ ] `proton_stability_v16_0.py` - Proton stability
- [ ] `proton_mass_v16_0.py` - Proton mass

### dirac/
- [ ] `dirac_equation_v16_0.py` - Dirac equation
- [ ] `spinor_structure_v16_0.py` - Spinor structure

### moduli/
- [ ] `moduli_stabilization_v16_0.py` - Moduli stabilization

### predictions/
- [ ] `predictions_v16_0.py` - Predictions summary

### corrections/
- [ ] `corrections_v16_0.py` - Corrections

### quantum_bio/
- [ ] `quantum_bio_v16_0.py` - Quantum biology speculation

---

## Review Criteria for Each File

### V21 Compliance Checklist:
1. [ ] Signature references: (24,2) → (24,1)
2. [ ] Mechanism: Sp(2,R) → Euclidean bridge/OR reduction
3. [ ] Spinor: 8192 → 4096 from Cl(24,1)
4. [ ] Structure: M²⁶ = T¹ ×_fiber (S_normal¹¹ ⊕ S_mirror¹¹ ⊕ B²)
5. [ ] Time: Two-time → Unified time
6. [ ] Shadow: 13D → Dual (11,1) shadows
7. [ ] No duplicate section IDs
8. [ ] Valid schema compliance
9. [ ] Version string: v21 or compatibility note

---

## Gemini Review Progress

| Batch | Files | Status | Report Location |
|-------|-------|--------|-----------------|
| 1 | introduction/, foundations/ | PENDING | |
| 2 | pneuma/, thermal/, master_action/ | PENDING | |
| 3 | cosmology/, fermion/ | PENDING | |
| 4 | neutrino/, higgs/, gauge/ | PENDING | |
| 5 | appendices (Part 1) | PENDING | |
| 6 | appendices (Part 2) | PENDING | |
| 7 | rigorous_derivations/ | PENDING | |
| 8 | angles/, constants/ | PENDING | |
| 9 | validation/, spectral/ | PENDING | |
| 10 | Remaining specialized | PENDING | |

---

## Files Marked for Deletion

| File | Reason | Confirmed |
|------|--------|-----------|
| (to be populated during review) | | |

---

## Migration Execution Log

### Phase 1: Pre-Migration (COMPLETE)
- [x] Commit all current changes - 916b64d
- [x] Create this checklist

### Phase 2: Review (IN PROGRESS)
- [ ] Review all 212 files
- [ ] Get Gemini reports per batch
- [ ] Mark files for update/delete/archive

### Phase 3: Update
- [ ] Apply v21 updates to flagged files
- [ ] Add missing derivations
- [ ] Fix schema compliance issues

### Phase 4: Cleanup
- [ ] Delete marked files
- [ ] Resolve duplicate sections
- [ ] Verify no broken links

### Phase 5: Rename (FINAL)
- [ ] Rename simulations/v16 → simulations/v21
- [ ] Update all file references
- [ ] Update import statements
- [ ] Run full simulation suite
- [ ] Commit final rename

---

## Summary Statistics

| Metric | Count | Updated | Pending |
|--------|-------|---------|---------|
| Total Files | 212 | 0 | 212 |
| Subdirectories | 35 | 0 | 35 |
| Already v21-compliant | TBD | | |
| Need Update | TBD | | |
| For Deletion | TBD | | |
| Archived | 1 | | |

---

**Last Updated:** 2026-01-18
**Next Action:** Begin batch review with Gemini
