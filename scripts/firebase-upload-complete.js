/**
 * Firebase Complete Data Upload Script
 *
 * Uploads ALL centralized data to Firebase Firestore:
 * - All 56+ formulas from formula-definitions.js
 * - All 15+ constants from formula-database.js
 * - Complete theory constants from theory_output.json
 * - Page content with proper structure
 * - Derivation chain validation
 *
 * Schema standardization:
 * - Formulas have: id, html, latex, label, category, terms, derivationChain, experimental
 * - Constants have: id, symbol, value, unit, pmRef, experimental, sigma, category
 * - All uploads are versioned in validation_history
 *
 * Usage: node scripts/firebase-upload-complete.js [--force]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT_DIR = path.join(__dirname, '..');
const FORCE_UPLOAD = process.argv.includes('--force');

// Colors for console
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

// Initialize Firebase
function initFirebase() {
  const possiblePaths = [
    path.join(__dirname, 'serviceAccountKey.json'),
    path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json'),
    path.join(ROOT_DIR, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json')
  ];

  let serviceAccountPath = null;
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      serviceAccountPath = p;
      break;
    }
  }

  if (!serviceAccountPath) {
    console.error('ERROR: Service account key not found');
    process.exit(1);
  }

  console.log(`Using service account: ${path.basename(serviceAccountPath)}`);

  const serviceAccount = require(serviceAccountPath);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: "principia-metaphysica"
  });

  return admin.firestore();
}

/**
 * Clean undefined values from objects
 */
function cleanUndefined(obj) {
  if (obj === null || obj === undefined) return null;
  if (typeof obj !== 'object') return obj;

  if (Array.isArray(obj)) {
    return obj.map(item => cleanUndefined(item)).filter(item => item !== undefined && item !== null);
  }

  const cleaned = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== undefined && value !== null) {
      const cleanedValue = cleanUndefined(value);
      if (cleanedValue !== undefined && cleanedValue !== null) {
        cleaned[key] = cleanedValue;
      }
    }
  }
  return Object.keys(cleaned).length > 0 ? cleaned : null;
}

/**
 * Load and parse formula-definitions.js using VM
 */
function loadFormulaDefinitions() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-definitions.js');
  if (!fs.existsSync(filePath)) {
    throw new Error('formula-definitions.js not found');
  }

  const content = fs.readFileSync(filePath, 'utf-8');

  // Create a sandbox to execute the JS
  const sandbox = { PM_FORMULAS: null };
  const script = new vm.Script(content + '\nPM_FORMULAS;');
  const result = script.runInNewContext(sandbox);

  return result || sandbox.PM_FORMULAS;
}

/**
 * Load and parse formula-database.js using VM
 */
function loadFormulaDatabase() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-database.js');
  if (!fs.existsSync(filePath)) {
    throw new Error('formula-database.js not found');
  }

  const content = fs.readFileSync(filePath, 'utf-8');

  // Create a sandbox to execute the JS
  const sandbox = { FORMULA_DATABASE: null };
  const script = new vm.Script(content + '\nFORMULA_DATABASE;');
  const result = script.runInNewContext(sandbox);

  return result || sandbox.FORMULA_DATABASE;
}

/**
 * Load theory_output.json
 */
function loadTheoryOutput() {
  const filePath = path.join(ROOT_DIR, 'theory_output.json');
  if (!fs.existsSync(filePath)) {
    throw new Error('theory_output.json not found');
  }

  let content = fs.readFileSync(filePath, 'utf-8');
  // Handle NaN values
  content = content.replace(/:\s*NaN\b/g, ': null');
  content = content.replace(/,\s*NaN\b/g, ', null');
  content = content.replace(/\[\s*NaN\b/g, '[ null');

  return JSON.parse(content);
}

/**
 * Flatten deeply nested objects for Firestore
 */
function flattenForFirestore(obj, depth = 0, maxDepth = 15) {
  if (obj === null || typeof obj !== 'object') return obj;

  if (Array.isArray(obj)) {
    if (depth >= maxDepth) return JSON.stringify(obj);
    return obj.map(item => flattenForFirestore(item, depth + 1, maxDepth));
  }

  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value === null || typeof value !== 'object') {
      result[key] = value;
    } else if (depth >= maxDepth) {
      result[key] = JSON.stringify(value);
    } else {
      result[key] = flattenForFirestore(value, depth + 1, maxDepth);
    }
  }
  return result;
}

/**
 * Validate derivation chains
 * Check that formulas link back to established physics
 */
function validateDerivationChains(formulas) {
  const warnings = [];
  const establishedIds = new Set();

  // Collect all established formula IDs
  for (const formula of formulas) {
    if (formula.category === 'ESTABLISHED') {
      establishedIds.add(formula.id);
    }
  }

  // Check that non-established formulas have valid derivation chains
  for (const formula of formulas) {
    if (formula.category !== 'ESTABLISHED') {
      if (!formula.derivesFrom || formula.derivesFrom.length === 0) {
        // Check if it has foundational references
        if (!formula.attribution && !formula.foundational) {
          warnings.push({
            id: formula.id,
            warning: 'No derivation chain or foundational reference',
            category: formula.category
          });
        }
      } else {
        // Validate that derivesFrom references exist
        for (const ref of formula.derivesFrom) {
          if (!establishedIds.has(ref)) {
            // Check if it references another theory formula (which is ok if that one is grounded)
            const refFormula = formulas.find(f => f.id === ref);
            if (!refFormula) {
              warnings.push({
                id: formula.id,
                warning: `References non-existent formula: ${ref}`,
                category: formula.category
              });
            }
          }
        }
      }
    }
  }

  return warnings;
}

/**
 * Upload all formulas
 */
async function uploadFormulas(db) {
  console.log(`\n${c.bright}📐 Uploading Formulas...${c.reset}`);

  const pmFormulas = loadFormulaDefinitions();
  const allFormulas = [];

  // Extract formulas from all categories
  const categories = ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS'];

  for (const category of categories) {
    if (pmFormulas[category]) {
      for (const [key, formula] of Object.entries(pmFormulas[category])) {
        allFormulas.push({
          ...formula,
          key: key,
          category: category,
          uploadedAt: admin.firestore.FieldValue.serverTimestamp()
        });
      }
    }
  }

  console.log(`  Found ${allFormulas.length} formulas in ${categories.length} categories`);

  // Validate derivation chains
  const warnings = validateDerivationChains(allFormulas);
  if (warnings.length > 0) {
    console.log(`\n  ${c.yellow}⚠ Derivation Chain Warnings (${warnings.length}):${c.reset}`);
    warnings.slice(0, 10).forEach(w => {
      console.log(`    - ${w.id}: ${w.warning}`);
    });
    if (warnings.length > 10) {
      console.log(`    ... and ${warnings.length - 10} more`);
    }
  }

  // Delete existing formulas collection
  console.log(`\n  Clearing existing formulas collection...`);
  const existingFormulas = await db.collection('formulas').listDocuments();
  for (const doc of existingFormulas) {
    await doc.delete();
  }

  // Upload in batches
  let batch = db.batch();
  let count = 0;
  let totalUploaded = 0;

  for (const formula of allFormulas) {
    const docId = formula.id || formula.key;
    const cleanedFormula = cleanUndefined(formula);

    if (cleanedFormula) {
      const docRef = db.collection('formulas').doc(docId);
      batch.set(docRef, cleanedFormula);
      count++;
      totalUploaded++;

      if (count >= 400) {
        await batch.commit();
        console.log(`  ✓ Uploaded batch of ${count} formulas`);
        batch = db.batch();
        count = 0;
      }
    }
  }

  if (count > 0) {
    await batch.commit();
    console.log(`  ✓ Uploaded final batch of ${count} formulas`);
  }

  // Summary by category
  const byCategory = {};
  for (const f of allFormulas) {
    byCategory[f.category] = (byCategory[f.category] || 0) + 1;
  }

  console.log(`\n  ${c.green}✓ Total: ${totalUploaded} formulas uploaded${c.reset}`);
  for (const [cat, count] of Object.entries(byCategory)) {
    console.log(`    - ${cat}: ${count}`);
  }

  return { success: true, count: totalUploaded, warnings: warnings.length };
}

/**
 * Upload formula database (constants/tooltips)
 */
async function uploadFormulaDatabase(db) {
  console.log(`\n${c.bright}📊 Uploading Formula Database (Constants)...${c.reset}`);

  const formulaDb = loadFormulaDatabase();
  const entries = Object.entries(formulaDb);

  console.log(`  Found ${entries.length} constant definitions`);

  // Delete existing
  console.log(`  Clearing existing formula_database collection...`);
  const existing = await db.collection('formula_database').listDocuments();
  for (const doc of existing) {
    await doc.delete();
  }

  // Upload
  let batch = db.batch();
  let count = 0;

  for (const [id, data] of entries) {
    const cleanedData = cleanUndefined({
      ...data,
      id: id,
      uploadedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    if (cleanedData) {
      const docRef = db.collection('formula_database').doc(id);
      batch.set(docRef, cleanedData);
      count++;

      if (count >= 400) {
        await batch.commit();
        batch = db.batch();
        count = 0;
      }
    }
  }

  if (count > 0) {
    await batch.commit();
  }

  console.log(`  ${c.green}✓ Uploaded ${entries.length} constant definitions${c.reset}`);

  return { success: true, count: entries.length };
}

/**
 * Upload theory constants with proper structure
 */
async function uploadTheoryConstants(db) {
  console.log(`\n${c.bright}📦 Uploading Theory Constants...${c.reset}`);

  const theoryOutput = loadTheoryOutput();
  const version = theoryOutput.meta?.version || '12.7';

  // Create structured document
  const theoryDoc = {
    meta: theoryOutput.meta,
    dimensions: theoryOutput.dimensions,
    topology: theoryOutput.topology,
    proton_decay: theoryOutput.proton_decay,
    pmns_matrix: theoryOutput.pmns_matrix,
    pmns_nufit_comparison: theoryOutput.pmns_nufit_comparison,
    dark_energy: theoryOutput.dark_energy,
    desi_dr2_data: theoryOutput.desi_dr2_data,
    neutrino_mass_ordering: flattenForFirestore(theoryOutput.neutrino_mass_ordering),
    proton_decay_channels: theoryOutput.proton_decay_channels,
    xy_bosons: theoryOutput.xy_bosons,
    validation: theoryOutput.validation,
    v12_7_pure_geometric: flattenForFirestore(theoryOutput.v12_7_pure_geometric, 0, 10),
    v12_3_updates: flattenForFirestore(theoryOutput.v12_3_updates, 0, 10),
    uploadedAt: admin.firestore.FieldValue.serverTimestamp()
  };

  // Clean the document
  const cleanedDoc = cleanUndefined(theoryDoc);

  // Upload current version
  await db.collection('theory_constants').doc('current').set(cleanedDoc);
  console.log(`  ✓ Uploaded to theory_constants/current`);

  // Upload versioned backup with timestamp
  const versionId = `v${version.replace(/\./g, '_')}_${Date.now()}`;
  await db.collection('theory_constants').doc(versionId).set(cleanedDoc);
  console.log(`  ✓ Uploaded to theory_constants/${versionId}`);

  // Also maintain a simple v12_7 reference
  await db.collection('theory_constants').doc(`v${version.replace(/\./g, '_')}`).set(cleanedDoc);
  console.log(`  ✓ Uploaded to theory_constants/v${version.replace(/\./g, '_')}`);

  // Extract and upload individual constants for easy querying
  console.log(`\n  Uploading individual constants...`);

  const constants = [];

  // Extract key constants from theory output
  if (theoryOutput.proton_decay) {
    for (const [key, value] of Object.entries(theoryOutput.proton_decay)) {
      if (typeof value === 'number') {
        constants.push({
          id: `proton_decay_${key}`,
          category: 'proton_decay',
          key: key,
          value: value,
          pmRef: `PM.proton_decay.${key}`
        });
      }
    }
  }

  if (theoryOutput.pmns_matrix) {
    for (const [key, value] of Object.entries(theoryOutput.pmns_matrix)) {
      if (typeof value === 'number') {
        constants.push({
          id: `pmns_${key}`,
          category: 'pmns_matrix',
          key: key,
          value: value,
          pmRef: `PM.pmns_matrix.${key}`
        });
      }
    }
  }

  if (theoryOutput.dark_energy) {
    for (const [key, value] of Object.entries(theoryOutput.dark_energy)) {
      if (typeof value === 'number') {
        constants.push({
          id: `dark_energy_${key}`,
          category: 'dark_energy',
          key: key,
          value: value,
          pmRef: `PM.dark_energy.${key}`
        });
      }
    }
  }

  // Upload constants collection
  let batch = db.batch();
  let count = 0;

  for (const constant of constants) {
    const cleanedConstant = cleanUndefined({
      ...constant,
      uploadedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    if (cleanedConstant) {
      const docRef = db.collection('constants').doc(constant.id);
      batch.set(docRef, cleanedConstant);
      count++;

      if (count >= 400) {
        await batch.commit();
        batch = db.batch();
        count = 0;
      }
    }
  }

  if (count > 0) {
    await batch.commit();
  }

  console.log(`  ${c.green}✓ Uploaded ${constants.length} individual constants${c.reset}`);

  return { success: true, version, constantsCount: constants.length };
}

/**
 * Create experimental comparison data
 */
async function uploadExperimentalData(db) {
  console.log(`\n${c.bright}🔬 Uploading Experimental Comparisons...${c.reset}`);

  const experimentalData = {
    nufit_6_0: {
      source: 'NuFIT 6.0 (2025)',
      url: 'http://www.nu-fit.org/',
      parameters: {
        theta_23: { value: 45.0, error: 1.1, unit: 'degrees' },
        theta_12: { value: 33.41, error: 0.75, unit: 'degrees' },
        theta_13: { value: 8.54, error: 0.12, unit: 'degrees' },
        delta_cp: { value: 232, error: 30, unit: 'degrees' },
        dm21_sq: { value: 7.42e-5, error: 0.21e-5, unit: 'eV²' },
        dm31_sq: { value: 2.515e-3, error: 0.028e-3, unit: 'eV²' }
      }
    },
    desi_dr2: {
      source: 'DESI DR2 (2025)',
      parameters: {
        w0: { value: -0.83, error: 0.06, unit: '' },
        wa: { value: -0.75, error: 0.30, unit: '' }
      }
    },
    pdg_2024: {
      source: 'PDG 2024',
      parameters: {
        m_h: { value: 125.25, error: 0.17, unit: 'GeV' },
        m_t: { value: 172.57, error: 0.29, unit: 'GeV' },
        alpha_s: { value: 0.1180, error: 0.0009, unit: '' },
        G_F: { value: 1.1663787e-5, error: 0.0000006e-5, unit: 'GeV⁻²' }
      }
    },
    super_k: {
      source: 'Super-Kamiokande 2024',
      parameters: {
        tau_p_limit: { value: 2.4e34, error: null, unit: 'years', type: 'lower_limit' }
      }
    }
  };

  await db.collection('experimental_data').doc('current').set({
    ...experimentalData,
    uploadedAt: admin.firestore.FieldValue.serverTimestamp()
  });

  console.log(`  ${c.green}✓ Uploaded experimental comparison data${c.reset}`);

  return { success: true };
}

/**
 * Create validation history entry
 */
async function createValidationEntry(db, results) {
  console.log(`\n${c.bright}📋 Creating Validation History Entry...${c.reset}`);

  const theoryOutput = loadTheoryOutput();

  const entry = {
    timestamp: admin.firestore.FieldValue.serverTimestamp(),
    version: theoryOutput.meta?.version || 'unknown',
    uploadType: 'complete_upload',
    results: {
      formulas: results.formulas,
      formulaDatabase: results.formulaDatabase,
      theoryConstants: results.theoryConstants,
      experimentalData: results.experimentalData
    },
    validation: theoryOutput.validation || {},
    derivationWarnings: results.formulas?.warnings || 0,
    summary: {
      totalFormulas: results.formulas?.count || 0,
      totalConstants: results.theoryConstants?.constantsCount || 0,
      totalFormulaDbEntries: results.formulaDatabase?.count || 0,
      predictions_within_1sigma: theoryOutput.validation?.predictions_within_1sigma,
      total_predictions: theoryOutput.validation?.total_predictions,
      exact_matches: theoryOutput.validation?.exact_matches
    }
  };

  const docId = `complete_upload_${Date.now()}`;
  await db.collection('validation_history').doc(docId).set(entry);
  console.log(`  ✓ Created validation_history/${docId}`);

  return { success: true, docId };
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(80));
  console.log(`${c.bright}${c.cyan} PRINCIPIA METAPHYSICA - COMPLETE FIREBASE UPLOAD${c.reset}`);
  console.log('═'.repeat(80));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Force mode: ${FORCE_UPLOAD}\n`);

  const db = initFirebase();
  const results = {};

  try {
    // Upload formulas
    results.formulas = await uploadFormulas(db);

    // Upload formula database (constants/tooltips)
    results.formulaDatabase = await uploadFormulaDatabase(db);

    // Upload theory constants
    results.theoryConstants = await uploadTheoryConstants(db);

    // Upload experimental data
    results.experimentalData = await uploadExperimentalData(db);

    // Create validation entry
    results.validation = await createValidationEntry(db, results);

    // Summary
    console.log('\n' + '═'.repeat(80));
    console.log(`${c.green}${c.bright} ✅ COMPLETE UPLOAD FINISHED${c.reset}`);
    console.log('═'.repeat(80));

    console.log(`\n${c.bright}Summary:${c.reset}`);
    console.log(`  Formulas: ${results.formulas?.count || 0} (${results.formulas?.warnings || 0} derivation warnings)`);
    console.log(`  Formula Database: ${results.formulaDatabase?.count || 0} constant definitions`);
    console.log(`  Theory Constants: v${results.theoryConstants?.version}`);
    console.log(`  Individual Constants: ${results.theoryConstants?.constantsCount || 0}`);
    console.log(`  Experimental Data: ✓`);

  } catch (error) {
    console.error(`\n${c.red}❌ UPLOAD FAILED:${c.reset}`, error);
    process.exit(1);
  }

  process.exit(0);
}

main();
