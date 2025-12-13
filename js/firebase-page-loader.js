/**
 * Firebase Page Loader
 *
 * Loads page content and PM values from Firebase Firestore.
 * Pages should call initPageFromFirebase(pageId) after authentication.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { getFirestore, doc, getDoc, collection, getDocs } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-firestore.js";

// Session cache
const cache = {
  theoryConstants: null,
  pageContent: {},
  cacheTime: null,
  CACHE_TTL: 5 * 60 * 1000 // 5 minutes
};

/**
 * Load theory constants from Firestore
 * Uses session cache to avoid repeated calls
 * @returns {Promise<Object>} Theory constants object
 */
export async function loadTheoryConstants() {
  // Check cache
  if (cache.theoryConstants && cache.cacheTime && (Date.now() - cache.cacheTime < cache.CACHE_TTL)) {
    console.log('[Firebase Page Loader] Using cached theory constants');
    return cache.theoryConstants;
  }

  // Load from Firestore
  console.log('[Firebase Page Loader] Loading theory constants from Firestore...');
  const db = getFirestore();
  const docRef = doc(db, 'theory_constants', 'current');

  try {
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      cache.theoryConstants = docSnap.data();
      cache.cacheTime = Date.now();
      console.log('[Firebase Page Loader] Theory constants loaded successfully');
      return cache.theoryConstants;
    }

    throw new Error('Theory constants not found in Firestore');
  } catch (error) {
    console.error('[Firebase Page Loader] Error loading theory constants:', error);
    throw error;
  }
}

/**
 * Load page content from Firestore
 * @param {string} pageId - Page identifier (e.g., 'index', 'fermion-sector')
 * @returns {Promise<Object|null>} Page content or null if not found
 */
export async function loadPageContent(pageId) {
  // Check cache
  if (cache.pageContent[pageId] && cache.cacheTime && (Date.now() - cache.cacheTime < cache.CACHE_TTL)) {
    console.log(`[Firebase Page Loader] Using cached page content for ${pageId}`);
    return cache.pageContent[pageId];
  }

  // Load from Firestore
  console.log(`[Firebase Page Loader] Loading page content for ${pageId}...`);
  const db = getFirestore();
  const docRef = doc(db, 'pages', pageId);

  try {
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      cache.pageContent[pageId] = docSnap.data();
      console.log(`[Firebase Page Loader] Page content loaded for ${pageId}`);
      return cache.pageContent[pageId];
    } else {
      console.log(`[Firebase Page Loader] No page content found for ${pageId}`);
      return null;
    }
  } catch (error) {
    console.error(`[Firebase Page Loader] Error loading page content for ${pageId}:`, error);
    return null;
  }
}

/**
 * Populate all PM values on the page
 * Finds all elements with class 'pm-value' and populates them
 * @param {Object} pmData - PM theory constants object
 * @returns {number} Number of elements populated
 */
export function populatePMValues(pmData) {
  if (!pmData) {
    console.warn('[Firebase Page Loader] No PM data provided to populatePMValues');
    return 0;
  }

  const pmElements = document.querySelectorAll('.pm-value');
  let populatedCount = 0;

  pmElements.forEach(el => {
    try {
      const category = el.getAttribute('data-category');
      const param = el.getAttribute('data-param');

      if (category && param) {
        // Navigate nested path (e.g., 'v12_7_pure_geometric.vev_pure.v_GeV')
        const value = getNestedValue(pmData, category, param);

        if (value !== undefined && value !== null) {
          el.textContent = formatValue(value);
          el.setAttribute('data-loaded', 'true');
          populatedCount++;
        } else {
          console.warn(`[Firebase Page Loader] Value not found for ${category}.${param}`);
        }
      } else {
        console.warn('[Firebase Page Loader] Missing data-category or data-param on element:', el);
      }
    } catch (error) {
      console.error('[Firebase Page Loader] Error populating element:', el, error);
    }
  });

  console.log(`[Firebase Page Loader] Populated ${populatedCount} PM values`);
  return populatedCount;
}

/**
 * Helper to get nested values
 * Supports paths like 'vev_pure.v_GeV' within a category
 * @param {Object} obj - PM data object
 * @param {string} category - Top-level category
 * @param {string} param - Parameter path (may be nested with dots)
 * @returns {*} Value or undefined
 */
function getNestedValue(obj, category, param) {
  const categoryObj = obj[category];
  if (!categoryObj) {
    console.warn(`[Firebase Page Loader] Category "${category}" not found`);
    return undefined;
  }

  // Handle nested paths like 'vev_pure.v_GeV'
  const value = param.split('.').reduce((acc, part) => {
    if (acc === null || acc === undefined) return undefined;
    return acc[part];
  }, categoryObj);

  // If we found an object with a 'value' property, extract that
  if (value && typeof value === 'object' && value.value !== undefined) {
    return value.value;
  }

  return value;
}

/**
 * Helper to format values
 * @param {*} val - Value to format
 * @returns {string} Formatted value
 */
function formatValue(val) {
  if (typeof val === 'number') {
    // Use scientific notation for very large or very small numbers
    if (Math.abs(val) >= 1e6 || (Math.abs(val) < 0.01 && val !== 0)) {
      return val.toExponential(4);
    }
    return val.toPrecision(6);
  }
  return String(val);
}

/**
 * Initialize page from Firebase
 * Call this after authentication succeeds
 * @param {string} pageId - Page identifier (e.g., 'index', 'fermion-sector')
 * @returns {Promise<Object>} PM data object
 */
export async function initPageFromFirebase(pageId) {
  console.log(`[Firebase Page Loader] Initializing page: ${pageId}`);

  try {
    // Load theory constants
    const pmData = await loadTheoryConstants();

    // Load page content (optional - may not exist for all pages)
    const pageContent = await loadPageContent(pageId);

    // Populate PM values on the page
    populatePMValues(pmData);

    // Make PM data available globally
    window.PM = pmData;

    // Make page content available if it exists
    if (pageContent) {
      window.PageContent = pageContent;
    }

    // Dispatch event for other scripts to hook into
    window.dispatchEvent(new CustomEvent('pm-data-ready', {
      detail: {
        pmData,
        pageContent,
        pageId
      }
    }));

    console.log('[Firebase Page Loader] Page initialized with PM data');
    return pmData;
  } catch (error) {
    console.error('[Firebase Page Loader] Error initializing page:', error);

    // Dispatch error event
    window.dispatchEvent(new CustomEvent('pm-data-error', {
      detail: {
        error: error.message,
        pageId
      }
    }));

    throw error;
  }
}

/**
 * Clear cache (useful for forcing refresh)
 */
export function clearCache() {
  cache.theoryConstants = null;
  cache.pageContent = {};
  cache.cacheTime = null;
  console.log('[Firebase Page Loader] Cache cleared');
}

/**
 * Refresh page data (clears cache and reloads)
 * @param {string} pageId - Page identifier
 * @returns {Promise<Object>} PM data object
 */
export async function refreshPageData(pageId) {
  console.log(`[Firebase Page Loader] Refreshing data for ${pageId}...`);
  clearCache();
  return await initPageFromFirebase(pageId);
}

/**
 * Get cache status for debugging
 * @returns {Object} Cache status information
 */
export function getCacheStatus() {
  return {
    hasTheoryConstants: !!cache.theoryConstants,
    pageContentCount: Object.keys(cache.pageContent).length,
    cacheAge: cache.cacheTime ? Date.now() - cache.cacheTime : null,
    ttl: cache.CACHE_TTL
  };
}
