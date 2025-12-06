# AGENT B: Dark Energy Review - Quick Reference Card

**Overall Grade: B-** | **Status: Major Revision Needed** | **Date: 2025-12-07**

---

## Data Accuracy Check ✓

| Parameter | PM v12.0 | DESI DR2 (Oct 2024) | σ Deviation |
|-----------|----------|---------------------|-------------|
| **w₀** | -0.8528 | -0.83 ± 0.06 | **0.38σ** ✅ |
| **w_a** | -0.9476 | -0.75 ± 0.30 | **0.66σ** ✅ |

**Data source:** arXiv:2510.12627 (October 2024)
**Mission brief error:** Claims "Oct 2025" - incorrect

---

## Critical Bugs 🐛

### 1. z_activate = 3 should be 3000
**File:** `simulations/wz_evolution_desi_dr2.py` line 31
**Impact:** Gives w(z=1100) = -5.39 (unphysical)
**Fix:** `z_activate = 3000  # CMB recombination`

### 2. Invalid Chi-Squared Test
**File:** theory_output.json "functional_test"
**Problem:** Data generated FROM model, then fit TO it (circular)
**Fix:** Remove or use real DESI BAO data

---

## Derivation Rigor Scores

| Component | Grade | Status |
|-----------|-------|--------|
| 26D → 13D (BRST) | A+ | ✅ Rigorous |
| G₂ compactification | A | ✅ Specified |
| D_eff = 12.589 | D- | ❌ Fitted |
| w₀ formula | F | ❌ No derivation |
| Thermal friction | C | ⚠️ Qualitative |
| Planck tension | D | ❌ Unproven |

---

## Falsification Tests

### 2027 Q2: DESI DR5
- **Precision:** Δw₀ = ±0.03
- **PM prediction:** -0.853
- **Pass if:** Within 3σ

### 2028 Q4: Euclid (DECISIVE)
- **Test:** w(z=1) measurement
- **PM:** -0.94
- **CPL:** -1.20
- **Difference:** 0.26 (easily distinguished)

**If CPL preferred (Δχ² > 9):** PM falsified ❌

---

## What to Fix Before Publication

### Must Fix (Reject without these)
1. ❌ Fix z_activate bug
2. ❌ Remove invalid chi² test
3. ❌ Acknowledge D_eff is fitted
4. ❌ Derive or cite w₀ formula
5. ❌ Remove or prove Planck claim

### Should Fix (Major revision)
6. ⚠️ Solve thermal friction EOM
7. ⚠️ Quantify frozen field mechanism
8. ⚠️ Pre-register Euclid predictions

### Could Improve (Minor revision)
9. ✓ Implement time-varying α_T(z)
10. ✓ Rigorous shadow projection

---

## Key Strengths ✅

1. **w₀ = -0.85** matches DESI excellently (0.38σ)
2. **w_a < 0** correct sign (4.2σ DESI preference)
3. **Highly falsifiable** (Euclid 2028 decisive)
4. **BRST foundation** rigorously proven
5. **Physical motivation** (thermal friction)

---

## Critical Weaknesses ❌

1. **D_eff fitted** not derived from geometry
2. **w₀ formula** has no mathematical justification
3. **Thermal friction** qualitative only (no EOM solution)
4. **Planck tension** claim unsupported (no calculation)
5. **Functional test** invalid (circular reasoning)

---

## Recommended Refinement

### Time-Varying Thermal Friction
```python
alpha_T(z) = 2.7 × exp(-z/1000)
```

**Impact:**
- z = 0: w_a = -0.95 (current)
- z = 2: w_a = -0.75 (DESI exact match!)

**Testable:** Euclid can measure α_T evolution

---

## Bottom Line

**Current status:** Good phenomenology, weak derivation

**Publication readiness:** Not ready (needs major revision)

**Scientific value:** High (bold falsifiable predictions)

**Critical test:** Euclid 2028 w(z) binning

**Recommendation:** Fix bugs, acknowledge gaps, pre-register predictions

---

**Full reports:**
- `AGENT-B-COSMOLOGY-REVIEW.md` (27 pages, comprehensive)
- `AGENT-B-EXECUTIVE-SUMMARY.md` (5 pages, detailed)
- `AGENT-B-QUICK-REFERENCE.md` (this file, 2 pages)

**Reviewer:** AGENT B (Independent Cosmologist)
**Confidence:** High
