# Hebrew Name Rename Tracking v23.2

**Date:** 2026-01-25
**Status:** COMPLETE

---

## Rename Operations

| Old Name | New Name | Value | Symbol | Status |
|----------|----------|-------|--------|--------|
| `elder_vessels` | `elders` | 24 | E_b3 | [x] COMPLETE |
| `demiurgic_gates` | `demiurgic_Yetts` | 135 | Yd | [x] COMPLETE |
| `ennoia_chi` | `qedem_chi_sum` | 144 | chi_Q | [x] COMPLETE |
| `chi_eff_total` | `qedem_chi_sum` | 144 | chi_Q | [x] COMPLETE |
| `bridge_effective` | `Echad_Prime` | 13 | Yud-Gimel | [x] COMPLETE |
| `bridge_local` | `Dodecad_Anchor` | 12 | Bet-Yod | [x] COMPLETE |

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
| **Total** | **64** | **95** |

---

## Validation Log

```
2026-01-25 - FormulasRegistry updated - COMPLETE
2026-01-25 - Simulations renamed - 76 changes in 59 files
2026-01-25 - Core files renamed - 9 changes in 2 files
2026-01-25 - Scripts renamed - 10 changes in 3 files
2026-01-25 - Documentation regenerated - COMPLETE
2026-01-25 - Final validation - ALL PASS (chi-squared: 1.265)
```

---

*Completed by bulk_hebrew_rename.py v23.2*
