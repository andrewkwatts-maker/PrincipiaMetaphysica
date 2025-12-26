# Foundations Metadata Audit Report

**Generated:** 2025-12-26

## Executive Summary

- **Total Foundations:** 17
- **Complete Foundations:** 17
- **Incomplete Foundations:** 0
- **Completion Rate:** 100.0%

### Quality Metrics

**Content Richness:**
- **Key Properties:** 6-8 properties per foundation (avg: 7.1)
- **Formulas:** 4-17 formulas per foundation (avg: 8.1)
- **Summary Length:** 122-187 characters (avg: 152.8)
- **PM Connection:** 327-1143 characters (avg: 554.9)

**Historical Coverage:**
- **Earliest Foundation:** 1854 (Ricci Tensor)
- **Latest Foundation:** 1987 (Tomita-Takesaki Theory)
- **Average Year:** 1937.2

**Category Distribution:**
- Established Physics: 2
- Established Mathematics: 2
- gravity: 2
- geometry: 2
- thermodynamics: 2
- quantum_field_theory: 1
- thermal_qft: 1
- algebra: 1
- differential_geometry: 1
- dimensional_reduction: 1
- quantum: 1
- Theoretical Physics: 1

**Badge Types:**
- established: 16
- theoretical: 1

## Foundations with Missing Fields

*All foundations are complete!*

## Complete Foundations

- Boltzmann Entropy (`boltzmann-entropy`)
- Calabi-Yau Manifolds (`calabi-yau`)
- Clifford Algebra (`clifford-algebra`)
- Dirac Equation (`dirac-equation`)
- Dirac Spinors (`dirac-spinor`)
- Einstein Field Equations (`einstein-field-equations`)
- Einstein-Hilbert Action (`einstein-hilbert-action`)
- G₂ Manifolds (`g2-manifolds`)
- Hawking Temperature (`hawking-temperature`)
- Kaluza-Klein Theory (`kaluza-klein`)
- KMS Condition (`kms-condition`)
- Metric Tensor (`metric-tensor`)
- Ricci Tensor & Ricci Scalar (`ricci-tensor`)
- SO(10) Grand Unified Theory (`so10-gut`)
- Unruh Effect (`unruh-effect`)
- Yang-Mills Theory (`yang-mills`)
- Tomita-Takesaki Theory (`tomita-takesaki`)

## Field-by-Field Analysis

| Field | Missing Count | Completion Rate |
|-------|---------------|-----------------|
| `id` | 0 | 100.0% |
| `title` | 0 | 100.0% |
| `category` | 0 | 100.0% |
| `year_established` | 0 | 100.0% |
| `badge_type` | 0 | 100.0% |
| `main_equation` | 0 | 100.0% |
| `main_equation_latex` | 0 | 100.0% |
| `summary` | 0 | 100.0% |
| `key_properties` | 0 | 100.0% |
| `pm_connection` | 0 | 100.0% |
| `formulas` | 0 | 100.0% |

## Quality Improvement Opportunities

While all foundations have complete required metadata (100% completion rate), there are opportunities to enhance content quality and consistency:

### Foundations Needing Enrichment

**Foundations with Fewest Key Properties (6 properties):**
1. Dirac Spinors (`dirac-spinor`)
2. Einstein Field Equations (`einstein-field-equations`)
3. Einstein-Hilbert Action (`einstein-hilbert-action`)

**Foundations with Fewest Formulas (4-6 formulas):**
1. Boltzmann Entropy (`boltzmann-entropy`) - 4 formulas
2. Calabi-Yau Manifolds (`calabi-yau`) - 6 formulas
3. Clifford Algebra (`clifford-algebra`) - 6 formulas
4. Kaluza-Klein Theory (`kaluza-klein`) - 6 formulas
5. Ricci Tensor & Ricci Scalar (`ricci-tensor`) - 6 formulas

**Foundations with Shortest PM Connections (327-355 chars):**
1. Tomita-Takesaki Theory (`tomita-takesaki`) - 327 chars
2. Yang-Mills Theory (`yang-mills`) - 341 chars
3. Ricci Tensor & Ricci Scalar (`ricci-tensor`) - 352 chars
4. SO(10) Grand Unified Theory (`so10-gut`) - 352 chars
5. Unruh Effect (`unruh-effect`) - 355 chars

### Recommendations

#### 1. Standardize Category Values
**Current Issue:** Mixed capitalization and naming conventions
- "Established Physics" vs "gravity" vs "quantum_field_theory"
- "Established Mathematics" vs "algebra" vs "differential_geometry"

**Recommendation:** Adopt consistent snake_case taxonomy:
- `established_physics` → `gravity`, `quantum`, `thermodynamics`
- `established_mathematics` → `differential_geometry`, `algebra`, `geometry`
- `theoretical_physics` → keep as is

#### 2. Enrich Key Properties
**Target:** 8-10 key properties per foundation (currently 6-8)

Focus on foundations with only 6 properties:
- Add mathematical properties
- Add physical interpretations
- Add historical significance
- Add connections to other theories

#### 3. Expand Formula Collections
**Target:** 8-12 formulas per foundation (currently 4-17)

Priority foundations:
- Boltzmann Entropy (4 → 8+ formulas)
- Add variations, special cases, and related equations

#### 4. Strengthen PM Connections
**Target:** 500-800 characters per foundation (currently 327-1143)

Priority foundations needing expansion:
- Tomita-Takesaki Theory (327 chars)
- Yang-Mills Theory (341 chars)
- Ricci Tensor & Ricci Scalar (352 chars)
- SO(10) Grand Unified Theory (352 chars)
- Unruh Effect (355 chars)

Expand with:
- Specific dimensional connections (26D → 13D)
- Formula references from PM theory
- Physical implications in PM framework
- Mathematical structure parallels

#### 5. Quality Assurance
- Verify all LaTeX equations render correctly
- Ensure consistent formatting across all foundations
- Cross-reference formulas with PM theory formulas
- Validate historical years against reliable sources

## Detailed Foundation Data

### Boltzmann Entropy (`boltzmann-entropy`)

```json
{
  "id": "boltzmann-entropy",
  "title": "Boltzmann Entropy",
  "category": "thermodynamics",
  "year_established": 1877,
  "badge_type": "established",
  "main_equation": "S = k_B ln \u03a9",
  "main_equation_latex": "S = k_B \\ln \\Omega",
  "summary": "The fundamental bridge between microscopic statistical mechanics and macroscopic thermodynamics, connecting the number of microstates to entropy.",
  "key_properties": [
    "Entropy is the logarithm of the number of ways a system can be arranged",
    "S measures macroscopic disorder or information content",
    "\u03a9 is the number of microscopic configurations (microstates)",
    "k_B = 1.38\u00d710\u207b\u00b2\u00b3 J/K is the fundamental bridge between energy and temperature",
    "The logarithm makes entropy additive: S_total = S_1 + S_2",
    "Always increases in isolated systems (Second Law of Thermodynamics)",
    "Provides statistical foundation for classical thermodynamics",
    "Connects to Shannon information theory: entropy measures missing information"
  ],
  "pm_connection": "Boltzmann entropy plays a crucial role in PM's dimensional framework through the thermal time hypothesis. The flow of time is related to entropy increase: t \u221d S = k_B ln \u03a9. In higher dimensions, entropy generalizes to 26D bulk (S_26 = k_B ln \u03a9_26) and 13D shadow (S_13 = k_B ln \u03a9_13). Dimensional reduction preserves entropy through compactification. Black hole entropy S_BH = k_B A/(4\u2113_P\u00b2) suggests entropy is fundamentally geometric in higher-dimensional theories.",
  "formulas": [
    {
      "id": "boltzmann-entropy-main",
      "label": "Boltzmann Entropy",
      "plain_text": "S = k_B ln \u03a9",
      "latex": "S = k_B \\ln \\Omega",
      "description": "The fundamental relation between entropy and microstates"
    },
    {
      "id": "boltzmann-gibbs-generalization",
      "label": "Gibbs Entropy",
      "plain_text": "S = -k_B \u03a3_i p_i ln p_i",
      "latex": "S = -k_B \\sum_i p_i \\ln p_i",
      "description": "Generalization for non-equilibrium systems with probability distribution p_i"
    },
    {
      "id": "boltzmann-bh-entropy",
      "label": "Black Hole Entropy",
      "plain_text": "S_BH = k_B A/(4\u2113_P\u00b2) = k_B ln \u03a9_horizon",
      "latex": "S_{\\text{BH}} = \\frac{k_B A}{4\\ell_P^2} = k_B \\ln \\Omega_{\\text{horizon}}",
      "description": "Bekenstein-Hawking entropy connecting area to microstates"
    },
    {
      "id": "boltzmann-thermal-time",
      "label": "Thermal Time Hypothesis",
      "plain_text": "t \u221d S = k_B ln \u03a9",
      "latex": "t \\propto S = k_B \\ln \\Omega",
      "description": "Time emergence from entropy increase (Carlo Rovelli)"
    }
  ],
  "used_in_sections": [
    {
      "section": "thermal-time",
      "description": "Entropy and time emergence"
    },
    {
      "section": "cosmology",
      "description": "Thermodynamic arrow of time"
    }
  ]
}
```

### Calabi-Yau Manifolds (`calabi-yau`)

```json
{
  "id": "calabi-yau",
  "title": "Calabi-Yau Manifolds",
  "category": "geometry",
  "year_established": 1977,
  "badge_type": "established",
  "main_equation": "R_{i j\u0304} = 0, c_1(M) = 0",
  "main_equation_latex": "R_{i\\bar{j}} = 0, \\quad c_1(M) = 0",
  "summary": "Special geometric spaces that preserve supersymmetry when used for dimensional compactification, central to string theory and F-theory.",
  "key_properties": [
    "Compact K\u00e4hler manifolds with vanishing first Chern class",
    "Ricci-flat metric: no intrinsic curvature in compact dimensions",
    "Preserve N=1 supersymmetry in compactification",
    "K\u00e4hler structure provides geometric stability",
    "Non-trivial topology allows chiral matter from index theorems",
    "Holonomy group determines preserved gauge symmetry",
    "Mirror symmetry relates different CY manifolds"
  ],
  "pm_connection": "In the 2T framework, the 26D bulk (24,2) projects via Sp(2,R) to 13D shadow (12,1), which undergoes G\u2082 compactification rather than CY4 (though CY4 concepts inform topology). Two CY4 spaces (CY4_A and CY4_B) are mirror pairs with \u03c7_A = \u03c7_B = 72, giving \u03c7_eff = 144 total. Fermion generations: n_gen = \u03c7_eff/48 = 144/48 = 3, where divisor 48 comes from SO(10) GUT embedding. KKLT flux stabilization with modulus VEV \u03c6_M = 2.493 M_Pl provides the effective topology.",
  "formulas": [
    {
      "id": "cy-ricci-flat",
      "label": "Ricci-Flat Condition",
      "plain_text": "R_{i j\u0304} = 0",
      "latex": "R_{i\\bar{j}} = 0",
      "description": "Ricci curvature vanishes for Calabi-Yau manifolds"
    },
    {
      "id": "cy-chern-class",
      "label": "First Chern Class",
      "plain_text": "c_1(M) = 0",
      "latex": "c_1(M) = 0",
      "description": "Topological condition equivalent to Ricci-flatness (Calabi conjecture)"
    },
    {
      "id": "cy-euler-characteristic",
      "label": "Euler Characteristic",
      "plain_text": "\u03c7 = \u03a3_{p,q} (-1)^{p+q} h^{p,q}",
      "latex": "\\chi = \\sum_{p,q} (-1)^{p+q} h^{p,q}",
      "description": "Topological invariant from Hodge numbers"
    },
    {
      "id": "cy-generation-formula",
      "label": "Fermion Generation Formula",
      "plain_text": "n_gen = \u03c7_eff/48 = 144/48 = 3",
      "latex": "n_{\\text{gen}} = \\frac{\\chi_{\\text{eff}}}{48} = \\frac{144}{48} = 3",
      "description": "Number of generations from effective Euler characteristic in 2T framework"
    },
    {
      "id": "cy-mirror-symmetry",
      "label": "Mirror Symmetry",
      "plain_text": "\u03c7_A + \u03c7_B = 72 + 72 = 144",
      "latex": "\\chi_A + \\chi_B = 72 + 72 = 144",
      "description": "Combined Euler characteristic from mirror CY4 pair"
    },
    {
      "id": "cy-kklt-flux",
      "label": "KKLT Flux Stabilization",
      "plain_text": "\u03c7_eff = \u03c7_bare + \u0394\u03c7_flux, \u03c6_M = 2.493 M_Pl",
      "latex": "\\chi_{\\text{eff}} = \\chi_{\\text{bare}} + \\Delta\\chi_{\\text{flux}}, \\quad \\varphi_M = 2.493 M_{\\text{Pl}}",
      "description": "Flux dressing modifies effective topology with modulus VEV"
    }
  ],
  "used_in_sections": [
    {
      "section": "geometric-framework",
      "description": "Comparison with G\u2082 compactification"
    }
  ]
}
```

### Clifford Algebra (`clifford-algebra`)

```json
{
  "id": "clifford-algebra",
  "title": "Clifford Algebra",
  "category": "algebra",
  "year_established": 1878,
  "badge_type": "established",
  "main_equation": "{\u03b3^\u03bc, \u03b3^\u03bd} = 2g^{\u03bc\u03bd}",
  "main_equation_latex": "\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2g^{\\mu\\nu}",
  "summary": "The mathematical framework that unifies real numbers, complex numbers, quaternions, and geometric algebra - essential for describing spinors and fermions in physics.",
  "key_properties": [
    "Natural generalization of complex numbers and quaternions to arbitrary dimensions",
    "Geometric product combines dot product and wedge product",
    "Spinors arise as elements of minimal left ideals (irreducible representations)",
    "Spinor dimension formula: 2^\u230an/2\u230b for n-dimensional space",
    "360\u00b0 rotation changes sign of spinor; 720\u00b0 returns to original (double cover)",
    "Fundamental for describing fermions (spin-1/2 particles)",
    "Hierarchy: R \u2192 C \u2192 H \u2192 Cl(p,q) generalizes number systems"
  ],
  "pm_connection": "Clifford algebras provide the mathematical framework for spinors at each dimensional level in PM. 26D bulk: Cl(24,2) with 8192-component spinors (2^13). 13D shadow: Cl(12,1) with 64-component spinors (2^6). Reduction factor: 8192/64 = 128 = 2^7 preserves power-of-two structure. The 64 components in 13D encode fermion generation structure: 64 = 4\u00d716 suggests SO(10) GUT embedding with 3 generations from topology.",
  "formulas": [
    {
      "id": "clifford-anticommutator",
      "label": "Clifford Algebra Relation",
      "plain_text": "{\u03b3^\u03bc, \u03b3^\u03bd} = 2g^{\u03bc\u03bd}",
      "latex": "\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2g^{\\mu\\nu}",
      "description": "Fundamental anticommutation relation defining Clifford algebra"
    },
    {
      "id": "clifford-geometric-product",
      "label": "Geometric Product",
      "plain_text": "ab = a\u00b7b + a\u2227b",
      "latex": "ab = a \\cdot b + a \\wedge b",
      "description": "Combines inner and outer products into unified algebraic structure"
    },
    {
      "id": "clifford-spinor-dimension",
      "label": "Spinor Dimension",
      "plain_text": "dim(Spinor) = 2^\u230an/2\u230b",
      "latex": "\\dim(\\text{Spinor}) = 2^{\\lfloor n/2 \\rfloor}",
      "description": "Irreducible spinor representation dimension for Cl(p,q) with n=p+q"
    },
    {
      "id": "clifford-26d-bulk",
      "label": "26D Bulk Spinor",
      "plain_text": "Cl(24,2) \u2192 2^13 = 8192 components",
      "latex": "\\text{Cl}(24,2) \\to 2^{13} = 8192 \\text{ components}",
      "description": "Spinor dimension in PM's 26D bulk with signature (24,2)"
    },
    {
      "id": "clifford-13d-shadow",
      "label": "13D Shadow Spinor",
      "plain_text": "Cl(12,1) \u2192 2^6 = 64 components",
      "latex": "\\text{Cl}(12,1) \\to 2^6 = 64 \\text{ components}",
      "description": "Spinor dimension in PM's 13D shadow manifold"
    },
    {
      "id": "clifford-4d-dirac",
      "label": "4D Dirac Spinor",
      "plain_text": "Cl(3,1) \u2192 2^2 = 4 components",
      "latex": "\\text{Cl}(3,1) \\to 2^2 = 4 \\text{ components}",
      "description": "Standard Dirac spinor in 4D spacetime"
    }
  ],
  "used_in_sections": [
    {
      "section": "fermion-sector",
      "description": "Spinor representations and chirality"
    },
    {
      "section": "pneuma-lagrangian",
      "description": "8192-component bulk spinor"
    },
    {
      "section": "geometric-framework",
      "description": "Cl(24,2) \u2192 Cl(12,1) reduction"
    }
  ]
}
```

### Dirac Equation (`dirac-equation`)

```json
{
  "id": "dirac-equation",
  "title": "Dirac Equation",
  "category": "quantum",
  "year_established": 1928,
  "badge_type": "established",
  "main_equation": "(i\u03b3^\u03bc\u2202_\u03bc - m)\u03c8 = 0",
  "main_equation_latex": "(i\\gamma^\\mu\\partial_\\mu - m)\\psi = 0",
  "summary": "The relativistic wave equation for spin-\u00bd particles, unifying quantum mechanics and special relativity. First equation to predict antimatter.",
  "key_properties": [
    "Describes particles with spin-\u00bd (electrons, quarks, neutrinos)",
    "Combines quantum mechanics, special relativity, and spin",
    "Predicts existence of antimatter (negative energy solutions)",
    "Uses 4\u00d74 gamma matrices satisfying Clifford algebra",
    "\u03c8 is a 4-component Dirac spinor field",
    "Lorentz invariant under proper Lorentz transformations",
    "Lagrangian form: L = \u03c8\u0304(i\u03b3^\u03bc\u2202_\u03bc - m)\u03c8 with Dirac adjoint \u03c8\u0304 = \u03c8\u2020\u03b3^0"
  ],
  "pm_connection": "The Pneuma Lagrangian is a 26D generalization of the Dirac equation in the 2T framework with fermionic primacy. 26D bulk: \u03a8_P has 8192 components from Cl(24,2) - geometry emerges from spinor condensate g_MN ~ \u27e8\u03a8\u0304_P \u0393_(MN) \u03a8_P\u27e9. 13D shadow: 64 components from Cl(12,1) after dimensional reduction (factor 128 = 2^7). The 64-component shadow spinor connects to SO(10) GUT and 3 generations: 64 = 4\u00d716 with each generation containing 16 fermions in SO(10).",
  "formulas": [
    {
      "id": "dirac-equation-main",
      "label": "Dirac Equation",
      "plain_text": "(i\u03b3^\u03bc\u2202_\u03bc - m)\u03c8 = 0",
      "latex": "(i\\gamma^\\mu\\partial_\\mu - m)\\psi = 0",
      "description": "Relativistic wave equation for spin-\u00bd particles"
    },
    {
      "id": "dirac-lagrangian",
      "label": "Dirac Lagrangian",
      "plain_text": "L = \u03c8\u0304(i\u03b3^\u03bc\u2202_\u03bc - m)\u03c8",
      "latex": "\\mathcal{L} = \\bar{\\psi}(i\\gamma^\\mu\\partial_\\mu - m)\\psi",
      "description": "Lagrangian density for Dirac field"
    },
    {
      "id": "dirac-adjoint",
      "label": "Dirac Adjoint",
      "plain_text": "\u03c8\u0304 = \u03c8\u2020\u03b3^0",
      "latex": "\\bar{\\psi} = \\psi^\\dagger \\gamma^0",
      "description": "Adjoint spinor ensuring Lorentz invariance"
    },
    {
      "id": "dirac-pneuma-26d",
      "label": "26D Pneuma Lagrangian",
      "plain_text": "\u03a8\u0304_P(i\u0393^A D_A - m_P)\u03a8_P",
      "latex": "\\bar{\\Psi}_P(i\\Gamma^A D_A - m_P)\\Psi_P",
      "description": "26D generalization with 8192-component spinor in Cl(24,2)"
    },
    {
      "id": "dirac-spinor-reduction",
      "label": "Spinor Reduction Pathway",
      "plain_text": "8192 (26D) \u2192 64 (13D) \u2192 4 (4D) components",
      "latex": "8192 \\text{ (26D)} \\to 64 \\text{ (13D)} \\to 4 \\text{ (4D) components}",
      "description": "Dimensional reduction preserves Clifford structure"
    },
    {
      "id": "dirac-geometry-emergence",
      "label": "Geometry from Spinor Condensate",
      "plain_text": "g_MN ~ \u27e8\u03a8\u0304_P \u0393_(MN) \u03a8_P\u27e9",
      "latex": "g_{MN} \\sim \\langle \\bar{\\Psi}_P \\Gamma_{(MN)} \\Psi_P \\rangle",
      "description": "Metric emerges from spinor bivector condensate (fermionic primacy)"
    },
    {
      "id": "dirac-6d-reduction",
      "label": "6D Dirac Equation",
      "plain_text": "(i\u0393^M\u2202_M - m)\u03a8 = 0, M=0,1,2,3,5,6",
      "latex": "(i\\Gamma^M\\partial_M - m)\\Psi = 0, \\quad M=0,1,2,3,5,6",
      "description": "Intermediate 6D stage with 8-component spinor from Cl(5,1)"
    },
    {
      "id": "dirac-kk-tower",
      "label": "KK Mode Expansion",
      "plain_text": "\u03a8(x^\u03bc,y,z) = \u03a3_{n,m} \u03c8_{n,m}(x^\u03bc) Y_{n,m}(y,z)",
      "latex": "\\Psi(x^\\mu,y,z) = \\sum_{n,m} \\psi_{n,m}(x^\\mu) Y_{n,m}(y,z)",
      "description": "Kaluza-Klein decomposition on T\u00b2 torus"
    }
  ],
  "used_in_sections": [
    {
      "section": "pneuma-lagrangian",
      "description": "26D generalization of Dirac equation"
    },
    {
      "section": "fermion-sector",
      "description": "Spinor fields"
    }
  ]
}
```

### Dirac Spinors (`dirac-spinor`)

```json
{
  "id": "dirac-spinor",
  "title": "Dirac Spinors",
  "category": "quantum_field_theory",
  "year_established": 1928,
  "badge_type": "established",
  "main_equation": "\u03c8 = (\u03c8\u2081, \u03c8\u2082, \u03c8\u2083, \u03c8\u2084)\u1d40",
  "main_equation_latex": "\\psi = \\begin{pmatrix} \\psi_1 \\\\ \\psi_2 \\\\ \\psi_3 \\\\ \\psi_4 \\end{pmatrix}",
  "summary": "The mathematical objects that describe fermions with spin-1/2 in relativistic quantum mechanics, transforming under Lorentz symmetry in a unique double-valued way.",
  "key_properties": [
    "4-component complex column vector in C\u2074 space",
    "Transform under spinor representation of Lorentz group",
    "Change sign under 360\u00b0 rotation, return to original after 720\u00b0",
    "Decompose into left-handed and right-handed Weyl spinors",
    "Double-valued representation: Spin(3,1) \u2192 SO(3,1) is 2-to-1 map",
    "Arise from Clifford algebra Cl(3,1) representation"
  ],
  "pm_connection": "In PM, the Pneuma field \u03a8\u209a\u0196 is fundamentally a spinor field in higher dimensions. The framework emphasizes fermionic primacy: spinors are the fundamental entities, and bosonic fields emerge from spinor bilinears. After dimensional reduction from 26D bulk (signature 24,2), the Pneuma field becomes a 64-component spinor in the 13D shadow manifold (signature 12,1). The metric tensor emerges from spinor bivector condensates: g_MN ~ \u27e8\u03a8\u0304\u209a \u0393_(MN) \u03a8\u209a\u27e9.",
  "formulas": [
    {
      "id": "dirac-spinor-main",
      "latex": "\\psi = \\begin{pmatrix} \\psi_1 \\\\ \\psi_2 \\\\ \\psi_3 \\\\ \\psi_4 \\end{pmatrix}",
      "plaintext": "\u03c8 = (\u03c8\u2081, \u03c8\u2082, \u03c8\u2083, \u03c8\u2084)\u1d40",
      "description": "4-component Dirac spinor - column vector in complex Hilbert space"
    },
    {
      "id": "weyl-decomposition",
      "latex": "\\psi = \\begin{pmatrix} \\psi_L \\\\ \\psi_R \\end{pmatrix}",
      "plaintext": "\u03c8 = (\u03c8_L, \u03c8_R)\u1d40",
      "description": "Weyl decomposition into left-handed and right-handed components"
    },
    {
      "id": "chirality-projector-left",
      "latex": "\\psi_L = P_L \\psi = \\frac{1}{2}(1 - \\gamma^5)\\psi",
      "plaintext": "\u03c8_L = P_L \u03c8 = (1/2)(1 - \u03b3\u2075)\u03c8",
      "description": "Left-handed chirality projector"
    },
    {
      "id": "chirality-projector-right",
      "latex": "\\psi_R = P_R \\psi = \\frac{1}{2}(1 + \\gamma^5)\\psi",
      "plaintext": "\u03c8_R = P_R \u03c8 = (1/2)(1 + \u03b3\u2075)\u03c8",
      "description": "Right-handed chirality projector"
    },
    {
      "id": "lorentz-transformation",
      "latex": "\\psi(x) \\to \\psi'(x') = S(\\Lambda)\\psi(x)",
      "plaintext": "\u03c8(x) \u2192 \u03c8'(x') = S(\u039b)\u03c8(x)",
      "description": "Spinor transformation under Lorentz transformation \u039b"
    },
    {
      "id": "spin-rotation-matrix",
      "latex": "S(\\Lambda) = \\exp\\left(\\frac{1}{4}\\omega_{\\mu\\nu}\\sigma^{\\mu\\nu}\\right)",
      "plaintext": "S(\u039b) = exp((1/4)\u03c9_\u03bc\u03bd \u03c3^\u03bc\u03bd)",
      "description": "Spin transformation matrix from gamma matrices"
    },
    {
      "id": "clifford-relation",
      "latex": "\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2\\eta^{\\mu\\nu}",
      "plaintext": "{\u03b3^\u03bc, \u03b3^\u03bd} = 2\u03b7^\u03bc\u03bd",
      "description": "Clifford algebra relation for signature \u03b7 = diag(+1,-1,-1,-1)"
    },
    {
      "id": "dirac-adjoint",
      "latex": "\\bar{\\psi} = \\psi^\\dagger \\gamma^0",
      "plaintext": "\u03c8\u0304 = \u03c8\u2020 \u03b3\u2070",
      "description": "Dirac adjoint (row vector)"
    },
    {
      "id": "spinor-dimension-formula",
      "latex": "\\text{dim}(\\text{Spinor}) = 2^{\\lfloor D/2 \\rfloor}",
      "plaintext": "dim(Spinor) = 2^\u230aD/2\u230b",
      "description": "General spinor dimension formula for D-dimensional spacetime"
    },
    {
      "id": "pm-pneuma-spinor-64",
      "latex": "\\Psi_{P,\\text{shadow}} \\in \\mathbb{C}^{64}",
      "plaintext": "\u03a8_P,shadow \u2208 C\u2076\u2074",
      "description": "PM Pneuma spinor: 64 components from Cl(12,1) in 13D shadow manifold"
    },
    {
      "id": "pm-metric-from-spinor",
      "latex": "g_{MN} \\sim \\langle \\bar{\\Psi}_P \\Gamma_{(MN)} \\Psi_P \\rangle",
      "plaintext": "g_MN ~ \u27e8\u03a8\u0304_P \u0393_(MN) \u03a8_P\u27e9",
      "description": "PM: Metric tensor emerges from spinor bivector condensate"
    }
  ]
}
```

### Einstein Field Equations (`einstein-field-equations`)

```json
{
  "id": "einstein-field-equations",
  "title": "Einstein Field Equations",
  "category": "gravity",
  "year_established": 1915,
  "badge_type": "established",
  "main_equation": "G_\u03bc\u03bd + \u039bg_\u03bc\u03bd = 8\u03c0G T_\u03bc\u03bd",
  "main_equation_latex": "G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = 8\\pi G T_{\\mu\\nu}",
  "summary": "The fundamental equations of General Relativity that describe how matter and energy curve spacetime, and how curved spacetime tells matter how to move.",
  "key_properties": [
    "Connects spacetime curvature (Einstein tensor G_\u03bc\u03bd) to matter/energy (stress-energy tensor T_\u03bc\u03bd)",
    "Diffeomorphism invariant (coordinate independent)",
    "Einstein tensor is divergence-free: \u2207^\u03bc G_\u03bc\u03bd = 0",
    "Reduces to Newton's law of gravity in weak-field, slow-velocity limit",
    "Contains cosmological constant \u039b for dark energy",
    "10 independent components (4D symmetric tensor)"
  ],
  "pm_connection": "Principia Metaphysica extends Einstein's General Relativity to higher dimensions in the 2T physics framework. The Einstein Field Equations generalize to each dimensional stage: 26D bulk (24,2), 13D shadow (12,1), 6D bulk (5,1), and 4D observed (3,1). The G\u2082 compactification maintains Ricci-flatness through TCS gluing, with flux corrections modifying the effective geometry. The cosmological constant connects to PM's dark energy prediction w\u2080 = -1.0269.",
  "formulas": [
    {
      "id": "efe-main",
      "latex": "G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = 8\\pi G T_{\\mu\\nu}",
      "plaintext": "G_\u03bc\u03bd + \u039bg_\u03bc\u03bd = 8\u03c0G T_\u03bc\u03bd",
      "description": "Einstein Field Equations with cosmological constant"
    },
    {
      "id": "einstein-tensor",
      "latex": "G_{\\mu\\nu} = R_{\\mu\\nu} - \\frac{1}{2}Rg_{\\mu\\nu}",
      "plaintext": "G_\u03bc\u03bd = R_\u03bc\u03bd - (1/2)Rg_\u03bc\u03bd",
      "description": "Einstein tensor from Ricci tensor and Ricci scalar"
    },
    {
      "id": "line-element",
      "latex": "ds^2 = g_{\\mu\\nu} dx^\\mu dx^\\nu",
      "plaintext": "ds\u00b2 = g_\u03bc\u03bd dx^\u03bc dx^\u03bd",
      "description": "Spacetime interval (line element)"
    },
    {
      "id": "schwarzschild-metric",
      "latex": "ds^2 = -\\left(1 - \\frac{2GM}{r}\\right)dt^2 + \\left(1 - \\frac{2GM}{r}\\right)^{-1}dr^2 + r^2 d\\Omega^2",
      "plaintext": "ds\u00b2 = -(1 - 2GM/r)dt\u00b2 + (1 - 2GM/r)\u207b\u00b9dr\u00b2 + r\u00b2d\u03a9\u00b2",
      "description": "Schwarzschild metric around spherical mass"
    },
    {
      "id": "pm-efe-26d",
      "latex": "G_{AB} + \\Lambda_{26} g_{AB} = 8\\pi G_{26} T_{AB}",
      "plaintext": "G_AB + \u039b_26 g_AB = 8\u03c0G_26 T_AB",
      "description": "PM: Einstein equations in 26D bulk with signature (24,2)"
    },
    {
      "id": "pm-efe-13d",
      "latex": "G_{MN} + \\Lambda_{13} g_{MN} = 8\\pi G_{13} T_{MN}",
      "plaintext": "G_MN + \u039b_13 g_MN = 8\u03c0G_13 T_MN",
      "description": "PM: Einstein equations in 13D shadow after Sp(2,R) gauge fixing"
    },
    {
      "id": "pm-g2-ricci-flat",
      "latex": "\\text{Ric}(g_{G_2}) = 0",
      "plaintext": "Ric(g_G\u2082) = 0",
      "description": "PM: G\u2082 manifold is Ricci-flat (satisfies vacuum Einstein equations)"
    },
    {
      "id": "pm-flux-corrected-efe",
      "latex": "G_{\\mu\\nu} = 8\\pi G\\left(T_{\\mu\\nu} + T_{\\mu\\nu}^{\\text{flux}}\\right)",
      "plaintext": "G_\u03bc\u03bd = 8\u03c0G(T_\u03bc\u03bd + T_\u03bc\u03bd^flux)",
      "description": "PM: Flux corrections modify effective geometry"
    }
  ]
}
```

### Einstein-Hilbert Action (`einstein-hilbert-action`)

```json
{
  "id": "einstein-hilbert-action",
  "title": "Einstein-Hilbert Action",
  "category": "gravity",
  "year_established": 1915,
  "badge_type": "established",
  "main_equation": "S = (1/16\u03c0G) \u222b d\u2074x \u221a|g| R",
  "main_equation_latex": "S = \\frac{1}{16\\pi G} \\int d^4x \\sqrt{|g|} R",
  "summary": "The action principle from which Einstein's field equations of General Relativity are derived through variational calculus.",
  "key_properties": [
    "Variational principle: extremizing \u03b4S = 0 yields Einstein field equations",
    "Proportional to total curvature integrated over spacetime",
    "Coordinate invariant (diffeomorphism invariant)",
    "Factor 1/16\u03c0G ensures correct coupling strength",
    "\u221a|g| ensures proper volume element in curved spacetime",
    "R = Ricci scalar measures total curvature"
  ],
  "pm_connection": "In Principia Metaphysica, the Einstein-Hilbert action generalizes to 26 dimensions with signature (24,2) in the 2T physics framework. The action undergoes dimensional reduction: 26D (24,2) bulk \u2192 13D (12,1) shadow via Sp(2,R) gauge fixing \u2192 6D bulk via G\u2082 compactification \u2192 4D observed. The 4D Planck mass emerges from compactification: M_Pl\u00b2 = M_*\u00b2\u2074 \u00d7 V_22, where V_22 is the 22-dimensional compact volume.",
  "formulas": [
    {
      "id": "eh-action-4d",
      "latex": "S_{\\text{EH}} = \\frac{1}{16\\pi G} \\int d^4x \\sqrt{|g|} R",
      "plaintext": "S_EH = (1/16\u03c0G) \u222b d\u2074x \u221a|g| R",
      "description": "4D Einstein-Hilbert action"
    },
    {
      "id": "pm-eh-action-26d",
      "latex": "S_{26D} = M_*^{24} \\int d^{26}X \\sqrt{|G_{(24,2)}|} R_{26}",
      "plaintext": "S_26D = M_*\u00b2\u2074 \u222b d\u00b2\u2076X \u221a|G_(24,2)| R_26",
      "description": "PM: 26D Einstein-Hilbert action with signature (24,2)"
    },
    {
      "id": "pm-eh-action-14x2",
      "latex": "S_{14\\times 2} = M_*^{24} \\int \\left[d^{14}x_1 \\sqrt{|g_1|} R_{14,1} + d^{14}x_2 \\sqrt{|g_2|} R_{14,2}\\right]",
      "plaintext": "S_14\u00d72 = M_*\u00b2\u2074 \u222b [d\u00b9\u2074x\u2081 \u221a|g\u2081| R_14,1 + d\u00b9\u2074x\u2082 \u221a|g\u2082| R_14,2]",
      "description": "PM: After Sp(2,R) gauge fixing to dual 14D sectors"
    },
    {
      "id": "pm-eh-action-7x2",
      "latex": "S_{7\\times 2} = M_7^5 \\int \\left[d^7x_1 \\sqrt{|h_1|} R_{7,1} + d^7x_2 \\sqrt{|h_2|} R_{7,2}\\right]",
      "plaintext": "S_7\u00d72 = M_7\u2075 \u222b [d\u2077x\u2081 \u221a|h\u2081| R_7,1 + d\u2077x\u2082 \u221a|h\u2082| R_7,2]",
      "description": "PM: After G\u2082 compactification to dual 7D sectors"
    },
    {
      "id": "pm-eh-action-4d",
      "latex": "S_{4D} = M_{\\text{Pl}}^2 \\int d^4x \\sqrt{|g|} R",
      "plaintext": "S_4D = M_Pl\u00b2 \u222b d\u2074x \u221a|g| R",
      "description": "PM: 4D effective action after full compactification"
    },
    {
      "id": "pm-planck-mass-kk",
      "latex": "M_{\\text{Pl}}^2 = M_*^{24} \\times V_{22}",
      "plaintext": "M_Pl\u00b2 = M_*\u00b2\u2074 \u00d7 V_22",
      "description": "PM: 4D Planck mass from Kaluza-Klein compactification"
    },
    {
      "id": "pm-v22-volume",
      "latex": "V_{22} = \\text{Vol}(M_1^7) \\times \\text{Vol}(M_2^7) \\times (\\text{Sp}(2,\\mathbb{R}) \\text{ volume factor})",
      "plaintext": "V_22 = Vol(M\u2081\u2077) \u00d7 Vol(M\u2082\u2077) \u00d7 (Sp(2,R) volume factor)",
      "description": "PM: 22-dimensional compact volume"
    }
  ]
}
```

### G₂ Manifolds (`g2-manifolds`)

```json
{
  "id": "g2-manifolds",
  "title": "G\u2082 Manifolds",
  "category": "geometry",
  "year_established": 1987,
  "badge_type": "established",
  "main_equation": "d\u03c6 = 0 and d(*\u03c6) = 0",
  "main_equation_latex": "d\\varphi = 0 \\quad \\text{and} \\quad d(\\star\\varphi) = 0",
  "summary": "7-dimensional Riemannian manifolds with holonomy group G\u2082, the smallest exceptional Lie group. These manifolds are Ricci-flat and preserve N=1 supersymmetry in M-theory compactifications.",
  "key_properties": [
    "7-dimensional with holonomy group G\u2082 \u2282 SO(7)",
    "Ricci-flat: Ric(g) = 0 (satisfy vacuum Einstein equations)",
    "Exactly one parallel spinor (8 real components)",
    "Defined by associative 3-form \u03c6 satisfying d\u03c6 = 0 and d(*\u03c6) = 0",
    "No complex structure (purely real geometry)",
    "Preserves N=1 supersymmetry in 4D after M-theory compactification",
    "Bare Euler characteristic \u03c7(G\u2082) = 0 for smooth compact G\u2082 manifolds"
  ],
  "pm_connection": "In PM's 2T physics framework, the 13D shadow (from 26D bulk via Sp(2,R) gauge fixing) compactifies on a 7D G\u2082 manifold constructed via Twisted Connected Sum (TCS). The specific construction uses extra-twisted TCS with involution blocks 3.25\u2081 and 3.25\u2082, gluing angle \u03b8 = \u03c0/6, yielding Betti numbers b\u2082 = 4, b\u2083 = 24. G\u2084 flux backreaction modifies bare topology \u03c7 = 0 to effective \u03c7_eff = 72 per G\u2082 copy, giving 3 fermion generations via n_gen = \u03c7_eff/24 = 3. D\u2085 ADE singularities provide SO(10) GUT gauge group. The GUT scale M_GUT = 2.118\u00d710\u00b9\u2076 GeV emerges topologically via logarithmic torsion formula. Total internal space: V\u2089 = V\u2087(G\u2082) \u00d7 V\u2082(T\u00b2).",
  "formulas": [
    {
      "id": "g2-defining-equations",
      "latex": "d\\varphi = 0 \\quad \\text{and} \\quad d(\\star\\varphi) = 0",
      "plaintext": "d\u03c6 = 0 and d(*\u03c6) = 0",
      "description": "Defining equations for torsion-free G\u2082 structure"
    },
    {
      "id": "g2-ricci-flat",
      "latex": "\\text{Ric}(g) = 0",
      "plaintext": "Ric(g) = 0",
      "description": "G\u2082 manifolds are Ricci-flat"
    },
    {
      "id": "g2-parallel-spinor",
      "latex": "\\nabla \\eta = 0",
      "plaintext": "\u2207\u03b7 = 0",
      "description": "Unique parallel spinor \u03b7 (8 real components)"
    },
    {
      "id": "pm-g2-tcs",
      "latex": "M^7 = M_1^7 \\cup_{S^3 \\times S^1} M_2^7",
      "plaintext": "M\u2077 = M\u2081\u2077 \u222a_S\u00b3\u00d7S\u00b9 M\u2082\u2077",
      "description": "PM: Twisted Connected Sum construction"
    },
    {
      "id": "pm-g2-bare-euler",
      "latex": "\\chi(M^7) = 0",
      "plaintext": "\u03c7(M\u2077) = 0",
      "description": "PM: Bare Euler characteristic (before flux)"
    },
    {
      "id": "pm-g2-flux-dressed-euler",
      "latex": "\\chi_{\\text{eff}}(M^7) = 72",
      "plaintext": "\u03c7_eff(M\u2077) = 72",
      "description": "PM: Flux-dressed effective Euler characteristic per G\u2082 copy"
    },
    {
      "id": "pm-g2-generation-count",
      "latex": "n_{\\text{gen}} = \\frac{\\chi_{\\text{eff}}}{24} = \\frac{72}{24} = 3",
      "plaintext": "n_gen = \u03c7_eff/24 = 72/24 = 3",
      "description": "PM: 3 fermion generations from flux-dressed topology"
    },
    {
      "id": "pm-g2-total-euler",
      "latex": "\\chi_{\\text{total}} = 144",
      "plaintext": "\u03c7_total = 144",
      "description": "PM: Total Euler characteristic from dual G\u2082 pair"
    },
    {
      "id": "pm-g2-betti-2",
      "latex": "b_2(M) = 4",
      "plaintext": "b\u2082(M) = 4",
      "description": "PM: Second Betti number (associative 3-cycles)"
    },
    {
      "id": "pm-g2-betti-3",
      "latex": "b_3(M) = 24",
      "plaintext": "b\u2083(M) = 24",
      "description": "PM: Third Betti number (coassociative 4-cycles)"
    },
    {
      "id": "pm-g2-torsion-invariant",
      "latex": "\\nu = 24",
      "plaintext": "\u03bd = 24",
      "description": "PM: Crowley-Nordenstam torsion invariant mod 48"
    },
    {
      "id": "pm-g2-gut-scale-formula",
      "latex": "\\ln\\left(\\frac{M_{\\text{GUT}}}{M_{\\text{Planck}}}\\right) = -2\\pi \\frac{b_2 + b_3}{\\nu}",
      "plaintext": "ln(M_GUT/M_Planck) = -2\u03c0(b\u2082 + b\u2083)/\u03bd",
      "description": "PM: Torsion logarithm formula for GUT scale"
    },
    {
      "id": "pm-g2-gut-scale-value",
      "latex": "M_{\\text{GUT}} = M_{\\text{Planck}} \\times e^{-7.33} = 2.118 \\times 10^{16} \\text{ GeV}",
      "plaintext": "M_GUT = M_Planck \u00d7 e^(-7.33) = 2.118\u00d710\u00b9\u2076 GeV",
      "description": "PM: GUT scale from torsion topology"
    },
    {
      "id": "pm-g2-v9-volume",
      "latex": "V_9 = V_7(G_2) \\times V_2(T^2)",
      "plaintext": "V\u2089 = V\u2087(G\u2082) \u00d7 V\u2082(T\u00b2)",
      "description": "PM: 9D internal volume factorization"
    },
    {
      "id": "pm-g2-susy-preservation",
      "latex": "\\text{Hol}(g) \\subseteq G_2 \\quad \\Rightarrow \\quad N=1 \\text{ SUSY preserved}",
      "plaintext": "Hol(g) \u2286 G\u2082 \u2192 N=1 SUSY preserved",
      "description": "PM: G\u2082 holonomy preserves N=1 supersymmetry in 4D"
    },
    {
      "id": "pm-g2-flux-quantization",
      "latex": "\\int_{\\Sigma_4} \\frac{G_4}{2\\pi \\ell_P^3} \\in \\mathbb{Z}",
      "plaintext": "\u222b_\u03a3\u2084 G\u2084/(2\u03c0\u2113_P\u00b3) \u2208 \u2124",
      "description": "PM: G\u2084 flux quantization condition"
    },
    {
      "id": "pm-g2-dimensional-reduction",
      "latex": "26D(24,2) \\xrightarrow{\\text{Sp}(2,\\mathbb{R})} 14D_1(12,2) \\otimes 14D_2(12,2) \\xrightarrow{G_2} 7D_1 \\otimes 7D_2 \\xrightarrow{\\text{shared time}} 4D(3,1)",
      "plaintext": "26D(24,2) --[Sp(2,R)]--> 14D\u2081(12,2)\u229714D\u2082(12,2) --[G\u2082]--> 7D\u2081\u22977D\u2082 --[shared time]--> 4D(3,1)",
      "description": "PM: Full dimensional reduction pathway in 2T framework"
    }
  ]
}
```

### Hawking Temperature (`hawking-temperature`)

```json
{
  "id": "hawking-temperature",
  "title": "Hawking Temperature",
  "category": "thermodynamics",
  "year_established": 1974,
  "badge_type": "established",
  "main_equation": "T_H = \u210fc\u00b3/(8\u03c0GMk_B) = \u210f\u03ba/(2\u03c0ck_B)",
  "main_equation_latex": "T_H = \\frac{\\hbar c^3}{8\\pi G M k_B} = \\frac{\\hbar \\kappa}{2\\pi c k_B}",
  "summary": "The temperature at which black holes emit thermal radiation, unifying quantum mechanics, general relativity, and thermodynamics.",
  "key_properties": [
    "Black holes are not completely black\u2014they emit thermal radiation at a temperature inversely proportional to their mass",
    "T_H \u221d 1/M: Smaller black holes are hotter and evaporate faster",
    "Contains \u210f (quantum), G (gravity), and c (relativity)\u2014a window into quantum gravity",
    "Surface gravity \u03ba at the event horizon determines the temperature",
    "For a solar mass black hole: T_H \u2248 60 nanokelvin (much colder than the CMB)",
    "Evaporation time scales as t_evap \u221d M\u00b3, making stellar-mass black holes effectively eternal",
    "Primordial black holes of mass ~10\u00b9\u2075 g could be evaporating now",
    "Leads to the black hole information paradox: how is quantum information preserved during evaporation?"
  ],
  "pm_connection": "Hawking temperature plays a crucial role in PM's treatment of black holes and dimensional reduction. In the thermal time hypothesis, Hawking radiation provides a concrete example where the vacuum state satisfies the KMS condition with \u03b2_H = 1/(k_B T_H). The modular flow generates evolution at the horizon, with temperature emerging from geometry (surface gravity \u03ba). PM extends black hole thermodynamics to the 26D bulk, where higher-dimensional horizons have different topology and thermodynamics. In Kaluza-Klein black holes, compactified dimensions affect black hole properties. The Hawking temperature indicates where quantum gravity becomes important: near the Planck mass M_Planck = \u221a(\u210fc/G), the semiclassical approximation breaks down and PM's higher-dimensional quantum geometry becomes relevant.",
  "formulas": [
    {
      "name": "Hawking Temperature (Mass Form)",
      "equation": "T_H = \u210fc\u00b3/(8\u03c0GMk_B)",
      "latex": "T_H = \\frac{\\hbar c^3}{8\\pi G M k_B}",
      "description": "Temperature as a function of black hole mass M. Inversely proportional to mass."
    },
    {
      "name": "Hawking Temperature (Surface Gravity Form)",
      "equation": "T_H = \u210f\u03ba/(2\u03c0ck_B)",
      "latex": "T_H = \\frac{\\hbar \\kappa}{2\\pi c k_B}",
      "description": "Temperature expressed in terms of surface gravity \u03ba at the event horizon."
    },
    {
      "name": "Surface Gravity (Schwarzschild)",
      "equation": "\u03ba = c\u2074/(4GM) = GM/r_s\u00b2",
      "latex": "\\kappa = \\frac{c^4}{4GM} = \\frac{GM}{r_s^2}",
      "description": "Surface gravity for a Schwarzschild black hole, where r_s = 2GM/c\u00b2 is the Schwarzschild radius."
    },
    {
      "name": "Bekenstein-Hawking Entropy",
      "equation": "S_BH = k_B A/(4\u2113_P\u00b2) = k_B c\u00b3A/(4\u210fG)",
      "latex": "S_{BH} = \\frac{k_B A}{4\\ell_P^2} = \\frac{k_B c^3 A}{4\\hbar G}",
      "description": "Black hole entropy proportional to horizon area A. Holographic principle."
    },
    {
      "name": "Evaporation Time",
      "equation": "t_evap = (5120\u03c0G\u00b2M\u00b3)/(\u210fc\u2074)",
      "latex": "t_{evap} = \\frac{5120\\pi G^2 M^3}{\\hbar c^4}",
      "description": "Time for a Schwarzschild black hole to completely evaporate via Hawking radiation."
    },
    {
      "name": "First Law of Black Hole Thermodynamics",
      "equation": "dM = (\u03ba/8\u03c0G)dA + \u03a9_H dJ + \u03a6_H dQ",
      "latex": "dM = \\frac{\\kappa}{8\\pi G}dA + \\Omega_H dJ + \\Phi_H dQ",
      "description": "Analogue of thermodynamic first law for black holes with rotation and charge."
    },
    {
      "name": "Kerr Black Hole Temperature",
      "equation": "T_H = \u210fc\u00b3(r\u208a - r\u208b)/(4\u03c0Gk_B(r\u208a\u00b2 + a\u00b2))",
      "latex": "T_H = \\frac{\\hbar c^3 (r_+ - r_-)}{4\\pi G k_B (r_+^2 + a^2)}",
      "description": "Hawking temperature for rotating (Kerr) black hole with spin parameter a = J/(Mc)."
    },
    {
      "name": "Unruh Temperature",
      "equation": "T_U = \u210fa/(2\u03c0ck_B)",
      "latex": "T_U = \\frac{\\hbar a}{2\\pi c k_B}",
      "description": "Temperature experienced by an accelerating observer with proper acceleration a. Related to Hawking temperature via equivalence principle."
    }
  ]
}
```

### Kaluza-Klein Theory (`kaluza-klein`)

```json
{
  "id": "kaluza-klein",
  "title": "Kaluza-Klein Theory",
  "category": "dimensional_reduction",
  "year_established": 1921,
  "badge_type": "established",
  "main_equation": "Higher D \u2192 4D | Compactification on S\u00b9",
  "main_equation_latex": "\\text{Higher } D \\rightarrow 4D \\quad | \\quad \\text{Compactification on } S^1",
  "summary": "The groundbreaking theory showing how extra spatial dimensions can be 'curled up' so small they become invisible, unifying gravity and electromagnetism in higher dimensions.",
  "key_properties": [
    "Extra dimensions can be compactified (curled up) to such small sizes that they're invisible at low energies",
    "Like a garden hose looks 1D from far away but is really 2D with a tiny circular dimension",
    "Motion in the compact dimension appears as massive particles in 4D with mass m_n = n/R",
    "The n=0 mode is massless and corresponds to the 4D fields we observe (photon, graviton)",
    "Heavy KK modes (n\u22651) are too massive to produce at current energies",
    "Current LHC limit: R < 10\u207b\u00b9\u2079 m from lack of observed KK modes",
    "5D metric component g_\u03bc5 becomes the electromagnetic potential A_\u03bc in 4D",
    "Kaluza-Klein theory is the foundation for string theory's extra dimensions"
  ],
  "pm_connection": "Principia Metaphysica employs a multi-stage compactification process from 26D down to the observed 4D. The pathway is: 26D \u2192 13D \u2192 6D \u2192 4D. The 26D \u2192 13D stage involves Sp(2,R) gauge fixing in 2T physics (not standard KK compactification but gauge-theoretic reduction). The 13D \u2192 6D stage uses a G\u2082 manifold compactification (7D with holonomy G\u2082), preserving N=1 supersymmetry. The specific construction is TCS G\u2082 with b\u2082=4, b\u2083=24, \u03c7=-540. The KK mass scale is m_KK ~ 1/R_G\u2082 where R_G\u2082 ~ 10\u207b\u00b3\u2075 m (Planck scale). Finally, 6D \u2192 4D involves further compactification on a 2D surface. Unlike single-scale KK theory, PM has multiple compactification scales at different stages, potentially explaining the hierarchy problem. PM likely employs flux compactification to stabilize the moduli (size and shape of compact dimensions), with background fluxes generating a potential that fixes the compactification radius.",
  "formulas": [
    {
      "name": "5D Kaluza-Klein Metric",
      "equation": "ds\u00b2\u208d\u2085D\u208e = g_\u03bc\u03bd dx^\u03bc dx^\u03bd + \u03c6\u00b2(dy + A_\u03bc dx^\u03bc)\u00b2",
      "latex": "ds^2_{(5D)} = g_{\\mu\\nu} dx^\\mu dx^\\nu + \\phi^2(dy + A_\\mu dx^\\mu)^2",
      "description": "5D metric decomposed into 4D metric g_\u03bc\u03bd, gauge field A_\u03bc (photon), and radion \u03c6 (dilaton)."
    },
    {
      "name": "KK Mass Spectrum",
      "equation": "m_n\u00b2 = (n/R)\u00b2",
      "latex": "m_n^2 = \\left(\\frac{n}{R}\\right)^2",
      "description": "Tower of massive states from quantized momentum in compact dimension. n = 0,1,2,3,..."
    },
    {
      "name": "Compactification Periodicity",
      "equation": "y\u2085 ~ y\u2085 + 2\u03c0R",
      "latex": "y_5 \\sim y_5 + 2\\pi R",
      "description": "Periodic identification for circle compactification of radius R."
    },
    {
      "name": "KK Mode Wavefunction",
      "equation": "\u03c8_n(y) = e^(iny/R) / \u221a(2\u03c0R)",
      "latex": "\\psi_n(y) = \\frac{e^{iny/R}}{\\sqrt{2\\pi R}}",
      "description": "Normalized wavefunction for nth KK mode in compact direction."
    },
    {
      "name": "Higher-Dimensional Bekenstein-Hawking Entropy",
      "equation": "S_BH = k_B A_{d-2} / (4\u2113_{P,d}^{d-2})",
      "latex": "S_{BH} = \\frac{k_B A_{d-2}}{4\\ell_{P,d}^{d-2}}",
      "description": "Black hole entropy in d spacetime dimensions, generalizing 4D formula."
    },
    {
      "name": "Fundamental vs Observed Planck Scale (ADD Model)",
      "equation": "M_Pl\u00b2 ~ M_*^{n+2} R^n",
      "latex": "M_{Pl}^2 \\sim M_*^{n+2} R^n",
      "description": "Relation between 4D Planck scale M_Pl and fundamental scale M_* with n extra dimensions of size R."
    }
  ]
}
```

### KMS Condition (`kms-condition`)

```json
{
  "id": "kms-condition",
  "title": "KMS Condition",
  "category": "thermal_qft",
  "year_established": 1967,
  "badge_type": "established",
  "main_equation": "\u27e8AB\u27e9_\u03b2 = \u27e8B \u03b1_{i\u03b2}(A)\u27e9",
  "main_equation_latex": "\\langle AB \\rangle_\\beta = \\langle B \\alpha_{i\\beta}(A) \\rangle",
  "summary": "The mathematical condition characterizing thermal equilibrium states in quantum field theory, connecting temperature to the analytic structure of correlation functions.",
  "key_properties": [
    "Thermal states exhibit periodicity in imaginary time with period \u03b2 = 1/(k_B T)",
    "Left side \u27e8AB\u27e9_\u03b2 is the thermal correlation between operators A and B",
    "Right side \u03b1_{i\u03b2}(A) is the operator A evolved in imaginary time by i\u03b2 (modular automorphism)",
    "Relates correlation functions to their analytically continued counterparts",
    "Correlation functions are analytic in the strip 0 < Im(t) < \u03b2",
    "Boundary conditions at Im(t) = 0 and Im(t) = \u03b2 give the KMS relation",
    "Generalizes thermal equilibrium beyond systems with a Hamiltonian to arbitrary quantum systems",
    "Appears naturally in curved spacetime: Hawking radiation and Unruh effect satisfy KMS condition"
  ],
  "pm_connection": "The KMS condition plays a crucial role in the thermodynamic properties of the pneuma field and the emergence of time in PM. In the thermal time hypothesis, the flow of time emerges from the thermal properties of quantum states. The modular flow \u03c3_t from the KMS condition provides a notion of 'thermal time' independent of external clocks. Physical time is identified with modular automorphism evolution, with inverse temperature \u03b2 setting the timescale for thermal processes. The pneuma field \u03a8 in the 26D bulk exhibits thermal characteristics related to dimensional reduction. Dimensional compactification induces effective thermal states, and each dimensional shadow (26D \u2192 13D \u2192 6D \u2192 4D) has associated KMS thermal properties. The holographic thermality relates KMS states in different dimensions via bulk-boundary correspondence. The observed CMB temperature T_CMB = 2.725 K connects to the KMS condition for the cosmological horizon, with horizon thermality exhibited by both cosmological and black hole horizons. The CMB temperature serves as a fossil record of early universe thermalization.",
  "formulas": [
    {
      "name": "KMS Condition",
      "equation": "\u27e8AB\u27e9_\u03b2 = \u27e8B \u03b1_{i\u03b2}(A)\u27e9",
      "latex": "\\langle AB \\rangle_\\beta = \\langle B \\alpha_{i\\beta}(A) \\rangle",
      "description": "Fundamental KMS relation for thermal states at inverse temperature \u03b2 = 1/(k_B T)."
    },
    {
      "name": "Thermal Density Matrix",
      "equation": "\u03c1_\u03b2 = e^{-\u03b2H} / Z",
      "latex": "\\rho_\\beta = \\frac{e^{-\\beta H}}{Z}",
      "description": "Gibbs thermal state with partition function Z = Tr(e^{-\u03b2H})."
    },
    {
      "name": "Thermal Expectation Value",
      "equation": "\u27e8A\u27e9_\u03b2 = Tr(e^{-\u03b2H}A)/Z",
      "latex": "\\langle A \\rangle_\\beta = \\frac{\\text{Tr}(e^{-\\beta H}A)}{Z}",
      "description": "Expectation value in the thermal state."
    },
    {
      "name": "Time Evolution Automorphism",
      "equation": "\u03b1_t(A) = e^{iHt} A e^{-iHt}",
      "latex": "\\alpha_t(A) = e^{iHt} A e^{-iHt}",
      "description": "Heisenberg time evolution. For imaginary time t \u2192 i\u03b2, becomes modular flow."
    },
    {
      "name": "Euclidean Correlation Function",
      "equation": "G(\u03c4) = \u27e8A(\u03c4)B(0)\u27e9_\u03b2 = Tr(e^{-\u03b2H} A(e^{-H\u03c4})B e^{H\u03c4})/Z",
      "latex": "G(\\tau) = \\langle A(\\tau)B(0) \\rangle_\\beta = \\frac{\\text{Tr}(e^{-\\beta H} A(e^{-H\\tau})B e^{H\\tau})}{Z}",
      "description": "Correlation function in imaginary (Euclidean) time, periodic with period \u03b2."
    },
    {
      "name": "Imaginary Time Periodicity",
      "equation": "G(\u03c4 + \u03b2) = G(\u03c4)",
      "latex": "G(\\tau + \\beta) = G(\\tau)",
      "description": "Thermal Green's functions are periodic in imaginary time with period \u03b2."
    },
    {
      "name": "Hawking Temperature (KMS Form)",
      "equation": "T_H = \u210fc\u00b3/(8\u03c0Gk_B M) = \u210f\u03ba/(2\u03c0ck_B)",
      "latex": "T_H = \\frac{\\hbar c^3}{8\\pi G k_B M} = \\frac{\\hbar \\kappa}{2\\pi c k_B}",
      "description": "Black holes emit thermal radiation satisfying KMS condition with this temperature."
    },
    {
      "name": "Unruh Temperature (KMS Form)",
      "equation": "T_U = \u210fa/(2\u03c0ck_B)",
      "latex": "T_U = \\frac{\\hbar a}{2\\pi c k_B}",
      "description": "Accelerating observer sees Minkowski vacuum as thermal bath at this temperature, satisfying KMS."
    },
    {
      "name": "Modular Automorphism (General)",
      "equation": "\u03c3_t(A) = \u0394^{it} A \u0394^{-it}",
      "latex": "\\sigma_t(A) = \\Delta^{it} A \\Delta^{-it}",
      "description": "Modular automorphism from Tomita-Takesaki theory, generalizing thermal time evolution."
    }
  ]
}
```

### Metric Tensor (`metric-tensor`)

```json
{
  "id": "metric-tensor",
  "title": "Metric Tensor",
  "category": "differential_geometry",
  "year_established": 1854,
  "badge_type": "established",
  "main_equation": "ds\u00b2 = g_\u03bc\u03bd dx^\u03bc dx^\u03bd",
  "main_equation_latex": "ds^2 = g_{\\mu\\nu} dx^\\mu dx^\\nu",
  "summary": "The fundamental mathematical object that encodes the geometry of spacetime, defining distances, angles, and the causal structure of the universe.",
  "key_properties": [
    "The metric tensor g_\u03bc\u03bd tells you how to measure distances and time intervals in curved spacetime",
    "Line element ds\u00b2 generalizes the Pythagorean theorem to curved spaces",
    "Metric signature determines which directions are timelike, spacelike, or null",
    "Standard 4D signature: (3,1) or (-,+,+,+) representing 3 space + 1 time dimensions",
    "Contains all geometric information: distances, angles, volumes, geodesics, and curvature derive from g_\u03bc\u03bd",
    "Invariant under coordinate transformations: all observers agree on ds\u00b2",
    "In 4D, the metric is a symmetric matrix with 10 independent components",
    "Inverse metric g^\u03bc\u03bd is used to raise indices and compute curvature tensors"
  ],
  "pm_connection": "The metric tensor is fundamental to PM's geometric framework. At each dimensional stage, a metric defines the geometry with specific signatures. The 26D bulk metric g_AB^(26) has signature (24,2) - two timelike directions allowing Sp(2,R) gauge symmetry. The extra time dimension enables causal paradox resolution. After Sp(2,R) gauge fixing, the 13D shadow metric g_MN^(13) has signature (12,1), returning to standard (n-1,1) signature spacetime. The 6D bulk metric g_\u03bc\u03bd^(6) has signature (5,1), with the G\u2082 manifold internal space contributing to this geometry. Finally, the observed 4D metric g_\u03bc\u03bd^(4) has signature (3,1), the standard spacetime metric we measure. The line element generalizes at each stage: ds\u00b2 = g_AB^(D) dx^A dx^B. The (n,2) signature in higher dimensions is essential for two-time physics. The Sp(2,R) gauge symmetry acts on the two timelike directions, and gauge fixing reduces to a single observed time dimension, resolving the apparent contradiction while maintaining mathematical consistency. All curvature quantities (Ricci tensor, Einstein tensor) are ultimately derived from the metric at each dimensional stage.",
  "formulas": [
    {
      "name": "Spacetime Interval (Line Element)",
      "equation": "ds\u00b2 = g_\u03bc\u03bd dx^\u03bc dx^\u03bd",
      "latex": "ds^2 = g_{\\mu\\nu} dx^\\mu dx^\\nu",
      "description": "Infinitesimal distance between nearby events in spacetime. Invariant under coordinate transformations."
    },
    {
      "name": "Minkowski Metric",
      "equation": "\u03b7_\u03bc\u03bd = diag(-1, 1, 1, 1)",
      "latex": "\\eta_{\\mu\\nu} = \\text{diag}(-1, 1, 1, 1)",
      "description": "Flat spacetime metric for Special Relativity. Signature (3,1) or (-,+,+,+)."
    },
    {
      "name": "Minkowski Line Element",
      "equation": "ds\u00b2 = -dt\u00b2 + dx\u00b2 + dy\u00b2 + dz\u00b2",
      "latex": "ds^2 = -dt^2 + dx^2 + dy^2 + dz^2",
      "description": "Flat spacetime interval in Cartesian coordinates."
    },
    {
      "name": "Schwarzschild Metric",
      "equation": "ds\u00b2 = -(1-r_s/r)dt\u00b2 + (1-r_s/r)\u207b\u00b9dr\u00b2 + r\u00b2d\u03a9\u00b2",
      "latex": "ds^2 = -\\left(1-\\frac{r_s}{r}\\right)dt^2 + \\left(1-\\frac{r_s}{r}\\right)^{-1}dr^2 + r^2 d\\Omega^2",
      "description": "Metric around a non-rotating spherical mass or black hole. r_s = 2GM/c\u00b2 is Schwarzschild radius."
    },
    {
      "name": "FLRW Metric",
      "equation": "ds\u00b2 = -dt\u00b2 + a(t)\u00b2[dr\u00b2/(1-kr\u00b2) + r\u00b2d\u03a9\u00b2]",
      "latex": "ds^2 = -dt^2 + a(t)^2\\left[\\frac{dr^2}{1-kr^2} + r^2 d\\Omega^2\\right]",
      "description": "Friedmann-Lema\u00eetre-Robertson-Walker metric for expanding universe. a(t) is scale factor, k is curvature."
    },
    {
      "name": "Inverse Metric Relation",
      "equation": "g^{\u03bc\u03bb}g_{\u03bb\u03bd} = \u03b4^\u03bc_\u03bd",
      "latex": "g^{\\mu\\lambda}g_{\\lambda\\nu} = \\delta^\\mu_\\nu",
      "description": "Inverse metric g^\u03bc\u03bd satisfies this relation (Kronecker delta on right side)."
    },
    {
      "name": "Index Raising",
      "equation": "V^\u03bc = g^{\u03bc\u03bd} V_\u03bd",
      "latex": "V^\\mu = g^{\\mu\\nu} V_\\nu",
      "description": "Convert covariant vector to contravariant using inverse metric."
    },
    {
      "name": "Index Lowering",
      "equation": "V_\u03bc = g_{\u03bc\u03bd} V^\u03bd",
      "latex": "V_\\mu = g_{\\mu\\nu} V^\\nu",
      "description": "Convert contravariant vector to covariant using metric."
    },
    {
      "name": "Proper Time",
      "equation": "d\u03c4\u00b2 = -ds\u00b2/c\u00b2",
      "latex": "d\\tau^2 = -\\frac{ds^2}{c^2}",
      "description": "Proper time along timelike worldline. Time measured by a clock following the path."
    },
    {
      "name": "Christoffel Symbols",
      "equation": "\u0393^\u03bb_{\u03bc\u03bd} = \u00bd g^{\u03bb\u03c1}(\u2202_\u03bc g_{\u03bd\u03c1} + \u2202_\u03bd g_{\u03c1\u03bc} - \u2202_\u03c1 g_{\u03bc\u03bd})",
      "latex": "\\Gamma^\\lambda_{\\mu\\nu} = \\frac{1}{2} g^{\\lambda\\rho}(\\partial_\\mu g_{\\nu\\rho} + \\partial_\\nu g_{\\rho\\mu} - \\partial_\\rho g_{\\mu\\nu})",
      "description": "Connection coefficients derived from metric. Describe parallel transport and geodesics."
    },
    {
      "name": "Volume Element",
      "equation": "d^4x \u221a|g|",
      "latex": "d^4x \\sqrt{|g|}",
      "description": "Invariant volume element in curved spacetime. g = det(g_\u03bc\u03bd)."
    },
    {
      "name": "Riemann Curvature Tensor (from metric)",
      "equation": "R^\u03c1_{\u03c3\u03bc\u03bd} = \u2202_\u03bc \u0393^\u03c1_{\u03bd\u03c3} - \u2202_\u03bd \u0393^\u03c1_{\u03bc\u03c3} + \u0393^\u03c1_{\u03bc\u03bb}\u0393^\u03bb_{\u03bd\u03c3} - \u0393^\u03c1_{\u03bd\u03bb}\u0393^\u03bb_{\u03bc\u03c3}",
      "latex": "R^\\rho_{\\sigma\\mu\\nu} = \\partial_\\mu \\Gamma^\\rho_{\\nu\\sigma} - \\partial_\\nu \\Gamma^\\rho_{\\mu\\sigma} + \\Gamma^\\rho_{\\mu\\lambda}\\Gamma^\\lambda_{\\nu\\sigma} - \\Gamma^\\rho_{\\nu\\lambda}\\Gamma^\\lambda_{\\mu\\sigma}",
      "description": "Full curvature tensor derived from Christoffel symbols (and thus from metric)."
    }
  ]
}
```

### Ricci Tensor & Ricci Scalar (`ricci-tensor`)

```json
{
  "id": "ricci-tensor",
  "title": "Ricci Tensor & Ricci Scalar",
  "category": "Established Mathematics",
  "year_established": "1854-1903",
  "badge_type": "established",
  "main_equation": "R_\u03bc\u03bd = R^\u03bb_\u03bc\u03bb\u03bd | R = g^\u03bc\u03bd R_\u03bc\u03bd",
  "main_equation_latex": "R_{\\mu\\nu} = R^{\\lambda}_{\\mu\\lambda\\nu} \\quad | \\quad R = g^{\\mu\\nu} R_{\\mu\\nu}",
  "summary": "The fundamental measures of spacetime curvature that describe how matter and energy bend space, forming the building blocks of Einstein's field equations.",
  "key_properties": [
    "Riemann tensor has 20 independent components in 4D spacetime",
    "Ricci tensor is a contraction of the Riemann tensor with 10 independent components",
    "Ricci scalar is the trace of the Ricci tensor - single number measuring total curvature",
    "Measures volume distortion: geodesic deviation and focusing of geodesics",
    "Appears in Einstein-Hilbert action as fundamental curvature invariant",
    "Symmetric tensor: R_\u03bc\u03bd = R_\u03bd\u03bc",
    "Connected to stress-energy tensor via Einstein field equations"
  ],
  "pm_connection": "In Principia Metaphysica's 2T physics framework, the Ricci tensor and scalar generalize to higher dimensions during the dimensional reduction cascade (26D \u2192 13D \u2192 6D \u2192 4D). The Ricci curvature describes how matter/energy curves space at each dimensional level, with G\u2082 compactification and Kaluza-Klein modes contributing to the effective 4D curvature.",
  "formulas": [
    {
      "symbol": "R^\u03c1_\u03c3\u03bc\u03bd",
      "name": "Riemann Curvature Tensor",
      "latex": "R^{\\rho}_{\\sigma\\mu\\nu} = \\partial_{\\mu}\\Gamma^{\\rho}_{\\nu\\sigma} - \\partial_{\\nu}\\Gamma^{\\rho}_{\\mu\\sigma} + \\Gamma^{\\rho}_{\\mu\\lambda}\\Gamma^{\\lambda}_{\\nu\\sigma} - \\Gamma^{\\rho}_{\\nu\\lambda}\\Gamma^{\\lambda}_{\\mu\\sigma}",
      "description": "The fundamental measure of spacetime curvature - measures how vectors change when parallel transported around closed loops"
    },
    {
      "symbol": "R_\u03bc\u03bd",
      "name": "Ricci Tensor",
      "latex": "R_{\\mu\\nu} = R^{\\lambda}_{\\mu\\lambda\\nu}",
      "description": "Contraction of Riemann tensor measuring volume distortion in curved space"
    },
    {
      "symbol": "R",
      "name": "Ricci Scalar",
      "latex": "R = g^{\\mu\\nu} R_{\\mu\\nu}",
      "description": "Trace of Ricci tensor - single number measuring total average curvature at a point"
    },
    {
      "symbol": "\u0393^\u03bb_\u03bc\u03bd",
      "name": "Christoffel Symbols",
      "latex": "\\Gamma^{\\lambda}_{\\mu\\nu} = \\frac{1}{2} g^{\\lambda\\rho}(\\partial_{\\mu}g_{\\nu\\rho} + \\partial_{\\nu}g_{\\rho\\mu} - \\partial_{\\rho}g_{\\mu\\nu})",
      "description": "Connection coefficients describing how basis vectors change in curved spacetime"
    },
    {
      "symbol": "G_\u03bc\u03bd",
      "name": "Einstein Tensor",
      "latex": "G_{\\mu\\nu} = R_{\\mu\\nu} - \\frac{1}{2}Rg_{\\mu\\nu}",
      "description": "Automatically divergence-free combination used in Einstein field equations"
    },
    {
      "symbol": "d\u00b2V/d\u03c4\u00b2",
      "name": "Raychaudhuri Equation",
      "latex": "\\frac{d^2 V}{d\\tau^2} = -R_{\\mu\\nu} u^{\\mu} u^{\\nu} V",
      "description": "Describes evolution of volume for geodesic congruences - shows how Ricci tensor controls focusing"
    }
  ]
}
```

### SO(10) Grand Unified Theory (`so10-gut`)

```json
{
  "id": "so10-gut",
  "title": "SO(10) Grand Unified Theory",
  "category": "Theoretical Physics",
  "year_established": "1974",
  "badge_type": "theoretical",
  "main_equation": "SO(10) \u2283 SU(3) \u00d7 SU(2) \u00d7 U(1)",
  "main_equation_latex": "\\text{SO}(10) \\supset \\text{SU}(3) \\times \\text{SU}(2) \\times \\text{U}(1)",
  "summary": "The most elegant grand unification: all Standard Model forces and one generation of matter (including the right-handed neutrino) fit into a single 16-dimensional spinor representation.",
  "key_properties": [
    "16-dimensional spinor contains exactly one generation of fermions plus right-handed neutrino",
    "45 gauge bosons in adjoint representation (12 SM + 33 new X,Y bosons)",
    "Gauge coupling unification at M_GUT \u2248 2.118 \u00d7 10^16 GeV",
    "Predicts proton decay: p \u2192 e\u207a\u03c0\u2070 with lifetime \u03c4_p \u2248 4.09 \u00d7 10^34 years",
    "Explains charge quantization automatically via group structure",
    "Seesaw mechanism naturally explains tiny neutrino masses",
    "Three generations require three copies of 16-plet"
  ],
  "pm_connection": "In Principia Metaphysica, SO(10) emerges from G\u2082 compactification on associative cycles (b\u2082=4) via D5-brane wrapping. The effective Euler characteristic \u03c7_eff = 144 = 3 \u00d7 48 provides topological origin for three generations. The 64-component 13D spinor decomposes as 16_SO(10) \u00d7 4_internal, connecting grand unification to fundamental spinor structure.",
  "formulas": [
    {
      "symbol": "16",
      "name": "Spinor Representation",
      "latex": "16 = u_{R,G,B}, d_{R,G,B}, Q_L, e_L, e_R, \\nu_L, \\nu_R",
      "description": "Minimal spinor representation containing all fermions of one generation"
    },
    {
      "symbol": "45",
      "name": "Gauge Bosons",
      "latex": "\\dim(\\text{SO}(10)) = \\frac{10 \\times 9}{2} = 45",
      "description": "Adjoint representation: 12 SM gauge bosons + 33 X,Y bosons mediating proton decay"
    },
    {
      "symbol": "M_GUT",
      "name": "GUT Scale",
      "latex": "M_{\\text{GUT}} = 2.118 \\times 10^{16} \\text{ GeV}",
      "description": "Energy scale where three SM coupling constants unify"
    },
    {
      "symbol": "\u03b1_GUT",
      "name": "Unified Coupling",
      "latex": "\\alpha_1(M_{\\text{GUT}}) = \\alpha_2(M_{\\text{GUT}}) = \\alpha_3(M_{\\text{GUT}})",
      "description": "Running coupling constants converge at GUT scale"
    },
    {
      "symbol": "m_\u03bd",
      "name": "Seesaw Mechanism",
      "latex": "m_{\\nu} \\sim \\frac{m_D^2}{M_R}",
      "description": "Type-I seesaw formula explaining tiny neutrino masses via heavy right-handed neutrinos"
    },
    {
      "symbol": "\u03c4_p",
      "name": "Proton Lifetime",
      "latex": "\\tau_p = 4.09 \\times 10^{34} \\text{ years}",
      "description": "PM prediction for proton decay lifetime via X,Y boson exchange"
    },
    {
      "symbol": "\u03c7_eff",
      "name": "Three Generations",
      "latex": "\\chi_{\\text{eff}} = 144 = 3 \\times 48 = 3 \\times (16 + \\bar{16} + 16_{\\text{vector}})",
      "description": "Topological explanation for three generations from G\u2082 Euler characteristic"
    }
  ]
}
```

### Unruh Effect (`unruh-effect`)

```json
{
  "id": "unruh-effect",
  "title": "Unruh Effect",
  "category": "Established Physics",
  "year_established": "1976",
  "badge_type": "established",
  "main_equation": "T_U = \u210fa / (2\u03c0ck_B)",
  "main_equation_latex": "T_U = \\frac{\\hbar a}{2\\pi c k_B}",
  "summary": "Accelerated observers perceive the quantum vacuum as a thermal bath, revealing the profound observer-dependence of temperature and particles in quantum field theory.",
  "key_properties": [
    "Uniformly accelerated observers detect thermal radiation in Minkowski vacuum",
    "Temperature proportional to proper acceleration: T \u221d a",
    "Rindler horizon at distance c\u00b2/a behind accelerated observer",
    "Particle content is observer-dependent (vacuum for inertial, thermal for accelerated)",
    "Related to Hawking radiation via equivalence principle",
    "KMS condition characterizes thermal equilibrium state",
    "Earth surface acceleration gives T_U \u2248 4 \u00d7 10^-20 K (unobservably small)"
  ],
  "pm_connection": "The Unruh effect demonstrates observer-dependent temperature crucial to PM's thermal time hypothesis. In the dimensional cascade (26D \u2192 13D \u2192 6D \u2192 4D), each transition induces effective 'acceleration' in compactified dimensions, generating thermal radiation. Temperature emerges from the observer's relationship to the Pneuma field state via modular flow.",
  "formulas": [
    {
      "symbol": "T_U",
      "name": "Unruh Temperature",
      "latex": "T_U = \\frac{\\hbar a}{2\\pi c k_B}",
      "description": "Temperature measured by observer with proper acceleration a"
    },
    {
      "symbol": "a",
      "name": "Proper Acceleration",
      "latex": "a",
      "description": "Acceleration in observer's own reference frame (m/s\u00b2)"
    },
    {
      "symbol": "\u03b2_U",
      "name": "Inverse Temperature",
      "latex": "\\beta_U = \\frac{2\\pi c}{a} = \\frac{1}{k_B T_U}",
      "description": "Inverse Unruh temperature from modular flow period"
    },
    {
      "symbol": "\u03c1,\u03b7",
      "name": "Rindler Coordinates",
      "latex": "t = \\frac{\\rho}{a}\\sinh(a\\eta), \\quad x = \\frac{\\rho}{a}\\cosh(a\\eta)",
      "description": "Coordinate system adapted to uniformly accelerated observer"
    },
    {
      "symbol": "ds\u00b2_R",
      "name": "Rindler Metric",
      "latex": "ds^2 = -(a\\rho)^2 d\\eta^2 + d\\rho^2 + dy^2 + dz^2",
      "description": "Metric in Rindler coordinates (looks like gravitational field)"
    },
    {
      "symbol": "\u03c1_R",
      "name": "Thermal State",
      "latex": "\\rho_R = Z^{-1} \\exp(-2\\pi\\omega H_R/a)",
      "description": "Minkowski vacuum appears as thermal state to Rindler observer"
    },
    {
      "symbol": "\u03ba",
      "name": "Surface Gravity",
      "latex": "\\kappa = a \\quad \\text{(Rindler)}, \\quad \\kappa = \\frac{c^4}{4GM} \\quad \\text{(Schwarzschild)}",
      "description": "Effective surface gravity of horizon - determines temperature"
    }
  ]
}
```

### Yang-Mills Theory (`yang-mills`)

```json
{
  "id": "yang-mills",
  "title": "Yang-Mills Theory",
  "category": "Established Physics",
  "year_established": "1954",
  "badge_type": "established",
  "main_equation": "\u2112 = -\u00bc F^a_\u03bc\u03bd F^a\u03bc\u03bd",
  "main_equation_latex": "\\mathcal{L} = -\\frac{1}{4} F^a_{\\mu\\nu} F^{a\\mu\\nu}",
  "summary": "The foundation of modern particle physics: a non-abelian gauge theory that underlies the strong and electroweak forces of the Standard Model.",
  "key_properties": [
    "Non-abelian gauge symmetry: transformations don't commute",
    "Gauge bosons carry charge and self-interact (unlike photons)",
    "Structure constants f^abc define Lie algebra: [T^a, T^b] = if^abc T^c",
    "Field strength includes self-interaction: F^a_\u03bc\u03bd = \u2202_\u03bcA^a_\u03bd - \u2202_\u03bdA^a_\u03bc - gf^abc A^b_\u03bc A^c_\u03bd",
    "3-gluon and 4-gluon vertices arise from non-abelian structure",
    "Asymptotic freedom: coupling decreases at high energies",
    "Confinement at low energies: only color-neutral states observed"
  ],
  "pm_connection": "Yang-Mills gauge fields emerge from 26D bulk theory via dimensional reduction. SO(10) GUT gauge symmetry arises from D5-branes wrapping b\u2082=4 associative 3-cycles in the G\u2082 manifold. The bulk 26D Yang-Mills action reduces to Standard Model SU(3)\u00d7SU(2)\u00d7U(1) after compactification and symmetry breaking, with gauge couplings unifying at M_GUT.",
  "formulas": [
    {
      "symbol": "F^a_\u03bc\u03bd",
      "name": "Field Strength Tensor",
      "latex": "F^a_{\\mu\\nu} = \\partial_{\\mu}A^a_{\\nu} - \\partial_{\\nu}A^a_{\\mu} - gf^{abc}A^b_{\\mu}A^c_{\\nu}",
      "description": "Non-abelian field strength - distinguishes from Maxwell theory via gf^abc term"
    },
    {
      "symbol": "A^a_\u03bc",
      "name": "Gauge Fields",
      "latex": "A^a_{\\mu}",
      "description": "Vector potentials in adjoint representation: 8 gluons (SU(3)), 3 weak bosons (SU(2)), 1 photon (U(1))"
    },
    {
      "symbol": "f^abc",
      "name": "Structure Constants",
      "latex": "[T^a, T^b] = if^{abc}T^c",
      "description": "Define Lie algebra commutation relations - completely antisymmetric"
    },
    {
      "symbol": "D_\u03bc",
      "name": "Covariant Derivative",
      "latex": "D_{\\mu} = \\partial_{\\mu} + igA^a_{\\mu}T^a",
      "description": "Ensures gauge covariance of fermion kinetic terms"
    },
    {
      "symbol": "\u03b1_s(\u03bc)",
      "name": "Running Coupling",
      "latex": "\\alpha_s(\\mu) = \\frac{\\alpha_s(\\mu_0)}{1 + \\alpha_s(\\mu_0)b\\ln(\\mu/\\mu_0)}",
      "description": "QCD coupling constant evolution - asymptotic freedom when b > 0"
    },
    {
      "symbol": "\u2112_YM",
      "name": "Yang-Mills Lagrangian",
      "latex": "\\mathcal{L}_{\\text{YM}} = -\\frac{1}{4} F^a_{\\mu\\nu} F^{a\\mu\\nu} + \\bar{\\psi}(i\\gamma^{\\mu}D_{\\mu} - m)\\psi",
      "description": "Full Yang-Mills Lagrangian with gauge fields and matter"
    },
    {
      "symbol": "N\u00b2-1",
      "name": "Number of Gluons",
      "latex": "\\dim(\\text{SU}(N)) = N^2 - 1",
      "description": "Dimension of Lie algebra: 8 for SU(3), 3 for SU(2)"
    }
  ]
}
```

### Tomita-Takesaki Theory (`tomita-takesaki`)

```json
{
  "id": "tomita-takesaki",
  "title": "Tomita-Takesaki Theory",
  "category": "Established Mathematics",
  "year_established": "1970",
  "badge_type": "established",
  "main_equation": "\u03c3_t(A) = \u0394^it A \u0394^-it",
  "main_equation_latex": "\\sigma_t(A) = \\Delta^{it} A \\Delta^{-it}",
  "summary": "Modular automorphism group and the profound connection between quantum states and intrinsic time evolution in von Neumann algebras.",
  "key_properties": [
    "Every faithful normal state naturally defines modular flow \u03c3_t",
    "Modular operator \u0394 = S*S is positive self-adjoint",
    "Modular conjugation J exchanges algebra with commutant: JMJ = M'",
    "State becomes KMS thermal state with respect to modular flow",
    "Tomita operator S: A\u03a9 \u21a6 A*\u03a9 is anti-linear and closed",
    "Modular Hamiltonian K = -log(\u0394) generates time evolution",
    "Thermal time hypothesis: physical time emerges from modular flow"
  ],
  "pm_connection": "Tomita-Takesaki theory is central to PM's thermal time hypothesis. Time at each dimensional level (26D \u2192 13D \u2192 6D \u2192 4D) emerges from modular flow of the Pneuma field state. The observable algebras form type III factors, with modular automorphisms generating intrinsic dynamics and thermodynamic behavior from the KMS condition.",
  "formulas": [
    {
      "symbol": "S",
      "name": "Tomita Operator",
      "latex": "S(A\\Omega) = A^*\\Omega \\quad \\text{for } A \\in M",
      "description": "Anti-linear closed operator encoding relation between operator and its adjoint"
    },
    {
      "symbol": "\u0394",
      "name": "Modular Operator",
      "latex": "\\Delta = S^*S = J\\Delta^{1/2}",
      "description": "Positive self-adjoint operator generating modular automorphisms"
    },
    {
      "symbol": "J",
      "name": "Modular Conjugation",
      "latex": "J = S\\Delta^{-1/2}, \\quad JMJ = M'",
      "description": "Anti-unitary operator from polar decomposition - exchanges algebra with commutant"
    },
    {
      "symbol": "\u03c3_t",
      "name": "Modular Automorphism Group",
      "latex": "\\sigma_t(A) = \\Delta^{it} A \\Delta^{-it}",
      "description": "One-parameter group of *-automorphisms representing intrinsic time evolution"
    },
    {
      "symbol": "\u03a9",
      "name": "Cyclic and Separating Vector",
      "latex": "\\{A\\Omega | A \\in M\\} \\text{ dense}, \\quad A\\Omega = 0 \\Rightarrow A = 0",
      "description": "GNS vector representing the state - both cyclic and separating"
    },
    {
      "symbol": "KMS",
      "name": "KMS Condition",
      "latex": "\\omega(AB) = \\omega(B\\sigma_{i\\beta}(A))",
      "description": "Thermal equilibrium condition at inverse temperature \u03b2 with respect to modular flow"
    },
    {
      "symbol": "K",
      "name": "Modular Hamiltonian",
      "latex": "K = -\\log(\\Delta), \\quad \\sigma_t(A) = e^{itK} A e^{-itK}",
      "description": "Natural notion of energy generating modular time evolution"
    },
    {
      "symbol": "(M,H,J,P_+)",
      "name": "Standard Form",
      "latex": "P_+ = \\{A\\Omega | A \\geq 0, A \\in M\\}, \\quad JP_+ = P_+",
      "description": "Canonical representation with natural positive self-dual cone"
    }
  ]
}
```
