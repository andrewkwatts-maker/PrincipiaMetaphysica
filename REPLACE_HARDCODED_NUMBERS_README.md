# Replace Hardcoded Numbers - Documentation

## Overview

`replace_hardcoded_numbers.py` is an automated tool that replaces hardcoded numeric values in HTML files with proper PM (Principia Metaphysica) value references. This ensures:

- **Single Source of Truth**: All values reference `theory_output.json`
- **Automatic Updates**: When theory values change, all HTML updates automatically
- **Hoverable Metadata**: Values become interactive with tooltips showing derivations
- **Consistency**: No more manually syncing numbers across files

## Features

### 1. Intelligent Number Extraction
- Loads all numeric values from `theory_output.json`
- Builds PM path references (e.g., `PM.proton_decay.M_GUT`)
- Indexes values by order of magnitude for fast lookup

### 2. Smart Matching Algorithms

#### Exact Match (Confidence: 1.0)
```python
# Matches with floating-point tolerance (1e-6)
12.5890655 → PM.shared_dimensions.d_eff
```

#### Scientific Notation Match (Confidence: 0.95)
```python
# Matches 2.118e16 to 2.1180954475766468e+16
2.118e16 → PM.proton_decay.M_GUT
```

#### Rounded Match (Confidence: 0.90)
```python
# Matches rounded versions
-0.85 → PM.shared_dimensions.w0_from_d_eff  # Full value: -0.8528228449557477
12.59 → PM.shared_dimensions.d_eff           # Full value: 12.5890655
```

#### Order of Magnitude Match (Confidence: 0.75)
```python
# Matches by OOM with 10% tolerance
144 → PM.topology.chi_eff
3 → PM.topology.n_gen
```

### 3. Smart Exclusions

The script automatically excludes:
- **Years**: 1900-2100 (e.g., 2024, 2025)
- **DOIs**: Pattern `10.xxxx/yyyy`
- **arXiv IDs**: Pattern `xxxx.xxxxx`
- **Page Numbers**: "pp. 123", "p. 45", "123-456"
- **Small Integers**: -10 to 10 (likely not physics values)
- **Already Tagged**: Numbers inside `<span data-category="...">` are skipped

### 4. Context-Aware Replacement

```html
<!-- Before -->
<p>The effective dimension is 12.589, yielding w₀ = -0.8528</p>

<!-- After -->
<p>The effective dimension is <span class="pm-value" data-category="shared_dimensions"
data-param="d_eff" data-format="fixed:3"></span>, yielding w₀ = <span class="pm-value"
data-category="shared_dimensions" data-param="w0_from_d_eff" data-format="fixed:4"></span></p>
```

### 5. Comprehensive Reporting

- **Unified Diffs**: See exactly what will change
- **Confidence Scores**: Each match has a confidence rating (0-1)
- **Match Types**: Know how each number was matched
- **JSON Audit Trail**: Complete record of all changes
- **Statistics**: Files scanned, replacements proposed/applied

## Installation

### Requirements
```bash
pip install beautifulsoup4
```

The script uses only standard library plus BeautifulSoup4.

## Usage

### Basic Examples

#### 1. Dry Run (Preview Only)
```bash
python replace_hardcoded_numbers.py --dry-run --files index.html
```

#### 2. Preview All HTML Files
```bash
python replace_hardcoded_numbers.py --dry-run --all-html
```

#### 3. Apply Changes with Confirmation
```bash
python replace_hardcoded_numbers.py --files index.html paper.html
```

#### 4. Auto-Apply All Changes
```bash
python replace_hardcoded_numbers.py --auto-apply --all-html
```

#### 5. Generate Detailed Report
```bash
python replace_hardcoded_numbers.py --dry-run --all-html --report report.json
```

#### 6. Show Unified Diffs
```bash
python replace_hardcoded_numbers.py --dry-run --files paper.html --show-diff
```

### Advanced Options

#### Custom Theory JSON Path
```bash
python replace_hardcoded_numbers.py --json custom_theory.json --files index.html
```

#### Adjust Confidence Threshold
```bash
# Only replace matches with ≥90% confidence
python replace_hardcoded_numbers.py --min-confidence 0.90 --all-html
```

#### Process Specific Files
```bash
python replace_hardcoded_numbers.py --files \
    index.html \
    principia-metaphysica-paper.html \
    beginners-guide.html
```

## Command-Line Reference

```
usage: replace_hardcoded_numbers.py [-h] [--json JSON]
                                    [--files FILES [FILES ...]]
                                    [--all-html]
                                    [--dry-run] [--auto-apply]
                                    [--report REPORT]
                                    [--min-confidence MIN_CONFIDENCE]
                                    [--show-diff]

Options:
  --json JSON              Path to theory_output.json (default: theory_output.json)
  --files FILES [...]      HTML files to process
  --all-html               Process all HTML files in current directory
  --dry-run                Preview changes without applying (default: True)
  --auto-apply             Automatically apply changes without confirmation
  --report REPORT          Output report to JSON file
  --min-confidence FLOAT   Minimum confidence threshold (0-1, default: 0.85)
  --show-diff              Show unified diff of changes
```

## Output Examples

### Console Output
```
================================================================================
REPLACEMENT SUMMARY
================================================================================

index.html: 151 replacements
  1. 26.0 -> PM.dimensions.D_bulk
     Type: exact, Confidence: 1.00
  2. 144 -> PM.topology.chi_eff
     Type: exact, Confidence: 1.00
  3. 2.118e16 -> PM.proton_decay.M_GUT
     Type: scientific, Confidence: 0.95
  4. -0.85 -> PM.shared_dimensions.w0_from_d_eff
     Type: rounded, Confidence: 0.88
  ... and 147 more

================================================================================
STATISTICS
================================================================================
Files scanned: 1
Total replacements proposed: 151
Replacements applied: 0 (dry run)
================================================================================
```

### JSON Report Structure
```json
{
  "timestamp": "2025-12-06T08:21:06.344482",
  "replacements": [
    {
      "file": "index.html",
      "original": "2.118e16",
      "replacement": "<span class=\"pm-value\" data-category=\"proton_decay\" data-param=\"M_GUT\" data-format=\"display\"></span>",
      "pm_path": "PM.proton_decay.M_GUT",
      "match_type": "scientific",
      "confidence": 0.95,
      "applied": false
    }
  ],
  "files_modified": [],
  "statistics": {
    "total_replacements": 151,
    "applied": 0,
    "files_scanned": 1,
    "files_modified": 0
  }
}
```

## Safety Features

### 1. Automatic Backups
Before modifying any file, the script creates a timestamped backup:
```
index.html.backup.20251206_082106
```

### 2. Dry Run Default
By default, the script runs in dry-run mode. You must explicitly use `--auto-apply` or confirm changes.

### 3. Skip Already Tagged Values
Numbers already inside `<span data-category="...">` are automatically skipped to avoid double-tagging.

### 4. Context Preservation
The script preserves:
- HTML structure
- Indentation
- Comments
- Special characters

### 5. Detailed Logging
All operations are logged to `replace_hardcoded_numbers.log`:
```
2025-12-06 08:21:06,310 - INFO - Extracted 106 numeric values from theory_output.json
2025-12-06 08:21:06,324 - INFO - Found 199 potential numbers in index.html
2025-12-06 08:21:06,344 - INFO - Dry run complete - no changes applied
```

## Workflow Recommendations

### Initial Setup (One-Time)

```bash
# 1. Test on a single file first
python replace_hardcoded_numbers.py --dry-run --files index.html --show-diff

# 2. Review the output carefully

# 3. Generate full report
python replace_hardcoded_numbers.py --dry-run --all-html --report full_analysis.json

# 4. Review the JSON report

# 5. Apply to one file
python replace_hardcoded_numbers.py --files index.html

# 6. Verify in browser

# 7. Apply to all files
python replace_hardcoded_numbers.py --auto-apply --all-html
```

### Regular Maintenance

```bash
# After updating theory_output.json:
python replace_hardcoded_numbers.py --dry-run --all-html --report update_$(date +%Y%m%d).json

# Review report, then apply:
python replace_hardcoded_numbers.py --auto-apply --all-html
```

## Matching Examples

### Physics Values

| Hardcoded | Matches | PM Path | Type |
|-----------|---------|---------|------|
| `144` | 144.0 | `PM.topology.chi_eff` | exact |
| `3` | 3.0 | `PM.topology.n_gen` | exact |
| `26` | 26.0 | `PM.dimensions.D_bulk` | exact |
| `12.589` | 12.5890655 | `PM.shared_dimensions.d_eff` | rounded |
| `-0.8528` | -0.8528228449557477 | `PM.shared_dimensions.w0_from_d_eff` | rounded |
| `2.118e16` | 2.1180954475766468e+16 | `PM.proton_decay.M_GUT` | scientific |
| `47.2` | 47.199999 | `PM.pmns_matrix.theta_23` | rounded |
| `23.54` | 23.538581563878598 | `PM.gauge_unification.alpha_GUT_inv` | rounded |

### Excluded Values (Not Replaced)

| Value | Reason |
|-------|--------|
| `2024` | Year (1900-2100) |
| `10.1103/PhysRevD.123.456` | DOI pattern |
| `2410.12627` | arXiv ID |
| `pp. 123-145` | Page numbers |
| `5` | Small integer (<10) |

## Troubleshooting

### Issue: Too Many False Positives

**Solution**: Increase confidence threshold
```bash
python replace_hardcoded_numbers.py --min-confidence 0.95 --files index.html
```

### Issue: Missing Expected Matches

**Solution**: Lower confidence threshold
```bash
python replace_hardcoded_numbers.py --min-confidence 0.75 --files index.html
```

### Issue: Wrong Values Being Matched

**Solution**: Review context in JSON report, manually exclude problematic numbers

### Issue: Unicode Errors on Windows

The script uses ASCII-safe arrow (`->`) instead of Unicode (`→`) for console output.

## Advanced Use Cases

### Custom Exclusion Patterns

Edit the `HTMLNumberScanner` class to add custom exclusion patterns:

```python
# In HTMLNumberScanner class
CUSTOM_PATTERN = re.compile(r'your_pattern_here')

def _should_exclude(self, number: float, text: str) -> bool:
    # Add custom exclusion logic
    if self.CUSTOM_PATTERN.search(text):
        return True
    # ... existing exclusions
```

### Custom Match Types

Add custom matching logic in `NumberMatcher`:

```python
def _try_custom_match(self, number: float, context: str) -> List[Match]:
    # Implement custom matching algorithm
    pass
```

### Formula Detection

The script can be extended to detect formulas and wrap entire expressions:

```python
# Detect MathJax/LaTeX environments
# Wrap formula instead of individual numbers
```

## Integration with Build Pipeline

```bash
#!/bin/bash
# pre-deploy.sh

# Update theory constants
python generate_enhanced_constants.py

# Replace hardcoded numbers
python replace_hardcoded_numbers.py --auto-apply --all-html --report deploy_report.json

# Validate HTML
python validate_pm_values.py

# Deploy
./deploy.sh
```

## Performance

- **Speed**: ~1-2 seconds per HTML file
- **Memory**: Minimal (loads entire JSON + HTML in memory)
- **Scalability**: Handles 100+ HTML files easily

## Version History

### v1.0 (2025-12-06)
- Initial release
- Exact, scientific, rounded, and magnitude matching
- Smart exclusions (years, DOIs, arXiv IDs)
- Backup creation
- JSON audit trails
- Dry-run mode
- Unified diff generation

## License

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

## Support

For issues or questions, contact: AndrewKWatts@Gmail.com
