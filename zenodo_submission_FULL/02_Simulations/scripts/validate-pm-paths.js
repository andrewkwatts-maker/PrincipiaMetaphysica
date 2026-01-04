/**
 * Validate PM Paths - Pre-sync validation
 *
 * Validates that all PM paths used in HTML pages exist in theory_output.json
 * Run this before syncing to Firebase to catch any missing values.
 *
 * Run: node scripts/validate-pm-paths.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

// Directories to scan for HTML files
const SCAN_DIRS = ['', 'sections', 'foundations', 'docs', 'diagrams'];

// Files to skip (partial HTML fragments)
const SKIP_FILES = [
  'appendices_content.html',
  'ATTRIBUTION_HTML_ADDITIONS.html',
  'ATTRIBUTION_HTML_ADDITIONS_PART2.html',
  'PAPER_2T_UPDATE_SECTION.html'
];

/**
 * Get value from nested object by path
 */
function getValueByPath(obj, pathStr) {
  const parts = pathStr.split('.');
  let current = obj;

  for (const part of parts) {
    if (current === null || current === undefined) {
      return undefined;
    }
    current = current[part];
  }

  return current;
}

/**
 * Extract PM paths from HTML file
 */
function extractPMPaths(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const paths = [];

  // Match data-pm-value="path.to.value"
  const regex = /data-pm-value="([^"]+)"/g;
  let match;

  while ((match = regex.exec(content)) !== null) {
    paths.push({
      path: match[1],
      file: path.relative(ROOT_DIR, filePath)
    });
  }

  return paths;
}

/**
 * Main validation function
 */
function validatePMPaths() {
  console.log('PM Path Validation');
  console.log('─'.repeat(70));

  // Load theory_output.json
  const theoryPath = path.join(ROOT_DIR, 'theory_output.json');
  if (!fs.existsSync(theoryPath)) {
    console.error('ERROR: theory_output.json not found!');
    console.log('Run: python run_all_simulations.py first');
    process.exit(1);
  }

  const theoryData = JSON.parse(fs.readFileSync(theoryPath, 'utf-8'));
  console.log('Loaded theory_output.json');
  console.log(`  Version: ${theoryData.meta?.version || 'unknown'}`);
  console.log(`  Last updated: ${theoryData.meta?.last_updated || 'unknown'}`);
  console.log('');

  // Collect all PM paths from HTML files
  const allPaths = [];
  let filesScanned = 0;

  for (const dir of SCAN_DIRS) {
    const dirPath = path.join(ROOT_DIR, dir);
    if (!fs.existsSync(dirPath)) continue;

    const files = fs.readdirSync(dirPath);
    for (const file of files) {
      if (!file.endsWith('.html')) continue;
      if (SKIP_FILES.includes(file)) continue;

      const filePath = path.join(dirPath, file);
      const paths = extractPMPaths(filePath);
      allPaths.push(...paths);
      filesScanned++;
    }
  }

  console.log(`Scanned ${filesScanned} HTML files`);
  console.log(`Found ${allPaths.length} PM path references`);
  console.log('');

  // Get unique paths
  const uniquePaths = [...new Set(allPaths.map(p => p.path))];
  console.log(`Unique paths: ${uniquePaths.length}`);
  console.log('');

  // Validate each path
  const valid = [];
  const missing = [];

  for (const pathStr of uniquePaths) {
    const value = getValueByPath(theoryData, pathStr);
    if (value !== undefined) {
      valid.push({ path: pathStr, value });
    } else {
      // Find which files use this path
      const files = allPaths.filter(p => p.path === pathStr).map(p => p.file);
      missing.push({ path: pathStr, files: [...new Set(files)] });
    }
  }

  // Report results
  console.log('─'.repeat(70));
  console.log('VALID PATHS (' + valid.length + ')');
  console.log('─'.repeat(70));
  for (const { path: p, value } of valid) {
    const displayVal = typeof value === 'number'
      ? (Math.abs(value) > 1e6 || Math.abs(value) < 0.001 ? value.toExponential(3) : value.toFixed(4))
      : typeof value === 'object' ? '[object]' : value;
    console.log(`  ✓ ${p} = ${displayVal}`);
  }

  if (missing.length > 0) {
    console.log('\n' + '─'.repeat(70));
    console.log('MISSING PATHS (' + missing.length + ')');
    console.log('─'.repeat(70));
    for (const { path: p, files } of missing) {
      console.log(`  ✗ ${p}`);
      console.log(`    Used in: ${files.join(', ')}`);
    }
  }

  // Summary
  console.log('\n' + '─'.repeat(70));
  console.log('SUMMARY');
  console.log('─'.repeat(70));
  console.log(`  Valid:   ${valid.length}/${uniquePaths.length} (${((valid.length/uniquePaths.length)*100).toFixed(1)}%)`);
  console.log(`  Missing: ${missing.length}/${uniquePaths.length}`);

  if (missing.length === 0) {
    console.log('\n✓ All PM paths validated successfully!');
    console.log('  Ready for Firebase sync.');
    return { success: true, valid: valid.length, missing: 0 };
  } else {
    console.log('\n✗ Some PM paths are missing!');
    console.log('  Run simulations again or fix HTML references.');
    return { success: false, valid: valid.length, missing: missing.length };
  }
}

// Run validation
const result = validatePMPaths();
process.exit(result.success ? 0 : 1);
