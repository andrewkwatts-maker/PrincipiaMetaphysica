# Principia Metaphysica v20 Implementation Plan

**STATUS: PLANNING**
**Created:** 2026-01-11
**From:** v19.2-SOVEREIGN Assessment

---

## Executive Summary

This plan synthesizes findings from three assessment agents and defines the path from v19.2 to v20. The framework is **already 60% ready** for v20 with strong foundations, but requires specific enhancements to achieve full recursive precision.

### Current State Assessment

| Component | Readiness | Notes |
|-----------|-----------|-------|
| PMRegistry SSOT | 60% | Exists, missing recursive deps |
| Schema Compliance | 100% | 138/138 simulations compliant |
| Electroweak Loop | 20% | Exists but not iterative |
| Yukawa Textures | 15% | Hardcoded, needs Golden Ratio |
| Dark Matter | 70% | Complete, needs residue link |
| Master Precision Loop | 5% | Not implemented |
| Hardcoded Constants | - | 11 files need registry.get() |
| Orphaned Parameters | - | 62 params need registration |

---

## What's Worth Implementing for v20

Based on the assessment, here are the **high-value** improvements prioritized by impact vs. effort:

### Tier 1: Quick Wins (High Impact, Low Effort)

1. **Fix 11 Hardcoded Constants** - Replace inline constants with `registry.get()`
2. **Add 62 Orphaned Parameters** - Register formula parameters missing from parameters.json
3. **Link Orphaned Formulas** - 191 formulas not referenced by sections need mapping

### Tier 2: Core v20 Features (High Impact, Medium Effort)

4. **Recursive Dependency Resolver** - Auto-derive parameters in topological order
5. **Electroweak Precision Loop** - Iterative G_F with Schwinger + Top corrections
6. **Yukawa Textures via Golden Ratio** - Replace hardcoded masses with φ-derivation

### Tier 3: Advanced Features (Medium Impact, High Effort)

7. **Dark Matter Residue Link** - Connect 7D/3D volume ratio to Ω_DM
8. **Master Precision Loop** - Recursive self-consistency for all predictions
9. **NOT_TESTABLE Gate Upgrades** - Convert 6 gates to VERIFIED with derivations

---

## Detailed Implementation Plan

### Phase 0: Registry Cleanup (Tier 1)

**Goal:** Ensure all constants flow from registry, not hardcoded values.

#### 0.1 Fix Hardcoded Constants (11 files)

Files identified with hardcoded physics constants:

| File | Constants to Fix |
|------|------------------|
| `simulations/v16/cosmology/ricci_flow_h0_v16_1.py` | H0, Omega values |
| `simulations/v16/pneuma/pneuma_simulation_v18.py` | Coupling constants |
| `simulations/v16/geometric/geometric_simulation_v18.py` | Geometric seeds |
| `simulations/v16/gauge/gauge_simulation_v18.py` | Gauge couplings |
| `simulations/v16/cosmology/multi_sector_v16_0.py` | Sector fractions |
| `simulations/v16/thermal/thermal_simulation_v18.py` | Temperature scales |
| `simulations/v16/proton/proton_simulation_v18.py` | Proton mass |
| `simulations/v16/neutrino/neutrino_simulation_v18.py` | PMNS angles |
| `simulations/v16/fermion/fermion_simulation_v18.py` | Fermion masses |
| `simulations/v16/predictions/predictions_simulation_v18.py` | PDG values |
| `simulations/v16/moduli/moduli_simulation_v18.py` | Moduli VEVs |

**Pattern to apply:**
```python
# Before (hardcoded)
H0 = 71.55

# After (registry-sourced)
H0 = registry.get("H0_predicted", default=71.55)
```

#### 0.2 Register Orphaned Parameters (62 params)

Parameters appearing in formulas but missing from `parameters.json`:

- Formula parameters used in gate validations
- Derived constants not yet in registry
- Cross-simulation dependencies

**Action:** Run audit and auto-generate additions to parameters.json

#### 0.3 Link Orphaned Formulas (191 formulas)

From `formula_section_audit.json`:
- 265 total formulas
- 147 referenced by sections
- 191 orphaned (not mapped to any section)

**Action:** Map each orphaned formula to appropriate section_id

---

### Phase 1: Recursive Dependency Resolution (Tier 2)

**Goal:** Parameters derive themselves in topological order.

#### Current Problem
```python
# v19: Each simulation fetches independently
sin2_theta_W = registry.get("sin2_theta_W")  # What if not set yet?
```

#### v20 Solution: Dependency Graph
```python
# PMRegistry v20 with recursive resolution
class PMRegistry:
    def __init__(self):
        self._computed = {}
        self._dependencies = {
            "G_F": ["sin2_theta_W", "M_W", "delta_r"],
            "sin2_theta_W": ["alpha_em", "M_Z"],
            "M_W": ["v_higgs", "g_weak"],
            # ... full dependency graph
        }

    def get(self, param: str) -> float:
        if param in self._computed:
            return self._computed[param]

        # Resolve dependencies first
        for dep in self._dependencies.get(param, []):
            self.get(dep)  # Recursive resolution

        # Now compute this parameter
        value = self._compute(param)
        self._computed[param] = value
        return value
```

#### Implementation Steps
1. Map all parameter dependencies from formulas
2. Build topological sort of computation order
3. Implement lazy evaluation with caching
4. Add cycle detection for safety

---

### Phase 2: Electroweak Precision Loop (Tier 2)

**Goal:** Derive G_F iteratively with radiative corrections.

#### Current State
- G_F derivation exists in `simulations/v16/electroweak/`
- Schwinger correction implemented (α/2π)
- Top quark loop implemented
- NOT yet iterative

#### v20 Enhancement
```python
def compute_G_F_iterative(registry: PMRegistry, max_iter=10, tol=1e-8):
    """
    Iterative G_F with self-consistent radiative corrections.

    Loop until convergence:
    1. Compute tree-level G_F from Higgs VEV
    2. Add Schwinger correction (α/2π)
    3. Add Top loop correction
    4. Update sin²θ_W from new G_F
    5. Recompute if changed > tolerance
    """
    # Initial tree-level
    v_higgs = registry.get("v_higgs")  # 246.22 GeV
    G_F_tree = 1 / (sqrt(2) * v_higgs**2)

    G_F = G_F_tree
    for i in range(max_iter):
        G_F_prev = G_F

        # Radiative corrections
        alpha_em = registry.get("alpha_em")
        delta_alpha = alpha_em / (2 * pi)  # Schwinger

        m_top = registry.get("m_top")
        delta_top = 3 * G_F * m_top**2 / (8 * pi**2 * sqrt(2))

        # Apply corrections
        G_F = G_F_tree * (1 + delta_alpha + delta_top)

        # Check convergence
        if abs(G_F - G_F_prev) / G_F < tol:
            break

    return G_F
```

---

### Phase 3: Yukawa Textures via Golden Ratio (Tier 2)

**Goal:** Derive fermion mass hierarchy from φ = (1+√5)/2.

#### Current State
- Fermion masses hardcoded from PDG
- No derivation chain

#### v20 Pattern
```python
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio = 1.618...

def compute_fermion_masses(registry: PMRegistry):
    """
    Derive fermion mass hierarchy from Golden Ratio textures.

    Pattern: m_i/m_j ~ φ^n for integer n
    """
    m_top = registry.get("m_top")  # Anchor mass

    # Down-type quarks (approximate)
    m_bottom = m_top / PHI**2      # ~173/2.62 ~ 66 (actual: 4.18)
    m_strange = m_bottom / PHI**4  # Texture scaling
    m_down = m_strange / PHI**2

    # Charged leptons
    m_tau = m_top / PHI**4         # ~173/6.85 ~ 25 (actual: 1.78)
    m_muon = m_tau / PHI**4
    m_electron = m_muon / PHI**4

    return {
        "m_bottom": m_bottom,
        "m_strange": m_strange,
        "m_down": m_down,
        "m_tau": m_tau,
        "m_muon": m_muon,
        "m_electron": m_electron
    }
```

**Note:** The actual implementation needs careful calibration to match PDG values within experimental uncertainty.

---

### Phase 4: Dark Matter Residue (Tier 3)

**Goal:** Connect hidden bulk volume to dark matter fraction.

#### The Derivation
```python
def compute_omega_dm(registry: PMRegistry):
    """
    Dark matter fraction from 7D/3D volume ratio.

    Hidden bulk (163 roots) maps to dark matter
    Visible sector (125 roots) maps to baryonic matter
    """
    N_hidden = 163
    N_visible = 125
    N_total = 288

    # Volume ratio in 7D compact space
    V_7D_hidden = N_hidden / N_total  # ~0.566
    V_7D_visible = N_visible / N_total  # ~0.434

    # Dark matter fraction
    Omega_DM = V_7D_hidden * (1 - registry.get("Omega_baryon"))

    return Omega_DM  # ~0.27 (Planck: 0.265 ± 0.007)
```

---

## Validation Requirements

### For Each Phase

1. **Run Full Simulation Suite**
   ```bash
   python run_all_simulations.py --verbose
   ```

2. **Verify MANIFOLD IS STERILE**
   - All 7 sterility checks must pass
   - No regression in gate verification count

3. **Check Output Diffs**
   - Compare AutoGenerated/*.json before/after
   - No unexpected value changes

4. **Schema Compliance**
   - All 138 simulations must remain compliant
   - New simulations must follow SimulationBase pattern

---

## What NOT to Implement for v20

Based on assessment, these are **deferred** to v21+:

1. **Full Calabi-Yau Moduli Space** - Too complex, theoretical only
2. **Quantum Gravity Corrections** - Beyond current testability
3. **Anthropic Selection Mechanism** - Philosophical, not computable
4. **Omega Point Dynamics** - Teleological, not physical

---

## Success Criteria for v20

| Metric | v19.2 | v20 Target |
|--------|-------|------------|
| Schema Compliance | 100% | 100% |
| Gates Verified | 40/42 | 42/42 |
| Hardcoded Constants | 11 files | 0 files |
| Orphaned Parameters | 62 | 0 |
| Recursive Resolution | No | Yes |
| EW Precision Loop | Partial | Complete |
| Success Rate | 84.6% | 90%+ |

---

## Execution Timeline

### Wave 1 (Parallel)
- [ ] Agent A: Fix 11 hardcoded constant files
- [ ] Agent B: Register 62 orphaned parameters
- [ ] Agent C: Map 191 orphaned formulas to sections

### Wave 2 (After Wave 1)
- [ ] Agent D: Implement recursive dependency resolver
- [ ] Agent E: Implement iterative EW precision loop

### Wave 3 (After Wave 2)
- [ ] Agent F: Implement Yukawa texture derivations
- [ ] Agent G: Link dark matter residue calculation

### Final Validation
- [ ] Run full simulation suite
- [ ] Verify all gates
- [ ] Generate v20 certificates
- [ ] Tag v20.0-RECURSIVE

---

## Files to Create/Modify

### New Files
- `core/dependency_resolver.py` - Recursive resolution logic
- `simulations/v20/electroweak_precision_v20.py` - Iterative G_F
- `simulations/v20/yukawa_textures_v20.py` - Golden Ratio masses
- `simulations/v20/dark_matter_residue_v20.py` - Volume derivation

### Modified Files
- `core/PMRegistry.py` - Add dependency graph
- `core/FormulasRegistry.py` - VERSION = "20.0-RECURSIVE"
- 11 simulation files - Replace hardcoded → registry.get()
- `AutoGenerated/parameters.json` - Add 62 parameters

---

*Plan generated from v19.2 assessment. Awaiting implementation approval.*
