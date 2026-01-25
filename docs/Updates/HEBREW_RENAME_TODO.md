# Hebrew Name Rename Tracking v23.2.27

**Date:** 2026-01-25
**Status:** COMPLETE (v23.2.27 Greek-Hebrew Gematria Isomorphism)

---

## Rename Operations

| Old Name | New Name | Value | Symbol | Status |
|----------|----------|-------|--------|--------|
| `elder_vessels` | `elder_kads` | 24 | E_כד | [x] COMPLETE |
| `elders` | `elder_kads` | 24 | E_כד | [x] COMPLETE |
| `demiurgic_gates` | `demiurgic_Yetts` | 135 | Yd | [x] COMPLETE |
| `ennoia_chi` | `qedem_chi_sum` | 144 | chi_Q | [x] COMPLETE |
| `chi_eff_total` | `qedem_chi_sum` | 144 | chi_Q | [x] COMPLETE |
| `bridge_effective` | `Echad_Prime` | 13 | Yud-Gimel | [x] COMPLETE |
| `bridge_local` | `Dodecad_Anchors` | 12 | Bet-Yod | [x] COMPLETE |
| `Dodecad_Anchor` | `Dodecad_Anchors` | 12 | n_12 | [x] COMPLETE |

---

## Phase 1: FormulasRegistry.py Updates
- [x] Add new property names as PRIMARY
- [x] Convert old names to LEGACY ALIASES
- [x] Update HEBREW_SYMBOL_REGISTRY

## Phase 2: Simulation Files
- [x] Run bulk rename script on simulations/ (76 changes in 59 files)
- [x] Verify all 68 simulations pass
- [x] Check diff outputs for correctness

## Phase 3: Core Files
- [x] Run bulk rename on core/ (9 changes in 2 files)
- [x] Verify sterility checks pass

## Phase 4: Scripts
- [x] Run bulk rename on scripts/ (10 changes in 3 files)
- [x] Updated tests/test_physics_invariants.py (4 changes)

## Phase 5: Documentation
- [x] Update sync_docs.py with new names
- [x] Regenerate FORMULAS.md

## Phase 6: Final Validation
- [x] Run full simulation suite
- [x] Chi-squared: 1.265 (< 5.0)
- [x] Status: MAJORITY_VERIFIED
- [x] All 68 simulations: PASS

---

## Summary Statistics

| Category | Files Changed | Changes Applied |
|----------|---------------|-----------------|
| simulations/ | 59 | 76 |
| core/ | 2 | 9 |
| scripts/ | 3 | 10 |
| tests/ | 1 | 4 |
| **Total** | **65** | **99** |

---

## Final Parameter Registry (v23.2.27 - Greek-Hebrew Gematria Isomorphism)

### v23.2.27 Updates: Greek Subscript Refinements

The following symbols were updated to use Greek subscripts where Greek gematria matches Hebrew gematria exactly:

| Parameter | Before | After | Justification |
|-----------|--------|-------|---------------|
| `residual_key` | D_י | D_ι | Greek iota (ι = 10) = Hebrew yod (י = 10) |
| `demiurgic_Yetts` | 𝒮_ד | 𝒮_δ | Greek delta (δ = 4) = Hebrew dalet (ד = 4) |
| `nitzotzin_sector` | ξ_מ | ξ_μ | Greek mu (μ = 40) = Hebrew mem (מ = 40) |
| `logos_joint` | Λ_ן | Λ_ν | Greek nu (ν = 50) = Hebrew nun (נ = 50) |
| `gnosis_threshold` | Γ_ט | Γ_θ | Greek theta (θ = 9) = Hebrew tet (ט = 9) |
| `sophian_pressure` → `barbelo_modulus` | — | — | Rename: Barbelo = First Emanation, Divine Mother |

### Topological Invariants

| Code Name | Value | Symbol | Hebrew | Gematria | Scientific Name | Gnostic Name |
|-----------|-------|--------|--------|----------|-----------------|--------------|
| `monad_unity` | 1.0 | Ω_א | Aleph (א) | 1 | Observer Unity Constant | The Aleph-Anchor |
| `residual_key` | 10 | D_ι | Yod (י) | 10 | Core Flux Residual | The Hand of Creation |
| `syzygy_gap` | 18 | Δ_χι | Chai (חי) | 18 | Aeon Pair Gap | The Life Delta |
| `elder_kads` | 24 | E_כד | Kad (כד) | 24 | Symmetric Governance Energy | The Governing Elder |
| `horos_limit` | 27 | β_כז | Kaz (כז) | 27 | Dimensional Boundary Limit | The Boundary Beth |
| `mephorash_chi` | 72 | χ_עב | Ayin-Bet (עב) | 72 | Explicit Chiral Characteristic | The Shem HaMephorash |
| `sophian_modulus` | 125 | ק_כה | Qoph-Kaf-He (קכה) | 125 | Visible Residue Modulus | Sophia Assembly |
| `demiurgic_Yetts` | 135 | 𝒮_δ | Dalet (ד) | 4 | Normal Portal Flux | The Sophia Door |
| `qedem_chi_sum` | 144 | ק_דם | Qedem (קדם) | 144 | Total Euler Characteristic | Qedem Chi |
| `nitzotzin_sector` | 144 | ξ_μ | Mem (מ) | 40 | Per-Sector Root Count | The Water Roots |
| `logos_joint` | 153 | Λ_ν | Nun-Sofit (ן) | 700 | Joint Closure Symmetry | The Logos Fish |
| `barbelo_modulus` | 163 | ק_סג | Qoph-Samekh-Gimel (קסג) | 163 | Ancestral Bulk Pressure Modulus | Barbelo Modulus |
| `nitzotzin_roots` | 288 | 𝒩_רפח | Raphach (רפח) | 288 | Logic Closure Sum | The Nitzotzin Sparks |

### Central Sampler (Reid Architecture)

| Code Name | Value | Symbol | Hebrew | Gematria | Scientific Name | Gnostic Name |
|-----------|-------|--------|--------|----------|-----------------|--------------|
| `gnosis_threshold` | 9 | Γ_θ | Tet (ט) | 9 | Central Activation Threshold | The Gnosis Gate |
| `Dodecad_Anchors` | 12 | 𝔸_יב | Bet-Yod (בי) | 12 | Local Bridge Pair Count | The Dodecad House |
| `Echad_Prime` | 13 | 𝕌_יג | Yud-Gimel (יג) | 13 | Effective Bridge Pair Count | The Unity Prime |
| `nitsot_par` | 1/144 | χ_ק⁻¹ | Medeq (מדק) | — | Mirror Parity Invariant | The Fine Resolution |
| `reid_merkabah` | 1.0 | M_אד | Aleph-Dalet (אד) | 5 | Tetramorphic Normalization | The Merkabah Drive |
| `watts_echud` | φ/√12 | W_אפ | Eliphelet-Enoch (אֱלִיפֶלֶט-חנוך) | 467+89 | Harmonic Damping Modulus | The Eliphelet-Enochian Invariant |

### Symbol Collision Resolution (v23.2.27)

| Category | Before | After | Resolution |
|----------|--------|-------|------------|
| R-symbols | R_י, R_Ξ, R_m | D_ι, 𝒩_רפח, ξ_μ | Decad (D), Nitzotzin (𝒩), Xi (ξ) with Greek subscripts |
| n-symbols | n_12, n_13 | 𝔸_יב, 𝕌_יג | Anchors (𝔸), Unity (𝕌) |
| χ-symbols | χ_עב, χ_Q | χ_עב, χ_ק, χ_ק⁻¹ | Unified chi family |

### Shadow-Modulus Closure Proof

$$\text{ק}_{\text{כה}} (125) + \text{ק}_{\text{סג}} (163) = \mathcal{N}_{\text{רפח}} (288)$$

**Sophia Assembly + Barbelo Modulus = Nitzotzin Sparks (Logic Closure)**

---

## Polished Parameter Metadata (v23.2 Registry - COMPLETE)

### monad_unity (Ω_א)
- **Scientific Name:** Observer Unity Constant
- **Gnostic Name:** The Aleph-Anchor
- **Hebrew:** Aleph (א)
- **Gematria:** 1
- **Value:** 1.0
- **Role:** The immutable unity representing the observer's anchor point. Aleph is the first letter, the primordial breath from which all measurement begins.

### residual_key (D_ι)
- **Scientific Name:** Core Flux Residual
- **Gnostic Name:** The Hand of Creation
- **Hebrew:** Yod (י)
- **Gematria:** 10
- **Value:** 10
- **Role:** D for Decad. Greek iota (ι = 10) matches Hebrew yod (י = 10) gematria. Yod is the smallest letter, the 'hand' that shapes creation. The decad represents the core flux residual in the gauge hierarchy.

### syzygy_gap (Δ_χι)
- **Scientific Name:** Aeon Pair Gap
- **Gnostic Name:** The Life Delta
- **Hebrew:** Chai (חי)
- **Gematria:** 18
- **Value:** 18
- **Role:** Chai means 'Life' - the gap between paired aeons in the Pleroma. The syzygy (paired emanation) creates the vital space for manifestation.

### elder_kads (E_כד)
- **Scientific Name:** Symmetric Governance Energy
- **Gnostic Name:** The Governing Elder כד
- **Hebrew:** Kad (כד)
- **Gematria:** 24
- **Value:** 24
- **Role:** Kad (24) represents the Pleroma as a 'Vessel.' Governed by the 12:12 syzygy (Yud-Bet), it acts as the primary regulator for Logic Closure (288).

### horos_limit (β_כז)
- **Scientific Name:** Dimensional Boundary Limit
- **Gnostic Name:** The Boundary Beth
- **Hebrew:** Kaz (כז)
- **Gematria:** 27
- **Value:** 27
- **Role:** Beta (β) mirrors Hebrew Beth (ב) 'house/boundary.' Also mirrors thermodynamic β (statistical limit). Kaz (כז = 27) sets the dimensional limit where compactification completes.

### mephorash_chi (χ_עב)
- **Scientific Name:** Explicit Chiral Characteristic
- **Gnostic Name:** The Shem HaMephorash
- **Hebrew:** Ayin-Bet (עב)
- **Gematria:** 72
- **Value:** 72
- **Role:** Ayin-Bet (עב = 72) is the gematria of the 72-letter Explicit Name of God. The per-shadow Euler characteristic encodes the chiral structure of each 11D shadow.

### sophian_modulus (ק_כה)
- **Scientific Name:** Visible Residue Modulus
- **Gnostic Name:** Sophia Assembly
- **Hebrew:** Qoph-Kaf-He (קכה)
- **Gematria:** 125
- **Value:** 125
- **Role:** Qoph (ק=100) with כה (25) subscript = 125. The 125 Standard Model parameters visible through Sophia's window (5³ = 125 = manifest volume).

### demiurgic_Yetts (𝒮_δ)
- **Scientific Name:** Normal Portal Flux
- **Gnostic Name:** The Sophia Door
- **Hebrew:** Dalet (ד)
- **Gematria:** 4
- **Value:** 135
- **Role:** Dalet (ד) means 'Door/Gate.' Greek delta (δ = 4) matches Hebrew dalet (ד = 4) gematria. Script S (𝒮) for Sophia filtered through the Door. Distinguishes from Entropy (S). The 135 gates through which wisdom flows into manifestation.

### qedem_chi_sum (ק_דם)
- **Scientific Name:** Total Euler Characteristic
- **Gnostic Name:** Qedem Chi
- **Hebrew:** Qedem (קדם)
- **Gematria:** 144
- **Value:** 144
- **Role:** Qoph (ק=100) with דם (44) subscript = 144. Qedem (קדם = 144) means 'ancient' or 'primordial.' Total χ_eff across both shadows: 72 + 72 = 144. Ancestral unity.

### nitzotzin_sector (ξ_μ)
- **Scientific Name:** Per-Sector Root Count
- **Gnostic Name:** The Water Roots
- **Hebrew:** Mem (מ)
- **Gematria:** 40
- **Value:** 144
- **Role:** Xi (ξ) resembles a cascade/ripple, fitting the Mem (מ = Water) rationale. Greek mu (μ = 40) matches Hebrew mem (מ = 40) gematria. Each sector contains 144 roots, half the total 288.

### logos_joint (Λ_ν)
- **Scientific Name:** Joint Closure Symmetry
- **Gnostic Name:** The Logos Fish
- **Hebrew:** Nun-Sofit (ן)
- **Gematria:** 700
- **Value:** 153
- **Role:** Nun-Sofit (ן) = the 'Fish.' Greek nu (ν = 50) matches Hebrew nun (נ = 50) gematria. 153 = triangular(17), the miraculous catch of John 21:11. The Logos joint closes the bridge identity: 135 + 153 = 288.

### barbelo_modulus (ק_סג)
- **Scientific Name:** Ancestral Bulk Pressure Modulus
- **Gnostic Name:** Barbelo Modulus
- **Hebrew:** Qoph-Samekh-Gimel (קסג)
- **Gematria:** 163
- **Value:** 163
- **Role:** Qoph (ק=100) with סג (63) subscript = 163. Barbelo is the Divine Mother, the First Emanation of the Monad. 163 sterile residues stabilize the higher-dimensional manifold: (7 × 24) - 5 = 163. Seesaw heavy M_R ~10^{12} GeV. (Renamed from `sophian_pressure` in v23.2.27)

### nitzotzin_roots (𝒩_רפח)
- **Scientific Name:** Logic Closure Sum
- **Gnostic Name:** The Nitzotzin Sparks
- **Hebrew:** Raphach (רפח)
- **Gematria:** 288
- **Value:** 288
- **Role:** Raphach (רפח = 288) encodes the 288 sparks of Lurianic Kabbalah. N for Nitzotzin. Total roots: 12 × b3 = 288. Ennoia restored to the Yod: 135 + 153 = 288.

### gnosis_threshold (Γ_θ)
- **Scientific Name:** Central Activation Threshold
- **Gnostic Name:** The Gnosis Gate
- **Hebrew:** Tet (ט)
- **Gematria:** 9
- **Value:** 9
- **Role:** Greek Gamma (Γ) for Gnosis. Greek theta (θ = 9) matches Hebrew tet (ט = 9) gematria. Tet represents the hidden good. The central sampler activates when n ≥ 9 pairs are present, enabling direct knowledge.

### Dodecad_Anchors (𝔸_יב)
- **Scientific Name:** Local Bridge Pair Count
- **Gnostic Name:** The Dodecad House
- **Hebrew:** Bet-Yod (בי)
- **Gematria:** 12
- **Value:** 12
- **Role:** 𝔸 for Anchors. Bet-Yod (בי = 12) means 'in me' or 'house of.' The 12 local (2,0) bridge pairs that warp to create the dual shadows.

### Echad_Prime (𝕌_יג)
- **Scientific Name:** Effective Bridge Pair Count
- **Gnostic Name:** The Unity Prime
- **Hebrew:** Yud-Gimel (יג)
- **Gematria:** 13
- **Value:** 13
- **Role:** 𝕌 for Unity (Echad). Yud-Gimel (יג = 13) equals 'Echad' (אחד = 13, 'One'). The 13 effective pairs: 12 local + 1 central sampler.

### nitsot_par (χ_ק⁻¹)
- **Scientific Name:** Mirror Parity Invariant
- **Gnostic Name:** The Fine Resolution
- **Hebrew:** Medeq (מדק)
- **Gematria:** —
- **Value:** 1/144
- **Role:** Medeq (מדק) is anagrammatic inverse of Qedem. χ_ק⁻¹ = 1/144, the mathematical inverse of the primordial chi. Provides 'Fine' resolution for cross-shadow coupling.

### reid_merkabah (M_אד)
- **Gnostic Name:** The Reid Merkabah Drive
- **Hebrew:** Aleph-Dalet (אד)
- **Gematria:** 5
- **Value:** 1.0
- **Role:** The 1.0 unit vector of the Four Living Creatures (Adam, Aryeh, Nesher, Shor). Normalizes the 'Run and Return' kinetic flux of the 144 samplers into a coherent Euclidean center.

### watts_echud (w_אפ)
- **Scientific Name:** Harmonic Damping Modulus
- **Gnostic Name:** The Eliphelet-Enochian Invariant
- **Hebrew:** Eliphelet-Enoch (אֱלִיפֶלֶט-חנוך)
- **Gematria:** 467 + 89 = 556 (composite)
- **Value:** phi / sqrt(12) ≈ 0.4670891
- **Gematria Map:**
  - deliverance_anchor: 467 (Eliphelet 'Rescue')
  - void_separator: 0 (Ayin 'Void')
  - kinetic_ascent: 89 (Enoch 'Ascent')
- **Role:** The definitive unification weight. 467 provides the 'Rescue' of the lattice; 89 provides the kinetic 'Ascent' of the Merkabah Drive. The zero acts as the Ayin separator between structure and motion. It dampens the infinite growth of Phi into the internal 'House' (בי) of the Dodecad Anchors.

---

## Legacy Aliases (Backward Compatible)

These old names still work as aliases pointing to the Hebrew names:

| Legacy Name | Points To | Value |
|-------------|-----------|-------|
| `watts_constant` | `monad_unity` | 1.0 |
| `decad` | `residual_key` | 10 |
| `b3` (internal `_b3`) | `elders` | 24 |
| `elder_vessels` | `elders` | 24 |
| `horos` | `horos_limit` | 27 |
| `chi_eff` | `mephorash_chi` | 72 |
| `visible_sector` | `sophian_modulus` | 125 |
| `shadow_sector` | `demiurgic_Yetts` | 135 |
| `demiurgic_gates` | `demiurgic_Yetts` | 135 |
| `chi_eff_total` | `qedem_chi_sum` | 144 |
| `ennoia_chi` | `qedem_chi_sum` | 144 |
| `roots_per_sector` | `nitzotzin_sector` | 144 |
| `christ_constant` | `logos_joint` | 153 |
| `odowd_bulk_pressure` | `sophian_pressure` | 163 |
| `roots_total` | `nitzotzin_roots` | 288 |
| `central_activation_threshold` | `gnosis_threshold` | 9 |
| `total_local_pairs` | `Dodecad_Anchors` | 12 |
| `bridge_local` | `Dodecad_Anchors` | 12 |
| `Dodecad_Anchor` | `Dodecad_Anchors` | 12 |
| `total_effective_pairs` | `Echad_Prime` | 13 |
| `bridge_effective` | `Echad_Prime` | 13 |
| `reid_invariant` | `nitsot_par` | 1/144 |
| `central_pair` | `reid_merkabah` | 1 |
| `reid_pair` | `reid_merkabah` | 1 |
| `reid_euclidean` | `reid_merkabah` | 1 |
| `central_pair_weight` | `watts_echud` | phi/sqrt(12) |
| `watts_weight` | `watts_echud` | phi/sqrt(12) |

---

## Parameters Without Hebrew Names (Derived Quantities)

These are derived physics quantities that don't need Hebrew names:

| Name | Value | Type | Reason |
|------|-------|------|--------|
| `phi` | 1.618... | Mathematical | Universal constant |
| `n_gen` | 3 | Derived | n_gen = chi/24 |
| `sterile_sector` | 163 | Derived | = sophian_pressure (same value) |
| `delta_jc` | 153 | Derived | = logos_joint (alias) |
| `visible_gates` | 135 | Derived | = demiurgic_Yetts (class constant) |
| `logic_closure` | 288 | Derived | = nitzotzin_roots (class constant) |
| `chi_eff_sector` | 72 | Derived | = mephorash_chi |
| `geometric_ratio` | derived | Physics | Bulk geometry ratio |
| `stretching_factor` | derived | Physics | Dimensional stretching |
| `bulk_*` / `manifest_*` | derived | Physics | Electroweak quantities |
| `*_alpha_inverse` | derived | Physics | Fine structure |

---

## Validation Log

```
2026-01-25 - FormulasRegistry updated - COMPLETE
2026-01-25 - Simulations renamed - 76 changes in 59 files
2026-01-25 - Core files renamed - 9 changes in 2 files
2026-01-25 - Scripts renamed - 10 changes in 3 files
2026-01-25 - Tests renamed - 4 changes in 1 file
2026-01-25 - Documentation regenerated - COMPLETE
2026-01-25 - Dodecad_Anchor → Dodecad_Anchors - COMPLETE
2026-01-25 - reid_euclidean → reid_merkabah - COMPLETE
2026-01-25 - watts_weight → watts_echud - COMPLETE
2026-01-25 - Polished metadata (elder_kads, reid_merkabah, watts_echud) - COMPLETE
2026-01-25 - sync_docs.py Hebrew names - COMPLETE
2026-01-25 - appendix_f_72gates Hebrew names - COMPLETE
2026-01-25 - watts_echud gematria 261 → 467+89 - COMPLETE
2026-01-25 - ALL 19 PARAMETERS: Complete metadata (symbol, scientific_name, gnostic_name, rationale) - COMPLETE
2026-01-25 - FormulasRegistry HEBREW_SYMBOL_REGISTRY fully polished - COMPLETE
2026-01-25 - sync_docs.py updated with Gnostic Names column - COMPLETE
2026-01-25 - Final validation - ALL PASS (chi-squared: 1.265, OMEGA=0 STERILE)
```

---

*Completed by bulk_hebrew_rename.py v23.2*
