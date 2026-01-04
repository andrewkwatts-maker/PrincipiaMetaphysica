#!/usr/bin/env python3
"""
Link Validation Script for Principia Metaphysica
================================================

Validates all links in visualization pages, checking:
1. Local image files exist
2. GitHub raw URLs are accessible
3. Simulation script mappings are correct

Usage:
    python scripts/validate_links.py
"""

import os
import sys
import json
import re
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from concurrent.futures import ThreadPoolExecutor, as_completed

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# GitHub base URL for simulation code
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/andrewkwatts-maker/PrincipiaMetaphysica/main/"

# Expected image directory
IMAGES_DIR = PROJECT_ROOT / "images"

# Simulation script mapping (from visualization-index.html simMappings)
# This mapping should match the actual simMappings in Pages/visualization-index.html
SIMULATION_MAPPING = {
    "dimensional-reduction-pathway.svg": "simulations/derivations/g2_geometry_derivations.py",
    "g2-manifold.png": "simulations/v16/geometric/g2_geometry_v16_0.py",
    "gauge-fixing-time.png": "simulations/renormalization_group_runner_fixed.py",
    "parameter-space.png": "simulations/v16/neutrino/neutrino_mixing_v16_0.py",
    "octonionic-triality-ckm-pmns.png": "simulations/v16/fermion/ckm_matrix_v16_0.py",
    "ricci-flow-hubble-evolution.png": "simulations/v16/cosmology/dark_energy_thawing_v16_2.py",
    "cosmology-evolution-diagram.png": "simulations/v16/cosmology/s8_suppression_v16_1.py",
    "cmb-power-spectrum.png": "simulations/v16/cosmology/cosmology_intro_v16_0.py",
    "generation-count-consistency.svg": "simulations/v16/fermion/ckm_matrix_v16_0.py",
    "kk-spectrum-2d-grid.png": "simulations/v16/cosmology/cosmology_intro_v16_0.py",
    "cmb-bubble-parameter-space.png": "simulations/v16/cosmology/cosmology_intro_v16_0.py",
    "heterogeneous-brane-structure.svg": "simulations/derivations/g2_geometry_derivations.py",
    "clifford-algebra-structure.png": "simulations/v16/fermion/ckm_matrix_v16_0.py",
    "so10-breaking.png": "simulations/v16/fermion/ckm_matrix_v16_0.py",
    "yukawa-couplings.png": "simulations/v16/fermion/ckm_matrix_v16_0.py",
    "validation-dashboard.svg": "simulations/validation/CERTIFICATES_v16_2.py",
    "swampland-criteria.png": "simulations/v16/cosmology/cosmology_intro_v16_0.py",
    "experimental-signatures.png": "simulations/v16/cosmology/cosmology_intro_v16_0.py",
}


def check_local_image(image_name: str) -> tuple[str, bool, str]:
    """Check if a local image file exists."""
    image_path = IMAGES_DIR / image_name
    if image_path.exists():
        return image_name, True, f"Found: {image_path}"
    return image_name, False, f"MISSING: {image_path}"


def check_github_url(url: str, timeout: int = 10) -> tuple[str, bool, str]:
    """Check if a GitHub raw URL is accessible."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                return url, True, f"OK (200)"
            return url, False, f"HTTP {response.status}"
    except HTTPError as e:
        return url, False, f"HTTP {e.code}: {e.reason}"
    except URLError as e:
        return url, False, f"URL Error: {e.reason}"
    except Exception as e:
        return url, False, f"Error: {str(e)}"


def check_simulation_exists(script_path: str) -> tuple[str, bool, str]:
    """Check if a simulation script exists locally."""
    full_path = PROJECT_ROOT / script_path
    if full_path.exists():
        return script_path, True, f"Found: {full_path}"
    return script_path, False, f"MISSING: {full_path}"


def scan_visualization_index() -> dict:
    """Scan visualization-index.html for all image references."""
    viz_index = PROJECT_ROOT / "Pages" / "visualization-index.html"
    if not viz_index.exists():
        print(f"ERROR: {viz_index} not found")
        return {}

    content = viz_index.read_text(encoding="utf-8")

    # Find all image sources in viz-card elements
    # Pattern: <img src="../images/filename.png"
    img_pattern = r'<img[^>]+src=["\']\.\.\/images\/([^"\']+)["\']'
    images = re.findall(img_pattern, content)

    return {"images": list(set(images))}


def validate_all():
    """Run all validation checks."""
    print("=" * 60)
    print("Principia Metaphysica Link Validation")
    print("=" * 60)

    results = {
        "local_images": {"passed": 0, "failed": 0, "details": []},
        "github_urls": {"passed": 0, "failed": 0, "details": []},
        "simulations": {"passed": 0, "failed": 0, "details": []},
    }

    # 1. Scan visualization-index.html for images
    print("\n[1/3] Scanning visualization-index.html for images...")
    viz_data = scan_visualization_index()
    images = viz_data.get("images", [])
    print(f"      Found {len(images)} unique images")

    # 2. Check local images
    print("\n[2/3] Checking local image files...")
    for img in images:
        name, exists, msg = check_local_image(img)
        if exists:
            results["local_images"]["passed"] += 1
            print(f"      [OK] {name}")
        else:
            results["local_images"]["failed"] += 1
            results["local_images"]["details"].append(msg)
            print(f"      [FAIL] {name}")

    # 3. Check simulation script mappings
    print("\n[3/3] Checking simulation script mappings...")
    unique_scripts = set(SIMULATION_MAPPING.values())
    for script in unique_scripts:
        name, exists, msg = check_simulation_exists(script)
        if exists:
            results["simulations"]["passed"] += 1
            print(f"      [OK] {name}")
        else:
            results["simulations"]["failed"] += 1
            results["simulations"]["details"].append(msg)
            print(f"      [FAIL] {name}")

    # 4. Optionally check GitHub URLs (slower, requires network)
    check_github = "--check-github" in sys.argv
    if check_github:
        print("\n[BONUS] Checking GitHub raw URLs (this may take a moment)...")
        urls_to_check = [
            GITHUB_RAW_BASE + script for script in unique_scripts
        ]
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(check_github_url, url): url for url in urls_to_check}
            for future in as_completed(futures):
                url, success, msg = future.result()
                short_url = url.replace(GITHUB_RAW_BASE, "")
                if success:
                    results["github_urls"]["passed"] += 1
                    print(f"      [OK] {short_url}")
                else:
                    results["github_urls"]["failed"] += 1
                    results["github_urls"]["details"].append(f"{short_url}: {msg}")
                    print(f"      [FAIL] {short_url}: {msg}")

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    total_passed = sum(r["passed"] for r in results.values())
    total_failed = sum(r["failed"] for r in results.values())

    print(f"\nLocal Images:     {results['local_images']['passed']} passed, {results['local_images']['failed']} failed")
    print(f"Simulation Files: {results['simulations']['passed']} passed, {results['simulations']['failed']} failed")
    if check_github:
        print(f"GitHub URLs:      {results['github_urls']['passed']} passed, {results['github_urls']['failed']} failed")

    print(f"\nTOTAL: {total_passed} passed, {total_failed} failed")

    if total_failed > 0:
        print("\n" + "-" * 60)
        print("FAILURES:")
        for category, data in results.items():
            if data["details"]:
                print(f"\n  {category}:")
                for detail in data["details"]:
                    print(f"    - {detail}")

    print("\n" + "=" * 60)
    status = "PASS" if total_failed == 0 else "FAIL"
    print(f"STATUS: {status}")
    print("=" * 60)

    return total_failed == 0


if __name__ == "__main__":
    success = validate_all()
    sys.exit(0 if success else 1)
