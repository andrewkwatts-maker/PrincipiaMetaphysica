/**
 * Test HTML Content Extraction
 *
 * Tests the HTML parsing and extraction logic without uploading to Firebase.
 * Useful for verifying the script works before running the full upload.
 *
 * Usage: node scripts/test-html-extraction.js
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const ROOT_DIR = path.join(__dirname, '..');

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
          htmlLength: html.length
        });
      }
    });

    // Extract formulas
    const formulas = [];
    $('.formula-box, .equation, .equation-box, .interactive-formula, [class*="formula"]').each((i, el) => {
      const $el = $(el);
      const formulaData = {
        id: $el.attr('id') || `formula-${i}`,
        dataRef: $el.attr('data-ref') || null,
        dataFormula: $el.attr('data-formula') || null
      };

      formulas.push(formulaData);
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

    return {
      title,
      description,
      mainContentLength: mainContent ? mainContent.length : 0,
      sectionsCount: sections.length,
      sections: sections.slice(0, 3), // Show first 3 sections
      formulasCount: formulas.length,
      pmRefsCount: pmValueRefs.length,
      pmRefs: pmValueRefs.slice(0, 5), // Show first 5 refs
      headingsCount: headings.length,
      headings: headings.slice(0, 5) // Show first 5 headings
    };

  } catch (error) {
    console.error(`  ! Error parsing ${relativePath}:`, error.message);
    return null;
  }
}

/**
 * Test a few sample files
 */
function testExtraction() {
  console.log('Testing HTML Content Extraction');
  console.log('='.repeat(70));

  const testFiles = [
    { path: 'index.html', category: 'root' },
    { path: 'sections/introduction.html', category: 'sections' },
    { path: 'sections/fermion-sector.html', category: 'sections' },
    { path: 'foundations/dirac-equation.html', category: 'foundations' }
  ];

  for (const file of testFiles) {
    console.log(`\nTesting: ${file.path}`);
    console.log('-'.repeat(70));

    const fullPath = path.join(ROOT_DIR, file.path);
    const result = extractPageContent(fullPath, file.path);

    if (result) {
      console.log(`✓ Successfully parsed`);
      console.log(`  Title: ${result.title}`);
      console.log(`  Description length: ${result.description.length} chars`);
      console.log(`  Main content length: ${result.mainContentLength} chars`);
      console.log(`  Sections: ${result.sectionsCount}`);

      if (result.sections.length > 0) {
        console.log('  First sections:');
        result.sections.forEach(s => {
          console.log(`    - ${s.heading} (${s.htmlLength} chars)`);
        });
      }

      console.log(`  Formulas: ${result.formulasCount}`);
      console.log(`  PM References: ${result.pmRefsCount}`);

      if (result.pmRefs.length > 0) {
        console.log('  Sample PM refs:');
        result.pmRefs.forEach(ref => {
          console.log(`    - ${ref.category}.${ref.param}`);
        });
      }

      console.log(`  Headings: ${result.headingsCount}`);

      if (result.headings.length > 0) {
        console.log('  Heading structure:');
        result.headings.forEach(h => {
          const indent = '  '.repeat(h.level - 1);
          console.log(`    ${indent}H${h.level}: ${h.text.substring(0, 50)}${h.text.length > 50 ? '...' : ''}`);
        });
      }
    } else {
      console.log('✗ Failed to parse');
    }
  }

  console.log('\n' + '='.repeat(70));
  console.log('Test complete! If extraction works, you can run the full upload.');
  console.log('Next step: node scripts/firebase-upload-website-content.js --dry-run');
}

// Run test
testExtraction();
