# Gate Categorization for Peer Review Issue 3

*Created: 2026-01-17*
*Purpose: Remove circular validation by categorizing all 72 gates*

---

## Categories

| Category | Definition | Example |
|----------|------------|---------|
| **DERIVED** | Derived from pure geometry with NO experimental input | n_gen = chi_eff/48 = 3 |
| **INPUT** | Uses experimental values as direct input (acknowledged) | m_top from PDG |
| **FITTED** | Parameters tuned to match data (problematic) | m_base = 0.049 eV |
| **TOPOLOGICAL** | Pure topological constraint (subset of DERIVED) | 288 = 125 + 163 |
| **GEOMETRIC** | Geometric identity (subset of DERIVED) | b3 = 24 |

---

## Phase 1: Structural Foundations (G01-G10) - Mostly TOPOLOGICAL

| Gate | Name | Category | Justification |
|------|------|----------|---------------|
| G01 | Integer Root Parity | TOPOLOGICAL | 288 is defined, not fitted |
| G02 | Holonomy Closure | GEOMETRIC | V7 holonomy is mathematical |
| G03 | Ancestral Mapping | TOPOLOGICAL | 125 + 163 = 288 is definition |
| G04 | Projection Tax | DERIVED | Lambda from 12/288^2 |
| G05 | Metric Continuity | GEOMETRIC | Smooth mapping requirement |
| G06 | Shadow-A/B Parity | TOPOLOGICAL | 12 + 12 = 24 |
| G07 | Torsion Orthogonality | GEOMETRIC | pi/2 is exact |
| G08 | Sterile Angle Anchor | DERIVED | arcsin(125/288) is exact |
| G09 | Pin Isotropic Distribution | TOPOLOGICAL | 4×6 = 24 |
| G10 | Torsion Tension Floor | DERIVED | Vacuum energy from topology |

---

## Phase 2: Gauge & Matter Registry (G11-G25) - Mixed

| Gate | Name | Category | Justification |
|------|------|----------|---------------|
| G11 | Strong Force Saturation | DERIVED | alpha_s from geometric formula |
| G12 | Electroweak Alignment | DERIVED | theta_W from shadow tilt |
| G13 | Photon Zero-Mass | GEOMETRIC | U(1) gauge symmetry |
| G14 | SU(N) Approximation | GEOMETRIC | Group theory |
| G15 | Gauge-Invariant Projection | GEOMETRIC | Ghost decoupling |
| G16 | Fermionic Dirac Mapping | GEOMETRIC | Spinor structure |
| G17 | Generation Triality | DERIVED | n_gen = chi_eff/48 |
| G18 | Quark Mass Hierarchy | FITTED | Uses Yukawa textures |
| G19 | Lepton Mass Hierarchy | FITTED | Uses Yukawa textures |
| G20 | CKM Matrix | FITTED | Octonionic mixing is speculative |
| G21 | PMNS Matrix | DERIVED | All 4 angles from geometry |
| G22 | Higgs VEV | FITTED | kRc = 11.21 tuned to v = 246 GeV |
| G23 | Higgs Mass | DERIVED | m_H from quartic coupling |
| G24 | W/Z Masses | DERIVED | From v and g,g' |
| G25 | Top Quark Mass | FITTED | y_t calibrated |

---

## Phase 3: Interaction & Mixing (G26-G40) - Mixed

| Gate | Name | Category | Justification |
|------|------|----------|---------------|
| G26 | QCD Confinement | DERIVED | Wilson loop area law |
| G27 | Asymptotic Freedom | DERIVED | RG flow from geometry |
| G28 | Proton Decay Bound | DERIVED | M_GUT from gauge unification |
| G29 | Neutron Decay | INPUT | Uses beta decay data |
| G30 | Baryon Asymmetry | DERIVED | V7 twist mechanism |
| G31 | CP Violation (quarks) | FITTED | delta_CKM tuned |
| G32 | CP Violation (leptons) | DERIVED | delta_PMNS from geometry |
| G33 | Anomaly Cancellation | GEOMETRIC | Mathematical consistency |
| G34 | Gauge Unification | DERIVED | M_GUT ~ 10^16 GeV |
| G35 | sin^2(theta_W) | DERIVED | From gauge coupling ratios |
| G36 | alpha_em | DERIVED | k_gimel formula |
| G37 | Fermi Constant | DERIVED | From M_W and g |
| G38 | Planck Mass | INPUT | Uses G_N as input |
| G39 | Cosmological Constant | DERIVED | Lambda from topology |
| G40 | Dark Energy w0 | DERIVED | w0 = -1 + 1/b3 |

---

## Phase 4: Cosmological & Metric (G41-G55) - Mixed

| Gate | Name | Category | Justification |
|------|------|----------|---------------|
| G41 | Dark Energy wa | **EXPLORATORY** | Formula not rigorous |
| G42 | Dark Matter Density | DERIVED | From sterile sector |
| G43 | Hubble Constant | **FITTED** | Brane angle is ad hoc |
| G44 | S8 Tension | DERIVED | Bulk viscosity mechanism |
| G45 | CMB Temperature | DERIVED | From vacuum energy |
| G46 | BBN Constraints | INPUT | Uses observed abundances |
| G47 | Inflation Slow-Roll | DERIVED | From 288-root descent |
| G48 | Reheating | DERIVED | From moduli decay |
| G49 | Gravitational Waves | DERIVED | Tensor-to-scalar ratio |
| G50 | Black Hole Entropy | DERIVED | From holographic bound |
| G51 | Speed of Light | DERIVED | c from dimensional analysis |
| G52 | Planck Length | DERIVED | From M_Pl |
| G53 | Planck Time | DERIVED | From M_Pl |
| G54 | KK Graviton Mass | DERIVED | From RS geometry |
| G55 | Extra Dimension Size | DERIVED | From kRc |

---

## Phase 5: Dimensional & Logical Closure (G56-G72) - Mostly GEOMETRIC

| Gate | Name | Category | Justification |
|------|------|----------|---------------|
| G56 | 26D Origin | GEOMETRIC | Bosonic string theory |
| G57 | Sp(2,R) Reduction | GEOMETRIC | Two-time physics |
| G58 | G2 Holonomy | GEOMETRIC | M-theory on G2 |
| G59 | 4D Emergence | GEOMETRIC | Compactification |
| G60 | Lorentz Invariance | GEOMETRIC | Symmetry requirement |
| G61 | CPT Theorem | GEOMETRIC | Mathematical theorem |
| G62 | Spin-Statistics | GEOMETRIC | Mathematical theorem |
| G63 | Unitarity | GEOMETRIC | Quantum mechanics |
| G64 | Causality | GEOMETRIC | Lightcone structure |
| G65 | Entropy Arrow | DERIVED | From 288-root initial state |
| G66 | Information Conservation | GEOMETRIC | Unitarity consequence |
| G67 | Omega Seal | TOPOLOGICAL | All gates consistent |
| G68 | Null Set Verification | TOPOLOGICAL | No 25th pin |
| G69 | Terminal Parity | GEOMETRIC | Closed manifold |
| G70 | Recursive Closure | GEOMETRIC | Self-consistent |
| G71 | Empty-Space Exclusion | GEOMETRIC | No hidden gauge |
| G72 | Final Terminal State | TOPOLOGICAL | All checks pass |

---

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| DERIVED | ~35 | 49% |
| GEOMETRIC/TOPOLOGICAL | ~25 | 35% |
| FITTED | ~8 | 11% |
| INPUT | ~3 | 4% |
| EXPLORATORY | ~1 | 1% |

---

## Critical Issues Identified

### FITTED Gates (Circular Validation Risk)

1. **G18/G19**: Quark/Lepton mass hierarchies - Yukawa textures are fitted
2. **G20**: CKM Matrix - Octonionic mixing is speculative
3. **G22**: Higgs VEV - kRc = 11.21 tuned to match v = 246 GeV
4. **G25**: Top quark mass - y_t is calibrated
5. **G31**: CP Violation (quarks) - delta_CKM is fitted
6. **G43**: Hubble Constant - Brane angle is completely ad hoc

### Neutrino Mass (Special Case)

The neutrino mass sum prediction (0.10 eV) is marked as **FALSIFICATION_RISK** because:
- m_base = 0.049 eV is explicitly "calibrated to atmospheric splitting"
- Inverted Ordering prediction creates tension with DESI < 0.072 eV
- This should be marked as FITTED, not DERIVED

---

## Action Items

1. Update Gate dataclass to include `category` field
2. Mark all 72 gates with appropriate category
3. Update simulation outputs to show category
4. Create clear legend in documentation
5. Acknowledge FITTED gates honestly in publications

---

## Conclusion

After categorization:
- ~60% of gates are genuinely DERIVED or GEOMETRIC (good)
- ~11% are FITTED and should be acknowledged (honest)
- ~4% use INPUT values (acceptable if acknowledged)

This categorization increases rigor by being transparent about which validations are genuine predictions vs. fits to data.
