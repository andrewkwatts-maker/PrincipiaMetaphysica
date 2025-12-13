/**
 * Firebase Website Content Upload Script
 *
 * Uploads ALL website HTML content to Firebase Firestore.
 * Extracts and structures content from all HTML files across the site.
 *
 * SETUP:
 *   1. Install dependencies: npm install
 *   2. Ensure Firebase service account key is in place:
 *      - scripts/serviceAccountKey.json OR
 *      - scripts/principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json OR
 *      - principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json (in root)
 *
 * USAGE:
 *   Dry run (test without uploading):
 *     node scripts/firebase-upload-website-content.js --dry-run
 *
 *   Live upload:
 *     node scripts/firebase-upload-website-content.js
 *
 * WHAT IT DOES:
 *   - Scans ALL HTML files in the project:
 *     * Root pages (index.html, beginners-guide.html, etc.)
 *     * sections/*.html (17 pages)
 *     * foundations/*.html (14 pages)
 *     * docs/*.html
 *     * diagrams/*.html
 *     * components/*.html
 *
 *   - For each page, extracts and uploads to Firestore 'pages' collection:
 *     * id: page identifier (e.g., 'sections-fermion-sector')
 *     * path: relative file path
 *     * title: from <title> tag
 *     * description: from meta description
 *     * mainContent: the main content HTML
 *     * sections: array of section objects with {id, heading, html}
 *     * formulas: array of formula references found in page
 *     * pmValueRefs: array of PM value references (data-category, data-param)
 *     * headings: document outline structure
 *     * links: external links found in page
 *     * lastUpdated: timestamp
 *
 *   - Uses batch uploads for efficiency (400 max per batch)
 *   - Shows progress and detailed summary
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const ROOT_DIR = path.join(__dirname, '..');
const DRY_RUN = process.argv.includes('--dry-run');

// Initialize Firebase
function initFirebase() {
  if (DRY_RUN) {
    console.log('DRY RUN MODE - No data will be uploaded to Firebase');
    return null;
  }

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
 * Extract comprehensive content from HTML file
 */
function extractPageContent(htmlPath, relativePath) {
  if (!fs.existsSync(htmlPath)) {
    console.warn(`  ! File not found: ${relativePath}`);
    return null;
  }

  try {
    const content = fs.readFileSync(htmlPath, 'utf-8');
    const $ = cheerio.load(content);

    // Extract basic metadata
    const title = $('title').text().trim() || $('h1').first().text().trim() || 'Untitled';
    const description = $('meta[name="description"]').attr('content') || '';

    // Extract main content (body, excluding header/footer/nav)
    let mainContent = '';
    const mainElement = $('main, .main-content, .content, article').first();
    if (mainElement.length > 0) {
      mainContent = mainElement.html();
    } else {
      // Fallback: get body content
      const bodyClone = $('body').clone();
      bodyClone.find('header, footer, nav, script, style').remove();
      mainContent = bodyClone.html();
    }

    // Extract all sections
    const sections = [];
    $('section, .section, .subsection, article').each((i, el) => {
      const $el = $(el);
      const id = $el.attr('id') || `section-${i}`;
      const heading = $el.find('h1, h2, h3').first().text().trim();
      const html = $el.html();

      if (html && html.trim().length > 0) {
        sections.push({
          id,
          heading: heading || 'Untitled Section',
          html: html.substring(0, 50000) // Limit section size
        });
      }
    });

    // Extract formulas
    const formulas = [];
    $('.formula-box, .equation, .equation-box, .interactive-formula, [class*="formula"]').each((i, el) => {
      const $el = $(el);
      const formulaData = {
        id: $el.attr('id') || `formula-${i}`,
        html: $el.html(),
        dataRef: $el.attr('data-ref') || null,
        dataFormula: $el.attr('data-formula') || null
      };

      if (formulaData.html && formulaData.html.trim().length > 0) {
        formulas.push(formulaData);
      }
    });

    // Extract PM value references
    const pmValueRefs = [];
    const seenRefs = new Set();

    $('.pm-value, [data-category][data-param]').each((i, el) => {
      const $el = $(el);
      const category = $el.attr('data-category');
      const param = $el.attr('data-param');

      if (category && param) {
        const refKey = `${category}:${param}`;
        if (!seenRefs.has(refKey)) {
          seenRefs.add(refKey);
          pmValueRefs.push({ category, param });
        }
      }
    });

    // Extract headings structure
    const headings = [];
    $('h1, h2, h3, h4').each((i, el) => {
      const $el = $(el);
      const level = parseInt($el.prop('tagName').substring(1));
      const text = $el.text().trim();
      const id = $el.attr('id') || null;

      if (text) {
        headings.push({ level, text, id });
      }
    });

    // Extract links
    const links = [];
    $('a[href]').each((i, el) => {
      const $el = $(el);
      const href = $el.attr('href');
      const text = $el.text().trim();

      if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
        links.push({ href, text });
      }
    });

    return {
      title,
      description,
      mainContent: mainContent ? mainContent.substring(0, 100000) : '', // Limit total size
      sections,
      formulas,
      pmValueRefs,
      headings,
      links: links.slice(0, 100), // Limit number of links
      lastUpdated: new Date().toISOString()
    };

  } catch (error) {
    console.error(`  ! Error parsing ${relativePath}:`, error.message);
    return null;
  }
}

/**
 * Get all HTML pages to process
 */
function getHtmlPages() {
  const pages = [];

  // Root pages (main site pages)
  const rootFiles = [
    'index.html',
    'principia-metaphysica-paper.html',
    'references.html',
    'beginners-guide.html',
    'philosophical-implications.html',
    'visualization-index.html',
    'ancient-numerology.html',
    'proverbs-31-wife-of-noble-character.html',
    'appendices_content.html'
  ];

  rootFiles.forEach(file => {
    const fullPath = path.join(ROOT_DIR, file);
    if (fs.existsSync(fullPath)) {
      pages.push({
        id: file.replace('.html', ''),
        path: file,
        fullPath,
        category: 'root'
      });
    }
  });

  // Directory-based pages
  const directories = [
    { dir: 'sections', category: 'sections', prefix: 'sections-' },
    { dir: 'foundations', category: 'foundations', prefix: 'foundations-' },
    { dir: 'docs', category: 'docs', prefix: 'docs-' },
    { dir: 'diagrams', category: 'diagrams', prefix: 'diagrams-' },
    { dir: 'components', category: 'components', prefix: 'components-' }
  ];

  directories.forEach(({ dir, category, prefix }) => {
    const dirPath = path.join(ROOT_DIR, dir);

    if (fs.existsSync(dirPath)) {
      try {
        const files = fs.readdirSync(dirPath);

        files.forEach(file => {
          if (file.endsWith('.html')) {
            const fullPath = path.join(dirPath, file);
            const fileName = file.replace('.html', '');

            // Skip index files in subdirectories (they're usually navigation)
            if (fileName === 'index') {
              pages.push({
                id: `${prefix}index`,
                path: `${dir}/${file}`,
                fullPath,
                category
              });
            } else {
              pages.push({
                id: `${prefix}${fileName}`,
                path: `${dir}/${file}`,
                fullPath,
                category
              });
            }
          }
        });
      } catch (error) {
        console.warn(`  ! Could not read directory ${dir}:`, error.message);
      }
    }
  });

  return pages;
}

/**
 * Upload page content to Firestore
 */
async function uploadPageContent(db) {
  console.log('\n' + '='.repeat(70));
  console.log(' UPLOADING WEBSITE CONTENT TO FIREBASE');
  console.log('='.repeat(70));

  const pages = getHtmlPages();
  console.log(`\nFound ${pages.length} HTML files to process\n`);

  const stats = {
    total: pages.length,
    success: 0,
    skipped: 0,
    failed: 0,
    byCategory: {}
  };

  // Process pages in batches
  const BATCH_SIZE = 400; // Firestore batch limit is 500
  let currentBatch = DRY_RUN ? null : db.batch();
  let batchCount = 0;
  let batchNumber = 1;

  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    const { id, path: relativePath, fullPath, category } = page;

    // Extract content
    const content = extractPageContent(fullPath, relativePath);

    if (!content) {
      stats.skipped++;
      continue;
    }

    // Track category stats
    if (!stats.byCategory[category]) {
      stats.byCategory[category] = 0;
    }
    stats.byCategory[category]++;

    // Prepare document data
    const docData = {
      id,
      path: relativePath,
      category,
      title: content.title,
      description: content.description,
      mainContent: content.mainContent,
      sections: content.sections,
      formulas: content.formulas,
      pmValueRefs: content.pmValueRefs,
      headings: content.headings,
      links: content.links,
      lastUpdated: content.lastUpdated,
      uploadedAt: DRY_RUN ? new Date().toISOString() : admin.firestore.FieldValue.serverTimestamp()
    };

    if (DRY_RUN) {
      // Dry run: just show what would be uploaded
      console.log(`[DRY RUN] Would upload: ${id}`);
      console.log(`  Path: ${relativePath}`);
      console.log(`  Title: ${content.title}`);
      console.log(`  Sections: ${content.sections.length}`);
      console.log(`  Formulas: ${content.formulas.length}`);
      console.log(`  PM Refs: ${content.pmValueRefs.length}`);
      console.log(`  Headings: ${content.headings.length}`);
      console.log('');
      stats.success++;
    } else {
      try {
        const docRef = db.collection('pages').doc(id);
        currentBatch.set(docRef, docData);
        batchCount++;
        stats.success++;

        // Show progress
        if ((i + 1) % 10 === 0 || i === pages.length - 1) {
          console.log(`  Progress: ${i + 1}/${pages.length} pages processed`);
        }

        // Commit batch when it reaches size limit
        if (batchCount >= BATCH_SIZE) {
          await currentBatch.commit();
          console.log(`  ✓ Committed batch #${batchNumber} (${batchCount} documents)`);
          currentBatch = db.batch();
          batchCount = 0;
          batchNumber++;
        }
      } catch (error) {
        console.error(`  ! Failed to add ${id} to batch:`, error.message);
        stats.failed++;
      }
    }
  }

  // Commit remaining batch
  if (!DRY_RUN && batchCount > 0) {
    try {
      await currentBatch.commit();
      console.log(`  ✓ Committed final batch #${batchNumber} (${batchCount} documents)`);
    } catch (error) {
      console.error('  ! Failed to commit final batch:', error.message);
      stats.failed += batchCount;
      stats.success -= batchCount;
    }
  }

  return stats;
}

/**
 * Main function
 */
async function main() {
  console.log('\n' + '='.repeat(70));
  console.log(' PRINCIPIA METAPHYSICA - WEBSITE CONTENT UPLOAD');
  console.log('='.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log(`Mode: ${DRY_RUN ? 'DRY RUN (no upload)' : 'LIVE UPLOAD'}`);

  const db = initFirebase();

  try {
    const stats = await uploadPageContent(db);

    console.log('\n' + '='.repeat(70));
    console.log(DRY_RUN ? ' DRY RUN COMPLETE' : ' UPLOAD COMPLETE');
    console.log('='.repeat(70));

    console.log('\nSummary:');
    console.log(`  Total files: ${stats.total}`);
    console.log(`  Successfully ${DRY_RUN ? 'processed' : 'uploaded'}: ${stats.success}`);
    console.log(`  Skipped: ${stats.skipped}`);
    console.log(`  Failed: ${stats.failed}`);

    console.log('\nBy Category:');
    Object.entries(stats.byCategory)
      .sort(([a], [b]) => a.localeCompare(b))
      .forEach(([category, count]) => {
        console.log(`  ${category}: ${count} pages`);
      });

    if (!DRY_RUN && stats.success > 0) {
      console.log('\n✓ All content uploaded to Firestore collection: pages');
      console.log('  Each document ID corresponds to the page identifier');
      console.log('  Query by category field to get pages by section');
    }

    if (DRY_RUN) {
      console.log('\nTo perform actual upload, run without --dry-run flag:');
      console.log('  node scripts/firebase-upload-website-content.js');
    }

  } catch (error) {
    console.error('\n✗ UPLOAD FAILED:', error);
    console.error(error.stack);
    process.exit(1);
  }

  process.exit(0);
}

main();
