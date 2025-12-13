# Firebase Database Structure Analysis

## Executive Summary

This report analyzes the Firebase Firestore database structure and identifies:
1. **Duplicated data** that needs consolidation
2. **Missing derivation chains** for formulas
3. **Proposed schema refactoring** for single source of truth

## Current Database Structure

### Collections Overview

| Collection | Documents | Size | Purpose |
|------------|-----------|------|---------|
| theory_constants | 10 | 159.2 KB | Physics constants and simulation outputs |
| formulas | 55 | 49.8 KB | Formula definitions with LaTeX/HTML |
| formula_database | 29 | 14.8 KB | Tooltip metadata for constants |
| pages | 57 | 2946.6 KB | HTML content for all website pages |
| appendices | 0 | 0.0 KB | Not yet populated |
| validation_history | 2 | 3.0 KB | Validation run results |

### Critical Issues Identified

#### 1. Massive Data Duplication in `pages` Collection

The `pages` collection stores **full HTML content** for each page at 2.9 MB total. This is problematic because:
- Same formulas appear on multiple pages with hardcoded HTML
- Updates to a formula require editing every page that references it
- No derivation chain linking formulas to their sources
- Sections (cosmology, fermion-sector, etc.) are stored as separate documents but also embedded in paper

#### 2. Inconsistent Formula References

**In `formulas` collection (55 formulas):**
```json
{
  "id": "alpha-gut",
  "html": "1/α<sub>GUT</sub> = 1/(10π) + corrections ≈ 23.54",
  "latex": "\\frac{1}{\\alpha_{GUT}} = \\frac{1}{10\\pi} + ...",
  "category": "DERIVED",
  "pm_constant": "PM.proton_decay.alpha_GUT_inv"
}
```

**In `formula_database` collection (29 constants):**
```json
{
  "id": "alpha_GUT_inv",
  "symbol": "1/α_GUT",
  "pmPath": "proton_decay.alpha_GUT_inv",
  "derivation": "1/(10π) = 24.30... from geometric considerations"
}
```

**PROBLEM:** Same constant exists in BOTH collections with different structures:
- `formulas.alpha-gut` has full formula HTML but limited derivation info
- `formula_database.alpha_GUT_inv` has path reference but different format

#### 3. No Derivation Chain Linking

Current formulas have NO linking structure. For example:
- `generation-number` formula: `n_gen = χ/24 = 72/24 = 3`
- References `f-theory-index` formula: `n_gen = χ/24`
- But there's NO formal link field connecting them

**Missing linkages:**
- PM formula → parent PM formula (derivation source)
- PM formula → established physics formula (foundation)
- PM formula → experimental verification (test)

#### 4. Version Data Scattered

The `theory_constants/current` document contains:
- `v9_transparency`, `v9_brst_proof`
- `v10_geometric_derivations`, `v10_1_neutrino_masses`, `v10_2_all_fermions`
- `v11_final_observables`
- `v12_final_values`, `v12_3_updates`, `v12_5_rigor_resolution`, `v12_6_geometric_derivations`
- `v12_7_pure_geometric`

Each version has overlapping fields with slightly different values. The "current" values at top level may not match version-specific values.

---

## Proposed Refactored Schema

### 1. Unified `formulas` Collection

```json
{
  "id": "alpha-gut-inv",
  "type": "DERIVED",
  "status": "VERIFIED",

  // Display formats
  "display": {
    "html": "1/α<sub>GUT</sub> = 1/(10π) + corrections ≈ 23.54",
    "latex": "\\frac{1}{\\alpha_{GUT}} = \\frac{1}{10\\pi} + \\text{corrections}",
    "plainText": "1/alpha_GUT = 1/(10*pi) + corrections ≈ 23.54",
    "label": "(4.2) GUT Coupling from Geometry"
  },

  // Value reference (single source)
  "value": {
    "pmPath": "proton_decay.alpha_GUT_inv",
    "currentValue": 23.54,
    "unit": "",
    "uncertainty": 0.82
  },

  // Derivation chain (NEW)
  "derivation": {
    "parent_formulas": ["casimir-so10", "tcs-g2-volume"],
    "established_physics": ["yang-mills"],
    "derivation_steps": [
      "Start with SO(10) Casimir C_A = 9",
      "Apply TCS G2 singularity volume",
      "Apply torsion correction exp(|T_ω|/h11)"
    ],
    "verification_page": "sections/gauge-unification.html"
  },

  // Experimental comparison
  "experimental": {
    "value": 24.3,
    "error": 0.3,
    "source": "RG evolution from SM couplings",
    "sigma": 0.82
  },

  // Terms for hoverable tooltips
  "terms": {
    "1/(10π)": {
      "name": "Leading Geometric Term",
      "description": "≈ 0.0318 from Casimir",
      "link": "#casimir-so10"
    },
    "corrections": {
      "name": "Loop Corrections",
      "description": "Threshold effects from heavy particles"
    }
  },

  // Metadata
  "usedIn": ["gauge-unification", "proton-decay", "paper"],
  "attribution": "Principia Metaphysica",
  "v12_7_status": "pure geometric - breakthrough result"
}
```

### 2. Simplified `constants` Collection

Merge `theory_constants` and `formula_database` into single collection:

```json
{
  "id": "alpha_GUT_inv",
  "symbol": "1/α<sub>GUT</sub>",
  "textSymbol": "1/alpha_GUT",

  // Value (SINGLE source of truth)
  "value": 23.54,
  "unit": "",
  "category": "gut",

  // Source
  "pmPath": "proton_decay.alpha_GUT_inv",
  "formula_id": "alpha-gut-inv",  // Link to formula

  // Experimental
  "experimental": {
    "value": 24.3,
    "error": 0.3,
    "source": "RG evolution",
    "year": 2024
  },

  // Usage tracking
  "occurrences": 45,
  "pages": ["gauge-unification", "proton-decay", "predictions"]
}
```

### 3. Minimal `pages` Collection

Instead of storing full HTML, store only:

```json
{
  "id": "gauge-unification",
  "title": "Gauge Unification",
  "category": "section",

  // Content structure (formulas load from formulas collection)
  "sections": [
    {
      "id": "intro",
      "heading": "Introduction",
      "content_type": "markdown",
      "content": "The PM framework unifies gauge couplings at M_GUT..."
    },
    {
      "id": "gut-scale-derivation",
      "heading": "GUT Scale Derivation",
      "formulas": ["gut-scale", "alpha-gut-inv", "m-gut-torsion"],
      "content_type": "formula_block"
    }
  ],

  // References to load
  "formula_refs": ["gut-scale", "alpha-gut-inv", "gauge-unification"],
  "constant_refs": ["M_GUT", "alpha_GUT_inv", "T_omega"]
}
```

### 4. New `derivation_chains` Collection

Track complete derivation chains from PM formulas to established physics:

```json
{
  "id": "n-gen-to-f-theory",
  "name": "Three Generations Derivation",

  "chain": [
    {
      "step": 1,
      "formula_id": "generation-number-26d",
      "statement": "n_gen = χ_eff/48 = 144/48 = 3",
      "type": "PM_DERIVED"
    },
    {
      "step": 2,
      "formula_id": "f-theory-index",
      "statement": "n_gen = χ/24 (F-theory index theorem)",
      "type": "ESTABLISHED",
      "citation": "[Sethi, Vafa, Witten 1996]"
    },
    {
      "step": 3,
      "formula_id": "atiyah-singer",
      "statement": "Index theorem for Dirac operator",
      "type": "ESTABLISHED",
      "citation": "[Atiyah-Singer 1968]"
    }
  ],

  "validation": {
    "experimental_test": "n_gen = 3 observed",
    "status": "VERIFIED",
    "sigma": 0
  }
}
```

---

## Data Migration Plan

### Phase 1: Consolidate Formulas

1. Merge `formulas` (55) and `formula_database` (29) into unified `formulas` collection
2. Eliminate duplicates (e.g., `w_a` and `wa` are same constant)
3. Add `derivation.parent_formulas` and `derivation.established_physics` fields

### Phase 2: Extract Constants

1. Parse `theory_constants/current` document
2. Create individual `constants` documents for each PM path
3. Link to corresponding formula_id

### Phase 3: Minimize Pages

1. Extract formula/constant references from HTML
2. Replace hardcoded values with `<pm-value path="...">` components
3. Store only text content, let formulas load dynamically

### Phase 4: Build Derivation Chains

1. Identify all PM formulas (category: THEORY, DERIVED, PREDICTIONS)
2. Trace each to established physics (category: ESTABLISHED)
3. Create `derivation_chains` documents

### Phase 5: Validation Script

Create script that:
1. Loads all PM formulas
2. Walks derivation.parent_formulas recursively
3. Verifies all chains terminate at ESTABLISHED physics
4. Reports any orphan formulas without proper derivation

---

## Identified Duplicates

### Formulas with Same Content

| ID 1 | ID 2 | Content |
|------|------|---------|
| `de-w0` | `mep-w0` | Both define w₀ = -0.8528 |
| `w_a` | `wa` | Both define w_a dark energy evolution |
| `generation-number` | `generation-number-26d` | Both derive n_gen = 3 |

### Constants with Same Data

| formula_database | theory_constants path | Value |
|------------------|----------------------|-------|
| `theta_23` | `pmns_matrix.theta_23` | 45.0 |
| `theta_12` | `pmns_matrix.theta_12` | 33.59 |
| `w0` | `dark_energy.w0_PM` | -0.8528 |
| `M_GUT` | `proton_decay.M_GUT` | 2.118e16 |

---

## Action Items

1. **Create migration script** (`scripts/firebase-schema-migration.js`)
   - Download current data
   - Transform to new schema
   - Upload with validation

2. **Update page rendering**
   - Load formulas from `formulas` collection
   - Render with hoverable terms
   - Show derivation chain on click

3. **Create derivation validator**
   - Ensure all PM formulas trace to established physics
   - Generate report of derivation chain completeness

4. **Update simulation pipeline**
   - After simulation, update `constants` collection values
   - Regenerate `formulas` collection with new values
   - Trigger page refresh

---

## Recommended Next Steps

1. Implement unified `formulas` schema with derivation chains
2. Create `<pm-formula>` web component for hoverable rendering
3. Build derivation chain validation script
4. Migrate one section (gauge-unification) as proof of concept
5. Roll out to all sections after validation

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
