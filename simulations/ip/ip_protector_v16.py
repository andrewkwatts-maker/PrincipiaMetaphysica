#!/usr/bin/env python3
"""
IP Protection and Citation Manager for Principia Metaphysica v16.2

This script adds copyright headers, citation information, and generates
protection manifests for all Python files in the project.

(c) 2025-2026 Andrew Keith Watts. All Rights Reserved.
Licensed under MIT via Principia Metaphysica v16.2
CITATION DOI: 10.5281/zenodo.18079602
Repository: https://github.com/andrewkwatts-maker/PrincipiaMetaphysica

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Copyright header template
COPYRIGHT_HEADER = """# (c) 2025-2026 Andrew Keith Watts. All Rights Reserved.
# Licensed under MIT via Principia Metaphysica v16.2
# CITATION DOI: 10.5281/zenodo.18079602
# Repository: https://github.com/andrewkwatts-maker/PrincipiaMetaphysica
"""

# Shebang patterns to preserve
SHEBANG_PATTERNS = ['#!/usr/bin/env python', '#!/usr/bin/python']


def calculate_checksum(file_path: str) -> str:
    """
    Calculate SHA-256 checksum for a file.

    Args:
        file_path: Path to the file

    Returns:
        Hexadecimal SHA-256 checksum string
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating checksum for {file_path}: {e}")
        return ""


def has_copyright_header(content: str) -> bool:
    """
    Check if file already has copyright header.

    Args:
        content: File content as string

    Returns:
        True if copyright header is present
    """
    return "Andrew Keith Watts. All Rights Reserved" in content and \
           "10.5281/zenodo.18079602" in content


def add_copyright_header(file_path: str, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Add copyright header to a Python file.

    Args:
        file_path: Path to the Python file
        dry_run: If True, don't actually modify files

    Returns:
        Tuple of (success, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if header already exists
        if has_copyright_header(content):
            return (True, "Already protected")

        lines = content.split('\n')

        # Check for shebang
        shebang_line = None
        start_index = 0
        if lines and any(lines[0].startswith(pattern) for pattern in SHEBANG_PATTERNS):
            shebang_line = lines[0]
            start_index = 1

        # Skip existing docstrings or comments at the top
        while start_index < len(lines) and (
            lines[start_index].strip().startswith('#') or
            lines[start_index].strip().startswith('"""') or
            lines[start_index].strip().startswith("'''") or
            lines[start_index].strip() == ''
        ):
            start_index += 1

        # Build new content
        new_lines = []

        # Add shebang if present
        if shebang_line:
            new_lines.append(shebang_line)

        # Add copyright header
        new_lines.append(COPYRIGHT_HEADER.rstrip())
        new_lines.append('')

        # Add rest of content
        new_lines.extend(lines[start_index:])

        new_content = '\n'.join(new_lines)

        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

        return (True, "Header added")

    except Exception as e:
        return (False, f"Error: {str(e)}")


def find_python_files(root_dir: str, exclude_dirs: List[str] = None) -> List[str]:
    """
    Find all Python files in directory tree.

    Args:
        root_dir: Root directory to search
        exclude_dirs: List of directory names to exclude

    Returns:
        List of Python file paths
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'venv', 'env', 'node_modules', '.vscode']

    python_files = []
    root_path = Path(root_dir)

    for path in root_path.rglob('*.py'):
        # Check if any excluded directory is in the path
        if not any(excluded in path.parts for excluded in exclude_dirs):
            python_files.append(str(path))

    return sorted(python_files)


def generate_manifest(files_info: List[Dict], output_path: str) -> None:
    """
    Generate JSON manifest of protected files.

    Args:
        files_info: List of file information dictionaries
        output_path: Path to save manifest
    """
    manifest = {
        "project": "Principia Metaphysica",
        "version": "16.2",
        "copyright": "(c) 2025-2026 Andrew Keith Watts. All Rights Reserved.",
        "license": "MIT",
        "doi": "10.5281/zenodo.18079602",
        "repository": "https://github.com/andrewkwatts-maker/PrincipiaMetaphysica",
        "generated": datetime.now().isoformat(),
        "total_files": len(files_info),
        "files": files_info
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest saved to: {output_path}")


def generate_protection_report(files_info: List[Dict], output_path: str) -> None:
    """
    Generate human-readable protection report.

    Args:
        files_info: List of file information dictionaries
        output_path: Path to save report
    """
    report_lines = [
        "=" * 80,
        "IP PROTECTION REPORT",
        "Principia Metaphysica v16.2",
        "=" * 80,
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Files Protected: {len(files_info)}",
        "",
        "Copyright: (c) 2025-2026 Andrew Keith Watts. All Rights Reserved.",
        "License: MIT via Principia Metaphysica v16.2",
        "CITATION DOI: 10.5281/zenodo.18079602",
        "Repository: https://github.com/andrewkwatts-maker/PrincipiaMetaphysica",
        "",
        "=" * 80,
        "PROTECTED FILES",
        "=" * 80,
        ""
    ]

    # Group by status
    added = [f for f in files_info if f['status'] == 'Header added']
    already_protected = [f for f in files_info if f['status'] == 'Already protected']
    errors = [f for f in files_info if f['status'].startswith('Error')]

    report_lines.append(f"\nNewly Protected: {len(added)}")
    report_lines.append("-" * 80)
    for file_info in added:
        report_lines.append(f"  {file_info['path']}")
        report_lines.append(f"    SHA-256: {file_info['checksum']}")

    report_lines.append(f"\nAlready Protected: {len(already_protected)}")
    report_lines.append("-" * 80)
    for file_info in already_protected:
        report_lines.append(f"  {file_info['path']}")
        report_lines.append(f"    SHA-256: {file_info['checksum']}")

    if errors:
        report_lines.append(f"\nErrors: {len(errors)}")
        report_lines.append("-" * 80)
        for file_info in errors:
            report_lines.append(f"  {file_info['path']}")
            report_lines.append(f"    {file_info['status']}")

    report_lines.append("\n" + "=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)

    report_content = '\n'.join(report_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Report saved to: {output_path}")


def protect_simulation_files(root_dir: str, dry_run: bool = False) -> None:
    """
    Apply copyright headers to all simulation Python files.

    Args:
        root_dir: Root directory containing simulation files
        dry_run: If True, don't actually modify files
    """
    print("=" * 80)
    print("Principia Metaphysica IP Protection System v16.2")
    print("=" * 80)
    print(f"\nRoot directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("\nSearching for Python files...")

    # Find all Python files
    python_files = find_python_files(root_dir)
    print(f"Found {len(python_files)} Python files")

    # Process each file
    files_info = []
    for i, file_path in enumerate(python_files, 1):
        print(f"\n[{i}/{len(python_files)}] Processing: {file_path}")

        # Add copyright header
        success, message = add_copyright_header(file_path, dry_run)

        # Calculate checksum (after modification if not dry run)
        checksum = calculate_checksum(file_path)

        # Store file info
        file_info = {
            "path": file_path,
            "relative_path": os.path.relpath(file_path, root_dir),
            "checksum": checksum,
            "status": message,
            "success": success,
            "processed_at": datetime.now().isoformat()
        }
        files_info.append(file_info)

        print(f"  Status: {message}")
        print(f"  Checksum: {checksum}")

    # Generate outputs
    if not dry_run:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create output directory if needed
        output_dir = os.path.join(root_dir, 'simulations', 'ip')
        os.makedirs(output_dir, exist_ok=True)

        # Generate manifest
        manifest_path = os.path.join(output_dir, f'protection_manifest_{timestamp}.json')
        generate_manifest(files_info, manifest_path)

        # Generate report
        report_path = os.path.join(output_dir, f'protection_report_{timestamp}.txt')
        generate_protection_report(files_info, report_path)

        print("\n" + "=" * 80)
        print("PROTECTION COMPLETE")
        print("=" * 80)
        print(f"\nTotal files processed: {len(files_info)}")
        print(f"Successfully protected: {sum(1 for f in files_info if f['success'])}")
        print(f"Errors: {sum(1 for f in files_info if not f['success'])}")
    else:
        print("\n" + "=" * 80)
        print("DRY RUN COMPLETE - No files were modified")
        print("=" * 80)


def verify_protection(manifest_path: str) -> None:
    """
    Verify file protection using a manifest.

    Args:
        manifest_path: Path to protection manifest JSON file
    """
    print("=" * 80)
    print("Verifying File Protection")
    print("=" * 80)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    print(f"\nManifest: {manifest_path}")
    print(f"Generated: {manifest['generated']}")
    print(f"Total files in manifest: {manifest['total_files']}")

    verification_results = []
    for file_info in manifest['files']:
        file_path = file_info['path']
        expected_checksum = file_info['checksum']

        if not os.path.exists(file_path):
            result = "MISSING"
            current_checksum = ""
        else:
            current_checksum = calculate_checksum(file_path)
            result = "OK" if current_checksum == expected_checksum else "MODIFIED"

        verification_results.append({
            "path": file_path,
            "expected_checksum": expected_checksum,
            "current_checksum": current_checksum,
            "result": result
        })

        print(f"\n{file_info['relative_path']}")
        print(f"  Status: {result}")
        if result != "OK":
            print(f"  Expected: {expected_checksum}")
            print(f"  Current:  {current_checksum}")

    # Summary
    ok_count = sum(1 for r in verification_results if r['result'] == 'OK')
    modified_count = sum(1 for r in verification_results if r['result'] == 'MODIFIED')
    missing_count = sum(1 for r in verification_results if r['result'] == 'MISSING')

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"OK: {ok_count}")
    print(f"Modified: {modified_count}")
    print(f"Missing: {missing_count}")


def main():
    """Main entry point for IP protection script."""
    import argparse

    parser = argparse.ArgumentParser(
        description='IP Protection System for Principia Metaphysica v16.2'
    )
    parser.add_argument(
        'command',
        choices=['protect', 'verify'],
        help='Command to execute'
    )
    parser.add_argument(
        '--root',
        default=os.getcwd(),
        help='Root directory to process (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run mode - do not modify files'
    )
    parser.add_argument(
        '--manifest',
        help='Path to manifest file (for verify command)'
    )

    args = parser.parse_args()

    if args.command == 'protect':
        protect_simulation_files(args.root, args.dry_run)
    elif args.command == 'verify':
        if not args.manifest:
            print("Error: --manifest required for verify command")
            return
        verify_protection(args.manifest)


if __name__ == '__main__':
    main()
