/**
 * Extract Page Content and Upload to Firebase Firestore
 *
 * This script reads HTML files from sections/, foundations/, and docs/,
 * extracts structured content including formulas and PM value references,
 * and uploads to Firebase Firestore 'pages' collection.
 *
 * Usage: node scripts/extract-page-content.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const ROOT_DIR = path.join(__dirname, '..');

// Initialize Firebase
function initFirebase() {
  const serviceAccountPath = path.join(__dirname, 'serviceAccountKey.json');

  if (!fs.existsSync(serviceAccountPath)) {
    console.error('ERROR: serviceAccountKey.json not found in scripts/ folder');
    console.error('Download from Firebase Console > Project Settings > Service Accounts');
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
 * Get all HTML pages to process
 */
function getHtmlPages() {
  const pages = [];

  // Section pages
  const sectionsDir = path.join(ROOT_DIR, 'sections');
  if (fs.existsSync(sectionsDir)) {
    fs.readdirSync(sectionsDir).forEach(file => {
      if (file.endsWith('.html') && file !== 'index.html') {
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
      if (file.endsWith('.html') && file !== 'index.html') {
        pages.push({
          id: `foundations-${file.replace('.html', '')}`,
          path: `foundations/${file}`,
          category: 'foundations'
        });
      }
    });
  }

  // Specific docs pages
  const docsPages = [
    'computational-appendices.html',
    'beginners-guide-printable.html'
  ];

  docsPages.forEach(file => {
    const fullPath = path.join(ROOT_DIR, 'docs', file);
    if (fs.existsSync(fullPath)) {
      pages.push({
        id: `docs-${file.replace('.html', '')}`,
        path: `docs/${file}`,
        category: 'docs'
      });
    }
  });

  return pages;
}

/**
 * Extract main content from HTML
 */
function extractMainContent($, selector = 'main') {
  const mainElement = $(selector);
  if (mainElement.length > 0) {
    return mainElement.html();
  }

  // Fallback to article
  const articleElement = $('article');
  if (articleElement.length > 0) {
    return articleElement.html();
  }

  // Fallback to container
  const containerElement = $('.container');
  if (containerElement.length > 0) {
    return containerElement.html();
  }

  return null;
}

/**
 * Extract sections from main content
 */
function extractSections($) {
  const sections = [];

  // Look for section elements, subsections, and divs with section-like classes
  const sectionSelectors = [
    'main section',
    'main .subsection',
    'main .section',
    'article section',
    'section.section-header'
  ];

  sectionSelectors.forEach(selector => {
    $(selector).each((i, el) => {
      const $el = $(el);
      const id = $el.attr('id') || `section-${sections.length}`;

      // Extract heading (h1, h2, h3, or h4)
      const heading = $el.find('h1, h2, h3, h4').first().text().trim();

      // Get the HTML content
      const content = $el.html();

      if (content && content.length > 0) {
        sections.push({
          id,
          heading: heading || 'Untitled Section',
          content
        });
      }
    });
  });

  return sections;
}

/**
 * Extract formulas and their metadata
 */
function extractFormulas($) {
  const formulas = [];
  const seen = new Set(); // Prevent duplicates

  // Look for formula containers
  const formulaSelectors = [
    '.formula-box',
    '.equation',
    '.interactive-formula',
    '.formula-container',
    '[data-formula]',
    '[data-ref]'
  ];

  formulaSelectors.forEach(selector => {
    $(selector).each((i, el) => {
      const $el = $(el);
      const id = $el.attr('id') ||
                 $el.attr('data-formula') ||
                 $el.attr('data-ref') ||
                 `formula-${formulas.length}`;

      // Skip if we've already seen this ID
      if (seen.has(id)) return;
      seen.add(id);

      const html = $el.html();
      const latexRef = $el.attr('data-ref') || $el.attr('data-formula') || null;
      const label = $el.find('.formula-label').text().trim() || null;

      formulas.push({
        id,
        html,
        latexRef,
        label
      });
    });
  });

  return formulas;
}

/**
 * Extract PM value references
 */
function extractPMValueRefs($) {
  const pmRefs = [];
  const seen = new Set(); // Prevent duplicates

  $('.pm-value').each((i, el) => {
    const $el = $(el);
    const category = $el.attr('data-category');
    const param = $el.attr('data-param');
    const format = $el.attr('data-format');

    // Skip if missing required fields
    if (!category || !param) return;

    // Create unique key
    const key = `${category}:${param}`;
    if (seen.has(key)) return;
    seen.add(key);

    pmRefs.push({
      category,
      param,
      format: format || null
    });
  });

  return pmRefs;
}

/**
 * Extract full page content with all metadata
 */
function extractPageContent(htmlPath) {
  if (!fs.existsSync(htmlPath)) {
    console.warn(`File not found: ${htmlPath}`);
    return null;
  }

  try {
    const content = fs.readFileSync(htmlPath, 'utf-8');
    const $ = cheerio.load(content);

    // Extract title
    const title = $('title').text().trim() ||
                  $('h1').first().text().trim() ||
                  'Untitled';

    // Extract description
    const description = $('meta[name="description"]').attr('content') || '';

    // Extract main content HTML
    const mainContent = extractMainContent($);

    // Extract sections
    const sections = extractSections($);

    // Extract formulas
    const formulas = extractFormulas($);

    // Extract PM value references
    const pmValueRefs = extractPMValueRefs($);

    // Get version from theory-constants script tag if present
    const version = '12.7'; // Default version

    return {
      title,
      description,
      mainContent,
      sections,
      formulas,
      pmValueRefs,
      metadata: {
        extractedAt: new Date().toISOString(),
        version,
        sectionCount: sections.length,
        formulaCount: formulas.length,
        pmValueRefCount: pmValueRefs.length
      }
    };
  } catch (error) {
    console.error(`Error extracting content from ${htmlPath}:`, error.message);
    return null;
  }
}

/**
 * Upload all page content to Firebase
 */
async function uploadPageContent(db) {
  console.log('\n' + '='.repeat(70));
  console.log(' EXTRACTING AND UPLOADING PAGE CONTENT TO FIREBASE');
  console.log('='.repeat(70));

  const pages = getHtmlPages();
  console.log(`\nFound ${pages.length} pages to process\n`);

  let uploaded = 0;
  let failed = 0;
  const results = [];

  for (const page of pages) {
    const fullPath = path.join(ROOT_DIR, page.path);
    console.log(`Processing: ${page.path}`);

    const content = extractPageContent(fullPath);

    if (content) {
      try {
        await db.collection('pages').doc(page.id).set({
          id: page.id,
          path: page.path,
          category: page.category,
          ...content,
          uploadedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        uploaded++;
        results.push({
          id: page.id,
          path: page.path,
          status: 'success',
          sections: content.metadata.sectionCount,
          formulas: content.metadata.formulaCount,
          pmValueRefs: content.metadata.pmValueRefCount
        });

        console.log(`  ✓ Uploaded: ${page.id}`);
        console.log(`    - Sections: ${content.metadata.sectionCount}`);
        console.log(`    - Formulas: ${content.metadata.formulaCount}`);
        console.log(`    - PM Value Refs: ${content.metadata.pmValueRefCount}\n`);
      } catch (error) {
        failed++;
        results.push({
          id: page.id,
          path: page.path,
          status: 'failed',
          error: error.message
        });
        console.error(`  ✗ Failed: ${page.id} - ${error.message}\n`);
      }
    } else {
      failed++;
      results.push({
        id: page.id,
        path: page.path,
        status: 'failed',
        error: 'Content extraction failed'
      });
      console.error(`  ✗ Failed: ${page.id} - Content extraction failed\n`);
    }
  }

  console.log('='.repeat(70));
  console.log(' UPLOAD SUMMARY');
  console.log('='.repeat(70));
  console.log(`Total pages: ${pages.length}`);
  console.log(`Successfully uploaded: ${uploaded}`);
  console.log(`Failed: ${failed}`);
  console.log('='.repeat(70));

  // Display detailed results
  console.log('\nDetailed Results:');
  results.forEach(result => {
    if (result.status === 'success') {
      console.log(`✓ ${result.id}: ${result.sections} sections, ${result.formulas} formulas, ${result.pmValueRefs} PM refs`);
    } else {
      console.log(`✗ ${result.id}: ${result.error}`);
    }
  });

  return { success: uploaded > 0, uploaded, failed, results };
}

/**
 * Main function
 */
async function main() {
  try {
    const db = initFirebase();
    const result = await uploadPageContent(db);

    if (result.success) {
      console.log('\n✅ Page content extraction and upload complete!');
      process.exit(0);
    } else {
      console.error('\n❌ All uploads failed');
      process.exit(1);
    }
  } catch (error) {
    console.error('\n❌ ERROR:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

// Export functions for use in other scripts
module.exports = {
  extractPageContent,
  getHtmlPages,
  uploadPageContent
};
