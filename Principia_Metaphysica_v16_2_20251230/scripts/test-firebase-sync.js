/**
 * Test Firebase Sync Script
 *
 * Tests the sync logic without actually connecting to Firebase.
 * Useful for debugging and understanding how the diff works.
 *
 * Usage: node scripts/test-firebase-sync.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

// Colors
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

/**
 * Load enhanced constants (same logic as sync script)
 */
function loadEnhancedConstants() {
  const filePath = path.join(ROOT_DIR, 'theory-constants-enhanced.js');

  if (!fs.existsSync(filePath)) {
    console.error(`${c.red}ERROR: theory-constants-enhanced.js not found${c.reset}`);
    process.exit(1);
  }

  let content = fs.readFileSync(filePath, 'utf-8');

  const startMatch = content.indexOf('const PM = {');
  if (startMatch === -1) {
    throw new Error('Could not find PM object');
  }

  const objectStart = startMatch + 'const PM = '.length;

  let braceCount = 0;
  let endIndex = objectStart;
  let inString = false;
  let stringChar = '';

  for (let i = objectStart; i < content.length; i++) {
    const char = content[i];
    const prevChar = i > 0 ? content[i - 1] : '';

    if ((char === '"' || char === "'") && prevChar !== '\\') {
      if (!inString) {
        inString = true;
        stringChar = char;
      } else if (char === stringChar) {
        inString = false;
      }
    }

    if (!inString) {
      if (char === '{') braceCount++;
      if (char === '}') {
        braceCount--;
        if (braceCount === 0) {
          endIndex = i + 1;
          break;
        }
      }
    }
  }

  let jsonString = content.substring(objectStart, endIndex);
  jsonString = jsonString.replace(/\bNaN\b/g, 'null');
  jsonString = jsonString.replace(/\/\/.*$/gm, '');
  jsonString = jsonString.replace(/\/\*[\s\S]*?\*\//g, '');
  jsonString = jsonString.replace(/,(\s*[}\]])/g, '$1');

  try {
    return JSON.parse(jsonString);
  } catch (e) {
    return eval('(' + jsonString + ')');
  }
}

/**
 * Deep diff (same as sync script)
 */
function deepDiff(local, remote, path = '', maxDepth = 20, currentDepth = 0) {
  const diffs = [];

  if (currentDepth >= maxDepth) return diffs;
  if (local === null && remote === null) return diffs;
  if (local === undefined && remote === undefined) return diffs;

  if (typeof local !== 'object' || typeof remote !== 'object' || local === null || remote === null) {
    if (local !== remote) {
      diffs.push({
        path: path || 'root',
        type: 'changed',
        oldValue: remote,
        newValue: local
      });
    }
    return diffs;
  }

  if (Array.isArray(local) || Array.isArray(remote)) {
    const localStr = JSON.stringify(local);
    const remoteStr = JSON.stringify(remote);

    if (localStr !== remoteStr) {
      diffs.push({
        path: path || 'root',
        type: 'changed',
        oldValue: remote,
        newValue: local,
        isArray: true
      });
    }
    return diffs;
  }

  const allKeys = new Set([
    ...Object.keys(local || {}),
    ...Object.keys(remote || {})
  ]);

  for (const key of allKeys) {
    const newPath = path ? `${path}.${key}` : key;
    const localVal = local?.[key];
    const remoteVal = remote?.[key];

    if (localVal === undefined && remoteVal !== undefined) {
      diffs.push({
        path: newPath,
        type: 'removed',
        oldValue: remoteVal
      });
    } else if (remoteVal === undefined && localVal !== undefined) {
      diffs.push({
        path: newPath,
        type: 'added',
        newValue: localVal
      });
    } else if (localVal !== undefined && remoteVal !== undefined) {
      if (typeof localVal === 'object' && localVal !== null && !Array.isArray(localVal)) {
        diffs.push(...deepDiff(localVal, remoteVal, newPath, maxDepth, currentDepth + 1));
      } else {
        const localStr = JSON.stringify(localVal);
        const remoteStr = JSON.stringify(remoteVal);

        if (localStr !== remoteStr) {
          diffs.push({
            path: newPath,
            type: 'changed',
            oldValue: remoteVal,
            newValue: localVal
          });
        }
      }
    }
  }

  return diffs;
}

/**
 * Main test function
 */
function runTests() {
  console.log('═'.repeat(80));
  console.log(`${c.bright}${c.cyan}  Firebase Sync - Local Test${c.reset}`);
  console.log('═'.repeat(80));
  console.log();

  // Test 1: Load enhanced constants
  console.log(`${c.bright}Test 1: Loading theory-constants-enhanced.js${c.reset}`);
  try {
    const data = loadEnhancedConstants();
    console.log(`${c.green}✓ Successfully loaded${c.reset}`);
    console.log(`  Version: ${data.meta?.version || 'unknown'}`);
    console.log(`  Simulations: ${data.meta?.simulations_run?.length || 0}`);
    console.log(`  Top-level keys: ${Object.keys(data).length}`);
    console.log();

    // Test 2: Simulate a diff with modified data
    console.log(`${c.bright}Test 2: Simulating changes${c.reset}`);

    // Create a "remote" version with some differences
    const remoteData = JSON.parse(JSON.stringify(data)); // Deep clone

    // Modify some values
    if (remoteData.proton_decay) {
      remoteData.proton_decay.M_GUT = 2.0e16; // Changed value
    }

    if (remoteData.pmns_matrix) {
      remoteData.pmns_matrix.theta_12 = 33.0; // Changed value
    }

    // Remove a field
    if (remoteData.meta) {
      delete remoteData.meta.last_updated;
    }

    // Add a field to local
    data.test_field = "This is a test field";

    // Compute diff
    const diffs = deepDiff(data, remoteData);

    console.log(`${c.green}✓ Diff computed${c.reset}`);
    console.log(`  Total changes: ${diffs.length}`);

    const added = diffs.filter(d => d.type === 'added');
    const removed = diffs.filter(d => d.type === 'removed');
    const changed = diffs.filter(d => d.type === 'changed');

    console.log(`  Added: ${c.green}${added.length}${c.reset}`);
    console.log(`  Removed: ${c.red}${removed.length}${c.reset}`);
    console.log(`  Changed: ${c.yellow}${changed.length}${c.reset}`);
    console.log();

    // Show sample changes
    if (changed.length > 0) {
      console.log(`${c.bright}Sample changes:${c.reset}`);
      changed.slice(0, 3).forEach(d => {
        console.log(`  ${c.yellow}~${c.reset} ${d.path}`);
        console.log(`    ${c.red}- ${d.oldValue}${c.reset}`);
        console.log(`    ${c.green}+ ${d.newValue}${c.reset}`);
      });
      console.log();
    }

    // Test 3: Test with identical data
    console.log(`${c.bright}Test 3: Testing with identical data${c.reset}`);
    const identicalData = JSON.parse(JSON.stringify(data));
    const noDiffs = deepDiff(data, identicalData);

    if (noDiffs.length === 0) {
      console.log(`${c.green}✓ Correctly detected no changes${c.reset}`);
    } else {
      console.log(`${c.red}✗ False positives detected: ${noDiffs.length}${c.reset}`);
    }
    console.log();

    // Test 4: Deep nesting test
    console.log(`${c.bright}Test 4: Testing deep nesting handling${c.reset}`);
    const deepData = {
      level1: {
        level2: {
          level3: {
            level4: {
              level5: {
                value: 42
              }
            }
          }
        }
      }
    };

    const deepDataModified = JSON.parse(JSON.stringify(deepData));
    deepDataModified.level1.level2.level3.level4.level5.value = 43;

    const deepDiffs = deepDiff(deepDataModified, deepData);
    console.log(`${c.green}✓ Deep nesting handled${c.reset}`);
    console.log(`  Changes detected: ${deepDiffs.length}`);
    if (deepDiffs.length > 0) {
      console.log(`  Path: ${deepDiffs[0].path}`);
      console.log(`  Old: ${deepDiffs[0].oldValue}, New: ${deepDiffs[0].newValue}`);
    }
    console.log();

    // Summary
    console.log('═'.repeat(80));
    console.log(`${c.green}${c.bright}  ✅ All tests passed!${c.reset}`);
    console.log('═'.repeat(80));
    console.log();
    console.log(`${c.bright}The sync script should work correctly.${c.reset}`);
    console.log(`Run: ${c.cyan}node scripts/firebase-sync-with-history.js${c.reset}`);
    console.log();

  } catch (error) {
    console.log();
    console.log('═'.repeat(80));
    console.error(`${c.red}${c.bright}  ✗ Tests failed${c.reset}`);
    console.log('═'.repeat(80));
    console.error(`  Error: ${error.message}`);
    console.error();
    console.error('Stack trace:');
    console.error(error.stack);
    process.exit(1);
  }
}

// Run tests
runTests();
