#!/usr/bin/env python3
"""
Simple HTTP Server for Principia Metaphysica
=============================================

Run this script to view the website locally. Opens in your default browser.

Usage:
    python serve.py
    python serve.py --port 8080

The server will start and automatically open the website in your browser.
Press Ctrl+C to stop the server.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import http.server
import socketserver
import webbrowser
import sys
import os
from pathlib import Path

# Default port
PORT = 8000

# Parse command line arguments
if len(sys.argv) > 1:
    if sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        sys.exit(0)
    elif sys.argv[1] == '--port' and len(sys.argv) > 2:
        PORT = int(sys.argv[2])
    else:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}")
            sys.exit(1)

# Change to the script's directory
os.chdir(Path(__file__).parent)

# Create handler with CORS headers for local development
class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress verbose logging, only show important messages
        if '200' not in str(args):
            print(f"  {args[0]}")

# Find available port if default is in use
def find_available_port(start_port):
    import socket
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return start_port

PORT = find_available_port(PORT)

# Start server
print("=" * 60)
print("  PRINCIPIA METAPHYSICA - Local Server")
print("=" * 60)
print(f"\n  Starting server at http://localhost:{PORT}")
print(f"  Serving files from: {os.getcwd()}")
print("\n  Press Ctrl+C to stop the server\n")
print("=" * 60)

with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    # Open browser
    url = f"http://localhost:{PORT}/index.html"
    print(f"\n  Opening: {url}\n")
    webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Server stopped.")
        sys.exit(0)
