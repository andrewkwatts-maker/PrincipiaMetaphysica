# Extract Page Content Script

## Overview

The `extract-page-content.js` script extracts structured content from HTML pages and uploads it to Firebase Firestore. It processes all HTML files in the `sections/`, `foundations/`, and `docs/` directories.

## Features

- Extracts main content from `<main>` or `<article>` tags
- Parses all sections with headings and content
- Extracts formulas with metadata (id, HTML, LaTeX references)
- Extracts PM value references (data-category, data-param, data-format)
- Creates structured JSON documents for Firestore
- Provides detailed upload progress and statistics

## Document Structure

Each page is uploaded to Firestore with the following structure:

```javascript
{
  id: 'sections-fermion-sector',           // Document ID
  path: 'sections/fermion-sector.html',    // File path
  title: 'Section 4: Fermion Sector',      // Page title
  category: 'sections',                     // Category (sections/foundations/docs)
  description: '...',                       // Meta description
  mainContent: '<html>...</html>',          // Full main content HTML
  sections: [
    {
      id: 'section-1',
      heading: 'The Fermion Sector...',
      content: '<html>...</html>'
    }
  ],
  formulas: [
    {
      id: 'formula-1',
      html: '...',
      latexRef: 'dirac-equation',
      label: 'Eq. 1'
    }
  ],
  pmValueRefs: [
    {
      category: 'pmns_matrix',
      param: 'theta_23',
      format: 'fixed:2'
    }
  ],
  metadata: {
    extractedAt: '2025-12-13T...',
    version: '12.7',
    sectionCount: 15,
    formulaCount: 42,
    pmValueRefCount: 128
  },
  uploadedAt: Firestore.Timestamp
}
```

## Files Processed

### Sections (17 files)
- pneuma-lagrangian-new.html
- cmb-bubble-collisions-comprehensive.html
- xy-gauge-bosons.html
- formulas.html
- introduction.html
- geometric-framework.html
- gauge-unification.html
- fermion-sector.html
- cosmology.html
- thermal-time.html
- predictions.html
- conclusion.html
- einstein-hilbert-term.html
- theory-analysis.html
- pneuma-lagrangian.html
- division-algebra-section.html

### Foundations (13 files)
- calabi-yau.html
- boltzmann-entropy.html
- einstein-field-equations.html
- tomita-takesaki.html
- dirac-equation.html
- clifford-algebra.html
- ricci-tensor.html
- kms-condition.html
- kaluza-klein.html
- yang-mills.html
- g2-manifolds.html
- so10-gut.html
- einstein-hilbert-action.html

### Docs (2 files)
- computational-appendices.html
- beginners-guide-printable.html

**Total: 32 HTML files**

## Prerequisites

1. Node.js installed
2. Firebase project set up
3. Service account key file at `scripts/serviceAccountKey.json`
4. Dependencies installed:
   - firebase-admin
   - cheerio

## Installation

```bash
# Install dependencies (if not already installed)
npm install
```

## Usage

### Run the script

```bash
node scripts/extract-page-content.js
```

### Expected Output

```
======================================================================
 EXTRACTING AND UPLOADING PAGE CONTENT TO FIREBASE
======================================================================

Found 32 pages to process

Processing: sections/fermion-sector.html
  ✓ Uploaded: sections-fermion-sector
    - Sections: 15
    - Formulas: 42
    - PM Value Refs: 128

Processing: sections/gauge-unification.html
  ✓ Uploaded: sections-gauge-unification
    - Sections: 12
    - Formulas: 38
    - PM Value Refs: 95

...

======================================================================
 UPLOAD SUMMARY
======================================================================
Total pages: 32
Successfully uploaded: 32
Failed: 0
======================================================================

Detailed Results:
✓ sections-fermion-sector: 15 sections, 42 formulas, 128 PM refs
✓ sections-gauge-unification: 12 sections, 38 formulas, 95 PM refs
...

✅ Page content extraction and upload complete!
```

## Error Handling

The script handles various error cases:

- Missing files are skipped with warnings
- Failed extractions are logged
- Upload failures are reported in the summary
- Process exits with code 1 if all uploads fail

## Firestore Collection

All pages are uploaded to the `pages` collection with document IDs in the format:
- `sections-{filename}` for section pages
- `foundations-{filename}` for foundation pages
- `docs-{filename}` for docs pages

## Integration with Existing Scripts

This script is designed to work alongside:
- `firebase-upload-all.js` - Comprehensive upload of all data
- `firebase-download.js` - Download data from Firestore
- `firebase-check-status.js` - Check Firestore status

You can also use it programmatically:

```javascript
const { extractPageContent, getHtmlPages } = require('./extract-page-content.js');

// Get list of pages
const pages = getHtmlPages();

// Extract content from a specific file
const content = extractPageContent('/path/to/file.html');
```

## Troubleshooting

### serviceAccountKey.json not found
Download the service account key from Firebase Console:
1. Go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Save as `scripts/serviceAccountKey.json`

### Permission denied errors
Ensure the Firebase service account has Firestore write permissions.

### Cheerio parsing errors
Check that HTML files are well-formed and valid.

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
