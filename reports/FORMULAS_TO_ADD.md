# Formulas to Add to theory_output.json

**Priority: HIGH - Core numbered equations from Sections 1-6**

This is the actionable list of formulas that should be added to `theory_output.json` to establish it as the single source of truth.

---

## Section 2: 26-Dimensional Bulk Spacetime

### Formula: master-action-full
- **Equation Number:** (2.3)
- **LaTeX:**
```latex
S_{26D} = \int d^{26}X \sqrt{G} \left[ M^{24} R + \bar{\Psi}_P (i\Gamma^M D_M - m)\Psi_P + \mathcal{L}_{Sp(2,\mathbb{R})} \right]
```
- **Description:** Complete 26D action with Einstein-Hilbert, Pneuma kinetic term, and Sp(2,R) gauge constraints
- **Category:** framework
- **Section:** 2.4 The Master Action and Pneuma Field

### Formula: pneuma-stress-energy
- **Equation Number:** (2.4)
- **LaTeX:**
```latex
T_{MN}^{(\text{Pneuma})} = \frac{i}{4}\left[\bar{\Psi}_P\Gamma_{(M}D_{N)}\Psi_P - D_{(M}\bar{\Psi}_P\Gamma_{N)}\Psi_P\right] - g_{MN}\mathcal{L}_{\Psi}
```
- **Description:** Pneuma field stress-energy tensor sourcing spacetime curvature
- **Category:** framework
- **Section:** 2.5 Pneuma Condensate as Source of Geometry

### Formula: racetrack-stability
- **Equation Number:** (2.8)
- **LaTeX:**
```latex
\frac{\partial V}{\partial \Psi_P} = 0 \quad \Rightarrow \quad Aa \, e^{-a\Psi_P} = Bb \, e^{-b\Psi_P}
```
- **Description:** Vacuum stability condition for racetrack potential minimum
- **Category:** vacuum
- **Section:** 2.7 Pneuma Vacuum Selection: Racetrack Mechanism

---

## Section 3: 13-Dimensional Shadow

### Formula: sp2r-algebra
- **Equation Number:** (3.1)
- **LaTeX:**
```latex
[J_{ab}, J_{cd}] = i(\eta_{ac}J_{bd} + \eta_{bd}J_{ac} - \eta_{ad}J_{bc} - \eta_{bc}J_{ad})
```
- **Description:** Sp(2,R) Lie algebra commutation relations for gauge fixing
- **Category:** framework
- **Section:** 3. Reduction to the 13-Dimensional Shadow

### Formula: sp2r-null-constraint
- **Equation Number:** (3.1a)
- **LaTeX:**
```latex
X^2 = X^M \eta_{MN} X^N = 0 \quad \text{(null constraint)}
```
- **Description:** Sp(2,R) null constraint eliminating second timelike dimension
- **Category:** framework
- **Section:** 3. Reduction to the 13-Dimensional Shadow

### Formula: sp2r-orthogonality
- **Equation Number:** (3.1b)
- **LaTeX:**
```latex
X \cdot P = X^M \eta_{MN} P^N = 0 \quad \text{(orthogonality constraint)}
```
- **Description:** Sp(2,R) orthogonality constraint between position and momentum
- **Category:** framework
- **Section:** 3. Reduction to the 13-Dimensional Shadow

### Formula: sp2r-mass-shell
- **Equation Number:** (3.1c)
- **LaTeX:**
```latex
P^2 = P^M \eta_{MN} P^N = M^2 \quad \text{(mass-shell constraint)}
```
- **Description:** Sp(2,R) mass-shell constraint for physical states
- **Category:** framework
- **Section:** 3. Reduction to the 13-Dimensional Shadow

---

## Section 4: TCS G₂ Compactification

### Formula: tcs-betti-numbers
- **Equation Number:** (4.1)
- **LaTeX:**
```latex
b_2 = 4, \quad b_3 = 24
```
- **Description:** Betti numbers of the TCS G₂ manifold uniquely determining topology
- **Category:** topology
- **Section:** 4. Compactification on the TCS G2 Manifold
- **Parameters:** `b2: 4`, `b3: 24`

### Formula: effective-euler-characteristic
- **Equation Number:** (4.1a)
- **LaTeX:**
```latex
\chi_{\text{eff}} = 2(h^{1,1} - h^{2,1} + h^{3,1}) = 2(4 - 0 + 68) = 144
```
- **Description:** Effective Euler characteristic from Hodge numbers
- **Category:** topology
- **Section:** 4. Compactification on the TCS G2 Manifold
- **Parameters:** `chi_eff: 144`

### Formula: generation-number-formula
- **Equation Number:** (4.2)
- **LaTeX:**
```latex
n_{\text{gen}} = \frac{|\chi_{\text{eff}}|}{48} = \frac{144}{48} = 3
```
- **Description:** Number of fermion generations from index theorem
- **Category:** topology
- **Section:** 4. Compactification on the TCS G2 Manifold
- **Parameters:** `n_gen: 3`
- **Note:** Already exists as `generation-number`, needs equation number mapping

### Formula: flux-quantization-formula
- **Equation Number:** (4.3)
- **LaTeX:**
```latex
N_{\text{flux}} = \frac{\chi_{\text{eff}}}{6} = \frac{144}{6} = 24 \quad \Rightarrow \quad T_{\omega,\text{eff}} = -\frac{b_3}{N_{\text{flux}}} = -1.0
```
- **Description:** Flux quantization and effective torsion from topology
- **Category:** topology
- **Section:** 4. Compactification on the TCS G2 Manifold
- **Parameters:** `N_flux: 24`, `T_omega_eff: -1.0`
- **Note:** Already exists as `flux-quantization`, verify LaTeX match

### Formula: kahler-racetrack
- **Equation Number:** (4.4a)
- **LaTeX:**
```latex
W_{\text{race}} = A e^{-a T} + B e^{-b T}
```
- **Description:** Racetrack superpotential for Kähler modulus stabilization
- **Category:** vacuum
- **Section:** 4. Compactification on the TCS G2 Manifold

### Formula: planck-mass-effective
- **Equation Number:** (4.4b)
- **LaTeX:**
```latex
M_{\text{Pl,eff}}^2 = \frac{1}{h^{1,1}} \sum_{i=1}^{4} w_i M_{\text{Pl,bulk}}^2 \approx \frac{M_{\text{Pl,bulk}}^2}{4}
```
- **Description:** Effective 4D Planck mass from modulus-weighted average
- **Category:** hierarchy
- **Section:** 4. Compactification on the TCS G2 Manifold

### Formula: ewsb-vev-weights
- **Equation Number:** (4.4c)
- **LaTeX:**
```latex
v_{\text{EW}} = v_{\text{EW,0}} \times w_0 \approx v_{\text{EW,0}}
```
- **Description:** EW VEV with modulus weight correction
- **Category:** ewsb
- **Section:** 4. Compactification on the TCS G2 Manifold

### Formula: hierarchy-geometric
- **Equation Number:** (4.4d)
- **LaTeX:**
```latex
\frac{M_{\text{Pl}}}{v_{\text{EW}}} \sim \frac{1}{\sqrt{h^{1,1}}} \times \frac{M_{\text{Pl,bulk}}}{M_{\text{GUT}}} \approx 10^{16}
```
- **Description:** Geometric origin of gauge hierarchy from Kähler moduli
- **Category:** hierarchy
- **Section:** 4. Compactification on the TCS G2 Manifold

---

## Section 5: Gauge Unification and Standard Model

### Formula: gut-scale-derivation
- **Equation Number:** (5.3)
- **LaTeX:**
```latex
M_{\text{GUT}} = M_{\text{Pl}} \times \left(\frac{\text{Vol}(G_2)}{\ell_P^7}\right)^{-1/3} \approx 2.1 \times 10^{16} \text{ GeV}
```
- **Description:** GUT scale from compactification volume
- **Category:** gauge
- **Section:** 5. Gauge Unification and the Standard Model
- **Note:** Related to existing `gut-scale` but with derivation

### Formula: threshold-corrections-general
- **Equation Number:** (5.3a)
- **LaTeX:**
```latex
\alpha_i^{-1}(M_Z) = \alpha_{\text{GUT}}^{-1} + \frac{b_i}{2\pi}\ln\left(\frac{M_{\text{GUT}}}{M_Z}\right) + \Delta_i
```
- **Description:** Gauge coupling running with threshold corrections
- **Category:** gauge
- **Section:** 5. Gauge Unification and the Standard Model

### Formula: gaugino-condensate
- **Equation Number:** (5.4a)
- **LaTeX:**
```latex
\langle\text{Tr}(\lambda\lambda)\rangle \sim \Lambda_{\text{hidden}}^3 e^{-8\pi^2/g^2}
```
- **Description:** Hidden sector gaugino condensation scale
- **Category:** gauge
- **Section:** 5. Gauge Unification and the Standard Model

### Formula: anomaly-cancellation-u1
- **Equation Number:** (5.4b)
- **LaTeX:**
```latex
\text{Tr}(Q_Y) = 0, \quad \text{Tr}(Q_Y^3) = 0
```
- **Description:** U(1)_Y anomaly cancellation from SO(10) embedding
- **Category:** gauge
- **Section:** 5. Gauge Unification and the Standard Model

### Formula: alpha-s-evolution
- **Equation Number:** (6.7)
- **LaTeX:**
```latex
\alpha_s(M_Z) = \frac{\alpha_{\text{GUT}}}{1 + \frac{7\alpha_{\text{GUT}}}{2\pi}\ln\left(\frac{M_{\text{GUT}}}{M_Z}\right)} = 0.1179
```
- **Description:** Strong coupling constant from GUT scale RG evolution
- **Category:** gauge
- **Section:** 6. Fermion Sector and Mixing Angles
- **Parameters:** `alpha_s: 0.1179 ± 0.0010`

---

## Section 6: Fermion Sector and Mixing Angles

### Formula: theta23-maximal-derivation
- **Equation Number:** (6.1)
- **LaTeX:**
```latex
\shadow_{\text{kuf}} = \shadow_{\text{chet}} \quad \Rightarrow \quad \theta_{23} = \frac{\pi}{4} = 45°
```
- **Description:** Maximal atmospheric mixing from G₂ holonomy symmetry (octonionic)
- **Category:** neutrino
- **Section:** 6. Fermion Sector and Mixing Angles
- **Note:** Related to existing `theta23-maximal` but with derivation

### Formula: neutrino-mass-21
- **Equation Number:** (6.2)
- **LaTeX:**
```latex
\Delta m^2_{21} = 7.97 \times 10^{-5} \text{ eV}^2 \quad (\text{exp: } 7.42 \times 10^{-5}, \text{ error: } 7.4\%)
```
- **Description:** Solar neutrino mass splitting
- **Category:** neutrino
- **Section:** 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons
- **Parameters:** `delta_m21_sq: 7.97e-5 eV^2`

### Formula: neutrino-mass-31-formula
- **Equation Number:** (6.3)
- **LaTeX:**
```latex
\Delta m^2_{31} = 2.525 \times 10^{-3} \text{ eV}^2 \quad (\text{exp: } 2.515 \times 10^{-3}, \text{ error: } 0.4\%)
```
- **Description:** Atmospheric neutrino mass splitting
- **Category:** neutrino
- **Section:** 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons
- **Parameters:** `delta_m31_sq: 2.525e-3 eV^2`
- **Note:** Already exists as `neutrino-mass-31`, needs equation number

### Formula: top-quark-mass
- **Equation Number:** (6.4)
- **LaTeX:**
```latex
m_t = y_t \times \frac{v_{\text{EW}}}{\sqrt{2}} = 172.7 \text{ GeV}
```
- **Description:** Top quark mass from Yukawa coupling
- **Category:** fermion_masses
- **Section:** 6. Fermion Sector and Mixing Angles
- **Parameters:** `m_t: 172.7 GeV`

### Formula: bottom-quark-mass
- **Equation Number:** (6.5)
- **LaTeX:**
```latex
m_b = y_b \times \frac{v_{\text{EW}}}{\sqrt{2}} = 4.18 \text{ GeV}
```
- **Description:** Bottom quark mass from Yukawa coupling
- **Category:** fermion_masses
- **Section:** 6. Fermion Sector and Mixing Angles
- **Parameters:** `m_b: 4.18 GeV`

### Formula: tau-lepton-mass
- **Equation Number:** (6.6)
- **LaTeX:**
```latex
m_\tau = y_\tau \times \frac{v_{\text{EW}}}{\sqrt{2}} = 1.777 \text{ GeV}
```
- **Description:** Tau lepton mass from Yukawa coupling
- **Category:** fermion_masses
- **Section:** 6. Fermion Sector and Mixing Angles
- **Parameters:** `m_tau: 1.777 GeV`

### Formula: quark-masses-light-up
- **Equation Number:** (6.3a)
- **LaTeX:**
```latex
m_u = 2.2 \text{ MeV}, \quad m_c = 1.27 \text{ GeV}
```
- **Description:** Up-type quark masses (first two generations)
- **Category:** fermion_masses
- **Section:** 6. Fermion Sector and Mixing Angles

### Formula: quark-masses-light-down
- **Equation Number:** (6.3b)
- **LaTeX:**
```latex
m_d = 4.7 \text{ MeV}, \quad m_s = 95 \text{ MeV}
```
- **Description:** Down-type quark masses (first two generations)
- **Category:** fermion_masses
- **Section:** 6. Fermion Sector and Mixing Angles

### Formula: lepton-masses-light
- **Equation Number:** (6.8)
- **LaTeX:**
```latex
m_e = 0.511 \text{ MeV}, \quad m_\mu = 105.66 \text{ MeV}
```
- **Description:** Charged lepton masses (first two generations)
- **Category:** fermion_masses
- **Section:** 6. Fermion Sector and Mixing Angles

### Formula: ckm-matrix-definition
- **Equation Number:** (6.9)
- **LaTeX:**
```latex
V_{\text{CKM}} = V_u^\dagger V_d
```
- **Description:** CKM matrix as mismatch between up and down rotation matrices
- **Category:** mixing
- **Section:** 6. Fermion Sector and Mixing Angles

---

## Section 7: Cosmology and Dark Energy

### Formula: d-eff-formula
- **Equation Number:** (7.1)
- **LaTeX:**
```latex
d_{\text{eff}} = 12 + \gamma(\shadow_{\text{kuf}} + \shadow_{\text{chet}}) = 12 + 0.5(1.152) = 12.576
```
- **Description:** Effective dimension for dark energy equation of state
- **Category:** cosmology
- **Section:** 7. Cosmology and Dark Energy

### Formula: dark-energy-w0-derivation
- **Equation Number:** (7.2)
- **LaTeX:**
```latex
w_0 = -\frac{d_{\text{eff}} - 1}{d_{\text{eff}} + 1} = -\frac{11.576}{13.576} = -0.8528
```
- **Description:** Dark energy equation of state from effective dimension
- **Category:** cosmology
- **Section:** 7. Cosmology and Dark Energy
- **Note:** Related to existing `dark-energy-w0` but with derivation

### Formula: dark-energy-evolution
- **Equation Number:** (7.3)
- **LaTeX:**
```latex
w(z) = w_0 \left[1 + \frac{\alpha_T}{3}\ln(1+z)\right]
```
- **Description:** Dark energy equation of state evolution with redshift
- **Category:** cosmology
- **Section:** 7. Cosmology and Dark Energy

### Formula: dark-energy-wa
- **Equation Number:** (7.4)
- **LaTeX:**
```latex
w_a = -\frac{\alpha_T}{3} \times \frac{w_0 + 1}{1 - w_0} = -0.75
```
- **Description:** Dark energy evolution parameter w_a in CPL parameterization
- **Category:** cosmology
- **Section:** 7. Cosmology and Dark Energy

### Formula: attractor-modulus
- **Equation Number:** (7.5)
- **LaTeX:**
```latex
\phi_M = \log(\text{Vol}_7)
```
- **Description:** Attractor scalar field as logarithm of G₂ volume
- **Category:** cosmology
- **Section:** 7.4 The Attractor Scalar

---

## Implementation Notes

### Suggested Workflow

1. **Batch 1 (Core Framework):** Add formulas from Section 2 (master action, stress-energy, racetrack)
2. **Batch 2 (Dimensional Reduction):** Add formulas from Section 3 (Sp(2,R) constraints)
3. **Batch 3 (Topology):** Add formulas from Section 4 (Betti numbers, generations, flux)
4. **Batch 4 (Gauge Sector):** Add formulas from Section 5 (GUT scale, couplings, thresholds)
5. **Batch 5 (Fermions):** Add formulas from Section 6 (masses, mixing, CKM)
6. **Batch 6 (Cosmology):** Add formulas from Section 7 (w_0, w_a, attractor)

### JSON Template

```json
{
  "formula-id": {
    "latex": "...",
    "description": "...",
    "category": "framework|topology|gauge|fermion_masses|neutrino|mixing|cosmology|vacuum",
    "equation_number": "(X.Y)",
    "section": "Section title",
    "parameters": {
      "param_name": "value"
    },
    "derivation": "Optional derivation notes",
    "references": ["paper section", "appendix"]
  }
}
```

### Cross-Referencing

Several formulas already exist in theory_output.json but lack equation number mapping:
- `generation-number` ↔ (4.2)
- `flux-quantization` ↔ (4.3)
- `theta23-maximal` ↔ (6.1)
- `neutrino-mass-31` ↔ (6.3)
- `dark-energy-w0` ↔ (7.2)

Update these with `"equation_number"` field.

---

**Total formulas to add:** ~40 core equations
**Existing to update:** ~5 mappings
**Estimated effort:** 2-3 hours for complete migration

---

This list provides the complete actionable set of formulas needed to establish theory_output.json as the single source of truth for all major equations in the paper.
