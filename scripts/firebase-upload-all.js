/**
 * Firebase Complete Upload Script
 *
 * Uploads ALL single source of truth data to Firebase Firestore:
 * - Theory constants (from theory_output.json)
 * - Formulas (from formula-definitions.js)
 * - Formula database (tooltip metadata)
 * - Page content (extracted from HTML files)
 * - Validation history
 *
 * Usage: node scripts/firebase-upload-all.js [--force]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const ROOT_DIR = path.join(__dirname, '..');
const FORCE_UPLOAD = process.argv.includes('--force');

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
    console.error('\nDownload from Firebase Console > Project Settings > Service Accounts');
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
 * Load and parse theory_output.json
 * Handles NaN values by converting them to null
 */
function loadTheoryOutput() {
  const filePath = path.join(ROOT_DIR, 'theory_output.json');
  if (!fs.existsSync(filePath)) {
    throw new Error('theory_output.json not found');
  }

  let content = fs.readFileSync(filePath, 'utf-8');
  // Replace NaN with null for valid JSON
  content = content.replace(/:\s*NaN\b/g, ': null');
  content = content.replace(/,\s*NaN\b/g, ', null');
  content = content.replace(/\[\s*NaN\b/g, '[ null');
  return JSON.parse(content);
}

/**
 * Load and parse theory-constants-enhanced.js
 */
function loadEnhancedConstants() {
  const filePath = path.join(ROOT_DIR, 'theory-constants-enhanced.js');
  if (!fs.existsSync(filePath)) {
    throw new Error('theory-constants-enhanced.js not found');
  }

  let content = fs.readFileSync(filePath, 'utf-8');

  // Extract PM object
  const startMatch = content.indexOf('const PM = {');
  if (startMatch === -1) throw new Error('Could not find PM object');

  const objectStart = startMatch + 'const PM = '.length;

  // Find matching brace
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
  jsonString = jsonString.replace(/,(\s*[}\]])/g, '$1');

  try {
    return JSON.parse(jsonString);
  } catch (e) {
    // Fallback: use eval (less safe)
    return eval('(' + jsonString + ')');
  }
}

/**
 * Extract page content from HTML files
 */
function extractPageContent(htmlPath) {
  if (!fs.existsSync(htmlPath)) return null;

  const content = fs.readFileSync(htmlPath, 'utf-8');
  const $ = cheerio.load(content);

  // Extract key elements
  const title = $('title').text() || $('h1').first().text();
  const description = $('meta[name="description"]').attr('content') || '';

  // Extract main content sections
  const sections = [];
  $('section, .section, article').each((i, el) => {
    const id = $(el).attr('id') || `section-${i}`;
    const heading = $(el).find('h2, h3').first().text();
    const html = $(el).html();
    sections.push({ id, heading, html });
  });

  // Extract formulas (filter out undefined values)
  const formulas = [];
  $('.formula-box, .equation, .interactive-formula').each((i, el) => {
    const formula = {
      id: $(el).attr('id') || `formula-${i}`,
      html: $(el).html() || ''
    };
    const dataRef = $(el).attr('data-ref');
    if (dataRef !== undefined) formula.dataRef = dataRef;
    formulas.push(formula);
  });

  // Extract PM value references (filter out undefined values)
  const pmRefs = [];
  $('.pm-value').each((i, el) => {
    const ref = {};
    const category = $(el).attr('data-category');
    const param = $(el).attr('data-param');
    if (category !== undefined) ref.category = category;
    if (param !== undefined) ref.param = param;
    if (Object.keys(ref).length > 0) pmRefs.push(ref);
  });

  return {
    title,
    description,
    sections,
    formulas,
    pmRefs,
    lastUpdated: new Date().toISOString()
  };
}

/**
 * Get all HTML pages to process
 */
function getHtmlPages() {
  const pages = [];

  // Root pages
  const rootFiles = [
    'index.html',
    'principia-metaphysica-paper.html',
    'references.html',
    'beginners-guide.html',
    'philosophical-implications.html',
    'visualization-index.html',
    'ancient-numerology.html',
    'proverbs-31-wife-of-noble-character.html'
  ];

  rootFiles.forEach(file => {
    const fullPath = path.join(ROOT_DIR, file);
    if (fs.existsSync(fullPath)) {
      pages.push({
        id: file.replace('.html', ''),
        path: file,
        category: 'root'
      });
    }
  });

  // Section pages
  const sectionsDir = path.join(ROOT_DIR, 'sections');
  if (fs.existsSync(sectionsDir)) {
    fs.readdirSync(sectionsDir).forEach(file => {
      if (file.endsWith('.html')) {
        pages.push({
          id: `sections-${file.replace('.html', '')}`,
          path: `sections/${file}`,
          category: 'sections'
        });
      }
    });
  }

  // Foundation pages
  const foundationsDir = path.join(ROOT_DIR, 'foundations');
  if (fs.existsSync(foundationsDir)) {
    fs.readdirSync(foundationsDir).forEach(file => {
      if (file.endsWith('.html')) {
        pages.push({
          id: `foundations-${file.replace('.html', '')}`,
          path: `foundations/${file}`,
          category: 'foundations'
        });
      }
    });
  }

  // Docs pages
  const docsDir = path.join(ROOT_DIR, 'docs');
  if (fs.existsSync(docsDir)) {
    fs.readdirSync(docsDir).forEach(file => {
      if (file.endsWith('.html')) {
        pages.push({
          id: `docs-${file.replace('.html', '')}`,
          path: `docs/${file}`,
          category: 'docs'
        });
      }
    });
  }

  // Diagrams pages
  const diagramsDir = path.join(ROOT_DIR, 'diagrams');
  if (fs.existsSync(diagramsDir)) {
    fs.readdirSync(diagramsDir).forEach(file => {
      if (file.endsWith('.html')) {
        pages.push({
          id: `diagrams-${file.replace('.html', '')}`,
          path: `diagrams/${file}`,
          category: 'diagrams'
        });
      }
    });
  }

  // Components pages
  const componentsDir = path.join(ROOT_DIR, 'components');
  if (fs.existsSync(componentsDir)) {
    fs.readdirSync(componentsDir).forEach(file => {
      if (file.endsWith('.html')) {
        pages.push({
          id: `components-${file.replace('.html', '')}`,
          path: `components/${file}`,
          category: 'components'
        });
      }
    });
  }

  return pages;
}

/**
 * Remove undefined and null values from an object recursively
 * Firestore doesn't accept undefined values
 */
function cleanUndefined(obj) {
  if (obj === null || obj === undefined) return null;
  if (typeof obj !== 'object') return obj;

  if (Array.isArray(obj)) {
    return obj.map(item => cleanUndefined(item)).filter(item => item !== undefined);
  }

  const cleaned = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== undefined) {
      const cleanedValue = cleanUndefined(value);
      if (cleanedValue !== undefined) {
        cleaned[key] = cleanedValue;
      }
    }
  }
  return cleaned;
}

/**
 * Flatten deeply nested objects to stay within Firestore limits
 * Converts objects nested more than 20 levels to JSON strings
 */
function flattenDeepNested(obj, depth = 0, maxDepth = 15) {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    if (depth >= maxDepth) {
      return JSON.stringify(obj);
    }
    return obj.map(item => flattenDeepNested(item, depth + 1, maxDepth));
  }

  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value === null || typeof value !== 'object') {
      result[key] = value;
    } else if (depth >= maxDepth) {
      // Stringify deeply nested objects
      result[key] = JSON.stringify(value);
    } else {
      result[key] = flattenDeepNested(value, depth + 1, maxDepth);
    }
  }
  return result;
}

/**
 * Select essential fields for the main document
 * Uploads additional data as separate subcollections
 */
function extractCoreConstants(theoryOutput) {
  // Extract only the most important fields for the main document
  return {
    meta: theoryOutput.meta,
    dimensions: theoryOutput.dimensions,
    topology: theoryOutput.topology,
    proton_decay: theoryOutput.proton_decay,
    pmns_matrix: theoryOutput.pmns_matrix,
    dark_energy: theoryOutput.dark_energy,
    validation: theoryOutput.validation,
    v12_7_pure_geometric: flattenDeepNested(theoryOutput.v12_7_pure_geometric, 0, 10),
    v12_3_updates: flattenDeepNested(theoryOutput.v12_3_updates, 0, 10)
  };
}

/**
 * Upload theory constants
 */
async function uploadTheoryConstants(db) {
  console.log('\n📦 Uploading theory constants...');

  const theoryOutput = loadTheoryOutput();

  // Extract core constants (flattened for Firestore compatibility)
  const coreData = extractCoreConstants(theoryOutput);

  // Add metadata
  const data = {
    ...coreData,
    uploadedAt: admin.firestore.FieldValue.serverTimestamp()
  };

  // Upload current version
  await db.collection('theory_constants').doc('current').set(data);
  console.log('  ✓ Uploaded to theory_constants/current');

  // Upload versioned backup
  const version = theoryOutput.meta?.version || '12.7';
  const versionId = `v${version.replace(/\./g, '_')}`;
  await db.collection('theory_constants').doc(versionId).set(data);
  console.log(`  ✓ Uploaded to theory_constants/${versionId}`);

  // Upload enhanced constants separately (they're smaller)
  try {
    const enhancedConstants = loadEnhancedConstants();
    const flattenedEnhanced = flattenDeepNested(enhancedConstants, 0, 10);
    await db.collection('theory_constants').doc('enhanced').set({
      ...flattenedEnhanced,
      uploadedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log('  ✓ Uploaded to theory_constants/enhanced');
  } catch (err) {
    console.log(`  ⚠ Could not upload enhanced constants: ${err.message}`);
  }

  return { success: true, version };
}

/**
 * Upload formulas
 */
async function uploadFormulas(db) {
  console.log('\n📦 Uploading formulas...');

  const formulasPath = path.join(ROOT_DIR, 'js', 'formula-definitions.js');
  if (!fs.existsSync(formulasPath)) {
    console.log('  ⚠ formula-definitions.js not found, skipping');
    return { success: false };
  }

  const content = fs.readFileSync(formulasPath, 'utf-8');

  // Extract formulas using regex (since it's JS, not JSON)
  const formulas = [];
  const categories = ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS'];

  for (const category of categories) {
    // Match formula definitions
    const formulaRegex = new RegExp(
      `(\\w+):\\s*\\{[^}]*id:\\s*["']([^"']+)["'][^}]*html:\\s*["']([^"']+)["'][^}]*label:\\s*["']([^"']+)["']`,
      'g'
    );

    let match;
    while ((match = formulaRegex.exec(content)) !== null) {
      formulas.push({
        name: match[1],
        id: match[2],
        html: match[3],
        label: match[4],
        category: category,
        uploadedAt: admin.firestore.FieldValue.serverTimestamp()
      });
    }
  }

  // Batch upload
  const batch = db.batch();
  let count = 0;

  for (const formula of formulas) {
    const docRef = db.collection('formulas').doc(formula.id);
    batch.set(docRef, formula);
    count++;

    if (count >= 400) {
      await batch.commit();
      console.log(`  ✓ Uploaded batch of ${count} formulas`);
      count = 0;
    }
  }

  if (count > 0) {
    await batch.commit();
    console.log(`  ✓ Uploaded final batch of ${count} formulas`);
  }

  console.log(`  ✓ Total: ${formulas.length} formulas uploaded`);
  return { success: true, count: formulas.length };
}

/**
 * Upload page content
 * Handles large pages by splitting content into chunks
 */
async function uploadPageContent(db) {
  console.log('\n📦 Uploading page content...');

  const pages = getHtmlPages();
  let uploaded = 0;
  let chunked = 0;
  const MAX_DOC_SIZE = 900000; // 900KB to leave room for metadata

  for (const page of pages) {
    const fullPath = path.join(ROOT_DIR, page.path);
    const content = extractPageContent(fullPath);

    if (content) {
      // Clean undefined values before uploading
      const cleanedContent = cleanUndefined({
        ...content,
        path: page.path,
        category: page.category
      });

      // Check estimated size
      const contentStr = JSON.stringify(cleanedContent);
      const estimatedSize = Buffer.byteLength(contentStr, 'utf8');

      if (estimatedSize > MAX_DOC_SIZE) {
        // Split large pages into chunks
        console.log(`  ⚠ ${page.id} is large (${(estimatedSize/1024/1024).toFixed(2)}MB), splitting...`);

        // Store metadata in main document
        const metadata = {
          title: content.title || '',
          description: content.description || '',
          path: page.path,
          category: page.category,
          isChunked: true,
          chunkCount: 0,
          totalFormulas: content.formulas?.length || 0,
          totalSections: content.sections?.length || 0,
          totalPmRefs: content.pmRefs?.length || 0,
          uploadedAt: admin.firestore.FieldValue.serverTimestamp()
        };

        await db.collection('pages').doc(page.id).set(metadata);

        // Store sections as subcollection
        if (content.sections && content.sections.length > 0) {
          let sectionBatch = db.batch();
          let sectionCount = 0;

          for (let i = 0; i < content.sections.length; i++) {
            const section = content.sections[i];
            const sectionDoc = db.collection('pages').doc(page.id).collection('sections').doc(`section-${i}`);
            const cleanedSection = cleanUndefined(section);
            if (cleanedSection) {
              sectionBatch.set(sectionDoc, cleanedSection);
              sectionCount++;
            }

            // Commit in batches of 400 and create new batch
            if (sectionCount >= 400) {
              await sectionBatch.commit();
              sectionBatch = db.batch();
              sectionCount = 0;
            }
          }

          if (sectionCount > 0) {
            await sectionBatch.commit();
          }
        }

        // Store formulas as subcollection
        if (content.formulas && content.formulas.length > 0) {
          let formulaBatch = db.batch();
          let formulaCount = 0;

          for (let i = 0; i < content.formulas.length; i++) {
            const formula = content.formulas[i];
            const formulaDoc = db.collection('pages').doc(page.id).collection('formulas').doc(`formula-${i}`);
            const cleanedFormula = cleanUndefined(formula);
            if (cleanedFormula) {
              formulaBatch.set(formulaDoc, cleanedFormula);
              formulaCount++;
            }

            if (formulaCount >= 400) {
              await formulaBatch.commit();
              formulaBatch = db.batch();
              formulaCount = 0;
            }
          }

          if (formulaCount > 0) {
            await formulaBatch.commit();
          }
        }

        // Store pmRefs as subcollection
        if (content.pmRefs && content.pmRefs.length > 0) {
          let pmRefBatch = db.batch();
          let pmRefCount = 0;

          for (let i = 0; i < content.pmRefs.length; i++) {
            const pmRef = content.pmRefs[i];
            const pmRefDoc = db.collection('pages').doc(page.id).collection('pmRefs').doc(`pmRef-${i}`);
            const cleanedPmRef = cleanUndefined(pmRef);
            if (cleanedPmRef && Object.keys(cleanedPmRef).length > 0) {
              pmRefBatch.set(pmRefDoc, cleanedPmRef);
              pmRefCount++;
            }

            if (pmRefCount >= 400) {
              await pmRefBatch.commit();
              pmRefBatch = db.batch();
              pmRefCount = 0;
            }
          }

          if (pmRefCount > 0) {
            await pmRefBatch.commit();
          }
        }

        chunked++;
        uploaded++;
      } else {
        // Small enough to upload directly
        cleanedContent.uploadedAt = admin.firestore.FieldValue.serverTimestamp();
        await db.collection('pages').doc(page.id).set(cleanedContent);
        uploaded++;
      }

      if (uploaded % 10 === 0) {
        console.log(`  ✓ Uploaded ${uploaded}/${pages.length} pages`);
      }
    }
  }

  console.log(`  ✓ Total: ${uploaded} pages uploaded (${chunked} were chunked)`);
  return { success: true, count: uploaded, chunked };
}

/**
 * Create validation history entry
 */
async function createValidationEntry(db, results) {
  console.log('\n📦 Creating validation history entry...');

  const theoryOutput = loadTheoryOutput();

  const entry = {
    timestamp: admin.firestore.FieldValue.serverTimestamp(),
    version: theoryOutput.meta?.version || 'unknown',
    uploadResults: results,
    validation: theoryOutput.validation || {},
    predictions_within_1sigma: theoryOutput.validation?.predictions_within_1sigma,
    total_predictions: theoryOutput.validation?.total_predictions,
    exact_matches: theoryOutput.validation?.exact_matches,
    overall_grade: theoryOutput.validation?.overall_grade
  };

  const docId = `upload_${Date.now()}`;
  await db.collection('validation_history').doc(docId).set(entry);
  console.log(`  ✓ Created validation_history/${docId}`);

  return { success: true, docId };
}

/**
 * Main function
 */
async function main() {
  console.log('═'.repeat(70));
  console.log(' PRINCIPIA METAPHYSICA - FIREBASE COMPLETE UPLOAD');
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Force mode: ${FORCE_UPLOAD}`);

  const db = initFirebase();
  const results = {};

  try {
    // Upload theory constants
    results.theoryConstants = await uploadTheoryConstants(db);

    // Upload formulas
    results.formulas = await uploadFormulas(db);

    // Upload page content
    results.pages = await uploadPageContent(db);

    // Create validation entry
    results.validation = await createValidationEntry(db, results);

    console.log('\n' + '═'.repeat(70));
    console.log(' ✅ UPLOAD COMPLETE');
    console.log('═'.repeat(70));

    console.log('\nSummary:');
    console.log(`  Theory constants: v${results.theoryConstants.version}`);
    console.log(`  Formulas: ${results.formulas.count || 0}`);
    console.log(`  Pages: ${results.pages.count || 0}`);

  } catch (error) {
    console.error('\n❌ UPLOAD FAILED:', error);
    process.exit(1);
  }

  process.exit(0);
}

main();
