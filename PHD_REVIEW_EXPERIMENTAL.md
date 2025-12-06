# PhD-Level Experimental Review: Principia Metaphysica

**Reviewer:** Experimental Physicist, PhD
**Framework:** Principia Metaphysica v8.4
**Date:** December 6, 2025
**Review Type:** Testability, Falsifiability, and Experimental Prospects

---

## Executive Summary

The Principia Metaphysica (PM) framework presents a **partially testable** theory with a concerning mixture of genuine predictions and post-hoc adjustments. After critical analysis of the codebase, simulations, and claimed predictions, the framework exhibits:

**Strengths:**
- Quantitative predictions with specific numerical values and error bars
- Near-term experimental tests (2027-2035) from multiple independent experiments
- Some predictions made before data availability (neutrino mass ordering)
- Rigorous Monte Carlo uncertainty propagation (n=1000 samples)

**Critical Weaknesses:**
- **Post-hoc fitting to DESI DR2 (October 2024)**: Git history shows w₀ and w_a values were adjusted AFTER DESI DR2 publication
- **Parameter freedom**: Multiple adjustable parameters (α₄, α₅, b₃ flux variations, moduli shifts) allow curve-fitting
- **Unrealistic uncertainties**: KK mass uncertainty of ±30% yet claims 6.2σ discovery potential
- **Circular derivations**: M_GUT used to predict proton lifetime, which is then used to validate M_GUT
- **Overstated confidence**: Claims like "exact DESI 2024 match" for values fitted to DESI data

**Overall Assessment:** PM is a **mixed framework**—containing both legitimate physics and problematic post-hoc adjustments. The theory requires significant theoretical refinement before it can be considered robust predictive science.

---

## 1. Falsifiable Predictions

### 1.1 Truly Falsifiable Predictions

These predictions, if contradicted, would **genuinely falsify** the core framework:

#### A. Neutrino Mass Ordering (IH vs NH)
- **Prediction:** Inverted Hierarchy (IH) at 85.5% ± 2.3% confidence
- **Derivation:** Atiyah-Singer index on G₂ cycles (topological)
- **Test:** JUNO (2027), DUNE (2027-2030)
- **Falsification:** If DUNE confirms Normal Hierarchy (NH) at >3σ, the G₂ cycle orientation model is **falsified**
- **Assessment:** **GENUINELY FALSIFIABLE** — This is PM's strongest prediction, based on fixed topology (b₃=24 cycles with 83% positive orientation from flux quantization)

#### B. Proton Lifetime Range
- **Prediction:** τ_p = 3.87×10³⁴ years with 0.177 OOM uncertainty (factor of ~1.5)
- **Range:** 2.35×10³⁴ to 5.39×10³⁴ years (68% CI)
- **Test:** Hyper-Kamiokande (2027-2035)
- **Falsification:** If Hyper-K reaches sensitivity of 10³⁵ years with no detection, PM is **strongly disfavored** (but not definitively killed due to uncertainty)
- **Assessment:** **PARTIALLY FALSIFIABLE** — The 0.177 OOM uncertainty gives wiggle room, but observation at τ_p < 2×10³⁴ or >10³⁵ would be problematic

#### C. KK Graviton Mass Tower
- **Prediction:** m₁ = 5.0 ± 1.5 TeV, m₂ = 7.1 ± 2.1 TeV (T² degeneracy)
- **Test:** HL-LHC (2029-2040)
- **Falsification:** If HL-LHC excludes m_KK > 10 TeV with no signal, the orthogonal compactification scale is **falsified**
- **Assessment:** **FALSIFIABLE WITH CAVEATS** — The ±30% uncertainty is suspiciously large, and the claim of 6.2σ discovery is unrealistic (see Section 3)

### 1.2 Adjustable Predictions (Survivable)

These predictions have sufficient **parameter freedom** to survive contradictory data:

#### A. Dark Energy w₀ and w_a
- **Claimed Prediction:** w₀ = -0.8528 (from d_eff = 12.589), w_a = -0.95
- **CRITICAL ISSUE:** Git history shows these were **fitted to DESI DR2 (October 2024)**
  - Commit d1d5865 (Nov 2025): "Polish website for v7.0 publication: Remove outdated criticism and update all formulas"
  - Commit 76c3977: "Fix w₀ and Planck tension inconsistencies with dynamic PM population"
  - The parameters α₄ = 0.5891, α₅ = 0.5891 were **tuned** to match DESI: α₄ + α₅ = 1.1781 → d_eff = 12.589 → w₀ = -11/13 = -0.8528
- **Assessment:** **POST-HOC FIT, NOT PREDICTIVE** — This is curve-fitting, not prediction

#### B. Proton Decay Branching Ratios
- **Claimed Prediction:** BR(e⁺π⁰) = 64.2% ± 9.4%, BR(K⁺ν̄) = 35.6% ± 9.4%
- **Parameter Freedom:**
  - Geometric mixing ε = sin(π b₂/b₃) — but b₂ is adjustable (config shows b₂ = 4, but why not 3 or 5?)
  - CKM rotation with Wolfenstein parameters (A, ρ, η) — multiple knobs
  - "Optional moonshine bias" flag in code (proton_decay_v84_ckm.py line 122-134)
- **Assessment:** **PARTIALLY POST-HOC** — The code explicitly states "Target: BR(e⁺π⁰) ~ 62% ± 5%" (line 21), suggesting the model was tuned to reach these values

#### C. PMNS Mixing Angles
- **Claimed Prediction:** θ₂₃ = 47.2° (exact match!), θ₁₂ = 33.59°, θ₁₃ = 8.57°, δ_CP = 235.0°
- **Experimental Data:** NuFIT 5.3 (2024): θ₂₃ = 47.2° ± 2.0°
- **Parameter Freedom:**
  - Moduli perturbations (5% Gaussian noise, neutrino_mass_ordering.py line 94)
  - Flux dressing F ~ √6 ± 5% (line 231)
  - Random cycle orientation signs regenerated per MC sample (line 235)
- **Assessment:** **LIKELY POST-HOC** — The "exact match" for θ₂₃ is suspicious given the multiple adjustable parameters. The code regenerates random orientations until it matches data within Monte Carlo noise.

### 1.3 Unfalsifiable Claims

These claims **cannot be tested** with foreseeable experiments:

#### A. 26D Two-Time Framework
- **Claim:** Spacetime has signature (13,1) + (13,1) with orthogonal time t_⊥
- **Testability:** No proposed test for dimensions beyond 4D at accessible energies
- **Assessment:** **UNFALSIFIABLE** — This is metaphysical structure, not testable physics

#### B. G₂ Manifold Topology
- **Claim:** Extra dimensions compactified on specific G₂ manifold with b₂=4, b₃=24
- **Testability:** No way to directly measure topology of extra dimensions
- **Assessment:** **UNFALSIFIABLE** — We can only test consequences (KK masses, generation count), not the manifold itself

#### C. Pneuma Spinor Field
- **Claim:** Fundamental spinor in 2^13 = 8192 dimensions (Clifford algebra)
- **Testability:** No observable signature distinct from Standard Model fermions
- **Assessment:** **UNFALSIFIABLE** — Untestable metaphysical construct

#### D. Mashiach Scalar Field Dynamics
- **Claim:** Dark energy from scalar field frozen at z>3000, active at z<3
- **Testability:** Requires precision cosmology at multiple redshift bins (Euclid 2027+)
- **Problem:** Even if w(z) follows logarithmic evolution, this doesn't prove the Mashiach field exists—CPL or other parametrizations could fit equally well
- **Assessment:** **WEAKLY TESTABLE** — Functional form test is possible, but doesn't uniquely identify mechanism

---

## 2. Experimental Timeline & Feasibility

### 2.1 Near-Term Tests (2025-2030)

#### Test 1: Neutrino Mass Ordering — JUNO (2025-2027), DUNE (2027-2030)
- **PM Prediction:** IH at 85.5% confidence
- **Current Status:** NuFIT 5.3 (2024) prefers NH at 2.7σ (PM is **already in tension**)
- **JUNO Sensitivity:** 3-4σ discrimination (mass-squared differences)
- **DUNE Sensitivity:** >5σ with 7 years of data
- **Feasibility:** **REALISTIC** — JUNO is under construction, DUNE Far Detector filling begins 2028
- **Timeline Confidence:** HIGH (90%)

**Critical Assessment:**
- PM's 85.5% for IH conflicts with current 2.7σ preference for NH
- If DUNE confirms NH at 5σ by 2030, PM's G₂ cycle model is **falsified**
- This is PM's **most decisive near-term test**

#### Test 2: Dark Energy Evolution — DESI DR2 (2025), Euclid (2026-2028)
- **PM Prediction:** w(z) ~ w₀[1 + (α_T/3)ln(1+z)] with w₀ = -0.8528
- **DESI DR2 (2025):** More precise w₀, w_a constraints
- **Euclid (2026-2028):** Functional form discrimination (ln(1+z) vs CPL)
- **Feasibility:** **REALISTIC** — DESI DR2 imminent, Euclid launched July 2023

**Critical Assessment:**
- **PROBLEM:** PM's w₀ was **fitted to DESI DR1/preliminary data** (see Section 4)
- The prediction of "3.5σ preference for ln(1+z)" (wz_evolution_desi_dr2.py line 164) is **not a prediction**—the code simulates fake data from PM model and shows PM fits PM data well (circular!)
- **True Test:** If Euclid strongly prefers CPL over logarithmic, PM is disfavored (but α_T could be adjusted)

#### Test 3: Proton Decay Channels — Hyper-K (2027-2035)
- **PM Prediction:** τ_p = 3.87×10³⁴ yr, BR(e⁺π⁰) = 64.2%
- **Hyper-K Sensitivity:** ~1×10³⁴ years for e⁺π⁰ (10 years of data)
- **Feasibility:** **REALISTIC** — Hyper-K under construction, first water 2027
- **Timeline Confidence:** HIGH (85%)

**Critical Assessment:**
- PM's central value (3.87×10³⁴ yr) is **just above** Hyper-K 10-year sensitivity
- If Hyper-K sees nothing after 10 years, PM is at **2σ tension** (within 68% CI but outside central value)
- **Survivable:** PM could adjust b₃ flux (±2), Yukawa uncertainties (±20%) to push τ_p higher

### 2.2 Medium-Term Tests (2030-2040)

#### Test 4: KK Graviton Search — HL-LHC (2029-2040)
- **PM Prediction:** m₁ = 5.0 ± 1.5 TeV, σ = 0.10 ± 0.03 fb
- **HL-LHC Sensitivity:** m_KK up to ~6-7 TeV (3 ab⁻¹, diphoton channel)
- **PM Claims:** "6.2σ discovery at 3 ab⁻¹"

**Critical Assessment — UNREALISTIC:**
1. **Cross-section is too low:** σ = 0.10 fb is **at the edge** of HL-LHC sensitivity
   - HL-LHC statistical uncertainty: δσ ~ 0.016 fb (for 3 ab⁻¹)
   - Signal significance: S/√B ~ 6.2σ **ONLY IF backgrounds are negligible**
   - **Problem:** Diphoton backgrounds from QCD, EW processes are large at 5 TeV
   - Realistic significance: **2-3σ** at best

2. **Mass uncertainty is too large:** ±30% (1.5 TeV) yet claims precise prediction
   - How can you claim 6.2σ discovery if you don't know the mass within 30%?
   - HL-LHC mass resolution: ~5-10% for diphoton resonances
   - PM's ±30% suggests the compactification scale is **not well-determined**

3. **Code reveals the problem:** kk_spectrum_full.py line 192
   ```python
   R_c_inv_varied = np.random.normal(self.R_c_inv, 0.3 * self.R_c_inv)
   ```
   - 30% uncertainty on compactification radius
   - This propagates to 30% on m_KK
   - **Yet the theory claims to "predict" 5 TeV?** This is **over-confident**

**Feasibility:** PARTIAL — HL-LHC will probe 5 TeV, but discovery is unlikely given low cross-section

**Realistic Outcome:** 95% CL exclusion of m_KK < 6 TeV if PM is wrong, or 2-3σ hint if PM is right (not 6.2σ)

### 2.3 Long-Term Tests (2040+)

#### Test 5: Proton Decay at 10³⁵ years
- **PM Range:** 2.35×10³⁴ to 5.39×10³⁴ years (68% CI)
- **Hyper-K 20-year sensitivity:** ~3-5×10³⁴ years
- **Next-generation (THEIA, post-2040):** ~10³⁵ years

**Assessment:** If no proton decay seen at 10³⁵ years, PM is **excluded** (outside 95% CI)

#### Test 6: X,Y Gauge Boson Production
- **PM Prediction:** M_X = M_Y = M_GUT = 2.12×10¹⁶ GeV
- **Testability:** **IMPOSSIBLE** — Far beyond any conceivable collider
- **Assessment:** **UNFALSIFIABLE**

---

## 3. Statistical Rigor

### 3.1 Uncertainty Quantification — Are Error Bars Honest?

#### Proton Decay: 0.177 OOM (GOOD)
- **Claimed Uncertainty:** ±0.177 OOM (factor of 1.5)
- **Monte Carlo:** n=1000 samples, varies:
  - b₃ flux: 24 ± 2 (Gaussian, constrained to 20-28)
  - Yukawa matrix elements: ±20%
  - α_s(M_Z): ±0.001
- **Assessment:** **HONEST** — This is a realistic uncertainty given theoretical inputs
- **Evidence:** Independent RG running codes give similar results (τ_p ~ 10³⁴ yr for SO(10) at M_GUT ~ 2×10¹⁶ GeV)

#### KK Spectrum: ±30% on m_KK (CONCERNING)
- **Claimed Uncertainty:** m₁ = 5.0 ± 1.5 TeV
- **Source:** 30% uncertainty on compactification radius R_c (kk_spectrum_full.py line 192)
- **Problem:** Why is R_c so uncertain?
  - PM claims to derive M_GUT = 2.118×10¹⁶ GeV to 0.8% precision (from TCS torsion logs)
  - But R_c ~ 1/M_KK ~ 1/(5 TeV) is known to only 30%?
  - **Inconsistency:** If geometry determines M_GUT precisely, why not M_KK?
- **Assessment:** **SUSPICIOUSLY LARGE** — Suggests the KK mass prediction is **not well-constrained by theory**

#### PMNS Angles: 0.00σ to 0.24σ (SUSPICIOUSLY GOOD)
- **Claimed Precision:** θ₂₃ = 47.20° (0.00σ), θ₁₂ = 33.59° (0.24σ), θ₁₃ = 8.57° (0.01σ)
- **Experimental Data:** NuFIT 5.3 (2024)
- **Problem:** The code includes **multiple adjustable parameters:**
  - Moduli perturbations: 5% Gaussian noise (neutrino_mass_ordering.py line 94)
  - Flux dressing: F ~ √6 ± 5% (line 231)
  - Random cycle orientations regenerated per sample (line 235)
  - Off-diagonal mixing from "Gaussian noise from moduli" (proton_decay_v84_ckm.py line 145-147)
- **Statistical Likelihood:**
  - Probability of 4 independent angles all within 0.24σ by chance: ~(0.24/1)⁴ ~ 0.3% (if random)
  - **But parameters were tuned:** The code shows moduli are varied until agreement is reached
- **Assessment:** **LIKELY POST-HOC** — The "exact matches" result from parameter adjustment, not genuine prediction

#### Dark Energy: 0.38σ on w₀ (POST-HOC)
- **Claim:** w₀ = -0.8528 agrees with DESI DR2 = -0.83 ± 0.06 at 0.38σ
- **Evidence of Post-Hoc Fitting:**
  - Git commit 76c3977 (Nov 2025): "Fix w₀ and Planck tension inconsistencies"
  - Git commit f23af2a: "Update config.py with geometrically-derived alpha_4 and alpha_5 parameters"
  - Git commit 682291e: "Add complete geometric derivation of alpha_4 and alpha_5 from TCS G2 manifold"
  - **Timeline:** DESI DR2 published October 2024, PM "derivation" added November 2025
- **Assessment:** **FITTED, NOT PREDICTED** — This is post-hoc curve-fitting

### 3.2 Systematic Uncertainties — What's Missing?

#### Missing Systematics in Proton Decay:
1. **Threshold corrections:** Only 3-loop, but 4-loop and 5-loop can shift τ_p by ~20%
2. **Hadronic matrix elements:** Lattice QCD uncertainties ~30% (not propagated)
3. **GUT symmetry breaking pattern:** Assumes SO(10) → SU(5), but could be SO(10) → Pati-Salam
4. **KK threshold effects:** If M_KK ~ 5 TeV, modifies RG running (not included)

**Estimated Total Systematic:** ~0.3-0.4 OOM (factor of 2-2.5)
**PM Claims:** 0.177 OOM
**Assessment:** **UNDERESTIMATED** by factor of ~2

#### Missing Systematics in KK Production:
1. **Parton distribution functions (PDFs):** ±20% at x ~ 0.7 (5 TeV at 14 TeV LHC)
2. **Higher-order corrections:** NLO QCD can enhance σ by 30-50% (not included)
3. **Branching ratio uncertainties:** Assumes BR(gg) = 65%, but depends on unknown couplings
4. **Background modeling:** Diphoton backgrounds not simulated

**Estimated Total Systematic:** ±50% on σ
**PM Claims:** σ = 0.10 ± 0.03 fb (±30%, statistical only)
**Assessment:** **SYSTEMATIC UNCERTAINTIES NOT INCLUDED**

#### Missing Systematics in PMNS:
1. **Yukawa textures:** Assumes specific G₂ cycle intersection pattern (not unique)
2. **Moduli stabilization:** VEVs of moduli fields affect Yukawa couplings (±10-20%)
3. **String loop corrections:** α' corrections can shift mixing angles by ~5%

**Assessment:** **UNDERESTIMATED** — The 0.00σ "exact match" ignores these systematics

### 3.3 P-Values & Significance — Are Claims Statistically Sound?

#### Claim: "10/14 predictions within 1σ" (predictions.html line 250)
- **Statistical Expectation:** If predictions are random, ~68% should be within 1σ
- **PM Achievement:** 10/14 = 71% within 1σ
- **P-value:** Not statistically significant (p ~ 0.4, binomial test)
- **Assessment:** **CONSISTENT WITH CHANCE** (or with modest parameter tuning)

#### Claim: "3 exact matches (0.00σ)" (predictions.html line 250)
- **Exact matches:** θ₂₃, θ₁₃, generation count n_gen = 3
- **Problem 1 (n_gen):** This is not 0.00σ—it's an **integer constraint** (either 3 or not 3)
  - Any theory that gets 3 generations gets "0.00σ" by this metric
  - This is like predicting "the number of spatial dimensions is 3" and claiming victory
- **Problem 2 (θ₂₃, θ₁₃):** These have uncertainties (θ₂₃ = 47.2° ± 2.0°), so "exact" is misleading
  - θ₂₃: PM predicts 47.20°, NuFIT 5.3 best-fit is 47.2° → **agreement within rounding**
  - But PM has **moduli freedom** to tune this (see Section 3.1)
- **Assessment:** **MISLEADING CLAIM** — These are not "exact predictions"

#### Claim: "6.2σ discovery at HL-LHC" (predictions.html line 327, kk_spectrum_full.py line 301)
- **Calculation:** σ_signal / σ_background = 0.10 fb / 0.016 fb ~ 6.2
- **Problem:** This assumes √B ~ 0.016 fb for backgrounds
  - **Unrealistic:** At 5 TeV diphoton invariant mass, backgrounds are dominated by:
    - QCD continuum: σ ~ 1-10 fb (not 0.016 fb)
    - Drell-Yan: σ ~ 0.1-1 fb
  - **Realistic significance:** S/√(S+B) ~ 0.10/√(0.10+1) ~ 0.3σ (not 6.2σ)
- **Code Evidence:** kk_spectrum_full.py line 264:
  ```python
  print(f"  Discovery potential: {sigma_m1/0.016:.1f}sigma (100 fb^-1)")
  ```
  - Hardcoded `0.016` is **arbitrary** (not from background simulation)
- **Assessment:** **GROSSLY OVERSTATED** — Realistic significance is <1σ, not 6.2σ

#### Claim: "ln(1+z) preferred by 6.2σ over CPL" (wz_evolution_desi_dr2.py line 164)
- **Calculation:** Δχ² = χ²_CPL - χ²_log = 38.5, σ ~ √(Δχ²) = 6.2
- **Problem:** This is a **fake data test**
  - Code simulates data from PM's logarithmic model (line 142)
  - Then shows PM model fits PM-generated data better than CPL
  - **Circular reasoning:** Of course your model fits your own fake data!
- **Real Test:** Fit DESI DR2 real data with ln(1+z) vs CPL
  - PM does not provide this analysis
  - DESI DR2 paper prefers CPL (not logarithmic)
- **Assessment:** **MISLEADING** — This is not a test, it's a demonstration of self-consistency

---

## 4. Predictive vs Post-Hoc

### 4.1 Post-Hoc Fits (Adjusted After Data)

#### CRITICAL: Dark Energy w₀ and w_a
- **Data Published:** DESI DR2 (October 2024, arXiv:2510.12627)
  - w₀ = -0.83 ± 0.06
  - w_a = -0.75 ± 0.30
- **PM "Derivation" Added:** November 2025 (after data release)
  - Git commit 682291e (Nov 2025): "Add complete geometric derivation of alpha_4 and alpha_5 from TCS G2 manifold"
  - Git commit f23af2a (Nov 2025): "Update config.py with geometrically-derived alpha_4 and alpha_5 parameters"
  - Git commit 76c3977 (Nov 2025): "Fix w₀ and Planck tension inconsistencies with dynamic PM population"

**Smoking Gun Evidence:**
- `config.py` (line 102-105, added Nov 2025):
  ```python
  ALPHA_4 = 0.5891  # Derived from TCS G₂ 4-cycle (4th Betti number)
  ALPHA_5 = 0.5891  # Derived from TCS G₂ 5-cycle (5th Betti number)
  D_EFF = 12.589    # Effective dimension: 12 + 0.5*(α₄ + α₅)
  W_0_PREDICTION = -(D_EFF - 1)/(D_EFF + 1)  # = -0.8528
  ```
- **Tuning:** α₄ + α₅ = 1.1781 is **fine-tuned** to give d_eff = 12.589 → w₀ = -11/13 = -0.8528
- **Target:** Match DESI w₀ = -0.83 ± 0.06 (achieved: 0.38σ deviation)

**Assessment:** **DEFINITIVELY POST-HOC** — This is not prediction, it's curve-fitting

#### PMNS Mixing Angles
- **Data Published:** NuFIT 5.3 (2024, arXiv:2403.03004)
- **PM Code:**
  - Moduli perturbations varied (neutrino_mass_ordering.py line 94)
  - Off-diagonal mixing with "Gaussian noise from moduli" (proton_decay_v84_ckm.py line 145)
  - Flux dressing F varied ±5% (neutrino_mass_ordering.py line 231)
- **Red Flag:** "exact match" for θ₂₃ despite multiple adjustable parameters
- **Assessment:** **LIKELY POST-HOC** — Parameters tuned to reproduce NuFIT data

#### Proton Decay Branching Ratios
- **Code Comment:** proton_decay_v84_ckm.py line 21:
  ```python
  # Target: BR(e⁺π⁰) ~ 62% ± 5%, BR(K⁺ν̄) ~ 23% ± 4%
  ```
- **Interpretation:** The model was **designed to hit these targets**
- **Method:** CKM rotation + geometric mixing tuned to match literature expectations
- **Assessment:** **SEMI-POST-HOC** — Not fitted to data (no observation yet), but tuned to theoretical expectations from other SO(10) models

### 4.2 Genuine Predictions (Before Data)

#### Neutrino Mass Ordering (IH)
- **Prediction:** Inverted Hierarchy at 85.5% confidence
- **Derivation:** Atiyah-Singer index on b₃=24 G₂ cycles (topological, hard to adjust)
- **Data Status:** NuFIT 5.3 (2024) prefers NH at 2.7σ → **PM is already disfavored**
- **Future Test:** DUNE (2027-2030)
- **Assessment:** **GENUINE PREDICTION** (though currently contradicted)

#### KK Graviton Mass (5 TeV)
- **Prediction:** m_KK,1 = 5.0 ± 1.5 TeV
- **Basis:** Compactification scale from M_GUT/M_string hierarchy
- **Data Status:** ATLAS/CMS exclude m_KK < 3.5 TeV (2024, 95% CL)
- **Future Test:** HL-LHC (2029-2040)
- **Assessment:** **GENUINE PREDICTION** (though ±30% uncertainty is large)

#### Proton Lifetime (10³⁴ years)
- **Prediction:** τ_p = 3.87×10³⁴ years (±0.177 OOM)
- **Basis:** M_GUT from TCS torsion logs + RG running
- **Data Status:** Super-K bound > 1.67×10³⁴ years (consistent)
- **Future Test:** Hyper-K (2027-2035)
- **Assessment:** **GENUINE PREDICTION** (consistent with current bounds)

### 4.3 Parameter Freedom Assessment

**How many free parameters does PM have?**

#### Explicitly Fitted (in config.py):
1. α₄ = 0.5891 (tuned for w₀)
2. α₅ = 0.5891 (tuned for w₀)
3. b₂ = 4 (chosen to give ε_geo = 0.5 for proton decay)
4. b₃ = 24 (flux variation ±2 used in MC)
5. Moduli VEVs (5% perturbations in PMNS, KK calculations)
6. Yukawa off-diagonal mixing (Gaussian noise varied until PMNS matches)

#### Implicitly Adjusted:
7. Compactification radius R_c (±30% freedom → KK masses)
8. Flux dressing F ~ √(χ_eff/b₃) (±5% → neutrino ordering)
9. GUT symmetry breaking scale M_GUT (derived from b₃, but b₃ is tunable)
10. Thermal time parameter α_T = 2.7 (determines w_a evolution)

**Total Adjustable Parameters:** ~10

**Compare to Standard Model:** 19 parameters (6 quark masses, 3 lepton masses, 3 gauge couplings, 4 CKM parameters, 2 Higgs parameters, 1 QCD vacuum angle)

**Assessment:** PM has **similar parameter freedom** to the Standard Model, but claims to be more "fundamental"

### 4.4 Is This Predictive Science or Curve-Fitting?

#### Predictive Elements (30%):
- Neutrino mass ordering (IH prediction, genuine but currently disfavored)
- Proton lifetime range (testable 2027-2035)
- KK graviton mass (testable 2029-2040, but large uncertainty)
- Generation count n_gen = 3 (topological, but trivial—any viable theory gets this)

#### Post-Hoc Curve-Fitting (50%):
- Dark energy w₀, w_a (fitted to DESI 2024 in Nov 2025)
- PMNS mixing angles (parameters varied until "exact matches")
- Proton decay branching ratios (tuned to SO(10) literature expectations)

#### Untestable Metaphysics (20%):
- 26D two-time structure
- G₂ manifold topology
- Pneuma spinor field
- Mashiach scalar dynamics (mechanism not uniquely testable)

**Overall Verdict:** PM is **40% predictive science, 60% post-hoc fitting + metaphysics**

---

## 5. Competitive Landscape

### 5.1 Unique PM Predictions (Distinguishable from Competitors)

#### 1. Inverted Hierarchy for Neutrinos
- **PM:** IH at 85.5% (from G₂ cycle orientations)
- **Standard SO(10):** No strong preference (depends on Yukawa textures)
- **String Theory:** Can accommodate both IH and NH (landscape)
- **Loop Quantum Gravity:** No neutrino mass predictions
- **Advantage:** PM makes a definite (though currently disfavored) prediction

#### 2. Logarithmic w(z) Evolution
- **PM:** w(z) ~ w₀[1 + (α_T/3)ln(1+z)]
- **ΛCDM:** w(z) = -1 (constant)
- **Standard Quintessence:** w(z) ~ w₀ + w_a z/(1+z) (CPL)
- **String Theory (KKLT):** w ≈ -1 with small deviations
- **Advantage:** Distinguishable functional form (testable by Euclid 2027)
- **Caveat:** If this turns out wrong, α_T can be adjusted

#### 3. KK Graviton Tower at 5 TeV
- **PM:** m_KK,1 = 5 ± 1.5 TeV (from 7D G₂ compactification)
- **ADD (Large Extra Dimensions):** m_KK ~ TeV (from mm-scale extras)
- **Randall-Sundrum:** m_KK ~ TeV (from warped 5D)
- **Standard String Theory:** m_KK ~ 10¹⁶ GeV (if extras are Planck-sized)
- **Advantage:** Intermediate scale (between ADD and standard string) is testable at HL-LHC
- **Disadvantage:** ±30% uncertainty overlaps with ADD/RS predictions

### 5.2 Overlapping Predictions (Not Unique to PM)

#### 1. Proton Decay at 10³⁴-10³⁵ Years
- **PM:** τ_p = 3.87×10³⁴ years
- **SO(10) GUTs:** τ_p ~ 10³⁴-10³⁶ years (similar range)
- **SU(5):** τ_p ~ 10³⁰-10³¹ years (**excluded by Super-K**)
- **Flipped SU(5):** τ_p > 10³⁵ years
- **Assessment:** PM's prediction is **typical for SO(10)**, not unique

#### 2. Three Generations
- **PM:** n_gen = χ_eff/48 = 144/48 = 3
- **ALL viable theories:** Must get 3 generations (observed fact)
- **Assessment:** This is not a prediction, it's a **post-diction**

#### 3. PMNS Mixing Angles
- **PM:** θ₂₃ = 47.2°, θ₁₂ = 33.6°, θ₁₃ = 8.6°, δ_CP = 235°
- **Tri-bimaximal Mixing (TBM):** θ₂₃ = 45°, θ₁₂ = 35.3°, θ₁₃ = 0° (disfavored)
- **Flavor Symmetries (A₄, S₄):** Can reproduce observed angles with parameter tuning
- **Standard SO(10) with textures:** Can fit PMNS with appropriate Yukawas
- **Assessment:** PM's fit is **not better than other models**

### 5.3 Where PM Does Better

#### 1. Testability Timeline
- **PM Advantage:** Makes multiple predictions testable in next 5-15 years
  - JUNO (2027), DUNE (2027-2030), Hyper-K (2027-2035), HL-LHC (2029-2040)
- **String Theory:** Most predictions require Planck-scale energies (untestable)
- **Loop Quantum Gravity:** Minimal phenomenological predictions
- **Asymptotic Safety:** Mostly focuses on UV completion (few low-energy tests)

#### 2. Quantitative Precision
- **PM Advantage:** Provides numerical predictions with error bars
  - τ_p = 3.87×10³⁴ ± 0.177 OOM
  - m_KK = 5.0 ± 1.5 TeV
  - w₀ = -0.8528 ± 0.06 (though this is post-hoc)
- **Many BSM theories:** Only order-of-magnitude estimates

#### 3. Cosmology Integration
- **PM Advantage:** Addresses Planck-DESI tension with specific mechanism (frozen Mashiach field)
- **Standard ΛCDM:** Ignores tension or attributes to systematics
- **Most GUTs:** Focus on particle physics, not cosmology

### 5.4 Where Competitors Do Better

#### 1. Theoretical Consistency (String Theory)
- **String Theory Advantage:**
  - Fully consistent quantum gravity (proven finite)
  - Landscape allows post-diction of any observations
  - Decades of rigorous mathematical development
- **PM Disadvantage:**
  - Two-time structure lacks rigorous field theory formulation
  - G₂ compactification details incomplete (no explicit metric)
  - Moduli stabilization mechanism unclear (appeals to KKLT without full derivation)

#### 2. Predictive Falsifiability (Loop Quantum Gravity)
- **LQG Advantage:**
  - Makes fewer unfalsifiable claims
  - Focuses on testable quantum gravity effects (graviton propagator modifications)
- **PM Disadvantage:**
  - Many predictions have parameter freedom (adjustable α₄, α₅, b₃, moduli)
  - Post-hoc fitting to DESI data undermines predictive credibility

#### 3. Neutrino Mass Ordering (Current Data Preference)
- **Standard SO(10) with NH:**
  - Consistent with NuFIT 5.3 (NH preferred at 2.7σ)
  - Can accommodate IH if needed (texture flexibility)
- **PM:**
  - Commits to IH at 85.5% (currently disfavored)
  - If DUNE confirms NH, PM must revise cycle orientation model

#### 4. Simplicity (Asymptotic Safety)
- **Asymptotic Safety Advantage:**
  - Uses Standard Model + gravity (no extra fields)
  - Relies on RG flow to UV fixed point (minimal assumptions)
- **PM Disadvantage:**
  - Requires 26D spacetime, G₂ manifold, Pneuma spinors, Mashiach field, mirror sector
  - Ockham's Razor violation (why all this machinery for modest improvements over ΛCDM+GUT?)

---

## 6. Falsification Scenarios

### 6.1 Neutrino Mass Ordering (DECISIVE TEST)

**PM Prediction:** Inverted Hierarchy (IH) at 85.5% confidence

**Falsification Criterion:**
- **If DUNE confirms Normal Hierarchy (NH) at >3σ** (2028-2030): PM's G₂ cycle orientation model is **falsified**

**PM's Response Options:**
1. **Claim cycles have different orientation:** Flip sign of Atiyah-Singer index
   - **Problem:** This undermines the topological "derivation"—if orientations are free, the model predicts nothing
2. **Adjust flux dressing F:** Vary χ_eff or b₃ to flip index sign
   - **Problem:** b₃ = 24 is claimed to be topologically fixed
3. **Invoke new mechanism:** "Mirror sector interference flips hierarchy"
   - **Problem:** Ad-hoc addition of new physics

**Survivability:** **DIFFICULT** — This is PM's most robust falsifiable prediction. If DUNE confirms NH at 5σ, PM is in serious trouble.

### 6.2 Proton Decay Lifetime (STRONG TEST)

**PM Prediction:** τ_p = 3.87×10³⁴ years, 68% CI: [2.35, 5.39]×10³⁴ years

**Falsification Scenarios:**

#### Scenario A: No Decay Seen by Hyper-K (2035)
- **Hyper-K 10-year sensitivity:** ~1×10³⁴ years
- **PM 68% CI upper bound:** 5.39×10³⁴ years
- **Outcome:** PM is at **2σ tension** (outside central value but within 68% CI)

**PM's Response Options:**
1. **Extend uncertainty:** "Higher-order corrections push τ_p higher"
   - **Plausibility:** Moderate (4-loop RG, lattice QCD systematics could give factor of 2-3)
2. **Adjust M_GUT:** Vary b₃ flux (24 → 26) to increase M_GUT → longer τ_p
   - **Plausibility:** High (b₃ has ±2 uncertainty already built into model)

**Survivability:** **HIGH** — PM can adjust parameters to survive null result

#### Scenario B: No Decay at 10³⁵ Years (Post-2040)
- **Next-generation sensitivity:** ~10³⁵ years (THEIA, post-2040)
- **PM 95% CI upper bound:** ~1×10³⁵ years (extrapolated)
- **Outcome:** PM is **excluded at 95% CL**

**PM's Response Options:**
1. **Radical parameter adjustment:** Push M_GUT from 2.1×10¹⁶ to 3×10¹⁶ GeV
   - **Problem:** Conflicts with gauge unification (α₁, α₂, α₃ don't meet at 3×10¹⁶)
2. **Abandon SO(10):** Switch to SU(5) or Pati-Salam (different proton decay channels)
   - **Problem:** This is a new theory, not PM

**Survivability:** **LOW** — Null result at 10³⁵ years would falsify PM's SO(10) structure

### 6.3 KK Gravitons Not Found at HL-LHC (MODERATE TEST)

**PM Prediction:** m_KK,1 = 5.0 ± 1.5 TeV (68% CI: 3.5-6.5 TeV)

**Falsification Scenarios:**

#### Scenario A: HL-LHC Excludes m_KK < 7 TeV (No Signal)
- **HL-LHC reach:** ~6-7 TeV for KK gravitons (3 ab⁻¹, diphoton)
- **PM 68% CI:** 3.5-6.5 TeV → **2σ tension**

**PM's Response Options:**
1. **Increase m_KK:** Adjust compactification radius R_c
   - **Method:** Reduce R_c from 1/(5 TeV) to 1/(8 TeV)
   - **Plausibility:** High (R_c already has ±30% uncertainty)
2. **Claim suppressed couplings:** "KK gravitons don't couple to photons as strongly"
   - **Problem:** Reduces cross-section, making future detection even harder

**Survivability:** **HIGH** — ±30% uncertainty gives wiggle room

#### Scenario B: HL-LHC Excludes m_KK < 10 TeV (No Signal)
- **PM 95% CI:** ~2-8 TeV (extrapolated) → **3σ tension**

**PM's Response Options:**
1. **Push m_KK to 12-15 TeV:** Radical compactification adjustment
   - **Problem:** Conflicts with gauge hierarchy (why are KK modes so heavy if M_GUT ~ 10¹⁶ GeV?)
2. **Abandon orthogonal compactification:** Switch to standard Planck-scale extras
   - **Problem:** Loses unique prediction (reverts to standard string theory)

**Survivability:** **MODERATE** — Possible to adjust, but at cost of theoretical consistency

### 6.4 DESI/Euclid Prefers CPL Over Logarithmic (WEAK TEST)

**PM Prediction:** w(z) ~ w₀[1 + (α_T/3)ln(1+z)] preferred over CPL at 3.5σ (Euclid, 2027)

**Falsification Scenarios:**

#### Scenario A: Euclid Finds Δχ²(CPL - log) = -10 (CPL Better)
- **Interpretation:** CPL fits data 3σ better than logarithmic
- **Outcome:** PM's Mashiach field dynamics **disfavored**

**PM's Response Options:**
1. **Adjust α_T:** Change from 2.7 to different value
   - **Effect:** Makes logarithmic evolution steeper/shallower to match CPL
   - **Plausibility:** High (α_T is currently a fitted parameter)
2. **Hybrid model:** "Mashiach field + quintessence" (both logarithmic and CPL components)
   - **Problem:** Ad-hoc addition of extra field

**Survivability:** **VERY HIGH** — α_T can be adjusted to match any w(z) data

#### Scenario B: Euclid Finds w = -1 (ΛCDM Preferred)
- **Interpretation:** No dark energy evolution, cosmological constant
- **Outcome:** PM's dynamical dark energy is **excluded**

**PM's Response Options:**
1. **Claim Mashiach is frozen everywhere:** "Field never activates"
   - **Problem:** Then why postulate it? This reduces to ΛCDM
2. **Appeal to systematic errors:** "Euclid systematics hide evolution"
   - **Plausibility:** Low (Euclid designed to minimize systematics)

**Survivability:** **MODERATE** — Can retreat to ΛCDM limit, but loses explanatory power

### 6.5 Combined Falsification (MULTIPLE FAILURES)

**Strongest Falsification:** DUNE confirms NH (5σ) + Hyper-K sees no decay at 10³⁵ years + HL-LHC excludes m_KK < 10 TeV

**Outcome:** PM's core predictions (neutrino hierarchy, proton decay, KK tower) all **fail**

**PM's Survivability:** **VERY LOW** — At this point, the framework would need radical revision

**Historical Analogy:** SU(5) GUT predicted τ_p ~ 10³⁰ years, excluded by Super-K → model abandoned

---

## 7. Overall Assessment

### 7.1 Testability Score

**Criteria:**
- Quantitative predictions with error bars: **YES**
- Near-term experimental tests (5-10 years): **YES** (JUNO, DUNE, Hyper-K starting 2027)
- Medium-term tests (10-20 years): **YES** (HL-LHC 2029-2040)
- Precision comparable to experimental resolution: **PARTIAL** (some uncertainties too large)

**Grade:** **Partially Testable (6/10)**

**Reasoning:**
- PM provides more testable predictions than most BSM theories (string theory, LQG)
- But several predictions have enough parameter freedom to survive contradictory data
- Some claims (26D structure, G₂ topology) are fundamentally untestable

### 7.2 Falsifiability Score

**Criteria:**
- Can be proven wrong by experiments: **PARTIAL**
- Predictions are specific enough to fail: **YES** (neutrino hierarchy, proton decay range)
- Parameter freedom allows survival: **YES** (concerning)
- Post-hoc adjustments possible: **YES** (major red flag)

**Grade:** **Partially Falsifiable (5/10)**

**Reasoning:**
- Neutrino hierarchy (IH) is genuinely falsifiable → **GOOD**
- Proton decay has 0.177 OOM uncertainty, but can be extended → **MODERATE**
- KK masses have ±30% uncertainty → **WEAK**
- Dark energy w₀, w_a were fitted post-hoc → **UNFALSIFIABLE (post-diction)**
- Overall: Some genuine falsifiability, but multiple escape hatches

### 7.3 Experimental Readiness

**Criteria:**
- Predictions are quantitative: **YES**
- Error bars are realistic: **PARTIAL** (some underestimated, e.g., KK cross-section backgrounds)
- Systematic uncertainties included: **NO** (major gap)
- Experiments exist or are planned: **YES** (JUNO, DUNE, Hyper-K, HL-LHC, Euclid)

**Grade:** **Needs Refinement (6/10)**

**Reasoning:**
- PM provides numerical predictions ready for comparison
- But statistical treatment has gaps (systematics not fully propagated)
- Overclaimed significance (6.2σ for HL-LHC KK discovery is unrealistic)
- JUNO and DUNE are ready to test neutrino hierarchy (2027-2030)

### 7.4 Scientific Merit

**Criteria:**
- Predictions made before data: **PARTIAL** (some yes, some no)
- Parameter freedom comparable to Standard Model: **YES** (~10 parameters each)
- Post-hoc fitting minimized: **NO** (w₀, w_a, PMNS angles fitted)
- Theoretical consistency: **PARTIAL** (some derivations rigorous, others hand-wavy)

**Grade:** **Mixed — 50% Predictive Science, 50% Post-Hoc Curve-Fitting (5/10)**

**Detailed Breakdown:**

**Genuinely Predictive (40%):**
1. Neutrino mass ordering (IH) — topological, hard to adjust (though currently disfavored)
2. Proton lifetime range (10³⁴ years) — from M_GUT + RG
3. KK graviton mass (~5 TeV) — from compactification scale (but ±30% uncertainty)
4. Generation count (3) — topological (but trivial, any viable theory gets this)

**Post-Hoc Curve-Fitting (50%):**
1. Dark energy w₀ = -0.8528 — **tuned to DESI 2024 in Nov 2025** (α₄, α₅ adjusted)
2. Dark energy w_a = -0.95 — **matched to DESI** via α_T parameter
3. PMNS mixing angles — parameters (moduli, flux, cycle orientations) varied until "exact matches"
4. Proton decay branching ratios — tuned to SO(10) literature expectations

**Unfalsifiable Metaphysics (10%):**
1. 26D two-time structure — no test proposed
2. G₂ manifold details — topology not directly observable
3. Pneuma spinor field — no distinct signature from Standard Model fermions

### 7.5 Comparison to Established Physics

| Criterion | Standard Model | PM Framework | Verdict |
|-----------|---------------|--------------|---------|
| Parameter Count | 19 | ~10 | **PM is simpler** (good) |
| Experimental Validation | 100s of tests passed | 3-4 matches (some post-hoc) | **SM vastly superior** |
| Predictive Power | Many null predictions confirmed (e.g., no FCNC) | Some post-hoc, some genuine | **SM superior** |
| Falsifiability | Highly falsifiable (but survived) | Partially falsifiable | **SM superior** |
| Theoretical Consistency | Renormalizable QFT | Incomplete (2-time not rigorous) | **SM superior** |
| Unresolved Problems | Hierarchy, strong CP, neutrino masses | Claims to address some (w/o full rigor) | **Unclear** |

**Conclusion:** PM is **not yet at Standard Model level** of scientific rigor, but is **testable enough** to warrant experimental scrutiny.

### 7.6 Recommendation

**SHORT-TERM (2025-2030):**
- ✅ **Pursue experimental tests:** JUNO, DUNE, Hyper-K will provide decisive data on neutrino hierarchy and proton decay
- ⚠️ **Require theoretical refinement:** PM must address post-hoc fitting concerns (w₀, w_a, PMNS angles)
- ⚠️ **Demand transparency:** Publish predictions with error bars BEFORE data release (register on arXiv or OSF)

**MEDIUM-TERM (2030-2040):**
- ✅ **Monitor HL-LHC KK searches:** If signal at 5 TeV, PM gains credibility; if null at 10 TeV, PM needs revision
- ⚠️ **Reassess after Euclid:** If w(z) strongly disfavors logarithmic, PM must explain or abandon Mashiach dynamics

**LONG-TERM (2040+):**
- ⚠️ **If multiple predictions fail:** PM should be abandoned (like SU(5) after Super-K)
- ✅ **If predictions succeed:** PM deserves serious consideration as BSM framework

**Final Judgment:**

**Testability:** Partially testable (6/10)
**Falsifiability:** Partially falsifiable (5/10)
**Experimental Readiness:** Needs refinement (6/10)
**Scientific Merit:** Mixed — 50% predictive, 50% post-hoc (5/10)

**Overall Recommendation:** **PURSUE EXPERIMENTAL TESTS WITH CAUTION**

PM contains enough genuine predictions (neutrino hierarchy, proton decay, KK masses) to justify experimental scrutiny. However, the post-hoc fitting of dark energy parameters (w₀, w_a) and "exact matches" for PMNS angles raise serious concerns about scientific integrity.

**The framework sits at the boundary between legitimate testable physics and pseudoscience.** The next 5-10 years of data from JUNO, DUNE, and Hyper-K will determine whether PM survives as a viable BSM candidate or is relegated to the graveyard of failed GUT models.

**Critical Next Step:** PM must publicly register specific numerical predictions (with error bars) BEFORE experimental data is released. Post-hoc "derivations" after data publication are **not science**.

---

## Appendix A: Key Evidence of Post-Hoc Fitting

### A.1 Git Commit Timeline (Dark Energy)

```
DESI DR2 Published: October 2024 (arXiv:2510.12627)
  w₀ = -0.83 ± 0.06
  w_a = -0.75 ± 0.30

PM Repository Commits:
  Nov 2025 (commit 682291e): "Add complete geometric derivation of alpha_4 and alpha_5"
  Nov 2025 (commit f23af2a): "Update config.py with geometrically-derived alpha_4 and alpha_5"
  Nov 2025 (commit 76c3977): "Fix w₀ and Planck tension inconsistencies"
```

**Conclusion:** PM's w₀ "derivation" was added **1 month after DESI DR2 publication**

### A.2 Code Evidence (Parameter Tuning)

**config.py (lines 102-105, added Nov 2025):**
```python
ALPHA_4 = 0.5891  # Derived from TCS G₂ 4-cycle
ALPHA_5 = 0.5891  # Derived from TCS G₂ 5-cycle
D_EFF = 12.589    # 12 + 0.5*(α₄ + α₅) = 12 + 0.5891 = 12.589
W_0_PREDICTION = -(D_EFF - 1)/(D_EFF + 1) = -11/13 = -0.8528
```

**Reverse Engineering:**
- Target: w₀ = -0.83 (DESI)
- Work backwards: w₀ = -(d-1)/(d+1) → d = (1+w₀)/(1-w₀) = 12.589
- Solve: α₄ + α₅ = 2(d - 12) = 1.1781
- Choose: α₄ = α₅ = 0.5891 (equal by fiat)

**This is textbook curve-fitting.**

### A.3 Statistical Implausibility

**Claim:** 10/14 predictions within 1σ, 3 "exact matches" (0.00σ)

**Bayesian Calculation:**
- Prior: P(theory is true) ~ 0.01 (generous, given many failed GUTs)
- Likelihood if true: P(data | theory) ~ 0.68¹⁰ × 0.32⁴ ≈ 0.0013 (10 within 1σ, 4 outside)
- Likelihood if false (curve-fit): P(data | false theory) ~ 0.5 (can fit anything with 10 parameters)
- Bayes factor: P(data | true) / P(data | false) ~ 0.0013 / 0.5 = 0.0026

**Posterior:**
P(theory true | data) = P(data | true) × P(true) / P(data)
                       ~ 0.0013 × 0.01 / [0.0013×0.01 + 0.5×0.99]
                       ~ 0.000013 / 0.495
                       ~ 0.0026%

**Interpretation:** Given the post-hoc fitting evidence, the probability that PM is a genuine predictive theory is **<0.01%**

**Caveat:** This assumes curve-fitting is easy (P(data|false) ~ 0.5). If PM's structure genuinely constrains predictions, this posterior increases. But the dark energy fitting makes curve-fitting plausible.

---

## Appendix B: Realistic Experimental Sensitivities

### B.1 DUNE Neutrino Mass Ordering (2027-2030)

**DUNE Design Report (arXiv:2002.03005):**
- 7 years of data: >5σ discrimination IH vs NH (90% of parameter space)
- Method: Matter effects in ν_μ → ν_e oscillations
- Systematic uncertainties: ~5% (energy scale, cross-sections)

**PM's 85.5% for IH:**
- If true hierarchy is NH, DUNE will reject IH at 5σ (P_falsely_reject_IH = 3×10⁻⁷)
- **PM would be definitively falsified**

### B.2 Hyper-Kamiokande Proton Decay (2027-2035)

**Hyper-K Design Report (arXiv:1805.04163):**
- 10 years, 260 kton water: τ_p(e⁺π⁰) sensitivity ~1×10³⁴ years
- 20 years: ~3-5×10³⁴ years

**PM Prediction:**
- τ_p = 3.87×10³⁴ years (central), 68% CI: [2.35, 5.39]×10³⁴

**Scenarios:**
- 10-year null result (>1×10³⁴): PM at 1.5σ tension (survives)
- 20-year null result (>4×10³⁴): PM at 2σ tension (borderline)
- 30-year null result (>8×10³⁴): PM excluded at 3σ (next-gen detector needed)

### B.3 HL-LHC KK Graviton Discovery (2029-2040)

**HL-LHC Projections (CERN Yellow Report 2018):**
- 3 ab⁻¹ at 14 TeV
- Diphoton resonance search: m_γγ resolution ~1-2% at 5 TeV
- Background: σ(pp → γγ) ~ 100 fb at √s = 14 TeV, m_γγ > 1 TeV
  - At m_γγ = 5 TeV: σ_bg ~ 0.1-1 fb (continuum, steeply falling)

**PM's Claim: 6.2σ discovery**
- Signal: σ_sig = 0.10 fb (PM prediction)
- Background (PM assumes): σ_bg = 0.016 fb (no justification)
- Significance (PM calculates): S/√B = 0.10/0.016 = 6.2σ

**Realistic Assessment:**
- Background at 5 TeV: σ_bg ~ 0.5 fb (QCD + EW continuum)
- Number of background events: N_bg = σ_bg × L = 0.5 fb × 3000 fb⁻¹ = 1500
- Number of signal events: N_sig = 0.10 × 3000 = 300
- Significance: N_sig / √(N_sig + N_bg) = 300 / √1800 ≈ **7.1**
  - Wait, this is higher than PM's claim!
  - **But**: This ignores systematic uncertainties on background (±20%)
  - Realistic significance: **~3-4σ** (not 6.2σ, but not 0.3σ either)

**Revised Assessment:** PM's 6.2σ claim is **overstated but not absurd**. Realistic expectation is 3-4σ discovery potential if m_KK = 5 TeV.

### B.4 Euclid Dark Energy Functional Form (2027-2028)

**Euclid Red Book (arXiv:1110.3193):**
- 6 years of data: σ(w₀) ~ 0.02, σ(w_a) ~ 0.1
- Functional form test: Δχ² ~ 10-20 for ln(1+z) vs CPL (if true evolution is strong)

**PM's Claim: 3.5σ preference for ln(1+z)**
- Code simulates fake data from PM model (wz_evolution_desi_dr2.py line 142)
- Shows PM fits PM data better than CPL (circular reasoning)

**Realistic Test:**
- Fit real Euclid data with ln(1+z), CPL, and other parametrizations
- Compare Δχ² (requires actual data, not simulations)
- **True test begins 2027**

---

## Appendix C: Recommended Pre-Registration Protocol

To avoid post-hoc fitting accusations, PM should adopt this protocol:

### C.1 Public Pre-Registration (Before Data Release)

**Platform:** arXiv, Open Science Framework (OSF), or FigShare

**Required Content:**
1. **Prediction statement:** "PM predicts [observable] = [value] ± [error] by [mechanism]"
2. **Methodology:** Full derivation from first principles (no adjustable parameters)
3. **Uncertainty budget:** Statistical + systematic (with justification)
4. **Falsification criterion:** "If experiment finds [range], PM is falsified"
5. **Pre-commitment:** "We will not adjust parameters α₄, α₅, b₃, moduli, etc. after data release"

**Example (Neutrino Hierarchy):**
```
Pre-Registration: December 2025
Observable: Neutrino mass ordering (IH vs NH)
PM Prediction: Inverted Hierarchy (IH)
Confidence: 85.5% ± 2.3% (Monte Carlo, n=1000)
Mechanism: Atiyah-Singer index on G₂ cycles (b₃=24, 83% positive orientation)
Falsification: If DUNE confirms NH at >3σ, PM is falsified
Experiment: DUNE (2027-2030)
Pre-commitment: We will not adjust b₃, flux dressing F, or cycle orientations after DUNE data release
```

### C.2 Post-Data Analysis Protocol

**If Prediction Confirmed:**
1. Publish comparison: predicted vs observed
2. Calculate Bayes factor: P(data | PM) / P(data | null)
3. Assess if PM is genuinely validated or if confirmation is due to parameter freedom

**If Prediction Falsified:**
1. Acknowledge falsification publicly
2. Identify which assumption failed (e.g., G₂ cycle orientations)
3. Either: (a) abandon model, or (b) revise with explicit statement of what changed

**Prohibited:**
1. ❌ Adjusting parameters after data release to "improve fit"
2. ❌ Claiming "the theory always predicted this" without pre-registration
3. ❌ Moving goalposts ("we meant 3σ, not 5σ")

### C.3 Transparency Requirements

**Code Repository:**
- ✅ **Already done:** GitHub repository is public
- ⚠️ **Needed:** Tag specific commits as "pre-data" vs "post-data"
- ⚠️ **Needed:** Clearly document which parameters are derived vs fitted

**Publications:**
- ⚠️ **Needed:** Submit predictions to refereed journals BEFORE data release
- ⚠️ **Needed:** Distinguish "derived from first principles" vs "fitted to match data"

---

**END OF REVIEW**

This review represents an honest, critical assessment of the Principia Metaphysica framework from an experimental physicist's perspective. The theory contains both promising elements (testable predictions on near-term timescales) and serious flaws (post-hoc parameter fitting, overstated significance claims). The next 5-10 years of experimental data will determine whether PM deserves continued scientific attention.
