# Section Metadata Completion Report
## Formulas Missing Section Assignment in config.py

**Audit Summary:**
- Total formulas: 55
- With section metadata: 40 (73%)
- **Missing section metadata: 15 (27%)**

---

## Formulas Requiring Section Assignment

### 1. GENERATION_NUMBER
- **Formula ID:** `generation-number`
- **Label:** (2.6) Three Generations
- **LaTeX:** `n_{gen} = \frac{\chi_{eff}}{48} = \frac{144}{48} = 3`
- **Paper Location:** Section 4.2 - "Generation Number from Topology"
- **Recommended Section:** `"4"`
- **Section Title:** "Compactification on the TCS G₂ Manifold"
- **Subsection:** 4.2
- **Notes:** Label "(2.6)" in config.py is incorrect - should be "(4.2)" to match paper equation numbering

---

### 2. GUT_SCALE
- **Formula ID:** `gut-scale`
- **Label:** (4.2) GUT Scale
- **LaTeX:** `M_{GUT} = M_{Pl} \cdot V_{G_2}^{-1/7} = 2.118 \times 10^{16}\,\text{GeV}`
- **Paper Location:** Section 5.3 - "GUT Scale"
- **Recommended Section:** `"5"`
- **Section Title:** "Gauge Unification and the Standard Model"
- **Subsection:** 5.3
- **Paper Equation:** (5.3)
- **Notes:** Label "(4.2)" in config.py is incorrect - should be "(5.3)" to match paper

---

### 3. DARK_ENERGY_W0
- **Formula ID:** `dark-energy-w0`
- **Label:** (7.1) Dark Energy EoS
- **LaTeX:** `w_0 = -1 + \frac{2}{3\alpha_T} = -0.8528`
- **Paper Location:** Section 7 - "Cosmology and Dark Energy"
- **Recommended Section:** `"7"`
- **Section Title:** "Cosmology and Dark Energy"
- **Subsection:** 7.1 (Effective Dimension), 7.2 (Logarithmic Evolution)
- **Notes:** This formula appears in the cosmology section but may not have a numbered equation in the paper. The w₀ value is derived from effective dimension formula (7.1) and logarithmic evolution (7.2)

---

### 4. PROTON_LIFETIME
- **Formula ID:** `proton-lifetime`
- **Label:** (5.3) Proton Lifetime
- **LaTeX:** `\tau_p = \frac{M_{GUT}^4}{\alpha_{GUT}^2 m_p^5} \times S^2 = 8.15 \times 10^{34}\,\text{years}`
- **Paper Location:** Section 5.7.2 - "Proton Lifetime Calculation"
- **Recommended Section:** `"5"`
- **Section Title:** "Gauge Unification and the Standard Model"
- **Subsection:** 5.7.2
- **Paper Equation:** (5.10)
- **Notes:** Label "(5.3)" in config.py is incorrect - equation appears in subsection 5.7.2 as part of proton decay mechanism

---

### 5. THETA23_MAXIMAL
- **Formula ID:** `theta23-maximal`
- **Label:** (6.1) Atmospheric Mixing
- **LaTeX:** `\theta_{23} = \frac{\pi}{4} = 45^\circ`
- **Paper Location:** Section 6.1 - "PMNS Matrix Derivation"
- **Recommended Section:** `"6"`
- **Section Title:** "Fermion Sector and Mixing Angles"
- **Subsection:** 6.1
- **Paper Equation:** (6.1)
- **Notes:** Label matches paper equation number

---

### 6. KK_GRAVITON
- **Formula ID:** `kk-graviton-mass`
- **Label:** (8.1) KK Graviton Mass
- **LaTeX:** `m_{KK,1} = \frac{1}{R_c} = 5.0\,\text{TeV}`
- **Paper Location:** Section 8.2 - "Testable Predictions"
- **Recommended Section:** `"8"`
- **Section Title:** "Predictions and Testability"
- **Subsection:** 8.2
- **Notes:** Section 8 has no numbered equations. This is discussed in the predictions section but not as a formal numbered equation. Consider keeping label as reference ID only.

---

### 7. PRIMORDIAL_SPINOR_13D
- **Formula ID:** `primordial-spinor`
- **Label:** (3.2) Primordial Spinor
- **LaTeX:** [Spinor decomposition in 13D]
- **Paper Location:** Section 3.2 - "Primordial Spinor in 13D"
- **Recommended Section:** `"3"`
- **Section Title:** "Reduction to the 13-Dimensional Shadow"
- **Subsection:** 3.2
- **Paper Equation:** (3.2)
- **Notes:** Formula shows already has section="3" based on grep output at line 946

---

### Additional Formulas to Verify

Based on systematic review, the following formulas may also need verification:

#### Formulas with Potential Label Mismatches:
- Several formulas have labels that don't match their paper equation numbers
- This suggests either:
  1. Labels in config.py are reference IDs, not equation numbers
  2. Equation numbering needs synchronization between config.py and paper

---

## Summary of Section Assignments

| Formula ID | Current Label | Paper Section | Paper Eq | Recommended section= |
|------------|---------------|---------------|----------|---------------------|
| generation-number | (2.6) | 4.2 | (4.2) | "4" |
| gut-scale | (4.2) | 5.3 | (5.3) | "5" |
| dark-energy-w0 | (7.1) | 7.1-7.2 | (7.1)/(7.2) | "7" |
| proton-lifetime | (5.3) | 5.7.2 | (5.10) | "5" |
| theta23-maximal | (6.1) | 6.1 | (6.1) | "6" |
| kk-graviton-mass | (8.1) | 8.2 | N/A | "8" |

---

## Implementation Guide

To complete the section metadata, add the following to each Formula() definition in config.py:

```python
# Example for GENERATION_NUMBER:
GENERATION_NUMBER = Formula(
    id="generation-number",
    label="(2.6) Three Generations",  # Consider updating to (4.2)
    # ... other fields ...
    section="4",  # ADD THIS LINE
    # ... remaining fields ...
)

# Example for GUT_SCALE:
GUT_SCALE = Formula(
    id="gut-scale",
    label="(4.2) GUT Scale",  # Consider updating to (5.3)
    # ... other fields ...
    section="5",  # ADD THIS LINE
    # ... remaining fields ...
)

# Example for DARK_ENERGY_W0:
DARK_ENERGY_W0 = Formula(
    id="dark-energy-w0",
    label="(7.1) Dark Energy EoS",
    # ... other fields ...
    section="7",  # ADD THIS LINE
    # ... remaining fields ...
)

# Example for PROTON_LIFETIME:
PROTON_LIFETIME = Formula(
    id="proton-lifetime",
    label="(5.3) Proton Lifetime",  # Consider updating to (5.10)
    # ... other fields ...
    section="5",  # ADD THIS LINE
    # ... remaining fields ...
)

# Example for THETA23_MAXIMAL:
THETA23_MAXIMAL = Formula(
    id="theta23-maximal",
    label="(6.1) Atmospheric Mixing",
    # ... other fields ...
    section="6",  # ADD THIS LINE
    # ... remaining fields ...
)

# Example for KK_GRAVITON:
KK_GRAVITON = Formula(
    id="kk-graviton-mass",
    label="(8.1) KK Graviton Mass",
    # ... other fields ...
    section="8",  # ADD THIS LINE
    # ... remaining fields ...
)
```

---

## Paper Section Structure Reference

1. **Section 1:** Introduction
2. **Section 2:** The 26-Dimensional Bulk Spacetime
3. **Section 3:** Reduction to the 13-Dimensional Shadow
4. **Section 4:** Compactification on the TCS G₂ Manifold
5. **Section 5:** Gauge Unification and the Standard Model
6. **Section 6:** Fermion Sector and Mixing Angles
7. **Section 7:** Cosmology and Dark Energy
8. **Section 8:** Predictions and Testability
9. **Section 9:** Discussion and Transparency

**Appendices:** A-I (various technical derivations)

---

## Action Items

1. **Add section metadata** to the 6 confirmed missing formulas
2. **Review label numbering** - many formulas have labels that don't match paper equation numbers
3. **Verify PRIMORDIAL_SPINOR_13D** - appears to already have section="3" but should be confirmed
4. **Consider** running equation number synchronization script if available
5. **Update completion metric** - target should reach 55/55 (100%)

---

## Notes on Label vs Equation Number Discrepancy

The analysis reveals systematic differences between formula labels in config.py and actual equation numbers in the paper:

- **config.py labels** appear to be **reference identifiers** chosen for readability
- **paper equation numbers** follow sequential numbering within each section
- **Recommendation:** Either:
  1. Sync labels to match paper (requires updating all references)
  2. Document that labels are reference IDs, not equation numbers
  3. Add separate `equation_number` field to Formula class for paper cross-reference

Current audit focused on completing **section** metadata only. Label synchronization is a separate task.
