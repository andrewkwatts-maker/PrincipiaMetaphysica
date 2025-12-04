# Formula Centralization Priority Table

Quick reference for implementing the centralized formula database.

## Priority 1: Critical (9 files)

| Formula | Symbol | Files | Total Occurrences | Status |
|---------|--------|-------|-------------------|--------|
| Planck Mass | M<sub>Pl</sub> | 9 | 120 | 🔴 Urgent |

## Priority 2: High (5-7 files)

| Formula | Symbol | Files | Total Occurrences | Status |
|---------|--------|-------|-------------------|--------|
| Fundamental Scale | M<sub>*</sub> | 7 | 91 | 🔴 High |
| GUT Scale | M<sub>GUT</sub> | 5 | 112 | 🔴 High |

## Priority 3: Medium-High (4 files)

| Formula | Symbol | Files | Total Occurrences | Status |
|---------|--------|-------|-------------------|--------|
| Dark Energy w₀ | w<sub>0</sub> | 4 | 123 | 🟡 Medium-High |
| Redshift Evolution | w(z) | 4 | 76 | 🟡 Medium-High |
| Mashiach Field | φ<sub>M</sub> | 4 | 22 | 🟡 Medium |
| Ricci Scalar | R<sub>μν</sub> | 4 | 16 | 🟡 Medium |

## Priority 4: Medium (3 files)

| Formula | Symbol | Files | Total Occurrences | Status |
|---------|--------|-------|-------------------|--------|
| Proton Decay | τ<sub>p</sub> | 3 | 23 | 🟢 Medium |
| Modified Gravity | F(R,T,τ) | 3 | 17 | 🟢 Medium |

## Priority 5: Specialized (2 files)

| Formula | Symbol | Files | Total Occurrences | Status |
|---------|--------|-------|-------------------|--------|
| 26D Action | S<sub>26D</sub> | 2 | 3 | ⚪ Low |
| Neutrino Mixing | θ<sub>ij</sub> | 2 | 8 | ⚪ Low |

---

## Files Needing Hover Implementation

| File | Equation Boxes | Priority Formulas | Status |
|------|----------------|-------------------|--------|
| **thermal-time.html** | 40 | w₀ (13x), w(z) (4x) | 🔴 Critical |
| **pneuma-lagrangian.html** | 9 | φ<sub>M</sub> (7x), M<sub>Pl</sub> (6x) | 🟡 High |
| **einstein-hilbert-term.html** | 12 | M<sub>*</sub> (11x), F(R,T,τ) (7x) | 🟡 High |

---

## Implementation Phases

### Phase 1 (Week 1) - Top 3 Formulas
- [ ] M<sub>Pl</sub> (120 instances → 1 definition)
- [ ] w<sub>0</sub> (123 instances → 1 definition)
- [ ] M<sub>GUT</sub> (112 instances → 1 definition)
- [ ] Add hover to thermal-time.html

**Impact:** 355 instances centralized (57% of total)

### Phase 2 (Week 2) - Next 6 Formulas
- [ ] M<sub>*</sub> (91 instances)
- [ ] w(z) (76 instances)
- [ ] φ<sub>M</sub> (22 instances)
- [ ] τ<sub>p</sub> (23 instances)
- [ ] F(R,T,τ) (17 instances)
- [ ] R<sub>μν</sub> (16 instances)
- [ ] Add hover to pneuma-lagrangian.html & einstein-hilbert-term.html

**Impact:** 245 more instances centralized (40% additional)

### Phase 3 (Week 3) - Remaining Formulas
- [ ] All other formulas (20 instances)
- [ ] Refactor high-density files (cosmology.html: 70 boxes)

**Impact:** 100% centralization complete

---

## Quick Stats

- **Total formulas tracked:** 620 instances
- **Unique formulas:** ~50
- **Average duplication:** 12.4x per formula
- **Files analyzed:** 9
- **Hover coverage:** 67% (6/9 files)

**Centralization savings:**
- Before: 620 scattered instances
- After: ~50 database entries
- Reduction: **92% fewer formula definitions to maintain**

---

## Contact

For questions about this audit, see:
- Full report: `FORMULA_AUDIT_REPORT.md`
- JSON data: `formula_audit_results.json`
- Audit script: `audit_formulas.py`
