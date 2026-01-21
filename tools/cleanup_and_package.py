#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA - Repository Packaging Script
====================================================

Creates clean, OFFLINE packages for distribution by:
1. Cloning a fresh copy of the repository
2. Removing .git, __pycache__, and other dev files
3. STRIPPING Firebase/Auth dependencies for offline use
4. Generating SHA-256 checksums

Usage:
    python tools/cleanup_and_package.py [options]

Options:
    --local     Use current repo instead of fresh clone (for testing)
    --full      Also create _FULL package (identical, for compatibility)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import os
import sys
import re
import shutil
import stat
import zipfile
import hashlib
import subprocess
import tempfile
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional


def _remove_readonly(func, path, excinfo):
    """Error handler for shutil.rmtree on Windows read-only files."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


# ============================================================
# CONFIGURATION
# ============================================================

REPO_URL = "https://github.com/andrewkwatts-maker/PrincipiaMetaphysica.git"
REPO_BRANCH = "main"
VERSION = "23.0"

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent

# Folders to remove from package
EXCLUDE_FOLDERS = [
    ".git",
    ".github",
    ".claude",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "zenodo_submission",
    "zenodo_submission_FULL",
    "zenodo_package",
]

# Files/patterns to remove
EXCLUDE_PATTERNS = [
    "*.pyc",
    "*.pyo",
    ".env*",
    ".DS_Store",
    "Thumbs.db",
    "nul",  # Windows reserved device name
]

# Firebase/Auth files to DELETE for offline mode
FIREBASE_AUTH_PATTERNS = [
    "*firebase*.js",
    "*firebase*.md",
    "*Firebase*.js",
    "*Firebase*.md",
    "auth-guard*.js",
    "auth-guard*.md",
    "secrets_config*",
]


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def run_command(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """Run shell command."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def get_file_hash(filepath: Path) -> str:
    """Generate SHA-256 hash."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def format_size(size_bytes: int) -> str:
    """Format file size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


# ============================================================
# CLONE & CLEAN FUNCTIONS
# ============================================================

def clone_fresh_repo(temp_dir: Path) -> Path:
    """Clone fresh repository."""
    print("\n" + "=" * 60)
    print("PHASE 1: Cloning Fresh Repository")
    print("=" * 60)

    clone_path = temp_dir / "PrincipiaMetaphysica"
    print(f"  Repository: {REPO_URL}")
    print(f"  Branch: {REPO_BRANCH}")

    cmd = ["git", "clone", "--depth", "1", "--branch", REPO_BRANCH, REPO_URL, str(clone_path)]
    returncode, stdout, stderr = run_command(cmd)

    if returncode != 0:
        raise RuntimeError(f"Git clone failed: {stderr}")

    print("  [OK] Cloned successfully")
    return clone_path


def clean_repo(repo_path: Path) -> int:
    """Remove unnecessary files and folders."""
    print("\n" + "=" * 60)
    print("PHASE 2: Cleaning Repository")
    print("=" * 60)

    removed = 0

    # Remove excluded folders
    for folder_name in EXCLUDE_FOLDERS:
        for folder in list(repo_path.rglob(folder_name)):
            if folder.is_dir():
                shutil.rmtree(folder, onerror=_remove_readonly)
                removed += 1
                print(f"  [DELETE] {folder.name}/")

    # Remove excluded file patterns
    for pattern in EXCLUDE_PATTERNS:
        for filepath in list(repo_path.rglob(pattern)):
            if filepath.is_file():
                filepath.unlink()
                removed += 1

    print(f"\n  [OK] Removed {removed} items")
    return removed


def strip_firebase_auth(repo_path: Path) -> int:
    """Remove all Firebase/Auth files and update HTML for offline use."""
    print("\n" + "=" * 60)
    print("PHASE 3: Stripping Firebase/Auth (Offline Mode)")
    print("=" * 60)

    deleted = 0

    # Delete Firebase/Auth files
    for pattern in FIREBASE_AUTH_PATTERNS:
        for filepath in list(repo_path.rglob(pattern)):
            if filepath.is_file():
                filepath.unlink()
                deleted += 1
                print(f"  [DELETE] {filepath.name}")

    # Update HTML files to remove Firebase references
    html_updated = 0
    for html_file in repo_path.rglob("*.html"):
        try:
            content = html_file.read_text(encoding='utf-8')
            original = content

            # Remove Firebase script tags
            content = re.sub(
                r'<script[^>]*firebase[^>]*>.*?</script>',
                '', content, flags=re.IGNORECASE | re.DOTALL
            )
            content = re.sub(
                r'<script[^>]*auth-guard[^>]*>.*?</script>',
                '', content, flags=re.IGNORECASE | re.DOTALL
            )

            # Remove auth-loading class from body
            content = content.replace('<body class="auth-loading">', '<body>')
            content = re.sub(r'(<body[^>]*) class="auth-loading"', r'\1', content)

            # Show main-content by default (remove display:none)
            content = content.replace('id="main-content" style="display: none;"', 'id="main-content"')
            content = re.sub(r'id="main-content"[^>]*style="[^"]*display:\s*none[^"]*"', 'id="main-content"', content)

            if content != original:
                html_file.write_text(content, encoding='utf-8')
                html_updated += 1

        except Exception as e:
            print(f"  [WARN] {html_file.name}: {e}")

    print(f"\n  [OK] Deleted {deleted} Firebase/auth files")
    print(f"  [OK] Updated {html_updated} HTML files for offline use")
    return deleted


# ============================================================
# PACKAGE CREATION
# ============================================================

def create_zip(source_path: Path, dest_path: Path, suffix: str = "") -> Tuple[Path, str]:
    """Create ZIP archive with SHA-256 checksum."""
    print("\n" + "=" * 60)
    print("PHASE 4: Creating ZIP Archive")
    print("=" * 60)

    date_str = datetime.now().strftime('%Y%m%d')
    zip_name = f"Principia_Metaphysica_v{VERSION}_{date_str}{suffix}.zip"
    zip_path = dest_path / zip_name

    if zip_path.exists():
        zip_path.unlink()

    count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root_dir, dirs, files in os.walk(source_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]
            for file in files:
                file_path = Path(root_dir) / file
                arc_name = file_path.relative_to(source_path)
                zipf.write(file_path, arc_name)
                count += 1

    # Compute SHA-256 hash
    sha256 = get_file_hash(zip_path)

    print(f"  Files: {count}")
    print(f"  Size: {format_size(zip_path.stat().st_size)}")
    print(f"  SHA-256: {sha256}")
    print(f"  [OK] Created {zip_name}")

    # Write checksum file
    checksum_path = dest_path / f"{zip_name}.sha256"
    with open(checksum_path, 'w') as f:
        f.write(f"{sha256}  {zip_name}\n")
    print(f"  [OK] Created {zip_name}.sha256")

    return zip_path, sha256


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Create distribution package")
    parser.add_argument("--local", action="store_true", help="Use local repo instead of fresh clone")
    parser.add_argument("--full", action="store_true", help="Also create _FULL package (same content)")
    args = parser.parse_args()

    print("=" * 60)
    print("PRINCIPIA METAPHYSICA - Package Creator")
    print("=" * 60)
    print(f"Version: {VERSION}")

    temp_dir = None

    try:
        if args.local:
            print("\nMode: LOCAL (using current repo)")
            # Copy to temp location for processing
            temp_dir = Path(tempfile.mkdtemp(prefix="pm_package_"))
            source_path = temp_dir / "PrincipiaMetaphysica"
            shutil.copytree(ROOT, source_path, ignore=shutil.ignore_patterns(*EXCLUDE_FOLDERS, *EXCLUDE_PATTERNS))
        else:
            print("\nMode: FRESH CLONE")
            temp_dir = Path(tempfile.mkdtemp(prefix="pm_package_"))
            source_path = clone_fresh_repo(temp_dir)

        # Clean repository
        clean_repo(source_path)

        # Strip Firebase/Auth for offline use
        strip_firebase_auth(source_path)

        # Create main ZIP
        zip_path, sha256 = create_zip(source_path, ROOT)

        # Create FULL ZIP if requested (identical content for compatibility)
        full_zip_path = None
        full_sha256 = None
        if args.full:
            full_zip_path, full_sha256 = create_zip(source_path, ROOT, "_FULL")

        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  ZIP: {zip_path.name}")
        print(f"  SHA-256: {sha256}")
        if full_zip_path:
            print(f"\n  FULL ZIP: {full_zip_path.name}")
            print(f"  FULL SHA-256: {full_sha256}")
        print(f"\n  Status: READY")

    finally:
        if temp_dir and temp_dir.exists():
            try:
                shutil.rmtree(temp_dir, onerror=_remove_readonly)
            except Exception:
                pass


if __name__ == "__main__":
    main()
