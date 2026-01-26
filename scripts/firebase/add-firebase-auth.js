/**
 * Add Firebase Authentication to All HTML Pages
 *
 * This script adds Firebase authentication to all HTML pages in the
 * Principia Metaphysica project.
 *
 * Usage: node scripts/add-firebase-auth.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');

// Root directory
const ROOT_DIR = path.join(__dirname, '..');

// HTML files to process with their page IDs
const HTML_FILES = {
  // Root pages
  'index.html': 'index',
  'principia-metaphysica-paper.html': 'paper',
  'references.html': 'references',
  'beginners-guide.html': 'beginners-guide',
  'philosophical-implications.html': 'philosophical-implications',
  'visualization-index.html': 'visualization-index',

  // Sections
  'sections/introduction.html': 'introduction',
  'sections.html#2': 'geometric-framework', // Migrated to unified sections
  'sections/gauge-unification.html': 'gauge-unification',
  'sections/fermion-sector.html': 'fermion-sector',
  'sections/cosmology.html': 'cosmology',
  'sections/thermal-time.html': 'thermal-time',
  'sections.html#predictions': 'predictions',
  'sections/conclusion.html': 'conclusion',
  'sections/formulas.html': 'formulas',
  'sections/theory-analysis.html': 'theory-analysis',
  'sections.html#geometric-framework': 'einstein-hilbert-term',
  'sections.html#pneuma-lagrangian': 'pneuma-lagrangian',
  'sections/pneuma-lagrangian-new.html': 'pneuma-lagrangian-new',
  'sections/xy-gauge-bosons.html': 'xy-gauge-bosons',
  'sections/cmb-bubble-collisions-comprehensive.html': 'cmb-bubble-collisions',
  'sections/division-algebras.html': 'division-algebras',
  'sections/index.html': 'sections-index',

  // Foundations
  'foundations/index.html': 'foundations-index',
  'foundations/boltzmann-entropy.html': 'foundations-boltzmann-entropy',
  'foundations/clifford-algebra.html': 'foundations-clifford-algebra',
  'foundations/dirac-equation.html': 'foundations-dirac-equation',
  'foundations/einstein-field-equations.html': 'foundations-einstein-field-equations',
  'foundations/einstein-hilbert-action.html': 'foundations-einstein-hilbert-action',
  'foundations/kms-condition.html': 'foundations-kms-condition',
  'foundations/ricci-tensor.html': 'foundations-ricci-tensor',
  'foundations/so10-gut.html': 'foundations-so10-gut',
  'foundations/tomita-takesaki.html': 'foundations-tomita-takesaki',
  'foundations/yang-mills.html': 'foundations-yang-mills',

  // Docs
  'docs/computational-appendices.html': 'docs-computational-appendices',
  'docs/beginners-guide-printable.html': 'docs-beginners-guide-printable',

  // Diagrams
  'diagrams/theory-diagrams.html': 'diagrams-theory-diagrams'
};

// CSS to add
const AUTH_CSS_LINK = '<link rel="stylesheet" href="/css/auth.css">';

// User controls HTML
const USER_CONTROLS = `
    <div class="user-controls">
      <img id="user-avatar" src="/images/default-avatar.svg" alt="User">
      <span id="user-email"></span>
      <button id="logout-btn">Logout</button>
    </div>`;

// Firebase script template
function getFirebaseScript(pageId) {
  return `
  <script type="module">
    import { setupAuthGuard } from '/js/auth-guard.js';
    setupAuthGuard('${pageId}');
  </script>`;
}

/**
 * Process a single HTML file to add Firebase authentication
 */
function processHtmlFile(filePath, pageId) {
  const fullPath = path.join(ROOT_DIR, filePath);

  // Check if file exists
  if (!fs.existsSync(fullPath)) {
    console.log(`⚠ Skipping ${filePath} - file not found`);
    return false;
  }

  let content = fs.readFileSync(fullPath, 'utf-8');
  let modified = false;

  // 1. Add auth CSS if not present
  if (!content.includes('/css/auth.css')) {
    // Find the last CSS link or the closing </head> tag
    const headCloseIndex = content.indexOf('</head>');
    if (headCloseIndex !== -1) {
      // Look for last stylesheet link before </head>
      const beforeHead = content.substring(0, headCloseIndex);
      const lastCssMatch = beforeHead.lastIndexOf('<link rel="stylesheet"');

      if (lastCssMatch !== -1) {
        // Find the end of that link tag
        const linkEndIndex = content.indexOf('>', lastCssMatch) + 1;
        content = content.substring(0, linkEndIndex) + '\n    ' + AUTH_CSS_LINK + content.substring(linkEndIndex);
      } else {
        // Insert before </head>
        content = content.substring(0, headCloseIndex) + '    ' + AUTH_CSS_LINK + '\n  ' + content.substring(headCloseIndex);
      }
      modified = true;
    }
  }

  // 2. Add class="not-authenticated" to body tag
  if (!content.includes('class="not-authenticated"')) {
    // Match <body> with or without existing attributes
    content = content.replace(/<body([^>]*)>/, (match, attrs) => {
      if (attrs.includes('class=')) {
        // Add to existing class
        return match.replace(/class="([^"]*)"/, 'class="not-authenticated $1"');
      } else {
        return `<body class="not-authenticated"${attrs}>`;
      }
    });
    modified = true;
  }

  // 3. Wrap body content in main-content div if not present
  if (!content.includes('id="main-content"')) {
    // Find <body> tag and </body> tag
    const bodyMatch = content.match(/<body[^>]*>/);
    const bodyEndIndex = content.lastIndexOf('</body>');

    if (bodyMatch && bodyEndIndex !== -1) {
      const bodyStartIndex = content.indexOf(bodyMatch[0]) + bodyMatch[0].length;

      // Find where scripts start (to exclude them from main-content)
      let scriptsStartIndex = bodyEndIndex;
      const scriptMatches = content.substring(bodyStartIndex, bodyEndIndex).match(/<script[\s\S]*?<\/script>/g);

      // Get content between body and closing body (excluding final scripts)
      let bodyContent = content.substring(bodyStartIndex, bodyEndIndex);

      // Find the last non-script content
      const lastNonScriptIndex = bodyContent.lastIndexOf('</footer>');
      const lastMainIndex = bodyContent.lastIndexOf('</main>');
      const insertPoint = Math.max(lastNonScriptIndex, lastMainIndex);

      if (insertPoint !== -1) {
        const endOfContentIndex = bodyStartIndex + insertPoint + (lastNonScriptIndex > lastMainIndex ? '</footer>'.length : '</main>'.length);

        // Wrap the content
        const beforeContent = content.substring(0, bodyStartIndex);
        const mainContent = content.substring(bodyStartIndex, endOfContentIndex);
        const afterContent = content.substring(endOfContentIndex);

        content = beforeContent + '\n  <div id="main-content" style="display: none;">' + mainContent + '\n  </div>' + afterContent;
        modified = true;
      }
    }
  }

  // 4. Add user controls to header if not present
  if (!content.includes('class="user-controls"')) {
    // Find closing </header> tag
    const headerCloseIndex = content.indexOf('</header>');
    if (headerCloseIndex !== -1) {
      content = content.substring(0, headerCloseIndex) + USER_CONTROLS + '\n  ' + content.substring(headerCloseIndex);
      modified = true;
    }
  }

  // 5. Add Firebase script if not present
  if (!content.includes('setupAuthGuard')) {
    // Find closing </body> tag
    const bodyCloseIndex = content.lastIndexOf('</body>');
    if (bodyCloseIndex !== -1) {
      content = content.substring(0, bodyCloseIndex) + getFirebaseScript(pageId) + '\n' + content.substring(bodyCloseIndex);
      modified = true;
    }
  }

  // Write back if modified
  if (modified) {
    fs.writeFileSync(fullPath, content, 'utf-8');
    console.log(`✓ Updated ${filePath}`);
    return true;
  } else {
    console.log(`- Skipped ${filePath} (already has auth)`);
    return false;
  }
}

/**
 * Find additional HTML files not in the predefined list
 */
function findAdditionalHtmlFiles(dir, baseDir = ROOT_DIR) {
  const files = [];
  const fullDir = path.join(baseDir, dir);

  if (!fs.existsSync(fullDir)) {
    return files;
  }

  const entries = fs.readdirSync(fullDir, { withFileTypes: true });

  for (const entry of entries) {
    const relativePath = path.join(dir, entry.name);

    if (entry.isDirectory() && !['node_modules', '.git', 'scripts', 'images', 'css', 'js'].includes(entry.name)) {
      files.push(...findAdditionalHtmlFiles(relativePath, baseDir));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      if (!HTML_FILES[relativePath.replace(/\\/g, '/')]) {
        files.push(relativePath.replace(/\\/g, '/'));
      }
    }
  }

  return files;
}

/**
 * Main function
 */
function main() {
  console.log('═══════════════════════════════════════════════════════════════');
  console.log(' Principia Metaphysica - Add Firebase Authentication');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  let updated = 0;
  let skipped = 0;
  let errors = 0;

  // Process predefined files
  console.log('Processing predefined HTML files...\n');

  for (const [filePath, pageId] of Object.entries(HTML_FILES)) {
    try {
      if (processHtmlFile(filePath, pageId)) {
        updated++;
      } else {
        skipped++;
      }
    } catch (error) {
      console.error(`✗ Error processing ${filePath}:`, error.message);
      errors++;
    }
  }

  // Find and process additional HTML files
  console.log('\nSearching for additional HTML files...\n');

  const additionalFiles = findAdditionalHtmlFiles('');

  for (const filePath of additionalFiles) {
    // Generate page ID from file path
    const pageId = filePath
      .replace(/\.html$/, '')
      .replace(/\//g, '-')
      .replace(/^-/, '');

    try {
      if (processHtmlFile(filePath, pageId)) {
        updated++;
      } else {
        skipped++;
      }
    } catch (error) {
      console.error(`✗ Error processing ${filePath}:`, error.message);
      errors++;
    }
  }

  console.log('\n═══════════════════════════════════════════════════════════════');
  console.log(` Results: ${updated} updated, ${skipped} skipped, ${errors} errors`);
  console.log('═══════════════════════════════════════════════════════════════');
}

// Run
main();
