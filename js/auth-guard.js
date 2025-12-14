/**
 * Authentication Guard Module for Principia Metaphysica
 *
 * Protects page content until user is authenticated.
 * Shows login overlay when not authenticated, reveals content when authenticated.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { onAuthReady, signInWithGoogle, signOutUser, getUserInfo } from './firebase-auth.js';
import { initializeData, loadAllPageData } from './firebase-data.js';
import { trackUserLogin, trackUserLogout, trackPageView } from './firebase-analytics.js';

// Current page identifier (set by page)
let currentPageId = null;

// Auth state
let isAuthenticated = false;

// Expose signInWithGoogle globally for header login button onclick handlers
window.signInWithGoogle = signInWithGoogle;

/**
 * Initialize the auth guard
 * @param {string} pageId - Identifier for this page (e.g., 'index', 'fermion-sector')
 */
export function setupAuthGuard(pageId = 'index') {
  currentPageId = pageId;

  console.log(`[PM Auth Guard] Setting up for page: ${pageId}`);

  // Start with loading state (prevents flicker)
  document.body.classList.add('auth-loading');
  document.body.classList.remove('not-authenticated', 'authenticated');

  // Create and inject loading screen if it doesn't exist
  if (!document.getElementById('auth-loading-screen')) {
    injectLoadingScreen();
  }

  // Create and inject auth overlay if it doesn't exist
  if (!document.getElementById('auth-overlay')) {
    injectAuthOverlay();
  }

  // Set up auth state listener
  onAuthReady(async (user) => {
    // Remove loading state
    document.body.classList.remove('auth-loading');

    if (user) {
      await handleAuthenticated(user);
    } else {
      handleNotAuthenticated();
    }
  });

  // Set up login button handlers (both overlay and header)
  setupLoginHandlers();

  // Set up logout button handler
  setupLogoutHandler();
}

/**
 * Set up login button handlers
 */
function setupLoginHandlers() {
  // Overlay login button
  const overlayLoginBtn = document.getElementById('google-login-btn');
  if (overlayLoginBtn) {
    overlayLoginBtn.addEventListener('click', handleLogin);
  }

  // Header login button
  const headerLoginBtn = document.getElementById('header-login-btn');
  if (headerLoginBtn) {
    headerLoginBtn.addEventListener('click', handleLogin);
  }
}

/**
 * Set up logout button handler
 */
function setupLogoutHandler() {
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

  // Track user login
  await trackUserLogin(user);

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

      // Track page view
      await trackPageView(user, currentPageId);

      // Dispatch event for page-specific handling
      window.dispatchEvent(new CustomEvent('pm-data-ready', { detail: pageData }));
    }
  } catch (error) {
    console.error('[PM Auth Guard] Error initializing data:', error);
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
  const user = getUserInfo();
  if (user) {
    await trackUserLogout(user);
  }
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
 * Inject loading screen HTML into the page
 */
function injectLoadingScreen() {
  const loadingScreen = document.createElement('div');
  loadingScreen.id = 'auth-loading-screen';
  loadingScreen.innerHTML = `
    <div class="auth-spinner"></div>
    <p class="loading-text">Loading Principia Metaphysica...</p>
  `;

  // Insert at beginning of body
  document.body.insertBefore(loadingScreen, document.body.firstChild);
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

      <footer class="auth-footer">
        <p>Copyright © Andrew K Watts 2025</p>
      </footer>
    </div>
  `;

  // Insert at beginning of body
  document.body.insertBefore(overlay, document.body.firstChild);
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
