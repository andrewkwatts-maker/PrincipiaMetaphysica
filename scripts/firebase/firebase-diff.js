/**
 * Firebase Diff Tool
 *
 * Compares local simulation output with Firebase Firestore data
 * and generates a detailed diff report with OOM validation.
 *
 * Usage: node scripts/firebase-diff.js
 *
 * Validates:
 * - All OOM values are within 1 OOM of experimental
 * - All predictions are better than or equal to previous version
 * - No regressions in accuracy
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

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

// Key values to track for OOM validation
const OOM_CRITICAL_VALUES = [
  { path: 'proton_decay.M_GUT', name: 'GUT Scale', experimental: 2e16, tolerance_oom: 1 },
  { path: 'proton_decay.tau_p_median', name: 'Proton Lifetime', experimental: 1.67e34, tolerance_oom: 1 },
  { path: 'v12_7_pure_geometric.kk_graviton_exact.m_KK_TeV', name: 'KK Graviton Mass', experimental: 5.0, tolerance_oom: 1 },
  { path: 'v12_7_pure_geometric.flux_stab_pure.m_h_GeV', name: 'Higgs Mass', experimental: 125.1, tolerance_oom: 0.1 },
  { path: 'v12_7_pure_geometric.vev_pure.v_GeV', name: 'VEV', experimental: 174.0, tolerance_oom: 0.1 },
  { path: 'pmns_matrix.theta_23', name: 'Theta 23', experimental: 45.0, tolerance_oom: 0.1 },
  { path: 'dark_energy.w0_PM', name: 'w0 Dark Energy', experimental: -0.83, tolerance_oom: 0.1 }
];

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

  const serviceAccount = require(serviceAccountPath);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: "principia-metaphysica"
  });

  return admin.firestore();
}

/**
 * Get nested value from object by path
 */
function getNestedValue(obj, path) {
  return path.split('.').reduce((acc, part) => acc?.[part], obj);
}

/**
 * Calculate order of magnitude
 */
function getOOM(value) {
  if (value === 0) return 0;
  return Math.log10(Math.abs(value));
}

/**
 * Calculate OOM difference
 */
function oomDiff(value1, value2) {
  if (value1 === 0 || value2 === 0) return Infinity;
  return Math.abs(getOOM(value1) - getOOM(value2));
}

/**
 * Deep diff two objects
 */
function deepDiff(obj1, obj2, path = '') {
  const diffs = [];

  const allKeys = new Set([...Object.keys(obj1 || {}), ...Object.keys(obj2 || {})]);

  for (const key of allKeys) {
    const newPath = path ? `${path}.${key}` : key;
    const val1 = obj1?.[key];
    const val2 = obj2?.[key];

    if (val1 === undefined) {
      diffs.push({ path: newPath, type: 'added', newValue: val2 });
    } else if (val2 === undefined) {
      diffs.push({ path: newPath, type: 'removed', oldValue: val1 });
    } else if (typeof val1 === 'object' && typeof val2 === 'object' && !Array.isArray(val1)) {
      diffs.push(...deepDiff(val1, val2, newPath));
    } else if (JSON.stringify(val1) !== JSON.stringify(val2)) {
      diffs.push({
        path: newPath,
        type: 'changed',
        oldValue: val1,
        newValue: val2
      });
    }
  }

  return diffs;
}

/**
 * Validate OOM values
 */
function validateOOM(localData, remoteData) {
  const results = [];

  for (const check of OOM_CRITICAL_VALUES) {
    const localValue = getNestedValue(localData, check.path);
    const remoteValue = getNestedValue(remoteData, check.path);

    const localOOM = localValue !== undefined ? oomDiff(localValue, check.experimental) : null;
    const remoteOOM = remoteValue !== undefined ? oomDiff(remoteValue, check.experimental) : null;

    const localValid = localOOM !== null && localOOM <= check.tolerance_oom;
    const remoteValid = remoteOOM !== null && remoteOOM <= check.tolerance_oom;

    // Check if local is better than or equal to remote
    const improvement = localOOM !== null && remoteOOM !== null ? remoteOOM - localOOM : null;
    const isBetter = improvement === null || improvement >= 0;

    results.push({
      name: check.name,
      path: check.path,
      experimental: check.experimental,
      tolerance_oom: check.tolerance_oom,
      local: {
        value: localValue,
        oom_diff: localOOM,
        valid: localValid
      },
      remote: {
        value: remoteValue,
        oom_diff: remoteOOM,
        valid: remoteValid
      },
      improvement,
      isBetter,
      status: localValid && isBetter ? 'PASS' : 'FAIL'
    });
  }

  return results;
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(70));
  console.log(`${c.bright}${c.cyan} PRINCIPIA METAPHYSICA - FIREBASE DIFF TOOL${c.reset}`);
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  // Load local data
  console.log('📁 Loading local data...');
  const localPath = path.join(ROOT_DIR, 'theory_output.json');

  if (!fs.existsSync(localPath)) {
    console.error('ERROR: theory_output.json not found');
    process.exit(1);
  }

  const localData = JSON.parse(fs.readFileSync(localPath, 'utf-8'));
  console.log(`  Local version: ${localData.meta?.version || 'unknown'}`);

  // Load remote data
  console.log('\n☁️  Loading remote data...');
  const db = initFirebase();

  let remoteData = null;
  try {
    const doc = await db.collection('theory_constants').doc('current').get();
    if (doc.exists) {
      remoteData = doc.data();
      console.log(`  Remote version: ${remoteData.meta?.version || 'unknown'}`);
    } else {
      console.log('  Remote data not found (new upload needed)');
    }
  } catch (error) {
    console.log(`  Error loading remote: ${error.message}`);
  }

  // Perform diff
  console.log('\n' + '─'.repeat(70));
  console.log(`${c.bright}📊 DIFF ANALYSIS${c.reset}`);
  console.log('─'.repeat(70));

  if (!remoteData) {
    console.log(`${c.yellow}No remote data to compare. Full upload will be required.${c.reset}`);
  } else {
    const diffs = deepDiff(localData, remoteData);
    const changedDiffs = diffs.filter(d => d.type === 'changed');
    const addedDiffs = diffs.filter(d => d.type === 'added');
    const removedDiffs = diffs.filter(d => d.type === 'removed');

    console.log(`\nChanges detected: ${diffs.length}`);
    console.log(`  ${c.yellow}Changed: ${changedDiffs.length}${c.reset}`);
    console.log(`  ${c.green}Added: ${addedDiffs.length}${c.reset}`);
    console.log(`  ${c.red}Removed: ${removedDiffs.length}${c.reset}`);

    // Show first 10 changes
    if (changedDiffs.length > 0) {
      console.log(`\n${c.bright}Key Changes:${c.reset}`);
      changedDiffs.slice(0, 10).forEach(d => {
        const oldStr = typeof d.oldValue === 'number' ? d.oldValue.toExponential(4) : JSON.stringify(d.oldValue).slice(0, 30);
        const newStr = typeof d.newValue === 'number' ? d.newValue.toExponential(4) : JSON.stringify(d.newValue).slice(0, 30);
        console.log(`  ${d.path}:`);
        console.log(`    ${c.red}- ${oldStr}${c.reset}`);
        console.log(`    ${c.green}+ ${newStr}${c.reset}`);
      });
      if (changedDiffs.length > 10) {
        console.log(`  ... and ${changedDiffs.length - 10} more changes`);
      }
    }
  }

  // OOM Validation
  console.log('\n' + '─'.repeat(70));
  console.log(`${c.bright}🔬 OOM VALIDATION${c.reset}`);
  console.log('─'.repeat(70));

  const oomResults = validateOOM(localData, remoteData || {});
  let allPassed = true;

  console.log('\n' + '┌' + '─'.repeat(68) + '┐');
  console.log('│' + ' Parameter'.padEnd(25) + '│' + ' Local OOM'.padEnd(12) + '│' + ' Remote OOM'.padEnd(13) + '│' + ' Status'.padEnd(15) + '│');
  console.log('├' + '─'.repeat(68) + '┤');

  for (const result of oomResults) {
    const localOOM = result.local.oom_diff !== null ? result.local.oom_diff.toFixed(3) : 'N/A';
    const remoteOOM = result.remote.oom_diff !== null ? result.remote.oom_diff.toFixed(3) : 'N/A';
    const statusColor = result.status === 'PASS' ? c.green : c.red;
    const statusIcon = result.status === 'PASS' ? '✓' : '✗';

    console.log(`│ ${result.name.padEnd(23)} │ ${localOOM.padEnd(10)} │ ${remoteOOM.padEnd(11)} │ ${statusColor}${statusIcon} ${result.status}${c.reset}`.padEnd(80) + '│');

    if (result.status === 'FAIL') allPassed = false;
  }

  console.log('└' + '─'.repeat(68) + '┘');

  // Summary
  console.log('\n' + '═'.repeat(70));

  if (allPassed) {
    console.log(`${c.green}${c.bright} ✅ ALL VALIDATIONS PASSED${c.reset}`);
    console.log('\nAll OOM values are within tolerance and no regressions detected.');
    console.log('Safe to push updates to Firebase.');
  } else {
    console.log(`${c.red}${c.bright} ❌ VALIDATION FAILED${c.reset}`);
    console.log('\nSome values failed OOM validation or regressed from previous version.');
    console.log('Review changes before pushing to Firebase.');
  }

  console.log('═'.repeat(70));

  // Save report
  const reportPath = path.join(ROOT_DIR, 'firebase-diff-report.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    localVersion: localData.meta?.version,
    remoteVersion: remoteData?.meta?.version,
    oomValidation: oomResults,
    allPassed
  }, null, 2));

  console.log(`\nReport saved to: ${reportPath}`);

  process.exit(allPassed ? 0 : 1);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
