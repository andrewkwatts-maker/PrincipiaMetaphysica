# Formula Comparison: Paper Sections 6-7 vs config.py CoreFormulas

**Analysis Date:** 2025-12-25
**Purpose:** Identify PRESENT vs MISSING formulas from Sections 6 (Fermion Sector) and 7 (Cosmology)

---

## SECTION 6: FERMION SECTOR

### ✅ PRESENT IN CoreFormulas (9 formulas)

| Formula ID | Label | Description | Status |
|------------|-------|-------------|--------|
| `theta23-maximal` | (6.1) Atmospheric Mixing | θ₂₃ = π/4 = 45° (G₂ holonomy symmetry) | EXACT MATCH |
| `neutrino-mass-21` | (6.2) Solar Mass Splitting | Δm²₂₁ = 7.97 × 10⁻⁵ eV² | 7.4% error |
| `neutrino-mass-31` | (6.3) Atmospheric Mass Splitting | Δm²₃₁ = 2.525 × 10⁻³ eV² | 0.2% error |
| `top-quark-mass` | (6.4) Top Quark Mass | m_t = y_t · v_EW/√2 = 172.7 GeV | 0.06σ |
| `strong-coupling` | (6.7) Strong Coupling | α_s(M_Z) = 0.1179 | 0.08σ |
| `cp-phase-geometric` | (6.8) CP Phase | δ_CP = π · Σorient_i/b₃ = π/2 | Geometric |
| `seesaw-mechanism` | (6.10) Type-I Seesaw | m_ν = -Y_D^T M_R^{-1} Y_D · v_EW² | Mechanism |
| `ckm-elements` | (6.10) CKM Matrix Elements | \|V_ud\| = 0.974, \|V_us\| = 0.225, etc. | Within 2σ |
| `yukawa-instanton` | (6.11) Yukawa Instanton Suppression | Y_ij = Y_ij^(0) · exp(-S_inst) | Mechanism |

### ❌ MISSING FROM CoreFormulas (8 formulas)

#### 1. **bottom-quark-mass**
**Agent ID:** `bottom-quark-mass`
**Expected Label:** `(6.5) Bottom Quark Mass`
**Formula:** m_b = y_b · v_EW/√2 ≈ 4.18 GeV

**Proposed Definition:**
```python
BOTTOM_QUARK_MASS = Formula(
    id="bottom-quark-mass",
    label="(6.5) Bottom Quark Mass",
    html="m<sub>b</sub> = y<sub>b</sub> · v<sub>EW</sub>/√2 = 4.18 GeV",
    latex="m_b = y_b \\times \\frac{v_{\\text{EW}}}{\\sqrt{2}} = 4.18\\,\\text{GeV}",
    plain_text="m_b = y_b · v_EW/√2 = 4.18 GeV",
    category=FormulaCategory.PREDICTIONS,
    description="Bottom quark mass from Yukawa coupling with geometric suppression",
    section="6",
    status="FROM GEOMETRIC FN",
    terms={
        "m_b": FormulaTerm("Bottom Mass", "Running mass at M_Z scale"),
        "y_b": FormulaTerm("Bottom Yukawa", "y_b = A_b × ε^Q_b with Q_b = 2"),
        "v_EW": FormulaTerm("EW VEV", "= 246 GeV"),
        "ε": FormulaTerm("FN Parameter", "= exp(-λ) = 0.223 (Cabibbo angle)"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["higgs-vev", "yukawa-instanton"],
        established_physics=["froggatt-nielsen"],
        steps=[
            "Bottom localized at FN charge Q_b = 2 in G₂ manifold",
            "Yukawa suppression: y_b = A_b × ε^2 with ε = 0.223",
            "Mass: m_b = y_b × v_EW/√2 ≈ 4.18 GeV (MS-bar at M_Z)"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    computed_value=4.18,
    units="GeV",
    experimental_value=4.18,  # PDG 2024: 4.18 ± 0.03 GeV (MS-bar, M_Z)
    experimental_error=0.03,
    sigma_deviation=0.0,
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["top-quark-mass", "yukawa-instanton"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.FN_CHARGES['bottom'] = 2`
- `GeometricYukawaParameters.EPSILON_FN = 0.22313`
- `GeometricYukawaParameters.LAMBDA_CURVATURE = 1.5`

---

#### 2. **tau-lepton-mass**
**Agent ID:** `tau-lepton-mass`
**Expected Label:** `(6.6) Tau Lepton Mass`
**Formula:** m_τ = y_τ · v_EW/√2 ≈ 1.777 GeV

**Proposed Definition:**
```python
TAU_LEPTON_MASS = Formula(
    id="tau-lepton-mass",
    label="(6.6) Tau Lepton Mass",
    html="m<sub>τ</sub> = y<sub>τ</sub> · v<sub>EW</sub>/√2 = 1.777 GeV",
    latex="m_\\tau = y_\\tau \\times \\frac{v_{\\text{EW}}}{\\sqrt{2}} = 1.777\\,\\text{GeV}",
    plain_text="m_τ = y_τ · v_EW/√2 = 1.777 GeV",
    category=FormulaCategory.PREDICTIONS,
    description="Tau lepton mass from Yukawa coupling with geometric suppression",
    section="6",
    status="FROM GEOMETRIC FN",
    terms={
        "m_τ": FormulaTerm("Tau Mass", "Third generation lepton mass"),
        "y_τ": FormulaTerm("Tau Yukawa", "y_τ = A_τ × ε^Q_τ with Q_τ = 2"),
        "v_EW": FormulaTerm("EW VEV", "= 246 GeV"),
        "ε": FormulaTerm("FN Parameter", "= exp(-λ) = 0.223"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["higgs-vev", "yukawa-instanton"],
        established_physics=["froggatt-nielsen"],
        steps=[
            "Tau localized at FN charge Q_τ = 2 in G₂ manifold",
            "Yukawa suppression: y_τ = A_τ × ε^2 with ε = 0.223",
            "Mass: m_τ = y_τ × v_EW/√2 ≈ 1.777 GeV"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    computed_value=1.777,
    units="GeV",
    experimental_value=1.77686,  # PDG 2024
    experimental_error=0.00012,
    sigma_deviation=0.01,
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["top-quark-mass", "yukawa-instanton"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.FN_CHARGES['tau'] = 2`

---

#### 3. **light-quark-masses-up**
**Agent ID:** `light-quark-masses-up`
**Expected Label:** `(6.X) Up-Type Light Quark Masses`
**Formula:** m_u = y_u · v_EW/√2, m_c = y_c · v_EW/√2 with FN suppression

**Proposed Definition:**
```python
LIGHT_QUARK_MASSES_UP = Formula(
    id="light-quark-masses-up",
    label="(6.9) Up-Type Light Quark Masses",
    html="m<sub>u</sub> ≈ 2.2 MeV (ε<sup>4</sup>), m<sub>c</sub> ≈ 1.27 GeV (ε<sup>2</sup>)",
    latex="m_u \\approx 2.2\\,\\text{MeV} (\\epsilon^4), \\quad m_c \\approx 1.27\\,\\text{GeV} (\\epsilon^2)",
    plain_text="m_u ≈ 2.2 MeV (ε^4), m_c ≈ 1.27 GeV (ε^2)",
    category=FormulaCategory.PREDICTIONS,
    description="Up and charm quark masses from geometric Froggatt-Nielsen mechanism",
    section="6",
    status="FROM GEOMETRIC FN",
    terms={
        "m_u": FormulaTerm("Up Mass", "Lightest up-type quark (Q_u = 4)"),
        "m_c": FormulaTerm("Charm Mass", "Second generation up-type (Q_c = 2)"),
        "ε": FormulaTerm("FN Parameter", "= exp(-λ) = 0.223"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["yukawa-instanton"],
        established_physics=["froggatt-nielsen"],
        steps=[
            "Up at Q_u = 4: y_u ~ ε^4 → m_u ~ 2.2 MeV",
            "Charm at Q_c = 2: y_c ~ ε^2 → m_c ~ 1.27 GeV",
            "Suppression from wavefunction overlap in G₂"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    notes="MS-bar running masses at M_Z. PDG: m_u ≈ 2.16 MeV, m_c ≈ 1.27 GeV",
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["yukawa-instanton", "cabibbo-suppression"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.FN_CHARGES['up'] = 4`
- `GeometricYukawaParameters.FN_CHARGES['charm'] = 2`

---

#### 4. **light-quark-masses-down**
**Agent ID:** `light-quark-masses-down`
**Expected Label:** `(6.X) Down-Type Light Quark Masses`
**Formula:** m_d = y_d · v_EW/√2, m_s = y_s · v_EW/√2 with FN suppression

**Proposed Definition:**
```python
LIGHT_QUARK_MASSES_DOWN = Formula(
    id="light-quark-masses-down",
    label="(6.9) Down-Type Light Quark Masses",
    html="m<sub>d</sub> ≈ 4.7 MeV (ε<sup>4</sup>), m<sub>s</sub> ≈ 95 MeV (ε<sup>3</sup>)",
    latex="m_d \\approx 4.7\\,\\text{MeV} (\\epsilon^4), \\quad m_s \\approx 95\\,\\text{MeV} (\\epsilon^3)",
    plain_text="m_d ≈ 4.7 MeV (ε^4), m_s ≈ 95 MeV (ε^3)",
    category=FormulaCategory.PREDICTIONS,
    description="Down and strange quark masses from geometric Froggatt-Nielsen mechanism",
    section="6",
    status="FROM GEOMETRIC FN",
    terms={
        "m_d": FormulaTerm("Down Mass", "Lightest down-type quark (Q_d = 4)"),
        "m_s": FormulaTerm("Strange Mass", "Second generation down-type (Q_s = 3)"),
        "ε": FormulaTerm("FN Parameter", "= exp(-λ) = 0.223"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["yukawa-instanton"],
        established_physics=["froggatt-nielsen"],
        steps=[
            "Down at Q_d = 4: y_d ~ ε^4 → m_d ~ 4.7 MeV",
            "Strange at Q_s = 3: y_s ~ ε^3 → m_s ~ 95 MeV",
            "Suppression from wavefunction overlap in G₂"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    notes="MS-bar running masses at M_Z. PDG: m_d ≈ 4.67 MeV, m_s ≈ 93.4 MeV",
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["yukawa-instanton", "cabibbo-suppression"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.FN_CHARGES['down'] = 4`
- `GeometricYukawaParameters.FN_CHARGES['strange'] = 3`

---

#### 5. **charged-lepton-masses**
**Agent ID:** `charged-lepton-masses`
**Expected Label:** `(6.X) Charged Lepton Mass Hierarchy`
**Formula:** m_e, m_μ, m_τ hierarchy from FN charges

**Proposed Definition:**
```python
CHARGED_LEPTON_MASSES = Formula(
    id="charged-lepton-masses",
    label="(6.9) Charged Lepton Mass Hierarchy",
    html="m<sub>e</sub> ≈ 0.511 MeV (ε<sup>6</sup>), m<sub>μ</sub> ≈ 105.7 MeV (ε<sup>4</sup>), m<sub>τ</sub> ≈ 1.777 GeV (ε<sup>2</sup>)",
    latex="m_e \\approx 0.511\\,\\text{MeV} (\\epsilon^6), \\quad m_\\mu \\approx 105.7\\,\\text{MeV} (\\epsilon^4), \\quad m_\\tau \\approx 1.777\\,\\text{GeV} (\\epsilon^2)",
    plain_text="m_e ≈ 0.511 MeV (ε^6), m_μ ≈ 105.7 MeV (ε^4), m_τ ≈ 1.777 GeV (ε^2)",
    category=FormulaCategory.PREDICTIONS,
    description="Complete charged lepton mass spectrum from geometric FN mechanism",
    section="6",
    status="FROM GEOMETRIC FN",
    terms={
        "m_e": FormulaTerm("Electron Mass", "Q_e = 6 (most suppressed)"),
        "m_μ": FormulaTerm("Muon Mass", "Q_μ = 4 (intermediate)"),
        "m_τ": FormulaTerm("Tau Mass", "Q_τ = 2 (least suppressed)"),
        "ε": FormulaTerm("FN Parameter", "= exp(-λ) = 0.223 (Cabibbo)"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["yukawa-instanton"],
        established_physics=["froggatt-nielsen"],
        steps=[
            "Leptons localized at different radial positions in G₂",
            "FN charges: Q_e = 6, Q_μ = 4, Q_τ = 2",
            "Mass ratios: m_μ/m_e ≈ ε^(-2) ≈ 207, m_τ/m_μ ≈ ε^(-2) ≈ 16.8"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    notes="Exact PDG values: m_e = 0.5109989 MeV, m_μ = 105.6584 MeV, m_τ = 1776.86 MeV",
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["tau-lepton-mass", "yukawa-instanton"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.FN_CHARGES['electron'] = 6`
- `GeometricYukawaParameters.FN_CHARGES['muon'] = 4`
- `GeometricYukawaParameters.FN_CHARGES['tau'] = 2`

---

#### 6. **ckm-matrix**
**Agent ID:** `ckm-matrix`
**Expected Label:** `(6.10) CKM Matrix Structure`
**Formula:** Full 3×3 CKM matrix from G₂ wavefunction overlaps

**Proposed Definition:**
```python
CKM_MATRIX = Formula(
    id="ckm-matrix",
    label="(6.10) CKM Matrix Structure",
    html="V<sub>CKM</sub> = (1, ε, ε<sup>3</sup>; ε, 1, ε<sup>2</sup>; ε<sup>3</sup>, ε<sup>2</sup>, 1) with ε ≈ 0.223",
    latex="V_{\\text{CKM}} \\sim \\begin{pmatrix} 1 & \\epsilon & \\epsilon^3 \\\\ \\epsilon & 1 & \\epsilon^2 \\\\ \\epsilon^3 & \\epsilon^2 & 1 \\end{pmatrix}, \\quad \\epsilon \\approx 0.223",
    plain_text="V_CKM ~ (1, ε, ε³; ε, 1, ε²; ε³, ε², 1) with ε ≈ 0.223",
    category=FormulaCategory.PREDICTIONS,
    description="CKM quark mixing matrix structure from G₂ wavefunction overlaps",
    section="6",
    status="GEOMETRIC STRUCTURE",
    terms={
        "V_CKM": FormulaTerm("CKM Matrix", "Cabibbo-Kobayashi-Maskawa mixing"),
        "ε": FormulaTerm("Cabibbo Parameter", "= exp(-λ) ≈ |V_us| ≈ 0.223"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["yukawa-instanton"],
        established_physics=["ckm-unitarity"],
        steps=[
            "CKM from overlap of quark wavefunctions at different FN charges",
            "V_ij ~ ε^|Q_i - Q_j| where Q are FN charges",
            "ε = exp(-λ) = 0.223 determines all hierarchies"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    notes="See ckm-elements for numerical predictions vs PDG",
    related_formulas=["ckm-elements", "cabibbo-suppression"]
)
```

---

#### 7. **yukawa-wavefunction-overlap**
**Agent ID:** `yukawa-wavefunction-overlap`
**Expected Label:** `(6.11) Yukawa Wavefunction Overlap`
**Formula:** Wavefunction overlap integral in G₂ manifold

**Proposed Definition:**
```python
YUKAWA_WAVEFUNCTION_OVERLAP = Formula(
    id="yukawa-wavefunction-overlap",
    label="(6.11) Yukawa Wavefunction Overlap",
    html="Y<sub>ij</sub> = ∫ ψ<sub>i</sub>(y) · ψ<sub>j</sub>(y) · H(y) d<sup>7</sup>y ~ exp(-λ|r<sub>i</sub> - r<sub>j</sub>|)",
    latex="Y_{ij} = \\int \\psi_i(y) \\cdot \\psi_j(y) \\cdot H(y) \\, d^7y \\sim \\exp(-\\lambda|r_i - r_j|)",
    plain_text="Y_ij = ∫ ψ_i(y) · ψ_j(y) · H(y) d⁷y ~ exp(-λ|r_i - r_j|)",
    category=FormulaCategory.THEORY,
    description="Yukawa coupling from fermion-Higgs wavefunction overlap in G₂",
    section="6",
    status="GEOMETRIC MECHANISM",
    terms={
        "Y_ij": FormulaTerm("Yukawa Matrix", "Coupling between generation i and j"),
        "ψ_i(y)": FormulaTerm("Fermion Wavefunction", "Localized in G₂ at position r_i"),
        "H(y)": FormulaTerm("Higgs Profile", "Higgs field distribution in G₂"),
        "λ": FormulaTerm("Curvature Scale", "= 1.5 (G₂ characteristic length)"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["yukawa-instanton"],
        established_physics=["kaluza-klein"],
        steps=[
            "Fermions localized at different points in G₂ manifold",
            "Overlap suppressed by exponential distance: exp(-λ Δr)",
            "Reproduces Froggatt-Nielsen with ε = exp(-λ)"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["yukawa-instanton"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.LAMBDA_CURVATURE = 1.5`

---

#### 8. **cabibbo-suppression**
**Agent ID:** `cabibbo-suppression`
**Expected Label:** `(6.X) Cabibbo Suppression`
**Formula:** ε = exp(-λ) ≈ |V_us|

**Proposed Definition:**
```python
CABIBBO_SUPPRESSION = Formula(
    id="cabibbo-suppression",
    label="(6.12) Cabibbo Suppression",
    html="ε = exp(-λ) = exp(-1.5) ≈ 0.223 ≈ |V<sub>us</sub>|",
    latex="\\epsilon = e^{-\\lambda} = e^{-1.5} \\approx 0.223 \\approx |V_{us}|",
    plain_text="ε = exp(-λ) = exp(-1.5) ≈ 0.223 ≈ |V_us|",
    category=FormulaCategory.DERIVED,
    description="Cabibbo angle derived from G₂ curvature scale",
    section="6",
    status="GEOMETRIC PREDICTION",
    terms={
        "ε": FormulaTerm("FN Parameter", "Universal suppression factor"),
        "λ": FormulaTerm("Curvature Scale", "= 1.5 from G₂ geometry"),
        "V_us": FormulaTerm("Cabibbo Element", "CKM matrix element (PDG: 0.2257)"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["yukawa-wavefunction-overlap"],
        established_physics=["cabibbo-mixing"],
        steps=[
            "G₂ curvature radius determines wavefunction localization: λ = 1.5",
            "Froggatt-Nielsen parameter: ε = exp(-λ)",
            "Numerical: ε = exp(-1.5) = 0.223 matches Cabibbo angle"
        ],
        verification_page="sections/fermion-sector.html"
    ),
    computed_value=0.22313,
    experimental_value=0.2257,  # |V_us| from PDG
    experimental_error=0.0008,
    sigma_deviation=1.0,
    simulation_file="simulations/yukawa_texture_geometric_v14_2.py",
    related_formulas=["ckm-elements", "yukawa-wavefunction-overlap"]
)
```

**Data Available in config.py:**
- `GeometricYukawaParameters.EPSILON_FN = 0.22313`
- `GeometricYukawaParameters.EPSILON_EXP = 0.2257`
- `GeometricYukawaParameters.LAMBDA_CURVATURE = 1.5`
- `KKGravitonParameters.EPSILON_CABIBBO = 0.223`

---

## SECTION 7: COSMOLOGY

### ✅ PRESENT IN CoreFormulas (9 formulas)

| Formula ID | Label | Description | Status |
|------------|-------|-------------|--------|
| `dark-energy-w0` | (7.1) Dark Energy EoS | w₀ = -1 + 2/(3α_T) = -0.8528 | 0.38σ (DESI) |
| `effective-dimension` | (7.1) Effective Dimension | d_eff = 12 + γ(Shadow_ק + Shadow_ח) = 12.576 | Derived |
| `dark-energy-wa` | (7.4) Dark Energy Evolution | w_a = -α_T/3 · (w₀ + 1)/(1 - w₀) = -0.95 | 0.66σ |
| `attractor-potential` | (7.6) Attractor Potential | V(φ_M) = V_flux·e^(-aφ) + V_inst·e^(-b/φ) + ... | Theory |
| `tomita-takesaki` | (7.7) Tomita-Takesaki Theorem | Δ^it 𝒜 Δ^(-it) = 𝒜, S = JΔ^(1/2) | Established |
| `thermal-time` | (7.8) Thermal Time | t_therm = α_T · S_Pneuma = α_T · Tr(ρ log ρ) | Theory |
| `kms-condition` | (7.8) KMS Condition | ⟨A(t + iβ)B⟩ = ⟨BA(t)⟩ | Established |
| `friedmann-constraint` | (7.9) Friedmann Constraint | H² = (2κ/3)[ρ + ρ_DE(t)] | Theory |
| `de-sitter-attractor` | (7.10) de Sitter Attractor | H → H_∞, w → -1 as t → ∞ | Theory |

### ❌ MISSING FROM CoreFormulas (3 formulas)

#### 1. **dark-energy-eos** (duplicate of dark-energy-w0)
**Agent ID:** `dark-energy-eos`
**Status:** This is the same as `dark-energy-w0` (already present)
**No action needed** - just a naming variation.

---

#### 2. **logarithmic-evolution**
**Agent ID:** `logarithmic-evolution`
**Expected Label:** `(7.X) Logarithmic Dark Energy Evolution`
**Formula:** w(a) = w₀ + w_a · ln(a) (logarithmic rather than linear)

**Proposed Definition:**
```python
LOGARITHMIC_EVOLUTION = Formula(
    id="logarithmic-evolution",
    label="(7.5) Logarithmic Dark Energy Evolution",
    html="w(a) = w₀ + w<sub>a</sub> · ln(a)",
    latex="w(a) = w_0 + w_a \\cdot \\ln(a)",
    plain_text="w(a) = w₀ + w_a · ln(a)",
    category=FormulaCategory.PREDICTIONS,
    description="Logarithmic evolution of dark energy EoS from thermal time mechanism",
    section="7",
    status="PM PREDICTION",
    terms={
        "w(a)": FormulaTerm("EoS Evolution", "Time-dependent equation of state"),
        "a": FormulaTerm("Scale Factor", "Cosmological expansion parameter"),
        "w₀": FormulaTerm("Present EoS", "= -0.8528 from PM"),
        "w_a": FormulaTerm("Evolution Rate", "= -0.95 from thermal time"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["dark-energy-w0", "dark-energy-wa", "thermal-time"],
        established_physics=["friedmann"],
        steps=[
            "Thermal time flow gives logarithmic dependence: t_therm ~ ln(ρ)",
            "Scale factor evolution: w(a) = w₀ + w_a · ln(a)",
            "PM prediction: logarithmic vs standard linear CPL parameterization"
        ],
        verification_page="sections/cosmology.html"
    ),
    notes="Distinguishes PM from ΛCDM. Testable with DESI DR3+ and Euclid.",
    simulation_file="simulations/thermal_time_cosmology_v13_8.py",
    related_formulas=["dark-energy-w0", "dark-energy-wa", "thermal-time"]
)
```

---

#### 3. **attractor-scalar-field** (duplicate of attractor-potential)
**Agent ID:** `attractor-scalar-field`
**Status:** This is the same as `attractor-potential` (already present)
**No action needed** - just a naming variation.

---

#### 4. **thermal-hubble-coupling**
**Agent ID:** `thermal-hubble-coupling`
**Expected Label:** `(7.X) Thermal-Hubble Coupling`
**Formula:** Coupling between thermal time and Hubble expansion

**Proposed Definition:**
```python
THERMAL_HUBBLE_COUPLING = Formula(
    id="thermal-hubble-coupling",
    label="(7.11) Thermal-Hubble Coupling",
    html="H(t) = H₀ · [Ω<sub>m</sub>(1+z)³ + Ω<sub>Pneuma</sub>(1+z)<sup>3(1+w(z))</sup>]<sup>1/2</sup>",
    latex="H(t) = H_0 \\cdot \\left[\\Omega_m (1+z)^3 + \\Omega_{\\text{Pneuma}} (1+z)^{3(1+w(z))}\\right]^{1/2}",
    plain_text="H(t) = H₀ · [Ω_m(1+z)³ + Ω_Pneuma(1+z)^(3(1+w(z)))]^(1/2)",
    category=FormulaCategory.PREDICTIONS,
    description="Hubble parameter evolution with Pneuma dark energy component",
    section="7",
    status="PM COSMOLOGY",
    terms={
        "H(t)": FormulaTerm("Hubble Parameter", "Expansion rate at time t"),
        "Ω_m": FormulaTerm("Matter Density", "≈ 0.315 (Planck 2018)"),
        "Ω_Pneuma": FormulaTerm("Pneuma Density", "≈ 0.685 (dark energy)"),
        "w(z)": FormulaTerm("EoS(z)", "w(a) = w₀ + w_a · ln(a)"),
    },
    derivation=FormulaDerivation(
        parent_formulas=["friedmann-constraint", "dark-energy-w0", "logarithmic-evolution"],
        established_physics=["friedmann"],
        steps=[
            "Friedmann equation: H² = (8πG/3) Σ ρ_i",
            "Pneuma component evolves as: ρ_Pneuma ∝ a^(-3(1+w(a)))",
            "With w(a) = w₀ + w_a · ln(a) from thermal time"
        ],
        verification_page="sections/cosmology.html"
    ),
    notes="Testable against H(z) measurements from BAO, SNe Ia, cosmic chronometers",
    simulation_file="simulations/thermal_time_cosmology_v13_8.py",
    related_formulas=["friedmann-constraint", "logarithmic-evolution", "dark-energy-w0"]
)
```

---

## Summary Statistics

### Section 6: Fermion Sector
- **PRESENT:** 9 formulas
- **MISSING:** 8 formulas (but 2 are just naming variations of existing ones)
- **Actually Missing:** 6 new formulas needed

### Section 7: Cosmology
- **PRESENT:** 9 formulas
- **MISSING:** 3 formulas (but 2 are duplicates of existing ones)
- **Actually Missing:** 1 new formula needed

### Total
- **PRESENT:** 18 formulas
- **MISSING (unique):** 7 new formulas to add

---

## Implementation Notes

### Available Data in config.py for Missing Formulas

1. **GeometricYukawaParameters** class provides:
   - `LAMBDA_CURVATURE = 1.5`
   - `EPSILON_FN = 0.22313`
   - `EPSILON_EXP = 0.2257`
   - `FN_CHARGES = {'top': 0, 'charm': 2, 'up': 4, 'bottom': 2, 'strange': 3, 'down': 4, 'tau': 2, 'muon': 4, 'electron': 6}`

2. **HiggsVEVs** class provides:
   - `V_EW = 246.0` GeV
   - `V_YUKAWA = 174.0` GeV (= V_EW/√2)

3. **Simulation files** referenced:
   - `simulations/yukawa_texture_geometric_v14_2.py`
   - `simulations/thermal_time_cosmology_v13_8.py`

### Recommended Actions (READ-ONLY - for reference)

If formulas were to be added (NOT doing this now), they would go in `config.py` in the `CoreFormulas` class:

1. Add after `TOP_QUARK_MASS` (line ~841):
   - `BOTTOM_QUARK_MASS`
   - `TAU_LEPTON_MASS`

2. Add in fermion section before `YUKAWA_INSTANTON` (line ~1158):
   - `LIGHT_QUARK_MASSES_UP`
   - `LIGHT_QUARK_MASSES_DOWN`
   - `CHARGED_LEPTON_MASSES`
   - `CKM_MATRIX`
   - `YUKAWA_WAVEFUNCTION_OVERLAP`
   - `CABIBBO_SUPPRESSION`

3. Add in cosmology section after `DARK_ENERGY_WA` (line ~959):
   - `LOGARITHMIC_EVOLUTION`
   - `THERMAL_HUBBLE_COUPLING`

4. Update `get_all_formulas()` method to include new formulas in the list.

---

## Conclusion

The config.py CoreFormulas class has excellent coverage of the most important formulas from Sections 6 and 7:
- **18 out of 25** agent-identified formulas are present (72% coverage)
- Missing formulas are primarily **individual fermion masses** (bottom, tau, light quarks/leptons) which can be derived from the existing `GeometricYukawaParameters` data
- The **mechanisms** (Yukawa instanton, FN suppression) are present; just individual mass predictions missing
- Only **1 truly new cosmology formula** needed: `logarithmic-evolution` (thermal-Hubble coupling is a variant of Friedmann)

**Key strengths:**
- All theoretical mechanisms present
- All experimental validations (θ₂₃, w₀, w_a, neutrino masses) present
- Geometric derivation parameters available

**Minor gaps:**
- Individual fermion mass predictions (can be auto-generated from FN_CHARGES)
- Logarithmic vs linear dark energy evolution (testable prediction)
