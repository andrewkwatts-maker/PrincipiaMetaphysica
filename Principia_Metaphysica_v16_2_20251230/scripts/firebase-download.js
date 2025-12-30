/**
 * Firebase Database Download Script
 *
 * Downloads ALL data from Firebase Firestore to local JSON files
 * for viewing, backup, and version control.
 *
 * Usage: node scripts/firebase-download.js
 *
 * Output:
 *   firebase-backup/
 *     theory_constants.json
 *     formulas.json
 *     formula_database.json
 *     pages.json
 *     validation_history.json
 *     metadata.json
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const BACKUP_DIR = path.join(ROOT_DIR, 'firebase-backup');

// Initialize Firebase
function initFirebase() {
  // Check multiple possible locations for service account key
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
    console.error('\nLooked in:');
    possiblePaths.forEach(p => console.error(`  - ${p}`));
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
 * Download a collection
 */
async function downloadCollection(db, collectionName) {
  console.log(`  Downloading ${collectionName}...`);

  const snapshot = await db.collection(collectionName).get();
  const data = {};

  snapshot.forEach(doc => {
    data[doc.id] = doc.data();
  });

  return {
    collectionName,
    documentCount: snapshot.size,
    data
  };
}

/**
 * Convert Firestore timestamps to ISO strings
 */
function serializeData(obj) {
  if (obj === null || obj === undefined) return obj;

  if (obj.toDate && typeof obj.toDate === 'function') {
    return obj.toDate().toISOString();
  }

  if (Array.isArray(obj)) {
    return obj.map(item => serializeData(item));
  }

  if (typeof obj === 'object') {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = serializeData(value);
    }
    return result;
  }

  return obj;
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(70));
  console.log(' PRINCIPIA METAPHYSICA - FIREBASE DATABASE DOWNLOAD');
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  const db = initFirebase();

  // Create backup directory
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }

  const collections = [
    'theory_constants',
    'formulas',
    'formula_database',
    'pages',
    'appendices',
    'validation_history'
  ];

  const metadata = {
    downloadedAt: new Date().toISOString(),
    collections: {}
  };

  console.log('📥 Downloading collections...\n');

  for (const collName of collections) {
    try {
      const result = await downloadCollection(db, collName);

      // Serialize and save
      const serialized = serializeData(result.data);
      const filePath = path.join(BACKUP_DIR, `${collName}.json`);
      fs.writeFileSync(filePath, JSON.stringify(serialized, null, 2));

      metadata.collections[collName] = {
        documentCount: result.documentCount,
        file: `${collName}.json`
      };

      console.log(`  ✓ ${collName}: ${result.documentCount} documents`);
    } catch (error) {
      console.log(`  ✗ ${collName}: ${error.message}`);
      metadata.collections[collName] = {
        error: error.message
      };
    }
  }

  // Save metadata
  const metadataPath = path.join(BACKUP_DIR, 'metadata.json');
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

  console.log('\n' + '═'.repeat(70));
  console.log(' ✅ DOWNLOAD COMPLETE');
  console.log('═'.repeat(70));
  console.log(`\nBackup saved to: ${BACKUP_DIR}`);

  // List files
  console.log('\nFiles created:');
  const files = fs.readdirSync(BACKUP_DIR);
  files.forEach(file => {
    const stats = fs.statSync(path.join(BACKUP_DIR, file));
    console.log(`  ${file} (${(stats.size / 1024).toFixed(1)} KB)`);
  });

  process.exit(0);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
