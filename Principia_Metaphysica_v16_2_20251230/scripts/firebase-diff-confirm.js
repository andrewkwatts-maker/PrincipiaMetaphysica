/**
 * Firebase Diff Confirmation System
 *
 * Compares local data with Firebase and shows detailed diff before upload.
 * Requires explicit confirmation before making any changes.
 *
 * Usage:
 *   node scripts/firebase-diff-confirm.js [--yes] [--collections=all|theory|pages|formulas]
 *
 * Features:
 * - Shows detailed diff for all collections
 * - Color-coded output (added/removed/modified)
 * - Requires explicit confirmation
 * - Creates backup before any changes
 * - Generates diff report file
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const ROOT_DIR = path.join(__dirname, '..');
const SKIP_CONFIRM = process.argv.includes('--yes') || process.argv.includes('-y');
const COLLECTIONS_ARG = process.argv.find(a => a.startsWith('--collections='));
const COLLECTIONS = COLLECTIONS_ARG ? COLLECTIONS_ARG.split('=')[1].split(',') : ['all'];

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  dim: '\x1b[2m'
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
    console.error('Service account key not found!');
    process.exit(1);
  }

  const serviceAccount = require(serviceAccountPath);
  if (!admin.apps.length) {
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });
  }

  return admin.firestore();
}

/**
 * Deep diff two objects
 */
function deepDiff(oldObj, newObj, path = '') {
  const changes = [];

  const allKeys = new Set([
    ...Object.keys(oldObj || {}),
    ...Object.keys(newObj || {})
  ]);

  for (const key of allKeys) {
    const currentPath = path ? `${path}.${key}` : key;
    const oldVal = oldObj?.[key];
    const newVal = newObj?.[key];

    // Skip internal Firebase fields
    if (key.startsWith('_') || key === 'uploadedAt') continue;

    if (oldVal === undefined && newVal !== undefined) {
      changes.push({ type: 'added', path: currentPath, value: newVal });
    } else if (oldVal !== undefined && newVal === undefined) {
      changes.push({ type: 'removed', path: currentPath, value: oldVal });
    } else if (typeof oldVal === 'object' && typeof newVal === 'object' &&
               oldVal !== null && newVal !== null && !Array.isArray(oldVal)) {
      // Recurse into nested objects
      changes.push(...deepDiff(oldVal, newVal, currentPath));
    } else if (JSON.stringify(oldVal) !== JSON.stringify(newVal)) {
      changes.push({ type: 'modified', path: currentPath, oldValue: oldVal, newValue: newVal });
    }
  }

  return changes;
}

/**
 * Format a value for display
 */
function formatValue(val) {
  if (val === null || val === undefined) return 'null';
  if (typeof val === 'object') {
    const str = JSON.stringify(val);
    return str.length > 60 ? str.substring(0, 57) + '...' : str;
  }
  if (typeof val === 'number') {
    if (Math.abs(val) > 1e6 || (Math.abs(val) < 0.001 && val !== 0)) {
      return val.toExponential(4);
    }
    return val.toString();
  }
  return String(val);
}

/**
 * Print diff in a readable format
 */
function printDiff(changes, collectionName) {
  if (changes.length === 0) {
    console.log(`${colors.green}  ✓ No changes${colors.reset}`);
    return;
  }

  const added = changes.filter(c => c.type === 'added');
  const removed = changes.filter(c => c.type === 'removed');
  const modified = changes.filter(c => c.type === 'modified');

  console.log(`  ${colors.green}+${added.length}${colors.reset} added, ${colors.red}-${removed.length}${colors.reset} removed, ${colors.yellow}~${modified.length}${colors.reset} modified\n`);

  // Show first 10 of each type
  if (added.length > 0) {
    console.log(`${colors.green}  Added:${colors.reset}`);
    added.slice(0, 10).forEach(c => {
      console.log(`    ${colors.green}+ ${c.path}${colors.reset}: ${formatValue(c.value)}`);
    });
    if (added.length > 10) console.log(`    ... and ${added.length - 10} more`);
  }

  if (removed.length > 0) {
    console.log(`${colors.red}  Removed:${colors.reset}`);
    removed.slice(0, 10).forEach(c => {
      console.log(`    ${colors.red}- ${c.path}${colors.reset}`);
    });
    if (removed.length > 10) console.log(`    ... and ${removed.length - 10} more`);
  }

  if (modified.length > 0) {
    console.log(`${colors.yellow}  Modified:${colors.reset}`);
    modified.slice(0, 15).forEach(c => {
      const oldStr = formatValue(c.oldValue);
      const newStr = formatValue(c.newValue);
      console.log(`    ${colors.yellow}~ ${c.path}${colors.reset}`);
      console.log(`      ${colors.dim}old: ${oldStr}${colors.reset}`);
      console.log(`      ${colors.cyan}new: ${newStr}${colors.reset}`);
    });
    if (modified.length > 15) console.log(`    ... and ${modified.length - 15} more`);
  }
}

/**
 * Load local data for a collection
 */
function loadLocalData(collectionName) {
  switch (collectionName) {
    case 'theory_constants':
      const theoryPath = path.join(ROOT_DIR, 'theory_output.json');
      if (fs.existsSync(theoryPath)) {
        return { current: JSON.parse(fs.readFileSync(theoryPath, 'utf-8')) };
      }
      break;

    case 'formulas':
      // Load from formula-definitions.js (would need parsing)
      return null;

    case 'pages':
      // Would need HTML extraction
      return null;
  }
  return null;
}

/**
 * Flatten complex numbers and matrices for Firestore
 */
function flattenForFirestore(obj) {
  if (obj === null || obj === undefined) return obj;

  // Handle complex numbers {real, imag}
  if (typeof obj === 'object' && !Array.isArray(obj)) {
    if (obj.hasOwnProperty('real') && obj.hasOwnProperty('imag') && Object.keys(obj).length === 2) {
      const { real, imag } = obj;
      if (imag === 0) return real;
      return imag >= 0 ? `${real}+${imag}i` : `${real}${imag}i`;
    }
  }

  // Handle arrays
  if (Array.isArray(obj)) {
    // Matrices (nested arrays) -> JSON strings
    if (obj.length > 0 && Array.isArray(obj[0])) {
      return JSON.stringify(obj.map(row =>
        row.map(item => {
          if (typeof item === 'object' && item !== null && item.real !== undefined) {
            return flattenForFirestore(item);
          }
          return item;
        })
      ));
    }
    return obj.map(item => flattenForFirestore(item));
  }

  // Handle objects recursively
  if (typeof obj === 'object') {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = flattenForFirestore(value);
    }
    return result;
  }

  return obj;
}

/**
 * Compare local and Firebase data
 */
async function compareCollection(db, collectionName) {
  console.log(`\n${colors.bold}═══ ${collectionName.toUpperCase()} ═══${colors.reset}\n`);

  // Load Firebase data
  const snapshot = await db.collection(collectionName).get();
  const firebaseData = {};
  snapshot.forEach(doc => {
    firebaseData[doc.id] = doc.data();
  });

  console.log(`  Firebase: ${snapshot.size} documents`);

  // Load local data
  const localData = loadLocalData(collectionName);
  if (!localData) {
    console.log(`  Local: ${colors.dim}Not available for comparison${colors.reset}`);
    return { collection: collectionName, changes: [], hasLocal: false };
  }

  console.log(`  Local: ${Object.keys(localData).length} documents\n`);

  // Flatten local data for comparison
  const flattenedLocal = {};
  for (const [docId, data] of Object.entries(localData)) {
    flattenedLocal[docId] = flattenForFirestore(data);
  }

  // Compare each document
  const allChanges = [];
  const allDocIds = new Set([...Object.keys(firebaseData), ...Object.keys(flattenedLocal)]);

  for (const docId of allDocIds) {
    const fbDoc = firebaseData[docId];
    const localDoc = flattenedLocal[docId];

    if (!fbDoc && localDoc) {
      allChanges.push({ type: 'added', path: docId, value: '(new document)' });
    } else if (fbDoc && !localDoc) {
      allChanges.push({ type: 'removed', path: docId, value: '(document removed)' });
    } else {
      const docChanges = deepDiff(fbDoc, localDoc);
      allChanges.push(...docChanges);
    }
  }

  printDiff(allChanges, collectionName);

  return { collection: collectionName, changes: allChanges, hasLocal: true };
}

/**
 * Ask for confirmation
 */
async function askConfirmation(question) {
  if (SKIP_CONFIRM) {
    console.log(`${question} (auto-confirmed with --yes)`);
    return true;
  }

  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question(`\n${colors.bold}${question}${colors.reset} [y/N]: `, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

/**
 * Create backup of current Firebase data
 */
async function createBackup(db, collectionName) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const snapshot = await db.collection(collectionName).get();

  if (snapshot.empty) return null;

  const backupData = {};
  snapshot.forEach(doc => {
    backupData[doc.id] = doc.data();
  });

  const backupRef = db.collection(`${collectionName}_backups`).doc(`backup_${timestamp}`);
  await backupRef.set({
    timestamp,
    documentCount: snapshot.size,
    data: backupData
  });

  return `backup_${timestamp}`;
}

/**
 * Apply changes to Firebase
 */
async function applyChanges(db, collectionName, localData) {
  console.log(`\n${colors.cyan}Applying changes to ${collectionName}...${colors.reset}`);

  // Create backup first
  const backupId = await createBackup(db, collectionName);
  if (backupId) {
    console.log(`  ${colors.green}✓ Backup created: ${backupId}${colors.reset}`);
  }

  // Flatten data for Firestore
  const flattenedData = flattenForFirestore(localData);

  // Upload each document
  for (const [docId, data] of Object.entries(flattenedData)) {
    await db.collection(collectionName).doc(docId).set({
      ...data,
      _last_synced: new Date().toISOString()
    });
    console.log(`  ${colors.green}✓ Updated: ${docId}${colors.reset}`);
  }

  return true;
}

/**
 * Generate diff report file
 */
function generateDiffReport(results) {
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      totalCollections: results.length,
      totalChanges: results.reduce((sum, r) => sum + r.changes.length, 0)
    },
    collections: {}
  };

  for (const result of results) {
    report.collections[result.collection] = {
      hasLocalData: result.hasLocal,
      changeCount: result.changes.length,
      changes: result.changes.slice(0, 100) // Limit to first 100
    };
  }

  const reportPath = path.join(ROOT_DIR, 'firebase-diff-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\n${colors.cyan}Diff report saved to: firebase-diff-report.json${colors.reset}`);

  return reportPath;
}

/**
 * Main function
 */
async function main() {
  console.log(`\n${colors.bold}${'═'.repeat(70)}${colors.reset}`);
  console.log(`${colors.bold} PRINCIPIA METAPHYSICA - FIREBASE DIFF & CONFIRMATION${colors.reset}`);
  console.log(`${colors.bold}${'═'.repeat(70)}${colors.reset}`);
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Auto-confirm: ${SKIP_CONFIRM ? 'YES' : 'NO'}`);

  const db = initFirebase();

  // Collections to compare
  const collectionsToCheck = COLLECTIONS.includes('all')
    ? ['theory_constants', 'formulas', 'formula_database', 'pages', 'appendices']
    : COLLECTIONS;

  console.log(`\nCollections: ${collectionsToCheck.join(', ')}`);

  // Compare each collection
  const results = [];
  for (const collection of collectionsToCheck) {
    try {
      const result = await compareCollection(db, collection);
      results.push(result);
    } catch (error) {
      console.log(`${colors.red}  Error: ${error.message}${colors.reset}`);
      results.push({ collection, changes: [], error: error.message });
    }
  }

  // Generate report
  generateDiffReport(results);

  // Summary
  const totalChanges = results.reduce((sum, r) => sum + r.changes.length, 0);
  console.log(`\n${colors.bold}${'─'.repeat(70)}${colors.reset}`);
  console.log(`${colors.bold}SUMMARY${colors.reset}`);
  console.log(`${colors.bold}${'─'.repeat(70)}${colors.reset}`);
  console.log(`Total changes detected: ${totalChanges}`);

  if (totalChanges === 0) {
    console.log(`\n${colors.green}✓ Firebase is up to date - no changes needed${colors.reset}`);
    process.exit(0);
  }

  // Ask for confirmation
  const confirmed = await askConfirmation('Apply these changes to Firebase?');

  if (!confirmed) {
    console.log(`\n${colors.yellow}✗ Changes cancelled - Firebase unchanged${colors.reset}`);
    process.exit(0);
  }

  // Apply changes
  console.log(`\n${colors.bold}Applying changes...${colors.reset}`);

  for (const result of results) {
    if (result.hasLocal && result.changes.length > 0) {
      const localData = loadLocalData(result.collection);
      if (localData) {
        await applyChanges(db, result.collection, localData);
      }
    }
  }

  console.log(`\n${colors.green}${'═'.repeat(70)}${colors.reset}`);
  console.log(`${colors.green} ✓ ALL CHANGES APPLIED SUCCESSFULLY${colors.reset}`);
  console.log(`${colors.green}${'═'.repeat(70)}${colors.reset}`);

  process.exit(0);
}

main().catch(error => {
  console.error(`\n${colors.red}Error: ${error.message}${colors.reset}`);
  process.exit(1);
});
