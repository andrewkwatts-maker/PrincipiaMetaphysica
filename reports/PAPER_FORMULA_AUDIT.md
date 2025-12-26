# Paper Formula Audit Report

**Generated:** audit_paper_formulas.py
**Date:** 2025-12-26

## Executive Summary

- **Total equations in paper:** 814
- **Total formulas in theory_output.json:** 62
- **Matched:** 180
- **Paper only (not in theory_output.json):** 634
- **Theory only (not referenced in paper):** 16

---

## 1. Matched Formulas

These 180 equations appear in both the paper and theory_output.json:

### reduction-cascade
- **Section:** 1. Introduction
- **Equation number:** (1.1)
- **LaTeX:** `\text{26D}_{(24,2)} \xrightarrow{\text{Sp}(2,\mathbb{R})} \text{13D}_{(12,1)} \xrightarrow{G_2} \tex...`

### master-action-26d
- **Section:** 2. The 26-Dimensional Bulk Spacetime
- **Equation number:** (2.1)
- **Derivation box:** Key Distinctions from Standard Approaches
- **LaTeX:** `S_{26} = \int d^{26}x \sqrt{|G_{(24,2)}|} \left[ M_*^{24} R_{26} + \bar{\Psi}_P \left( i\Gamma^M D_M...`

### virasoro-anomaly
- **Section:** 2. The 26-Dimensional Bulk Spacetime
- **Equation number:** (2.2)
- **Derivation box:** Key Distinctions from Standard Approaches
- **LaTeX:** `c_{\text{total}} = c_{\text{matter}} + c_{\text{ghost}} = D + (-26) = 0 \quad \Rightarrow \quad D = ...`

### bekenstein-hawking
- **Section:** 2.6 Holographic Entropy from Pneuma
- **Equation number:** (2.5)
- **LaTeX:** `S_{\text{BH}} = \frac{A}{4l_P^2} = \frac{N_{\text{Pneuma}}}{4} \cdot \log(2)...`

### racetrack-superpotential
- **Section:** 2.7 Pneuma Vacuum Selection: Racetrack Mechanism
- **Equation number:** (2.6)
- **LaTeX:** `W(\Psi_P) = A \cdot e^{-a\Psi_P} - B \cdot e^{-b\Psi_P}...`

### scalar-potential
- **Section:** 2.7 Pneuma Vacuum Selection: Racetrack Mechanism
- **Equation number:** (2.7)
- **LaTeX:** `V(\Psi_P) = \left| \frac{\partial W}{\partial \Psi_P} \right|^2 = \left| -Aa \, e^{-a\Psi_P} + Bb \,...`

### pneuma-vev
- **Section:** 2.7 Pneuma Vacuum Selection: Racetrack Mechanism
- **Equation number:** (2.9)
- **LaTeX:** `\langle\Psi_P\rangle = \frac{\ln(Aa/Bb)}{a - b}...`

### primordial-spinor-13d
- **Section:** 3. Reduction to the 13-Dimensional Shadow
- **Equation number:** (3.2)
- **LaTeX:** `\Psi_{64} \in \text{Spin}(12,1), \quad \dim(\Psi) = 2^{[13/2]} = 64...`

### hidden-variables
- **Section:** 3.3 Hidden Variables from Shadow Branes
- **Equation number:** (3.3)
- **LaTeX:** `\rho_{\Sigma_1} = \text{Tr}_{\Sigma_2,\Sigma_3,\Sigma_4} \left[|\Psi\rangle_{\text{bulk}} \langle\Ps...`

### flux-quantization
- **Section:** 4. Compactification on the TCS G2 Manifold
- **Equation number:** (4.3)
- **LaTeX:** `N_{\text{flux}} = \frac{\chi_{\text{eff}}}{6} = \frac{144}{6} = 24 \quad \Rightarrow \quad T_{\omega...`

### mirror-dm-ratio
- **Section:** 4. Compactification on the TCS G2 Manifold
- **LaTeX:** `\frac{\Omega_{\text{DM}}}{\Omega_b} = \left(\frac{T}{T'}\right)^3 = \left(\frac{1}{0.57}\right)^3 \a...`

### so10-breaking
- **Section:** 5. Gauge Unification and the Standard Model
- **Equation number:** (5.1)
- **LaTeX:** `\text{SO}(10) \supset \text{SU}(3)_C \times \text{SU}(2)_L \times \text{U}(1)_Y...`

### gut-coupling
- **Section:** 5. Gauge Unification and the Standard Model
- **Equation number:** (5.2)
- **LaTeX:** `\frac{1}{\alpha_{\text{GUT}}} = 10\pi \times \frac{\text{Vol}(\Sigma_{\text{sing}})}{\text{Vol}(G_2)...`

### doublet-triplet
- **Section:** 5. Gauge Unification and the Standard Model
- **Equation number:** (5.4c)
- **LaTeX:** `N_{\text{doublets}} - N_{\text{triplets}} = \int_M \hat{A}(M) \wedge \text{ch}(L_Y) \mod \mathbb{Z}_...`

### weak-mixing-angle
- **Section:** 5. Gauge Unification and the Standard Model
- **Equation number:** (5.5)
- **LaTeX:** `\sin^2\theta_W(M_Z) = 0.23121...`

### ckm-elements
- **Section:** 6. Fermion Sector and Mixing Angles
- **Equation number:** (6.10)
- **LaTeX:** `|V_{ud}| = 0.974, \quad |V_{us}| = 0.225, \quad |V_{cb}| = 0.041, \quad |V_{ub}| = 0.0036...`

### yukawa-instanton
- **Section:** 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons
- **LaTeX:** `Y_{ij} = Y_{ij}^{(0)} \cdot e^{-S_{\text{inst}}} = Y_{ij}^{(0)} \cdot e^{-\text{Vol}(\Sigma_{ij})/l_...`

### cp-phase-geometric
- **Section:** 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons
- **Equation number:** (6.8)
- **LaTeX:** `\delta_{\text{CP}} = \pi \frac{\sum_i \text{orientation}_i}{b_3} = \pi \frac{12}{24} = \frac{\pi}{2}...`

### seesaw-mechanism
- **Section:** 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons
- **LaTeX:** `m_\nu = -Y_D^T M_R^{-1} Y_D \cdot v_{\text{EW}}^2...`

### attractor-potential
- **Section:** 7.4 The Attractor Scalar
- **Equation number:** (7.6)
- **LaTeX:** `V(\phi_M) = V_{\text{flux}} e^{-a\phi_M} + V_{\text{inst}} e^{-b/\phi_M} + V_{\text{axion}} \cos\lef...`

*... and 160 more matched formulas*

---

## 2. Paper Equations NOT in theory_output.json

These 634 equations appear in the paper but are MISSING from theory_output.json.
They should be added to ensure single source of truth.

### 1. Introduction (3 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\mathcal{N}=1
```

**Suggested formula ID:** `unnamed-108`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}/M_{\text{Pl}} \sim 10^{-3}
```

**Suggested formula ID:** `unnamed-109`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
w_0 \approx -0.85
```

**Suggested formula ID:** `unnamed-110`

### 2. The 26-Dimensional Bulk Spacetime (5 equations)

#### Equation None
- **Context:** Key Distinctions from Standard Approaches
- **Type:** inline
- **LaTeX:**
```latex
2^{13} = 8192
```

**Suggested formula ID:** `unnamed-113`

#### Equation None
- **Context:** Key Distinctions from Standard Approaches
- **Type:** inline
- **LaTeX:**
```latex
[L_m, L_n] = (m-n)L_{m+n} + \frac{c}{12}m(m^2-1)\delta_{m+n,0}
```

**Suggested formula ID:** `unnamed-114`

#### Equation None
- **Context:** Key Distinctions from Standard Approaches
- **Type:** inline
- **LaTeX:**
```latex
c_{\text{matter}} = D
```

**Suggested formula ID:** `unnamed-115`

#### Equation None
- **Context:** Key Distinctions from Standard Approaches
- **Type:** inline
- **LaTeX:**
```latex
c_{\text{ghost}} = -26
```

**Suggested formula ID:** `unnamed-116`

#### Equation None
- **Context:** Key Distinctions from Standard Approaches
- **Type:** inline
- **LaTeX:**
```latex
c_{\text{total}} = 0
```

**Suggested formula ID:** `unnamed-117`

### 2.4 The Master Action and Pneuma Field (8 equations)

#### Equation 2.3
- **Context:** Key Distinctions from Standard Approaches
- **Type:** display
- **LaTeX:**
```latex
S_{26D} = \int d^{26}X \sqrt{G} \left[ M^{24} R + \bar{\Psi}_P (i\Gamma^M D_M - m)\Psi_P + \mathcal{L}_{Sp(2,\mathbb{R})} \right]
```

**Suggested formula ID:** `eq-2-3`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\{\Gamma^M, \Gamma^N\} = 2\eta^{MN}
```

**Suggested formula ID:** `unnamed-121`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M,N = 0,...,25
```

**Suggested formula ID:** `unnamed-122`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
2^{26/2} = 2^{13} = 8192
```

**Suggested formula ID:** `unnamed-123`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\langle\bar{\Psi}_P\Psi_P\rangle
```

**Suggested formula ID:** `pneuma-vev-dynamics`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M^{24}R
```

**Suggested formula ID:** `unnamed-128`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\bar{\Psi}_P(i\Gamma D - m)\Psi_P
```

**Suggested formula ID:** `unnamed-129`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\mathcal{L}_{Sp(2,\mathbb{R})}
```

**Suggested formula ID:** `unnamed-130`

### 2.5 Pneuma Condensate as Source of Geometry (7 equations)

#### Equation 2.4
- **Type:** display
- **LaTeX:**
```latex
T_{MN}^{(\text{Pneuma})} = \frac{i}{4}\left[\bar{\Psi}_P\Gamma_{(M}D_{N)}\Psi_P - D_{(M}\bar{\Psi}_P\Gamma_{N)}\Psi_P\right] - g_{MN}\mathcal{L}_{\Psi}
```

**Suggested formula ID:** `pneuma-stress-energy`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\langle\bar{\Psi}_P\Psi_P\rangle
```

**Suggested formula ID:** `pneuma-vev-dynamics`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\langle\bar{\Psi}_P\Psi_P\rangle = v_P^3
```

**Suggested formula ID:** `pneuma-vev-dynamics`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
R_{MN} - \frac{1}{2}g_{MN}R = \frac{1}{M^{24}}T_{MN}^{(\text{Pneuma})}
```

**Suggested formula ID:** `pneuma-stress-energy`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Delta = \lambda v_P / (1 + g \cdot t_\perp / E_F)
```

**Suggested formula ID:** `unnamed-134`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Lambda_{\text{eff}} = \lambda v_P^4 / M^{24}
```

**Suggested formula ID:** `unnamed-135`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
T_c \sim
```

**Suggested formula ID:** `unnamed-136`

### 2.6 Holographic Entropy from Pneuma (6 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
S = A/(4G\hbar)
```

**Suggested formula ID:** `unnamed-137`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
A = 4\pi r_S^2
```

**Suggested formula ID:** `unnamed-138`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
r_S = 2GM
```

**Suggested formula ID:** `unnamed-139`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{cells}} = A / l_P^2
```

**Suggested formula ID:** `unnamed-140`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Omega = 2^{N_{\text{cells}}/4}
```

**Suggested formula ID:** `unnamed-141`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
S = \log\Omega = (A/4l_P^2) \log 2 \propto A
```

**Suggested formula ID:** `unnamed-142`

### 2.7 Pneuma Vacuum Selection: Racetrack Mechanism (18 equations)

#### Equation 2.8
- **Type:** display
- **LaTeX:**
```latex
\frac{\partial V}{\partial \Psi_P} = 0 \quad \Rightarrow \quad Aa \, e^{-a\Psi_P} = Bb \, e^{-b\Psi_P}
```

**Suggested formula ID:** `eq-2-8`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\langle\Psi_P\rangle \approx 1.08
```

**Suggested formula ID:** `pneuma-vev-dynamics`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{flux}} = 24
```

**Suggested formula ID:** `unnamed-144`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{flux}} + 1 = 25
```

**Suggested formula ID:** `unnamed-145`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_c
```

**Suggested formula ID:** `unnamed-146`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
a = 2\pi / N_{\text{flux}} = 2\pi / 24 \approx 0.262
```

**Suggested formula ID:** `unnamed-147`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
b = 2\pi / (N_{\text{flux}} + 1) = 2\pi / 25 \approx 0.251
```

**Suggested formula ID:** `unnamed-148`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
A, B
```

**Suggested formula ID:** `unnamed-149`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\mathcal{O}(1)
```

**Suggested formula ID:** `unnamed-150`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
a = 2\pi/24 = 0.2618
```

**Suggested formula ID:** `unnamed-153`

*... and 8 more equations in this section*

### 3. Reduction to the 13-Dimensional Shadow (21 equations)

#### Equation 3.1
- **Type:** display
- **LaTeX:**
```latex
[J_{ab}, J_{cd}] = i(\eta_{ac}J_{bd} + \eta_{bd}J_{ac} - \eta_{ad}J_{bc} - \eta_{bc}J_{ad})
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation 3.1a
- **Type:** display
- **LaTeX:**
```latex
X^2 = X^M \eta_{MN} X^N = 0 \quad \text{(null constraint)}
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation 3.1b
- **Type:** display
- **LaTeX:**
```latex
X \cdot P = X^M \eta_{MN} P^N = 0 \quad \text{(orthogonality constraint)}
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation 3.1c
- **Type:** display
- **LaTeX:**
```latex
P^2 = P^M \eta_{MN} P^N = M^2 \quad \text{(mass-shell constraint)}
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(X^M, P^M)
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M = 0, 1, \ldots, 25
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\eta_{MN} = \text{diag}(-1, -1, +1, \ldots, +1)
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
X^M
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
P^M
```

**Suggested formula ID:** `dimensional-reduction`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
P^2 = M^2
```

**Suggested formula ID:** `dimensional-reduction`

*... and 11 more equations in this section*

### 4. Compactification on the TCS G2 Manifold (64 equations)

#### Equation 4.1
- **Type:** display
- **LaTeX:**
```latex
b_2 = <span class="pm-value" data-pm-value="parameters.topology.b2"></span>, \quad b_3 = <span class="pm-value" data-pm-value="parameters.topology.b3"></span>, \quad \chi_{\text{eff}} = <span class="pm-value" data-pm-value="parameters.topology.CHI_EFF"></span>, \quad \nu = <span class="pm-value" data-pm-value="parameters.topology.NU"></span>
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 4.1a
- **Type:** display
- **LaTeX:**
```latex
\chi_{\text{eff}} = 2(h^{1,1} - h^{2,1} + h^{3,1}) = 2(<span class="pm-value" data-pm-value="parameters.topology.h11"></span> - 0 + <span class="pm-value" data-pm-value="parameters.topology.h31"></span>) = <span class="pm-value" data-pm-value="parameters.topology.CHI_EFF"></span>
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
E_{\text{condensate}} \sim -\frac{g^2}{\chi_{\text{eff}}}
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
n_{\text{gen}} = \frac{|\chi_{\text{eff}}|}{48} = 3 \quad \Rightarrow \quad \chi_{\text{eff}} \geq 144
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 4.2
- **Type:** display
- **LaTeX:**
```latex
n_{\text{gen}} = \frac{|\chi_{\text{eff}}|}{48} = \frac{144}{48} = 3
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
n_{\text{gen}} = \frac{N_{\text{flux}}}{\text{spinor}_{\text{DOF}}} = \frac{24}{8} = 3
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 4.4a
- **Type:** display
- **LaTeX:**
```latex
W_{\text{race}} = A e^{-a T} + B e^{-b T}
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 4.4b
- **Type:** display
- **LaTeX:**
```latex
M_{\text{Pl,eff}}^2 = \frac{1}{h^{1,1}} \sum_{i=1}^{4} w_i M_{\text{Pl,bulk}}^2 \approx \frac{1}{4} M_{\text{Pl,bulk}}^2
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 4.4c
- **Type:** display
- **LaTeX:**
```latex
v_{\text{EW}} = v_{\text{EW,0}} \times w_0 \approx v_{\text{EW,0}}
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 4.4d
- **Type:** display
- **LaTeX:**
```latex
\frac{M_{\text{Pl}}}{v_{\text{EW}}} \sim \frac{1}{\sqrt{h^{1,1}}} \times \frac{M_{\text{Pl,bulk}}}{v_{\text{EW,0}}} = 2 \times \frac{M_{\text{Pl,bulk}}}{v_{\text{EW,0}}} \sim 10^{16}
```

**Suggested formula ID:** `g2-manifold-property`

*... and 54 more equations in this section*

### 5. Gauge Unification and the Standard Model (76 equations)

#### Equation 5.3
- **Type:** display
- **LaTeX:**
```latex
M_{\text{GUT}} = M_{\text{Pl}} \times \left(\frac{\text{Vol}(G_2)}{\ell_P^7}\right)^{-1/2} \times e^{|T_\omega|} = <span class="pm-value" data-pm-value="parameters.gauge.M_GUT" data-format="scientific:2"></span> \text{ GeV}
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 5.3a
- **Type:** display
- **LaTeX:**
```latex
\text{SO}(10) \to \text{SU}(4)_C \times \text{SU}(2)_L \times \text{SU}(2)_R \to \text{SM}
```

**Suggested formula ID:** `eq-5-3a`

#### Equation 5.4a
- **Type:** display
- **LaTeX:**
```latex
\mathbf{10}_{\text{Higgs}} = (1,2)_{+1/2} \oplus (\bar{3},1)_{-2/3} \oplus (3,1)_{+2/3}
```

**Suggested formula ID:** `eq-5-4a`

#### Equation 5.4b
- **Type:** display
- **LaTeX:**
```latex
\mathcal{T}_{\text{shadow}}: \quad \mathbf{3}_C \to \text{shadow sector}, \quad \mathbf{2}_L \to \text{4D vacuum}
```

**Suggested formula ID:** `eq-5-4b`

#### Equation 5.5a
- **Type:** display
- **LaTeX:**
```latex
\alpha_{\text{em}}^{-1}(M_Z) = \frac{\alpha_2^{-1}(M_Z)}{\sin^2\theta_W(M_Z)} = \frac{29.6}{0.23121} = 127.9
```

**Suggested formula ID:** `eq-5-5a`

#### Equation 5.6
- **Type:** display
- **LaTeX:**
```latex
v_{\text{EW}} = M_{\text{Pl}} \times e^{-h^{2,1}/b_3} \times e^{|T_\omega|} = 173.97 \text{ GeV}
```

**Suggested formula ID:** `eq-5-6`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
V(\Psi_P) = |A e^{-2\pi/N_{\text{flux}}\Psi_P} - B e^{-2\pi/(N_{\text{flux}}+1)\Psi_P}|^2
```

**Suggested formula ID:** `unnamed-41`

#### Equation 5.6a
- **Type:** display
- **LaTeX:**
```latex
\lambda_0 = \frac{1}{4}\left(g_2^2 + \frac{3}{5}g_1^2\right) = \frac{1}{4}\left(\frac{4\pi\alpha_{\text{GUT}}}{1} + \frac{3}{5}\cdot\frac{4\pi\alpha_{\text{GUT}}}{1}\right) = 0.1289
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation 5.7
- **Type:** display
- **LaTeX:**
```latex
\mathbf{45}_{\text{SO}(10)} = \underbrace{(\mathbf{8},1)_0}_{\text{8 gluons}} + \underbrace{(1,\mathbf{3})_0}_{\text{3 weak}} + \underbrace{(1,1)_0}_{\text{1 hypercharge}} + \underbrace{(\mathbf{3},2)_{+5/6}}_{\text{6 X}} + \underbrace{(\bar{\mathbf{3}},2)_{-5/6}}_{\text{6 } \bar{X}} + \underbrace{(\mathbf{3},2)_{-1/6}}_{\text{6 Y}} + \underbrace{(\bar{\mathbf{3}},2)_{+1/6}}_{\text{6 } \bar{Y}} + \underbrace{\text{9 neutrals}}_{\text{heavy}}
```

**Suggested formula ID:** `eq-5-7`

#### Equation 5.8
- **Type:** display
- **LaTeX:**
```latex
\mathcal{O}_6 = \frac{g_{\text{GUT}}^2}{M_X^2} \epsilon^{abc} \epsilon^{ij} (u_a^c \gamma_\mu d_b)(Q_{ci} \gamma^\mu L_j)
```

**Suggested formula ID:** `eq-5-8`

*... and 66 more equations in this section*

### 5.8 Threshold Corrections (6 equations)

#### Equation 5.11
- **Type:** display
- **LaTeX:**
```latex
\Delta\left(\frac{1}{\alpha_i}\right) = \frac{k_i \cdot h^{1,1}}{2\pi} \log\left(\frac{M_*}{M_{\text{GUT}}}\right)
```

**Suggested formula ID:** `eq-5-11`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
h^{1,1} = 4
```

**Suggested formula ID:** `unnamed-336`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_* \sim 5
```

**Suggested formula ID:** `unnamed-337`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{string}} \sim 10^{17}
```

**Suggested formula ID:** `unnamed-338`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
k_3 = 3, k_2 = 2, k_1 = 1
```

**Suggested formula ID:** `unnamed-339`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Delta\sin^2\theta_W \approx +0.0002
```

**Suggested formula ID:** `unnamed-340`

### 6. Fermion Sector and Mixing Angles (92 equations)

#### Equation 6.1
- **Type:** display
- **LaTeX:**
```latex
\shadow_kuf = \shadow_chet \quad \Rightarrow \quad \theta_{23} = \frac{\pi}{4} = 45°
```

**Suggested formula ID:** `eq-6-1`

#### Equation 6.4
- **Type:** display
- **LaTeX:**
```latex
m_t = y_t 	imes rac{v_{	ext{EW}}}{\sqrt{2}} = 172.7 	ext{ GeV}
```

**Suggested formula ID:** `eq-6-4`

#### Equation 6.5
- **Type:** display
- **LaTeX:**
```latex
m_b = y_b \times \frac{v_{\text{EW}}}{\sqrt{2}} = 4.18 \text{ GeV}
```

**Suggested formula ID:** `eq-6-5`

#### Equation 6.6
- **Type:** display
- **LaTeX:**
```latex
m_\tau = y_\tau \times \frac{v_{\text{EW}}}{\sqrt{2}} = 1.777 \text{ GeV}
```

**Suggested formula ID:** `eq-6-6`

#### Equation 6.7
- **Type:** display
- **LaTeX:**
```latex
\alpha_s(M_Z) = \frac{\alpha_{\text{GUT}}}{1 + \frac{7\alpha_{\text{GUT}}}{2\pi}\ln\left(\frac{M_{\text{GUT}}}{M_Z}\right)} = 0.1179
```

**Suggested formula ID:** `eq-6-7`

#### Equation 6.3a
- **Type:** display
- **LaTeX:**
```latex
m_u = 2.2 \text{ MeV}, \quad m_c = 1.27 \text{ GeV}
```

**Suggested formula ID:** `eq-6-3a`

#### Equation 6.3b
- **Type:** display
- **LaTeX:**
```latex
m_d = 4.7 \text{ MeV}, \quad m_s = 95 \text{ MeV}
```

**Suggested formula ID:** `eq-6-3b`

#### Equation 6.8
- **Type:** display
- **LaTeX:**
```latex
m_e = 0.511 \text{ MeV}, \quad m_\mu = 105.66 \text{ MeV}
```

**Suggested formula ID:** `eq-6-8`

#### Equation 6.9
- **Type:** display
- **LaTeX:**
```latex
V_{\text{CKM}} = V_u^\dagger V_d
```

**Suggested formula ID:** `eq-6-9`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{23} = 45°
```

**Suggested formula ID:** `unnamed-341`

*... and 82 more equations in this section*

### 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons (48 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
Y_{ij} = Y_0 \int \psi_i^* \cdot \phi_H \cdot \psi_j \sim Y_0 \, e^{-\lambda(\Delta y_i^2 + \Delta y_j^2)/L^2}
```

**Suggested formula ID:** `unnamed-60`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\epsilon = e^{-\lambda \Delta y^2/L^2} \approx e^{-1.5} \approx 0.223
```

**Suggested formula ID:** `unnamed-61`

#### Equation 6.2
- **Type:** display
- **LaTeX:**
```latex
\Delta m^2_{21} = 7.97 \times 10^{-5} \text{ eV}^2 \quad (\text{exp: } 7.42 \times 10^{-5}, \text{ error: } 7.4\%)
```

**Suggested formula ID:** `eq-6-2`

#### Equation 6.3
- **Type:** display
- **LaTeX:**
```latex
\Delta m^2_{31} = 2.525 \times 10^{-3} \text{ eV}^2 \quad (\text{exp: } 2.515 \times 10^{-3}, \text{ error: } 0.4\%)
```

**Suggested formula ID:** `eq-6-3`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
m_s/m_\mu
```

**Suggested formula ID:** `unnamed-435`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
m_d/m_e = m_s/m_\mu = m_b/m_\tau = 1
```

**Suggested formula ID:** `unnamed-436`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
m_s/m_\mu = 1/3
```

**Suggested formula ID:** `unnamed-437`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-438`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
m_s \approx 95
```

**Suggested formula ID:** `unnamed-439`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
e^{-S_{\text{inst}}} \sim e^{-b_3/(4\pi)} \approx 0.15
```

**Suggested formula ID:** `unnamed-442`

*... and 38 more equations in this section*

### 7. Cosmology and Dark Energy (29 equations)

#### Equation 7.1
- **Type:** display
- **LaTeX:**
```latex
d_{\text{eff}} = 12 + \gamma(\shadow_kuf + \shadow_chet) = 12 + 0.5(1.152) = <span class="pm-value" data-pm-value="parameters.dark_energy.d_eff" data-format="fixed:3"></span>
```

**Suggested formula ID:** `eq-7-1`

#### Equation 7.2
- **Type:** display
- **LaTeX:**
```latex
w_0 = -\frac{d_{\text{eff}} - 1}{d_{\text{eff}} + 1} = -\frac{11.576}{13.576} = -0.8528
```

**Suggested formula ID:** `eq-7-2`

#### Equation 7.3
- **Type:** display
- **LaTeX:**
```latex
w(z) = w_0 \left[1 + \frac{\alpha_T}{3}\ln(1+z)\right]
```

**Suggested formula ID:** `eq-7-3`

#### Equation 7.4
- **Type:** display
- **LaTeX:**
```latex
w_a = -rac{lpha_T}{3} 	imes rac{w_0 + 1}{1 - w_0} = -0.75
```

**Suggested formula ID:** `eq-7-4`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\gamma = 0.5
```

**Suggested formula ID:** `unnamed-487`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
c_{\text{matter}} = 26
```

**Suggested formula ID:** `unnamed-488`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
c_{\text{ghost}} = -26
```

**Suggested formula ID:** `unnamed-489`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\gamma = \frac{|c_{\text{ghost}}|}{2 c_{\text{matter}}} = \frac{26}{52} = 0.5
```

**Suggested formula ID:** `unnamed-490`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\shadow_kuf + \shadow_chet = 1.152
```

**Suggested formula ID:** `unnamed-491`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
d_{\text{eff}} = 12 + 0.5 \times 1.152 = <span class="pm-value" data-pm-value="parameters.dark_energy.d_eff" data-format="fixed:3"></span>
```

**Suggested formula ID:** `unnamed-492`

*... and 19 more equations in this section*

### 7.4 The Attractor Scalar (15 equations)

#### Equation 7.5
- **Type:** display
- **LaTeX:**
```latex
\phi_M = \log(\text{Vol}_7)
```

**Suggested formula ID:** `eq-7-5`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
a = \sqrt{\chi_{\text{eff}}/6} = \sqrt{144/6} = \sqrt{24} \approx 4.9
```

**Suggested formula ID:** `unnamed-520`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
b = b_3 = 24
```

**Suggested formula ID:** `unnamed-522`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
f = 12
```

**Suggested formula ID:** `unnamed-523`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
V(\phi_M) = V_0[1 + A\cos(\omega\phi_M/f)]
```

**Suggested formula ID:** `unnamed-524`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\ddot{\phi}_M + 3H\dot{\phi}_M + V'(\phi_M) = 0
```

**Suggested formula ID:** `unnamed-525`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\epsilon = \frac{1}{2}\left(\frac{V'}{V}\right)^2 \ll 1
```

**Suggested formula ID:** `unnamed-526`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\dot{\phi}_M \to 0
```

**Suggested formula ID:** `unnamed-527`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
w = \frac{\dot{\phi}^2/2 - V}{\dot{\phi}^2/2 + V} \to -1
```

**Suggested formula ID:** `unnamed-528`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Lambda
```

**Suggested formula ID:** `unnamed-530`

*... and 5 more equations in this section*

### 7.5 The Thermal Time Hypothesis (24 equations)

#### Equation 7.9
- **Type:** display
- **LaTeX:**
```latex
\alpha_T = \frac{d(\ln \tau)}{d(\ln a)} - \frac{d(\ln H)}{d(\ln a)}
```

**Suggested formula ID:** `eq-7-9`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
K = -\log(\rho)
```

**Suggested formula ID:** `unnamed-538`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\rho = e^{-\beta H}/Z
```

**Suggested formula ID:** `unnamed-539`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
K = -\log(\rho) = \beta H + \log Z
```

**Suggested formula ID:** `unnamed-540`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\sigma_t(A) = e^{iKt} A e^{-iKt}
```

**Suggested formula ID:** `unnamed-541`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\text{Tr}(\rho \sigma_t(A) B) = \text{Tr}(\rho B \sigma_{t+i\beta}(A))
```

**Suggested formula ID:** `unnamed-542`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\sigma_t = \Delta^{it}(\cdot)\Delta^{-it}
```

**Suggested formula ID:** `unnamed-547`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\beta = 1
```

**Suggested formula ID:** `unnamed-548`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
t = \alpha_T \cdot S
```

**Suggested formula ID:** `unnamed-549`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
S = -\text{Tr}(\rho \log \rho) = \langle K \rangle
```

**Suggested formula ID:** `unnamed-550`

*... and 14 more equations in this section*

### 8. Predictions and Testability (20 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}}
```

**Suggested formula ID:** `unnamed-571`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-575`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{12}
```

**Suggested formula ID:** `unnamed-579`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{13}
```

**Suggested formula ID:** `unnamed-580`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\delta_{CP}
```

**Suggested formula ID:** `unnamed-581`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
m_1 = <span class="pm-value" data-pm-value="simulations.kk_graviton.m_KK_TeV" data-format="fixed:1"></span>
```

**Suggested formula ID:** `unnamed-585`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tau_p = <span class="pm-value" data-pm-value="simulations.proton_decay.tau_p_years" data-format="scientific:2"></span>
```

**Suggested formula ID:** `unnamed-586`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(p\to e^+\pi^0)
```

**Suggested formula ID:** `unnamed-587`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\eta \approx 0.113
```

**Suggested formula ID:** `unnamed-588`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
w(z)
```

**Suggested formula ID:** `unnamed-589`

*... and 10 more equations in this section*

### 8.3 Hidden Sector Particles (13 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\gamma'
```

**Suggested formula ID:** `unnamed-601`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\epsilon \sim 10^{-4}
```

**Suggested formula ID:** `unnamed-603`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\sim 1-10
```

**Suggested formula ID:** `unnamed-605`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
g' \sim g_Z \cdot 10^{-2}
```

**Suggested formula ID:** `unnamed-606`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
f_a \sim 10^{12}
```

**Suggested formula ID:** `unnamed-608`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
g_{a\gamma\gamma} \sim \alpha/(2\pi f_a)
```

**Suggested formula ID:** `unnamed-609`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\sim 100
```

**Suggested formula ID:** `unnamed-610`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\chi_0
```

**Suggested formula ID:** `unnamed-611`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tilde{\Sigma}_1
```

**Suggested formula ID:** `unnamed-612`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
m_{\chi_0} \sim v_{\text{shadow}} / \sqrt{2} \approx 100-500
```

**Suggested formula ID:** `unnamed-614`

*... and 3 more equations in this section*

### 9. Discussion and Transparency (19 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
M_{\text{SUSY}} \gtrsim M_{\text{GUT}} \approx 2.1 \times 10^{16}~\text{GeV} \gg M_{\text{LHC}} \sim 10^4~\text{GeV}
```

**Suggested formula ID:** `unnamed-74`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{13}
```

**Suggested formula ID:** `unnamed-620`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\delta_{CP}
```

**Suggested formula ID:** `unnamed-621`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(T) = 7.086
```

**Suggested formula ID:** `unnamed-623`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
10^{500}
```

**Suggested formula ID:** `unnamed-626`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}} = 3
```

**Suggested formula ID:** `unnamed-627`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_s \approx 1 - 2/N_e = 0.967
```

**Suggested formula ID:** `unnamed-630`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_e = 60
```

**Suggested formula ID:** `unnamed-631`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
0.965 \pm 0.004
```

**Suggested formula ID:** `unnamed-632`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
r \sim 0.003
```

**Suggested formula ID:** `unnamed-633`

*... and 9 more equations in this section*

### Appendix A: Virasoro Anomaly Cancellation (3 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
c_{\text{matter}} = D, \quad c_{\text{ghost}} = -26, \quad c_{\text{total}} = D - 26 = 0
```

**Suggested formula ID:** `virasoro-constraint`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
D_{\text{total}} = D_{\text{space}} + D_{\text{time}} = 24 + 2 = 26 \quad \Rightarrow \quad c_{\text{total}} = 0
```

**Suggested formula ID:** `virasoro-constraint`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\text{26D}_{(24,2)} \xrightarrow{\text{Sp}(2,\mathbb{R})} \text{13D}_{(12,1)} \xrightarrow{\text{gauge fixing}} \text{Effective 4D}_{(3,1)}
```

**Suggested formula ID:** `virasoro-constraint`

### Appendix B: Generation Number Derivation (11 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
n_{\text{gen}} = \frac{|\chi_{\text{eff}}|}{24 \times Z_2} = \frac{144}{24 \times 2} = \frac{144}{48} = 3
```

**Suggested formula ID:** `unnamed-78`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}} = 3
```

**Suggested formula ID:** `unnamed-647`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Psi_L(t_{\text{therm}}) \sim \Psi_R(t_{\text{ortho}})
```

**Suggested formula ID:** `unnamed-648`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Sigma_i
```

**Suggested formula ID:** `unnamed-649`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tilde{\Sigma}_i
```

**Suggested formula ID:** `unnamed-650`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
Z_2: (t_{\text{therm}}, t_{\text{ortho}}) \to (t_{\text{therm}}, -t_{\text{ortho}})
```

**Suggested formula ID:** `unnamed-651`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\Sigma_i
```

**Suggested formula ID:** `unnamed-652`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\leftrightarrow
```

**Suggested formula ID:** `unnamed-653`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tilde{\Sigma}_i
```

**Suggested formula ID:** `unnamed-654`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tilde{\Sigma}_1
```

**Suggested formula ID:** `unnamed-656`

*... and 1 more equations in this section*

### Appendix C: Atmospheric Mixing Angle Derivation (2 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
G_2 \supset SU(3), \quad \mathbf{7} = \mathbf{3} + \bar{\mathbf{3}} + \mathbf{1} \quad \Rightarrow \quad \shadow_kuf = \shadow_chet
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{23} = 45°
```

**Suggested formula ID:** `unnamed-659`

### Appendix D: Dark Energy Equation of State (4 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\gamma = \frac{|c_{\text{ghost}}|}{2 c_{\text{matter}}} = \frac{26}{2 \times 26} = \frac{26}{52} = 0.5
```

**Suggested formula ID:** `unnamed-80`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
d_{\text{eff}} = 12 + \gamma(\shadow_kuf + \shadow_chet) = 12 + 0.5(0.576152 + 0.576152) = <span class="pm-value" data-pm-value="parameters.dark_energy.d_eff" data-format="fixed:3"></span>
```

**Suggested formula ID:** `unnamed-81`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
w_0 = -\frac{d_{\text{eff}} - 1}{d_{\text{eff}} + 1} = -\frac{11.576}{13.576} = -0.8528
```

**Suggested formula ID:** `unnamed-82`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
w_0 = -0.8528
```

**Suggested formula ID:** `unnamed-660`

### Appendix E: Proton Decay Calculation (25 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
M_{\text{GUT}} = M_{\text{GUT,base}} \times \left(1 + \frac{3}{22 - \nu/12} \times s\right) = <span class="pm-value" data-pm-value="parameters.gauge.M_GUT" data-format="scientific:2"></span> \text{ GeV}
```

**Suggested formula ID:** `unnamed-83`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\tau_p = C \times \left(\frac{M_{\text{GUT}}}{10^{16} \text{ GeV}}\right)^4 \times \left(\frac{0.03}{\alpha_{\text{GUT}}}\right)^2 \times S
```

**Suggested formula ID:** `unnamed-84`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\tau_p = <span class="pm-value" data-pm-value="simulations.proton_decay.tau_p_years" data-format="scientific:2"></span> \text{ years}
```

**Suggested formula ID:** `unnamed-85`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
M_{\text{GUT}} = M_{\text{Pl}} \exp\left(-\frac{\kappa \cdot 2\pi}{g_{\text{GUT}}^2}\right) = M_{\text{Pl}} \exp\left(-\frac{1.46 \times 2\pi}{0.0425}\right) = 2.12 \times 10^{16} \text{ GeV}
```

**Suggested formula ID:** `unnamed-87`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-661`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
s = (\ln(M_{\text{Pl}}/M_{\text{GUT,base}}) - T_\omega) / (2\pi/(\nu/b_3))
```

**Suggested formula ID:** `unnamed-662`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
C = 3.82 \times 10^{33}
```

**Suggested formula ID:** `unnamed-663`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
S = \exp(2\pi d/R) \approx <span class="pm-value" data-pm-value="simulations.proton_decay.suppression_factor" data-format="fixed:1"></span>
```

**Suggested formula ID:** `unnamed-664`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
d/R = \ln(K)/2\pi = \ln(4)/2\pi \approx 0.12
```

**Suggested formula ID:** `unnamed-665`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
S = e^{2\pi \times 0.12} = e^{0.754} = <span class="pm-value" data-pm-value="simulations.proton_decay.suppression_factor" data-format="fixed:3"></span>
```

**Suggested formula ID:** `unnamed-666`

*... and 15 more equations in this section*

### Appendix F: Dimensional Decomposition (4 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\mathcal{M}^{26} = \mathcal{M}^4 \times T^{15} \times G_2^7
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\mathcal{M}^4
```

**Suggested formula ID:** `unnamed-684`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
T^{15}
```

**Suggested formula ID:** `unnamed-685`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
G_2^7
```

**Suggested formula ID:** `g2-manifold-property`

### Appendix G: Effective Torsion from Flux Quantization (7 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
T_{\omega} = -\frac{b_3}{N_{\text{flux}}} = -\frac{24}{24} = -1.000
```

**Suggested formula ID:** `unnamed-90`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tau = 0
```

**Suggested formula ID:** `unnamed-687`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\chi_{\text{eff}} = 6 N_{\text{flux}}
```

**Suggested formula ID:** `unnamed-688`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{flux}} = \chi_{\text{eff}}/6 = 24
```

**Suggested formula ID:** `unnamed-689`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
T_\omega = -1.000 \times (7/8) = -0.875
```

**Suggested formula ID:** `unnamed-692`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
-0.884
```

**Suggested formula ID:** `unnamed-693`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\eta = e^{|T_\omega|}/b_3 = e^{0.875}/24 \approx 0.100
```

**Suggested formula ID:** `unnamed-694`

### Appendix H: Proton Decay Branching Ratio (1 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
b_3/2 = 24/2 = 12
```

**Suggested formula ID:** `unnamed-697`

### Appendix I: Gravitational Wave Dispersion (18 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\eta = \frac{e^{|T_\omega|}}{b_3} = \frac{e^{1.0}}{24} \approx 0.113
```

**Suggested formula ID:** `unnamed-93`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
T_{\omega}^{\text{(alt)}} = -\frac{b_3}{C} = -\frac{24}{27.2} = -0.882
```

**Suggested formula ID:** `unnamed-94`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tau \equiv t_{\text{ortho}}
```

**Suggested formula ID:** `unnamed-698`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\langle X \cdot P \rangle = 0
```

**Suggested formula ID:** `unnamed-699`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GW}} \sim M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-700`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
ds^2 = -dt_{\text{therm}}^2 - d\tau^2 + dx_i^2
```

**Suggested formula ID:** `unnamed-707`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{flux}} = \chi_{\text{eff}}/6 = 144/6 = 24
```

**Suggested formula ID:** `unnamed-708`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
T_\omega = -b_3/N_{\text{flux}} = -24/24 = -1.000
```

**Suggested formula ID:** `unnamed-710`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\langle \delta\tau^2 \rangle \sim e^{|T_\omega|}/b_3
```

**Suggested formula ID:** `unnamed-712`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\eta = e^{|T_\omega|}/b_3 = e^{1.0}/24 \approx 0.113
```

**Suggested formula ID:** `unnamed-713`

*... and 8 more equations in this section*

### Appendix J: Monte Carlo Error Propagation (3 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}}
```

**Suggested formula ID:** `unnamed-730`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-735`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\delta_{CP}
```

**Suggested formula ID:** `unnamed-736`

### Appendix K: Transparency Statement (18 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-738`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}}
```

**Suggested formula ID:** `unnamed-740`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
D=26
```

**Suggested formula ID:** `unnamed-745`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{12}
```

**Suggested formula ID:** `unnamed-746`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{13}
```

**Suggested formula ID:** `unnamed-748`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\delta_{CP}
```

**Suggested formula ID:** `unnamed-749`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(T)
```

**Suggested formula ID:** `unnamed-750`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{13}
```

**Suggested formula ID:** `unnamed-752`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\delta_{CP}
```

**Suggested formula ID:** `unnamed-753`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(T)
```

**Suggested formula ID:** `unnamed-755`

*... and 8 more equations in this section*

### Appendix L: Complete PM Values Summary (26 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
D_{\text{bulk}}
```

**Suggested formula ID:** `unnamed-769`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
c = D - 26 = 0
```

**Suggested formula ID:** `unnamed-770`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
D_{\text{shadow}}
```

**Suggested formula ID:** `unnamed-771`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(24,2) \to (12,1)
```

**Suggested formula ID:** `unnamed-772`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
D_{G_2}
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
H^2(X,\mathbb{Z})
```

**Suggested formula ID:** `unnamed-776`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}}
```

**Suggested formula ID:** `unnamed-779`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
|\chi_{\text{eff}}|/48
```

**Suggested formula ID:** `unnamed-780`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
M_{\text{GUT}}
```

**Suggested formula ID:** `unnamed-781`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(2.0 \pm 0.3) \times 10^{16}
```

**Suggested formula ID:** `unnamed-783`

*... and 16 more equations in this section*

### Appendix M: Speculative Extensions - Consciousness and the Pneuma Vacuum (15 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
\tau = \frac{\hbar}{E_G} \quad \text{where} \quad E_G \approx \frac{G m_{\text{total}}^2}{r}
```

**Suggested formula ID:** `unnamed-95`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
f_{\text{eff}} = f_0 \times \exp\left(-\frac{(\phi - \phi_0)^2}{2\sigma^2}\right)
```

**Suggested formula ID:** `unnamed-96`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\sim 10^{16}
```

**Suggested formula ID:** `unnamed-814`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
E_G \approx \hbar/\tau
```

**Suggested formula ID:** `unnamed-815`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tau \approx 500
```

**Suggested formula ID:** `unnamed-816`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N \approx 10^{16}
```

**Suggested formula ID:** `unnamed-817`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
r \approx 1
```

**Suggested formula ID:** `unnamed-818`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\tau \approx 500
```

**Suggested formula ID:** `unnamed-819`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
E_G
```

**Suggested formula ID:** `unnamed-820`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\phi_0 = 0.5
```

**Suggested formula ID:** `unnamed-822`

*... and 5 more equations in this section*

### Appendix N: G₂ Topology Landscape (10 equations)

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}} = 3
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
h^{1,1} \in [4, 52]
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
h^{3,1} \in [20, 100]
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
h^{2,1} = 0
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}} = 3
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{flux}} \leq 50
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
h^{1,1} + h^{3,1} = 72
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
N_{\text{flux}} = 24
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
h^{1,1} = 4
```

**Suggested formula ID:** `g2-manifold-property`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}}
```

**Suggested formula ID:** `g2-manifold-property`

### Unknown Section (13 equations)

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
', '
```

**Suggested formula ID:** `unnamed-1`

#### Equation None
- **Type:** display
- **LaTeX:**
```latex
', '\
```

**Suggested formula ID:** `unnamed-97`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
', '
```

**Suggested formula ID:** `unnamed-98`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
b_2=4
```

**Suggested formula ID:** `unnamed-99`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
b_3=24
```

**Suggested formula ID:** `unnamed-100`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
n_{\text{gen}} = |\chi_{\text{eff}}|/48 = 144/48 = 3
```

**Suggested formula ID:** `unnamed-101`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{23} = 45°
```

**Suggested formula ID:** `unnamed-102`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
(p\to e^+\pi^0) = 0.25
```

**Suggested formula ID:** `unnamed-103`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\eta \approx 0.113
```

**Suggested formula ID:** `unnamed-104`

#### Equation None
- **Type:** inline
- **LaTeX:**
```latex
\theta_{13}
```

**Suggested formula ID:** `unnamed-105`

*... and 3 more equations in this section*

---

## 3. Theory Formulas NOT Referenced in Paper

These 16 formulas exist in theory_output.json but are not found in the paper:

### generation-number
- **Description:** Number of fermion generations from G₂ topology
- **LaTeX:** `n_{gen} = \frac{\chi_{eff}}{48} = \frac{144}{48} = 3...`

### kk-graviton-mass
- **Description:** First KK graviton mode mass from compactification radius
- **LaTeX:** `m_{KK,1} = \frac{1}{R_c} = 5.0\,\text{TeV}...`

### division-algebra
- **Description:** 13D as unique combination of division algebra dimensions
- **LaTeX:** `D = 13 = 1(\mathbb{R}) + 4(\mathbb{H}) + 8(\mathbb{O})...`

### dirac-pneuma
- **Description:** Dirac equation for Pneuma spinor field
- **LaTeX:** `(i\Gamma^M D_M - m)\Psi_P = 0...`

### effective-torsion
- **Description:** Effective torsion from topology
- **LaTeX:** `T_{\omega,\text{eff}} = -\frac{b_3}{N_{\text{flux}}} = -\frac{24}{24} = -1.0...`

### planck-mass-derivation
- **Description:** 4D Planck mass from 13D fundamental scale and internal volume
- **LaTeX:** `M_{Pl}^2 = M_*^{11} \times V_9 / 16\pi G_N...`

### higgs-vev
- **Description:** Electroweak VEV from geometric moduli
- **LaTeX:** `v_{\text{EW}} = M_{\text{Pl}} \times e^{-h^{2,1}/b_3} \times e^{|T_\omega|} = 173.97\,\text{GeV}...`

### neutrino-mass-31
- **Description:** Atmospheric neutrino mass splitting
- **LaTeX:** `\Delta m^2_{31} = 2.525 \times 10^{-3}\,\text{eV}^2...`

### kms-condition
- **Description:** Kubo-Martin-Schwinger condition for thermal equilibrium
- **LaTeX:** `\langle A(t + i\beta)B \rangle = \langle BA(t) \rangle \, \text{with} \, \beta = \frac{1}{k_B T}...`

### ghost-coefficient
- **Description:** Ghost coefficient from Virasoro anomaly structure
- **LaTeX:** `\gamma = \frac{|c_{\text{ghost}}|}{2 c_{\text{matter}}} = \frac{26}{2 \times 26} = 0.5...`

### gw-dispersion-alt
- **Description:** Alternative GW dispersion with phenomenological normalization
- **LaTeX:** `\eta^{\text{alt}} = \frac{e^{0.882}}{24} \approx 0.101...`

### vacuum-minimization
- **Description:** Vacuum stability condition for racetrack potential minimum
- **LaTeX:** `\frac{\partial V}{\partial \Psi_P} = 0 \quad \Rightarrow \quad Aa \, e^{-a\langle\Psi_P\rangle} = Bb...`

### mirror-temp-ratio
- **Description:** Mirror sector temperature ratio from G₂ topology
- **LaTeX:** `\frac{T'}{T} = 0.57 = \left(\frac{b_2}{b_3}\right)^{1/4}...`

### pati-salam-chain
- **Description:** Intermediate Pati-Salam symmetry breaking chain (geometrically preferred)
- **LaTeX:** `\text{SO}(10) \to \text{SU}(4)_C \times \text{SU}(2)_L \times \text{SU}(2)_R \to \text{SU}(3)_C \tim...`

### higgs-potential
- **Description:** Standard Model Higgs potential from EWSB
- **LaTeX:** `V(H) = -\mu^2 |H|^2 + \lambda |H|^4...`

### rg-running-couplings
- **Description:** One-loop RG evolution equations for SM gauge couplings
- **LaTeX:** `\frac{d\alpha_i^{-1}}{d\ln(\mu)} = -\frac{b_i}{2\pi}, \quad b = \left(\frac{41}{10}, -\frac{19}{6}, ...`

---

## 4. Equation Distribution by Section

| Section | Display Equations | Inline Equations | Total |
|---------|-------------------|------------------|-------|
| 1. Introduction | 1 | 3 | 4 |
| 2. The 26-Dimensional Bulk Spacetime | 2 | 7 | 9 |
| 2.4 The Master Action and Pneuma Field | 1 | 11 | 12 |
| 2.5 Pneuma Condensate as Source of Geometry | 1 | 6 | 7 |
| 2.6 Holographic Entropy from Pneuma | 1 | 6 | 7 |
| 2.7 Pneuma Vacuum Selection: Racetrack Mechanism | 4 | 18 | 22 |
| 3. Reduction to the 13-Dimensional Shadow | 5 | 21 | 26 |
| 3.3 Hidden Variables from Shadow Branes | 1 | 2 | 3 |
| 4. Compactification on the TCS G2 Manifold | 13 | 68 | 81 |
| 5. Gauge Unification and the Standard Model | 16 | 79 | 95 |
| 5.8 Threshold Corrections | 1 | 5 | 6 |
| 6. Fermion Sector and Mixing Angles | 10 | 88 | 98 |
| 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons | 7 | 49 | 56 |
| 7. Cosmology and Dark Energy | 4 | 28 | 32 |
| 7.4 The Attractor Scalar | 2 | 17 | 19 |
| 7.5 The Thermal Time Hypothesis | 3 | 31 | 34 |
| 8. Predictions and Testability | 0 | 29 | 29 |
| 8.3 Hidden Sector Particles | 0 | 14 | 14 |
| 9. Discussion and Transparency | 1 | 25 | 26 |
| Appendix A: Virasoro Anomaly Cancellation | 3 | 2 | 5 |
| Appendix B: Generation Number Derivation | 1 | 12 | 13 |
| Appendix C: Atmospheric Mixing Angle Derivation | 1 | 1 | 2 |
| Appendix D: Dark Energy Equation of State | 3 | 1 | 4 |
| Appendix E: Proton Decay Calculation | 5 | 23 | 28 |
| Appendix F: Dimensional Decomposition | 1 | 3 | 4 |
| Appendix G: Effective Torsion from Flux Quantization | 2 | 8 | 10 |
| Appendix H: Proton Decay Branching Ratio | 1 | 3 | 4 |
| Appendix I: Gravitational Wave Dispersion | 3 | 29 | 32 |
| Appendix J: Monte Carlo Error Propagation | 0 | 8 | 8 |
| Appendix K: Transparency Statement | 0 | 31 | 31 |
| Appendix L: Complete PM Values Summary | 0 | 44 | 44 |
| Appendix M: Speculative Extensions - Consciousness and the Pneuma Vacuum | 2 | 15 | 17 |
| Appendix N: G₂ Topology Landscape | 0 | 19 | 19 |
| Unknown Section | 2 | 11 | 13 |

---

## 5. Recommendations

### Priority 1: Add Missing Core Equations
The following numbered equations in Sections 1-6 should be added to theory_output.json:

- **(2.3)** 2.4 The Master Action and Pneuma Field
  - Suggested ID: `eq-2-3`
  - LaTeX: `S_{26D} = \int d^{26}X \sqrt{G} \left[ M^{24} R + \bar{\Psi}_P (i\Gamma^M D_M - ...`

- **(2.4)** 2.5 Pneuma Condensate as Source of Geometry
  - Suggested ID: `pneuma-stress-energy`
  - LaTeX: `T_{MN}^{(\text{Pneuma})} = \frac{i}{4}\left[\bar{\Psi}_P\Gamma_{(M}D_{N)}\Psi_P ...`

- **(2.8)** 2.7 Pneuma Vacuum Selection: Racetrack Mechanism
  - Suggested ID: `eq-2-8`
  - LaTeX: `\frac{\partial V}{\partial \Psi_P} = 0 \quad \Rightarrow \quad Aa \, e^{-a\Psi_P...`

- **(3.1)** 3. Reduction to the 13-Dimensional Shadow
  - Suggested ID: `dimensional-reduction`
  - LaTeX: `[J_{ab}, J_{cd}] = i(\eta_{ac}J_{bd} + \eta_{bd}J_{ac} - \eta_{ad}J_{bc} - \eta_...`

- **(3.1a)** 3. Reduction to the 13-Dimensional Shadow
  - Suggested ID: `dimensional-reduction`
  - LaTeX: `X^2 = X^M \eta_{MN} X^N = 0 \quad \text{(null constraint)}...`

- **(3.1b)** 3. Reduction to the 13-Dimensional Shadow
  - Suggested ID: `dimensional-reduction`
  - LaTeX: `X \cdot P = X^M \eta_{MN} P^N = 0 \quad \text{(orthogonality constraint)}...`

- **(3.1c)** 3. Reduction to the 13-Dimensional Shadow
  - Suggested ID: `dimensional-reduction`
  - LaTeX: `P^2 = P^M \eta_{MN} P^N = M^2 \quad \text{(mass-shell constraint)}...`

- **(4.1)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `b_2 = <span class="pm-value" data-pm-value="parameters.topology.b2"></span>, \qu...`

- **(4.1a)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `\chi_{\text{eff}} = 2(h^{1,1} - h^{2,1} + h^{3,1}) = 2(<span class="pm-value" da...`

- **(4.2)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `n_{\text{gen}} = \frac{|\chi_{\text{eff}}|}{48} = \frac{144}{48} = 3...`

- **(4.4a)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `W_{\text{race}} = A e^{-a T} + B e^{-b T}...`

- **(4.4b)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `M_{\text{Pl,eff}}^2 = \frac{1}{h^{1,1}} \sum_{i=1}^{4} w_i M_{\text{Pl,bulk}}^2 ...`

- **(4.4c)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `v_{\text{EW}} = v_{\text{EW,0}} \times w_0 \approx v_{\text{EW,0}}...`

- **(4.4d)** 4. Compactification on the TCS G2 Manifold
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `\frac{M_{\text{Pl}}}{v_{\text{EW}}} \sim \frac{1}{\sqrt{h^{1,1}}} \times \frac{M...`

- **(5.3)** 5. Gauge Unification and the Standard Model
  - Suggested ID: `g2-manifold-property`
  - LaTeX: `M_{\text{GUT}} = M_{\text{Pl}} \times \left(\frac{\text{Vol}(G_2)}{\ell_P^7}\rig...`

### Priority 2: Verify Theory-Only Formulas
Consider whether these theory formulas should appear in the paper:

- `generation-number`: Number of fermion generations from G₂ topology
- `kk-graviton-mass`: First KK graviton mode mass from compactification radius
- `division-algebra`: 13D as unique combination of division algebra dimensions
- `dirac-pneuma`: Dirac equation for Pneuma spinor field
- `effective-torsion`: Effective torsion from topology
- `planck-mass-derivation`: 4D Planck mass from 13D fundamental scale and internal volume
- `higgs-vev`: Electroweak VEV from geometric moduli
- `neutrino-mass-31`: Atmospheric neutrino mass splitting
- `kms-condition`: Kubo-Martin-Schwinger condition for thermal equilibrium
- `ghost-coefficient`: Ghost coefficient from Virasoro anomaly structure

### Priority 3: Inline Math Consolidation
There are 717 inline math expressions.
Review whether frequently-used expressions should be promoted to named formulas.

---

## Appendix: Full Paper Equation List

Complete list of all 814 equations extracted from the paper:

1. **Unknown Section** - unnumbered - display
2. **1. Introduction** - (1.1) - display
3. **2. The 26-Dimensional Bulk Spacetime** - (2.1) - display
4. **2. The 26-Dimensional Bulk Spacetime** - (2.2) - display
5. **2.4 The Master Action and Pneuma Field** - (2.3) - display
6. **2.5 Pneuma Condensate as Source of Geometry** - (2.4) - display
7. **2.6 Holographic Entropy from Pneuma** - (2.5) - display
8. **2.7 Pneuma Vacuum Selection: Racetrack Mechanism** - (2.6) - display
9. **2.7 Pneuma Vacuum Selection: Racetrack Mechanism** - (2.7) - display
10. **2.7 Pneuma Vacuum Selection: Racetrack Mechanism** - (2.8) - display
11. **2.7 Pneuma Vacuum Selection: Racetrack Mechanism** - (2.9) - display
12. **3. Reduction to the 13-Dimensional Shadow** - (3.1) - display
13. **3. Reduction to the 13-Dimensional Shadow** - (3.1a) - display
14. **3. Reduction to the 13-Dimensional Shadow** - (3.1b) - display
15. **3. Reduction to the 13-Dimensional Shadow** - (3.1c) - display
16. **3. Reduction to the 13-Dimensional Shadow** - (3.2) - display
17. **3.3 Hidden Variables from Shadow Branes** - (3.3) - display
18. **4. Compactification on the TCS G2 Manifold** - (4.1) - display
19. **4. Compactification on the TCS G2 Manifold** - (4.1a) - display
20. **4. Compactification on the TCS G2 Manifold** - unnumbered - display
21. **4. Compactification on the TCS G2 Manifold** - unnumbered - display
22. **4. Compactification on the TCS G2 Manifold** - (4.2) - display
23. **4. Compactification on the TCS G2 Manifold** - unnumbered - display
24. **4. Compactification on the TCS G2 Manifold** - (4.3) - display
25. **4. Compactification on the TCS G2 Manifold** - (4.4a) - display
26. **4. Compactification on the TCS G2 Manifold** - (4.4b) - display
27. **4. Compactification on the TCS G2 Manifold** - (4.4c) - display
28. **4. Compactification on the TCS G2 Manifold** - (4.4d) - display
29. **4. Compactification on the TCS G2 Manifold** - unnumbered - display
30. **4. Compactification on the TCS G2 Manifold** - unnumbered - display
31. **5. Gauge Unification and the Standard Model** - (5.1) - display
32. **5. Gauge Unification and the Standard Model** - (5.2) - display
33. **5. Gauge Unification and the Standard Model** - (5.3) - display
34. **5. Gauge Unification and the Standard Model** - (5.3a) - display
35. **5. Gauge Unification and the Standard Model** - (5.4a) - display
36. **5. Gauge Unification and the Standard Model** - (5.4b) - display
37. **5. Gauge Unification and the Standard Model** - (5.4c) - display
38. **5. Gauge Unification and the Standard Model** - (5.5) - display
39. **5. Gauge Unification and the Standard Model** - (5.5a) - display
40. **5. Gauge Unification and the Standard Model** - (5.6) - display
41. **5. Gauge Unification and the Standard Model** - unnumbered - display
42. **5. Gauge Unification and the Standard Model** - (5.6a) - display
43. **5. Gauge Unification and the Standard Model** - (5.7) - display
44. **5. Gauge Unification and the Standard Model** - (5.8) - display
45. **5. Gauge Unification and the Standard Model** - (5.9) - display
46. **5. Gauge Unification and the Standard Model** - (5.10) - display
47. **5.8 Threshold Corrections** - (5.11) - display
48. **6. Fermion Sector and Mixing Angles** - (6.1) - display
49. **6. Fermion Sector and Mixing Angles** - (6.4) - display
50. **6. Fermion Sector and Mixing Angles** - (6.5) - display
51. **6. Fermion Sector and Mixing Angles** - (6.6) - display
52. **6. Fermion Sector and Mixing Angles** - (6.7) - display
53. **6. Fermion Sector and Mixing Angles** - (6.3a) - display
54. **6. Fermion Sector and Mixing Angles** - (6.3b) - display
55. **6. Fermion Sector and Mixing Angles** - (6.8) - display
56. **6. Fermion Sector and Mixing Angles** - (6.9) - display
57. **6. Fermion Sector and Mixing Angles** - (6.10) - display
58. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - unnumbered - display
59. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - (6.8) - display
60. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - unnumbered - display
61. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - unnumbered - display
62. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - (6.2) - display
63. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - (6.3) - display
64. **6.2h Yukawa Texture: Georgi-Jarlskog and Instantons** - unnumbered - display
65. **7. Cosmology and Dark Energy** - (7.1) - display
66. **7. Cosmology and Dark Energy** - (7.2) - display
67. **7. Cosmology and Dark Energy** - (7.3) - display
68. **7. Cosmology and Dark Energy** - (7.4) - display
69. **7.4 The Attractor Scalar** - (7.5) - display
70. **7.4 The Attractor Scalar** - (7.6) - display
71. **7.5 The Thermal Time Hypothesis** - (7.7) - display
72. **7.5 The Thermal Time Hypothesis** - (7.8) - display
73. **7.5 The Thermal Time Hypothesis** - (7.9) - display
74. **9. Discussion and Transparency** - unnumbered - display
75. **Appendix A: Virasoro Anomaly Cancellation** - unnumbered - display
76. **Appendix A: Virasoro Anomaly Cancellation** - unnumbered - display
77. **Appendix A: Virasoro Anomaly Cancellation** - unnumbered - display
78. **Appendix B: Generation Number Derivation** - unnumbered - display
79. **Appendix C: Atmospheric Mixing Angle Derivation** - unnumbered - display
80. **Appendix D: Dark Energy Equation of State** - unnumbered - display
81. **Appendix D: Dark Energy Equation of State** - unnumbered - display
82. **Appendix D: Dark Energy Equation of State** - unnumbered - display
83. **Appendix E: Proton Decay Calculation** - unnumbered - display
84. **Appendix E: Proton Decay Calculation** - unnumbered - display
85. **Appendix E: Proton Decay Calculation** - unnumbered - display
86. **Appendix E: Proton Decay Calculation** - (E.4) - display
87. **Appendix E: Proton Decay Calculation** - unnumbered - display
88. **Appendix F: Dimensional Decomposition** - unnumbered - display
89. **Appendix G: Effective Torsion from Flux Quantization** - unnumbered - display
90. **Appendix G: Effective Torsion from Flux Quantization** - unnumbered - display
91. **Appendix H: Proton Decay Branching Ratio** - unnumbered - display
92. **Appendix I: Gravitational Wave Dispersion** - unnumbered - display
93. **Appendix I: Gravitational Wave Dispersion** - unnumbered - display
94. **Appendix I: Gravitational Wave Dispersion** - unnumbered - display
95. **Appendix M: Speculative Extensions - Consciousness and the Pneuma Vacuum** - unnumbered - display
96. **Appendix M: Speculative Extensions - Consciousness and the Pneuma Vacuum** - unnumbered - display
97. **Unknown Section** - unnumbered - display
98. **Unknown Section** - unnumbered - inline
99. **Unknown Section** - unnumbered - inline
100. **Unknown Section** - unnumbered - inline
*... and 714 more equations*