# PDG 2024 & Experimental Citation Additions
**Document**: principia-metaphysica-paper.html
**Date**: 2025-12-18
**Status**: Ready to apply

---

## Executive Summary

This document specifies exact edits needed to add proper PDG 2024 and experimental citations to hardcoded values. Six values have been audited; three need new citations, three need verification.

**Values needing citations**: 3
**Values with existing citations**: 3
**References section**: Needs CODATA 2022 entry

---

## EDIT 1: M_Z = 91.2 GeV (Line 1051)

**Current state**: Used without citation
**Location**: Section 5.4, in derivation box
**Current text**:
```html
<li class="derivation-step">RG evolution from $M_{\text{GUT}} = 2.12 \times 10^{16}$ GeV to $M_Z = 91.2$ GeV</li>
```

**Edit needed**: Add inline PDG citation after this line
**New text to insert after line 1051**:
```html
<p style="margin-top: 0.5rem; font-size: 0.85rem; color: #555;"><em>PDG 2024: $M_Z = 91.1876 \pm 0.0021$ GeV</em></p>
```

**Justification**: M_Z is used in RG evolution; should have explicit source
**Priority**: LOW - well-documented constant

---

## EDIT 2: M_Pl = 2.435 × 10^18 GeV (Line 1084)

**Current state**: Used without citation
**Location**: Section 5.5, in derivation box
**Current text**:
```html
<li class="derivation-step">Planck mass: $M_{\text{Pl}} = 2.435 \times 10^{18}$ GeV</li>
```

**Edit needed**: Add inline CODATA citation after this line
**New text to insert after line 1084**:
```html
<p style="margin-top: 0.5rem; font-size: 0.85rem; color: #555;"><em>CODATA 2022: $M_{\text{Pl}} = 2.4351 \times 10^{18}$ GeV (from $\hbar c/G_N$)</em></p>
```

**Justification**: Planck mass is derived from fundamental constants; CODATA is authoritative source
**Priority**: MEDIUM - appears in critical VEV derivation

---

## EDIT 3: sin²θ_W = 0.23121 (Line 1044-1055)

**Current state**: HAS PDG citation already
**Location**: Section 5.4, equation and derivation box

**Verification result**: ADEQUATE
**Current citation** (line 1055):
```html
<p style="margin-top: 1rem; font-size: 0.9rem; color: #666;"><em>PDG 2024: $\sin^2\theta_W = 0.23122 \pm 0.00003$ &mdash; 0.33σ agreement</em></p>
```

**Action**: NO EDIT NEEDED - citation present and correct
**Note**: Small discrepancy between paper value (0.23121) and PDG (0.23122) is within tolerance

---

## EDIT 4: m_h = 125.1 GeV (Line 1592)

**Current state**: Used without citation
**Location**: Section 9.1 Input Summary, bullet point
**Current text**:
```html
<li><strong>1 constraint:</strong> Higgs mass $m_h = 125.1$ GeV fixes Re$(T) = 7.086$</li>
```

**Edit needed**: Add inline ATLAS+CMS citation
**New text replacement**:
```html
<li><strong>1 constraint:</strong> Higgs mass $m_h = 125.1$ GeV (PDG 2024: $125.09 \pm 0.24$ GeV) fixes Re$(T) = 7.086$</li>
```

**Justification**: Higgs mass is key input constraint; should reference combined experimental result
**Priority**: MEDIUM - key input parameter

---

## EDIT 5: m_t = 172.7 GeV (Line 1241-1253)

**Current state**: HAS PDG citation
**Location**: Section 6.2a Top Quark Mass

**Verification result**: ADEQUATE
**Current equation** (line 1241):
```html
$$m_t = y_t 	imes rac{v_{	ext{EW}}}{\sqrt{2}} = 172.7 	ext{ GeV}$$
```

**Current citation** (line 1253):
```html
<p style="margin-top: 1rem; font-size: 0.9rem; color: #666;"><em>PDG 2024: $m_t = 172.69 \pm 0.30$ GeV &mdash; exact agreement</em></p>
```

**Action**: NO EDIT NEEDED - citation present and excellent agreement
**Note**: 172.7 GeV vs PDG 172.69 ± 0.30 GeV is within 0.1%

---

## EDIT 6: Super-K Proton Decay Limit (Lines 1143 & 1850)

**Current state**: INCONSISTENCY DETECTED
**Locations**:
- Line 1143: "Super-K limit: τ_p > 2.4 × 10^34 yr"
- Line 1850: "Super-Kamiokande bound: τ_p > 1.67 × 10^34 yr"

**Issue**: Two different values cited for same experimental limit
**Current text (line 1143)**:
```html
<p style="margin-top: 1rem; font-size: 0.9rem; color: #666;"><em>Super-K limit: $\tau_p > 2.4 \times 10^{34}$ years &mdash; PM prediction compatible</em></p>
```

**Current text (line 1850)**:
```html
Super-Kamiokande bound: $\tau_p > 1.67 \times 10^{34}$ yr. PM prediction is 2.3&times; the current bound, consistent and testable at Hyper-Kamiokande.
```

**Edit needed**: UNIFY to single correct value
**Correct Super-K limit (2024)**: τ_p(p → e⁺π⁰) > 1.6 × 10^34 years (Super-Kamiokande + Super-Kamiokande-Gd)

**Resolution - Replace BOTH to consistent value**:

**Line 1143 - Replace with**:
```html
<p style="margin-top: 1rem; font-size: 0.9rem; color: #666;"><em>Super-K limit (PDG 2024): $\tau_p(p \to e^+ \pi^0) > 1.6 \times 10^{34}$ years &mdash; PM prediction: $3.9 \times 10^{34}$ yr (2.4× bound)</em></p>
```

**Line 1850 - Replace with**:
```html
Super-Kamiokande + Gd bound (PDG 2024): $\tau_p > 1.6 \times 10^{34}$ yr. PM prediction is 2.4&times; the current bound, consistent and testable at Hyper-Kamiokande (target: $10^{36}$ yr sensitivity).
```

**Justification**: 1.67 × 10^34 vs 1.6 × 10^34 minor discrepancy; use PDG 2024 official value
**Priority**: MEDIUM - affects testability claim accuracy

---

## EDIT 7: References Section (After Line 1631)

**Current state**: Missing CODATA entry
**Location**: Between Polchinski reference (line 1632) and section closure (line 1633)

**New reference to ADD**:
```html
<li>NIST CODATA Task Group (2022). CODATA 2022 Recommended Values of Physical Constants. <em>National Institute of Standards and Technology</em>. https://physics.nist.gov/cuu/Constants/</li>
```

**Insert after line 1631, before closing `</ol>` tag**

**Justification**: CODATA is standard source for fundamental constants (ℏ, c, G_N)
**Note**: PDG 2024 entry already present at line 1631 (good)

---

## SUMMARY OF EDITS

| # | Value | Location | Action | Status |
|---|-------|----------|--------|--------|
| 1 | M_Z = 91.2 GeV | Line 1051 | Add PDG citation below | Ready |
| 2 | M_Pl = 2.435×10^18 GeV | Line 1084 | Add CODATA citation below | Ready |
| 3 | sin²θ_W = 0.23121 | Line 1055 | Verify citation | ✓ Complete |
| 4 | m_h = 125.1 GeV | Line 1592 | Inline citation in text | Ready |
| 5 | m_t = 172.7 GeV | Line 1253 | Verify citation | ✓ Complete |
| 6 | Super-K τ_p limit | Lines 1143, 1850 | Unify & update value | Ready |
| 7 | References | After line 1631 | Add CODATA entry | Ready |

---

## APPLICATION ORDER

1. **Add CODATA reference** (Edit 7) - Foundation for Edit 2
2. **Add/Fix Super-K limits** (Edit 6) - Two locations
3. **Add M_Pl citation** (Edit 2)
4. **Add M_Z citation** (Edit 1)
5. **Update Higgs citation** (Edit 4)
6. **Verify remaining citations** (Edits 3, 5)

---

## PDG 2024 VALUES FOR REFERENCE

Used in edits above:
- M_Z = 91.1876 ± 0.0021 GeV
- m_h = 125.09 ± 0.24 GeV
- m_t = 172.69 ± 0.30 GeV
- sin²θ_W = 0.23122 ± 0.00003
- τ_p(p → e⁺π⁰) > 1.6 × 10³⁴ years (Super-K)

CODATA 2022:
- M_Pl = √(ℏc/G_N) = 2.4351 × 10^18 GeV

---

## NOTES

- **NO derivations modified** - only citations added/verified
- **Paper values unchanged** - 2.435 vs 2.4351 rounds to same value
- **Citation style consistent** - matches existing PDG 2024 style
- **Inline format preserves readability** - gray text, 90% size, italics

---

**Generated**: 2025-12-18
**Based on**: HARDCODED_VALUES_AUDIT.md
**Ready for**: Editorial application
