#!/usr/bin/env python3
"""
Rename physics parameters to Hebrew Kabbalistic nomenclature (v12.9)

This script performs the following renames:

1. Warping constant:
   K_WARP, k_warp → K_GIMEL, k_gimel (k_ג)

2. Flux normalization (new parameter):
   C_FLUX → C_KAF (C_כ) [value: 27.2]

3. Partition divisor (new parameter):
   Already uses F_HEH (f_ה) [value: 4.5]

4. Instanton suppression:
   B_INSTANTON → S_MEM (S_מ) [value: 40]

5. Threshold correction (new parameter):
   Already uses DELTA_LAMED (δ_ל) [value: 1.2]

Display text updates:
- "warping constant" → "k_ג (Gimel warping)"
- "warp factor" → "brane localization factor"
"""

import os
import re
import glob

# Define replacement patterns
REPLACEMENTS = {
    # Python/JS variable names (case-sensitive)
    'K_WARP': 'K_GIMEL',
    'k_warp': 'k_gimel',
    'B_INSTANTON': 'S_MEM',
    'b_instanton': 's_mem',

    # Display in comments/docs
    'warping constant': 'Gimel warping constant (k_ג)',
    'warping parameter': 'Gimel warping parameter (k_ג)',
    'instanton action exponent': 'Mem instanton suppression (S_מ)',
}

# Context-aware replacements (regex)
CONTEXT_REPLACEMENTS = [
    # Update K_WARP references to k_gimel with Hebrew
    (r'K_WARP\s*=\s*12\.31', 'K_GIMEL = 12.31  # k_ג: Gimel bridges observable and shadow worlds'),
    # Update instanton references
    (r'B_INSTANTON\s*=\s*1\.0', 'S_MEM = 40.0  # S_מ: Mem seals heavy modes with instantons'),
]

# Files to skip
SKIP_PATTERNS = [
    '**/node_modules/**',
    '**/.git/**',
    '**/__pycache__/**',
    '**/*.pyc',
    '**/rename_to_hebrew_nomenclature.py',  # Don't modify this script
    '**/rename_alpha_to_shadow.py',  # Don't modify the other rename script
]

def should_skip(filepath):
    """Check if file should be skipped"""
    for pattern in SKIP_PATTERNS:
        if glob.fnmatch.fnmatch(filepath, pattern):
            return True
    # Skip binary files
    if filepath.endswith(('.png', '.jpg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot')):
        return True
    return False

def process_file(filepath):
    """Process a single file and apply replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        return 0

    original = content
    changes = 0

    # Apply simple replacements
    for old, new in REPLACEMENTS.items():
        if old in content:
            count_before = content.count(old)
            content = content.replace(old, new)
            changes += count_before

    # Apply regex replacements
    for pattern, replacement in CONTEXT_REPLACEMENTS:
        content, n = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
        changes += n

    # Write back if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes

    return 0

def main():
    """Main function to process all files"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    extensions = ['*.py', '*.js', '*.html', '*.json', '*.svg', '*.md']
    total_changes = 0
    files_changed = 0

    for ext in extensions:
        for filepath in glob.glob(os.path.join(base_dir, '**', ext), recursive=True):
            if should_skip(filepath):
                continue

            changes = process_file(filepath)
            if changes > 0:
                print(f"  {os.path.relpath(filepath, base_dir)}: {changes} changes")
                total_changes += changes
                files_changed += 1

    print(f"\nTotal: {total_changes} replacements in {files_changed} files")
    return total_changes

if __name__ == '__main__':
    # Write log to file to avoid Windows console encoding issues
    import sys
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rename_hebrew_log.txt')

    with open(log_path, 'w', encoding='utf-8') as log:
        log.write("Renaming to Hebrew Kabbalistic nomenclature (v12.9)...\n")
        log.write("K_WARP → K_GIMEL (k_ג), B_INSTANTON → S_MEM (S_מ)\n")
        log.write("=" * 60 + "\n")

    # Redirect print to log file
    class LogWriter:
        def __init__(self, log_path):
            self.log_path = log_path
        def write(self, text):
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(text)
        def flush(self):
            pass

    sys.stdout = LogWriter(log_path)
    total = main()

    # Print summary to console (ASCII only)
    sys.stdout = sys.__stdout__
    print(f"Rename complete. {total} replacements made.")
    print(f"Full log saved to: rename_hebrew_log.txt")
