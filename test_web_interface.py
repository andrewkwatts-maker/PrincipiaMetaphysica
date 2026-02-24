#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Principia Metaphysica - Web Interface Test & Validation Script
===============================================================

Tests the web interface to ensure all pages load correctly and
data files are accessible via HTTP server.

Usage:
    python test_web_interface.py

This script will:
1. Start a local HTTP server on port 8001
2. Test all HTML pages load correctly
3. Verify JSON data files are accessible
4. Check JavaScript file loading
5. Generate a validation report

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import http.server
import socketserver
import threading
import time
import urllib.request
import urllib.error
import json
import sys
import io
from pathlib import Path
from typing import List, Tuple, Dict

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Test configuration
TEST_PORT = 8002  # Changed from 8001 to avoid conflicts
BASE_URL = f"http://localhost:{TEST_PORT}"

# ANSI color codes for terminal output (disabled on Windows for compatibility)
GREEN = ""
RED = ""
YELLOW = ""
BLUE = ""
RESET = ""


class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with CORS and minimal logging."""

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress all logging
        pass


def start_test_server(port: int) -> socketserver.TCPServer:
    """Start HTTP server on specified port in background thread."""
    handler = QuietHTTPHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(1)  # Give server time to start
    return httpd


def test_url(url: str, expected_content: str = None) -> Tuple[bool, str]:
    """
    Test if URL loads successfully.

    Args:
        url: URL to test
        expected_content: Optional string to check for in response

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status != 200:
                return False, f"HTTP {response.status}"

            if expected_content:
                content = response.read().decode('utf-8')
                if expected_content not in content:
                    return False, f"Missing expected content: {expected_content}"

            return True, "OK"
    except urllib.error.URLError as e:
        return False, f"URLError: {e.reason}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def test_json_file(url: str) -> Tuple[bool, str, Dict]:
    """
    Test if JSON file loads and parses correctly.

    Returns:
        Tuple of (success: bool, message: str, data: dict)
    """
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status != 200:
                return False, f"HTTP {response.status}", {}

            data = json.loads(response.read().decode('utf-8'))
            return True, f"OK ({len(str(data))} bytes)", data
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}", {}
    except Exception as e:
        return False, f"Error: {str(e)}", {}


def print_header(text: str):
    """Print formatted section header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text.center(70)}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_test_result(name: str, success: bool, message: str):
    """Print formatted test result."""
    status = "[PASS]" if success else "[FAIL]"
    print(f"  {status}  {name:<40} {message}")


def main():
    """Run all web interface tests."""
    print_header("PRINCIPIA METAPHYSICA - WEB INTERFACE VALIDATION")

    # Change to script directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)

    print(f"  Working Directory: {os.getcwd()}")
    print(f"  Test Server Port: {TEST_PORT}")
    print(f"  Base URL: {BASE_URL}")

    # Start test server
    print(f"\n  Starting HTTP server on port {TEST_PORT}...")
    try:
        httpd = start_test_server(TEST_PORT)
        print(f"  [OK] Server started successfully\n")
    except Exception as e:
        print(f"  [ERROR] FAILED to start server: {e}")
        sys.exit(1)

    # Track results
    total_tests = 0
    passed_tests = 0
    failed_tests = []

    # Test 1: Main HTML Pages
    print_header("TEST 1: HTML Pages")

    html_pages = [
        ("index.html", "Principia Metaphysica"),
        ("Pages/paper.html", "Paper"),
        ("Pages/formulas.html", "Formula"),
        ("Pages/parameters.html", "Parameters"),
        ("Pages/certificates.html", "Certificates"),
        ("Pages/simulations.html", "Simulations"),
        ("Pages/beginners-guide.html", "Beginner"),
        ("Pages/foundations.html", "Foundations"),
        ("Pages/appendices.html", "Appendices"),
    ]

    for page, expected_text in html_pages:
        url = f"{BASE_URL}/{page}"
        success, message = test_url(url, expected_text)
        print_test_result(page, success, message)
        total_tests += 1
        if success:
            passed_tests += 1
        else:
            failed_tests.append((page, message))

    # Test 2: JSON Data Files
    print_header("TEST 2: JSON Data Files")

    json_files = [
        "formulas.json",
        "parameters.json",
        "sections.json",
        "metadata.json",
        "statistics.json",
        "theory_output.json",
        "simulations.json",
        "GATES_74_CERTIFICATES.json",
    ]

    for json_file in json_files:
        url = f"{BASE_URL}/AutoGenerated/{json_file}"
        success, message, data = test_json_file(url)
        print_test_result(json_file, success, message)
        total_tests += 1
        if success:
            passed_tests += 1
        else:
            failed_tests.append((json_file, message))

    # Test 3: JavaScript Files
    print_header("TEST 3: JavaScript Files")

    js_files = [
        "JS/constants.js",
        "JS/formulas.js",
        "JS/parameters.js",
    ]

    for js_file in js_files:
        url = f"{BASE_URL}/{js_file}"
        success, message = test_url(url)
        print_test_result(js_file, success, message)
        total_tests += 1
        if success:
            passed_tests += 1
        else:
            failed_tests.append((js_file, message))

    # Test 4: Visualization Files
    print_header("TEST 4: Visualization Files (Sample)")

    plot_files = [
        "AutoGenerated/plots/certificate_dashboard_v16_2.png",
        "AutoGenerated/plots/figure1_m27_decomposition.png",
        "AutoGenerated/plots/figure2_convergence_scatter.png",
    ]

    for plot_file in plot_files:
        url = f"{BASE_URL}/{plot_file}"
        success, message = test_url(url)
        print_test_result(Path(plot_file).name, success, message)
        total_tests += 1
        if success:
            passed_tests += 1
        else:
            failed_tests.append((plot_file, message))

    # Final Summary
    print_header("VALIDATION SUMMARY")

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"  Total Tests:  {total_tests}")
    print(f"  Passed:       {passed_tests}")
    print(f"  Failed:       {len(failed_tests)}")
    print(f"  Success Rate: {success_rate:.1f}%\n")

    if failed_tests:
        print("  FAILED TESTS:\n")
        for test_name, error_msg in failed_tests:
            print(f"    [X] {test_name}")
            print(f"        {error_msg}\n")

    # Usage Instructions
    print_header("USAGE INSTRUCTIONS")

    if success_rate < 100:
        print("  [WARNING] Some tests failed. This may indicate:\n")
        print("    - Missing data files (run: python simulations/run_all_simulations.py)")
        print("    - Incorrect file paths")
        print("    - Server configuration issues\n")

    print("  To view the web interface properly:\n")
    print("    1. Run the development server:")
    print("       python serve.py\n")
    print("    2. Open your browser to:")
    print("       http://localhost:8000\n")
    print("  [WARNING] DO NOT open HTML files directly with file:// protocol")
    print("  This causes CORS errors preventing JavaScript from loading data.\n")

    # Clean shutdown
    httpd.shutdown()

    # Exit code
    sys.exit(0 if success_rate == 100 else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n  FATAL ERROR: {e}")
        sys.exit(1)
