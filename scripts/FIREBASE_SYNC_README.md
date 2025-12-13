# Firebase Sync with Version History

## Overview

The Firebase sync system now includes **intelligent diffing** and **automatic version history** to prevent data loss and track changes over time.

## Key Features

1. **Smart Diffing**: Compares local data against current Firebase data before pushing
2. **Version History**: Automatically backs up current data before overwriting
3. **Change Detection**: Only uploads if actual changes are detected
4. **Clear Reporting**: Shows exactly what changed (added/removed/modified)
5. **Safe Rollback**: All previous versions stored in `theory_constants/history/backups/`

## Scripts

### Primary Script: `firebase-sync-with-history.js`

**Purpose**: Smart sync with automatic diffing and version history

**Usage**:
```bash
node scripts/firebase-sync-with-history.js
node scripts/firebase-sync-with-history.js --force  # Show all changes
```

**What it does**:
1. Reads `theory-constants-enhanced.js` (single source of truth)
2. Fetches current Firebase data from `theory_constants/current`
3. Computes detailed diff showing:
   - Added fields (green)
   - Removed fields (red)
   - Changed values (yellow, with old → new)
4. If changes detected:
   - Backs up current Firebase data to `theory_constants/history/backups/{timestamp}`
   - Updates `theory_constants/current` with new values
   - Updates `theory_constants/v{version}` with new values
   - Logs metadata: version, timestamp, simulation runs
5. If no changes: Reports "No changes detected" and exits

**Output Example**:
```
════════════════════════════════════════════════════════════════════════════════
  Firebase Sync with Version History
════════════════════════════════════════════════════════════════════════════════

[1/5] Initializing Firebase...
✓ Loaded theory-constants-enhanced.js
  Version: 12.7
  Simulations: 49

[2/5] Fetching current Firebase data...
✓ Fetched theory_constants/current
  Version: 12.7

[3/5] Computing differences...

Changes detected: 5

Summary:
  Added:   2
  Removed: 0
  Changed: 3

CHANGED (3):
  ~ proton_decay.M_GUT
    - 2.1e+16
    + 2.12e+16
  ~ pmns_matrix.theta_12
    - 33.41
    + 33.59
  ~ dark_energy.w0_PM
    - -0.83
    + -0.85

[4/5] Updating Firebase...
✓ Backed up to theory_constants/history/backups/2025-12-13_14-30-45
✓ Updated theory_constants/current
✓ Updated theory_constants/v12_7

════════════════════════════════════════════════════════════════════════════════
  ✅ Sync complete!
════════════════════════════════════════════════════════════════════════════════
  Changes applied: 5
  Version: 12.7
  Backup: theory_constants/history/backups/2025-12-13_14-30-45
```

### Integrated Scripts

The sync function is now integrated into:

#### 1. `firebase-upload-all.js`
- Uploads ALL data (theory constants, formulas, pages)
- Uses sync-with-history for theory constants
- Falls back to direct upload if sync fails

**Usage**:
```bash
node scripts/firebase-upload-all.js
node scripts/firebase-upload-all.js --force
```

#### 2. `firebase-push-validated.js`
- Full validation pipeline (OOM checks, derivation chains)
- Uses sync-with-history for the actual push
- Records validation results in `validation_history`

**Usage**:
```bash
node scripts/firebase-push-validated.js
node scripts/firebase-push-validated.js --force
```

## Data Structure

### Firebase Collections

```
theory_constants/
├── current                    # Latest version (synced)
├── enhanced                   # Enhanced constants
├── v12_7                      # Version-specific snapshot
├── v12_6                      # Previous versions...
└── history/
    └── backups/
        ├── 2025-12-13_14-30-45  # Timestamped backups
        ├── 2025-12-13_10-15-22
        └── ...
```

### Backup Document Structure

```javascript
{
  // All original data fields
  ...originalData,

  // Backup metadata
  backup_timestamp: "2025-12-13T14:30:45.123Z",
  backed_up_at: Timestamp,
  replaced_by_version: "12.7",
  metadata: {
    version: "12.6",
    simulations_run: [...],
    backup_reason: "automatic_sync"
  }
}
```

### Current Document Structure

```javascript
{
  // All PM data
  meta: { version, last_updated, simulations_run, ... },
  dimensions: { ... },
  topology: { ... },
  proton_decay: { ... },
  pmns_matrix: { ... },
  // ... all other theory data

  // Sync metadata
  syncedAt: Timestamp,
  sync_metadata: {
    previous_backup: "2025-12-13_14-30-45",
    version: "12.7",
    simulations_run: [...],
    last_updated: "2025-12-08"
  }
}
```

## Service Account Setup

The scripts look for Firebase service account keys in these locations (in order):

1. `scripts/serviceAccountKey.json`
2. `scripts/principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json`
3. `./principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json`
4. `./serviceAccountKey.json`

**To obtain a service account key**:
1. Go to Firebase Console
2. Project Settings > Service Accounts
3. Click "Generate new private key"
4. Save to one of the above locations

## Diff Algorithm

The diff algorithm:
- Recursively compares nested objects up to 20 levels deep
- Handles arrays, primitives, and objects
- Categorizes changes as: `added`, `removed`, `changed`
- Formats scientific notation for readability
- Limits display to prevent console spam (use `--force` for full output)

## Safety Features

1. **No data loss**: Current data always backed up before overwrite
2. **Change transparency**: See exactly what will change before push
3. **Idempotent**: Running multiple times with same data = no changes
4. **Fallback**: If sync fails, scripts fall back to direct upload
5. **Version tracking**: Every backup tagged with version and timestamp

## Rollback Process

To rollback to a previous version:

```javascript
// In Firebase Console or via script
const backupId = '2025-12-13_14-30-45';
const backup = await db.collection('theory_constants')
  .doc('history')
  .collection('backups')
  .doc(backupId)
  .get();

const backupData = backup.data();
delete backupData.backup_timestamp;
delete backupData.backed_up_at;
delete backupData.replaced_by_version;
delete backupData.metadata;

await db.collection('theory_constants')
  .doc('current')
  .set({
    ...backupData,
    restoredFrom: backupId,
    restoredAt: admin.firestore.FieldValue.serverTimestamp()
  });
```

## Best Practices

1. **Always run sync before making manual Firebase edits**
2. **Review diff output before confirming pushes**
3. **Keep service account key secure** (add to .gitignore)
4. **Use `--force` mode for detailed debugging**
5. **Check `validation_history` for push records**

## Troubleshooting

### "No changes detected" when you expect changes

- Check that you've updated `theory-constants-enhanced.js`
- Verify the file parses correctly (test with `node -e "require('./theory-constants-enhanced.js')"`)
- Make sure Firebase has existing data to compare against

### "Service account key not found"

- Download key from Firebase Console
- Save to one of the expected locations
- Make sure filename matches expectations

### Diff shows too many changes

- Use `--force` flag to see all changes
- Check if this is a major version update
- Verify you're not comparing completely different datasets

### Firestore depth limit errors

- The sync script automatically flattens deep nesting (max 15 levels)
- Very deep objects are stringified
- This is handled automatically

## Integration Example

To use the sync function in your own scripts:

```javascript
const { firebaseSyncWithHistory } = require('./firebase-sync-with-history.js');

async function myUploadScript() {
  // Sync theory constants with history
  const result = await firebaseSyncWithHistory();

  if (result.updated) {
    console.log(`Synced ${result.diffs} changes`);
    console.log(`Backup: ${result.backupId}`);
  } else {
    console.log('No changes to sync');
  }

  // Continue with other uploads...
}
```

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
