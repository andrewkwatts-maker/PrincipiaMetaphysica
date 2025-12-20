# Config.py Consistency Audit - Simulation Files

**Audit Date:** 2025-12-20
**Config Version:** v12.8
**Auditor:** Claude Code Agent
**Status:** CRITICAL ISSUES FOUND

---

## Executive Summary

Audited 4 simulation files to verify they properly import from `config.py` as the single source of truth:

| File | Imports Config? | Uses Config Values? | Status |
|------|----------------|---------------------|--------|
| `torsion_effective_v12_8.py` | ✅ YES | ⚠️ PARTIAL | NEEDS FIX |
| `gw_dispersion_v12_8.py` | ✅ YES | ⚠️ PARTIAL | NEEDS FIX |
| `proton_lifetime_mc_v12_8.py` | ❌ NO | ❌ NO | **CRITICAL** |
| `neutrino_mass_matrix_final_v12_7.py` | ❌ NO | ❌ NO | **CRITICAL** |

**Finding:** 2 files completely bypass config.py, 2 files partially use it. This violates the single source of truth principle.

---

## Detailed Findings

### 1. `simulations/torsion_effective_v12_8.py`

**Import Status:** ✅ Uses config.py (lines 50-59)

**Imports Used:**
```python
from config import FluxQuantization
CHI_EFF = FluxQuantization.CHI_EFF  # 144
B3 = FluxQuantization.B3            # 24
B2 = FluxQuantization.B2            # 4
```

**Issues Found:**

1. **HARDCODED VALUES** (lines 56-59):
   ```python
   # Fallback values if config.py not available
   CHI_EFF = 144
   B3 = 24
   B2 = 4
   ```
   - **Issue:** Duplicates config.py values as hardcoded fallbacks
   - **Risk:** If config.py is updated, fallbacks become stale
   - **Recommendation:** Remove fallbacks or make them clearly throw an error

2. **HARDCODED FORMULA CONSTANTS** (line 110):
   ```python
   FLUX_DIVISOR = 6  # Standard in M-theory G₂ literature
   ```
   - **Issue:** Not imported from config.py
   - **Comment says:** "Standard in M-theory G₂ literature"
   - **Recommendation:** Should be documented in `config.py` if it's a fundamental constant

**Values Properly Used:**
- ✅ `CHI_EFF = 144` (from config)
- ✅ `B3 = 24` (from config)
- ✅ `B2 = 4` (from config)

**Consistency Check:**
- All config values match file comments ✓
- No contradictions found ✓

**Grade:** B+ (Uses config but has fallback risk)

---

### 2. `simulations/gw_dispersion_v12_8.py`

**Import Status:** ✅ Uses config.py (lines 41-51)

**Imports Used:**
```python
from config import FluxQuantization, FundamentalConstants
CHI_EFF = FluxQuantization.CHI_EFF  # 144
B3 = FluxQuantization.B3            # 24
SHADOW_SPATIAL = FundamentalConstants.SIGNATURE_BULK[0]  # 12
```

**Issues Found:**

1. **HARDCODED FALLBACKS** (lines 48-51):
   ```python
   # Fallback values if config.py not available
   CHI_EFF = 144
   B3 = 24
   SHADOW_SPATIAL = 12
   ```
   - **Issue:** Same as torsion file - duplicates config values
   - **Risk:** Stale fallbacks if config updated

2. **HARDCODED CONSTANTS** (lines 56-58):
   ```python
   FLUX_DIVISOR = 6  # Standard in M-theory G2 literature
   N_FLUX = CHI_EFF / FLUX_DIVISOR  # = 24
   T_OMEGA_GEOMETRIC = -B3 / N_FLUX  # = -1.000
   ```
   - **Issue:** `FLUX_DIVISOR` not from config.py
   - **Issue:** `T_OMEGA_GEOMETRIC` computed locally instead of imported
   - **Note:** File comment (line 14) says `T_omega (-1.000)` but config.py has different derivation

**Inconsistency with config.py:**

File (line 14):
```python
# T_omega (-1.000): Effective torsion from flux quantization
#                   T_omega = -b3 / N_flux
```

Config.py (`TorsionClass.T_OMEGA` = `-0.884`):
```python
# From TCS G₂ construction #187 (CHNP database)
T_OMEGA = -0.884             # Torsion class (exact from geometry)
```

**🚨 CRITICAL INCONSISTENCY:** The file derives `T_omega = -1.000` but `config.py` has `T_OMEGA = -0.884`. The file comment (line 15) acknowledges "13% agreement with phenomenological -0.884" but this suggests the file is using a different derivation than config.py!

**Values Properly Used:**
- ✅ `CHI_EFF = 144` (from config)
- ✅ `B3 = 24` (from config)
- ✅ `SHADOW_SPATIAL = 12` (from config)
- ❌ `T_OMEGA` NOT from config (locally derived as -1.000 vs config's -0.884)

**Grade:** C+ (Uses config but has T_omega inconsistency)

---

### 3. `simulations/proton_lifetime_mc_v12_8.py`

**Import Status:** ❌ **DOES NOT IMPORT CONFIG.PY**

**Hardcoded Values Found:**

Line 19:
```python
def proton_lifetime_mc(n_mc=10000, M_GUT_mean=2.118e16, M_GUT_std=1e14):
```

Line 44:
```python
tau_p_baseline = 3.91e34  # years (from simulations)
```

Line 61:
```python
tau_p_superK = 2.4e34  # years (90% CL lower limit)
```

**Values in config.py:**

```python
# GaugeUnificationParameters
M_GUT = 2.118e16            # [GeV] Geometric derivation (was 1.8e16)
M_GUT_ERROR = 0.09e16       # [GeV] From b3 flux variations (5%)

# PhenomenologyParameters
TAU_PROTON = 3.70e34        # Proton lifetime [years] (geometric + RG hybrid)
TAU_PROTON_LOWER_68 = 2.35e34   # 68% CI lower bound [years]
TAU_PROTON_UPPER_68 = 5.39e34   # 68% CI upper bound [years]
TAU_PROTON_SUPER_K_BOUND = 1.67e34  # Super-Kamiokande lower bound [years]
```

**🚨 CRITICAL ISSUES:**

1. **M_GUT**: Uses `2.118e16` ✓ (matches config) but NOT imported
2. **M_GUT_std**: Uses `1e14` but config has `M_GUT_ERROR = 0.09e16` (different!)
3. **tau_p_baseline**: Uses `3.91e34` but config has `TAU_PROTON = 3.70e34` (**5.7% discrepancy!**)
4. **tau_p_superK**: Uses `2.4e34` but config has `TAU_PROTON_SUPER_K_BOUND = 1.67e34` (**43.7% discrepancy!**)

**Grade:** F (Completely bypasses config.py with inconsistent values)

---

### 4. `simulations/neutrino_mass_matrix_final_v12_7.py`

**Import Status:** ❌ **DOES NOT IMPORT CONFIG.PY**

**Hardcoded Values Found:**

Lines 23-27:
```python
Omega = np.array([
    [  0,   8,   3],
    [  8,   0,  12],
    [  3,  12,   0]
])
```

Lines 30-34:
```python
phi = np.array([
    [0.000, 2.813, 1.107],
    [2.813, 0.000, 0.911],
    [1.107, 0.911, 0.000]
])
```

Line 37:
```python
M_R_diag = np.array([5.1e13, 2.3e13, 5.7e12])  # GeV
```

Lines 44-45:
```python
b3 = 24
chi_eff = 144
```

Line 57:
```python
v_EW = 246  # GeV
```

Lines 70-71:
```python
nufit_delta21 = 7.42e-5  # eV^2
nufit_delta3l = 2.515e-3  # eV^2
```

**Values in config.py:**

```python
# FluxQuantization
B3 = 24
CHI_EFF = 144

# NeutrinoMassMatrix
OMEGA_INTERSECTIONS = np.array([
    [  0,  11,   4],
    [ 11,   0,  16],
    [  4,  16,   0]
])

WILSON_PHASES = np.array([
    [0.000, 2.827, 1.109],
    [2.827, 0.000, 0.903],
    [1.109, 0.903, 0.000]
])

# RightHandedNeutrinoMasses
M_R_1 = M_R_BASE * N_FLUX_1**2  # 1.89e15 GeV
M_R_2 = M_R_BASE * N_FLUX_2**2  # 8.4e14 GeV
M_R_3 = M_R_BASE * N_FLUX_3**2  # 2.1e14 GeV

# HiggsVEVs
V_EW = 246.0  # [GeV] Electroweak VEV
```

**🚨 CRITICAL ISSUES:**

1. **Omega matrix:** File uses different values than `NeutrinoMassMatrix.OMEGA_INTERSECTIONS`!
   - File: `[[0,8,3], [8,0,12], [3,12,0]]`
   - Config: `[[0,11,4], [11,0,16], [4,16,0]]`
   - **Complete mismatch!**

2. **Wilson phases:** File uses slightly different values
   - File: `[2.813, 1.107, 0.911]` (off-diagonal)
   - Config: `[2.827, 1.109, 0.903]`
   - Small differences but inconsistent

3. **Right-handed neutrino masses:** File uses different scale
   - File: `[5.1e13, 2.3e13, 5.7e12]`
   - Config: `[1.89e15, 8.4e14, 2.1e14]`
   - **Order of magnitude difference!**

4. **chi_eff, b3:** Uses `144, 24` ✓ (matches) but NOT imported

**Note:** File is v12.7, might be using different physics than v12.8 config

**Grade:** F (Completely bypasses config.py with major inconsistencies)

---

## Summary of Violations

### Single Source of Truth Violations

| Parameter | config.py Value | File(s) with Different Value |
|-----------|----------------|------------------------------|
| `T_OMEGA` | `-0.884` | `gw_dispersion_v12_8.py` (-1.000) |
| `TAU_PROTON` | `3.70e34` | `proton_lifetime_mc_v12_8.py` (3.91e34) |
| `TAU_PROTON_SUPER_K_BOUND` | `1.67e34` | `proton_lifetime_mc_v12_8.py` (2.4e34) |
| `M_GUT_ERROR` | `0.09e16` | `proton_lifetime_mc_v12_8.py` (1e14) |
| `OMEGA_INTERSECTIONS` | `[[0,11,4],...]` | `neutrino_mass_matrix_final_v12_7.py` ([[0,8,3],...]) |
| `WILSON_PHASES` | `[2.827,1.109,0.903]` | `neutrino_mass_matrix_final_v12_7.py` ([2.813,1.107,0.911]) |
| `M_R` masses | `[1.89e15, 8.4e14, 2.1e14]` | `neutrino_mass_matrix_final_v12_7.py` ([5.1e13, 2.3e13, 5.7e12]) |

### Missing Imports

| File | Missing Import |
|------|----------------|
| `proton_lifetime_mc_v12_8.py` | `GaugeUnificationParameters.M_GUT` |
| `proton_lifetime_mc_v12_8.py` | `GaugeUnificationParameters.M_GUT_ERROR` |
| `proton_lifetime_mc_v12_8.py` | `PhenomenologyParameters.TAU_PROTON` |
| `proton_lifetime_mc_v12_8.py` | `PhenomenologyParameters.TAU_PROTON_SUPER_K_BOUND` |
| `neutrino_mass_matrix_final_v12_7.py` | `FluxQuantization.CHI_EFF` |
| `neutrino_mass_matrix_final_v12_7.py` | `FluxQuantization.B3` |
| `neutrino_mass_matrix_final_v12_7.py` | `NeutrinoMassMatrix.OMEGA_INTERSECTIONS` |
| `neutrino_mass_matrix_final_v12_7.py` | `NeutrinoMassMatrix.WILSON_PHASES` |
| `neutrino_mass_matrix_final_v12_7.py` | `RightHandedNeutrinoMasses.M_R_1/2/3` |
| `neutrino_mass_matrix_final_v12_7.py` | `HiggsVEVs.V_EW` |
| `torsion_effective_v12_8.py` | `FluxQuantization.FLUX_DIVISOR` (if it should exist) |
| `gw_dispersion_v12_8.py` | `TorsionClass.T_OMEGA` |

### Hardcoded Fallbacks (Risk Factor)

Both `torsion_effective_v12_8.py` and `gw_dispersion_v12_8.py` have:
```python
except ImportError:
    # Fallback values if config.py not available
    CHI_EFF = 144
    B3 = 24
    ...
```

**Risk:** These fallbacks silently mask import failures and can become stale.

---

## Recommendations

### High Priority (Fix Immediately)

1. **`proton_lifetime_mc_v12_8.py`:**
   ```python
   # ADD THIS:
   from config import GaugeUnificationParameters, PhenomenologyParameters

   # CHANGE THIS:
   def proton_lifetime_mc(
       n_mc=10000,
       M_GUT_mean=GaugeUnificationParameters.M_GUT,
       M_GUT_std=GaugeUnificationParameters.M_GUT_ERROR
   ):
       tau_p_baseline = PhenomenologyParameters.TAU_PROTON
       tau_p_superK = PhenomenologyParameters.TAU_PROTON_SUPER_K_BOUND
   ```

2. **`neutrino_mass_matrix_final_v12_7.py` or create v12_8:**
   ```python
   # ADD THIS:
   from config import (
       FluxQuantization,
       NeutrinoMassMatrix,
       RightHandedNeutrinoMasses,
       HiggsVEVs
   )

   # REPLACE HARDCODED VALUES:
   Omega = NeutrinoMassMatrix.OMEGA_INTERSECTIONS
   phi = NeutrinoMassMatrix.WILSON_PHASES
   M_R = RightHandedNeutrinoMasses.mass_matrix()
   v_EW = HiggsVEVs.V_EW
   chi_eff = FluxQuantization.CHI_EFF
   b3 = FluxQuantization.B3
   ```

3. **`gw_dispersion_v12_8.py`:**
   ```python
   # ADD THIS:
   from config import TorsionClass

   # CHANGE THIS:
   T_OMEGA_GEOMETRIC = TorsionClass.T_OMEGA  # Use config value
   # OR document why -1.000 differs from config's -0.884
   ```

### Medium Priority

4. **Remove fallback values** in `torsion_effective_v12_8.py` and `gw_dispersion_v12_8.py`:
   ```python
   # CHANGE THIS:
   except ImportError:
       raise ImportError("config.py is required - no fallback values provided")
   ```

5. **Add FLUX_DIVISOR to config.py** if it's a fundamental constant:
   ```python
   # In FluxQuantization class:
   FLUX_DIVISOR = 6  # Standard in M-theory G₂ literature (Acharya et al. 2001)
   ```

### Low Priority (Code Quality)

6. Add validation function in config.py:
   ```python
   def validate_simulation_consistency():
       """Check all simulation files use config values"""
       # Could use AST parsing to verify imports
   ```

7. Add unit tests to catch hardcoded values:
   ```python
   def test_no_hardcoded_values():
       """Ensure simulations import from config.py"""
       # Parse simulation files and check for hardcoded constants
   ```

---

## Impact Assessment

### Current State Impact

| Issue | Impact | Severity |
|-------|--------|----------|
| Proton lifetime discrepancy (3.91 vs 3.70) | Published results may differ from config | HIGH |
| Super-K bound discrepancy (2.4 vs 1.67) | Wrong experimental comparison | HIGH |
| Neutrino Omega matrix mismatch | Completely different physics calculation | **CRITICAL** |
| T_omega inconsistency (-1.000 vs -0.884) | 13% error in GW predictions | MEDIUM |
| Fallback values | Silent failures, stale data | MEDIUM |
| Missing imports | Violates single source of truth | HIGH |

### Version Control Impact

- **`neutrino_mass_matrix_final_v12_7.py`** may be using older physics (v12.7 vs v12.8 config)
- If config.py updated to v12.8 but this file not updated, causes version drift
- Suggests need for v12_8 version of neutrino file

---

## Files That Need Updates

1. ✅ `config.py` - Already correct (single source of truth)
2. ❌ `simulations/proton_lifetime_mc_v12_8.py` - **NEEDS MAJOR FIXES**
3. ❌ `simulations/neutrino_mass_matrix_final_v12_7.py` - **NEEDS MAJOR FIXES OR v12_8 VERSION**
4. ⚠️ `simulations/gw_dispersion_v12_8.py` - **NEEDS T_OMEGA CLARIFICATION**
5. ⚠️ `simulations/torsion_effective_v12_8.py` - **NEEDS FALLBACK REMOVAL**

---

## Conclusion

**Overall Grade: D+ (Passing but needs significant work)**

The project has a well-structured `config.py` as a single source of truth, but **only 2 out of 4 simulation files actually use it**, and those 2 only use it partially. The worst violations are:

1. **Neutrino file** uses completely different Omega matrix values
2. **Proton file** uses wrong Super-K bound (43% error)
3. **Both missing config files** don't import anything from config.py

This creates a **high risk of inconsistency** where simulation results differ from the documented theory in config.py.

**Action Required:** Update all simulation files to import from config.py before publication or further analysis.

---

**Generated by:** Claude Code Consistency Audit
**Report Version:** 1.0
**Config Version Audited:** v12.8
