# Parameter Terminology Standard - v24.2

**Date**: 2026-02-24
**Purpose**: Resolve "zero fitted" vs "2-5 fitted" inconsistency per Gemini feedback
**Gemini Priority**: CRITICAL / IMPORTANT

---

## Problem Statement

**Current inconsistency** across documentation:
- README: "zero fitted parameters (sterile model)"
- Same README: "2 fitted parameters" and "~5 fitted parameters"
- Abstract: "EDOF=3 (3 geometric seeds)"
- Appendices: "zero free parameters"

**Gemini critique**: "Cannot claim both 'zero fitted' and '2-5 fitted' parameters"

---

## Standardized Terminology (v24.2)

### Framework Classification

**Principia Metaphysica v24.2: Topologically Anchored Framework**

Total constants: **125**
Total inputs: **8**
Pure predictions: **117**

---

### Parameter Categories (Defined in config.py ParameterCategory)

#### 1. GEOMETRIC (Pure Topology)
**Definition**: Derived entirely from G₂ manifold topology with no phenomenological input

**Examples**:
- b₃ = 24 (Betti number of G₂ associative 3-cycles)
- χ_eff = 144 (Euler characteristic from TCS #187)
- n_gen = 3 (from G₂ index theorem: χ_eff/(2·b₃) = 144/48 = 3)

**Count**: ~20 parameters
**Status**: PURE TOPOLOGY (zero free parameters in this category)

---

#### 2. INPUT (Phenomenological Scale Anchors)
**Definition**: Experimental values used to fix energy scales (not topology)

**Examples**:
- M_Planck = 2.435×10¹⁸ GeV (reduced Planck mass, PDG 2024)
- m_H = 125.25 GeV (Higgs mass, LHC)
- α_GUT coefficient = 1/(10π) ≈ 0.0318 (phenomenological calibration)

**Count**: **3 parameters**
**Status**: PHENOMENOLOGICAL ANCHORS (fix scales, not topology)

---

#### 3. CALIBRATED (Semi-Derived Scale Factors)
**Definition**: Coefficients derived from geometric formulas but requiring one phenomenological constraint

**Examples**:
- VEV coefficient = 1.5859 (semi-derived via ln(M_Pl/v_EW)/b₃ + |T_ω|/b₃)
- Re(T) = 7.086 (derived from m_H constraint via racetrack minimization)

**Count**: **3 parameters**
**Status**: GEOMETRIC DERIVATION + SCALE CONSTRAINT

---

#### 4. FITTED (Pending Explicit Derivation)
**Definition**: Parameters currently fitted to data but theoretically derivable from explicit Yukawa calculation

**Examples**:
- θ₁₃ = 8.65° (fitted to NuFIT 6.0; pending explicit Yukawa from G₂ overlap integrals)
- δ_CP = 278° (fitted to NuFIT 6.0; pending CP-violating phase derivation)

**Count**: **2 parameters**
**Status**: TEMPORARILY FITTED (pending v25.0 Yukawa completion)

---

#### 5. DERIVED (Computed from Topology + Scales)
**Definition**: Calculated from GEOMETRIC + INPUT parameters via explicit formulas

**Examples**:
- M_GUT = 3.98×10¹⁶ GeV (from b₃, M_Planck, α_GUT)
- τ_proton = 8.15×10³⁴ years (from TCS cycle separation)
- w₀ = -23/24 (from bridge pressure mismatch)

**Count**: ~60 parameters
**Status**: DERIVED (no free parameters, computed from topology + scales)

---

#### 6. PREDICTED (Pure Testable Outputs)
**Definition**: Predictions for not-yet-measured quantities

**Examples**:
- M_KK = 4.5 TeV (KK graviton mass)
- m_ALP = 3.510 meV (axion-like particle mass)
- g_aγγ = 1.0×10⁻¹¹ GeV⁻¹ (ALP-photon coupling)

**Count**: ~37 parameters
**Status**: PURE PREDICTIONS (testable by experiments 2025-2035)

---

## Effective Degrees of Freedom (EDOF)

**EDOF = 3** (topological seeds that fix all topology)
- b₃ = 24
- φ = (1+√5)/2 (golden ratio, from minimal surface geometry)
- χ_eff = 144 (from TCS Euler characteristic)

**Statistical Interpretation**:
All 125 constants are correlated through single G₂ manifold geometry.
Jacobian rank analysis: rank(J) = 3 (where J is 125×3 sensitivity matrix).

**NOT counted as EDOF**:
- 3 INPUT (phenomenological scale anchors - fix energy scales only)
- 2 FITTED (pending Yukawa derivation)

---

## Compression Ratios

### Conservative Estimate (All Inputs)
**125 constants : 8 inputs = 15.6:1 compression**
- 8 inputs = 3 GEOMETRIC seeds + 3 INPUT scales + 2 FITTED angles

### Topological Compression (Pure Topology)
**117 predictions : 3 topological seeds = 39:1 compression**
- 117 = 125 total - 3 INPUT - 3 CALIBRATED - 2 FITTED

### Information-Theoretic (Claimed in Appendix T)
**8000 bits : 69 bits = 116:1 compression**
- 8000 bits: PDG data representation
- 69 bits: 3 seeds (assuming ~23 bits each for precision)

---

## Standardized Claims (What to Say)

### ✅ CORRECT Phrasing

**For Abstract/Introduction**:
> "The framework achieves a topologically anchored structure with EDOF=3
> (three geometric seeds: b₃, φ, χ_eff), deriving 117 of 125 fundamental
> constants. Three phenomenological inputs (M_Planck, m_H, α_GUT) fix energy
> scales only, not topology. Two PMNS angles (θ₁₃, δ_CP) are currently fitted
> pending explicit Yukawa derivation."

**For Claims of "Zero Parameters"**:
> "Zero free topological parameters: All manifold topology fixed by G₂ choice.
> Compression ratio: 125 constants from 3 topological seeds + 3 scale anchors."

**For Statistical Framework**:
> "Effective degrees of freedom EDOF=3 confirmed by Jacobian rank analysis
> (rank(J)=3 for 125×3 sensitivity matrix). The 125 constants are highly
> correlated through shared G₂ geometric origin."

---

### ❌ INCORRECT Phrasing (Do Not Use)

**WRONG**: "Zero fitted parameters"
- Contradicts θ₁₃, δ_CP being fitted

**WRONG**: "No free parameters"
- Ambiguous; could imply no inputs at all

**WRONG**: "All 125 constants derived from pure topology"
- Ignores phenomenological scale anchors

**WRONG**: "Parameter-free theory"
- Too strong; implies no experimental inputs

---

## Implementation Checklist

Update the following files with standardized terminology:

- [ ] README.md (remove "zero fitted parameters", use standard language)
- [ ] Abstract (simulations/PM/paper/abstract.py)
- [ ] Introduction (simulations/PM/paper/introduction.py)
- [ ] Methodology (simulations/PM/paper/methodology.py)
- [ ] Results (simulations/PM/paper/results.py)
- [ ] Discussion (simulations/PM/paper/discussion.py)
- [ ] All appendices claiming "zero free parameters"
- [ ] Website index.html and all HTML pages
- [ ] CHANGELOG.md

---

## Definition Summary Table

| Category | Count | Status | Purpose |
|----------|-------|--------|---------|
| GEOMETRIC | ~20 | Pure topology | Fix manifold structure |
| INPUT | 3 | Phenomenological | Fix energy scales |
| CALIBRATED | 3 | Semi-derived | Geometric + scale constraint |
| FITTED | 2 | Pending derivation | NuFIT oscillation data |
| DERIVED | ~60 | Computed | Topology + scales → outputs |
| PREDICTED | ~37 | Testable | Pure predictions |
| **TOTAL** | **125** | | |

**EDOF**: 3 (topological seeds only)
**Total Inputs**: 8 (3 + 3 + 2)
**Pure Predictions**: 117 (125 - 8)
**Compression**: 125:8 = 15.6:1 (or 117:3 = 39:1 for topology only)

---

**END OF PARAMETER TERMINOLOGY STANDARD v24.2**
