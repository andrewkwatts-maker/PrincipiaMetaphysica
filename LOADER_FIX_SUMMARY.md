# JS Loader Fix Summary

## Date: 2025-12-25

## Problem
The JavaScript loaders (`pm-constants-loader.js` and `pm-formula-loader.js`) were unable to reliably find and load data from `theory_output.json` and the AUTO_GENERATED directory. This caused data to not display properly on HTML pages.

## Root Causes

1. **Limited path search** - Only tried a few paths
2. **No fallback to individual JSON files** - If `theory_output.json` wasn't in the expected location, loaders failed completely
3. **Poor error messages** - Hard to debug why loading failed
4. **No CORS guidance** - Users didn't know how to handle file:// protocol issues
5. **Limited debugging tools** - No way to trace what paths were tried

## Solutions Implemented

### 1. Enhanced `pm-constants-loader.js`

**Changes**:
- ✅ Added comprehensive path search strategy (6 different path prefixes)
- ✅ Added fallback to individual JSON files in `AUTO_GENERATED/json/`:
  - `simulations.json`
  - `formulas.json`
  - `parameters.json`
  - `statistics.json`
- ✅ Added colored console logging (green=success, orange=warning, red=error)
- ✅ Added debug mode support via `window.PM_DEBUG = true`
- ✅ Exposed global objects for debugging:
  - `window.PM_DATA` - Raw data
  - `window.PM_FORMULAS` - Formula lookup
- ✅ Added detailed error messages with solutions
- ✅ Track and report all tried paths

**Path Search Order**:
```
1. theory_output.json (root)
2. AUTO_GENERATED/theory_output.json
3. ../theory_output.json
4. ../AUTO_GENERATED/theory_output.json
5. ../../theory_output.json
6. ../../AUTO_GENERATED/theory_output.json

If all fail, try individual JSON files:
7. AUTO_GENERATED/json/simulations.json
8. AUTO_GENERATED/json/formulas.json
9. AUTO_GENERATED/json/parameters.json
10. AUTO_GENERATED/json/statistics.json
(repeated for all 6 path prefixes)
```

### 2. Enhanced `pm-formula-loader.js`

**Changes**:
- ✅ Same path search strategy as constants loader
- ✅ Fallback to `AUTO_GENERATED/json/formulas.json`
- ✅ Added colored console logging
- ✅ Added debug mode support
- ✅ Exposed `window.PM_FORMULAS` globally
- ✅ Better error messages with solutions
- ✅ Added `render()` and `renderAll()` methods for automatic formula rendering

### 3. Enhanced `pm-section-renderer.js`

**Changes**:
- ✅ Updated to use same path search strategy
- ✅ Check multiple global objects: `window.PM.sections`, `window.PM_DATA.sections`
- ✅ Try `AUTO_GENERATED/json/sections.json` as primary source
- ✅ Fallback to `theory_output.json`
- ✅ Better error messages
- ✅ Debug mode support

### 4. Created `test-loaders.html`

**Purpose**: Comprehensive test page for debugging loaders

**Features**:
- ✅ Real-time loader status indicators
- ✅ Test all loading strategies
- ✅ Display console messages on page
- ✅ Test JavaScript API functions
- ✅ Inspect global objects
- ✅ Test data-pm-value attributes
- ✅ Test data-category/data-param attributes
- ✅ Test formula loading and rendering
- ✅ Display simulation results
- ✅ Manual reload and debug controls

### 5. Created `LOADER_DEBUG_GUIDE.md`

**Purpose**: Comprehensive documentation for loader system

**Contents**:
- Overview of loader architecture
- How loaders work (multi-path strategy)
- Global objects exposed
- HTML usage examples
- JavaScript API reference
- Debugging instructions
- Common issues and solutions
- Performance notes
- Best practices
- Version history

## Files Modified

1. `js/pm-constants-loader.js` - Enhanced with multi-path loading and better error handling
2. `js/pm-formula-loader.js` - Enhanced with multi-path loading and rendering
3. `js/pm-section-renderer.js` - Updated path search and error handling

## Files Created

1. `test-loaders.html` - Comprehensive test and debug page
2. `js/LOADER_DEBUG_GUIDE.md` - Complete documentation
3. `LOADER_FIX_SUMMARY.md` - This summary document

## Usage Examples

### Enable Debug Mode
```javascript
window.PM_DEBUG = true;
```

### Check Loader Status
```javascript
console.log('PM loaded:', window.PM._loaded);
console.log('PM error:', window.PM._error);
console.log('Formulas loaded:', window.PMFormulaLoader._loaded);
```

### Access Data
```javascript
// Via PM object
PM.get('simulations.proton_decay.tau_p_years')
PM.simulation('wz_evolution.m_W_GeV')
PM.formula('generation-number')

// Via global objects
window.PM_DATA.simulations.proton_decay
window.PM_FORMULAS['generation-number']
```

### HTML Usage
```html
<!-- Data values -->
<span data-pm-value="simulations.proton_decay.tau_p_years"></span>
<span data-pm-value="parameters.topology.B2"></span>

<!-- Formulas -->
<div data-formula-id="generation-number"></div>

<!-- With formatting -->
<span data-pm-value="simulations.wz_evolution.m_W_GeV" data-format="fixed:3"></span>
```

## Testing

To test the fixes:

1. **Generate JSON files**:
   ```bash
   python run_all_simulations.py --export
   ```

2. **Start local web server** (to avoid CORS issues):
   ```bash
   python -m http.server 8000
   ```

3. **Open test page**:
   ```
   http://localhost:8000/test-loaders.html
   ```

4. **Check status indicators**:
   - Green = Success
   - Yellow = Loading
   - Red = Error

5. **Review console messages** for detailed path information

## Error Messages

The enhanced loaders provide helpful error messages:

```
PM: Failed to load data!
  Tried paths: ["theory_output.json", "AUTO_GENERATED/theory_output.json", ...]

  SOLUTIONS:
  1. Run: python run_all_simulations.py --export
  2. Check that theory_output.json or AUTO_GENERATED/json/*.json exist
  3. If using file:// protocol, you may need to run a local web server
     Try: python -m http.server 8000

  Set window.PM_DEBUG = true for verbose logging
```

## Benefits

1. **Robustness**: Loaders now work from any directory depth
2. **Flexibility**: Can use unified `theory_output.json` OR individual JSON files
3. **Debuggability**: Clear error messages and debug mode
4. **Transparency**: Shows exactly which paths were tried
5. **User-Friendly**: Provides solutions, not just error messages
6. **Performance**: Still caches data and only loads once
7. **Backward Compatible**: Old HTML pages continue to work

## Known Limitations

1. **CORS**: Still requires web server for local file:// protocol
   - **Solution**: Use `python -m http.server 8000`

2. **No retry on network errors**: If fetch fails due to network, won't auto-retry
   - **Solution**: Manual reload via `PM.load()` or refresh page

3. **No progressive loading**: All data loaded at once
   - **Future**: Could implement lazy loading for large datasets

## Future Enhancements

Potential improvements for future versions:

1. **Service Worker caching** - Offline support
2. **Progressive/lazy loading** - Load data on demand
3. **WebSocket support** - Real-time updates from simulations
4. **IndexedDB storage** - Client-side caching
5. **Automatic retry** - Retry failed requests
6. **Loading progress indicators** - Show % loaded
7. **Differential updates** - Only update changed data
8. **Compression** - Gzip JSON files for faster loading

## Version

**Current Version**: 2.1.0 (2025-12-25)

## Conclusion

The JS loaders are now significantly more robust and easier to debug. They handle multiple deployment scenarios, provide clear error messages, and expose debugging tools. The comprehensive test page and documentation make it easy to verify functionality and troubleshoot issues.

All existing HTML pages should continue to work without modification, while benefiting from the improved error handling and fallback mechanisms.
