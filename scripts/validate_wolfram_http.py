#!/usr/bin/env python3
"""
Simple Wolfram Alpha validation using HTTP API directly.
Validates key PM formulas and generates wolfram_results.json.
"""

import json
import urllib.request
import urllib.parse
import time
import sys
import os

# Add simulations to path for secrets
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulations'))

try:
    from secrets_config import WOLFRAM_APP_ID
except ImportError:
    WOLFRAM_APP_ID = None
    print("No API key found in secrets_config.py")

# Key PM formulas to validate
PM_FORMULAS = [
    {
        "id": "k_gimel",
        "name": "Warp Factor k_gimel",
        "formula": "k_gimel = b3/2 + 1/pi",
        "query": "24/2 + 1/pi",
        "expected": 12.318
    },
    {
        "id": "c_kaf",
        "name": "Flux Constraint C_kaf",
        "formula": "C_kaf = b3(b3-7)/(b3-9)",
        "query": "24 * (24-7) / (24-9)",
        "expected": 27.2
    },
    {
        "id": "chi_eff",
        "name": "Effective Euler Characteristic",
        "formula": "chi_eff = 6 * b3",
        "query": "6 * 24",
        "expected": 144
    },
    {
        "id": "alpha_gut",
        "name": "GUT Coupling Inverse",
        "formula": "1/alpha_GUT = b3 + 1/10 + 1/(5*b3)",
        "query": "24 + 1/10 + 1/(5*24)",
        "expected": 24.108
    },
    {
        "id": "w0",
        "name": "Dark Energy w0",
        "formula": "w0 = -(b3-1)/b3 = -23/24",
        "query": "-23/24",
        "expected": -0.9583
    },
    {
        "id": "n_gen",
        "name": "Number of Generations",
        "formula": "N_gen = b3/8",
        "query": "24/8",
        "expected": 3
    },
    {
        "id": "theta_12",
        "name": "Solar Mixing Angle Base",
        "formula": "theta_12_base = arcsin(sqrt(1/3))",
        "query": "arcsin(sqrt(1/3)) in degrees",
        "expected": 35.26,
        "note": "Base tribimaximal angle; PM adds epsilon correction"
    },
    {
        "id": "theta_23",
        "name": "Atmospheric Mixing Angle",
        "formula": "theta_23 = 45 + 4.75",
        "query": "45 + 4.75",
        "expected": 49.75
    },
    {
        "id": "theta_w",
        "name": "Weinberg Angle (GUT)",
        "formula": "sin^2(theta_W) = 3/8",
        "query": "3/8",
        "expected": 0.375
    },
    {
        "id": "anomaly",
        "name": "Anomaly Correction",
        "formula": "1 - 1/b3^2 = 575/576",
        "query": "1 - 1/576",
        "expected": 0.99826
    }
]


def query_wolfram(query_string: str, app_id: str) -> dict:
    """Query Wolfram Alpha API via HTTP."""
    encoded_query = urllib.parse.quote(query_string)
    url = f'http://api.wolframalpha.com/v2/query?appid={app_id}&input={encoded_query}&output=json'

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        return {"error": str(e)}


def extract_result(response: dict) -> tuple:
    """Extract result value from Wolfram response."""
    if "error" in response:
        return None, response["error"]

    queryresult = response.get("queryresult", {})
    if not queryresult.get("success", False):
        return None, "Query failed"

    pods = queryresult.get("pods", [])
    for pod in pods:
        title = pod.get("title", "").lower()
        if title in ["result", "decimal approximation", "exact result"]:
            subpods = pod.get("subpods", [])
            if subpods:
                text = subpods[0].get("plaintext", "")
                if text:
                    return text, None

    # If no result pod, try to get any value
    for pod in pods:
        subpods = pod.get("subpods", [])
        for subpod in subpods:
            text = subpod.get("plaintext", "")
            if text and any(c.isdigit() for c in text):
                return text, None

    return None, "No result found"


def parse_numeric(text: str) -> float:
    """Parse numeric value from Wolfram result text."""
    import re
    import math

    if not text:
        return None

    # Clean up the text - remove extra info in parentheses
    text = re.sub(r'\s*\([^)]*\)', '', text).strip()

    # Handle simple numbers
    try:
        return float(text)
    except ValueError:
        pass

    # Handle fractions like "-23/24" or "136/5"
    fraction_match = re.match(r'^(-?\d+)/(\d+)$', text)
    if fraction_match:
        try:
            num = float(fraction_match.group(1))
            den = float(fraction_match.group(2))
            return num / den
        except:
            pass

    # Handle expressions like "12 + 1/π"
    if '+' in text and 'π' in text:
        # Try to evaluate: extract integer part and pi part
        parts = text.split('+')
        try:
            int_part = float(parts[0].strip())
            # Check if second part is fraction with pi
            pi_part = parts[1].strip()
            if '/π' in pi_part:
                num_match = re.search(r'(\d+)/π', pi_part)
                if num_match:
                    pi_frac = float(num_match.group(1)) / math.pi
                    return int_part + pi_frac
        except:
            pass

    # Handle "approximately" prefix
    if text.startswith('~') or text.startswith('≈'):
        try:
            return float(text[1:].strip())
        except:
            pass

    # Handle degree symbol: "35.26°"
    degree_match = re.match(r'^([\d.]+)°', text)
    if degree_match:
        try:
            return float(degree_match.group(1))
        except:
            pass

    # Extract first number
    match = re.search(r'-?[\d.]+', text)
    if match:
        try:
            return float(match.group())
        except:
            pass

    return None


def validate_all(app_id: str) -> list:
    """Validate all PM formulas."""
    results = []

    for formula in PM_FORMULAS:
        print(f"Validating: {formula['name']}...")

        response = query_wolfram(formula["query"], app_id)
        result_text, error = extract_result(response)

        entry = {
            "id": formula["id"],
            "name": formula["name"],
            "formula": formula["formula"],
            "query": formula["query"],
            "expected": formula["expected"],
            "wolfram_result": result_text,
            "wolfram_link": f"https://www.wolframalpha.com/input/?i={urllib.parse.quote(formula['query'])}"
        }

        if error:
            entry["status"] = "ERROR"
            entry["error"] = error
            entry["match"] = False
        elif result_text:
            wolfram_numeric = parse_numeric(result_text)
            if wolfram_numeric is not None:
                rel_error = abs(wolfram_numeric - formula["expected"]) / max(abs(formula["expected"]), 1e-10)
                entry["wolfram_numeric"] = wolfram_numeric
                entry["relative_error"] = rel_error
                if rel_error < 0.001:
                    entry["status"] = "MATCH"
                    entry["match"] = True
                elif rel_error < 0.01:
                    entry["status"] = "CLOSE"
                    entry["match"] = True
                else:
                    entry["status"] = "MISMATCH"
                    entry["match"] = False
            else:
                entry["status"] = "PARSE_ERROR"
                entry["match"] = False
        else:
            entry["status"] = "NO_RESULT"
            entry["match"] = False

        results.append(entry)
        print(f"  -> {entry['status']}: {result_text}")

        # Rate limit
        time.sleep(1)

    return results


def main():
    if not WOLFRAM_APP_ID:
        print("ERROR: No Wolfram App ID configured")
        sys.exit(1)

    print("=" * 60)
    print("PRINCIPIA METAPHYSICA - Wolfram Alpha Validation")
    print("=" * 60)
    print()

    results = validate_all(WOLFRAM_APP_ID)

    # Summary
    matches = sum(1 for r in results if r.get("match", False))
    print()
    print("=" * 60)
    print(f"VALIDATION COMPLETE: {matches}/{len(results)} validated")
    print("=" * 60)

    # Save results
    output_path = os.path.join(os.path.dirname(__file__), '..', 'AutoGenerated', 'wolfram_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "version": "16.2",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total": len(results),
            "validated": matches,
            "results": results
        }, f, indent=2)

    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
