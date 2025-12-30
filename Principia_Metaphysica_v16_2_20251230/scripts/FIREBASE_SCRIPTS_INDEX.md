# Firebase Scripts Index

## Quick Start

```bash
# Most common command - sync with diff and history
node scripts/firebase-helper.js sync

# Show all available commands
node scripts/firebase-helper.js help
```

## Files Created/Modified

### New Files (Created)

1. **`firebase-sync-with-history.js`** ⭐ PRIMARY SCRIPT
   - Smart sync with diff detection and version history
   - Reads `theory-constants-enhanced.js`
   - Compares against Firebase current data
   - Shows detailed diff (added/removed/changed)
   - Backs up to `theory_constants/history/backups/`
   - Only uploads if changes detected

2. **`firebase-helper.js`** 🎯 CONVENIENCE CLI
   - Wrapper for common operations
   - Commands: `sync`, `upload`, `validate`, `test`, `help`
   - Colored, user-friendly output

3. **`test-firebase-sync.js`** 🧪 TEST SUITE
   - Tests sync logic without Firebase connection
   - Verifies diff algorithm
   - Validates data loading
   - Safe to run anytime

4. **`FIREBASE_SYNC_README.md`** 📖 FULL DOCS
   - Complete technical documentation
   - API reference
   - Data structures
   - Rollback procedures

5. **`QUICK_START_FIREBASE_SYNC.md`** 🚀 QUICK GUIDE
   - TL;DR commands
   - Common scenarios
   - Troubleshooting table

6. **`FIREBASE_SYNC_SUMMARY.md`** 📝 IMPLEMENTATION
   - What was created
   - Technical details
   - Integration examples

7. **`README_FIREBASE.md`** 📚 COMPLETE GUIDE
   - Workflow examples
   - Setup instructions
   - Advanced usage
   - Security notes

8. **`FIREBASE_SCRIPTS_INDEX.md`** 📑 THIS FILE
   - Overview of all scripts
   - File organization

### Modified Files (Updated)

1. **`firebase-upload-all.js`** ✅
   - Now uses `syncWithHistory()` for theory constants
   - Fallback to direct upload if sync fails
   - Reports sync results

2. **`firebase-push-validated.js`** ✅
   - Integrated with sync-with-history
   - Records sync results in validation_history
   - Shows diff before validated push

## File Organization

```
scripts/
├── Primary Scripts (Use These)
│   ├── firebase-sync-with-history.js     ⭐ Smart sync with diff
│   ├── firebase-upload-all.js            📦 Full upload (all data)
│   ├── firebase-push-validated.js        ✅ Production push
│   ├── firebase-helper.js                🎯 CLI wrapper
│   └── test-firebase-sync.js             🧪 Local testing
│
├── Documentation
│   ├── README_FIREBASE.md                📚 Complete guide (START HERE)
│   ├── QUICK_START_FIREBASE_SYNC.md      🚀 Quick start
│   ├── FIREBASE_SYNC_README.md           📖 Full technical docs
│   ├── FIREBASE_SYNC_SUMMARY.md          📝 Implementation details
│   └── FIREBASE_SCRIPTS_INDEX.md         📑 This file
│
└── Legacy/Helper Scripts (Still Available)
    ├── firebase-diff.js                  Show diff only
    ├── firebase-download.js              Download from Firebase
    ├── firebase-check-status.js          Connection check
    ├── upload-formula-database.js        Formulas only
    └── upload-tooltip-database.js        Tooltips only
```

## Which Script to Use?

### Decision Tree

```
Are you updating theory values after simulations?
├─ Yes → node scripts/firebase-helper.js sync
└─ No
   └─ Are you doing a production release?
      ├─ Yes → node scripts/firebase-helper.js validate
      └─ No
         └─ Are you uploading ALL data (formulas, pages, etc.)?
            ├─ Yes → node scripts/firebase-helper.js upload
            └─ No
               └─ Are you testing/debugging?
                  ├─ Yes → node scripts/firebase-helper.js test
                  └─ No → node scripts/firebase-helper.js help
```

### Quick Reference

| Scenario | Command |
|----------|---------|
| Updated theory values | `node scripts/firebase-helper.js sync` |
| Production release | `node scripts/firebase-helper.js validate` |
| Full data upload | `node scripts/firebase-helper.js upload` |
| Testing locally | `node scripts/firebase-helper.js test` |
| Show help | `node scripts/firebase-helper.js help` |

## Features by Script

### firebase-sync-with-history.js

✅ Diff detection (shows what changed)
✅ Version history (automatic backups)
✅ No-change detection (idempotent)
✅ Colored output
✅ Safe rollback
✅ Metadata tracking
✅ Deep nesting handling

### firebase-upload-all.js

✅ Theory constants (via sync)
✅ Formulas upload
✅ Page content upload
✅ Validation history entry
✅ Chunk handling for large docs

### firebase-push-validated.js

✅ Derivation chain validation
✅ OOM accuracy checks
✅ Regression detection
✅ Diff display
✅ User confirmation
✅ Sync with history

### firebase-helper.js

✅ Simple CLI interface
✅ Runs other scripts
✅ Colored help output
✅ Error handling

### test-firebase-sync.js

✅ No Firebase connection needed
✅ Tests data loading
✅ Tests diff algorithm
✅ Tests no-change detection
✅ Tests deep nesting

## Common Workflows

### Workflow 1: Daily Development

```bash
# 1. Run simulations
python run_all_simulations.py

# 2. Sync to Firebase
node scripts/firebase-helper.js sync

# Expected: See diff of changes, auto-backup created
```

### Workflow 2: Production Release

```bash
# Full validation + sync
node scripts/firebase-helper.js validate

# Expected:
# - Derivation chain check
# - OOM validation
# - Diff display
# - Confirmation prompts
# - Sync with history
```

### Workflow 3: Testing Changes

```bash
# Test locally first
node scripts/firebase-helper.js test

# Then sync if tests pass
node scripts/firebase-helper.js sync
```

### Workflow 4: Full Upload (Rare)

```bash
# Upload everything
node scripts/firebase-helper.js upload

# Expected:
# - Theory constants synced
# - Formulas uploaded
# - Pages uploaded
# - Validation entry created
```

## Data Flow Overview

```
┌──────────────────────┐
│  config.py           │ ← Source of truth
└──────┬───────────────┘
       │
       v
┌──────────────────────┐
│  simulations         │
└──────┬───────────────┘
       │
       v
┌──────────────────────┐
│  theory_output.json  │
└──────┬───────────────┘
       │
       v
┌──────────────────────────────────────┐
│  theory-constants-enhanced.js        │ ← Single source for uploads
└──────┬───────────────────────────────┘
       │
       v
┌──────────────────────────────────────┐
│  firebase-sync-with-history.js       │
│  ├─ Load local                       │
│  ├─ Fetch Firebase                   │
│  ├─ Compute diff                     │
│  ├─ Backup current                   │
│  └─ Update if changes                │
└──────┬───────────────────────────────┘
       │
       v
┌──────────────────────────────────────┐
│  Firebase Firestore                  │
│  ├─ theory_constants/current         │
│  ├─ theory_constants/v12_7           │
│  └─ theory_constants/history/        │
│      └─ backups/{timestamp}          │
└──────────────────────────────────────┘
```

## Firebase Structure

```
theory_constants/
├── current                    ← Latest synced data
│   ├── meta
│   ├── dimensions
│   ├── proton_decay
│   ├── pmns_matrix
│   ├── syncedAt: Timestamp
│   └── sync_metadata
│
├── v12_7                      ← Version snapshots
├── v12_6
│
└── history/
    └── backups/
        ├── 2025-12-13_14-30-45
        │   ├── (all original data)
        │   ├── backup_timestamp
        │   └── replaced_by_version
        │
        ├── 2025-12-13_10-15-22
        └── ...
```

## Setup Checklist

- [ ] Download Firebase service account key
- [ ] Save to `scripts/serviceAccountKey.json` (or other location)
- [ ] Add `**/serviceAccountKey.json` to `.gitignore`
- [ ] Run `npm install firebase-admin`
- [ ] Test: `node scripts/firebase-helper.js test`
- [ ] First sync: `node scripts/firebase-helper.js sync`
- [ ] Verify in Firebase Console

## Troubleshooting Quick Fix

| Problem | Solution |
|---------|----------|
| "Service account key not found" | Download from Firebase Console, save to `scripts/serviceAccountKey.json` |
| "No changes detected" unexpectedly | Check `theory-constants-enhanced.js` was actually modified |
| Syntax errors | Run `node scripts/test-firebase-sync.js` to debug |
| Connection errors | Run `node scripts/firebase-check-status.js` |
| Want more details | Use `--force` flag: `node scripts/firebase-sync-with-history.js --force` |

## Documentation Guide

**Start here:**
1. `README_FIREBASE.md` - Complete guide

**For specific needs:**
- Quick start: `QUICK_START_FIREBASE_SYNC.md`
- Technical details: `FIREBASE_SYNC_README.md`
- Implementation: `FIREBASE_SYNC_SUMMARY.md`
- This index: `FIREBASE_SCRIPTS_INDEX.md`

## Best Practices

1. ✅ Always test locally first: `node scripts/firebase-helper.js test`
2. ✅ Review diff before confirming uploads
3. ✅ Use validated push for production: `node scripts/firebase-helper.js validate`
4. ✅ Keep service account key secure (add to .gitignore)
5. ✅ Check Firebase Console after uploads
6. ✅ Use `--force` for debugging detailed diffs

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

---

**Need help?** Run: `node scripts/firebase-helper.js help`
