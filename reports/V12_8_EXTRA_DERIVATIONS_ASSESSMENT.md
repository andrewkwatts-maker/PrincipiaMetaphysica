# V12.8 Extra Derivations Assessment

## Date: 2025-12-13
## Status: REJECTED - None of the proposed derivations work numerically

---

## Executive Summary

The user proposed 8 additional derivations to push the prediction count from 45/48 to 58/58.
After rigorous numerical testing, **NONE of these derivations work as claimed**.

**Recommendation**: Do NOT add these to the framework. The existing 45/48 = 93.8% success rate
is already exceptional. Adding fake derivations would undermine the framework's credibility.

---

## Detailed Assessment

### 1. CKM |V_ub| from Cycle Volumes

**Proposed Formula**: `|V_ub| = Vol(cycle_u) / Vol(cycle_b) = exp(3/4pi) / exp(18/4pi)`

**Numerical Test**:
```
Calculated |V_ub| = 0.303
Experimental |V_ub| = 0.00361 (PDG 2024)
Ratio: 84x OFF (2 orders of magnitude)
```

**Status**: INVALID - Does not match experiment

---

### 2. CKM |V_td| from Cycle Volumes

**Proposed Formula**: Same as |V_ub|

**Status**: INVALID - Same issue as above

---

### 3. Proton Decay Branching Ratio

**Proposed Formula**: `BR(p->e+pi0) = (12/24)^2 = 0.25`

**Issues**:
- Why 12? No derivation provided
- Proton decay not observed - cannot validate
- Completely ad-hoc number choice

**Status**: UNFALSIFIABLE SPECULATION

---

### 4. GW Dispersion eta

**Proposed Formula**: `eta = exp(|T_omega|) / b3`

**Issues**:
- No experimental data exists for GW dispersion
- Formula derivation unclear
- Cannot be validated

**Status**: UNFALSIFIABLE SPECULATION

---

### 5. Neutrino theta_13 from Triple Intersection

**Proposed Formula**: `sin^2(theta_13) = (I_123 / Vol)^2` where I_123 = 3

**Numerical Test**:
```
Calculated theta_13 = 26.4 degrees
Experimental theta_13 = 8.57 degrees (NuFIT 6.0)
Discrepancy: 17.8 degrees
```

**Status**: INVALID - Does not match experiment

---

### 6. Neutrino Sum from Atmospheric Splitting

**Proposed Formula**: `Sum(m_nu) = 3 * sqrt(delta_m31_sq)`

**Numerical Test**:
```
Calculated Sum(m_nu) = 0.150 eV
Planck upper limit: < 0.120 eV
```

**Issues**:
- Uses experimental delta_m31 as INPUT (circular)
- Result EXCEEDS Planck upper limit

**Status**: CIRCULAR AND WRONG

---

### 7. Spectral Index n_s from d_eff

**Proposed Formula**: `n_s = 1 - 2/(d_eff - 1)`

**Numerical Test**:
```
Calculated n_s = 0.827
Experimental n_s = 0.9649 +/- 0.0042 (Planck 2018)
Sigma deviation: 32 sigma
```

**Issues**:
- This is just the standard slow-roll inflation formula disguised
- Requires N_e ~ 57 e-folds, not d_eff = 12.576
- Formula does not connect to PM geometry

**Status**: INVALID - Wrong by 32 sigma

---

## Conclusion

**DO NOT ADD THESE DERIVATIONS**

The Principia Metaphysica framework already achieves:
- 56/58 SM parameters derived from geometry
- 45/48 predictions within 1 sigma (93.8%)
- 12 exact matches (0.0 sigma)
- 2 honest calibrations (theta_13, delta_CP)

This is **already exceptional** for any theoretical physics framework. Adding fake
derivations that don't actually work would:
1. Undermine the framework's credibility
2. Create embarrassing errors when peer-reviewed
3. Violate the principle of honest transparency established in v12.8

**Keep the honest assessment. The math speaks for itself.**

---

## Python Verification Code

```python
import numpy as np

# 1. CKM |V_ub|
Vol_u = np.exp(3 / (4 * np.pi))
Vol_b = np.exp(18 / (4 * np.pi))
V_ub_calc = Vol_u / Vol_b  # 0.303, not 0.00361

# 5. theta_13
I123 = 3
Vol = np.exp(24 / (4 * np.pi))
sin2 = (I123 / Vol)**2
theta13 = np.degrees(np.arcsin(np.sqrt(sin2)))  # 26.4, not 8.57

# 6. Neutrino sum
sum_m_nu = 3 * np.sqrt(2.515e-3)  # 0.150 eV, exceeds 0.120 limit

# 7. Spectral index
n_s = 1 - 2/(12.576 - 1)  # 0.827, not 0.9649
```

---

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
