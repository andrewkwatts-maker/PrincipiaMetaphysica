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

  // Inject user identifier for content tracking
  injectUserIdentifier(user);

  // Inject download watermark for paper page
  injectDownloadWatermark(user);

  // Inject embedded identifiers in paper content
  injectEmbeddedIdentifiers(user);

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

      <div class="auth-tos">
        <p class="tos-notice">By logging in, you agree to the <a href="#terms-of-service" onclick="document.getElementById('tos-modal').style.display='flex'">Terms of Service</a></p>
        <p class="tos-summary">All content is protected. Redistribution prohibited.</p>
      </div>

      <footer class="auth-footer">
        <p>Copyright © Andrew K Watts 2025</p>
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

/**
 * Inject user identifier at bottom of page for content tracking
 * @param {Object} user - Firebase user object
 */
function injectUserIdentifier(user) {
  // Remove existing identifier if present
  const existing = document.getElementById('pm-user-identifier');
  if (existing) {
    existing.remove();
  }

  if (!user || !user.email) return;

  const hash = generateUserHash(user.email);
  const identifier = document.createElement('div');
  identifier.id = 'pm-user-identifier';
  identifier.className = 'pm-user-identifier';
  identifier.textContent = `Ux="${hash}"`;

  // Append to body (will appear at bottom)
  document.body.appendChild(identifier);
}

/**
 * Inject download watermark at top of paper page
 * @param {Object} user - Firebase user object
 */
function injectDownloadWatermark(user) {
  // Remove existing watermark if present
  const existing = document.getElementById('download-watermark');
  if (existing) {
    existing.remove();
  }

  if (!user || !user.email) return;

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

  const hash = generateUserHash(user.email);

  const watermark = document.createElement('div');
  watermark.id = 'download-watermark';
  watermark.className = 'download-watermark';
  watermark.innerHTML = `
    <div class="watermark-row">
      <span class="watermark-label">Downloaded By:</span>
      <span class="watermark-value">${user.email}</span>
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

/**
 * Inject embedded identifiers in middle of paper and appendices
 * Uses different variable names and noise for each location
 * @param {Object} user - Firebase user object
 */
function injectEmbeddedIdentifiers(user) {
  if (!user || !user.email) return;

  // Only inject on paper page
  if (currentPageId !== 'paper' && currentPageId !== 'principia-metaphysica-paper') return;

  // Remove existing embedded identifiers
  document.querySelectorAll('.pm-embedded-id').forEach(el => el.remove());

  // Variable name options for different locations
  const varNames = ['Vx', 'Wx', 'Qx', 'Rx', 'Tx', 'Zx'];

  // Find sections to inject into
  const paper = document.querySelector('.paper');
  if (!paper) return;

  // Get all major sections (h2 headers indicate section breaks)
  const sections = paper.querySelectorAll('section, .section, [id^="section-"], [id^="appendix-"]');

  // If no sections found, try to find content by other means
  let targetElements = [];
  if (sections.length > 0) {
    targetElements = Array.from(sections);
  } else {
    // Fallback: find all h2 elements and use their parent containers
    const h2s = paper.querySelectorAll('h2');
    targetElements = Array.from(h2s).map(h2 => h2.parentElement).filter(Boolean);
  }

  // Inject at strategic locations (middle of paper, middle of appendices)
  const totalSections = targetElements.length;
  if (totalSections === 0) return;

  // Calculate injection points: middle of main content and middle of appendices
  const midPoint = Math.floor(totalSections / 2);
  const appendixStart = targetElements.findIndex(el =>
    el.id?.toLowerCase().includes('appendix') ||
    el.querySelector('h2')?.textContent?.toLowerCase().includes('appendix')
  );

  const injectionPoints = [midPoint];
  if (appendixStart > 0 && appendixStart < totalSections) {
    const appendixMid = appendixStart + Math.floor((totalSections - appendixStart) / 2);
    if (appendixMid !== midPoint) {
      injectionPoints.push(appendixMid);
    }
  }

  // Inject at each point with different variable name and noise
  injectionPoints.forEach((index, i) => {
    if (index >= 0 && index < targetElements.length) {
      const section = targetElements[index];
      const varName = varNames[i % varNames.length];
      const noise = Date.now() + (i * 1000); // Different noise for each
      const hash = generateUserHash(user.email, noise);

      const identifier = document.createElement('div');
      identifier.className = 'pm-embedded-id';
      identifier.textContent = `${varName}="${hash}"`;

      // Insert at end of section
      section.appendChild(identifier);
    }
  });
}
