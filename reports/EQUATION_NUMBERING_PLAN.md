# Equation Numbering Implementation Plan

## Current Statistics Clarification

**IMPORTANT DISTINCTION:**

| Metric | Value | Meaning |
|--------|-------|---------|
| Parameters DERIVED | 56/58 (96.6%) | Derived from geometry (2 calibrated: θ₁₃, δ_CP) |
| Predictions within 1σ | 45/48 (93.8%) | Match experiment within 1σ |
| Exact matches | 12/48 (25%) | 0.0σ deviation from central value |
| Exact matches | 20 (user count) | Including additional exact agreements |

**Source of Truth:** `theory_output.json` and `simulations/final_transparency_v12_8.py`

---

## Phase 1: Statistics Consistency Fix

### Files with "45/48" that need context:
1. `principia-metaphysica-paper.html` (lines 819, 848, 8680, 48620)
2. `references.html` (line 974)
3. `sections/predictions.html` (line 259)
4. `sections/pneuma-lagrangian.html` (line 1337)
5. `sections/pneuma-lagrangian-new.html` (line 600)

### Action: Ensure both metrics are clearly stated:
- "56 of 58 parameters derived from geometry (2 calibrated)"
- "45 of 48 predictions within 1σ (93.8%), 12 exact matches"

---

## Phase 2: θ₁₃ and δ_CP Derivation Note

### Add to transparency section:
```
Attempts to derive θ₁₃ and δ_CP from triple cycle intersections and flux
phases were explored but did not yield the observed values; they remain
experimental inputs pending rigorous Yukawa intersection calculation.
```

### Files to update:
1. `principia-metaphysica-paper.html` - Transparency statement
2. `simulations/final_transparency_v12_8.py` - Add to calibrated parameter notes

---

## Phase 3: Equation Numbering Strategy

### Key Equations to Number:

**Master Actions:**
1. S₂₆ - Master 26D Action (Eq. 1)
2. S₁₃ - 13D Shadow Action (Eq. 2)
3. S₄ - 4D Effective Action (Eq. 3)

**Topological:**
4. n_gen = χ_eff/48 (Eq. 4)
5. χ_eff = 2(h¹¹ - h²¹ + h³¹) (Eq. 5)

**Gauge:**
6. α_GUT = 1/(10π) (Eq. 6)
7. M_GUT from torsion (Eq. 7)

**Dark Energy:**
8. w₀ = -(d_eff - 1)/(d_eff + 1) (Eq. 8)
9. w(z) functional form (Eq. 9)

**Neutrino:**
10. tan²θ₂₃ = Shadow_ק/Shadow_ח = 1 (Eq. 10)
11. Seesaw formula (Eq. 11)

**Predictions:**
12. τ_p proton lifetime (Eq. 12)
13. KK graviton mass (Eq. 13)
14. BR(p→e⁺π⁰) (Eq. 14)
15. η GW dispersion (Eq. 15)

### Implementation Script:

```python
#!/usr/bin/env python3
"""
add_equation_numbers.py - Add equation numbering to PM paper

Strategy:
1. Identify key equations by pattern matching
2. Add (Eq. N) labels systematically
3. Create cross-reference index
4. Validate no broken references
"""

EQUATION_PATTERNS = [
    (r'S_{26}.*=.*\int', 'Master 26D Action', 1),
    (r'n_{\text{gen}}.*=.*\\chi', 'Generation Number', 4),
    (r'w_0.*=.*-\\frac{d_{\text{eff}}', 'Dark Energy EoS', 8),
    # ... etc
]
```

---

## Phase 4: Validation Agent Tasks

1. **Diff Analysis**: Review all changes for consistency
2. **Cross-reference Check**: Ensure equation numbers don't conflict
3. **Source of Truth Validation**: Verify PM constants used throughout
4. **LaTeX Syntax Check**: Ensure MathJax renders correctly

---

## Execution Order

1. ✅ Fix statistics inconsistency (clarify 56/58 vs 45/48)
2. ✅ Add θ₁₃/δ_CP derivation attempt note
3. Create equation numbering script
4. Apply to paper (test on small section first)
5. Deploy validation agent
6. Commit and push

---

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
