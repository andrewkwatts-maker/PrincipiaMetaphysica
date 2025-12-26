# Formula Display Styling Update Guide

## Objective
Update dynamic formula displays to match the clean, academic styling from `principia-metaphysica-paper.html`.

## Key Differences Between Old Paper and Current Dynamic Pages

### Old Paper Style (principia-metaphysica-paper.html)
- **Equation Display**: Clean, centered with minimal background
- **Equation Numbers**: Right-aligned in parentheses like `(2.1)`
- **Derivation Boxes**: Light gradient background with simple border
- **Terms**: Simple, academic presentation
- **Font**: Consistent Times New Roman for math

```css
/* Old Paper Styling */
.equation-block {
    margin: 1.5rem 0;
    padding: 1rem 0;
    overflow-x: auto;
}

.equation-number {
    float: right;
    color: #666;
    font-size: 0.9rem;
}

.derivation-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 1.5rem 0;
}
```

### Current Dynamic Style (formulas.html)
- **Equation Display**: Heavy card background with borders
- **Equation Numbers**: Missing!
- **Derivation Boxes**: Dark theme, modern styling
- **Terms**: Card-based grid layout
- **Font**: Mixed fonts

## Files to Update

### 1. `formulas.html`
**Location**: Lines 123-137

**Current:**
```css
.formula-equation {
    background: var(--bg-secondary);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    text-align: center;
    font-size: 1.3rem;
    border: 1px solid var(--border-primary);
    overflow-x: auto;
}
```

**Replace with:**
```css
/* Formula Equation Display - Match old paper styling */
.formula-equation {
    margin: 1.5rem 0;
    padding: 1rem 0;
    overflow-x: auto;
    text-align: center;
    position: relative;
    clear: both;
}

.formula-equation .MathJax,
.formula-equation mjx-container {
    font-size: 1.2em !important;
}

/* Equation number (right-aligned, in parentheses) */
.equation-number {
    float: right;
    color: #666;
    font-size: 0.9rem;
    font-family: 'Crimson Text', serif;
    margin-left: 1rem;
}
```

### 2. `js/pm-formula-component.js`
**Location**: Lines 252-259

**Add after `.formula-display` style:**
```css
.equation-number {
    float: right;
    color: #666;
    font-size: 0.9rem;
    font-family: 'Crimson Text', Georgia, serif;
    margin-left: 1rem;
    line-height: 2;
}
```

### 3. `js/pm-formula-loader.js`
**Location**: Lines 359-362 (render function)

**Update rendering to include equation numbers:**

Before:
```javascript
// Main formula display
html += `<div class="formula-display" style="font-size: 1.2rem; padding: 0.5rem 0; text-align: center;">
    ${formula.html || formula.latex || formula.plainText || ''}
</div>`;
```

After:
```javascript
// Main formula display with equation number
const equationNumber = formula.section ? `(${formula.section})` : '';
html += `<div class="formula-display" style="font-size: 1.2rem; padding: 0.5rem 0; text-align: center; position: relative; clear: both;">
    ${equationNumber ? `<span class="equation-number">${equationNumber}</span>` : ''}
    ${formula.html || formula.latex || formula.plainText || ''}
</div>`;
```

### 4. Update `renderFormulaCard()` in `formulas.html`
**Location**: Lines 1007-1010

**Update equation rendering:**

Before:
```javascript
<!-- Equation -->
<div class="formula-equation">
    ${formula.latex ? `$$${formula.latex}$$` : (formula.html || escapeHtml(formula.plainText || 'No equation available'))}
</div>
```

After:
```javascript
<!-- Equation -->
<div class="formula-equation">
    ${formula.section ? `<span class="equation-number">(${escapeHtml(formula.section)})</span>` : ''}
    ${formula.latex ? `$$${formula.latex}$$` : (formula.html || escapeHtml(formula.plainText || 'No equation available'))}
</div>
```

### 5. Include the new CSS file

Add to `formulas.html` after existing stylesheet links:
```html
<link rel="stylesheet" href="css/formula-display-fix.css">
```

Add to any other dynamic pages using formulas:
```html
<link rel="stylesheet" href="css/formula-display-fix.css">
```

## Testing Checklist

1. **Equation Numbers**:
   - [ ] Equation numbers appear on the right side
   - [ ] Numbers are in parentheses like `(2.1)`
   - [ ] Float right properly without overlapping equation

2. **Formula Display**:
   - [ ] Equations are centered
   - [ ] No heavy background boxes (clean like old paper)
   - [ ] MathJax renders at consistent size
   - [ ] Mobile: equations scroll horizontally if needed

3. **Derivation Boxes**:
   - [ ] Light gray gradient background
   - [ ] Simple border styling
   - [ ] Numbered steps with proper indentation

4. **Terms/Parameters**:
   - [ ] Clean, readable layout
   - [ ] Terms have left border accent
   - [ ] Symbol and description clearly separated

5. **Status Badges**:
   - [ ] EXACT MATCH: green
   - [ ] VALIDATED: purple
   - [ ] GEOMETRIC: yellow
   - [ ] PREDICTION: pink

6. **Responsive Design**:
   - [ ] Mobile: formulas are readable
   - [ ] Tablet: proper grid layouts
   - [ ] Desktop: optimal spacing

## Implementation Order

1. Create `css/formula-display-fix.css` ✓ (Already done)
2. Update `formulas.html` inline styles
3. Update `js/pm-formula-loader.js` rendering
4. Update `js/pm-formula-component.js` styles
5. Test on multiple pages
6. Verify MathJax rendering
7. Check mobile responsiveness

## Rollback Plan

If issues occur, the old styling can be restored by:
1. Removing `<link rel="stylesheet" href="css/formula-display-fix.css">`
2. Reverting changes to inline styles
3. Removing equation number spans from rendering code

## Notes

- The new CSS file uses `!important` to override existing styles
- Equation numbers are extracted from `formula.section` property
- All changes are backward compatible
- MathJax re-typesetting is preserved
- Print styles included for academic papers
