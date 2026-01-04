#!/usr/bin/env node

/**
 * Migrate References to Firebase
 *
 * Parses references from references.html and uploads to Firestore.
 * Creates structured reference documents with full metadata.
 *
 * Usage: node scripts/migrate-references-to-firebase.js [--dry-run]
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Initialize Firebase Admin
const serviceAccount = require('../firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: 'principia-metaphysica'
});

const db = admin.firestore();

// Command line arguments
const args = process.argv.slice(2);
const isDryRun = args.includes('--dry-run');

/**
 * Parse references.html and extract reference data
 * @returns {Array} Array of parsed reference objects
 */
function parseReferencesHTML() {
  const htmlPath = path.join(__dirname, '..', 'references.html');
  const html = fs.readFileSync(htmlPath, 'utf-8');
  const dom = new JSDOM(html);
  const document = dom.window.document;

  const references = [];
  const categories = document.querySelectorAll('.ref-category');

  console.log(`Found ${categories.length} reference categories`);

  categories.forEach(categorySection => {
    const categoryId = categorySection.id;
    const categoryTitle = categorySection.querySelector('h3')?.textContent || '';

    console.log(`\nProcessing category: ${categoryId} - ${categoryTitle}`);

    const refItems = categorySection.querySelectorAll('.ref-item');

    refItems.forEach(refItem => {
      const ref = parseReferenceItem(refItem, categoryId);
      if (ref) {
        references.push(ref);
      }
    });
  });

  console.log(`\nTotal references parsed: ${references.length}`);
  return references;
}

/**
 * Parse a single reference item element
 * @param {Element} refItem - The .ref-item DOM element
 * @param {string} category - Category identifier
 * @returns {Object|null} Parsed reference object
 */
function parseReferenceItem(refItem, category) {
  try {
    const id = refItem.id;
    if (!id) {
      console.warn('Reference item missing ID, skipping');
      return null;
    }

    // Extract title
    const titleEl = refItem.querySelector('.ref-title');
    const title = titleEl ? titleEl.textContent.trim() : '';

    // Extract authors
    const authorsEl = refItem.querySelector('.ref-authors');
    const authors = authorsEl ? authorsEl.textContent.trim() : '';

    // Extract journal/publication info
    const journalEl = refItem.querySelector('.ref-journal');
    const journal = journalEl ? journalEl.textContent.trim() : '';

    // Extract year from journal string
    const yearMatch = journal.match(/\((\d{4})\)/);
    const year = yearMatch ? parseInt(yearMatch[1]) : null;

    // Extract links
    const links = [];
    const linkEls = refItem.querySelectorAll('.ref-links a');
    linkEls.forEach(a => {
      const url = a.href;
      const label = a.textContent.replace('→', '').trim();
      links.push({ label, url });
    });

    // Extract DOI and arXiv from links
    let doi = null;
    let arxiv = null;
    links.forEach(link => {
      if (link.url.includes('doi.org')) {
        doi = link.url.replace('https://doi.org/', '');
      } else if (link.url.includes('arxiv.org')) {
        const arxivMatch = link.url.match(/arxiv\.org\/abs\/([^\s&]+)/);
        if (arxivMatch) {
          arxiv = arxivMatch[1];
        }
      }
    });

    // Extract description (if available)
    let description = '';
    const descEl = refItem.querySelector('div[style*="background: rgba(139, 127, 255, 0.08)"]');
    if (descEl) {
      description = descEl.textContent.trim();
    }

    // Extract tags
    const tags = [];
    const tagEls = refItem.querySelectorAll('.ref-tag');
    tagEls.forEach(tag => {
      tags.push(tag.textContent.trim());
    });

    // Determine reference type
    const type = determineReferenceType(tags, journal);

    // Generate citation key (e.g., "Einstein 1915")
    const citationKey = generateCitationKey(authors, year);

    // Parse volume and pages from journal string
    const { volume, pages } = parseJournalInfo(journal);

    const reference = {
      id,
      title,
      authors,
      journal,
      year,
      volume,
      pages,
      doi,
      arxiv,
      links,
      description,
      tags,
      category,
      type,
      citation_key: citationKey,
      cited_in_formulas: [],
      cited_in_sections: [],
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    };

    console.log(`  ✓ Parsed: ${id} - ${citationKey}`);
    return reference;

  } catch (error) {
    console.error(`Error parsing reference item:`, error);
    return null;
  }
}

/**
 * Determine reference type from tags and journal info
 * @param {Array} tags - Array of tag strings
 * @param {string} journal - Journal string
 * @returns {string} Reference type
 */
function determineReferenceType(tags, journal) {
  const tagStr = tags.join(' ').toLowerCase();
  const journalLower = journal.toLowerCase();

  if (tagStr.includes('textbook') || journalLower.includes('isbn')) {
    return 'textbook';
  } else if (tagStr.includes('review') || journalLower.includes('review')) {
    return 'review';
  } else if (tagStr.includes('experimental') || tagStr.includes('atlas') || tagStr.includes('super-kamiokande')) {
    return 'experimental';
  } else {
    return 'theoretical';
  }
}

/**
 * Generate citation key from author and year
 * Examples: "Einstein 1915", "Joyce 2000", "Acharya et al. 1998"
 * @param {string} authors - Authors string
 * @param {number} year - Publication year
 * @returns {string} Citation key
 */
function generateCitationKey(authors, year) {
  if (!authors || !year) return '';

  // Split authors and get first author's last name
  const authorList = authors.split(',');
  const firstAuthor = authorList[0].trim();

  // Extract last name (handle various formats)
  let lastName = firstAuthor;
  if (firstAuthor.includes('.')) {
    // Format: "Last, A.B." or "Initials. Last"
    const parts = firstAuthor.split('.');
    lastName = parts[parts.length - 1].trim();
  }

  // Clean up any remaining commas or periods
  lastName = lastName.replace(/[,\.]/g, '').trim();

  // Add "et al." if multiple authors
  const etAl = authorList.length > 2 ? ' et al.' : '';

  return `${lastName}${etAl} ${year}`;
}

/**
 * Parse volume and pages from journal string
 * @param {string} journal - Journal citation string
 * @returns {Object} { volume, pages }
 */
function parseJournalInfo(journal) {
  let volume = null;
  let pages = null;

  // Try to extract volume: "Vol. 123" or "123(4)"
  const volumeMatch = journal.match(/(?:Vol\.\s*|volume\s*)(\d+)|(\d+)\s*\(/i);
  if (volumeMatch) {
    volume = volumeMatch[1] || volumeMatch[2];
  }

  // Try to extract pages: "pp. 123-456" or ": 123-456"
  const pagesMatch = journal.match(/(?:pp\.\s*|pages?\s*|:\s*)(\d+[-–]\d+)/i);
  if (pagesMatch) {
    pages = pagesMatch[1];
  }

  return { volume, pages };
}

/**
 * Generate BibTeX for a reference
 * @param {Object} ref - Reference object
 * @returns {string} BibTeX formatted string
 */
function generateBibTeX(ref) {
  const type = ref.type === 'textbook' ? 'book' : 'article';
  const key = ref.id;

  let bibtex = `@${type}{${key},\n`;
  bibtex += `  author = {${ref.authors}},\n`;
  bibtex += `  title = {${ref.title}},\n`;

  if (ref.journal && ref.type !== 'textbook') {
    bibtex += `  journal = {${ref.journal.split('(')[0].trim()}},\n`;
  } else if (ref.type === 'textbook') {
    bibtex += `  publisher = {${ref.journal.split('ISBN')[0].trim()}},\n`;
  }

  if (ref.year) bibtex += `  year = {${ref.year}},\n`;
  if (ref.volume) bibtex += `  volume = {${ref.volume}},\n`;
  if (ref.pages) bibtex += `  pages = {${ref.pages}},\n`;
  if (ref.doi) bibtex += `  doi = {${ref.doi}},\n`;

  if (ref.arxiv) {
    bibtex += `  eprint = {${ref.arxiv}},\n`;
    bibtex += `  archivePrefix = {arXiv},\n`;
  }

  // Remove trailing comma
  bibtex = bibtex.replace(/,\n$/, '\n');
  bibtex += '}';

  return bibtex;
}

/**
 * Upload references to Firestore
 * @param {Array} references - Array of reference objects
 */
async function uploadReferences(references) {
  console.log('\n=== Uploading References to Firestore ===\n');

  const batch = db.batch();
  let batchCount = 0;
  const maxBatchSize = 500; // Firestore limit

  for (const ref of references) {
    // Generate BibTeX
    ref.bibtex = generateBibTeX(ref);

    if (isDryRun) {
      console.log(`[DRY RUN] Would upload: ${ref.id}`);
      console.log(JSON.stringify(ref, null, 2));
      console.log('\nBibTeX:');
      console.log(ref.bibtex);
      console.log('\n---\n');
    } else {
      const docRef = db.collection('references').doc(ref.id);
      batch.set(docRef, ref);
      batchCount++;

      if (batchCount >= maxBatchSize) {
        console.log(`Committing batch of ${batchCount} references...`);
        await batch.commit();
        batchCount = 0;
      }
    }
  }

  if (!isDryRun && batchCount > 0) {
    console.log(`Committing final batch of ${batchCount} references...`);
    await batch.commit();
  }

  if (isDryRun) {
    console.log(`\n[DRY RUN] Would have uploaded ${references.length} references`);
  } else {
    console.log(`\n✓ Successfully uploaded ${references.length} references to Firestore`);
  }
}

/**
 * Create Firestore indexes for efficient querying
 */
async function createIndexes() {
  console.log('\n=== Firestore Index Configuration ===\n');
  console.log('The following indexes should be created in Firebase Console:');
  console.log('\nCollection: references');
  console.log('1. Composite index: category (Ascending) + year (Ascending)');
  console.log('2. Composite index: type (Ascending) + year (Ascending)');
  console.log('3. Single field index: citation_key (Ascending)');
  console.log('4. Array-contains index: cited_in_formulas');
  console.log('5. Array-contains index: cited_in_sections');
  console.log('\nOr use the Firebase CLI with firestore.indexes.json');
}

/**
 * Generate Firestore index configuration file
 * @param {string} outputPath - Path to save indexes.json
 */
function generateIndexConfig(outputPath) {
  const indexConfig = {
    indexes: [
      {
        collectionGroup: 'references',
        queryScope: 'COLLECTION',
        fields: [
          { fieldPath: 'category', order: 'ASCENDING' },
          { fieldPath: 'year', order: 'ASCENDING' }
        ]
      },
      {
        collectionGroup: 'references',
        queryScope: 'COLLECTION',
        fields: [
          { fieldPath: 'type', order: 'ASCENDING' },
          { fieldPath: 'year', order: 'ASCENDING' }
        ]
      }
    ],
    fieldOverrides: [
      {
        collectionGroup: 'references',
        fieldPath: 'citation_key',
        indexes: [
          { order: 'ASCENDING', queryScope: 'COLLECTION' }
        ]
      },
      {
        collectionGroup: 'references',
        fieldPath: 'cited_in_formulas',
        indexes: [
          { arrayConfig: 'CONTAINS', queryScope: 'COLLECTION' }
        ]
      },
      {
        collectionGroup: 'references',
        fieldPath: 'cited_in_sections',
        indexes: [
          { arrayConfig: 'CONTAINS', queryScope: 'COLLECTION' }
        ]
      }
    ]
  };

  fs.writeFileSync(outputPath, JSON.stringify(indexConfig, null, 2));
  console.log(`\n✓ Index configuration saved to ${outputPath}`);
  console.log('Deploy with: firebase deploy --only firestore:indexes');
}

/**
 * Print summary statistics
 * @param {Array} references - Array of reference objects
 */
function printSummary(references) {
  console.log('\n=== Migration Summary ===\n');

  // Count by category
  const byCategory = {};
  const byType = {};
  let withDOI = 0;
  let withArXiv = 0;

  references.forEach(ref => {
    byCategory[ref.category] = (byCategory[ref.category] || 0) + 1;
    byType[ref.type] = (byType[ref.type] || 0) + 1;
    if (ref.doi) withDOI++;
    if (ref.arxiv) withArXiv++;
  });

  console.log('References by Category:');
  Object.entries(byCategory)
    .sort((a, b) => b[1] - a[1])
    .forEach(([cat, count]) => {
      console.log(`  ${cat}: ${count}`);
    });

  console.log('\nReferences by Type:');
  Object.entries(byType).forEach(([type, count]) => {
    console.log(`  ${type}: ${count}`);
  });

  console.log(`\nReferences with DOI: ${withDOI}`);
  console.log(`References with arXiv: ${withArXiv}`);
  console.log(`\nTotal References: ${references.length}`);
}

/**
 * Main migration function
 */
async function main() {
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║   Principia Metaphysica - References Migration to Firebase   ║');
  console.log('╚═══════════════════════════════════════════════════════════╝\n');

  if (isDryRun) {
    console.log('🔍 DRY RUN MODE - No data will be uploaded\n');
  }

  try {
    // Parse references from HTML
    const references = parseReferencesHTML();

    // Print summary
    printSummary(references);

    // Upload to Firestore
    await uploadReferences(references);

    // Generate index config
    const indexPath = path.join(__dirname, '..', 'firestore.indexes.json');
    generateIndexConfig(indexPath);

    // Print index instructions
    createIndexes();

    console.log('\n✅ Migration completed successfully!\n');

    if (!isDryRun) {
      console.log('Next steps:');
      console.log('1. Deploy indexes: firebase deploy --only firestore:indexes');
      console.log('2. Test references module: node scripts/test-references.js');
      console.log('3. Update references.html to use firebase-references.js\n');
    }

  } catch (error) {
    console.error('\n❌ Migration failed:', error);
    process.exit(1);
  }

  process.exit(0);
}

// Run migration
main();
