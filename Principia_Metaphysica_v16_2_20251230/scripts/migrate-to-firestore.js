/**
 * Firebase Firestore Data Migration Script
 *
 * Migrates theory constants, formulas, and formula database from static JS files
 * to Firebase Firestore collections.
 *
 * Usage: node scripts/migrate-to-firestore.js
 *
 * Prerequisites:
 * - npm install firebase-admin
 * - Set GOOGLE_APPLICATION_CREDENTIALS environment variable to service account JSON path
 *   OR place serviceAccountKey.json in this directory
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

// Firebase configuration
const firebaseConfig = {
  projectId: "principia-metaphysica",
  storageBucket: "principia-metaphysica.firebasestorage.app"
};

// Initialize Firebase Admin
try {
  // Try to load service account from file
  const serviceAccountPath = path.join(__dirname, 'serviceAccountKey.json');
  if (fs.existsSync(serviceAccountPath)) {
    const serviceAccount = require(serviceAccountPath);
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount),
      ...firebaseConfig
    });
    console.log('✓ Initialized with service account file');
  } else if (process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    admin.initializeApp(firebaseConfig);
    console.log('✓ Initialized with GOOGLE_APPLICATION_CREDENTIALS');
  } else {
    console.error('ERROR: No Firebase credentials found.');
    console.error('Please either:');
    console.error('  1. Place serviceAccountKey.json in scripts/ folder');
    console.error('  2. Set GOOGLE_APPLICATION_CREDENTIALS environment variable');
    process.exit(1);
  }
} catch (error) {
  console.error('Failed to initialize Firebase:', error);
  process.exit(1);
}

const db = admin.firestore();

/**
 * Load theory constants from theory-constants-enhanced.js
 */
function loadTheoryConstants() {
  console.log('\n📦 Loading theory constants...');

  const filePath = path.join(__dirname, '..', 'theory-constants-enhanced.js');
  let content = fs.readFileSync(filePath, 'utf-8');

  // Remove the const PM = declaration and get just the object
  // The file has: const PM = { ... }; plus some additional PM.xxx = ... lines
  // We need to extract just the main object

  // Find the PM object definition
  const startMatch = content.match(/const PM = \{/);
  if (!startMatch) {
    throw new Error('Could not find PM object in theory-constants-enhanced.js');
  }

  const startIndex = content.indexOf('const PM = {') + 'const PM = '.length;

  // Find the matching closing brace by counting braces
  let braceCount = 0;
  let endIndex = startIndex;
  let inString = false;
  let stringChar = '';

  for (let i = startIndex; i < content.length; i++) {
    const char = content[i];
    const prevChar = i > 0 ? content[i - 1] : '';

    // Track string state
    if ((char === '"' || char === "'") && prevChar !== '\\') {
      if (!inString) {
        inString = true;
        stringChar = char;
      } else if (char === stringChar) {
        inString = false;
      }
    }

    // Count braces outside strings
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

  let jsonString = content.substring(startIndex, endIndex);

  // Clean up for JSON parsing
  // Replace NaN with null
  jsonString = jsonString.replace(/\bNaN\b/g, 'null');
  // Remove comments
  jsonString = jsonString.replace(/\/\/.*$/gm, '');
  // Handle trailing commas (simple approach)
  jsonString = jsonString.replace(/,(\s*[}\]])/g, '$1');

  try {
    const PM = JSON.parse(jsonString);
    console.log(`✓ Loaded ${Object.keys(PM).length} top-level keys`);
    return PM;
  } catch (error) {
    console.error('Failed to parse PM object:', error.message);
    // Try eval as fallback (less safe but handles JS objects)
    console.log('Trying eval fallback...');
    const PMEval = eval('(' + jsonString + ')');
    console.log(`✓ Loaded ${Object.keys(PMEval).length} top-level keys via eval`);
    return PMEval;
  }
}

/**
 * Load formula definitions from formula-definitions.js
 */
function loadFormulaDefinitions() {
  console.log('\n📦 Loading formula definitions...');

  const filePath = path.join(__dirname, '..', 'js', 'formula-definitions.js');
  let content = fs.readFileSync(filePath, 'utf-8');

  // Extract PM_FORMULAS object
  const startMatch = content.indexOf('const PM_FORMULAS = {');
  if (startMatch === -1) {
    throw new Error('Could not find PM_FORMULAS object');
  }

  const objectStart = startMatch + 'const PM_FORMULAS = '.length;

  // Find matching closing brace
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

  // Clean up - this is JS not JSON, so we need to be careful
  // For simplicity, we'll extract formulas manually
  const formulas = [];
  const categories = ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS'];

  for (const category of categories) {
    const categoryRegex = new RegExp(`${category}:\\s*\\{([\\s\\S]*?)\\n    \\}`, 'g');
    const categoryMatch = jsonString.match(categoryRegex);

    if (categoryMatch) {
      // Extract individual formulas from this category
      const formulaRegex = /(\w+):\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}/g;
      let match;

      while ((match = formulaRegex.exec(categoryMatch[0])) !== null) {
        try {
          // Try to parse the formula object
          const formulaName = match[1];
          const formulaContent = match[2];

          // Extract key fields
          const idMatch = formulaContent.match(/id:\s*["']([^"']+)["']/);
          const htmlMatch = formulaContent.match(/html:\s*["']([^"']+)["']/);
          const labelMatch = formulaContent.match(/label:\s*["']([^"']+)["']/);
          const descMatch = formulaContent.match(/description:\s*["']([^"']+)["']/);

          if (idMatch && htmlMatch && labelMatch) {
            formulas.push({
              id: idMatch[1],
              name: formulaName,
              html: htmlMatch[1],
              label: labelMatch[1],
              description: descMatch ? descMatch[1] : '',
              category: category
            });
          }
        } catch (e) {
          // Skip malformed entries
        }
      }
    }
  }

  console.log(`✓ Extracted ${formulas.length} formulas`);
  return formulas;
}

/**
 * Load formula database from formula-database.js
 */
function loadFormulaDatabase() {
  console.log('\n📦 Loading formula database...');

  const filePath = path.join(__dirname, '..', 'js', 'formula-database.js');

  if (!fs.existsSync(filePath)) {
    console.log('⚠ formula-database.js not found, skipping');
    return {};
  }

  let content = fs.readFileSync(filePath, 'utf-8');

  // Extract FORMULA_DATABASE object
  const startMatch = content.indexOf('const FORMULA_DATABASE = {');
  if (startMatch === -1) {
    const altMatch = content.indexOf('window.FORMULA_DATABASE = {');
    if (altMatch === -1) {
      console.log('⚠ Could not find FORMULA_DATABASE object');
      return {};
    }
  }

  // For simplicity, extract entries using regex
  const database = {};
  const entryRegex = /["']?(\w+)["']?\s*:\s*\{([^}]+)\}/g;
  let match;

  while ((match = entryRegex.exec(content)) !== null) {
    const key = match[1];
    const value = match[2];

    // Extract basic fields
    const symbolMatch = value.match(/symbol:\s*["']([^"']+)["']/);
    const valueMatch = value.match(/value:\s*([\d.e+-]+)/);
    const unitMatch = value.match(/unit:\s*["']([^"']+)["']/);
    const categoryMatch = value.match(/category:\s*["']([^"']+)["']/);
    const descMatch = value.match(/description:\s*["']([^"']+)["']/);

    if (symbolMatch || valueMatch) {
      database[key] = {
        symbol: symbolMatch ? symbolMatch[1] : key,
        value: valueMatch ? parseFloat(valueMatch[1]) : null,
        unit: unitMatch ? unitMatch[1] : '',
        category: categoryMatch ? categoryMatch[1] : 'general',
        description: descMatch ? descMatch[1] : ''
      };
    }
  }

  console.log(`✓ Extracted ${Object.keys(database).length} database entries`);
  return database;
}

/**
 * Upload theory constants to Firestore
 */
async function uploadTheoryConstants(PM) {
  console.log('\n☁️ Uploading theory constants to Firestore...');

  try {
    // Upload as single document
    await db.collection('theory_constants').doc('current').set(PM);
    console.log('✓ Uploaded to theory_constants/current');

    // Also upload with version tag
    const version = PM.meta?.version || '12.7';
    await db.collection('theory_constants').doc(`v${version.replace('.', '_')}`).set(PM);
    console.log(`✓ Uploaded to theory_constants/v${version.replace('.', '_')}`);

    return true;
  } catch (error) {
    console.error('Failed to upload theory constants:', error);
    return false;
  }
}

/**
 * Upload formulas to Firestore
 */
async function uploadFormulas(formulas) {
  console.log('\n☁️ Uploading formulas to Firestore...');

  const batch = db.batch();
  let count = 0;

  for (const formula of formulas) {
    const docRef = db.collection('formulas').doc(formula.id);
    batch.set(docRef, formula);
    count++;

    // Firestore batches have a limit of 500 operations
    if (count >= 400) {
      await batch.commit();
      console.log(`✓ Committed batch of ${count} formulas`);
      count = 0;
    }
  }

  if (count > 0) {
    await batch.commit();
    console.log(`✓ Committed final batch of ${count} formulas`);
  }

  console.log(`✓ Uploaded ${formulas.length} formulas total`);
  return true;
}

/**
 * Upload formula database to Firestore
 */
async function uploadFormulaDatabase(database) {
  console.log('\n☁️ Uploading formula database to Firestore...');

  const batch = db.batch();
  let count = 0;

  for (const [key, value] of Object.entries(database)) {
    const docRef = db.collection('formula_database').doc(key);
    batch.set(docRef, value);
    count++;

    if (count >= 400) {
      await batch.commit();
      console.log(`✓ Committed batch of ${count} entries`);
      count = 0;
    }
  }

  if (count > 0) {
    await batch.commit();
    console.log(`✓ Committed final batch of ${count} entries`);
  }

  console.log(`✓ Uploaded ${Object.keys(database).length} database entries total`);
  return true;
}

/**
 * Main migration function
 */
async function migrate() {
  console.log('═══════════════════════════════════════════════════════════════');
  console.log(' Principia Metaphysica - Firebase Data Migration');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log(`Timestamp: ${new Date().toISOString()}`);

  try {
    // Load data from static files
    const theoryConstants = loadTheoryConstants();
    const formulas = loadFormulaDefinitions();
    const formulaDatabase = loadFormulaDatabase();

    // Upload to Firestore
    const results = await Promise.all([
      uploadTheoryConstants(theoryConstants),
      uploadFormulas(formulas),
      uploadFormulaDatabase(formulaDatabase)
    ]);

    console.log('\n═══════════════════════════════════════════════════════════════');
    if (results.every(r => r)) {
      console.log(' ✅ MIGRATION COMPLETE');
    } else {
      console.log(' ⚠️ MIGRATION COMPLETED WITH ERRORS');
    }
    console.log('═══════════════════════════════════════════════════════════════');

  } catch (error) {
    console.error('\n❌ MIGRATION FAILED:', error);
    process.exit(1);
  }

  process.exit(0);
}

// Run migration
migrate();
