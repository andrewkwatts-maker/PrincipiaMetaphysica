/**
 * Test Formula Parser - No Firebase Dependencies
 *
 * This script tests the parsing logic without uploading to Firebase.
 * Run this first to verify the parsing works correctly.
 *
 * Usage: node scripts/test-formula-parser.js
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

/**
 * Parse formula-definitions.js to extract PM_FORMULAS object
 */
function parseFormulaDefinitions() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-definitions.js');

  if (!fs.existsSync(filePath)) {
    throw new Error(`formula-definitions.js not found at ${filePath}`);
  }

  console.log(`📖 Reading ${filePath}...`);
  const content = fs.readFileSync(filePath, 'utf-8');

  // Extract PM_FORMULAS object
  const startPattern = 'const PM_FORMULAS = {';
  const startIndex = content.indexOf(startPattern);

  if (startIndex === -1) {
    throw new Error('Could not find PM_FORMULAS object');
  }

  // Find the matching closing brace
  let braceCount = 0;
  let inString = false;
  let stringChar = '';
  let escapeNext = false;
  let objectStart = startIndex + 'const PM_FORMULAS = '.length;
  let objectEnd = objectStart;

  for (let i = objectStart; i < content.length; i++) {
    const char = content[i];

    // Handle escape sequences
    if (escapeNext) {
      escapeNext = false;
      continue;
    }
    if (char === '\\') {
      escapeNext = true;
      continue;
    }

    // Handle strings
    if ((char === '"' || char === "'" || char === '`') && !inString) {
      inString = true;
      stringChar = char;
      continue;
    }
    if (char === stringChar && inString) {
      inString = false;
      continue;
    }

    // Count braces only outside strings
    if (!inString) {
      if (char === '{') braceCount++;
      if (char === '}') {
        braceCount--;
        if (braceCount === 0) {
          objectEnd = i + 1;
          break;
        }
      }
    }
  }

  let objectString = content.substring(objectStart, objectEnd);

  // Use eval to parse the JavaScript object
  let PM_FORMULAS;
  try {
    PM_FORMULAS = eval('(' + objectString + ')');
  } catch (e) {
    console.error('Failed to parse PM_FORMULAS object:', e.message);
    throw e;
  }

  console.log(`✓ Parsed PM_FORMULAS object`);
  return PM_FORMULAS;
}

/**
 * Parse formula-database.js to extract FORMULA_DATABASE object
 */
function parseFormulaDatabase() {
  const filePath = path.join(ROOT_DIR, 'js', 'formula-database.js');

  if (!fs.existsSync(filePath)) {
    console.log(`⚠ formula-database.js not found at ${filePath}, skipping`);
    return null;
  }

  console.log(`📖 Reading ${filePath}...`);
  const content = fs.readFileSync(filePath, 'utf-8');

  // Extract FORMULA_DATABASE object
  const startPattern = 'const FORMULA_DATABASE = {';
  const startIndex = content.indexOf(startPattern);

  if (startIndex === -1) {
    console.log('⚠ Could not find FORMULA_DATABASE object');
    return null;
  }

  // Find the matching closing brace
  let braceCount = 0;
  let inString = false;
  let stringChar = '';
  let escapeNext = false;
  let objectStart = startIndex + 'const FORMULA_DATABASE = '.length;
  let objectEnd = objectStart;

  for (let i = objectStart; i < content.length; i++) {
    const char = content[i];

    if (escapeNext) {
      escapeNext = false;
      continue;
    }
    if (char === '\\') {
      escapeNext = true;
      continue;
    }

    if ((char === '"' || char === "'" || char === '`') && !inString) {
      inString = true;
      stringChar = char;
      continue;
    }
    if (char === stringChar && inString) {
      inString = false;
      continue;
    }

    if (!inString) {
      if (char === '{') braceCount++;
      if (char === '}') {
        braceCount--;
        if (braceCount === 0) {
          objectEnd = i + 1;
          break;
        }
      }
    }
  }

  let objectString = content.substring(objectStart, objectEnd);

  let FORMULA_DATABASE;
  try {
    FORMULA_DATABASE = eval('(' + objectString + ')');
  } catch (e) {
    console.error('Failed to parse FORMULA_DATABASE object:', e.message);
    return null;
  }

  console.log(`✓ Parsed FORMULA_DATABASE object`);
  return FORMULA_DATABASE;
}

/**
 * Analyze formula structure
 */
function analyzeFormulas(PM_FORMULAS) {
  console.log('\n📊 Analyzing formula structure...\n');

  const categories = ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS'];
  let totalFormulas = 0;
  const stats = {};

  for (const category of categories) {
    const formulas = PM_FORMULAS[category] || {};
    const count = Object.keys(formulas).length;
    stats[category] = count;
    totalFormulas += count;

    console.log(`${category}: ${count} formulas`);

    // Show first formula as example
    const firstKey = Object.keys(formulas)[0];
    if (firstKey) {
      const first = formulas[firstKey];
      console.log(`  Example: ${first.id}`);
      console.log(`    Label: ${first.label}`);
      console.log(`    HTML: ${first.html.substring(0, 60)}...`);
      if (first.pm_constant) {
        console.log(`    PM Constant: ${first.pm_constant}`);
      }
      if (first.experimental_value !== undefined) {
        console.log(`    Experimental: ${first.experimental_value}`);
      }
      if (first.sigma !== undefined) {
        console.log(`    Sigma: ${first.sigma}`);
      }
      console.log('');
    }
  }

  console.log(`\nTotal: ${totalFormulas} formulas across all categories`);
  return { totalFormulas, stats };
}

/**
 * Analyze formula database
 */
function analyzeFormulaDatabase(FORMULA_DATABASE) {
  if (!FORMULA_DATABASE) {
    console.log('\n⚠ No formula database to analyze');
    return { totalEntries: 0 };
  }

  console.log('\n📊 Analyzing formula database (tooltips)...\n');

  const entries = Object.keys(FORMULA_DATABASE);
  console.log(`Total entries: ${entries.length}`);

  // Show a few examples
  console.log('\nExamples:');
  for (let i = 0; i < Math.min(3, entries.length); i++) {
    const key = entries[i];
    const entry = FORMULA_DATABASE[key];
    console.log(`  ${entry.id}:`);
    console.log(`    Symbol: ${entry.htmlSymbol}`);
    console.log(`    Description: ${entry.description}`);
    if (entry.value) {
      console.log(`    Value: ${entry.value}`);
    }
    if (entry.pmRef) {
      console.log(`    PM Ref: ${entry.pmRef}`);
    }
    console.log('');
  }

  return { totalEntries: entries.length };
}

/**
 * Main function
 */
function main() {
  console.log('═'.repeat(70));
  console.log(' FORMULA PARSER TEST');
  console.log('═'.repeat(70));
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log('═'.repeat(70));

  try {
    // Parse formula-definitions.js
    const PM_FORMULAS = parseFormulaDefinitions();

    // Parse formula-database.js
    const FORMULA_DATABASE = parseFormulaDatabase();

    // Analyze
    const formulaStats = analyzeFormulas(PM_FORMULAS);
    const databaseStats = analyzeFormulaDatabase(FORMULA_DATABASE);

    console.log('\n' + '═'.repeat(70));
    console.log(' ✅ PARSING SUCCESSFUL');
    console.log('═'.repeat(70));
    console.log(`\nFormulas: ${formulaStats.totalFormulas}`);
    console.log(`Tooltips: ${databaseStats.totalEntries}`);
    console.log('\nReady to upload to Firebase!');
    console.log('Run: npm install && node scripts/upload-formula-database.js');

  } catch (error) {
    console.error('\n❌ PARSING FAILED:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
