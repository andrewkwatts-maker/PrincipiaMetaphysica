#!/usr/bin/env python3
"""
Apply enhanced validation_summary to theory_output.json
"""

import json
from pathlib import Path
import shutil

# Load enhanced validation summary
with open('validation_summary_enhanced.json', 'r', encoding='utf-8') as f:
    new_validation_summary = json.load(f)

# Load theory_output.json
theory_path = Path('theory_output.json')
with open(theory_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Backup original file
backup_path = theory_path.with_suffix('.json.backup')
shutil.copy2(theory_path, backup_path)
print(f"Backup created: {backup_path}")

# Replace validation_summary
old_count = len(data.get('validation_summary', []))
data['validation_summary'] = new_validation_summary
new_count = len(new_validation_summary)

print(f"\nReplacing validation_summary:")
print(f"  Old format: {old_count} entries (simplified array format)")
print(f"  New format: {new_count} entries (enhanced object format)")

# Save updated theory_output.json
with open(theory_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nUpdated theory_output.json saved")

# Show summary statistics
status_counts = {}
with_data = 0
without_data = 0

for entry in new_validation_summary:
    status = entry['status']
    status_counts[status] = status_counts.get(status, 0) + 1

    if entry['computed'] is not None:
        with_data += 1
    else:
        without_data += 1

print(f"\nValidation Summary Statistics:")
print(f"  Total entries: {new_count}")
print(f"\n  Status distribution:")
for status in ['PASS', 'CHECK', 'ERROR', 'FAIL']:
    count = status_counts.get(status, 0)
    if count > 0:
        pct = 100.0 * count / new_count
        print(f"    {status}: {count} ({pct:.1f}%)")

print(f"\n  Data completeness:")
print(f"    With computed values: {with_data} ({100.0*with_data/new_count:.1f}%)")
print(f"    Without computed values: {without_data} ({100.0*without_data/new_count:.1f}%)")

# List entries with full data
entries_with_full_data = [
    e for e in new_validation_summary
    if e['computed'] is not None and e['experimental'] is not None
]

print(f"\n  Entries with full quantitative data: {len(entries_with_full_data)}")
for entry in entries_with_full_data:
    print(f"    - {entry['name']}")

print(f"\n✓ Validation summary successfully updated!")
print(f"  Format: Array → Object with metadata")
print(f"  Backup: {backup_path}")
