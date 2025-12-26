# Related Formulas Completion Report
## config.py CoreFormulas Metadata Enhancement

**Date:** December 25, 2025
**Audit Status:** 31/55 formulas have related_formulas (56% complete)
**Missing:** 24 formulas need related_formulas metadata

---

## Executive Summary

This report identifies the 24 formulas missing `related_formulas` metadata in `H:\Github\PrincipiaMetaphysica\config.py` and provides recommended related formula lists based on:

1. **Parent formulas** - What each formula derives from (identified in derivation.parent_formulas)
2. **Child formulas** - What formulas derive from it
3. **Sibling formulas** - Formulas in the same category/section or sharing physics connections

---

## Formulas Missing related_formulas (24 total)

### 1. generation-number
**Label:** (2.6) Three Generations
**Category:** DERIVED
**Section:** Fermion
**Current Derivation Parents:** ["tcs-euler-characteristic"]

**Recommended related_formulas:**
```python
related_formulas=["tcs-topology", "effective-euler", "flux-quantization", "theta23-maximal"]
```

**Rationale:**
- **Parent:** Derives from TCS topology (χ_eff = 144)
- **Sibling:** effective-euler provides the χ_eff value used
- **Sibling:** flux-quantization relates to the index theorem divisor
- **Child:** theta23-maximal uses generation structure from G₂ holonomy

---

### 2. gut-scale
**Label:** (4.2) GUT Scale
**Category:** DERIVED
**Section:** 4 (Gauge Unification)
**Current Derivation Parents:** ["g2-compactification"]

**Recommended related_formulas:**
```python
related_formulas=["tcs-topology", "gut-coupling", "proton-lifetime", "planck-mass-derivation"]
```

**Rationale:**
- **Parent:** Derives from G₂ compactification volume
- **Sibling:** gut-coupling uses M_GUT for unification scale
- **Child:** proton-lifetime uses M_GUT⁴ in decay formula
- **Sibling:** planck-mass-derivation shows dimensional reduction from 13D

---

### 3. dark-energy-w0
**Label:** (7.1) Dark Energy EoS
**Category:** PREDICTIONS
**Section:** 7 (Cosmology)
**Current Derivation Parents:** ["thermal-time-flow", "mep-constraint"]

**Recommended related_formulas:**
```python
related_formulas=["dark-energy-wa", "thermal-time", "kms-condition", "effective-dimension"]
```

**Rationale:**
- **Sibling:** dark-energy-wa is the time derivative/evolution
- **Parent:** thermal-time provides the fundamental flow mechanism
- **Parent:** kms-condition determines α_T = 4.5 parameter
- **Sibling:** effective-dimension influences dark energy EoS

---

### 4. proton-lifetime
**Label:** (5.3) Proton Lifetime
**Category:** PREDICTIONS
**Section:** 5 (Gauge)
**Current Derivation Parents:** ["gut-scale", "tcs-suppression"]

**Recommended related_formulas:**
```python
related_formulas=["gut-scale", "gut-coupling", "proton-branching", "doublet-triplet"]
```

**Rationale:**
- **Parent:** Uses M_GUT from gut-scale
- **Parent:** Uses α_GUT from gut-coupling
- **Sibling:** proton-branching gives decay mode BR(e⁺π⁰)
- **Sibling:** doublet-triplet mechanism prevents fast Higgs-mediated decay

---

### 5. theta23-maximal
**Label:** (6.1) Atmospheric Mixing
**Category:** DERIVED
**Section:** 6 (Fermion)
**Current Derivation Parents:** ["g2-holonomy"]

**Recommended related_formulas:**
```python
related_formulas=["neutrino-mass-21", "neutrino-mass-31", "tcs-topology", "cp-phase-geometric"]
```

**Rationale:**
- **Sibling:** neutrino mass splittings are already linked back to theta23
- **Parent:** G₂ holonomy comes from TCS topology
- **Sibling:** cp-phase-geometric shares geometric origin from G₂

---

### 6. kk-graviton-mass
**Label:** (8.1) KK Graviton Mass
**Category:** PREDICTIONS
**Section:** 8 (Predictions)
**Current Derivation Parents:** ["g2-compactification"]

**Recommended related_formulas:**
```python
related_formulas=["gut-scale", "tcs-topology", "planck-mass-derivation"]
```

**Rationale:**
- **Sibling:** gut-scale also derives from G₂ compactification volume
- **Parent:** TCS topology determines compactification radius R_c
- **Sibling:** planck-mass-derivation shares dimensional reduction physics

---

### 7. neutrino-mass-21
**Status:** HAS related_formulas (already includes neutrino-mass-31, theta23-maximal)
**Note:** This formula is already complete - skip

---

### 8. neutrino-mass-31
**Status:** HAS related_formulas (already includes neutrino-mass-21, theta23-maximal)
**Note:** This formula is already complete - skip

---

## Additional Formulas Likely Missing (Analysis continues...)

Based on the grep search showing only 31 formulas with related_formulas out of 55 total, let me identify the remaining 22 formulas that are missing this metadata:

---

### Analysis Method

I'll cross-reference the formulas WITH related_formulas against the complete list of 55 formulas:

**Formulas WITH related_formulas (31):**
1. master-action-26d
2. virasoro-anomaly
3. sp2r-constraints
4. racetrack-superpotential
5. pneuma-vev
6. reduction-cascade
7. primordial-spinor-13d
8. tcs-topology
9. effective-euler
10. flux-quantization
11. effective-torsion
12. mirror-dm-ratio
13. so10-breaking
14. gut-coupling
15. weak-mixing-angle
16. higgs-vev
17. top-quark-mass
18. strong-coupling
19. neutrino-mass-21
20. neutrino-mass-31
21. cp-phase-geometric
22. effective-dimension
23. dark-energy-wa
24. thermal-time
25. gw-dispersion
26. gw-dispersion-coeff
27. proton-branching
28. bekenstein-hawking
29. scalar-potential
30. hidden-variables
31. hierarchy-ratio
32. division-algebra
33. seesaw-mechanism
34. ckm-elements
35. yukawa-instanton
36. attractor-potential
37. friedmann-constraint
38. de-sitter-attractor
39. tomita-takesaki
40. kms-condition
41. planck-mass-derivation
42. doublet-triplet
43. dirac-pneuma
44. ghost-coefficient
45. kappa-gut-coefficient
46. effective-torsion-spinor
47. gw-dispersion-alt
48. vacuum-minimization
49. mirror-temp-ratio
50. pati-salam-chain
51. higgs-potential
52. higgs-quartic
53. rg-running-couplings
54. bottom-quark-mass
55. tau-lepton-mass
56. higgs-mass

**Formulas WITHOUT related_formulas (24):**

Based on the list above (56 items but audit says 31/55), let me identify which are missing:

The 55 total formulas minus 31 with related_formulas = **24 missing**

---

## Complete List of 24 Formulas Missing related_formulas

### Section 0: Top-Level Predictions (6 formulas)

#### 1. generation-number
```python
related_formulas=["tcs-topology", "effective-euler", "flux-quantization", "theta23-maximal"]
```

#### 2. gut-scale
```python
related_formulas=["tcs-topology", "gut-coupling", "proton-lifetime", "planck-mass-derivation"]
```

#### 3. dark-energy-w0
```python
related_formulas=["dark-energy-wa", "thermal-time", "kms-condition", "effective-dimension"]
```

#### 4. proton-lifetime
```python
related_formulas=["gut-scale", "gut-coupling", "proton-branching", "doublet-triplet"]
```

#### 5. theta23-maximal
```python
related_formulas=["neutrino-mass-21", "neutrino-mass-31", "tcs-topology", "cp-phase-geometric"]
```

#### 6. kk-graviton-mass
```python
related_formulas=["gut-scale", "tcs-topology", "planck-mass-derivation"]
```

---

## VERIFICATION NEEDED

To complete this report accurately, I need to verify which specific 18 additional formulas beyond the first 6 are missing related_formulas.

From the grep output, I can confirm these formulas HAVE related_formulas (partial list shown in grep):
- master-action-26d ✓
- virasoro-anomaly ✓
- sp2r-constraints ✓
- racetrack-superpotential ✓
- pneuma-vev ✓
- reduction-cascade ✓
- primordial-spinor-13d ✓
- tcs-topology ✓
- effective-euler ✓
- flux-quantization ✓
- effective-torsion ✓
- mirror-dm-ratio ✓
- so10-breaking ✓
- gut-coupling ✓
- weak-mixing-angle ✓
- higgs-vev ✓
- top-quark-mass ✓
- strong-coupling ✓
- neutrino-mass-21 ✓
- neutrino-mass-31 ✓
- cp-phase-geometric ✓
- effective-dimension ✓
- dark-energy-wa ✓
- thermal-time ✓
- gw-dispersion ✓
- gw-dispersion-coeff ✓
- proton-branching ✓
- bekenstein-hawking ✓
- scalar-potential ✓
- hidden-variables ✓
- hierarchy-ratio ✓

This confirms 31 formulas have related_formulas.

---

## Remaining 18 Formulas to Analyze

Since the first 6 (generation-number through kk-graviton-mass) don't have related_formulas, the remaining 18 must be among:

- division-algebra (?)
- seesaw-mechanism (?)
- ckm-elements (?)
- yukawa-instanton (?)
- attractor-potential (?)
- friedmann-constraint (?)
- de-sitter-attractor (?)
- tomita-takesaki (?)
- kms-condition (?)
- planck-mass-derivation (?)
- doublet-triplet (?)
- dirac-pneuma (?)
- ghost-coefficient (?)
- kappa-gut-coefficient (?)
- effective-torsion-spinor (?)
- gw-dispersion-alt (?)
- vacuum-minimization (?)
- mirror-temp-ratio (?)
- pati-salam-chain (?)
- higgs-potential (?)
- higgs-quartic (?)
- rg-running-couplings (?)
- bottom-quark-mass (?)
- tau-lepton-mass (?)
- higgs-mass (?)

Need to verify which of these DO have related_formulas vs which don't.

---

## Next Steps

1. Parse config.py systematically to identify exact 24 formulas without related_formulas
2. For each formula:
   - Examine derivation.parent_formulas
   - Identify child formulas (formulas that use it)
   - Find sibling formulas in same section/category
3. Generate final recommended related_formulas list

---

## Methodology for Determining Related Formulas

### Parent Formulas
- Check derivation.parent_formulas field
- Link to formulas it directly derives from

### Child Formulas
- Search for formulas that list this one in their derivation.parent_formulas
- Search for formulas that use this formula's computed_value

### Sibling Formulas
- Same section number
- Same physics category (gauge, fermion, cosmology, etc.)
- Share common parent formulas
- Part of same derivation chain

---

## Status

**Current Progress:** 6/24 formulas analyzed with recommended related_formulas

**Remaining:** Need to identify and analyze 18 additional formulas

**Next Action:** Systematically check each formula in config.py to determine which are missing related_formulas field
