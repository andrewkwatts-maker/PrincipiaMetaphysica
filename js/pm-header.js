/**
 * Principia Metaphysica - Centralized Header Component
 *
 * Injects a consistent header across all pages.
 * Single source of truth for navigation and user controls.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

/**
 * Navigation links - single source of truth
 */
const NAV_LINKS = [
  { href: 'index.html', label: 'Home', id: 'home' },
  { href: 'beginners-guide.html', label: "Beginner's Guide", id: 'beginners-guide' },
  { href: 'sections.html', label: 'Sections', id: 'sections' },
  { href: 'foundations/index.html', label: 'Foundations', id: 'foundations' },
  { href: 'references.html', label: 'References', id: 'references' },
  { href: 'formulas.html', label: 'Formulas', id: 'formulas' },
  { href: 'parameters.html', label: 'Parameters', id: 'parameters' },
  { href: 'principia-metaphysica-paper.html', label: 'Paper', id: 'paper' },
  { href: 'simulations.html', label: 'Simulations', id: 'simulations' }
];

/**
 * Get the base path for links based on current page location
 */
function getBasePath() {
  const path = window.location.pathname;
  // If in subdirectory (e.g., foundations/), add ../
  if (path.includes('/foundations/') || path.includes('/sections/')) {
    return '../';
  }
  return '';
}

/**
 * Create the header HTML
 * @param {string} activePageId - The ID of the current page to highlight
 */
function createHeaderHTML(activePageId = '') {
  const basePath = getBasePath();

  const navItems = NAV_LINKS.map(link => {
    const isActive = link.id === activePageId;
    const activeClass = isActive ? ' class="active"' : '';
    const href = basePath + link.href;
    return `<li><a href="${href}"${activeClass}>${link.label}</a></li>`;
  }).join('\n          ');

  return `
    <header class="pm-header">
      <div class="header-content">
        <a href="${basePath}index.html" class="site-title">Principia Metaphysica</a>
        <nav class="main-nav">
          <ul>
            ${navItems}
            <li class="user-controls-nav">
              <div class="user-controls" style="display: none;">
                <img id="user-avatar" src="${basePath}images/default-avatar.svg" alt="User" class="user-avatar">
                <span id="user-email" class="user-email"></span>
                <button id="logout-btn" class="logout-btn">Logout</button>
              </div>
              <button id="header-login-btn" class="header-login-btn" style="display: none;">
                <img src="${basePath}images/google-icon.svg" alt="G" class="google-icon-small">
                Login
              </button>
            </li>
          </ul>
        </nav>
        <button class="mobile-menu-btn" aria-label="Toggle menu">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </header>
  `;
}

/**
 * Inject header into page
 * @param {string} activePageId - The ID of the current page
 * @param {string} targetSelector - CSS selector for where to inject (default: start of body)
 */
export function injectHeader(activePageId = '', targetSelector = null) {
  const headerHTML = createHeaderHTML(activePageId);

  // Check if header already exists
  if (document.querySelector('.pm-header')) {
    console.log('[PM Header] Header already exists, skipping injection');
    return;
  }

  if (targetSelector) {
    const target = document.querySelector(targetSelector);
    if (target) {
      target.insertAdjacentHTML('afterbegin', headerHTML);
    }
  } else {
    // Insert at start of body or main-content
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.insertAdjacentHTML('afterbegin', headerHTML);
    } else {
      document.body.insertAdjacentHTML('afterbegin', headerHTML);
    }
  }

  // Setup mobile menu toggle
  setupMobileMenu();

  console.log(`[PM Header] Injected header for page: ${activePageId}`);
}

/**
 * Setup mobile menu toggle functionality
 */
function setupMobileMenu() {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const nav = document.querySelector('.main-nav');

  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      nav.classList.toggle('mobile-open');
      menuBtn.classList.toggle('active');
    });
  }
}

/**
 * Update user display in header (called by auth-guard)
 * @param {Object|null} user - Firebase user object or null
 */
export function updateHeaderUserDisplay(user) {
  const userAvatar = document.getElementById('user-avatar');
  const userEmail = document.getElementById('user-email');
  const logoutBtn = document.getElementById('logout-btn');
  const userControls = document.querySelector('.user-controls');
  const loginBtn = document.getElementById('header-login-btn');

  if (user) {
    if (userAvatar) {
      userAvatar.src = user.photoURL || 'images/default-avatar.svg';
      userAvatar.alt = user.displayName || 'User';
    }
    if (userEmail) {
      userEmail.textContent = user.email;
    }
    if (userControls) {
      userControls.style.display = 'flex';
    }
    if (loginBtn) {
      loginBtn.style.display = 'none';
    }
  } else {
    if (userControls) {
      userControls.style.display = 'none';
    }
    if (loginBtn) {
      loginBtn.style.display = 'block';
    }
  }
}

// Export nav links for use elsewhere
export { NAV_LINKS };
