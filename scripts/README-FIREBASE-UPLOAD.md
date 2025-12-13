# Firebase Website Content Upload

This script uploads all website HTML content to Firebase Firestore for use in the mobile app and other platforms.

## Setup

### 1. Install Dependencies

```bash
npm install
```

This will install:
- `firebase-admin` - Firebase Admin SDK for Node.js
- `cheerio` - HTML parsing library

### 2. Service Account Key

You need a Firebase service account key file. The script will automatically look for it in these locations:

1. `scripts/serviceAccountKey.json`
2. `scripts/principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json`
3. `principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json` (root directory)

**To download the service account key:**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select the `principia-metaphysica` project
3. Go to Project Settings (gear icon) > Service Accounts
4. Click "Generate New Private Key"
5. Save the downloaded JSON file to one of the locations above

## Usage

### Dry Run (Test Mode)

Test the script without actually uploading to Firebase:

```bash
node scripts/firebase-upload-website-content.js --dry-run
```

This will:
- Scan all HTML files
- Extract content from each file
- Show what would be uploaded
- Display detailed statistics
- **NOT** upload anything to Firebase

### Live Upload

Upload all content to Firebase:

```bash
node scripts/firebase-upload-website-content.js
```

This will:
- Scan all HTML files across the entire site
- Extract comprehensive content from each page
- Upload to Firestore `pages` collection
- Use efficient batch uploads (400 documents per batch)
- Show progress and final statistics

## What Gets Uploaded

The script processes ALL HTML files in these directories:

### Root Pages (9 files)
- `index.html`
- `principia-metaphysica-paper.html`
- `references.html`
- `beginners-guide.html`
- `philosophical-implications.html`
- `visualization-index.html`
- `ancient-numerology.html`
- `proverbs-31-wife-of-noble-character.html`
- `appendices_content.html`

### Sections (17 files)
- All files in `sections/*.html`
- Theory sections, formulas, analysis pages

### Foundations (14 files)
- All files in `foundations/*.html`
- Mathematical and physics foundations

### Documentation (3 files)
- All files in `docs/*.html`

### Diagrams (1 file)
- All files in `diagrams/*.html`

### Components (14 files)
- All files in `components/*.html`

## Data Structure

For each HTML page, the following is extracted and uploaded to Firestore:

```javascript
{
  id: "sections-fermion-sector",          // Document ID
  path: "sections/fermion-sector.html",   // Relative file path
  category: "sections",                    // Category (root, sections, foundations, etc.)
  title: "Section 4: Fermion Sector",     // From <title> tag
  description: "...",                      // From meta description
  mainContent: "<div>...</div>",          // Main HTML content
  sections: [                              // Array of sections
    {
      id: "section-id",
      heading: "Section Heading",
      html: "<div>...</div>"
    }
  ],
  formulas: [                              // Array of formulas
    {
      id: "formula-1",
      html: "<div>...</div>",
      dataRef: "ref-id",
      dataFormula: "formula-id"
    }
  ],
  pmValueRefs: [                           // PM value references
    {
      category: "geometry",
      param: "D_bulk"
    }
  ],
  headings: [                              // Document outline
    {
      level: 1,
      text: "Introduction",
      id: "intro"
    }
  ],
  links: [                                 // External links
    {
      href: "https://example.com",
      text: "Link text"
    }
  ],
  lastUpdated: "2025-12-13T...",          // ISO timestamp
  uploadedAt: Firebase Timestamp           // Server timestamp
}
```

## Firestore Collection

All pages are stored in the `pages` collection:

- **Collection:** `pages`
- **Document ID:** Unique page identifier (e.g., `sections-fermion-sector`)
- **Indexing:** Can be queried by `category`, `path`, or `id`

## Performance

- **Batch Uploads:** Uses Firestore batch writes (400 documents per batch)
- **Size Limits:**
  - Main content: 100KB max
  - Sections: 50KB max per section
  - Links: First 100 links only
- **Error Handling:** Gracefully handles missing files and parsing errors

## Example Output

```
======================================================================
 PRINCIPIA METAPHYSICA - WEBSITE CONTENT UPLOAD
======================================================================
Timestamp: 2025-12-13T10:30:00.000Z
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

## Querying Data

### Get All Pages

```javascript
const snapshot = await db.collection('pages').get();
```

### Get Pages by Category

```javascript
const snapshot = await db.collection('pages')
  .where('category', '==', 'sections')
  .get();
```

### Get Specific Page

```javascript
const doc = await db.collection('pages').doc('sections-fermion-sector').get();
```

## Troubleshooting

### "Service account key not found"

Make sure the Firebase service account key is in one of the expected locations. Download it from Firebase Console if needed.

### "Cannot find module 'firebase-admin'"

Run `npm install` in the project root directory.

### "Permission denied"

Make sure the service account has the necessary permissions in Firebase Console.

### Large Upload Times

The script processes 50+ HTML files and uploads them in batches. This can take 1-2 minutes depending on network speed.

## Notes

- The script is idempotent - running it multiple times will overwrite existing documents
- Use `--dry-run` flag to test changes before uploading
- All timestamps use ISO 8601 format for consistency
- HTML content is sanitized and size-limited to fit Firestore constraints
- The script handles missing files gracefully and continues processing
