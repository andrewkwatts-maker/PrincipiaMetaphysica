# Principia Metaphysica - Firebase Pipeline

## Overview

This document describes the complete Firebase integration for the Principia Metaphysica website, including:
- Single source of truth data management (ALL data in Firebase Firestore)
- Authentication flow (Google login required)
- Simulation-to-website pipeline
- Data validation and push workflow with MANDATORY confirmations

---

## Quick Start

### 1. Check Firebase Status
```batch
firebase-status.bat
```
Shows sync status between local files and Firebase.

### 2. Download Firebase Data
```batch
firebase-download.bat
```
Downloads all Firebase data to `firebase-backup/` folder for viewing.

### 3. Push Simulation Updates
```batch
firebase-push.bat
```
**MANDATORY CONFIRMATION REQUIRED:**
1. Displays complete OOM validation table
2. Displays complete diff of all changes
3. Requires 3 explicit Y/N confirmations:
   - [1/3] OOM Values Review
   - [2/3] Diff Changes Review
   - [3/3] Final Push Confirmation

Push will be BLOCKED if:
- Any OOM value fails validation
- Any value regresses from previous Firebase version

### 4. Full Pipeline (Simulation → Firebase → Website)
```batch
firebase-full-pipeline.bat
```
Runs complete pipeline:
1. Run all simulations
2. Generate constants
3. Validate OOM constraints
4. Push to Firebase (with mandatory confirmation)

---

## Firebase Configuration

### Project Details
- **Project ID**: `principia-metaphysica`
- **Auth Domain**: `principia-metaphysica.firebaseapp.com`
- **Console**: https://console.firebase.google.com/project/principia-metaphysica

### Required Setup

1. **Service Account Key**
   - Go to Firebase Console → Project Settings → Service Accounts
   - Generate New Private Key
   - Save as one of:
     - `scripts/serviceAccountKey.json` (recommended)
     - `scripts/principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json`
     - `principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json` (root)
   - **IMPORTANT**: These files are in `.gitignore` - NEVER commit them

2. **Firestore Security Rules**
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read: if request.auth != null;
         allow write: if false;
       }
     }
   }
   ```

3. **Enable Google Auth**
   - Firebase Console → Authentication → Sign-in method
   - Enable Google provider

---

## Single Source of Truth Architecture

**ALL website data is stored in Firebase Firestore.**

Pages cannot display content without:
1. User authentication (Google login)
2. Successful data load from Firestore

### Data Loading Flow
```
User visits page
       ↓
auth-guard.js shows login overlay
       ↓
User clicks "Login with Google"
       ↓
Firebase authentication
       ↓
Load theory_constants/current from Firestore
       ↓
Populate all .pm-value elements
       ↓
Initialize tooltips
       ↓
Show page content
       ↓
Dispatch 'pm-data-ready' event
```

---

## Firestore Collections

### `theory_constants`
Main source of truth for all physics constants.

| Document | Description |
|----------|-------------|
| `current` | Current version (always points to latest) |
| `v12_7` | Version 12.7 backup |
| `v12_7_1702500000000` | Timestamped backup |

Structure:
```json
{
  "meta": { "version": "12.7", "last_updated": "2025-12-08" },
  "dimensions": { "D_bulk": 26, "D_after_sp2r": 13, ... },
  "topology": { "b2": 4, "b3": 24, "chi_eff": 144, "n_gen": 3 },
  "proton_decay": { "M_GUT": 2.118e16, "tau_p_median": 3.87e34, ... },
  "pmns_matrix": { "theta_23": 45.0, "theta_12": 33.59, ... },
  "dark_energy": { "w0_PM": -0.8528, ... },
  "v12_7_pure_geometric": { ... },
  "validation": { "predictions_within_1sigma": 45, ... }
}
```

### `formulas`
All physics formulas with metadata.

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g., `einstein-field`) |
| `html` | HTML-safe equation string |
| `latex` | LaTeX version |
| `label` | Display name |
| `category` | ESTABLISHED, THEORY, DERIVED, PREDICTIONS |
| `description` | Plain English explanation |
| `terms` | Symbol definitions |
| `pm_constant` | Path to PM value if applicable |

### `pages`
Extracted page content for dynamic loading.

| Field | Description |
|-------|-------------|
| `id` | Page identifier (e.g., `sections-fermion-sector`) |
| `path` | Relative file path |
| `title` | Page title |
| `mainContent` | HTML content |
| `sections` | Array of section objects |
| `formulas` | Array of formula references |
| `pmValueRefs` | Array of PM value references |

### `validation_history`
Historical record of all data pushes.

| Field | Description |
|-------|-------------|
| `timestamp` | When pushed |
| `version` | PM version |
| `action` | push_update, initial_upload, etc. |
| `validation` | Validation results |
| `oom_validated` | Whether OOM validation passed |

---

## Pipeline Scripts

### Node.js Scripts (in `scripts/`)

| Script | Purpose |
|--------|---------|
| `firebase-check-status.js` | Check sync status |
| `firebase-download.js` | Download all data |
| `firebase-diff.js` | Compare local vs remote |
| `firebase-push-updates.js` | Validate and push (with confirmations) |
| `firebase-upload-all.js` | Initial full upload |
| `firebase-upload-website-content.js` | Upload HTML page content |
| `migrate-to-firestore.js` | Migrate from static files |
| `extract-page-content.js` | Extract HTML to Firestore |
| `upload-formula-database.js` | Upload formula definitions |

### BAT Files (in root)

| File | Purpose |
|------|---------|
| `firebase-status.bat` | Quick status check |
| `firebase-download.bat` | Download and view |
| `firebase-push.bat` | Validate and push (MANDATORY CONFIRMATIONS) |
| `firebase-full-pipeline.bat` | Complete simulation → website pipeline |

---

## OOM Validation

Before pushing updates, the system validates Order of Magnitude (OOM) constraints.

### Critical Parameters

| Parameter | Experimental | Tolerance | Description |
|-----------|--------------|-----------|-------------|
| M_GUT | 2×10¹⁶ GeV | 1 OOM | GUT Scale |
| τ_p | 1.67×10³⁴ years | 1 OOM | Proton Lifetime |
| m_KK | 5 TeV | 1 OOM | KK Graviton Mass |
| m_h | 125.1 GeV | 0.1 OOM | Higgs Mass |
| VEV | 174 GeV | 0.1 OOM | Vacuum Expectation Value |
| w₀ | -0.85 | 0.1 OOM | Dark Energy EoS |
| θ₂₃ | 45.0° | 0.05 OOM | PMNS Atmospheric Angle |
| θ₁₂ | 33.41° | 0.05 OOM | PMNS Solar Angle |
| θ₁₃ | 8.54° | 0.05 OOM | PMNS Reactor Angle |

### Push Blocking Conditions

Push will be **BLOCKED** if:
- ❌ Any value exceeds OOM tolerance from experimental
- ❌ Any value regresses (is worse than previous Firebase version)

Use `--force` flag to override (NOT RECOMMENDED).

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    SIMULATION LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  config.py → simulations/*.py → theory_output.json          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATION LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  firebase-push-updates.js                                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ STEP 1: Load local theory_output.json                   ││
│  │ STEP 2: Load Firebase theory_constants/current          ││
│  │ STEP 3: Display OOM validation table (MANDATORY)        ││
│  │ STEP 4: Display complete diff (MANDATORY)               ││
│  │ STEP 5: Display validation summary                      ││
│  │ STEP 6: Check for failures/regressions                  ││
│  │ STEP 7: Require 3 confirmations (Y/N)                   ││
│  │ STEP 8: Push to Firebase                                ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FIREBASE LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  Firestore Collections:                                      │
│  - theory_constants/current (SINGLE SOURCE OF TRUTH)         │
│  - theory_constants/v12_7_<timestamp> (version backup)       │
│  - formulas/*                                                │
│  - pages/*                                                   │
│  - validation_history/*                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEBSITE LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  User → Google Auth → Firebase Auth                          │
│       → Load theory_constants from Firestore                 │
│       → Populate PM values in HTML                           │
│       → Display page with live data                          │
│       → Dispatch 'pm-data-ready' event                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

1. User visits any page
2. `auth-guard.js` shows login overlay:
   ```
   ┌────────────────────────────────────────┐
   │         Principia Metaphysica          │
   │  Philosophiae Metaphysicae Principia   │
   │           Mathematica                  │
   │                                        │
   │      The Two-Time Framework            │
   │   A First-Principles Geometric Theory  │
   │                                        │
   │  A unified geometric framework...      │
   │                                        │
   │     [🔵 Login with Google]             │
   │                                        │
   │   Copyright © Andrew K Watts 2025      │
   └────────────────────────────────────────┘
   ```
3. User clicks "Login with Google"
4. Firebase popup authentication
5. On success:
   - Hide overlay, show content
   - Load `theory_constants/current` from Firestore
   - Populate all `.pm-value` elements with live data
   - Initialize tooltips
   - Make `window.PM` available globally
   - Dispatch `pm-data-ready` event

---

## Troubleshooting

### "Service account key not found"
The scripts check multiple locations:
1. `scripts/serviceAccountKey.json`
2. `scripts/principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json`
3. `principia-metaphysica-firebase-adminsdk-fbsvc-8cbaa9f520.json` (root)

Download from Firebase Console → Project Settings → Service Accounts

### "Permission denied" in Firestore
Check security rules allow authenticated reads

### "OOM validation failed"
Review simulation outputs - a value is outside expected range.
Check the OOM validation table for which parameter failed.

### "Push blocked: REGRESSED"
A value is worse than the previous Firebase version.
Review simulations to fix the regression before pushing.

### "Cannot read property 'version'"
theory_output.json may be malformed - re-run simulations

### Login popup blocked
Enable popups for the site, or try a different browser

---

## User Analytics Tracking

The system tracks user activity in Firebase collections (free tier compatible):

### Collections

| Collection | Description |
|------------|-------------|
| `users` | User profiles with login count |
| `user_sessions` | Login/logout events with timestamps |
| `page_views` | Page view events with user, page, timestamp |

### Tracked Events

1. **User Login**
   - User ID, email, display name
   - Login timestamp
   - Browser user agent
   - Screen dimensions

2. **Page Views**
   - User ID, page ID, URL
   - Page title
   - Timestamp
   - Session ID
   - Referrer

3. **User Logout**
   - User ID, timestamp

### Security

- All analytics data requires authentication to read/write
- Users can only see their own page view history
- Admin access to aggregate data via Firebase Console
- No sensitive data stored (only public profile info)

### Viewing Analytics

```batch
# Generate status report with analytics summary
node scripts/firebase-status-report.js

# View raw data in Firebase Console
# https://console.firebase.google.com/project/principia-metaphysica/firestore
```

---

## Dependencies

```bash
# Node.js packages
npm install firebase-admin cheerio

# Python packages (for simulations)
pip install numpy scipy
```

---

## File Structure

```
PrincipiaMetaphysica/
├── .gitignore                    # Excludes service account keys
├── firebase-status.bat           # Quick status check
├── firebase-download.bat         # Download Firebase data
├── firebase-push.bat             # Push with confirmations
├── firebase-full-pipeline.bat    # Full simulation pipeline
│
├── scripts/
│   ├── serviceAccountKey.json    # (gitignored) Firebase credentials
│   ├── firebase-check-status.js  # Status checker
│   ├── firebase-download.js      # Download tool
│   ├── firebase-diff.js          # Diff tool
│   ├── firebase-push-updates.js  # Push with validation
│   ├── firebase-upload-all.js    # Initial upload
│   └── firebase-upload-website-content.js  # HTML upload
│
├── js/
│   ├── firebase-config.js        # Firebase configuration
│   ├── firebase-auth.js          # Authentication module
│   ├── firebase-data.js          # Firestore data loader
│   ├── firebase-analytics.js     # User analytics tracking
│   ├── firebase-page-loader.js   # Page content loader
│   └── auth-guard.js             # Content protection + analytics
│
├── css/
│   └── auth.css                  # Login page styles
│
├── images/
│   ├── google-icon.svg           # Google login button
│   └── default-avatar.svg        # Default user avatar
│
└── firebase-backup/              # (gitignored) Downloaded data
    ├── theory_constants.json
    ├── formulas.json
    ├── pages.json
    └── metadata.json
```

---

## Next Steps After Initial Setup

1. **Install dependencies**
   ```bash
   npm install firebase-admin cheerio
   ```

2. **Place service account key**
   - Download from Firebase Console
   - Save to `scripts/serviceAccountKey.json`

3. **Initial data upload**
   ```bash
   node scripts/firebase-upload-all.js
   ```

4. **Upload website content**
   ```bash
   node scripts/firebase-upload-website-content.js
   ```

5. **Verify status**
   ```batch
   firebase-status.bat
   ```

6. **Test authentication flow**
   - Open website in browser
   - Verify login overlay appears
   - Login with Google
   - Verify content loads from Firebase

---

## Copyright

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Developed with assistance from Claude (Anthropic).
