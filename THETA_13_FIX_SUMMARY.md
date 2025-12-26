# Theta_13 Fix Summary

## Issue Identified

The theta_13 (θ₁₃) neutrino mixing angle has **inconsistent values** across HTML files:
- Some show **8.57°** (old calibrated value)
- Some show **8.65°** (new v14.1 geometric derivation)

## Root Cause

Two different simulation approaches exist:

1. **OLD (pmns_full_matrix.py)**: θ₁₃ = 8.57° - **CALIBRATED** to NuFIT experimental value
2. **NEW (pmns_theta13_delta_geometric_v14_1.py)**: θ₁₃ = 8.65° - **DERIVED** from pure G₂ topology

The v14.1 approach is the theoretical goal: deriving values from geometry without calibration.

## Correct Values

- **Theoretical Prediction**: θ₁₃ = **8.65°** (precisely 8.647°)
- **Experimental Value** (NuFIT 6.0): θ₁₃ = **8.57° ± 0.12°**
- **Agreement**: 0.64σ (excellent!)

## Files Requiring Updates

### 1. principia-metaphysica-paper.html
- Line ~3822: Change `8.57°` → `8.65°`
- Line ~3824: Change `CALIBRATED` → `DERIVED`

### 2. beginners-guide.html
- Line ~1750: Change `θ<sub>13</sub> = 8.57°` → `θ<sub>13</sub> = 8.65°`

### 3. principia-metaphysica-paper-old.html (optional - legacy file)
- Update for consistency if desired

## How to Fix

### Option 1: Automated Script (Recommended)
```bash
python fix_theta13_atomic.py
```

This script:
- Uses atomic file operations (safe for file watchers)
- Updates all 3 files automatically
- Shows what changed

### Option 2: Manual Edits
See `THETA_13_FIX_INSTRUCTIONS.md` for detailed line-by-line instructions.

## Verification After Fix

```bash
# Should show 8.65° as predicted value
grep -n "8\.65" *.html | grep -i theta

# Should show DERIVED (not CALIBRATED)
grep -n "DERIVED" *.html | grep theta_13

# Should still show 8.57° as experimental value
grep -n "8\.57.*0\.12" *.html
```

## Important: Do NOT Change

These instances of 8.57° should **remain unchanged** (they're experimental values):
- `principia-metaphysica-paper.html` line ~2007: NuFIT experimental value in table
- `principia-metaphysica-paper.html` line ~2044: NuFIT reference note

## What This Demonstrates

Changing from 8.57° (calibrated) to 8.65° (derived) shows that:

1. **The theory makes genuine predictions** (not just fitting data)
2. **Pure geometry works**: No phenomenological parameters needed
3. **Agreement is excellent**: 0.64σ deviation from experiment
4. **v14.1 is a major advancement**: True geometric derivation achieved

This is the difference between a **fitted theory** and a **predictive theory**.
