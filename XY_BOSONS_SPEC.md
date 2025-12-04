# X,Y Gauge Bosons Specification

## Parameters to Add to Config/Simulation System

### Geometrically Constrained (from G₂ + SO(10)):
1. **M_X, M_Y** - Mass scale (from M_GUT)
   - Source: PM.proton_decay.M_GUT (already exists)
   - Value: 2.118×10¹⁶ GeV
   - Uncertainty: From TCS torsion log variations

2. **alpha_GUT** - Coupling strength at M_GUT
   - Source: PM.proton_decay.alpha_GUT (already exists)
   - Value: 1/23.54
   - From: 3-loop RG running + gauge unification

3. **Charge_X** - Electric charge of X boson
   - Value: ±4/3 e
   - Source: SO(10) representation theory (fixed)

4. **Charge_Y** - Electric charge of Y boson
   - Value: ±1/3 e
   - Source: SO(10) representation theory (fixed)

5. **Spin** - Vector boson spin
   - Value: 1
   - Source: Gauge symmetry (fixed)

6. **B_violation, L_violation** - Baryon/Lepton number
   - Value: Both violated
   - Source: SO(10) group structure (fixed)

### Theoretical Estimates (calculable but not constrained by geometry):
7. **tau_X, tau_Y** - Lifetime
   - Formula: τ ~ 1/M_GUT ~ 10⁻⁴¹ s
   - Uncertainty: Order of magnitude estimate
   - Should calculate from: τ = ℏ/(Γ_total) where Γ from Wilson coefficients

8. **BR_X_uu** - X → u + ū branching ratio
   - Needs: Yukawa matrix from wavefunction overlaps
   - Current: Unknown (marked as such)

9. **BR_X_ue** - X → u + e⁺ branching ratio
   - Needs: Yukawa matrix + lepton sector
   - Related to: proton_decay_channels BR(e⁺π⁰)

10. **BR_Y_dd** - Y → d + d̄ branching ratio
    - Needs: Yukawa matrix
    - Current: Unknown

11. **BR_Y_Knu** - Y → K + ν̄ effective branching
    - Related to: proton_decay_channels BR(K⁺ν̄)

### SO(10) Gauge Structure (Fixed by Group Theory):
12. **N_gauge_bosons** - Total SO(10) bosons
    - Value: 45 total
    - Breakdown: 12 SM + 12 X + 12 Y + 9 Z',W' neutral

13. **N_X_bosons** - Number of X-type bosons
    - Value: 12 (from SO(10) adjoint representation)

14. **N_Y_bosons** - Number of Y-type bosons
    - Value: 12 (from SO(10) adjoint representation)

## Implementation Strategy

### Phase 1: Add to config.py
```python
class XYGaugeBosons:
    """SO(10) X and Y heavy gauge bosons"""

    # Geometrically derived
    M_X = proton_decay.M_GUT  # 2.118e16 GeV
    M_Y = proton_decay.M_GUT  # Same (assume degeneracy)
    alpha_GUT = proton_decay.alpha_GUT  # 1/23.54

    # SO(10) group theory (fixed)
    CHARGE_X = 4/3  # e
    CHARGE_Y = 1/3  # e
    SPIN = 1
    B_VIOLATING = True
    L_VIOLATING = True

    # SO(10) counting
    N_TOTAL = 45
    N_SM = 12  # 8 gluons + 3 W + 1 γ
    N_X = 12
    N_Y = 12
    N_NEUTRAL_HEAVY = 9  # Z', W'' cousins

    # Theoretical estimates
    @staticmethod
    def lifetime():
        """τ ~ ℏ/M_GUT"""
        import scipy.constants as const
        return const.hbar / (XYGaugeBosons.M_X * const.e * 1e9)  # Convert GeV to J

    # Branching ratios - TO BE CALCULATED
    # Would require full Yukawa matrix diagonalization
    BR_UNKNOWN = True
```

### Phase 2: Create simulation module (if needed)
- simulations/xy_bosons_properties.py
- Calculate lifetimes from Wilson coefficients
- Estimate branching ratios from Yukawa overlaps
- Add to run_all_simulations.py

### Phase 3: Add to theory-constants-enhanced.js
```javascript
xy_bosons: {
  M_X: { value: 2.118e16, units: "GeV", derived: true },
  M_Y: { value: 2.118e16, units: "GeV", derived: true },
  charge_X: { value: 4/3, units: "e", fixed: true },
  charge_Y: { value: 1/3, units: "e", fixed: true },
  alpha_GUT: { value: 0.0425, units: "", derived: true },
  tau_estimate: { value: 1e-41, units: "s", estimate: true },
  N_total: { value: 45, units: "", fixed: true },
  N_X: { value: 12, units: "", fixed: true },
  N_Y: { value: 12, units: "", fixed: true }
}
```

### Phase 4: Create dedicated page
- Create: sections/xy-gauge-bosons.html
- Use PM.xy_bosons.* for dynamic population
- Link from predictions.html header
- Style similar to other section pages

## Current Status
- X,Y section exists in predictions.html (line 855)
- M_GUT hardcoded (should use PM reference)
- All other parameters hardcoded or marked "unknown"
- No simulation module yet
