#!/usr/bin/env python3
"""
Gemini TwoLayerOR Debate Script
=================================
For each of the 12 sub-topic files extracted from TwoLayerOR And Dark Forces.txt,
this script:
1. Reads the sub-topic proposal
2. Reads the corresponding current simulation file(s)
3. Reads relevant theory_output.json data
4. Sends both to Gemini 2.0 Flash for scientific debate
5. Gemini acts as scrum product owner / scientific peer reviewer
6. Outputs a verdict: ADOPT, REJECT, MODIFY, or MERGE

Usage:
    python scripts/validation/gemini_twolayer_debate.py
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyD6mQiE1Ls4A7s17o5kBMq-A27N0EokFOA")
GEMINI_MODEL = "gemini-2.0-flash"

# Sub-topic files and their target simulation files
SUBTOPICS = [
    {
        "id": "01",
        "name": "Two-Layer OR Reduction Structure",
        "file": "docs/twolayer_subtopics/01_two_layer_or_structure.txt",
        "targets": [
            "simulations/PM/geometry/four_face_structure.py",
            "simulations/PM/geometry/geometric_anchors.py",
            "simulations/PM/field_dynamics/orch_or_bridge.py",
        ],
        "priority": "HIGHEST",
    },
    {
        "id": "02",
        "name": "Bridge Warping Potential (V_bridge)",
        "file": "docs/twolayer_subtopics/02_bridge_warping_potential.txt",
        "targets": [
            "simulations/PM/derivations/lagrangian_master.py",
            "simulations/PM/support/bridge_pressure.py",
        ],
        "priority": "HIGHEST",
    },
    {
        "id": "03",
        "name": "Face Warping Potential (V_face)",
        "file": "docs/twolayer_subtopics/03_face_warping_potential.txt",
        "targets": [
            "simulations/PM/geometry/four_face_structure.py",
            "simulations/PM/derivations/lagrangian_master.py",
        ],
        "priority": "HIGHEST",
    },
    {
        "id": "04",
        "name": "Updated Master Lagrangian (Both OR Layers)",
        "file": "docs/twolayer_subtopics/04_updated_master_lagrangian.txt",
        "targets": [
            "simulations/PM/derivations/lagrangian_master.py",
            "simulations/PM/gauge/master_action.py",
        ],
        "priority": "HIGHEST",
    },
    {
        "id": "05",
        "name": "Dark Matter Portal Coupling & Relic Density",
        "file": "docs/twolayer_subtopics/05_dark_matter_portal.txt",
        "targets": [
            "simulations/PM/cosmology/dark_energy.py",
            "simulations/PM/geometry/four_face_structure.py",
            "simulations/PM/support/bridge_pressure.py",
        ],
        "priority": "HIGH",
    },
    {
        "id": "06",
        "name": "Dark Light Leakage (Cross-Shadow EM)",
        "file": "docs/twolayer_subtopics/06_dark_light_leakage.txt",
        "targets": [
            "simulations/PM/support/bridge_pressure.py",
            "simulations/PM/field_dynamics/orch_or_bridge.py",
        ],
        "priority": "HIGH",
    },
    {
        "id": "07",
        "name": "Dark Force Hierarchy (All Four Forces)",
        "file": "docs/twolayer_subtopics/07_dark_force_hierarchy.txt",
        "targets": [
            "simulations/PM/support/bridge_pressure.py",
            "simulations/PM/gauge/master_action.py",
        ],
        "priority": "HIGH",
    },
    {
        "id": "08",
        "name": "Chirality Reversal Mechanism",
        "file": "docs/twolayer_subtopics/08_chirality_reversal.txt",
        "targets": [
            "simulations/PM/field_dynamics/orch_or_bridge.py",
            "simulations/PM/particle/neutrino_mixing.py",
        ],
        "priority": "MEDIUM",
    },
    {
        "id": "09",
        "name": "Torsion from Topology (T_omega Derivation)",
        "file": "docs/twolayer_subtopics/09_torsion_from_topology.txt",
        "targets": [
            "simulations/PM/geometry/geometric_anchors.py",
            "simulations/PM/geometry/torsional_constants.py",
            "simulations/PM/support/bridge_pressure.py",
        ],
        "priority": "MEDIUM-HIGH",
    },
    {
        "id": "10",
        "name": "Reduced Lagrangians (13D & 4D)",
        "file": "docs/twolayer_subtopics/10_reduced_lagrangians.txt",
        "targets": [
            "simulations/PM/derivations/lagrangian_master.py",
            "simulations/PM/gauge/kk_reduction_gr_gauge.py",
        ],
        "priority": "MEDIUM",
    },
    {
        "id": "11",
        "name": "Experimental Signatures & Observables",
        "file": "docs/twolayer_subtopics/11_experimental_signatures.txt",
        "targets": [
            "simulations/PM/paper/sections/predictions.py",
            "simulations/PM/cosmology/gw_dispersion.py",
        ],
        "priority": "HIGH",
    },
    {
        "id": "12",
        "name": "Falsifiability & Paper Strengthening",
        "file": "docs/twolayer_subtopics/12_falsifiability_paper.txt",
        "targets": [
            "simulations/PM/paper/sections/abstract.py",
            "simulations/PM/paper/sections/predictions.py",
            "simulations/PM/paper/sections/discussion.py",
        ],
        "priority": "HIGH",
    },
]


def read_file_safe(path, max_lines=300):
    """Read file content, truncated to max_lines."""
    full_path = PROJECT_ROOT / path
    if not full_path.exists():
        return f"[FILE NOT FOUND: {path}]"
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        if len(lines) > max_lines:
            return "".join(lines[:max_lines]) + f"\n\n[... TRUNCATED at {max_lines}/{len(lines)} lines ...]"
        return "".join(lines)
    except Exception as e:
        return f"[ERROR reading {path}: {e}]"


def read_theory_output_excerpt():
    """Read key values from theory_output.json."""
    path = PROJECT_ROOT / "AutoGenerated" / "theory_output.json"
    if not path.exists():
        return "[theory_output.json not found]"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        excerpt = {
            "version": data.get("version", "unknown"),
            "total_simulations": len(data.get("simulations", [])),
            "omega_hash": data.get("omega_hash", "unknown"),
        }
        params = data.get("parameters", {})
        key_params = [
            "alpha_inverse", "speed_of_light", "mass_ratio", "h0_local",
            "w0_dark_energy", "higgs_vev", "weak_mixing_angle", "strong_coupling",
            "planck_mass", "cosmological_constant", "sigma_8",
        ]
        for k in key_params:
            for section in params.values():
                if isinstance(section, dict):
                    if k in section:
                        excerpt[k] = section[k]
                    for sub in section.values():
                        if isinstance(sub, dict) and k in sub:
                            excerpt[k] = sub[k]
        return json.dumps(excerpt, indent=2, default=str)[:3000]
    except Exception as e:
        return f"[ERROR: {e}]"


def read_statistics():
    """Read statistics.json for overall framework health."""
    path = PROJECT_ROOT / "AutoGenerated" / "statistics.json"
    if not path.exists():
        return "[statistics.json not found]"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:2000]
    except Exception as e:
        return f"[ERROR: {e}]"


def call_gemini(prompt, max_retries=3):
    """Call Gemini API via REST."""
    import urllib.request
    import urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY,
    }

    data = json.dumps(payload).encode("utf-8")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "[empty response]")
                return "[no candidates in response]"
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            print(f"  [HTTP {e.code}] Attempt {attempt+1}/{max_retries}: {body[:200]}")
            if e.code == 429:
                time.sleep(15 * (attempt + 1))
            else:
                time.sleep(5)
        except Exception as e:
            print(f"  [ERROR] Attempt {attempt+1}/{max_retries}: {e}")
            time.sleep(5)

    return "[GEMINI API FAILED after retries]"


def build_debate_prompt(subtopic, proposal_text, sim_texts, theory_excerpt, stats):
    """Build the debate prompt for Gemini."""
    sim_section = ""
    for name, content in sim_texts:
        sim_section += f"\n--- CURRENT SIMULATION: {name} ---\n{content}\n"

    return f"""You are the SCIENTIFIC PEER REVIEWER and SCRUM PRODUCT OWNER for Principia Metaphysica,
a theoretical physics framework based on G₂ holonomy manifolds, dual-shadow compactification,
and spectral residue mechanics.

Your job is to evaluate a PROPOSED CHANGE from the "TwoLayerOR And Dark Forces" brainstorming
document against the CURRENT IMPLEMENTATION that is already working and tested (69/69 simulations
pass, OMEGA=0).

## FRAMEWORK HEALTH (Current)
{stats}

## THEORY OUTPUT EXCERPT (Current derived values)
{theory_excerpt}

## PROPOSED CHANGE: Sub-Topic {subtopic['id']} — {subtopic['name']}
Priority: {subtopic['priority']}

{proposal_text}

## CURRENT IMPLEMENTATION (Target simulation files):
{sim_section}

## YOUR TASK

As scientific peer reviewer, evaluate the proposal against the current code. Consider:

1. **Mathematical Rigor**: Is the proposed formula mathematically well-defined and derivable from the existing G₂ framework?
2. **Geometric Purity**: Are all terms genuinely derived from topology (b₃, χ_eff, flux), or are there hidden free parameters?
3. **Consistency**: Does the proposal fit within the existing SSOT framework without breaking other derivations?
4. **Novelty**: Does it introduce genuinely new physics predictions vs restating existing results?
5. **Testability**: Does it produce falsifiable predictions with specific numerical values?
6. **Implementation Risk**: Can it be added as additive content (new formulas, section content) without modifying existing run() results?

## IMPORTANT CONTEXT
- The current framework achieves 69/69 simulations pass with OMEGA=0
- All existing formulas use SSOT architecture (FormulasRegistry → all simulations)
- Two-layer OR is a NEW structural proposal that adds V_bridge + V_face to the master action
- Dark force leakage is a NEW set of predictions (P_leak ~ 10^{-6} for EM/gravity)
- Strong and weak force leakage are claimed to be zero — verify this is physically reasonable
- The α_leak ≈ 0.57 dark matter portal coupling should be checked for self-consistency
- REJECT proposals that introduce hidden free parameters or u_phys-style fudge factors
- FAVOR proposals that add genuine geometric predictions without modifying existing values

## OUTPUT FORMAT

Provide your verdict in this exact structure:

**VERDICT:** [ADOPT / REJECT / MODIFY / MERGE]
**CONFIDENCE:** [HIGH / MEDIUM / LOW]
**SCIENTIFIC_SCORE:** [1-10]

**STRENGTHS:**
- [bullet points]

**WEAKNESSES:**
- [bullet points]

**RECOMMENDATION:**
[2-3 sentences on what to do]

**SPECIFIC_ACTIONS:**
- [concrete actions if ADOPT/MODIFY/MERGE, or reasons if REJECT]
"""


def main():
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set. Export it before running.")
        sys.exit(1)

    print(f"=== Gemini TwoLayerOR Debate Script ===")
    print(f"Model: {GEMINI_MODEL}")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Sub-topics: {len(SUBTOPICS)}")
    print()

    # Create output directory
    run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = PROJECT_ROOT / "AutoGenerated" / "gemini_debates" / f"twolayer_{run_ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Read shared context
    theory_excerpt = read_theory_output_excerpt()
    stats = read_statistics()

    results = []

    for i, st in enumerate(SUBTOPICS):
        print(f"\n[{i+1}/{len(SUBTOPICS)}] Debating: {st['name']} (Priority: {st['priority']})")

        # Read proposal
        proposal = read_file_safe(st["file"], max_lines=200)

        # Read target simulations
        sim_texts = []
        for target in st["targets"]:
            content = read_file_safe(target, max_lines=250)
            sim_texts.append((target, content))

        # Build prompt
        prompt = build_debate_prompt(st, proposal, sim_texts, theory_excerpt, stats)

        # Call Gemini
        print(f"  Sending to Gemini ({len(prompt)} chars)...")
        response = call_gemini(prompt)
        print(f"  Response: {len(response)} chars")

        # Save individual review
        safe_name = st['name'].replace(' ', '_').replace('/', '_').replace('>', '').replace('<', '').replace('(', '').replace(')', '').replace('&', 'and')
        review_path = out_dir / f"{st['id']}_{safe_name}.md"
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(f"# Gemini Debate: {st['name']}\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n")
            f.write(f"**Priority:** {st['priority']}\n")
            f.write(f"**Targets:** {', '.join(st['targets'])}\n\n")
            f.write("---\n\n")
            f.write(response)

        # Parse verdict
        verdict = "UNKNOWN"
        confidence = "UNKNOWN"
        score = 0
        for line in response.split("\n"):
            if "**VERDICT:**" in line:
                verdict = line.split("**VERDICT:**")[-1].strip().strip("[]* ")
            if "**CONFIDENCE:**" in line:
                confidence = line.split("**CONFIDENCE:**")[-1].strip().strip("[]* ")
            if "**SCIENTIFIC_SCORE:**" in line:
                try:
                    score = int(line.split("**SCIENTIFIC_SCORE:**")[-1].strip().strip("[]* ").split("/")[0])
                except (ValueError, IndexError):
                    score = 0

        result = {
            "id": st["id"],
            "name": st["name"],
            "priority": st["priority"],
            "verdict": verdict,
            "confidence": confidence,
            "score": score,
            "review_file": str(review_path.relative_to(PROJECT_ROOT)),
        }
        results.append(result)
        print(f"  => VERDICT: {verdict} | CONFIDENCE: {confidence} | SCORE: {score}/10")

        # Rate limit
        if i < len(SUBTOPICS) - 1:
            time.sleep(4)

    # Save aggregate results
    aggregate = {
        "timestamp": datetime.now().isoformat(),
        "model": GEMINI_MODEL,
        "source_document": "TwoLayerOR And Dark Forces.txt",
        "total_subtopics": len(SUBTOPICS),
        "results": results,
        "summary": {
            "adopt": sum(1 for r in results if "ADOPT" in r["verdict"].upper()),
            "reject": sum(1 for r in results if "REJECT" in r["verdict"].upper()),
            "modify": sum(1 for r in results if "MODIFY" in r["verdict"].upper()),
            "merge": sum(1 for r in results if "MERGE" in r["verdict"].upper()),
            "mean_score": sum(r["score"] for r in results) / max(len(results), 1),
        },
    }

    agg_path = out_dir / "debate_results.json"
    with open(agg_path, "w", encoding="utf-8") as f:
        json.dump(aggregate, f, indent=2, ensure_ascii=False)

    # Also save to AutoGenerated root
    latest_path = PROJECT_ROOT / "AutoGenerated" / "gemini_twolayer_debate_results.json"
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(aggregate, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 60)
    print("DEBATE SUMMARY — TwoLayerOR And Dark Forces")
    print("=" * 60)
    for r in results:
        print(f"  [{r['id']}] {r['name']:50s} => {r['verdict']:8s} ({r['score']}/10)")
    print()
    print(f"  ADOPT:  {aggregate['summary']['adopt']}")
    print(f"  REJECT: {aggregate['summary']['reject']}")
    print(f"  MODIFY: {aggregate['summary']['modify']}")
    print(f"  MERGE:  {aggregate['summary']['merge']}")
    print(f"  Mean Score: {aggregate['summary']['mean_score']:.1f}/10")
    print(f"\nResults saved to: {out_dir}")


if __name__ == "__main__":
    main()
