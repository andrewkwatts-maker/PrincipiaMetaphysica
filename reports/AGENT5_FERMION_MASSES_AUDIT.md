# AGENT5: FERMION MASSES & YUKAWA PARAMETERS AUDIT

**Date:** 2025-12-15
**Task:** Compare OLD paper vs NEW paper vs fermion-sector.html for fermion mass derivations

---

## EXECUTIVE SUMMARY

**CRITICAL FINDING:** The NEW paper has SEVERELY DEGRADED fermion sector content compared to the OLD paper. Only 3 out of ~15 fermion masses have derivation boxes in the NEW paper.

### Migration Status
- **Top quark (m_t = 172.7 GeV):** ✅ MIGRATED (with derivation box)
- **Bottom quark (m_b = 4.18 GeV):** ✅ MIGRATED (with derivation box)
- **Tau lepton (m_tau = 1.777 GeV):** ✅ MIGRATED (with derivation box)
- **Charm quark (m_c):** ❌ MISSING (no derivation in NEW paper)
- **Strange quark (m_s):** ❌ MISSING (no derivation in NEW paper)
- **Up quark (m_u):** ❌ MISSING (no derivation in NEW paper)
- **Down quark (m_d):** ❌ MISSING (no derivation in NEW paper)
- **Electron (m_e):** ❌ MISSING (no derivation in NEW paper)
- **Muon (m_mu):** ❌ MISSING (no derivation in NEW paper)
- **CKM matrix elements:** ⚠️ PARTIAL (mentioned in fermion-sector.html but not in NEW paper)
- **Yukawa coupling ratios (y_b/y_t):** ✅ MIGRATED (in bottom mass derivation)
- **Yukawa matrix texture:** ❌ MISSING from NEW paper (exists in OLD paper and fermion-sector.html)
- **Mass hierarchy explanation:** ⚠️ PARTIAL (basic explanation present, detailed texture missing)

**Overall Grade: PARTIAL MIGRATION (20% complete)**

---

## DETAILED PARAMETER AUDIT

### 1. TOP QUARK MASS (m_t = 172.7 GeV)

**Status:** ✅ MIGRATED

**OLD Paper (principia-metaphysica-paper-old.html):**
- Location: Lines 22816-22938 (extensive discussion in fermion mass hierarchy section)
- Content: Described as part of numerical hierarchy m_t/m_e ~ 10^5
- Qualitative discussion of geometric localization: "Top quark (3rd gen): Δy_t ≈ 0 (localized near Higgs) ⇒ Y_t ≈ g_* ≈ 1"
- No standalone derivation box in OLD paper

**NEW Paper (principia-metaphysica-paper.html):**
- Location: Lines 943-959
- **Has dedicated derivation box:** "Derivation: Top Mass from G_2 Geometry"
- Derivation steps:
  1. Yukawa coupling y_t from dominant G_2 cycle intersection
  2. VEW from Section 5.5: v_EW = 173.97 GeV
  3. Mass formula: m_t = y_t × v/√2
  4. Intersection calculation yields y_t ≈ 1.0
  5. Result: m_t = 1.0 × 173.97/√2 = 172.7 GeV
- PDG comparison: "PDG 2024: m_t = 172.69 ± 0.30 GeV — exact agreement"
- Summary table (lines 1983-1987): Shows m_t = 172.7 GeV with <0.01% error

**fermion-sector.html:**
- Location: Lines 4023-4161 (detailed hierarchy discussion)
- Content: Extensive quantitative example showing top quark at Δy_t ≈ 0
- Shows Y_t ≈ g_* ≈ 1 from wavefunction overlap
- Part of larger Yukawa matrix texture derivation

**Assessment:** IMPROVED in NEW paper - now has explicit derivation box with step-by-step calculation. OLD paper only had qualitative discussion.

---

### 2. BOTTOM QUARK MASS (m_b = 4.18 GeV)

**Status:** ✅ MIGRATED

**OLD Paper:**
- Location: Lines 22816-22938 (no separate section for bottom)
- Not explicitly derived in standalone section
- Implied through Yukawa texture with ε suppression factors

**NEW Paper:**
- Location: Lines 961-976
- **Has dedicated derivation box:** "Derivation: Bottom Mass from G_2 Cycle Volumes"
- Derivation steps:
  1. Yukawa coupling from secondary G_2 cycle intersection: y_b = Vol(Σ_b)/Vol(Σ_t)
  2. Cycle volume ratio from TCS geometry: y_b/y_t ≈ 0.024
  3. Bottom Yukawa: y_b = 0.024 × 1.0 = 0.024
  4. Result: m_b = 0.024 × 173.97/√2 = 4.18 GeV
- PDG comparison: "PDG 2024: m_b(MS-bar) = 4.18 ± 0.03 GeV — exact agreement"
- Summary table (lines 1989-1993): Shows m_b = 4.18 GeV with <0.1% error

**fermion-sector.html:**
- Similar content as OLD paper (wavefunction overlap discussion)
- No standalone derivation box

**Assessment:** IMPROVED in NEW paper - now has explicit derivation box linking to G_2 cycle volumes. This is NEW content not present in OLD paper.

---

### 3. TAU LEPTON MASS (m_tau = 1.777 GeV)

**Status:** ✅ MIGRATED

**OLD Paper:**
- Location: Lines 22816-22938 (no separate tau section)
- Not explicitly derived
- Would be part of Yukawa texture if present

**NEW Paper:**
- Location: Lines 978-993
- **Has dedicated derivation box:** "Derivation: Tau Mass from Leptonic G_2 Cycles"
- Derivation steps:
  1. Lepton Yukawa coupling from coassociative 4-cycle intersections
  2. Geometric suppression: y_tau/y_t = (Vol(Σ_tau)/Vol(Σ_t))^(1/2)
  3. Tau Yukawa: y_tau ≈ 0.0102
  4. Result: m_tau = 0.0102 × 173.97/√2 = 1.777 GeV
- PDG comparison: "PDG 2024: m_tau = 1.77686 ± 0.00012 GeV — 0.01% error"
- Summary table (lines 1995-1999): Shows m_tau = 1.777 GeV with <0.01% error

**fermion-sector.html:**
- No standalone tau derivation
- Would be part of larger lepton discussion

**Assessment:** IMPROVED in NEW paper - completely new derivation box with explicit G_2 geometry link.

---

### 4. CHARM QUARK MASS (m_c ~ 1.27 GeV)

**Status:** ❌ MISSING

**OLD Paper:**
- Location: Lines 22846-22865
- **Content present:** "Charm quark (2nd gen): Δy_c ≈ 2L ⇒ Y_c ≈ g_* e^(-4λ) ≈ 10^(-2)"
- Part of quantitative example showing mass hierarchy
- Explained via geometric localization and wavefunction overlap

**NEW Paper:**
- **NOT FOUND:** No mention of charm quark mass derivation
- No derivation box
- Not in summary table (lines 1974-2000)

**fermion-sector.html:**
- Location: Lines 4055-4079
- **Content present:** "Charm quark (2nd gen): Δy_c ≈ 2L ⇒ Y_c ≈ g_* e^(-4λ) ≈ 10^(-2)"
- Same content as OLD paper

**Assessment:** REGRESSION - Charm mass derivation was present in OLD paper but DELETED from NEW paper. This is a significant loss of content.

---

### 5. STRANGE QUARK MASS (m_s ~ 95 MeV)

**Status:** ❌ MISSING

**OLD Paper:**
- Location: No explicit mention of strange quark mass value
- Would be part of down-type Yukawa matrix (mentioned at line 23204)
- Down-type quark texture mentioned but not fully detailed

**NEW Paper:**
- **NOT FOUND:** No mention of strange quark
- No derivation

**fermion-sector.html:**
- Location: Line 4605-4608
- **Brief mention:** "Down-type quarks: Similar structure with slightly different ε values"
- No explicit strange quark mass

**Assessment:** MISSING from all versions - strange quark mass never had a dedicated derivation.

---

### 6. UP QUARK MASS (m_u)

**Status:** ❌ MISSING from NEW paper

**OLD Paper:**
- Location: Lines 22867-22887
- **Content present:** "Up quark (1st gen): Δy_u ≈ 3L ⇒ Y_u ≈ g_* e^(-9λ) ≈ 10^(-5)"
- Part of quantitative hierarchy example
- Shows 5 orders of magnitude suppression from top

**NEW Paper:**
- **NOT FOUND:** No up quark mass derivation
- Not in summary table

**fermion-sector.html:**
- Location: Lines 4081-4104
- **Content present:** Same as OLD paper
- "Up quark (1st gen): Δy_u ≈ 3L ⇒ Y_u ≈ g_* e^(-9λ) ≈ 10^(-5)"

**Assessment:** REGRESSION - Up quark derivation DELETED from NEW paper.

---

### 7. DOWN QUARK MASS (m_d)

**Status:** ❌ MISSING

**OLD Paper:**
- Location: No explicit down quark mass derivation
- Mentioned in context of down-type Yukawa matrix (line 23204)

**NEW Paper:**
- **NOT FOUND:** No down quark mass

**fermion-sector.html:**
- Brief mention in down-type quark discussion (line 4605)
- No explicit derivation

**Assessment:** MISSING from all versions.

---

### 8. ELECTRON MASS (m_e)

**Status:** ❌ MISSING from NEW paper

**OLD Paper:**
- Location: Lines 22889-22909
- **Content present:** "Electron (1st gen lepton): Δy_e ≈ 3.5L ⇒ Y_e ≈ g_* e^(-12λ) ≈ 3×10^(-6)"
- Part of m_t/m_e ~ 10^5 hierarchy calculation
- Key reference for mass hierarchy: "m_t/m_e = Y_t/Y_e ≈ e^12 ≈ 1.6×10^5" (lines 22916-22936)

**NEW Paper:**
- **NOT FOUND:** No electron mass derivation
- Not in summary table

**fermion-sector.html:**
- Location: Lines 4106-4129
- **Content present:** Same as OLD paper
- Shows electron as most suppressed: Y_e ≈ 3×10^(-6)

**Assessment:** REGRESSION - Electron mass derivation (crucial for showing mass hierarchy) DELETED from NEW paper.

---

### 9. MUON MASS (m_mu)

**Status:** ❌ MISSING

**OLD Paper:**
- Location: No explicit muon mass derivation
- Would be intermediate between electron and tau

**NEW Paper:**
- **NOT FOUND:** No muon mass

**fermion-sector.html:**
- No explicit muon derivation

**Assessment:** MISSING from all versions.

---

### 10. CKM MATRIX ELEMENTS

**Status:** ⚠️ PARTIAL (not in NEW paper, present in fermion-sector.html)

**CKM Parameters:**
- |V_ud| ~ 1 (diagonal)
- |V_us| ~ ε ~ 0.22 (Cabibbo angle)
- |V_ub| ~ ε^3 (small)
- |V_cb| ~ ε^2 ~ 0.04

**OLD Paper:**
- Location: Lines 23182-23199
- **Content:** "CKM mixing angles: V_us ~ ε, V_cb ~ ε^2, V_ub ~ ε^3"
- Shows connection to Yukawa matrix texture through ε ≈ 0.05
- Wolfenstein parameterization mentioned at lines 26696-26857
- Full CKM discussion in proton decay section

**NEW Paper:**
- **NOT FOUND:** No CKM matrix derivation in main paper
- No mention of |V_ud|, |V_us|, |V_cb|, |V_ub| with values

**fermion-sector.html:**
- Location: Lines 4578-4602
- **Content present:** "CKM mixing angles: V_us ~ ε, V_cb ~ ε^2, V_ub ~ ε^3"
- Same structure as OLD paper
- Detailed discussion in proton decay section (lines 9110-9303)

**Assessment:** REGRESSION - CKM matrix content removed from NEW paper. This is especially problematic since CKM is mentioned in beginners-guide.html as a key prediction.

---

### 11. YUKAWA COUPLING RATIOS

**Status:** ✅ MIGRATED (y_b/y_t ratio only)

**OLD Paper:**
- Location: Lines 22940-23199
- **Yukawa Matrix Texture:** Full 3×3 texture shown with ε suppression factors
- Up-type quark matrix (lines 23060-23124):
  ```
  Y_u ~ g_* × [ε^4  ε^3  ε^2]
                [ε^3  ε^2  ε  ]
                [ε^2  ε    1  ]
  ```
- Quantitative: ε ≈ 0.05 from Cabibbo angle λ_C
- Ratios: Y_u : Y_c : Y_t ≈ ε^4 : ε^2 : 1 ≈ 10^(-5) : 10^(-2) : 1

**NEW Paper:**
- Location: Lines 970-971 (bottom mass derivation)
- **Content:** "Cycle volume ratio from TCS geometry: y_b/y_t ≈ 0.024"
- Only shows single ratio for bottom/top
- No full Yukawa matrix texture

**fermion-sector.html:**
- Location: Lines 4163-4517
- **Full Yukawa Matrix Texture:** Complete 3×3 texture with interactive tooltips
- Same structure as OLD paper
- Shows all generation ratios

**Assessment:** PARTIAL MIGRATION - Only y_b/y_t ratio migrated to NEW paper. Full Yukawa texture matrix DELETED.

---

### 12. YUKAWA GEOMETRY (G2 Cycle Intersections)

**Status:** ✅ PARTIALLY MIGRATED

**OLD Paper:**
- Location: Lines 22285-22701
- **Comprehensive discussion:**
  - "Yukawa couplings from wavefunction overlaps on K_Pneuma" (line 22346)
  - "b_3 = 24 Co-associative Cycles Control Yukawa Textures" (line 22369)
  - Full derivation of overlap integrals Y_ij = g ∫_K χ_i^† χ_j Φ
  - Connection to G2 geometry and 24 associative 3-cycles

**NEW Paper:**
- Location: Lines 949-993 (derivation boxes for t, b, tau)
- **Content:**
  - Top: "Yukawa coupling y_t from dominant G_2 cycle intersection"
  - Bottom: "Yukawa coupling from secondary G_2 cycle intersection: y_b = Vol(Σ_b)/Vol(Σ_t)"
  - Tau: "Lepton Yukawa coupling from coassociative 4-cycle intersections"
  - Geometric suppression formula for leptons: y_tau/y_t = (Vol(Σ_tau)/Vol(Σ_t))^(1/2)

**fermion-sector.html:**
- Location: Lines 3086-3880
- **Extensive content:** Full wavefunction overlap formalism
- Interactive formulas with tooltips
- Detailed explanation of how 24 cycles determine Yukawa couplings

**Assessment:** PARTIAL - NEW paper has basic G_2 cycle connection but lacks detailed wavefunction overlap mathematics present in OLD paper.

---

### 13. MASS HIERARCHY EXPLANATION

**Status:** ⚠️ PARTIAL

**OLD Paper:**
- Location: Lines 22528-22938
- **Comprehensive section:** "Numerical Derivation: m_t/m_e ~ 10^5"
- Quantitative example showing all generations:
  - Top: Y_t ≈ 1 (Δy_t ≈ 0)
  - Charm: Y_c ≈ 10^(-2) (Δy_c ≈ 2L)
  - Up: Y_u ≈ 10^(-5) (Δy_u ≈ 3L)
  - Electron: Y_e ≈ 3×10^(-6) (Δy_e ≈ 3.5L)
- Explicit calculation: m_t/m_e = e^12 ≈ 1.6×10^5
- Full Yukawa matrix texture with Froggatt-Nielsen mechanism
- Connection to geometric localization on K_Pneuma

**NEW Paper:**
- Location: Lines 943-993 (three derivation boxes only)
- **Limited content:**
  - Shows top (y_t ≈ 1.0), bottom (y_b ≈ 0.024), tau (y_tau ≈ 0.0102)
  - Ratios: y_b/y_t ≈ 0.024, y_tau/y_t ≈ 0.0102
  - No explanation of why these specific ratios
  - No lighter fermion masses (charm, up, electron, muon)
  - No explicit m_t/m_e calculation

**fermion-sector.html:**
- Location: Lines 4008-4162
- **Full hierarchy:** Same comprehensive content as OLD paper
- All 4 mass examples (top, charm, up, electron)
- Explicit m_t/m_e ~ 10^5 calculation

**Assessment:** DEGRADATION - NEW paper only shows 3 heavy fermions. Missing the crucial 5-order-of-magnitude hierarchy explanation that was in OLD paper.

---

## CRITICAL GAPS IN NEW PAPER

### Missing Derivation Boxes

The NEW paper should have derivation boxes for ALL major fermion masses, linking each to G2 geometry:

1. ❌ **Charm quark (m_c ~ 1.27 GeV)** - Was in OLD paper, now missing
2. ❌ **Strange quark (m_s ~ 95 MeV)** - Never had dedicated section
3. ❌ **Up quark (m_u ~ 2.2 MeV)** - Was in OLD paper, now missing
4. ❌ **Down quark (m_d ~ 4.7 MeV)** - Never had dedicated section
5. ❌ **Electron (m_e ~ 0.511 MeV)** - Was in OLD paper, now missing (CRITICAL LOSS)
6. ❌ **Muon (m_mu ~ 105.7 MeV)** - Never had dedicated section

### Missing Yukawa Matrix Content

The OLD paper had a beautiful Yukawa matrix texture section showing:
- Full 3×3 up-type quark matrix with ε suppression factors
- Connection to Cabibbo angle: ε ≈ λ_C^(1/2) ≈ 0.05
- Froggatt-Nielsen mechanism as geometric origin
- Mass ratios: m_u : m_c : m_t ≈ ε^4 : ε^2 : 1

**Status in NEW paper:** ❌ COMPLETELY DELETED

This should be restored, preferably as a dedicated section with derivation boxes.

### Missing CKM Matrix

The OLD paper showed how CKM mixing angles emerge from Yukawa texture:
- V_us ~ ε (Cabibbo angle)
- V_cb ~ ε^2
- V_ub ~ ε^3

**Status in NEW paper:** ❌ COMPLETELY DELETED

This is critical because:
1. Beginners guide claims CKM matrix is a prediction
2. Proton decay branching ratios depend on CKM (mentioned in predictions)
3. Connection to geometric origin should be explicit

---

## COMPARISON: DERIVATION BOX COVERAGE

### OLD Paper Derivation Boxes
The OLD paper didn't use "derivation boxes" as styled elements, but had comprehensive derivations:
- ✅ Mass hierarchy (m_t/m_e ~ 10^5): Full quantitative example
- ✅ Yukawa matrix texture: Complete 3×3 matrices with ε factors
- ✅ Wavefunction overlap formalism: Full mathematical framework
- ✅ Connection to 24 G2 cycles: Explicit topology link
- ✅ Froggatt-Nielsen mechanism: Geometric UV completion

### NEW Paper Derivation Boxes
Only 3 heavy fermion masses:
- ✅ Top quark (m_t = 172.7 GeV)
- ✅ Bottom quark (m_b = 4.18 GeV)
- ✅ Tau lepton (m_tau = 1.777 GeV)

Missing derivation boxes for:
- ❌ Charm, strange, up, down quarks
- ❌ Electron, muon
- ❌ Yukawa matrix texture
- ❌ CKM matrix elements
- ❌ Mass hierarchy explanation

### fermion-sector.html Derivation Coverage
- ✅ Full wavefunction overlap formalism (lines 3086-3880)
- ✅ Mass hierarchy example with 4 fermions (lines 4008-4162)
- ✅ Yukawa matrix texture (lines 4163-4517)
- ✅ CKM mixing angles (lines 4578-4602)
- ✅ Froggatt-Nielsen connection (lines 4610-4710)

**Conclusion:** fermion-sector.html has the most complete content, but NEW paper is severely lacking.

---

## NUMERICAL VALUES: OLD vs NEW

| Parameter | OLD Paper | NEW Paper | fermion-sector.html | Status |
|-----------|-----------|-----------|---------------------|--------|
| m_t | Qualitative (Y_t ≈ 1) | 172.7 GeV (explicit) | Qualitative | ✅ IMPROVED |
| m_b | Not explicit | 4.18 GeV (explicit) | Not explicit | ✅ NEW |
| m_tau | Not explicit | 1.777 GeV (explicit) | Not explicit | ✅ NEW |
| m_c | Y_c ~ 10^(-2) | ❌ MISSING | Y_c ~ 10^(-2) | ❌ DELETED |
| m_s | Not present | ❌ MISSING | Brief mention | ❌ MISSING |
| m_u | Y_u ~ 10^(-5) | ❌ MISSING | Y_u ~ 10^(-5) | ❌ DELETED |
| m_d | Not explicit | ❌ MISSING | Not explicit | ❌ MISSING |
| m_e | Y_e ~ 3×10^(-6) | ❌ MISSING | Y_e ~ 3×10^(-6) | ❌ DELETED |
| m_mu | Not present | ❌ MISSING | Not present | ❌ MISSING |
| y_b/y_t | From texture | 0.024 (explicit) | From texture | ✅ IMPROVED |
| y_tau/y_t | Not explicit | 0.0102 (explicit) | Not explicit | ✅ NEW |
| V_us | ~ ε ~ 0.22 | ❌ MISSING | ~ ε | ❌ DELETED |
| V_cb | ~ ε^2 ~ 0.04 | ❌ MISSING | ~ ε^2 | ❌ DELETED |
| V_ub | ~ ε^3 | ❌ MISSING | ~ ε^3 | ❌ DELETED |
| ε (texture param) | 0.05 | ❌ MISSING | 0.05 | ❌ DELETED |

---

## G2 GEOMETRY LINKS

### How Many Fermion Masses Link to G2 Cycles?

**Requirement:** ALL quark and lepton masses should have derivation boxes linking to G2 geometry (24 associative 3-cycles).

**NEW Paper Status:**

✅ **LINKED TO G2 (3 fermions):**
1. Top quark: "Yukawa coupling y_t from dominant G_2 cycle intersection"
2. Bottom quark: "Yukawa coupling from secondary G_2 cycle intersection: y_b = Vol(Σ_b)/Vol(Σ_t)"
3. Tau lepton: "Lepton Yukawa coupling from coassociative 4-cycle intersections"

❌ **NOT LINKED (9+ fermions):**
1. Charm quark - MISSING
2. Strange quark - MISSING
3. Up quark - MISSING
4. Down quark - MISSING
5. Electron - MISSING
6. Muon - MISSING
7. First-generation neutrinos (m_1, m_2, m_3) - Has seesaw derivation but not explicit G2 cycle link

**Coverage: 3/12 fermion masses = 25%**

**OLD Paper Status:**
- No explicit "derivation boxes" but has comprehensive wavefunction overlap discussion
- Shows how 24 G2 cycles control all Yukawa textures (line 22369)
- Provides geometric mechanism for full mass hierarchy
- Links entire Yukawa matrix to K_Pneuma geometry

**fermion-sector.html Status:**
- Full wavefunction overlap formalism showing how all masses emerge from G2 geometry
- Comprehensive discussion of 24 associative 3-cycles
- Yukawa matrix texture explicitly linked to geometric localization

---

## RECOMMENDATIONS

### CRITICAL (Must Fix)

1. **Add derivation boxes for light quarks:**
   - Charm quark (m_c ~ 1.27 GeV): Link to 2nd-generation G2 cycle
   - Strange quark (m_s ~ 95 MeV): Link to down-type G2 cycles
   - Up quark (m_u ~ 2.2 MeV): Link to 1st-generation G2 cycle, show 5-order suppression
   - Down quark (m_d ~ 4.7 MeV): Link to down-type G2 cycles

2. **Add derivation boxes for leptons:**
   - Electron (m_e ~ 0.511 MeV): CRITICAL - this is needed to show m_t/m_e ~ 10^5 hierarchy
   - Muon (m_mu ~ 105.7 MeV): Link to 2nd-generation leptonic cycles

3. **Restore Yukawa matrix texture section:**
   - Add full 3×3 up-type quark Yukawa matrix with ε factors
   - Show ε ≈ 0.05 from geometric localization
   - Explain Froggatt-Nielsen mechanism as geometric origin
   - Link to 24 associative 3-cycles explicitly

4. **Add CKM matrix derivation:**
   - Show V_us ~ ε, V_cb ~ ε^2, V_ub ~ ε^3
   - Link to Yukawa texture
   - Explain geometric origin from wavefunction overlap

5. **Restore mass hierarchy explanation:**
   - Add explicit m_t/m_e ~ 10^5 calculation
   - Show all intermediate masses (top → charm → up, tau → muon → electron)
   - Explain geometric localization mechanism with positions on K_Pneuma

### HIGH PRIORITY (Should Add)

6. **Add comprehensive Yukawa coupling section:**
   - y_t ≈ 1.0 (already present)
   - y_c/y_t ≈ 10^(-2) from ε^2 suppression
   - y_u/y_t ≈ 10^(-5) from ε^4 suppression
   - y_tau/y_t ≈ 0.0102 (already present)
   - y_mu/y_t (needs to be added)
   - y_e/y_t ≈ 3×10^(-6) from ε^4-ε^5 suppression

7. **Link all masses to 24 G2 cycles:**
   - Add explicit statement: "The 24 associative 3-cycles (b_3 = 24) determine all 12 fermion masses"
   - Show how different cycles correspond to different generations
   - Explain volume ratios between cycles

### MEDIUM PRIORITY (Nice to Have)

8. **Add interactive Yukawa matrix visualization:**
   - Similar to what exists in fermion-sector.html
   - Hoverable elements showing geometric origin of each matrix element

9. **Add comparison table:**
   - All fermion masses: PM prediction vs PDG 2024
   - All Yukawa ratios: geometric prediction vs measured
   - CKM elements: PM prediction vs experiment

---

## MIGRATION CHECKLIST

### What MUST be migrated from OLD paper or fermion-sector.html:

- [ ] Charm quark mass derivation (from OLD paper lines 22846-22865)
- [ ] Up quark mass derivation (from OLD paper lines 22867-22887)
- [ ] Electron mass derivation (from OLD paper lines 22889-22909)
- [ ] m_t/m_e ~ 10^5 calculation (from OLD paper lines 22916-22936)
- [ ] Yukawa matrix texture (from OLD paper lines 22940-23124)
- [ ] CKM matrix elements (from OLD paper lines 23182-23199)
- [ ] Froggatt-Nielsen mechanism (from fermion-sector.html lines 4610-4710)
- [ ] Wavefunction overlap formalism (from fermion-sector.html lines 3086-3880)
- [ ] Connection to 24 G2 cycles (from OLD paper line 22369)

### What is already good in NEW paper:

- [x] Top quark derivation box
- [x] Bottom quark derivation box
- [x] Tau lepton derivation box
- [x] y_b/y_t ratio
- [x] y_tau/y_t ratio
- [x] G2 cycle intersection language
- [x] Neutrino seesaw mechanism

---

## CONCLUSION

The NEW paper has made EXCELLENT progress on the 3 heaviest fermions (top, bottom, tau) with beautiful derivation boxes linking to G2 geometry. However, it has **REGRESSED** significantly by deleting:

1. All light quark masses (charm, up)
2. All charged lepton masses except tau (electron, muon)
3. Complete Yukawa matrix texture
4. CKM matrix derivation
5. Mass hierarchy explanation (m_t/m_e ~ 10^5)

**Current coverage: 3 out of ~12-15 fermion parameters have derivation boxes (20%)**

The fermion-sector.html file contains all the missing content and should be used as the source for restoration. The OLD paper provides additional context and numerical examples.

**PRIORITY:** Add derivation boxes for electron and charm masses at minimum. These are critical for showing the 5-order-of-magnitude mass hierarchy that is a key feature of the framework.

**Grade: D+ (Partial Migration, Major Gaps)**

---

## FILES AUDITED

1. `h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper-old.html`
   - Lines 22285-23199: Comprehensive Yukawa coupling and mass hierarchy section
   - Lines 26690-26857: CKM matrix and proton decay

2. `h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html`
   - Lines 943-993: Top, bottom, tau mass derivations
   - Lines 1974-2000: Summary table

3. `h:\Github\PrincipiaMetaphysica\sections\fermion-sector.html`
   - Lines 3086-3880: Wavefunction overlap formalism
   - Lines 4008-4710: Mass hierarchy, Yukawa texture, Froggatt-Nielsen

---

**Audit completed: 2025-12-15**
**Next steps: Restore missing fermion mass derivations to NEW paper**
