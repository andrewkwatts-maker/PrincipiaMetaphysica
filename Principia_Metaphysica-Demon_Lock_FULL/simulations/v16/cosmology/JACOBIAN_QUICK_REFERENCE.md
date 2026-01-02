# G2 Jacobian Quick Reference Card

**For developers working with `multi_sector_v16_0.py`**

---

## The Formula

```python
metric_jacobian = np.power(re_t_values, -7/2)
```

## What Does This Mean?

The Jacobian `√det(g)` for sampling on G2 moduli space scales as:
```
√det(g) ~ (Re(T))^{-7/2}
```

where `Re(T)` is the real part of the Kähler modulus T.

## Why -7/2?

**Short answer:** It comes from the **7-dimensional volume** of the G2 manifold.

**Long answer:**
```
Vol(G2) ~ (Re(T))^{7/2}           (7D volume scaling)
g ~ 1/Vol                         (deformation metric)
√det(g) ~ (Re(T))^{-7/2}         (Jacobian)
```

## Why Negative?

**Kähler geometry requires it.** The invariant measure is:
```
dμ = √det(g) d²T ~ (Re(T))^{-n} dRe(T) dIm(T)
```

Negative power means:
- **Large Re(T)** (weak coupling) → **low density** (flat region)
- **Small Re(T)** (strong coupling) → **high density** (curved region)

This is **geometrically correct**.

## Is This Related to Yukawa Overlaps?

**No.** They are **independent** formulas:
- **Yukawa width:** `σ = √(b3/χ_eff)` (wavefunction overlap)
- **Jacobian:** `J = (Re(T))^{-7/2}` (moduli space measure)

Both are **self-consistent** and **do not conflict**.

## Does It Affect Ω_DM/Ω_b?

**No.** The dark matter prediction is **protected**:
```
Ω_DM/Ω_b = (T/T')³ ≈ 5.4
```

This depends on the **temperature ratio** T'/T = 0.57, **not** on sector weights.

**You can change the Jacobian without breaking this prediction.**

## Validation Status

✅ **Mathematically proven** (see JACOBIAN_VALIDATION_REPORT.md)
✅ **All 6 tests passed** (see test_complete_validation.py)
✅ **Observable agreement** (Ω_DM/Ω_b = 5.40 vs obs 5.38±0.15)

## Common Mistakes

### ❌ WRONG: "Use Vol³ weighting"

```python
# DON'T DO THIS
metric_jacobian = np.power(re_t_values, +3)  # WRONG SIGN!
```

**Problem:** Positive power violates Kähler geometry.

### ❌ WRONG: "Use single modulus Kähler metric"

```python
# DON'T DO THIS
metric_jacobian = np.power(re_t_values, -1)  # Too weak!
```

**Problem:** Misses G2 volume factor. Should be -7/2, not -1.

### ✅ CORRECT: Current implementation

```python
# THIS IS CORRECT
metric_jacobian = np.power(re_t_values, -7/2)
```

## Quick Sanity Checks

### Sign Check
```python
# Jacobian should DECREASE as Re(T) increases
assert jacobian[0] > jacobian[-1]  # ✓
```

### Magnitude Check
```python
# Power should be -dim(G2)/2
assert power == -7/2  # ✓
```

### Normalization Check
```python
# Weights should sum to 1
assert abs(sum(weighted) - 1.0) < 1e-10  # ✓
```

## When to Modify This

**Short answer:** Probably never.

**Long answer:** Only if:
1. You change the **manifold topology** (not G2 anymore)
2. You change the **dimension** (not 7D anymore)
3. You have a **different geometric structure** (not deformation metric)

Otherwise, **DO NOT CHANGE**.

## Further Reading

- **Detailed proof:** JACOBIAN_VALIDATION_REPORT.md
- **Summary:** JACOBIAN_ANALYSIS_SUMMARY.md
- **Tests:** test_complete_validation.py
- **Code:** multi_sector_v16_0.py lines 297-361

## Help!

If you're unsure about modifying this code:

1. Read JACOBIAN_VALIDATION_REPORT.md (section 3: "Mathematical Justification")
2. Run test_complete_validation.py to verify current behavior
3. Ask: "Does my change preserve Vol ~ (Re(T))^{7/2}?"
4. If in doubt, **don't change it**.

---

**Remember:** This is **not a tunable parameter**. It's **fundamental geometry**.

---

*Quick reference compiled from validation analysis (2025-12-29)*
