# Detailed Changes to auth-guard.js

## Summary of Changes

This document outlines the specific changes made to enhance `auth-guard.js` with Firebase data loading, PM value population, and tooltip initialization.

---

## 1. File Header Documentation
**Changed:** Updated copyright header to reflect enhanced functionality

```diff
  /**
   * Authentication Guard Module for Principia Metaphysica
   *
   * Protects page content until user is authenticated.
   * Shows login overlay when not authenticated, reveals content when authenticated.
+  * Loads Firebase data and populates PM values after authentication.
   *
   * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
   */
```

---

## 2. handleAuthenticated() Function
**Changed:** Complete rewrite to implement proper data loading workflow

### BEFORE:
```javascript
async function handleAuthenticated(user) {
  console.log(`[PM Auth Guard] User authenticated: ${user.email}`);
  isAuthenticated = true;

  // Hide overlay, show content
  document.body.classList.remove('not-authenticated');
  document.body.classList.add('authenticated');

  const overlay = document.getElementById('auth-overlay');
  if (overlay) {
    overlay.style.display = 'none';
  }

  const mainContent = document.getElementById('main-content');
  if (mainContent) {
    mainContent.style.display = 'block';
  }

  // Update user info display
  updateUserDisplay(user);

  // Initialize data from Firestore
  try {
    await initializeData();

    // Load page-specific data if needed
    if (currentPageId) {
      const pageData = await loadAllPageData(currentPageId);
      console.log(`[PM Auth Guard] Page data loaded for ${currentPageId}`);

      // Dispatch event for page-specific handling
      window.dispatchEvent(new CustomEvent('pm-data-ready', { detail: pageData }));
    }
  } catch (error) {
    console.error('[PM Auth Guard] Error initializing data:', error);
  }
}
```

### AFTER:
```javascript
async function handleAuthenticated(user) {
  console.log(`[PM Auth Guard] User authenticated: ${user.email}`);
  isAuthenticated = true;

  // Update user info display
  updateUserDisplay(user);

  // Show loading state
  showLoadingState();

  try {
    // Initialize data from Firestore
    console.log('[PM Auth Guard] Loading Firebase data...');
    await initializeData();

    // Load page-specific data if needed
    let pageData = null;
    if (currentPageId) {
      pageData = await loadAllPageData(currentPageId);
      console.log(`[PM Auth Guard] Page data loaded for ${currentPageId}`);
    }

    // Ensure PM object is available globally
    if (!window.PM) {
      console.error('[PM Auth Guard] PM object not available after data load!');
      throw new Error('Theory constants failed to load');
    }

    // Populate all PM values on the page
    populatePMValues();

    // Initialize tooltips
    initializeTooltips();

    // Hide overlay, show content
    hideLoadingState();
    document.body.classList.remove('not-authenticated');
    document.body.classList.add('authenticated');

    const overlay = document.getElementById('auth-overlay');
    if (overlay) {
      overlay.style.display = 'none';
    }

    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.style.display = 'block';
    }

    // Dispatch event for page-specific handling
    console.log('[PM Auth Guard] Dispatching pm-data-ready event');
    window.dispatchEvent(new CustomEvent('pm-data-ready', {
      detail: pageData || { loaded: true, timestamp: Date.now() }
    }));

    console.log('[PM Auth Guard] Page initialization complete');

  } catch (error) {
    console.error('[PM Auth Guard] Error initializing data:', error);
    showErrorState(error.message || 'Failed to load data');
  }
}
```

**Key Differences:**
1. Shows loading state immediately
2. Validates PM object is available
3. Calls `populatePMValues()` before showing content
4. Calls `initializeTooltips()` before showing content
5. Hides loading state after data loads
6. Shows content ONLY after data is ready
7. Better error handling with `showErrorState()`
8. More detailed logging

---

## 3. injectAuthOverlay() Function
**Changed:** Added loading and error message containers

### BEFORE:
```html
      <button id="google-login-btn" class="google-login-btn">
        <img src="/images/google-icon.svg" alt="Google" class="google-icon">
        Login with Google
      </button>

      <footer class="auth-footer">
        <p>Copyright © Andrew K Watts 2025</p>
      </footer>
```

### AFTER:
```html
      <button id="google-login-btn" class="google-login-btn">
        <img src="/images/google-icon.svg" alt="Google" class="google-icon">
        Login with Google
      </button>

      <div id="auth-loading" style="display: none; margin-top: 20px; color: #4caf50;">
        <p>Loading data...</p>
      </div>

      <div id="auth-error" style="display: none; margin-top: 20px; color: #f44336;">
        <p></p>
      </div>

      <footer class="auth-footer">
        <p>Copyright © Andrew K Watts 2025</p>
      </footer>
```

---

## 4. New Functions Added

### showLoadingState()
**Purpose:** Show loading message while Firebase data loads
```javascript
function showLoadingState() {
  const loadingDiv = document.getElementById('auth-loading');
  const errorDiv = document.getElementById('auth-error');
  const loginBtn = document.getElementById('google-login-btn');

  if (loadingDiv) {
    loadingDiv.style.display = 'block';
  }
  if (errorDiv) {
    errorDiv.style.display = 'none';
  }
  if (loginBtn) {
    loginBtn.style.display = 'none';
  }

  console.log('[PM Auth Guard] Showing loading state');
}
```

### hideLoadingState()
**Purpose:** Hide loading message after data loads
```javascript
function hideLoadingState() {
  const loadingDiv = document.getElementById('auth-loading');
  if (loadingDiv) {
    loadingDiv.style.display = 'none';
  }
  console.log('[PM Auth Guard] Hiding loading state');
}
```

### showErrorState(message)
**Purpose:** Show error message if data loading fails
```javascript
function showErrorState(message) {
  const loadingDiv = document.getElementById('auth-loading');
  const errorDiv = document.getElementById('auth-error');
  const loginBtn = document.getElementById('google-login-btn');

  if (loadingDiv) {
    loadingDiv.style.display = 'none';
  }
  if (errorDiv) {
    errorDiv.innerHTML = `<p>Error: ${message}</p><p>Please refresh the page to try again.</p>`;
    errorDiv.style.display = 'block';
  }
  if (loginBtn) {
    loginBtn.style.display = 'none';
  }

  console.error('[PM Auth Guard] Showing error state:', message);
}
```

### populatePMValues()
**Purpose:** Populate all PM values from window.PM object
```javascript
function populatePMValues() {
  if (!window.PM) {
    console.warn('[PM Auth Guard] Cannot populate PM values - PM object not available');
    return;
  }

  const elements = document.querySelectorAll('.pm-value, [data-category][data-param]');
  let populatedCount = 0;

  elements.forEach(el => {
    const category = el.dataset.category;
    const param = el.dataset.param;
    const format = el.dataset.format;
    const field = el.dataset.field;

    if (!category || !param) {
      console.warn('[PM Auth Guard] Missing data-category or data-param on element:', el);
      return;
    }

    if (!window.PM[category]) {
      console.warn(`[PM Auth Guard] Category "${category}" not found in PM constants`);
      return;
    }

    const obj = window.PM[category][param];
    if (!obj) {
      console.warn(`[PM Auth Guard] Parameter "${param}" not found in PM.${category}`);
      return;
    }

    // Get the value - either from a nested field or the main value
    let value;
    if (field && obj[field] !== undefined) {
      value = obj[field];
    } else {
      value = obj.value;
    }

    // Use display string if available, otherwise format value
    let displayValue;
    if (format === 'display' && obj.display) {
      displayValue = obj.display;
    } else if (typeof value === 'number') {
      displayValue = formatValue(value, format);
    } else {
      displayValue = value.toString();
    }

    // Set the text content
    el.textContent = displayValue;

    // Add unit if specified and not already in display
    if (!field && obj.unit && !el.dataset.noUnit && format !== 'display') {
      el.textContent += ' ' + obj.unit;
    }

    // Store object reference for tooltip
    el._pmObject = obj;

    populatedCount++;
  });

  console.log(`[PM Auth Guard] Populated ${populatedCount} PM values on the page`);
}
```

### formatValue(value, format)
**Purpose:** Format numeric values according to specification
```javascript
function formatValue(value, format) {
  if (!format) {
    return value.toString();
  }

  const [type, precision] = format.split(':');
  const prec = parseInt(precision) || 2;

  switch (type) {
    case 'scientific':
      return value.toExponential(prec);
    case 'fixed':
      return value.toFixed(prec);
    case 'percent':
      return (value * 100).toFixed(prec) + '%';
    case 'display':
      return value;
    default:
      return value.toString();
  }
}
```

### initializeTooltips()
**Purpose:** Set up tooltip system for PM values
```javascript
function initializeTooltips() {
  if (!window.PM) {
    console.warn('[PM Auth Guard] Cannot initialize tooltips - PM object not available');
    return;
  }

  // Add PM.getTooltip helper if not already present
  if (!window.PM.getTooltip) {
    window.PM.getTooltip = buildTooltipFunction();
  }

  // Setup hover listeners
  document.addEventListener('mouseover', (e) => {
    if (e.target.classList.contains('pm-value') && e.target._pmObject) {
      showTooltip(e, e.target._pmObject);
    }
  });

  document.addEventListener('mouseout', (e) => {
    if (e.target.classList.contains('pm-value')) {
      removeTooltip();
    }
  });

  // Update tooltip position on mouse move
  document.addEventListener('mousemove', (e) => {
    const tooltip = document.querySelector('.pm-tooltip-popup');
    if (tooltip) {
      tooltip.style.left = e.pageX + 10 + 'px';
      tooltip.style.top = e.pageY + 10 + 'px';
    }
  });

  console.log('[PM Auth Guard] Tooltip system initialized');
}
```

### buildTooltipFunction()
**Purpose:** Create tooltip generation function
- Builds comprehensive tooltip HTML with all PM object metadata

### showTooltip(event, obj)
**Purpose:** Display tooltip at cursor position
```javascript
function showTooltip(event, obj) {
  removeTooltip();

  const tooltip = document.createElement('div');
  tooltip.className = 'pm-tooltip-popup';
  tooltip.innerHTML = window.PM.getTooltip(obj);

  tooltip.style.position = 'absolute';
  tooltip.style.left = event.pageX + 10 + 'px';
  tooltip.style.top = event.pageY + 10 + 'px';
  tooltip.style.zIndex = '10000';

  document.body.appendChild(tooltip);
}
```

### removeTooltip()
**Purpose:** Remove tooltip from DOM
```javascript
function removeTooltip() {
  const existing = document.querySelector('.pm-tooltip-popup');
  if (existing) {
    existing.remove();
  }
}
```

---

## File Statistics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Lines | 245 | 609 | +364 |
| Functions | 8 | 18 | +10 |
| LOC (code) | ~200 | ~550 | +350 |
| Comments | ~45 | ~60 | +15 |

---

## Testing Checklist

After replacing the file, verify:

- [ ] User can log in successfully
- [ ] "Loading data..." message appears after login
- [ ] PM values populate on the page
- [ ] Tooltips appear on hover over PM values
- [ ] Error message displays if data fails to load
- [ ] Console shows proper logging messages
- [ ] `pm-data-ready` event is dispatched
- [ ] `window.PM` object is available globally
- [ ] Page content shows ONLY after data loads
