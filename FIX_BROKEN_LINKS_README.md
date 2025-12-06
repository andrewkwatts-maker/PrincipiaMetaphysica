# Broken Links Fixer - Usage Guide

## Overview

`fix_broken_links.py` is an intelligent broken link analyzer and fixer for the PrincipiaMetaphysica project. It analyzes the 50 broken links identified in `centralization_validation_results.json` and proposes smart fixes with varying confidence levels.

## Analysis Results

Based on the latest analysis:

- **Total broken links**: 50 across 17 files
- **Auto-fixable (≥90% confidence)**: 15 links
- **Needs confirmation (50-89% confidence)**: 10 links
- **Manual review (<50% confidence)**: 25 links

### Fix Strategies Breakdown

| Strategy | Count | Description |
|----------|-------|-------------|
| **manual** | 25 | Existing anchors that validation incorrectly flagged as broken |
| **update_path** | 11 | Files moved to new locations (e.g., `docs/` folder) |
| **create_page** | 5 | Missing foundation pages that should exist |
| **remove_link** | 4 | Dead links to non-existent pages |
| **add_anchor** | 3 | Missing anchor IDs in existing files |
| **fix_typo** | 2 | Anchor name typos (e.g., `four-brane-structure` → `four_brane_structure`) |

## Installation

Requires Python 3.7+ with BeautifulSoup4:

```bash
pip install beautifulsoup4
```

## Usage

### 1. Dry Run (Safe Analysis Only)

Analyze all broken links without making any changes:

```bash
python fix_broken_links.py --dry-run
```

This generates `broken_links_fix_report.json` with detailed analysis.

### 2. Auto-Fix Safe Cases

Apply only high-confidence fixes (≥90%):

```bash
python fix_broken_links.py --auto-only --no-dry-run
```

This will fix:
- **11 path updates**: `beginners-guide-printable.html` → `docs/beginners-guide-printable.html`
- **4 dead link removals**: Remove links to non-existent pages
- **2 anchor typo fixes**: `four-brane-structure` → `four_brane_structure`

### 3. Interactive Mode

Review and approve each ambiguous fix:

```bash
python fix_broken_links.py --interactive --no-dry-run
```

You'll be prompted for:
- Missing pages to create (5 foundation pages)
- Missing anchors to add (3 reference anchors)

### 4. Apply All Fixes (Use with Caution!)

Apply all fixes automatically:

```bash
python fix_broken_links.py --apply-all --no-dry-run
```

⚠️ **Warning**: This includes fixing the 25 "manual" items that may actually be false positives!

## Command Line Options

```
--root-dir PATH           Project root directory (default: current)
--validation-file FILE    JSON validation results (default: centralization_validation_results.json)
--dry-run                 Don't make changes (default: True)
--no-dry-run              Actually apply changes to files
--interactive             Ask for confirmation on ambiguous fixes
--auto-only               Only apply high-confidence fixes
--apply-all               Apply all fixes (requires --no-dry-run)
--no-backup               Don't create .bak backup files
--report FILE             Output report filename (default: broken_links_fix_report.json)
```

## What Gets Fixed Automatically (Auto-Fixable)

### Path Updates (11 links)
All 9 instances of `beginners-guide-printable.html` → `docs/beginners-guide-printable.html`:
- `visualization-index.html` (9 instances)
- `beginners-guide.html` (1 instance)

Plus:
- `foundations/so10-gut.html`: `../sections/computational-appendices.html` → `../docs/computational-appendices.html`

### Dead Link Removal (4 links)
- `foundations/index.html`: Remove links to:
  - `dirac-lagrangian.html`
  - `generation-formula.html`
  - `thermal-time-relation.html`
- `foundations/tomita-takesaki.html`: Remove link to `quantum-foundations.html`

## What Needs Confirmation

### Pages to Create (5 links)
These foundation pages are referenced but don't exist:

1. **foundations/metric-tensor.html** - Linked from `einstein-hilbert-action.html`
2. **foundations/hawking-temperature.html** - Linked from `kms-condition.html`
3. **foundations/unruh-effect.html** - Linked from `kms-condition.html`
4. **foundations/dirac-spinor.html** - Linked from `dirac-equation.html`
5. **sections/dark-sector.html** - Linked from `fermion-sector.html`

### Anchors to Add (3 links)
These reference anchors are missing:

1. **references.html#g2-manifolds** - Add to `#geometry-topology` section
2. **references.html#calabi-yau** - Add to `#geometry-topology` section (exists as `yau1977`)
3. **sections/gauge-unification.html#symmetry-breaking** - Add section anchor

### Anchor Typo Fixes (2 links)
- `principia-metaphysica-paper.html#four-brane-structure` → `#four_brane_structure`
- Same fix in `sections/fermion-sector.html`

## Manual Review Items (25 links)

These are likely **false positives** where the validation tool incorrectly flagged them as broken:

### Existing Anchors (verified to exist):
- `index.html#abstract` ✓
- `index.html#sections` ✓
- `index.html#predictions` ✓
- `references.html#einstein1915` ✓
- `references.html#dirac1928` ✓
- `references.html#thermal-time` ✓
- `references.html#cosmology` ✓
- `references.html#neutrinos` ✓
- `references.html#grand-unification` ✓

**Recommendation**: These 25 "manual" items are probably validation errors and should NOT be modified. The anchors exist and links are valid.

## Report Structure

The generated `broken_links_fix_report.json` contains:

```json
{
  "timestamp": "2025-12-06T08:29:38",
  "dry_run": true,
  "summary": {
    "total_fixes_applied": 0,
    "total_manual_needed": 25,
    "total_pending": 0,
    "total_analyzed": 50
  },
  "all_fixes_analyzed": [
    {
      "source_file": "foundations\\index.html",
      "broken_link": "dirac-lagrangian.html",
      "strategy": "remove_link",
      "new_link": null,
      "reason": "Dead link - should be removed",
      "confidence": 0.9,
      "metadata": {}
    }
    // ... more fixes
  ],
  "fixes_applied": [],
  "fixes_manual": [],
  "fixes_pending": []
}
```

## Recommended Workflow

1. **Run dry-run analysis**:
   ```bash
   python fix_broken_links.py --dry-run
   ```

2. **Review the report**:
   ```bash
   # View broken_links_fix_report.json
   ```

3. **Apply safe fixes**:
   ```bash
   python fix_broken_links.py --auto-only --no-dry-run
   ```
   This fixes the 15 high-confidence items (path updates, dead links, typos).

4. **Address confirmations manually**:
   - Create the 5 missing foundation pages
   - Add the 3 missing anchor IDs
   - Or use interactive mode: `python fix_broken_links.py --interactive --no-dry-run`

5. **Ignore manual items**:
   The 25 "manual" items are likely validation false positives.

## Safety Features

- **Backups**: Creates `.bak` files before modifying (disable with `--no-backup`)
- **Dry-run default**: Must explicitly use `--no-dry-run` to make changes
- **Detailed logging**: All actions logged with timestamps
- **JSON report**: Full audit trail of all decisions
- **Preserves formatting**: Uses BeautifulSoup to maintain HTML structure

## Examples

### Example 1: Quick Fix
Apply only the safest fixes:
```bash
python fix_broken_links.py --auto-only --no-dry-run
```

### Example 2: Interactive Session
Review each ambiguous case:
```bash
python fix_broken_links.py --interactive --no-dry-run
```

### Example 3: Custom Report
Generate analysis with custom report name:
```bash
python fix_broken_links.py --dry-run --report my_analysis.json
```

## Troubleshooting

### "Link not found in file"
The HTML structure may have changed since validation. Re-run validation first.

### Unicode errors
Files must be UTF-8 encoded. The script handles this automatically.

### Path issues on Windows
Script uses `pathlib.Path` for cross-platform compatibility.

## Next Steps

After running the fixer:

1. **Test the website**: Verify all links work
2. **Re-run validation**: `python centralize_pm_constants.py --validate-links`
3. **Commit changes**: Git will show exact changes made
4. **Review .bak files**: Can restore if needed

## Technical Details

### How It Works

1. **Indexing**: Builds map of all HTML files in project
2. **Anchor Extraction**: Parses each file for `id` attributes using BeautifulSoup
3. **Path Resolution**: Resolves relative paths from source to target
4. **Strategy Selection**: Applies 6 different fix strategies based on confidence
5. **Application**: Modifies HTML files while preserving structure

### Confidence Levels

- **1.0 (100%)**: Known file moves, exact mappings
- **0.9 (90%)**: Known dead links, high-confidence removals
- **0.8 (80%)**: Fuzzy-matched anchors/filenames
- **0.7 (70%)**: Should-exist pages, similar filenames
- **0.5 (50%)**: Missing anchors to add
- **0.0 (0%)**: Manual review required

## License

Part of the PrincipiaMetaphysica project.
