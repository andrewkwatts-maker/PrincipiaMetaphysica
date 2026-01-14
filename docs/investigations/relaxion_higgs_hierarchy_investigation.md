# Investigation: Relaxion Mechanism for Higgs Hierarchy

**Investigation ID**: HG-05-RELAXION
**Date**: 2026-01-14
**Status**: COMPREHENSIVE ANALYSIS

---

## Executive Summary

This investigation examines whether the relaxion mechanism (Graham, Kaplan, Rajendran 2015) could resolve the Higgs hierarchy problem within the Principia Metaphysica (PM) framework. The relaxion is a cosmological solution where a slowly-rolling scalar field scans the Higgs mass-squared parameter during inflation until QCD dynamics generates a stopping barrier.

**Key Finding**: While PM's G2 axionic moduli share structural similarities with relaxions, significant tensions exist between the relaxion requirements and PM's cosmological framework. The mechanism faces serious challenges regarding inflation duration, decay constant bounds, and the QCD transition barrier.

---

## 1. The Relaxion Mechanism: Mathematical Foundation

### 1.1 Core Concept

The relaxion mechanism addresses why v = 246 GeV instead of M_Pl = 2.4 x 10^18 GeV through cosmological dynamics rather than symmetry or fine-tuning.

The key insight: During inflation, a pseudo-Nambu-Goldstone boson (the relaxion) slowly rolls down its potential, dynamically scanning the Higgs mass parameter. When the Higgs mass crosses zero and electroweak symmetry breaks, QCD dynamics generate a periodic barrier that traps the relaxion.

### 1.2 The Relaxion Lagrangian

The effective Lagrangian contains:

```
L = L_SM + (1/2)(d_mu phi)^2 - V(phi, H)
```

where the potential is:

```
V(phi, H) = (-M^2 + g*phi)*|H|^2 + lambda*|H|^4 + V_roll(phi) + V_barrier(phi, h)
```

**Terms**:
- **(-M^2 + g*phi)|H|^2**: Higgs mass parameter scanned by relaxion
- **M**: Cutoff scale (could be GUT scale ~ 10^16 GeV)
- **g**: Relaxion-Higgs coupling (dimensionally g ~ M^2/f)
- **V_roll(phi) = r*M^4*phi/f**: Slow-roll potential driving relaxion evolution
- **V_barrier(phi, h) = Lambda_c^4 * cos(phi/f)**: QCD-induced barrier (appears only when h != 0)
- **f**: Relaxion decay constant
- **Lambda_c**: Confinement scale (Lambda_QCD ~ 200 MeV for QCD barrier)

### 1.3 Dynamical Scanning

The Higgs mass-squared parameter evolves as:

```
m_H^2(phi) = -M^2 + g*phi
```

**Evolution sequence**:
1. Initially: phi ~ 0, so m_H^2 ~ -M^2 < 0 (wrong-sign mass)
2. As phi rolls: m_H^2 increases, crosses zero at phi_crit = M^2/g
3. When m_H^2 > 0: EWSB occurs, Higgs gets VEV, QCD barrier turns on
4. Barrier growth eventually stops relaxion roll

### 1.4 Stopping Condition

The relaxion stops when the barrier force equals the rolling force:

```
|dV_roll/dphi| = |dV_barrier/dphi|

r*M^4/f = (Lambda_c^4/f) * sin(phi/f)
```

At stopping:
```
r*M^4 ~ Lambda_c^4
```

where Lambda_c ~ Lambda_QCD * (v/Lambda_QCD)^n with n depending on the specific barrier mechanism.

### 1.5 The Electroweak Scale Emerges

The final Higgs VEV is determined by when the barrier becomes strong enough to halt the roll. The "naturalness" emerges because:

```
v^2 ~ Lambda_c^4 / (r * M^2)
```

With appropriate parameter choices, v ~ 246 GeV emerges dynamically.

---

## 2. Cosmological Requirements

### 2.1 Inflation Duration

The relaxion must scan from phi ~ 0 to phi ~ M^2/g during inflation. The field excursion is:

```
Delta_phi ~ M^2/g ~ f * (M/Lambda_c)^4
```

This requires many e-folds of inflation:

```
N_e > (Delta_phi)^2 / (M_Pl^2 * epsilon)
```

For M ~ 10^16 GeV and Lambda_c ~ GeV scale:
```
N_e > 10^32 to 10^40 e-folds
```

This is far beyond the ~60 e-folds required for solving horizon/flatness problems.

### 2.2 Hubble Scale Constraint

During inflation, quantum fluctuations must not kick the relaxion over barriers:

```
H_I < Lambda_c^2 / f
```

For QCD barrier: Lambda_c ~ Lambda_QCD ~ 200 MeV
```
H_I < (200 MeV)^2 / f ~ (40 MeV)^2 / (f / 10^9 GeV)
```

This implies very low-scale inflation: H_I < keV to MeV scale.

### 2.3 QCD Transition During Inflation

The QCD barrier requires the QCD phase transition to occur during inflation. This is problematic because:

1. Standard QCD transition occurs at T ~ 150 MeV
2. During inflation, T ~ H_I / (2*pi)
3. If H_I < MeV, then T << Lambda_QCD and QCD is already confined

**Resolution**: Variants use non-QCD barriers (e.g., new strong sector, explicit breaking terms).

---

## 3. PM Framework Assessment

### 3.1 PM's Axionic Moduli

PM features several axionic fields from G2 compactification:

**From `axion_dm_v18.py`**:
```
f_a = M_Pl / k_gimel^6 ~ 3.5 x 10^12 GeV
```

**From `moduli_simulation_v18.py`**:
```
Im(T) = axionic component of Kahler modulus
Stabilized at Im(T) = 0 by racetrack potential
```

**From `attractor_potential_v18.py`**:
```
V(phi_M) = V_0 * [1 + A * cos(omega * phi_M / f)]
f = M_Pl / sqrt(chi_eff) ~ 2 x 10^17 GeV
```

### 3.2 Structural Similarities

| Property | Relaxion | PM Axions |
|----------|----------|-----------|
| Shift symmetry | Yes (approximate) | Yes (from higher-D gauge invariance) |
| Periodic potential | Yes (barrier) | Yes (cosine from instanton effects) |
| Coupling to Higgs | Required | Indirect (through moduli stabilization) |
| Decay constant | f ~ 10^9-10^12 GeV | f ~ 10^12-10^17 GeV |

### 3.3 Critical Differences

**1. Decay Constant Scale**

PM's axion decay constants are too large for standard relaxion:
- Relaxion requires: f ~ 10^9 GeV for QCD barrier
- PM predicts: f ~ 10^12-10^17 GeV

This mismatch by 3-8 orders of magnitude is severe.

**2. Moduli Stabilization**

PM's moduli are stabilized by racetrack potential, not by cosmological evolution:
```
W(T) = A*exp(-aT) + B*exp(-bT)
<T> = ln(Aa/Bb) / (a - b) ~ 1.833
```

This is a static vacuum solution, not a dynamical scanning mechanism.

**3. Higgs as Modulus**

In PM (Appendix E), the Higgs is identified with a G2 modulus:
```
H ~ T_3 + i*A_3
```

This means the Higgs VEV is determined by moduli stabilization, not by cosmological relaxation.

### 3.4 PM's Cosmological Framework

PM's cosmology (from `cosmology_sector_complete_v19.py`) features:

**Hubble constant**:
```
H_0 = 71.55 km/s/Mpc (O'Dowd formula)
```

**Dark energy**:
```
w_0 = -23/24 = -0.9583 (tzimtzum pressure)
```

**Attractor dynamics**:
```
phi_M evolves under Ricci flow toward fixed point
```

This is a late-time cosmology, not an inflationary framework.

---

## 4. Could G2 Axions Serve as Relaxions?

### 4.1 Requirements for Adaptation

To make PM axions function as relaxions, we would need:

**1. Lower decay constant**
- Current: f ~ 10^17 GeV
- Required: f ~ 10^9 GeV
- This requires 8 additional powers of suppression

**2. Higgs-axion coupling**
- Must introduce: g*phi*|H|^2 term
- PM has: Higgs = modulus identification (no direct coupling)

**3. Extended inflation**
- Current: No PM inflation model
- Required: 10^30+ e-folds at H_I < MeV

**4. Barrier mechanism**
- QCD barrier requires low H_I
- Non-QCD barriers need new strong sector at TeV scale

### 4.2 The Decay Constant Problem

PM derives (from `axion_dm_v18.py`):
```
f_a = M_Pl / k_gimel^6 = 1.22 x 10^19 / (12.318)^6 ~ 3.5 x 10^12 GeV
```

For relaxion, we need:
```
f ~ Lambda_barrier^2 / H_I
```

With H_I ~ 10^6 GeV (to fit PM's natural inflation scale from moduli):
```
f ~ (200 MeV)^2 / 10^6 GeV ~ 4 x 10^-11 GeV  (absurdly small!)
```

Or with H_I ~ 1 GeV:
```
f ~ (200 MeV)^2 / 1 GeV ~ 40 MeV (still too small)
```

The only way to have f ~ 10^12 GeV requires H_I << meV, which is incompatible with any reasonable inflationary model.

### 4.3 The N_e Problem in PM

PM's b3 = 24 structure does not provide a natural mechanism for 10^30+ e-folds.

Standard estimates for modular inflation:
```
N_e ~ M_Pl^2 / (field range)^2 ~ 60-100
```

For relaxion to work:
```
N_e ~ (f/H_I)^2 * (M/Lambda_c)^8 >> 10^30
```

No known mechanism in string/M-theory produces such extended inflation.

---

## 5. Variants and Alternatives

### 5.1 Non-QCD Barriers

Some relaxion models use TeV-scale barriers instead of QCD:
- New confining gauge group at TeV scale
- Higgs-dependent mass for new fermions

**PM Assessment**: The 163/125 visible/sterile sector split could in principle house such a sector, but:
- No mechanism specified in PM for TeV-scale confinement
- Would require adding to the framework rather than deriving from it

### 5.2 Clockwork Mechanism

The "clockwork" variant exponentially enhances the effective decay constant:
```
f_eff = f_0 * q^N
```

where q ~ few and N ~ number of "gears."

**PM Assessment**: PM's b3 = 24 cycles could provide a clockwork-like structure, but:
- Would require specific identification of cycles with clockwork sites
- Decay constant enhancement works opposite to what relaxion needs

### 5.3 Sliding Naturalness

Hybrid models where SUSY and relaxion cooperate:
- SUSY provides partial cancellation down to TeV
- Relaxion scans the remaining hierarchy

**PM Assessment**: PM's SUSY breaking occurs at high scale (Re(T) ~ 1.833 gives m_3/2 ~ TeV), so this could be viable if:
- SUSY breaking scale set by moduli
- Relaxion scans residual hierarchy
- Still faces e-fold problem

---

## 6. Constraints on Relaxion Models

### 6.1 Theoretical Constraints

| Constraint | Requirement | PM Status |
|------------|-------------|-----------|
| Decay constant | f < 10^12 GeV (QCD barrier) | f ~ 10^17 GeV (FAILS) |
| Inflation duration | N_e > 10^30 | No mechanism (FAILS) |
| Hubble scale | H_I < MeV | Not specified |
| Shift symmetry quality | Planck-suppressed breaking | Could work |
| Weak gravity conjecture | f < M_Pl | Satisfied |

### 6.2 Observational Constraints

**Higgs physics**:
- Relaxion-Higgs mixing constrained by LHC
- theta ~ v^2 / (f * Lambda) < 0.01

**Cosmology**:
- Isocurvature perturbations constrained by Planck
- Relaxion must be sufficiently massive today

**Fifth force**:
- Long-range forces from light relaxion
- Constrained by Eot-Wash, MICROSCOPE

---

## 7. Honest Assessment

### 7.1 The Fundamental Tension

The relaxion mechanism and PM's geometric approach represent **fundamentally different philosophies**:

**Relaxion**: The electroweak scale is anthropically/cosmologically selected from a continuum of possibilities through dynamical evolution.

**PM**: The electroweak scale is geometrically fixed by the topology of the internal G2 manifold through moduli stabilization.

These are philosophically incompatible:
- Relaxion: v is dynamical and scanned
- PM: v is fixed by topology

### 7.2 What PM's Axionic Structure Could Provide

If we were to abandon the "geometric derivation" approach, PM's axions could contribute:
1. A shift-symmetric scalar from dimensional reduction
2. A naturally periodic potential from instanton effects
3. Possible clockwork-like structure from b3 = 24 cycles

### 7.3 What PM Cannot Provide

1. A natural mechanism for 10^30+ e-folds of inflation
2. A QCD-like barrier that appears during inflation
3. A decay constant in the right range (10^9 GeV)
4. A Higgs-relaxion coupling from first principles

### 7.4 The Mismatch with Appendix E

Appendix E honestly acknowledges that naive geometric formulas fail by 15+ orders of magnitude. The relaxion is one possible resolution, but it requires:

1. Abandoning the hope of a purely geometric derivation
2. Introducing an extended inflationary epoch not present in PM
3. Assuming anthropic selection from a landscape of vacua

This is a significant departure from PM's stated goals.

---

## 8. Conclusions

### 8.1 Viability Assessment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Mathematical consistency | 6/10 | Relaxion math is sound; PM adaptation problematic |
| Framework compatibility | 2/10 | Fundamental philosophical tension |
| Cosmological requirements | 2/10 | N_e problem is severe |
| Decay constant matching | 2/10 | 5-8 orders of magnitude mismatch |
| Predictive power | 3/10 | Loses geometric determination |
| Overall viability | 3/10 | Not viable within current PM framework |

### 8.2 Recommendations

**Option A: Accept Geometric Mismatch**
The current PM approach honestly acknowledges that v = 246 GeV is not derived from topology. Continue refining warp factor or moduli stabilization approaches.

**Option B: Hybrid Mechanism**
Investigate whether PM's b3 = 24 structure could provide partial hierarchy resolution, with relaxion-like dynamics handling the residual gap.

**Option C: Alternative Scanning**
Consider whether PM's Ricci flow cosmology could provide a scanning mechanism distinct from relaxion that is more compatible with the framework.

### 8.3 Future Investigations

1. **Warp factor enhancement**: Can warped G2 geometry provide the needed 10^16 suppression without relaxion?

2. **Moduli-Higgs coupling**: What is the precise relationship between G2 moduli and the Higgs field in PM?

3. **PM inflation model**: Develop an explicit inflationary sector compatible with PM's geometric constraints.

4. **Non-QCD barriers**: Could PM's sterile sector (163 states) provide a barrier mechanism?

---

## References

1. Graham, P.W., Kaplan, D.E., Rajendran, S. (2015). "Cosmological Relaxation of the Electroweak Scale." Phys. Rev. Lett. 115, 221801

2. Espinosa, J.R., Grojean, C., Panico, G., Pomarol, A., Pujolas, O., Servant, G. (2015). "Cosmological Higgs-Axion Interplay for a Naturally Small Electroweak Scale." arXiv:1506.09217

3. Choi, K., Im, S.H. (2016). "Relaxion Window." JHEP 01, 149

4. Fonseca, N., de Vries, J., Marzola, L., Reina, B. (2018). "Relaxion dark matter." arXiv:1811.10633

5. Banerjee, S., Chakrabarty, K., Chowdhury, D. (2020). "Relaxion models: current status and future prospects." arXiv:2010.13118

---

*Investigation completed: 2026-01-14*
*Principia Metaphysica v20.11*
