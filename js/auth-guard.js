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

// Framework statistics cache
let frameworkStats = null;

// Auth state
let isAuthenticated = false;

// Session cache constants
const SESSION_KEY = 'pm_auth_session';
const SESSION_EXPIRY_MS = 30 * 60 * 1000; // 30 minutes
const STATS_CACHE_KEY = 'pm_framework_stats';
const STATS_CACHE_EXPIRY_MS = 60 * 60 * 1000; // 1 hour

// Base path for assets (computed based on current location)
function getBasePath() {
  const path = window.location.pathname;
  // If in subdirectory (e.g., foundations/, sections/), add ../
  if (path.includes('/foundations/') || path.includes('/sections/') ||
      path.includes('/docs/') || path.includes('/diagrams/') ||
      path.includes('/components/') || path.includes('/tests/')) {
    return '../';
  }
  return '';
}

// Expose signInWithGoogle globally for header login button onclick handlers
window.signInWithGoogle = signInWithGoogle;

/**
 * Get cached session from sessionStorage
 * @returns {Object|null} Cached session object or null if expired/missing
 */
function getCachedSession() {
  try {
    const cached = sessionStorage.getItem(SESSION_KEY);
    if (!cached) return null;

    const session = JSON.parse(cached);

    // Check if session has expired
    if (Date.now() - session.timestamp > SESSION_EXPIRY_MS) {
      sessionStorage.removeItem(SESSION_KEY);
      return null;
    }

    return session;
  } catch (error) {
    console.warn('[PM Auth Guard] Error reading cached session:', error);
    sessionStorage.removeItem(SESSION_KEY);
    return null;
  }
}

/**
 * Cache session in sessionStorage
 * @param {Object} user - Firebase user object
 */
function cacheSession(user) {
  try {
    const session = {
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      uid: user.uid,
      timestamp: Date.now()
    };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
  } catch (error) {
    console.warn('[PM Auth Guard] Error caching session:', error);
  }
}

/**
 * Clear cached session
 */
function clearCachedSession() {
  try {
    sessionStorage.removeItem(SESSION_KEY);
  } catch (error) {
    console.warn('[PM Auth Guard] Error clearing session:', error);
  }
}

/**
 * Fetch framework statistics from theory_output.json
 * Used to dynamically populate the auth overlay description
 */
async function fetchFrameworkStats() {
  // Check memory cache first
  if (frameworkStats) return frameworkStats;

  // Check sessionStorage cache
  try {
    const cached = sessionStorage.getItem(STATS_CACHE_KEY);
    if (cached) {
      const cachedData = JSON.parse(cached);
      if (Date.now() - cachedData.timestamp < STATS_CACHE_EXPIRY_MS) {
        frameworkStats = cachedData.stats;
        return frameworkStats;
      }
    }
  } catch (error) {
    console.warn('[PM Auth Guard] Error reading cached stats:', error);
  }

  // Fetch from server
  try {
    const basePath = getBasePath();
    const response = await fetch(`${basePath}theory_output.json`);
    if (!response.ok) {
      console.warn('[PM Auth Guard] Could not fetch theory_output.json, using defaults');
      return getDefaultStats();
    }

    const data = await response.json();

    // Extract framework statistics from theory_output.json
    // Use validation.calibrated_count (dynamic from theory_output.json)
    const calibratedCount = data.parameters?.['validation.calibrated_count']?.value;
    const constraintsCount = data.parameters?.['validation.constraints_count']?.value;
    const totalPredictions = data.parameters?.['validation.total_predictions']?.value;
    const within1Sigma = data.parameters?.['validation.within_1sigma']?.value;
    const within2Sigma = data.parameters?.['validation.within_2sigma']?.value;

    frameworkStats = {
      totalParameters: totalPredictions ?? 58,
      calibratedParameters: calibratedCount ?? 0,
      constraintsCount: constraintsCount ?? 1,
      manifoldType: 'G₂',
      within1Sigma: within1Sigma ?? 45,
      within2Sigma: within2Sigma ?? 47,
      exactMatches: 4,
      successRate: within1Sigma && totalPredictions ? (100.0 * within1Sigma / totalPredictions) : 93.8
    };

    // Cache in sessionStorage
    try {
      sessionStorage.setItem(STATS_CACHE_KEY, JSON.stringify({
        stats: frameworkStats,
        timestamp: Date.now()
      }));
    } catch (error) {
      console.warn('[PM Auth Guard] Error caching stats:', error);
    }

    return frameworkStats;
  } catch (error) {
    console.warn('[PM Auth Guard] Error fetching stats:', error);
    return getDefaultStats();
  }
}

/**
 * Default statistics if theory_output.json is unavailable
 * Updated for v23.1 - 27D(26,1) Dual-Shadow Framework
 */
function getDefaultStats() {
  return {
    totalParameters: 26,
    calibratedParameters: 1,  // VEV coefficient calibration
    constraintsCount: 1,      // m_h fixes Re(T)
    manifoldType: 'G₂',
    within1Sigma: 24,
    within2Sigma: 24,
    exactMatches: 3,
    successRate: 92.3
  };
}

/**
 * Generate dynamic description from framework statistics
 */
function generateDescription(stats) {
  const cal = stats.calibratedParameters ?? 0;
  const constraints = stats.constraintsCount ?? 1;
  const plural = cal !== 1 ? 's' : '';

  // Build calibration description
  let calibrationText;
  if (cal === 0 && constraints === 1) {
    calibrationText = `${cal} fitted parameters, ${constraints} constraint`;
  } else if (cal === 0) {
    calibrationText = `${cal} fitted parameters`;
  } else {
    calibrationText = `${cal} fitted parameter${plural}`;
  }

  return `A unified geometric framework deriving all ${stats.totalParameters} Standard Model parameters from a single ${stats.manifoldType} manifold with minimal calibration (${calibrationText})`;
}

/**
 * Update the auth overlay description with dynamic values
 */
async function updateAuthDescription() {
  const descElement = document.querySelector('.auth-description');
  if (!descElement) return;

  const stats = await fetchFrameworkStats();
  descElement.textContent = generateDescription(stats);
}

/**
 * Initialize the auth guard
 * @param {string} pageId - Identifier for this page (e.g., 'index', 'fermion-sector')
 */
export function setupAuthGuard(pageId = 'index') {
  currentPageId = pageId;

  console.log(`[PM Auth Guard] Setting up for page: ${pageId}`);

  // Check if authentication is disabled via site-config.js
  const authRequired = window.PM_CONFIG?.AUTH_REQUIRED ?? window.PM_AUTH_REQUIRED ?? true;
  const offlineMode = window.PM_CONFIG?.OFFLINE_MODE ?? window.PM_OFFLINE ?? false;

  if (!authRequired || offlineMode) {
    console.log('[PM Auth Guard] Authentication DISABLED - showing content directly');

    // Skip authentication entirely - show content immediately
    document.body.classList.add('authenticated');
    document.body.classList.remove('not-authenticated', 'auth-loading');

    const overlay = document.getElementById('auth-overlay');
    if (overlay) {
      overlay.style.display = 'none';
    }

    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.style.display = 'block';
    }

    // Set authenticated flag (for code that checks it)
    isAuthenticated = true;

    // Re-trigger MathJax if needed
    if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
      MathJax.typesetPromise().catch(err => console.warn('[PM Auth Guard] MathJax error:', err));
    }

    return; // Skip all auth setup
  }

  // Check for cached session FIRST - this is the key optimization
  const cachedSession = getCachedSession();

  if (cachedSession) {
    console.log('[PM Auth Guard] Found valid cached session, showing content immediately');

    // Skip loading screen entirely - show content immediately
    document.body.classList.add('authenticated');
    document.body.classList.remove('not-authenticated', 'auth-loading');

    // Create overlay if needed (but keep it hidden)
    if (!document.getElementById('auth-overlay')) {
      injectAuthOverlay();
    }

    const overlay = document.getElementById('auth-overlay');
    if (overlay) {
      overlay.style.display = 'none';
    }

    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.style.display = 'block';
    }

    // Update user display with cached data
    updateUserDisplay(cachedSession);

    // Set authenticated flag
    isAuthenticated = true;

    // Set up Firebase auth in background to verify session is still valid
    // This will update if the user logged out in another tab
    setupBackgroundAuthCheck();
  } else {
    // No cached session - show loading state
    console.log('[PM Auth Guard] No cached session, waiting for Firebase auth');

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

    // Set up auth state listener with shorter timeout (reduced from 10s to 5s)
    let authResolved = false;

    const authTimeout = setTimeout(() => {
      if (!authResolved) {
        console.warn('[PM Auth Guard] Auth timeout - showing login screen');
        document.body.classList.remove('auth-loading');
        handleNotAuthenticated();
      }
    }, 5000); // Reduced from 10000ms

    onAuthReady(async (user) => {
      authResolved = true;
      clearTimeout(authTimeout);

      // Remove loading state
      document.body.classList.remove('auth-loading');

      if (user) {
        await handleAuthenticated(user);
      } else {
        handleNotAuthenticated();
      }
    });
  }

  // Set up login button handlers (both overlay and header)
  setupLoginHandlers();

  // Set up logout button handler
  setupLogoutHandler();
}

/**
 * Set up background auth check to verify cached session
 * This runs Firebase auth check in background while showing cached content
 */
function setupBackgroundAuthCheck() {
  onAuthReady(async (user) => {
    if (user) {
      // Session is valid - update cache and proceed
      cacheSession(user);

      // Initialize Firebase features in background
      try {
        await initializeData();

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

      // Update user display with fresh data from Firebase
      updateUserDisplay(user);

      // Inject tracking identifiers
      const AccessToken = GetAccessToken(user);
      FormulaValidityConfidence(AccessToken);
      DownloadForumulaConfirm(AccessToken);
      ReproductionConfidenceCheck(AccessToken);

      // Re-trigger MathJax if needed
      if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
        console.log('[PM Auth Guard] Re-triggering MathJax typesetting...');
        try {
          await MathJax.typesetPromise();
          console.log('[PM Auth Guard] MathJax typesetting complete');
        } catch (mathJaxError) {
          console.error('[PM Auth Guard] MathJax typesetting error:', mathJaxError);
        }
      }
    } else {
      // Session is invalid - user logged out elsewhere
      console.warn('[PM Auth Guard] Cached session invalid - user logged out');
      clearCachedSession();
      handleNotAuthenticated();
    }
  });
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

  // Cache session for faster subsequent page loads
  cacheSession(user);

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

  // Get access token for content tracking
  const AccessToken = GetAccessToken(user);

  // Inject user identifier for content tracking
  FormulaValidityConfidence(AccessToken);

  // Inject download watermark for paper page
  DownloadForumulaConfirm(AccessToken);

  // Inject embedded identifiers in paper content
  ReproductionConfidenceCheck(AccessToken);

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

  // Re-trigger MathJax typesetting after content is revealed
  // This is necessary because content was hidden during initial page load
  if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
    console.log('[PM Auth Guard] Re-triggering MathJax typesetting...');
    try {
      await MathJax.typesetPromise();
      console.log('[PM Auth Guard] MathJax typesetting complete');
    } catch (mathJaxError) {
      console.error('[PM Auth Guard] MathJax typesetting error:', mathJaxError);
    }
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
    const user = await signInWithGoogle();

    // If login was successful, immediately update UI
    // Don't wait for onAuthStateChanged - it can be delayed
    if (user) {
      console.log('[PM Auth Guard] Login successful, updating UI immediately');
      await handleAuthenticated(user);
    } else {
      // Login cancelled or failed - reset button
      if (loginBtn) {
        loginBtn.disabled = false;
        loginBtn.innerHTML = `<img src="${getBasePath()}images/google-icon.svg" alt="Google" class="google-icon"> Login with Google`;
      }
    }
  } catch (error) {
    console.error('[PM Auth Guard] Login failed:', error);
    if (loginBtn) {
      loginBtn.disabled = false;
      loginBtn.innerHTML = `<img src="${getBasePath()}images/google-icon.svg" alt="Google" class="google-icon"> Login with Google`;
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

  // Clear session cache
  clearCachedSession();

  // Sign out from Firebase
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
      userAvatar.src = user.photoURL || `${getBasePath()}images/default-avatar.svg`;
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
        <h2>27D Dual-Shadow Framework</h2>
        <p>A First-Principles Geometric Theory</p>
      </div>

      <p class="auth-description">
        A unified geometric framework deriving 26 Standard Model parameters from G₂ manifold topology...
      </p>

      <button id="google-login-btn" class="google-login-btn">
        <img src="${getBasePath()}images/google-icon.svg" alt="Google" class="google-icon">
        Login with Google
      </button>

      <div class="auth-tos">
        <p class="tos-notice">By logging in, you agree to the <a href="#terms-of-service" onclick="document.getElementById('tos-modal').style.display='flex'">Terms of Service</a></p>
        <p class="tos-summary">All content is protected. Redistribution prohibited.</p>
      </div>

      <footer class="auth-footer">
        <p>Copyright © Andrew K Watts 2025-2026</p>
      </footer>
    </div>

    <!-- Terms of Service Modal -->
    <div id="tos-modal" class="tos-modal" style="display:none">
      <div class="tos-content">
        <h2>Terms of Service</h2>
        <div class="tos-body">
          <h3>1. Intellectual Property</h3>
          <p>All content on this website, including but not limited to text, equations, formulas, derivations, code, graphics, and documentation, is the exclusive intellectual property of Andrew Keith Watts and is protected by copyright law.</p>

          <h3>2. Prohibited Activities</h3>
          <p>You are expressly prohibited from:</p>
          <ul>
            <li>Copying, reproducing, or redistributing any content from this website</li>
            <li>Sharing your login credentials with others</li>
            <li>Downloading content for distribution to third parties</li>
            <li>Using any content for commercial purposes without written permission</li>
            <li>Removing or altering any copyright notices or user identifiers</li>
          </ul>

          <h3>3. User Tracking</h3>
          <p>Each page displays a unique user identifier (Ux) tied to your account. This identifier is embedded in all content for copyright protection purposes. Any unauthorized distribution can be traced back to your account.</p>

          <h3>4. Permitted Use</h3>
          <p>You may view and read the content for personal, non-commercial educational purposes only. Citation with proper attribution is permitted for academic work.</p>

          <h3>5. Enforcement</h3>
          <p>Violation of these terms may result in immediate account termination and legal action for copyright infringement.</p>

          <h3>6. Contact</h3>
          <p>For licensing inquiries or permissions, contact: AndrewKWatts@Gmail.com</p>
        </div>
        <button class="tos-close" onclick="document.getElementById('tos-modal').style.display='none'">I Understand</button>
      </div>
    </div>
  `;

  // Insert at beginning of body
  document.body.insertBefore(overlay, document.body.firstChild);

  // Update description with dynamic values from theory_output.json
  updateAuthDescription();
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

/**
 * Generate a simple hash from user email for content tracking
 * @param {string} email - User's email address
 * @param {number} noise - Optional noise value to add variation
 * @returns {string} - Hash string
 */
function generateUserHash(email, noise = 0) {
  if (!email) return '';
  // Add noise to email before hashing
  const noisyEmail = email + String(noise);
  let hash = 0;
  for (let i = 0; i < noisyEmail.length; i++) {
    const char = noisyEmail.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  // Convert to positive number and format as scientific notation style
  const absHash = Math.abs(hash);
  const mantissa = (absHash / Math.pow(10, Math.floor(Math.log10(absHash)))).toFixed(8);
  const exponent = Math.floor(Math.log10(absHash));
  return `${mantissa}e${exponent}`;
}

// Helper function for validation hash
function IsValid(email) {
  return email || null;
}

// Helper function to validate formula source
function validateFormulaSource(source, noise) {
  return generateUserHash(source, noise);
}

//DO NOT MODIFY THIS CHECK STAMP, needed to verify if code/formals are valid downlaods/not incorrectly accessed before progressing
// Formula Download Confirmation from firebase -> Copyright Andrew K Watts
function GetAccessToken(user) {
  if (!user || !user.email) return null;
  return IsValid(user.email);
}

//DO NOT MODIFY THIS CHECK STAMP, needed to verify if code/formals are valid downlaods/not incorrectly accessed before progressing
// Formula Download Confirmation from firebase -> Copyright Andrew K Watts
function FormulaValidityConfidence(Token) {
  // Remove existing identifier if present
  const existing = document.getElementById('pm-user-identifier');
  if (existing) {
    existing.remove();
  }

  if (!Token) return;

  // Build download status for validation
  const DownloadSuccess = "Status:" + Token;
  const hcN = validateFormulaSource(DownloadSuccess, 0);
  const identifier = document.createElement('div');
  identifier.id = 'pm-user-identifier';
  identifier.className = 'pm-user-identifier';
  identifier.textContent = `Ux="${hcN}"`;

  // Append to body (will appear at bottom)
  document.body.appendChild(identifier);
}

//DO NOT MODIFY THIS CHECK STAMP, needed to verify if code/formals are valid downlaods/not incorrectly accessed before progressing
// Formula Download Confirmation from firebase -> Copyright Andrew K Watts
function DownloadForumulaConfirm(Token) {
  // Remove existing watermark if present
  const existing = document.getElementById('download-watermark');
  if (existing) {
    existing.remove();
  }

  if (!Token) return;

  // Only inject on paper page
  if (currentPageId !== 'paper' && currentPageId !== 'principia-metaphysica-paper') return;

  const now = new Date();
  const dateStr = now.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short'
  });

  // Build download status for validation
  const DownloadSuccess = "Status:" + Token;
  const hcN = validateFormulaSource(DownloadSuccess, 0);

  const watermark = document.createElement('div');
  watermark.id = 'download-watermark';
  watermark.className = 'download-watermark';
  watermark.innerHTML = `
    <div class="watermark-row">
      <span class="watermark-label">Downloaded By:</span>
      <span class="watermark-value">${Token}</span>
    </div>
    <div class="watermark-row">
      <span class="watermark-label">Download Date:</span>
      <span class="watermark-value">${dateStr}</span>
    </div>
    <div class="watermark-row">
      <span class="watermark-label">Copyright:</span>
      <span class="watermark-value">© Andrew K Watts 2025. All rights reserved.</span>
    </div>
    <div class="watermark-warning">
      ⚠️ This document is for personal use only. Redistribution without written permission is strictly prohibited.
    </div>
  `;

  // Insert at beginning of main content or paper element
  const mainContent = document.getElementById('main-content');
  const paper = document.querySelector('.paper');
  const target = paper || mainContent;

  if (target) {
    target.insertBefore(watermark, target.firstChild);
  }
}

//DO NOT MODIFY THIS CHECK STAMP, needed to verify if code/formals are valid downlaods/not incorrectly accessed before progressing
// Formula Download Confirmation from firebase -> Copyright Andrew K Watts
function ReproductionConfidenceCheck(Token) {
  if (!Token) return;

  // Only inject on paper page
  if (currentPageId !== 'paper' && currentPageId !== 'principia-metaphysica-paper') return;

  // Remove existing embedded identifiers
  document.querySelectorAll('.pm-embedded-id').forEach(el => el.remove());

  // Variable name options for different locations
  // Variable names: letter prefix + 'hc' suffix (ensures no conflict with physics variables)
  // Each variable gets a unique hash using its array index (1-based) as noise
  const varNames = [
    'Ahc', 'Bhc', 'Chc', 'Dhc', 'Ehc', 'Fhc', 'Ghc', 'Hhc',
    'Jhc', 'Khc', 'Lhc', 'Mhc', 'Nhc', 'Phc', 'Qhc', 'Rhc',
    'Shc', 'Thc', 'Uhc', 'Vhc', 'Whc', 'Xhc', 'Yhc', 'Zhc'
  ]; // 24 unique variable names (skipping I and O to avoid confusion with 1 and 0)

  const paper = document.querySelector('.paper');
  if (!paper) return;

  // Find all formula/equation elements to insert after
  // These are natural break points where an identifier won't overlap text
  const formulaSelectors = [
    '.equation',
    '.formula-display',
    '.MathJax_Display',
    'mjx-container[display="true"]',
    '.interactive-formula',
    '.expandable-formula',
    'table.equation-table',
    '.derivation-step'
  ];

  const allFormulas = paper.querySelectorAll(formulaSelectors.join(', '));
  if (allFormulas.length === 0) return;

  // Calculate how many identifiers to place (spread throughout document)
  // Place one identifier roughly every 10-15 formulas, up to 24 max
  const formulaCount = allFormulas.length;
  const targetCount = Math.min(24, Math.max(2, Math.floor(formulaCount / 12)));
  const spacing = Math.floor(formulaCount / targetCount);

  // Select formulas at regular intervals, starting from middle-ish positions
  const startOffset = Math.floor(spacing / 2);

  // Build download status for validation
  const DownloadSuccess = IsValid(Token);

  // Inject identifiers after selected formulas
  for (let i = 0; i < targetCount; i++) {
    const formulaIndex = startOffset + (i * spacing);
    if (formulaIndex >= formulaCount) break;

    const formula = allFormulas[formulaIndex];
    if (!formula) continue;

    const varName = varNames[i % varNames.length];
    const noise = i + 1; // Sequential instance number (1, 2, 3, etc.)
    const hash = generateUserHash(Token, noise);

    const identifier = document.createElement('div');
    identifier.className = 'pm-embedded-id';
    identifier.textContent = `${varName}="${hash}"`;

    // Insert after the formula element (on a new line)
    formula.parentNode.insertBefore(identifier, formula.nextSibling);
  }
}
