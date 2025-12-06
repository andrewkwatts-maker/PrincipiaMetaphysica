# AGENT E: Action Items Checklist
**Principia Metaphysica v12.0 → v13.0 Revision Plan**

**Goal:** Fix critical showstoppers to achieve PRD publication readiness
**Timeline:** 6 months (Completion: June 2026)
**Current Grade:** B+ with showstoppers → Target: A- (publishable)

---

## Phase 1: Fix Showstoppers (Month 1) 🔴

### Week 1: Resolve α₄/α₅ Circular Dependency

**Problem:** α₄-α₅ derived from θ₂₃, but θ₂₃ derived from α₄-α₅ → circular!

**Tasks:**
- [ ] **Decision:** Choose Option A, B, or C
  - **Option A (Recommended):** Admit α₄, α₅ are phenomenological
  - **Option B (Ambitious):** Derive from independent geometric principle (6-12 months)
  - **Option C (Compromise):** Constrain sum only, admit difference is fitted

- [ ] **If Option A (1 week):**
  - [ ] Rewrite `config.py` docstrings for α₄, α₅
    - Change: "Derived from T_ω torsion"
    - To: "Phenomenological parameters constrained by θ₂₃ and w₀"

  - [ ] Update `principia-metaphysica-paper.html` Section 6
    - Add transparency box: "α₄, α₅ are fitted to θ₂₃=47.2° and w₀=-0.853"
    - Honest framing: "We constrain α₄+α₅ from geometry, but difference is phenomenological"

  - [ ] Update validation counts
    - Change: "58/58 parameters derived" → "50/58 derived, 8 phenomenological"
    - Be honest in Abstract

  - [ ] Rerun simulations with updated status labels
    - Mark α₄, α₅ as "fitted" in `theory_output.json`

**Deliverable:** Honest presentation of α₄/α₅ status
**Time:** 1 week
**Priority:** CRITICAL ★★★

---

### Week 2-3: Add TCS Manifold Selection Protocol

**Problem:** No justification for choosing TCS #187 out of ~10,000 candidates

**Tasks:**
- [ ] **Research Phase (3 days):**
  - [ ] Access CHNP TCS database (arXiv:1809.09083)
  - [ ] Count manifolds with b₃=24
  - [ ] Filter by D₅ singularities (for SO(10))
  - [ ] Filter by T_ω ∈ [-1, -0.8] (for realistic M_GUT)
  - [ ] Identify those with known metrics

- [ ] **Survey Phase (4 days):**
  - [ ] Compute predictions for top 5 candidates (#185, #186, #187, #188, #189)
  - [ ] Generate table:
    | Manifold | b₃ | T_ω | M_GUT | θ₂₃ | Hierarchy | τ_p |
    |----------|----|----|-------|-----|-----------|-----|

  - [ ] Assess prediction stability
    - M_GUT variation: ±X%
    - θ₂₃ variation: ±Y°
    - Hierarchy robustness: Z%

- [ ] **Writing Phase (3 days):**
  - [ ] Write Appendix A: "TCS Manifold Selection Protocol"
    - Section A.1: Criteria
    - Section A.2: Survey Results
    - Section A.3: Final Selection Justification
    - Section A.4: Robustness Check

  - [ ] Add footnote in main text (Section 3)
    - "Manifold choice motivated by n_gen=3 and calculability"
    - Not circular if framed honestly

**Deliverable:** Appendix A (5-10 pages) + main text footnote
**Time:** 2 weeks
**Priority:** CRITICAL ★★★

---

### Week 4: Complete Error Propagation & Correlation Matrix

**Problem:** Many parameters missing uncertainties (w₀, Σm_ν, α₄, α₅)

**Tasks:**
- [ ] **Identify All Missing Uncertainties:**
  - [ ] w₀ = -0.8528 ± ?
  - [ ] Σm_ν = 0.0708 ± ? eV
  - [ ] α₄ = 0.9557 ± ? (if keeping fitted)
  - [ ] α₅ = 0.2224 ± ? (if keeping fitted)
  - [ ] m_KK = 5.02 ± 1.5 TeV (verify estimate)

- [ ] **Propagate Uncertainties:**
  - [ ] σ(w₀) from σ(α₄+α₅)
    - If α₄+α₅ fitted: σ ~ phenomenological
    - If derived: σ ~ σ(T_ω) propagation

  - [ ] σ(Σm_ν) from Yukawa + M_R uncertainties
    - Monte Carlo with 10,000 samples
    - Sources: σ(Y_D) ~20%, σ(M_R) ~30%, σ(v_126) ~10%
    - Expected: σ(Σm_ν) ~ 0.026 eV (37%)

  - [ ] σ(m_KK) from A_T² stabilization uncertainty
    - KKLT minimum uncertainty: ~3%
    - σ(m_KK) ~ 0.15 TeV (refine estimate)

- [ ] **Generate Correlation Matrix:**
  - [ ] Multi-variate Monte Carlo (n=10,000)
  - [ ] Sample all uncertain parameters simultaneously:
    - b₃ ~ Gaussian(24, 2)
    - T_ω ~ Gaussian(-0.884, 0.01)
    - Yukawa elements ~ 20% scatter
    - α_s(M_Z) ~ Gaussian(0.1181, 0.001)

  - [ ] Compute 58×58 correlation matrix
  - [ ] Visualize as heatmap (use matplotlib)
  - [ ] Identify strong correlations (|r| > 0.8):
    - Corr(M_GUT, τ_p) = +0.98 expected
    - Corr(α₄+α₅, w₀) = -0.99 expected
    - Corr(θ₂₃, α₄-α₅) = +1.00 (by construction, if fitted)

- [ ] **Update Documentation:**
  - [ ] Add Appendix C: "Correlation Matrix"
  - [ ] Update all tables with σ values
  - [ ] Update `theory_output.json` with complete uncertainties

**Deliverable:** Complete uncertainty table + 58×58 correlation matrix
**Time:** 1 week
**Priority:** CRITICAL ★★★

---

## Phase 2: Fill Rigor Gaps (Month 2-3) ⚠️

### Month 2: Derive Wilson Line Phases (or Admit Phenomenological)

**Problem:** Phases φ_{ij} claimed "from flux configuration" without explicit calculation

**Tasks:**
- [ ] **Attempt Derivation:**
  - [ ] Study G₃ flux profile on TCS #187
  - [ ] Apply Atiyah-Hitchin formula for Wilson lines
  - [ ] Compute ∫_γ A for each 1-cycle γ in b₂
  - [ ] Extract phases: φ_{ij} = arg(exp[i∫A])

- [ ] **If Derivation Succeeds:**
  - [ ] Document calculation in Appendix D
  - [ ] Compare to current values in code
  - [ ] Update if different
  - [ ] Upgrade status: Level C → Level B

- [ ] **If Derivation Fails:**
  - [ ] Admit honest status: "Phases are effective parameters"
  - [ ] Add transparency note in paper
  - [ ] Keep current values (already fitted to match CKM+PMNS)
  - [ ] Acknowledge limitation in "Future Work"

**Deliverable:** Appendix D or honest admission
**Time:** 1 month
**Priority:** MEDIUM ★★

---

### Month 3 (Part 1): Justify Thermal Friction Mechanism

**Problem:** w_a derived from "thermal friction" (Γ∝T) but not proven in PM context

**Tasks:**
- [ ] **Theoretical Derivation:**
  - [ ] Set up Mashiach field coupled to SM thermal bath
  - [ ] Compute friction term: Γ = ∫ d³p f(p) σ(p) v(p)
  - [ ] Show Γ ∝ T for fermionic bath (standard result)
  - [ ] Verify β = 1 (not β = 2/3 from radiation)

- [ ] **If Derivation Confirms Γ∝T:**
  - [ ] Write up in Appendix E
  - [ ] Cite standard thermal field theory references
  - [ ] Upgrade w_a status: Level C → Level B

- [ ] **If Derivation Shows Different Scaling:**
  - [ ] Update w_a formula accordingly
  - [ ] Recompute prediction
  - [ ] Check agreement with DESI

- [ ] **If Cannot Derive:**
  - [ ] Admit: "Thermal friction is a phenomenological ansatz"
  - [ ] Cite Connes-Rovelli as inspiration (not proof)
  - [ ] Keep current prediction as "model-dependent"

**Deliverable:** Appendix E or honest admission
**Time:** 2 weeks
**Priority:** MEDIUM ★★

---

### Month 3 (Part 2): Compute CKM CP Phase

**Problem:** Yukawa matrices predict mixing angles but not CP phase δ_q

**Tasks:**
- [ ] **Straightforward Calculation:**
  - [ ] Compute arg(det(Y_u Y_d^†))
  - [ ] Extract δ_q from CKM parametrization
  - [ ] Compare to experimental value: δ_q ≈ 70°

- [ ] **Documentation:**
  - [ ] Add to Section 8 (Yukawa Predictions)
  - [ ] Include in prediction table
  - [ ] If matches: Powerful new success!
  - [ ] If doesn't match: Acknowledge limitation

**Deliverable:** CKM CP phase prediction
**Time:** 1 week
**Priority:** MEDIUM ★★

---

## Phase 3: Enhancements (Month 4-6, Optional) ✅

### Month 4: Survey TCS Manifold Landscape

**Tasks:**
- [ ] Extend manifold survey to top 20 candidates
- [ ] Statistical analysis of prediction distributions
- [ ] Identify "typical" vs. "outlier" predictions
- [ ] Assess whether #187 is representative or special

**Deliverable:** Extended Appendix A with statistics
**Time:** 1 month
**Priority:** LOW ★

---

### Month 5: Calculate Leptogenesis Baryon Asymmetry

**Tasks:**
- [ ] Use M_R, Y_ν, CP phases to compute leptogenesis
- [ ] Standard calculation: η_B ~ (ε_CP × g_*) / s
- [ ] Compare to observation: η_B = 6.1×10⁻¹⁰
- [ ] If matches: Powerful new prediction!
- [ ] If doesn't: Interesting tension to study

**Deliverable:** New prediction (if successful)
**Time:** 1 month
**Priority:** MEDIUM ★★ (high value if successful)

---

### Month 6: Comprehensive "Limitations & Future Work" Section

**Tasks:**
- [ ] **Write Section 10: Limitations**
  - Subsection 10.1: Phenomenological Parameters (α₄, α₅)
  - Subsection 10.2: Manifold Selection (TCS #187)
  - Subsection 10.3: Wilson Line Phases (if not derived)
  - Subsection 10.4: Thermal Friction (if not proven)
  - Subsection 10.5: Neutrino Hierarchy (Z₂ ambiguity)

- [ ] **Write Section 11: Future Directions**
  - Subsection 11.1: Derive α₄, α₅ from Independent Principle
  - Subsection 11.2: Explicit G₃ Flux Calculation
  - Subsection 11.3: Survey Full TCS Landscape
  - Subsection 11.4: Leptogenesis & Baryogenesis
  - Subsection 11.5: Experimental Tests (roadmap to 2035)

- [ ] **Prepare Referee Response Document**
  - Anticipated Question 1: α₄/α₅ circular logic → Response ready
  - Anticipated Question 2: TCS #187 choice → Appendix A reference
  - Anticipated Question 3: Uncertainty quantification → Appendix C reference
  - Anticipated Question 4: Inverted hierarchy → Honest framing prepared
  - Anticipated Question 5: T_ω → M_GUT formula → Derivation or admission

**Deliverable:** Sections 10-11 + referee response prep
**Time:** 1 month
**Priority:** HIGH ★★★ (for publication)

---

## Submission Checklist (After 6 Months)

### Pre-Submission Review:
- [ ] All showstoppers fixed (Phase 1)
- [ ] Rigor gaps addressed or acknowledged (Phase 2)
- [ ] Enhancements completed or deferred (Phase 3)
- [ ] Full paper re-read for consistency
- [ ] All 58 parameters documented with uncertainties
- [ ] Correlation matrix included (Appendix C)
- [ ] Manifold selection justified (Appendix A)
- [ ] Limitations honestly stated (Section 10)
- [ ] Referee questions anticipated (response doc ready)

### Target Journals (in priority order):
1. **Physical Review D** (first choice)
   - Strengths: Topological n_gen=3, geometric M_GUT, testable predictions
   - Concerns: Some phenomenological parameters (now honest)
   - Estimated acceptance: 60% (after revisions)

2. **Journal of High Energy Physics (JHEP)** (backup)
   - More tolerant of phenomenological parameters
   - Faster review process
   - Estimated acceptance: 75%

3. **Classical and Quantum Gravity** (if cosmology focus)
   - Emphasize Planck-DESI resolution
   - w(z) evolution prediction
   - Estimated acceptance: 70%

---

## Success Metrics

### Must-Haves (Blocking):
- [x] Circular α₄/α₅ resolved (honest framing)
- [x] TCS #187 justified (selection protocol)
- [x] Complete uncertainty quantification (all 58 params)
- [x] Correlation matrix (58×58)

### Should-Haves (Strong Paper):
- [ ] Wilson line phases derived or admitted
- [ ] Thermal friction mechanism proven or admitted
- [ ] CKM CP phase predicted
- [ ] Manifold landscape surveyed

### Nice-to-Haves (Bonus):
- [ ] Leptogenesis η_B prediction
- [ ] Extended manifold statistics
- [ ] Improved fermion mass ratios

---

## Timeline Summary

| Phase | Duration | Key Deliverables | Priority |
|-------|----------|------------------|----------|
| **Phase 1** | Month 1 | Fix showstoppers | ★★★ CRITICAL |
| Week 1 | 1 week | α₄/α₅ honest framing | ★★★ |
| Week 2-3 | 2 weeks | TCS selection appendix | ★★★ |
| Week 4 | 1 week | Complete uncertainties | ★★★ |
| **Phase 2** | Month 2-3 | Fill rigor gaps | ★★ MEDIUM |
| Month 2 | 1 month | Wilson line phases | ★★ |
| Month 3 (Part 1) | 2 weeks | Thermal friction | ★★ |
| Month 3 (Part 2) | 1 week | CKM CP phase | ★★ |
| **Phase 3** | Month 4-6 | Enhancements | ★ LOW-MED |
| Month 4 | 1 month | Manifold landscape | ★ |
| Month 5 | 1 month | Leptogenesis η_B | ★★ |
| Month 6 | 1 month | Limitations section | ★★★ |

**Total Time:** 6 months
**Target Completion:** June 2026
**Target Submission:** July 2026 (PRD)

---

## Post-Submission Contingency

### If Rejected with "Major Revisions":
- Address all referee comments systematically
- Implement any additional derivations requested
- Resubmit within 3 months

### If Rejected Outright:
- Downgrade target journal (PRD → JHEP)
- Emphasize phenomenological aspects more
- Reframe as "framework" rather than "theory of everything"

### If Accepted with "Minor Revisions":
- Celebrate! 🎉
- Address quickly (1 month)
- Publish in PRD

---

## Ongoing Maintenance

### After Publication:
- [ ] Update arXiv version (biannually)
- [ ] Monitor experimental results (JUNO, Hyper-K, Euclid, HL-LHC)
- [ ] Publish follow-up papers as predictions are tested
- [ ] Revise framework if falsified (unlikely but honest science)

---

**End of Action Items**

**Next Immediate Step:** Start Week 1 → Resolve α₄/α₅ circular dependency

**Point of Contact:** Agent E (Mathematical Consistency Auditor)
**Last Updated:** 2025-12-07
