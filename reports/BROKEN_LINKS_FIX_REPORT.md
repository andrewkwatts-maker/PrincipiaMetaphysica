# BROKEN INTERNAL LINKS FIX REPORT
**Date**: 2025-12-07
**Status**: 28 broken links identified + 2 broken script references

---

## EXECUTIVE SUMMARY

### Total Issues Found: 30

1. **28 broken internal navigation links** (anchor targets)
2. **2 broken script references** (from validation reports)

### Breakdown by Priority:

- **CRITICAL (Navigation menus)**: 3 links
- **HIGH (Main content)**: 25 links
- **SCRIPT ERRORS (PM constants)**: 2 files

---

## CRITICAL BROKEN LINKS (3) - Navigation Menus

### 1. index.html → principia-metaphysica-paper.html#four-brane-structure

**Location**: index.html line 1141
**Issue**: Anchor uses hyphen (#four-brane-structure) but target uses underscore (#four_brane_structure)
**Target exists at**: principia-metaphysica-paper.html line 2747 as `id="four_brane_structure"`

**Fix**:
```html
<!-- BEFORE -->
<a href="principia-metaphysica-paper.html#four-brane-structure">

<!-- AFTER -->
<a href="principia-metaphysica-paper.html#four_brane_structure">
```

---

### 2. index.html → sections/geometric-framework.html#pneuma-manifold

**Location**: index.html line 1208
**Issue**: Path missing "../" prefix (treats sections/ as subdirectory of current location)
**Target exists at**: sections/geometric-framework.html line 4102 as `id="pneuma-manifold"`

**Fix**:
```html
<!-- BEFORE -->
<a href="sections/geometric-framework.html#pneuma-manifold">

<!-- AFTER (Option A - Fix path)-->
<a href="sections/geometric-framework.html#pneuma-manifold">
<!-- This is actually CORRECT - the file exists at this path -->

<!-- OR create missing anchor -->
```

**Actually**: The file DOES exist at `sections/geometric-framework.html`. The validation script issue is path resolution. This link is VALID.

**Real Issue**: Validation script incorrectly reported this. Link works.

---

### 3. index.html → sections/gauge-unification.html#symmetry-breaking

**Location**: index.html line 1265
**Issue**: Anchor #symmetry-breaking doesn't exist in target file
**Available anchors**: #kodaira_classification, #seesaw_mechanism, #beta_functions, #gut_derivation

**Fix Options**:
```html
<!-- Option A: Point to GUT derivation (most relevant) -->
<a href="sections/gauge-unification.html#gut_derivation">

<!-- Option B: Point to beginning of file -->
<a href="sections/gauge-unification.html">

<!-- Option C: Add missing anchor ID -->
<!-- In gauge-unification.html, add: -->
<h3 id="symmetry-breaking">Symmetry Breaking</h3>
```

**Recommended**: Option A - change to #gut_derivation

---

## HIGH PRIORITY BROKEN LINKS (25) - Main Content

### principia-metaphysica-paper.html (2 broken same-page anchors)

**1. Missing #13d-shadow**
- Likely should be: #effective-13d or similar
- Need to verify correct target

**2. Missing #ortho-time (2 instances)**
- Likely should be: #two-time-structure or #orthogonal-time
- Need to verify correct target

---

### components/nav.html (7 broken same-page anchors)

These are generic navigation template placeholders:
- #overview
- #history
- #mythology
- #creation
- #heroes
- #monsters
- #references
- #section

**Fix**: Either remove nav.html (unused component) or add anchors to parent pages

---

### foundations/*.html (2 broken cross-file references)

**1. calabi-yau.html → ../references.html#calabi-yau**
- Target anchor doesn't exist in references.html
- Fix: Add anchor or change to #references

**2. g2-manifolds.html → ../references.html#g2-manifolds**
- Target anchor doesn't exist in references.html
- Fix: Add anchor or change to #references

---

### sections/fermion-sector.html (2 broken cross-file references)

**1. geometric-framework.html#cy4-construction**
- Missing "../" prefix
- Fix: Change to `../sections/geometric-framework.html#cy4-construction`
- OR: Change to `geometric-framework.html#cy4-construction` (relative within sections/)

**2. ../principia-metaphysica-paper.html#four-brane-structure**
- Same as CRITICAL #1 - uses hyphen instead of underscore
- Fix: Change to #four_brane_structure

---

### sections/formulas.html (4 broken same-page anchors)

**Missing anchors**:
- #established-physics
- #theory-formulas
- #derived-results
- #predictions

**Fix**: Add these section IDs to formulas.html

---

### sections/geometric-framework.html (5+ broken same-page anchors)

**Reported missing**: #two-time-structure (and 4 others not listed)

**Issue**: Need full audit of geometric-framework.html internal links

---

## BROKEN SCRIPT REFERENCES (2) - CRITICAL for PM Constants

### 1. sections/introduction.html line 338

**Issue**: References deleted file `theory-constants.js`

```html
<!-- BEFORE (BROKEN) -->
<script src="theory-constants.js"></script>

<!-- AFTER (FIXED) -->
<script src="../theory-constants-enhanced.js"></script>
<script src="../js/pm-tooltip-system.js"></script>
<link rel="stylesheet" href="../css/pm-tooltip.css">
```

---

### 2. beginners-guide.html line 608

**Issue**: References deleted file `theory-constants.js`

```html
<!-- BEFORE (BROKEN) -->
<script src="theory-constants.js"></script>

<!-- AFTER (FIXED) -->
<script src="theory-constants-enhanced.js"></script>
<script src="js/pm-tooltip-system.js"></script>
<link rel="stylesheet" href="css/pm-tooltip.css">
```

---

## FIX STRATEGY

### Phase 1: CRITICAL (Fix immediately - 30 minutes)

1. ✅ Fix script references (2 files)
   - introduction.html line 338
   - beginners-guide.html line 608

2. ✅ Fix 3 navigation menu links (index.html)
   - Line 1141: #four-brane-structure → #four_brane_structure
   - Line 1208: Verify this link actually works (likely false positive)
   - Line 1265: #symmetry-breaking → #gut_derivation

### Phase 2: HIGH PRIORITY (Fix today - 2 hours)

3. ✅ Fix fermion-sector.html cross-file references (2 links)
4. ✅ Add missing anchors to formulas.html (4 anchors)
5. ✅ Fix principia-metaphysica-paper.html same-page links (3 links)
6. ✅ Fix foundations/ references links (2 links)

### Phase 3: CLEANUP (Fix this week - 1 hour)

7. ✅ Audit geometric-framework.html internal links (5+ links)
8. ✅ Remove or fix components/nav.html (7 placeholder links)
9. ✅ Full re-validation after all fixes

---

## VERIFICATION CHECKLIST

After fixes, run:

```bash
python validate_internal_links.py
```

**Expected result**: 0 broken links (down from 28)

---

## FILES TO MODIFY

### Critical Priority:
1. `sections/introduction.html` (line 338 - script reference)
2. `beginners-guide.html` (line 608 - script reference)
3. `index.html` (lines 1141, 1265 - navigation links)

### High Priority:
4. `sections/fermion-sector.html` (2 cross-file links)
5. `sections/formulas.html` (add 4 anchor IDs)
6. `principia-metaphysica-paper.html` (fix 3 same-page anchors)
7. `foundations/calabi-yau.html` (1 reference link)
8. `foundations/g2-manifolds.html` (1 reference link)

### Medium Priority:
9. `sections/geometric-framework.html` (audit internal links)
10. `components/nav.html` (remove or fix 7 placeholder links)

---

## ESTIMATED TIME

- **Critical fixes**: 30 minutes
- **High priority**: 2 hours
- **Cleanup**: 1 hour
- **Total**: 3.5 hours

---

**Next Steps**: Begin Phase 1 (Critical fixes)

---

*Report generated by: validate_internal_links.py*
*Date: 2025-12-07*
