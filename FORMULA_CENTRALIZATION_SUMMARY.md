# Formula Centralization Summary - v8.4

**Date**: 2025-12-06
**Status**: Phase 1 Complete ✅

---

## Executive Summary

Successfully created centralized formula database with **32 essential v8.4 formulas** covering all active physics in the framework. All formulas reference PM constants from `theory_output.json`, ensuring single source of truth architecture.

**Key Achievement**: 37/40 PM constant references (92.5%) are simulation-backed. Only 3 constants (xy_bosons) are from config.py directly.

---

## Formula Database: formula_definitions.py

### Statistics
- **Total Formulas**: 32 essential formulas
- **Categories**: 11 physics topics
- **PM Values Referenced**: 40 unique constants
- **Simulation-Backed**: 37/40 (92.5%)

### Categories (by formula count)

1. **Proton Decay** (5 formulas)
   - τ_p formula with M_GUT, α_GUT
   - M_GUT geometric derivation from TCS torsion
   - α_GUT from 3-loop RG + thresholds
   - BR(e⁺π⁰) = 64.2% ± 9.4% (v8.4 CKM rotation)
   - BR(K⁺ν̄) = 35.6% ± 9.4%

2. **PMNS Matrix** (5 formulas)
   - θ₂₃ = 47.20° (exact match)
   - θ₁₃ = 8.57° (exact match)
   - θ₁₂ = 33.59° (0.22σ)
   - δ_CP = 235° (0.09σ)
   - P(IH) = 85.5% ± 2.3% (mass ordering)

3. **Dark Energy** (4 formulas)
   - w(z) = w₀ + w_a ln(1 + z) evolution
   - Δχ² = 38.84 (6.2σ preference for logarithmic)
   - w(z > 3000) = -1.0 (frozen field, Planck tension resolved)
   - DESI validation: 0.38σ agreement

4. **Dimensional Framework** (4 formulas)
   - D_eff = 12 + 0.5(α₄ + α₅) = 12.589
   - w₀ = -(D_eff - 1)/(D_eff + 1) = -0.8528
   - α₄ + α₅ = 1.178 (from TCS torsion)
   - α₄ - α₅ = 0.733 (from θ₂₃ matching)

5. **Gauge Unification** (2 formulas)
   - SO(10) ⊃ SU(3) × SU(2) × U(1)
   - α₁⁻¹ = α₂⁻¹ = α₃⁻¹ = 23.54 at M_GUT

6. **KK Spectrum** (2 formulas)
   - m_KK(n,m) = √(n² + m²) × 5 TeV (T² tower)
   - BR(gg) = 65%, BR(qq̄) = 25%, BR(ℓℓ) = 8%

7. **Topology** (2 formulas)
   - n_gen = χ_eff/48 = 144/48 = 3 (exact)
   - χ_eff = 144 from flux-dressed G₂

8. **Thermal Time** (2 formulas)
   - t = α_T · S[ρ] (time from entropy)
   - KMS condition (thermal equilibrium)

9. **Gravity** (2 formulas)
   - Einstein field equations
   - 13D Einstein-Hilbert action → 4D GR

10. **Clifford Algebra** (2 formulas)
    - dim(Cl(24,2)) = 2¹³ = 8192
    - Γ^μ = γ^μ ⊗ 𝟙₁₆ decomposition

11. **X,Y Bosons** (2 formulas)
    - M_X = M_Y ≈ M_GUT = 2.118×10¹⁶ GeV
    - τ_X,Y ~ ℏ/M_GUT ≈ 10⁻⁴¹ s

---

## PM Constant Coverage

### Found in theory_output.json (37/40)

**Dark Energy** (7 constants):
- ✓ w0_PM, w0_DESI, w0_deviation_sigma
- ✓ wa_PM_effective, w_CMB_frozen
- ✓ functional_test_delta_chi2, functional_test_sigma_preference

**KK Spectrum** (6 constants):
- ✓ m1, m2, m3 (masses)
- ✓ BR_gg, BR_qq, BR_ll (branching ratios)

**PMNS Matrix** (4 constants):
- ✓ theta_23, theta_12, theta_13, delta_cp

**Proton Decay** (8 constants):
- ✓ M_GUT, alpha_GUT, alpha_GUT_inv
- ✓ tau_p_central, T_omega_torsion, s_parameter
- ✓ BR_epi0_mean, BR_epi0_std, BR_Knu_mean, BR_Knu_std (from proton_decay_channels)

**Neutrino Mass Ordering** (2 constants):
- ✓ prob_IH_mean, prob_IH_std

**Shared Dimensions** (4 constants):
- ✓ alpha_4, alpha_5, d_eff, w0_from_d_eff

**Topology** (4 constants):
- ✓ chi_eff, b2, b3, n_gen

### Missing from theory_output.json (3/40)

**X,Y Bosons** (3 constants):
- ✗ xy_bosons.M_X (in config.py, not simulation)
- ✗ xy_bosons.M_Y (in config.py, not simulation)
- ✗ xy_bosons.tau_estimate (in config.py, not simulation)

**Resolution**: These are derived from config.XYGaugeBosonParameters and available in theory-constants-enhanced.js. No simulation needed (geometric + theoretical).

---

## Orphaned Formula Analysis

### Total Formulas Scanned: 259
- **Under Topic Headings**: 132 (51%)
- **Orphaned**: 127 (49%)
- **Unique**: 257

### By Category (orphaned count):
- action: 17 total, 16 orphaned
- metric: 15 total, 13 orphaned
- dimension: 14 total, 9 orphaned
- gauge: 12 total, 7 orphaned
- thermal: 10 total, 6 orphaned
- other: 179 total, 69 orphaned

### Most Common Orphaned Formulas:
1. t = α_T · S[ρ] (thermal time) - **KEEP** (in database)
2. Γ^μ = γ^μ ⊗ 𝟙₁₆ (gamma matrices) - **KEEP** (in database)
3. Coleman-De Luccia bubble formulas (S_E, r_b, Γ) - **REVIEW** (CMB predictions)
4. CMB statistics (kurtosis, probability) - **REVIEW** (testable but not core)

---

## Relevance Assessment

### KEEP (Essential v8.4 formulas):
- All 32 formulas in `formula_definitions.py`
- Actively used in simulations or foundational
- PM constants available from theory_output.json or config.py

### UPDATE (Need correction):
- Old χ_raw = -300 → replace with χ_eff = 144
- Old proton decay uncertainty 0.8 OOM → 0.177 OOM
- Old placeholder BRs → v8.4 CKM rotation values

### REMOVE (Deprecated):
- 14D×2 vacuum structure (replaced by 26D→13D shadow)
- CY₄ construction (replaced by TCS G₂)

### REVIEW (Context-dependent):
- CMB bubble collision formulas (testable but not core v8.4)
- String landscape formulas (context-dependent relevance)

---

## Next Steps

### Phase 2: Formula Replacement (Pending)
1. ✅ Create centralized formula_definitions.py
2. ⏳ Create script to replace orphaned formulas with centralized references
3. ⏳ Ensure all formulas have PM constant hover tooltips

### Phase 3: Orphaned Content Blocks (Pending)
1. ⏳ Deploy Agent A: calabi-yau.html (10 blocks)
2. ⏳ Deploy Agent B: g2-manifolds.html (9 blocks)
3. ⏳ Deploy Agent C: index.html + paper.html (9 blocks)

---

## Files Created

1. **formula_definitions.py** (406 lines)
   - Centralized database with 32 essential formulas
   - LaTeX, HTML, and metadata for each
   - PM constant references
   - Derivation notes

2. **analyze_orphaned_formulas.py** (216 lines)
   - Scans all HTML files for formulas
   - Categorizes by physics topic
   - Identifies orphaned vs under-topic formulas
   - Exports JSON analysis

3. **assess_formula_relevance.py** (240 lines)
   - Assesses formulas against v8.4 framework
   - Categorizes as KEEP/UPDATE/REMOVE/REVIEW
   - Cross-references with simulation output

4. **check_missing_constants.py** (60 lines)
   - Validates PM constant coverage
   - Identifies missing constants
   - Reports 37/40 (92.5%) coverage

5. **orphaned_formulas_analysis.json** (auto-generated)
   - 259 formulas analyzed
   - Categorized by type and orphan status

6. **formula_relevance_assessment.json** (auto-generated)
   - Relevance decisions for all formulas

7. **missing_constants.json** (auto-generated)
   - 3 missing constants (xy_bosons)

---

## Validation Results

### PM Constant Integration: ✅ 92.5%
- 37/40 PM values from simulation
- 3/40 from config.py (geometric/theoretical)
- All formulas traceable to single source of truth

### Formula Database Completeness: ✅ 100%
- All active v8.4 physics covered
- 32 essential formulas documented
- Full metadata (derivation, references, PM values)

### Simulation Backing: ✅ Excellent
- Proton decay: proton_decay_rg_hybrid.py, proton_decay_v84_ckm.py
- PMNS matrix: pmns_full_matrix.py
- Dark energy: wz_evolution_desi_dr2.py
- KK spectrum: kk_spectrum_full.py
- Mass ordering: neutrino_mass_ordering.py

---

## Conclusion

Phase 1 of formula centralization is **complete**. We now have:

✅ **Single formula database** with 32 essential v8.4 formulas
✅ **92.5% PM constant coverage** from simulations
✅ **Full metadata** for tooltips and validation
✅ **Traceability** from config.py → simulations → formulas

Next phase will deploy agents to integrate orphaned content blocks and ensure all HTML pages use centralized formula references.

---

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

Developed with assistance from Claude (Anthropic), Grok (xAI), and Gemini (Google).
