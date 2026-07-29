/**
 * Firebase References Module for Principia Metaphysica
 *
 * Manages academic references across both the main paper and references page.
 * Loads reference data from Firestore and provides rendering utilities.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { db } from './firebase-config.js';
import {
  collection,
  getDocs,
  query,
  where,
  orderBy,
  doc,
  getDoc
} from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-firestore.js';

// Cache for loaded references
const referencesCache = {
  all: null,
  byId: new Map(),
  byCategory: new Map(),
  lastUpdated: null
};

// Cache TTL in milliseconds (10 minutes - references change rarely)
const CACHE_TTL = 10 * 60 * 1000;

/**
 * Reference Categories
 */
export const CATEGORIES = {
  FOUNDATIONAL_PHYSICS: 'foundational-physics',
  QUANTUM_FIELD_THEORY: 'quantum-field-theory',
  GEOMETRY_TOPOLOGY: 'geometry-topology',
  STRING_M_THEORY: 'string-m-theory',
  TCS_G2_CONSTRUCTIONS: 'tcs-g2-constructions',
  TWO_TIME_PHYSICS: 'two-time-physics',
  MODULI_STABILIZATION: 'moduli-stabilization',
  EXTRA_DIMENSIONS: 'extra-dimensions',
  GRAND_UNIFICATION: 'grand-unification',
  PHENOMENOLOGY_EXPERIMENT: 'phenomenology-experiment',
  THERMAL_TIME: 'thermal-time',
  COSMOLOGY: 'cosmology',
  NEUTRINOS: 'neutrinos'
};

/**
 * Reference Types
 */
export const TYPES = {
  EXPERIMENTAL: 'experimental',
  THEORETICAL: 'theoretical',
  REVIEW: 'review',
  TEXTBOOK: 'textbook',
  PAPER: 'paper'
};

/**
 * Load all references from Firestore
 * @returns {Promise<Array>} Array of reference objects
 */
export async function loadAllReferences() {
  // Check cache
  if (referencesCache.all && isCacheValid()) {
    console.log('[PM References] Returning cached references');
    return referencesCache.all;
  }

  try {
    console.log('[PM References] Loading references from Firestore...');
    const refsCollection = collection(db, 'references');
    const q = query(refsCollection, orderBy('category'), orderBy('year'));
    const snapshot = await getDocs(q);

    const references = [];
    snapshot.forEach(docSnap => {
      const ref = { id: docSnap.id, ...docSnap.data() };
      references.push(ref);
      referencesCache.byId.set(ref.id, ref);
    });

    referencesCache.all = references;
    referencesCache.lastUpdated = Date.now();

    // Build category index
    buildCategoryIndex(references);

    console.log(`[PM References] Loaded ${references.length} references`);
    return references;
  } catch (error) {
    console.error('[PM References] Error loading references:', error);
    return [];
  }
}

/**
 * Load a single reference by ID
 * @param {string} refId - The reference ID (e.g., 'einstein1915', 'joyce2000')
 * @returns {Promise<Object|null>} Reference object or null
 */
export async function loadReference(refId) {
  // Check cache first
  if (referencesCache.byId.has(refId)) {
    return referencesCache.byId.get(refId);
  }

  try {
    const docRef = doc(db, 'references', refId);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      const ref = { id: docSnap.id, ...docSnap.data() };
      referencesCache.byId.set(refId, ref);
      return ref;
    } else {
      console.warn(`[PM References] Reference ${refId} not found`);
      return null;
    }
  } catch (error) {
    console.error(`[PM References] Error loading reference ${refId}:`, error);
    return null;
  }
}

/**
 * Load references by category
 * @param {string} category - Category identifier
 * @returns {Promise<Array>} Array of references in category
 */
export async function loadReferencesByCategory(category) {
  // Check cache first
  if (referencesCache.byCategory.has(category) && isCacheValid()) {
    return referencesCache.byCategory.get(category);
  }

  try {
    const refsCollection = collection(db, 'references');
    const q = query(
      refsCollection,
      where('category', '==', category),
      orderBy('year')
    );
    const snapshot = await getDocs(q);

    const references = [];
    snapshot.forEach(docSnap => {
      const ref = { id: docSnap.id, ...docSnap.data() };
      references.push(ref);
      referencesCache.byId.set(ref.id, ref);
    });

    referencesCache.byCategory.set(category, references);
    return references;
  } catch (error) {
    console.error(`[PM References] Error loading category ${category}:`, error);
    return [];
  }
}

/**
 * Load references by citation key (for in-text citations)
 * Examples: "Einstein 1915", "Joyce 2000", "Acharya et al. 1998"
 * @param {string} citationKey - Citation key to look up
 * @returns {Promise<Object|null>} Reference object or null
 */
export async function loadReferenceByCitation(citationKey) {
  // First try to load all references if not cached
  if (!referencesCache.all) {
    await loadAllReferences();
  }

  // Search for matching citation key
  const ref = referencesCache.all?.find(r => r.citation_key === citationKey);
  return ref || null;
}

/**
 * Search references by text (author, title, keywords)
 * @param {string} searchText - Text to search for
 * @returns {Promise<Array>} Array of matching references
 */
export async function searchReferences(searchText) {
  // Load all references if not cached
  if (!referencesCache.all) {
    await loadAllReferences();
  }

  const searchLower = searchText.toLowerCase();
  return referencesCache.all.filter(ref => {
    return (
      ref.authors?.toLowerCase().includes(searchLower) ||
      ref.title?.toLowerCase().includes(searchLower) ||
      ref.tags?.some(tag => tag.toLowerCase().includes(searchLower)) ||
      ref.id?.toLowerCase().includes(searchLower)
    );
  });
}

/**
 * Build category index from references array
 * @param {Array} references - Array of reference objects
 */
function buildCategoryIndex(references) {
  referencesCache.byCategory.clear();
  references.forEach(ref => {
    if (!referencesCache.byCategory.has(ref.category)) {
      referencesCache.byCategory.set(ref.category, []);
    }
    referencesCache.byCategory.get(ref.category).push(ref);
  });
}

/**
 * Check if cache is still valid
 * @returns {boolean} True if cache is valid
 */
function isCacheValid() {
  if (!referencesCache.lastUpdated) return false;
  return (Date.now() - referencesCache.lastUpdated) < CACHE_TTL;
}

/**
 * Clear references cache
 */
export function clearReferencesCache() {
  referencesCache.all = null;
  referencesCache.byId.clear();
  referencesCache.byCategory.clear();
  referencesCache.lastUpdated = null;
  console.log('[PM References] Cache cleared');
}

/**
 * Render a reference in full citation format (for references.html)
 * @param {Object} ref - Reference object
 * @returns {HTMLElement} Rendered reference element
 */
export function renderFullReference(ref) {
  const div = document.createElement('div');
  div.className = 'ref-item';
  div.id = ref.id;

  // Title
  const titleDiv = document.createElement('div');
  titleDiv.className = 'ref-title';
  titleDiv.textContent = ref.title;
  div.appendChild(titleDiv);

  // Authors
  const authorsDiv = document.createElement('div');
  authorsDiv.className = 'ref-authors';
  authorsDiv.textContent = ref.authors;
  div.appendChild(authorsDiv);

  // Journal/Publication
  const journalDiv = document.createElement('div');
  journalDiv.className = 'ref-journal';
  journalDiv.textContent = ref.journal;
  div.appendChild(journalDiv);

  // Links (DOI, arXiv, etc.)
  if (ref.links && ref.links.length > 0) {
    const linksDiv = document.createElement('div');
    linksDiv.className = 'ref-links';

    ref.links.forEach(link => {
      const a = document.createElement('a');
      a.href = link.url;
      a.target = '_blank';
      a.textContent = `${link.label} →`;
      linksDiv.appendChild(a);
    });

    div.appendChild(linksDiv);
  }

  // Description/Note (if available)
  if (ref.description) {
    const descDiv = document.createElement('div');
    descDiv.style.cssText = 'margin-top: 0.5rem; padding: 0.5rem; background: rgba(139, 127, 255, 0.08); border-radius: 4px; font-size: 0.85rem; color: var(--text-secondary);';
    descDiv.textContent = ref.description;
    div.appendChild(descDiv);
  }

  // Tags
  if (ref.tags && ref.tags.length > 0) {
    ref.tags.forEach(tag => {
      const tagSpan = document.createElement('span');
      tagSpan.className = 'ref-tag';
      tagSpan.textContent = tag;
      div.appendChild(tagSpan);
    });
  }

  return div;
}

/**
 * Render an inline citation (for use in paper)
 * @param {Object} ref - Reference object
 * @param {Object} options - Rendering options
 * @returns {HTMLElement} Rendered citation element
 */
export function renderInlineCitation(ref, options = {}) {
  const span = document.createElement('span');
  span.className = 'inline-citation';

  // Format: [Author Year] with link to reference
  const citationText = ref.citation_key || `${ref.authors.split(',')[0]} ${ref.year}`;

  if (options.link !== false) {
    const a = document.createElement('a');
    a.href = `references.html#${ref.id}`;
    a.textContent = `[${citationText}]`;
    a.style.cssText = 'color: var(--accent-secondary); text-decoration: none;';
    a.title = ref.title;
    span.appendChild(a);
  } else {
    span.textContent = `[${citationText}]`;
  }

  return span;
}

/**
 * Render a category section for references.html
 * @param {string} category - Category identifier
 * @param {string} title - Category display title
 * @param {Array} references - Array of references in this category
 * @param {Object} options - Rendering options
 * @returns {HTMLElement} Rendered category section
 */
export function renderReferenceCategory(category, title, references, options = {}) {
  const section = document.createElement('section');
  section.className = 'ref-category';
  section.id = category;

  // Category title
  const h3 = document.createElement('h3');
  h3.textContent = title;
  section.appendChild(h3);

  // Optional category description
  if (options.description) {
    const desc = document.createElement('p');
    desc.style.cssText = 'font-size: 0.9rem; color: var(--text-muted); font-style: italic; margin-bottom: 1rem;';
    desc.textContent = options.description;
    section.appendChild(desc);
  }

  // Render each reference
  references.forEach(ref => {
    section.appendChild(renderFullReference(ref));
  });

  return section;
}

/**
 * Render all references grouped by category
 * @param {Array} references - Array of all references
 * @param {HTMLElement} container - Container element to render into
 */
export async function renderAllReferences(container) {
  if (!container) {
    console.error('[PM References] No container provided for rendering');
    return;
  }

  // Load references if not already loaded
  const refs = await loadAllReferences();

  // Group by category
  const categoryGroups = {};
  refs.forEach(ref => {
    if (!categoryGroups[ref.category]) {
      categoryGroups[ref.category] = [];
    }
    categoryGroups[ref.category].push(ref);
  });

  // Category metadata
  const categoryMeta = {
    'foundational-physics': { title: 'Foundational Physics', order: 1 },
    'quantum-field-theory': { title: 'Quantum Field Theory', order: 2 },
    'geometry-topology': { title: 'Geometry & Topology', order: 3 },
    'string-m-theory': { title: 'String Theory & M-Theory', order: 4 },
    'tcs-g2-constructions': { title: 'TCS G₂ Manifolds & Modern Constructions', order: 5 },
    'two-time-physics': { title: 'Two-Time Physics', order: 6 },
    'moduli-stabilization': { title: 'Moduli Stabilization', order: 7 },
    'extra-dimensions': { title: 'Extra Dimensions, Kaluza-Klein Theory & Warped Geometry', order: 8 },
    'grand-unification': { title: 'Grand Unified Theories (GUTs)', order: 9 },
    'phenomenology-experiment': { title: 'Phenomenology & Experiment', order: 10 },
    'thermal-time': { title: 'Thermal Time & Statistical Mechanics', order: 11 },
    'cosmology': { title: 'Cosmology & Dark Energy', order: 12 },
    'neutrinos': { title: 'Neutrino Physics', order: 13 }
  };

  // Sort categories by order
  const sortedCategories = Object.keys(categoryGroups).sort((a, b) => {
    const orderA = categoryMeta[a]?.order || 999;
    const orderB = categoryMeta[b]?.order || 999;
    return orderA - orderB;
  });

  // Render each category
  sortedCategories.forEach(category => {
    const meta = categoryMeta[category] || { title: category };
    const section = renderReferenceCategory(
      category,
      meta.title,
      categoryGroups[category],
      meta.options || {}
    );
    container.appendChild(section);
  });

  console.log(`[PM References] Rendered ${refs.length} references in ${sortedCategories.length} categories`);
}

/**
 * Get BibTeX for a reference
 * @param {Object} ref - Reference object
 * @returns {string} BibTeX formatted string
 */
export function getBibTeX(ref) {
  if (ref.bibtex) {
    return ref.bibtex;
  }

  // Generate basic BibTeX if not provided
  const type = ref.type === TYPES.TEXTBOOK ? 'book' : 'article';
  const key = ref.id;

  let bibtex = `@${type}{${key},\n`;
  bibtex += `  author = {${ref.authors}},\n`;
  bibtex += `  title = {${ref.title}},\n`;
  if (ref.journal) bibtex += `  journal = {${ref.journal}},\n`;
  if (ref.year) bibtex += `  year = {${ref.year}},\n`;
  if (ref.volume) bibtex += `  volume = {${ref.volume}},\n`;
  if (ref.pages) bibtex += `  pages = {${ref.pages}},\n`;
  if (ref.doi) bibtex += `  doi = {${ref.doi}},\n`;
  if (ref.arxiv) bibtex += `  eprint = {${ref.arxiv}},\n`;
  bibtex += '}';

  return bibtex;
}

/**
 * Copy BibTeX to clipboard
 * @param {string} refId - Reference ID
 * @returns {Promise<boolean>} True if successful
 */
export async function copyBibTeXToClipboard(refId) {
  const ref = await loadReference(refId);
  if (!ref) {
    console.error(`[PM References] Reference ${refId} not found`);
    return false;
  }

  const bibtex = getBibTeX(ref);

  try {
    await navigator.clipboard.writeText(bibtex);
    console.log(`[PM References] BibTeX copied for ${refId}`);
    return true;
  } catch (error) {
    console.error('[PM References] Failed to copy BibTeX:', error);
    return false;
  }
}

/**
 * Get references that cite a specific formula or section
 * @param {string} formulaId - Formula identifier (e.g., 'pneuma_lagrangian')
 * @returns {Promise<Array>} Array of references
 */
export async function getReferencesForFormula(formulaId) {
  if (!referencesCache.all) {
    await loadAllReferences();
  }

  return referencesCache.all.filter(ref =>
    ref.cited_in_formulas?.includes(formulaId) ||
    ref.cited_in_sections?.includes(formulaId)
  );
}

/**
 * Initialize the references module
 * Preloads reference data
 */
export async function initializeReferences() {
  console.log('[PM References] Initializing references module...');
  await loadAllReferences();
  console.log('[PM References] References module initialized');
  return true;
}

// Make available globally for debugging
if (typeof window !== 'undefined') {
  window.PMReferences = {
    loadAllReferences,
    loadReference,
    loadReferencesByCategory,
    loadReferenceByCitation,
    searchReferences,
    renderFullReference,
    renderInlineCitation,
    renderAllReferences,
    getBibTeX,
    copyBibTeXToClipboard,
    getReferencesForFormula,
    clearReferencesCache,
    CATEGORIES,
    TYPES
  };
}
