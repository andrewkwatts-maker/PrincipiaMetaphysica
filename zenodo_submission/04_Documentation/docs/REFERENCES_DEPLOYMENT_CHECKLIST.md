# References System Deployment Checklist

## Pre-Deployment

### 1. Verify Prerequisites
- [ ] Node.js installed (v16+ recommended)
- [ ] Firebase CLI installed (`npm install -g firebase-tools`)
- [ ] Firebase project initialized (`firebase init`)
- [ ] Service account key exists (`firebase-service-account.json`)
- [ ] Firebase authentication configured

### 2. Install Dependencies

```bash
npm install
```

This installs:
- `firebase-admin` - For server-side Firebase operations
- `jsdom` - For HTML parsing in migration script

## Deployment Steps

### Phase 1: Migration (Dry Run)

#### 1.1 Test Migration Script

```bash
npm run migrate-references-dry
```

**Expected Output**:
- Parses `references.html` successfully
- Extracts all reference metadata
- Shows preview of references to be uploaded
- Generates BibTeX for each reference
- **Does not upload to Firestore**

**Verify**:
- [ ] All references parsed correctly
- [ ] Citation keys generated (e.g., "Einstein 1915")
- [ ] BibTeX formatted properly
- [ ] Categories identified correctly
- [ ] No parsing errors

#### 1.2 Review Output

Check the dry run output for:
- [ ] Total references count matches expected (~50-80 references)
- [ ] All categories present
- [ ] No missing required fields
- [ ] DOI/arXiv links extracted correctly

### Phase 2: Migration (Production)

#### 2.1 Run Migration

```bash
npm run migrate-references
```

**Expected Output**:
```
╔═══════════════════════════════════════════════════════════╗
║   Principia Metaphysica - References Migration to Firebase   ║
╚═══════════════════════════════════════════════════════════╝

Found 13 reference categories

Processing category: foundational-physics - Foundational Physics
  ✓ Parsed: einstein1915 - Einstein 1915
  ✓ Parsed: hilbert1915 - Hilbert 1915
  ...

=== Uploading References to Firestore ===

Committing batch of 72 references...
✓ Successfully uploaded 72 references to Firestore

✓ Index configuration saved to firestore.indexes.json
Deploy with: firebase deploy --only firestore:indexes

✅ Migration completed successfully!
```

**Verify**:
- [ ] All references uploaded successfully
- [ ] No errors during batch commit
- [ ] Index config generated

#### 2.2 Verify in Firebase Console

1. Go to Firebase Console → Firestore Database
2. Navigate to `references` collection
3. Check:
   - [ ] All documents present
   - [ ] Sample reference has all required fields
   - [ ] `citation_key` field exists
   - [ ] `bibtex` field populated
   - [ ] `tags` array populated
   - [ ] Timestamps (`created_at`, `updated_at`) set

### Phase 3: Deploy Indexes

#### 3.1 Deploy Firestore Indexes

```bash
firebase deploy --only firestore:indexes
```

**Expected Output**:
```
=== Deploying to 'principia-metaphysica'...

i  firestore: reading indexes from firestore.indexes.json...
i  firestore: uploading rules firestore.indexes.json...
✔  firestore: deployed indexes in firestore.indexes.json successfully
```

**Verify**:
- [ ] Indexes deployment successful
- [ ] No errors or warnings

#### 3.2 Wait for Index Building

1. Go to Firebase Console → Firestore Database → Indexes
2. Check index status:
   - [ ] `category + year` → Building/Enabled
   - [ ] `type + year` → Building/Enabled
   - [ ] `citation_key` → Building/Enabled
   - [ ] `cited_in_formulas` → Building/Enabled
   - [ ] `cited_in_sections` → Building/Enabled
   - [ ] `tags` → Building/Enabled

**Note**: Index building may take 5-30 minutes depending on data size.

### Phase 4: Deploy Security Rules

#### 4.1 Review Security Rules

Check `firestore.rules` includes:

```javascript
match /references/{refId} {
  allow read: if isAuthenticated();
  allow write: if false;
}
```

#### 4.2 Deploy Rules

```bash
firebase deploy --only firestore:rules
```

**Expected Output**:
```
=== Deploying to 'principia-metaphysica'...

i  firestore: reading indexes from firestore.rules
✔  firestore: released rules firestore.rules to cloud.firestore
```

**Verify**:
- [ ] Rules deployment successful
- [ ] No syntax errors

### Phase 5: Testing

#### 5.1 Run Test Suite

```bash
npm run test-references
```

**Expected Output**:
```
╔═══════════════════════════════════════════════════════════╗
║     Principia Metaphysica - References Module Tests         ║
╚═══════════════════════════════════════════════════════════╝

📚 Test: Load All References
────────────────────────────────────────────────────────
✓ Loaded 72 references

References by category:
  foundational-physics: 3 references
  quantum-field-theory: 3 references
  geometry-topology: 8 references
  ...

🔍 Test: Load Reference by ID
────────────────────────────────────────────────────────
✓ einstein1915: Einstein 1915 - Die Feldgleichungen der Gravitation...
✓ joyce2000: Joyce 2000 - Compact Manifolds with Special Holonomy...
✓ acharya1998: Acharya 1998 - M Theory, Joyce Orbifolds and Super Yang-Mills...

...

═══════════════════════════════════════════════════════════
📊 TEST SUMMARY
═══════════════════════════════════════════════════════════

Tests Passed: 9/9

✅ All tests passed!
```

**Verify**:
- [ ] All 9 tests pass
- [ ] References load correctly
- [ ] Citation keys work
- [ ] BibTeX generated
- [ ] Data integrity >95%
- [ ] No errors

#### 5.2 Test in Browser

1. Open `examples/references-integration-example.html` in browser
2. Run each example:
   - [ ] Example 1: Load All References
   - [ ] Example 2: Load by Category
   - [ ] Example 3: Citation Key Lookup
   - [ ] Example 4: Inline Citations
   - [ ] Example 5: Full Reference Rendering
   - [ ] Example 6: BibTeX Export
   - [ ] Example 7: Search References
   - [ ] Example 8: Render All References

**Verify**:
- [ ] No console errors
- [ ] All examples work
- [ ] References display correctly
- [ ] BibTeX copy works
- [ ] Search returns results

### Phase 6: Integration

#### 6.1 Update references.html

Add to `<head>`:
```html
<script type="module" src="js/firebase-references.js"></script>
```

Add before `</body>`:
```html
<script type="module">
  import { initializeReferences, renderAllReferences } from './js/firebase-references.js';

  document.addEventListener('DOMContentLoaded', async () => {
    const container = document.querySelector('main');
    await initializeReferences();
    await renderAllReferences(container);
  });
</script>
```

**Test**:
- [ ] Load `references.html` in browser
- [ ] References render correctly
- [ ] All categories present
- [ ] BibTeX links work
- [ ] External links work

#### 6.2 Update principia-metaphysica-paper.html

For inline citations, add citation replacement logic:

```html
<script type="module">
  import { loadReferenceByCitation, renderInlineCitation } from './js/firebase-references.js';

  async function replaceCitations() {
    const citations = document.querySelectorAll('.citation-key');
    for (const el of citations) {
      const key = el.textContent.replace(/[\[\]]/g, '').trim();
      const ref = await loadReferenceByCitation(key);
      if (ref) {
        el.replaceWith(renderInlineCitation(ref));
      }
    }
  }

  document.addEventListener('DOMContentLoaded', replaceCitations);
</script>
```

**Test**:
- [ ] Citation keys replaced with links
- [ ] Links point to `references.html#refId`
- [ ] Hover shows reference title
- [ ] No broken citations

### Phase 7: Performance Validation

#### 7.1 Check Load Times

**references.html**:
- [ ] Initial load < 2 seconds
- [ ] Cached load < 100ms
- [ ] No layout shift

**Paper inline citations**:
- [ ] Citation replacement < 500ms
- [ ] No blocking on render
- [ ] Smooth user experience

#### 7.2 Check Cache

Open browser console:
```javascript
// Should log cache hit after 2nd load
await PMReferences.loadAllReferences();
// Check console: "[PM References] Returning cached references"
```

**Verify**:
- [ ] Cache working (10 min TTL)
- [ ] Cache invalidates after TTL
- [ ] Manual cache clear works

### Phase 8: Final Verification

#### 8.1 Production Checklist

- [ ] All references migrated
- [ ] All indexes deployed and enabled
- [ ] Security rules deployed
- [ ] Tests passing (9/9)
- [ ] Browser integration working
- [ ] Performance acceptable (<2s initial load)
- [ ] Cache functioning
- [ ] No console errors

#### 8.2 Data Quality

- [ ] Citation keys consistent format
- [ ] BibTeX properly formatted
- [ ] All DOI/arXiv links work
- [ ] Categories appropriate
- [ ] Tags descriptive
- [ ] Descriptions present where relevant

#### 8.3 Documentation

- [ ] Schema documentation complete
- [ ] README created
- [ ] Integration examples provided
- [ ] Deployment checklist complete (this file)
- [ ] API documentation available

## Post-Deployment

### Monitor Performance

Check Firebase Console → Analytics:
- [ ] References read count
- [ ] Average query time
- [ ] Error rate
- [ ] Cache hit rate

### Maintenance Tasks

Weekly:
- [ ] Review Firebase usage (stay within free tier)
- [ ] Check error logs

Monthly:
- [ ] Review reference citations (add to `cited_in_formulas`)
- [ ] Update outdated references
- [ ] Add new papers

Quarterly:
- [ ] Archive old references
- [ ] Update metadata
- [ ] Optimize indexes

## Rollback Procedure

If issues occur:

1. **Disable new system**:
   - Comment out Firebase references module
   - Restore static HTML references

2. **Revert security rules**:
   ```bash
   git checkout HEAD~1 firestore.rules
   firebase deploy --only firestore:rules
   ```

3. **Clear Firestore data** (if needed):
   ```bash
   # Delete references collection via Firebase Console
   # Or use Admin SDK script
   ```

4. **Investigate issues**:
   - Check console errors
   - Review deployment logs
   - Run test suite
   - Verify indexes enabled

## Success Criteria

The deployment is successful when:

✅ **All tests pass** (9/9)
✅ **References load in <2s**
✅ **Cache works** (10 min TTL)
✅ **No console errors**
✅ **BibTeX export works**
✅ **Inline citations work in paper**
✅ **Search returns results**
✅ **All indexes enabled**
✅ **Security rules active**
✅ **Documentation complete**

## Support

If you encounter issues:

1. Check troubleshooting section in `REFERENCES_SYSTEM_README.md`
2. Review error logs in Firebase Console
3. Run test suite to isolate issue
4. Check this deployment checklist
5. Contact: AndrewKWatts@Gmail.com

## Next Steps After Deployment

1. **Enhance citations**:
   - Add `cited_in_formulas` arrays to references
   - Link formulas to papers
   - Track citation usage

2. **Add features**:
   - Export to EndNote/Zotero
   - Citation graph visualization
   - Related papers suggestions

3. **Optimize**:
   - Add pagination for large lists
   - Implement full-text search (Algolia)
   - Add server-side caching

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Version**: 1.0.0
**Status**: [ ] Pending [ ] In Progress [ ] Complete

---

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
