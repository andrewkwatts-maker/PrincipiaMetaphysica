# Principia Metaphysica - Project Architecture

## v16.2 STERILE: Two-Time Framework

### Theoretical Architecture: (13,1) + (13,1) Dimensional Structure

```
    26D Bulk (24,2) Signature
    ┌────────────────────────────────────────────────────────────────┐
    │                                                                │
    │   Sp(2,ℝ) Gauge Fixing (removes 13 ghost dimensions)          │
    │                         ▼                                      │
    │   ┌──────────────────────────────────────────────────────┐    │
    │   │           13D Shadow Manifold (12,1)                  │    │
    │   │                                                       │    │
    │   │   G₂ Compactification (7 dimensions → geometry)      │    │
    │   │                         ▼                             │    │
    │   │   ┌──────────────────────────────────────────────┐   │    │
    │   │   │        6D Observable Bulk (5,1)              │   │    │
    │   │   │                                              │   │    │
    │   │   │   ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │    │
    │   │   │   │Observable│  │ Shadow 1 │  │ Shadow 2 │  │   │    │
    │   │   │   │Universe  │  │ (hidden) │  │ (hidden) │  │   │    │
    │   │   │   │  (3,1)   │  │  (3,1)   │  │  (3,1)   │  │   │    │
    │   │   │   └──────────┘  └──────────┘  └──────────┘  │   │    │
    │   │   └──────────────────────────────────────────────┘   │    │
    │   └──────────────────────────────────────────────────────┘    │
    └────────────────────────────────────────────────────────────────┘
```

### 72-Gate Integrity Framework

The v16.2 STERILE model is validated by 72 hard gates organized in 6 blocks:

| Block | Gates   | Domain                                    |
|-------|---------|-------------------------------------------|
| A     | G01-G12 | Root Basis (Manifold Potential & Holonomy)|
| B     | G13-G24 | Torsion Cage (Pin Alignment & Forces)     |
| C     | G25-G36 | Gauge Sector (Force Unification)          |
| D     | G37-G48 | Residue Bank (Mixing & Cosmology)         |
| E     | G49-G60 | Metric Sector (Spacetime Anchoring)       |
| F     | G61-G72 | Omega Closure (Information & Recursion)   |

**Key Constants (Zero Free Parameters):**
- **b₃ = 24**: G₂ manifold third Betti number
- **χ_eff = 144**: Effective Euler characteristic (6 × b₃)
- **w₀ = -23/24**: Dark energy equation of state

---

## Simple Answer: What Does What?

```
                    ┌─────────────────────┐
                    │    config.py        │  ← SINGLE SOURCE OF TRUTH
                    │                     │     • All parameter values
                    │  M_Pl = 2.435e18    │     • Physical constants
                    │  w_0 = -23/24       │     • Theory parameters (v16.2)
                    │  b_3 = 24           │     • Static definitions only
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │SimulateTheory.py    │      │generate_js_         │
    │                     │      │  constants.py       │
    │ • SymPy derivations │      │                     │
    │ • QuTiP simulations │      │ • Auto-generates JS │
    │ • Parameter calcs   │      │ • Keeps values synced│
    └──────────┬──────────┘      └──────────┬──────────┘
               │                            │
               ▼                            ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │  parameters.csv     │      │js/theory-           │
    │                     │      │  constants.js       │
    │ • Derived params    │      │                     │
    │ • Analysis data     │      │ • JavaScript values │
    │ • Excel-ready       │      │ • Used by HTML      │
    └─────────────────────┘      └──────────┬──────────┘
                                            │
                                            ▼
                                 ┌─────────────────────┐
                                 │  HTML Webpages      │
                                 │                     │
                                 │ • index.html        │
                                 │ • sections/*.html   │
                                 │ • Auto-updated      │
                                 └─────────────────────┘
```

## Key Files

### 1. config.py - The Source of Truth
**Purpose:** Store all input values/parameters
**Contains:**
- Physical constants (M_Pl, α_em, H₀)
- Theory parameters (D_bulk=26, generations=3)
- v6.1 predictions (m_KK, η, c_μν)
- Computational settings (tolerances, grid sizes)

**You edit this when:** You want to change a parameter value

### 2. SimulateTheory.py - The Calculator
**Purpose:** Calculate derived quantities using values from config.py
**Contains:**
- SymPy symbolic derivations
- QuTiP quantum simulations
- Parameter validation logic
- CSV/Excel export code

**You edit this when:** You want to change a formula or add new calculations

### 3. HTML Files - The Theory Documentation
**Purpose:** Human-readable theory presentation
**Main files:**
- `index.html` - Landing page
- `principia-metaphysica-paper.html` - Full paper
- `sections/*.html` - Theory sections
- `computational-appendices.html` - Code examples

**You edit these when:** Updating the theory presentation

## Workflow (Updated with Automation!)

### To Change a Parameter Value:
1. Edit `config.py` (single source of truth)
2. Run `python generate_js_constants.py` (updates JavaScript)
3. Run `python SimulateTheory.py` (updates CSV if needed)
4. HTML webpages automatically use new values!

### To Add a New Prediction:
1. Add parameter to `config.py` (e.g., in V61Predictions class)
2. Run `python generate_js_constants.py` (adds to JavaScript)
3. Add derivation to `SimulateTheory.py` if calculation needed
4. Run SimulateTheory.py to generate updated CSV

### To Update Theory Documentation:
1. Edit appropriate `sections/*.html` file
2. HTML uses `TheoryConstants` from auto-generated JS
3. No manual value sync needed - edit config.py only!

## Why NOT Merge Into One File?

**Separation of Concerns:**
- config.py = "WHAT values?" (data)
- SimulateTheory.py = "HOW to calculate?" (logic)

**Benefits:**
1. **Easy parameter exploration** - Change config, rerun calculations
2. **Version control friendly** - Separate value changes from code changes
3. **Collaborative** - Physicist edits config, programmer edits calculation logic
4. **Testable** - Can test calculations with different config values
5. **Reusable** - Other scripts can import config.py

## File Organization

```
PrincipiaMetaphysica/
├── config.py                    ⭐ SOURCE OF TRUTH (all values)
├── SimulateTheory.py            ⭐ CALCULATION ENGINE
│
├── index.html                   📄 Main landing page
├── principia-metaphysica-paper.html  📄 Full paper
├── beginners-guide.html         📄 Beginner's guide
├── computational-appendices.html     📄 Code examples
│
├── sections/                    📁 Theory sections
│   ├── cosmology.html
│   ├── predictions.html
│   ├── gauge-unification.html
│   └── ... (15 total)
│
├── README.md                    📖 Project overview
├── CONFIG_README.md             📖 How to use config.py
├── SimulateTheory_README.md    📖 How to use SimulateTheory.py
└── VARIABLE_EXTRACTION_CONSOLIDATED.md  📖 Variable inventory
```

## Quick Reference

| Task | File to Edit |
|------|--------------|
| Change M_Planck value | config.py → PhenomenologyParameters.M_PLANCK |
| Change w₀ formula | SimulateTheory.py → w_0 derivation section |
| Add new prediction | 1) config.py (add value), 2) SimulateTheory.py (add calculation) |
| Update paper text | principia-metaphysica-paper.html |
| Change GW dispersion formula | SimulateTheory.py → GW section |
| Adjust QuTiP grid size | config.py → ComputationalSettings.N_QUTIP_* |

## Summary

**Don't merge config.py and SimulateTheory.py.**

They work together as a team:
- **config.py** = The library of values
- **SimulateTheory.py** = The calculator that uses those values

This separation makes the project cleaner, more maintainable, and easier to update.
