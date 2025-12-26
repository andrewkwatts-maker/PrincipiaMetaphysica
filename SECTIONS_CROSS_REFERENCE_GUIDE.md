# Sections Cross-Reference Quick Guide

This guide shows which formulas and parameters are used in each section for quick lookup.

---

## By Section

### Section 1: Introduction (Framework)

**Formulas (6):**
- `master-action-26d` - 26D fundamental action
- `sp2r-constraints` - Sp(2,R) gauge fixing constraints
- `reduction-cascade` - Dimensional reduction sequence
- `effective-euler` - Effective Euler characteristic
- `generation-number` - Number of fermion generations
- `tcs-topology` - TCS manifold topology

**Parameters (8):**
- `dimensions.D_BULK` - 26
- `dimensions.D_AFTER_SP2R` - 13
- `dimensions.D_EFFECTIVE` - 6
- `dimensions.SIGNATURE_INITIAL` - [24, 2]
- `topology.CHI_EFF` - 144
- `topology.n_gen` - 3
- `topology.B2` - 4
- `topology.B3` - 24

---

### Section 2: Geometric Framework (Framework)

**Formulas (11):**
- `reduction-cascade`, `virasoro-anomaly`, `sp2r-constraints`
- `tcs-topology`, `effective-euler`, `flux-quantization`
- `effective-torsion`, `division-algebra`, `primordial-spinor-13d`
- `planck-mass-derivation`, `effective-dimension`

**Parameters (15):**
- All `dimensions.*` fields
- All main `topology.*` fields
- `topology.HODGE_H11`, `topology.HODGE_H21`, `topology.HODGE_H31`

---

### Section 3: Fermion Sector (Phenomenology)

**Formulas (12):**
- `generation-number`, `yukawa-instanton`, `hierarchy-ratio`
- `top-quark-mass`, `bottom-quark-mass`, `tau-lepton-mass`
- `neutrino-mass-21`, `neutrino-mass-31`, `seesaw-mechanism`
- `ckm-elements`, `cp-phase-geometric`, `theta23-maximal`

**Parameters (18):**
- `topology.CHI_EFF`, `topology.n_gen`, `topology.B3`
- All `neutrino.pmns_angles.*` (theta_12, theta_23, theta_13, delta_cp)
- All `neutrino.mass_splittings.*` (delta_m21_sq, delta_m31_sq)
- All `neutrino.mass_spectrum.*` (m_nu_1/2/3, sum_m_nu)
- `neutrino.seesaw.m_rh_neutrino`
- All `pmns.*` (theta_12, theta_23, theta_13, delta_CP)

---

### Section 4: Gauge Unification (Phenomenology)

**Formulas (15):**
- `gut-scale`, `gut-coupling`, `so10-breaking`, `pati-salam-chain`
- `weak-mixing-angle`, `doublet-triplet`, `proton-lifetime`, `proton-branching`
- `strong-coupling`, `higgs-vev`, `higgs-potential`, `higgs-quartic`
- `higgs-mass`, `rg-running-couplings`, `effective-torsion`

**Parameters (12):**
- All `gauge.*` (ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE)
- All `proton_decay.*` (tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound)
- `topology.B2`, `topology.B3`
- All `xy_bosons.*` (M_X, M_Y)

---

### Section 5: Cosmology and Predictions (Predictions)

**Formulas (17):**
- `dark-energy-w0`, `dark-energy-wa`, `pneuma-vev`
- `racetrack-superpotential`, `scalar-potential`, `attractor-potential`
- `friedmann-constraint`, `de-sitter-attractor`, `kk-graviton-mass`
- `gw-dispersion`, `gw-dispersion-coeff`, `gw-dispersion-alt`
- `mirror-dm-ratio`, `mirror-temp-ratio`, `thermal-time`
- `tomita-takesaki`, `kms-condition`

**Parameters (13):**
- All `dark_energy.*` (w0, wa, d_eff)
- `pneuma.VEV`
- All `kk_spectrum.*` (m1_TeV, uncertainty_TeV, LHC_BOUND_TEV)
- `neutrino.mass_spectrum.sum_m_nu`
- All `mirror_sector.*` (temperature_ratio, dm_baryon_ratio, modulation_width)
- All `mirror_sector.multi_sector.*` (n_sectors, gravity_dilution)

---

### Section 6: Conclusion (Framework)

**Formulas (8):**
- `generation-number`, `gut-scale`, `proton-lifetime`
- `dark-energy-w0`, `kk-graviton-mass`, `gw-dispersion`
- `planck-mass-derivation`, `bekenstein-hawking`

**Parameters (8):**
- `topology.CHI_EFF`, `topology.n_gen`
- `gauge.M_GUT`, `proton_decay.tau_p_years`
- `dark_energy.w0`
- `kk_spectrum.m1_TeV`, `kk_spectrum.LHC_BOUND_TEV`
- `neutrino.mass_spectrum.sum_m_nu`

---

## By Formula

### Most Used Formulas (appearing in 3+ sections)

**`generation-number`** (3 sections)
- Section 1 (Introduction)
- Section 3 (Fermion Sector)
- Section 6 (Conclusion)

**`reduction-cascade`** (2 sections)
- Section 1 (Introduction)
- Section 2 (Geometric Framework)

**`effective-euler`** (2 sections)
- Section 1 (Introduction)
- Section 2 (Geometric Framework)

**`tcs-topology`** (2 sections)
- Section 1 (Introduction)
- Section 2 (Geometric Framework)

**`planck-mass-derivation`** (2 sections)
- Section 2 (Geometric Framework)
- Section 6 (Conclusion)

**`effective-torsion`** (2 sections)
- Section 2 (Geometric Framework)
- Section 4 (Gauge Unification)

**`gut-scale`** (2 sections)
- Section 4 (Gauge Unification)
- Section 6 (Conclusion)

**`proton-lifetime`** (2 sections)
- Section 4 (Gauge Unification)
- Section 6 (Conclusion)

**`dark-energy-w0`** (2 sections)
- Section 5 (Cosmology and Predictions)
- Section 6 (Conclusion)

**`kk-graviton-mass`** (2 sections)
- Section 5 (Cosmology and Predictions)
- Section 6 (Conclusion)

**`gw-dispersion`** (2 sections)
- Section 5 (Cosmology and Predictions)
- Section 6 (Conclusion)

---

## By Parameter

### Most Used Parameters (appearing in 3+ sections)

**`topology.CHI_EFF`** (5 sections)
- Sections 1, 2, 3, 6

**`topology.n_gen`** (5 sections)
- Sections 1, 2, 3, 6

**`topology.B3`** (4 sections)
- Sections 1, 2, 3, 4

**`topology.B2`** (3 sections)
- Sections 1, 2, 4

**`dimensions.D_BULK`** (2 sections)
- Sections 1, 2

**`dimensions.D_AFTER_SP2R`** (2 sections)
- Sections 1, 2

**`dimensions.D_EFFECTIVE`** (2 sections)
- Sections 1, 2

**`neutrino.mass_spectrum.sum_m_nu`** (3 sections)
- Sections 3, 5, 6

**`gauge.M_GUT`** (2 sections)
- Sections 4, 6

**`proton_decay.tau_p_years`** (2 sections)
- Sections 4, 6

**`dark_energy.w0`** (2 sections)
- Sections 5, 6

**`kk_spectrum.m1_TeV`** (2 sections)
- Sections 5, 6

**`kk_spectrum.LHC_BOUND_TEV`** (2 sections)
- Sections 5, 6

---

## By Category

### Framework Sections (1, 2, 6)
- **Total formulas:** 25 unique
- **Total parameters:** 31 unique
- **Focus:** Dimensional structure, topology, fundamental principles

### Phenomenology Sections (3, 4)
- **Total formulas:** 27 unique (some overlap)
- **Total parameters:** 30 unique (some overlap)
- **Focus:** Particle masses, mixings, gauge unification

### Predictions Sections (5)
- **Total formulas:** 17 unique
- **Total parameters:** 13 unique
- **Focus:** Dark energy, KK modes, gravitational waves, observables

---

## Common Cross-References

### Core Topology Parameters
Used across framework sections:
- `topology.CHI_EFF` = 144
- `topology.n_gen` = 3
- `topology.B2` = 4
- `topology.B3` = 24

### Core Dimensional Parameters
Used in introduction and geometric framework:
- `dimensions.D_BULK` = 26
- `dimensions.D_AFTER_SP2R` = 13
- `dimensions.D_EFFECTIVE` = 6

### Core Predictions
Referenced in conclusion:
- `gauge.M_GUT` - GUT scale
- `proton_decay.tau_p_years` - Proton lifetime
- `dark_energy.w0` - Dark energy EOS
- `kk_spectrum.m1_TeV` - KK graviton mass

---

## Usage Examples

### Finding all sections that use a formula:
```python
# Example: Which sections use "generation-number"?
sections_using_formula = []
for section_id, section in sections.items():
    if "generation-number" in section.get("formulaRefs", []):
        sections_using_formula.append(section_id)
# Result: ["1", "3", "6"]
```

### Finding all formulas used in a category:
```python
# Example: All formulas in phenomenology sections
formulas_in_phenomenology = set()
for section in sections.values():
    if section.get("category") == "phenomenology":
        formulas_in_phenomenology.update(section.get("formulaRefs", []))
# Result: 27 unique formulas
```

### Finding parameter dependencies:
```python
# Example: All parameters used in fermion sector
params_in_fermion = sections["3"].get("paramRefs", [])
# Result: 18 parameters related to neutrinos, topology, PMNS
```

---

**Reference Date:** 2025-12-26
**Total Sections:** 6
**Total Unique Formulas Referenced:** 62
**Total Unique Parameters Referenced:** 40+
**Cross-Reference Density:** High (avg 11.5 formulas, 12.3 params per section)
