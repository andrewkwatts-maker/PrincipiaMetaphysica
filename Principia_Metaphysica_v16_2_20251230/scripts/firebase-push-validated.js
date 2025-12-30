/**
 * Firebase Push with Full Validation
 *
 * Enhanced push script with:
 * - OOM validation for all critical parameters
 * - Derivation chain validation (formulas must link to established physics)
 * - Complete diff display with mandatory confirmation
 * - Version history tracking
 * - Regression blocking
 *
 * Usage: node scripts/firebase-push-validated.js [--force]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const vm = require('vm');

const ROOT_DIR = path.join(__dirname, '..');
const FORCE_MODE = process.argv.includes('--force');

// Colors
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bgRed: '\x1b[41m',
  bgGreen: '\x1b[42m'
};

// Critical OOM parameters
const OOM_CRITICAL_VALUES = [
  { path: 'proton_decay.M_GUT', name: 'M_GUT', experimental: 2e16, tolerance: 1 },
  { path: 'proton_decay.tau_p_median', name: 'τ_p', experimental: 1.67e34, tolerance: 1 },
  { path: 'pmns_matrix.theta_23', name: 'θ₂₃', experimental: 45.0, tolerance: 0.1 },
  { path: 'pmns_matrix.theta_12', name: 'θ₁₂', experimental: 33.41, tolerance: 0.1 },
  { path: 'pmns_matrix.theta_13', name: 'θ₁₃', experimental: 8.54, tolerance: 0.1 },
  { path: 'dark_energy.w0_PM', name: 'w₀', experimental: -0.83, tolerance: 0.1 }
];

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

  const serviceAccount = require(serviceAccountPath);
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: "principia-metaphysica"
  });

  return admin.firestore();
}

/**
 * Get nested value from object
 */
function getNestedValue(obj, path) {
  return path.split('.').reduce((acc, part) => acc?.[part], obj);
}

/**
 * Calculate OOM difference
 */
function oomDiff(value, experimental) {
  if (value === 0 || experimental === 0) return Infinity;
  return Math.abs(Math.log10(Math.abs(value)) - Math.log10(Math.abs(experimental)));
}

/**
 * Load formula definitions
 */
function loadFormulaDefinitions() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-definitions.js');
  const content = fs.readFileSync(filePath, 'utf-8');
  const sandbox = { PM_FORMULAS: null };
  const script = new vm.Script(content + '\nPM_FORMULAS;');
  return script.runInNewContext(sandbox);
}

/**
 * Validate derivation chains
 */
function validateDerivationChains(formulas) {
  const results = {
    valid: [],
    warnings: [],
    errors: []
  };

  const establishedIds = new Set();

  // Collect established formula IDs
  for (const formula of formulas) {
    if (formula.category === 'ESTABLISHED') {
      establishedIds.add(formula.id);
    }
  }

  // Validate each non-established formula
  for (const formula of formulas) {
    if (formula.category === 'ESTABLISHED') {
      results.valid.push({ id: formula.id, status: 'ESTABLISHED (foundation)' });
      continue;
    }

    // Check for derivation references
    if (formula.derivesFrom && formula.derivesFrom.length > 0) {
      let hasEstablishedRoot = false;
      const chain = [];

      for (const ref of formula.derivesFrom) {
        if (establishedIds.has(ref)) {
          hasEstablishedRoot = true;
        }
        chain.push(ref);
      }

      if (hasEstablishedRoot) {
        results.valid.push({
          id: formula.id,
          status: 'Valid chain',
          chain: chain
        });
      } else {
        results.warnings.push({
          id: formula.id,
          warning: 'Chain does not reach established physics',
          chain: chain
        });
      }
    } else if (formula.attribution) {
      // Has citation/attribution
      results.valid.push({
        id: formula.id,
        status: 'Has attribution',
        attribution: formula.attribution
      });
    } else if (formula.foundational) {
      // Marked as foundational
      results.valid.push({
        id: formula.id,
        status: 'Marked foundational'
      });
    } else {
      // No derivation chain
      results.warnings.push({
        id: formula.id,
        warning: 'No derivation chain or attribution',
        category: formula.category
      });
    }
  }

  return results;
}

/**
 * Prompt user for confirmation
 */
async function confirm(prompt) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise(resolve => {
    rl.question(`${prompt} (Y/N): `, answer => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

/**
 * Load local data
 */
function loadLocalData() {
  const theoryPath = path.join(ROOT_DIR, 'theory_output.json');
  let content = fs.readFileSync(theoryPath, 'utf-8');
  content = content.replace(/:\s*NaN\b/g, ': null');
  return JSON.parse(content);
}

/**
 * Deep diff two objects
 */
function deepDiff(local, remote, path = '') {
  const diffs = [];

  const allKeys = new Set([...Object.keys(local || {}), ...Object.keys(remote || {})]);

  for (const key of allKeys) {
    const newPath = path ? `${path}.${key}` : key;
    const localVal = local?.[key];
    const remoteVal = remote?.[key];

    if (localVal === undefined && remoteVal !== undefined) {
      diffs.push({ path: newPath, type: 'removed', oldValue: remoteVal });
    } else if (remoteVal === undefined && localVal !== undefined) {
      diffs.push({ path: newPath, type: 'added', newValue: localVal });
    } else if (typeof localVal === 'object' && typeof remoteVal === 'object' && !Array.isArray(localVal)) {
      diffs.push(...deepDiff(localVal, remoteVal, newPath));
    } else if (JSON.stringify(localVal) !== JSON.stringify(remoteVal)) {
      diffs.push({ path: newPath, type: 'changed', oldValue: remoteVal, newValue: localVal });
    }
  }

  return diffs;
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(80));
  console.log(`${c.bright}${c.cyan} PRINCIPIA METAPHYSICA - VALIDATED FIREBASE PUSH${c.reset}`);
  console.log('═'.repeat(80));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Force mode: ${FORCE_MODE}\n`);

  const db = initFirebase();

  // ─────────────────────────────────────────────────────────────────────────
  // STEP 1: Load and validate formula derivation chains
  // ─────────────────────────────────────────────────────────────────────────
  console.log(`${c.bright}[1/5] DERIVATION CHAIN VALIDATION${c.reset}`);
  console.log('─'.repeat(60));

  const pmFormulas = loadFormulaDefinitions();
  const allFormulas = [];

  for (const category of ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS']) {
    if (pmFormulas[category]) {
      for (const [key, formula] of Object.entries(pmFormulas[category])) {
        allFormulas.push({ ...formula, key, category });
      }
    }
  }

  const chainValidation = validateDerivationChains(allFormulas);

  console.log(`  Total formulas: ${allFormulas.length}`);
  console.log(`  ${c.green}✓ Valid chains: ${chainValidation.valid.length}${c.reset}`);
  console.log(`  ${c.yellow}⚠ Warnings: ${chainValidation.warnings.length}${c.reset}`);
  console.log(`  ${c.red}✗ Errors: ${chainValidation.errors.length}${c.reset}`);

  if (chainValidation.warnings.length > 0) {
    console.log(`\n  ${c.yellow}Warnings:${c.reset}`);
    chainValidation.warnings.slice(0, 5).forEach(w => {
      console.log(`    - ${w.id}: ${w.warning}`);
    });
    if (chainValidation.warnings.length > 5) {
      console.log(`    ... and ${chainValidation.warnings.length - 5} more`);
    }
  }

  if (chainValidation.errors.length > 0 && !FORCE_MODE) {
    console.log(`\n${c.red}${c.bright}BLOCKED: Derivation chain errors found${c.reset}`);
    console.log('Use --force to override (NOT RECOMMENDED)');
    process.exit(1);
  }

  // ─────────────────────────────────────────────────────────────────────────
  // STEP 2: Load local and remote data
  // ─────────────────────────────────────────────────────────────────────────
  console.log(`\n${c.bright}[2/5] LOADING DATA${c.reset}`);
  console.log('─'.repeat(60));

  const localData = loadLocalData();
  console.log(`  Local version: ${localData.meta?.version || 'unknown'}`);

  let remoteData = null;
  try {
    const doc = await db.collection('theory_constants').doc('current').get();
    if (doc.exists) {
      remoteData = doc.data();
      console.log(`  Remote version: ${remoteData.meta?.version || 'unknown'}`);
    } else {
      console.log(`  ${c.yellow}Remote data not found (new upload)${c.reset}`);
    }
  } catch (error) {
    console.log(`  ${c.red}Error loading remote: ${error.message}${c.reset}`);
  }

  // ─────────────────────────────────────────────────────────────────────────
  // STEP 3: OOM Validation
  // ─────────────────────────────────────────────────────────────────────────
  console.log(`\n${c.bright}[3/5] OOM VALIDATION${c.reset}`);
  console.log('─'.repeat(60));

  console.log(`\n  ${'Parameter'.padEnd(15)} ${'Local'.padEnd(15)} ${'Exp'.padEnd(15)} ${'OOM Diff'.padEnd(10)} ${'Status'}`);
  console.log('  ' + '─'.repeat(70));

  let oomFailures = 0;
  let regressions = 0;

  for (const param of OOM_CRITICAL_VALUES) {
    const localValue = getNestedValue(localData, param.path);
    const remoteValue = remoteData ? getNestedValue(remoteData, param.path) : null;

    const localOOM = localValue !== null && localValue !== undefined ? oomDiff(localValue, param.experimental) : null;
    const remoteOOM = remoteValue !== null && remoteValue !== undefined ? oomDiff(remoteValue, param.experimental) : null;

    const localValid = localOOM !== null && localOOM <= param.tolerance;
    const regressed = remoteOOM !== null && localOOM !== null && localOOM > remoteOOM;

    let status = '';
    let statusColor = c.green;

    if (!localValid) {
      status = 'FAIL (OOM)';
      statusColor = c.red;
      oomFailures++;
    } else if (regressed) {
      status = 'REGRESSED';
      statusColor = c.yellow;
      regressions++;
    } else {
      status = 'PASS';
    }

    const localStr = localValue !== null ? (typeof localValue === 'number' ? localValue.toExponential(2) : String(localValue)) : 'N/A';
    const expStr = typeof param.experimental === 'number' ? param.experimental.toExponential(2) : String(param.experimental);
    const oomStr = localOOM !== null ? localOOM.toFixed(3) : 'N/A';

    console.log(`  ${param.name.padEnd(15)} ${localStr.padEnd(15)} ${expStr.padEnd(15)} ${oomStr.padEnd(10)} ${statusColor}${status}${c.reset}`);
  }

  console.log('  ' + '─'.repeat(70));

  if (oomFailures > 0 || regressions > 0) {
    console.log(`\n  ${c.red}${oomFailures} OOM failures, ${regressions} regressions${c.reset}`);

    if (!FORCE_MODE) {
      console.log(`\n${c.red}${c.bright}BLOCKED: Validation failures detected${c.reset}`);
      process.exit(1);
    }
  } else {
    console.log(`\n  ${c.green}✓ All OOM validations passed${c.reset}`);
  }

  // ─────────────────────────────────────────────────────────────────────────
  // STEP 4: Display diff
  // ─────────────────────────────────────────────────────────────────────────
  console.log(`\n${c.bright}[4/5] CHANGES DIFF${c.reset}`);
  console.log('─'.repeat(60));

  if (remoteData) {
    const diffs = deepDiff(localData, remoteData);
    const changed = diffs.filter(d => d.type === 'changed');
    const added = diffs.filter(d => d.type === 'added');
    const removed = diffs.filter(d => d.type === 'removed');

    console.log(`\n  Total changes: ${diffs.length}`);
    console.log(`    ${c.yellow}Changed: ${changed.length}${c.reset}`);
    console.log(`    ${c.green}Added: ${added.length}${c.reset}`);
    console.log(`    ${c.red}Removed: ${removed.length}${c.reset}`);

    if (changed.length > 0) {
      console.log(`\n  ${c.bright}Key changes:${c.reset}`);
      changed.slice(0, 10).forEach(d => {
        console.log(`    ${d.path}:`);
        console.log(`      ${c.red}- ${JSON.stringify(d.oldValue).slice(0, 50)}${c.reset}`);
        console.log(`      ${c.green}+ ${JSON.stringify(d.newValue).slice(0, 50)}${c.reset}`);
      });
    }
  } else {
    console.log(`  ${c.yellow}No remote data to compare (full upload)${c.reset}`);
  }

  // ─────────────────────────────────────────────────────────────────────────
  // STEP 5: Confirmation and push
  // ─────────────────────────────────────────────────────────────────────────
  console.log(`\n${c.bright}[5/5] CONFIRMATION${c.reset}`);
  console.log('─'.repeat(60));

  if (!FORCE_MODE) {
    console.log(`\n${c.bright}${c.yellow}MANDATORY CONFIRMATIONS REQUIRED${c.reset}\n`);

    const confirm1 = await confirm('[1/3] Have you reviewed the OOM validation table?');
    if (!confirm1) {
      console.log(`\n${c.red}Push cancelled.${c.reset}`);
      process.exit(0);
    }

    const confirm2 = await confirm('[2/3] Have you reviewed all changes?');
    if (!confirm2) {
      console.log(`\n${c.red}Push cancelled.${c.reset}`);
      process.exit(0);
    }

    const confirm3 = await confirm('[3/3] Do you want to push these changes to Firebase?');
    if (!confirm3) {
      console.log(`\n${c.red}Push cancelled.${c.reset}`);
      process.exit(0);
    }
  }

  // Push to Firebase using smart sync with history
  console.log(`\n${c.bright}Pushing to Firebase with version history...${c.reset}`);

  try {
    // Use the sync-with-history script
    const { syncWithHistory } = require('./firebase-sync-with-history.js');

    // Close current Firebase connection to avoid conflicts
    const currentApp = admin.app();
    await currentApp.delete();

    // Run sync (it will re-initialize Firebase)
    const syncResult = await syncWithHistory();

    // Re-initialize Firebase for validation history
    const serviceAccountPath = path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json');
    if (!fs.existsSync(serviceAccountPath)) {
      // Try alternate location
      const altPath = path.join(ROOT_DIR, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json');
      if (!fs.existsSync(altPath)) {
        throw new Error('Service account key not found after sync');
      }
    }

    const serviceAccount = require(serviceAccountPath);
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount),
      projectId: "principia-metaphysica"
    });

    const db2 = admin.firestore();

    // Create validation history entry
    const version = localData.meta?.version || '12.7';
    await db2.collection('validation_history').doc(`push_${Date.now()}`).set({
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      version: version,
      action: 'validated_push_with_history',
      sync_result: {
        updated: syncResult.updated,
        changes: syncResult.diffs,
        backupId: syncResult.backupId || null
      },
      derivation_validation: {
        valid: chainValidation.valid.length,
        warnings: chainValidation.warnings.length,
        errors: chainValidation.errors.length
      },
      oom_validation: {
        failures: oomFailures,
        regressions: regressions
      },
      forced: FORCE_MODE
    });

    console.log(`\n${c.green}${c.bright}✅ PUSH COMPLETE${c.reset}`);
    console.log(`  Version: ${version}`);
    if (syncResult.updated) {
      console.log(`  Changes: ${syncResult.diffs}`);
      console.log(`  Backup: ${syncResult.backupId}`);
    } else {
      console.log(`  Status: No changes (Firebase already up to date)`);
    }

  } catch (error) {
    console.error(`\n${c.red}❌ PUSH FAILED: ${error.message}${c.reset}`);
    process.exit(1);
  }

  process.exit(0);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
