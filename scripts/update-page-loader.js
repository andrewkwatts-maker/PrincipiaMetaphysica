/**
 * Script to update firebase-page-loader.js with enhanced PM value population
 * Run with: node scripts/update-page-loader.js
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', 'js', 'firebase-page-loader.js');

const newContent = `/**
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
 */
export async function loadTheoryConstants() {
  if (cache.theoryConstants && cache.cacheTime && (Date.now() - cache.cacheTime < cache.CACHE_TTL)) {
    console.log('[Firebase Page Loader] Using cached theory constants');
    return cache.theoryConstants;
  }

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
 */
export async function loadPageContent(pageId) {
  if (cache.pageContent[pageId] && cache.cacheTime && (Date.now() - cache.cacheTime < cache.CACHE_TTL)) {
    return cache.pageContent[pageId];
  }

  console.log('[Firebase Page Loader] Loading page content for ' + pageId + '...');
  const db = getFirestore();
  const docRef = doc(db, 'pages', pageId);

  try {
    const docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      cache.pageContent[pageId] = docSnap.data();
      return cache.pageContent[pageId];
    } else {
      return null;
    }
  } catch (error) {
    console.error('[Firebase Page Loader] Error loading page content:', error);
    return null;
  }
}

/**
 * Populate all PM values on the page
 * Supports: data-category + data-param (legacy) or data-pm-value (full path)
 * Also supports data-format for formatting (e.g., "fixed:4", "scientific:2")
 */
export function populatePMValues(pmData) {
  if (!pmData) {
    console.warn('[Firebase Page Loader] No PM data provided');
    return 0;
  }

  const pmElements = document.querySelectorAll('.pm-value');
  let populatedCount = 0;
  let errorCount = 0;

  pmElements.forEach(el => {
    try {
      let value = null;
      let valuePath = '';

      // Check for data-pm-value (full path format)
      const pmValuePath = el.getAttribute('data-pm-value');
      if (pmValuePath) {
        valuePath = pmValuePath;
        value = getValueByPath(pmData, pmValuePath);
      } else {
        // Fallback to data-category + data-param format
        const category = el.getAttribute('data-category');
        const param = el.getAttribute('data-param');

        if (category && param) {
          valuePath = category + '.' + param;
          value = getNestedValue(pmData, category, param);
        }
      }

      if (value !== undefined && value !== null) {
        const format = el.getAttribute('data-format');
        el.textContent = formatValue(value, format);
        el.setAttribute('data-loaded', 'true');
        el.setAttribute('data-raw-value', value);
        populatedCount++;
      } else if (valuePath) {
        console.warn('[Firebase Page Loader] Value not found for path: ' + valuePath);
        el.setAttribute('data-error', 'not-found');
        errorCount++;
      }
    } catch (error) {
      console.error('[Firebase Page Loader] Error populating element:', el, error);
      el.setAttribute('data-error', error.message);
      errorCount++;
    }
  });

  console.log('[Firebase Page Loader] Populated ' + populatedCount + ' PM values (' + errorCount + ' errors)');
  return populatedCount;
}

/**
 * Get value by full path (e.g., "v12_6_geometric_derivations.vev_pneuma.v_EW")
 */
function getValueByPath(obj, path) {
  const parts = path.split('.');
  let current = obj;

  for (const part of parts) {
    if (current === null || current === undefined) {
      return undefined;
    }
    current = current[part];
  }

  if (current && typeof current === 'object' && current.value !== undefined) {
    return current.value;
  }

  return current;
}

/**
 * Helper to get nested values within a category
 */
function getNestedValue(obj, category, param) {
  const categoryObj = obj[category];
  if (!categoryObj) {
    console.warn('[Firebase Page Loader] Category "' + category + '" not found');
    return undefined;
  }

  const value = param.split('.').reduce((acc, part) => {
    if (acc === null || acc === undefined) return undefined;
    return acc[part];
  }, categoryObj);

  if (value && typeof value === 'object' && value.value !== undefined) {
    return value.value;
  }

  return value;
}

/**
 * Helper to format values with optional format specification
 */
function formatValue(val, format) {
  if (typeof val !== 'number') {
    return String(val);
  }

  if (format) {
    const [type, precision] = format.split(':');
    const p = precision ? parseInt(precision, 10) : 4;

    switch (type) {
      case 'fixed':
        return val.toFixed(p);
      case 'scientific':
        return val.toExponential(p);
      case 'percent':
        return (val * 100).toFixed(p) + '%';
      case 'sigma':
        return val.toFixed(p) + '\\u03C3';
      default:
        break;
    }
  }

  if (Math.abs(val) >= 1e6 || (Math.abs(val) < 0.01 && val !== 0)) {
    return val.toExponential(4);
  }
  return val.toPrecision(6);
}

/**
 * Initialize page from Firebase
 */
export async function initPageFromFirebase(pageId) {
  console.log('[Firebase Page Loader] Initializing page: ' + pageId);

  try {
    const pmData = await loadTheoryConstants();
    const pageContent = await loadPageContent(pageId);
    populatePMValues(pmData);

    window.PM = pmData;
    if (pageContent) {
      window.PageContent = pageContent;
    }

    window.dispatchEvent(new CustomEvent('pm-data-ready', {
      detail: { pmData, pageContent, pageId }
    }));

    console.log('[Firebase Page Loader] Page initialized with PM data');
    return pmData;
  } catch (error) {
    console.error('[Firebase Page Loader] Error initializing page:', error);
    window.dispatchEvent(new CustomEvent('pm-data-error', {
      detail: { error: error.message, pageId }
    }));
    throw error;
  }
}

/**
 * Clear cache
 */
export function clearCache() {
  cache.theoryConstants = null;
  cache.pageContent = {};
  cache.cacheTime = null;
  console.log('[Firebase Page Loader] Cache cleared');
}

/**
 * Refresh page data
 */
export async function refreshPageData(pageId) {
  console.log('[Firebase Page Loader] Refreshing data for ' + pageId + '...');
  clearCache();
  return await initPageFromFirebase(pageId);
}

/**
 * Get cache status
 */
export function getCacheStatus() {
  return {
    hasTheoryConstants: !!cache.theoryConstants,
    pageContentCount: Object.keys(cache.pageContent).length,
    cacheAge: cache.cacheTime ? Date.now() - cache.cacheTime : null,
    ttl: cache.CACHE_TTL
  };
}
`;

fs.writeFileSync(filePath, newContent);
console.log('Updated firebase-page-loader.js with enhanced PM value population');
console.log('New file size:', fs.statSync(filePath).size, 'bytes');
