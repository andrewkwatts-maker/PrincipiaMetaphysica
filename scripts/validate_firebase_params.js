#!/usr/bin/env node
/**
 * Firebase Parameter Validation Script (v12.9)
 *
 * Validates that all critical parameters in Firebase match expected values
 * from the authoritative sources (config.py, theory_output.json)
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

// Initialize Firebase
const serviceAccountPath = path.join(__dirname, 'principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json');
if (!fs.existsSync(serviceAccountPath)) {
  console.error('ERROR: Firebase service account file not found');
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// Expected values from config.py (v12.9)
const EXPECTED_VALUES = {
  // Shadow Dimension Parameters
  shadow_kuf: { value: 0.576152, tolerance: 0.000001, description: 'Sitra Shadow Coupling (ק)' },
  shadow_chet: { value: 0.576152, tolerance: 0.000001, description: 'Sitra Shadow Coupling (ח)' },
  d_eff: { value: 12.576, tolerance: 0.001, description: 'Effective dimension' },

  // Dark Energy
  w0_PM: { value: -0.8527, tolerance: 0.001, description: 'Dark energy equation of state' },

  // Hebrew Physics Parameters
  k_gimel: { value: 12.31, tolerance: 0.01, description: 'Warping parameter (k_ג)' },
  S_mem: { value: 40.0, tolerance: 0.1, description: 'Instanton action (S_מ)' },
  C_kaf: { value: 27.2, tolerance: 0.1, description: 'Flux normalization (C_כ)' },
  f_heh: { value: 4.5, tolerance: 0.1, description: 'Partition factor (f_ה)' },
  delta_lamed: { value: 1.2, tolerance: 0.1, description: 'Threshold correction (δ_ל)' },

  // Gate Mirror Letters (directionally aligned)
  gate_letters: {
    value: ['Ρ', 'Τ', 'Ζ', 'Ο', 'Ι', 'Σ', 'Π', 'Ω', 'Χ', 'Υ', 'Β', 'Κ'],
    type: 'array',
    description: 'Gate Mirror Greek letters'
  },

  // Foundation Mirror Letters (directionally aligned)
  foundation_letters: {
    value: ['Δ', 'Ε', 'Γ', 'Α', 'Λ', 'Μ', 'Ν', 'Ξ', 'Η', 'Θ', 'Φ', 'Ψ'],
    type: 'array',
    description: 'Foundation Mirror Greek letters'
  },

  // Directional alignment verification
  north_notation: { value: ['X_{Ρ–Δ}', 'X_{Τ–Ε}', 'X_{Ζ–Γ}'], type: 'array', description: 'North wall pairings (Γ=Earth)' },
  east_notation: { value: ['X_{Ο–Α}', 'X_{Ι–Λ}', 'X_{Σ–Μ}'], type: 'array', description: 'East wall pairings (Α=Air)' },
  south_notation: { value: ['X_{Π–Ν}', 'X_{Ω–Ξ}', 'X_{Χ–Η}'], type: 'array', description: 'South wall pairings (Π=Fire)' },
  west_notation: { value: ['X_{Υ–Θ}', 'X_{Β–Φ}', 'X_{Κ–Ψ}'], type: 'array', description: 'West wall pairings (Υ=Water)' },
};

// Paths to check in Firebase (all nested under 'current' document)
const FIREBASE_PATHS = {
  shadow_kuf: ['current', 'shared_dimensions.shadow_kuf'],
  shadow_chet: ['current', 'shared_dimensions.shadow_chet'],
  d_eff: ['current', 'shared_dimensions.d_eff'],
  w0_PM: ['current', 'dark_energy.w0_PM'],
  k_gimel: ['current', 'hebrew_physics_nomenclature.parameters.k_gimel.value'],
  S_mem: ['current', 'hebrew_physics_nomenclature.parameters.S_mem.value'],
  C_kaf: ['current', 'hebrew_physics_nomenclature.parameters.C_kaf.value'],
  f_heh: ['current', 'hebrew_physics_nomenclature.parameters.f_heh.value'],
  delta_lamed: ['current', 'hebrew_physics_nomenclature.parameters.delta_lamed.value'],
  gate_letters: ['current', 'shadow_dimension_nomenclature.gate_mirror.letters'],
  foundation_letters: ['current', 'shadow_dimension_nomenclature.foundation_mirror.letters'],
  north_notation: ['current', 'shadow_dimension_nomenclature.wall_pairings.north.notation'],
  east_notation: ['current', 'shadow_dimension_nomenclature.wall_pairings.east.notation'],
  south_notation: ['current', 'shadow_dimension_nomenclature.wall_pairings.south.notation'],
  west_notation: ['current', 'shadow_dimension_nomenclature.wall_pairings.west.notation'],
};

// Helper to get nested value
function getNestedValue(obj, path) {
  const parts = path.split('.');
  let current = obj;
  for (const part of parts) {
    if (current === undefined || current === null) return undefined;
    current = current[part];
  }
  return current;
}

// Compare values with tolerance
function compareValues(actual, expected, tolerance = 0) {
  if (expected.type === 'array') {
    if (!Array.isArray(actual)) return { match: false, reason: 'Not an array' };
    if (actual.length !== expected.value.length) return { match: false, reason: `Length mismatch: ${actual.length} vs ${expected.value.length}` };
    for (let i = 0; i < expected.value.length; i++) {
      if (actual[i] !== expected.value[i]) {
        return { match: false, reason: `Index ${i}: "${actual[i]}" vs "${expected.value[i]}"` };
      }
    }
    return { match: true };
  }

  if (typeof expected.value === 'number') {
    const tol = expected.tolerance || 0;
    const diff = Math.abs(actual - expected.value);
    if (diff > tol) {
      return { match: false, reason: `${actual} vs ${expected.value} (diff: ${diff.toFixed(6)})` };
    }
    return { match: true };
  }

  return { match: actual === expected.value };
}

async function validateFirebase() {
  console.log('═'.repeat(70));
  console.log(' FIREBASE PARAMETER VALIDATION (v12.9)');
  console.log('═'.repeat(70));
  console.log();

  const results = {
    passed: [],
    failed: [],
    missing: [],
  };

  // Fetch all theory_constants
  const theoryConstantsRef = db.collection('theory_constants');
  const snapshot = await theoryConstantsRef.get();

  const firebaseData = {};
  snapshot.forEach(doc => {
    firebaseData[doc.id] = doc.data();
  });

  console.log(`Fetched ${Object.keys(firebaseData).length} documents from theory_constants\n`);

  // Validate each parameter
  for (const [paramName, expected] of Object.entries(EXPECTED_VALUES)) {
    const pathInfo = FIREBASE_PATHS[paramName];
    if (!pathInfo) {
      results.missing.push({ param: paramName, reason: 'No path defined' });
      continue;
    }

    const [docId, fieldPath] = pathInfo;
    const doc = firebaseData[docId];

    if (!doc) {
      results.missing.push({ param: paramName, reason: `Document "${docId}" not found` });
      continue;
    }

    const actual = getNestedValue(doc, fieldPath);

    if (actual === undefined) {
      results.missing.push({ param: paramName, reason: `Field "${fieldPath}" not found in ${docId}` });
      continue;
    }

    const comparison = compareValues(actual, expected);

    if (comparison.match) {
      results.passed.push({ param: paramName, value: actual, description: expected.description });
    } else {
      results.failed.push({
        param: paramName,
        expected: expected.value,
        actual: actual,
        reason: comparison.reason,
        description: expected.description,
        path: `${docId}.${fieldPath}`
      });
    }
  }

  // Output results
  console.log('─'.repeat(70));
  console.log(' PASSED (' + results.passed.length + ')');
  console.log('─'.repeat(70));
  for (const p of results.passed) {
    const val = Array.isArray(p.value) ? `[${p.value.length} items]` : p.value;
    console.log(`  ✓ ${p.param}: ${val}`);
  }

  if (results.failed.length > 0) {
    console.log('\n' + '─'.repeat(70));
    console.log(' FAILED (' + results.failed.length + ')');
    console.log('─'.repeat(70));
    for (const f of results.failed) {
      console.log(`  ✗ ${f.param}: ${f.reason}`);
      console.log(`    Path: ${f.path}`);
      console.log(`    Expected: ${JSON.stringify(f.expected)}`);
      console.log(`    Actual: ${JSON.stringify(f.actual)}`);
    }
  }

  if (results.missing.length > 0) {
    console.log('\n' + '─'.repeat(70));
    console.log(' MISSING (' + results.missing.length + ')');
    console.log('─'.repeat(70));
    for (const m of results.missing) {
      console.log(`  ? ${m.param}: ${m.reason}`);
    }
  }

  // Summary
  console.log('\n' + '═'.repeat(70));
  console.log(' SUMMARY');
  console.log('═'.repeat(70));
  console.log(`  Passed:  ${results.passed.length}`);
  console.log(`  Failed:  ${results.failed.length}`);
  console.log(`  Missing: ${results.missing.length}`);
  console.log(`  Total:   ${Object.keys(EXPECTED_VALUES).length}`);

  const allGood = results.failed.length === 0 && results.missing.length === 0;
  console.log(`\n  Status: ${allGood ? '✓ ALL PARAMETERS VALID' : '✗ ISSUES FOUND'}`);
  console.log('═'.repeat(70));

  // Save report
  const report = {
    timestamp: new Date().toISOString(),
    version: '12.9',
    results,
    summary: {
      passed: results.passed.length,
      failed: results.failed.length,
      missing: results.missing.length,
      total: Object.keys(EXPECTED_VALUES).length,
      status: allGood ? 'VALID' : 'ISSUES_FOUND'
    }
  };

  const reportPath = path.join(__dirname, '..', 'firebase-validation-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\nReport saved: ${reportPath}`);

  await admin.app().delete();
  process.exit(allGood ? 0 : 1);
}

validateFirebase().catch(err => {
  console.error('Validation error:', err);
  process.exit(1);
});
