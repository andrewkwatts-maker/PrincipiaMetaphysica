# Simulations Metadata Audit Report
**Generated:** 2025-12-26
**Source:** theory_output.json

## Metadata Coverage Overview

| Field | Coverage | Count |
|-------|----------|-------|
| Status Field | 20% | 7/35 |
| Validation Object | 8% | 3/35 |
| Formula Reference | 5% | 2/35 |
| Mechanism Description | 28% | 10/35 |
| Source Reference | 25% | 9/35 |
| **Overall Completeness** | **17%** | **31/175 fields** |

**Key Finding:** Only 17% of expected metadata fields are populated. Zero simulations have complete metadata across all five categories.

## Executive Summary
- **Total Simulations:** 35
- **Missing Status:** 28
- **Missing Validation:** 32
- **Incomplete Validation:** 2
- **Missing Formula:** 33
- **Incomplete Formula:** 0
- **Missing Mechanism:** 25
- **Missing Source:** 26

## Available Metadata Keys
All keys found across simulations: A, B, D_critical, Re_T_modulus, T_stabilized, a, above_super_k, abundance_ratio_obs, abundance_ratio_pred, agreement_atm_pct, agreement_solar_pct, all_converged, all_valid, alpha_gut_inv, anomaly_free, b, b2, br_e_pi0, bulk_dim, c_total, cabibbo_agreement_pct, chain, chain_geometric, chi_eff, chi_eff_selected, chiral_filter_strength, ckm_elements, collapse_timescale_ms, comparison, d2V_dpsi2, d_over_r, delta_cp_deg, delta_m21_sq, delta_m3l_sq, derivation_chain, deviation_sigma, dim_reduction_correct, dirac_modification, doublet_index_per_gen, doublet_preservation, effective_coupling_Hz, effective_torsion, epsilon, epsilon_derivation, epsilon_derived, epsilon_dynamic, epsilon_source, error, fixed_point, formula, formula_chiral, formula_generations, formula_id, formula_potential, formula_validated, formula_vev, hessian_analytic, hessian_numerical, higgs_gut_break, higgs_ps_break, hl_lhc_discovery, holonomy_valid, holonomy_validation, index_formula, is_exact, is_stable, jarlskog, jarlskog_analysis, k_matching, lhc_consistent, m1_eV, m2_eV, m3_eV, m_KK_GeV, m_KK_TeV, m_ew, m_gut, m_h_GeV, m_ps, m_susy_min, mass_hierarchy, matches_observed, maximal_cp, mechanism, method, modulation_factor, n_flux, n_gen, n_gen_required, n_generations, n_generations_exact, n_samples, n_tubulins, oom_uncertainty, ordering, orientation_sum, overall_valid, perturbation_valid, pneuma_alignment, pneuma_vielbein, rg_flow, selection_probability, shadow_dim, signature_reduced, sm_rank, source, spin7_active, spin7_total, spinor_dof, squark_margin, stabilizer_group, status, sum_masses_eV, super_k_ratio, suppression_factor, target_GeV, target_TeV, tau_p_68_high, tau_p_68_low, tau_p_years, temp_ratio, timescale_valid, topology_supports_filter, total_doublets, triplet_index, triplet_suppression, uniquely_selected, v_min, validated, validation, version, vev_agreement_pct, vev_analytic, vev_numeric, vev_numerical, yukawa_couplings, z2_action, z2_filter_active

## Detailed Findings

### 1. Simulations Missing Status Field
**Count:** 28

- `neutrino_masses`
- `higgs_mass`
- `hebrew_physics`
- `kk_spectrum_v14_2`
- `yukawa_textures`
- `cp_phase`
- `g2_metric_ricci`
- `yukawa_overlap`
- `asymptotic_safety`
- `moduli_racetrack_v15`
- `g2_metric_v15`
- `yukawa_overlap_v15`
- `pneuma_bridge_v15_1`
- `multi_sector_v16_0`
- `lattice_dispersion_v16_0`
- `evolutionary_orchestration_v16_1`
- `subleading_dispersion_v16_1`
- `pmns_geometric_v14_1`
- `pneuma_potential_v14_1`
- `g2_landscape_v14_1`
- `superpartner_bounds_v14_1`
- `lqg_timescale_v14_1`
- `mirror_dm_v15_3`
- `landscape_selection_v15_4`
- `virasoro_v12_8`
- `sp2r_validation_v13_0`
- `orientation_sum_v12_8`
- `zero_modes_v12_8`

### 2. Simulations Missing Validation Object
**Count:** 32

- `kk_graviton`
- `doublet_triplet`
- `breaking_chain`
- `fermion_chirality`
- `pneuma_stability`
- `hebrew_physics`
- `kk_spectrum_v14_2`
- `yukawa_textures`
- `cp_phase`
- `g2_metric_ricci`
- `yukawa_overlap`
- `asymptotic_safety`
- `moduli_racetrack_v15`
- `g2_metric_v15`
- `yukawa_overlap_v15`
- `pneuma_bridge_v15_1`
- `multi_sector_v16_0`
- `microtubule_v15_2`
- `lattice_dispersion_v16_0`
- `evolutionary_orchestration_v16_1`
- `subleading_dispersion_v16_1`
- `pmns_geometric_v14_1`
- `pneuma_potential_v14_1`
- `g2_landscape_v14_1`
- `superpartner_bounds_v14_1`
- `lqg_timescale_v14_1`
- `mirror_dm_v15_3`
- `landscape_selection_v15_4`
- `virasoro_v12_8`
- `sp2r_validation_v13_0`
- `orientation_sum_v12_8`
- `zero_modes_v12_8`

### 3. Simulations with Incomplete Validation Data
**Count:** 2

Required fields: `computed`, `experimental`, `sigma`

#### `proton_decay`
```json
{
  "computed": 8.149598829720118e+34,
  "bound": 1.67e+34,
  "bound_type": "lower",
  "ratio": 4.879999299233603,
  "passed": "True",
  "units": "years",
  "status": "PASS (4.88x bound)"
}
```

#### `neutrino_masses`
```json
{
  "solar_splitting": {
    "computed": 7.96e-05,
    "experimental": 7.42e-05,
    "error": 2e-06,
    "deviation": 5.399999999999996e-06,
    "sigma": 2.699999999999998,
    "passed": true,
    "units": "eV^2",
    "status": "PASS (2.70 sigma)"
  },
  "atmospheric_splitting": {
    "computed": 0.002521,
    "experimental": 0.002515,
    "error": 2.8e-05,
    "deviation": 5.999999999999929e-06,
    "sigma": 0.21428571428571175,
    "passed": true,
    "units": "eV^2",
    "status": "PASS (0.21 sigma)"
  },
  "cosmological_sum": {
    "computed": 0.06,
    "bound": 0.072,
    "bound_type": "upper",
    "ratio": 1.2,
    "passed": true,
    "units": "eV",
    "status": "PASS (1.20x bound)"
  }
}
```

### 4. Simulations Missing Formula Reference
**Count:** 33

- `neutrino_masses`
- `higgs_mass`
- `doublet_triplet`
- `breaking_chain`
- `fermion_chirality`
- `pneuma_stability`
- `hebrew_physics`
- `kk_spectrum_v14_2`
- `yukawa_textures`
- `cp_phase`
- `g2_metric_ricci`
- `yukawa_overlap`
- `asymptotic_safety`
- `moduli_racetrack_v15`
- `g2_metric_v15`
- `yukawa_overlap_v15`
- `pneuma_bridge_v15_1`
- `multi_sector_v16_0`
- `microtubule_v15_2`
- `lattice_dispersion_v16_0`
- `evolutionary_orchestration_v16_1`
- `subleading_dispersion_v16_1`
- `pmns_geometric_v14_1`
- `pneuma_potential_v14_1`
- `g2_landscape_v14_1`
- `superpartner_bounds_v14_1`
- `lqg_timescale_v14_1`
- `mirror_dm_v15_3`
- `landscape_selection_v15_4`
- `virasoro_v12_8`
- `sp2r_validation_v13_0`
- `orientation_sum_v12_8`
- `zero_modes_v12_8`

### 5. Simulations with Incomplete Formula Data
✓ All simulations with formula have complete data

### 6. Simulations Missing Mechanism/Derivation Description
**Count:** 25

Looking for one of: `mechanism`, `derivation`, `description`

- `neutrino_masses`
- `kk_graviton`
- `pneuma_stability`
- `hebrew_physics`
- `kk_spectrum_v14_2`
- `yukawa_textures`
- `cp_phase`
- `g2_metric_ricci`
- `yukawa_overlap`
- `asymptotic_safety`
- `g2_metric_v15`
- `yukawa_overlap_v15`
- `pneuma_bridge_v15_1`
- `multi_sector_v16_0`
- `microtubule_v15_2`
- `lattice_dispersion_v16_0`
- `evolutionary_orchestration_v16_1`
- `subleading_dispersion_v16_1`
- `pmns_geometric_v14_1`
- `g2_landscape_v14_1`
- `lqg_timescale_v14_1`
- `virasoro_v12_8`
- `sp2r_validation_v13_0`
- `orientation_sum_v12_8`
- `zero_modes_v12_8`

### 7. Simulations Missing Source Reference
**Count:** 26

- `proton_decay`
- `kk_graviton`
- `doublet_triplet`
- `breaking_chain`
- `fermion_chirality`
- `pneuma_stability`
- `hebrew_physics`
- `kk_spectrum_v14_2`
- `yukawa_textures`
- `cp_phase`
- `g2_metric_ricci`
- `yukawa_overlap`
- `asymptotic_safety`
- `moduli_racetrack_v15`
- `g2_metric_v15`
- `yukawa_overlap_v15`
- `pneuma_bridge_v15_1`
- `microtubule_v15_2`
- `pneuma_potential_v14_1`
- `superpartner_bounds_v14_1`
- `mirror_dm_v15_3`
- `landscape_selection_v15_4`
- `virasoro_v12_8`
- `sp2r_validation_v13_0`
- `orientation_sum_v12_8`
- `zero_modes_v12_8`

## Recommendations

### HIGH Priority: Add status field to all simulations
Add `status` field (PASS/FAIL/CHECK) to 28 simulations

**Affected simulations:** 28 total (see detailed findings above)

### HIGH Priority: Add validation objects
Add validation data with computed, experimental, and sigma values to 32 simulations

**Affected simulations:** 32 total (see detailed findings above)

### HIGH Priority: Complete validation data
Ensure all validation objects have computed, experimental, and sigma fields for 2 simulations

**Affected simulations:**
- `proton_decay`
- `neutrino_masses`

### MEDIUM Priority: Add formula references
Link simulations to their corresponding formulas for 33 simulations

**Affected simulations:** 33 total (see detailed findings above)

### MEDIUM Priority: Add mechanism descriptions
Document the physical mechanism or derivation for 25 simulations

**Affected simulations:** 25 total (see detailed findings above)

### LOW Priority: Add source references
Add source references to Python simulation files for 26 simulations

**Affected simulations:** 26 total (see detailed findings above)

## Simulations with Complete Metadata

**Count:** 0 out of 35

*No simulations have complete metadata*

---

## Appendix: Examples and Best Practices

### Example: Best Current Metadata (proton_decay)

The `proton_decay` simulation has the most complete metadata structure:

```json
{
  "tau_p_years": 8.149598829720118e+34,
  "mechanism": "TCS cycle separation (K=4 neck topology)",
  "status": "RESOLVED - Geometric selection rule from TCS cycle separation",
  "formula": {
    "id": "proton-lifetime",
    "label": "(5.10) Proton Lifetime",
    "plain_text": "τ_p = M_GUT⁴/(α_GUT² m_p⁵) × S² = 8.15 × 10³⁴ years",
    "validated": "True"
  },
  "validation": {
    "computed": 8.149598829720118e+34,
    "bound": 1.67e+34,
    "bound_type": "lower",
    "ratio": 4.879999299233603,
    "passed": "True",
    "units": "years",
    "status": "PASS (4.88x bound)"
  }
}
```

**Missing:** Only lacks `experimental` and `sigma` fields in validation (uses bounds instead).

### Example: Simulation with Good Validation but Missing Other Fields (higgs_mass)

```json
{
  "m_h_GeV": 125.1,
  "source": "config.py HiggsMassParameters",
  "validation": {
    "computed": 125.1,
    "experimental": 125.2,
    "error": 0.11,
    "sigma": 0.9090909090909866,
    "status": "PASS (0.91 sigma)"
  },
  "mechanism": "Moduli stabilization with Re(T)=7.086"
}
```

**Missing:** `status` field and `formula` reference.

### Example: Minimal Metadata (hebrew_physics)

```json
{
  "error": "'charmap' codec can't encode character '\\u05d2'..."
}
```

**Issues:** Only contains an error message. No metadata at all.

### Recommended Metadata Template

Based on analysis of simulation Python files, here's the recommended structure:

```json
{
  "status": "PASS|FAIL|CHECK|RESOLVED|SPECULATIVE",

  "validation": {
    "computed": <number>,
    "experimental": <number>,
    "error": <number>,
    "sigma": <number>,
    "units": "<unit string>",
    "status": "PASS (X.XX sigma)"
  },

  "formula": {
    "id": "<formula-id>",
    "label": "(<section>.<number>) <name>",
    "plain_text": "<LaTeX or Unicode formula>",
    "validated": "True|False"
  },

  "mechanism": "<physical mechanism or derivation summary>",

  "source": "simulations/<filename>.py",

  // Simulation-specific results
  "key_result_1": <value>,
  "key_result_2": <value>
}
```

### Actionable Steps for Each Missing Field

#### 1. Status Field (28 missing)

Add one of:
- `"status": "PASS"` - Matches experimental data within error bars
- `"status": "FAIL"` - Conflicts with experimental data
- `"status": "CHECK"` - Requires further validation
- `"status": "RESOLVED"` - Addresses a theoretical concern
- `"status": "SPECULATIVE"` - Exploratory/not yet testable

**Action:** Review simulation results and assign appropriate status based on validation outcome.

#### 2. Validation Objects (32 missing, 2 incomplete)

For simulations comparing to experimental data, add:
```json
"validation": {
  "computed": <theoretical_prediction>,
  "experimental": <measured_value>,
  "error": <experimental_error>,
  "sigma": abs(computed - experimental) / error,
  "units": "<appropriate units>",
  "status": "PASS (X.XX sigma)" or "FAIL (X.XX sigma)"
}
```

For simulations with bounds (like proton decay):
```json
"validation": {
  "computed": <value>,
  "bound": <limit>,
  "bound_type": "upper" or "lower",
  "ratio": computed / bound,
  "units": "<appropriate units>",
  "status": "PASS (X.XXx bound)"
}
```

**Action:** Extract validation data from simulation Python files. Many already calculate these values but don't export them to JSON.

#### 3. Formula References (33 missing)

Link each simulation to its primary formula in the formula database.

**Action:**
1. Review simulation Python file docstring for formula used
2. Search `js/formula-database.js` for matching formula ID
3. Add formula object with id, label, and plain_text

Example mapping:
- `pmns_geometric_v14_1` → `"id": "pmns-theta13"` or `"id": "pmns-delta-cp"`
- `yukawa_textures` → `"id": "yukawa-texture"`
- `pneuma_stability` → `"id": "pneuma-potential"`

#### 4. Mechanism Descriptions (25 missing)

Extract from simulation Python file docstrings. Most have detailed explanations already written.

**Example sources:**
- `proton_decay_geometric_v13_0.py` lines 1-31: Contains full mechanism description
- `pmns_theta13_delta_geometric_v14_1.py` lines 1-60: Contains derivation details

**Action:** Copy mechanism description from Python file docstring into JSON as `"mechanism": "..."` field.

#### 5. Source References (26 missing)

Add reference to the Python simulation file.

**Action:** Add `"source": "simulations/<filename>.py"` for each simulation.

### Priority Order for Completion

**Phase 1 (HIGH):** Core validation data
1. Add status field to all 28 simulations
2. Complete validation objects for the 2 incomplete ones (proton_decay, neutrino_masses)
3. Add validation objects to simulations that compare to experimental data

**Phase 2 (MEDIUM):** Documentation
4. Add formula references linking to formula database
5. Extract mechanism descriptions from Python docstrings

**Phase 3 (LOW):** Traceability
6. Add source file references

### Estimated Effort

Based on review of simulation files:
- Most metadata already exists in Python docstrings
- Primary task is extraction and JSON formatting
- Estimated 5-10 minutes per simulation for complete metadata
- Total effort: ~3-6 hours for all 35 simulations
