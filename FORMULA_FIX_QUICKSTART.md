# Formula Display Fix - Quick Start Guide

## What This Fixes
Makes dynamic formula pages match the old paper's clean, academic styling.

## Before & After

**Before:**
- ❌ No equation numbers
- ❌ Heavy background boxes
- ❌ Modern card styling
- ❌ Inconsistent with paper

**After:**
- ✅ Equation numbers (like "(2.1)")
- ✅ Clean backgrounds
- ✅ Academic styling
- ✅ Matches old paper perfectly

## 5-Minute Setup

### Step 1: View the Problem
Open `examples/formula-styling-comparison.html` in your browser to see:
- Current styling (heavy boxes, no equation numbers)
- Fixed styling (clean, academic, with equation numbers)

### Step 2: Apply the Fix
Choose ONE method:

#### Option A: Automated (Easiest)
```bash
bash apply-formula-display-fixes.sh
# Then follow the printed instructions
```

#### Option B: Manual (More control)
Copy-paste code from `FORMULA_DISPLAY_FIXES.txt`:
1. Update `formulas.html` (3 changes)
2. Update `js/pm-formula-loader.js` (1 change)
3. Update `js/pm-formula-component.js` (1 change)

### Step 3: Test
1. Open `formulas.html`
2. Check for equation numbers on the right
3. Verify clean backgrounds (no heavy boxes)
4. Test on mobile device

### Step 4: Deploy
If everything looks good, commit and push!

## Files You'll Use

### Core Fix
- `css/formula-display-fix.css` - Main stylesheet ✓ Already created

### Documentation
- `FORMULA_DISPLAY_FIXES.txt` - Exact code to copy-paste
- `FORMULA_STYLING_FIX_SUMMARY.md` - Complete overview
- `examples/formula-styling-comparison.html` - Visual demo

### Tools
- `apply-formula-display-fixes.sh` - Automated patch script

## Changes Required

### 1. formulas.html (3 changes)
```html
<!-- Add this line after styles.css -->
<link rel="stylesheet" href="css/formula-display-fix.css">
```
```css
/* Update .formula-equation CSS (lines 123-137) */
/* See FORMULA_DISPLAY_FIXES.txt for exact code */
```
```javascript
// Update renderFormulaCard() to add equation numbers (line 1007)
// See FORMULA_DISPLAY_FIXES.txt for exact code
```

### 2. js/pm-formula-loader.js (1 change)
```javascript
// Update render() function to add equation numbers (line 360)
// See FORMULA_DISPLAY_FIXES.txt for exact code
```

### 3. js/pm-formula-component.js (1 change)
```css
/* Add .equation-number style after .formula-display (line 259) */
/* See FORMULA_DISPLAY_FIXES.txt for exact code */
```

## Testing Checklist
- [ ] Equation numbers appear (right side, in parentheses)
- [ ] Clean backgrounds (no heavy boxes)
- [ ] Derivation boxes have light gradients
- [ ] MathJax renders correctly
- [ ] Mobile view works
- [ ] Desktop view works

## Need Help?

1. **Visual Reference**: Open `examples/formula-styling-comparison.html`
2. **Code Snippets**: See `FORMULA_DISPLAY_FIXES.txt`
3. **Full Details**: See `FORMULA_STYLING_FIX_SUMMARY.md`
4. **Rollback**: Run `cp backups/formula-display-fix-*/formulas.html .`

## One-Line Summary
**New CSS file + 5 small code updates = Clean academic formula display with equation numbers**

---

Ready? Start with `examples/formula-styling-comparison.html` to see what you're aiming for!
