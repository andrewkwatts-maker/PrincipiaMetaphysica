# Firebase Website Content Upload - File Index

Quick navigation for all Firebase upload documentation and scripts.

## Start Here

**New to the upload system?** Start with these files in order:

1. **QUICK-REFERENCE.md** - Quick command reference (3 min read)
2. **README-FIREBASE-UPLOAD.md** - Setup guide (5 min read)
3. **test-html-extraction.js** - Test without Firebase (run this first)
4. **firebase-upload-website-content.js** - Main upload script

## All Files

### Scripts

| File | Lines | Purpose | Run Command |
|------|-------|---------|-------------|
| **firebase-upload-website-content.js** | 465 | Main upload script | `node scripts/firebase-upload-website-content.js` |
| **test-html-extraction.js** | ~200 | Test HTML parsing | `node scripts/test-html-extraction.js` |

### Documentation

| File | Size | Purpose | Read Time |
|------|------|---------|-----------|
| **QUICK-REFERENCE.md** | 3KB | Command cheat sheet | 3 min |
| **README-FIREBASE-UPLOAD.md** | 7KB | Setup and usage guide | 5 min |
| **USAGE-EXAMPLES.md** | 13KB | Code examples and queries | 10 min |
| **FIREBASE-UPLOAD-SUMMARY.md** | 12KB | Comprehensive overview | 10 min |
| **INDEX-FIREBASE-UPLOAD.md** | This file | File navigation | 2 min |

**Total:** 2 scripts + 5 documentation files

## Quick Start Guide

### First Time Setup

```bash
# 1. Install dependencies
npm install

# 2. Test HTML extraction (no Firebase needed)
node scripts/test-html-extraction.js

# 3. Add Firebase service account key
# Download from: Firebase Console > Project Settings > Service Accounts
# Save to: scripts/serviceAccountKey.json

# 4. Dry run (test upload without committing)
node scripts/firebase-upload-website-content.js --dry-run

# 5. Live upload
node scripts/firebase-upload-website-content.js
```

### Regular Usage

```bash
# After updating HTML files, re-upload
node scripts/firebase-upload-website-content.js
```

## File Descriptions

### firebase-upload-website-content.js

**Main upload script** - Uploads all website HTML content to Firestore

**Features:**
- Scans 58+ HTML files across all directories
- Extracts title, description, content, sections, formulas, PM refs
- Batch uploads (400 docs per batch)
- Dry run mode for testing
- Comprehensive error handling
- Progress tracking and statistics

**Usage:**
```bash
# Dry run (no upload)
node scripts/firebase-upload-website-content.js --dry-run

# Live upload
node scripts/firebase-upload-website-content.js
```

### test-html-extraction.js

**Testing script** - Tests HTML parsing without Firebase

**Features:**
- Tests extraction on sample files
- No Firebase credentials needed
- Shows what data would be extracted
- Useful for debugging parsing issues

**Usage:**
```bash
node scripts/test-html-extraction.js
```

### QUICK-REFERENCE.md

**Quick reference card** - Command cheat sheet

**Contains:**
- All commands
- Document structure
- Query examples
- Troubleshooting table

**When to use:** Quick lookup while working

### README-FIREBASE-UPLOAD.md

**Setup guide** - Detailed setup and usage instructions

**Contains:**
- Setup steps
- File locations
- Data structure
- Querying examples
- Troubleshooting

**When to use:** First time setup, detailed reference

### USAGE-EXAMPLES.md

**Code examples** - Comprehensive usage examples

**Contains:**
- Test examples
- Dry run examples
- Live upload examples
- Query code (Web, Node.js, React Native)
- Sample documents
- Advanced usage
- CI/CD integration

**When to use:** When integrating with apps, writing queries

### FIREBASE-UPLOAD-SUMMARY.md

**Complete overview** - Comprehensive summary

**Contains:**
- All features
- Performance metrics
- Cost estimation
- Security considerations
- Maintenance guide
- Future enhancements

**When to use:** Understanding the full system, planning

### INDEX-FIREBASE-UPLOAD.md

**This file** - Navigation index

**Contains:**
- File descriptions
- Quick start
- Navigation links

**When to use:** Finding the right documentation

## What Gets Uploaded

### File Coverage

| Directory | Files | Examples |
|-----------|-------|----------|
| Root | 9 | index.html, beginners-guide.html |
| sections/ | 17 | introduction.html, fermion-sector.html |
| foundations/ | 14 | dirac-equation.html, clifford-algebra.html |
| docs/ | 3 | computational-appendices.html |
| diagrams/ | 1 | theory-diagrams.html |
| components/ | 14 | button.html, expandable.html |

**Total: ~58 files**

### Data Extracted Per File

- **id** - Unique identifier (e.g., `sections-fermion-sector`)
- **path** - Relative file path
- **category** - Directory category
- **title** - Page title
- **description** - Meta description
- **mainContent** - Main HTML content (100KB max)
- **sections** - Array of sections with {id, heading, html}
- **formulas** - Array of formula elements
- **pmValueRefs** - Array of PM value references
- **headings** - Document outline structure
- **links** - External links (max 100)
- **lastUpdated** - ISO timestamp
- **uploadedAt** - Firebase server timestamp

## Common Tasks

### Test Before Upload

```bash
node scripts/test-html-extraction.js
```

### See What Would Be Uploaded

```bash
node scripts/firebase-upload-website-content.js --dry-run
```

### Upload Everything

```bash
node scripts/firebase-upload-website-content.js
```

### Query Uploaded Data

See **USAGE-EXAMPLES.md** for detailed query examples:
- Get all pages
- Get by category
- Get specific page
- Search by title
- Filter by PM references

## Troubleshooting

| Problem | File to Check | Section |
|---------|---------------|---------|
| Can't find modules | README-FIREBASE-UPLOAD.md | Setup |
| Service account issues | README-FIREBASE-UPLOAD.md | Service Account Key |
| Parse errors | Test with test-html-extraction.js | - |
| Query help | USAGE-EXAMPLES.md | Querying the Data |
| Upload failures | FIREBASE-UPLOAD-SUMMARY.md | Troubleshooting |

## Architecture

### Upload Flow

```
HTML Files (58)
    ↓
test-html-extraction.js (test locally)
    ↓
firebase-upload-website-content.js --dry-run (test Firebase flow)
    ↓
firebase-upload-website-content.js (live upload)
    ↓
Firestore collection: pages (58 documents)
    ↓
Mobile app / Web app (query and display)
```

### Data Flow

```
index.html
    ↓ [cheerio parsing]
{
  title: "Principia Metaphysica",
  description: "...",
  sections: [...],
  formulas: [...]
}
    ↓ [batch upload]
Firestore: pages/index
    ↓ [Firebase SDK]
Mobile App Display
```

## Integration Points

### React Native

```javascript
import firestore from '@react-native-firebase/firestore';

const pages = await firestore()
  .collection('pages')
  .where('category', '==', 'sections')
  .get();
```

See **USAGE-EXAMPLES.md** → Integration Examples → React Native

### Web (Firebase v9)

```javascript
import { getFirestore, collection, getDocs } from 'firebase/firestore';

const db = getFirestore();
const snapshot = await getDocs(collection(db, 'pages'));
```

See **USAGE-EXAMPLES.md** → Integration Examples → Web App

### Node.js Backend

```javascript
const admin = require('firebase-admin');
const db = admin.firestore();

const doc = await db.collection('pages').doc('sections-fermion-sector').get();
```

See **USAGE-EXAMPLES.md** → Integration Examples → Backend/Admin

## Performance

- **Upload time:** 1-2 minutes for 58 files
- **Batch size:** 400 documents per batch
- **Document size:** ~50KB average
- **Total storage:** ~3MB
- **Query time:** 20-100ms typical

See **FIREBASE-UPLOAD-SUMMARY.md** → Performance Metrics

## Costs

- **Storage:** Free tier (1GB includes 3MB easily)
- **Reads:** Free tier (50K/day)
- **Writes:** Free tier (20K/day)
- **Estimated:** $0-$5/month for normal usage

See **FIREBASE-UPLOAD-SUMMARY.md** → Cost Estimation

## Support

1. **Quick answers:** Check QUICK-REFERENCE.md
2. **Setup help:** Check README-FIREBASE-UPLOAD.md
3. **Code examples:** Check USAGE-EXAMPLES.md
4. **Deep dive:** Check FIREBASE-UPLOAD-SUMMARY.md
5. **Test locally:** Run test-html-extraction.js
6. **Test Firebase:** Run with --dry-run flag

## Next Steps

1. **Read:** QUICK-REFERENCE.md (3 min)
2. **Setup:** Follow README-FIREBASE-UPLOAD.md
3. **Test:** Run test-html-extraction.js
4. **Upload:** Run firebase-upload-website-content.js --dry-run
5. **Go Live:** Run without --dry-run
6. **Integrate:** Use examples from USAGE-EXAMPLES.md

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Part of the Principia Metaphysica project.
