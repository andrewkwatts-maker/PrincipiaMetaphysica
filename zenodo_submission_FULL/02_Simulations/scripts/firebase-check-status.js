/**
 * Firebase Migration Status Checker
 *
 * Checks the current state of Firebase Firestore data vs local files
 * and reports what needs to be migrated.
 *
 * Usage: node scripts/firebase-check-status.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

const ROOT_DIR = path.join(__dirname, '..');

// Initialize Firebase Admin
function initFirebase() {
  // Check multiple possible locations for service account key
  const possiblePaths = [
    path.join(__dirname, 'serviceAccountKey.json'),
    path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json'),
    path.join(ROOT_DIR, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json')
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      console.log(`${colors.cyan}Using service account: ${path.basename(p)}${colors.reset}`);
      const serviceAccount = require(p);
      admin.initializeApp({
        credential: admin.credential.cert(serviceAccount),
        projectId: "principia-metaphysica"
      });
      return true;
    }
  }

  if (process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    admin.initializeApp({
      projectId: "principia-metaphysica"
    });
    return true;
  }

  console.error(`${colors.red}ERROR: Service account key not found${colors.reset}`);
  console.error('Looked in:');
  possiblePaths.forEach(p => console.error(`  - ${p}`));
  return false;
}

/**
 * Check local source files
 */
function checkLocalFiles() {
  const files = {
    'theory_output.json': { path: 'theory_output.json', required: true, type: 'json' },
    'theory-constants-enhanced.js': { path: 'theory-constants-enhanced.js', required: true, type: 'js' },
    'formula-definitions.js': { path: 'js/formula-definitions.js', required: true, type: 'js' },
    'formula-database.js': { path: 'js/formula-database.js', required: false, type: 'js' },
    'config.py': { path: 'config.py', required: true, type: 'python' }
  };

  const status = {};

  for (const [name, info] of Object.entries(files)) {
    const fullPath = path.join(ROOT_DIR, info.path);
    const exists = fs.existsSync(fullPath);

    let size = 0;
    let lastModified = null;
    let version = null;

    if (exists) {
      const stats = fs.statSync(fullPath);
      size = stats.size;
      lastModified = stats.mtime;

      // Try to extract version
      if (info.type === 'json') {
        try {
          const data = JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
          version = data.meta?.version || null;
        } catch (e) {}
      } else if (info.type === 'js') {
        try {
          const content = fs.readFileSync(fullPath, 'utf-8');
          const versionMatch = content.match(/version['":\s]+['"]?([\d.]+)['"]?/i);
          if (versionMatch) version = versionMatch[1];
        } catch (e) {}
      }
    }

    status[name] = {
      exists,
      path: info.path,
      size,
      lastModified,
      version,
      required: info.required
    };
  }

  return status;
}

/**
 * Check Firestore collections
 */
async function checkFirestoreCollections(db) {
  const collections = [
    'theory_constants',
    'formulas',
    'formula_database',
    'pages',
    'appendices',
    'validation_history'
  ];

  const status = {};

  for (const collName of collections) {
    try {
      const snapshot = await db.collection(collName).get();
      const docs = [];

      snapshot.forEach(doc => {
        const data = doc.data();
        docs.push({
          id: doc.id,
          version: data.meta?.version || data.version || null,
          lastUpdated: data.meta?.last_updated || data.lastUpdated || null
        });
      });

      status[collName] = {
        exists: true,
        documentCount: snapshot.size,
        documents: docs
      };
    } catch (error) {
      status[collName] = {
        exists: false,
        error: error.message
      };
    }
  }

  return status;
}

/**
 * Compare local and remote versions
 */
function compareVersions(localFiles, firestoreStatus) {
  const comparison = {
    needsUpload: [],
    synced: [],
    conflicts: [],
    missing: []
  };

  // Check theory constants
  const localVersion = localFiles['theory_output.json']?.version;
  const remoteTheory = firestoreStatus['theory_constants'];

  if (remoteTheory?.exists && remoteTheory.documentCount > 0) {
    const remoteCurrent = remoteTheory.documents.find(d => d.id === 'current');
    const remoteVersion = remoteCurrent?.version;

    if (localVersion && remoteVersion) {
      if (localVersion === remoteVersion) {
        comparison.synced.push(`theory_constants (v${localVersion})`);
      } else if (parseFloat(localVersion) > parseFloat(remoteVersion)) {
        comparison.needsUpload.push({
          collection: 'theory_constants',
          localVersion,
          remoteVersion,
          action: 'Upload newer version'
        });
      } else {
        comparison.conflicts.push({
          collection: 'theory_constants',
          localVersion,
          remoteVersion,
          issue: 'Remote is newer than local'
        });
      }
    }
  } else {
    comparison.missing.push('theory_constants');
  }

  // Check formulas
  if (!firestoreStatus['formulas']?.exists || firestoreStatus['formulas'].documentCount === 0) {
    comparison.missing.push('formulas');
  } else {
    comparison.synced.push(`formulas (${firestoreStatus['formulas'].documentCount} docs)`);
  }

  // Check formula_database
  if (!firestoreStatus['formula_database']?.exists || firestoreStatus['formula_database'].documentCount === 0) {
    comparison.missing.push('formula_database');
  } else {
    comparison.synced.push(`formula_database (${firestoreStatus['formula_database'].documentCount} docs)`);
  }

  // Check pages
  if (!firestoreStatus['pages']?.exists || firestoreStatus['pages'].documentCount === 0) {
    comparison.missing.push('pages (website content)');
  }

  return comparison;
}

/**
 * Generate migration report
 */
function generateReport(localFiles, firestoreStatus, comparison) {
  console.log('\n' + '═'.repeat(70));
  console.log(`${colors.bright}${colors.cyan} PRINCIPIA METAPHYSICA - FIREBASE MIGRATION STATUS${colors.reset}`);
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  // Local Files Section
  console.log(`${colors.bright}📁 LOCAL SOURCE FILES${colors.reset}`);
  console.log('─'.repeat(50));

  for (const [name, info] of Object.entries(localFiles)) {
    const icon = info.exists ? '✓' : '✗';
    const color = info.exists ? colors.green : colors.red;
    const version = info.version ? ` (v${info.version})` : '';
    const size = info.exists ? ` [${(info.size / 1024).toFixed(1)} KB]` : '';
    console.log(`${color}${icon}${colors.reset} ${name}${version}${size}`);
  }

  // Firestore Section
  console.log(`\n${colors.bright}☁️  FIRESTORE COLLECTIONS${colors.reset}`);
  console.log('─'.repeat(50));

  for (const [name, info] of Object.entries(firestoreStatus)) {
    const icon = info.exists && info.documentCount > 0 ? '✓' : '○';
    const color = info.exists && info.documentCount > 0 ? colors.green : colors.yellow;
    const count = info.exists ? ` (${info.documentCount} docs)` : ' (not found)';
    console.log(`${color}${icon}${colors.reset} ${name}${count}`);
  }

  // Comparison Section
  console.log(`\n${colors.bright}📊 SYNC STATUS${colors.reset}`);
  console.log('─'.repeat(50));

  if (comparison.synced.length > 0) {
    console.log(`${colors.green}Synced:${colors.reset}`);
    comparison.synced.forEach(item => console.log(`  ✓ ${item}`));
  }

  if (comparison.needsUpload.length > 0) {
    console.log(`${colors.yellow}Needs Upload:${colors.reset}`);
    comparison.needsUpload.forEach(item => {
      console.log(`  ↑ ${item.collection}: local v${item.localVersion} → remote v${item.remoteVersion}`);
    });
  }

  if (comparison.missing.length > 0) {
    console.log(`${colors.red}Missing (needs initial upload):${colors.reset}`);
    comparison.missing.forEach(item => console.log(`  ✗ ${item}`));
  }

  if (comparison.conflicts.length > 0) {
    console.log(`${colors.red}Conflicts:${colors.reset}`);
    comparison.conflicts.forEach(item => {
      console.log(`  ⚠ ${item.collection}: ${item.issue}`);
    });
  }

  // Recommendations
  console.log(`\n${colors.bright}📋 RECOMMENDATIONS${colors.reset}`);
  console.log('─'.repeat(50));

  if (comparison.missing.length > 0) {
    console.log(`${colors.yellow}1. Run initial migration:${colors.reset}`);
    console.log('   node scripts/firebase-upload-all.js');
  }

  if (comparison.needsUpload.length > 0) {
    console.log(`${colors.yellow}2. Upload updated data:${colors.reset}`);
    console.log('   node scripts/firebase-push-updates.js');
  }

  if (comparison.synced.length === Object.keys(firestoreStatus).length) {
    console.log(`${colors.green}All data is synced! No action needed.${colors.reset}`);
  }

  console.log('\n' + '═'.repeat(70));

  // Return summary for programmatic use
  return {
    localFiles,
    firestoreStatus,
    comparison,
    needsAction: comparison.missing.length > 0 || comparison.needsUpload.length > 0
  };
}

/**
 * Main function
 */
async function main() {
  // Check local files first (doesn't need Firebase)
  console.log('Checking local source files...');
  const localFiles = checkLocalFiles();

  // Try to initialize Firebase
  const firebaseInitialized = initFirebase();

  if (!firebaseInitialized) {
    console.log('\n' + '═'.repeat(70));
    console.log(`${colors.bright}${colors.yellow} FIREBASE NOT CONFIGURED${colors.reset}`);
    console.log('═'.repeat(70));
    console.log('\nTo enable Firebase sync, please:');
    console.log('1. Download service account key from Firebase Console');
    console.log('2. Save as: scripts/serviceAccountKey.json');
    console.log('\n📁 LOCAL FILES STATUS:');

    for (const [name, info] of Object.entries(localFiles)) {
      const icon = info.exists ? '✓' : '✗';
      const version = info.version ? ` (v${info.version})` : '';
      console.log(`${icon} ${name}${version}`);
    }

    console.log('\n' + '═'.repeat(70));
    process.exit(0);
  }

  const db = admin.firestore();

  console.log('Checking Firestore collections...');
  const firestoreStatus = await checkFirestoreCollections(db);

  const comparison = compareVersions(localFiles, firestoreStatus);
  const report = generateReport(localFiles, firestoreStatus, comparison);

  // Save report to file
  const reportPath = path.join(ROOT_DIR, 'firebase-status-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\nReport saved to: ${reportPath}`);

  process.exit(report.needsAction ? 1 : 0);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
