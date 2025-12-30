#!/usr/bin/env python3
"""
Rename alpha_4/alpha_5 to Shadow_ק/Shadow_ח (Sitra Shadow Coupling)

This script performs the following renames:
- Python/JS variables: alpha_4 → shadow_kuf, alpha_5 → shadow_chet
- Display text: α₄ → Shadow_ק, α₅ → Shadow_ח
- Collective term: "alpha parameters" → "Sitra Shadow Coupling"
"""

import os
import re
import glob

# Define replacement patterns
REPLACEMENTS = {
    # Python/JS variable names (case-sensitive)
    'alpha_4': 'shadow_kuf',
    'alpha_5': 'shadow_chet',
    'ALPHA_4': 'SHADOW_KUF',
    'ALPHA_5': 'SHADOW_CHET',

    # Display symbols (Unicode)
    'α₄': 'Shadow_ק',
    'α₅': 'Shadow_ח',

    # HTML subscript versions
    'α<sub>4</sub>': 'Shadow<sub>ק</sub>',
    'α<sub>5</sub>': 'Shadow<sub>ח</sub>',
    'alpha<sub>4</sub>': 'Shadow<sub>ק</sub>',
    'alpha<sub>5</sub>': 'Shadow<sub>ח</sub>',

    # Category/section names
    'alpha_parameters': 'sitra_shadow_coupling',
    'Alpha Parameters': 'Sitra Shadow Coupling',
    'alpha parameters': 'Sitra Shadow Coupling',
}

# Additional context-aware replacements
CONTEXT_REPLACEMENTS = [
    # Add Sitra terminology to descriptions
    (r'shared extra dimension couplings?', 'Sitra Shadow Coupling'),
    (r'torsion-based coupling', 'Sitra Shadow Coupling'),
]

# Files to skip
SKIP_PATTERNS = [
    '**/node_modules/**',
    '**/.git/**',
    '**/__pycache__/**',
    '**/*.pyc',
    '**/rename_alpha_to_shadow.py',  # Don't modify this script
]

def should_skip(filepath):
    """Check if file should be skipped"""
    for pattern in SKIP_PATTERNS:
        if glob.fnmatch.fnmatch(filepath, pattern):
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
            content = content.replace(old, new)
            changes += content.count(new) - original.count(new)

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
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rename_log.txt')

    with open(log_path, 'w', encoding='utf-8') as log:
        log.write("Renaming alpha_4/alpha_5 to Shadow_ק/Shadow_ח (Sitra Shadow Coupling)...\n")
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
    print(f"Full log saved to: rename_log.txt")
