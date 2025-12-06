# Quick Start Guide - Replace Hardcoded Numbers

## TL;DR

Replace hardcoded numbers in HTML files with PM value references in 3 steps:

```bash
# 1. Preview changes
python replace_hardcoded_numbers.py --dry-run --files index.html

# 2. Review output

# 3. Apply changes
python replace_hardcoded_numbers.py --files index.html
```

## Common Commands

### Preview Changes (Recommended First)
```bash
# Single file
python replace_hardcoded_numbers.py --dry-run --files index.html

# All HTML files
python replace_hardcoded_numbers.py --dry-run --all-html

# With detailed diff
python replace_hardcoded_numbers.py --dry-run --files paper.html --show-diff
```

### Apply Changes
```bash
# With confirmation prompt
python replace_hardcoded_numbers.py --files index.html paper.html

# Auto-apply (no confirmation)
python replace_hardcoded_numbers.py --auto-apply --all-html
```

### Generate Reports
```bash
# JSON audit trail
python replace_hardcoded_numbers.py --dry-run --all-html --report analysis.json
```

## What It Does

### Before
```html
<p>The framework predicts exactly 3 generations from χ_eff = 144.</p>
<p>The proton lifetime is 3.83×10³⁴ years.</p>
<p>Dark energy: w₀ = -0.8528</p>
```

### After
```html
<p>The framework predicts exactly <span class="pm-value" data-category="topology"
data-param="n_gen" data-format="display"></span> generations from χ_eff =
<span class="pm-value" data-category="topology" data-param="chi_eff"
data-format="display"></span>.</p>

<p>The proton lifetime is <span class="pm-value" data-category="proton_decay"
data-param="tau_p_median" data-format="display"></span> years.</p>

<p>Dark energy: w₀ = <span class="pm-value" data-category="shared_dimensions"
data-param="w0_from_d_eff" data-format="fixed:4"></span></p>
```

## What Gets Replaced

✅ **Replaced**:
- Physics values: `144`, `3`, `26`, `12.589`
- Negative numbers: `-0.8528`, `-0.83`
- Scientific notation: `2.118e16`, `3.83e34`
- Decimals: `47.2`, `23.54`, `0.955732`

❌ **NOT Replaced**:
- Years: `2024`, `2025`, `1900-2100`
- DOIs: `10.1103/PhysRevD.123.456`
- arXiv IDs: `2410.12627`
- Page numbers: `pp. 123-145`
- Small integers: `-9` to `9`
- Already tagged: `<span data-category="...">`

## Example Output

```
================================================================================
REPLACEMENT SUMMARY
================================================================================

index.html: 151 replacements
  1. 144 -> PM.topology.chi_eff
     Type: exact, Confidence: 1.00

  2. 3 -> PM.topology.n_gen
     Type: exact, Confidence: 1.00

  3. 2.118e16 -> PM.proton_decay.M_GUT
     Type: scientific, Confidence: 0.95

  4. -0.8528 -> PM.shared_dimensions.w0_from_d_eff
     Type: rounded, Confidence: 0.88

  ... and 147 more

================================================================================
STATISTICS
================================================================================
Files scanned: 1
Total replacements proposed: 151
================================================================================
```

## Safety Features

1. **Dry Run Default**: Always previews before applying
2. **Automatic Backups**: Creates `.backup.TIMESTAMP` files
3. **Skip Already Tagged**: Won't double-tag existing PM values
4. **Detailed Logging**: All operations logged to `replace_hardcoded_numbers.log`

## Confidence Levels

- **1.00 (Exact)**: Perfect match with floating-point tolerance
- **0.95 (Scientific)**: Scientific notation match (2.118e16 ≈ 2.1180954e16)
- **0.90 (Rounded)**: Rounded version match (12.59 ≈ 12.5890655)
- **0.75 (Magnitude)**: Order of magnitude match (within 10%)

Default minimum: **0.85** (excludes low-confidence matches)

## Troubleshooting

### "Too many replacements"
Increase confidence threshold:
```bash
python replace_hardcoded_numbers.py --min-confidence 0.95 --files index.html
```

### "Missing some numbers"
Lower confidence threshold:
```bash
python replace_hardcoded_numbers.py --min-confidence 0.75 --files index.html
```

### "Wrong number matched"
Review the JSON report to see context:
```bash
python replace_hardcoded_numbers.py --dry-run --files index.html --report review.json
```

## Full Workflow

```bash
# Step 1: Test on one file
python replace_hardcoded_numbers.py --dry-run --files index.html --show-diff

# Step 2: Generate full report
python replace_hardcoded_numbers.py --dry-run --all-html --report full_analysis.json

# Step 3: Review report file
cat full_analysis.json | head -50

# Step 4: Apply to one file (test)
python replace_hardcoded_numbers.py --files index.html

# Step 5: Check in browser
# Open index.html and verify values are correct

# Step 6: Apply to all files
python replace_hardcoded_numbers.py --auto-apply --all-html

# Step 7: Commit changes
git add *.html
git commit -m "Replace hardcoded numbers with PM value references"
```

## Help

```bash
python replace_hardcoded_numbers.py --help
```

For full documentation, see [REPLACE_HARDCODED_NUMBERS_README.md](REPLACE_HARDCODED_NUMBERS_README.md)
