#!/usr/bin/env python3
"""
Gemini Peer Review System — Principia Metaphysica
===================================================

Automated AI peer review of simulation files using Google Gemini.
Produces standardized JSON ratings and improvement reports.

Features:
  1. Per-simulation file review (formula strength, derivation rigor, etc.)
  2. Whole-paper section consistency review
  3. Improvement suggestions saved as .md files next to simulations
  4. Theory innovation ideas
  5. Auto-fix suggestions for poor results

Usage:
    # Review all simulation files
    python scripts/validation/gemini_peer_review.py --all

    # Review a specific file
    python scripts/validation/gemini_peer_review.py --file simulations/PM/cosmology/dark_energy.py

    # Review with auto-fix suggestions enabled
    python scripts/validation/gemini_peer_review.py --all --auto-fix

    # Review whole paper sections for consistency
    python scripts/validation/gemini_peer_review.py --paper-review

    # Full review (per-file + paper)
    python scripts/validation/gemini_peer_review.py --all --paper-review

Environment:
    GEMINI_API_KEY or GOOGLE_API_KEY must be set.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import os
import sys
import time
import importlib
import inspect
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ─── Gemini Review JSON Schema ─────────────────────────────────────────────

REVIEW_SCHEMA = {
    "simulation_id": "",
    "file_path": "",
    "timestamp": "",
    "model": "",
    "overall_score": 0.0,  # 0-10
    "ratings": {
        "formula_strength": {
            "score": 0.0,  # 0-10
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "derivation_rigor": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "validation_strength": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "section_wording": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "scientific_standing": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "description_accuracy": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "metadata_polish": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "schema_compliance": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "internal_consistency": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        },
        "theory_consistency": {
            "score": 0.0,
            "justification": "",
            "issues": [],
            "suggestions": []
        }
    },
    "improvement_plan": [],
    "innovation_ideas": [],
    "auto_fix_suggestions": [],
    "summary": ""
}

PAPER_REVIEW_SCHEMA = {
    "timestamp": "",
    "model": "",
    "overall_coherence": 0.0,
    "section_flow": {
        "score": 0.0,
        "issues": [],
        "suggestions": []
    },
    "terminology_consistency": {
        "score": 0.0,
        "issues": [],
        "suggestions": []
    },
    "argument_structure": {
        "score": 0.0,
        "issues": [],
        "suggestions": []
    },
    "mathematical_notation": {
        "score": 0.0,
        "issues": [],
        "suggestions": []
    },
    "cross_references": {
        "score": 0.0,
        "issues": [],
        "suggestions": []
    },
    "publication_readiness": {
        "score": 0.0,
        "issues": [],
        "suggestions": []
    },
    "section_reviews": [],
    "innovation_ideas": [],
    "summary": ""
}


# ─── Gemini Client ─────────────────────────────────────────────────────────

class GeminiClient:
    """Wrapper for Google Gemini API calls."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except ImportError:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model)
        return self._client

    def generate(self, prompt: str, max_retries: int = 3) -> str:
        """Send prompt to Gemini and return text response."""
        client = self._get_client()
        for attempt in range(max_retries):
            try:
                try:
                    # New google.genai API
                    response = client.models.generate_content(
                        model=self.model,
                        contents=prompt
                    )
                    return response.text
                except AttributeError:
                    # Old google.generativeai API
                    response = client.generate_content(prompt)
                    return response.text
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    print(f"  [RETRY] Gemini error: {e}, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise RuntimeError(f"Gemini API failed after {max_retries} attempts: {e}")


# ─── Simulation File Analyzer ──────────────────────────────────────────────

class SimulationAnalyzer:
    """Extract metadata from simulation files for review."""

    def __init__(self):
        self.theory_output = self._load_theory_output()

    def _load_theory_output(self) -> Dict:
        path = PROJECT_ROOT / "AutoGenerated" / "theory_output.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract all SSOT metadata from a simulation file."""
        result = {
            "file_path": str(file_path.relative_to(PROJECT_ROOT)),
            "source_code": "",
            "simulation_id": "",
            "formulas": [],
            "parameters": [],
            "section_content": None,
            "certificates": [],
            "learning_materials": [],
            "references": [],
            "self_validation": {},
            "gate_checks": [],
            "has_get_certificates": False,
            "has_get_references": False,
            "has_get_learning_materials": False,
            "has_validate_self": False,
            "has_get_gate_checks": False,
        }

        # Read source code
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                result["source_code"] = f.read()
        except Exception:
            return result

        # Check method presence
        src = result["source_code"]
        result["has_get_certificates"] = "def get_certificates" in src
        result["has_get_references"] = "def get_references" in src
        result["has_get_learning_materials"] = "def get_learning_materials" in src
        result["has_validate_self"] = "def validate_self" in src
        result["has_get_gate_checks"] = "def get_gate_checks" in src

        # Try to import and instantiate
        try:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            # Convert path to module path: strip .py suffix, then replace separators
            stem = str(rel_path)
            if stem.endswith('.py'):
                stem = stem[:-3]
            module_path = stem.replace(os.sep, '.').replace('/', '.')

            mod = importlib.import_module(module_path)

            # Find SimulationBase subclass
            from simulations.base.simulation_base import SimulationBase
            sim_class = None
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, SimulationBase) and obj is not SimulationBase:
                    sim_class = obj
                    break

            if sim_class:
                sim = sim_class()
                result["simulation_id"] = sim.metadata.id

                # Extract formulas
                try:
                    formulas = sim.get_formulas()
                    result["formulas"] = [self._formula_to_dict(f) for f in formulas]
                except Exception:
                    pass

                # Extract parameters
                try:
                    params = sim.get_output_param_definitions()
                    result["parameters"] = [self._param_to_dict(p) for p in params]
                except Exception:
                    pass

                # Extract section content
                try:
                    sc = sim.get_section_content()
                    if sc:
                        result["section_content"] = {
                            "title": getattr(sc, 'title', ''),
                            "blocks": len(getattr(sc, 'content_blocks', [])),
                            "text": self._extract_text(sc)
                        }
                except Exception:
                    pass

                # Extract certificates
                try:
                    result["certificates"] = sim.get_certificates()
                except Exception:
                    pass

                # Extract references
                try:
                    result["references"] = sim.get_references()
                except Exception:
                    pass

                # Extract learning materials
                try:
                    result["learning_materials"] = sim.get_learning_materials()
                except Exception:
                    pass

                # Extract self validation
                try:
                    result["self_validation"] = sim.validate_self()
                except Exception:
                    pass

                # Extract gate checks
                try:
                    result["gate_checks"] = sim.get_gate_checks()
                except Exception:
                    pass

        except Exception as e:
            result["import_error"] = str(e)

        return result

    def _formula_to_dict(self, f) -> Dict:
        return {
            "id": getattr(f, 'id', ''),
            "latex": getattr(f, 'latex', ''),
            "description": getattr(f, 'description', ''),
            "category": getattr(f, 'category', ''),
            "derivation": getattr(f, 'derivation', {}),
            "terms": getattr(f, 'terms', {}),
            "input_params": getattr(f, 'input_params', []),
            "output_params": getattr(f, 'output_params', []),
        }

    def _param_to_dict(self, p) -> Dict:
        return {
            "path": getattr(p, 'path', ''),
            "name": getattr(p, 'name', ''),
            "units": getattr(p, 'units', ''),
            "status": getattr(p, 'status', ''),
            "description": getattr(p, 'description', ''),
            "experimental_bound": getattr(p, 'experimental_bound', None),
            "bound_source": getattr(p, 'bound_source', ''),
            "uncertainty": getattr(p, 'uncertainty', None),
            "no_experimental_value": getattr(p, 'no_experimental_value', False),
        }

    def _extract_text(self, sc) -> str:
        blocks = getattr(sc, 'content_blocks', [])
        texts = []
        for b in blocks:
            content = getattr(b, 'content', '')
            if content:
                texts.append(content[:500])
        return "\n\n".join(texts[:5])

    def get_all_simulation_files(self) -> List[Path]:
        """Find all simulation Python files."""
        sim_dir = PROJECT_ROOT / "simulations" / "PM"
        files = []
        for py in sim_dir.rglob("*.py"):
            if py.name.startswith("__"):
                continue
            # Check it's a simulation file (has SimulationBase)
            try:
                text = py.read_text(encoding='utf-8')
                if 'SimulationBase' in text and 'class ' in text:
                    files.append(py)
            except Exception:
                pass
        return sorted(files)

    def get_ordered_sections(self) -> List[Dict]:
        """Get all sections in paper order from theory_output."""
        sections = self.theory_output.get("sections", {})
        ordered = []
        for sid, sdata in sorted(sections.items()):
            ordered.append({
                "id": sid,
                "title": sdata.get("title", ""),
                "content": sdata.get("content", "")[:2000],
                "subsections": list(sdata.get("subsections", {}).keys()),
            })
        return ordered


# ─── Prompt Builders ────────────────────────────────────────────────────────

def build_file_review_prompt(analysis: Dict, theory_context: str, auto_fix: bool = False) -> str:
    """Build the Gemini prompt for reviewing a single simulation file."""
    formulas_text = ""
    for f in analysis.get("formulas", []):
        formulas_text += f"\n  - {f['id']}: {f['description'][:100]}"
        if f.get('derivation'):
            steps = f['derivation'].get('steps', [])
            formulas_text += f" ({len(steps)} derivation steps)"
        formulas_text += f" [category: {f.get('category', 'NONE')}]"

    params_text = ""
    for p in analysis.get("parameters", []):
        exp = f"exp={p.get('experimental_bound')}" if p.get('experimental_bound') else "NO_EXP"
        params_text += f"\n  - {p['path']}: {p['description'][:80]} [{p.get('status','?')}] {exp}"

    certs_text = ""
    for c in analysis.get("certificates", []):
        certs_text += f"\n  - {c.get('id','?')}: {c.get('assertion','')[:80]} [{c.get('status','?')}]"

    section_text = ""
    sc = analysis.get("section_content")
    if sc:
        section_text = f"Title: {sc.get('title','')}\nBlocks: {sc.get('blocks',0)}\nText preview: {sc.get('text','')[:500]}"

    refs_text = ""
    for r in analysis.get("references", []):
        refs_text += f"\n  - [{r.get('id','')}] {r.get('authors','')}: {r.get('title','')[:60]} ({r.get('year','')})"

    validation_text = json.dumps(analysis.get("self_validation", {}), indent=2, default=str)[:500]

    auto_fix_instruction = ""
    if auto_fix:
        auto_fix_instruction = """

## AUTO-FIX INSTRUCTIONS
For any rating below 7/10, provide specific code-level fixes in auto_fix_suggestions.
Each fix should include:
- "target": the method name or code section to fix
- "current_issue": what's wrong
- "suggested_fix": specific code or text to add/change
- "expected_improvement": how much the rating would improve
"""

    prompt = f"""# PRINCIPIA METAPHYSICA — Simulation File Peer Review

You are reviewing a simulation file from the Principia Metaphysica unified physics framework.
This framework derives Standard Model parameters from 26D string theory with G2 holonomy compactification.

## FILE: {analysis.get('file_path', '')}
## SIMULATION ID: {analysis.get('simulation_id', '')}

## SSOT STATUS
- get_certificates(): {"YES" if analysis.get('has_get_certificates') else "MISSING"}
- get_references(): {"YES" if analysis.get('has_get_references') else "MISSING"}
- get_learning_materials(): {"YES" if analysis.get('has_get_learning_materials') else "MISSING"}
- validate_self(): {"YES" if analysis.get('has_validate_self') else "MISSING"}
- get_gate_checks(): {"YES" if analysis.get('has_get_gate_checks') else "MISSING"}

## FORMULAS ({len(analysis.get('formulas', []))} total)
{formulas_text or "  (none found)"}

## PARAMETERS ({len(analysis.get('parameters', []))} total)
{params_text or "  (none found)"}

## CERTIFICATES ({len(analysis.get('certificates', []))} total)
{certs_text or "  (none found)"}

## SECTION CONTENT
{section_text or "(no section content)"}

## REFERENCES ({len(analysis.get('references', []))} total)
{refs_text or "  (none found)"}

## SELF-VALIDATION
{validation_text}

## THEORY CONTEXT (summary)
{theory_context[:3000]}
{auto_fix_instruction}

## INSTRUCTIONS
Rate this simulation file on a scale of 0-10 for each criterion.
Return ONLY valid JSON matching this exact schema (no markdown, no code blocks):

{{
  "overall_score": <float 0-10>,
  "ratings": {{
    "formula_strength": {{
      "score": <float 0-10>,
      "justification": "<why this score>",
      "issues": ["<issue 1>", ...],
      "suggestions": ["<suggestion 1>", ...]
    }},
    "derivation_rigor": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "validation_strength": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "section_wording": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "scientific_standing": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "description_accuracy": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "metadata_polish": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "schema_compliance": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "internal_consistency": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }},
    "theory_consistency": {{
      "score": <float 0-10>,
      "justification": "<why>",
      "issues": [...],
      "suggestions": [...]
    }}
  }},
  "improvement_plan": [
    "<step 1: most impactful improvement>",
    "<step 2>",
    ...
  ],
  "innovation_ideas": [
    "<idea 1: novel extension or prediction>",
    ...
  ],
  "auto_fix_suggestions": [
    {{
      "target": "<method or section>",
      "current_issue": "<what's wrong>",
      "suggested_fix": "<what to change>",
      "expected_improvement": "<rating delta>"
    }},
    ...
  ],
  "summary": "<2-3 sentence overall assessment>"
}}
"""
    return prompt


def build_paper_review_prompt(sections: List[Dict], theory_context: str) -> str:
    """Build the Gemini prompt for reviewing the whole paper."""
    sections_text = ""
    for s in sections:
        sections_text += f"\n### Section {s['id']}: {s['title']}\n"
        sections_text += s.get('content', '')[:800] + "\n"
        if s.get('subsections'):
            sections_text += f"  Subsections: {', '.join(s['subsections'][:5])}\n"

    prompt = f"""# PRINCIPIA METAPHYSICA — Whole Paper Peer Review

Review the complete paper structure and content for publication readiness.

## ORDERED SECTIONS
{sections_text[:15000]}

## THEORY CONTEXT
{theory_context[:3000]}

## INSTRUCTIONS
Assess the paper as a whole for coherence, flow, and publication readiness.
Return ONLY valid JSON (no markdown, no code blocks):

{{
  "overall_coherence": <float 0-10>,
  "section_flow": {{
    "score": <float 0-10>,
    "issues": ["<issue>", ...],
    "suggestions": ["<suggestion>", ...]
  }},
  "terminology_consistency": {{
    "score": <float 0-10>,
    "issues": [...],
    "suggestions": [...]
  }},
  "argument_structure": {{
    "score": <float 0-10>,
    "issues": [...],
    "suggestions": [...]
  }},
  "mathematical_notation": {{
    "score": <float 0-10>,
    "issues": [...],
    "suggestions": [...]
  }},
  "cross_references": {{
    "score": <float 0-10>,
    "issues": [...],
    "suggestions": [...]
  }},
  "publication_readiness": {{
    "score": <float 0-10>,
    "issues": [...],
    "suggestions": [...]
  }},
  "section_reviews": [
    {{
      "section_id": "<id>",
      "score": <float 0-10>,
      "issues": [...],
      "suggestions": [...]
    }},
    ...
  ],
  "innovation_ideas": [
    "<idea for theory extension>",
    ...
  ],
  "summary": "<overall assessment>"
}}
"""
    return prompt


# ─── Report Generator ───────────────────────────────────────────────────────

def generate_markdown_report(analysis: Dict, review: Dict) -> str:
    """Generate a markdown improvement report for a simulation file."""
    sim_id = analysis.get('simulation_id', 'unknown')
    file_path = analysis.get('file_path', '')

    lines = [
        f"# Gemini Peer Review: {sim_id}",
        f"**File:** `{file_path}`",
        f"**Date:** {datetime.now().isoformat()[:10]}",
        f"**Model:** {review.get('model', 'gemini-2.5-flash')}",
        f"**Overall Score:** {review.get('overall_score', 0):.1f}/10",
        "",
        "## Ratings Summary",
        "",
        "| Criterion | Score | Key Issue |",
        "|-----------|-------|-----------|",
    ]

    ratings = review.get("ratings", {})
    for criterion, data in ratings.items():
        score = data.get("score", 0) if isinstance(data, dict) else 0
        issues = data.get("issues", []) if isinstance(data, dict) else []
        top_issue = issues[0][:60] if issues else "—"
        display_name = criterion.replace("_", " ").title()
        emoji = "✅" if score >= 7 else "⚠️" if score >= 5 else "❌"
        lines.append(f"| {display_name} | {emoji} {score:.1f} | {top_issue} |")

    lines.append("")
    lines.append("## Detailed Ratings")
    lines.append("")

    for criterion, data in ratings.items():
        if not isinstance(data, dict):
            continue
        display_name = criterion.replace("_", " ").title()
        lines.append(f"### {display_name}: {data.get('score', 0):.1f}/10")
        lines.append(f"**Justification:** {data.get('justification', '')}")
        if data.get("issues"):
            lines.append("\n**Issues:**")
            for issue in data["issues"]:
                lines.append(f"- {issue}")
        if data.get("suggestions"):
            lines.append("\n**Suggestions:**")
            for sug in data["suggestions"]:
                lines.append(f"- {sug}")
        lines.append("")

    # Improvement plan
    plan = review.get("improvement_plan", [])
    if plan:
        lines.append("## Improvement Plan (Priority Order)")
        lines.append("")
        for i, step in enumerate(plan, 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    # Innovation ideas
    ideas = review.get("innovation_ideas", [])
    if ideas:
        lines.append("## Innovation Ideas for Theory")
        lines.append("")
        for idea in ideas:
            lines.append(f"- {idea}")
        lines.append("")

    # Auto-fix suggestions
    fixes = review.get("auto_fix_suggestions", [])
    if fixes:
        lines.append("## Auto-Fix Suggestions")
        lines.append("")
        for fix in fixes:
            if isinstance(fix, dict):
                lines.append(f"### Target: `{fix.get('target', '')}`")
                lines.append(f"- **Issue:** {fix.get('current_issue', '')}")
                lines.append(f"- **Fix:** {fix.get('suggested_fix', '')}")
                lines.append(f"- **Expected Improvement:** {fix.get('expected_improvement', '')}")
                lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(review.get("summary", "No summary available."))
    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by Gemini Peer Review System — {datetime.now().isoformat()}*")

    return "\n".join(lines)


# ─── Main Review Pipeline ──────────────────────────────────────────────────

def get_theory_context() -> str:
    """Build a compact theory context string from theory_output.json."""
    path = PROJECT_ROOT / "AutoGenerated" / "theory_output.json"
    if not path.exists():
        return "(theory_output.json not found)"

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    meta = data.get("metadata", {})
    validation = data.get("validation", {})
    formulas = data.get("formulas", {})
    params = data.get("parameters", {})

    context = f"""Principia Metaphysica v23 (PM Framework)
Simulations: {validation.get('simulations_run', 0)} run, {validation.get('simulations_passed', 0)} passed
Omega Hash: {'PASS' if validation.get('omega_hash_passed') else 'FAIL'}
Total Formulas: {len(formulas)}
Total Parameters: {len(params)}
Certificates: {len(data.get('certificates', []))}
Learning Materials: {len(data.get('learning_materials', []))}
Gate Checks: {len(data.get('gate_checks', []))}

Key derived values:
- Fine structure α⁻¹ derived from G2 topology
- 3 fermion generations from b3/8 = 24/8 = 3
- Dark energy w0 = -23/24 from third Betti number
- Higgs mass from brane partition function
- All 125 SM parameters from geometric residues
"""
    return context


def parse_gemini_json(text: str) -> Dict:
    """Parse JSON from Gemini response, handling markdown code blocks."""
    # Strip markdown code blocks
    text = text.strip()
    if text.startswith("```"):
        # Remove first line (```json or ```)
        lines = text.split("\n")
        text = "\n".join(lines[1:])
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    return {"error": "Failed to parse Gemini response", "raw": text[:500]}


def review_simulation_file(
    client: GeminiClient,
    analyzer: SimulationAnalyzer,
    file_path: Path,
    theory_context: str,
    auto_fix: bool = False
) -> Tuple[Dict, str]:
    """Review a single simulation file. Returns (review_dict, markdown_report)."""
    print(f"  Reviewing: {file_path.name}...")

    analysis = analyzer.analyze_file(file_path)
    prompt = build_file_review_prompt(analysis, theory_context, auto_fix)

    response_text = client.generate(prompt)
    review = parse_gemini_json(response_text)

    # Add metadata
    review["simulation_id"] = analysis.get("simulation_id", "")
    review["file_path"] = analysis.get("file_path", "")
    review["timestamp"] = datetime.now().isoformat()
    review["model"] = client.model

    # Generate markdown report
    report = generate_markdown_report(analysis, review)

    return review, report


def review_paper_sections(
    client: GeminiClient,
    analyzer: SimulationAnalyzer,
    theory_context: str,
) -> Dict:
    """Review the whole paper for consistency."""
    print("  Reviewing paper sections for consistency...")

    sections = analyzer.get_ordered_sections()
    prompt = build_paper_review_prompt(sections, theory_context)

    response_text = client.generate(prompt)
    review = parse_gemini_json(response_text)

    review["timestamp"] = datetime.now().isoformat()
    review["model"] = client.model

    return review


# ─── CLI Entry Point ────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Gemini Peer Review System")
    parser.add_argument("--all", action="store_true", help="Review all simulation files")
    parser.add_argument("--file", type=str, help="Review a specific file")
    parser.add_argument("--paper-review", action="store_true", help="Review whole paper sections")
    parser.add_argument("--auto-fix", action="store_true", help="Enable auto-fix suggestions")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="Gemini model")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory for reports")
    parser.add_argument("--dry-run", action="store_true", help="Analyze files without calling Gemini")
    args = parser.parse_args()

    print("=" * 72)
    print("  PRINCIPIA METAPHYSICA — Gemini Peer Review System")
    print("=" * 72)

    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key and not args.dry_run:
        print("\n[ERROR] No Gemini API key found.")
        print("  Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
        print("  Or use --dry-run to analyze files without calling Gemini.")
        sys.exit(1)

    # Initialize
    analyzer = SimulationAnalyzer()
    theory_context = get_theory_context()
    client = GeminiClient(api_key or "", model=args.model) if not args.dry_run else None

    all_reviews = []
    paper_review = None

    # Create timestamped output directory for reviews
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.output_dir:
        review_dir = Path(args.output_dir)
    else:
        review_dir = PROJECT_ROOT / "AutoGenerated" / "gemini_reviews" / run_timestamp
    review_dir.mkdir(parents=True, exist_ok=True)

    # Select files
    if args.file:
        files = [PROJECT_ROOT / args.file]
    elif args.all:
        files = analyzer.get_all_simulation_files()
    else:
        files = []

    print(f"\n  Files to review: {len(files)}")
    print(f"  Review output:   {review_dir}")
    print(f"  Paper review: {'YES' if args.paper_review else 'NO'}")
    print(f"  Auto-fix: {'YES' if args.auto_fix else 'NO'}")
    print(f"  Model: {args.model}")
    print(f"  Dry run: {'YES' if args.dry_run else 'NO'}")
    print()

    # Review individual files
    if files:
        print("─" * 72)
        print("  PER-FILE REVIEWS")
        print("─" * 72)

        for i, fpath in enumerate(files, 1):
            if args.dry_run:
                analysis = analyzer.analyze_file(fpath)
                print(f"  [{i}/{len(files)}] {fpath.name}: "
                      f"{len(analysis.get('formulas',[]))} formulas, "
                      f"{len(analysis.get('parameters',[]))} params, "
                      f"certs={'Y' if analysis.get('has_get_certificates') else 'N'}")
                all_reviews.append({
                    "file_path": str(fpath.relative_to(PROJECT_ROOT)),
                    "simulation_id": analysis.get("simulation_id", ""),
                    "dry_run": True,
                    "formulas": len(analysis.get('formulas', [])),
                    "parameters": len(analysis.get('parameters', [])),
                    "has_certificates": analysis.get('has_get_certificates', False),
                    "has_references": analysis.get('has_get_references', False),
                    "has_learning_materials": analysis.get('has_get_learning_materials', False),
                    "has_validate_self": analysis.get('has_validate_self', False),
                    "has_gate_checks": analysis.get('has_get_gate_checks', False),
                })
                continue

            try:
                review, report = review_simulation_file(
                    client, analyzer, fpath, theory_context, args.auto_fix
                )
                all_reviews.append(review)

                # Save markdown report in timestamped review directory
                report_name = fpath.stem + '.review.md'
                report_path = review_dir / report_name
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)

                score = review.get("overall_score", 0)
                print(f"  [{i}/{len(files)}] {fpath.name}: {score:.1f}/10"
                      f" → {report_name}")

                # Rate limit
                if i < len(files):
                    time.sleep(1)

            except Exception as e:
                print(f"  [{i}/{len(files)}] {fpath.name}: ERROR - {e}")
                all_reviews.append({
                    "file_path": str(fpath.relative_to(PROJECT_ROOT)),
                    "error": str(e)
                })

    # Paper review
    if args.paper_review:
        print()
        print("─" * 72)
        print("  WHOLE PAPER REVIEW")
        print("─" * 72)

        if args.dry_run:
            sections = analyzer.get_ordered_sections()
            print(f"  Sections: {len(sections)}")
            for s in sections[:10]:
                print(f"    {s['id']}: {s['title']}")
        else:
            try:
                paper_review = review_paper_sections(client, analyzer, theory_context)
                coherence = paper_review.get("overall_coherence", 0)
                print(f"  Overall coherence: {coherence:.1f}/10")

                # Save paper review
                paper_path = review_dir / "gemini_paper_review.json"
                with open(paper_path, 'w', encoding='utf-8') as f:
                    json.dump(paper_review, f, indent=2, ensure_ascii=False, default=str)
                print(f"  Saved to: {paper_path}")

            except Exception as e:
                print(f"  Paper review ERROR: {e}")

    # Save aggregate results
    output = {
        "timestamp": datetime.now().isoformat(),
        "model": args.model,
        "auto_fix": args.auto_fix,
        "dry_run": args.dry_run,
        "files_reviewed": len(all_reviews),
        "file_reviews": all_reviews,
        "paper_review": paper_review,
    }

    # Compute aggregates
    if all_reviews and not args.dry_run:
        scores = [r.get("overall_score", 0) for r in all_reviews if "overall_score" in r]
        if scores:
            output["aggregate"] = {
                "mean_score": sum(scores) / len(scores),
                "min_score": min(scores),
                "max_score": max(scores),
                "below_7": sum(1 for s in scores if s < 7),
                "above_8": sum(1 for s in scores if s >= 8),
            }

    out_path = review_dir / "gemini_peer_review_results.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    # Also keep a copy in AutoGenerated for pipeline integration
    latest_path = PROJECT_ROOT / "AutoGenerated" / "gemini_peer_review_results.json"
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)

    # Summary
    print()
    print("=" * 72)
    print("  REVIEW SUMMARY")
    print("=" * 72)
    print(f"  Files reviewed: {len(all_reviews)}")
    if not args.dry_run and "aggregate" in output:
        agg = output["aggregate"]
        print(f"  Mean score: {agg['mean_score']:.1f}/10")
        print(f"  Min score: {agg['min_score']:.1f}/10")
        print(f"  Max score: {agg['max_score']:.1f}/10")
        print(f"  Below 7.0: {agg['below_7']} files")
        print(f"  Above 8.0: {agg['above_8']} files")
    if paper_review:
        print(f"  Paper coherence: {paper_review.get('overall_coherence', 0):.1f}/10")
    print(f"  Results saved: {out_path}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
