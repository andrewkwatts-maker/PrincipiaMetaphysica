# Centralization Validation Report

Generated: CENTRALIZATION_VALIDATION_REPORT

## Executive Summary

**Centralization Score: 47.6/100**

🔴 CRITICAL

## Key Metrics

| Metric | Count | Status |
|--------|-------|--------|
| PM References | 47 | ⚠️ |
| Hardcoded Numbers | 571 | 🔴 |
| Topic Sections | 404 | ✅ |
| Orphaned Content Blocks | 46 | 🔴 |
| Orphaned HTML Files | 31 | ⚠️ |
| Broken Links | 50 | 🔴 |
| Formulas (Integrated) | 1099 | ⚠️ |
| Formulas (Orphaned) | 1720 | ⚠️ |

---

## 1. PM Reference Analysis

### Valid PM References Found
Total unique PM references: **47**

Sample of PM references in use:

- `PM.dark_energy.planck_tension_resolved`
- `PM.dark_energy.w0_DESI_central`
- `PM.dark_energy.w0_DESI_error`
- `PM.dark_energy.w0_PM`
- `PM.dark_energy.w0_sigma`
- `PM.dark_energy.wa_PM_effective`
- `PM.gauge_unification.alpha_GUT_inv`
- `PM.kk_spectrum.hl_lhc_significance`
- `PM.kk_spectrum.m1_central`
- `PM.neutrino_mass_ordering.flux_dressing`
- `PM.neutrino_mass_ordering.m1_IH`
- `PM.neutrino_mass_ordering.m1_NH`
- `PM.neutrino_mass_ordering.m2_IH`
- `PM.neutrino_mass_ordering.m2_NH`
- `PM.neutrino_mass_ordering.m3_IH`
- `PM.neutrino_mass_ordering.m3_NH`
- `PM.neutrino_mass_ordering.prob_IH`
- `PM.neutrino_mass_ordering.prob_IH_mean`
- `PM.neutrino_mass_ordering.prob_IH_std`
- `PM.neutrino_mass_ordering.prob_NH`
- ... and 27 more

### Hardcoded Numbers Detected
Total hardcoded numbers: **571**

⚠️ **ACTION REQUIRED**: Replace these hardcoded values with PM references


**predictions.html**: 16 hardcoded numbers
  - `12.589`
  - `2.118`
  - `12.589`
  - `12.589`
  - `12.589`
  - ... and 11 more

**references.html**: 34 hardcoded numbers
  - `10.2307`
  - `10.1515`
  - `0802.3391`
  - `10.1103`
  - `83.3370`
  - ... and 29 more


---

## 2. Topic Integration Analysis

### Topic Sections Implemented
Total topic sections: **404**

### Orphaned Content Blocks
Total orphaned blocks: **46**

⚠️ **ACTION REQUIRED**: Integrate these content blocks into topic sections


**calabi-yau.html**: 10 orphaned blocks
  - Classes: `['detail-section']` - Text: DefinitionA Calabi-Yau manifold is a compact Kähler manifold...
  - Classes: `['detail-section']` - Text: Why Calabi-Yau Manifolds?Key PropertiesSupersymmetry Preserv...
  - Classes: `['detail-section']` - Text: Hodge Numbers and TopologyThe topology of a Calabi-Yau manif...
  - ... and 7 more

**g2-manifolds.html**: 9 orphaned blocks
  - Classes: `['detail-section']` - Text: What is G₂?G₂ is thesmallest exceptional Lie group, a 14-dim...
  - Classes: `['detail-section']` - Text: G₂ Holonomy ManifoldsAG₂ manifoldis a 7-dimensional Riemanni...
  - Classes: `['detail-section']` - Text: G₂ Manifolds vs. Calabi-Yau ManifoldsPropertyG₂ ManifoldsCal...
  - ... and 6 more

**index.html**: 5 orphaned blocks
  - Classes: `['detail-section']` - Text: General Relativity & GravityEstablishedEinstein Field Equati...
  - Classes: `['detail-section']` - Text: Quantum Field TheoryEstablishedDirac Equation(iγμ∂μ- m)ψ = 0...
  - Classes: `['detail-section']` - Text: Extra Dimensions & UnificationEstablishedKaluza-Klein Theory...
  - ... and 2 more

**principia-metaphysica-paper.html**: 4 orphaned blocks
  - Classes: `['info-box']` - Text: Bell Inequality Consideration:This hidden variable structure...
  - Classes: `['info-box']` - Text: Quaternion Structure:The observable 3D space B1= Im(ℍ) inher...
  - Classes: `['info-box']` - Text: Testability Note:These interpretations are currently not exp...
  - ... and 1 more

**thermal-time.html**: 2 orphaned blocks
  - Classes: `['detail-section']` - Text: 5.1 The Problem of Time in Quantum GravityOne of the most pr...
  - Classes: `['detail-section']` - Text: 5.2 The Thermal Time Hypothesis (TTH)TheThermal Time Hypothe...


---

## 3. File Organization

### Defined Pages (in sections_content.py)
Total: **8**

- index.html
- principia-metaphysica-paper.html
- sections/einstein-hilbert-term.html
- sections/fermion-sector.html
- sections/formulas.html
- sections/geometric-framework.html
- sections/pneuma-lagrangian.html
- sections/theory-analysis.html


### Orphaned HTML Files
Total: **31**

⚠️ **ACTION REQUIRED**: Add these files to sections_content.py or document why they're excluded

- `beginners-guide.html`
- `diagrams/theory-diagrams.html`
- `docs/PAPER_2T_UPDATE_SECTION.html`
- `docs/beginners-guide-printable.html`
- `docs/computational-appendices.html`
- `foundations/boltzmann-entropy.html`
- `foundations/calabi-yau.html`
- `foundations/clifford-algebra.html`
- `foundations/dirac-equation.html`
- `foundations/einstein-field-equations.html`
- `foundations/einstein-hilbert-action.html`
- `foundations/g2-manifolds.html`
- `foundations/kaluza-klein.html`
- `foundations/kms-condition.html`
- `foundations/ricci-tensor.html`
- `foundations/so10-gut.html`
- `foundations/tomita-takesaki.html`
- `foundations/yang-mills.html`
- `philosophical-implications.html`
- `references.html`
- `sections/cmb-bubble-collisions-comprehensive.html`
- `sections/conclusion.html`
- `sections/cosmology.html`
- `sections/division-algebra-section.html`
- `sections/gauge-unification.html`
- `sections/introduction.html`
- `sections/pneuma-lagrangian-new.html`
- `sections/predictions.html`
- `sections/thermal-time.html`
- `sections/xy-gauge-bosons.html`
- `visualization-index.html`


---

## 4. Link Integrity

🔴 **CRITICAL**: 50 broken links detected


**index.html**:
  - `dirac-lagrangian.html`
  - `generation-formula.html`
  - `thermal-time-relation.html`

**einstein-hilbert-action.html**:
  - `metric-tensor.html`
  - `../references.html#einstein1915`

**so10-gut.html**:
  - `../sections/computational-appendices.html`

**g2-manifolds.html**:
  - `../references.html#g2-manifolds`

**calabi-yau.html**:
  - `../references.html#calabi-yau`

**tomita-takesaki.html**:
  - `../sections/quantum-foundations.html`

**visualization-index.html**:
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`
  - `beginners-guide-printable.html`

**kms-condition.html**:
  - `hawking-temperature.html`
  - `unruh-effect.html`

**thermal-time.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#sections`
  - `../references.html#thermal-time`

**cosmology.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#sections`
  - `../references.html#cosmology`

**fermion-sector.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#predictions`
  - `../index.html#sections`
  - `geometric-framework.html#cy4-construction`
  - `../principia-metaphysica-paper.html#four-brane-structure`
  - `dark-sector.html`
  - `../references.html#neutrinos`

**dirac-equation.html**:
  - `dirac-spinor.html`
  - `../references.html#dirac1928`

**geometric-framework.html**:
  - `../index.html#sections`

**introduction.html**:
  - `../index.html#sections`

**gauge-unification.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#predictions`
  - `../index.html#sections`
  - `../references.html#grand-unification`

**index.html**:
  - `principia-metaphysica-paper.html#framework`
  - `principia-metaphysica-paper.html#four-brane-structure`
  - `sections/geometric-framework.html#pneuma-manifold`
  - `sections/gauge-unification.html#symmetry-breaking`

**beginners-guide.html**:
  - `beginners-guide-printable.html`


---

## 5. Formula Integration

### Formulas in Topic Sections
Total: **1099**

### Orphaned Formulas
Total: **1720**

⚠️ **ACTION REQUIRED**: Integrate these formulas into topic sections


**einstein-hilbert-action.html**: 22 orphaned formulas
  - `Established Physics (1915)The Einstein-Hilbert Act`
  - `S = &frac{1}{16πG} ∫ d4x √|g| R`
  - `S = &frac{1}{16πG} ∫ d4x √|g| REstablished▼SAction`
  - ... and 19 more

**so10-gut.html**: 8 orphaned formulas
  - `Theoretical Physics (1974)SO(10) Grand Unified The`
  - `SO(10) ⊃ SU(3) × SU(2) × U(1)`
  - `SO(10) Gauge Group: 16 spinor ⊕ 45 gauge bosonsThe`
  - ... and 5 more


---

## Recommendations

### Priority 1: Critical Issues
- 🔴 Fix 50 broken links
- 🔴 Replace 571 hardcoded numbers with PM references

### Priority 2: Important Improvements
- 🟡 Document or integrate 31 orphaned HTML files
- 🟡 Integrate 1720 orphaned formulas

### Priority 3: Nice to Have
- 🟢 Continue expanding topic sections for better organization
- 🟢 Add more PM references for dynamic value population
- 🟢 Document rationale for any intentionally orphaned files

---

## Next Steps

1. **Review this report** and prioritize fixes based on severity
2. **Run migration scripts** for hardcoded numbers → PM references
3. **Integrate orphaned content** into appropriate topic sections
4. **Fix broken links** to ensure site navigation works
5. **Re-run validation** to verify improvements

---

*Report generated by validate_centralization.py*

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
