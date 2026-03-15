#!/usr/bin/env python3
"""
Gemini v24.2 Rigor Upgrade Consultation Script
===============================================

Custom consultation script for systematic peer review of the v24.2 rigor upgrade package.
Sends GEMINI_V24_2_RIGOR_REVIEW.md to Gemini and collects structured feedback.

Features:
  - Chunked consultation to handle token limits
  - Component-by-component evaluation
  - Priority ranking
  - Synthesis of critical methodological questions
  - Structured output to GEMINI_V24_2_CONSULTATION_RESULTS.md

Usage:
    python scripts/gemini_consult.py

Environment:
    GEMINI_API_KEY or GOOGLE_API_KEY must be set in .env file

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env file for API key
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                os.environ.setdefault(_key.strip(), _val.strip())


# ─── Gemini Client ──────────────────────────────────────────────────────────

class GeminiClient:
    """Wrapper for Google Gemini API calls with REST fallback."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self._use_rest = True  # Always use REST for simplicity

    def _generate_rest(self, prompt: str, max_tokens: int = 8192) -> str:
        """Call Gemini via REST API (no SDK needed)."""
        import urllib.request
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{self.model}:generateContent?key={self.api_key}")
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 40
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

    def generate(self, prompt: str, max_retries: int = 3, max_tokens: int = 8192) -> str:
        """Send prompt to Gemini and return text response."""
        for attempt in range(max_retries):
            try:
                return self._generate_rest(prompt, max_tokens)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    print(f"  [RETRY] Gemini error: {e}, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise RuntimeError(f"Gemini API failed after {max_retries} attempts: {e}")


# ─── Consultation Pipeline ──────────────────────────────────────────────────

def load_review_request() -> str:
    """Load the full GEMINI_V24_2_RIGOR_REVIEW.md content."""
    path = PROJECT_ROOT / "GEMINI_V24_2_RIGOR_REVIEW.md"
    if not path.exists():
        raise FileNotFoundError(f"Review request not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def run_consultation(client: GeminiClient) -> Dict[str, Any]:
    """
    Run the full v24.2 consultation process.

    Returns structured results dict.
    """
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "model": client.model,
            "version": "v24.2",
        },
        "component_reviews": [],
        "synthesis": {},
        "critical_questions": {},
        "overall_recommendation": "",
        "priority_ranking": [],
        "raw_responses": []
    }

    print("=" * 80)
    print("  GEMINI v24.2 RIGOR UPGRADE CONSULTATION")
    print("=" * 80)
    print()

    # Load the full review request
    review_request = load_review_request()
    print(f"  Loaded review request: {len(review_request)} characters")
    print()

    # PHASE 1: Initial Overview and Context Setting
    print("─" * 80)
    print("  PHASE 1: Initial Overview")
    print("─" * 80)

    phase1_prompt = f"""You are reviewing a comprehensive rigor upgrade package for the Principia Metaphysica theoretical physics framework.

This framework proposes a G2 manifold-based unification deriving all Standard Model parameters from topology.

The v24.2 upgrade contains 10 major components addressing peer review concerns.

I will ask you to evaluate each component systematically, then provide:
1. Priority ranking (1-10)
2. Overall recommendation (A/B/C/D/E)
3. Assessment of 3 critical methodological questions

First, here is the EXECUTIVE SUMMARY section:

{review_request[:2000]}

Please provide a brief initial assessment: What is your overall impression of this upgrade package? What are your initial concerns or questions?

Respond in 3-4 paragraphs.
"""

    phase1_response = client.generate(phase1_prompt, max_tokens=2048)
    results["raw_responses"].append({
        "phase": "1_overview",
        "response": phase1_response
    })
    print(f"  Response received ({len(phase1_response)} chars)")
    print()
    time.sleep(2)

    # PHASE 2: Component-by-Component Reviews (Components 1-5)
    print("─" * 80)
    print("  PHASE 2: Components 1-5 Reviews")
    print("─" * 80)

    # Extract components 1-5 from review_request
    components_1_5_start = review_request.find("## COMPONENT 1:")
    components_1_5_end = review_request.find("## COMPONENT 6:")
    components_1_5_text = review_request[components_1_5_start:components_1_5_end]

    phase2_prompt = f"""Now let's evaluate the first 5 components in detail.

{components_1_5_text}

For EACH component (1-5), please provide:

1. **Scientific Merit Score** (1-10, 10=highest)
2. **Implementation Quality Score** (1-10, 10=best)
3. **Publication Impact**: STRONGLY POSITIVE / POSITIVE / NEUTRAL / NEGATIVE / STRONGLY NEGATIVE
4. **Priority**: CRITICAL / IMPORTANT / NICE / DEFER / SKIP
5. **Specific Recommendations**: What to change, if anything
6. **Red Flags**: Any concerns or risks

Format your response as:

### COMPONENT 1: [Title]
Scientific Merit: [score]/10
Implementation Quality: [score]/10
Publication Impact: [rating]
Priority: [priority]
Recommendations: [bullet points]
Red Flags: [bullet points]

[Repeat for components 2-5]
"""

    phase2_response = client.generate(phase2_prompt, max_tokens=8192)
    results["raw_responses"].append({
        "phase": "2_components_1_5",
        "response": phase2_response
    })
    print(f"  Response received ({len(phase2_response)} chars)")
    print()
    time.sleep(10)  # Longer delay to avoid rate limits

    # PHASE 3: Component-by-Component Reviews (Components 6-10)
    print("─" * 80)
    print("  PHASE 3: Components 6-10 Reviews")
    print("─" * 80)

    components_6_10_start = review_request.find("## COMPONENT 6:")
    components_6_10_end = review_request.find("## SYNTHESIS QUESTIONS")
    components_6_10_text = review_request[components_6_10_start:components_6_10_end]

    phase3_prompt = f"""Now let's evaluate components 6-10.

{components_6_10_text}

For EACH component (6-10), please provide:

1. **Scientific Merit Score** (1-10)
2. **Implementation Quality Score** (1-10)
3. **Publication Impact**: STRONGLY POSITIVE / POSITIVE / NEUTRAL / NEGATIVE / STRONGLY NEGATIVE
4. **Priority**: CRITICAL / IMPORTANT / NICE / DEFER / SKIP
5. **Specific Recommendations**
6. **Red Flags**

Use the same format as before.
"""

    phase3_response = client.generate(phase3_prompt, max_tokens=8192)
    results["raw_responses"].append({
        "phase": "3_components_6_10",
        "response": phase3_response
    })
    print(f"  Response received ({len(phase3_response)} chars)")
    print()
    time.sleep(10)  # Longer delay

    # PHASE 4: Synthesis and Priority Ranking
    print("─" * 80)
    print("  PHASE 4: Synthesis and Priority Ranking")
    print("─" * 80)

    synthesis_start = review_request.find("## SYNTHESIS QUESTIONS")
    synthesis_end = review_request.find("## CRITICAL METHODOLOGICAL QUESTIONS")
    synthesis_text = review_request[synthesis_start:synthesis_end]

    phase4_prompt = f"""Based on your component reviews, please answer these synthesis questions:

{synthesis_text}

Provide:
1. List of which components genuinely strengthen the framework
2. List of which components add complexity without value
3. List of which components carry risk
4. **Priority ranking (1=highest, 10=lowest)** as a numbered list
5. **Overall recommendation**: Choose A, B, C, D, or E and justify
6. **Biggest risk**: Which component most likely to backfire?
7. **Biggest opportunity**: Which component adds most credibility?
8. **Timeline recommendation**: All at once / Phased / Selective / ArXiv first
"""

    phase4_response = client.generate(phase4_prompt, max_tokens=8192)
    results["raw_responses"].append({
        "phase": "4_synthesis",
        "response": phase4_response
    })
    print(f"  Response received ({len(phase4_response)} chars)")
    print()
    time.sleep(10)  # Longer delay

    # PHASE 5: Critical Methodological Questions
    print("─" * 80)
    print("  PHASE 5: Critical Methodological Questions")
    print("─" * 80)

    critical_start = review_request.find("## CRITICAL METHODOLOGICAL QUESTIONS")
    critical_end = review_request.find("## REQUEST FOR DETAILED FEEDBACK")
    critical_text = review_request[critical_start:critical_end]

    phase5_prompt = f"""Now address these 3 critical methodological questions in depth:

{critical_text}

For each question, provide:
- Your assessment of the arguments FOR and AGAINST
- Your verdict on which interpretation is correct
- Specific evidence or reasoning
- Recommendation for how to handle in the paper

Be thorough and honest. These are the most important questions for publication viability.
"""

    phase5_response = client.generate(phase5_prompt, max_tokens=8192)
    results["raw_responses"].append({
        "phase": "5_critical_questions",
        "response": phase5_response
    })
    print(f"  Response received ({len(phase5_response)} chars)")
    print()
    time.sleep(10)  # Longer delay

    # PHASE 6: Final Verdict
    print("─" * 80)
    print("  PHASE 6: Final Verdict")
    print("─" * 80)

    phase6_prompt = f"""Based on everything discussed, provide your final verdict:

1. **Is v24.2 upgrade wise or premature?**
2. **Should the paper go to arXiv first in current v24.1 state?**
3. **What single change would most improve submission prospects?**
4. **Overall grade for the upgrade package**: A+ to F
5. **Your confidence level in this assessment**: High / Medium / Low
6. **Top 3 action items** for the author

Be direct and actionable.
"""

    phase6_response = client.generate(phase6_prompt, max_tokens=4096)
    results["raw_responses"].append({
        "phase": "6_final_verdict",
        "response": phase6_response
    })
    print(f"  Response received ({len(phase6_response)} chars)")
    print()

    return results


def format_markdown_report(results: Dict[str, Any]) -> str:
    """Format consultation results as markdown report."""
    lines = [
        "# Gemini v24.2 Rigor Upgrade Consultation Results",
        "",
        f"**Date**: {results['metadata']['timestamp'][:10]}",
        f"**Model**: {results['metadata']['model']}",
        f"**Version**: {results['metadata']['version']}",
        "",
        "---",
        "",
    ]

    # Add each phase response
    for i, resp in enumerate(results["raw_responses"], 1):
        phase_name = resp["phase"].replace("_", " ").title()
        lines.append(f"## {phase_name}")
        lines.append("")
        lines.append(resp["response"])
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Consultation Complete")
    lines.append("")
    lines.append(f"Generated: {results['metadata']['timestamp']}")
    lines.append("")

    return "\n".join(lines)


# ─── Main Entry Point ───────────────────────────────────────────────────────

def main():
    print()
    print("=" * 80)
    print("  Principia Metaphysica — Gemini v24.2 Rigor Upgrade Consultation")
    print("=" * 80)
    print()

    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[ERROR] No Gemini API key found.")
        print("  Set GEMINI_API_KEY or GOOGLE_API_KEY in .env file.")
        sys.exit(1)

    print(f"  API Key: {api_key[:20]}... (loaded from .env)")
    print()

    # Initialize client
    client = GeminiClient(api_key, model="gemini-2.0-flash")
    print(f"  Model: {client.model}")
    print()

    # Run consultation
    try:
        results = run_consultation(client)
    except Exception as e:
        print()
        print(f"[ERROR] Consultation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Save structured results as JSON
    json_path = PROJECT_ROOT / "GEMINI_V24_2_CONSULTATION_RESULTS.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print(f"  Structured results saved: {json_path}")

    # Save formatted markdown report
    md_path = PROJECT_ROOT / "GEMINI_V24_2_CONSULTATION_RESULTS.md"
    markdown = format_markdown_report(results)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"  Markdown report saved:   {md_path}")
    print()

    # Print summary
    print("=" * 80)
    print("  CONSULTATION COMPLETE")
    print("=" * 80)
    print()
    print(f"  Total phases: {len(results['raw_responses'])}")
    print(f"  Total response length: {sum(len(r['response']) for r in results['raw_responses'])} chars")
    print()
    print("  Next steps:")
    print("    1. Review GEMINI_V24_2_CONSULTATION_RESULTS.md")
    print("    2. Extract priority ranking and recommendations")
    print("    3. Implement highest-priority components first")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
