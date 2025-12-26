# Sections Metadata - JSON Structure Changes

This document shows the exact JSON structure changes made to sections in `theory_output.json`.

---

## Example: Section 3 (Fermion Sector)

### BEFORE (from audit)

```json
{
  "id": "3",
  "title": "Fermion Sector",
  "sectionType": "section",
  "parentId": "",
  "abstract": "Fermion masses and mixings arise from G₂ cycle intersections and Yukawa overlaps. The geometric Froggatt-Nielsen mechanism with ε = exp(-λ) ≈ 0.223 reproduces the observed mass hierarchies. CP violation emerges from H₃(G₂,Z) cycle orientations.",
  "contentBlocks": [],
  "appendices": [],
  "formulaRefs": [],          ← EMPTY
  "paramRefs": [],            ← EMPTY
  "figureRefs": [],
  "citationRefs": [],
  "prevSection": "2",
  "nextSection": "4",
  "subsections": [],
  "paperLineStart": 0,
  "paperLineEnd": 0,
  "sectionFile": "sections/fermion-sector.html",
  "beginnerSummary": "How particle masses (electron, quark masses) come from geometry. Different particles 'live' at different positions in the folded dimensions, which determines their mass.",
  "keyTakeaways": [
    "Three generations from χ_eff/48 = 144/48 = 3",
    "Mass hierarchies from geometric Froggatt-Nielsen: Y_f ∝ ε^Q_f",
    "Cabibbo angle ε ≈ 0.223 derived from G₂ curvature scale λ = 1.5",
    "Neutrino masses from G₂ volume modulus: m_ν ∝ exp(-b₃/(8π)) ≈ 0.05 eV",
    "CP phases from cycle orientations: δ_CP ∝ π × (orientation sum) / b₃"
  ],
  "learningObjectives": [],
  "websiteOnlyContent": []
}
```

**Missing fields:**
- ❌ No `order` field
- ❌ No `category` field
- ❌ No `description` field
- ❌ Empty `formulaRefs` array
- ❌ Empty `paramRefs` array

---

### AFTER (current state)

```json
{
  "id": "3",
  "title": "Fermion Sector",
  "order": 3,                                      ← ADDED
  "category": "phenomenology",                     ← ADDED
  "description": "Fermion masses, mixing angles, and CP violation from geometric cycles",  ← ADDED
  "sectionType": "section",
  "parentId": "",
  "abstract": "Fermion masses and mixings arise from G₂ cycle intersections and Yukawa overlaps. The geometric Froggatt-Nielsen mechanism with ε = exp(-λ) ≈ 0.223 reproduces the observed mass hierarchies. CP violation emerges from H₃(G₂,Z) cycle orientations.",
  "contentBlocks": [],
  "appendices": [],
  "formulaRefs": [                                 ← POPULATED
    "generation-number",
    "yukawa-instanton",
    "hierarchy-ratio",
    "top-quark-mass",
    "bottom-quark-mass",
    "tau-lepton-mass",
    "neutrino-mass-21",
    "neutrino-mass-31",
    "seesaw-mechanism",
    "ckm-elements",
    "cp-phase-geometric",
    "theta23-maximal"
  ],
  "paramRefs": [                                   ← POPULATED
    "topology.CHI_EFF",
    "topology.n_gen",
    "topology.B3",
    "neutrino.pmns_angles.theta_12",
    "neutrino.pmns_angles.theta_23",
    "neutrino.pmns_angles.theta_13",
    "neutrino.pmns_angles.delta_cp",
    "neutrino.mass_splittings.delta_m21_sq",
    "neutrino.mass_splittings.delta_m31_sq",
    "neutrino.mass_spectrum.m_nu_1",
    "neutrino.mass_spectrum.m_nu_2",
    "neutrino.mass_spectrum.m_nu_3",
    "neutrino.mass_spectrum.sum_m_nu",
    "neutrino.seesaw.m_rh_neutrino",
    "pmns.theta_12",
    "pmns.theta_23",
    "pmns.theta_13",
    "pmns.delta_CP"
  ],
  "figureRefs": [],
  "citationRefs": [],
  "prevSection": "2",
  "nextSection": "4",
  "subsections": [],
  "paperLineStart": 0,
  "paperLineEnd": 0,
  "sectionFile": "sections/fermion-sector.html",
  "beginnerSummary": "How particle masses (electron, quark masses) come from geometry. Different particles 'live' at different positions in the folded dimensions, which determines their mass.",
  "keyTakeaways": [
    "Three generations from χ_eff/48 = 144/48 = 3",
    "Mass hierarchies from geometric Froggatt-Nielsen: Y_f ∝ ε^Q_f",
    "Cabibbo angle ε ≈ 0.223 derived from G₂ curvature scale λ = 1.5",
    "Neutrino masses from G₂ volume modulus: m_ν ∝ exp(-b₃/(8π)) ≈ 0.05 eV",
    "CP phases from cycle orientations: δ_CP ∝ π × (orientation sum) / b₃"
  ],
  "learningObjectives": [],
  "websiteOnlyContent": []
}
```

**Added fields:**
- ✓ `order`: 3
- ✓ `category`: "phenomenology"
- ✓ `description`: "Fermion masses, mixing angles, and CP violation from geometric cycles"
- ✓ `formulaRefs`: 12 formula IDs (all validated)
- ✓ `paramRefs`: 18 parameter paths (all validated)

---

## Summary of Changes Across All Sections

### Section 1: Introduction
**New fields added:**
```json
{
  "order": 1,
  "category": "framework",
  "description": "Overview of the 26D geometric framework and dimensional reduction mechanism",
  "formulaRefs": [6 items],
  "paramRefs": [8 items]
}
```

### Section 2: Geometric Framework
**New fields added:**
```json
{
  "order": 2,
  "category": "framework",
  "description": "Detailed mathematical structure of dimensional reduction and G₂ compactification",
  "formulaRefs": [11 items],
  "paramRefs": [15 items]
}
```

### Section 3: Fermion Sector
**New fields added:**
```json
{
  "order": 3,
  "category": "phenomenology",
  "description": "Fermion masses, mixing angles, and CP violation from geometric cycles",
  "formulaRefs": [12 items],
  "paramRefs": [18 items]
}
```

### Section 4: Gauge Unification
**New fields added:**
```json
{
  "order": 4,
  "category": "phenomenology",
  "description": "GUT scale unification, proton decay, and gauge symmetry breaking",
  "formulaRefs": [15 items],
  "paramRefs": [12 items]
}
```

### Section 5: Cosmology and Predictions
**New fields added:**
```json
{
  "order": 5,
  "category": "predictions",
  "description": "Dark energy, KK gravitons, gravitational waves, and observable signatures",
  "formulaRefs": [17 items],
  "paramRefs": [13 items]
}
```

### Section 6: Conclusion
**New fields added:**
```json
{
  "order": 6,
  "category": "framework",
  "description": "Summary of predictions, testability, and future experimental prospects",
  "formulaRefs": [8 items],
  "paramRefs": [8 items]
}
```

---

## Change Statistics

### Fields Added Per Section
- 3 new scalar fields: `order`, `category`, `description`
- 2 populated array fields: `formulaRefs`, `paramRefs`

### Total Additions
- **New scalar fields:** 6 sections × 3 fields = 18 fields
- **Populated arrays:** 6 sections × 2 arrays = 12 arrays
- **Total formula references:** 69 IDs
- **Total parameter references:** 74 paths

### Data Integrity
- **All formula IDs validated:** 100% (69/69)
- **All parameter paths validated:** 100% (74/74)
- **No existing data modified:** All original fields preserved
- **No data loss:** 100% backward compatible

---

## Field Definitions

### `order` (number)
Sequential position of section in the document (1-6).
- **Type:** Integer
- **Range:** 1-6
- **Purpose:** Explicit ordering for table of contents and navigation

### `category` (string)
Logical grouping for section organization.
- **Type:** String
- **Values:** "framework" | "phenomenology" | "predictions"
- **Purpose:** Hierarchical organization and filtering

### `description` (string)
Concise one-sentence overview of section content.
- **Type:** String
- **Length:** ~60-100 characters
- **Purpose:** Quick reference and navigation aid

### `formulaRefs` (array of strings)
Formula IDs referenced in this section.
- **Type:** Array<string>
- **Format:** Formula IDs from formulas database
- **Purpose:** Cross-referencing, validation, dependency tracking

### `paramRefs` (array of strings)
Parameter paths referenced in this section.
- **Type:** Array<string>
- **Format:** Dot-notation paths (e.g., "topology.CHI_EFF")
- **Purpose:** Cross-referencing, validation, dependency tracking

---

## Backward Compatibility

All changes are **100% backward compatible**:

1. **Additive only:** Only new fields added, no existing fields modified
2. **Optional consumption:** Systems can ignore new fields if not needed
3. **Preserves structure:** All original arrays and objects maintained
4. **Safe for existing code:** Code that reads sections will continue to work

### Example: Backward Compatible Reading

```python
# Old code - still works
section_title = sections["3"]["title"]
section_abstract = sections["3"]["abstract"]

# New code - can use additional metadata
section_order = sections["3"].get("order", 0)
section_category = sections["3"].get("category", "uncategorized")
formulas_used = sections["3"].get("formulaRefs", [])
```

---

## Validation Checklist

For each section, verify:

- [x] `id` field exists
- [x] `title` field exists
- [x] `order` field exists and is 1-6
- [x] `category` field exists and is valid value
- [x] `description` field exists and is non-empty
- [x] `formulaRefs` array populated (6-17 items)
- [x] `paramRefs` array populated (8-18 items)
- [x] All formula IDs exist in formulas database
- [x] All parameter paths exist in parameters structure
- [x] No duplicate references
- [x] All existing fields preserved

**Status: All checks passed ✓**

---

**Document Date:** 2025-12-26
**JSON Structure Version:** 14.1
**Validation Status:** Complete ✓
