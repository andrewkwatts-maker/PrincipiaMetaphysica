# Zenodo Upload Checklist for Principia Metaphysica v16.2

**DOI:** 10.5281/zenodo.18079602
**Date:** 2025-12-29 11:22:30
**Package:** PM_GUT_v16.2.zip
**Size:** 496.66 KB

## Pre-Upload Checklist

- [ ] Verify ZIP archive integrity
- [ ] Review all file checksums
- [ ] Confirm all required files are included
- [ ] Test extraction of ZIP archive
- [ ] Review package README
- [ ] Verify LICENSE file is included

## Upload Instructions

### Step 1: Access Zenodo
1. Go to https://zenodo.org
2. Log in to your account
3. Navigate to "Upload" -> "New Upload"

### Step 2: Upload File
1. Click "Choose files" or drag and drop
2. Upload: `PM_GUT_v16.2.zip`
3. Wait for upload to complete
4. Verify file size matches: 496.66 KB

### Step 3: Fill Metadata

**Basic Information:**
- **Upload type:** Publication → Article
- **Publication date:** 2025-12-29
- **Title:** Principia Metaphysica: A Unified Theory of Gravity, Gauge Forces, and Time
- **Authors:** Watts, Andrew Keith (add ORCID if available)
- **Description:**

```
Complete theoretical framework and computational implementation for Principia
Metaphysica v16.2, presenting a unified theory of gravity, gauge forces, and
time through higher-dimensional geometry. Includes 109 formulas, 58 parameters,
validation data, and interactive web interface.

Key features:
- 26D spacetime reducing to 4D via Sp(2,R) gauge projection and G2 compactification
- Predicts 3 fermion generations from χ_eff = 144
- Dark energy w₀ = -11/13 matching DESI 2024
- SO(10) grand unification with 3% coupling precision
- 88% parameter validation rate (51/58)
- 10 of 14 predictions within experimental bounds
```

**License & Access:**
- **License:** Other (Open) - specify custom license
- **Access right:** Open Access

**Communities:**
- [ ] Add to relevant communities (e.g., "Physics", "Theoretical Physics")

**Keywords:**
```
unified field theory
grand unified theory
higher-dimensional geometry
dark energy
SO(10) GUT
G2 manifold
extra dimensions
thermal time hypothesis
quantum gravity
cosmology
```

**Version:** v16.2

**Language:** English

**Related/alternate identifiers:**
- **Relation:** is supplement to
- **Identifier:** https://principiametaphysica.com
- **Relation:** is supplement to
- **Identifier:** https://github.com/andrewkwatts/PrincipiaMetaphysica

### Step 4: Reserve DOI
1. Click "Reserve DOI" (if creating new record)
2. Note the DOI: **10.5281/zenodo.18079602**
3. Verify DOI matches expected value

### Step 5: Save and Publish
1. Review all metadata fields
2. Click "Save" (draft)
3. Review preview
4. Click "Publish" when ready
5. **WARNING:** Publishing is irreversible!

## Post-Upload Checklist

- [ ] Verify DOI resolves correctly
- [ ] Check all files are accessible
- [ ] Download and verify checksums
- [ ] Test web interface files
- [ ] Update GitHub README with DOI badge
- [ ] Update website with Zenodo link
- [ ] Announce release (if applicable)

## Package Contents Summary

**Total Files:** 29
**Categories:**
- Documentation: README, LICENSE, CITATION
- Data: theory_output.json, formulas.json, parameters.json
- Code: config.py
- Web: HTML, JavaScript, CSS files
- Metadata: manifests and checksums

**File Breakdown:**
- Data: 7 files, 1.21 MB
- Documentation: 6 files, 384.40 KB
- Web: 16 files, 768.04 KB


## Verification Commands

**Verify ZIP integrity:**
```bash
unzip -t PM_GUT_v16.2.zip
```

**Extract and verify checksums:**
```bash
unzip PM_GUT_v16.2.zip
cd PM_GUT_v16.2
sha256sum -c metadata/CHECKSUMS.txt
```

## DOI Badge for README

Add this badge to your GitHub README:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18079602.svg)](https://doi.org/10.5281/zenodo.18079602)
```

## Citation

**BibTeX:**
```bibtex
@article{watts2025principia,
  title={Principia Metaphysica: A Unified Theory of Gravity, Gauge Forces, and Time},
  author={Watts, Andrew Keith},
  year={2025},
  version={v16.2},
  doi={10.5281/zenodo.18079602},
  url={https://doi.org/10.5281/zenodo.18079602},
  publisher={Zenodo}
}
```

**APA:**
```
Watts, A. K. (2025). Principia Metaphysica: A Unified Theory of Gravity,
Gauge Forces, and Time (Version v16.2). Zenodo.
https://doi.org/10.5281/zenodo.18079602
```

## Troubleshooting

**If upload fails:**
- Check file size limits (Zenodo max: 50GB per file)
- Verify internet connection
- Try uploading via API if web interface fails
- Contact Zenodo support if needed

**If DOI doesn't match:**
- You may need to request a specific DOI
- Contact Zenodo support with your preference
- Update all references after confirmation

## Contact Information

**For technical issues:**
- Zenodo Support: https://zenodo.org/support
- Email: support@zenodo.org

**For content questions:**
- Author: Andrew Keith Watts
- Email: AndrewKWatts@Gmail.com

## Notes

- Keep this checklist for your records
- Save Zenodo record URL once published
- Update all references to point to new DOI
- Archive this version in institutional repository if applicable

---

**Generated:** 2025-12-29 11:22:30
**Package Version:** v16.2
**Target DOI:** 10.5281/zenodo.18079602
