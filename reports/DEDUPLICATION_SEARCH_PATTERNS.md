# Deduplication Implementation: Search Patterns & Replacements

**Purpose:** Exact patterns for find-and-replace operations
**Format:** Ready to paste into VS Code Find & Replace
**Tool:** VS Code (Ctrl+H) or sed/grep

---

## REMOVAL PATTERNS

### PATTERN 1: Appendix A.1 Central Charge Equation

**Search For (Exact):**
```html
            <h3 class="subsection-title">A.1 Central Charge Calculation</h3>
            <div class="equation-block">
                $$c_{\text{matter}} = D, \quad c_{\text{ghost}} = -26, \quad c_{\text{total}} = D - 26 = 0$$
            </div>
```

**Replace With:**
```html
            <h3 class="subsection-title">A.1 Central Charge Calculation</h3>
            <p>
                The critical dimension $D = 26$ is derived in <strong>Section 2.3</strong> (Eq. 2.2).
                This appendix provides computational verification of the Virasoro anomaly cancellation condition.
            </p>
```

**Verification:**
- [ ] Next line should be: `<h3 class="subsection-title">A.2 Simulation Code</h3>`

---

### PATTERN 2: Appendix D.1 Ghost Coefficient Equation

**Search For (Exact):**
```html
            <h3 class="subsection-title">D.1 Ghost Coefficient</h3>
            <div class="equation-block">
                $$\gamma = \frac{|c_{\text{ghost}}|}{2 c_{\text{matter}}} = \frac{26}{2 \times 26} = \frac{26}{52} = 0.5$$
            </div>
```

**Replace With:**
```html
            <h3 class="subsection-title">D.1 Dark Energy Derivation Context</h3>
            <p>
                The ghost coefficient $\gamma = 0.5$ and effective dimension $d_{\text{eff}} = 12.576$ are derived in
                <strong>Section 7.1</strong> (Equations 7.1-7.2 context). This appendix provides the computational
                implementation and numerical verification.
            </p>
```

**Verification:**
- [ ] Next section should be: `<h3 class="subsection-title">D.2 ...`

---

### PATTERN 3: Appendix D.2 Effective Dimension Equation

**Search For (Exact):**
```html
            <h3 class="subsection-title">D.2 Effective Dimension</h3>
            <div class="equation-block">
                $$d_{\text{eff}} = 12 + \gamma(\alpha_4 + \alpha_5) = 12 + 0.5(0.576152 + 0.576152) = 12.576$$
            </div>
```

**Replace With:**
```html
            <h3 class="subsection-title">D.2 Computational Implementation</h3>
            <p>
                From <strong>Section 7.1</strong>, the effective dimension is $d_{\text{eff}} = 12.576$ and
                equation of state is $w_0 = -0.8528$. Below we provide numerical computation code.
            </p>
```

**Verification:**
- [ ] Should be followed by code block or next section

---

### PATTERN 4: Appendix D.3 Equation of State (DELETE ENTIRE SECTION)

**Search For (Exact):**
```html
            <h3 class="subsection-title">D.3 Equation of State</h3>
            <div class="equation-block">
                $$w_0 = -\frac{d_{\text{eff}} - 1}{d_{\text{eff}} + 1} = -\frac{11.576}{13.576} = -0.8528$$
            </div>

```

**Replace With:** (Empty - DELETE THESE LINES)

**Then Find & Replace D.4 → D.3:**
- **Search:** `<h3 class="subsection-title">D.4 Simulation Code</h3>`
- **Replace:** `<h3 class="subsection-title">D.3 Simulation Code</h3>`

**Verification:**
- [ ] Appendix D should now go: D.1 → D.2 → D.3 (code) only

---

### PATTERN 5: Appendix C.1 G₂ Holonomy Explanation

**Search For (Exact):**
```html
            <h3 class="subsection-title">C.1 G<sub>2</sub> Holonomy Argument</h3>
            <div class="equation-block">
                $$G_2 \supset SU(3), \quad \mathbf{7} = \mathbf{3} + \bar{\mathbf{3}} + \mathbf{1} \quad \Rightarrow \quad \alpha_4 = \alpha_5$$
            </div>
            <p>
                The SU(3) maximal compact subgroup enforces symmetric treatment of the three (3,1) shadow branes, requiring equal coupling parameters.
            </p>
```

**Replace With:**
```html
            <h3 class="subsection-title">C.1 Atmospheric Mixing Angle Simulation</h3>
            <p>
                The atmospheric mixing angle $\theta_{23} = 45°$ is derived in <strong>Section 6.1</strong> (Eq. 6.1)
                from G₂ holonomy symmetry. This appendix provides numerical simulation and verification.
            </p>
```

**Verification:**
- [ ] Next section should be: `<h3 class="subsection-title">C.2 Simulation Code</h3>`

---

## ADDITION PATTERNS

### PATTERN ADD-1: Section 2.3 Forward Reference

**Search For:**
```html
            <div class="equation-block">
                $$c_{\text{total}} = c_{\text{matter}} + c_{\text{ghost}} = D + (-26) = 0 \quad \Rightarrow \quad D = 26$$
                <span class="equation-number">(2.2)</span>
            </div>
```

**Add After This Block:**
```html
            <p style="font-size: 0.9rem; color: #666;">
                <em>See <a href="#appendix-a">Appendix A</a> for computational verification code and signature (24,2) compatibility discussion.</em>
            </p>
```

**Location Context:** Section 2.3 header, near line 748

---

### PATTERN ADD-2: Section 6.1 Forward Reference

**Search For (in Section 6.1, near θ₂₃ equation):**
```html
                $$\theta_{23} = 45°$$
```

**Add After Full Equation Block:**
```html
            <p style="font-size: 0.9rem; color: #666;">
                <em>See <a href="#appendix-c">Appendix C</a> for simulation code and numerical verification of maximal mixing.</em>
            </p>
```

**Note:** Look for equation numbered (6.1)

---

### PATTERN ADD-3: Section 7.1 Forward Reference

**Search For (in Section 7.1, after w₀ equation):**
```html
                $$w_0 = -\frac{d_{\text{eff}} - 1}{d_{\text{eff}} + 1} = -\frac{11.576}{13.576} = -0.8528$$
                <span class="equation-number">(7.2)</span>
```

**Add After This Block:**
```html
            <p style="font-size: 0.9rem; color: #666;">
                <em>See <a href="#appendix-d">Appendix D</a> for computational implementation and DESI constraints comparison.</em>
            </p>
```

**Location Context:** Section 7.1, Equation of State subsection

---

## ENHANCEMENT PATTERNS

### PATTERN ENH-1: Appendix B.1 Add Context Before Equation

**Search For:**
```html
            <h3 class="subsection-title">B.1 Index Formula</h3>
            <div class="equation-block">
```

**Replace With:**
```html
            <h3 class="subsection-title">B.1 Index Formula with Z₂ Factor</h3>
            <p>
                The generation count formula from <strong>Section 4.2</strong> (Eq. 4.2) is summarized here with
                explicit Z₂ factor from Sp(2,ℝ) gauge fixing:
            </p>
            <div class="equation-block">
```

**Then Add After Equation Block:**
```html
            <p style="font-size: 0.9rem; color: #666;">
                <em>Compare to main text Eq. 4.2: $n_{\text{gen}} = |\chi_{\text{eff}}|/48 = 144/48 = 3$</em>
            </p>
```

---

### PATTERN ENH-2: Appendix B.2 Add Section Reference

**Search For:**
```html
            <h3 class="subsection-title">B.2 Z<sub>2</sub> Factor Origin</h3>
            <p>
                The Z<sub>2</sub> parity arises from Sp(2,&#x211D;) gauge fixing in two-time physics.
```

**Replace With:**
```html
            <h3 class="subsection-title">B.2 Z<sub>2</sub> Factor Origin</h3>
            <p>
                This unique factor in the PM framework arises from Sp(2,ℝ) gauge fixing in two-time physics
                (derived in <strong>Section 4.2</strong>). It identifies spinors across the two time dimensions:
```

---

### PATTERN ENH-3: Appendix A.4 Add Section Reference

**Search For:**
```html
            <h3 class="subsection-title">A.4 PM Framework Applications</h3>
            <p>
                The $D = 26$ constraint and (24,2) signature enable the PM framework's dimensional reduction:
```

**Replace With:**
```html
            <h3 class="subsection-title">A.4 PM Framework Applications</h3>
            <p>
                The $D = 26$ constraint from <strong>Section 2.3</strong> and (24,2) signature are fundamental to
                the PM framework's dimensional reduction cascade:
```

---

## VS CODE QUICK REFERENCE

Open `principia-metaphysica-paper.html` and use **Find & Replace** (Ctrl+H):

### Shortcut Workflow:

```
1. Open file: principia-metaphysica-paper.html
2. Press: Ctrl+H (Open Find & Replace)
3. Copy/paste pattern from section above
4. Click Replace All (or Replace for caution)
5. Verify replacement in editor
6. Move to next pattern
```

### Using Regex (Advanced):

If you want to use regex patterns:

- **Match Virasoro equation:** `c_{\text{matter}} = D, \quad c_{\text{ghost}} = -26`
- **Match d_eff equation:** `d_{\text{eff}} = 12 \+ \\gamma`
- **Match w₀ equation:** `w_0 = -\\frac\{d_{\text{eff}} - 1`

Enable **Regex Mode** (Alt+R) in VS Code Find & Replace.

---

## VERIFICATION PATTERNS

After each change, search for these patterns to verify no duplicates remain:

### Critical Duplicates to Check (Should Find ONLY in Main Text):

**Should appear ONLY in Section 2.3:**
```
c_{\text{matter}} = D, \quad c_{\text{ghost}} = -26, \quad c_{\text{total}} = D + (-26) = 0
```

**Should appear ONLY in Section 4.2:**
```
n_{\text{gen}} = \frac{|\chi_{\text{eff}}|}{48} = \frac{144}{48} = 3
```

**Should appear ONLY in Section 6.1:**
```
\theta_{23} = 45°
```

**Should appear ONLY in Section 7.1:**
```
d_{\text{eff}} = 12 + \gamma(\alpha_4 + \alpha_5)
w_0 = -\frac{d_{\text{eff}} - 1}{d_{\text{eff}} + 1} = -\frac{11.576}{13.576} = -0.8528
```

### Cross-Reference Check:

Search for these anchor IDs to verify they exist:

- [ ] `id="appendix-a"` (in Appendix A header)
- [ ] `id="appendix-b"` (in Appendix B header)
- [ ] `id="appendix-c"` (in Appendix C header)
- [ ] `id="appendix-d"` (in Appendix D header)

Search for these link references:

- [ ] `href="#appendix-a"` (should appear in Section 2.3)
- [ ] `href="#appendix-b"` (should appear in Section 4.2)
- [ ] `href="#appendix-c"` (should appear in Section 6.1)
- [ ] `href="#appendix-d"` (should appear in Section 7.1)

---

## UNIX/SED COMMANDS (Alternative)

If using command line instead of VS Code:

```bash
# Backup original
cp principia-metaphysica-paper.html principia-metaphysica-paper.html.bak

# Remove Appendix A.1 equation (use -i'' for macOS, -i for Linux)
sed -i.bak '/A.1 Central Charge Calculation/,/<\/div>/c\
            <h3 class="subsection-title">A.1 Central Charge Calculation<\/h3>\
            <p>\
                The critical dimension $D = 26$ is derived in <strong>Section 2.3<\/strong> (Eq. 2.2).\
                This appendix provides computational verification of the Virasoro anomaly cancellation condition.\
            <\/p>' principia-metaphysica-paper.html
```

**Note:** Sed approach is error-prone. Use VS Code instead.

---

## ORDER OF EXECUTION

**Recommended sequence to minimize errors:**

1. [ ] **REMOVALS FIRST** (5 patterns) - Reduce file size
   - Pattern 1: A.1 equation
   - Pattern 2: D.1 equation
   - Pattern 3: D.2 equation
   - Pattern 4: D.3 section + renumber D.4→D.3
   - Pattern 5: C.1 explanation

2. [ ] **ADDITIONS NEXT** (3 patterns) - Add cross-refs
   - Add-1: Section 2.3
   - Add-2: Section 6.1
   - Add-3: Section 7.1

3. [ ] **ENHANCEMENTS LAST** (3 patterns) - Polish
   - Enh-1: Appendix B.1
   - Enh-2: Appendix B.2
   - Enh-3: Appendix A.4

4. [ ] **VERIFY ALL** - Test completeness

---

## COMMON MISTAKES TO AVOID

1. **Don't change equation numbers** - Keep (2.2), (4.2), (6.1), (7.1), (7.2) exactly as-is
2. **Don't modify code blocks** - Only remove redundant equations, not code
3. **Don't forget D.4→D.3 renumbering** - After removing D.3, next section must be renumbered
4. **Don't break hyperlinks** - Ensure `href="#appendix-x"` matches `id="appendix-x"`
5. **Don't mix indentation** - Keep 12 spaces for `<h3>` tags, 16 for `<div>`
6. **Don't remove math delimiters** - Keep `$$..$$` and `\text{}` formatting
7. **Don't change styling classes** - Keep `class="subsection-title"` and `style="font-size: 0.9rem"`

---

## TESTING AFTER COMPLETION

```bash
# Option 1: HTML5 Validator
html5-validator principia-metaphysica-paper.html

# Option 2: Quick syntax check (bash)
grep "equation-block" principia-metaphysica-paper.html | wc -l

# Option 3: Find orphaned anchors
grep "href=\"#appendix" principia-metaphysica-paper.html
grep "id=\"appendix" principia-metaphysica-paper.html
```

---

**Ready to implement. Copy patterns directly into VS Code Find & Replace (Ctrl+H).**

Generated: 2025-12-18
