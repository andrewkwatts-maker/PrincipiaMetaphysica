/**
 * Principia Metaphysica - Centralized Header Component
 *
 * Injects a consistent header across all pages: site title, navigation,
 * research-status notice, and the mobile menu. (The global Normal/EML
 * math switcher and Speculation toggle were removed 2026-08-25 in favour
 * of per-formula toggles and collapsed speculation panels.)
 *
 * Usage:
 *   import { injectHeader } from './js/pm-header.js';
 *   injectHeader('sections', { breadcrumbs: [{ label: 'Paper Home', href: 'index.html' }] });
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

// (The lazy math-mode.js loader that lived here was removed 2026-08-25
// along with the global switchers it served. Per-card toggles are
// self-contained in js/pm-math-toggle.js; the speculation panels are
// plain <details> elements needing no module.)

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
  { href: 'falsification.html', label: 'Falsification', id: 'falsification' },
  { href: 'appendices.html', label: 'Appendices', id: 'appendices' },
  { href: 'philosophical-implications.html', label: 'Philosophy', id: 'philosophical-implications' },
  { href: 'consciousness-speculative.html', label: 'Consciousness', id: 'consciousness-speculative' },
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
      <div class="header-top-row">
        <a href="${homeHref}" class="site-title">Principia Metaphysica</a>
        <div class="header-controls">
          <!-- The global Normal/EML pill switcher and the Speculation toggle
               were removed 2026-08-25. Math notation is chosen per formula
               card (js/pm-math-toggle.js, defaulting to normal), and
               speculative content lives in coloured details.speculation-block
               panels that are collapsed by default and expanded individually.
               Global overrides duplicated both and confused the defaults. -->
          <button class="mobile-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
      <nav class="main-nav-row" role="navigation" aria-label="Main navigation">
        <ul role="list">
          ${navItems}
        </ul>
      </nav>
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

    // Inject research-status notice at the top of main content (v2.2.0 honesty
    // polish — every sub-page must carry the not-peer-reviewed disclaimer).
    const mainContent = document.querySelector('main') ||
                       document.querySelector('.app-main') ||
                       document.querySelector('.content-wrapper') ||
                       document.querySelector('#main-content');
    if (mainContent && !mainContent.querySelector('.pm-research-notice')) {
      mainContent.insertAdjacentHTML('afterbegin',
        '<div class="pm-research-notice" role="note" aria-label="Research status" ' +
        'style="max-width:900px;margin:1rem auto 2rem;padding:1.25rem 1.5rem;' +
        'background:rgba(255,170,46,0.10);border:2px solid rgba(255,170,46,0.55);' +
        'border-radius:12px;color:var(--text-primary);text-align:left;">' +
        '<p style="margin:0;font-weight:700;color:#ffb554;font-size:1.05rem;' +
        'text-transform:uppercase;letter-spacing:0.06em;">&#9888; Research status</p>' +
        '<p style="margin:0.5rem 0 0;line-height:1.55;color:var(--text-primary);">' +
        '<strong>Principia Metaphysica is a speculative theoretical model.</strong> ' +
        'It has <strong>not</strong> been peer-reviewed and is <strong>not</strong> ' +
        'scientifically validated. All derivations, predictions, and “closures” ' +
        'documented on this site are candidate proposals awaiting experimental ' +
        'confirmation and independent expert review. The framework is intended ' +
        'for exploration and research purposes only; no claim on this site ' +
        'represents established scientific fact.</p></div>'
      );
    }

    // Breadcrumbs go ABOVE the notice: this is a second 'afterbegin' on the
    // same element, so it lands on top of what was just inserted. That is the
    // wanted result -- a thin nav strip above the banner is ordinary page
    // furniture and does not bury it -- but it is the opposite of what the
    // insertion order reads like, hence this note.
    if (breadcrumbHTML) {
      const bcTarget = mainContent ||
                       document.querySelector('#main-content');
      if (bcTarget) {
        bcTarget.insertAdjacentHTML('afterbegin', breadcrumbHTML);
      }
    }
  }

  // Setup mobile menu toggle
  setupMobileMenu();

  // Global math/speculation overrides retired 2026-08-25 (see the header
  // template comment). Clear any persisted global speculation override so
  // returning visitors get the collapsed-by-default panels too, instead of
  // a state they can no longer change now that the button is gone.
  try {
    localStorage.removeItem('pm-speculation');
  } catch (e) { /* storage unavailable (private mode) — default is correct */ }
  document.documentElement.removeAttribute('data-speculation');
  document.documentElement.removeAttribute('data-math-mode');

  console.log(`[PM Header] Injected header for page: ${activePageId}`);
}

/**
 * Setup mobile menu toggle functionality
 */
function setupMobileMenu() {
  const menuBtn = document.querySelector('.pm-header .mobile-menu-btn');
  const nav = document.querySelector('.pm-header .main-nav-row');

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
    // Note: Don't set aria-hidden on nav initially - it's always visible on desktop
    // Only set aria-hidden when menu is actually closed on mobile
    menuBtn.setAttribute('aria-expanded', 'false');
    // Check if we're on mobile before setting aria-hidden
    if (window.matchMedia('(max-width: 768px)').matches) {
      nav.setAttribute('aria-hidden', 'true');
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
