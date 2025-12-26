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
  // If in subdirectory (e.g., foundations/, sections/), add ../
  if (path.includes('/foundations/') || path.includes('/sections/')) {
    return '../';
  }
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

  const navItems = NAV_LINKS.map(link => {
    const isActive = link.id === activePageId;
    const activeClass = isActive ? ' class="active"' : '';
    const href = basePath + link.href;
    return `<li><a href="${href}"${activeClass}>${link.label}</a></li>`;
  }).join('\n            ');

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
