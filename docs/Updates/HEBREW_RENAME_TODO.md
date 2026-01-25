# Hebrew Name Rename Tracking v23.2

**Date:** 2026-01-25
**Status:** COMPLETE

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

## Final Parameter List (v23.2 Hebrew Names)

### Topological Invariants

| Code Name | Hebrew | Gematria | Value | Symbol | Old Name |
|-----------|--------|----------|-------|--------|----------|
| `monad_unity` | Aleph | 1 | 1.0 | - | `watts_constant` |
| `residual_key` | Yod | 10 | 10 | - | `decad` |
| `syzygy_gap` | Chai | 18 | 18 | - | `syzygy_gap` |
| `elder_kads` | Kad (כד) | 24 | 24 | E_כד | `b3`, `elders`, `elder_vessels` |
| `horos_limit` | Kaz | 27 | 27 | - | `horos` |
| `mephorash_chi` | Av | 72 | 72 | - | `chi_eff` |
| `sophian_registry` | Lamed | 74 | 125 | V_l | `visible_sector` |
| `demiurgic_Yetts` | Kalah | 135 | 135 | Yd | `shadow_sector`, `demiurgic_gates` |
| `qedem_chi_sum` | Qedem | 144 | 144 | chi_Q | `chi_eff_total`, `ennoia_chi` |
| `nitzotzin_sector` | Mem | 144 | 144 | R_m | `roots_per_sector` |
| `logos_joint` | 153 | 153 | 153 | - | `christ_constant` |
| `sophian_pressure` | 163 | 163 | 163 | P_S | `odowd_bulk_pressure` |
| `nitzotzin_roots` | 288 | 288 | 288 | R_Xi | `roots_total` |

### Central Sampler (Reid Architecture)

| Code Name | Hebrew | Gematria | Value | Symbol | Old Name |
|-----------|--------|----------|-------|--------|----------|
| `gnosis_threshold` | Tet | 9 | 9 | G_Tet | `central_activation_threshold` |
| `Dodecad_Anchors` | Bet-Yod | 12 | 12 | n_12 | `total_local_pairs`, `bridge_local` |
| `Echad_Prime` | Yud-Gimel | 13 | 13 | n_13 | `total_effective_pairs`, `bridge_effective` |
| `nitsot_par` | Nun-Qoph | 150 | 1/144 | N_p | `reid_invariant` |
| `reid_pair` | Resh | 200 | 1 | R_Resh | `central_pair` |
| `watts_weight` | Resh-Phi | 261 | phi/sqrt(12) | W_phi | `central_pair_weight` |

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
| `visible_sector` | `sophian_registry` | 125 |
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
| `central_pair` | `reid_pair` | 1 |
| `central_pair_weight` | `watts_weight` | phi/sqrt(12) |

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
2026-01-25 - Final validation - ALL PASS (chi-squared: 1.265)
```

---

*Completed by bulk_hebrew_rename.py v23.2*
