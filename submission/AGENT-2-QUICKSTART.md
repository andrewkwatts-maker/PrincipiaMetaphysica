# AGENT 2: Quick Start Guide

## Your Mission

Convert the **Introduction** and **Theoretical Foundations** sections from the HTML paper to LaTeX format and insert them into the template.

## Files You Need

**Input:**
- `h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html` (source content)

**Output:**
- `h:/Github/PrincipiaMetaphysica/submission/principia-metaphysica-submission.tex` (edit this file)

**Reference:**
- `h:/Github/PrincipiaMetaphysica/submission/equations-converted.tex` (pre-converted equations)
- `h:/Github/PrincipiaMetaphysica/submission/equation-index.txt` (equation locations)

## Sections You Need to Fill

### 1. Section I: Introduction (Line 102-110)
Replace the TODO comment with content from HTML section "1. Introduction and Motivation"

**Expected Content:**
- Motivation for unified framework
- Standard Model limitations
- Brief overview of M-theory and G₂ manifolds
- Paper outline

### 2. Section II: Theoretical Foundations (Line 116-149)

**Subsection A: G₂ Holonomy and M-Theory Compactification (Line 121-129)**
- Extract from HTML section "3. Geometric Structure: The Pneuma Manifold"
- Define G₂ manifolds
- Explain holonomy groups
- Describe M-theory compactification

**Subsection B: Sp(2,ℝ) Gauge Fixing via BRST (Line 131-139)**
- Extract from HTML section "2.1.2 Sp(2,R) Gauge Symmetry"
- Explain two-time physics
- BRST quantization procedure
- Ghost state removal

**Subsection C: Dimensional Reduction: 26D → 13D → 7D → 4D (Line 141-149)**
- Extract from HTML sections 2.1.1, 2.1.3, 2.2.1
- 26D starting point
- Sp(2,R) projection to 13D
- G₂ compactification to 6D
- Brane structure to 4D

## HTML Section Mapping

| LaTeX Section | HTML Section ID | HTML Section Title |
|--------------|----------------|-------------------|
| I. Introduction | `#intro` | 1. Introduction and Motivation |
| II.A | `#geometry` | 3. Geometric Structure |
| II.B | `#sp2r_gauge` | 2.1.2 Sp(2,R) Gauge Symmetry |
| II.C | `#26d_structure`, `#13d-shadow`, `#four_brane_structure` | 2.1.1, 2.1.3, 2.2.1 |

## How to Edit

### Using the Edit Tool

```
Edit the file at line X, replacing:
OLD STRING: % TODO: Agent 2 will fill this section
NEW STRING: [Your actual LaTeX content here]
```

### Converting HTML to LaTeX

**HTML Tags to Remove:**
- `<p>`, `</p>`, `<div>`, `</div>`
- `<span>`, `</span>`
- `<em>`, `</em>` → `\emph{...}`
- `<strong>`, `</strong>` → `\textbf{...}`

**Subscripts/Superscripts:**
- `<sub>eff</sub>` → `$_{\text{eff}}$`
- `<sup>2</sup>` → `$^2$`
- `G<sub>2</sub>` → `$G_2$`

**Mathematical Expressions:**
- Inline math: `$...$`
- Display math: `\begin{equation}...\end{equation}`
- Aligned equations: `\begin{align}...\end{align}`

**Citations:**
- Add `\cite{reference_key}` where appropriate
- Note which references you need for Agent 7

## Pre-Converted Equations

Check `equations-converted.tex` for ready-to-use equations. Common ones you'll need:

**Dimensional reduction:**
```latex
\text{Signature: } (24,2) \xrightarrow{\text{Sp}(2,\mathbb{R})} (12,1) \xrightarrow{G_2} (5,1) \to (3,1)
```

**Generation count:**
```latex
n_{\text{gen}} = \frac{\chi_{\text{eff}}}{48} = \frac{144}{48} = 3
```

**Sp(2,R) gauge fixing:**
```latex
S = \int d^{26}x \sqrt{-g} \left[ R + \mathcal{L}_{\text{BRST}} \right]
```

## Checklist

Before marking your section complete:

- [ ] All TODO comments removed from your sections
- [ ] HTML converted to clean LaTeX
- [ ] All equations properly formatted with `\label{eq:...}`
- [ ] Citations added (even if just `\cite{TODO}`)
- [ ] Mathematical symbols use LaTeX commands, not Unicode
- [ ] Subscripts/superscripts in math mode
- [ ] No HTML tags remaining
- [ ] Sections flow logically
- [ ] Cross-references to other sections use `\ref{sec:...}`

## Example Conversion

**HTML:**
```html
<p>The framework begins with 26-dimensional spacetime with signature (24,2).
An Sp(2,R) gauge symmetry projects to 13D with signature (12,1).</p>
```

**LaTeX:**
```latex
The framework begins with 26-dimensional spacetime with signature $(24,2)$.
An $\text{Sp}(2,\mathbb{R})$ gauge symmetry projects to 13D with signature $(12,1)$.
```

## Where to Find Content in HTML

Use grep to search for specific sections:
```bash
Grep pattern="Introduction" path=h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html
```

Or read specific line ranges:
```bash
Read file_path=h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html offset=START limit=COUNT
```

## Tips

1. **Read first, then convert:** Understand the HTML structure before editing
2. **Use equation-index.txt:** Find which equations belong in your sections
3. **Preserve numerical precision:** Copy exact values from HTML
4. **Add labels consistently:** `\label{eq:dimensional_reduction}` for equations
5. **Note missing citations:** Comment which references you need
6. **Test incrementally:** Make small edits and verify structure

## Questions?

Check these reference files:
- `AGENT-1-TEMPLATE-REPORT.md` - Full template documentation
- `TEMPLATE-STRUCTURE-SUMMARY.txt` - Quick structure reference
- `accessibility-guidelines.md` - PRD formatting guidelines

## When You're Done

1. Verify all your sections compile (or would compile with content)
2. Create a summary report: `AGENT-2-COMPLETION-REPORT.md`
3. List any citations needed for Agent 7
4. Note any figures/tables needed
5. Pass to Agent 3 for Fermion Sector

## Time Estimate

- Reading HTML sections: 20 minutes
- Converting to LaTeX: 45 minutes
- Formatting equations: 30 minutes
- Review and polish: 15 minutes
- **Total: ~2 hours**

Good luck, Agent 2! 🚀
