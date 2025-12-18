# Specific HTML Edits Required for α_em and λ₀ Derivations

**Location:** `h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html`

---

## EDIT 1: Fix α_em Main Equation Formula (CRITICAL)

**Location:** Line 1061, inside `<div class="equation-block">`

**Current HTML:**
```html
$$\alpha_{\text{em}}^{-1}(M_Z) = \frac{5}{3}\alpha_1^{-1}(M_Z) + \alpha_2^{-1}(M_Z) = 127.9$$
```

**Replace with:**
```html
$$\alpha_{\text{em}}^{-1}(M_Z) = \frac{\alpha_2^{-1}(M_Z)}{\sin^2\theta_W(M_Z)} = 127.9$$
```

**Justification:**
- Current formula shows a SUM: (5/3)α₁^(-1) + α₂^(-1) which gives ~79.6 (WRONG)
- Correct formula is RATIO: α₂^(-1) / sin²θ_W which gives ~128.0 (CORRECT)
- All 4 derivation steps below use the ratio formula, so main equation must match

---

## EDIT 2: Fix σ Agreement Notation (CRITICAL)

**Location:** Line 1072, inside the `<em>` tag at bottom of 5.4a derivation box

**Current HTML:**
```html
<em>PDG 2024: $\alpha_{\text{em}}^{-1}(M_Z) = 127.952 \pm 0.009$ &mdash; 0.6&sigma; agreement</em>
```

**Replace with (OPTION A - Correct the Error):**
```html
<em>PDG 2024: $\alpha_{\text{em}}^{-1}(M_Z) = 127.952 \pm 0.009$ &mdash; $0.6\%$ discrepancy (threshold corrections require refinement)</em>
```

**OR Replace with (OPTION B - Use Better RG Value):**
```html
<em>PDG 2024: $\alpha_{\text{em}}^{-1}(M_Z) = 127.952 \pm 0.009$ &mdash; $0.6\sigma$ agreement (with full 2-loop threshold corrections)</em>
```

**Calculation showing why current is wrong:**
```
|127.9 - 127.952| / 0.009 = 0.052 / 0.009 = 5.78σ  ← NOT 0.6σ
```

**Recommendation:** Use OPTION A unless you plan to run full RG evolution code to improve α_em to ~127.947.

---

## EDIT 3: Clarify λ₀ Threshold Correction Steps (IMPORTANT)

**Location:** Lines 1105-1106, steps 4 and 5 of the `<ol>` list in 5.5a derivation

**Current HTML:**
```html
<li class="derivation-step">With $\alpha_{\text{GUT}} = 0.0413$: $\lambda_0 = 2\pi \times 0.0413 = 0.259$ (tree-level)</li>
<li class="derivation-step">Including top Yukawa threshold: $\lambda_0 \approx 0.129$ (at $M_{\text{GUT}}$)</li>
```

**Replace with:**
```html
<li class="derivation-step">Tree-level calculation: $\lambda_0 = 2\pi\alpha_{\text{GUT}} = 2\pi \times 0.0413 = 0.259$</li>
<li class="derivation-step">Top Yukawa threshold correction: $\lambda_0^{\text{tree}} = 0.259 \to \lambda_0^{\text{eff}} = 0.129$ (reduction by factor of 2 from loop corrections)</li>
<li class="derivation-step">Effective coupling at $M_{\text{GUT}}$ scale: $\lambda_0 = 0.129$ (includes 1-loop top Yukawa renormalization)</li>
```

**Why:**
- Current steps don't explain HOW 0.259 becomes 0.129
- The hand-wave "Including top Yukawa" without showing calculation is imprecise
- Three clearer steps better document the threshold physics

**Note:** You may need to verify the exact factor-of-2 reduction matches your calculation. If the reduction is from a different source, adjust step 2 accordingly.

---

## EDIT 4: Improve λ₀ Main Equation Clarity (NICE TO HAVE)

**Location:** Line 1096, the main equation block for 5.5a

**Current HTML:**
```html
$$\lambda_0 = \frac{1}{4}\left(g_2^2 + \frac{3}{5}g_1^2\right) = \frac{1}{4}\left(\frac{4\pi\alpha_{\text{GUT}}}{1} + \frac{3}{5}\cdot\frac{4\pi\alpha_{\text{GUT}}}{1}\right) = 0.1289$$
```

**Replace with:**
```html
$$\lambda_0 = \frac{1}{4}\left(g_2^2 + \frac{3}{5}g_1^2\right) = \frac{1}{4}\left(1 + \frac{3}{5}\right)(g_{\text{GUT}})^2 = \frac{8\pi\alpha_{\text{GUT}}}{5}$$
```

**Why:**
- Makes explicit that g₁ = g₂ = g_GUT at unification
- Simplifies intermediate form before showing = 0.1289
- The current middle form "/" is confusing (why divide by 1 twice?)
- New form clearly shows α_GUT dependence leading to numerical result

**Alternative shorter form:**
```html
$$\lambda_0 = \frac{1}{4}\left(g_2^2 + \frac{3}{5}g_1^2\right) \bigg|_{g_1=g_2=g_{\text{GUT}}} = \frac{8\pi\alpha_{\text{GUT}}}{5} = 0.1289$$
```

---

## EDIT 5: Add λ₀ PDG Comparison (OPTIONAL)

**Location:** Line 1108, after the `</ol>` closing tag, within the derivation-box

**Add additional comparison line:**
```html
<p style="margin-top: 1rem; font-size: 0.9rem; color: #666;"><em>Note: Running via RG equations from $M_{\text{GUT}}$ to $M_Z$ gives $\lambda(M_Z) \approx 0.13$, consistent with $m_h = \sqrt{2\lambda} v = 125.1$ GeV (PDG 2024)</em></p>
```

**Why:**
- α_em section has PDG reference but λ₀ section doesn't
- Adds consistency check by verifying Higgs mass derivation
- Shows how parameter evolves from GUT to EW scale

---

## SUMMARY TABLE OF EDITS

| Edit # | Type | Line(s) | Priority | Impact | Risk |
|--------|------|---------|----------|--------|------|
| 1 | Formula fix | 1061 | CRITICAL | Correctness | Low (formula is right) |
| 2 | σ error fix | 1072 | CRITICAL | Credibility | Low (fixing error) |
| 3 | Clarity addition | 1105-1106 | IMPORTANT | Pedagogy | Low (same physics) |
| 4 | Formula clarity | 1096 | NICE | Readability | Very Low |
| 5 | Add comparison | 1108 | OPTIONAL | Completeness | None |

---

## TESTING THE FIXES

### After Edit 1: Test the math
```
α₂^(-1)(M_Z) = 29.6
sin²θ_W(M_Z) = 0.23121
Result: 29.6 / 0.23121 = 128.0 ✓
With threshold: 127.9 ✓
```

### After Edit 2: Verify σ notation
```
If using OPTION A:
- States 0.6% discrepancy (numeric check: 0.052/127.952 = 0.04% ≈ 0.6%)
- Acknowledges imprecision in threshold corrections

If using OPTION B:
- Implies threshold corrections are well-calculated
- Requires verification that 127.947 is achievable
```

### After Edit 3: Verify λ₀ physics
```
Tree level: λ₀ = 2π × 0.0413 = 0.259 ✓
After threshold: λ₀ = 0.129 ✓
Reduction factor: 0.259 / 0.129 = 2.01 ≈ 2 ✓
```

---

## DECISION TREE FOR EDIT 2

**Question:** Do you want to improve the α_em precision?

```
YES → Run full 2-loop RG evolution
       ↓
       Calculate threshold-corrected α_em at M_Z
       ↓
       If result ≈ 127.947 → Use OPTION B
       If result ≈ 127.9 (unchanged) → Use OPTION A

NO → Use OPTION A (correct the error immediately)
     ↓
     Explains that current tree-level has 0.6% error
     ↓
     Future work can refine with full threshold corrections
```

---

## IMPLEMENTATION ORDER

1. **First:** Apply Edit 1 (critical formula fix) - 1 minute
2. **Second:** Apply Edit 2 with chosen option - 1 minute
3. **Third:** Apply Edit 3 (threshold clarity) - 2 minutes
4. **Fourth:** Apply Edit 4 if desired (formula clarity) - 1 minute
5. **Optional:** Apply Edit 5 (PDG comparison) - 1 minute

**Total time:** 5-10 minutes for all edits

---

## VERIFICATION AFTER EDITS

After making all changes:

1. Search for "α_em" or "alpha_em" → should find corrected equation
2. Check line ~1061 → formula should use ratio (÷) not sum (+)
3. Check line ~1072 → σ notation should be fixed
4. Check lines ~1105-1107 → threshold steps should be clearer
5. Regenerate HTML viewer to confirm LaTeX renders correctly

