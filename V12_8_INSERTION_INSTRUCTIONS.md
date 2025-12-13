# V12.8 Content Insertion Instructions

Due to an auto-save/linter process modifying the HTML file, I've prepared the content in separate files for manual insertion.

## Files Created

1. **`v12_8_appendix_e_content.html`** - Content for Appendix E (Cosmology)
2. **`v12_8_appendix_g_content.html`** - Content for Appendix G (Predictions)

## Insertion Points

### Appendix E (Cosmology)
**Location:** After line ~32014 in `principia-metaphysica-paper.html`

**Insert after this text:**
```html
            Value is <strong>geometry-derived</strong> from explicit TCS G₂ construction (arXiv:1809.09083), not phenomenologically fit.
          </p>
        </div>
```

**Insert before this text:**
```html
      </div>


</div>
      </div>


      <!-- VERSION 6.1: BPS Stability and Brane Configuration -->
```

**What to insert:** Copy the entire contents of `v12_8_appendix_e_content.html`

This adds:
- V12.8 Ghost Central Charge Derivation (d_eff formula with 0.5 coefficient explanation)
- V12.8 Effective Torsion from G-Flux (T_omega_eff = -b3/C formula)

### Appendix G (Predictions)
**Location:** After the proton decay branching ratio discussion (around line ~6336)

**Insert after this text:**
```html
            prediction distinct from total lifetime, testable by Hyper-K channel-resolved measurements.
    </p>
   </div>
```

**Insert before the next major section:** (e.g., "7.2 Geometric Derivation of Shared Dimension Parameters")

**What to insert:** Copy the entire contents of `v12_8_appendix_g_content.html`

This adds:
- V12.8 Proton Decay Branching Ratio Prediction (BR formula)
- V12.8 GW Dispersion Prediction (η formula, LISA testable)
- V12.8 Monte Carlo Error Propagation Summary (58×58 correlation matrix)

## Content Summary

### Appendix E Additions:

1. **Ghost Central Charge Derivation**
   - Formula: `ghost_coefficient = |c_ghost|/(2*c_matter) = 26/52 = 0.5`
   - LaTeX: `$$d_{eff} = 12 + 0.5 \times (\alpha_4 + \alpha_5) = 12.576$$`
   - LaTeX: `$$w_0 = -(d_{eff}-1)/(d_{eff}+1) = -0.8528$$`
   - Python code from `derive_d_eff_v12_8.py`

2. **Effective Torsion from G-Flux**
   - Formula: `T_omega_eff = -b3/C = -24/27.2 = -0.882`
   - LaTeX: `$$T_{\omega,eff} = -\frac{b_3}{C} = -\frac{24}{27.2} = -0.882$$`
   - Python code from `torsion_effective_v12_8.py`
   - Explains: TCS G₂ are Ricci-flat (no geometric torsion), but G-flux creates effective torsion

### Appendix G Additions:

1. **Proton Decay Branching Ratio**
   - Formula: `BR(p→e+π0) = (orientation_sum/b3)^2 = (12/24)^2 = 0.25`
   - LaTeX: `$$BR(p \to e^+ \pi^0) = \left(\frac{12}{24}\right)^2 = 0.25$$`
   - Python code from `proton_decay_br_v12_8.py`
   - Status: PREDICTION (Hyper-K 2032-2038)

2. **GW Dispersion**
   - Formula: `η = exp(|T_omega|)/b3 = exp(0.884)/24 = 0.101`
   - LaTeX: `$$\eta = \frac{\exp(|T_\omega|)}{b_3} = 0.101$$`
   - Python code from `gw_dispersion_v12_8.py`
   - Status: PREDICTION (LISA 2037+)

3. **MC Error Propagation**
   - 58×58 correlation matrix
   - Mean error ~5%, Max ~16%
   - Topological parameters EXACT
   - Python code from `mc_error_propagation_v12_8.py`

## Manual Steps

1. Open `principia-metaphysica-paper.html` in your text editor
2. Navigate to line ~32014 (end of existing d_eff derivation section in Appendix E)
3. Copy contents of `v12_8_appendix_e_content.html` and insert
4. Navigate to line ~6336 (end of proton decay section in Appendix G)
5. Copy contents of `v12_8_appendix_g_content.html` and insert
6. Save the file

## Verification

After insertion, verify:
- [ ] MathJax formulas render correctly ($$...$$)
- [ ] Python code blocks have proper syntax highlighting (<pre><code class="language-python">)
- [ ] All file references are correct (simulations/*_v12_8.py)
- [ ] Styling matches surrounding content (theorem-box, note-box, etc.)

## Notes

- All LaTeX formulas use MathJax `$$...$$` for display math
- All code blocks use `<pre><code class="language-python">...</code></pre>` format
- Content follows existing HTML styling conventions
- References to simulation files: `simulations/*_v12_8.py`
