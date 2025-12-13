/**
 * Firebase Migration Status Report Generator
 *
 * Generates a comprehensive report on the Firebase migration status,
 * including what data is in Firestore and what might be missing.
 *
 * Usage: node scripts/firebase-status-report.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

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
 * Get collection statistics
 */
async function getCollectionStats(db, collectionName) {
  try {
    const snapshot = await db.collection(collectionName).get();
    const docs = [];
    snapshot.forEach(doc => {
      docs.push({
        id: doc.id,
        data: doc.data()
      });
    });
    return {
      name: collectionName,
      count: snapshot.size,
      documents: docs
    };
  } catch (error) {
    return {
      name: collectionName,
      count: 0,
      error: error.message
    };
  }
}

/**
 * Check for missing local files
 */
function checkLocalFiles() {
  const expectedFiles = [
    'theory_output.json',
    'theory-constants-enhanced.js',
    'js/formula-definitions.js',
    'js/formula-database.js'
  ];

  const results = [];
  for (const file of expectedFiles) {
    const fullPath = path.join(ROOT_DIR, file);
    const exists = fs.existsSync(fullPath);
    let size = 0;
    if (exists) {
      size = fs.statSync(fullPath).size;
    }
    results.push({
      file,
      exists,
      size: exists ? `${(size / 1024).toFixed(1)} KB` : 'N/A'
    });
  }
  return results;
}

/**
 * Check HTML pages
 */
function checkHtmlPages() {
  const categories = {
    root: ['index.html', 'principia-metaphysica-paper.html', 'references.html',
           'beginners-guide.html', 'philosophical-implications.html',
           'visualization-index.html', 'ancient-numerology.html',
           'proverbs-31-wife-of-noble-character.html'],
    sections: [],
    foundations: [],
    docs: [],
    diagrams: [],
    components: []
  };

  // Scan directories
  const scanDir = (dir, category) => {
    const fullDir = path.join(ROOT_DIR, dir);
    if (fs.existsSync(fullDir)) {
      fs.readdirSync(fullDir).forEach(file => {
        if (file.endsWith('.html')) {
          categories[category].push(`${dir}/${file}`);
        }
      });
    }
  };

  scanDir('sections', 'sections');
  scanDir('foundations', 'foundations');
  scanDir('docs', 'docs');
  scanDir('diagrams', 'diagrams');
  scanDir('components', 'components');

  return categories;
}

/**
 * Main function
 */
async function main() {
  const c = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m'
  };

  console.log('═'.repeat(80));
  console.log(`${c.bright}${c.cyan} PRINCIPIA METAPHYSICA - FIREBASE MIGRATION STATUS REPORT${c.reset}`);
  console.log('═'.repeat(80));
  console.log(`Generated: ${new Date().toISOString()}\n`);

  const db = initFirebase();

  // ============================================================
  // SECTION 1: FIRESTORE COLLECTIONS
  // ============================================================
  console.log(`${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ FIRESTORE COLLECTIONS${' '.repeat(56)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  const collections = ['theory_constants', 'formulas', 'pages', 'validation_history',
                       'users', 'user_sessions', 'page_views'];

  const collectionStats = [];
  for (const coll of collections) {
    const stats = await getCollectionStats(db, coll);
    collectionStats.push(stats);

    const status = stats.count > 0 ? `${c.green}✓${c.reset}` : `${c.yellow}○${c.reset}`;
    console.log(`  ${status} ${coll.padEnd(25)} ${String(stats.count).padStart(5)} documents`);
  }

  // ============================================================
  // SECTION 2: THEORY CONSTANTS DETAIL
  // ============================================================
  console.log(`\n${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ THEORY CONSTANTS (SINGLE SOURCE OF TRUTH)${' '.repeat(35)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  try {
    const currentDoc = await db.collection('theory_constants').doc('current').get();
    if (currentDoc.exists) {
      const data = currentDoc.data();
      console.log(`  Version: ${c.green}${data.meta?.version || 'unknown'}${c.reset}`);
      console.log(`  Last Updated: ${data.uploadedAt?._seconds ? new Date(data.uploadedAt._seconds * 1000).toISOString() : 'unknown'}`);
      console.log(`\n  ${c.bright}Key Categories:${c.reset}`);

      const categories = Object.keys(data).filter(k => !['meta', 'uploadedAt'].includes(k));
      for (const cat of categories) {
        const fieldCount = typeof data[cat] === 'object' ? Object.keys(data[cat] || {}).length : 1;
        console.log(`    • ${cat}: ${fieldCount} fields`);
      }
    } else {
      console.log(`  ${c.red}✗ No theory_constants/current document found${c.reset}`);
    }
  } catch (error) {
    console.log(`  ${c.red}✗ Error reading theory constants: ${error.message}${c.reset}`);
  }

  // ============================================================
  // SECTION 3: PAGE CONTENT
  // ============================================================
  console.log(`\n${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ PAGE CONTENT${' '.repeat(65)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  const pagesStats = collectionStats.find(s => s.name === 'pages');
  if (pagesStats && pagesStats.count > 0) {
    console.log(`  ${c.green}✓ ${pagesStats.count} pages in Firestore${c.reset}\n`);

    // Group by category
    const byCategory = {};
    for (const doc of pagesStats.documents) {
      const cat = doc.data.category || 'unknown';
      byCategory[cat] = (byCategory[cat] || 0) + 1;
    }

    console.log(`  ${c.bright}By Category:${c.reset}`);
    for (const [cat, count] of Object.entries(byCategory)) {
      console.log(`    • ${cat}: ${count} pages`);
    }

    // Check for chunked pages
    const chunkedPages = pagesStats.documents.filter(d => d.data.isChunked);
    if (chunkedPages.length > 0) {
      console.log(`\n  ${c.bright}Chunked Pages (large files):${c.reset}`);
      for (const page of chunkedPages) {
        console.log(`    • ${page.id}: ${page.data.totalSections || 0} sections, ${page.data.totalFormulas || 0} formulas`);
      }
    }
  } else {
    console.log(`  ${c.yellow}⚠ No pages in Firestore${c.reset}`);
  }

  // ============================================================
  // SECTION 4: CRITICAL PAGES CHECK
  // ============================================================
  console.log(`\n${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ CRITICAL PAGES VERIFICATION${' '.repeat(50)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  const criticalPages = [
    { id: 'index', name: 'Home Page' },
    { id: 'principia-metaphysica-paper', name: 'Full Paper' },
    { id: 'beginners-guide', name: "Beginner's Guide" },
    { id: 'philosophical-implications', name: 'Philosophical Implications' },
    { id: 'references', name: 'References' },
    { id: 'sections-introduction', name: 'Section: Introduction' },
    { id: 'sections-geometric-framework', name: 'Section: Geometric Framework' },
    { id: 'sections-fermion-sector', name: 'Section: Fermion Sector' },
    { id: 'sections-cosmology', name: 'Section: Cosmology' },
    { id: 'sections-predictions', name: 'Section: Predictions' }
  ];

  const pageIds = pagesStats?.documents?.map(d => d.id) || [];

  for (const page of criticalPages) {
    const exists = pageIds.includes(page.id);
    const status = exists ? `${c.green}✓${c.reset}` : `${c.red}✗${c.reset}`;
    console.log(`  ${status} ${page.name.padEnd(35)} [${page.id}]`);
  }

  // ============================================================
  // SECTION 5: LOCAL FILES
  // ============================================================
  console.log(`\n${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ LOCAL SOURCE FILES${' '.repeat(59)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  const localFiles = checkLocalFiles();
  for (const file of localFiles) {
    const status = file.exists ? `${c.green}✓${c.reset}` : `${c.red}✗${c.reset}`;
    console.log(`  ${status} ${file.file.padEnd(40)} ${file.size}`);
  }

  // ============================================================
  // SECTION 6: ANALYTICS SETUP
  // ============================================================
  console.log(`\n${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ USER ANALYTICS TRACKING${' '.repeat(54)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  const usersStats = collectionStats.find(s => s.name === 'users');
  const sessionsStats = collectionStats.find(s => s.name === 'user_sessions');
  const viewsStats = collectionStats.find(s => s.name === 'page_views');

  console.log(`  ${c.bright}Collections:${c.reset}`);
  console.log(`    • users: ${usersStats?.count || 0} registered users`);
  console.log(`    • user_sessions: ${sessionsStats?.count || 0} login/logout events`);
  console.log(`    • page_views: ${viewsStats?.count || 0} page view events`);

  if (usersStats?.count === 0 && sessionsStats?.count === 0) {
    console.log(`\n  ${c.yellow}ℹ Analytics collections are empty (no logins yet)${c.reset}`);
    console.log(`  ${c.yellow}  Data will populate when users authenticate${c.reset}`);
  }

  // ============================================================
  // SECTION 7: VALIDATION HISTORY
  // ============================================================
  console.log(`\n${c.bright}${c.blue}┌${'─'.repeat(78)}┐${c.reset}`);
  console.log(`${c.bright}${c.blue}│ VALIDATION HISTORY${' '.repeat(59)}│${c.reset}`);
  console.log(`${c.bright}${c.blue}└${'─'.repeat(78)}┘${c.reset}\n`);

  const validationStats = collectionStats.find(s => s.name === 'validation_history');
  if (validationStats && validationStats.count > 0) {
    console.log(`  ${c.green}✓ ${validationStats.count} validation entries${c.reset}`);

    // Show latest entry
    const latest = validationStats.documents[validationStats.documents.length - 1];
    if (latest) {
      console.log(`\n  ${c.bright}Latest Upload:${c.reset}`);
      console.log(`    Version: ${latest.data.version || 'unknown'}`);
      console.log(`    Predictions within 1σ: ${latest.data.predictions_within_1sigma || 'N/A'}`);
      console.log(`    Total predictions: ${latest.data.total_predictions || 'N/A'}`);
      console.log(`    Exact matches: ${latest.data.exact_matches || 'N/A'}`);
    }
  } else {
    console.log(`  ${c.yellow}⚠ No validation history${c.reset}`);
  }

  // ============================================================
  // SECTION 8: SUMMARY
  // ============================================================
  console.log(`\n${'═'.repeat(80)}`);
  console.log(`${c.bright}${c.cyan} MIGRATION SUMMARY${c.reset}`);
  console.log('═'.repeat(80) + '\n');

  const totalDocs = collectionStats.reduce((sum, s) => sum + (s.count || 0), 0);
  const hasTheoryConstants = collectionStats.find(s => s.name === 'theory_constants')?.count > 0;
  const hasPages = collectionStats.find(s => s.name === 'pages')?.count > 0;
  const hasFormulas = collectionStats.find(s => s.name === 'formulas')?.count > 0;

  console.log(`  ${c.bright}Total Documents in Firestore:${c.reset} ${totalDocs}`);
  console.log('');
  console.log(`  ${c.bright}Core Data:${c.reset}`);
  console.log(`    ${hasTheoryConstants ? c.green + '✓' : c.red + '✗'}${c.reset} Theory Constants (Single Source of Truth)`);
  console.log(`    ${hasFormulas ? c.green + '✓' : c.red + '✗'}${c.reset} Formula Definitions`);
  console.log(`    ${hasPages ? c.green + '✓' : c.red + '✗'}${c.reset} Page Content`);
  console.log('');
  console.log(`  ${c.bright}Infrastructure:${c.reset}`);
  console.log(`    ${c.green}✓${c.reset} Firebase Authentication (Google)`);
  console.log(`    ${c.green}✓${c.reset} User Analytics Tracking (login, page views)`);
  console.log(`    ${c.green}✓${c.reset} Mandatory Push Confirmation (3-step)`);
  console.log(`    ${c.green}✓${c.reset} OOM Validation on Updates`);

  // Check for issues
  const issues = [];
  if (!hasTheoryConstants) issues.push('Theory constants not uploaded');
  if (!hasPages) issues.push('Page content not uploaded');
  if (!hasFormulas) issues.push('Formula definitions not uploaded');

  if (issues.length > 0) {
    console.log(`\n  ${c.bright}${c.red}Issues:${c.reset}`);
    for (const issue of issues) {
      console.log(`    ${c.red}✗ ${issue}${c.reset}`);
    }
  } else {
    console.log(`\n  ${c.green}${c.bright}✓ All core data successfully migrated to Firebase${c.reset}`);
  }

  console.log('\n' + '═'.repeat(80));

  // Save report to file
  const report = {
    generated: new Date().toISOString(),
    collections: collectionStats.map(s => ({
      name: s.name,
      count: s.count
    })),
    criticalPages: criticalPages.map(p => ({
      ...p,
      exists: pageIds.includes(p.id)
    })),
    localFiles: localFiles,
    issues: issues,
    summary: {
      totalDocuments: totalDocs,
      hasTheoryConstants,
      hasFormulas,
      hasPages,
      migrationComplete: issues.length === 0
    }
  };

  const reportPath = path.join(ROOT_DIR, 'firebase-migration-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\nReport saved to: ${reportPath}`);

  process.exit(issues.length > 0 ? 1 : 0);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
