# Firestore References Schema - Principia Metaphysica

## Overview

The references system stores academic citations in Firestore to serve both the main paper (`principia-metaphysica-paper.html`) and the references page (`references.html`). This enables centralized management, dynamic updates, and consistent formatting across the entire website.

## Collection: `references`

Each document in the `references` collection represents a single academic reference (paper, book, article, etc.).

### Document Structure

```typescript
interface Reference {
  // === Core Metadata ===
  id: string;                    // Firestore document ID (e.g., 'einstein1915', 'joyce2000')
  title: string;                 // Full title of the work
  authors: string;               // Comma-separated author list (e.g., "Einstein, A.")
  year: number;                  // Publication year

  // === Publication Details ===
  journal: string;               // Journal/publisher/conference (full citation string)
  volume?: string;               // Volume number
  pages?: string;                // Page range (e.g., "123-456")

  // === Identifiers ===
  doi?: string;                  // DOI (without https://doi.org/ prefix)
  arxiv?: string;                // arXiv identifier (e.g., "hep-th/0107177")
  isbn?: string;                 // ISBN for books

  // === Citation ===
  citation_key: string;          // Short citation key (e.g., "Einstein 1915", "Acharya et al. 1998")
  bibtex: string;                // Full BibTeX entry

  // === Categorization ===
  category: string;              // Reference category (see CATEGORIES below)
  type: ReferenceType;           // Reference type (see TYPES below)
  tags: string[];                // Keyword tags for searching/filtering

  // === Links ===
  links: Link[];                 // External links (DOI, arXiv, Wikipedia, etc.)

  // === Context ===
  description?: string;          // Optional description/note about the reference
  cited_in_formulas: string[];   // Array of formula IDs that cite this reference
  cited_in_sections: string[];   // Array of section IDs that cite this reference

  // === Metadata ===
  created_at: Timestamp;         // Firestore server timestamp
  updated_at: Timestamp;         // Firestore server timestamp
}

interface Link {
  label: string;                 // Display label (e.g., "DOI", "arXiv", "Wikipedia")
  url: string;                   // Full URL
}

enum ReferenceType {
  EXPERIMENTAL = 'experimental',    // Experimental papers (LHC, Super-K, etc.)
  THEORETICAL = 'theoretical',      // Theoretical papers
  REVIEW = 'review',                // Review articles
  TEXTBOOK = 'textbook',            // Textbooks and monographs
  PAPER = 'paper'                   // Generic paper
}
```

### Categories

References are organized into the following categories:

| Category ID | Display Title | Description |
|------------|---------------|-------------|
| `foundational-physics` | Foundational Physics | Einstein field equations, general relativity foundations |
| `quantum-field-theory` | Quantum Field Theory | QFT, Dirac equation, Yang-Mills theory |
| `geometry-topology` | Geometry & Topology | G₂ manifolds, Calabi-Yau, Clifford algebras, index theorem |
| `string-m-theory` | String Theory & M-Theory | M-theory on G₂, string compactifications |
| `tcs-g2-constructions` | TCS G₂ Manifolds & Modern Constructions | Twisted connected sums, modern G₂ constructions |
| `two-time-physics` | Two-Time Physics | Sp(2,R) formalism, ghost elimination |
| `moduli-stabilization` | Moduli Stabilization | KKLT, Large Volume Scenario, flux compactifications |
| `extra-dimensions` | Extra Dimensions, Kaluza-Klein Theory & Warped Geometry | KK theory, Randall-Sundrum, heterogeneous branes |
| `grand-unification` | Grand Unified Theories (GUTs) | SU(5), SO(10), proton decay |
| `phenomenology-experiment` | Phenomenology & Experiment | LHC searches, gravitational waves, experimental bounds |
| `thermal-time` | Thermal Time & Statistical Mechanics | Thermal time hypothesis, KMS condition, modular theory |
| `cosmology` | Cosmology & Dark Energy | DESI, Planck, dark energy evolution |
| `neutrinos` | Neutrino Physics | Seesaw mechanism, oscillations, mass ordering |

## Indexes

The following Firestore indexes are required for efficient querying:

### Composite Indexes

1. **Category + Year**: Enables loading references by category, sorted chronologically
   - Fields: `category (ASC)`, `year (ASC)`

2. **Type + Year**: Enables filtering by reference type, sorted chronologically
   - Fields: `type (ASC)`, `year (ASC)`

### Single Field Indexes

3. **Citation Key**: Fast lookup for inline citations
   - Field: `citation_key (ASC)`

### Array-Contains Indexes

4. **Cited in Formulas**: Find all references cited by a specific formula
   - Field: `cited_in_formulas (ARRAY_CONTAINS)`

5. **Cited in Sections**: Find all references cited in a specific section
   - Field: `cited_in_sections (ARRAY_CONTAINS)`

### Deployment

Deploy indexes using the Firebase CLI:

```bash
firebase deploy --only firestore:indexes
```

Index configuration is stored in `firestore.indexes.json`.

## Example Documents

### Theoretical Paper (with arXiv)

```json
{
  "id": "acharya1998",
  "title": "M Theory, Joyce Orbifolds and Super Yang-Mills",
  "authors": "Acharya, B.S.",
  "year": 1998,
  "journal": "Advances in Theoretical and Mathematical Physics 3: 227-248 (1998)",
  "volume": "3",
  "pages": "227-248",
  "arxiv": "hep-th/9812205",
  "citation_key": "Acharya 1998",
  "category": "string-m-theory",
  "type": "theoretical",
  "tags": ["M-Theory", "G₂ Compactification"],
  "links": [
    {
      "label": "arXiv",
      "url": "https://arxiv.org/abs/hep-th/9812205"
    }
  ],
  "description": "M-theory compactifications on G₂ manifolds. Shows how ADE singularities yield SO(10) and other gauge groups. Foundation for PM's gauge structure from geometry.",
  "cited_in_formulas": ["gauge_unification", "g2_holonomy"],
  "cited_in_sections": ["geometric-framework", "gauge-sector"],
  "bibtex": "@article{acharya1998,\n  author = {Acharya, B.S.},\n  title = {M Theory, Joyce Orbifolds and Super Yang-Mills},\n  journal = {Advances in Theoretical and Mathematical Physics},\n  year = {1998},\n  volume = {3},\n  pages = {227-248},\n  eprint = {hep-th/9812205},\n  archivePrefix = {arXiv}\n}",
  "created_at": "2025-12-13T00:00:00Z",
  "updated_at": "2025-12-13T00:00:00Z"
}
```

### Textbook

```json
{
  "id": "joyce2000",
  "title": "Compact Manifolds with Special Holonomy",
  "authors": "Joyce, D.D.",
  "year": 2000,
  "journal": "Oxford Mathematical Monographs (2000) ISBN: 978-0198506010",
  "isbn": "978-0198506010",
  "citation_key": "Joyce 2000",
  "category": "geometry-topology",
  "type": "textbook",
  "tags": ["G₂ Holonomy", "Special Geometry"],
  "links": [
    {
      "label": "Wikipedia",
      "url": "https://en.wikipedia.org/wiki/G2_manifold"
    }
  ],
  "description": "Definitive text on G₂ geometry. Covers construction methods, deformation theory, and moduli spaces of G₂ manifolds. Essential for understanding the geometric foundation of Principia Metaphysica compactifications.",
  "cited_in_formulas": ["g2_metric", "g2_holonomy"],
  "cited_in_sections": ["geometric-framework"],
  "bibtex": "@book{joyce2000,\n  author = {Joyce, D.D.},\n  title = {Compact Manifolds with Special Holonomy},\n  publisher = {Oxford Mathematical Monographs},\n  year = {2000},\n  isbn = {978-0198506010}\n}",
  "created_at": "2025-12-13T00:00:00Z",
  "updated_at": "2025-12-13T00:00:00Z"
}
```

### Experimental Paper (with DOI)

```json
{
  "id": "atlas2019",
  "title": "Search for new resonances in mass distributions of jet pairs using 139 fb⁻¹ of pp collisions at √s = 13 TeV with the ATLAS detector",
  "authors": "ATLAS Collaboration",
  "year": 2019,
  "journal": "Journal of High Energy Physics 2019, 145 (2019)",
  "volume": "2019",
  "pages": "145",
  "doi": "10.1007/JHEP03(2020)145",
  "arxiv": "1910.08447",
  "citation_key": "ATLAS 2019",
  "category": "phenomenology-experiment",
  "type": "experimental",
  "tags": ["LHC", "KK Gravitons"],
  "links": [
    {
      "label": "arXiv",
      "url": "https://arxiv.org/abs/1910.08447"
    },
    {
      "label": "DOI",
      "url": "https://doi.org/10.1007/JHEP03(2020)145"
    }
  ],
  "description": "Current experimental bounds on KK graviton masses: M_KK > 3.5 TeV at 95% CL. Sets constraints on compactification scale in extra-dimensional models.",
  "cited_in_formulas": ["kk_graviton_mass"],
  "cited_in_sections": ["predictions", "phenomenology"],
  "bibtex": "@article{atlas2019,\n  author = {ATLAS Collaboration},\n  title = {Search for new resonances in mass distributions of jet pairs using 139 fb⁻¹ of pp collisions at √s = 13 TeV with the ATLAS detector},\n  journal = {Journal of High Energy Physics},\n  year = {2019},\n  volume = {2019},\n  pages = {145},\n  doi = {10.1007/JHEP03(2020)145},\n  eprint = {1910.08447},\n  archivePrefix = {arXiv}\n}",
  "created_at": "2025-12-13T00:00:00Z",
  "updated_at": "2025-12-13T00:00:00Z"
}
```

## JavaScript Module API

### Loading Functions

```javascript
// Load all references
const refs = await loadAllReferences();

// Load single reference by ID
const ref = await loadReference('einstein1915');

// Load references by category
const geometryRefs = await loadReferencesByCategory('geometry-topology');

// Load by citation key
const ref = await loadReferenceByCitation('Einstein 1915');

// Search references
const results = await searchReferences('G₂ manifold');

// Get references for a formula
const refs = await getReferencesForFormula('pneuma_lagrangian');
```

### Rendering Functions

```javascript
// Render full reference (for references.html)
const element = renderFullReference(ref);

// Render inline citation (for paper)
const citation = renderInlineCitation(ref, { link: true });

// Render entire category
const section = renderReferenceCategory(
  'geometry-topology',
  'Geometry & Topology',
  refs,
  { description: 'Optional category description' }
);

// Render all references into container
await renderAllReferences(document.getElementById('references-container'));
```

### Utility Functions

```javascript
// Get BibTeX
const bibtex = getBibTeX(ref);

// Copy BibTeX to clipboard
await copyBibTeXToClipboard('einstein1915');

// Clear cache
clearReferencesCache();

// Initialize module (preload data)
await initializeReferences();
```

## Usage in HTML Pages

### references.html

```html
<script type="module">
  import { initializeReferences, renderAllReferences } from './js/firebase-references.js';

  // Initialize on page load
  document.addEventListener('DOMContentLoaded', async () => {
    await initializeReferences();
    const container = document.querySelector('main');
    await renderAllReferences(container);
  });
</script>
```

### principia-metaphysica-paper.html

```html
<script type="module">
  import { loadReferenceByCitation, renderInlineCitation } from './js/firebase-references.js';

  // Replace citation keys with links
  document.querySelectorAll('.citation').forEach(async (el) => {
    const citationKey = el.textContent;
    const ref = await loadReferenceByCitation(citationKey);
    if (ref) {
      el.replaceWith(renderInlineCitation(ref));
    }
  });
</script>
```

## Migration Process

1. **Parse existing references** from `references.html`
2. **Extract metadata**: title, authors, year, journal, DOI, arXiv, tags
3. **Generate BibTeX** for each reference
4. **Upload to Firestore** in batches
5. **Deploy indexes** for efficient querying
6. **Update HTML pages** to use `firebase-references.js`

### Running the Migration

```bash
# Dry run (preview without uploading)
node scripts/migrate-references-to-firebase.js --dry-run

# Actual migration
node scripts/migrate-references-to-firebase.js

# Deploy indexes
firebase deploy --only firestore:indexes
```

## Security Rules

Firestore security rules for the `references` collection:

```javascript
match /references/{refId} {
  // Anyone can read references
  allow read: if true;

  // Only authenticated users can write
  allow write: if request.auth != null;
}
```

## Maintenance

### Adding New References

New references can be added via:

1. **Firebase Console**: Manually add documents to `references` collection
2. **Admin Script**: Use Firebase Admin SDK to bulk upload
3. **Web Interface**: Future admin panel for authenticated users

### Updating Citations

To update which formulas/sections cite a reference:

```javascript
await db.collection('references').doc('einstein1915').update({
  cited_in_formulas: admin.firestore.FieldValue.arrayUnion('new_formula_id'),
  cited_in_sections: admin.firestore.FieldValue.arrayUnion('new_section_id'),
  updated_at: admin.firestore.FieldValue.serverTimestamp()
});
```

### Analytics

Track reference usage:

```javascript
// Log reference views
await logEvent(analytics, 'view_reference', {
  reference_id: 'einstein1915',
  category: 'foundational-physics',
  source: 'paper' // or 'references_page'
});

// Track BibTeX downloads
await logEvent(analytics, 'download_bibtex', {
  reference_id: 'einstein1915'
});
```

## Future Enhancements

1. **Citation Graph**: Visualize which formulas/sections cite which references
2. **Export Formats**: Export to EndNote, Zotero, Mendeley
3. **Related References**: Suggest related papers based on tags/citations
4. **PDF Links**: Integrate with PDF repository
5. **Citation Counts**: Track how many times each reference is viewed/cited
6. **Admin Panel**: Web interface for managing references
7. **Full-Text Search**: Integrate with Algolia for advanced search

## Copyright

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
