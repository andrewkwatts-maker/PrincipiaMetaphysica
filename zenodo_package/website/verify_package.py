#!/usr/bin/env python3
"""
Verify the integrity of the Zenodo website package.
Checks all files against the manifest checksums.
"""

import json
import hashlib
import sys
from pathlib import Path


def calculate_sha256(file_path):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_package():
    """Verify all files in the package against the manifest."""
    package_dir = Path(__file__).parent
    manifest_path = package_dir / "website_manifest.json"

    if not manifest_path.exists():
        print("ERROR: website_manifest.json not found!")
        return False

    print("Zenodo Website Package Verification")
    print("=" * 70)
    print()

    # Load manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    print(f"Package: {manifest['package_name']}")
    print(f"Version: {manifest['package_version']}")
    print(f"Created: {manifest['created']}")
    print(f"Total Files: {manifest['summary']['total_files']}")
    print(f"Total Size: {manifest['summary']['total_size_mb']} MB")
    print()
    print("Verifying file integrity...")
    print()

    errors = []
    warnings = []
    verified = 0

    for file_info in manifest['files']:
        file_path = package_dir / file_info['path']
        expected_checksum = file_info['sha256']
        expected_size = file_info['size']

        # Check if file exists
        if not file_path.exists():
            errors.append(f"MISSING: {file_info['path']}")
            continue

        # Check file size
        actual_size = file_path.stat().st_size
        if actual_size != expected_size:
            warnings.append(
                f"SIZE MISMATCH: {file_info['path']} "
                f"(expected {expected_size}, got {actual_size})"
            )

        # Calculate and verify checksum
        actual_checksum = calculate_sha256(file_path)
        if actual_checksum != expected_checksum:
            errors.append(
                f"CHECKSUM MISMATCH: {file_info['path']}\n"
                f"  Expected: {expected_checksum}\n"
                f"  Actual:   {actual_checksum}"
            )
        else:
            verified += 1
            print(f"[OK] {file_info['path']}")

    print()
    print("=" * 70)
    print("Verification Results:")
    print(f"  Verified: {verified}/{manifest['summary']['total_files']} files")

    if warnings:
        print(f"  Warnings: {len(warnings)}")
        for warning in warnings:
            print(f"    - {warning}")

    if errors:
        print(f"  Errors: {len(errors)}")
        for error in errors:
            print(f"    - {error}")
        print()
        print("VERIFICATION FAILED!")
        return False
    else:
        print()
        print("ALL FILES VERIFIED SUCCESSFULLY!")
        print("Package is ready for Zenodo upload.")
        return True


if __name__ == "__main__":
    success = verify_package()
    sys.exit(0 if success else 1)
