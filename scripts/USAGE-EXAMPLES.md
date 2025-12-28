# Firebase Upload Script - Usage Examples

This document provides comprehensive examples of using the Firebase website content upload script.

## Quick Start

### 1. First Time Setup

```bash
# Install dependencies (only needed once)
npm install

# Test that HTML extraction works (no Firebase needed)
node scripts/test-html-extraction.js

# Dry run to see what would be uploaded (requires Firebase key)
node scripts/firebase-upload-website-content.js --dry-run

# Actual upload (requires Firebase key)
node scripts/firebase-upload-website-content.js
```

## Testing Without Firebase

The `test-html-extraction.js` script lets you verify HTML parsing works without needing Firebase credentials:

```bash
node scripts/test-html-extraction.js
```

**Example output:**
```
Testing HTML Content Extraction
======================================================================

Testing: index.html
----------------------------------------------------------------------
✓ Successfully parsed
  Title: Principia Metaphysica - Andrew Keith Watts
  Description length: 89 chars
  Main content length: 45623 chars
  Sections: 8
  First sections:
    - Introduction (1234 chars)
    - The Framework (2345 chars)
    - Key Predictions (1890 chars)
  Formulas: 12
  PM References: 15
  Sample PM refs:
    - geometry.D_bulk
    - geometry.D_observed
    - gauge.alpha_unified
  Headings: 24
  Heading structure:
    H1: Principia Metaphysica
    H2: Introduction
      H3: The Quest for Unification
      H3: A New Framework

Testing: sections/introduction.html
----------------------------------------------------------------------
✓ Successfully parsed
...
```

## Dry Run Mode

Dry run mode processes all files and shows exactly what would be uploaded, but doesn't actually upload anything:

```bash
node scripts/firebase-upload-website-content.js --dry-run
```

**Example output:**
```
======================================================================
 PRINCIPIA METAPHYSICA - WEBSITE CONTENT UPLOAD
======================================================================
Timestamp: 2025-12-13T10:30:00.000Z
Mode: DRY RUN (no upload)

DRY RUN MODE - No data will be uploaded to Firebase

======================================================================
 UPLOADING WEBSITE CONTENT TO FIREBASE
======================================================================

Found 58 HTML files to process

[DRY RUN] Would upload: index
  Path: index.html
  Title: Principia Metaphysica - Andrew Keith Watts
  Sections: 8
  Formulas: 12
  PM Refs: 15
  Headings: 24

[DRY RUN] Would upload: sections-introduction
  Path: sections/introduction.html
  Title: Section 1: Introduction - Principia Metaphysica
  Sections: 4
  Formulas: 8
  PM Refs: 10
  Headings: 15

... (58 files total)

======================================================================
 DRY RUN COMPLETE
======================================================================

Summary:
  Total files: 58
  Successfully processed: 58
  Skipped: 0
  Failed: 0

By Category:
  components: 14 pages
  diagrams: 1 pages
  docs: 3 pages
  foundations: 14 pages
  root: 9 pages
  sections: 17 pages

To perform actual upload, run without --dry-run flag:
  node scripts/firebase-upload-website-content.js
```

## Live Upload

Upload all content to Firebase:

```bash
node scripts/firebase-upload-website-content.js
```

**Example output:**
```
======================================================================
 PRINCIPIA METAPHYSICA - WEBSITE CONTENT UPLOAD
======================================================================
Timestamp: 2025-12-13T10:35:00.000Z
Mode: LIVE UPLOAD

Using service account: principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json

======================================================================
 UPLOADING WEBSITE CONTENT TO FIREBASE
======================================================================

Found 58 HTML files to process

  Progress: 10/58 pages processed
  Progress: 20/58 pages processed
  Progress: 30/58 pages processed
  ✓ Committed batch #1 (30 documents)
  Progress: 40/58 pages processed
  Progress: 50/58 pages processed
  Progress: 58/58 pages processed
  ✓ Committed final batch #2 (28 documents)

======================================================================
 UPLOAD COMPLETE
======================================================================

Summary:
  Total files: 58
  Successfully uploaded: 58
  Skipped: 0
  Failed: 0

By Category:
  components: 14 pages
  diagrams: 1 pages
  docs: 3 pages
  foundations: 14 pages
  root: 9 pages
  sections: 17 pages

✓ All content uploaded to Firestore collection: pages
  Each document ID corresponds to the page identifier
  Query by category field to get pages by section
```

## Querying the Data

After uploading, you can query the data from your app:

### Firebase Web SDK

```javascript
import { getFirestore, collection, getDocs, doc, getDoc, query, where } from 'firebase/firestore';

const db = getFirestore();

// Get all pages
const querySnapshot = await getDocs(collection(db, 'pages'));
querySnapshot.forEach((doc) => {
  console.log(doc.id, '=>', doc.data());
});

// Get specific page
const docRef = doc(db, 'pages', 'sections-fermion-sector');
const docSnap = await getDoc(docRef);
if (docSnap.exists()) {
  console.log('Page data:', docSnap.data());
}

// Get all section pages
const q = query(collection(db, 'pages'), where('category', '==', 'sections'));
const sectionPages = await getDocs(q);

// Get all pages with specific PM reference
const q2 = query(
  collection(db, 'pages'),
  where('pmValueRefs', 'array-contains', { category: 'geometry', param: 'D_bulk' })
);
```

### Firebase Admin SDK (Node.js)

```javascript
const admin = require('firebase-admin');
const db = admin.firestore();

// Get all pages
const snapshot = await db.collection('pages').get();
snapshot.forEach(doc => {
  console.log(doc.id, '=>', doc.data());
});

// Get specific page
const doc = await db.collection('pages').doc('sections-fermion-sector').get();
if (doc.exists) {
  console.log('Page data:', doc.data());
}

// Get all foundation pages
const foundations = await db.collection('pages')
  .where('category', '==', 'foundations')
  .get();

// Get pages by title search (requires index)
const results = await db.collection('pages')
  .where('title', '>=', 'Fermion')
  .where('title', '<=', 'Fermion\uf8ff')
  .get();
```

### React Native / Mobile App

```javascript
import firestore from '@react-native-firebase/firestore';

// Get all section pages
const pages = await firestore()
  .collection('pages')
  .where('category', '==', 'sections')
  .get();

const sectionData = pages.docs.map(doc => ({
  id: doc.id,
  ...doc.data()
}));

// Get specific page with real-time updates
const unsubscribe = firestore()
  .collection('pages')
  .doc('sections-introduction')
  .onSnapshot(documentSnapshot => {
    console.log('Page data:', documentSnapshot.data());
  });

// Later: unsubscribe()
```

## Sample Document Structure

Here's what a typical uploaded document looks like:

```javascript
{
  id: "sections-fermion-sector",
  path: "sections/fermion-sector.html",
  category: "sections",
  title: "Section 4: Fermion Sector - Principia Metaphysica",
  description: "Section 4: The Fermion Sector and Emergent Chirality - Clifford algebras, Kaluza-Klein zero modes, and the Pneuma mechanism",

  mainContent: "<div class='section-hero'>...</div>...",

  sections: [
    {
      id: "clifford-structure",
      heading: "4.1 Clifford Algebra Structure",
      html: "<h2>4.1 Clifford Algebra Structure</h2><p>...</p>"
    },
    {
      id: "kk-zero-modes",
      heading: "4.2 Kaluza-Klein Zero Modes",
      html: "<h2>4.2 Kaluza-Klein Zero Modes</h2><p>...</p>"
    }
  ],

  formulas: [
    {
      id: "dirac-equation",
      html: "<div class='equation-box'>...</div>",
      dataRef: "dirac-eq",
      dataFormula: null
    }
  ],

  pmValueRefs: [
    { category: "geometry", param: "D_bulk" },
    { category: "geometry", param: "D_observed" },
    { category: "fermion", param: "generations" }
  ],

  headings: [
    { level: 1, text: "Section 4: Fermion Sector", id: "main-heading" },
    { level: 2, text: "4.1 Clifford Algebra Structure", id: "clifford-structure" },
    { level: 3, text: "Real Representation", id: null },
    { level: 2, text: "4.2 Kaluza-Klein Zero Modes", id: "kk-zero-modes" }
  ],

  links: [
    { href: "../foundations/clifford-algebra.html", text: "Clifford Algebra" },
    { href: "../foundations.html#kaluza-klein", text: "Kaluza-Klein Theory" }
  ],

  lastUpdated: "2025-12-13T10:35:00.000Z",
  uploadedAt: Timestamp { seconds: 1702468500, nanoseconds: 0 }
}
```

## Troubleshooting

### Problem: "Cannot find module 'firebase-admin'"

**Solution:**
```bash
npm install
```

### Problem: "Service account key not found"

**Solution:**
1. Go to Firebase Console
2. Select project "principia-metaphysica"
3. Project Settings > Service Accounts
4. Generate New Private Key
5. Save to one of these locations:
   - `scripts/serviceAccountKey.json`
   - `scripts/principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json`
   - `principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json` (root)

### Problem: Slow upload times

**Explanation:** The script uploads 50+ HTML files in batches. This is normal and can take 1-2 minutes.

**What's happening:**
- Batch #1: 30 documents (first commit point)
- Batch #2: 28 documents (final commit)

### Problem: Some pages showing 0 sections

**Explanation:** Some pages (like components) might not have `<section>` tags. The script will still capture the main content.

### Problem: Want to re-upload specific pages only

**Solution:** Modify the script to filter specific pages:

```javascript
// In getHtmlPages() function, add a filter
const pages = getHtmlPages();
const filteredPages = pages.filter(p =>
  p.category === 'sections' // Only upload sections
  // OR
  p.id === 'sections-fermion-sector' // Only upload specific page
);
```

## Advanced Usage

### Custom Page Selection

Edit `getHtmlPages()` in the script to customize which pages are uploaded:

```javascript
// Only upload sections and foundations
const directories = [
  { dir: 'sections', category: 'sections', prefix: 'sections-' },
  { dir: 'foundations', category: 'foundations', prefix: 'foundations-' }
  // Remove docs, diagrams, components
];
```

### Scheduled Updates

Set up a cron job to automatically upload content:

```bash
# crontab -e
# Upload every night at 2 AM
0 2 * * * cd /path/to/PrincipiaMetaphysica && node scripts/firebase-upload-website-content.js >> logs/firebase-upload.log 2>&1
```

### CI/CD Integration

Add to GitHub Actions or other CI/CD:

```yaml
# .github/workflows/upload-content.yml
name: Upload Content to Firebase

on:
  push:
    branches: [main]
    paths:
      - '**.html'

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - name: Upload to Firebase
        env:
          FIREBASE_SERVICE_ACCOUNT: ${{ secrets.FIREBASE_SERVICE_ACCOUNT }}
        run: |
          echo "$FIREBASE_SERVICE_ACCOUNT" > serviceAccountKey.json
          node scripts/firebase-upload-website-content.js
```

## Performance Considerations

### Upload Speed
- **Batch size:** 400 documents per batch (Firestore limit is 500)
- **Typical time:** 1-2 minutes for ~60 files
- **Rate limiting:** Firestore handles this automatically

### Document Size
- **Main content:** Limited to 100KB
- **Sections:** Limited to 50KB each
- **Total document:** Should be under 1MB (Firestore limit)

### Optimization Tips
1. Use dry-run mode first to verify structure
2. Upload during off-peak hours if serving users
3. Monitor Firebase Console for costs
4. Consider compression for very large HTML files

## Support

For issues or questions:
- Check the README-FIREBASE-UPLOAD.md
- Review the test output from test-html-extraction.js
- Verify service account permissions in Firebase Console
- Check Firestore rules allow writes from service account
