# Centralization Validation Report

Generated: CENTRALIZATION_VALIDATION_REPORT

## Executive Summary

**Centralization Score: 47.6/100**

🔴 CRITICAL

## Key Metrics

| Metric | Count | Status |
|--------|-------|--------|
| PM References | 86 | ✅ |
| Hardcoded Numbers | 462 | 🔴 |
| Topic Sections | 404 | ✅ |
| Orphaned Content Blocks | 46 | 🔴 |
| Orphaned HTML Files | 22 | ⚠️ |
| Broken Links | 50 | 🔴 |
| Formulas (Integrated) | 1099 | ⚠️ |
| Formulas (Orphaned) | 1720 | ⚠️ |

---

## 1. PM Reference Analysis

### Valid PM References Found
Total unique PM references: **86**

Sample of PM references in use:

- `PM.dark_energy.functional_test_chi2_log`
- `PM.dark_energy.functional_test_delta_chi2`
- `PM.dark_energy.functional_test_sigma_preference`
- `PM.dark_energy.planck_tension_resolved`
- `PM.dark_energy.w0_DESI`
- `PM.dark_energy.w0_DESI_central`
- `PM.dark_energy.w0_DESI_error`
- `PM.dark_energy.w0_PM`
- `PM.dark_energy.w0_deviation_sigma`
- `PM.dark_energy.w0_sigma`
- `PM.dark_energy.w_CMB_frozen`
- `PM.dark_energy.w_CPL_at_CMB`
- `PM.dark_energy.w_DESI_average`
- `PM.dark_energy.wa_DESI`
- `PM.dark_energy.wa_PM_effective`
- `PM.dark_energy.wa_deviation_sigma`
- `PM.desi_dr2_data.significance`
- `PM.desi_dr2_data.w0_error`
- `PM.desi_dr2_data.wa_error`
- `PM.dimensions.D_common`
- ... and 66 more

### Hardcoded Numbers Detected
Total hardcoded numbers: **462**

⚠️ **ACTION REQUIRED**: Replace these hardcoded values with PM references


**beginners-guide.html**: 12 hardcoded numbers
  - `1.178`
  - `0.733`
  - `0.9557`
  - `0.2224`
  - `0.846`
  - ... and 7 more

**geometric-framework.html**: 21 hardcoded numbers
  - `1.488`
  - `1.488`
  - `2.118`
  - `2.118`
  - `2.1181`
  - ... and 16 more

**philosophical-implications.html**: 4 hardcoded numbers
  - `2.493`
  - `2.493`
  - `2.493`
  - `2.493`

**references.html**: 1 hardcoded numbers
  - `10.2307`

**theory-diagrams.html**: 7 hardcoded numbers
  - `0.9557`
  - `0.2224`
  - `0.9557`
  - `0.2224`
  - `1.178`
  - ... and 2 more

**tomita-takesaki.html**: 2 hardcoded numbers
  - `1803.04993`
  - `1803.04993`

**yang-mills.html**: 3 hardcoded numbers
  - `0.001`
  - `2.118`
  - `0.118`


---

## 2. Topic Integration Analysis

### Topic Sections Implemented
Total topic sections: **404**

### Orphaned Content Blocks
Total orphaned blocks: **46**

⚠️ **ACTION REQUIRED**: Integrate these content blocks into topic sections


**calabi-yau.html**: 4 orphaned blocks
  - Classes: `['detail-section']` - Text: DefinitionA Calabi-Yau manifold is a compact Kähler manifold...
  - Classes: `['detail-section']` - Text: Why Calabi-Yau Manifolds?Key PropertiesSupersymmetry Preserv...
  - Classes: `['detail-section']` - Text: Hodge Numbers and TopologyThe topology of a Calabi-Yau manif...
  - ... and 1 more

**g2-manifolds.html**: 9 orphaned blocks
  - Classes: `['detail-section']` - Text: What is G₂?G₂ is thesmallest exceptional Lie group, a 14-dim...
  - Classes: `['detail-section']` - Text: G₂ Holonomy ManifoldsAG₂ manifoldis a 7-dimensional Riemanni...
  - Classes: `['detail-section']` - Text: G₂ Manifolds vs. Calabi-Yau ManifoldsPropertyG₂ ManifoldsCal...
  - ... and 6 more

**index.html**: 6 orphaned blocks
  - Classes: `['detail-section']` - Text: Falsifiable PredictionsThe theory makes concrete, testable p...
  - Classes: `['detail-section']` - Text: General Relativity & GravityEstablishedEinstein Field Equati...
  - Classes: `['detail-section']` - Text: Quantum Field TheoryEstablishedDirac Equation(iγμ∂μ- m)ψ = 0...
  - ... and 3 more

**thermal-time.html**: 11 orphaned blocks
  - Classes: `['detail-section']` - Text: 5.1 The Problem of Time in Quantum GravityOne of the most pr...
  - Classes: `['detail-section']` - Text: 5.2 The Thermal Time Hypothesis (TTH)TheThermal Time Hypothe...
  - Classes: `['detail-section']` - Text: 5.2b Two-Time Structure in the 26D FrameworkIn the full 26-d...
  - ... and 8 more


---

## 3. File Organization

### Defined Pages (in sections_content.py)
Total: **17**

- index.html
- principia-metaphysica-paper.html
- sections/cmb-bubble-collisions-comprehensive.html
- sections/conclusion.html
- sections/cosmology.html
- sections/division-algebra-section.html
- sections/einstein-hilbert-term.html
- sections/fermion-sector.html
- sections/formulas.html
- sections/gauge-unification.html
- sections/geometric-framework.html
- sections/introduction.html
- sections/pneuma-lagrangian.html
- sections/predictions.html
- sections/theory-analysis.html
- sections/thermal-time.html
- sections/xy-gauge-bosons.html


### Orphaned HTML Files
Total: **22**

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
- `sections/pneuma-lagrangian-new.html`
- `visualization-index.html`


---

## 4. Link Integrity

🔴 **CRITICAL**: 50 broken links detected


**tomita-takesaki.html**:
  - `../sections/quantum-foundations.html`

**geometric-framework.html**:
  - `../index.html#sections`

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

**g2-manifolds.html**:
  - `../references.html#g2-manifolds`

**dirac-equation.html**:
  - `dirac-spinor.html`
  - `../references.html#dirac1928`

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

**thermal-time.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#sections`
  - `../references.html#thermal-time`

**index.html**:
  - `principia-metaphysica-paper.html#framework`
  - `principia-metaphysica-paper.html#four-brane-structure`
  - `sections/geometric-framework.html#pneuma-manifold`
  - `sections/gauge-unification.html#symmetry-breaking`

**introduction.html**:
  - `../index.html#sections`

**so10-gut.html**:
  - `../sections/computational-appendices.html`

**index.html**:
  - `dirac-lagrangian.html`
  - `generation-formula.html`
  - `thermal-time-relation.html`

**calabi-yau.html**:
  - `../references.html#calabi-yau`

**gauge-unification.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#predictions`
  - `../index.html#sections`
  - `../references.html#grand-unification`

**einstein-hilbert-action.html**:
  - `metric-tensor.html`
  - `../references.html#einstein1915`

**cosmology.html**:
  - `../index.html#abstract`
  - `../index.html#sections`
  - `../index.html#sections`
  - `../references.html#cosmology`

**kms-condition.html**:
  - `hawking-temperature.html`
  - `unruh-effect.html`


---

## 5. Formula Integration

### Formulas in Topic Sections
Total: **1099**

### Orphaned Formulas
Total: **1720**

⚠️ **ACTION REQUIRED**: Integrate these formulas into topic sections


**pneuma-lagrangian-new.html**: 30 orphaned formulas
  - `The Pneuma LagrangianThe fundamental fermionic fie`
  - `ℒ =Ψ(iΓMDM+ g·tortho)Ψ + λ(ΨΨ)²`
  - `Ψ(iΓMDM+ g·tortho)Ψ + λ(ΨΨ)²PM-Specific (26D)▼(iγμ`
  - ... and 27 more


---

## Recommendations

### Priority 1: Critical Issues
- 🔴 Fix 50 broken links
- 🔴 Replace 462 hardcoded numbers with PM references

### Priority 2: Important Improvements
- 🟡 Document or integrate 22 orphaned HTML files
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
