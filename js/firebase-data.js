/**
 * Firebase Firestore Data Module for Principia Metaphysica
 *
 * Loads theory constants, formulas, and page content from Firestore.
 * Provides caching and fallback to static files.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { db } from './firebase-config.js';
import {
  doc,
  getDoc,
  collection,
  getDocs,
  query,
  orderBy
} from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-firestore.js';

// Cache for loaded data
const dataCache = {
  theoryConstants: null,
  formulas: null,
  formulaDatabase: null,
  pages: {},
  appendices: null,
  lastUpdated: null
};

// Cache TTL in milliseconds (5 minutes)
const CACHE_TTL = 5 * 60 * 1000;

/**
 * Load theory constants (PM object)
 * Tries static JSON files FIRST (faster, no auth required), then falls back to Firestore
 * @returns {Promise<Object>} PM constants object
 */
export async function loadTheoryConstants() {
  // Check cache
  if (dataCache.theoryConstants && isCacheValid()) {
    return dataCache.theoryConstants;
  }

  // Strategy 1: Try static JSON files first (faster, no auth needed)
  const staticResult = await loadStaticTheoryConstants();
  if (staticResult && Object.keys(staticResult).length > 0) {
    return staticResult;
  }

  // Strategy 2: Fall back to Firestore only if static files failed
  try {
    console.log('[PM Data] Static files unavailable, trying Firestore...');
    const docRef = doc(db, 'theory_constants', 'current');
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      const data = docSnap.data();
      dataCache.theoryConstants = data;
      dataCache.lastUpdated = Date.now();
      console.log('[PM Data] Theory constants loaded from Firestore');
      window.PM = buildPMObject(data);
      return window.PM;
    }
  } catch (error) {
    // Silently fail - static files are the primary source
  }

  console.warn('[PM Data] No data sources available');
  return {};
}

/**
 * Build the PM object with helper functions from Firestore data
 * @param {Object} data - Raw data from Firestore
 * @returns {Object} Complete PM object with helpers
 */
function buildPMObject(data) {
  const PM = { ...data };

  // Add format helpers
  PM.format = {
    scientific: (value, decimals = 2) => value.toExponential(decimals),
    fixed: (value, decimals = 2) => value.toFixed(decimals),
    percent: (value) => (value * 100).toFixed(1) + '%',
    sigma: (value) => value.toFixed(2) + 'σ',
    eV: (value) => value.toFixed(5) + ' eV',
    GeV: (value) => value.toFixed(3) + ' GeV',
    TeV: (value) => value.toFixed(2) + ' TeV',
    years: (value) => value.toExponential(2) + ' years'
  };

  // Version accessors
  PM.getVersion = () => PM.meta?.version || 'unknown';
  PM.getTransparency = () => PM.v9_transparency;
  PM.getBRSTProof = () => PM.v9_brst_proof;
  PM.getGeometricDerivations = () => PM.v10_geometric_derivations;
  PM.getNeutrinoMasses = () => PM.v10_1_neutrino_masses;
  PM.getAllFermions = () => PM.v10_2_all_fermions;
  PM.getFinalObservables = () => PM.v11_final_observables;
  PM.getFinalValues = () => PM.v12_final_values;

  // Set version-agnostic alias
  PM.pure_geometric = PM.v12_7_pure_geometric;

  return PM;
}

/**
 * Load formulas - tries static JSON files first, falls back to Firestore
 * @returns {Promise<Array>} Array of formula objects
 */
export async function loadFormulas() {
  if (dataCache.formulas && isCacheValid()) {
    return dataCache.formulas;
  }

  // Strategy 1: Try static JSON files first
  const staticFormulas = await loadStaticFormulas();
  if (staticFormulas && staticFormulas.length > 0) {
    dataCache.formulas = staticFormulas;
    return staticFormulas;
  }

  // Strategy 2: Fall back to Firestore
  try {
    const formulasRef = collection(db, 'formulas');
    const q = query(formulasRef, orderBy('category'));
    const snapshot = await getDocs(q);

    const formulas = [];
    snapshot.forEach(doc => {
      formulas.push({ id: doc.id, ...doc.data() });
    });

    if (formulas.length > 0) {
      dataCache.formulas = formulas;
      console.log(`[PM Data] Loaded ${formulas.length} formulas from Firestore`);
    }
    return formulas;
  } catch (error) {
    // Silently fail - static files are the primary source
    return [];
  }
}

/**
 * Load formula database (tooltip metadata) - tries static files first
 * @returns {Promise<Object>} Formula database object
 */
export async function loadFormulaDatabase() {
  if (dataCache.formulaDatabase && isCacheValid()) {
    return dataCache.formulaDatabase;
  }

  // Strategy 1: Try static JSON files first (formulas.json contains the database)
  const staticDb = await loadStaticFormulaDatabase();
  if (staticDb && Object.keys(staticDb).length > 0) {
    dataCache.formulaDatabase = staticDb;
    window.FORMULA_DATABASE = staticDb;
    return staticDb;
  }

  // Strategy 2: Fall back to Firestore
  try {
    const dbRef = collection(db, 'formula_database');
    const snapshot = await getDocs(dbRef);

    const database = {};
    snapshot.forEach(doc => {
      database[doc.id] = doc.data();
    });

    if (Object.keys(database).length > 0) {
      dataCache.formulaDatabase = database;
      window.FORMULA_DATABASE = database;
      console.log(`[PM Data] Loaded ${Object.keys(database).length} formula entries from Firestore`);
    }
    return database;
  } catch (error) {
    // Silently fail - static files are the primary source
    return {};
  }
}

/**
 * Load page-specific content from Firestore
 * @param {string} pageId - The page identifier (e.g., 'index', 'fermion-sector')
 * @returns {Promise<Object|null>} Page content object or null
 */
export async function loadPageContent(pageId) {
  if (dataCache.pages[pageId] && isCacheValid()) {
    console.log(`[PM Data] Returning cached content for ${pageId}`);
    return dataCache.pages[pageId];
  }

  try {
    console.log(`[PM Data] Loading page content for ${pageId}...`);
    const docRef = doc(db, 'pages', pageId);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      const content = docSnap.data();
      dataCache.pages[pageId] = content;
      console.log(`[PM Data] Page content loaded for ${pageId}`);
      return content;
    } else {
      console.log(`[PM Data] No Firestore content for ${pageId}, using static HTML`);
      return null;
    }
  } catch (error) {
    console.error(`[PM Data] Error loading page ${pageId}:`, error);
    return null;
  }
}

/**
 * Load all appendices for the paper
 * @returns {Promise<Array>} Array of appendix objects sorted by order
 */
export async function loadAppendices() {
  if (dataCache.appendices && isCacheValid()) {
    console.log('[PM Data] Returning cached appendices');
    return dataCache.appendices;
  }

  try {
    console.log('[PM Data] Loading appendices from Firestore...');
    const appendicesRef = collection(db, 'appendices');
    const q = query(appendicesRef, orderBy('order_index'));
    const snapshot = await getDocs(q);

    const appendices = [];
    snapshot.forEach(doc => {
      appendices.push({ id: doc.id, ...doc.data() });
    });

    dataCache.appendices = appendices;
    console.log(`[PM Data] Loaded ${appendices.length} appendices`);
    return appendices;
  } catch (error) {
    console.error('[PM Data] Error loading appendices:', error);
    return [];
  }
}

/**
 * Load all data required for a page
 * @param {string} pageId - The page identifier
 * @returns {Promise<Object>} Object with all loaded data
 */
export async function loadAllPageData(pageId) {
  console.log(`[PM Data] Loading all data for page: ${pageId}`);

  // Load in parallel for performance
  const [theoryConstants, formulas, formulaDatabase, pageContent] = await Promise.all([
    loadTheoryConstants(),
    loadFormulas(),
    loadFormulaDatabase(),
    loadPageContent(pageId)
  ]);

  return {
    PM: theoryConstants,
    formulas,
    formulaDatabase,
    pageContent,
    loaded: true,
    timestamp: Date.now()
  };
}

/**
 * Check if cache is still valid
 * @returns {boolean} True if cache is valid
 */
function isCacheValid() {
  if (!dataCache.lastUpdated) return false;
  return (Date.now() - dataCache.lastUpdated) < CACHE_TTL;
}

/**
 * Clear all cached data
 */
export function clearCache() {
  dataCache.theoryConstants = null;
  dataCache.formulas = null;
  dataCache.formulaDatabase = null;
  dataCache.pages = {};
  dataCache.appendices = null;
  dataCache.lastUpdated = null;
  console.log('[PM Data] Cache cleared');
}

/**
 * Get base path for AutoGenerated files based on current page location
 */
function getBasePath() {
  const path = window.location.pathname;
  return (path.includes('/Pages/') || path.includes('/foundations/') ||
          path.includes('/docs/') || path.includes('/diagrams/'))
    ? '../AutoGenerated/' : 'AutoGenerated/';
}

/**
 * Load theory constants from static JSON files
 * @returns {Promise<Object>} PM object from static JSON files
 */
async function loadStaticTheoryConstants() {
  const basePath = getBasePath();
  const paths = [
    '/AutoGenerated/theory_output.json',
    `${basePath}theory_output.json`,
    'AutoGenerated/theory_output.json',
    '../AutoGenerated/theory_output.json'
  ];

  for (const jsonPath of paths) {
    try {
      const response = await fetch(jsonPath);
      if (response.ok) {
        const data = await response.json();
        console.log(`[PM Data] Loaded theory constants from ${jsonPath}`);
        const PM = buildPMObject(data);
        window.PM = PM;
        dataCache.theoryConstants = PM;
        dataCache.lastUpdated = Date.now();
        return PM;
      }
    } catch (e) {
      continue;
    }
  }
  return {};
}

/**
 * Load formulas from static JSON files
 * @returns {Promise<Array>} Array of formula objects
 */
async function loadStaticFormulas() {
  const basePath = getBasePath();
  const paths = [
    '/AutoGenerated/formulas.json',
    `${basePath}formulas.json`,
    'AutoGenerated/formulas.json',
    '../AutoGenerated/formulas.json'
  ];

  for (const jsonPath of paths) {
    try {
      const response = await fetch(jsonPath);
      if (response.ok) {
        const data = await response.json();
        // formulas.json has structure { formulas: {...}, count: N }
        // Convert to array format expected by consumers
        if (data.formulas && typeof data.formulas === 'object') {
          const formulas = Object.entries(data.formulas).map(([id, formula]) => ({
            id,
            ...formula
          }));
          console.log(`[PM Data] Loaded ${formulas.length} formulas from ${jsonPath}`);
          return formulas;
        }
        // If it's already an array, return it
        if (Array.isArray(data)) {
          console.log(`[PM Data] Loaded ${data.length} formulas from ${jsonPath}`);
          return data;
        }
      }
    } catch (e) {
      continue;
    }
  }
  return [];
}

/**
 * Load formula database from static JSON files
 * @returns {Promise<Object>} Formula database object
 */
async function loadStaticFormulaDatabase() {
  const basePath = getBasePath();
  const paths = [
    '/AutoGenerated/formulas.json',
    `${basePath}formulas.json`,
    'AutoGenerated/formulas.json',
    '../AutoGenerated/formulas.json'
  ];

  for (const jsonPath of paths) {
    try {
      const response = await fetch(jsonPath);
      if (response.ok) {
        const data = await response.json();
        // formulas.json has structure { formulas: {...}, count: N }
        if (data.formulas && typeof data.formulas === 'object') {
          console.log(`[PM Data] Loaded formula database from ${jsonPath}`);
          return data.formulas;
        }
      }
    } catch (e) {
      continue;
    }
  }
  return {};
}

/**
 * Initialize the data module
 * Call this after authentication is confirmed
 */
export async function initializeData() {
  console.log('[PM Data] Initializing data module...');

  // Preload essential data
  await loadTheoryConstants();
  await loadFormulaDatabase();

  console.log('[PM Data] Data module initialized');
  return true;
}
