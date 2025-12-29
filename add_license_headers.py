#!/usr/bin/env python3
"""
Script to add IP protection headers to all simulation files.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Standard copyright header for Python files
COPYRIGHT_HEADER = """# Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
# Licensed under the MIT License. See LICENSE file for details.
"""

DOCSTRING_COPYRIGHT = """Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

def check_file_has_copyright(content: str) -> Tuple[bool, bool]:
    """Check if file has copyright and license notice."""
    has_copyright = "Copyright (c) 2025-2026 Andrew Keith Watts" in content or \
                   "Copyright (c) 2025 Andrew Keith Watts" in content
    has_license = "Licensed under the MIT License" in content or \
                  "MIT License" in content
    return has_copyright, has_license

def update_python_file(filepath: Path) -> str:
    """Update a Python file with copyright header if needed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    has_copyright, has_license = check_file_has_copyright(content)

    # If already has both, return status
    if has_copyright and has_license:
        return "ALREADY_COMPLETE"

    # Check if file starts with shebang
    lines = content.split('\n')
    has_shebang = lines[0].startswith('#!')

    # Check if file has a docstring
    has_docstring = False
    docstring_start = -1
    docstring_end = -1

    if has_shebang:
        search_start = 1
    else:
        search_start = 0

    # Skip initial comments
    while search_start < len(lines) and (lines[search_start].strip() == '' or lines[search_start].strip().startswith('#')):
        search_start += 1

    if search_start < len(lines) and lines[search_start].strip().startswith('"""'):
        has_docstring = True
        docstring_start = search_start

        # Find end of docstring
        if lines[search_start].strip().count('"""') >= 2:
            # One-line docstring
            docstring_end = search_start
        else:
            # Multi-line docstring
            for i in range(search_start + 1, len(lines)):
                if '"""' in lines[i]:
                    docstring_end = i
                    break

    # Strategy: Add license reference to existing docstring if it has copyright but no license
    if has_docstring and has_copyright and not has_license:
        # Add license line after copyright in docstring
        new_lines = []
        added = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if docstring_start <= i <= docstring_end and not added:
                if "Copyright (c) 2025" in line and "Andrew Keith Watts" in line:
                    new_lines.append("Licensed under the MIT License. See LICENSE file for details.")
                    added = True

        if added:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            return "ADDED_LICENSE"

    # If no copyright at all, add complete header
    if not has_copyright:
        new_content = []

        if has_shebang:
            new_content.append(lines[0])
            new_content.append(COPYRIGHT_HEADER.rstrip())
            new_content.extend(lines[1:])
        else:
            new_content.append(COPYRIGHT_HEADER.rstrip())
            new_content.append(content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_content) if not has_shebang else '\n'.join(new_content))
        return "ADDED_COMPLETE"

    return "NO_CHANGE"

def update_config_file(filepath: Path) -> str:
    """Update config.py with MIT license header."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # config.py has a different copyright format - replace it
    old_copyright = '''"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""'''

    new_copyright = '''"""
Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""'''

    if old_copyright in content:
        content = content.replace(old_copyright, new_copyright)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return "UPDATED_TO_MIT"

    has_copyright, has_license = check_file_has_copyright(content)
    if has_copyright and has_license:
        return "ALREADY_COMPLETE"

    return "MANUAL_REVIEW_NEEDED"

def scan_and_update(root_dir: str) -> dict:
    """Scan and update all Python files."""
    results = {
        'already_complete': [],
        'added_license': [],
        'added_complete': [],
        'updated_to_mit': [],
        'no_change': [],
        'errors': []
    }

    # Patterns to include
    base_patterns = [
        'simulations/base/*.py',
        'simulations/v16/*/*.py',
        'simulations/v16/*/*/*.py',
    ]

    # Special files
    special_files = [
        'config.py',
        'run_all_simulations.py',
    ]

    root = Path(root_dir)

    # Process pattern-based files
    for pattern in base_patterns:
        for filepath in root.glob(pattern):
            if filepath.is_file():
                try:
                    status = update_python_file(filepath)
                    rel_path = filepath.relative_to(root)

                    if status == "ALREADY_COMPLETE":
                        results['already_complete'].append(str(rel_path))
                    elif status == "ADDED_LICENSE":
                        results['added_license'].append(str(rel_path))
                    elif status == "ADDED_COMPLETE":
                        results['added_complete'].append(str(rel_path))
                    elif status == "NO_CHANGE":
                        results['no_change'].append(str(rel_path))
                except Exception as e:
                    results['errors'].append(f"{filepath}: {str(e)}")

    # Process special files
    for filename in special_files:
        filepath = root / filename
        if filepath.exists():
            try:
                if filename == 'config.py':
                    status = update_config_file(filepath)
                else:
                    status = update_python_file(filepath)

                if status == "ALREADY_COMPLETE":
                    results['already_complete'].append(filename)
                elif status == "ADDED_LICENSE":
                    results['added_license'].append(filename)
                elif status == "ADDED_COMPLETE":
                    results['added_complete'].append(filename)
                elif status == "UPDATED_TO_MIT":
                    results['updated_to_mit'].append(filename)
                elif status == "NO_CHANGE":
                    results['no_change'].append(filename)
            except Exception as e:
                results['errors'].append(f"{filename}: {str(e)}")

    return results

def main():
    """Main execution."""
    repo_root = r"h:\Github\PrincipiaMetaphysica"

    print("Scanning and updating files...")
    print("=" * 70)

    results = scan_and_update(repo_root)

    print(f"\nAlready Complete: {len(results['already_complete'])} files")
    print(f"Added License Reference: {len(results['added_license'])} files")
    print(f"Added Complete Header: {len(results['added_complete'])} files")
    print(f"Updated to MIT: {len(results['updated_to_mit'])} files")
    print(f"No Change: {len(results['no_change'])} files")
    print(f"Errors: {len(results['errors'])} files")

    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")

    # Generate report
    report_path = Path(repo_root) / "IP_HEADERS_AUDIT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# IP Protection Headers Audit Report\n\n")
        f.write(f"**Generated:** {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Already Complete:** {len(results['already_complete'])} files\n")
        f.write(f"- **Added License Reference:** {len(results['added_license'])} files\n")
        f.write(f"- **Added Complete Header:** {len(results['added_complete'])} files\n")
        f.write(f"- **Updated to MIT License:** {len(results['updated_to_mit'])} files\n")
        f.write(f"- **No Change Needed:** {len(results['no_change'])} files\n")
        f.write(f"- **Errors:** {len(results['errors'])} files\n\n")

        f.write("## Files Already Complete\n\n")
        for file in sorted(results['already_complete']):
            f.write(f"- `{file}`\n")

        f.write("\n## Files Updated - License Reference Added\n\n")
        for file in sorted(results['added_license']):
            f.write(f"- `{file}`\n")

        f.write("\n## Files Updated - Complete Header Added\n\n")
        for file in sorted(results['added_complete']):
            f.write(f"- `{file}`\n")

        f.write("\n## Files Updated to MIT License\n\n")
        for file in sorted(results['updated_to_mit']):
            f.write(f"- `{file}`\n")

        if results['errors']:
            f.write("\n## Errors\n\n")
            for error in results['errors']:
                f.write(f"- {error}\n")

        f.write("\n## Copyright Header Format\n\n")
        f.write("All Python files now include:\n\n")
        f.write("```python\n")
        f.write(COPYRIGHT_HEADER)
        f.write("```\n\n")
        f.write("Or within docstrings:\n\n")
        f.write("```python\n")
        f.write('"""\n')
        f.write(DOCSTRING_COPYRIGHT)
        f.write('"""\n')
        f.write("```\n\n")
        f.write("## License File\n\n")
        f.write("MIT License file created at repository root: `LICENSE`\n")

    print(f"\nReport generated: {report_path}")

if __name__ == "__main__":
    main()
