# V12.8 Simulation Code Insertion Instructions

This document explains where to insert the v12.8 simulation code blocks into `principia-metaphysica-paper.html`.

## Appendix B (Geometric Framework)

**Location:** Around line 14357-14359
**Insert content from:** `appendix_b_insert.html`

### Exact insertion point:
After the text:
```html
This natural emergence of the GUT scale provides a consistency check on the framework.
</p>
```

And before:
```html
</section>
<section class="subsection" id="pneuma-manifold">
```

### What to insert:
The content in `appendix_b_insert.html` contains three simulation boxes:

1. **Virasoro Anomaly Cancellation** (purple box)
   - LaTeX formula: $$c_{total} = c_{matter} + c_{ghost} = D + (-26) = 0 \implies D = 26$$
   - Python code from `virasoro_anomaly_v12_8.py`

2. **Dimensional Decomposition** (green box)
   - LaTeX formula: $$26D = 4D \times T^{15} \times G_2(7D)$$
   - Python code from `dim_decomp_v12_8.py`

3. **Generation Count with Z₂ Factor** (yellow box)
   - LaTeX formula: $$n_{gen} = \frac{|\chi_{eff}|}{48} = \frac{|\chi_{eff}|}{24 \times 2} = \frac{144}{48} = 3$$
   - Python code from `zero_modes_gen_v12_8.py`

---

## Appendix D (Fermion Sector)

**Location:** Around line 31705-31710
**Insert content from:** `appendix_d_insert.html`

### Exact insertion point:
After the text:
```html
<p style="margin-top: 1rem;">
    <a href="../references.html#neutrinos" style="color: var(--accent-secondary);">
        See full references page →
    </a>
</p>
```

And before:
```html
</section>
<!-- Navigation -->
```

### What to insert:
The content in `appendix_d_insert.html` contains one simulation box:

1. **θ₂₃ Derivation from G₂ Holonomy** (purple/pink box)
   - LaTeX formula: $$\theta_{23} = \frac{\pi}{4} = 45° \quad (\text{from } \alpha_4 = \alpha_5 \text{ via } G_2 \text{ holonomy SU(3) symmetry})$$
   - Python code from `derive_theta23_g2_v12_8.py`
   - Includes geometric derivation steps
   - Shows derive_theta23_g2() and derive_alpha_parameters() functions

---

## Notes

- The HTML file appears to be dynamically updated (possibly by a linter or auto-save), so manual insertion may be required
- All LaTeX formulas use MathJax syntax with $$ for display math
- Code blocks are styled with dark theme matching the rest of the paper
- Interactive formula divs use the same styling as existing formulas in the paper
- Each simulation box has:
  - A colored header with version number (V12.8)
  - LaTeX formula in a centered interactive-formula div
  - Python code block with syntax highlighting
  - References to source files and academic papers

## Files Generated

1. `appendix_b_insert.html` - Content for Appendix B (Geometric Framework)
2. `appendix_d_insert.html` - Content for Appendix D (Fermion Sector)
3. `INSERTION_INSTRUCTIONS.md` - This file

## File Structure

```
H:\Github\PrincipiaMetaphysica\
├── principia-metaphysica-paper.html  (target file)
├── appendix_b_insert.html            (content to insert in Appendix B)
├── appendix_d_insert.html            (content to insert in Appendix D)
└── INSERTION_INSTRUCTIONS.md         (this file)
```

## Testing After Insertion

After inserting the content, verify:
1. MathJax formulas render correctly (check that $$ delimiters work)
2. Code blocks maintain proper syntax highlighting
3. Interactive formula hovers work
4. Color schemes match the rest of the paper
5. Line numbers mentioned in instructions are approximate due to file modifications
