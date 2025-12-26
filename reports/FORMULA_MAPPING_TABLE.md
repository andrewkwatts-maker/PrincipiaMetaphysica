# Formula Mapping Table: Paper ↔ theory_output.json

**Purpose:** Quick reference showing which paper equations are in theory_output.json

**Legend:**
- ✅ = Formula exists in theory_output.json with matching content
- ⚠️ = Partial match (formula exists but needs equation number mapping)
- ❌ = Missing from theory_output.json (needs to be added)
- 🔧 = In theory_output.json but not in paper (backend only or unused)

---

## Section 1: Introduction

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (1.1) | Dimensional cascade 26D→13D→6D→4D | ✅ | `reduction-cascade` |

---

## Section 2: 26-Dimensional Bulk Spacetime

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (2.1) | Master action S₂₆ | ✅ | `master-action-26d` |
| (2.2) | Virasoro anomaly c_total = D - 26 = 0 | ✅ | `virasoro-anomaly` |
| (2.3) | Master action with Pneuma (alternative form) | ❌ | `master-action-full` (proposed) |
| (2.4) | Pneuma stress-energy tensor | ❌ | `pneuma-stress-energy` (proposed) |
| (2.5) | Bekenstein-Hawking entropy | ✅ | `bekenstein-hawking` |
| (2.6) | Racetrack superpotential | ✅ | `racetrack-superpotential` |
| (2.7) | Scalar potential V(Ψ_P) | ✅ | `scalar-potential` |
| (2.8) | Vacuum stability ∂V/∂Ψ = 0 | ❌ | `racetrack-stability` (proposed) |
| (2.9) | Pneuma VEV ⟨Ψ_P⟩ | ✅ | `pneuma-vev` |

---

## Section 3: 13-Dimensional Shadow

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (3.1) | Sp(2,R) algebra [J,J] | ❌ | `sp2r-algebra` (proposed) |
| (3.1a) | Null constraint X² = 0 | ❌ | `sp2r-null-constraint` (proposed) |
| (3.1b) | Orthogonality X·P = 0 | ❌ | `sp2r-orthogonality` (proposed) |
| (3.1c) | Mass-shell P² = M² | ❌ | `sp2r-mass-shell` (proposed) |
| (3.2) | Primordial spinor Ψ₆₄ | ✅ | `primordial-spinor-13d` |
| (3.3) | Hidden variables ρ_Σ₁ | ✅ | `hidden-variables` |

---

## Section 4: TCS G₂ Compactification

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (4.1) | Betti numbers b₂=4, b₃=24 | ❌ | `tcs-betti-numbers` (proposed) |
| (4.1a) | Effective Euler χ_eff = 144 | ❌ | `effective-euler-characteristic` (proposed) |
| (4.2) | Generation number n_gen = 3 | ⚠️ | `generation-number` (needs eq #) |
| (4.3) | Flux quantization N_flux = 24 | ⚠️ | `flux-quantization` (needs eq #) |
| (4.4a) | Racetrack W(T) | ❌ | `kahler-racetrack` (proposed) |
| (4.4b) | Effective Planck mass | ❌ | `planck-mass-effective` (proposed) |
| (4.4c) | EW VEV with weights | ❌ | `ewsb-vev-weights` (proposed) |
| (4.4d) | Geometric hierarchy | ❌ | `hierarchy-geometric` (proposed) |
| - | Effective torsion T_ω = -1 | ✅ | `effective-torsion` |
| - | Mirror DM ratio Ω_DM/Ω_b | ✅ | `mirror-dm-ratio` |

---

## Section 5: Gauge Unification

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (5.1) | SO(10) breaking | ✅ | `so10-breaking` |
| (5.2) | GUT coupling α_GUT | ✅ | `gut-coupling` |
| (5.3) | GUT scale M_GUT | ❌ | `gut-scale-derivation` (proposed) |
| (5.3a) | Threshold corrections | ❌ | `threshold-corrections-general` (proposed) |
| (5.4a) | Gaugino condensate | ❌ | `gaugino-condensate` (proposed) |
| (5.4b) | U(1)_Y anomaly cancellation | ❌ | `anomaly-cancellation-u1` (proposed) |
| (5.4c) | Doublet-triplet splitting | ✅ | `doublet-triplet` |
| (5.5) | Weak mixing angle sin²θ_W | ✅ | `weak-mixing-angle` |
| (5.5a-10) | Additional gauge formulas | ❌ | (various) |
| (5.11) | Threshold corrections detailed | ❌ | (proposed) |

---

## Section 6: Fermion Sector

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (6.1) | Maximal atmospheric mixing θ₂₃ = 45° | ⚠️ | `theta23-maximal` (needs eq #) |
| (6.2) | Solar mass splitting Δm²₂₁ | ❌ | `neutrino-mass-21` (proposed) |
| (6.3) | Atmospheric mass splitting Δm²₃₁ | ⚠️ | `neutrino-mass-31` (needs eq #) |
| (6.3a) | Up-quark masses m_u, m_c | ❌ | `quark-masses-light-up` (proposed) |
| (6.3b) | Down-quark masses m_d, m_s | ❌ | `quark-masses-light-down` (proposed) |
| (6.4) | Top quark mass m_t | ❌ | `top-quark-mass` (proposed) |
| (6.5) | Bottom quark mass m_b | ❌ | `bottom-quark-mass` (proposed) |
| (6.6) | Tau mass m_τ | ❌ | `tau-lepton-mass` (proposed) |
| (6.7) | Strong coupling α_s(M_Z) | ❌ | `alpha-s-evolution` (proposed) |
| (6.8) | CP phase δ_CP | ✅ | `cp-phase-geometric` |
| (6.8) | Lepton masses m_e, m_μ | ❌ | `lepton-masses-light` (proposed) |
| (6.9) | CKM matrix definition | ❌ | `ckm-matrix-definition` (proposed) |
| (6.10) | CKM elements | ✅ | `ckm-elements` |
| - | Yukawa instanton | ✅ | `yukawa-instanton` |
| - | Seesaw mechanism | ✅ | `seesaw-mechanism` |

---

## Section 7: Cosmology and Dark Energy

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| (7.1) | Effective dimension d_eff | ❌ | `d-eff-formula` (proposed) |
| (7.2) | Dark energy w₀ | ⚠️ | `dark-energy-w0` (needs eq #) |
| (7.3) | Dark energy evolution w(z) | ❌ | `dark-energy-evolution` (proposed) |
| (7.4) | Evolution parameter w_a | ❌ | `dark-energy-wa` (proposed) |
| (7.5) | Attractor modulus φ_M | ❌ | `attractor-modulus` (proposed) |
| (7.6) | Attractor potential V(φ_M) | ✅ | `attractor-potential` |

---

## Section 8: Predictions

| Eq # | Formula | Status | theory_output ID |
|------|---------|--------|------------------|
| - | Proton lifetime τ_p | ✅ | `proton-lifetime` |
| - | KK graviton mass | ✅ | `kk-graviton-mass` |
| - | GW dispersion η | ✅ | `gw-dispersion-alt` |

---

## Backend-Only Formulas (in theory_output.json, not paper)

| theory_output ID | Description | Use Case |
|------------------|-------------|----------|
| `division-algebra` | 13D = R + H + O | Conceptual foundation |
| `dirac-pneuma` | (iΓD - m)Ψ = 0 | Implicit in master action |
| `planck-mass-derivation` | M_Pl from M_* and V₉ | Internal calculation |
| `higgs-vev` | v_EW from moduli | Derived parameter |
| `kms-condition` | Thermal equilibrium | Thermal time section |
| `ghost-coefficient` | γ = 0.5 | Dark energy calculation |
| `mirror-temp-ratio` | T'/T = 0.57 | Mirror sector |
| `pati-salam-chain` | Alternative breaking | Optional path |
| `higgs-potential` | V(H) = -μ²|H|² + λ|H|⁴ | Standard SM |
| `rg-running-couplings` | dα/dlnμ equations | RG evolution |

---

## Summary Statistics

### By Status
- ✅ **Matched:** 20 formulas (fully synchronized)
- ⚠️ **Partial:** 5 formulas (need equation number mapping)
- ❌ **Missing:** ~40 formulas (need to be added)
- 🔧 **Backend-only:** 10 formulas (legitimate or unused)

### By Section
| Section | Total Eqs | In DB | Missing | Coverage |
|---------|-----------|-------|---------|----------|
| 1. Introduction | 1 | 1 | 0 | 100% |
| 2. 26D Bulk | 9 | 5 | 4 | 56% |
| 3. 13D Shadow | 6 | 2 | 4 | 33% |
| 4. TCS G₂ | 10 | 4 | 6 | 40% |
| 5. Gauge | 12+ | 4 | 8+ | ~33% |
| 6. Fermions | 15+ | 6 | 9+ | ~40% |
| 7. Cosmology | 6 | 2 | 4 | 33% |
| **Total** | **~60** | **~24** | **~36** | **~40%** |

---

## Recommended Actions

### Immediate (Priority 1)
1. Add equation numbers to 5 partial matches:
   - `generation-number` → (4.2)
   - `flux-quantization` → (4.3)
   - `theta23-maximal` → (6.1)
   - `neutrino-mass-31` → (6.3)
   - `dark-energy-w0` → (7.2)

2. Add 10 critical missing formulas:
   - Pneuma stress-energy (2.4)
   - Sp(2,R) constraints (3.1a-c)
   - Betti numbers (4.1)
   - GUT scale derivation (5.3)
   - Top/bottom/tau masses (6.4-6.6)

### Short-term (Priority 2)
3. Add remaining Section 4-6 formulas (~25 equations)

### Medium-term (Priority 3)
4. Review backend-only formulas for paper inclusion
5. Add appendix equations (if needed for reproducibility)

---

**Last Updated:** 2025-12-26
**Source:** audit_paper_formulas.py analysis
**See also:** FORMULAS_TO_ADD.md for detailed formula specifications
