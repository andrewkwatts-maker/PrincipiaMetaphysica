# How to Update README with Zenodo DOI

## Quick Update (After Zenodo Upload)

Once you've uploaded to Zenodo and confirmed the DOI, update your README:

```bash
cd /h/Github/PrincipiaMetaphysica
mv README.md README_OLD_BACKUP.md
mv README_UPDATED.md README.md
git add README.md
git commit -m "Add Zenodo DOI badge and citation information"
git push
```

## What Changed

The updated README (`README_UPDATED.md`) includes:

### 1. Badges Section (New)
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18079602.svg)](https://doi.org/10.5281/zenodo.18079602)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v16.2-blue.svg)](https://github.com/andrewkwatts/PrincipiaMetaphysica/releases)
```

### 2. Citation Section (New)
Complete citation information in multiple formats:

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

**APA Style:**
```
Watts, A. K. (2025). Principia Metaphysica: A Unified Theory of Gravity,
Gauge Forces, and Time (Version v16.2). Zenodo.
https://doi.org/10.5281/zenodo.18079602
```

**Chicago Style:**
```
Watts, Andrew Keith. 2025. "Principia Metaphysica: A Unified Theory of
Gravity, Gauge Forces, and Time." Version v16.2. Zenodo.
https://doi.org/10.5281/zenodo.18079602.
```

**Plain Text:**
```
Watts, A. K. (2025). Principia Metaphysica: A Unified Theory of Gravity,
Gauge Forces, and Time (v16.2). Zenodo. DOI: 10.5281/zenodo.18079602
```

### 3. Links Section (Enhanced)
```markdown
## Links

- **Interactive Paper:** [https://principiametaphysica.com](https://principiametaphysica.com)
- **GitHub Repository:** [https://github.com/andrewkwatts/PrincipiaMetaphysica](https://github.com/andrewkwatts/PrincipiaMetaphysica)
- **Zenodo Archive:** [https://doi.org/10.5281/zenodo.18079602](https://doi.org/10.5281/zenodo.18079602)
```

## Manual Update (Alternative)

If you prefer to manually edit the current README:

### Step 1: Add Badges (after title)
Insert after "Philosophiæ Metaphysicæ Principia Mathematica":

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18079602.svg)](https://doi.org/10.5281/zenodo.18079602)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v16.2-blue.svg)](https://github.com/andrewkwatts/PrincipiaMetaphysica/releases)
```

### Step 2: Add Citation Section (before "Known Open Problems")
Insert a new section:

```markdown
---

## Citation

### Zenodo Archive

This work is archived on Zenodo with DOI: [10.5281/zenodo.18079602](https://doi.org/10.5281/zenodo.18079602)

### BibTeX

[... citation formats as shown above ...]

---
```

### Step 3: Add Links Section (at bottom, before Contact)
```markdown
## Links

- **Interactive Paper:** [https://principiametaphysica.com](https://principiametaphysica.com)
- **GitHub Repository:** [https://github.com/andrewkwatts/PrincipiaMetaphysica](https://github.com/andrewkwatts/PrincipiaMetaphysica)
- **Zenodo Archive:** [https://doi.org/10.5281/zenodo.18079602](https://doi.org/10.5281/zenodo.18079602)
```

## Verify Changes

After updating, verify the badges render correctly:

1. **Locally:**
   ```bash
   # View in VS Code preview or any Markdown viewer
   code README.md
   ```

2. **On GitHub:**
   - Push changes and check https://github.com/andrewkwatts/PrincipiaMetaphysica
   - Badges should appear with colors:
     - DOI badge: blue with "DOI" label
     - License badge: red with "Proprietary" label
     - Version badge: blue with "v16.2" label

3. **Click Badges:**
   - DOI badge → Should go to Zenodo record
   - License badge → Should go to LICENSE file
   - Version badge → Should go to releases page

## After Zenodo Upload

Once Zenodo upload is complete and DOI is confirmed:

1. **Update README** (as described above)
2. **Update website** (add Zenodo link)
3. **Update CITATION.cff** (if DOI changes)
4. **Create GitHub release** (tag v16.2)
5. **Update paper HTML** (add Zenodo reference)

## Rollback (if needed)

If you need to revert:

```bash
cd /h/Github/PrincipiaMetaphysica
mv README.md README_WITH_DOI.md
mv README_OLD_BACKUP.md README.md
git add README.md
git commit -m "Revert README changes"
git push
```

## Files Involved

- `README.md` - Current README (original)
- `README_UPDATED.md` - New README with DOI badge
- `README_OLD_BACKUP.md` - Backup of original (after update)

## Comparison

### Before (README.md)
```markdown
# Principia Metaphysica
Philosophiæ Metaphysicæ Principia Mathematica

## Abstract
[...]
```

### After (README_UPDATED.md)
```markdown
# Principia Metaphysica
Philosophiæ Metaphysicæ Principia Mathematica

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18079602.svg)](https://doi.org/10.5281/zenodo.18079602)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v16.2-blue.svg)](https://github.com/andrewkwatts/PrincipiaMetaphysica/releases)

## Abstract
[...]

---

## Citation

### Zenodo Archive
[...]
```

## Notes

- The DOI badge will only work after Zenodo upload is complete
- Badges use shields.io for rendering
- All links are absolute URLs for portability
- Citation formats follow standard academic styles
- Zenodo link goes directly to DOI (permanent)

## Questions?

- Check: ZENODO_UPLOAD_CHECKLIST.md
- Review: ZENODO_PACKAGE_CREATION_SUMMARY.md
- Contact: AndrewKWatts@Gmail.com
