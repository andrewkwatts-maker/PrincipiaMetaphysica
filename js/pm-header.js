/**
 * Principia Metaphysica - Centralized Header Component
 *
 * Injects a consistent header across all pages.
 * Single source of truth for navigation and user controls.
 *
 * Usage:
 *   import { injectHeader } from './js/pm-header.js';
 *   injectHeader('sections', { breadcrumbs: [{ label: 'Paper Home', href: 'index.html' }] });
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

/**
 * Navigation links - single source of truth
 * All pages are now in the /Pages/ folder
 *
 * To add a new navigation item, simply add an object to this array:
 * { href: 'new-page.html', label: 'New Page', id: 'new-page' }
 *
 * Properties:
 * - href: The URL (relative to /Pages/ folder, or absolute with isRoot)
 * - label: Display text for the link
 * - id: Unique identifier for highlighting active page
 * - isRoot: (optional) If true, the link points to root directory
 */
const NAV_LINKS = [
  { href: '../index.html', label: 'Home', id: 'home', isRoot: true },
  { href: 'beginners-guide.html', label: "Beginner's Guide", id: 'beginners-guide' },
  { href: 'sections.html', label: 'Sections', id: 'sections' },
  { href: 'foundations.html', label: 'Foundations', id: 'foundations' },
  { href: 'references.html', label: 'References', id: 'references' },
  { href: 'formulas.html', label: 'Formulas', id: 'formulas' },
  { href: 'parameters.html', label: 'Parameters', id: 'parameters' },
  { href: 'paper.html', label: 'Paper', id: 'paper' },
  { href: 'simulations.html', label: 'Simulations', id: 'simulations' },
  { href: 'certificates.html', label: 'Certificates', id: 'certificates' },
  { href: 'appendices.html', label: 'Appendices', id: 'appendices' },
  { href: 'philosophical-implications.html', label: 'Philosophy', id: 'philosophical-implications' },
  { href: 'visualization-index.html', label: 'Visualizations', id: 'visualization-index' },
  { href: 'faq.html', label: 'FAQ', id: 'faq' }
];

/**
 * Validate a navigation link object
 * @param {Object} link - Navigation link object to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateNavLink(link) {
  if (!link || typeof link !== 'object') {
    console.warn('[PM Header] Invalid nav link: not an object', link);
    return false;
  }
  if (!link.href || typeof link.href !== 'string') {
    console.warn('[PM Header] Invalid nav link: missing or invalid href', link);
    return false;
  }
  if (!link.label || typeof link.label !== 'string') {
    console.warn('[PM Header] Invalid nav link: missing or invalid label', link);
    return false;
  }
  if (!link.id || typeof link.id !== 'string') {
    console.warn('[PM Header] Invalid nav link: missing or invalid id', link);
    return false;
  }
  return true;
}

/**
 * Get the base path for resources (CSS, images) based on current page location
 * Resources are always at the root level
 */
function getBasePath() {
  const path = window.location.pathname;
  // If in Pages folder, go up one level to reach root resources
  if (path.includes('/Pages/')) {
    return '../';
  }
  // If in nested subdirectory, go up appropriately
  if (path.includes('/foundations/') || path.includes('/sections/')) {
    return '../';
  }
  // At root level
  return '';
}

/**
 * Ensure CSS is loaded
 */
function ensureCSS() {
  const cssId = 'pm-header-css';
  if (document.getElementById(cssId)) return;

  const basePath = getBasePath();
  const link = document.createElement('link');
  link.id = cssId;
  link.rel = 'stylesheet';
  link.href = `${basePath}css/pm-header.css`;
  document.head.appendChild(link);
}

/**
 * Create the header HTML
 * @param {string} activePageId - The ID of the current page to highlight
 */
function createHeaderHTML(activePageId = '') {
  const basePath = getBasePath();
  const path = window.location.pathname;
  const isInPages = path.includes('/Pages/');

  const navItems = NAV_LINKS.filter(validateNavLink).map(link => {
    const isActive = link.id === activePageId;
    const activeClass = isActive ? ' class="active"' : '';
    let href;
    if (link.isRoot) {
      // Home link - always goes to root index.html
      href = isInPages ? '../index.html' : 'index.html';
    } else {
      // Other links - in Pages folder
      href = isInPages ? link.href : 'Pages/' + link.href;
    }
    return `<li><a href="${href}"${activeClass}>${link.label}</a></li>`;
  }).join('\n            ');

  // Site title always links to root
  const homeHref = isInPages ? '../index.html' : 'index.html';

  return `
    <a href="#main-content" class="skip-to-content">Skip to main content</a>
    <header class="pm-header">
      <div class="header-content">
        <a href="${homeHref}" class="site-title">Principia Metaphysica</a>
        <nav class="main-nav" role="navigation" aria-label="Main navigation">
          <ul role="list">
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
        <button class="mobile-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </header>
  `;
}

/**
 * Create breadcrumb HTML
 * @param {Array} breadcrumbs - Array of {label, href} objects. Last item is current page (no href needed).
 * @param {string} currentLabel - Label for current page
 */
function createBreadcrumbHTML(breadcrumbs = [], currentLabel = '') {
  if (!breadcrumbs.length && !currentLabel) return '';

  const basePath = getBasePath();
  const items = [];

  breadcrumbs.forEach((crumb, index) => {
    if (crumb.href) {
      items.push(`<a href="${basePath}${crumb.href}">${crumb.label}</a>`);
    } else {
      items.push(`<span class="current">${crumb.label}</span>`);
    }
  });

  if (currentLabel) {
    items.push(`<span class="current">${currentLabel}</span>`);
  }

  const separator = '<span class="separator">/</span>';
  return `<div class="pm-breadcrumb">${items.join(separator)}</div>`;
}

/**
 * Inject header into page
 * @param {string} activePageId - The ID of the current page
 * @param {Object} options - Configuration options
 * @param {Array} options.breadcrumbs - Breadcrumb trail [{label, href}]
 * @param {string} options.currentLabel - Current page label for breadcrumbs
 * @param {string} options.targetSelector - CSS selector for where to inject
 */
export function injectHeader(activePageId = '', options = {}) {
  // Ensure CSS is loaded
  ensureCSS();

  // Check if header already exists
  if (document.querySelector('.pm-header')) {
    console.log('[PM Header] Header already exists, skipping injection');
    return;
  }

  const headerHTML = createHeaderHTML(activePageId);
  const breadcrumbHTML = createBreadcrumbHTML(options.breadcrumbs || [], options.currentLabel);

  // Remove any existing non-pm headers to avoid duplicates
  const existingHeaders = document.querySelectorAll('header:not(.pm-header), .app-header:not(.pm-header)');
  existingHeaders.forEach(h => {
    // Only remove if it looks like a nav header (has nav element or site title)
    if (h.querySelector('nav') || h.querySelector('.site-title') || h.querySelector('.header-content')) {
      h.style.display = 'none';
    }
  });

  // Find injection target
  let target;
  if (options.targetSelector) {
    target = document.querySelector(options.targetSelector);
  }

  if (!target) {
    // Try common targets
    target = document.querySelector('.app-container') ||
             document.getElementById('main-content') ||
             document.body;
  }

  // Inject header at start of target
  if (target) {
    target.insertAdjacentHTML('afterbegin', headerHTML);

    // If breadcrumbs, inject after header inside main content area
    if (breadcrumbHTML) {
      const mainContent = document.querySelector('.app-main') ||
                         document.querySelector('.content-wrapper') ||
                         document.querySelector('main') ||
                         document.querySelector('#main-content');
      if (mainContent) {
        mainContent.insertAdjacentHTML('afterbegin', breadcrumbHTML);
      }
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
  const menuBtn = document.querySelector('.pm-header .mobile-menu-btn');
  const nav = document.querySelector('.pm-header .main-nav');

  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('mobile-open');
      menuBtn.classList.toggle('active');

      // Update ARIA attributes for accessibility
      menuBtn.setAttribute('aria-expanded', isOpen);
      nav.setAttribute('aria-hidden', !isOpen);
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!menuBtn.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('mobile-open');
        menuBtn.classList.remove('active');
        menuBtn.setAttribute('aria-expanded', 'false');
        nav.setAttribute('aria-hidden', 'true');
      }
    });

    // Close menu on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('mobile-open')) {
        nav.classList.remove('mobile-open');
        menuBtn.classList.remove('active');
        menuBtn.setAttribute('aria-expanded', 'false');
        nav.setAttribute('aria-hidden', 'true');
        menuBtn.focus(); // Return focus to button
      }
    });

    // Initialize ARIA attributes
    menuBtn.setAttribute('aria-expanded', 'false');
    nav.setAttribute('aria-hidden', 'true');
  }
}

/**
 * Update user display in header (called by auth-guard)
 * @param {Object|null} user - Firebase user object or null
 */
export function updateHeaderUserDisplay(user) {
  const userAvatar = document.getElementById('user-avatar');
  const userEmail = document.getElementById('user-email');
  const userControls = document.querySelector('.pm-header .user-controls');
  const loginBtn = document.getElementById('header-login-btn');

  const basePath = getBasePath();
  if (user) {
    if (userAvatar) {
      userAvatar.src = user.photoURL || `${basePath}images/default-avatar.svg`;
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
      loginBtn.style.display = 'flex';
    }
  }
}

/**
 * Remove injected header (useful for cleanup)
 */
export function removeHeader() {
  const header = document.querySelector('.pm-header');
  if (header) {
    header.remove();
  }
  const breadcrumb = document.querySelector('.pm-breadcrumb');
  if (breadcrumb) {
    breadcrumb.remove();
  }
}

// Export nav links for use elsewhere
export { NAV_LINKS, getBasePath };
