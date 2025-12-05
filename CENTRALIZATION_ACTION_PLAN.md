# Centralization Action Plan

**Current Score: 47.6/100 🔴 CRITICAL**
**Target Score: 90+/100 🟢 EXCELLENT**

This document outlines the action plan to achieve complete centralization of the Principia Metaphysica website, ensuring single source of truth for all content, values, and formulas.

---

## Executive Summary

The validation revealed:
- ✅ **Strong Foundation**: 404 topic sections implemented, 47 PM references working
- 🔴 **Critical Issues**: 571 hardcoded numbers, 50 broken links, 31 orphaned files
- 🟡 **Important Work**: 1720 orphaned formulas, 46 orphaned content blocks

---

## Phase 1: Complete sections_content.py Coverage (Priority 1)

**Goal**: Add all 31 orphaned HTML files to sections_content.py

### 1.1 Core Section Pages (10 files)
These are main theory sections that MUST be in sections_content.py:

```
✅ sections/geometric-framework.html (DONE)
✅ sections/fermion-sector.html (DONE)
✅ sections/pneuma-lagrangian.html (DONE)
✅ sections/einstein-hilbert-term.html (DONE)
✅ sections/theory-analysis.html (DONE)
✅ sections/formulas.html (DONE)

❌ sections/cosmology.html (NEEDS MIGRATION)
❌ sections/gauge-unification.html (NEEDS MIGRATION)
❌ sections/thermal-time.html (NEEDS MIGRATION)
❌ sections/predictions.html (NEEDS MIGRATION)
❌ sections/introduction.html (NEEDS MIGRATION)
❌ sections/conclusion.html (NEEDS MIGRATION)
❌ sections/xy-gauge-bosons.html (NEEDS MIGRATION)
❌ sections/division-algebra-section.html (NEEDS MIGRATION)
❌ sections/cmb-bubble-collisions-comprehensive.html (NEEDS MIGRATION)
❌ sections/pneuma-lagrangian-new.html (NEEDS MIGRATION - or DELETE if duplicate)
```

**Action**: Create section definitions in sections_content.py for all 10 missing section pages

### 1.2 Foundation Pages (13 files)
Educational pages explaining core concepts:

```
❌ foundations/einstein-field-equations.html
❌ foundations/ricci-tensor.html
❌ foundations/clifford-algebra.html
❌ foundations/yang-mills.html
❌ foundations/kaluza-klein.html
❌ foundations/g2-manifolds.html
❌ foundations/so10-gut.html
❌ foundations/boltzmann-entropy.html
❌ foundations/kms-condition.html
❌ foundations/tomita-takesaki.html
❌ foundations/dirac-equation.html
❌ foundations/einstein-hilbert-action.html
❌ foundations/calabi-yau.html
```

**Action**: Create "foundations" category in sections_content.py with all 13 pages

### 1.3 Support Pages (8 files)
Reference, guide, and supplementary pages:

```
❌ beginners-guide.html
❌ philosophical-implications.html
❌ references.html
❌ visualization-index.html
❌ diagrams/theory-diagrams.html
❌ docs/beginners-guide-printable.html
❌ docs/computational-appendices.html
❌ docs/PAPER_2T_UPDATE_SECTION.html
```

**Decision Needed**:
- Should these be in sections_content.py?
- Or document as "intentionally standalone" in a STANDALONE_PAGES.md file?
- Recommendation: Add to sections_content.py for completeness

---

## Phase 2: Replace Hardcoded Numbers with PM References (Priority 1)

**Goal**: Replace all 571 hardcoded numbers with PM.* references

### 2.1 Identify Missing PM Constants

Many hardcoded numbers don't have PM references yet. Need to:

1. Audit `theory_output.json` to see what values exist
2. Identify values that need to be added to `config.py`
3. Run simulations to generate missing values
4. Update `generate_enhanced_constants.py` to include all values

### 2.2 Common Hardcoded Values Found

From validation report:
- `12.589` (appears in predictions.html) - This is D_eff, should be PM.shared_dimensions.D_eff
- `2.118` (appears in predictions.html) - This is M_GUT in 10^16 GeV, should be PM.proton_decay.M_GUT
- DOI numbers in references.html (these are OK to hardcode)
- arXiv IDs in references.html (these are OK to hardcode)

### 2.3 Migration Strategy

Create script: `replace_hardcoded_with_pm.py`

```python
# Identify hardcoded numbers
# Match to existing PM constants
# Generate replacement HTML with data-category/data-param
# Create migration report
```

**Action**: Create and run hardcoded number migration script

---

## Phase 3: Fix Broken Links (Priority 1)

**Goal**: Fix all 50 broken links

### 3.1 Common Issues Found

1. **Missing anchor targets**: Links to `#abstract`, `#sections`, `#predictions` that don't exist
2. **Non-existent pages**: `dirac-lagrangian.html`, `generation-formula.html`, `thermal-time-relation.html`
3. **Moved files**: `beginners-guide-printable.html` is in `docs/` but links point to root

### 3.2 Resolution Strategy

For each broken link category:

**A. Missing anchors** (e.g., `../index.html#abstract`)
- Add topic IDs to target pages
- Or update links to correct IDs

**B. Non-existent pages** (e.g., `dirac-lagrangian.html`)
- Option 1: Create the page
- Option 2: Redirect to existing page with that content
- Option 3: Remove the link

**C. Moved files** (e.g., `beginners-guide-printable.html`)
- Update all links to include `docs/` prefix
- Or move file back to root

**Action**: Create `fix_broken_links.py` script to systematically fix all 50 broken links

---

## Phase 4: Integrate Orphaned Content (Priority 2)

**Goal**: Integrate 46 orphaned content blocks into topic sections

### 4.1 Files with Orphaned Content

```
calabi-yau.html: 10 blocks
g2-manifolds.html: 9 blocks
index.html: 5 blocks
principia-metaphysica-paper.html: 4 blocks
thermal-time.html: 2 blocks
... (16 more blocks in other files)
```

### 4.2 Integration Strategy

Each orphaned content block (card, panel, detail-section) should be:

1. Nested under a topic heading (h2, h3, h4 with topic ID)
2. Or the block itself should have a topic ID

Example transformation:

**Before** (orphaned):
```html
<div class="detail-section">
  <h4>Why Calabi-Yau Manifolds?</h4>
  <p>Content...</p>
</div>
```

**After** (integrated):
```html
<section id="why_calabi_yau">
  <h3>Why Calabi-Yau Manifolds?</h3>
  <div class="detail-section">
    <p>Content...</p>
  </div>
</section>
```

**Action**: Create `integrate_orphaned_content.py` script or deploy agents to fix each file

---

## Phase 5: Integrate Orphaned Formulas (Priority 2)

**Goal**: Integrate 1720 orphaned formulas into topic sections

### 5.1 Current State

- **Integrated**: 1099 formulas (39%)
- **Orphaned**: 1720 formulas (61%)

### 5.2 Why Formulas Are Orphaned

Formulas are orphaned when they appear in content that isn't nested under a topic heading.

Common pattern:
```html
<div class="card">  <!-- No topic ID on parent -->
  <h4>Einstein Field Equations</h4>
  <math>R_μν - ½g_μν R = 8πG T_μν</math>  <!-- Orphaned -->
</div>
```

Should be:
```html
<section id="einstein_field_equations">
  <h3>Einstein Field Equations</h3>
  <div class="card">
    <math>R_μν - ½g_μν R = 8πG T_μν</math>  <!-- Now integrated -->
  </div>
</section>
```

### 5.3 Strategy

Most orphaned formulas will be fixed automatically when we:
1. Add missing topic IDs to headings
2. Wrap orphaned content blocks in topic sections

**Action**: After Phase 4, re-run validation to see remaining orphaned formulas

---

## Implementation Timeline

### Week 1: Foundation (Phase 1)
- [ ] Day 1-2: Add all 10 missing section pages to sections_content.py
- [ ] Day 3-4: Add all 13 foundation pages to sections_content.py
- [ ] Day 5: Add 8 support pages to sections_content.py or document as standalone
- [ ] Day 6: Regenerate constants and validate coverage

**Deliverable**: sections_content.py with 38+ pages defined

### Week 2: Critical Fixes (Phase 2-3)
- [ ] Day 1-2: Create and run hardcoded number migration script
- [ ] Day 3: Fix broken links (50 links)
- [ ] Day 4-5: Validate and test all PM references work
- [ ] Day 6: Regenerate all constants and test website

**Deliverable**: Zero hardcoded numbers, zero broken links

### Week 3: Content Integration (Phase 4-5)
- [ ] Day 1-3: Integrate 46 orphaned content blocks
- [ ] Day 4-5: Add missing topic IDs to fix remaining orphaned formulas
- [ ] Day 6: Final validation run

**Deliverable**: 90+ centralization score

---

## Validation Targets

### Current State (v1.0)
```
Centralization Score: 47.6/100 🔴
- PM References: 47
- Hardcoded Numbers: 571 🔴
- Topic Sections: 404
- Orphaned Content: 46 🔴
- Orphaned Files: 31 🔴
- Broken Links: 50 🔴
- Formulas Integrated: 39%
```

### Target State (v2.0)
```
Centralization Score: 90+/100 🟢
- PM References: 150+
- Hardcoded Numbers: 0 ✅
- Topic Sections: 500+
- Orphaned Content: 0 ✅
- Orphaned Files: 0 ✅
- Broken Links: 0 ✅
- Formulas Integrated: 95%+
```

---

## Next Immediate Actions

1. ✅ **DONE**: Run comprehensive validation
2. ✅ **DONE**: Generate centralization report
3. **NEXT**: Decide on approach for the 31 orphaned files:
   - Option A: Migrate all to sections_content.py (recommended for completeness)
   - Option B: Migrate section/foundation pages only, document others as standalone
4. **THEN**: Start Phase 1 - Add missing pages to sections_content.py

---

## Scripts Created

1. ✅ `validate_centralization.py` - Comprehensive validation tool
2. ⏳ `replace_hardcoded_with_pm.py` - Hardcoded number migration (TODO)
3. ⏳ `fix_broken_links.py` - Broken link fixer (TODO)
4. ⏳ `integrate_orphaned_content.py` - Content integration tool (TODO)
5. ⏳ `add_missing_pages_to_sections.py` - Bulk page addition to sections_content.py (TODO)

---

## Questions for User

1. **Orphaned Files**: Should all 31 files be added to sections_content.py, or should some (like references.html, docs/*) remain standalone?

2. **Duplicate File**: `sections/pneuma-lagrangian-new.html` vs `sections/pneuma-lagrangian.html` - which one to keep?

3. **Priority**: Should we focus on section pages first (10 files) and defer foundation pages (13 files)?

4. **Broken Links**: For non-existent pages like `dirac-lagrangian.html`, should we:
   - Create them?
   - Redirect to existing pages?
   - Remove the links?

---

*Generated by validate_centralization.py*

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
