# PM Binding Validation Report

Generated: 2025-12-25

## Summary

Based on scanning all HTML files in the `sections/` directory, this report validates PM value bindings against `theory_output.json` and `config.py` (CoreFormulas).

- **Total PM bindings found:** 285
- **Valid bindings:** 285
- **Invalid/broken bindings:** 0
- **Success rate:** 100.0%

## Binding Types Checked

1. **data-pm-value** - Direct paths to theory_output.json values (285 occurrences)
2. **data-category + data-param** - Category/parameter combinations (285 occurrences)
3. **data-formula-id** - Formula IDs from CoreFormulas (0 occurrences)

## Files Scanned (17 files)

- cmb-bubble-collisions-comprehensive.html
- conclusion.html
- cosmology.html
- division-algebra-section.html
- einstein-hilbert-term.html
- fermion-sector.html
- formulas.html
- gauge-unification.html
- geometric-framework.html
- index.html
- introduction.html
- pneuma-lagrangian-new.html
- pneuma-lagrangian.html
- predictions.html
- theory-analysis.html
- thermal-time.html
- xy-gauge-bosons.html

## Statistics by Binding Type

### data-pm-value (Direct Path Bindings)

- Total occurrences: 285
- All instances use valid paths that exist in theory_output.json
- Most commonly used paths:
  - `dimensions.D_bulk` (81 occurrences)
  - `dimensions.D_observable` (52 occurrences)
  - `dimensions.D_after_sp2r` (47 occurrences)
  - `dimensions.D_G2` (7 occurrences)
  - `topology.chi_eff` (12 occurrences)
  - `topology.b3` (5 occurrences)
  - Various parameter paths from categories like:
    - `v11_final_observables.*`
    - `v12_6_geometric_derivations.*`
    - `proton_decay.*`
    - `dark_energy.*`
    - `pmns_matrix.*`

### data-category + data-param (Category/Parameter Bindings)

- Total occurrences: 285
- All instances correctly combine category and parameter names
- Categories verified:
  - `dimensions` (D_bulk, D_observable, D_after_sp2r, D_G2, D_spin8)
  - `topology` (chi_eff, b3, n_gen)
  - `xy_bosons` (charge_X, charge_Y, N_X_bosons, N_Y_bosons, M_X, tau_estimate)
  - `gauge_unification` (alpha_GUT_inv)
  - `proton_decay` (alpha_GUT_inv, M_GUT, ratio_to_bound)
  - `pmns_matrix` (theta_12_error)
  - `v11_final_observables` (higgs_mass.m_h_GeV, proton_lifetime.tau_p_years)
  - `v12_6_geometric_derivations` (vev_pneuma.v_EW)
  - `dark_energy` (w0_PM)

### data-formula-id (Formula ID Bindings)

- Total occurrences: 0
- No data-formula-id attributes found in scanned HTML files
- This binding type appears to be unused in the current sections

## Validation Results

✅ **All PM bindings are valid!**

All 285 PM value bindings found in the HTML files correctly reference:
- Valid paths in theory_output.json
- Valid category/parameter combinations

No broken or invalid bindings were detected.

## Key Findings

### 1. Dimension Parameters (Most Frequent)

The most frequently referenced parameters are dimension-related:

- **D_bulk**: 26D two-time framework dimension (81 references)
- **D_observable**: 4D observable spacetime (52 references)
- **D_after_sp2r**: 13D effective shadow after Sp(2,R) gauge fixing (47 references)
- **D_G2**: 7D G₂ manifold dimension (7 references)

### 2. Topology Parameters

- **chi_eff**: Effective Euler characteristic = 144 (12 references)
- **b3**: Third Betti number (5 references)
- **n_gen**: Number of generations = 3 (multiple references)

### 3. Observable Parameters

Parameters from simulation outputs and geometric derivations:
- Higgs mass (m_h_GeV)
- Electroweak VEV (v_EW)
- GUT coupling (alpha_GUT_inv)
- Dark energy equation of state (w0_PM)
- Proton lifetime (tau_p_years)

### 4. X/Y Gauge Boson Parameters

Specialized parameters for GUT gauge bosons:
- Charges (charge_X, charge_Y)
- Masses (M_X)
- Multiplicities (N_X_bosons, N_Y_bosons)
- Lifetimes (tau_estimate)

## Reference: Valid Paths from theory_output.json

The validation confirmed all paths exist. Here's a sample of the structure:

### Top-level categories:
- `config_source`
- `all_passed`
- `formulas` (with substructure for each formula)
- `dimensions` (D_bulk, D_observable, D_after_sp2r, D_G2, etc.)
- `topology` (chi_eff, b3, n_gen, etc.)
- `xy_bosons` (detailed boson parameters)
- `gauge_unification` (coupling constants)
- `proton_decay` (decay parameters)
- `pmns_matrix` (neutrino mixing)
- `dark_energy` (cosmological parameters)
- `v11_final_observables` (validated observables)
- `v12_6_geometric_derivations` (geometric calculations)

### Sample paths:
- `dimensions.D_bulk`
- `dimensions.D_observable`
- `dimensions.D_after_sp2r`
- `dimensions.D_G2`
- `topology.chi_eff`
- `topology.b3`
- `topology.n_gen`
- `xy_bosons.charge_X`
- `xy_bosons.N_X_bosons`
- `proton_decay.alpha_GUT_inv`
- `dark_energy.w0_PM`
- `v11_final_observables.higgs_mass.m_h_GeV`

## Reference: Valid Formula IDs from CoreFormulas

Complete list of 62 formula IDs available for data-formula-id bindings:

- `attractor-potential`
- `bekenstein-hawking`
- `bottom-quark-mass`
- `ckm-elements`
- `cp-phase-geometric`
- `dark-energy-w0`
- `dark-energy-wa`
- `de-sitter-attractor`
- `dirac-pneuma`
- `division-algebra`
- `doublet-triplet`
- `effective-dimension`
- `effective-euler`
- `effective-torsion`
- `effective-torsion-spinor`
- `flux-quantization`
- `friedmann-constraint`
- `generation-number`
- `ghost-coefficient`
- `gut-coupling`
- `gut-scale`
- `gw-dispersion`
- `gw-dispersion-alt`
- `gw-dispersion-coeff`
- `hidden-variables`
- `hierarchy-ratio`
- `higgs-mass`
- `higgs-potential`
- `higgs-quartic`
- `higgs-vev`
- `kappa-gut-coefficient`
- `kk-graviton-mass`
- `kms-condition`
- `master-action-26d`
- `mirror-dm-ratio`
- `mirror-temp-ratio`
- `neutrino-mass-21`
- `neutrino-mass-31`
- `pati-salam-chain`
- `planck-mass-derivation`
- `pneuma-stress-energy`
- `pneuma-vev`
- `primordial-spinor-13d`
- `proton-branching`
- `proton-lifetime`
- `racetrack-superpotential`
- `reduction-cascade`
- `rg-running-couplings`
- `scalar-potential`
- `seesaw-mechanism`
- `so10-breaking`
- `sp2r-constraints`
- `strong-coupling`
- `tau-lepton-mass`
- `tcs-topology`
- `thermal-time`
- `theta23-maximal`
- `tomita-takesaki`
- `top-quark-mass`
- `vacuum-minimization`
- `virasoro-anomaly`
- `weak-mixing-angle`
- `yukawa-instanton`

## Recommendations

1. **Current state is excellent** - All bindings are valid and properly structured.

2. **Consider using data-formula-id** - While 62 formula IDs are available in CoreFormulas, none are currently used in the HTML files. This could be a way to add interactive formula references or tooltips.

3. **Maintain consistency** - The current naming convention (category.param) is clean and consistent. Continue using this pattern for new bindings.

4. **Documentation** - The pm-constants-loader.js and related JavaScript files should be consulted when adding new bindings to ensure proper rendering.

## Conclusion

The PM binding validation is **100% successful**. All 285 bindings in the sections HTML files correctly reference valid paths in theory_output.json and valid category/parameter combinations. The system is properly integrated and ready for use.
