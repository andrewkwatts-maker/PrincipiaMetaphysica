#!/usr/bin/env python3
"""
Resume Gemini v24.2 Consultation - Complete Missing Phases
===========================================================

This script completes the missing phases 2 and 5 from the rate-limited consultation.
Uses Gemini 1.5 Flash model with higher rate limits.

Usage:
    python scripts/gemini_v24_2_consult_resume.py
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Setup
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                os.environ.setdefault(_key.strip(), _val.strip())


def call_gemini(api_key: str, prompt: str, model: str = "gemini-1.5-pro") -> str:
    """Simple Gemini API call with REST."""
    import urllib.request
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent?key={api_key}")
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 8192,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    print()
    print("=" * 80)
    print("  Resume Gemini v24.2 Consultation - Complete Missing Phases")
    print("=" * 80)
    print()

    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[ERROR] No API key found")
        sys.exit(1)

    # Load review request
    review_path = PROJECT_ROOT / "GEMINI_V24_2_RIGOR_REVIEW.md"
    with open(review_path, 'r', encoding='utf-8') as f:
        review_request = f.read()

    print(f"  Model: gemini-1.5-pro")
    print()

    # PHASE 2: Components 1-5
    print("-" * 80)
    print("  PHASE 2: Components 1-5 (RETRY)")
    print("-" * 80)

    components_1_5_start = review_request.find("## COMPONENT 1:")
    components_1_5_end = review_request.find("## COMPONENT 6:")
    components_1_5_text = review_request[components_1_5_start:components_1_5_end]

    phase2_prompt = f"""You are reviewing the v24.2 rigor upgrade for Principia Metaphysica, a G2 manifold-based physics unification framework.

Evaluate components 1-5:

{components_1_5_text}

For EACH component (1-5), provide:

1. **Scientific Merit Score** (1-10)
2. **Implementation Quality Score** (1-10)
3. **Publication Impact**: STRONGLY POSITIVE / POSITIVE / NEUTRAL / NEGATIVE / STRONGLY NEGATIVE
4. **Priority**: CRITICAL / IMPORTANT / NICE / DEFER / SKIP
5. **Specific Recommendations**
6. **Red Flags**

Format:

### COMPONENT 1: [Title]
Scientific Merit: X/10
Implementation Quality: X/10
Publication Impact: [rating]
Priority: [priority]
Recommendations:
- [rec 1]
Red Flags:
- [flag 1]
"""

    print("  Calling Gemini API...")
    phase2_response = call_gemini(api_key, phase2_prompt)
    print(f"  Response: {len(phase2_response)} chars")
    print()

    # Save immediately
    phase2_path = PROJECT_ROOT / "GEMINI_V24_2_PHASE2_COMPONENTS_1_5.md"
    with open(phase2_path, 'w', encoding='utf-8') as f:
        f.write(f"# Phase 2: Components 1-5 Review\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()[:19]}\n")
        f.write(f"**Model**: gemini-1.5-pro\n\n")
        f.write("---\n\n")
        f.write(phase2_response)
    print(f"  Saved to: {phase2_path}")
    print()

    # Wait before next call
    print("  Waiting 15 seconds before next API call...")
    time.sleep(15)

    # PHASE 5: Critical Methodological Questions
    print("-" * 80)
    print("  PHASE 5: Critical Methodological Questions (RETRY)")
    print("-" * 80)

    critical_start = review_request.find("## CRITICAL METHODOLOGICAL QUESTIONS")
    critical_end = review_request.find("## REQUEST FOR DETAILED FEEDBACK")
    critical_text = review_request[critical_start:critical_end]

    phase5_prompt = f"""You are reviewing the v24.2 rigor upgrade for Principia Metaphysica.

Address these 3 critical methodological questions:

{critical_text}

For each question, provide:
- Assessment of arguments FOR and AGAINST
- Your verdict on which is correct
- Specific evidence/reasoning
- Recommendation for the paper

Be thorough and honest.
"""

    print("  Calling Gemini API...")
    phase5_response = call_gemini(api_key, phase5_prompt)
    print(f"  Response: {len(phase5_response)} chars")
    print()

    # Save
    phase5_path = PROJECT_ROOT / "GEMINI_V24_2_PHASE5_CRITICAL_QUESTIONS.md"
    with open(phase5_path, 'w', encoding='utf-8') as f:
        f.write(f"# Phase 5: Critical Methodological Questions\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()[:19]}\n")
        f.write(f"**Model**: gemini-1.5-pro\n\n")
        f.write("---\n\n")
        f.write(phase5_response)
    print(f"  Saved to: {phase5_path}")
    print()

    print("=" * 80)
    print("  COMPLETION SUCCESSFUL")
    print("=" * 80)
    print()
    print("  Results saved:")
    print(f"    - {phase2_path}")
    print(f"    - {phase5_path}")
    print()
    print("  To view full consultation:")
    print("    - GEMINI_V24_2_CONSULTATION_RESULTS.md (phases 1, 3, 4, 6)")
    print("    - GEMINI_V24_2_PHASE2_COMPONENTS_1_5.md (phase 2)")
    print("    - GEMINI_V24_2_PHASE5_CRITICAL_QUESTIONS.md (phase 5)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
