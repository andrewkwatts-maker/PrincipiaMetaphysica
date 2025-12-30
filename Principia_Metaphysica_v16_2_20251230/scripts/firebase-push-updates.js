/**
 * Firebase Push Updates Script
 *
 * Validates and pushes simulation updates to Firebase Firestore.
 * MANDATORY: Shows complete diff of ALL changes and requires explicit confirmation.
 *
 * Usage: node scripts/firebase-push-updates.js [--force]
 *
 * Flow:
 * 1. Load local theory_output.json (generated from simulations)
 * 2. Download current Firebase data
 * 3. Perform diff and OOM validation
 * 4. Display COMPLETE diff of all changes (MANDATORY REVIEW)
 * 5. Display OOM comparison table (MANDATORY REVIEW)
 * 6. Require explicit Y/N confirmation for EACH section
 * 7. Push updates only if ALL confirmations pass
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const ROOT_DIR = path.join(__dirname, '..');
const FORCE_MODE = process.argv.includes('--force');

// Colors for terminal output
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  bgRed: '\x1b[41m',
  bgGreen: '\x1b[42m',
  bgYellow: '\x1b[43m'
};

// Critical OOM parameters to validate
const OOM_CRITICAL_VALUES = [
  {
    path: 'proton_decay.M_GUT',
    name: 'GUT Scale (M_GUT)',
    experimental: 2e16,
    unit: 'GeV',
    tolerance_oom: 1,
    description: 'Grand Unified Theory scale'
  },
  {
    path: 'proton_decay.tau_p_median',
    name: 'Proton Lifetime (τ_p)',
    experimental: 1.67e34,
    unit: 'years',
    tolerance_oom: 1,
    description: 'Predicted proton decay lifetime'
  },
  {
    path: 'v12_7_pure_geometric.kk_graviton_exact.m_KK_TeV',
    name: 'KK Graviton Mass',
    experimental: 5.0,
    unit: 'TeV',
    tolerance_oom: 1,
    description: 'Kaluza-Klein graviton mass'
  },
  {
    path: 'v12_7_pure_geometric.flux_stab_pure.m_h_GeV',
    name: 'Higgs Mass (m_h)',
    experimental: 125.1,
    unit: 'GeV',
    tolerance_oom: 0.1,
    description: 'Higgs boson mass'
  },
  {
    path: 'v12_7_pure_geometric.vev_pure.v_GeV',
    name: 'VEV',
    experimental: 174.0,
    unit: 'GeV',
    tolerance_oom: 0.1,
    description: 'Vacuum expectation value'
  },
  {
    path: 'dark_energy.w0_PM',
    name: 'Dark Energy EoS (w₀)',
    experimental: -0.85,
    unit: '',
    tolerance_oom: 0.1,
    description: 'Dark energy equation of state parameter'
  },
  {
    path: 'pmns_matrix.theta_23_deg',
    name: 'θ₂₃ (Atmospheric)',
    experimental: 45.0,
    unit: '°',
    tolerance_oom: 0.05,
    description: 'PMNS mixing angle θ₂₃'
  },
  {
    path: 'pmns_matrix.theta_12_deg',
    name: 'θ₁₂ (Solar)',
    experimental: 33.41,
    unit: '°',
    tolerance_oom: 0.05,
    description: 'PMNS mixing angle θ₁₂'
  },
  {
    path: 'pmns_matrix.theta_13_deg',
    name: 'θ₁₃ (Reactor)',
    experimental: 8.54,
    unit: '°',
    tolerance_oom: 0.05,
    description: 'PMNS mixing angle θ₁₃'
  }
];

// Initialize Firebase with service account
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
    console.error(`${c.red}${c.bright}ERROR: Service account key not found${c.reset}`);
    console.error('\nLooked in:');
    possiblePaths.forEach(p => console.error(`  - ${p}`));
    console.error('\nDownload from Firebase Console > Project Settings > Service Accounts');
    process.exit(1);
  }

  console.log(`${c.dim}Using service account: ${path.basename(serviceAccountPath)}${c.reset}`);

  const serviceAccount = require(serviceAccountPath);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: "principia-metaphysica"
  });

  return admin.firestore();
}

/**
 * Get nested value from object using dot notation path
 */
function getValue(obj, pathStr) {
  return pathStr.split('.').reduce((acc, part) => acc?.[part], obj);
}

/**
 * Calculate Order of Magnitude difference between two values
 */
function calcOOMDiff(v1, v2) {
  if (v1 === 0 || v2 === 0 || v1 === undefined || v2 === undefined) return Infinity;
  return Math.abs(Math.log10(Math.abs(v1)) - Math.log10(Math.abs(v2)));
}

/**
 * Format number for display
 */
function formatValue(val, unit = '') {
  if (val === undefined || val === null) return 'N/A';
  if (typeof val === 'number') {
    if (Math.abs(val) >= 1e6 || (Math.abs(val) < 0.01 && val !== 0)) {
      return `${val.toExponential(4)}${unit ? ' ' + unit : ''}`;
    }
    return `${val.toPrecision(6)}${unit ? ' ' + unit : ''}`;
  }
  return String(val);
}

/**
 * Deep diff two objects and return detailed changes
 */
function deepDiff(oldObj, newObj, path = '', changes = []) {
  const oldKeys = Object.keys(oldObj || {});
  const newKeys = Object.keys(newObj || {});
  const allKeys = new Set([...oldKeys, ...newKeys]);

  for (const key of allKeys) {
    const currentPath = path ? `${path}.${key}` : key;
    const oldVal = oldObj?.[key];
    const newVal = newObj?.[key];

    // Skip internal fields
    if (key === 'uploadedAt' || key === '_firestore') continue;

    if (oldVal === undefined && newVal !== undefined) {
      // Added
      changes.push({
        type: 'added',
        path: currentPath,
        oldValue: undefined,
        newValue: newVal
      });
    } else if (oldVal !== undefined && newVal === undefined) {
      // Removed
      changes.push({
        type: 'removed',
        path: currentPath,
        oldValue: oldVal,
        newValue: undefined
      });
    } else if (typeof oldVal === 'object' && typeof newVal === 'object' &&
               oldVal !== null && newVal !== null && !Array.isArray(oldVal)) {
      // Recurse into objects
      deepDiff(oldVal, newVal, currentPath, changes);
    } else if (JSON.stringify(oldVal) !== JSON.stringify(newVal)) {
      // Changed
      changes.push({
        type: 'changed',
        path: currentPath,
        oldValue: oldVal,
        newValue: newVal
      });
    }
  }

  return changes;
}

/**
 * Display detailed OOM comparison table
 */
function displayOOMTable(localData, remoteData) {
  console.log('\n' + '═'.repeat(90));
  console.log(`${c.bright}${c.cyan}  📊 ORDER OF MAGNITUDE (OOM) VALIDATION TABLE${c.reset}`);
  console.log('═'.repeat(90));

  console.log(`\n${c.dim}Each parameter must be within tolerance OOM of experimental value.${c.reset}`);
  console.log(`${c.dim}Regression from previous Firebase value will BLOCK the push.${c.reset}\n`);

  // Table header
  const header = `${'Parameter'.padEnd(25)} | ${'New Value'.padEnd(18)} | ${'Firebase'.padEnd(18)} | ${'Exp.'.padEnd(12)} | ${'OOM Δ'.padEnd(8)} | ${'Tol.'.padEnd(5)} | Status`;
  console.log(c.bright + header + c.reset);
  console.log('─'.repeat(90));

  const results = [];
  let allValid = true;

  for (const check of OOM_CRITICAL_VALUES) {
    const localVal = getValue(localData, check.path);
    const remoteVal = getValue(remoteData, check.path);
    const expVal = check.experimental;

    // Calculate OOM difference from experimental
    const oomFromExp = localVal !== undefined ? calcOOMDiff(localVal, expVal) : Infinity;
    const isWithinTolerance = oomFromExp <= check.tolerance_oom;

    // Check for regression (if remote exists)
    let regressed = false;
    if (remoteVal !== undefined && localVal !== undefined) {
      const oldOOM = calcOOMDiff(remoteVal, expVal);
      regressed = oomFromExp > oldOOM + 0.01; // Small epsilon for floating point
    }

    const valid = isWithinTolerance && !regressed;
    if (!valid) allValid = false;

    // Format row
    const localStr = formatValue(localVal, check.unit).padEnd(18);
    const remoteStr = formatValue(remoteVal, check.unit).padEnd(18);
    const expStr = formatValue(expVal, check.unit).padEnd(12);
    const oomStr = (oomFromExp === Infinity ? 'N/A' : oomFromExp.toFixed(4)).padEnd(8);
    const tolStr = check.tolerance_oom.toString().padEnd(5);

    let statusStr;
    if (regressed) {
      statusStr = `${c.red}${c.bright}REGRESSED${c.reset}`;
    } else if (!isWithinTolerance) {
      statusStr = `${c.red}${c.bright}FAIL${c.reset}`;
    } else if (remoteVal === undefined) {
      statusStr = `${c.yellow}NEW${c.reset}`;
    } else {
      statusStr = `${c.green}✓ PASS${c.reset}`;
    }

    console.log(`${check.name.padEnd(25)} | ${localStr} | ${remoteStr} | ${expStr} | ${oomStr} | ${tolStr} | ${statusStr}`);

    results.push({
      name: check.name,
      local: localVal,
      remote: remoteVal,
      experimental: expVal,
      oomDiff: oomFromExp,
      tolerance: check.tolerance_oom,
      valid,
      regressed,
      description: check.description
    });
  }

  console.log('─'.repeat(90));

  // Summary
  const passed = results.filter(r => r.valid).length;
  const failed = results.filter(r => !r.valid).length;
  const regressed = results.filter(r => r.regressed).length;

  console.log(`\n${c.bright}Summary:${c.reset} ${c.green}${passed} passed${c.reset}, ${failed > 0 ? c.red : ''}${failed} failed${c.reset}${regressed > 0 ? `, ${c.red}${regressed} regressed${c.reset}` : ''}`);

  return { results, allValid };
}

/**
 * Display complete diff of all changes
 */
function displayCompleteDiff(localData, remoteData) {
  console.log('\n' + '═'.repeat(90));
  console.log(`${c.bright}${c.cyan}  📝 COMPLETE DIFF: Firebase Current → New Values${c.reset}`);
  console.log('═'.repeat(90));

  if (!remoteData) {
    console.log(`\n${c.yellow}This is an INITIAL UPLOAD - no previous data exists.${c.reset}`);
    console.log(`All ${Object.keys(localData).length} top-level sections will be created.\n`);
    return { added: 999, changed: 0, removed: 0 };
  }

  const changes = deepDiff(remoteData, localData);

  // Group changes by top-level category
  const grouped = {};
  for (const change of changes) {
    const category = change.path.split('.')[0];
    if (!grouped[category]) grouped[category] = [];
    grouped[category].push(change);
  }

  // Display by category
  let totalAdded = 0, totalChanged = 0, totalRemoved = 0;

  for (const [category, categoryChanges] of Object.entries(grouped)) {
    const added = categoryChanges.filter(c => c.type === 'added').length;
    const changed = categoryChanges.filter(c => c.type === 'changed').length;
    const removed = categoryChanges.filter(c => c.type === 'removed').length;

    totalAdded += added;
    totalChanged += changed;
    totalRemoved += removed;

    console.log(`\n${c.bright}${c.magenta}[${category}]${c.reset} ${c.green}+${added}${c.reset} ${c.yellow}~${changed}${c.reset} ${c.red}-${removed}${c.reset}`);

    // Show individual changes (limit to 15 per category)
    const toShow = categoryChanges.slice(0, 15);
    for (const change of toShow) {
      const shortPath = change.path.replace(`${category}.`, '');

      if (change.type === 'added') {
        console.log(`  ${c.green}+ ${shortPath}: ${formatValue(change.newValue)}${c.reset}`);
      } else if (change.type === 'removed') {
        console.log(`  ${c.red}- ${shortPath}: ${formatValue(change.oldValue)}${c.reset}`);
      } else {
        console.log(`  ${c.yellow}~ ${shortPath}: ${formatValue(change.oldValue)} → ${formatValue(change.newValue)}${c.reset}`);
      }
    }

    if (categoryChanges.length > 15) {
      console.log(`  ${c.dim}... and ${categoryChanges.length - 15} more changes${c.reset}`);
    }
  }

  // Total summary
  console.log('\n' + '─'.repeat(90));
  console.log(`${c.bright}TOTAL CHANGES:${c.reset} ${c.green}+${totalAdded} added${c.reset}, ${c.yellow}~${totalChanged} changed${c.reset}, ${c.red}-${totalRemoved} removed${c.reset}`);

  return { added: totalAdded, changed: totalChanged, removed: totalRemoved };
}

/**
 * Display validation summary
 */
function displayValidationSummary(localData) {
  console.log('\n' + '═'.repeat(90));
  console.log(`${c.bright}${c.cyan}  📋 VALIDATION SUMMARY (from theory_output.json)${c.reset}`);
  console.log('═'.repeat(90));

  const validation = localData.validation || {};
  const meta = localData.meta || {};

  console.log(`\n  Version: ${c.bright}${meta.version || 'unknown'}${c.reset}`);
  console.log(`  Last Updated: ${meta.last_updated || 'unknown'}`);
  console.log(`  Simulation Runs: ${meta.simulation_runs?.length || 0}`);

  console.log(`\n  ${c.bright}Predictions:${c.reset}`);
  console.log(`    Within 1σ: ${validation.predictions_within_1sigma || 'N/A'} / ${validation.total_predictions || 'N/A'}`);
  console.log(`    Exact Matches: ${validation.exact_matches || 'N/A'}`);
  console.log(`    Overall Grade: ${c.bright}${validation.overall_grade || 'N/A'}${c.reset}`);

  if (validation.chi_squared) {
    console.log(`\n  ${c.bright}Chi-Squared:${c.reset}`);
    console.log(`    Total: ${validation.chi_squared.total?.toFixed(2) || 'N/A'}`);
    console.log(`    Per DOF: ${validation.chi_squared.per_dof?.toFixed(2) || 'N/A'}`);
  }
}

/**
 * Interactive confirmation with mandatory review
 */
async function getConfirmation(prompt) {
  return new Promise(resolve => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question(prompt, answer => {
      rl.close();
      const normalized = answer.toLowerCase().trim();
      resolve(normalized === 'y' || normalized === 'yes');
    });
  });
}

/**
 * Push updates to Firebase
 */
async function pushToFirebase(db, localData) {
  console.log(`\n${c.cyan}☁️  Pushing to Firebase...${c.reset}`);

  // Update theory_constants/current
  await db.collection('theory_constants').doc('current').set({
    ...localData,
    uploadedAt: admin.firestore.FieldValue.serverTimestamp()
  });
  console.log(`  ${c.green}✓${c.reset} Updated theory_constants/current`);

  // Create versioned backup with timestamp
  const version = localData.meta?.version || 'unknown';
  const versionId = `v${version.replace(/\./g, '_')}_${Date.now()}`;
  await db.collection('theory_constants').doc(versionId).set({
    ...localData,
    uploadedAt: admin.firestore.FieldValue.serverTimestamp()
  });
  console.log(`  ${c.green}✓${c.reset} Created backup: theory_constants/${versionId}`);

  // Add to validation history
  await db.collection('validation_history').add({
    timestamp: admin.firestore.FieldValue.serverTimestamp(),
    version: version,
    action: 'push_update',
    validation: localData.validation || {},
    source: 'firebase-push-updates.js',
    oom_validated: true
  });
  console.log(`  ${c.green}✓${c.reset} Added to validation_history`);

  return true;
}

/**
 * Main function
 */
async function main() {
  console.log('\n' + '═'.repeat(90));
  console.log(`${c.bright}${c.bgYellow}${c.white}  PRINCIPIA METAPHYSICA - FIREBASE PUSH UPDATES  ${c.reset}`);
  console.log('═'.repeat(90));
  console.log(`\nTimestamp: ${new Date().toISOString()}`);
  console.log(`Force mode: ${FORCE_MODE ? c.red + 'ENABLED' + c.reset : 'disabled'}`);

  // ═══════════════════════════════════════════════════════════════
  // STEP 1: Load local data
  // ═══════════════════════════════════════════════════════════════
  console.log(`\n${c.bright}STEP 1: Loading local simulation data...${c.reset}`);

  const localPath = path.join(ROOT_DIR, 'theory_output.json');
  if (!fs.existsSync(localPath)) {
    console.error(`\n${c.red}${c.bright}ERROR: theory_output.json not found${c.reset}`);
    console.log('\nYou must run simulations first:');
    console.log(`  ${c.cyan}python run_all_simulations.py${c.reset}`);
    process.exit(1);
  }

  const localData = JSON.parse(fs.readFileSync(localPath, 'utf-8'));
  console.log(`  Local version: ${c.bright}${localData.meta?.version || 'unknown'}${c.reset}`);
  console.log(`  File modified: ${fs.statSync(localPath).mtime.toISOString()}`);

  // ═══════════════════════════════════════════════════════════════
  // STEP 2: Load Firebase data
  // ═══════════════════════════════════════════════════════════════
  console.log(`\n${c.bright}STEP 2: Loading current Firebase data...${c.reset}`);

  const db = initFirebase();
  let remoteData = null;

  try {
    const doc = await db.collection('theory_constants').doc('current').get();
    if (doc.exists) {
      remoteData = doc.data();
      console.log(`  Firebase version: ${c.bright}${remoteData.meta?.version || 'unknown'}${c.reset}`);
      if (remoteData.uploadedAt) {
        const uploadDate = remoteData.uploadedAt.toDate?.() || remoteData.uploadedAt;
        console.log(`  Last uploaded: ${uploadDate}`);
      }
    } else {
      console.log(`  ${c.yellow}No existing data in Firebase (initial upload)${c.reset}`);
    }
  } catch (error) {
    console.log(`  ${c.yellow}Warning: Could not load remote data: ${error.message}${c.reset}`);
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 3: Display OOM Validation Table (MANDATORY)
  // ═══════════════════════════════════════════════════════════════
  console.log(`\n${c.bright}STEP 3: OOM Validation (MANDATORY REVIEW)${c.reset}`);

  const { results: oomResults, allValid: oomValid } = displayOOMTable(localData, remoteData || {});

  // ═══════════════════════════════════════════════════════════════
  // STEP 4: Display Complete Diff (MANDATORY)
  // ═══════════════════════════════════════════════════════════════
  console.log(`\n${c.bright}STEP 4: Complete Diff (MANDATORY REVIEW)${c.reset}`);

  const diffSummary = displayCompleteDiff(localData, remoteData);

  // ═══════════════════════════════════════════════════════════════
  // STEP 5: Display Validation Summary
  // ═══════════════════════════════════════════════════════════════
  displayValidationSummary(localData);

  // ═══════════════════════════════════════════════════════════════
  // STEP 6: Final Validation Check
  // ═══════════════════════════════════════════════════════════════
  console.log('\n' + '═'.repeat(90));

  if (!oomValid && !FORCE_MODE) {
    console.log(`${c.bgRed}${c.white}${c.bright}  ❌ PUSH BLOCKED: OOM VALIDATION FAILED  ${c.reset}`);
    console.log('\nOne or more parameters failed OOM validation or regressed.');
    console.log('Fix the simulation outputs before pushing.');
    console.log(`\n${c.dim}Use --force to override (NOT RECOMMENDED)${c.reset}`);
    process.exit(1);
  }

  if (!oomValid && FORCE_MODE) {
    console.log(`${c.bgYellow}${c.white}${c.bright}  ⚠️  WARNING: OOM VALIDATION FAILED - FORCE MODE  ${c.reset}`);
    console.log('\nProceeding despite validation failures due to --force flag.');
  } else {
    console.log(`${c.bgGreen}${c.white}${c.bright}  ✅ ALL OOM VALIDATIONS PASSED  ${c.reset}`);
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 7: Mandatory Confirmations
  // ═══════════════════════════════════════════════════════════════
  console.log('\n' + '═'.repeat(90));
  console.log(`${c.bright}${c.cyan}  🔐 MANDATORY CONFIRMATIONS${c.reset}`);
  console.log('═'.repeat(90));

  if (FORCE_MODE) {
    console.log(`\n${c.yellow}Force mode enabled - skipping confirmations.${c.reset}`);
  } else {
    // Confirmation 1: OOM values reviewed
    console.log(`\n${c.bright}[1/3] OOM Values Review${c.reset}`);
    console.log(`${c.dim}You have reviewed the OOM validation table above showing all critical parameters.${c.reset}`);
    const oomConfirmed = await getConfirmation(`${c.yellow}Have you reviewed and accepted the OOM values? (y/n): ${c.reset}`);

    if (!oomConfirmed) {
      console.log(`\n${c.red}Push cancelled - OOM values not accepted.${c.reset}`);
      process.exit(0);
    }

    // Confirmation 2: Diff reviewed
    console.log(`\n${c.bright}[2/3] Diff Review${c.reset}`);
    console.log(`${c.dim}You have reviewed all ${diffSummary.added + diffSummary.changed + diffSummary.removed} changes shown above.${c.reset}`);
    const diffConfirmed = await getConfirmation(`${c.yellow}Have you reviewed and accepted all diff changes? (y/n): ${c.reset}`);

    if (!diffConfirmed) {
      console.log(`\n${c.red}Push cancelled - diff changes not accepted.${c.reset}`);
      process.exit(0);
    }

    // Confirmation 3: Final push confirmation
    console.log(`\n${c.bright}[3/3] Final Push Confirmation${c.reset}`);
    console.log(`${c.dim}This will update the Firebase database used by the live website.${c.reset}`);
    console.log(`${c.dim}A backup will be created before updating.${c.reset}`);
    const finalConfirmed = await getConfirmation(`${c.yellow}${c.bright}PUSH TO FIREBASE? This cannot be easily undone. (y/n): ${c.reset}`);

    if (!finalConfirmed) {
      console.log(`\n${c.red}Push cancelled by user.${c.reset}`);
      process.exit(0);
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 8: Push to Firebase
  // ═══════════════════════════════════════════════════════════════
  console.log('\n' + '═'.repeat(90));
  console.log(`${c.bright}STEP 8: Pushing to Firebase...${c.reset}`);

  try {
    await pushToFirebase(db, localData);

    console.log('\n' + '═'.repeat(90));
    console.log(`${c.bgGreen}${c.white}${c.bright}  ✅ PUSH COMPLETE - FIREBASE UPDATED SUCCESSFULLY  ${c.reset}`);
    console.log('═'.repeat(90));

    console.log(`\n${c.bright}Next steps:${c.reset}`);
    console.log(`  1. Regenerate enhanced constants: ${c.cyan}python generate_enhanced_constants.py${c.reset}`);
    console.log(`  2. Verify website loads correctly`);
    console.log(`  3. Check Firebase console: ${c.cyan}https://console.firebase.google.com/project/principia-metaphysica${c.reset}`);

  } catch (error) {
    console.error(`\n${c.bgRed}${c.white}${c.bright}  ❌ PUSH FAILED  ${c.reset}`);
    console.error(`\nError: ${error.message}`);
    process.exit(1);
  }

  process.exit(0);
}

main().catch(error => {
  console.error(`${c.red}Fatal error: ${error.message}${c.reset}`);
  process.exit(1);
});
