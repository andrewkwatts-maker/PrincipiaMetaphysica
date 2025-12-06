# Hardcoded Numbers Found by Agent 4

## Task Summary
Added two sections to sections_content.py:
1. xy_gauge_bosons (sections/xy-gauge-bosons.html)
2. division_algebras (sections/division-algebra-section.html)

## Hardcoded Numbers in xy-gauge-bosons.html

### Energy Scales
- **"10¹⁶ GeV"** - Lines 165, 170, 177, 343
  - Context: M_GUT scale references in descriptive text
  - Note: Should use PM reference `M_X` which is already used in lines 216, 287, 341, 460

### Proton Decay Parameters
- **"3.83×10³⁴ years"** - Line 443
  - Context: Proton lifetime prediction
  - Note: Should use PM reference `tau_p_median`

- **"64.2%"** - Line 444
  - Context: BR(e⁺π⁰) branching ratio
  - Note: Should use PM reference `BR_epi0_mean`

### Collider Energy Comparisons
- **"14 TeV"** - Lines 413, 419
  - Context: LHC energy

- **"100 TeV"** - Line 424
  - Context: FCC-hh energy

- **"~10²⁰ eV = 100 EeV"** - Line 428
  - Context: UHECRs energy

- **"0 - 91 GeV"** - Line 159
  - Context: Standard Model boson mass range

### Scientific Notation Powers
- **"10¹²"** - Lines 414, 419
  - Context: "10¹² times too weak" for collider comparisons

- **"10¹¹"** - Line 424
  - Context: Similar comparison for FCC-hh

- **"10⁶"** - Line 429
  - Context: "Still 10⁶× too weak" for UHECRs

- **"~10⁻⁴¹ s"** - Lines 378, 475
  - Context: X,Y boson lifetime estimates
  - Note: PM reference `tau_estimate` is used in lines 232, 303

### Gauge Boson Counts
- **"45"** - Lines 144, 181, 349, 466
  - Context: Total SO(10) gauge bosons

- **"12"** - Lines 158, 164, 170, 361
  - Context: Standard Model bosons, X bosons, Y bosons counts each

- **"9"** - Lines 176, 466
  - Context: Additional neutral heavy bosons

### Other Numbers
- **"1/23.54"** - Line 470
  - Context: α_GUT coupling
  - Note: PM reference `alpha_GUT_inv` is available and used in line 353

- **"~2%"** - Line 321
  - Context: Precision of gauge coupling unification

## Hardcoded Numbers in division-algebra-section.html

### Division Algebra Dimensions
- **"1, 2, 4, 8"** - Throughout the document
  - Context: The four normed division algebra dimensions (R, C, H, O)
  - Note: These are mathematical constants from Hurwitz theorem (1898), not PM parameters

- **"13"** - Throughout the document
  - Context: D = 13 = 1 + 4 + 8
  - Note: This is a derived sum, not a free parameter

### Alternative Dimensions (Invalid)
- **"3"** and **"9"** - Lines 122, 124, 125, 133
  - Context: Showing why 1 + 3 + 9 = 13 is invalid (not division algebra dimensions)

- **"10"** - Lines 156-165
  - Context: String theory D = 10 = 2 + 8 (C + O)

- **"11"** - Lines 169-179
  - Context: M-theory D = 11 = 1 + 2 + 8 (R + C + O)

- **"5"** and **"10"** - Lines 132, 129
  - Context: Invalid decompositions (5 + 8, 1 + 2 + 10)

- **"7"** - Line 178
  - Context: M-theory's 7D G₂ holonomy (partial)

### Exceptional Mathematics
- **"52 = 4 × 13"** - Line 241
  - Context: dim(F₄) automorphisms of J₃(O)

- **"78 = 6 × 13"** - Line 245
  - Context: dim(E₆) collineations of OP²

- **"27 - 14 = 13"** - Line 249
  - Context: dim(J₃(O)) - dim(G₂)

## PM References Successfully Used

### In xy-gauge-bosons.html
- `M_X` - Lines 216, 287, 341, 460
- `tau_estimate` - Lines 232, 303
- `alpha_GUT_inv` - Line 353

### In division-algebra-section.html
- None (this is a mathematical foundations section without numerical predictions)

## Recommendations

### High Priority (xy-gauge-bosons.html)
1. Replace "3.83×10³⁴ years" (line 443) with `<span class="pm-value" data-category="proton_decay" data-param="tau_p_median" data-format="scientific:2"></span>`
2. Replace "64.2%" (line 444) with calculation from `BR_epi0_mean`: `<span class="pm-value" data-category="proton_decay" data-param="BR_epi0_mean" data-format="percent:1"></span>`

### Medium Priority (xy-gauge-bosons.html)
3. Replace "10¹⁶ GeV" references with consistent use of `M_X` PM value
4. Add PM references for "1/23.54" → `alpha_GUT_inv` where not already used

### Low Priority
- Gauge boson counts (12, 45, 9) are structural constants from SO(10) representation theory
- Collider energies (14 TeV, 100 TeV) are factual references, not predictions
- Division algebra dimensions (1, 2, 4, 8) are mathematical constants, not parameters

## Notes
- Division algebra dimensions are fundamental mathematical constants (Hurwitz theorem 1898)
- They are not free parameters or predictions, so no PM references are needed
- The decomposition D = 13 = 1 + 4 + 8 is a consequence of the fundamental framework choice
