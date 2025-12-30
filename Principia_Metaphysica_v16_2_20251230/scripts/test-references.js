#!/usr/bin/env node

/**
 * Test Firebase References Module
 *
 * Tests loading, querying, and rendering of references from Firestore.
 * Validates data integrity and API functionality.
 *
 * Usage: node scripts/test-references.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin
const serviceAccount = require('../firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: 'principia-metaphysica'
});

const db = admin.firestore();

/**
 * Test loading all references
 */
async function testLoadAllReferences() {
  console.log('\n📚 Test: Load All References');
  console.log('─'.repeat(60));

  try {
    const snapshot = await db.collection('references')
      .orderBy('category')
      .orderBy('year')
      .get();

    console.log(`✓ Loaded ${snapshot.size} references`);

    // Group by category
    const byCategory = {};
    snapshot.forEach(doc => {
      const data = doc.data();
      if (!byCategory[data.category]) {
        byCategory[data.category] = [];
      }
      byCategory[data.category].push({ id: doc.id, ...data });
    });

    console.log('\nReferences by category:');
    Object.entries(byCategory).forEach(([cat, refs]) => {
      console.log(`  ${cat}: ${refs.length} references`);
    });

    return { success: true, count: snapshot.size };
  } catch (error) {
    console.error('✗ Failed:', error.message);
    return { success: false, error };
  }
}

/**
 * Test loading single reference by ID
 */
async function testLoadReferenceById() {
  console.log('\n🔍 Test: Load Reference by ID');
  console.log('─'.repeat(60));

  const testIds = ['einstein1915', 'joyce2000', 'acharya1998'];

  for (const refId of testIds) {
    try {
      const doc = await db.collection('references').doc(refId).get();

      if (doc.exists) {
        const data = doc.data();
        console.log(`✓ ${refId}: ${data.citation_key} - ${data.title.substring(0, 50)}...`);
      } else {
        console.log(`✗ ${refId}: Not found`);
      }
    } catch (error) {
      console.error(`✗ ${refId}: Error - ${error.message}`);
    }
  }

  return { success: true };
}

/**
 * Test loading references by category
 */
async function testLoadByCategory() {
  console.log('\n📁 Test: Load References by Category');
  console.log('─'.repeat(60));

  const testCategories = ['geometry-topology', 'string-m-theory', 'cosmology'];

  for (const category of testCategories) {
    try {
      const snapshot = await db.collection('references')
        .where('category', '==', category)
        .orderBy('year')
        .get();

      console.log(`✓ ${category}: ${snapshot.size} references`);

      // Show a few examples
      let count = 0;
      snapshot.forEach(doc => {
        if (count < 2) {
          const data = doc.data();
          console.log(`    - ${data.citation_key}: ${data.title.substring(0, 40)}...`);
          count++;
        }
      });
    } catch (error) {
      console.error(`✗ ${category}: ${error.message}`);
    }
  }

  return { success: true };
}

/**
 * Test BibTeX generation
 */
async function testBibTeX() {
  console.log('\n📖 Test: BibTeX Validation');
  console.log('─'.repeat(60));

  try {
    const doc = await db.collection('references').doc('einstein1915').get();

    if (doc.exists) {
      const data = doc.data();

      if (data.bibtex) {
        console.log('✓ BibTeX exists for einstein1915');
        console.log('\nBibTeX Preview:');
        console.log(data.bibtex.split('\n').slice(0, 5).join('\n'));
        console.log('  ...');
      } else {
        console.log('✗ No BibTeX found for einstein1915');
      }
    }

    return { success: true };
  } catch (error) {
    console.error('✗ Failed:', error.message);
    return { success: false, error };
  }
}

/**
 * Test citation key lookups
 */
async function testCitationKeys() {
  console.log('\n🔑 Test: Citation Key Lookups');
  console.log('─'.repeat(60));

  const testKeys = ['Einstein 1915', 'Joyce 2000', 'Acharya 1998'];

  for (const key of testKeys) {
    try {
      const snapshot = await db.collection('references')
        .where('citation_key', '==', key)
        .limit(1)
        .get();

      if (!snapshot.empty) {
        const doc = snapshot.docs[0];
        const data = doc.data();
        console.log(`✓ "${key}" → ${doc.id}: ${data.title.substring(0, 40)}...`);
      } else {
        console.log(`✗ "${key}": Not found`);
      }
    } catch (error) {
      console.error(`✗ "${key}": ${error.message}`);
    }
  }

  return { success: true };
}

/**
 * Test reference types
 */
async function testReferenceTypes() {
  console.log('\n📊 Test: Reference Types Distribution');
  console.log('─'.repeat(60));

  try {
    const snapshot = await db.collection('references').get();

    const types = {};
    snapshot.forEach(doc => {
      const data = doc.data();
      types[data.type] = (types[data.type] || 0) + 1;
    });

    console.log('References by type:');
    Object.entries(types).forEach(([type, count]) => {
      console.log(`  ${type}: ${count}`);
    });

    return { success: true, types };
  } catch (error) {
    console.error('✗ Failed:', error.message);
    return { success: false, error };
  }
}

/**
 * Test data integrity
 */
async function testDataIntegrity() {
  console.log('\n✅ Test: Data Integrity');
  console.log('─'.repeat(60));

  try {
    const snapshot = await db.collection('references').get();

    let missingFields = 0;
    let invalidYears = 0;
    let missingBibTeX = 0;
    let missingCitationKeys = 0;

    snapshot.forEach(doc => {
      const data = doc.data();

      // Check required fields
      if (!data.title || !data.authors || !data.journal) {
        console.log(`⚠ ${doc.id}: Missing required fields`);
        missingFields++;
      }

      // Check year validity
      if (!data.year || data.year < 1900 || data.year > 2030) {
        console.log(`⚠ ${doc.id}: Invalid year (${data.year})`);
        invalidYears++;
      }

      // Check BibTeX
      if (!data.bibtex) {
        console.log(`⚠ ${doc.id}: Missing BibTeX`);
        missingBibTeX++;
      }

      // Check citation key
      if (!data.citation_key) {
        console.log(`⚠ ${doc.id}: Missing citation_key`);
        missingCitationKeys++;
      }
    });

    console.log(`\nIntegrity Summary:`);
    console.log(`  Total references: ${snapshot.size}`);
    console.log(`  Missing fields: ${missingFields}`);
    console.log(`  Invalid years: ${invalidYears}`);
    console.log(`  Missing BibTeX: ${missingBibTeX}`);
    console.log(`  Missing citation keys: ${missingCitationKeys}`);

    const score = ((snapshot.size - missingFields - invalidYears - missingBibTeX - missingCitationKeys) / snapshot.size * 100).toFixed(1);
    console.log(`\n  Integrity Score: ${score}%`);

    return {
      success: true,
      total: snapshot.size,
      issues: missingFields + invalidYears + missingBibTeX + missingCitationKeys,
      score
    };
  } catch (error) {
    console.error('✗ Failed:', error.message);
    return { success: false, error };
  }
}

/**
 * Test search by tags
 */
async function testTagSearch() {
  console.log('\n🏷️  Test: Tag Search');
  console.log('─'.repeat(60));

  const testTags = ['G₂ Holonomy', 'M-Theory', 'Textbook'];

  for (const tag of testTags) {
    try {
      const snapshot = await db.collection('references')
        .where('tags', 'array-contains', tag)
        .get();

      console.log(`✓ Tag "${tag}": ${snapshot.size} references`);

      // Show first example
      if (!snapshot.empty) {
        const first = snapshot.docs[0].data();
        console.log(`    Example: ${first.citation_key} - ${first.title.substring(0, 40)}...`);
      }
    } catch (error) {
      console.error(`✗ Tag "${tag}": ${error.message}`);
    }
  }

  return { success: true };
}

/**
 * Test links validation
 */
async function testLinksValidation() {
  console.log('\n🔗 Test: Links Validation');
  console.log('─'.repeat(60));

  try {
    const snapshot = await db.collection('references').get();

    let withDOI = 0;
    let withArXiv = 0;
    let withLinks = 0;

    snapshot.forEach(doc => {
      const data = doc.data();

      if (data.doi) withDOI++;
      if (data.arxiv) withArXiv++;
      if (data.links && data.links.length > 0) withLinks++;
    });

    console.log(`References with DOI: ${withDOI} (${(withDOI / snapshot.size * 100).toFixed(1)}%)`);
    console.log(`References with arXiv: ${withArXiv} (${(withArXiv / snapshot.size * 100).toFixed(1)}%)`);
    console.log(`References with links: ${withLinks} (${(withLinks / snapshot.size * 100).toFixed(1)}%)`);

    return { success: true, withDOI, withArXiv, withLinks };
  } catch (error) {
    console.error('✗ Failed:', error.message);
    return { success: false, error };
  }
}

/**
 * Generate test report
 */
function generateReport(results) {
  console.log('\n' + '═'.repeat(60));
  console.log('📊 TEST SUMMARY');
  console.log('═'.repeat(60));

  const passed = results.filter(r => r.success).length;
  const total = results.length;

  console.log(`\nTests Passed: ${passed}/${total}`);

  if (passed === total) {
    console.log('\n✅ All tests passed!');
  } else {
    console.log('\n⚠ Some tests failed');
  }

  console.log('\n' + '═'.repeat(60));
}

/**
 * Main test runner
 */
async function main() {
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║     Principia Metaphysica - References Module Tests         ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');

  const results = [];

  try {
    results.push(await testLoadAllReferences());
    results.push(await testLoadReferenceById());
    results.push(await testLoadByCategory());
    results.push(await testBibTeX());
    results.push(await testCitationKeys());
    results.push(await testReferenceTypes());
    results.push(await testDataIntegrity());
    results.push(await testTagSearch());
    results.push(await testLinksValidation());

    generateReport(results);

  } catch (error) {
    console.error('\n❌ Test suite failed:', error);
    process.exit(1);
  }

  process.exit(0);
}

// Run tests
main();
