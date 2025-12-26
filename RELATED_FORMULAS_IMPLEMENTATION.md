# Related Formulas Implementation Guide
## Exact Code Changes for config.py

**File:** H:\Github\PrincipiaMetaphysica\config.py
**Changes Needed:** 6 formulas require `related_formulas` field addition

---

## Change 1: GENERATION_NUMBER (line ~648)

**Current Code:**
```python
    GENERATION_NUMBER = Formula(
        id="generation-number",
        label="(2.6) Three Generations",
        html="n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3",
        latex="n_{gen} = \\frac{\\chi_{eff}}{48} = \\frac{144}{48} = 3",
        plain_text="n_gen = χ_eff/48 = 144/48 = 3",
        category=FormulaCategory.DERIVED,
        description="Number of fermion generations from G₂ topology",
        status="EXACT MATCH",
        terms={
            "n_gen": FormulaTerm("Generations", "Number of fermion families", "sections/fermion-sector.html"),
            "χ_eff": FormulaTerm("Effective Euler", "χ_eff = 144 from TCS construction"),
            "48": FormulaTerm("Index Divisor", "From G₂ index theorem (2× F-theory's 24)"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["tcs-euler-characteristic"],
            established_physics=["f-theory-index"],
            steps=[
                "Start with G₂ manifold effective Euler characteristic χ_eff = 144",
                "Apply G₂ index theorem: n_gen = χ_eff/48 (twice F-theory divisor)",
                "Result: n_gen = 144/48 = 3 exactly"
            ],
            verification_page="sections/fermion-sector.html"
        ),
        computed_value=3,
        experimental_value=3,
        sigma_deviation=0.0
    )
```

**Modified Code:**
```python
    GENERATION_NUMBER = Formula(
        id="generation-number",
        label="(2.6) Three Generations",
        html="n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3",
        latex="n_{gen} = \\frac{\\chi_{eff}}{48} = \\frac{144}{48} = 3",
        plain_text="n_gen = χ_eff/48 = 144/48 = 3",
        category=FormulaCategory.DERIVED,
        description="Number of fermion generations from G₂ topology",
        status="EXACT MATCH",
        terms={
            "n_gen": FormulaTerm("Generations", "Number of fermion families", "sections/fermion-sector.html"),
            "χ_eff": FormulaTerm("Effective Euler", "χ_eff = 144 from TCS construction"),
            "48": FormulaTerm("Index Divisor", "From G₂ index theorem (2× F-theory's 24)"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["tcs-euler-characteristic"],
            established_physics=["f-theory-index"],
            steps=[
                "Start with G₂ manifold effective Euler characteristic χ_eff = 144",
                "Apply G₂ index theorem: n_gen = χ_eff/48 (twice F-theory divisor)",
                "Result: n_gen = 144/48 = 3 exactly"
            ],
            verification_page="sections/fermion-sector.html"
        ),
        computed_value=3,
        experimental_value=3,
        sigma_deviation=0.0,
        related_formulas=["tcs-topology", "effective-euler", "flux-quantization"]
    )
```

**Change:** Add comma after `sigma_deviation=0.0` and add line:
```python
        related_formulas=["tcs-topology", "effective-euler", "flux-quantization"]
```

---

## Change 2: GUT_SCALE (line ~676)

**Current Code:**
```python
    GUT_SCALE = Formula(
        id="gut-scale",
        label="(4.2) GUT Scale",
        html="M<sub>GUT</sub> = M<sub>Pl</sub> · V<sub>G₂</sub><sup>-1/7</sup> = 2.118 × 10<sup>16</sup> GeV",
        latex="M_{GUT} = M_{Pl} \\cdot V_{G_2}^{-1/7} = 2.118 \\times 10^{16}\\,\\text{GeV}",
        plain_text="M_GUT = M_Pl · V_G2^(-1/7) = 2.118 × 10^16 GeV",
        category=FormulaCategory.DERIVED,
        description="Grand unification scale from G₂ compactification volume",
        status="GEOMETRIC",
        terms={
            "M_GUT": FormulaTerm("GUT Scale", "Grand unification mass scale"),
            "M_Pl": FormulaTerm("Planck Mass", "Reduced Planck mass 2.435×10¹⁸ GeV"),
            "V_G2": FormulaTerm("G₂ Volume", "Compactification volume in Planck units"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["g2-compactification"],
            established_physics=["kaluza-klein"],
            steps=[
                "G₂ manifold volume V_G2 determines effective 4D Planck scale",
                "Dimensional reduction: M_GUT = M_Pl · V_G2^(-1/7)",
                "From TCS topology: V_G2 yields M_GUT = 2.118×10¹⁶ GeV"
            ],
            verification_page="sections/gauge-unification.html"
        ),
        computed_value=2.118e16,
        units="GeV"
    )
```

**Modified Code:**
```python
    GUT_SCALE = Formula(
        id="gut-scale",
        label="(4.2) GUT Scale",
        html="M<sub>GUT</sub> = M<sub>Pl</sub> · V<sub>G₂</sub><sup>-1/7</sup> = 2.118 × 10<sup>16</sup> GeV",
        latex="M_{GUT} = M_{Pl} \\cdot V_{G_2}^{-1/7} = 2.118 \\times 10^{16}\\,\\text{GeV}",
        plain_text="M_GUT = M_Pl · V_G2^(-1/7) = 2.118 × 10^16 GeV",
        category=FormulaCategory.DERIVED,
        description="Grand unification scale from G₂ compactification volume",
        status="GEOMETRIC",
        terms={
            "M_GUT": FormulaTerm("GUT Scale", "Grand unification mass scale"),
            "M_Pl": FormulaTerm("Planck Mass", "Reduced Planck mass 2.435×10¹⁸ GeV"),
            "V_G2": FormulaTerm("G₂ Volume", "Compactification volume in Planck units"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["g2-compactification"],
            established_physics=["kaluza-klein"],
            steps=[
                "G₂ manifold volume V_G2 determines effective 4D Planck scale",
                "Dimensional reduction: M_GUT = M_Pl · V_G2^(-1/7)",
                "From TCS topology: V_G2 yields M_GUT = 2.118×10¹⁶ GeV"
            ],
            verification_page="sections/gauge-unification.html"
        ),
        computed_value=2.118e16,
        units="GeV",
        related_formulas=["tcs-topology", "gut-coupling", "planck-mass-derivation", "kappa-gut-coefficient"]
    )
```

**Change:** Add comma after `units="GeV"` and add line:
```python
        related_formulas=["tcs-topology", "gut-coupling", "planck-mass-derivation", "kappa-gut-coefficient"]
```

---

## Change 3: DARK_ENERGY_W0 (line ~704)

**Current Code:**
```python
    DARK_ENERGY_W0 = Formula(
        id="dark-energy-w0",
        label="(7.1) Dark Energy EoS",
        html="w₀ = -1 + 2/(3α<sub>T</sub>) = -0.8528",
        latex="w_0 = -1 + \\frac{2}{3\\alpha_T} = -0.8528",
        plain_text="w₀ = -1 + 2/(3α_T) = -0.8528",
        category=FormulaCategory.PREDICTIONS,
        description="Dark energy equation of state from thermal time mechanism",
        status="DESI DR2 VALIDATED (0.38σ)",
        terms={
            "w₀": FormulaTerm("EoS Parameter", "w = p/ρ at present epoch"),
            "α_T": FormulaTerm("Thermal Exponent", "α_T = 4.5 from KMS condition"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["thermal-time-flow", "mep-constraint"],
            established_physics=["kms-condition", "tomita-takesaki"],
            steps=[
                "Thermal time flow from Pneuma statistics: H = -ln(ρ)",
                "Apply MEP constraint for stationary vacuum",
                "Result: w₀ = -1 + 2/(3α_T) with α_T = 4.5"
            ],
            verification_page="sections/cosmology.html"
        ),
        computed_value=-0.8528,
        experimental_value=-0.83,
        sigma_deviation=0.38
    )
```

**Modified Code:**
```python
    DARK_ENERGY_W0 = Formula(
        id="dark-energy-w0",
        label="(7.1) Dark Energy EoS",
        html="w₀ = -1 + 2/(3α<sub>T</sub>) = -0.8528",
        latex="w_0 = -1 + \\frac{2}{3\\alpha_T} = -0.8528",
        plain_text="w₀ = -1 + 2/(3α_T) = -0.8528",
        category=FormulaCategory.PREDICTIONS,
        description="Dark energy equation of state from thermal time mechanism",
        status="DESI DR2 VALIDATED (0.38σ)",
        terms={
            "w₀": FormulaTerm("EoS Parameter", "w = p/ρ at present epoch"),
            "α_T": FormulaTerm("Thermal Exponent", "α_T = 4.5 from KMS condition"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["thermal-time-flow", "mep-constraint"],
            established_physics=["kms-condition", "tomita-takesaki"],
            steps=[
                "Thermal time flow from Pneuma statistics: H = -ln(ρ)",
                "Apply MEP constraint for stationary vacuum",
                "Result: w₀ = -1 + 2/(3α_T) with α_T = 4.5"
            ],
            verification_page="sections/cosmology.html"
        ),
        computed_value=-0.8528,
        experimental_value=-0.83,
        sigma_deviation=0.38,
        related_formulas=["dark-energy-wa", "thermal-time", "kms-condition", "effective-dimension"]
    )
```

**Change:** Add comma after `sigma_deviation=0.38` and add line:
```python
        related_formulas=["dark-energy-wa", "thermal-time", "kms-condition", "effective-dimension"]
```

---

## Change 4: PROTON_LIFETIME (line ~733)

**Current Code:**
```python
    PROTON_LIFETIME = Formula(
        id="proton-lifetime",
        label="(5.3) Proton Lifetime",
        html="τ<sub>p</sub> = M<sub>GUT</sub>⁴/(α<sub>GUT</sub>² m<sub>p</sub>⁵) × S² = 8.15 × 10<sup>34</sup> years",
        latex="\\tau_p = \\frac{M_{GUT}^4}{\\alpha_{GUT}^2 m_p^5} \\times S^2 = 8.15 \\times 10^{34}\\,\\text{years}",
        plain_text="τ_p = M_GUT⁴/(α_GUT² m_p⁵) × S² = 8.15 × 10³⁴ years",
        category=FormulaCategory.PREDICTIONS,
        description="Proton lifetime from GUT scale with TCS suppression",
        status="TESTABLE (Hyper-K ~2030s)",
        terms={
            "τ_p": FormulaTerm("Proton Lifetime", "p → e⁺π⁰ decay timescale"),
            "M_GUT": FormulaTerm("GUT Scale", "2.118×10¹⁶ GeV"),
            "α_GUT": FormulaTerm("GUT Coupling", "1/23.54"),
            "S": FormulaTerm("Suppression", "TCS cycle separation factor ~2.1"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["gut-scale", "tcs-suppression"],
            established_physics=["yang-mills"],
            steps=[
                "Standard dimension-6 decay: τ_p ∝ M_GUT⁴/(α_GUT² m_p⁵)",
                "TCS geometry provides additional suppression S = 2.1 from cycle separation",
                "Result: τ_p = 8.15×10³⁴ years (4.9× Super-K bound)"
            ],
            verification_page="sections/gauge-unification.html"
        ),
        computed_value=8.15e34,
        units="years"
    )
```

**Modified Code:**
```python
    PROTON_LIFETIME = Formula(
        id="proton-lifetime",
        label="(5.3) Proton Lifetime",
        html="τ<sub>p</sub> = M<sub>GUT</sub>⁴/(α<sub>GUT</sub>² m<sub>p</sub>⁵) × S² = 8.15 × 10<sup>34</sup> years",
        latex="\\tau_p = \\frac{M_{GUT}^4}{\\alpha_{GUT}^2 m_p^5} \\times S^2 = 8.15 \\times 10^{34}\\,\\text{years}",
        plain_text="τ_p = M_GUT⁴/(α_GUT² m_p⁵) × S² = 8.15 × 10³⁴ years",
        category=FormulaCategory.PREDICTIONS,
        description="Proton lifetime from GUT scale with TCS suppression",
        status="TESTABLE (Hyper-K ~2030s)",
        terms={
            "τ_p": FormulaTerm("Proton Lifetime", "p → e⁺π⁰ decay timescale"),
            "M_GUT": FormulaTerm("GUT Scale", "2.118×10¹⁶ GeV"),
            "α_GUT": FormulaTerm("GUT Coupling", "1/23.54"),
            "S": FormulaTerm("Suppression", "TCS cycle separation factor ~2.1"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["gut-scale", "tcs-suppression"],
            established_physics=["yang-mills"],
            steps=[
                "Standard dimension-6 decay: τ_p ∝ M_GUT⁴/(α_GUT² m_p⁵)",
                "TCS geometry provides additional suppression S = 2.1 from cycle separation",
                "Result: τ_p = 8.15×10³⁴ years (4.9× Super-K bound)"
            ],
            verification_page="sections/gauge-unification.html"
        ),
        computed_value=8.15e34,
        units="years",
        related_formulas=["gut-scale", "gut-coupling", "proton-branching", "doublet-triplet"]
    )
```

**Change:** Add comma after `units="years"` and add line:
```python
        related_formulas=["gut-scale", "gut-coupling", "proton-branching", "doublet-triplet"]
```

---

## Change 5: THETA23_MAXIMAL (line ~762)

**Current Code:**
```python
    THETA23_MAXIMAL = Formula(
        id="theta23-maximal",
        label="(6.1) Atmospheric Mixing",
        html="θ<sub>23</sub> = π/4 = 45° (G₂ holonomy symmetry)",
        latex="\\theta_{23} = \\frac{\\pi}{4} = 45^\\circ",
        plain_text="θ_23 = π/4 = 45° (G₂ holonomy symmetry)",
        category=FormulaCategory.DERIVED,
        description="Maximal atmospheric mixing from G₂ holonomy",
        status="EXACT MATCH",
        terms={
            "θ_23": FormulaTerm("Atmospheric Angle", "PMNS mixing angle"),
            "G₂": FormulaTerm("G₂ Holonomy", "7D exceptional holonomy group"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["g2-holonomy"],
            established_physics=[],
            steps=[
                "G₂ holonomy provides Z₂ symmetry between 2nd and 3rd generation",
                "This discrete symmetry enforces θ_23 = π/4 exactly",
                "Result: maximal atmospheric mixing (45°)"
            ],
            verification_page="sections/fermion-sector.html"
        ),
        computed_value=45.0,
        units="degrees",
        experimental_value=45.2,
        sigma_deviation=0.15
    )
```

**Modified Code:**
```python
    THETA23_MAXIMAL = Formula(
        id="theta23-maximal",
        label="(6.1) Atmospheric Mixing",
        html="θ<sub>23</sub> = π/4 = 45° (G₂ holonomy symmetry)",
        latex="\\theta_{23} = \\frac{\\pi}{4} = 45^\\circ",
        plain_text="θ_23 = π/4 = 45° (G₂ holonomy symmetry)",
        category=FormulaCategory.DERIVED,
        description="Maximal atmospheric mixing from G₂ holonomy",
        status="EXACT MATCH",
        terms={
            "θ_23": FormulaTerm("Atmospheric Angle", "PMNS mixing angle"),
            "G₂": FormulaTerm("G₂ Holonomy", "7D exceptional holonomy group"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["g2-holonomy"],
            established_physics=[],
            steps=[
                "G₂ holonomy provides Z₂ symmetry between 2nd and 3rd generation",
                "This discrete symmetry enforces θ_23 = π/4 exactly",
                "Result: maximal atmospheric mixing (45°)"
            ],
            verification_page="sections/fermion-sector.html"
        ),
        computed_value=45.0,
        units="degrees",
        experimental_value=45.2,
        sigma_deviation=0.15,
        related_formulas=["neutrino-mass-21", "neutrino-mass-31", "tcs-topology", "cp-phase-geometric", "ckm-elements"]
    )
```

**Change:** Add comma after `sigma_deviation=0.15` and add line:
```python
        related_formulas=["neutrino-mass-21", "neutrino-mass-31", "tcs-topology", "cp-phase-geometric", "ckm-elements"]
```

---

## Change 6: KK_GRAVITON (line ~789)

**Current Code:**
```python
    KK_GRAVITON = Formula(
        id="kk-graviton-mass",
        label="(8.1) KK Graviton Mass",
        html="m<sub>KK,1</sub> = 1/R<sub>c</sub> = 5.0 TeV",
        latex="m_{KK,1} = \\frac{1}{R_c} = 5.0\\,\\text{TeV}",
        plain_text="m_KK,1 = 1/R_c = 5.0 TeV",
        category=FormulaCategory.PREDICTIONS,
        description="First KK graviton mode mass from compactification radius",
        status="HL-LHC TESTABLE",
        terms={
            "m_KK,1": FormulaTerm("First KK Mode", "Lowest graviton excitation mass"),
            "R_c": FormulaTerm("Compactification Radius", "G₂ manifold characteristic size"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["g2-compactification"],
            established_physics=["kaluza-klein"],
            steps=[
                "KK tower masses: m_n = n/R_c",
                "R_c determined by M_GUT and volume: R_c = 1/(5.0 TeV)",
                "First mode at 5.0 TeV, accessible at HL-LHC"
            ],
            verification_page="sections/predictions.html"
        ),
        computed_value=5.0,
        units="TeV"
    )
```

**Modified Code:**
```python
    KK_GRAVITON = Formula(
        id="kk-graviton-mass",
        label="(8.1) KK Graviton Mass",
        html="m<sub>KK,1</sub> = 1/R<sub>c</sub> = 5.0 TeV",
        latex="m_{KK,1} = \\frac{1}{R_c} = 5.0\\,\\text{TeV}",
        plain_text="m_KK,1 = 1/R_c = 5.0 TeV",
        category=FormulaCategory.PREDICTIONS,
        description="First KK graviton mode mass from compactification radius",
        status="HL-LHC TESTABLE",
        terms={
            "m_KK,1": FormulaTerm("First KK Mode", "Lowest graviton excitation mass"),
            "R_c": FormulaTerm("Compactification Radius", "G₂ manifold characteristic size"),
        },
        derivation=FormulaDerivation(
            parent_formulas=["g2-compactification"],
            established_physics=["kaluza-klein"],
            steps=[
                "KK tower masses: m_n = n/R_c",
                "R_c determined by M_GUT and volume: R_c = 1/(5.0 TeV)",
                "First mode at 5.0 TeV, accessible at HL-LHC"
            ],
            verification_page="sections/predictions.html"
        ),
        computed_value=5.0,
        units="TeV",
        related_formulas=["gut-scale", "tcs-topology", "planck-mass-derivation"]
    )
```

**Change:** Add comma after `units="TeV"` and add line:
```python
        related_formulas=["gut-scale", "tcs-topology", "planck-mass-derivation"]
```

---

## Quick Reference Summary

| Formula ID | Line | Last Field Before Change | Related Formulas to Add |
|------------|------|-------------------------|------------------------|
| generation-number | ~648 | sigma_deviation=0.0 | ["tcs-topology", "effective-euler", "flux-quantization"] |
| gut-scale | ~676 | units="GeV" | ["tcs-topology", "gut-coupling", "planck-mass-derivation", "kappa-gut-coefficient"] |
| dark-energy-w0 | ~704 | sigma_deviation=0.38 | ["dark-energy-wa", "thermal-time", "kms-condition", "effective-dimension"] |
| proton-lifetime | ~733 | units="years" | ["gut-scale", "gut-coupling", "proton-branching", "doublet-triplet"] |
| theta23-maximal | ~762 | sigma_deviation=0.15 | ["neutrino-mass-21", "neutrino-mass-31", "tcs-topology", "cp-phase-geometric", "ckm-elements"] |
| kk-graviton-mass | ~789 | units="TeV" | ["gut-scale", "tcs-topology", "planck-mass-derivation"] |

---

## Testing After Implementation

Run these checks:
1. Python syntax validation: `python -c "import config"`
2. Check all related formula IDs exist: verify no broken links
3. Check bidirectional consistency: formulas that reference each other should have mutual links
4. Verify JSON export: `config.CoreFormulas.export_formulas()` should include all related_formulas

---

**Implementation Date:** December 25, 2025
**File Version:** config.py v14.1
