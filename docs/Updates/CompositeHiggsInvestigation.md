# Composite Higgs Investigation: pNGB Mechanism and PM Compatibility

**Investigation Report: HG-05.1**
**Date**: 2026-01-14
**Status**: CRITICAL ANALYSIS

---

## Executive Summary

This investigation examines whether the pseudo-Nambu-Goldstone boson (pNGB) mechanism for composite Higgs models could explain why v = 246 GeV instead of M_Pl = 2.4 x 10^18 GeV, and assesses compatibility with the Principia Metaphysica (PM) framework.

**Key Finding**: The composite Higgs mechanism offers a compelling physical explanation for the hierarchy, but faces significant tension with PM's fundamental assumption that the Higgs is a modulus field from G2 compactification. However, a potential synthesis exists where G2 geometry could provide the confining dynamics needed for compositeness.

---

## 1. The Hierarchy Problem: Core Statement

The Standard Model Higgs mass receives quadratic quantum corrections:

$$\delta m_H^2 \sim \frac{\Lambda^2}{16\pi^2}$$

For Lambda = M_Pl, this gives delta m_H ~ 10^16 GeV, but the observed Higgs mass is 125 GeV. This 10^16 discrepancy is the **hierarchy problem**.

**PM's Current Approach** (Appendix E): Claims the hierarchy is "geometric fate" from G2 topology, specifically from exponential warp factors and moduli stabilization. However, as honestly documented in `appendix_e_higgs_vev.md`, all naive formulas give v ~ 10^16-10^18 GeV - **wrong by 15+ orders of magnitude**.

---

## 2. The Composite Higgs Mechanism

### 2.1 Mathematical Framework

In composite Higgs models, the Higgs is not a fundamental scalar but a **pseudo-Nambu-Goldstone boson (pNGB)** arising from spontaneous symmetry breaking in a new strongly-coupled sector.

**Core Structure**:

1. **Global Symmetry Breaking**: A strong sector has global symmetry G spontaneously broken to subgroup H at scale f:

   $$G \xrightarrow{\langle\Sigma\rangle \neq 0} H$$

   Example: SO(5) -> SO(4), producing 4 Goldstone bosons (the Higgs doublet).

2. **Goldstone Theorem**: The breaking produces dim(G/H) massless Goldstone bosons:

   $$n_{GB} = \dim(G) - \dim(H)$$

3. **Explicit Breaking**: SM gauge and Yukawa couplings explicitly break G, giving Goldstones a potential:

   $$V(h) = \alpha f^4 \sin^2(h/f) - \beta f^4 \sin^4(h/f)$$

   where alpha, beta ~ g^2/(16 pi^2) are loop-suppressed.

### 2.2 The Higgs as pNGB

The Higgs mass is naturally light because:

$$m_H^2 \sim \frac{g^2}{16\pi^2} f^2$$

The loop suppression factor g^2/(16 pi^2) ~ 10^-2 automatically provides hierarchy protection.

### 2.3 Key Scales and Relations

**Compositeness scale f**: Sets the scale where new physics appears.

**VEV relation**:
$$v = f \sin(\theta)$$

where theta = <h>/f is the "misalignment angle". Typically sin(theta) ~ 0.1-0.3 for viable models.

**Electroweak-Planck hierarchy**:
$$\frac{v}{M_{Pl}} = \frac{f}{M_{Pl}} \sin(\theta)$$

To get v = 246 GeV with sin(theta) ~ 0.2:
$$f \sim 1-2 \text{ TeV}$$

The question then becomes: **why is f << M_Pl?**

---

## 3. How Compositeness Protects the Higgs Mass

### 3.1 Symmetry Protection Mechanism

In composite models, the Higgs mass is protected by two mechanisms:

1. **Goldstone Shift Symmetry**: Under the broken generators of G/H:
   $$h \to h + \epsilon \cdot f$$
   This forbids m_H^2 h^2 terms at tree level.

2. **Collective Breaking**: Multiple spurions (SM couplings) must combine to generate the Higgs potential:
   $$V(h) \sim g_1^2 g_2^2 f^4 \cdot (\text{trigonometric in } h/f)$$

### 3.2 The Coleman-Weinberg Potential

The one-loop effective potential takes the form:

$$V_{CW}(h) = \frac{N_c}{16\pi^2} m_t^4(h) \left[\log\frac{m_t^2(h)}{\mu^2} - \frac{3}{2}\right]$$

With m_t(h) = y_t f sin(h/f) / sqrt(2), this generates:

$$V(h) \approx -\frac{3 y_t^2}{8\pi^2} f^4 \sin^2(h/f)$$

The minimum occurs at h = <h> where:
$$\tan(2\langle h \rangle/f) = \frac{\beta}{\alpha}$$

### 3.3 Tuning Requirements

Composite models still require tuning at the level of:
$$\Delta \sim \frac{f^2}{v^2} \sim \xi^{-1}$$

For xi = v^2/f^2 ~ 0.1, this is ~ 10% tuning (much better than SM's 10^-32 tuning).

---

## 4. G2 Geometry and Strong Dynamics

### 4.1 Could G2 Provide Confining Dynamics?

The PM framework already contains the ingredients for strong dynamics:

**QCD from G2 (Appendix C)**:
- SU(3) color emerges from G2 -> SU(3) branching
- 8 gluons from adjoint representation decomposition: 14_G2 -> 8 + 3 + 3-bar
- Confinement from associative 3-cycle collapse (`wilson_loop_v18.py`)

**Key Observation**: The same geometric mechanism that produces QCD confinement could, in principle, produce a new confining sector responsible for Higgs compositeness.

### 4.2 Potential G2 Composite Mechanism

Consider a hypothetical **"Technicolor from G2"** scenario:

1. **Additional Strong Sector**: A second SU(N) gauge group from different G2 cycle structure
2. **Technifermions**: Matter charged under this new SU(N), arising from M2-branes on associative cycles
3. **Chiral Symmetry Breaking**: Condensate <psi-bar psi> at scale f ~ Lambda_TC
4. **Higgs as Techni-pion**: The lightest pseudo-scalar bound state

The compositeness scale would be:
$$f \sim \Lambda_{TC} \sim \frac{M_{Pl}}{V_{cycle}} \cdot e^{-S_{inst}}$$

where S_inst is the instanton action on the relevant cycle.

### 4.3 Specific G2 Realization

From PM's G2 manifold with b_3 = 24:
- 24 associative 3-cycles available
- 8 used for QCD gluons
- Remaining 16 could support additional gauge sectors

**Possible structure**:
$$\text{G2} \supset SU(3)_C \times SU(N)_{TC} \times ...$$

The technicolor scale would be set by cycle volumes:
$$\Lambda_{TC} \sim M_{GUT} \cdot \exp\left(-\frac{2\pi V_3}{\alpha'}\right)$$

---

## 5. Connection to Holographic QCD and AdS/CFT

### 5.1 AdS/CFT Perspective on Composite Higgs

In the AdS/CFT correspondence:
- 4D strongly-coupled CFT <-> 5D weakly-coupled gravity in AdS
- Composite Higgs models have a natural 5D holographic dual

**Randall-Sundrum as Composite Higgs**:
The RS warped extra dimension can be interpreted as:
- UV brane: Elementary sector (Planck scale)
- IR brane: Composite sector (TeV scale)
- Warp factor: Dynamical generation of hierarchy

This is exactly the mechanism invoked in PM's Section E.7.3 (warp factor suppression).

### 5.2 PM's Implicit Holographic Structure

PM's framework contains holographic elements:
- 7D G2 manifold reduces to effective 4D
- Warped geometry from moduli stabilization
- Bulk-to-boundary propagation in dimensional reduction

**Critical Insight**: If PM's "warp factor" (kR ~ 12) is taken seriously, it effectively implements a composite/holographic Higgs mechanism without explicit strong dynamics.

The formula:
$$v_H = v_0 \cdot e^{-\pi k R}$$

with kR ~ 12 gives e^(-pi * 12) ~ 10^-16, which is precisely the hierarchy ratio.

### 5.3 G2 Holography

Recent work on G2 holography suggests:
- M-theory on G2 x AdS_4 has a 3D CFT dual
- The 4D physics lives on a "defect" in this picture
- Composite states correspond to wrapped M2/M5-branes

This provides a potential bridge between PM's geometric approach and composite Higgs dynamics.

---

## 6. PM Moduli as Composite States?

### 6.1 Current PM Treatment of Moduli

In PM (`moduli_simulation_v18.py`), moduli are treated as:
- Fundamental scalar fields from G2 reduction
- Stabilized by racetrack superpotential
- VEV determined by flux quantization

The Higgs is identified with a specific 3-cycle modulus (Section E.3):
$$H \sim T_3 + i A_3$$

### 6.2 Composite Reinterpretation

An alternative interpretation:
- **Moduli = collective coordinates** of wrapped brane configurations
- **Higgs = bound state** of M2-branes wrapping shrinking cycles
- **VEV = condensate** of the strong dynamics

This would change the derivation chain:
1. G2 geometry determines confinement scale Lambda
2. Lambda sets compositeness scale f
3. f and misalignment angle theta give v = f sin(theta)
4. Higgs mass m_H from collective-breaking potential

### 6.3 Implications for PM Formulas

The current PM formula:
$$v_H = \frac{M_{Pl}}{4\pi\sqrt{b_3}} \cdot \epsilon$$

would be reinterpreted as:
$$v_H = f \cdot \sin(\theta) = \Lambda_{TC} \cdot \xi^{1/2}$$

where Lambda_TC comes from G2 cycle dynamics and xi ~ v^2/f^2 ~ 0.1.

---

## 7. Honest Assessment of PM Compatibility

### 7.1 Tensions

1. **Fundamental vs. Composite**: PM treats Higgs as fundamental modulus; composite models treat it as bound state. These are conceptually different.

2. **Scale Generation**: PM's formulas for v from topology give wrong values (10^16-10^18 GeV). This is honestly acknowledged in Appendix E.

3. **New Physics Signatures**: Composite Higgs predicts:
   - Higgs self-coupling deviations: lambda_hhh / lambda_SM ~ 1 - 2 xi
   - Top partner resonances at scale f ~ 1 TeV
   - Higgs coupling modifications: g_hVV / g_SM ~ sqrt(1 - xi)

   PM makes no such predictions from geometry alone.

### 7.2 Potential Compatibilities

1. **Warped Geometry = Holographic Dual**: PM's warp factor mechanism (Section E.7.3) is mathematically equivalent to a holographic composite Higgs.

2. **G2 Confinement**: The same mechanism producing QCD confinement could produce technicolor dynamics.

3. **Moduli = Collective Modes**: Reinterpreting moduli as collective coordinates of brane configurations bridges the approaches.

### 7.3 What PM Would Need to Incorporate

For composite Higgs compatibility, PM would need:

1. **Explicit Strong Sector**: Identify which G2 cycles support the confining gauge group
2. **Compositeness Scale**: Derive f from geometric data (not just v)
3. **Misalignment Angle**: Explain why sin(theta) ~ 0.1-0.3
4. **Resonance Predictions**: Bound state spectrum from M2-brane dynamics

---

## 8. Proposed Resolution

### 8.1 Synthesis: Geometric Compositeness

A potential synthesis combines PM geometry with composite dynamics:

**G2 Geometric Compositeness**:
1. G2 manifold contains confining sector from subset of b_3 = 24 cycles
2. M2-branes wrapping these cycles form bound states
3. Lightest bound state = Higgs (pNGB of broken chiral symmetry)
4. Compositeness scale f set by cycle volumes: f ~ M_GUT * exp(-V_3/alpha')
5. VEV from potential: v = f * sin(theta) with theta determined by flux

**Key Formula**:
$$v = M_{GUT} \cdot \exp\left(-\frac{\pi \cdot \text{Vol}(\Sigma_3)}{g_s \alpha'}\right) \cdot \sin(\theta)$$

This provides:
- Exponential hierarchy from geometry (not fine-tuning)
- Loop-protected Higgs mass (from Goldstone nature)
- Testable predictions (composite resonances)

### 8.2 Required Developments

To implement this:
1. Identify the "technicolor" 3-cycles in TCS #187
2. Calculate cycle volumes and instanton actions
3. Derive misalignment angle from flux configuration
4. Predict resonance spectrum from wrapped M2-brane dynamics

---

## 9. Conclusions

### 9.1 Assessment Summary

| Criterion | Composite Higgs | PM Current | PM + Composite |
|-----------|-----------------|------------|----------------|
| Explains v = 246 GeV | Yes (with f input) | No (formulas fail) | Potentially |
| Explains v << M_Pl | Yes (Goldstone protection) | Claimed but unproven | Yes |
| No fine-tuning | 10% tuning in xi | Claims none | 10% tuning |
| Testable predictions | Yes (resonances) | Limited | Yes |
| Fits G2 framework | Not inherently | Yes | Yes |

### 9.2 Scientific Honesty Statement

**What composite Higgs provides**: A well-understood physical mechanism for protecting the Higgs mass through Goldstone shift symmetry and collective breaking. The hierarchy is dynamically generated, though the scale f must still be explained.

**What PM provides**: A geometric framework where all scales emerge from topology. However, the specific derivation of v = 246 GeV from G2 data fails by 15+ orders of magnitude with naive formulas.

**Synthesis potential**: G2 geometry could provide the confining dynamics needed for a composite Higgs. The warp factor mechanism already present in PM is mathematically equivalent to holographic compositeness. This synthesis would combine the explanatory power of both approaches but requires significant development.

### 9.3 Recommendations

1. **Acknowledge the gap**: PM's Higgs VEV derivation remains an open problem, as Section E.12 honestly states.

2. **Explore G2 compositeness**: Investigate whether a subset of the b_3 = 24 cycles could support a confining sector producing composite Higgs.

3. **Develop holographic connection**: Formalize the relationship between PM's warp factor and AdS/CFT composite Higgs models.

4. **Predict testable signatures**: If the Higgs is composite, derive the resonance spectrum from G2 brane dynamics.

---

## References

1. Kaplan, D.B. & Georgi, H. (1984). "SU(2) x U(1) Breaking by Vacuum Misalignment". Phys. Lett. B 136, 183
2. Agashe, K., Contino, R., & Pomarol, A. (2005). "The Minimal Composite Higgs Model". Nucl. Phys. B 719, 165
3. Panico, G. & Wulzer, A. (2016). "The Composite Nambu-Goldstone Higgs". Springer
4. Randall, L. & Sundrum, R. (1999). "Large Mass Hierarchy from a Small Extra Dimension". Phys. Rev. Lett. 83, 3370
5. Maldacena, J. (1998). "The Large N Limit of Superconformal Field Theories". Adv. Theor. Math. Phys. 2, 231
6. Contino, R., Nomura, Y., & Pomarol, A. (2003). "Higgs as a Holographic Pseudo-Goldstone Boson". Nucl. Phys. B 671, 148
7. Acharya, B.S. et al. (2007). "M theory, G2-manifolds and Four-Dimensional Physics". Class. Quantum Grav. 24, S489

---

*Document generated: 2026-01-14*
*Principia Metaphysica - Hierarchy Investigation HG-05.1*
