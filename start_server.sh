#!/bin/bash
# Start local web server for testing Principia Metaphysica
# Copyright (c) 2025 Andrew Keith Watts

echo "========================================"
echo "Principia Metaphysica - Local Server"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.x"
    exit 1
fi

echo "Starting local web server on port 8000..."
echo ""
echo "Open your browser to:"
echo "  - Main site: http://localhost:8000/"
echo "  - References: http://localhost:8000/Pages/references.html"
echo "  - Test page: http://localhost:8000/test_references_page.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m http.server 8000
