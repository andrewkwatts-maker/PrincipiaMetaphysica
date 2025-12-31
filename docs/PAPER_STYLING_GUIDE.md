# Principia Metaphysica Paper Styling & Formatting Guide

## Purpose
This guide ensures consistent visual presentation across all sections and appendices of the paper. Each agent is responsible for their assigned section and must fix ALL encoding issues and formatting problems.

---

## 1. CHARACTER ENCODING RULES

### 1.1 FORBIDDEN Mojibake Patterns (MUST FIX)
These corrupted character sequences must be replaced with correct Unicode:

| Corrupted Pattern | Correct Character | Description |
|-------------------|-------------------|-------------|
| `â†'` | `→` | Right arrow |
| `â‡'` | `⇒` | Double right arrow (implies) |
| `â€"` | `—` | Em dash |
| `â€™` | `'` | Right single quote |
| `â€œ` | `"` | Left double quote |
| `â€` | `"` | Right double quote |
| `âˆ'` | `−` | Minus sign |
| `âˆš` | `√` | Square root |
| `âˆž` | `∞` | Infinity |
| `âˆ‚` | `∂` | Partial derivative |
| `âˆ«` | `∫` | Integral |
| `âˆ'` | `∑` | Summation |
| `âˆ` | `∏` | Product |
| `Ã—` | `×` | Multiplication |
| `Ã·` | `÷` | Division |
| `Â±` | `±` | Plus-minus |
| `Â²` | `²` | Superscript 2 |
| `Â³` | `³` | Superscript 3 |
| `Î±` | `α` | Alpha |
| `Î²` | `β` | Beta |
| `Î³` | `γ` | Gamma |
| `Î´` | `δ` | Delta |
| `Îµ` | `ε` | Epsilon |
| `Î¶` | `ζ` | Zeta |
| `Î·` | `η` | Eta |
| `Î¸` | `θ` | Theta |
| `Î¹` | `ι` | Iota |
| `Îº` | `κ` | Kappa |
| `Î»` | `λ` | Lambda |
| `Î¼` | `μ` | Mu |
| `Î½` | `ν` | Nu |
| `Î¾` | `ξ` | Xi |
| `Ï€` | `π` | Pi |
| `Ï` | `ρ` | Rho |
| `Ïƒ` | `σ` | Sigma |
| `Ï„` | `τ` | Tau |
| `Ï†` | `φ` | Phi |
| `Ï‡` | `χ` | Chi |
| `Ïˆ` | `ψ` | Psi |
| `Ï‰` | `ω` | Omega |
| `Î"` | `Γ` | Gamma (uppercase) |
| `Î"` | `Δ` | Delta (uppercase) |
| `Î£` | `Σ` | Sigma (uppercase) |
| `Î¨` | `Ψ` | Psi (uppercase) |
| `Î©` | `Ω` | Omega (uppercase) |

### 1.2 Subscript Characters
| Corrupted | Correct | Description |
|-----------|---------|-------------|
| `â‚€` | `₀` | Subscript 0 |
| `â‚` | `₁` | Subscript 1 |
| `â‚‚` | `₂` | Subscript 2 |
| `â‚ƒ` | `₃` | Subscript 3 |
| `â‚„` | `₄` | Subscript 4 |
| `â‚…` | `₅` | Subscript 5 |
| `â‚†` | `₆` | Subscript 6 |
| `â‚‡` | `₇` | Subscript 7 |
| `â‚ˆ` | `₈` | Subscript 8 |
| `â‚‰` | `₉` | Subscript 9 |
| `â‚™` | `ₙ` | Subscript n |
| `â‚˜` | `ₘ` | Subscript m |
| `â‚š` | `ₚ` | Subscript p |
| `â‚'` | `ₑ` | Subscript e |
| `â‚›` | `ₛ` | Subscript s |
| `â‚•` | `ₕ` | Subscript h |

### 1.3 Superscript Characters
| Corrupted | Correct | Description |
|-----------|---------|-------------|
| `â°` | `⁰` | Superscript 0 |
| `Â¹` | `¹` | Superscript 1 |
| `Â²` | `²` | Superscript 2 |
| `Â³` | `³` | Superscript 3 |
| `â´` | `⁴` | Superscript 4 |
| `âµ` | `⁵` | Superscript 5 |
| `â¶` | `⁶` | Superscript 6 |
| `â·` | `⁷` | Superscript 7 |
| `â¸` | `⁸` | Superscript 8 |
| `â¹` | `⁹` | Superscript 9 |
| `â»Â¹` | `⁻¹` | Superscript -1 |
| `â»Â²` | `⁻²` | Superscript -2 |
| `âº` | `⁺` | Superscript + |
| `â»` | `⁻` | Superscript - |
| `â¿` | `ⁿ` | Superscript n |

### 1.4 Mathematical Operators
| Corrupted | Correct | Description |
|-----------|---------|-------------|
| `âŠ—` | `⊗` | Tensor product |
| `âŠ•` | `⊕` | Direct sum |
| `âŠ‚` | `⊂` | Subset |
| `âŠƒ` | `⊃` | Superset |
| `âˆˆ` | `∈` | Element of |
| `âˆ‰` | `∉` | Not element of |
| `â‰ˆ` | `≈` | Approximately |
| `â‰¡` | `≡` | Identical to |
| `â‰¤` | `≤` | Less than or equal |
| `â‰¥` | `≥` | Greater than or equal |
| `â‰ ` | `≠` | Not equal |
| `âˆ¼` | `∼` | Similar to |
| `âˆ` | `∝` | Proportional to |
| `âŒŠ` | `⌊` | Left floor |
| `âŒ‹` | `⌋` | Right floor |
| `âŒˆ` | `⌈` | Left ceiling |
| `âŒ‰` | `⌉` | Right ceiling |
| `âŸ¨` | `⟨` | Left angle bracket |
| `âŸ©` | `⟩` | Right angle bracket |

---

## 2. MATHJAX FORMATTING RULES

### 2.1 Inline Math
Use `\( ... \)` for inline math, NOT `$ ... $`:
```html
The energy is \( E = mc^2 \).
```

### 2.2 Display Math
Use `\[ ... \]` for display equations, NOT `$$ ... $$`:
```html
\[
S = \int d^{26}x \sqrt{|G|} \left[ M_*^{11} R_{13} + \bar{\Psi}_P (i\Gamma^M \nabla_M - m)\Psi_P \right]
\]
```

### 2.3 Common LaTeX Commands
| Symbol | LaTeX |
|--------|-------|
| Greek | `\alpha, \beta, \gamma, \delta, \theta, \phi, \psi, \omega` |
| Uppercase Greek | `\Gamma, \Delta, \Sigma, \Psi, \Omega` |
| Subscripts | `x_1, x_{12}, M_{GUT}` |
| Superscripts | `x^2, x^{-1}, M^{11}` |
| Fractions | `\frac{a}{b}` |
| Square root | `\sqrt{x}, \sqrt[n]{x}` |
| Integrals | `\int, \int_0^\infty, \oint` |
| Sums | `\sum, \sum_{i=1}^n` |
| Products | `\prod, \prod_{i=1}^n` |
| Partial | `\partial` |
| Nabla | `\nabla` |
| Arrows | `\rightarrow, \Rightarrow, \leftrightarrow` |
| Operators | `\times, \cdot, \otimes, \oplus` |
| Relations | `\approx, \equiv, \leq, \geq, \neq, \sim` |
| Set | `\in, \notin, \subset, \supset` |
| Brackets | `\langle x \rangle, \lfloor x \rfloor, \lceil x \rceil` |
| Text in math | `\text{some text}` |
| Bold math | `\mathbf{v}` |
| Calligraphic | `\mathcal{L}, \mathcal{M}` |

### 2.4 Common Physics Notation
```latex
% Spacetime
\mathcal{M}^{26}, G_{MN}, R_{13}

% Spinors
\Psi_P, \bar{\Psi}, \Gamma^M

% Field strengths
F_{\mu\nu}, G_{\mu\nu\rho}

% Covariant derivative
\nabla_\mu, D_\mu

% Metric determinant
\sqrt{|G|}, \sqrt{-g}

% Generation number
n_{\text{gen}} = \frac{\chi_{\text{eff}}}{48}

% GUT scale
M_{\text{GUT}} = 2.1 \times 10^{16} \text{ GeV}

% Moduli
\text{Re}(T), \text{Im}(T)
```

---

## 3. HTML FORMATTING RULES

### 3.1 Section Headers
```html
<h2>Section Title</h2>
<h3>Subsection Title</h3>
<h4>Sub-subsection Title</h4>
```

### 3.2 Equations with Numbers
```html
<div class="equation" id="eq-name">
  \[ E = mc^2 \]
  <span class="eq-number">(1)</span>
</div>
```

### 3.3 Definition Boxes
```html
<div style="background: rgba(139, 127, 255, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
  <strong>Definition:</strong> Content here
</div>
```

### 3.4 Important Results
```html
<div style="background: rgba(80, 200, 120, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #50c878;">
  <strong>Key Result:</strong> Content here
</div>
```

### 3.5 Warnings/Caveats
```html
<div style="background: rgba(255, 126, 182, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ff7eb6;">
  <strong>Note:</strong> Content here
</div>
```

---

## 4. PM VALUE REFERENCES

### 4.1 Using PM Constants
Always use span elements with data attributes for dynamic values:
```html
<span class="pm-value" data-pm-value="dimensions.D_bulk"></span>D spacetime
<span class="pm-value" data-pm-value="topology.n_gen"></span> generations
<span class="pm-value" data-pm-value="pmns_matrix.theta_23" data-format="fixed:1"></span>°
```

### 4.2 Common PM Paths
| Value | Path |
|-------|------|
| 26D | `dimensions.D_bulk` |
| 4D | `dimensions.D_observable` |
| n_gen = 3 | `topology.n_gen` |
| χ_eff = 144 | `topology.chi_eff` |
| b₃ = 24 | `topology.b3` |
| θ₂₃ = 45° | `pmns_matrix.theta_23` |
| w₀ = -0.9583 (-23/24) | `dark_energy.w0_PM` |
| M_GUT | `proton_decay.M_GUT` |
| α_GUT⁻¹ | `proton_decay.alpha_GUT_inv` |
| τ_p | `proton_decay.tau_p_median` |

---

## 5. VALIDATION CHECKLIST

Each agent must verify:

### 5.1 Encoding
- [ ] No mojibake patterns (â€, Â, Ã, etc.)
- [ ] All Greek letters render correctly
- [ ] All subscripts render correctly
- [ ] All superscripts render correctly
- [ ] All mathematical operators render correctly
- [ ] All arrows render correctly

### 5.2 MathJax
- [ ] All inline math uses `\( ... \)`
- [ ] All display math uses `\[ ... \]`
- [ ] No raw LaTeX outside delimiters
- [ ] All equations render properly

### 5.3 Structure
- [ ] Headers are properly nested (h2 > h3 > h4)
- [ ] IDs are unique and meaningful
- [ ] Links work correctly
- [ ] Navigation links to previous/next section

### 5.4 Visual
- [ ] No visible HTML artifacts
- [ ] Consistent spacing
- [ ] Tables properly formatted
- [ ] Lists properly formatted
- [ ] Code blocks properly formatted

---

## 6. AGENT ASSIGNMENTS

### Main Paper Sections (Lines 1-9367)
- **Agent-Main**: Abstract, Title, TOC, Introduction overview

### Appendices
- **Agent-A**: Lines 9368-10570 (Introduction)
- **Agent-B**: Lines 10571-18917 (Geometric Framework)
- **Agent-C**: Lines 18918-22540 (Gauge Unification)
- **Agent-D**: Lines 22541-31759 (Fermion Sector)
- **Agent-E**: Lines 31760-35781 (Cosmology)
- **Agent-F**: Lines 35782-39283 (Thermal Time)
- **Agent-G**: Lines 39284-42859 (Predictions)
- **Agent-H**: Lines 42860-46039 (Conclusion)
- **Agent-I**: Lines 46040-47931 (Formulas)
- **Agent-J**: Lines 47932-50958 (Theory Analysis)
- **Agent-K**: Lines 50959-51207 (Einstein-Hilbert Term)
- **Agent-L**: Lines 51208-54308 (Pneuma Lagrangian)
- **Agent-M**: Lines 54309-54708 (XY Gauge Bosons)
- **Agent-N**: Lines 54709-55311 (CMB Bubble Collisions)
- **Agent-O**: Lines 55312-55679 (Division Algebras)
- **Agent-P**: Lines 55680-55911 (Section Index)
- **Agent-Q**: Lines 55912-END (Pneuma Lagrangian New)

---

## 7. REPORTING

Each agent must output:
1. Number of encoding fixes made
2. Number of MathJax fixes made
3. Number of structural fixes made
4. Any remaining issues that couldn't be auto-fixed
5. Verification that all checklist items pass

---

## 8. COMMON PATTERNS TO FIX

### 8.1 Corrupted Arrow Sequences
```
WRONG: â†' or â‡' or â†"
RIGHT: → or ⇒ or ↔
```

### 8.2 Corrupted Subscript Sequences
```
WRONG: Mâ‚'â‚'â‚" or nâ‚'â‚'â‚™
RIGHT: M_{GUT} or n_{gen} (use MathJax)
```

### 8.3 Corrupted Greek Letters
```
WRONG: Î±, Î², Î³, Ï€
RIGHT: α, β, γ, π (or use MathJax: \alpha, \beta, \gamma, \pi)
```

### 8.4 Mixed Encoding
Sometimes characters are partially corrupted:
```
WRONG: θ₂₃ = 45Â° (mixed correct θ with corrupted °)
RIGHT: θ₂₃ = 45° or \theta_{23} = 45°
```

---

## 9. PRIORITY ORDER

1. **CRITICAL**: Fix all mojibake (corrupted characters)
2. **HIGH**: Fix all MathJax rendering issues
3. **MEDIUM**: Fix structural issues (headers, links)
4. **LOW**: Polish formatting (spacing, alignment)

---

*Last Updated: December 2025*
*Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.*
