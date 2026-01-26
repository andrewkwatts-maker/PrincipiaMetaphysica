/**
 * Firebase Sync with History
 *
 * Syncs local theory constants to Firebase with:
 * - Diff detection (only uploads if changes exist)
 * - Version history (backs up old data before overwriting)
 * - Change logging
 * - CONFIRMATION PROMPT before push (unless --yes flag)
 *
 * Run: node scripts/firebase-sync-with-history.js [--yes]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const admin = require('firebase-admin');

// Check for --yes flag (skip confirmation)
const SKIP_CONFIRMATION = process.argv.includes('--yes') || process.argv.includes('-y');

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
  console.log('Looked in:', keyPaths);
  console.log('\nTo fix: Place your Firebase service account key in one of these locations.');
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}

const db = admin.firestore();

/**
 * Convert complex number object {real, imag} to string format "a+bi"
 */
function complexToString(obj) {
  if (typeof obj !== 'object' || obj === null) return obj;
  if (!obj.hasOwnProperty('real') || !obj.hasOwnProperty('imag')) return obj;
  if (Object.keys(obj).length !== 2) return obj;

  const real = obj.real;
  const imag = obj.imag;
  if (imag === 0) return real;
  if (real === 0) return imag + 'i';
  return imag >= 0 ? `${real}+${imag}i` : `${real}${imag}i`;
}

/**
 * Check if value is a matrix (array of arrays)
 */
function isMatrix(val) {
  return Array.isArray(val) && val.length > 0 && Array.isArray(val[0]);
}

/**
 * Flatten data for Firestore compatibility
 * - Converts complex numbers {real, imag} to strings
 * - Converts matrices (nested arrays) to JSON strings
 * - Firestore has limits on nested entities
 */
function flattenForFirestore(obj, depth = 0) {
  if (obj === null || obj === undefined) {
    return obj;
  }

  // Handle complex number objects {real, imag}
  if (typeof obj === 'object' && !Array.isArray(obj)) {
    const asComplex = complexToString(obj);
    if (asComplex !== obj) return asComplex;
  }

  // Handle arrays
  if (Array.isArray(obj)) {
    // Matrices (array of arrays) should be serialized as JSON strings
    if (isMatrix(obj)) {
      // Recursively convert complex numbers within the matrix first
      const converted = obj.map(row =>
        row.map(item => {
          if (typeof item === 'object' && item !== null) {
            return complexToString(item);
          }
          return item;
        })
      );
      return JSON.stringify(converted);
    }

    // Regular arrays - process each element
    return obj.map(item => flattenForFirestore(item, depth + 1));
  }

  // Handle objects recursively
  if (typeof obj === 'object') {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = flattenForFirestore(value, depth + 1);
    }
    return result;
  }

  return obj;
}

/**
 * Load local theory constants from theory-constants-enhanced.js or theory_output.json
 */
function loadLocalData() {
  // Try theory_output.json first (raw simulation output)
  const jsonPath = path.join(ROOT_DIR, 'theory_output.json');
  if (fs.existsSync(jsonPath)) {
    console.log('Loading from theory_output.json...');
    return JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  }

  // Try theory-constants-enhanced.js
  const jsPath = path.join(ROOT_DIR, 'theory-constants-enhanced.js');
  if (fs.existsSync(jsPath)) {
    console.log('Loading from theory-constants-enhanced.js...');
    const content = fs.readFileSync(jsPath, 'utf-8');
    // Extract JSON from "const PM = {...};"
    const match = content.match(/const PM\s*=\s*(\{[\s\S]*?\});/);
    if (match) {
      return JSON.parse(match[1]);
    }
  }

  throw new Error('No local data file found');
}

/**
 * Compute diff between two objects (shallow comparison of top-level keys)
 */
function computeDiff(oldData, newData) {
  const changes = [];
  const allKeys = new Set([...Object.keys(oldData || {}), ...Object.keys(newData || {})]);

  for (const key of allKeys) {
    const oldVal = oldData?.[key];
    const newVal = newData?.[key];
    const oldStr = JSON.stringify(oldVal);
    const newStr = JSON.stringify(newVal);

    if (oldStr !== newStr) {
      changes.push({
        key,
        type: !oldVal ? 'added' : !newVal ? 'removed' : 'changed',
        oldValue: oldVal,
        newValue: newVal
      });
    }
  }

  return changes;
}

/**
 * Format change for display
 */
function formatChange(change) {
  if (change.type === 'added') {
    return '  + ' + change.key + ': (new)';
  } else if (change.type === 'removed') {
    return '  - ' + change.key + ': (removed)';
  } else {
    const oldStr = JSON.stringify(change.oldValue);
    const newStr = JSON.stringify(change.newValue);
    if (oldStr.length < 50 && newStr.length < 50) {
      return '  ~ ' + change.key + ': ' + oldStr.substring(0, 30) + ' -> ' + newStr.substring(0, 30);
    } else {
      return '  ~ ' + change.key + ': (changed, ' + newStr.length + ' chars)';
    }
  }
}

/**
 * Prompt user for confirmation
 */
function askConfirmation(question) {
  return new Promise((resolve) => {
    if (SKIP_CONFIRMATION) {
      console.log(question + ' (auto-confirmed with --yes flag)');
      resolve(true);
      return;
    }

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question(question + ' [y/N]: ', (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

/**
 * Main sync function
 */
async function syncToFirebase() {
  console.log('Firebase Sync with History');
  console.log('─'.repeat(70));

  // Load local data
  let localData;
  try {
    localData = loadLocalData();
    console.log('Local data loaded: ' + Object.keys(localData).length + ' top-level keys');
  } catch (error) {
    console.error('Error loading local data:', error.message);
    process.exit(1);
  }

  // Load current Firebase data
  console.log('\nFetching current Firebase data...');
  const currentRef = db.collection('theory_constants').doc('current');
  const currentSnap = await currentRef.get();
  const currentData = currentSnap.exists ? currentSnap.data() : null;

  if (currentData) {
    console.log('Firebase data exists: ' + Object.keys(currentData).length + ' top-level keys');
  } else {
    console.log('No existing Firebase data found');
  }

  // Compute diff
  console.log('\nComputing diff...');
  const changes = computeDiff(currentData, localData);

  if (changes.length === 0) {
    console.log('\n✓ No changes detected - Firebase is up to date');
    return { status: 'no_changes', changes: 0 };
  }

  console.log('\nFound ' + changes.length + ' changes:');
  changes.slice(0, 20).forEach(c => console.log(formatChange(c)));
  if (changes.length > 20) {
    console.log('  ... and ' + (changes.length - 20) + ' more changes');
  }

  // Summary of what will be synced
  const added = changes.filter(c => c.type === 'added').length;
  const removed = changes.filter(c => c.type === 'removed').length;
  const modified = changes.filter(c => c.type === 'changed').length;
  console.log('\nSummary:');
  console.log('  Added:    ' + added + ' keys');
  console.log('  Removed:  ' + removed + ' keys');
  console.log('  Modified: ' + modified + ' keys');
  console.log('  Total:    ' + changes.length + ' changes');

  // Ask for confirmation before proceeding
  const confirmed = await askConfirmation('\nPush these changes to Firebase?');
  if (!confirmed) {
    console.log('\n✗ Sync cancelled by user');
    return { status: 'cancelled', changes: changes.length };
  }

  // Create backup of current data
  if (currentData) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const historyRef = db.collection('theory_constants').doc('history_' + timestamp);

    console.log('\nBacking up current data to history_' + timestamp + '...');
    await historyRef.set({
      ...currentData,
      _backup_timestamp: timestamp,
      _backup_reason: 'pre-sync backup'
    });
    console.log('  Backup created');
  }

  // Update current data
  console.log('\nUploading new data to Firebase...');
  const version = localData.meta?.version || new Date().toISOString().split('T')[0];

  // Flatten data for Firestore compatibility (converts complex numbers and matrices)
  console.log('  Flattening nested structures for Firestore...');
  const flattenedData = flattenForFirestore(localData);

  await currentRef.set({
    ...flattenedData,
    _last_synced: new Date().toISOString(),
    _sync_version: version,
    _changes_count: changes.length
  });

  console.log('\n✓ Sync complete!');
  console.log('  Version: ' + version);
  console.log('  Changes: ' + changes.length);

  // Save sync report
  const reportPath = path.join(ROOT_DIR, 'firebase-sync-report.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    version,
    changesCount: changes.length,
    changes: changes.slice(0, 50)
  }, null, 2));
  console.log('  Report saved: ' + reportPath);

  return { status: 'synced', changes: changes.length };
}

// Run sync
syncToFirebase()
  .then(result => {
    console.log('\n' + '─'.repeat(70));
    if (result.status === 'synced') {
      console.log('SUCCESS: ' + result.changes + ' changes synced to Firebase');
    } else {
      console.log('SUCCESS: Firebase is up to date');
    }
    process.exit(0);
  })
  .catch(error => {
    console.error('\nERROR:', error);
    process.exit(1);
  });
