# V22.5 Publication Polish Plan

**Date:** 2026-01-20
**Status:** IN PROGRESS
**Scrum Master:** Claude Opus 4.5
**Product Owner/Peer Reviewer:** Gemini

---

## Executive Summary

All 25 parameters are within 1σ (PUBLICATION_READY). This plan focuses on:
1. **HTML Polish**: Replace hardcoded values with PM params
2. **LaTeX Polish**: Clean formula rendering
3. **Master Action Verification**: 100% physics recovery
4. **Certificate Updates**: Reflect v22.5.1
5. **Parameter Review**: Decide refinements vs. leave as-is

---

## Current Parameter Status (All PASS)

| # | Parameter | Sigma | Decision |
|---|-----------|-------|----------|
| 1 | θ₁₃ (Reactor) | 0.89 | LEAVE AS-IS (already <1σ) |
| 2 | η_baryon | 0.80 | LEAVE AS-IS (already <1σ) |
| 3 | sin²θW | 0.69 | LEAVE AS-IS (already <1σ) |
| 4 | G_F | 0.69 | LEAVE AS-IS (already <1σ) |
| 5 | T_CMB | 0.56 | LEAVE AS-IS (excellent) |
| 6 | w_a | 0.54 | LEAVE AS-IS (excellent) |

**Rationale**: All parameters are well within 1σ. Further refinement risks:
- Overbaking adjustments
- Introducing numerology
- Losing geometric clarity

---

## Workstream A: HTML File Polish

### Files to Review
- Pages/index.html
- Pages/philosophical-implications.html
- Pages/faq.html
- Pages/beginners-guide.html
- Pages/parameters.html
- Pages/visualization-index.html
- foundations/*.html

### Tasks
1. Find all hardcoded numeric values
2. Replace with `<span class="pm-value" data-pm-value="...">` format
3. Ensure consistency with config.py values
4. Verify all v22.5 terminology (24,1 signature, unified time, etc.)

---

## Workstream B: LaTeX Formula Polish

### Focus Areas
1. Review FORMULAS.md for rendering issues
2. Check appendix LaTeX equations
3. Ensure consistent notation:
   - χ_eff vs chi_eff
   - b₃ vs b_3
   - Proper subscripts/superscripts

### Quality Criteria
- All formulas render correctly in MathJax
- Consistent notation throughout
- Clear derivation chains

---

## Workstream C: Master Action Physics Recovery

### Verification Checklist
1. ☐ Gravity sector (Einstein-Hilbert + higher curvature)
2. ☐ Gauge sector (SM gauge fields)
3. ☐ Higgs sector (Brane-localized)
4. ☐ Fermion sector (Chiral from G2)
5. ☐ Dark matter (Mirror sector)
6. ☐ Cosmology (DESI-compatible w0, wa)
7. ☐ Neutrino mixing (PMNS from triality)
8. ☐ CKM mixing (From octonionic structure)

### Key Formula
$$S_{master} = S_{EH} + S_{gauge} + S_{Higgs} + S_{fermion} + S_{portal}$$

---

## Workstream D: Certificate Updates

### Current Version
- OMEGA_HASH: v21.0 sealed
- Certificates: v16.2 format

### Required Updates
1. Regenerate certificates with v22.5.1 version string
2. Update OMEGA seal metadata
3. Verify all 72 gates pass

---

## Workstream E: Appendix Derivation Polish

### Priority Appendices
1. appendix_a_master_action.md - Full Lagrangian
2. appendix_b_dimensional_reduction.md - 25D → 4D chain
3. appendix_c_gauge_unification.md - SO(10) → SM
4. appendix_d_electroweak.md - sin²θW derivation
5. appendix_g_euclidean_bridge.md - G.11 localization (DONE)

### Derivation Requirements
- Step-by-step mathematics
- Clear physical interpretation
- Connection to observables

---

## Agent Allocation

| Agent | Workstream | Gemini Role |
|-------|------------|-------------|
| HTML-Polish | A | Review diffs for consistency |
| LaTeX-Polish | B | Verify formula correctness |
| Master-Action | C | Physics completeness review |
| Certificate | D | Version validation |
| Appendix | E | Derivation rigor check |

---

## Decision Framework

### When to Refine Parameters
✓ REFINE if:
- Sigma > 2.0 AND geometric improvement is clear
- Formula has known approximation that can be improved
- Experimental value updated significantly

✗ LEAVE AS-IS if:
- Sigma < 1.0 (current situation - ALL parameters)
- Refinement introduces arbitrary factors
- No clear geometric justification

### Current Decision: LEAVE ALL PARAMETERS AS-IS
All parameters are within 1σ. The framework is PUBLICATION_READY.

---

## Gemini Consultation Points

1. **Parameter Refinements**: Confirm leave-as-is decision
2. **LaTeX Notation**: Review for consistency
3. **Master Action**: Verify all sectors included
4. **Derivation Rigor**: Check step-by-step logic

---

*Plan created: 2026-01-20*
*Status: READY FOR AGENT DEPLOYMENT*
