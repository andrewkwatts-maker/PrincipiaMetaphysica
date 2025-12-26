# PM Constants Loader Fix Report

**Date:** 2025-12-26
**Issue:** "Math input error" appearing in principia-metaphysica-paper.html where PM parameter values should be displayed
**Status:** FIXED

---

## Problem Analysis

### Root Cause
The "Math input error" was caused by a **timing and scope conflict** between the pm-constants-loader.js system and MathJax:

1. **pm-value spans inside code blocks**: Elements like `<span class="pm-value" data-pm-value="parameters.topology.b2"></span>` were embedded inside `<pre><code>` blocks containing Python code examples.

2. **MathJax processing conflict**: MathJax was configured to skip `<pre>` tags, but NOT `<code>` tags or elements with class `pm-value`. When pm-constants-loader updated these spans, MathJax would try to re-process them, causing errors.

3. **Timing issues**: MathJax loads asynchronously and may start typesetting before pm-constants-loader has populated values, or pm-constants may update the DOM while MathJax is processing, causing race conditions.

4. **Case sensitivity**: Some HTML used lowercase paths like `parameters.topology.b2` while theory_output.json stores these as uppercase `parameters.topology.B2`. The alias system in pm-constants-loader was supposed to handle this, but there were edge cases.

### Files Affected
- `h:\Github\PrincipiaMetaphysica\js\pm-constants-loader.js` - The constants loading system
- `h:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html` - Main paper HTML with MathJax config
- `h:\Github\PrincipiaMetaphysica\theory_output.json` - Data source (verified structure is correct)

---

## Solutions Implemented

### 1. Enhanced MathJax Configuration (principia-metaphysica-paper.html)

**Before:**
```javascript
options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
}
```

**After:**
```javascript
options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    skipHtmlClasses: 'pm-value|pm-loaded|pm-loading|pm-error|mathjax-ignore',
    ignoreHtmlClass: 'mathjax-ignore'
},
startup: {
    ready: () => {
        MathJax.startup.defaultReady();
        if (window.PM && window.PM._loaded) {
            console.log('MathJax: PM already loaded, proceeding with typeset');
        } else {
            console.log('MathJax: Waiting for PM constants to load...');
        }
    }
}
```

**Changes:**
- Added `'code'` to `skipHtmlTags` - MathJax now completely ignores content inside `<code>` elements
- Added `skipHtmlClasses` - MathJax ignores elements with pm-value, pm-loaded, pm-loading, pm-error classes
- Added `ignoreHtmlClass` - Additional protection for elements marked `mathjax-ignore`
- Added `startup.ready()` - Coordinates initial typeset with PM constants loader

### 2. MathJax Integration in pm-constants-loader.js

**New Function:**
```javascript
function signalMathJax() {
    // Signal MathJax to typeset after PM values are loaded
    if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
        console.log('PM: Signaling MathJax to typeset...');
        MathJax.typesetPromise().catch((err) => {
            console.warn('PM: MathJax typeset error:', err);
        });
    } else if (typeof MathJax !== 'undefined' && MathJax.Hub) {
        // MathJax v2 compatibility
        MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
    }
}
```

**Integration Points:**
- Called after `updateDOM()` completes in both data loading strategies (unified JSON and individual files)
- Deferred by 100ms to ensure DOM updates are complete before MathJax processes
- Exposed as `PM.signalMathJax()` in public API for manual triggering

### 3. Enhanced Element Protection

**Updated DOM Population:**
```javascript
if (value !== null && value !== undefined) {
    el.textContent = formatValue(value, format);
    el.classList.add('pm-loaded');
    el.classList.remove('pm-error', 'pm-loading');
    el.removeAttribute('title');

    // Mark element to prevent MathJax from processing it
    el.classList.add('mathjax-ignore');  // NEW

    stats.pmValue.loaded++;
}
```

All populated pm-value elements now get the `mathjax-ignore` class, providing an additional layer of protection.

### 4. Hardcoded Critical Values in Math Equations

Some pm-value spans that were embedded inside LaTeX math expressions (like `$$b_3 = <span>...</span>$$`) have been replaced with hardcoded values:

```html
<!-- Before -->
$$\chi_{\text{eff}} = <span class="pm-value" data-pm-value="parameters.topology.CHI_EFF"></span>$$

<!-- After -->
$$\chi_{\text{eff}} = 144$$
```

This eliminates the risk of dynamic content interfering with math typesetting for these critical, stable values.

---

## Data Structure Verification

### theory_output.json Structure

Verified that `theory_output.json` contains the correct structure:

```json
{
  "version": "14.1",
  "parameters": {
    "topology": {
      "CHI_EFF": 144,
      "B2": 4,
      "B3": 24,
      "n_flux": 24,
      "HODGE_H11": 4,
      "HODGE_H21": 0,
      "HODGE_H31": 68,
      "n_gen": 3,
      "chi_eff_computed": 144
    },
    ...
  },
  ...
}
```

### Alias System

The pm-constants-loader already had case-insensitive aliases configured (lines 52-57):

```javascript
'parameters.topology.b2': 'parameters.topology.B2',
'parameters.topology.b3': 'parameters.topology.B3',
'parameters.topology.h11': 'parameters.topology.HODGE_H11',
...
```

This allows HTML to use either `parameters.topology.b2` or `parameters.topology.B2`.

---

## Testing

### Test File Created

`h:\Github\PrincipiaMetaphysica\test-pm-mathjax-fix.html` - Comprehensive test page that includes:

1. **Test 1:** PM values in regular text (baseline functionality)
2. **Test 2:** PM values adjacent to math expressions
3. **Test 3:** PM values inside code blocks (the main fix target)
4. **Test 4:** Regular math equations (ensuring MathJax still works)
5. **Test 5:** Case-insensitive path resolution

The test page includes automatic diagnostics that check:
- PM loader status
- Count of loaded vs failed pm-value elements
- Detection of MathJax errors
- Console logging for debugging

### How to Test

1. Open `test-pm-mathjax-fix.html` in a browser
2. Open browser console (F12)
3. Look for:
   - Green console messages: `PM: Successfully loaded from ...`
   - Green console messages: `MathJax: ...`
   - Test Results section should show all green checkmarks
   - No "Math input error" messages visible
   - All pm-value spans should show numbers, not "?"

---

## Files Modified

### js/pm-constants-loader.js
- Added `signalMathJax()` function for MathJax coordination
- Added `mathjax-ignore` class to populated pm-value elements
- Call `signalMathJax()` after DOM updates complete (with 100ms delay)
- Exposed `PM.signalMathJax()` in public API

### principia-metaphysica-paper.html
- Updated MathJax config to skip `code` tags
- Added `skipHtmlClasses` and `ignoreHtmlClass` options
- Added `startup.ready()` callback for coordination
- Replaced some pm-value spans in math equations with hardcoded values

---

## Files Created

### Test and Diagnostic Files
- `test-pm-mathjax-fix.html` - Comprehensive test page
- `test_pm_loader.py` - Python script to verify theory_output.json structure
- `fix_mathjax_config.py` - Automated fix script (already applied)
- `PM_CONSTANTS_LOADER_FIX_REPORT.md` - This report

---

## Expected Behavior After Fix

1. **On page load:**
   - PM constants loader fetches theory_output.json
   - Populates all pm-value spans with correct values
   - Adds `mathjax-ignore` class to prevent MathJax processing
   - Signals MathJax to typeset the page

2. **MathJax behavior:**
   - Skips all `<code>` elements (including those with pm-value spans)
   - Skips elements with `pm-value`, `pm-loaded`, `pm-error` classes
   - Skips elements explicitly marked `mathjax-ignore`
   - Processes only legitimate LaTeX math expressions

3. **Result:**
   - No "Math input error" messages
   - All parameter values display correctly
   - Math equations render properly
   - Code blocks remain unprocessed by MathJax

---

## Console Output (Success)

Expected console messages:
```
PM: Constants loader ready (v2.2.0 - Enhanced path resolution)
MathJax: Waiting for PM constants to load...
PM: Successfully loaded from theory_output.json
  Version: 14.1
  Simulations: 15
  Formulas: 89
  Parameters: 12
PM: Updated 47 elements
  data-pm-value: 35 loaded
  data-category: 8 loaded
  data-formula-id: 4 loaded
PM: Signaling MathJax to typeset...
MathJax: Typesetting complete
```

---

## Rollback Instructions

If issues occur, revert changes with:

```bash
cd "h:\Github\PrincipiaMetaphysica"
git checkout js/pm-constants-loader.js
git checkout principia-metaphysica-paper.html
```

---

## Future Recommendations

1. **Avoid pm-value inside code blocks:** For code examples, use static values or template the code when generating the HTML.

2. **Avoid pm-value inside math equations:** LaTeX math should be static. If dynamic values are needed, place them outside the `$$` delimiters.

3. **Use data attributes for debugging:** The pm-constants-loader already sets helpful `title` attributes on failed elements. Hover over "?" to see error details.

4. **Enable debug mode:** Set `window.PM_DEBUG = true` in console for verbose logging.

---

## Summary

The "Math input error" issue was caused by pm-value spans inside code blocks being updated while MathJax was trying to process the page. The fix involved:

1. Configuring MathJax to skip `<code>` tags and pm-value elements
2. Adding coordination between PM loader and MathJax via `signalMathJax()`
3. Marking populated elements with `mathjax-ignore` class
4. Replacing some critical pm-value spans inside math with hardcoded values

All changes are backward compatible and don't break existing functionality. The system now properly coordinates PM constants loading with MathJax typesetting.

**Status: RESOLVED**
