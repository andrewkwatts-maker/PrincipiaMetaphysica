# References.html Debug Guide

## Quick Diagnostic Steps

### 1. Check if JSON file exists
```bash
ls -la AUTO_GENERATED/json/references.json
```

Expected: File should be ~42KB with 95 references

### 2. Validate JSON structure
```bash
python -c "import json; data = json.load(open('AUTO_GENERATED/json/references.json')); print(f'Valid: {len(data)} refs')"
```

Expected output: `Valid: 95 refs`

### 3. Open test page
Open in browser: `test-references-standalone.html`

This page:
- ✓ No authentication required
- ✓ Shows detailed diagnostic logs
- ✓ Tests all fetch paths
- ✓ Displays first 10 references
- ✓ Highlights any errors

### 4. Check browser console
1. Open `references.html` in browser
2. Press F12 to open DevTools
3. Go to Console tab
4. Look for `[References]` prefixed messages

## Expected Console Output (Success)

```
[References] Document still loading, waiting for DOMContentLoaded
[References] DOMContentLoaded event fired
[References] Document ready state: interactive
[References] Starting to load references...
[References] Current URL: http://localhost:3000/references.html
[References] Attempting to fetch from: AUTO_GENERATED/json/references.json
[References] Response status for AUTO_GENERATED/json/references.json: 200 OK
[References] Fetched 42750 bytes from AUTO_GENERATED/json/references.json
[References] First 100 chars: {
  "vafa1996": {
    "id": "vafa1996",
    "title": "Evidence for F-Theory",
    "authors": "Vafa...
[References] Successfully parsed JSON from AUTO_GENERATED/json/references.json
[References] Successfully loaded from: AUTO_GENERATED/json/references.json
[References] Data type: object
[References] Data keys: ["vafa1996", "acharya2001_chiral", "corti2015", "acharya1998", "acharya2003_freund"]
[References] Converted to array, length: 95
[References] Sample reference: {id: "vafa1996", title: "Evidence for F-Theory", ...}
[References] Updating stats...
[References] Stats updated: {totalRefs: 95, withArxiv: 72, withDOI: 45, avgYear: 2008}
[References] Displaying references, count: 95
[References] Grouping references by decade...
[References] Grouping by decade, input count: 95
[References] Grouped by decade (before sort): ["1990", "2000", "2010", "2020"]
[References] Final sorted decades: ["2020", "2010", "2000", "1990"]
[References] Grouped into decades: ["2020", "2010", "2000", "1990"]
[References] Processing decade 2020s with 25 references
[References] Processing decade 2010s with 30 references
[References] Processing decade 2000s with 28 references
[References] Processing decade 1990s with 12 references
[References] Generated HTML length: 45230
[References] References rendered to DOM
[References] Successfully rendered references
[References] Found filter buttons: 4
[References] Attaching listener to filter button 0: all
[References] Attaching listener to filter button 1: year
[References] Attaching listener to filter button 2: author
[References] Attaching listener to filter button 3: cited
[References] All event listeners attached
```

## Common Error Patterns

### Error: 404 Not Found
```
[References] Response status for AUTO_GENERATED/json/references.json: 404 Not Found
```

**Solution**: File doesn't exist or wrong path
- Check file exists: `ls AUTO_GENERATED/json/references.json`
- Try absolute path in browser
- Ensure you're in correct directory

### Error: CORS
```
Access to fetch at 'file:///...' from origin 'null' has been blocked by CORS policy
```

**Solution**: Must use web server, not file:// protocol
- Use `python -m http.server 8000`
- Or use VS Code Live Server
- Or configure local web server

### Error: JSON Parse
```
[References] Error: Unexpected token < in JSON at position 0
```

**Solution**: Received HTML instead of JSON
- Server might be returning 404 page (HTML)
- Check Network tab in DevTools
- Verify path is correct

### Error: Empty Array
```
[References] Converted to array, length: 0
```

**Solution**: JSON file is empty or has wrong structure
- Validate JSON: `python -c "import json; print(json.load(open('AUTO_GENERATED/json/references.json')))"`
- Check file isn't corrupted
- Re-generate references.json

### Error: Container Not Found
```
[References] Container element not found!
```

**Solution**: DOM not ready or auth hiding content
- Check if `<div id="references-container">` exists
- Check if auth.js is hiding `#main-content`
- Try test-references-standalone.html instead

## Testing Different Scenarios

### Test 1: Search Functionality
```javascript
// In browser console:
searchReferences('vafa');
// Should show filtered results and log:
// [References] Search called with query: vafa
// [References] Search results: 5 out of 95
```

### Test 2: Sort by Year
```javascript
sortReferences('year');
// Should show all refs sorted by year and log:
// [References] Sort called with: year
// [References] Sorted by year
// [References] Displaying as single list
```

### Test 3: Sort by Author
```javascript
sortReferences('author');
// Should show all refs sorted alphabetically by author
```

### Test 4: Sort by Citations
```javascript
sortReferences('cited');
// Should show most-cited references first
```

### Test 5: Back to Grouped View
```javascript
sortReferences('all');
// Should restore decade grouping
```

## Manual Inspection

### Check Stats Display
The stats box should show:
```
95 total references • 72 with arXiv • 45 with DOI • Average year: 2008
```

### Check Decade Sections
You should see sections like:
- 2020s (with recent papers)
- 2010s (bulk of references)
- 2000s (foundational work)
- 1990s (seminal papers)

### Check Reference Cards
Each reference should display:
- ✓ Title (bold, primary color)
- ✓ Authors (gray text)
- ✓ Year and ID (italic, muted)
- ✓ Description (if available)
- ✓ arXiv link (if available)
- ✓ DOI link (if available)
- ✓ Formula tags (if cited by formulas)

## Performance Metrics

### Expected Load Times
- JSON fetch: < 100ms
- JSON parse: < 50ms
- HTML generation: < 200ms
- DOM render: < 100ms
- **Total**: < 500ms

### Expected Sizes
- JSON file: ~42KB
- Generated HTML: ~45KB
- Total references: 95
- Decades: 4 (1990s, 2000s, 2010s, 2020s)

## Debugging Commands

### Check current state
```javascript
console.log('References loaded:', allReferences.length);
console.log('Current filter:', currentFilter);
console.log('First reference:', allReferences[0]);
console.log('Last reference:', allReferences[allReferences.length - 1]);
```

### Force reload
```javascript
allReferences = [];
loadReferences();
```

### Test specific reference
```javascript
const testRef = allReferences.find(r => r.id === 'vafa1996');
console.log(createReferenceHTML(testRef));
```

### Check DOM elements
```javascript
console.log('Container:', document.getElementById('references-container'));
console.log('Search input:', document.getElementById('search-input'));
console.log('Stats:', document.getElementById('ref-stats'));
console.log('Filter buttons:', document.querySelectorAll('.filter-btn').length);
```

## Network Tab Inspection

In DevTools > Network:
1. Look for `references.json` request
2. Should show:
   - **Status**: 200 OK
   - **Type**: xhr or fetch
   - **Size**: ~42KB
   - **Time**: < 100ms

3. Click on the request to see:
   - **Headers**: Content-Type: application/json
   - **Preview**: JSON object with references
   - **Response**: Raw JSON text

## If All Else Fails

1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard reload (Ctrl+Shift+R)
3. Try different browser
4. Check file permissions
5. Verify web server is running
6. Look for JavaScript errors in console
7. Check if other pages load correctly
8. Try test-references-standalone.html
9. Regenerate references.json
10. Contact developer with console logs

## Success Criteria

✓ No errors in console
✓ Stats show "95 total references"
✓ 4 decade sections visible
✓ References display with titles, authors, years
✓ Search filters results
✓ Sort buttons change view
✓ Links are clickable
✓ Spinner disappears after load
✓ No "loading" message stuck on screen
