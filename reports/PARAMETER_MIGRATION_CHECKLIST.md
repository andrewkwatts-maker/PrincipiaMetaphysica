# Parameter Migration Checklist - Old Paper to New Paper

**Generated:** 2025-12-15
**Version:** v12.8 FINAL
**Total Parameters:** ~80 across all categories
**Audit Complete:** YES (6 parallel agents)

---

## Migration Status Legend

- ✅ MIGRATED - Full derivation chain in new paper
- ⚠️ PARTIAL - Present but needs derivation enhancement
- ✗ MISSING - Not in new paper, needs migration
- 📋 TABLE ONLY - Value in summary table, no derivation section

---

## Category 1: Dimensions & Topology (~13 params) - Score: 70%

| Parameter | Value | Old Paper | New Paper | Status |
|-----------|-------|-----------|-----------|--------|
| D_bulk | 26 | ✅ | ✅ | ✅ MIGRATED (Virasoro) |
| D_after_sp2r | 13 | ✅ | ⚠️ | ⚠️ PARTIAL (needs Sp(2,R) detail) |
| D_internal | 7 | ✅ | ✅ | ✅ MIGRATED (G₂ ref) |
| D_effective | 6 | ✅ | ✅ | ✅ MIGRATED |
| D_common | 4 | ✅ | ✅ | ✅ MIGRATED |
| b2 | 4 | ✅ | ⚠️ | ⚠️ PARTIAL (needs CY derivation) |
| b3 | 24 | ✅ | ✅ | ✅ MIGRATED |
| chi_eff | 144 | ✅ | ⚠️ | ⚠️ PARTIAL (needs flux calc) |
| nu | 24 | ✅ | ✅ | ✅ MIGRATED |
| n_gen | 3 | ✅ | ✅ | ✅ MIGRATED (EXCELLENT) |
| Cl(24,2) dim | 8192 | ✅ | ⚠️ | ⚠️ PARTIAL (needs justification) |
| Z2 factor | 2 | ✅ | ✅ | ✅ MIGRATED |
| TCS manifold | #187 | ✅ | ✅ | ✅ MIGRATED |

---

## Category 2: GUT & Proton Decay (~14 params) - Score: 68%

| Parameter | Value | Old Paper | New Paper | Status |
|-----------|-------|-----------|-----------|--------|
| M_GUT | 2.118e16 GeV | ✅ | ✅ | ✅ MIGRATED |
| alpha_GUT_inv | 23.54 | ✅ | ⚠️ | ⚠️ PARTIAL (24.10→23.54 gap) |
| alpha_GUT | 0.0425 | ✅ | ✅ | ✅ MIGRATED |
| T_omega | -0.884 | ✅ | ✅ | ✅ MIGRATED |
| tau_p | 3.91e34 yr | ✅ | ✅ | ✅ MIGRATED |
| tau_p_MC | ±0.74e34 | ✅ | ⚠️ | ⚠️ PARTIAL (propagation unclear) |
| Super-K bound | 2.4e34 yr | ✅ | ⚠️ | ⚠️ PARTIAL (1.67 vs 2.4 inconsistency) |
| M_X | 2.118e16 GeV | ✅ | ✗ | ✗ MISSING |
| M_Y | 2.118e16 GeV | ✅ | ✗ | ✗ MISSING |
| charge_X | 4/3 | ✅ | ✗ | ✗ MISSING |
| charge_Y | 1/3 | ✅ | ✗ | ✗ MISSING |
| N_X_bosons | 12 | ✅ | ✗ | ✗ MISSING |
| N_Y_bosons | 12 | ✅ | ✗ | ✗ MISSING |
| BR(e+pi0) | 0.25 | ✅ | ✅ | ✅ MIGRATED |
| **kappa** | **1.46** | ✅ | ✗ | **✗ CRITICAL MISSING** |
| **s_parameter** | **1.178** | ✅ | ⚠️ | **⚠️ CRITICAL (ν undefined)** |

---

## Category 3: PMNS & Neutrino (~15 params) - Score: 65%

| Parameter | Value | Old Paper | New Paper | Status |
|-----------|-------|-----------|-----------|--------|
| theta_23 | 45.0° | ✅ | ✅ | ✅ MIGRATED (EXCELLENT) |
| theta_12 | 33.59° | ✅ | ✅ | ✅ MIGRATED |
| theta_13 | 8.57° | ✅ | ✅ | ✅ MIGRATED (calibrated) |
| delta_CP | 235° | ✅ | ✅ | ✅ MIGRATED (calibrated) |
| **m1** | **0.83 meV** | ✅ | ✗ | **✗ MISSING (only splittings)** |
| **m2** | **8.97 meV** | ✅ | ✗ | **✗ MISSING** |
| **m3** | **50.3 meV** | ✅ | ✗ | **✗ MISSING** |
| sum_masses | 60.1 meV | ✅ | ✗ | ✗ MISSING |
| delta_m21_sq | 7.97e-5 eV² | ✅ | ✅ | ✅ MIGRATED |
| delta_m31_sq | 2.525e-3 eV² | ✅ | ✅ | ✅ MIGRATED |
| NH probability | 76% | ✅ | ✅ | ✅ MIGRATED |
| Seesaw M_R1 | 5.1e13 GeV | ✅ | ⚠️ | ⚠️ PARTIAL (narrative missing) |
| Suppression | 124.22 | ✅ | ⚠️ | ⚠️ PARTIAL |
| alpha_4 | 0.576152 | ✅ | ⚠️ | **⚠️ CRITICAL (source undefined)** |
| alpha_5 | 0.576152 | ✅ | ⚠️ | **⚠️ CRITICAL (source undefined)** |

---

## Category 4: Dark Energy & Cosmology (~10 params) - Score: 60%

| Parameter | Value | Old Paper | New Paper | Status |
|-----------|-------|-----------|-----------|--------|
| w0 | -0.8528 | ✅ | ✅ | ✅ MIGRATED |
| wa | -0.95 | ✅ | ✅ | ✅ MIGRATED |
| d_eff | 12.576 | ✅ | ✅ | ✅ MIGRATED |
| **alpha_T** | **2.7** | ✅ | ✗ | **✗ CRITICAL MISSING (no derivation)** |
| gamma_ghost | 0.5 | ✅ | ✅ | ✅ MIGRATED |
| w0_DESI | -0.83 | ✅ | ✅ | ✅ MIGRATED |
| wa_DESI | -0.75 | ✅ | ✅ | ✅ MIGRATED |
| w0_sigma | 0.38σ | ✅ | ✅ | ✅ MIGRATED |
| w(z) form | log | ✅ | ⚠️ | ⚠️ PARTIAL (justification weak) |
| eta_GW | 0.113 | ✅ | ⚠️ | ⚠️ PARTIAL (0.113 vs 0.101) |

---

## Category 5: Fermion Masses & Yukawa (~15 params) - Score: 20%

| Parameter | Value | Old Paper | New Paper | Status |
|-----------|-------|-----------|-----------|--------|
| m_t | 172.7 GeV | ✅ | ✅ | ✅ MIGRATED |
| **m_b** | **4.18 GeV** | ✅ | 📋 | **📋 TABLE ONLY (no derivation)** |
| **m_tau** | **1.777 GeV** | ✅ | 📋 | **📋 TABLE ONLY (no derivation)** |
| **m_u** | **2.2 MeV** | ✅ | ✗ | **✗ MISSING** |
| **m_c** | **1.27 GeV** | ✅ | ✗ | **✗ MISSING** |
| **m_d** | **4.7 MeV** | ✅ | ✗ | **✗ MISSING** |
| **m_s** | **95 MeV** | ✅ | ✗ | **✗ MISSING** |
| **m_e** | **0.511 MeV** | ✅ | ✗ | **✗ MISSING** |
| **m_mu** | **105.7 MeV** | ✅ | ✗ | **✗ MISSING** |
| **|V_ud|** | **0.974** | ✅ | ✗ | **✗ MISSING** |
| **|V_us|** | **0.225** | ✅ | ✗ | **✗ MISSING** |
| **|V_ub|** | **0.0036** | ✅ | ✗ | **✗ MISSING** |
| **|V_cb|** | **0.041** | ✅ | ✗ | **✗ MISSING** |
| y_t | ~1.0 | ✅ | ⚠️ | ⚠️ PARTIAL (stated not derived) |
| y_b/y_t | 0.024 | ✅ | ✗ | ✗ MISSING |

---

## Category 6: Gauge & Higgs (~10 params) - Score: 55%

| Parameter | Value | Old Paper | New Paper | Status |
|-----------|-------|-----------|-----------|--------|
| **alpha_s(M_Z)** | **0.1179** | ✅ | ✗ | **✗ CRITICAL MISSING** |
| **alpha_em(M_Z)** | **1/137** | ✅ | ✗ | **✗ CRITICAL MISSING** |
| sin2_theta_W | 0.23121 | ✅ | ✅ | ✅ MIGRATED |
| m_h | 125.10 GeV | ✅ | ⚠️ | ⚠️ PARTIAL (CONSTRAINED not derived) |
| Re(T) | 7.086 | ✅ | ⚠️ | ⚠️ PARTIAL (from m_h constraint) |
| v_EW | 173.97 GeV | ✅ | ✅ | ✅ MIGRATED |
| m_KK | 5.0 TeV | ✅ | ✅ | ✅ MIGRATED |
| M_Z | 91.19 GeV | ✅ | ✅ | ✅ MIGRATED |
| M_W | 80.38 GeV | ✅ | ✅ | ✅ MIGRATED |
| **lambda_0** | **0.1289** | ✅ | ✗ | **✗ CRITICAL MISSING** |
| **lambda_eff** | **?** | ✅ | ✗ | **✗ CRITICAL MISSING** |
| VEV coeff | 1.5859 | ✅ | ✅ | ✅ MIGRATED (calibrated) |

---

## Summary Statistics

### Overall Migration Status:

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ MIGRATED | 35 | 44% |
| ⚠️ PARTIAL | 18 | 23% |
| ✗ MISSING | 20 | 25% |
| 📋 TABLE ONLY | 2 | 3% |
| **CRITICAL** | **7** | **9%** |

### Critical Items Requiring Immediate Action:

1. **κ = 1.46** - GUT exponent coefficient (no derivation)
2. **α_T = 2.7** - Thermal friction (no Tomita-Takesaki derivation)
3. **α₄ = α₅ = 0.576152** - Torsion parameters (source undefined)
4. **α_s(M_Z)** - Strong coupling (completely missing)
5. **α_em(M_Z)** - EM coupling (completely missing)
6. **λ₀, λ_eff** - Higgs quartic couplings (not documented)
7. **Fermion sector** - 8 masses + 4 CKM elements missing

---

## Implementation Priority Queue

### Week 1 (Highest Impact):
1. Add fermion mass derivation sections (6.2c-6.2f)
2. Add CKM matrix section (6.2g)
3. Add α_T derivation from Tomita-Takesaki (7.2a)

### Week 2:
4. Add κ = 1.46 derivation (Appendix E.4)
5. Add α_s, α_em sections (5.2b, 5.2c)
6. Add individual neutrino masses to Appendix L

### Week 3:
7. Clarify α₄, α₅ source (Section 6.1 expansion)
8. Add λ₀ quartic coupling derivation
9. Add XY boson properties

### Week 4 (Polish):
10. Resolve η_GW value ambiguity
11. Resolve Super-K bound inconsistency
12. Expand b2, χ_eff derivations
13. Add Higgs constraint transparency section

---

**Agent Assignment Completed:**
- Agent 1: Categories 1 (Dimensions & Topology) ✅
- Agent 2: Category 2 (GUT & Proton Decay) ✅
- Agent 3: Category 3 (PMNS & Neutrino) ✅
- Agent 4: Category 4 (Dark Energy & Cosmology) ✅
- Agent 5: Category 6 (Gauge & Higgs) ✅
- Agent 6: Category 5 (Fermion Masses) ✅

---

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
