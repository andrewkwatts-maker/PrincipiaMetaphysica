/**
 * Authentication Guard Module for Principia Metaphysica
 *
 * Protects page content until user is authenticated.
 * Shows login overlay when not authenticated, reveals content when authenticated.
 * Loads Firebase data and populates PM values after authentication.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { onAuthReady, signInWithGoogle, signOutUser, getUserInfo } from './firebase-auth.js';
import { initializeData, loadAllPageData } from './firebase-data.js';

// Current page identifier (set by page)
let currentPageId = null;

// Auth state
let isAuthenticated = false;

/**
 * Initialize the auth guard
 * @param {string} pageId - Identifier for this page (e.g., 'index', 'fermion-sector')
 */
export function setupAuthGuard(pageId = 'index') {
  currentPageId = pageId;

  console.log(`[PM Auth Guard] Setting up for page: ${pageId}`);

  // Add not-authenticated class to body initially
  document.body.classList.add('not-authenticated');

  // Create and inject auth overlay if it doesn't exist
  if (!document.getElementById('auth-overlay')) {
    injectAuthOverlay();
  }

  // Set up auth state listener
  onAuthReady(async (user) => {
    if (user) {
      await handleAuthenticated(user);
    } else {
      handleNotAuthenticated();
    }
  });

  // Set up login button handler
  const loginBtn = document.getElementById('google-login-btn');
  if (loginBtn) {
    loginBtn.addEventListener('click', handleLogin);
  }

  // Set up logout button handler
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
}

/**
 * Handle authenticated state
 * @param {Object} user - Firebase user object
 */
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

/**
 * Handle not authenticated state
 */
function handleNotAuthenticated() {
  console.log('[PM Auth Guard] User not authenticated');
  isAuthenticated = false;

  // Show overlay, hide content
  document.body.classList.add('not-authenticated');
  document.body.classList.remove('authenticated');

  const overlay = document.getElementById('auth-overlay');
  if (overlay) {
    overlay.style.display = 'flex';
  }

  const mainContent = document.getElementById('main-content');
  if (mainContent) {
    mainContent.style.display = 'none';
  }

  // Clear user display
  updateUserDisplay(null);
}

/**
 * Handle login button click
 */
async function handleLogin() {
  const loginBtn = document.getElementById('google-login-btn');
  if (loginBtn) {
    loginBtn.disabled = true;
    loginBtn.textContent = 'Signing in...';
  }

  try {
    await signInWithGoogle();
  } catch (error) {
    console.error('[PM Auth Guard] Login failed:', error);
  } finally {
    if (loginBtn) {
      loginBtn.disabled = false;
      loginBtn.innerHTML = '<img src="/images/google-icon.svg" alt="Google" class="google-icon"> Login with Google';
    }
  }
}

/**
 * Handle logout button click
 */
async function handleLogout() {
  await signOutUser();
}

/**
 * Update user display in header
 * @param {Object|null} user - Firebase user object or null
 */
function updateUserDisplay(user) {
  const userAvatar = document.getElementById('user-avatar');
  const userEmail = document.getElementById('user-email');
  const logoutBtn = document.getElementById('logout-btn');
  const userControls = document.querySelector('.user-controls');

  if (user) {
    if (userAvatar) {
      userAvatar.src = user.photoURL || '/images/default-avatar.svg';
      userAvatar.alt = user.displayName || 'User';
      userAvatar.style.display = 'block';
    }
    if (userEmail) {
      userEmail.textContent = user.email;
      userEmail.style.display = 'block';
    }
    if (logoutBtn) {
      logoutBtn.style.display = 'block';
    }
    if (userControls) {
      userControls.style.display = 'flex';
    }
  } else {
    if (userAvatar) userAvatar.style.display = 'none';
    if (userEmail) userEmail.style.display = 'none';
    if (logoutBtn) logoutBtn.style.display = 'none';
    if (userControls) userControls.style.display = 'none';
  }
}

/**
 * Inject the auth overlay HTML into the page
 */
function injectAuthOverlay() {
  const overlay = document.createElement('div');
  overlay.id = 'auth-overlay';
  overlay.className = 'auth-overlay';
  overlay.innerHTML = `
    <div class="auth-card">
      <div class="auth-logo">
        <span class="pm-symbol">PM</span>
      </div>

      <h1 class="auth-title">Principia Metaphysica</h1>
      <p class="auth-latin">Philosophiae Metaphysicae Principia Mathematica</p>

      <div class="auth-framework">
        <h2>The Two-Time Framework</h2>
        <p>A First-Principles Geometric Theory</p>
      </div>

      <p class="auth-description">
        A unified geometric framework deriving all 58 Standard Model
        parameters from a single G₂ manifold with minimal calibration
        (2 fitted parameters)
      </p>

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
    </div>
  `;

  // Insert at beginning of body
  document.body.insertBefore(overlay, document.body.firstChild);
}

/**
 * Show loading state in auth overlay
 */
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

/**
 * Hide loading state
 */
function hideLoadingState() {
  const loadingDiv = document.getElementById('auth-loading');
  if (loadingDiv) {
    loadingDiv.style.display = 'none';
  }
  console.log('[PM Auth Guard] Hiding loading state');
}

/**
 * Show error state in auth overlay
 * @param {string} message - Error message to display
 */
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

/**
 * Populate all PM values on the page
 * Finds elements with class 'pm-value' and populates them with data from window.PM
 */
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

/**
 * Format a value according to specified format
 * @param {number} value - The value to format
 * @param {string} format - Format specification (e.g., 'scientific:2', 'fixed:3', 'percent')
 * @returns {string} Formatted value
 */
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

/**
 * Initialize tooltip system
 * Sets up hover listeners for PM values to show tooltips
 */
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

/**
 * Build tooltip generation function
 * @returns {Function} Function that generates tooltip HTML
 */
function buildTooltipFunction() {
  return (obj) => {
    let tooltip = `<div class="pm-tooltip-content">`;

    // Value and unit
    tooltip += `<div class="pm-tooltip-value"><strong>${obj.display || obj.value}</strong>`;
    if (obj.unit) {
      tooltip += ` ${obj.unit}`;
    }
    tooltip += `</div>`;

    // Description
    if (obj.description) {
      tooltip += `<div class="pm-tooltip-desc">${obj.description}</div>`;
    }

    // Formula
    if (obj.formula) {
      tooltip += `<div class="pm-tooltip-formula"><em>Formula:</em> ${obj.formula}</div>`;
    }

    // Derivation
    if (obj.derivation) {
      tooltip += `<div class="pm-tooltip-derivation"><em>Derivation:</em> ${obj.derivation}</div>`;
    }

    // Uncertainty
    if (obj.uncertainty !== undefined || obj.uncertainty_oom !== undefined) {
      const unc = obj.uncertainty_oom !== undefined
        ? `±${obj.uncertainty_oom.toFixed(2)} OOM`
        : obj.uncertainty_lower && obj.uncertainty_upper
          ? `${obj.confidence_level || '68%'} CI: [${obj.uncertainty_lower.toExponential(2)}-${obj.uncertainty_upper.toExponential(2)}]`
          : `±${obj.uncertainty}`;
      tooltip += `<div class="pm-tooltip-uncertainty"><em>Uncertainty:</em> ${unc}</div>`;
    }

    // Experimental comparison
    if (obj.experimental_value !== undefined) {
      tooltip += `<div class="pm-tooltip-experiment">`;
      tooltip += `<em>Experiment:</em> ${obj.experimental_value}`;
      if (obj.experimental_uncertainty) {
        tooltip += ` ± ${obj.experimental_uncertainty}`;
      }
      if (obj.experimental_source) {
        tooltip += ` (${obj.experimental_source})`;
      }
      tooltip += `</div>`;
    }

    // Agreement
    if (obj.agreement_sigma !== undefined || obj.agreement || obj.agreement_text) {
      const sigma = obj.agreement_sigma || 0;
      const color = sigma < 1 ? '#4caf50' : sigma < 3 ? '#ff9800' : '#f44336';
      tooltip += `<div class="pm-tooltip-agreement" style="color:${color}">`;
      tooltip += `<em>Agreement:</em> ${obj.agreement_text || obj.agreement || `${sigma.toFixed(2)}σ`}`;
      tooltip += `</div>`;
    }

    // Testability
    if (obj.testable) {
      tooltip += `<div class="pm-tooltip-testable"><em>Testable:</em> ${obj.testable}</div>`;
    }

    // Source
    if (obj.source) {
      tooltip += `<div class="pm-tooltip-source"><em>Source:</em> <code>${obj.source}</code></div>`;
    }

    // References
    if (obj.references && obj.references.length > 0) {
      tooltip += `<div class="pm-tooltip-refs"><em>References:</em> ${obj.references.join(', ')}</div>`;
    }

    tooltip += `</div>`;
    return tooltip;
  };
}

/**
 * Show tooltip for a PM value
 * @param {MouseEvent} event - Mouse event
 * @param {Object} obj - PM object data
 */
function showTooltip(event, obj) {
  // Remove any existing tooltips
  removeTooltip();

  const tooltip = document.createElement('div');
  tooltip.className = 'pm-tooltip-popup';
  tooltip.innerHTML = window.PM.getTooltip(obj);

  // Position tooltip near cursor
  tooltip.style.position = 'absolute';
  tooltip.style.left = event.pageX + 10 + 'px';
  tooltip.style.top = event.pageY + 10 + 'px';
  tooltip.style.zIndex = '10000';

  document.body.appendChild(tooltip);
}

/**
 * Remove tooltip from DOM
 */
function removeTooltip() {
  const existing = document.querySelector('.pm-tooltip-popup');
  if (existing) {
    existing.remove();
  }
}

/**
 * Check if user is currently authenticated
 * @returns {boolean}
 */
export function isUserAuthenticated() {
  return isAuthenticated;
}

/**
 * Get current page ID
 * @returns {string|null}
 */
export function getCurrentPageId() {
  return currentPageId;
}
