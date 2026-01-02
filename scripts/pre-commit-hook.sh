#!/bin/bash
#
# Pre-commit Hook for Principia Metaphysica v17 Sterile Sovereign
# ================================================================
# This hook enforces sterility before any commit can proceed.
# It runs the DemonLockGuard and AST Sterility Audit.
#
# To install:
#   cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Or run: python scripts/install_hooks.py
#
# Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
#

echo "========================================"
echo " PM v17: PRE-COMMIT STERILITY CHECK"
echo "========================================"

# Find Python executable
PYTHON=""
for py in python3 python py; do
    if command -v $py &> /dev/null; then
        PYTHON=$py
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] Python not found. Skipping sterility check."
    exit 0  # Allow commit but warn
fi

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel)

# 1. Run DemonLockGuard
echo ""
echo "[1/2] Running DemonLockGuard..."
$PYTHON "$REPO_ROOT/core/demon_lock_guard.py" 2>&1

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo " PRE-COMMIT BLOCKED: STERILITY FAILED"
    echo "========================================"
    echo "The DemonLockGuard detected violations."
    echo "Fix the issues before committing."
    echo ""
    echo "To bypass (not recommended):"
    echo "  git commit --no-verify"
    echo "========================================"
    exit 1
fi

# 2. Check for Ghost Literals in staged Python files
echo ""
echo "[2/2] Scanning for Ghost Literals..."

# Get list of staged Python files
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -n "$STAGED_PY" ]; then
    # Check for known Ghost Literals
    GHOST_FOUND=0

    for file in $STAGED_PY; do
        # Skip test files that document ghost literals
        if [[ "$file" == *"test_sterility_audit.py"* ]]; then
            continue
        fi

        # Check for deprecated holonomy (1.280145)
        if grep -q "1\.280145" "$file" 2>/dev/null; then
            echo "[GHOST] Deprecated holonomy 1.280145 found in: $file"
            GHOST_FOUND=1
        fi

        # Check for truncated Sophian Gamma (0.5772 without full precision)
        # Allow 0.57721566490153286 but flag 0.5772 alone
        if grep -E "0\.5772[^1]|0\.5772$" "$file" 2>/dev/null | grep -v "0.57721566490153286" > /dev/null; then
            echo "[GHOST] Truncated Sophian Gamma found in: $file"
            GHOST_FOUND=1
        fi
    done

    if [ $GHOST_FOUND -eq 1 ]; then
        echo ""
        echo "========================================"
        echo " PRE-COMMIT BLOCKED: GHOST LITERALS"
        echo "========================================"
        echo "Use FormulasRegistry values instead of"
        echo "hardcoded magic numbers."
        echo ""
        echo "To bypass (not recommended):"
        echo "  git commit --no-verify"
        echo "========================================"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo " PRE-COMMIT CHECK PASSED"
echo " Manifold is sterile. Commit allowed."
echo "========================================"

exit 0
