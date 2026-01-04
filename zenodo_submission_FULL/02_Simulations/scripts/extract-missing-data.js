/**
 * Extract Missing Data for Firebase
 *
 * Scans all HTML pages and extracts:
 * 1. All unique formulas that should be in Firebase
 * 2. All unique constants with their values
 * 3. All tooltip/hover content data
 *
 * Outputs a JSON file with data to upload
 *
 * Run: node scripts/extract-missing-data.js
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const ROOT_DIR = path.join(__dirname, '..');

// Directories to scan
const SCAN_DIRS = ['', 'sections', 'foundations', 'docs', 'diagrams'];

// Storage for extracted data
const extracted = {
  formulas: new Map(),
  constants: new Map(),
  tooltips: new Map(),
  pmValueRefs: new Map()
};

/**
 * Get all HTML files
 */
function getAllHtmlFiles() {
  const files = [];
  for (const dir of SCAN_DIRS) {
    const fullPath = path.join(ROOT_DIR, dir);
    if (!fs.existsSync(fullPath)) continue;

    const dirFiles = fs.readdirSync(fullPath)
      .filter(f => f.endsWith('.html') && !f.includes('node_modules'))
      .map(f => path.join(dir, f));

    files.push(...dirFiles);
  }
  return files;
}

/**
 * Extract formulas from a page
 */
function extractFormulas($, filePath) {
  const formulas = [];

  // Find formula boxes
  $('.formula-box, .formula, .equation, .interactive-formula').each((i, el) => {
    const $el = $(el);
    const id = $el.attr('data-formula-id') || $el.attr('id');
    const html = $el.html();
    const text = $el.text().replace(/\s+/g, ' ').trim();

    if (text.length > 5) {
      formulas.push({
        id: id || `formula-${filePath.replace(/[\/\\\.]/g, '-')}-${i}`,
        html: html,
        text: text,
        source: filePath,
        hasFirebaseRef: !!$el.attr('data-formula-id')
      });
    }
  });

  // Find inline equations
  $('span.equation, span.math, .inline-formula').each((i, el) => {
    const $el = $(el);
    const html = $el.html();
    const text = $el.text().trim();

    if (text.length > 3) {
      formulas.push({
        id: `inline-${filePath.replace(/[\/\\\.]/g, '-')}-${i}`,
        html: html,
        text: text,
        source: filePath,
        isInline: true,
        hasFirebaseRef: false
      });
    }
  });

  return formulas;
}

/**
 * Extract PM value references
 */
function extractPMValueRefs($, filePath) {
  const refs = [];

  $('.pm-value').each((i, el) => {
    const $el = $(el);
    const category = $el.attr('data-category');
    const param = $el.attr('data-param');
    const pmValue = $el.attr('data-pm-value');
    const format = $el.attr('data-format');
    const currentValue = $el.text().trim();

    refs.push({
      category,
      param,
      pmValue,
      format,
      currentValue,
      source: filePath,
      hasProperRef: !!(category && param) || !!pmValue
    });
  });

  return refs;
}

/**
 * Extract tooltip content
 */
function extractTooltips($, filePath) {
  const tooltips = [];

  $('.var-tooltip, .formula-tooltip, .tooltip-content').each((i, el) => {
    const $el = $(el);
    const parent = $el.parent();

    const tooltip = {
      name: $el.find('.var-name, .tooltip-title').text().trim(),
      description: $el.find('.var-description, .tooltip-desc').text().trim(),
      units: $el.find('.var-units, .tooltip-units').text().trim(),
      value: $el.find('.var-value, .tooltip-value').text().trim(),
      contribution: $el.find('.var-contribution').text().trim(),
      source: filePath,
      parentText: parent.text().substring(0, 50)
    };

    if (tooltip.name || tooltip.description) {
      tooltips.push(tooltip);
    }
  });

  return tooltips;
}

/**
 * Extract hardcoded physics values from text content
 */
function extractHardcodedValues(content, filePath) {
  const values = [];

  // Patterns for physics constants
  const patterns = [
    { regex: /(\d+\.?\d*)\s*GeV/g, type: 'mass', unit: 'GeV' },
    { regex: /(\d+\.?\d*)\s*TeV/g, type: 'mass', unit: 'TeV' },
    { regex: /(\d+\.?\d*)°/g, type: 'angle', unit: 'degrees' },
    { regex: /(\d+\.?\d*)\s*×\s*10\^?(\d+)/g, type: 'scientific', unit: '' },
    { regex: /(\d+\.?\d*)σ/g, type: 'sigma', unit: 'σ' },
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.regex.exec(content)) !== null) {
      values.push({
        value: match[0],
        numericValue: parseFloat(match[1]),
        type: pattern.type,
        unit: pattern.unit,
        source: filePath,
        context: content.substring(Math.max(0, match.index - 50), match.index + match[0].length + 50)
      });
    }
  }

  return values;
}

/**
 * Scan a single file
 */
function scanFile(filePath) {
  const fullPath = path.join(ROOT_DIR, filePath);
  if (!fs.existsSync(fullPath)) return;

  const content = fs.readFileSync(fullPath, 'utf-8');
  const $ = cheerio.load(content);

  // Extract formulas
  const formulas = extractFormulas($, filePath);
  for (const f of formulas) {
    const key = f.text.substring(0, 100);
    if (!extracted.formulas.has(key)) {
      extracted.formulas.set(key, f);
    }
  }

  // Extract PM value refs
  const refs = extractPMValueRefs($, filePath);
  for (const r of refs) {
    const key = `${r.category}.${r.param}` || r.pmValue;
    if (key && !extracted.pmValueRefs.has(key)) {
      extracted.pmValueRefs.set(key, r);
    }
  }

  // Extract tooltips
  const tooltips = extractTooltips($, filePath);
  for (const t of tooltips) {
    if (t.name && !extracted.tooltips.has(t.name)) {
      extracted.tooltips.set(t.name, t);
    }
  }

  return {
    formulas: formulas.length,
    refs: refs.length,
    tooltips: tooltips.length
  };
}

/**
 * Main execution
 */
async function main() {
  console.log('Extracting Missing Data for Firebase');
  console.log('─'.repeat(70));

  const files = getAllHtmlFiles();
  console.log(`Found ${files.length} HTML files to scan\n`);

  let totalFormulas = 0;
  let totalRefs = 0;
  let totalTooltips = 0;

  for (const file of files) {
    if (file.includes('node_modules')) continue;

    const result = scanFile(file);
    if (result) {
      totalFormulas += result.formulas;
      totalRefs += result.refs;
      totalTooltips += result.tooltips;
    }
  }

  console.log('\nExtraction Summary:');
  console.log('─'.repeat(70));
  console.log(`Unique formulas found:     ${extracted.formulas.size}`);
  console.log(`PM value references:       ${extracted.pmValueRefs.size}`);
  console.log(`Tooltip definitions:       ${extracted.tooltips.size}`);

  // Convert to arrays for output
  const output = {
    timestamp: new Date().toISOString(),
    formulas: Array.from(extracted.formulas.values()),
    pmValueRefs: Array.from(extracted.pmValueRefs.values()),
    tooltips: Array.from(extracted.tooltips.values()),
    summary: {
      totalFormulas: extracted.formulas.size,
      totalRefs: extracted.pmValueRefs.size,
      totalTooltips: extracted.tooltips.size
    }
  };

  // Save output
  const outputPath = path.join(ROOT_DIR, 'extracted-data.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`\nData saved to: ${outputPath}`);

  // Also create a report of formulas without Firebase refs
  const formulasNeedingUpload = output.formulas.filter(f => !f.hasFirebaseRef);
  console.log(`\nFormulas needing Firebase upload: ${formulasNeedingUpload.length}`);

  // Create upload-ready format
  const uploadData = {
    formulas: formulasNeedingUpload.map((f, i) => ({
      id: f.id || `extracted-formula-${i}`,
      html: f.html,
      text: f.text,
      category: 'EXTRACTED',
      source: f.source,
      needsReview: true
    })),
    tooltips: output.tooltips.map((t, i) => ({
      id: t.name.toLowerCase().replace(/\s+/g, '_') || `tooltip-${i}`,
      name: t.name,
      description: t.description,
      units: t.units,
      value: t.value,
      source: t.source
    }))
  };

  const uploadPath = path.join(ROOT_DIR, 'data-to-upload.json');
  fs.writeFileSync(uploadPath, JSON.stringify(uploadData, null, 2));
  console.log(`Upload-ready data saved to: ${uploadPath}`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
