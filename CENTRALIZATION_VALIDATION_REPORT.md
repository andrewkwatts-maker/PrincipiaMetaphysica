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


**references.html**: 34 hardcoded numbers
  - `10.2307`
  - `10.1515`
  - `0802.3391`
  - `10.1103`
  - `83.3370`
  - ... and 29 more

**theory-analysis.html**: 16 hardcoded numbers
  - `0.884`
  - `0.884`
  - `0.853`
  - `12.589`
  - `0.853`
  - ... and 11 more


---

## 2. Topic Integration Analysis

### Topic Sections Implemented
Total topic sections: **404**

### Orphaned Content Blocks
Total orphaned blocks: **46**

⚠️ **ACTION REQUIRED**: Integrate these content blocks into topic sections


**cosmology.html**: 6 orphaned blocks
  - Classes: `['detail-section']` - Text: 6.1 Deriving 4D Gravity from Kaluza-Klein ReductionThe Princ...
  - Classes: `['detail-section']` - Text: 6.2 Myrzakulov F(R,T) GravityThe dimensional reduction from ...
  - Classes: `['detail-section']` - Text: 6.3 The Mashiach Field as a ModulusCentral to the cosmologic...
  - ... and 3 more

**g2-manifolds.html**: 9 orphaned blocks
  - Classes: `['detail-section']` - Text: What is G₂?G₂ is thesmallest exceptional Lie group, a 14-dim...
  - Classes: `['detail-section']` - Text: G₂ Holonomy ManifoldsAG₂ manifoldis a 7-dimensional Riemanni...
  - Classes: `['detail-section']` - Text: G₂ Manifolds vs. Calabi-Yau ManifoldsPropertyG₂ ManifoldsCal...
  - ... and 6 more

**index.html**: 1 orphaned blocks
  - Classes: `['detail-section']` - Text: Falsifiable PredictionsThe theory makes concrete, testable p...

**principia-metaphysica-paper.html**: 3 orphaned blocks
  - Classes: `['info-box']` - Text: Bell Inequality Consideration:This hidden variable structure...
  - Classes: `['info-box']` - Text: Quaternion Structure:The observable 3D space B1= Im(ℍ) inher...
  - Classes: `['info-box']` - Text: Testability Note:These interpretations are currently not exp...

**thermal-time.html**: 11 orphaned blocks
  - Classes: `['detail-section']` - Text: 5.1 The Problem of Time in Quantum GravityOne of the most pr...
  - Classes: `['detail-section']` - Text: 5.2 The Thermal Time Hypothesis (TTH)TheThermal Time Hypothe...
  - Classes: `['detail-section']` - Text: 5.2b Two-Time Structure in the 26D FrameworkIn the full 26-d...
  - ... and 8 more


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

**einstein-hilbert-action.html**:
  - `metric-tensor.html`
  - `../references.html#einstein1915`

**dirac-equation.html**:
  - `dirac-spinor.html`
  - `../references.html#dirac1928`

**beginners-guide.html**:
  - `beginners-guide-printable.html`

**fermion-sector.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#predictions`
  - `../index.html#sections`
  - `geometric-framework.html#cy4-construction`
  - `../principia-metaphysica-paper.html#four-brane-structure`
  - `dark-sector.html`
  - `../references.html#neutrinos`

**kms-condition.html**:
  - `hawking-temperature.html`
  - `unruh-effect.html`

**so10-gut.html**:
  - `../sections/computational-appendices.html`

**index.html**:
  - `principia-metaphysica-paper.html#framework`
  - `principia-metaphysica-paper.html#four-brane-structure`
  - `sections/geometric-framework.html#pneuma-manifold`
  - `sections/gauge-unification.html#symmetry-breaking`

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

**g2-manifolds.html**:
  - `../references.html#g2-manifolds`

**index.html**:
  - `dirac-lagrangian.html`
  - `generation-formula.html`
  - `thermal-time-relation.html`

**gauge-unification.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#predictions`
  - `../index.html#sections`
  - `../references.html#grand-unification`

**calabi-yau.html**:
  - `../references.html#calabi-yau`

**geometric-framework.html**:
  - `../index.html#sections`

**introduction.html**:
  - `../index.html#sections`


---

## 5. Formula Integration

### Formulas in Topic Sections
Total: **1099**

### Orphaned Formulas
Total: **1720**

⚠️ **ACTION REQUIRED**: Integrate these formulas into topic sections


**einstein-hilbert-action.html**: 9 orphaned formulas
  - `Established Physics (1915)The Einstein-Hilbert Act`
  - `S = &frac{1}{16πG} ∫ d4x √|g| R`
  - `S = &frac{1}{16πG} ∫ d4x √|g| REstablished▼SAction`
  - ... and 6 more

**tomita-takesaki.html**: 21 orphaned formulas
  - `Established Mathematics (1970)Tomita-Takesaki Theo`
  - `σt(A) = ΔitA Δ-it`
  - `σt(A) = ΔitA Δ-itEstablished▼STomita OperatorThe a`
  - ... and 18 more


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
