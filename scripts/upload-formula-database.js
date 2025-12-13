/**
 * Upload Formula Database to Firebase Firestore
 *
 * This script:
 * 1. Parses formula-definitions.js to extract all formulas with metadata
 * 2. Parses formula-database.js to extract tooltip metadata
 * 3. Uploads formulas to 'formulas' collection
 * 4. Uploads tooltip data to 'formula_database' collection
 * 5. Links formulas to PM constant values
 *
 * Each formula document contains:
 * - id, html, latex, label
 * - category (ESTABLISHED/THEORY/DERIVED/PREDICTIONS)
 * - description, attribution
 * - terms (symbol definitions with tooltips)
 * - pm_constant (path to PM value if applicable)
 * - experimental_value, sigma
 * - status, v12_7_status
 * - derivation, references, etc.
 *
 * Usage: node scripts/upload-formula-database.js [--force] [--dry-run]
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const FORCE_UPLOAD = process.argv.includes('--force');
const DRY_RUN = process.argv.includes('--dry-run');

// Initialize Firebase
function initFirebase() {
  const serviceAccountPath = path.join(__dirname, 'serviceAccountKey.json');

  if (!fs.existsSync(serviceAccountPath)) {
    console.error('ERROR: serviceAccountKey.json not found in scripts/ folder');
    console.error('Download from Firebase Console > Project Settings > Service Accounts');
    process.exit(1);
  }

  const serviceAccount = require(serviceAccountPath);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: "principia-metaphysica"
  });

  return admin.firestore();
}

/**
 * Parse formula-definitions.js to extract PM_FORMULAS object
 */
function parseFormulaDefinitions() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-definitions.js');

  if (!fs.existsSync(filePath)) {
    throw new Error(`formula-definitions.js not found at ${filePath}`);
  }

  console.log(`📖 Reading ${filePath}...`);
  const content = fs.readFileSync(filePath, 'utf-8');

  // Extract PM_FORMULAS object
  const startPattern = 'const PM_FORMULAS = {';
  const startIndex = content.indexOf(startPattern);

  if (startIndex === -1) {
    throw new Error('Could not find PM_FORMULAS object');
  }

  // Find the matching closing brace
  let braceCount = 0;
  let inString = false;
  let stringChar = '';
  let escapeNext = false;
  let objectStart = startIndex + 'const PM_FORMULAS = '.length;
  let objectEnd = objectStart;

  for (let i = objectStart; i < content.length; i++) {
    const char = content[i];
    const prevChar = i > 0 ? content[i - 1] : '';

    // Handle escape sequences
    if (escapeNext) {
      escapeNext = false;
      continue;
    }
    if (char === '\\') {
      escapeNext = true;
      continue;
    }

    // Handle strings
    if ((char === '"' || char === "'" || char === '`') && !inString) {
      inString = true;
      stringChar = char;
      continue;
    }
    if (char === stringChar && inString) {
      inString = false;
      continue;
    }

    // Count braces only outside strings
    if (!inString) {
      if (char === '{') braceCount++;
      if (char === '}') {
        braceCount--;
        if (braceCount === 0) {
          objectEnd = i + 1;
          break;
        }
      }
    }
  }

  let objectString = content.substring(objectStart, objectEnd);

  // Use eval to parse the JavaScript object (since it's not valid JSON)
  // This is safe because we're reading our own source file
  let PM_FORMULAS;
  try {
    PM_FORMULAS = eval('(' + objectString + ')');
  } catch (e) {
    console.error('Failed to parse PM_FORMULAS object:', e.message);
    throw e;
  }

  console.log(`✓ Parsed PM_FORMULAS object`);
  return PM_FORMULAS;
}

/**
 * Parse formula-database.js to extract FORMULA_DATABASE object
 */
function parseFormulaDatabase() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-database.js');

  if (!fs.existsSync(filePath)) {
    console.log(`⚠ formula-database.js not found at ${filePath}, skipping tooltip metadata`);
    return null;
  }

  console.log(`📖 Reading ${filePath}...`);
  const content = fs.readFileSync(filePath, 'utf-8');

  // Extract FORMULA_DATABASE object
  const startPattern = 'const FORMULA_DATABASE = {';
  const startIndex = content.indexOf(startPattern);

  if (startIndex === -1) {
    console.log('⚠ Could not find FORMULA_DATABASE object, skipping');
    return null;
  }

  // Find the matching closing brace
  let braceCount = 0;
  let inString = false;
  let stringChar = '';
  let escapeNext = false;
  let objectStart = startIndex + 'const FORMULA_DATABASE = '.length;
  let objectEnd = objectStart;

  for (let i = objectStart; i < content.length; i++) {
    const char = content[i];

    if (escapeNext) {
      escapeNext = false;
      continue;
    }
    if (char === '\\') {
      escapeNext = true;
      continue;
    }

    if ((char === '"' || char === "'" || char === '`') && !inString) {
      inString = true;
      stringChar = char;
      continue;
    }
    if (char === stringChar && inString) {
      inString = false;
      continue;
    }

    if (!inString) {
      if (char === '{') braceCount++;
      if (char === '}') {
        braceCount--;
        if (braceCount === 0) {
          objectEnd = i + 1;
          break;
        }
      }
    }
  }

  let objectString = content.substring(objectStart, objectEnd);

  let FORMULA_DATABASE;
  try {
    FORMULA_DATABASE = eval('(' + objectString + ')');
  } catch (e) {
    console.error('Failed to parse FORMULA_DATABASE object:', e.message);
    return null;
  }

  console.log(`✓ Parsed FORMULA_DATABASE object`);
  return FORMULA_DATABASE;
}

/**
 * Convert a formula object to Firestore document
 */
function formulaToDocument(formulaKey, formula, category) {
  const doc = {
    // Core identification
    id: formula.id,
    key: formulaKey,
    category: category,

    // Display
    html: formula.html || '',
    latex: formula.latex || '',
    label: formula.label || '',

    // Metadata
    description: formula.description || '',
    attribution: formula.attribution || '',
    status: formula.status || null,
    v12_7_status: formula.v12_7_status || null,

    // Terms with tooltips
    terms: formula.terms || {},

    // PM constant reference
    pm_constant: formula.pm_constant || null,

    // Experimental comparison
    experimental_value: formula.experimental_value || null,
    experimental_source: formula.experimental_source || null,
    sigma: formula.sigma || null,

    // Additional fields
    derivation: formula.derivation || null,
    consistency: formula.consistency || null,
    references: formula.references || null,
    testBy: formula.testBy || null,
    currentData: formula.currentData || null,
    currentLimit: formula.currentLimit || null,
    falsification: formula.falsification || null,
    explanation: formula.explanation || null,
    sensitivity: formula.sensitivity || null,
    discovery_significance: formula.discovery_significance || null,

    // Metadata
    uploadedAt: admin.firestore.FieldValue.serverTimestamp()
  };

  // Remove null/undefined values to save storage
  Object.keys(doc).forEach(key => {
    if (doc[key] === null || doc[key] === undefined) {
      delete doc[key];
    }
  });

  return doc;
}

/**
 * Upload formulas to Firestore
 */
async function uploadFormulas(db, PM_FORMULAS) {
  console.log('\n📦 Uploading formulas to Firestore...');

  const categories = ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS'];
  let totalCount = 0;
  let uploadedCount = 0;
  const stats = {
    ESTABLISHED: 0,
    THEORY: 0,
    DERIVED: 0,
    PREDICTIONS: 0
  };

  // Count total formulas
  for (const category of categories) {
    const formulas = PM_FORMULAS[category] || {};
    totalCount += Object.keys(formulas).length;
  }

  console.log(`Total formulas to upload: ${totalCount}`);

  // Process each category
  for (const category of categories) {
    const formulas = PM_FORMULAS[category] || {};
    const formulaKeys = Object.keys(formulas);

    if (formulaKeys.length === 0) {
      continue;
    }

    console.log(`\n  Processing ${category} (${formulaKeys.length} formulas)...`);

    // Use batched writes (max 500 operations per batch)
    const batchSize = 400; // Leave some margin
    let batch = db.batch();
    let batchCount = 0;

    for (const key of formulaKeys) {
      const formula = formulas[key];
      const doc = formulaToDocument(key, formula, category);

      if (DRY_RUN) {
        console.log(`    [DRY RUN] Would upload: ${doc.id} (${doc.label})`);
      } else {
        const docRef = db.collection('formulas').doc(doc.id);
        batch.set(docRef, doc, { merge: !FORCE_UPLOAD });
        batchCount++;
        uploadedCount++;
        stats[category]++;

        // Commit batch when it reaches the size limit
        if (batchCount >= batchSize) {
          await batch.commit();
          console.log(`    ✓ Committed batch of ${batchCount} formulas`);
          batch = db.batch();
          batchCount = 0;
        }
      }
    }

    // Commit remaining formulas in batch
    if (batchCount > 0 && !DRY_RUN) {
      await batch.commit();
      console.log(`    ✓ Committed final batch of ${batchCount} formulas`);
    }
  }

  console.log(`\n✓ Uploaded ${uploadedCount}/${totalCount} formulas`);
  console.log('\nBreakdown by category:');
  for (const category of categories) {
    console.log(`  ${category}: ${stats[category]}`);
  }

  return { totalCount, uploadedCount, stats };
}

/**
 * Upload formula database (tooltip metadata) to Firestore
 */
async function uploadFormulaDatabase(db, FORMULA_DATABASE) {
  if (!FORMULA_DATABASE) {
    console.log('\n⚠ Skipping formula database upload (not loaded)');
    return { totalCount: 0, uploadedCount: 0 };
  }

  console.log('\n📦 Uploading formula database (tooltip metadata)...');

  const entries = Object.keys(FORMULA_DATABASE);
  let uploadedCount = 0;

  const batchSize = 400;
  let batch = db.batch();
  let batchCount = 0;

  for (const key of entries) {
    const entry = FORMULA_DATABASE[key];

    const doc = {
      id: entry.id,
      key: key,
      symbol: entry.symbol || '',
      htmlSymbol: entry.htmlSymbol || '',
      textSymbol: entry.textSymbol || '',
      value: entry.value || null,
      pmRef: entry.pmRef || null,
      description: entry.description || '',
      longDescription: entry.longDescription || '',
      category: entry.category || 'general',
      formula: entry.formula || null,
      experimental: entry.experimental || null,
      derivation: entry.derivation || null,
      explanation: entry.explanation || null,
      occurrences: entry.occurrences || 0,
      usedIn: entry.usedIn || [],
      foundational: entry.foundational || false,
      validated: entry.validated || false,
      exactMatch: entry.exactMatch || false,
      prediction: entry.prediction || false,
      uploadedAt: admin.firestore.FieldValue.serverTimestamp()
    };

    // Remove null/undefined values
    Object.keys(doc).forEach(k => {
      if (doc[k] === null || doc[k] === undefined) {
        delete doc[k];
      }
    });

    if (DRY_RUN) {
      console.log(`  [DRY RUN] Would upload: ${doc.id} (${doc.description})`);
    } else {
      const docRef = db.collection('formula_database').doc(doc.id);
      batch.set(docRef, doc, { merge: !FORCE_UPLOAD });
      batchCount++;
      uploadedCount++;

      if (batchCount >= batchSize) {
        await batch.commit();
        console.log(`  ✓ Committed batch of ${batchCount} entries`);
        batch = db.batch();
        batchCount = 0;
      }
    }
  }

  // Commit remaining
  if (batchCount > 0 && !DRY_RUN) {
    await batch.commit();
    console.log(`  ✓ Committed final batch of ${batchCount} entries`);
  }

  console.log(`✓ Uploaded ${uploadedCount}/${entries.length} tooltip entries`);
  return { totalCount: entries.length, uploadedCount };
}

/**
 * Create metadata document with upload summary
 */
async function createMetadata(db, formulaResults, databaseResults) {
  if (DRY_RUN) {
    console.log('\n[DRY RUN] Would create metadata document');
    return;
  }

  console.log('\n📦 Creating metadata document...');

  const metadata = {
    uploadedAt: admin.firestore.FieldValue.serverTimestamp(),
    version: '12.7',
    formulas: {
      total: formulaResults.totalCount,
      uploaded: formulaResults.uploadedCount,
      stats: formulaResults.stats
    },
    tooltips: {
      total: databaseResults.totalCount,
      uploaded: databaseResults.uploadedCount
    },
    source: {
      formulas: 'js/formula-definitions.js',
      tooltips: 'js/formula-database.js'
    }
  };

  await db.collection('formula_metadata').doc('current').set(metadata);
  console.log('✓ Created formula_metadata/current');
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(70));
  console.log(' PRINCIPIA METAPHYSICA - FORMULA DATABASE UPLOAD');
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Mode: ${DRY_RUN ? 'DRY RUN' : 'LIVE UPLOAD'}`);
  console.log(`Force: ${FORCE_UPLOAD}`);
  console.log('═'.repeat(70));

  let db = null;
  if (!DRY_RUN) {
    db = initFirebase();
  }

  try {
    // Step 1: Parse formula-definitions.js
    const PM_FORMULAS = parseFormulaDefinitions();

    // Step 2: Parse formula-database.js (optional)
    const FORMULA_DATABASE = parseFormulaDatabase();

    // Step 3: Upload formulas
    const formulaResults = await uploadFormulas(db, PM_FORMULAS);

    // Step 4: Upload formula database
    const databaseResults = await uploadFormulaDatabase(db, FORMULA_DATABASE);

    // Step 5: Create metadata
    if (!DRY_RUN) {
      await createMetadata(db, formulaResults, databaseResults);
    }

    console.log('\n' + '═'.repeat(70));
    console.log(' ✅ UPLOAD COMPLETE');
    console.log('═'.repeat(70));
    console.log('\nSummary:');
    console.log(`  Formulas uploaded: ${formulaResults.uploadedCount}/${formulaResults.totalCount}`);
    console.log(`  Tooltips uploaded: ${databaseResults.uploadedCount}/${databaseResults.totalCount}`);
    console.log('\nCollections updated:');
    console.log('  - formulas/');
    console.log('  - formula_database/');
    console.log('  - formula_metadata/current');

    if (DRY_RUN) {
      console.log('\n⚠ This was a DRY RUN - no data was uploaded to Firebase');
      console.log('Run without --dry-run to perform actual upload');
    }

  } catch (error) {
    console.error('\n❌ UPLOAD FAILED:', error);
    console.error(error.stack);
    process.exit(1);
  }

  process.exit(0);
}

main();
