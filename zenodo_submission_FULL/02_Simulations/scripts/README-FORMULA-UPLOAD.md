# Formula Database Upload to Firebase

This directory contains scripts to upload the Principia Metaphysica formula database to Firebase Firestore.

## Files

- **upload-formula-database.js** - Main upload script
- **test-formula-parser.js** - Test parser without Firebase (no dependencies required)
- **../upload-formulas.bat** - Windows batch file to run the upload

## What Gets Uploaded

### 1. Formulas Collection (`formulas/`)

Each formula from `js/formula-definitions.js` is uploaded as a document with:

- **Core Fields:**
  - `id` - Unique identifier
  - `key` - Object key in PM_FORMULAS
  - `category` - ESTABLISHED / THEORY / DERIVED / PREDICTIONS
  - `html` - HTML-formatted equation
  - `latex` - LaTeX version
  - `label` - Equation number and name

- **Content:**
  - `description` - Plain English explanation
  - `attribution` - Source/citation
  - `terms` - Object mapping symbols to definitions with tooltips

- **Validation:**
  - `status` - Current validation status
  - `v12_7_status` - Status in v12.7 verified framework
  - `pm_constant` - Path to PM value (e.g., "PM.topology.n_gen")
  - `experimental_value` - Measured value
  - `experimental_source` - Source of measurement
  - `sigma` - Agreement with experiment (standard deviations)

- **Additional:**
  - `derivation` - How the formula was derived
  - `consistency` - Consistency checks
  - `references` - Related pages
  - `testBy` - Future experimental test
  - `currentData` - Current experimental status
  - `falsification` - Falsification criteria

### 2. Formula Database Collection (`formula_database/`)

Tooltip metadata from `js/formula-database.js`:

- `id` - Unique identifier
- `symbol` / `htmlSymbol` / `textSymbol` - Different symbol formats
- `value` - Numerical value
- `pmRef` - Reference to PM constant path
- `description` - Short description
- `longDescription` - Extended explanation
- `category` - scales / cosmology / neutrinos / etc.
- `formula` - Formula representation
- `experimental` - Experimental comparison
- `occurrences` - Usage count
- `usedIn` - Pages where used
- `foundational` / `validated` / `exactMatch` / `prediction` - Boolean flags

### 3. Metadata Collection (`formula_metadata/`)

Summary document at `formula_metadata/current`:

- Upload timestamp
- Version (12.7)
- Formula counts by category
- Tooltip counts
- Source file paths

## Setup

### Prerequisites

1. **Node.js** - Version 14 or higher
2. **Firebase Service Account Key**
   - Download from [Firebase Console](https://console.firebase.google.com/)
   - Project: `principia-metaphysica`
   - Go to: Project Settings > Service Accounts > Generate New Private Key
   - Save as: `scripts/serviceAccountKey.json`

### Install Dependencies

```bash
npm install
```

This installs:
- `firebase-admin` - Firebase SDK
- `cheerio` - HTML parsing (for other scripts)

## Usage

### Option 1: Windows Batch File (Recommended)

```cmd
upload-formulas.bat
```

This will:
1. Install dependencies if needed
2. Check for service account key
3. Run the upload
4. Show results

### Option 2: Direct Node Command

```bash
# Test parsing without uploading
node scripts/test-formula-parser.js

# Upload to Firebase (merge mode)
node scripts/upload-formula-database.js

# Force overwrite all documents
node scripts/upload-formula-database.js --force

# Dry run (test without uploading)
node scripts/upload-formula-database.js --dry-run
```

### Option 3: NPM Scripts

```bash
# Dry run
npm run upload-formulas-dry

# Upload
npm run upload-formulas
```

## Output Example

```
══════════════════════════════════════════════════════════════════════
 PRINCIPIA METAPHYSICA - FORMULA DATABASE UPLOAD
══════════════════════════════════════════════════════════════════════
Timestamp: 2025-12-13T02:56:34.986Z
Mode: LIVE UPLOAD
Force: false
══════════════════════════════════════════════════════════════════════

📖 Reading formula-definitions.js...
✓ Parsed PM_FORMULAS object

📖 Reading formula-database.js...
✓ Parsed FORMULA_DATABASE object

📦 Uploading formulas to Firestore...
Total formulas to upload: 55

  Processing ESTABLISHED (18 formulas)...
    ✓ Committed batch of 18 formulas

  Processing THEORY (19 formulas)...
    ✓ Committed batch of 19 formulas

  Processing DERIVED (8 formulas)...
    ✓ Committed batch of 8 formulas

  Processing PREDICTIONS (10 formulas)...
    ✓ Committed batch of 10 formulas

✓ Uploaded 55/55 formulas

Breakdown by category:
  ESTABLISHED: 18
  THEORY: 19
  DERIVED: 8
  PREDICTIONS: 10

📦 Uploading formula database (tooltip metadata)...
  ✓ Committed final batch of 15 entries
✓ Uploaded 15/15 tooltip entries

📦 Creating metadata document...
✓ Created formula_metadata/current

══════════════════════════════════════════════════════════════════════
 ✅ UPLOAD COMPLETE
══════════════════════════════════════════════════════════════════════

Summary:
  Formulas uploaded: 55/55
  Tooltips uploaded: 15/15

Collections updated:
  - formulas/
  - formula_database/
  - formula_metadata/current
```

## Data Structure

### Formula Document Example

```json
{
  "id": "generation-number-26d",
  "key": "generationNumber26D",
  "category": "DERIVED",
  "html": "n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3",
  "latex": "n_{gen} = \\chi_{eff}/48 = 144/48 = 3",
  "label": "(2.6) Three Generations [26D Framework]",
  "description": "Topological derivation of exactly 3 fermion generations...",
  "attribution": "Principia Metaphysica",
  "status": "VERIFIED",
  "v12_7_status": "exact - topologically required",
  "pm_constant": "PM.topology.n_gen",
  "experimental_value": 3,
  "sigma": 0.0,
  "derivation": "Pure topology - χ_eff = 144 from G-flux corrections...",
  "terms": {
    "n<sub>gen</sub>": {
      "name": "Generations",
      "description": "= 3 (observed)"
    },
    "χ<sub>eff</sub>": {
      "name": "Effective Euler Char",
      "description": "144 from flux-dressed topology"
    }
  },
  "uploadedAt": "2025-12-13T02:56:35.123Z"
}
```

### Tooltip Entry Example

```json
{
  "id": "M_GUT",
  "key": "M_GUT",
  "symbol": "M<sub>GUT</sub>",
  "htmlSymbol": "M<sub>GUT</sub>",
  "textSymbol": "M_GUT",
  "value": "2.118 × 10¹⁶ GeV",
  "pmRef": "PM.proton_decay.M_GUT",
  "description": "Grand unified scale",
  "longDescription": "GUT scale derived geometrically from G₂ manifold TCS torsion",
  "category": "scales",
  "formula": "M<sub>GUT</sub> = M<sub>*</sub> exp(T<sub>ω</sub>s/2)",
  "derivation": "Geometric from twisted connected sum (TCS) G₂ torsion, not fitted",
  "occurrences": 112,
  "usedIn": ["gauge-unification", "predictions", "fermion-sector", "paper"],
  "foundational": true,
  "uploadedAt": "2025-12-13T02:56:35.456Z"
}
```

## Firestore Security Rules

Ensure your Firestore rules allow writes:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Formulas - read-only for public, write for admin
    match /formulas/{formulaId} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }

    match /formula_database/{entryId} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }

    match /formula_metadata/{docId} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
  }
}
```

## Troubleshooting

### "serviceAccountKey.json not found"

Download from Firebase Console:
1. https://console.firebase.google.com/
2. Select: principia-metaphysica
3. Settings > Service Accounts
4. Generate New Private Key
5. Save to: `scripts/serviceAccountKey.json`

### "Cannot find module 'firebase-admin'"

Run: `npm install`

### "Permission denied"

Check Firebase security rules and service account permissions.

### Parsing Errors

Run test parser first:
```bash
node scripts/test-formula-parser.js
```

This will show exactly what's being parsed without uploading.

## Integration with Website

After uploading, the website can:

1. **Fetch formulas dynamically:**
   ```javascript
   const formulas = await db.collection('formulas')
     .where('category', '==', 'PREDICTIONS')
     .get();
   ```

2. **Show tooltips from formula_database:**
   ```javascript
   const tooltip = await db.collection('formula_database')
     .doc('M_GUT')
     .get();
   ```

3. **Link to PM constants:**
   ```javascript
   const formula = await db.collection('formulas')
     .where('pm_constant', '==', 'PM.topology.n_gen')
     .get();
   ```

## Maintenance

- **Update formulas:** Edit `js/formula-definitions.js` and re-run upload
- **Update tooltips:** Edit `js/formula-database.js` and re-run upload
- **Version tracking:** Upload creates versioned backups in metadata
- **Incremental updates:** Default merge mode preserves existing data
- **Force refresh:** Use `--force` flag to completely overwrite

## Source Files

- **Formulas:** `h:/Github/PrincipiaMetaphysica/js/formula-definitions.js`
- **Tooltips:** `h:/Github/PrincipiaMetaphysica/js/formula-database.js`
- **Upload Script:** `h:/Github/PrincipiaMetaphysica/scripts/upload-formula-database.js`

## License

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
