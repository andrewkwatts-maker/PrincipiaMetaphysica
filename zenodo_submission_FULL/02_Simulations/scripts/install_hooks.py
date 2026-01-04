#!/usr/bin/env python3
"""
Install Git Hooks for Principia Metaphysica v17
================================================
Installs the pre-commit sterility enforcement hook.

Usage:
    python scripts/install_hooks.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import shutil
import stat
import sys
from pathlib import Path


def install_pre_commit_hook():
    """Install the pre-commit hook into .git/hooks/"""

    # Get paths
    repo_root = Path(__file__).parent.parent
    hook_source = repo_root / "scripts" / "pre-commit-hook.sh"
    hooks_dir = repo_root / ".git" / "hooks"
    hook_dest = hooks_dir / "pre-commit"

    # Check source exists
    if not hook_source.exists():
        print(f"[ERROR] Hook source not found: {hook_source}")
        return False

    # Check .git/hooks exists
    if not hooks_dir.exists():
        print(f"[ERROR] Git hooks directory not found: {hooks_dir}")
        print("       Are you in a git repository?")
        return False

    # Check if hook already exists
    if hook_dest.exists():
        print(f"[INFO] Pre-commit hook already exists: {hook_dest}")
        response = input("       Overwrite? [y/N]: ").strip().lower()
        if response != 'y':
            print("       Skipping installation.")
            return True

    # Copy hook
    try:
        shutil.copy2(hook_source, hook_dest)

        # Make executable (Unix)
        if sys.platform != 'win32':
            hook_dest.chmod(hook_dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        print(f"[OK] Pre-commit hook installed: {hook_dest}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to install hook: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print(" PRINCIPIA METAPHYSICA v17 - GIT HOOKS INSTALLER")
    print("=" * 60)

    success = install_pre_commit_hook()

    if success:
        print("\n[OK] Git hooks installed successfully!")
        print("     The pre-commit hook will enforce sterility on every commit.")
        print("     Use 'git commit --no-verify' to bypass (not recommended).")
    else:
        print("\n[WARN] Some hooks failed to install.")
        sys.exit(1)


if __name__ == "__main__":
    main()
