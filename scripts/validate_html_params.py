#!/usr/bin/env python3
"""
validate_html_params.py - Validate HTML parameter references against pm-constants-loader.js

This script scans all HTML files for pm-value references and checks if they exist
in the JavaScript constants loader or will resolve correctly.

Usage:
    python scripts/validate_html_params.py
    python scripts/validate_html_params.py --fix  # Suggest fixes

Author: Andrew Keith Watts
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass


@dataclass
class ParamReference:
    """A parameter reference found in HTML."""
    file: str
    line: int
    path: str
    element_type: str  # 'data-pm-value', 'data-category', etc.


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def extract_js_aliases(js_path: Path) -> Dict[str, str]:
    """Extract parameter aliases from pm-constants-loader.js."""
    aliases = {}

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the _parameterAliases object
    alias_match = re.search(r'_parameterAliases:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)
    if alias_match:
        alias_block = alias_match.group(1)
        # Extract key-value pairs
        pairs = re.findall(r"'([^']+)':\s*'([^']+)'", alias_block)
        for key, value in pairs:
            aliases[key.lower()] = value

    return aliases


def extract_hardcoded_values(js_path: Path) -> Set[str]:
    """Extract hardcoded value keys from pm-constants-loader.js."""
    keys = set()

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the _hardcodedValues object
    match = re.search(r'_hardcodedValues:\s*\{([^}]+)\}', content, re.DOTALL)
    if match:
        block = match.group(1)
        # Extract keys
        key_matches = re.findall(r"'([^']+)':", block)
        keys.update(key_matches)

    return keys


def extract_dimension_keys(js_path: Path) -> Set[str]:
    """Extract dimension keys from pm-constants-loader.js."""
    keys = set()

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the dimensions object
    match = re.search(r'dimensions:\s*\{([^}]+)\}', content, re.DOTALL)
    if match:
        block = match.group(1)
        # Extract keys (like D_BULK, D_AFTER_SP2R, etc.)
        key_matches = re.findall(r'([A-Z_0-9]+):', block)
        keys.update(key_matches)

    return keys


def extract_default_named_constants(js_path: Path) -> Set[str]:
    """Extract default named constant keys from pm-constants-loader.js."""
    keys = set()

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the _defaultNamedConstants object
    match = re.search(r'_defaultNamedConstants:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)
    if match:
        block = match.group(1)
        # Extract keys
        key_matches = re.findall(r"'([^']+)':", block)
        keys.update(key_matches)

    return keys


def load_json_params(json_path: Path) -> Set[str]:
    """Load parameter paths from a JSON file."""
    keys = set()

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        def extract_keys(obj, prefix=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    full_key = f"{prefix}.{k}" if prefix else k
                    keys.add(full_key)
                    extract_keys(v, full_key)

        extract_keys(data)
    except Exception as e:
        print(f"  Warning: Could not load {json_path}: {e}")

    return keys


def scan_html_file(file_path: Path) -> List[ParamReference]:
    """Scan an HTML file for parameter references."""
    references = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  Warning: Could not read {file_path}: {e}")
        return references

    for line_num, line in enumerate(lines, 1):
        # data-pm-value="path.to.value"
        for match in re.finditer(r'data-pm-value=["\']([^"\']+)["\']', line):
            references.append(ParamReference(
                file=str(file_path),
                line=line_num,
                path=match.group(1),
                element_type='data-pm-value'
            ))

        # data-category="X" data-param="Y" -> X.Y
        cat_match = re.search(r'data-category=["\']([^"\']+)["\']', line)
        param_match = re.search(r'data-param=["\']([^"\']+)["\']', line)
        if cat_match and param_match:
            path = f"{cat_match.group(1)}.{param_match.group(1)}"
            references.append(ParamReference(
                file=str(file_path),
                line=line_num,
                path=path,
                element_type='data-category+data-param'
            ))

    return references


def check_param_resolvable(
    path: str,
    aliases: Dict[str, str],
    hardcoded: Set[str],
    dimensions: Set[str],
    named_constants: Set[str],
    json_params: Set[str]
) -> Tuple[bool, str]:
    """
    Check if a parameter path will resolve.

    Returns:
        (resolvable: bool, reason: str)
    """
    path_lower = path.lower()

    # Check if it's aliased
    if path_lower in aliases:
        target = aliases[path_lower]
        if target.startswith('_hardcoded.'):
            key = target.replace('_hardcoded.', '')
            if key in hardcoded:
                return True, f"alias -> _hardcoded.{key}"
            return False, f"alias -> _hardcoded.{key} (NOT FOUND in hardcoded)"
        elif target.startswith('_named.'):
            key = target.replace('_named.', '')
            if key in named_constants:
                return True, f"alias -> _named.{key}"
            return False, f"alias -> _named.{key} (NOT FOUND in named constants)"
        else:
            # Points to another path
            return True, f"alias -> {target}"

    # Check dimensions
    if path.startswith('dimensions.'):
        dim_key = path.split('.')[1].upper()
        if dim_key in dimensions:
            return True, "dimensions built-in"
        return False, f"dimensions.{dim_key} NOT FOUND"

    # Check _hardcoded paths
    if path.startswith('_hardcoded.'):
        key = path.replace('_hardcoded.', '')
        if key in hardcoded:
            return True, "hardcoded value"
        return False, f"_hardcoded.{key} NOT FOUND"

    # Check _named paths
    if path.startswith('_named.'):
        key = path.replace('_named.', '')
        if key in named_constants:
            return True, "named constant"
        return False, f"_named.{key} NOT FOUND"

    # Check JSON parameters (might be in parameters.json or theory_output.json)
    if path in json_params or path.lower() in {p.lower() for p in json_params}:
        return True, "JSON parameter"

    # Check with 'parameters.' prefix
    if f"parameters.{path}" in json_params:
        return True, "JSON parameter (with prefix)"

    # Check common simulation paths
    if path.startswith('simulations.') or path.startswith('validation.') or path.startswith('cosmology.'):
        # These often resolve at runtime from loaded JSON
        return True, "simulation/validation path (runtime)"

    return False, "NOT FOUND in any source"


def main():
    """Run the HTML parameter validation."""
    project_root = get_project_root()

    print("=" * 70)
    print(" HTML PARAMETER VALIDATION")
    print("=" * 70)
    print(f"Project root: {project_root}")
    print()

    # Load JS configuration
    js_path = project_root / 'js' / 'pm-constants-loader.js'
    print(f"Loading JS configuration from {js_path}...")

    aliases = extract_js_aliases(js_path)
    print(f"  Found {len(aliases)} aliases")

    hardcoded = extract_hardcoded_values(js_path)
    print(f"  Found {len(hardcoded)} hardcoded values")

    dimensions = extract_dimension_keys(js_path)
    print(f"  Found {len(dimensions)} dimension keys")

    named_constants = extract_default_named_constants(js_path)
    print(f"  Found {len(named_constants)} named constants")

    # Load JSON parameters
    json_params: Set[str] = set()
    for json_file in ['parameters.json', 'theory_output.json', 'named_constants.json']:
        json_path = project_root / 'AutoGenerated' / json_file
        if json_path.exists():
            params = load_json_params(json_path)
            json_params.update(params)
            print(f"  Loaded {len(params)} keys from {json_file}")

    print()

    # Scan HTML files
    html_files = list(project_root.glob('*.html')) + \
                 list(project_root.glob('Pages/*.html')) + \
                 list(project_root.glob('foundations/*.html')) + \
                 list(project_root.glob('components/*.html'))

    # Exclude Demon Lock packages
    html_files = [f for f in html_files if 'Demon_Lock' not in str(f)]

    print(f"Scanning {len(html_files)} HTML files...")
    print()

    all_refs: List[ParamReference] = []
    for html_file in html_files:
        refs = scan_html_file(html_file)
        all_refs.extend(refs)

    print(f"Found {len(all_refs)} parameter references")
    print()

    # Check each reference
    unresolved: List[Tuple[ParamReference, str]] = []
    resolved_count = 0

    for ref in all_refs:
        resolvable, reason = check_param_resolvable(
            ref.path, aliases, hardcoded, dimensions, named_constants, json_params
        )
        if resolvable:
            resolved_count += 1
        else:
            unresolved.append((ref, reason))

    # Report
    print("=" * 70)
    print(" RESULTS")
    print("=" * 70)
    print(f"  Resolved: {resolved_count}")
    print(f"  Unresolved: {len(unresolved)}")
    print()

    if unresolved:
        print("UNRESOLVED REFERENCES:")
        print("-" * 70)

        # Group by file
        by_file: Dict[str, List[Tuple[ParamReference, str]]] = {}
        for ref, reason in unresolved:
            rel_path = os.path.relpath(ref.file, project_root)
            if rel_path not in by_file:
                by_file[rel_path] = []
            by_file[rel_path].append((ref, reason))

        for file_path, refs in sorted(by_file.items()):
            print(f"\n{file_path}:")
            for ref, reason in refs:
                print(f"  Line {ref.line}: {ref.path}")
                print(f"    Reason: {reason}")

        print()
        print("=" * 70)
        print(f" VERDICT: {len(unresolved)} UNRESOLVED REFERENCES")
        print("=" * 70)

        # Suggest fixes
        if '--fix' in sys.argv:
            print()
            print("SUGGESTED FIXES:")
            print("-" * 70)
            unique_paths = set(ref.path for ref, _ in unresolved)
            for path in sorted(unique_paths):
                print(f"  Add alias: '{path}': '_hardcoded.{path.split('.')[-1]}',")

        return 1

    print("=" * 70)
    print(" VERDICT: ALL REFERENCES RESOLVED")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
