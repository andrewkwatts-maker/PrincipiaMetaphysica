# Theta_13 Neutrino Mixing Angle Correction Instructions

## Executive Summary

The theta_13 (θ₁₃) neutrino mixing angle needs to be corrected from **8.57°** to **8.65°** in several HTML files to match the pure geometric derivation from v14.1.

## Background

### Authoritative Sources

1. **Simulation: pmns_theta13_delta_geometric_v14_1.py**
   - Pure geometric derivation (NO calibration)
   - Result: θ₁₃ = 8.65° (precisely 8.647°)
   - Formula: sin(θ₁₃) = √(b₂ × n_gen)/b₃ × (1 + S/(2×χ_eff))
   - Deviation from NuFIT: 0.64σ

2. **theory_output.json**
   - `pmns_geometric_v14_1.theta_13_deg: 8.647304725338865`
   - This is the v14.1 pure geometric value

3. **Legacy: pmns_full_matrix.py**
   - Old calibrated value: θ₁₃ = 8.57° (CALIBRATED to NuFIT)
   - This was used before the v14.1 geometric derivation

### Experimental Reference
- **NuFIT 6.0**: θ₁₃ = 8.57° ± 0.12° (experimental measurement)
- This value should remain unchanged where it appears as the experimental comparison

## Required Changes

### 1. principia-metaphysica-paper.html

**Line ~3820-3825** (may vary slightly):
```html
<!-- BEFORE -->
<tr>
    <td>$\theta_{13}$</td>
    <td>8.57&deg;</td>
    <td>$8.57 \pm 0.12$&deg;</td>
    <td>CALIBRATED</td>
</tr>

<!-- AFTER -->
<tr>
    <td>$\theta_{13}$</td>
    <td>8.65&deg;</td>
    <td>$8.57 \pm 0.12$&deg;</td>
    <td>DERIVED</td>
</tr>
```

**DO NOT CHANGE** these lines (they correctly show experimental NuFIT value):
- Line ~2007: `<td>$8.57° \pm 0.12°$</td>` (experimental value in comparison table)
- Line ~2044: `NuFIT 6.0: $8.57° \pm 0.12°$` (experimental reference)

### 2. beginners-guide.html

**Line ~1750**:
```html
<!-- BEFORE -->
<strong>Values:</strong> θ<sub>23</sub> = ... θ<sub>12</sub> = 33.6°, θ<sub>13</sub> = 8.57°

<!-- AFTER -->
<strong>Values:</strong> θ<sub>23</sub> = ... θ<sub>12</sub> = 33.6°, θ<sub>13</sub> = 8.65°
```

### 3. principia-metaphysica-paper-old.html (Optional - Old Version)

This file appears to be a legacy version. You may choose to update it for consistency:

**Line ~845**:
```
<!-- BEFORE -->
Two PMNS parameters ($\theta_{13} = 8.57^\circ$, $\delta_{CP} = 235^\circ$)

<!-- AFTER -->
Two PMNS parameters ($\theta_{13} = 8.65^\circ$, $\delta_{CP} = 235^\circ$)
```

**Line ~41924**:
```
<!-- BEFORE -->
\(\theta_{13} = 8.57°\) calibrated to NuFIT

<!-- AFTER -->
\(\theta_{13} = 8.65°\) derived from G₂ topology
```

## Verification

After making changes, verify:

1. **Predicted value** (what the theory predicts): **8.65°**
2. **Experimental value** (NuFIT measurement): **8.57° ± 0.12°**
3. **Status**: Should be **DERIVED** (not CALIBRATED)
4. **Deviation**: 0.64σ agreement

### Search Commands to Verify

```bash
# Find all instances of 8.57 (review context to ensure experimental values aren't changed)
grep -r "8\.57" *.html sections/*.html

# Find all instances of 8.65 (should see the predicted values)
grep -r "8\.65" *.html sections/*.html

# Verify CALIBRATED vs DERIVED status
grep -i "theta.*13.*CALIBRATED" *.html sections/*.html
```

## Why This Change Matters

The v14.1 simulation represents a major theoretical advancement: it derives θ₁₃ purely from G₂ manifold topology without any phenomenological fitting. The old value (8.57°) was calibrated to match experiments, but the new geometric derivation (8.65°) is a genuine prediction with 0.64σ agreement with experiment.

This demonstrates the theory's predictive power rather than just fitting experimental data.

## Technical Details

### v14.1 Derivation Formula
```
sin(θ₁₃) = √(b₂ × n_gen) / b₃ × (1 + S/(2×χ_eff))
```

Where:
- b₂ = 4 (Kähler moduli from Donaldson-Thomas)
- n_gen = 3 (from |χ_eff|/48)
- b₃ = 24 (associative 3-cycles)
- S = orientation_sum = 12 (from Sp(2,R) gauge fixing)
- χ_eff = 144 (from h¹¹ + h³¹ constraint)

Result:
- sin(θ₁₃) = √(4 × 3) / 24 × (1 + 12/(2×144))
- sin(θ₁₃) = 0.1443 × 1.0417 = 0.1504
- θ₁₃ = arcsin(0.1504) = 8.65° (8.647° precisely)

### Comparison with NuFIT 6.0
- Predicted: 8.65°
- Experimental: 8.57° ± 0.12°
- Deviation: |8.65 - 8.57| / 0.12 = 0.67σ ≈ 0.64σ
- Status: Excellent agreement (< 1σ)

## Files Status

Files with 8.57° that need review:
- ✓ principia-metaphysica-paper.html (1 instance needs change, 2 experimental refs keep)
- ✓ beginners-guide.html (1 instance needs change)
- ○ principia-metaphysica-paper-old.html (optional - old version)

No changes needed in sections/*.html (clean)
