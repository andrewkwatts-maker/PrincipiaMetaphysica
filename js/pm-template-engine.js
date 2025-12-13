/**
 * Principia Metaphysica - Centralized Template Engine
 *
 * Renders content from Firebase Firestore for:
 * - Website HTML display
 * - LaTeX document generation
 * - PDF export
 *
 * All content is loaded from Firebase - no hardcoded values.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { getFirestore, collection, doc, getDoc, getDocs, query, where, orderBy } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-firestore.js";
import { app } from './firebase-config.js';

const db = getFirestore(app);

// Cache for loaded data
const cache = {
  formulas: null,
  formulaDatabase: null,
  theoryConstants: null,
  experimentalData: null,
  constants: null,
  cacheTime: null,
  CACHE_TTL: 5 * 60 * 1000 // 5 minutes
};

/**
 * Check if cache is valid
 */
function isCacheValid() {
  return cache.cacheTime && (Date.now() - cache.cacheTime) < cache.CACHE_TTL;
}

/**
 * Load all formulas from Firebase
 */
export async function loadFormulas() {
  if (isCacheValid() && cache.formulas) {
    return cache.formulas;
  }

  const snapshot = await getDocs(collection(db, 'formulas'));
  const formulas = {};

  snapshot.forEach(doc => {
    formulas[doc.id] = doc.data();
  });

  cache.formulas = formulas;
  cache.cacheTime = Date.now();

  return formulas;
}

/**
 * Load formula database (constants/tooltips) from Firebase
 */
export async function loadFormulaDatabase() {
  if (isCacheValid() && cache.formulaDatabase) {
    return cache.formulaDatabase;
  }

  const snapshot = await getDocs(collection(db, 'formula_database'));
  const formulaDb = {};

  snapshot.forEach(doc => {
    formulaDb[doc.id] = doc.data();
  });

  cache.formulaDatabase = formulaDb;
  cache.cacheTime = Date.now();

  return formulaDb;
}

/**
 * Load theory constants from Firebase
 */
export async function loadTheoryConstants() {
  if (isCacheValid() && cache.theoryConstants) {
    return cache.theoryConstants;
  }

  const docRef = doc(db, 'theory_constants', 'current');
  const docSnap = await getDoc(docRef);

  if (docSnap.exists()) {
    cache.theoryConstants = docSnap.data();
    cache.cacheTime = Date.now();
    return cache.theoryConstants;
  }

  throw new Error('Theory constants not found in Firebase');
}

/**
 * Load experimental data from Firebase
 */
export async function loadExperimentalData() {
  if (isCacheValid() && cache.experimentalData) {
    return cache.experimentalData;
  }

  const docRef = doc(db, 'experimental_data', 'current');
  const docSnap = await getDoc(docRef);

  if (docSnap.exists()) {
    cache.experimentalData = docSnap.data();
    return cache.experimentalData;
  }

  return null;
}

/**
 * Load individual constants from Firebase
 */
export async function loadConstants() {
  if (isCacheValid() && cache.constants) {
    return cache.constants;
  }

  const snapshot = await getDocs(collection(db, 'constants'));
  const constants = {};

  snapshot.forEach(doc => {
    constants[doc.id] = doc.data();
  });

  cache.constants = constants;
  return constants;
}

/**
 * Get a specific formula by ID
 */
export async function getFormula(formulaId) {
  const formulas = await loadFormulas();
  return formulas[formulaId] || null;
}

/**
 * Get formulas by category
 */
export async function getFormulasByCategory(category) {
  const formulas = await loadFormulas();
  return Object.values(formulas).filter(f => f.category === category);
}

/**
 * Get a specific constant definition
 */
export async function getConstantDefinition(constantId) {
  const formulaDb = await loadFormulaDatabase();
  return formulaDb[constantId] || null;
}

/**
 * Get a PM value by path (e.g., "proton_decay.M_GUT")
 */
export async function getPMValue(path) {
  const tc = await loadTheoryConstants();
  const parts = path.split('.');
  let value = tc;

  for (const part of parts) {
    if (value && typeof value === 'object') {
      value = value[part];
    } else {
      return null;
    }
  }

  return value;
}

// =============================================================================
// HTML RENDERING
// =============================================================================

/**
 * Render a formula as HTML with hover tooltip
 */
export async function renderFormulaHTML(formulaId, options = {}) {
  const formula = await getFormula(formulaId);

  if (!formula) {
    return `<span class="formula-error">Formula not found: ${formulaId}</span>`;
  }

  const classes = ['formula-box', `formula-${formula.category?.toLowerCase() || 'unknown'}`];
  if (options.interactive) classes.push('interactive-formula');

  let html = `<div class="${classes.join(' ')}" data-formula-id="${formulaId}">`;

  // Label
  if (formula.label) {
    html += `<span class="formula-label">${formula.label}</span>`;
  }

  // Formula content
  html += `<span class="formula-content">${formula.html || ''}</span>`;

  // Terms tooltip data
  if (formula.terms) {
    html += `<div class="formula-terms" style="display:none;">`;
    for (const [symbol, info] of Object.entries(formula.terms)) {
      html += `<div class="term" data-symbol="${symbol}">`;
      html += `<span class="term-name">${info.name || ''}</span>`;
      html += `<span class="term-desc">${info.description || ''}</span>`;
      html += `</div>`;
    }
    html += `</div>`;
  }

  html += `</div>`;

  return html;
}

/**
 * Render a PM value as HTML with hover tooltip
 */
export async function renderPMValueHTML(pmPath, options = {}) {
  const value = await getPMValue(pmPath);
  const parts = pmPath.split('.');
  const key = parts[parts.length - 1];

  // Try to get additional metadata from formula database
  const formulaDb = await loadFormulaDatabase();
  const metadata = formulaDb[key] || {};

  // Format value
  let displayValue = value;
  if (typeof value === 'number') {
    if (Math.abs(value) > 1e4 || (Math.abs(value) < 1e-4 && value !== 0)) {
      displayValue = value.toExponential(4);
    } else {
      displayValue = value.toFixed(4);
    }
  }

  const classes = ['pm-value'];
  if (metadata.exactMatch) classes.push('exact-match');
  if (metadata.validated) classes.push('validated');

  let html = `<span class="${classes.join(' ')}" `;
  html += `data-pm-path="${pmPath}" `;
  html += `data-category="${parts[0] || ''}" `;
  html += `data-param="${key}" `;
  html += `title="${metadata.description || key}">`;
  html += displayValue;

  if (metadata.unit) {
    html += ` <span class="unit">${metadata.unit}</span>`;
  }

  html += `</span>`;

  return html;
}

/**
 * Render experimental comparison as HTML
 */
export async function renderExperimentalComparisonHTML(pmPath, experimentalSource) {
  const pmValue = await getPMValue(pmPath);
  const experimental = await loadExperimentalData();

  if (!experimental || !experimental[experimentalSource]) {
    return `<span class="comparison-error">Experimental data not found</span>`;
  }

  const parts = pmPath.split('.');
  const key = parts[parts.length - 1];
  const expData = experimental[experimentalSource].parameters[key];

  if (!expData) {
    return `<span class="comparison-error">Parameter ${key} not in ${experimentalSource}</span>`;
  }

  // Calculate sigma deviation
  let sigma = 0;
  if (expData.error && expData.error > 0) {
    sigma = Math.abs(pmValue - expData.value) / expData.error;
  }

  const sigmaClass = sigma < 1 ? 'within-1sigma' : sigma < 2 ? 'within-2sigma' : 'outside-2sigma';

  let html = `<div class="experimental-comparison ${sigmaClass}">`;
  html += `<span class="pm-value">${pmValue.toFixed(4)}</span>`;
  html += ` vs `;
  html += `<span class="exp-value">${expData.value} ± ${expData.error || '?'}</span>`;
  html += ` <span class="sigma">(${sigma.toFixed(2)}σ)</span>`;
  html += `</div>`;

  return html;
}

// =============================================================================
// LATEX RENDERING
// =============================================================================

/**
 * Render a formula as LaTeX
 */
export async function renderFormulaLaTeX(formulaId, options = {}) {
  const formula = await getFormula(formulaId);

  if (!formula) {
    return `% Formula not found: ${formulaId}`;
  }

  let latex = '';

  // Add label as equation number
  if (options.numbered && formula.label) {
    latex += `% ${formula.label}\n`;
  }

  // Use latex field if available, otherwise convert html
  if (formula.latex) {
    if (options.display) {
      latex += `\\begin{equation}\n  ${formula.latex}\n\\end{equation}`;
    } else {
      latex += `$${formula.latex}$`;
    }
  } else {
    // Convert HTML to LaTeX (basic conversion)
    let converted = formula.html || '';
    converted = converted.replace(/<sub>/g, '_{');
    converted = converted.replace(/<\/sub>/g, '}');
    converted = converted.replace(/<sup>/g, '^{');
    converted = converted.replace(/<\/sup>/g, '}');
    converted = converted.replace(/×/g, '\\times ');
    converted = converted.replace(/±/g, '\\pm ');
    converted = converted.replace(/≈/g, '\\approx ');
    converted = converted.replace(/∫/g, '\\int ');
    converted = converted.replace(/∑/g, '\\sum ');
    converted = converted.replace(/√/g, '\\sqrt');
    converted = converted.replace(/∂/g, '\\partial ');
    converted = converted.replace(/α/g, '\\alpha ');
    converted = converted.replace(/β/g, '\\beta ');
    converted = converted.replace(/γ/g, '\\gamma ');
    converted = converted.replace(/δ/g, '\\delta ');
    converted = converted.replace(/θ/g, '\\theta ');
    converted = converted.replace(/λ/g, '\\lambda ');
    converted = converted.replace(/μ/g, '\\mu ');
    converted = converted.replace(/ν/g, '\\nu ');
    converted = converted.replace(/π/g, '\\pi ');
    converted = converted.replace(/σ/g, '\\sigma ');
    converted = converted.replace(/τ/g, '\\tau ');
    converted = converted.replace(/Λ/g, '\\Lambda ');
    converted = converted.replace(/Ψ/g, '\\Psi ');
    converted = converted.replace(/ψ/g, '\\psi ');

    if (options.display) {
      latex += `\\begin{equation}\n  ${converted}\n\\end{equation}`;
    } else {
      latex += `$${converted}$`;
    }
  }

  return latex;
}

/**
 * Render a PM value as LaTeX
 */
export async function renderPMValueLaTeX(pmPath, options = {}) {
  const value = await getPMValue(pmPath);

  if (value === null || value === undefined) {
    return `% Value not found: ${pmPath}`;
  }

  // Format value
  let latex = '';
  if (typeof value === 'number') {
    if (Math.abs(value) > 1e4 || (Math.abs(value) < 1e-4 && value !== 0)) {
      // Scientific notation
      const exp = Math.floor(Math.log10(Math.abs(value)));
      const mantissa = value / Math.pow(10, exp);
      latex = `${mantissa.toFixed(3)} \\times 10^{${exp}}`;
    } else {
      latex = value.toFixed(4);
    }
  } else {
    latex = String(value);
  }

  if (options.inline) {
    return `$${latex}$`;
  }

  return latex;
}

/**
 * Generate a complete LaTeX document section
 */
export async function generateLaTeXSection(sectionConfig) {
  const { title, formulas = [], constants = [], text = '' } = sectionConfig;

  let latex = '';

  // Section header
  latex += `\\section{${title}}\n\n`;

  // Text content
  if (text) {
    latex += `${text}\n\n`;
  }

  // Formulas
  if (formulas.length > 0) {
    for (const formulaId of formulas) {
      const formulaLatex = await renderFormulaLaTeX(formulaId, { display: true, numbered: true });
      latex += `${formulaLatex}\n\n`;
    }
  }

  // Constants table
  if (constants.length > 0) {
    latex += `\\begin{table}[h]\n`;
    latex += `\\centering\n`;
    latex += `\\begin{tabular}{|l|c|c|}\n`;
    latex += `\\hline\n`;
    latex += `Parameter & PM Value & Experimental \\\\\n`;
    latex += `\\hline\n`;

    for (const constant of constants) {
      const pmValue = await getPMValue(constant.pmPath);
      const expValue = constant.experimental || 'N/A';
      latex += `${constant.name} & ${pmValue} & ${expValue} \\\\\n`;
    }

    latex += `\\hline\n`;
    latex += `\\end{tabular}\n`;
    latex += `\\end{table}\n\n`;
  }

  return latex;
}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Initialize the template engine and preload data
 */
export async function initialize() {
  console.log('[PM Template Engine] Initializing...');

  try {
    await Promise.all([
      loadFormulas(),
      loadFormulaDatabase(),
      loadTheoryConstants(),
      loadExperimentalData(),
      loadConstants()
    ]);

    console.log('[PM Template Engine] Data loaded successfully');
    console.log(`  - ${Object.keys(cache.formulas || {}).length} formulas`);
    console.log(`  - ${Object.keys(cache.formulaDatabase || {}).length} constant definitions`);
    console.log(`  - ${Object.keys(cache.constants || {}).length} individual constants`);

    return true;
  } catch (error) {
    console.error('[PM Template Engine] Initialization failed:', error);
    return false;
  }
}

/**
 * Clear the cache
 */
export function clearCache() {
  cache.formulas = null;
  cache.formulaDatabase = null;
  cache.theoryConstants = null;
  cache.experimentalData = null;
  cache.constants = null;
  cache.cacheTime = null;
}

// Export cache for debugging
export function getCache() {
  return { ...cache };
}

export default {
  initialize,
  loadFormulas,
  loadFormulaDatabase,
  loadTheoryConstants,
  loadExperimentalData,
  loadConstants,
  getFormula,
  getFormulasByCategory,
  getConstantDefinition,
  getPMValue,
  renderFormulaHTML,
  renderPMValueHTML,
  renderExperimentalComparisonHTML,
  renderFormulaLaTeX,
  renderPMValueLaTeX,
  generateLaTeXSection,
  clearCache,
  getCache
};
