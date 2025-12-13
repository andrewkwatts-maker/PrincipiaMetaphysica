# Firebase Upload - Quick Reference Card

## Commands

```bash
# 1. Test HTML extraction (no Firebase needed)
node scripts/test-html-extraction.js

# 2. Dry run (requires Firebase key, shows what would be uploaded)
node scripts/firebase-upload-website-content.js --dry-run

# 3. Live upload (requires Firebase key, uploads to Firestore)
node scripts/firebase-upload-website-content.js
```

## What Gets Uploaded

| Category | Files | Example IDs |
|----------|-------|-------------|
| Root | 9 | `index`, `beginners-guide`, `philosophical-implications` |
| Sections | 17 | `sections-introduction`, `sections-fermion-sector` |
| Foundations | 14 | `foundations-dirac-equation`, `foundations-clifford-algebra` |
| Docs | 3 | `docs-beginners-guide-printable` |
| Diagrams | 1 | `diagrams-theory-diagrams` |
| Components | 14 | `components-button`, `components-expandable` |

**Total: ~58 HTML files**

## Document Structure

```javascript
{
  id: "sections-fermion-sector",           // Document ID
  path: "sections/fermion-sector.html",    // File path
  category: "sections",                     // Category
  title: "Section 4: Fermion Sector...",   // Page title
  description: "...",                       // Meta description
  mainContent: "<html>...</html>",         // Main HTML (100KB max)
  sections: [{id, heading, html}, ...],    // Page sections
  formulas: [{id, html, dataRef}, ...],    // Formula elements
  pmValueRefs: [{category, param}, ...],   // PM references
  headings: [{level, text, id}, ...],      // Outline
  links: [{href, text}, ...],              // Links (max 100)
  lastUpdated: "2025-12-13T...",           // ISO timestamp
  uploadedAt: Firebase Timestamp           // Server timestamp
}
```

## Querying

### Get All Pages
```javascript
const snapshot = await db.collection('pages').get();
```

### Get Specific Page
```javascript
const doc = await db.collection('pages').doc('sections-fermion-sector').get();
```

### Get by Category
```javascript
const snapshot = await db.collection('pages')
  .where('category', '==', 'sections')
  .get();
```

### Search by Title
```javascript
const snapshot = await db.collection('pages')
  .where('title', '>=', 'Fermion')
  .where('title', '<=', 'Fermion\uf8ff')
  .get();
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot find module 'firebase-admin'" | Run `npm install` |
| "Service account key not found" | Download from Firebase Console > Project Settings > Service Accounts |
| Upload is slow | Normal for 50+ files, takes 1-2 minutes |
| Some pages have 0 sections | Expected for component files, mainContent still captured |

## Files

- `firebase-upload-website-content.js` - Main upload script (15KB)
- `test-html-extraction.js` - Test without Firebase (6KB)
- `README-FIREBASE-UPLOAD.md` - Detailed setup guide (7KB)
- `USAGE-EXAMPLES.md` - Comprehensive examples (13KB)
- `QUICK-REFERENCE.md` - This file

## Firestore Collection

**Collection:** `pages`
- **Total Documents:** ~58
- **Average Size:** ~50KB per document
- **Total Storage:** ~3MB
- **Queries:** No special indexes needed for basic queries

## Next Steps

1. **First time setup:**
   ```bash
   npm install
   ```

2. **Test extraction:**
   ```bash
   node scripts/test-html-extraction.js
   ```

3. **Dry run:**
   ```bash
   node scripts/firebase-upload-website-content.js --dry-run
   ```

4. **Upload:**
   ```bash
   node scripts/firebase-upload-website-content.js
   ```

5. **Verify in Firebase Console:**
   - Go to Firestore Database
   - Check `pages` collection
   - Browse documents

## Support

See detailed documentation:
- Setup: `README-FIREBASE-UPLOAD.md`
- Examples: `USAGE-EXAMPLES.md`
- Test first: `node scripts/test-html-extraction.js`
