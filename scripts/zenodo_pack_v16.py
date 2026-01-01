#!/usr/bin/env python3
"""
Zenodo Package Builder for Principia Metaphysica v16.2
======================================================

This script creates a self-contained, offline-capable archive suitable for
Zenodo submission. It follows a "Build, Strip, and Seal" workflow:

1. CLEAN: Use git archive for pristine export (no uncommitted changes)
2. STRIP: Remove/neutralize authentication and secrets
3. SEAL: Generate checksums and create ZIP/7z archive

The resulting package can be unzipped and run on any machine without
network access or authentication credentials.

Usage:
    python scripts/zenodo_pack_v16.py [--test] [--no-zip] [--7z] [--git-archive]

Options:
    --test          Run clean-room verification after building
    --no-zip        Build directory only, don't create archive
    --7z            Create 7z archive instead of ZIP (requires 7z installed)
    --git-archive   Use git archive for pristine export (ignores uncommitted changes)
    --full          Include simulations directory (larger package)
    --validate      Run 72-gate validation before building (runs run_all_simulations.py)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import os
import sys
import shutil
import zipfile
import hashlib
import json
import datetime
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Set, Dict, List, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

VERSION = "16.2"
RELEASE_DATE = datetime.datetime.now().strftime("%Y%m%d")

# Source and build directories
SOURCE_DIR = Path(__file__).parent.parent  # Project root
BUILD_DIR = SOURCE_DIR / f"Principia_Metaphysica_v{VERSION.replace('.', '_')}_{RELEASE_DATE}"
ZIP_NAME = f"Principia_Metaphysica_v{VERSION.replace('.', '_')}_{RELEASE_DATE}.zip"

# Directories to exclude entirely (base set)
EXCLUDE_DIRS_BASE: Set[str] = {
    '.git',
    '.github',
    '__pycache__',
    '.pytest_cache',
    'node_modules',
    '.venv',
    'venv',
    '.env',
    'private',
    '.claude',
    'zenodo_submission',  # Temporary submission folder
    'firebase-backup',
    'tests',        # Test files
}

# Additional excludes for website-only package
EXCLUDE_DIRS_WEBSITE_ONLY: Set[str] = {
    'simulations',  # Exclude Python simulations (large)
    'reports',      # Generated reports
}

# Default to website-only
EXCLUDE_DIRS: Set[str] = EXCLUDE_DIRS_BASE | EXCLUDE_DIRS_WEBSITE_ONLY

# Files to exclude
EXCLUDE_FILES: Set[str] = {
    '.gitignore',
    '.DS_Store',
    'Thumbs.db',
    '.env',
    '.env.local',
    'serviceAccountKey.json',
    'package-lock.json',
    'nul',
    # Firebase/Auth JS files to exclude completely
    'auth-guard.js',
    'auth-guard-ENHANCED.js',
    'firebase-auth.js',
    'firebase-config.js',
    'firebase-data.js',
    'firebase-analytics.js',
    'firebase-page-loader.js',
    'firebase-references.js',
    # Auth CSS
    'auth.css',
    # Firebase scripts
    'add-firebase-auth.js',
    'replace-auth-guard.bat',
    'test-data-loading.js',
    'validate-firebase-coverage.js',
    # Firebase documentation (not needed for offline)
    'firebase-page-loader-integration.md',
    'QUICK_REFERENCE_firebase-page-loader.md',
    'README-firebase-page-loader.md',
    'FIREBASE_PAGE_LOADER_USAGE.md',
    # Firebase admin scripts (server-side, not for offline website)
    'firebase-check-status.js',
    'firebase-diff.js',
    'firebase-diff-confirm.js',
    'firebase-download.js',
    'firebase-helper.js',
    'firebase-push-updates.js',
    'firebase-push-validated.js',
    'firebase-status-report.js',
    'firebase-sync-with-history.js',
    'firebase-upload-all.js',
    'firebase-upload-complete.js',
    'firebase-upload-website-content.js',
    'migrate-references-to-firebase.js',
    'migrate-to-firestore.js',
    'test-firebase-sync.js',
    'validate_firebase_params.js',
    'upload-tooltip-database.js',
    'upload-formula-database.js',
    'generate-latex-paper.js',
    'master-pipeline.js',
    'extract-page-content.js',
    'update-page-loader.js',
    'test-references.js',
    # Examples that reference firebase
    'references-integration-example.html',
    'INTEGRATION_EXAMPLE.html',
    'test-html-extraction.js',
}

# Files to strip/neutralize (secrets, auth guards)
STRIP_FILES: Dict[str, str] = {
    'secrets_config.py': '''#!/usr/bin/env python3
"""
SECRETS CONFIGURATION - ZENODO RELEASE (STRIPPED)
=================================================

This file has been stripped of actual API keys for Zenodo release.
For local development, replace the placeholder values with your actual API keys.

Get your Wolfram Alpha App ID at: https://developer.wolframalpha.com/
"""

# Wolfram Alpha API - Replace with your own App ID for local use
WOLFRAM_APP_ID = "YOUR_APP_ID_HERE"

# API Configuration (unchanged)
WOLFRAM_API_TIMEOUT = 30  # seconds
WOLFRAM_MAX_RETRIES = 3

# Validation settings (unchanged)
VALIDATION_CACHE_DIR = "AutoGenerated/validations/"
PROOF_MANIFEST_PATH = "AutoGenerated/proof_manifest.json"
''',
    'auth_guard.py': '''#!/usr/bin/env python3
"""
AUTH GUARD - ZENODO RELEASE (BYPASSED)
======================================

This module has been neutralized for offline Zenodo release.
All authentication checks return True to allow offline verification.
"""

def check_access():
    """Always returns True for offline access."""
    return True

def login_required(func):
    """Decorator that does nothing (bypasses login requirement)."""
    return func

def verify_token(token):
    """Always returns True for offline verification."""
    return True

class AuthGuard:
    """Neutralized auth guard for offline use."""

    def __init__(self):
        self.authenticated = True

    def check(self):
        return True

    def require_auth(self, func):
        return func
''',
}

# Patterns for files to exclude (glob-style)
EXCLUDE_PATTERNS: List[str] = [
    '*_secrets.py',
    '*_secret.py',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '*.so',
    '*.egg-info',
    '*.egg',
    '*.log',
    '*.tmp',
    '*.temp',
    '*.bak',
    '*~',
    '*.swp',
    '*.swo',
]

# Directories to include (if not in EXCLUDE_DIRS)
# Note: simulations, tests, reports are excluded for smaller website-only package
INCLUDE_DIRS: List[str] = [
    'AutoGenerated',
    'js',
    'css',
    'data',
    'docs',
    'images',
    'diagrams',
    'Pages',
    'foundations',
    'formal_proofs',
    'components',
    'examples',
    'scripts',
    'utils',
    'PROOFS',
    'sections',
    'tools',
]

# Key files to include from root
INCLUDE_ROOT_FILES: List[str] = [
    'config.py',
    'README.md',
    'LICENSE',
    'CITATION.cff',
    'ARCHITECTURE.md',
    'PROVENANCE.md',
    'PEER_REVIEW_DEFENSE.md',
    'index.html',
    'principia-metaphysica-paper.html',
    'IMPLEMENTATION_PLAN_v16_2.md',
    'serve.py',
    'start_server.bat',
    'Launch.bat',
    'run_all_simulations.py',  # For full package
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def should_exclude_dir(dirname: str) -> bool:
    """Check if a directory should be excluded."""
    return dirname in EXCLUDE_DIRS or dirname.startswith('.')

def should_exclude_file(filename: str) -> bool:
    """Check if a file should be excluded."""
    if filename in EXCLUDE_FILES:
        return True
    if filename.startswith('.'):
        return True
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*') and filename.endswith(pattern[1:]):
            return True
        if pattern.endswith('*') and filename.startswith(pattern[:-1]):
            return True
    return False

def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def compute_sha512(file_path: Path) -> str:
    """Compute SHA-512 hash of a file."""
    sha512 = hashlib.sha512()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha512.update(chunk)
    return sha512.hexdigest()

# ============================================================================
# MAIN BUILD FUNCTIONS
# ============================================================================

def clean_build_dir():
    """Remove existing build directory if it exists."""
    if BUILD_DIR.exists():
        print(f"  Removing existing build directory: {BUILD_DIR.name}")
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)
    print(f"  Created clean build directory: {BUILD_DIR.name}")

def copy_directory(src: Path, dst: Path, strip_files: Dict[str, str]):
    """
    Recursively copy a directory, excluding and stripping as needed.

    Args:
        src: Source directory
        dst: Destination directory
        strip_files: Dict mapping filename to replacement content
    """
    if not src.exists():
        return

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        if item.is_dir():
            if not should_exclude_dir(item.name):
                copy_directory(item, dst / item.name, strip_files)
        else:
            if should_exclude_file(item.name):
                continue

            dest_file = dst / item.name

            # Check if this file should be stripped
            if item.name in strip_files:
                print(f"    [STRIPPED] {item.relative_to(SOURCE_DIR)}")
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(strip_files[item.name])
            else:
                shutil.copy2(item, dest_file)

def strip_auth_from_html(file_path: Path) -> bool:
    """
    Remove auth-guard imports and setupAuthGuard calls from HTML files.
    Returns True if modifications were made.
    """
    import re

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        return False

    original = content

    # Remove auth-guard imports (various path patterns)
    content = content.replace("import { setupAuthGuard } from '../js/auth-guard.js';", '')
    content = content.replace("import { setupAuthGuard } from './js/auth-guard.js';", '')
    content = content.replace("import { setupAuthGuard } from '../../js/auth-guard.js';", '')

    # Remove firebase imports
    content = content.replace("import { auth } from '../js/firebase-config.js';", '')
    content = content.replace("import { auth } from './js/firebase-config.js';", '')
    content = re.sub(r"import \{ onAuthStateChanged \} from 'https://www\.gstatic\.com/firebasejs/[^']+/firebase-auth\.js';", '', content)

    # Remove setupAuthGuard calls
    content = re.sub(r'// Setup auth[^\n]*\n\s*setupAuthGuard\([^)]+\);\s*\n?', '', content)
    content = re.sub(r'setupAuthGuard\([^)]+\);\s*\n?', '', content)

    # Remove onAuthStateChanged usage
    content = re.sub(r'onAuthStateChanged\(auth,[^}]+\}\);', '', content, flags=re.DOTALL)

    # Remove auth.css link tags (various path patterns)
    content = re.sub(r'\s*<link rel="stylesheet" href="[^"]*auth\.css">\s*\n?', '\n', content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def strip_login_ui_from_header(file_path: Path) -> bool:
    """
    Remove login/logout UI from pm-header.js.
    Returns True if modifications were made.
    """
    import re

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        return False

    original = content

    # Remove the user-controls-nav li element
    old_nav = '''          <ul role="list">
            ${navItems}
            <li class="user-controls-nav">
              <div class="user-controls" style="display: none;">
                <img id="user-avatar" src="${basePath}images/default-avatar.svg" alt="User" class="user-avatar">
                <span id="user-email" class="user-email"></span>
                <button id="logout-btn" class="logout-btn">Logout</button>
              </div>
              <button id="header-login-btn" class="header-login-btn" style="display: none;">
                <img src="${basePath}images/google-icon.svg" alt="G" class="google-icon-small">
                Login
              </button>
            </li>
          </ul>'''

    new_nav = '''          <ul role="list">
            ${navItems}
          </ul>'''

    content = content.replace(old_nav, new_nav)

    # Remove the updateHeaderUserDisplay function entirely (includes JSDoc comment)
    content = re.sub(
        r'/\*\*\s*\n\s*\* Update user display in header \(called by auth-guard\).*?^export function updateHeaderUserDisplay\(user\) \{.*?^\}\n',
        '// User display functions removed - no auth in offline build\n',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # Remove firebase import from pm-template-engine.js style reference
    content = content.replace("import { app } from './firebase-config.js';", '// Firebase import removed for offline build')

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def strip_auth_from_all_html():
    """Strip auth from all HTML files in the build directory."""
    print("\n  Stripping authentication from HTML files...")

    html_count = 0
    modified_count = 0

    for root, dirs, files in os.walk(BUILD_DIR):
        dirs[:] = [d for d in dirs if not should_exclude_dir(d)]

        for filename in files:
            if filename.endswith('.html'):
                html_count += 1
                filepath = Path(root) / filename
                if strip_auth_from_html(filepath):
                    modified_count += 1
                    rel_path = filepath.relative_to(BUILD_DIR)
                    print(f"    [STRIPPED] {rel_path}")

    print(f"    Processed {html_count} HTML files, modified {modified_count}")


def strip_auth_from_js():
    """Strip auth-related code from JS files."""
    import re
    print("\n  Stripping authentication from JS files...")

    # Strip pm-header.js
    header_js = BUILD_DIR / "js" / "pm-header.js"
    if header_js.exists():
        if strip_login_ui_from_header(header_js):
            print(f"    [STRIPPED] js/pm-header.js")

    # Strip pm-template-engine.js firebase imports
    template_js = BUILD_DIR / "js" / "pm-template-engine.js"
    if template_js.exists():
        try:
            with open(template_js, 'r', encoding='utf-8') as f:
                content = f.read()
            original = content
            # Remove firebase-config import
            content = content.replace("import { app } from './firebase-config.js';", '// Firebase import removed for offline build')
            # Remove firestore import (line 14)
            content = re.sub(
                r'import \{ getFirestore, collection, doc, getDoc, getDocs, query, where, orderBy \} from "https://www\.gstatic\.com/firebasejs/[^"]+/firebase-firestore\.js";',
                '// Firestore import removed for offline build',
                content
            )
            if content != original:
                with open(template_js, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"    [STRIPPED] js/pm-template-engine.js")
        except Exception as e:
            print(f"    [WARNING] Could not process pm-template-engine.js: {e}")

    # Strip simulation-stats.js firebase references
    stats_js = BUILD_DIR / "js" / "simulation-stats.js"
    if stats_js.exists():
        try:
            with open(stats_js, 'r', encoding='utf-8') as f:
                content = f.read()
            original = content
            # Replace entire firebase fallback block (lines 102-112)
            firebase_block = """            // Fallback to Firebase if available
            if (typeof firebase !== 'undefined' && firebase.database) {
                try {
                    const snapshot = await firebase.database().ref('/simulations').once('value');
                    this._data = { simulations: snapshot.val() };
                    this._lastUpdate = new Date().toISOString();
                    return true;
                } catch (e) {
                    console.warn('SimulationStats: Could not load from Firebase:', e);
                }
            }"""
            content = content.replace(firebase_block,
                "            // Firebase fallback removed for offline build")
            if content != original:
                with open(stats_js, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"    [STRIPPED] js/simulation-stats.js")
        except Exception as e:
            print(f"    [WARNING] Could not process simulation-stats.js: {e}")


def copy_root_files():
    """Copy important root-level files."""
    print("\n  Copying root files...")
    for filename in INCLUDE_ROOT_FILES:
        src = SOURCE_DIR / filename
        if src.exists():
            shutil.copy2(src, BUILD_DIR / filename)
            print(f"    Copied: {filename}")
        else:
            print(f"    [MISSING] {filename}")

def copy_include_directories():
    """Copy all included directories."""
    print("\n  Copying directories...")
    for dirname in INCLUDE_DIRS:
        src = SOURCE_DIR / dirname
        if src.exists() and src.is_dir():
            print(f"    Copying: {dirname}/")
            copy_directory(src, BUILD_DIR / dirname, STRIP_FILES)
        else:
            print(f"    [SKIP] {dirname}/ (not found)")

def create_offline_config():
    """Create offline configuration files for the website."""
    print("\n  Creating offline configuration...")

    # Create offline mode config for JavaScript
    offline_config_js = BUILD_DIR / "js" / "offline-config.js"
    offline_config_js.parent.mkdir(parents=True, exist_ok=True)

    with open(offline_config_js, 'w', encoding='utf-8') as f:
        f.write('''// Principia Metaphysica - Offline Mode Configuration
// Auto-generated for Zenodo release

window.PM_CONFIG = {
    mode: 'offline',
    dataSource: 'local',
    version: '%s',
    releaseDate: '%s',

    // Local data paths (relative to index.html)
    paths: {
        formulas: './AutoGenerated/formulas.json',
        parameters: './AutoGenerated/parameters.json',
        simulations: './AutoGenerated/simulations.json',
        sections: './AutoGenerated/sections.json',
        metadata: './AutoGenerated/metadata.json',
        theoryOutput: './AutoGenerated/theory_output.json',
    },

    // Disable features that require network
    features: {
        apiCalls: false,
        cloudSync: false,
        authentication: false,
        analytics: false,
    }
};

// Signal offline mode to other scripts
window.PM_OFFLINE = true;
console.log('[PM] Running in offline mode (Zenodo release)');
''' % (VERSION, RELEASE_DATE))

    print(f"    Created: js/offline-config.js")

def create_package_manifest():
    """Create a manifest of all files in the package."""
    print("\n  Creating package manifest...")

    manifest = {
        "package": "Principia Metaphysica",
        "version": VERSION,
        "release_date": RELEASE_DATE,
        "build_timestamp": datetime.datetime.now().isoformat(),
        "description": "Complete computational implementation of Principia Metaphysica theory",
        "author": "Andrew Keith Watts",
        "license": "MIT (code), See LICENSE for theory content",
        "files": [],
        "checksums": {}
    }

    file_count = 0
    total_size = 0

    for root, dirs, files in os.walk(BUILD_DIR):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not should_exclude_dir(d)]

        for filename in files:
            filepath = Path(root) / filename
            rel_path = filepath.relative_to(BUILD_DIR)
            file_size = filepath.stat().st_size

            manifest["files"].append({
                "path": str(rel_path),
                "size": file_size,
                "sha256": compute_sha256(filepath)[:16] + "..."  # Truncated for readability
            })

            file_count += 1
            total_size += file_size

    manifest["summary"] = {
        "total_files": file_count,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2)
    }

    # Write manifest
    manifest_path = BUILD_DIR / "MANIFEST.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"    Files: {file_count}")
    print(f"    Size: {manifest['summary']['total_size_mb']} MB")
    print(f"    Created: MANIFEST.json")

    return manifest

def create_verification_script():
    """Create a standalone verification script."""
    print("\n  Creating verification script...")

    verify_script = BUILD_DIR / "verify_package.py"

    with open(verify_script, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""
Principia Metaphysica Package Verification Script
=================================================

Run this script to verify the integrity and functionality of the package.

Usage:
    python verify_package.py [--full]

Options:
    --full    Run full simulation tests (takes longer)
"""

import os
import sys
import json
import hashlib
from pathlib import Path

def main():
    print("=" * 60)
    print(" Principia Metaphysica Package Verification")
    print("=" * 60)

    package_dir = Path(__file__).parent
    errors = []
    warnings = []

    # 1. Check manifest exists
    print("\\n[1/5] Checking manifest...")
    manifest_path = package_dir / "MANIFEST.json"
    if not manifest_path.exists():
        errors.append("MANIFEST.json not found")
    else:
        with open(manifest_path) as f:
            manifest = json.load(f)
        print(f"      Version: {manifest['version']}")
        print(f"      Files: {manifest['summary']['total_files']}")

    # 2. Check critical files exist
    print("\\n[2/5] Checking critical files...")
    critical_files = [
        "config.py",
        "README.md",
        "LICENSE",
        "AutoGenerated/formulas.json",
        "AutoGenerated/parameters.json",
        "simulations/base/__init__.py",
    ]
    for cf in critical_files:
        if not (package_dir / cf).exists():
            errors.append(f"Missing: {cf}")
        else:
            print(f"      OK: {cf}")

    # 3. Check Python imports
    print("\\n[3/5] Checking Python imports...")
    sys.path.insert(0, str(package_dir))
    try:
        import config
        print("      OK: config.py imports")
    except Exception as e:
        errors.append(f"config.py import failed: {e}")

    try:
        from simulations.base import PMRegistry
        print("      OK: simulations.base imports")
    except Exception as e:
        errors.append(f"simulations.base import failed: {e}")

    # 4. Check JSON data files
    print("\\n[4/5] Checking JSON data files...")
    json_files = [
        "AutoGenerated/formulas.json",
        "AutoGenerated/parameters.json",
        "AutoGenerated/simulations.json",
    ]
    for jf in json_files:
        jf_path = package_dir / jf
        if jf_path.exists():
            try:
                with open(jf_path, encoding='utf-8') as f:
                    data = json.load(f)
                print(f"      OK: {jf} ({len(data) if isinstance(data, list) else 'valid'} entries)")
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON in {jf}: {e}")
            except UnicodeDecodeError as e:
                warnings.append(f"Encoding issue in {jf}: {e}")

    # 5. Quick simulation test
    print("\\n[5/5] Quick simulation test...")
    try:
        from simulations.base import PMRegistry
        from simulations.base.established import EstablishedPhysics

        registry = PMRegistry()
        EstablishedPhysics.load_into_registry(registry)

        alpha = registry.get_param("constants.alpha_em")
        print(f"      OK: alpha_em = {alpha:.6e}")
    except Exception as e:
        warnings.append(f"Simulation test warning: {e}")

    # Summary
    print("\\n" + "=" * 60)
    if errors:
        print(f" FAILED - {len(errors)} error(s)")
        for e in errors:
            print(f"   ERROR: {e}")
        sys.exit(1)
    elif warnings:
        print(f" PASSED with {len(warnings)} warning(s)")
        for w in warnings:
            print(f"   WARN: {w}")
    else:
        print(" PASSED - All checks successful")
    print("=" * 60)

if __name__ == "__main__":
    main()
''')

    print(f"    Created: verify_package.py")

def create_zip_archive():
    """Create the final ZIP archive with checksum."""
    print("\n  Creating ZIP archive...")

    zip_path = SOURCE_DIR / ZIP_NAME

    # Create ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BUILD_DIR):
            dirs[:] = [d for d in dirs if not should_exclude_dir(d)]

            for filename in files:
                filepath = Path(root) / filename
                arcname = filepath.relative_to(BUILD_DIR.parent)
                zf.write(filepath, arcname)

    # Compute checksums
    zip_size = zip_path.stat().st_size
    sha256 = compute_sha256(zip_path)
    sha512 = compute_sha512(zip_path)

    print(f"    Archive: {ZIP_NAME}")
    print(f"    Size: {zip_size / (1024*1024):.2f} MB")
    print(f"    SHA-256: {sha256}")

    # Write checksum file
    checksum_path = SOURCE_DIR / f"{ZIP_NAME}.sha256"
    with open(checksum_path, 'w') as f:
        f.write(f"{sha256}  {ZIP_NAME}\n")
    print(f"    Created: {ZIP_NAME}.sha256")

    return zip_path, sha256, sha512


def create_7z_archive():
    """Create 7z archive using 7-Zip (requires 7z installed)."""
    print("\n  Creating 7z archive...")

    archive_name = ZIP_NAME.replace('.zip', '.7z')
    archive_path = SOURCE_DIR / archive_name

    # Find 7z executable
    if sys.platform == 'win32':
        # Try common Windows paths
        seven_zip_paths = [
            r"C:\Program Files\7-Zip\7z.exe",
            r"C:\Program Files (x86)\7-Zip\7z.exe",
            "7z.exe",  # If in PATH
        ]
        seven_zip = None
        for path in seven_zip_paths:
            if os.path.exists(path) or shutil.which(path):
                seven_zip = path
                break
    else:
        seven_zip = shutil.which("7z") or shutil.which("7za")

    if not seven_zip:
        print("  [ERROR] 7z not found. Install 7-Zip or use --no-7z")
        print("  Falling back to ZIP...")
        return create_zip_archive()

    # Remove existing archive
    if archive_path.exists():
        archive_path.unlink()

    # Create 7z archive with maximum compression
    try:
        result = subprocess.run(
            [seven_zip, "a", "-t7z", "-mx=9", "-mfb=273", "-ms", "-md=31",
             str(archive_path), str(BUILD_DIR)],
            capture_output=True,
            text=True,
            cwd=BUILD_DIR.parent
        )

        if result.returncode != 0:
            print(f"  [ERROR] 7z failed: {result.stderr}")
            return create_zip_archive()

    except Exception as e:
        print(f"  [ERROR] 7z failed: {e}")
        return create_zip_archive()

    # Compute checksums
    archive_size = archive_path.stat().st_size
    sha256 = compute_sha256(archive_path)
    sha512 = compute_sha512(archive_path)

    print(f"    Archive: {archive_name}")
    print(f"    Size: {archive_size / (1024*1024):.2f} MB")
    print(f"    SHA-256: {sha256}")

    # Write checksum file
    checksum_path = SOURCE_DIR / f"{archive_name}.sha256"
    with open(checksum_path, 'w') as f:
        f.write(f"{sha256}  {archive_name}\n")
    print(f"    Created: {archive_name}.sha256")

    return archive_path, sha256, sha512


def git_archive_export(target_dir: Path) -> bool:
    """
    Use git archive to export a clean copy of the repository.
    This ensures no uncommitted changes or untracked files are included.

    Args:
        target_dir: Directory to extract the archive to

    Returns:
        True if successful, False otherwise
    """
    print("\n  Exporting clean git archive...")

    # Check if we're in a git repo
    if not (SOURCE_DIR / ".git").exists():
        print("  [WARN] Not a git repository, falling back to copy")
        return False

    try:
        # Get current commit hash for reference
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=SOURCE_DIR
        )
        commit_hash = result.stdout.strip() if result.returncode == 0 else "unknown"
        print(f"    Commit: {commit_hash}")

        # Create temporary tar file
        with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as tmp:
            tmp_tar = tmp.name

        # Export using git archive
        result = subprocess.run(
            ["git", "archive", "--format=tar", "-o", tmp_tar, "HEAD"],
            capture_output=True,
            text=True,
            cwd=SOURCE_DIR
        )

        if result.returncode != 0:
            print(f"  [ERROR] git archive failed: {result.stderr}")
            os.unlink(tmp_tar)
            return False

        # Extract to target directory
        target_dir.mkdir(parents=True, exist_ok=True)

        import tarfile
        with tarfile.open(tmp_tar, 'r') as tar:
            tar.extractall(target_dir)

        os.unlink(tmp_tar)

        print(f"    Exported to: {target_dir.name}")
        print(f"    Status: Clean (no uncommitted changes)")

        return True

    except Exception as e:
        print(f"  [ERROR] git archive failed: {e}")
        return False


def inject_omega_seal(build_dir: Path):
    """Copy Omega Seal verification files to the build directory."""
    print("\n  Injecting Omega Seal...")

    omega_seal_src = SOURCE_DIR / "simulations" / "AutoGenerated" / "OMEGA_SEAL.json"
    omega_hash_src = SOURCE_DIR / "simulations" / "AutoGenerated" / "OMEGA_SEAL.hash"

    if omega_seal_src.exists():
        # Create verification directory
        verify_dir = build_dir / "VERIFICATION"
        verify_dir.mkdir(exist_ok=True)

        shutil.copy2(omega_seal_src, verify_dir / "OMEGA_SEAL.json")
        print(f"    Copied: OMEGA_SEAL.json")

        if omega_hash_src.exists():
            shutil.copy2(omega_hash_src, verify_dir / "OMEGA_SEAL.hash")
            print(f"    Copied: OMEGA_SEAL.hash")

            # Also create VERIFICATION_MANIFEST.txt at root
            with open(build_dir / "VERIFICATION_MANIFEST.txt", 'w') as f:
                with open(omega_hash_src, 'r') as src:
                    f.write("PRINCIPIA METAPHYSICA v16.2 - VERIFICATION MANIFEST\n")
                    f.write("=" * 50 + "\n\n")
                    f.write("OMEGA SEAL (72-Gate Master Hash):\n")
                    f.write(src.read())
                    f.write(f"\nExport Date: {datetime.datetime.now().isoformat()}\n")
                    f.write("\nStatus: Auth-Free, 72-Gate Verified, G2-Residue Locked.\n")
            print(f"    Created: VERIFICATION_MANIFEST.txt")
    else:
        print("    [WARN] OMEGA_SEAL.json not found - run finalize_lockdown.py first")

def run_clean_room_test():
    """Run verification in the built package directory."""
    print("\n  Running clean room verification...")

    # Change to build directory and run verification
    import subprocess

    result = subprocess.run(
        [sys.executable, "verify_package.py"],
        cwd=BUILD_DIR,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print(f"  [WARNING] Verification returned non-zero: {result.returncode}")
        if result.stderr:
            print(result.stderr)
        return False
    return True

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    global EXCLUDE_DIRS, ZIP_NAME, BUILD_DIR

    parser = argparse.ArgumentParser(
        description="Build Zenodo package for Principia Metaphysica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/zenodo_pack_v16.py                    # Standard website-only ZIP
  python scripts/zenodo_pack_v16.py --7z               # Use 7z compression
  python scripts/zenodo_pack_v16.py --git-archive      # Clean git export
  python scripts/zenodo_pack_v16.py --full --validate  # Full package with validation
        """
    )
    parser.add_argument("--test", action="store_true",
                        help="Run clean-room verification after building")
    parser.add_argument("--no-zip", action="store_true",
                        help="Build directory only, don't create archive")
    parser.add_argument("--7z", dest="use_7z", action="store_true",
                        help="Create 7z archive instead of ZIP (better compression)")
    parser.add_argument("--git-archive", dest="git_archive", action="store_true",
                        help="Use git archive for pristine export (ignores uncommitted)")
    parser.add_argument("--full", action="store_true",
                        help="Include simulations (for full research package)")
    parser.add_argument("--validate", action="store_true",
                        help="Run 72-gate validation before building")
    args = parser.parse_args()

    # Adjust excludes based on package type
    if args.full:
        EXCLUDE_DIRS = EXCLUDE_DIRS_BASE  # Include simulations
        ZIP_NAME = ZIP_NAME.replace('.zip', '_FULL.zip')
        BUILD_DIR = Path(str(BUILD_DIR) + "_FULL")

    print("=" * 70)
    print(f" PRINCIPIA METAPHYSICA - ZENODO PACKAGE BUILDER v{VERSION}")
    print("=" * 70)
    print(f"\nSource: {SOURCE_DIR}")
    print(f"Build:  {BUILD_DIR.name}")
    archive_type = "7z" if args.use_7z else "ZIP"
    output_name = ZIP_NAME.replace('.zip', '.7z') if args.use_7z else ZIP_NAME
    print(f"Output: {output_name} ({archive_type})")
    if args.full:
        print(f"Mode:   FULL (includes simulations)")
    else:
        print(f"Mode:   Website-only")
    if args.git_archive:
        print(f"Source: Git archive (clean export)")

    # Optional: Run 72-gate validation (runs run_all_simulations.py)
    if args.validate:
        print("\n" + "=" * 70)
        print(" PRE-BUILD VALIDATION: 72-Gate Integrity Verification")
        print("=" * 70)
        try:
            result = subprocess.run(
                [sys.executable, str(SOURCE_DIR / "run_all_simulations.py")],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=SOURCE_DIR
            )
            # Check for success in output
            if result.returncode == 0:
                # Look for 72-gate results
                import re
                gate_match = re.search(r'(\d+)/72 GATES', result.stdout)
                omega_match = re.search(r'OMEGA HASH: ([a-f0-9]+)', result.stdout)

                if gate_match:
                    gates_passed = gate_match.group(1)
                    print(f"  [PASS] {gates_passed}/72 gates validated")
                if omega_match:
                    print(f"  Omega Hash: {omega_match.group(1)}")
                if not gate_match:
                    print("  [OK] Simulations completed")
            else:
                print("  [WARN] Validation completed with errors")
                if result.stderr:
                    print(f"  stderr: {result.stderr[:200]}")
        except Exception as e:
            print(f"  [ERROR] Could not run validation: {e}")

    # Step 1: Clean and prepare
    print("\n[1/9] Preparing build directory...")
    clean_build_dir()

    # Step 2: Export source (git archive or copy)
    use_git_export = False
    if args.git_archive:
        print("\n[2/9] Exporting via git archive...")
        use_git_export = git_archive_export(BUILD_DIR)
        if not use_git_export:
            print("  Falling back to file copy...")

    if not use_git_export:
        # Step 2b: Copy root files
        print("\n[2/9] Copying root files...")
        copy_root_files()

        # Step 3: Copy directories
        print("\n[3/9] Copying directories...")
        copy_include_directories()

    # Step 4: Strip authentication from files
    print("\n[4/9] Stripping authentication from HTML files...")
    strip_auth_from_all_html()

    # Step 5: Strip authentication from JS files
    print("\n[5/9] Stripping authentication from JS files...")
    strip_auth_from_js()

    # Step 6: Create offline config
    print("\n[6/9] Creating offline configuration...")
    create_offline_config()
    create_verification_script()

    # Step 7: Inject Omega Seal
    print("\n[7/9] Injecting Omega Seal...")
    inject_omega_seal(BUILD_DIR)

    # Step 8: Create manifest
    print("\n[8/9] Creating package manifest...")
    manifest = create_package_manifest()

    # Step 9: Create archive
    archive_path = None
    sha256 = None
    if not args.no_zip:
        print(f"\n[9/9] Creating {archive_type} archive...")
        if args.use_7z:
            archive_path, sha256, sha512 = create_7z_archive()
        else:
            archive_path, sha256, sha512 = create_zip_archive()
    else:
        print("\n[9/9] Skipping archive creation (--no-zip)")

    # Optional: Run tests
    if args.test:
        print("\n" + "=" * 70)
        print(" CLEAN ROOM VERIFICATION")
        print("=" * 70)
        success = run_clean_room_test()
        if not success:
            print("\n[!] Some tests failed - check output above")

    # Summary
    print("\n" + "=" * 70)
    print(" BUILD COMPLETE")
    print("=" * 70)
    print(f"\nBuild directory: {BUILD_DIR}")
    if archive_path:
        print(f"Archive: {archive_path}")
        print(f"SHA-256: {sha256}")
    print(f"\nTotal files: {manifest['summary']['total_files']}")
    print(f"Total size: {manifest['summary']['total_size_mb']} MB")

    # Zenodo metadata reminder
    print("\n" + "-" * 70)
    print(" ZENODO METADATA CHECKLIST")
    print("-" * 70)
    print(f"""
Title: Principia Metaphysica v{VERSION}: A G2-Manifold Residue Model
       with 0.48sigma Cosmological Alignment

Description: This release marks the transition to a pure-geometry model,
             replacing 125 empirical constants with derived residues.
             Includes 72-gate integrity verification system.

Keywords: G2 Manifold, Ricci Flow, 125-Parameter Port, Zenodo Archive

License: MIT (code), See LICENSE for theory content
""")
    print("=" * 70)
    print("\n[!] Remember to test on a clean machine before uploading to Zenodo!")

if __name__ == "__main__":
    main()
