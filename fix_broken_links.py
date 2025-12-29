#!/usr/bin/env python3
"""
Automated Link Fixer for Principia Metaphysica
Fixes the most common broken link patterns identified in the audit
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

BASE_DIR = Path(r'h:\Github\PrincipiaMetaphysica')
BACKUP_DIR = BASE_DIR / f'backup_before_link_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

# Exclude patterns
EXCLUDE_PATTERNS = ['node_modules', '.git', 'zenodo_package', '__pycache__', 'backup_']

def should_exclude(path):
    """Check if path should be excluded"""
    path_str = str(path)
    return any(exclude in path_str for exclude in EXCLUDE_PATTERNS)

def find_html_files():
    """Find all HTML files to process"""
    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(excl in d for excl in EXCLUDE_PATTERNS)]

        for file in files:
            if file.endswith('.html'):
                file_path = Path(root) / file
                if not should_exclude(file_path):
                    html_files.append(file_path)

    return sorted(html_files)

def backup_file(file_path):
    """Create backup of file before modification"""
    backup_path = BACKUP_DIR / file_path.relative_to(BASE_DIR)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, backup_path)

def fix_root_html_references(content):
    """Fix references to HTML files that should be in Pages/"""
    fixes = []

    # Pattern 1: ../file.html -> ../Pages/file.html (from subdirectories)
    replacements = [
        (r'"\.\./paper\.html"', '"../Pages/paper.html"'),
        (r'"\.\./foundations\.html"', '"../Pages/foundations.html"'),
        (r'"\.\./sections\.html"', '"../Pages/sections.html"'),
        (r'"\.\./references\.html"', '"../Pages/references.html"'),
        (r'"\.\./beginners-guide\.html"', '"../Pages/beginners-guide.html"'),
        (r'"\.\./formulas\.html"', '"../Pages/formulas.html"'),
        (r'"\.\./parameters\.html"', '"../Pages/parameters.html"'),
        (r'"\.\./simulations\.html"', '"../Pages/simulations.html"'),
        (r'"\.\./appendices\.html"', '"../Pages/appendices.html"'),

        # Single quotes version
        (r"'\.\./paper\.html'", "'../Pages/paper.html'"),
        (r"'\.\./foundations\.html'", "'../Pages/foundations.html'"),
        (r"'\.\./sections\.html'", "'../Pages/sections.html'"),
        (r"'\.\./references\.html'", "'../Pages/references.html'"),
        (r"'\.\./beginners-guide\.html'", "'../Pages/beginners-guide.html'"),
    ]

    modified = content
    for pattern, replacement in replacements:
        count = len(re.findall(pattern, modified))
        if count > 0:
            modified = re.sub(pattern, replacement, modified)
            fixes.append(f"  - Fixed {count} instance(s) of {pattern} -> {replacement}")

    return modified, fixes

def fix_theory_constants_references(content):
    """Fix theory-constants-enhanced.js references"""
    fixes = []

    # Check if file exists in different locations
    possible_locations = [
        BASE_DIR / 'theory-constants-enhanced.js',
        BASE_DIR / 'Pages' / 'theory-constants-enhanced.js',
        BASE_DIR / 'js' / 'theory-constants-enhanced.js',
    ]

    correct_path = None
    for loc in possible_locations:
        if loc.exists():
            correct_path = loc
            break

    if correct_path:
        # Determine relative path based on where file actually is
        if 'Pages' in str(correct_path):
            new_ref = '../Pages/theory-constants-enhanced.js'
        elif 'js' in str(correct_path):
            new_ref = '../js/theory-constants-enhanced.js'
        else:
            new_ref = '../theory-constants-enhanced.js'

        pattern = r'"\.\./theory-constants-enhanced\.js"'
        count = len(re.findall(pattern, content))
        if count > 0:
            modified = re.sub(pattern, f'"{new_ref}"', content)
            fixes.append(f"  - Updated {count} theory-constants-enhanced.js reference(s)")
            return modified, fixes
    else:
        # File doesn't exist - comment out the script tag
        pattern = r'<script[^>]*src=["\']\.\.\/theory-constants-enhanced\.js["\'][^>]*></script>'
        count = len(re.findall(pattern, content))
        if count > 0:
            modified = re.sub(
                pattern,
                '<!-- COMMENTED OUT: theory-constants-enhanced.js not found\n'
                '     <script src="../theory-constants-enhanced.js"></script> -->',
                content
            )
            fixes.append(f"  - Commented out {count} missing theory-constants-enhanced.js reference(s)")
            return modified, fixes

    return content, fixes

def fix_section_html_links(content):
    """Convert section HTML file links to hash navigation"""
    fixes = []

    # Map section file names to their hash equivalents
    section_mappings = {
        'thermal-time': 'thermal-time',
        'fermion-sector': 'fermion-sector',
        'cosmology': 'cosmology',
        'gauge-unification': 'gauge-unification',
        'geometric-framework': 'geometric-framework',
        'index': 'all',  # sections/index.html -> sections.html#all
    }

    modified = content
    for filename, hash_name in section_mappings.items():
        # Pattern: ../sections/filename.html or ./sections/filename.html
        pattern = rf'["\']\.\.?/sections/{filename}\.html["\']'
        replacement = f'"../Pages/sections.html#{hash_name}"'

        count = len(re.findall(pattern, modified))
        if count > 0:
            modified = re.sub(pattern, replacement, modified)
            fixes.append(f"  - Converted {count} sections/{filename}.html -> sections.html#{hash_name}")

    return modified, fixes

def remove_einstein_field_equations_links(content):
    """Remove or comment out links to non-existent einstein-field-equations.html"""
    fixes = []

    # Check if file exists
    einstein_file = BASE_DIR / 'foundations' / 'einstein-field-equations.html'
    if not einstein_file.exists():
        # Comment out <a> tags linking to it
        pattern = r'<a\s+href=["\']einstein-field-equations\.html["\'][^>]*>(.*?)</a>'
        matches = re.findall(pattern, content)
        if matches:
            modified = re.sub(
                pattern,
                r'<!-- Link disabled: einstein-field-equations.html not found -->\1',
                content
            )
            fixes.append(f"  - Disabled {len(matches)} link(s) to einstein-field-equations.html")
            return modified, fixes

    return content, fixes

def fix_css_path_in_test(content, file_path):
    """Fix CSS path in test files"""
    fixes = []

    if 'tests' in str(file_path) and 'pm-tooltip.css' in content:
        pattern = r'href=["\']css/pm-tooltip\.css["\']'
        replacement = 'href="../css/pm-tooltip.css"'
        count = len(re.findall(pattern, content))
        if count > 0:
            modified = re.sub(pattern, replacement, content)
            fixes.append(f"  - Fixed {count} CSS path(s) in test file")
            return modified, fixes

    return content, fixes

def process_file(file_path):
    """Process a single HTML file and apply all fixes"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"

    content = original_content
    all_fixes = []

    # Apply all fix functions
    content, fixes = fix_root_html_references(content)
    all_fixes.extend(fixes)

    content, fixes = fix_theory_constants_references(content)
    all_fixes.extend(fixes)

    content, fixes = fix_section_html_links(content)
    all_fixes.extend(fixes)

    content, fixes = remove_einstein_field_equations_links(content)
    all_fixes.extend(fixes)

    content, fixes = fix_css_path_in_test(content, file_path)
    all_fixes.extend(fixes)

    # Only write if changes were made
    if content != original_content:
        # Backup original
        backup_file(file_path)

        # Write fixed content
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, all_fixes
        except Exception as e:
            return False, f"Error writing file: {e}"

    return False, []

def main():
    """Main execution"""
    print("=" * 80)
    print("AUTOMATED LINK FIXER FOR PRINCIPIA METAPHYSICA")
    print("=" * 80)
    print()

    # Create backup directory
    BACKUP_DIR.mkdir(exist_ok=True)
    print(f"Backups will be saved to: {BACKUP_DIR}")
    print()

    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files to process")
    print()

    files_modified = 0
    total_fixes = 0

    for file_path in html_files:
        rel_path = file_path.relative_to(BASE_DIR)

        modified, result = process_file(file_path)

        if modified:
            files_modified += 1
            fixes = result if isinstance(result, list) else []
            total_fixes += len(fixes)

            print(f"[MODIFIED] {rel_path}")
            for fix in fixes:
                print(fix)
            print()
        else:
            # Uncomment to see unmodified files
            # print(f"[NO CHANGE] {rel_path}")
            pass

    print("=" * 80)
    print(f"FIXING COMPLETE")
    print("=" * 80)
    print(f"Files modified: {files_modified}/{len(html_files)}")
    print(f"Total fixes applied: {total_fixes}")
    print(f"Backups saved to: {BACKUP_DIR}")
    print()
    print("Next steps:")
    print("1. Review changes with: git diff")
    print("2. Test the website locally")
    print("3. Run audit again: python audit_links.py")
    print("4. Commit changes if everything looks good")
    print()

    return files_modified

if __name__ == '__main__':
    modified_count = main()
    exit(0)
