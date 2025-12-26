# Paper Section Migration Plan
## Complete Audit of principia-metaphysica-paper.html → theory_output.json

**Date:** 2025-12-26
**Source:** `H:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html`
**Target:** `H:\Github\PrincipiaMetaphysica\theory_output.json`

---

## Executive Summary

This audit provides a comprehensive inventory of all sections in the Principia Metaphysica paper and maps them to the existing `sections` object in `theory_output.json`.

### Current State
- **Paper Sections:** 9 main sections + References + 14 Appendices (A-N)
- **theory_output.json Sections:** 6 sections (numbered 1-6)
- **Coverage:** ~26% of paper content is currently represented in theory_output.json
- **Gap:** Sections 7-9, References, and all 14 appendices are missing

### Migration Priority
1. **High Priority:** Sections 7-9 (core content)
2. **Medium Priority:** Appendices A-K (technical details)
3. **Low Priority:** Appendices L-N (reference materials)

---

## Paper Structure Inventory

### Main Sections (9 total)

#### Section 1: Introduction
- **ID:** `section-1`
- **Status in theory_output.json:** ✅ EXISTS (id: "1")
- **Title Match:** "Introduction"
- **Subsections:** 3
  - 1.1 Historical Context
  - 1.2 Problems Addressed
  - 1.3 Framework Overview
- **Key Content:** Framework overview, historical context, problems addressed
- **Tables:** 1 (Table of Contents)
- **Migration Notes:** Already migrated. Section exists with proper structure.

---

#### Section 2: The 26-Dimensional Bulk Spacetime
- **ID:** `section-2`
- **Status in theory_output.json:** ✅ EXISTS (id: "2", title: "Geometric Framework")
- **Title Match:** Different title but covers same content
- **Subsections:** 7
  - 2.1 Motivation for (24,2) Signature
  - 2.2 Master Action
  - 2.3 Virasoro Anomaly Cancellation
  - 2.4 The Master Action and Pneuma Field (id: `master-action`)
  - 2.5 Pneuma Condensate as Source of Geometry (id: `pneuma-condensate`)
  - 2.6 Holographic Entropy from Pneuma (id: `holographic-entropy`)
  - 2.7 Pneuma Vacuum Selection: Racetrack Mechanism (id: `pneuma-racetrack`)
- **Key Content:** 26D geometry, Virasoro anomaly, Pneuma field, master action
- **Tables:** 2 (Dimensional decomposition, Pneuma vacuum parameters)
- **Migration Notes:** Exists but title differs. Paper uses "The 26-Dimensional Bulk Spacetime" while theory_output.json uses "Geometric Framework"

---

#### Section 3: Reduction to the 13-Dimensional Shadow
- **ID:** `section-3`
- **Status in theory_output.json:** ⚠️ PARTIAL (may be subsumed in section "2")
- **Title in theory_output.json:** N/A (content may be in "Geometric Framework")
- **Subsections:** 3 (+ 1 sub-subsection)
  - 3.1 Sp(2,ℝ) Gauge Fixing
    - 3.1.1 Sp(2,ℝ) Constraint Equations
  - 3.2 Primordial Spinor in 13D
  - 3.3 Hidden Variables from Shadow Branes (id: `hidden-variables`)
- **Key Content:** Sp(2,R) gauge fixing, 13D shadow projection, hidden variables
- **Tables:** 0
- **Migration Notes:** This is a major section that should potentially be its own entry in theory_output.json

---

#### Section 4: Compactification on the TCS G₂ Manifold
- **ID:** `section-4`
- **Status in theory_output.json:** ⚠️ PARTIAL (may be subsumed in section "2")
- **Title in theory_output.json:** N/A
- **Subsections:** 4 (+ 5 sub-subsections)
  - 4.1 TCS Construction
    - 4.1a Effective Euler Characteristic from Hodge Numbers
  - 4.2 Generation Number from Topology
  - 4.3 Effective Torsion from Flux
  - 4.4 The Blended Vacuum
    - Core Concept: Multi-Sector Sampling
    - Racetrack Stabilization Fixes the Sampling Position
    - Quantitative Hierarchy Solution
    - Mirror Dark Matter
    - All Parameters Derived from Topology
- **Key Content:** TCS G₂ manifold, generation number, effective torsion, blended vacuum
- **Tables:** 2 (TCS topology, blended vacuum parameters)
- **Migration Notes:** Critical section with detailed G₂ construction, should be separate entry

---

#### Section 5: Gauge Unification and the Standard Model
- **ID:** `section-5`
- **Status in theory_output.json:** ⚠️ PARTIAL (appears to be split between sections "3" and "4")
- **Title in theory_output.json:** Section 3 "Fermion Sector", Section 4 "Gauge Unification"
- **Subsections:** 9 (+ 7 sub-subsections)
  - 5.1 SO(10) from Singularities
  - 5.2 Unified Coupling
  - 5.3 GUT Scale
    - 5.3.1 Geometrically Preferred Breaking Chain
  - 5.4 Native Geometric Doublet-Triplet Splitting via Topological Filter
    - 5.4.1 Topological Filter Mechanism
    - 5.4.2 Index Theorem and Topology Requirement
    - 5.4.3 Zero-Mode Counting
  - 5.5 Weinberg Angle
    - 5.5a Electromagnetic Fine Structure Constant at M_Z
  - 5.6 Electroweak VEV
    - 5.6a Higgs Quartic Coupling from Kähler Potential
  - 5.7 XY Gauge Bosons and Proton Decay Mechanism
    - 5.7.1 Geometric Selection Rules
    - 5.7.2 Proton Lifetime Calculation
  - 5.8 Threshold Corrections (id: `threshold-corrections`)
  - 5.9 Gauge Unification: Theoretical Closure (v14.1) (id: `gauge-closure`)
- **Key Content:** SO(10) GUT, gauge unification, doublet-triplet splitting, proton decay
- **Tables:** 0
- **Migration Notes:** Most comprehensive section in paper. Maps to theory_output.json section 4 "Gauge Unification"

---

#### Section 6: Fermion Sector and Mixing Angles
- **ID:** `section-6`
- **Status in theory_output.json:** ⚠️ PARTIAL (appears to be section "3")
- **Title in theory_output.json:** Section 3 "Fermion Sector"
- **Subsections:** 11
  - 6.1 PMNS Matrix Derivation
  - 6.2 PMNS Parameters
  - 6.2a Top Quark Mass
  - 6.2b Bottom Quark Mass
  - 6.2c Tau Lepton Mass
  - 6.2d Strong Coupling Constant
  - 6.2e Light Quark Masses
  - 6.2f Charged Lepton Masses
  - 6.2g CKM Matrix Elements
  - 6.2h Yukawa Texture: Georgi-Jarlskog and Instantons (id: `yukawa-texture`)
  - 6.3 Neutrino Mass Splittings
- **Key Content:** PMNS matrix, fermion masses, CKM matrix, neutrino masses
- **Tables:** 2 (PMNS parameters, Yukawa hierarchy)
- **Migration Notes:** Maps to theory_output.json section 3 "Fermion Sector"

---

#### Section 7: Cosmology and Dark Energy
- **ID:** `section-7`
- **Status in theory_output.json:** ⚠️ PARTIAL (appears to be in section "5")
- **Title in theory_output.json:** Section 5 "Cosmology and Predictions"
- **Subsections:** 5
  - 7.1 Dark Energy from Effective Dimension
  - 7.2 Logarithmic Evolution
  - 7.3 Dark Energy Evolution Parameter
  - 7.4 The Attractor Scalar (id: `attractor-scalar`)
  - 7.5 The Thermal Time Hypothesis (id: `thermal-time`)
- **Key Content:** Dark energy, Pneuma field cosmology, thermal time
- **Tables:** 0
- **Migration Notes:** Content likely in section 5 "Cosmology and Predictions"

---

#### Section 8: Predictions and Testability
- **ID:** `section-8`
- **Status in theory_output.json:** ⚠️ PARTIAL (appears to be in section "5")
- **Title in theory_output.json:** Section 5 "Cosmology and Predictions"
- **Subsections:** 3
  - 8.1 Summary of 58 Parameters
  - 8.2 Testable Predictions
  - 8.3 Hidden Sector Particles (id: `hidden-sector`)
- **Key Content:** Parameter summary, predictions, hidden sector
- **Tables:** 4 (58 parameters, predictions, hidden sector particles, future tests)
- **Migration Notes:** Critical section with all predictions. Should potentially be its own section in theory_output.json

---

#### Section 9: Discussion and Transparency
- **ID:** `section-9`
- **Status in theory_output.json:** ⚠️ PARTIAL (appears to be section "6")
- **Title in theory_output.json:** Section 6 "Conclusion"
- **Subsections:** 7
  - 9.1 Input Summary
  - 9.2 Comparison with Other Models
  - 9.3 Early Universe and Inflation
  - 9.4 Black Hole Information
  - 9.5 Supersymmetry Fate
  - 9.6 Limitations and Future Work
  - 9.7 Conclusion
- **Key Content:** Discussion, limitations, comparison with other theories
- **Tables:** 1 (Future work summary)
- **Migration Notes:** Maps to section 6 "Conclusion" but much more comprehensive

---

### References Section
- **ID:** `references`
- **Status in theory_output.json:** ❌ MISSING
- **Content:** Bibliography with ~35 references
- **Migration Notes:** Should be added as standalone section or special object in theory_output.json

---

### Appendices (14 total: A-N)

#### Appendix A: Virasoro Anomaly Cancellation
- **ID:** `appendix-a`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 4
  - A.1 Central Charge Calculation
  - A.2 Simulation Code
  - A.3 Signature (24,2) Compatibility
  - A.4 PM Framework Applications
- **Key Content:** Virasoro anomaly derivation, central charge calculation
- **Tables:** 0
- **Migration Priority:** HIGH (critical theoretical foundation)

---

#### Appendix B: Generation Number Derivation
- **ID:** `appendix-b`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 3
  - B.1 Index Formula
  - B.2 Z₂ Mirror Symmetry
  - B.3 Simulation Code
- **Key Content:** Index theorem, generation number calculation
- **Tables:** 0
- **Migration Priority:** HIGH (fundamental prediction)

---

#### Appendix C: Atmospheric Mixing Angle Derivation
- **ID:** `appendix-c`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 2
  - C.1 G₂ Holonomy Argument
  - C.2 Simulation Code
- **Key Content:** PMNS θ₂₃ derivation
- **Tables:** 0
- **Migration Priority:** HIGH (testable prediction)

---

#### Appendix D: Dark Energy Equation of State
- **ID:** `appendix-d`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 4
  - D.1 Ghost Coefficient
  - D.2 Effective Dimension
  - D.3 Equation of State
  - D.4 Simulation Code
- **Key Content:** Dark energy w₀ calculation, effective dimension
- **Tables:** 0
- **Migration Priority:** HIGH (cosmological prediction)

---

#### Appendix E: Proton Decay Calculation
- **ID:** `appendix-e`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 4
  - E.1 GUT Scale Derivation
  - E.2 Proton Lifetime
  - E.3 Uncertainty Analysis
  - E.4 GUT Scale Exponent: κ = 1.46
- **Key Content:** Proton lifetime calculation, uncertainty analysis
- **Tables:** 0
- **Migration Priority:** HIGH (key testable prediction)

---

#### Appendix F: Dimensional Decomposition
- **ID:** `appendix-f`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 2
  - F.1 Compactification Structure
  - F.2 Simulation Code
- **Key Content:** Dimensional reduction details
- **Tables:** 1 (Dimensional decomposition table)
- **Migration Priority:** MEDIUM

---

#### Appendix G: Effective Torsion from Flux Quantization
- **ID:** `appendix-g`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 3
  - G.1 Flux Quantization
  - G.2 Effective Torsion
  - G.3 Simulation Code
- **Key Content:** Flux quantization, effective torsion derivation
- **Tables:** 0
- **Migration Priority:** MEDIUM

---

#### Appendix H: Proton Decay Branching Ratio
- **ID:** `appendix-h`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 2
  - H.1 Geometric Derivation
  - H.2 Simulation Code
- **Key Content:** Proton decay branching ratio p → e⁺π⁰
- **Tables:** 0
- **Migration Priority:** MEDIUM

---

#### Appendix I: Gravitational Wave Dispersion
- **ID:** `appendix-i`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 4
  - I.1 Orthogonal Time and GW Propagation
  - I.2 Dispersion Formula
  - I.3 Simulation Code
  - I.4 Alternative Derivation: Phenomenological Normalization
- **Key Content:** GW dispersion relation, testable prediction
- **Tables:** 1 (Dispersion comparison)
- **Migration Priority:** HIGH (testable with LIGO/Virgo)

---

#### Appendix J: Monte Carlo Error Propagation
- **ID:** `appendix-j`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 2
  - J.1 Error Summary
  - J.2 Simulation Code
- **Key Content:** Error analysis, uncertainty quantification
- **Tables:** 1 (Error summary)
- **Migration Priority:** MEDIUM

---

#### Appendix K: Transparency Statement
- **ID:** `appendix-k`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 4
  - K.1 Parameter Classification
  - K.2 Validation Statistics
  - K.3 Outstanding Issues Resolution
  - K.4 Source of Truth
- **Key Content:** Parameter classification, validation metrics
- **Tables:** 3 (Parameter classification, validation stats, issues)
- **Migration Priority:** HIGH (transparency and reproducibility)

---

#### Appendix L: Complete PM Values Summary
- **ID:** `appendix-l`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 6
  - L.1 Topological Parameters (Exact)
  - L.2 Gauge Unification Parameters
  - L.3 PMNS Matrix Parameters
  - L.4 Dark Energy Parameters
  - L.5 Proton Decay & Future Predictions
  - L.6 Fermion Masses (Selected)
- **Key Content:** Complete parameter summary tables
- **Tables:** 6 (one per subsection)
- **Migration Priority:** LOW (reference material, data already in simulations)

---

#### Appendix M: Speculative Extensions - Consciousness and the Pneuma Vacuum
- **ID:** `appendix-m`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 5
  - M.1 Orchestrated Objective Reduction (Orch OR) Overview
  - M.2 Speculative PM Vacuum Connection
  - M.3 Quantitative Framework
  - M.4 Future Directions and Potential Tests
  - M.5 Disclaimer and Status
- **Key Content:** Speculative consciousness connection, Orch OR
- **Tables:** 1 (Quantitative framework)
- **Migration Priority:** LOW (speculative content)

---

#### Appendix N: G₂ Topology Landscape
- **ID:** `appendix-topology-list`
- **Status in theory_output.json:** ❌ MISSING
- **Subsections:** 3
  - N.1 Search Parameters
  - N.2 Complete Valid Topology List
  - N.3 Key Observations
- **Key Content:** Complete list of 64 valid TCS topologies
- **Tables:** 3 (B2=3, B2=4, B2=5 topologies)
- **Migration Priority:** MEDIUM (reference data for topology selection)

---

## Mapping Analysis

### Current theory_output.json Sections vs Paper Sections

| theory_output.json ID | Title | Maps to Paper Section(s) | Coverage |
|---|---|---|---|
| 1 | Introduction | Section 1 | ✅ Complete |
| 2 | Geometric Framework | Sections 2, 3, 4 | ⚠️ Partial (3 sections compressed) |
| 3 | Fermion Sector | Section 6 | ⚠️ Good coverage |
| 4 | Gauge Unification | Section 5 | ⚠️ Good coverage |
| 5 | Cosmology and Predictions | Sections 7, 8 | ⚠️ Partial (2 sections compressed) |
| 6 | Conclusion | Section 9 | ⚠️ Partial coverage |
| - | (missing) | References | ❌ Not represented |
| - | (missing) | Appendices A-K | ❌ Not represented |
| - | (missing) | Appendices L-N | ❌ Not represented |

### Coverage Summary

**Well-Represented Content:**
- Section 1: Introduction ✅
- Section 5: Gauge Unification (in section 4) ✅
- Section 6: Fermion Sector (in section 3) ✅

**Compressed/Merged Content:**
- Sections 2-4 → theory_output.json section 2 "Geometric Framework"
- Sections 7-8 → theory_output.json section 5 "Cosmology and Predictions"

**Missing Content:**
- All 14 Appendices (A-N)
- References section
- Detailed subsection structure for most sections

---

## Migration Recommendations

### Phase 1: Core Content Expansion (High Priority)

**1. Separate Section 2 into Multiple Sections**
- Split theory_output.json section 2 into:
  - Section 2: "The 26-Dimensional Bulk Spacetime"
  - Section 3: "Reduction to 13-Dimensional Shadow"
  - Section 4: "Compactification on TCS G₂ Manifold"
- This matches paper structure more closely

**2. Separate Sections 7-8**
- Split theory_output.json section 5 into:
  - Section 7: "Cosmology and Dark Energy"
  - Section 8: "Predictions and Testability"
- This gives predictions proper prominence

**3. Expand Section 9 (Discussion)**
- Rename section 6 from "Conclusion" to "Discussion and Transparency"
- Add subsections for:
  - Input summary
  - Comparison with other models
  - Limitations and future work

### Phase 2: Appendices (High Priority Technical Content)

Add the following appendices with complete subsection structure:

**Critical Theory:**
- Appendix A: Virasoro Anomaly Cancellation
- Appendix B: Generation Number Derivation
- Appendix C: Atmospheric Mixing Angle

**Key Predictions:**
- Appendix D: Dark Energy Equation of State
- Appendix E: Proton Decay Calculation
- Appendix I: Gravitational Wave Dispersion

**Transparency:**
- Appendix K: Transparency Statement

### Phase 3: Supporting Appendices (Medium Priority)

- Appendix F: Dimensional Decomposition
- Appendix G: Effective Torsion
- Appendix H: Proton Decay Branching
- Appendix J: Monte Carlo Error Propagation
- Appendix N: G₂ Topology Landscape

### Phase 4: Reference Material (Low Priority)

- Appendix L: Complete PM Values Summary
- Appendix M: Speculative Extensions
- References Section

---

## Detailed Content Analysis

### Section Content Density

| Section | Subsections | Tables | Formulas (est.) | Lines (est.) |
|---|---|---|---|---|
| 1. Introduction | 3 | 1 | ~5 | ~100 |
| 2. 26D Bulk | 7 | 2 | ~15 | ~450 |
| 3. 13D Shadow | 3 | 0 | ~10 | ~200 |
| 4. G₂ Compactification | 4 | 2 | ~20 | ~400 |
| 5. Gauge Unification | 9 | 0 | ~25 | ~550 |
| 6. Fermion Sector | 11 | 2 | ~30 | ~450 |
| 7. Cosmology | 5 | 0 | ~15 | ~250 |
| 8. Predictions | 3 | 4 | ~10 | ~200 |
| 9. Discussion | 7 | 1 | ~5 | ~200 |
| Appendices A-N | 46 | 11 | ~80 | ~1500 |

**Total:** 98 subsections, 25 tables, ~215 formulas, ~4300 lines

---

## Key Formulas by Section

### Section 2: 26D Bulk
- Master action S_26D
- Virasoro constraints
- Pneuma field Lagrangian
- Racetrack superpotential
- Holographic entropy formula

### Section 3: 13D Shadow
- Sp(2,R) constraint equations
- Primordial spinor structure
- Dimensional reduction formulas

### Section 4: G₂ Compactification
- Effective Euler characteristic
- Generation number formula
- Flux quantization condition
- Effective torsion derivation
- TCS topology specification

### Section 5: Gauge Unification
- GUT scale M_GUT
- Unified coupling α_GUT
- Weinberg angle sin²θ_W
- Higgs VEV v_EW
- Proton lifetime τ_p
- Doublet-triplet splitting mechanism

### Section 6: Fermion Sector
- PMNS matrix elements
- Neutrino mass splittings
- CKM matrix elements
- Yukawa hierarchy ε^Q
- Fermion mass formulas (t, b, τ, etc.)

### Section 7: Cosmology
- Dark energy w₀, w_a
- Effective dimension d_eff
- Pneuma VEV φ_P
- Thermal time flow

### Section 8: Predictions
- KK graviton mass M_KK
- GW dispersion relation
- Hidden sector particle masses
- Mirror dark matter parameters

---

## Implementation Strategy

### Step 1: Schema Design
Define section schema in theory_output.json to support:
- Subsections (nested structure)
- Sub-subsections (3-level hierarchy)
- Appendix flag
- Content type (main/appendix/reference)
- Cross-references between sections

### Step 2: Content Migration
For each section/appendix:
1. Extract title, ID, subsection structure
2. Identify formula references (formulaRefs array)
3. Identify parameter references (paramRefs array)
4. Extract key takeaways
5. Write beginner-friendly summary
6. Map to existing simulation results

### Step 3: Validation
- Verify all section IDs match paper
- Ensure all subsections are captured
- Check formula and parameter references are valid
- Validate prevSection/nextSection links
- Test navigation flow

### Step 4: Enhancement
- Add learning objectives for each section
- Create difficulty ratings (beginner/intermediate/advanced)
- Link to relevant simulation files
- Add figure references when figures are created
- Include citation references

---

## Technical Considerations

### Section ID Convention
- Main sections: `"1"`, `"2"`, ..., `"9"`
- Appendices: `"A"`, `"B"`, ..., `"N"`
- References: `"references"`

### Subsection Structure
```json
"subsections": [
  {
    "id": "2.1",
    "title": "Motivation for (24,2) Signature",
    "formulaRefs": ["virasoro-anomaly"],
    "paramRefs": ["dimensions.SIGNATURE_INITIAL"],
    "subsections": []
  }
]
```

### Cross-References
- formulaRefs: Array of formula IDs from formula-registry.js
- paramRefs: Dot-notation paths to parameters in theory_output.json
- figureRefs: Array of figure IDs (when implemented)
- citationRefs: Array of reference keys (when implemented)

### Content Block Types
- derivation: Mathematical derivation
- explanation: Conceptual explanation
- table: Data table
- simulation: Link to simulation code
- prediction: Testable prediction
- issue: Known issue or limitation

---

## Estimated Migration Effort

| Phase | Sections/Appendices | Estimated Hours |
|---|---|---|
| Phase 1: Core sections 2-4, 7-8 | 5 sections | 10-15 hours |
| Phase 2: Critical appendices | 7 appendices | 14-20 hours |
| Phase 3: Supporting appendices | 5 appendices | 8-12 hours |
| Phase 4: Reference material | 2 appendices + refs | 4-6 hours |
| **Total** | **19 items** | **36-53 hours** |

---

## Migration Priorities by Section

### Immediate (Phase 1)
1. ✅ Section 2: 26D Bulk Spacetime (theory foundation)
2. ✅ Section 3: 13D Shadow (dimensional reduction)
3. ✅ Section 4: G₂ Compactification (topology selection)
4. ✅ Section 7: Cosmology (dark energy predictions)
5. ✅ Section 8: Predictions (testability)

### Soon (Phase 2)
6. ✅ Appendix A: Virasoro anomaly
7. ✅ Appendix B: Generation number
8. ✅ Appendix D: Dark energy EOS
9. ✅ Appendix E: Proton decay
10. ✅ Appendix I: GW dispersion
11. ✅ Appendix K: Transparency

### Later (Phase 3-4)
12. Appendix C: PMNS angle
13. Appendix F-H: Technical derivations
14. Appendix J: Error analysis
15. Appendix N: Topology list
16. Appendix L: Value summary
17. Appendix M: Speculative extensions
18. References section

---

## Success Metrics

### Coverage
- [ ] All 9 main sections represented
- [ ] All 14 appendices included
- [ ] References section added
- [ ] 100% of subsections captured

### Quality
- [ ] All formula references validated
- [ ] All parameter references validated
- [ ] Beginner summaries for all sections
- [ ] Key takeaways for all sections
- [ ] Navigation links (prev/next) complete

### Functionality
- [ ] Section renderer can display all content
- [ ] Formula lookups work for all sections
- [ ] Parameter lookups work for all sections
- [ ] Subsection navigation functional
- [ ] Search/filter by section works

---

## Notes

1. **Current Compression:** theory_output.json currently has 6 sections representing 9 paper sections + appendices. This is efficient but loses granularity.

2. **Recommended Structure:** Expand to 9+ main sections to match paper exactly, then add appendices as separate top-level entries or nested under an "appendices" object.

3. **Formula Integration:** Many formulas in the paper need corresponding entries in formula-registry.js. Cross-check and add missing formulas.

4. **Simulation Links:** Each appendix has a "Simulation Code" subsection. These should link to actual .py files in the simulations/ directory.

5. **Content Blocks:** The paper has rich narrative content. Consider extracting key paragraphs into contentBlocks arrays for rendering.

6. **Table Data:** 25 tables in the paper. Consider extracting table data into structured JSON for dynamic rendering.

---

## Next Steps

1. **Decide on structure:** Keep compressed (6 sections) or expand (9+ sections)?
2. **Create appendix schema:** Design how appendices fit into sections object
3. **Begin Phase 1 migration:** Expand sections 2, 7-8
4. **Add subsection support:** Implement nested subsection rendering
5. **Migrate formulas:** Ensure all paper formulas exist in formula-registry.js
6. **Link simulations:** Connect appendix code blocks to actual .py files

---

**End of Report**
