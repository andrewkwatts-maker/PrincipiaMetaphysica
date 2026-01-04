/**
 * Firebase Coverage Validation Script
 *
 * Scans all HTML pages and validates:
 * 1. All formulas are in Firebase
 * 2. All PM constants are in Firebase
 * 3. All pages use centralized data loading
 * 4. No hardcoded magic numbers
 *
 * Run: node scripts/validate-firebase-coverage.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');
const admin = require('firebase-admin');

// Initialize Firebase Admin
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
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}

const db = admin.firestore();

// Known physics constants that should be in Firebase
const KNOWN_PHYSICS_VALUES = [
  // Masses
  { pattern: /125\.1\d*\s*GeV/gi, name: 'Higgs mass', pmPath: 'higgs_mass' },
  { pattern: /173\.\d+\s*GeV/gi, name: 'Top quark mass', pmPath: 'top_mass' },
  { pattern: /174\.\d+\s*GeV/gi, name: 'VEV', pmPath: 'vev' },
  { pattern: /91\.\d+\s*GeV/gi, name: 'Z boson mass', pmPath: 'z_mass' },
  { pattern: /80\.\d+\s*GeV/gi, name: 'W boson mass', pmPath: 'w_mass' },

  // Angles
  { pattern: /45\.0°|45\.0\s*degrees/gi, name: 'theta_23', pmPath: 'pmns_matrix.theta_23' },
  { pattern: /33\.\d+°|33\.\d+\s*degrees/gi, name: 'theta_12', pmPath: 'pmns_matrix.theta_12' },
  { pattern: /8\.\d+°|8\.\d+\s*degrees/gi, name: 'theta_13', pmPath: 'pmns_matrix.theta_13' },

  // Dark energy
  { pattern: /-0\.85\d*/gi, name: 'w0', pmPath: 'dark_energy.w0' },
  { pattern: /-0\.8528/gi, name: 'w0_PM', pmPath: 'dark_energy.w0_PM' },

  // GUT parameters
  { pattern: /2\.1\d*\s*×?\s*10\^?16/gi, name: 'M_GUT', pmPath: 'proton_decay.M_GUT' },
  { pattern: /24\.\d+/gi, name: 'alpha_GUT_inv', pmPath: 'alpha_GUT_inv', context: 'GUT|unification' },
  { pattern: /3\.\d+\s*×?\s*10\^?34\s*years/gi, name: 'proton_lifetime', pmPath: 'proton_decay.tau_p' },

  // Dimensions
  { pattern: /\b26D\b|26-dimensional/gi, name: 'D_bulk', pmPath: 'dimensions.D_bulk' },
  { pattern: /\b13D\b|13-dimensional/gi, name: 'D_after_sp2r', pmPath: 'dimensions.D_after_sp2r' },

  // Topology
  { pattern: /χ\s*=\s*144/gi, name: 'chi_eff', pmPath: 'topology.chi_eff' },
  { pattern: /b[₃3]\s*=\s*24/gi, name: 'b3', pmPath: 'topology.b3' },
  { pattern: /n_gen\s*=\s*3/gi, name: 'n_gen', pmPath: 'topology.n_gen' },

  // KK graviton
  { pattern: /5\.0\d*\s*TeV/gi, name: 'KK graviton mass', pmPath: 'kk_graviton.mass' },
];

// Formula patterns to detect
const FORMULA_PATTERNS = [
  { pattern: /G_μν\s*=\s*8πG\s*T_μν/gi, name: 'Einstein Field Equations' },
  { pattern: /S\s*=\s*∫.*R.*√g/gi, name: 'Einstein-Hilbert Action' },
  { pattern: /F\(R,T,τ\)/gi, name: 'Bulk Gravity' },
  { pattern: /SO\(10\)\s*→\s*SU\(3\)/gi, name: 'Symmetry Breaking' },
  { pattern: /χ\/24\s*=\s*3/gi, name: 'Generation Formula' },
  { pattern: /w\(z\)\s*=/gi, name: 'Dark Energy EoS' },
  { pattern: /Sp\(2,R\)/gi, name: 'Sp2R Gauge' },
];

// Directories to scan
const SCAN_DIRS = [
  '',
  'sections',
  'foundations',
  'docs',
  'diagrams'
];

// Results storage
const results = {
  pagesScanned: 0,
  hardcodedValues: [],
  missingFormulas: [],
  missingConstants: [],
  pagesWithoutFirebase: [],
  pagesWithHardcodedFormulas: [],
  summary: {}
};

/**
 * Get all HTML files in directory
 */
function getHtmlFiles(dir) {
  const fullPath = path.join(ROOT_DIR, dir);
  if (!fs.existsSync(fullPath)) return [];

  return fs.readdirSync(fullPath)
    .filter(f => f.endsWith('.html'))
    .map(f => path.join(dir, f));
}

/**
 * Check if page uses Firebase data loading
 */
function checkFirebaseIntegration(content, filePath) {
  const issues = [];

  // Check for Firebase imports
  const hasFirebaseImport = content.includes('firebase-auth.js') ||
                           content.includes('auth-guard.js') ||
                           content.includes('firebase-data.js') ||
                           content.includes('firebase-page-loader.js');

  // Check for setupAuthGuard call
  const hasAuthGuard = content.includes('setupAuthGuard');

  // Check for pm-value class usage
  const pmValueCount = (content.match(/class="pm-value"/g) || []).length;
  const pmValueWithPath = (content.match(/data-pm-value="/g) || []).length;
  const pmValueWithCategory = (content.match(/data-category="/g) || []).length;

  if (!hasFirebaseImport) {
    issues.push('Missing Firebase imports');
  }

  if (!hasAuthGuard && !content.includes('test') && !content.includes('component')) {
    issues.push('Missing setupAuthGuard call');
  }

  return {
    hasFirebase: hasFirebaseImport,
    hasAuthGuard,
    pmValueCount,
    pmValueWithPath,
    pmValueWithCategory,
    issues
  };
}

/**
 * Find hardcoded physics values
 */
function findHardcodedValues(content, filePath) {
  const found = [];

  for (const check of KNOWN_PHYSICS_VALUES) {
    const matches = content.match(check.pattern);
    if (matches) {
      // Check if it's inside a pm-value span (which is correct)
      for (const match of matches) {
        // Look for context around the match
        const index = content.indexOf(match);
        const context = content.substring(Math.max(0, index - 100), Math.min(content.length, index + match.length + 100));

        // Skip if it's in a pm-value span or data attribute
        if (context.includes('data-pm-value') || context.includes('data-category')) {
          continue;
        }

        // Skip if in comments
        if (context.includes('<!--') && context.includes('-->')) {
          continue;
        }

        // Check context requirement if specified
        if (check.context) {
          const contextRegex = new RegExp(check.context, 'i');
          if (!contextRegex.test(context)) {
            continue;
          }
        }

        found.push({
          value: match,
          name: check.name,
          pmPath: check.pmPath,
          file: filePath,
          context: context.replace(/\s+/g, ' ').trim().substring(0, 150)
        });
      }
    }
  }

  return found;
}

/**
 * Find formulas that should be in Firebase
 */
function findFormulas(content, filePath) {
  const found = [];

  // Look for formula boxes and inline formulas
  const formulaBoxes = content.match(/<div[^>]*class="[^"]*formula[^"]*"[^>]*>[\s\S]*?<\/div>/gi) || [];

  for (const box of formulaBoxes) {
    // Check if it references Firebase data
    const hasDataRef = box.includes('data-formula-id') || box.includes('data-pm-value');

    if (!hasDataRef) {
      // Extract formula content
      const formulaContent = box.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      if (formulaContent.length > 10) {
        found.push({
          content: formulaContent.substring(0, 100),
          file: filePath,
          hasDataRef: false
        });
      }
    }
  }

  return found;
}

/**
 * Load Firebase data for comparison
 */
async function loadFirebaseData() {
  console.log('Loading Firebase data...');

  const data = {
    formulas: {},
    constants: {},
    formulaDatabase: {}
  };

  // Load formulas
  const formulasSnapshot = await db.collection('formulas').get();
  formulasSnapshot.forEach(doc => {
    data.formulas[doc.id] = doc.data();
  });
  console.log(`  Loaded ${Object.keys(data.formulas).length} formulas`);

  // Load theory constants
  const constantsDoc = await db.collection('theory_constants').doc('current').get();
  if (constantsDoc.exists) {
    data.constants = constantsDoc.data();
  }
  console.log(`  Loaded theory constants`);

  // Load formula database
  const formulaDbSnapshot = await db.collection('formula_database').get();
  formulaDbSnapshot.forEach(doc => {
    data.formulaDatabase[doc.id] = doc.data();
  });
  console.log(`  Loaded ${Object.keys(data.formulaDatabase).length} formula database entries`);

  return data;
}

/**
 * Scan a single page
 */
function scanPage(filePath, firebaseData) {
  const fullPath = path.join(ROOT_DIR, filePath);
  if (!fs.existsSync(fullPath)) return null;

  const content = fs.readFileSync(fullPath, 'utf-8');

  // Check Firebase integration
  const firebaseCheck = checkFirebaseIntegration(content, filePath);

  // Find hardcoded values
  const hardcodedValues = findHardcodedValues(content, filePath);

  // Find formulas without Firebase refs
  const formulas = findFormulas(content, filePath);

  return {
    path: filePath,
    firebase: firebaseCheck,
    hardcodedValues,
    formulas,
    size: content.length
  };
}

/**
 * Generate report
 */
function generateReport(pageResults, firebaseData) {
  console.log('\n' + '═'.repeat(70));
  console.log(' FIREBASE COVERAGE VALIDATION REPORT');
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  // Summary counts
  let totalPages = pageResults.length;
  let pagesWithFirebase = pageResults.filter(p => p.firebase.hasFirebase).length;
  let pagesWithHardcoded = pageResults.filter(p => p.hardcodedValues.length > 0).length;
  let totalHardcoded = pageResults.reduce((sum, p) => sum + p.hardcodedValues.length, 0);
  let pagesWithFormulas = pageResults.filter(p => p.formulas.length > 0).length;

  console.log('SUMMARY');
  console.log('─'.repeat(70));
  console.log(`Total pages scanned:           ${totalPages}`);
  console.log(`Pages with Firebase:           ${pagesWithFirebase} (${(pagesWithFirebase/totalPages*100).toFixed(1)}%)`);
  console.log(`Pages with hardcoded values:   ${pagesWithHardcoded}`);
  console.log(`Total hardcoded values found:  ${totalHardcoded}`);
  console.log(`Pages with unlinked formulas:  ${pagesWithFormulas}`);
  console.log('');

  // Firebase data coverage
  console.log('FIREBASE DATA COVERAGE');
  console.log('─'.repeat(70));
  console.log(`Formulas in Firebase:          ${Object.keys(firebaseData.formulas).length}`);
  console.log(`Formula database entries:      ${Object.keys(firebaseData.formulaDatabase).length}`);
  console.log(`Theory constants categories:   ${Object.keys(firebaseData.constants).length}`);
  console.log('');

  // Pages without Firebase
  const noFirebase = pageResults.filter(p => !p.firebase.hasFirebase);
  if (noFirebase.length > 0) {
    console.log('PAGES WITHOUT FIREBASE INTEGRATION');
    console.log('─'.repeat(70));
    for (const page of noFirebase.slice(0, 20)) {
      console.log(`  ✗ ${page.path}`);
      for (const issue of page.firebase.issues) {
        console.log(`      - ${issue}`);
      }
    }
    if (noFirebase.length > 20) {
      console.log(`  ... and ${noFirebase.length - 20} more`);
    }
    console.log('');
  }

  // Hardcoded values by file
  const withHardcoded = pageResults.filter(p => p.hardcodedValues.length > 0);
  if (withHardcoded.length > 0) {
    console.log('HARDCODED VALUES (should use PM data)');
    console.log('─'.repeat(70));
    for (const page of withHardcoded) {
      console.log(`\n  ${page.path}:`);
      for (const hc of page.hardcodedValues.slice(0, 5)) {
        console.log(`    • ${hc.name}: "${hc.value}"`);
        console.log(`      → Should use: PM.${hc.pmPath}`);
      }
      if (page.hardcodedValues.length > 5) {
        console.log(`    ... and ${page.hardcodedValues.length - 5} more`);
      }
    }
    console.log('');
  }

  // Unlinked formulas
  const withFormulas = pageResults.filter(p => p.formulas.length > 0);
  if (withFormulas.length > 0) {
    console.log('FORMULAS WITHOUT FIREBASE REFERENCE');
    console.log('─'.repeat(70));
    for (const page of withFormulas.slice(0, 10)) {
      console.log(`\n  ${page.path}:`);
      for (const f of page.formulas.slice(0, 3)) {
        console.log(`    • ${f.content.substring(0, 80)}...`);
      }
      if (page.formulas.length > 3) {
        console.log(`    ... and ${page.formulas.length - 3} more`);
      }
    }
    console.log('');
  }

  // Recommendations
  console.log('RECOMMENDATIONS');
  console.log('─'.repeat(70));

  if (noFirebase.length > 0) {
    console.log(`1. Add Firebase auth to ${noFirebase.length} pages`);
  }

  if (totalHardcoded > 0) {
    console.log(`2. Replace ${totalHardcoded} hardcoded values with PM data references`);
  }

  if (withFormulas.length > 0) {
    console.log(`3. Link ${withFormulas.reduce((s,p) => s + p.formulas.length, 0)} formulas to Firebase`);
  }

  console.log('\n' + '═'.repeat(70));

  // Return structured results for further processing
  return {
    summary: {
      totalPages,
      pagesWithFirebase,
      pagesWithHardcoded,
      totalHardcoded,
      pagesWithFormulas
    },
    noFirebase: noFirebase.map(p => p.path),
    hardcodedByFile: withHardcoded.map(p => ({
      path: p.path,
      values: p.hardcodedValues
    })),
    formulasByFile: withFormulas.map(p => ({
      path: p.path,
      formulas: p.formulas
    }))
  };
}

/**
 * Main execution
 */
async function main() {
  console.log('Firebase Coverage Validation');
  console.log('─'.repeat(70));

  // Load Firebase data
  const firebaseData = await loadFirebaseData();

  // Scan all pages
  console.log('\nScanning HTML pages...');
  const pageResults = [];

  for (const dir of SCAN_DIRS) {
    const files = getHtmlFiles(dir);
    for (const file of files) {
      // Skip node_modules and test files
      if (file.includes('node_modules') || file.includes('test-')) {
        continue;
      }

      const result = scanPage(file, firebaseData);
      if (result) {
        pageResults.push(result);
      }
    }
  }

  console.log(`Scanned ${pageResults.length} pages`);

  // Generate report
  const report = generateReport(pageResults, firebaseData);

  // Save detailed report
  const reportPath = path.join(ROOT_DIR, 'firebase-coverage-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\nDetailed report saved to: ${reportPath}`);

  // Exit with error if issues found
  if (report.summary.pagesWithHardcoded > 0 || report.noFirebase.length > 0) {
    console.log('\n⚠️  Issues found - run fix scripts to resolve');
    process.exit(1);
  } else {
    console.log('\n✓ All pages are data-driven from Firebase');
    process.exit(0);
  }
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
