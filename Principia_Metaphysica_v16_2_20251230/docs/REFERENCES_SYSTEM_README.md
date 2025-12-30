# Firebase References System - Principia Metaphysica

## Overview

The Firebase References System provides centralized management of academic citations across the entire Principia Metaphysica website. References are stored in Firestore and dynamically loaded on both the main paper and the references page.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Firestore Database                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Collection: references                               │   │
│  │  ├─ einstein1915                                      │   │
│  │  ├─ joyce2000                                         │   │
│  │  ├─ acharya1998                                       │   │
│  │  └─ ...                                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
                   ┌───────────────┐
                   │ firebase-     │
                   │ references.js │
                   └───────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                                      ↓
┌──────────────────┐                  ┌──────────────────┐
│ references.html  │                  │ principia-       │
│                  │                  │ metaphysica-     │
│ - Full citations │                  │ paper.html       │
│ - BibTeX export  │                  │                  │
│ - Category view  │                  │ - Inline cites   │
└──────────────────┘                  │ - Reference links│
                                      └──────────────────┘
```

## File Structure

```
PrincipiaMetaphysica/
├── js/
│   └── firebase-references.js          # Main references module
├── scripts/
│   ├── migrate-references-to-firebase.js  # Migration script
│   └── test-references.js              # Test suite
├── docs/
│   ├── FIRESTORE_REFERENCES_SCHEMA.md  # Schema documentation
│   └── REFERENCES_SYSTEM_README.md     # This file
├── firestore.rules                      # Security rules
└── firestore.indexes.json              # Index configuration
```

## Quick Start

### 1. Install Dependencies

```bash
npm install firebase-admin jsdom
```

### 2. Run Migration

Parse existing references from `references.html` and upload to Firestore:

```bash
# Dry run (preview only)
node scripts/migrate-references-to-firebase.js --dry-run

# Actual migration
node scripts/migrate-references-to-firebase.js
```

### 3. Deploy Indexes

Deploy Firestore indexes for efficient querying:

```bash
firebase deploy --only firestore:indexes
```

### 4. Deploy Security Rules

```bash
firebase deploy --only firestore:rules
```

### 5. Test the System

```bash
node scripts/test-references.js
```

## Usage Examples

### Loading References in HTML

#### references.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>References - Principia Metaphysica</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <main id="references-container">
        <!-- References will be dynamically loaded here -->
    </main>

    <script type="module">
        import { initializeReferences, renderAllReferences } from './js/firebase-references.js';

        document.addEventListener('DOMContentLoaded', async () => {
            // Initialize and load all references
            await initializeReferences();
            const container = document.getElementById('references-container');
            await renderAllReferences(container);
        });
    </script>
</body>
</html>
```

#### principia-metaphysica-paper.html

```html
<script type="module">
    import {
        loadReferenceByCitation,
        renderInlineCitation,
        getReferencesForFormula
    } from './js/firebase-references.js';

    // Replace citation keys with linked references
    async function replaceCitations() {
        const citations = document.querySelectorAll('.citation-key');

        for (const el of citations) {
            const citationKey = el.textContent.trim();
            const ref = await loadReferenceByCitation(citationKey);

            if (ref) {
                const citation = renderInlineCitation(ref, { link: true });
                el.replaceWith(citation);
            }
        }
    }

    // Get references for a specific formula
    async function showFormulaReferences(formulaId) {
        const refs = await getReferencesForFormula(formulaId);
        console.log(`Formula ${formulaId} cites:`, refs);
    }

    document.addEventListener('DOMContentLoaded', async () => {
        await replaceCitations();
    });
</script>
```

### JavaScript API Examples

```javascript
import {
    loadAllReferences,
    loadReference,
    loadReferencesByCategory,
    loadReferenceByCitation,
    searchReferences,
    getBibTeX,
    copyBibTeXToClipboard
} from './js/firebase-references.js';

// Load all references
const allRefs = await loadAllReferences();
console.log(`Loaded ${allRefs.length} references`);

// Load a specific reference
const einstein = await loadReference('einstein1915');
console.log(einstein.title); // "Die Feldgleichungen der Gravitation"

// Load by category
const geometryRefs = await loadReferencesByCategory('geometry-topology');
console.log(`Geometry & Topology: ${geometryRefs.length} references`);

// Load by citation key (for inline citations)
const joyce = await loadReferenceByCitation('Joyce 2000');
console.log(joyce.title); // "Compact Manifolds with Special Holonomy"

// Search references
const g2Refs = await searchReferences('G₂ manifold');
console.log(`Found ${g2Refs.length} references about G₂ manifolds`);

// Get BibTeX
const bibtex = getBibTeX(einstein);
console.log(bibtex);

// Copy BibTeX to clipboard
await copyBibTeXToClipboard('einstein1915');
// User notification: "BibTeX copied to clipboard!"
```

### Rendering References

```javascript
import {
    renderFullReference,
    renderInlineCitation,
    renderReferenceCategory
} from './js/firebase-references.js';

// Render full reference (for references page)
const ref = await loadReference('joyce2000');
const refElement = renderFullReference(ref);
document.getElementById('references-list').appendChild(refElement);

// Render inline citation (for paper)
const citation = renderInlineCitation(ref, { link: true });
// Creates: <span class="inline-citation"><a href="references.html#joyce2000">[Joyce 2000]</a></span>

// Render an entire category
const geometryRefs = await loadReferencesByCategory('geometry-topology');
const section = renderReferenceCategory(
    'geometry-topology',
    'Geometry & Topology',
    geometryRefs,
    { description: 'Mathematical foundations of differential geometry' }
);
document.querySelector('main').appendChild(section);
```

## Data Structure

### Reference Object

```javascript
{
  id: "acharya1998",
  title: "M Theory, Joyce Orbifolds and Super Yang-Mills",
  authors: "Acharya, B.S.",
  year: 1998,
  journal: "Advances in Theoretical and Mathematical Physics 3: 227-248 (1998)",
  volume: "3",
  pages: "227-248",
  doi: null,
  arxiv: "hep-th/9812205",
  citation_key: "Acharya 1998",
  category: "string-m-theory",
  type: "theoretical",
  tags: ["M-Theory", "G₂ Compactification"],
  links: [
    {
      label: "arXiv",
      url: "https://arxiv.org/abs/hep-th/9812205"
    }
  ],
  description: "M-theory compactifications on G₂ manifolds...",
  cited_in_formulas: ["gauge_unification", "g2_holonomy"],
  cited_in_sections: ["geometric-framework", "gauge-sector"],
  bibtex: "@article{acharya1998,...}",
  created_at: Timestamp,
  updated_at: Timestamp
}
```

## Categories

- **foundational-physics**: Einstein field equations, general relativity
- **quantum-field-theory**: QFT, Dirac equation, Yang-Mills
- **geometry-topology**: G₂ manifolds, Calabi-Yau, Clifford algebras
- **string-m-theory**: M-theory on G₂, string compactifications
- **tcs-g2-constructions**: Twisted connected sums
- **two-time-physics**: Sp(2,R) formalism
- **moduli-stabilization**: KKLT, flux compactifications
- **extra-dimensions**: Kaluza-Klein, Randall-Sundrum
- **grand-unification**: SU(5), SO(10), GUTs
- **phenomenology-experiment**: LHC, Super-K, experimental data
- **thermal-time**: Thermal time hypothesis, KMS condition
- **cosmology**: DESI, Planck, dark energy
- **neutrinos**: Seesaw mechanism, oscillations

## Reference Types

- **experimental**: Experimental papers (LHC, Super-K)
- **theoretical**: Theoretical papers
- **review**: Review articles
- **textbook**: Textbooks and monographs
- **paper**: Generic paper

## Maintenance

### Adding New References

#### Via Firebase Console

1. Go to Firebase Console → Firestore Database
2. Navigate to `references` collection
3. Click "Add document"
4. Set document ID (e.g., `newauthor2025`)
5. Add fields according to schema
6. Save

#### Via Script

Create a new script `scripts/add-reference.js`:

```javascript
const admin = require('firebase-admin');
const serviceAccount = require('../firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: 'principia-metaphysica'
});

const db = admin.firestore();

async function addReference() {
  const ref = {
    title: "New Paper Title",
    authors: "Author, A., Coauthor, B.",
    year: 2025,
    journal: "Journal Name 123: 456-789 (2025)",
    category: "string-m-theory",
    type: "theoretical",
    citation_key: "Author 2025",
    tags: ["Tag1", "Tag2"],
    links: [
      { label: "arXiv", url: "https://arxiv.org/abs/2501.12345" }
    ],
    description: "Brief description of the paper's relevance",
    cited_in_formulas: [],
    cited_in_sections: [],
    created_at: admin.firestore.FieldValue.serverTimestamp(),
    updated_at: admin.firestore.FieldValue.serverTimestamp()
  };

  await db.collection('references').doc('author2025').set(ref);
  console.log('Reference added!');
}

addReference();
```

### Updating References

```javascript
const admin = require('firebase-admin');
// ... initialization ...

async function updateReference(refId, updates) {
  await db.collection('references').doc(refId).update({
    ...updates,
    updated_at: admin.firestore.FieldValue.serverTimestamp()
  });
}

// Example: Add citation to a formula
await updateReference('einstein1915', {
  cited_in_formulas: admin.firestore.FieldValue.arrayUnion('new_formula_id')
});
```

### Bulk Updates

```javascript
async function bulkUpdateCategory(category, updates) {
  const batch = db.batch();
  const snapshot = await db.collection('references')
    .where('category', '==', category)
    .get();

  snapshot.forEach(doc => {
    batch.update(doc.ref, {
      ...updates,
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
  });

  await batch.commit();
  console.log(`Updated ${snapshot.size} references`);
}
```

## Performance Optimization

### Caching

The references module implements client-side caching with a 10-minute TTL:

```javascript
// Cache is automatically managed
const refs1 = await loadAllReferences(); // Hits Firestore
const refs2 = await loadAllReferences(); // Returns cached data

// Clear cache manually if needed
clearReferencesCache();
```

### Pagination (Future)

For large reference lists, implement pagination:

```javascript
async function loadReferencesPaginated(category, limit = 50, startAfter = null) {
  let query = db.collection('references')
    .where('category', '==', category)
    .orderBy('year')
    .limit(limit);

  if (startAfter) {
    query = query.startAfter(startAfter);
  }

  const snapshot = await query.get();
  const references = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  const lastDoc = snapshot.docs[snapshot.docs.length - 1];

  return { references, lastDoc };
}
```

## Troubleshooting

### References not loading

1. Check Firebase authentication is working
2. Verify Firestore security rules allow read access
3. Check browser console for errors
4. Verify indexes are deployed

### Citation keys not found

1. Ensure citation_key field is correctly set
2. Check for typos in citation key string
3. Verify index on citation_key is deployed

### Slow loading

1. Check cache is working (10 minute TTL)
2. Verify Firestore indexes are deployed
3. Consider pagination for large lists
4. Check network conditions

## Security

- **Read Access**: Requires Google authentication
- **Write Access**: Admin SDK only (no client writes)
- **Rate Limiting**: Implemented via Firebase App Check
- **Data Validation**: Schema validation in migration script

## Testing

Run the test suite to verify everything works:

```bash
node scripts/test-references.js
```

Tests include:
- Loading all references
- Loading by ID
- Loading by category
- Citation key lookups
- BibTeX generation
- Data integrity validation
- Tag searching
- Link validation

## Future Enhancements

1. **Citation Graph Visualization**: Show which formulas cite which papers
2. **Export Formats**: EndNote, Zotero, Mendeley
3. **Related Papers**: Suggest related references based on tags
4. **PDF Repository**: Link to hosted PDFs
5. **Citation Analytics**: Track most-cited papers
6. **Admin Web UI**: Manage references via browser interface
7. **Full-Text Search**: Algolia integration for advanced search
8. **Author Disambiguation**: Handle name variations
9. **DOI Resolver**: Auto-fetch metadata from DOI
10. **arXiv Integration**: Auto-update from arXiv API

## Support

For questions or issues:
- Email: AndrewKWatts@Gmail.com
- Documentation: `/docs/FIRESTORE_REFERENCES_SCHEMA.md`
- Test Suite: `scripts/test-references.js`

## Copyright

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
