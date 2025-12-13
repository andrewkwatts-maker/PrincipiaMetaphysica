/**
 * End-to-End Test for Firebase Data Loading
 *
 * Validates that all pages properly load data from Firebase
 * and that PM values are populated correctly.
 *
 * Run: node scripts/test-data-loading.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');
const admin = require('firebase-admin');
const cheerio = require('cheerio');

const ROOT_DIR = path.join(__dirname, '..');

// Find service account key
const keyPaths = [
  path.join(__dirname, 'serviceAccountKey.json'),
  path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json'),
  path.join(ROOT_DIR, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json')
];

let serviceAccountPath = null;
for (const p of keyPaths) {
  if (fs.existsSync(p)) {
    serviceAccountPath = p;
    break;
  }
}

if (!serviceAccountPath) {
  console.error('Service account key not found!');
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}

const db = admin.firestore();

// Pages to test (main pages only, excluding partials)
const MAIN_PAGES = [
  'index.html',
  'principia-metaphysica-paper.html',
  'beginners-guide.html',
  'references.html',
  'sections/introduction.html',
  'sections/geometric-framework.html',
  'sections/gauge-unification.html',
  'sections/fermion-sector.html',
  'sections/cosmology.html',
  'sections/predictions.html',
  'sections/conclusion.html'
];

// Partial files to exclude from testing
const PARTIAL_FILES = [
  'appendices_content.html',
  'ATTRIBUTION_HTML_ADDITIONS.html',
  'ATTRIBUTION_HTML_ADDITIONS_PART2.html',
  'PAPER_2T_UPDATE_SECTION.html'
];

/**
 * Get value from PM object by path
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

  // Handle nested value objects
  if (current && typeof current === 'object' && current.value !== undefined) {
    return current.value;
  }

  return current;
}

/**
 * Load theory constants from Firebase
 */
async function loadTheoryConstants() {
  console.log('Loading theory constants from Firebase...');
  const docRef = db.collection('theory_constants').doc('current');
  const docSnap = await docRef.get();

  if (!docSnap.exists) {
    throw new Error('Theory constants document not found');
  }

  return docSnap.data();
}

/**
 * Load formula database from Firebase
 */
async function loadFormulaDatabase() {
  console.log('Loading formula database from Firebase...');
  const snapshot = await db.collection('formula_database').get();
  const database = {};

  snapshot.forEach(doc => {
    database[doc.id] = doc.data();
  });

  return database;
}

/**
 * Analyze PM value references in a page
 */
function analyzePMValues(filePath, $, theoryConstants) {
  const pmValues = [];
  const errors = [];
  const warnings = [];

  // Find all PM value elements
  $('.pm-value').each((i, el) => {
    const $el = $(el);
    const pmPath = $el.attr('data-pm-value');
    const category = $el.attr('data-category');
    const param = $el.attr('data-param');

    let valuePath = '';
    let value = null;

    if (pmPath) {
      valuePath = pmPath;
      value = getValueByPath(theoryConstants, pmPath);
    } else if (category && param) {
      valuePath = `${category}.${param}`;
      value = getValueByPath(theoryConstants, valuePath);
    }

    const result = {
      path: valuePath,
      hasValue: value !== undefined && value !== null,
      value: value
    };

    pmValues.push(result);

    if (!result.hasValue && valuePath) {
      errors.push(`Missing value for path: ${valuePath}`);
    }

    if (!valuePath) {
      warnings.push('PM value element without path specified');
    }
  });

  return { pmValues, errors, warnings };
}

/**
 * Test a single page
 */
async function testPage(filePath, theoryConstants, formulaDatabase) {
  const fullPath = path.join(ROOT_DIR, filePath);

  if (!fs.existsSync(fullPath)) {
    return { status: 'not_found', file: filePath };
  }

  const content = fs.readFileSync(fullPath, 'utf-8');
  const $ = cheerio.load(content);

  // Check for Firebase integration
  const hasFirebaseImport = content.includes('firebase-config.js') ||
                           content.includes('firebase-auth.js') ||
                           content.includes('auth-guard.js');

  const hasAuthGuard = content.includes('setupAuthGuard');
  const hasPageLoader = content.includes('firebase-page-loader.js') ||
                       content.includes('initPageFromFirebase');

  // Analyze PM values
  const { pmValues, errors, warnings } = analyzePMValues(filePath, $, theoryConstants);

  // Count formula references
  const formulaRefs = [];
  $('[data-formula-id]').each((i, el) => {
    formulaRefs.push($(el).attr('data-formula-id'));
  });

  return {
    status: 'tested',
    file: filePath,
    firebase: {
      hasImport: hasFirebaseImport,
      hasAuthGuard: hasAuthGuard,
      hasPageLoader: hasPageLoader
    },
    pmValues: {
      total: pmValues.length,
      resolved: pmValues.filter(v => v.hasValue).length,
      unresolved: pmValues.filter(v => !v.hasValue).length
    },
    formulaRefs: formulaRefs.length,
    errors: errors,
    warnings: warnings
  };
}

/**
 * Main test function
 */
async function runTests() {
  console.log('End-to-End Data Loading Test');
  console.log('─'.repeat(70));

  // Load Firebase data
  const theoryConstants = await loadTheoryConstants();
  const formulaDatabase = await loadFormulaDatabase();

  console.log(`Loaded ${Object.keys(theoryConstants).length} theory constant categories`);
  console.log(`Loaded ${Object.keys(formulaDatabase).length} formula database entries`);
  console.log('');

  // Run tests
  const results = [];
  let passCount = 0;
  let warnCount = 0;
  let failCount = 0;

  for (const page of MAIN_PAGES) {
    const result = await testPage(page, theoryConstants, formulaDatabase);
    results.push(result);

    // Determine status
    let status = '✓';
    if (result.errors.length > 0) {
      status = '✗';
      failCount++;
    } else if (result.warnings.length > 0 || !result.firebase.hasImport) {
      status = '⚠';
      warnCount++;
    } else {
      passCount++;
    }

    // Print result
    console.log(`${status} ${page}`);
    if (result.pmValues.total > 0) {
      console.log(`    PM Values: ${result.pmValues.resolved}/${result.pmValues.total} resolved`);
    }
    if (result.formulaRefs > 0) {
      console.log(`    Formula refs: ${result.formulaRefs}`);
    }
    if (result.errors.length > 0) {
      result.errors.forEach(e => console.log(`    ERROR: ${e}`));
    }
    if (result.warnings.length > 0) {
      result.warnings.slice(0, 3).forEach(w => console.log(`    WARN: ${w}`));
    }
    console.log('');
  }

  // Summary
  console.log('─'.repeat(70));
  console.log('SUMMARY');
  console.log(`  Passed: ${passCount}`);
  console.log(`  Warnings: ${warnCount}`);
  console.log(`  Failed: ${failCount}`);
  console.log(`  Total: ${MAIN_PAGES.length}`);

  // Validate PM paths coverage
  console.log('\n─'.repeat(70));
  console.log('PM PATH COVERAGE ANALYSIS');

  const allPaths = new Set();
  const resolvedPaths = new Set();

  for (const result of results) {
    if (result.pmValues) {
      // Would need to track individual paths for full analysis
    }
  }

  // Check critical paths
  const criticalPaths = [
    'dimensions.D_bulk',
    'dimensions.D_after_sp2r',
    'topology.chi_eff',
    'topology.b3',
    'topology.n_gen',
    'pmns_matrix.theta_23',
    'pmns_matrix.theta_12',
    'pmns_matrix.theta_13',
    'pmns_matrix.delta_CP',
    'dark_energy.w0_PM',
    'dark_energy.wa_PM',
    'proton_decay.M_GUT',
    'proton_decay.alpha_GUT_inv',
    'proton_decay.tau_p_median',
    'v11_final_observables.higgs_mass.m_h_GeV'
  ];

  console.log('\nCritical Path Availability:');
  for (const p of criticalPaths) {
    const value = getValueByPath(theoryConstants, p);
    const status = value !== undefined ? '✓' : '✗';
    console.log(`  ${status} ${p}: ${value !== undefined ? value : 'NOT FOUND'}`);
  }

  // Save results
  const reportPath = path.join(ROOT_DIR, 'test-data-loading-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
  console.log(`\nDetailed report saved to: ${reportPath}`);

  return { pass: passCount, warn: warnCount, fail: failCount };
}

// Run tests
runTests()
  .then(summary => {
    if (summary.fail > 0) {
      process.exit(1);
    }
  })
  .catch(error => {
    console.error('Test failed:', error);
    process.exit(1);
  });
