# How Parameter Values Work in Principia Metaphysica

## Quick Answer

**The HTML webpages do NOT run SimulateTheory.py or load its CSV output.**

Instead, there are **THREE separate systems** for parameter values:

```
1. config.py (Python)        → For SimulateTheory.py calculations
2. theory-constants.js (JS)  → For HTML webpage displays
3. Hard-coded in HTML        → Static values in the pages

These are INDEPENDENT and need to be kept in sync manually.
```

---

## The Three Value Systems

### 1. Python Config (config.py)
**Used by:** SimulateTheory.py
**Purpose:** Parameter generation, calculations, CSV export
**Language:** Python
**Example:**
```python
class PhenomenologyParameters:
    M_PLANCK = 1.2195e19  # GeV
    W0_NUMERATOR = -11
    W0_DENOMINATOR = 13
```

### 2. JavaScript Constants (js/theory-constants.js)
**Used by:** HTML pages (index.html, sections/*.html)
**Purpose:** Display values dynamically in webpages
**Language:** JavaScript
**Example:**
```javascript
const TheoryConstants = {
    fundamentalScales: {
        mPlanck: 1.2195e19,  // GeV
    },
    darkEnergy: {
        w0: -11/13,  // ≈ -0.846
    }
}
```

### 3. Hard-coded HTML
**Used by:** Static text in HTML files
**Purpose:** Explanatory text, formulas, descriptions
**Language:** HTML
**Example:**
```html
<p>Planck mass M<sub>Pl</sub> = 1.22×10<sup>19</sup> GeV</p>
<p>Dark energy w₀ = -11/13 ≈ -0.846</p>
```

---

## How They're Currently Used

### SimulateTheory.py Workflow:
```
config.py → SimulateTheory.py → parameters.csv
   ↑              ↓                    ↓
Values      Calculations           Output file
stored      performed              (NOT used by HTML)
```

**The CSV is NOT loaded by webpages.** It's for:
- Your analysis
- Spreadsheet review
- Data validation
- External tools

### HTML Webpage Workflow:
```
theory-constants.js → index.html + sections/*.html
        ↑                      ↓
   JS values            Display on webpage
   defined              (browser renders)
```

**When you open index.html in a browser:**
1. HTML loads
2. JavaScript file (theory-constants.js) loads
3. JS values are used to dynamically populate some displays
4. Most values are hard-coded in HTML itself

**SimulateTheory.py is NEVER run** by the webpage.

---

## Current Situation (Problem)

**The three systems are OUT OF SYNC:**

| Parameter | config.py | theory-constants.js | HTML Files |
|-----------|-----------|---------------------|------------|
| M_Pl | 1.2195e19 ✓ | 1.2195e19 ✓ | Various (~1e19) ⚠️ |
| w₀ | -11/13 ✓ | -11/13 ✓ | -0.846 ✓ |
| m_KK | 5.0 TeV ✓ | Missing ❌ | Mentioned but no value ⚠️ |
| α_T | 2.7 ✓ | Missing ❌ | Missing ❌ |
| M_GUT | 1.8e16 ✓ | Missing ❌ | 2e16 (approx) ⚠️ |

**You have to update values in THREE places manually.**

---

## Solutions (Pick One)

### Option 1: Keep Current System (Manual Sync)
**Pro:** Simple, no automation needed
**Con:** Must manually update 3 places every time

**When you change a value:**
1. Update `config.py` (Python)
2. Update `js/theory-constants.js` (JavaScript)
3. Update HTML files (search & replace)
4. Run `SimulateTheory.py` to regenerate CSV

### Option 2: Auto-Generate JS from Python
**Pro:** Single source of truth (config.py)
**Con:** Requires automation script

**Create a script:**
```python
# generate_js_constants.py
from config import *

js_output = f"""
const TheoryConstants = {{
    mPlanck: {PP.M_PLANCK},
    w0: {PP.w0_value()},
    mKK: {V61.M_KK_CENTRAL},
    // ... etc
}};
"""
with open('js/theory-constants.js', 'w') as f:
    f.write(js_output)
```

**Workflow:**
1. Edit `config.py`
2. Run `python generate_js_constants.py` (auto-creates JS file)
3. Run `python SimulateTheory.py` (generates CSV)
4. HTML automatically uses updated JS values

### Option 3: Make HTML Load CSV (Dynamic)
**Pro:** HTML shows exact calculated results
**Con:** Requires fetch() API, web server

**Modify HTML:**
```javascript
// In index.html
fetch('parameters.csv')
    .then(response => response.text())
    .then(csv => {
        // Parse CSV and inject values into HTML
        document.getElementById('m_planck').textContent = parsedValue;
    });
```

**Limitations:**
- Requires running a local web server (can't just open file://)
- More complex to maintain
- Users need to generate CSV first

### Option 4: Hybrid (Recommended)
**Pro:** Best of all worlds
**Con:** Most complex setup

**Architecture:**
```
config.py (SOURCE OF TRUTH)
    ↓
    ├─→ SimulateTheory.py → parameters.csv (for analysis)
    └─→ generate_js_constants.py → theory-constants.js → HTML
```

**Benefits:**
- `config.py` is the ONLY place to edit values
- Automation generates both CSV and JS
- HTML always shows correct values
- No web server needed

**Setup:**
```bash
# After editing config.py, run:
python generate_js_constants.py  # Updates JS
python SimulateTheory.py          # Updates CSV
# HTML automatically uses new JS values
```

---

## Recommendation

**I recommend Option 4 (Hybrid)** because:

1. **Single Source of Truth:** config.py is the master
2. **Automation:** One command updates everything
3. **Flexibility:** Can still hand-edit JS if needed
4. **No Web Server:** HTML works with file:// protocol
5. **Consistency:** JS and CSV always match config.py

**Want me to create `generate_js_constants.py` for you?**

---

## Current vs Recommended Architecture

### Current (Manual, 3 Locations):
```
config.py         (you edit here)
                   ↓ manual copy
theory-constants.js   (you edit here too)
                   ↓ loads
HTML files        (you edit here as well!)
                   ↓ browser displays
Webpage

SimulateTheory.py  (separate, generates CSV not used by HTML)
```

### Recommended (Automated, 1 Location):
```
config.py (ONLY place to edit)
    ↓
    ├─→ generate_js_constants.py
    │        ↓
    │   theory-constants.js
    │        ↓ loads
    │   HTML files
    │        ↓ browser displays
    │   Webpage
    │
    └─→ SimulateTheory.py
             ↓
        parameters.csv (for analysis)
```

**One edit → everything updates automatically**

---

## Summary

**To answer your questions:**

1. **Does the theory reference SimulateTheory.py output?**
   - NO, HTML files do NOT load the CSV

2. **Does the webpage run SimulateTheory.py when launched?**
   - NO, it's pure HTML/CSS/JS (static site)
   - Values come from `js/theory-constants.js` and hard-coded HTML

3. **How do values get into the HTML?**
   - Currently: Manual editing in 3 places (config.py, theory-constants.js, HTML)
   - Should be: Auto-generate JS from config.py

**Next step:** Want me to create the `generate_js_constants.py` automation script to make config.py the single source of truth for everything?
