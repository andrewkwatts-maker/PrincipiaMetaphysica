#!/usr/bin/env python3
"""
SSOT Full Compliance Checker v23.3
====================================
Tests all simulation files against the 9 mandatory SSOT schema rules.

Every simulation that extends SimulationBase must satisfy:
  Rule 1: Formulas      - get_formulas() returns >=1 Formula with derivation, terms, category
  Rule 2: Parameters    - get_output_param_definitions() returns >=1 Parameter with units, desc, bounds
  Rule 3: Sections      - get_section_content() returns SectionContent with >=1 content_block
  Rule 4: Certificates  - get_certificates() returns >=1 dict with id/assertion/condition/status
  Rule 5: Validation    - validate_self() returns dict with >=1 check
  Rule 6: References    - get_references() returns >=1 dict with id/authors/title/year/url|doi
  Rule 7: Learning      - get_learning_materials() returns >=1 dict with topic/url/relevance
  Rule 8: PM Inputs     - required_inputs has >=1 entry (except geometric_anchors seed simulation)
  Rule 9: Gate Checks   - get_gate_checks() returns a list (can be empty during migration)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field

import pytest

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "simulations"))

# ---------------------------------------------------------------------------
# Import the simulation runner to get all registered simulations
# ---------------------------------------------------------------------------
from simulations.run_all_simulations import SimulationRunner
from simulations.base.simulation_base import SimulationBase


# ===========================================================================
# Constants
# ===========================================================================
VALID_FORMULA_CATEGORIES = frozenset({
    "DERIVED", "ESTABLISHED", "GEOMETRIC", "PREDICTED",
})

VALID_CERT_STATUSES = frozenset({"PASS", "FAIL", "OFFLINE"})

# Simulation IDs that are allowed to have empty required_inputs (seed/root sims)
EMPTY_INPUTS_ALLOWED = frozenset({
    "geometric_anchors_v16_2",
})

MIN_DERIVATION_STEPS = 3
MIN_PARAGRAPH_LENGTH = 50


# ===========================================================================
# Rule checker dataclass
# ===========================================================================
@dataclass
class RuleResult:
    """Result of a single rule check on a single simulation."""
    rule_number: int
    rule_name: str
    passed: bool
    details: str = ""


@dataclass
class SimComplianceReport:
    """Full compliance report for a single simulation."""
    sim_id: str
    sim_class: str
    rules: List[RuleResult] = field(default_factory=list)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.rules if r.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.rules if not r.passed)

    @property
    def total_count(self) -> int:
        return len(self.rules)

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.rules)

    @property
    def compliance_pct(self) -> float:
        if not self.rules:
            return 0.0
        return 100.0 * self.passed_count / self.total_count


# ===========================================================================
# Helper: collect all simulations from the pipeline
# ===========================================================================
def _get_all_simulations() -> List[SimulationBase]:
    """
    Instantiate the SimulationRunner (which populates self.phases during __init__)
    and collect every simulation instance across all phases.
    """
    runner = SimulationRunner(verbose=False)
    all_sims: List[SimulationBase] = []
    for phase_num in sorted(runner.phases.keys()):
        all_sims.extend(runner.phases[phase_num])
    return all_sims


# Cache so we only build the list once per session
_ALL_SIMS_CACHE: List[SimulationBase] = []


def get_all_simulations() -> List[SimulationBase]:
    global _ALL_SIMS_CACHE
    if not _ALL_SIMS_CACHE:
        _ALL_SIMS_CACHE = _get_all_simulations()
    return _ALL_SIMS_CACHE


# ===========================================================================
# Rule checkers
# ===========================================================================

def check_rule_1_formulas(sim: SimulationBase) -> RuleResult:
    """
    Rule 1: Formulas (min 1)
    - get_formulas() returns >=1 Formula
    - Each has derivation dict with steps[] containing >=3 items
    - Each has terms{} dict (non-empty)
    - Each has category in VALID_FORMULA_CATEGORIES
    """
    rule = RuleResult(rule_number=1, rule_name="Formulas", passed=True)
    issues: List[str] = []

    try:
        formulas = sim.get_formulas()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_formulas() raised {type(exc).__name__}: {exc}"
        return rule

    if not formulas or len(formulas) < 1:
        rule.passed = False
        rule.details = "get_formulas() returned 0 formulas (need >=1)"
        return rule

    for i, f in enumerate(formulas):
        fid = getattr(f, "id", f"formula[{i}]")

        # Check category
        cat = getattr(f, "category", None)
        if cat not in VALID_FORMULA_CATEGORIES:
            issues.append(
                f"{fid}: category='{cat}' not in {sorted(VALID_FORMULA_CATEGORIES)}"
            )

        # Check derivation
        deriv = getattr(f, "derivation", None)
        if deriv is None:
            issues.append(f"{fid}: missing derivation dict")
        elif not isinstance(deriv, dict):
            issues.append(f"{fid}: derivation is not a dict")
        else:
            steps = deriv.get("steps", [])
            if not isinstance(steps, (list, tuple)) or len(steps) < MIN_DERIVATION_STEPS:
                issues.append(
                    f"{fid}: derivation.steps has {len(steps) if isinstance(steps, (list, tuple)) else 0} "
                    f"items (need >={MIN_DERIVATION_STEPS})"
                )

        # Check terms
        terms = getattr(f, "terms", None)
        if not terms or not isinstance(terms, dict) or len(terms) == 0:
            issues.append(f"{fid}: terms dict is empty or missing")

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_2_parameters(sim: SimulationBase) -> RuleResult:
    """
    Rule 2: Parameters (min 1)
    - get_output_param_definitions() returns >=1 Parameter
    - Each has non-empty units and description
    - Each has either (experimental_bound + bound_source) or no_experimental_value=True
    """
    rule = RuleResult(rule_number=2, rule_name="Parameters", passed=True)
    issues: List[str] = []

    try:
        params = sim.get_output_param_definitions()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_output_param_definitions() raised {type(exc).__name__}: {exc}"
        return rule

    if not params or len(params) < 1:
        rule.passed = False
        rule.details = "get_output_param_definitions() returned 0 params (need >=1)"
        return rule

    for i, p in enumerate(params):
        pid = getattr(p, "path", f"param[{i}]")

        units = getattr(p, "units", None)
        if not units or not str(units).strip():
            issues.append(f"{pid}: empty units")

        desc = getattr(p, "description", None)
        if not desc or not str(desc).strip():
            issues.append(f"{pid}: empty description")

        # Must have either experimental_bound+bound_source OR no_experimental_value=True
        exp_bound = getattr(p, "experimental_bound", None)
        bound_src = getattr(p, "bound_source", None)
        no_exp = getattr(p, "no_experimental_value", False)

        if no_exp:
            pass  # OK, explicitly marked as having no experimental value
        elif exp_bound is not None and bound_src:
            pass  # OK, has experimental bound with source
        else:
            issues.append(
                f"{pid}: needs (experimental_bound + bound_source) or no_experimental_value=True"
            )

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_3_sections(sim: SimulationBase) -> RuleResult:
    """
    Rule 3: Section Content (min 1)
    - get_section_content() returns non-None SectionContent
    - content_blocks[] contains >=1 block
    - At least one block has type="paragraph" with content >50 chars
    """
    rule = RuleResult(rule_number=3, rule_name="Sections", passed=True)
    issues: List[str] = []

    try:
        section = sim.get_section_content()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_section_content() raised {type(exc).__name__}: {exc}"
        return rule

    if section is None:
        rule.passed = False
        rule.details = "get_section_content() returned None"
        return rule

    blocks = getattr(section, "content_blocks", [])
    if not blocks or len(blocks) < 1:
        rule.passed = False
        rule.details = "content_blocks is empty (need >=1)"
        return rule

    # Check for at least one paragraph block with >50 chars
    has_substantial_paragraph = False
    for block in blocks:
        btype = getattr(block, "type", None)
        bcontent = getattr(block, "content", None)
        if btype == "paragraph" and bcontent and len(str(bcontent)) > MIN_PARAGRAPH_LENGTH:
            has_substantial_paragraph = True
            break

    if not has_substantial_paragraph:
        issues.append(
            f"no paragraph block with >{MIN_PARAGRAPH_LENGTH} chars found "
            f"({len(blocks)} blocks total)"
        )

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_4_certificates(sim: SimulationBase) -> RuleResult:
    """
    Rule 4: Certificates (min 1)
    - get_certificates() returns >=1 dict
    - Each dict has: id, assertion, condition, status (PASS/FAIL/OFFLINE)
    """
    rule = RuleResult(rule_number=4, rule_name="Certificates", passed=True)
    issues: List[str] = []

    try:
        certs = sim.get_certificates()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_certificates() raised {type(exc).__name__}: {exc}"
        return rule

    if not certs or len(certs) < 1:
        rule.passed = False
        rule.details = "get_certificates() returned 0 certs (need >=1)"
        return rule

    required_keys = {"id", "assertion", "condition", "status"}
    for i, cert in enumerate(certs):
        if not isinstance(cert, dict):
            issues.append(f"cert[{i}]: not a dict")
            continue
        cid = cert.get("id", f"cert[{i}]")
        missing = required_keys - set(cert.keys())
        if missing:
            issues.append(f"{cid}: missing keys {sorted(missing)}")

        status = cert.get("status", "")
        if status not in VALID_CERT_STATUSES:
            issues.append(f"{cid}: status='{status}' not in {sorted(VALID_CERT_STATUSES)}")

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_5_validation(sim: SimulationBase) -> RuleResult:
    """
    Rule 5: Validation (min 1)
    - validate_self() returns dict with checks[] containing >=1 check
    - Each check has name, passed, log_level
    """
    rule = RuleResult(rule_number=5, rule_name="Validation", passed=True)
    issues: List[str] = []

    try:
        result = sim.validate_self()
    except Exception as exc:
        rule.passed = False
        rule.details = f"validate_self() raised {type(exc).__name__}: {exc}"
        return rule

    if not isinstance(result, dict):
        rule.passed = False
        rule.details = f"validate_self() returned {type(result).__name__}, expected dict"
        return rule

    checks = result.get("checks", [])
    if not checks or len(checks) < 1:
        rule.passed = False
        rule.details = "validate_self() returned 0 checks (need >=1)"
        return rule

    required_keys = {"name", "passed", "log_level"}
    for i, check in enumerate(checks):
        if not isinstance(check, dict):
            issues.append(f"check[{i}]: not a dict")
            continue
        cname = check.get("name", f"check[{i}]")
        missing = required_keys - set(check.keys())
        if missing:
            issues.append(f"{cname}: missing keys {sorted(missing)}")

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_6_references(sim: SimulationBase) -> RuleResult:
    """
    Rule 6: References (min 1)
    - get_references() returns >=1 dict
    - Each dict has: id, authors, title, year, and either url or doi
    """
    rule = RuleResult(rule_number=6, rule_name="References", passed=True)
    issues: List[str] = []

    try:
        refs = sim.get_references()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_references() raised {type(exc).__name__}: {exc}"
        return rule

    if not refs or len(refs) < 1:
        rule.passed = False
        rule.details = "get_references() returned 0 refs (need >=1)"
        return rule

    required_keys = {"id", "authors", "title", "year"}
    for i, ref in enumerate(refs):
        if not isinstance(ref, dict):
            issues.append(f"ref[{i}]: not a dict")
            continue
        rid = ref.get("id", f"ref[{i}]")
        missing = required_keys - set(ref.keys())
        if missing:
            issues.append(f"{rid}: missing keys {sorted(missing)}")

        # Must have either url or doi
        has_url = bool(ref.get("url"))
        has_doi = bool(ref.get("doi"))
        if not has_url and not has_doi:
            issues.append(f"{rid}: needs either 'url' or 'doi'")

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_7_learning(sim: SimulationBase) -> RuleResult:
    """
    Rule 7: Learning Materials (min 1)
    - get_learning_materials() returns >=1 dict
    - Each dict has: topic, url, relevance
    """
    rule = RuleResult(rule_number=7, rule_name="Learning", passed=True)
    issues: List[str] = []

    try:
        materials = sim.get_learning_materials()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_learning_materials() raised {type(exc).__name__}: {exc}"
        return rule

    if not materials or len(materials) < 1:
        rule.passed = False
        rule.details = "get_learning_materials() returned 0 materials (need >=1)"
        return rule

    required_keys = {"topic", "url", "relevance"}
    for i, mat in enumerate(materials):
        if not isinstance(mat, dict):
            issues.append(f"material[{i}]: not a dict")
            continue
        mtopic = mat.get("topic", f"material[{i}]")
        missing = required_keys - set(mat.keys())
        if missing:
            issues.append(f"{mtopic}: missing keys {sorted(missing)}")

    if issues:
        rule.passed = False
        rule.details = "; ".join(issues)

    return rule


def check_rule_8_inputs(sim: SimulationBase) -> RuleResult:
    """
    Rule 8: PM Param Inputs (min 1, except seed simulations)
    - required_inputs has >=1 entry
    - Exception: geometric_anchors simulation may have empty required_inputs
    """
    rule = RuleResult(rule_number=8, rule_name="PM Inputs", passed=True)

    try:
        inputs = sim.required_inputs
    except Exception as exc:
        rule.passed = False
        rule.details = f"required_inputs raised {type(exc).__name__}: {exc}"
        return rule

    sim_id = getattr(sim.metadata, "id", "")

    if sim_id in EMPTY_INPUTS_ALLOWED:
        # Seed simulations are exempt
        rule.details = f"exempt (seed simulation: {sim_id})"
        return rule

    if not inputs or len(inputs) < 1:
        rule.passed = False
        rule.details = f"required_inputs is empty (need >=1 for non-seed simulation '{sim_id}')"

    return rule


def check_rule_9_gate_checks(sim: SimulationBase) -> RuleResult:
    """
    Rule 9: Gate Checks
    - get_gate_checks() returns a list (can be empty during migration)
    """
    rule = RuleResult(rule_number=9, rule_name="Gate Checks", passed=True)

    try:
        gates = sim.get_gate_checks()
    except Exception as exc:
        rule.passed = False
        rule.details = f"get_gate_checks() raised {type(exc).__name__}: {exc}"
        return rule

    if not isinstance(gates, list):
        rule.passed = False
        rule.details = f"get_gate_checks() returned {type(gates).__name__}, expected list"
        return rule

    # During migration, empty list is acceptable
    if len(gates) == 0:
        rule.details = "empty list (acceptable during migration)"

    return rule


# ===========================================================================
# Run all 9 rules on a single simulation
# ===========================================================================
ALL_RULE_CHECKERS = [
    check_rule_1_formulas,
    check_rule_2_parameters,
    check_rule_3_sections,
    check_rule_4_certificates,
    check_rule_5_validation,
    check_rule_6_references,
    check_rule_7_learning,
    check_rule_8_inputs,
    check_rule_9_gate_checks,
]


def check_simulation(sim: SimulationBase) -> SimComplianceReport:
    """Run all 9 SSOT rules on a single simulation and return the report."""
    sim_id = getattr(sim.metadata, "id", type(sim).__name__)
    report = SimComplianceReport(
        sim_id=sim_id,
        sim_class=type(sim).__name__,
    )
    for checker in ALL_RULE_CHECKERS:
        report.rules.append(checker(sim))
    return report


# ===========================================================================
# Aggregate report
# ===========================================================================
def generate_full_report(reports: List[SimComplianceReport]) -> str:
    """Generate a human-readable compliance report across all simulations."""
    lines: List[str] = []
    lines.append("=" * 90)
    lines.append("SSOT FULL COMPLIANCE REPORT - 9 Rules x {} Simulations".format(len(reports)))
    lines.append("=" * 90)
    lines.append("")

    total_rules = 0
    total_passed = 0
    fully_compliant = 0

    for rpt in reports:
        total_rules += rpt.total_count
        total_passed += rpt.passed_count
        if rpt.all_passed:
            fully_compliant += 1

        status = "PASS" if rpt.all_passed else "FAIL"
        lines.append(
            f"[{status}] {rpt.sim_id} ({rpt.sim_class}) "
            f"- {rpt.passed_count}/{rpt.total_count} rules"
        )

        for r in rpt.rules:
            mark = "  OK" if r.passed else "FAIL"
            detail = f" -- {r.details}" if r.details else ""
            lines.append(f"    [{mark}] Rule {r.rule_number}: {r.rule_name}{detail}")

        lines.append("")

    # Aggregate summary
    lines.append("=" * 90)
    lines.append("AGGREGATE SUMMARY")
    lines.append("=" * 90)
    lines.append(f"  Simulations checked:      {len(reports)}")
    lines.append(f"  Fully compliant:          {fully_compliant}/{len(reports)}")
    lines.append(f"  Total rule checks:        {total_rules}")
    lines.append(f"  Total passed:             {total_passed}")
    lines.append(f"  Total failed:             {total_rules - total_passed}")
    pct = 100.0 * total_passed / total_rules if total_rules > 0 else 0.0
    lines.append(f"  Compliance percentage:    {pct:.1f}%")
    lines.append("")

    # Per-rule summary
    lines.append("-" * 60)
    lines.append("PER-RULE PASS RATE")
    lines.append("-" * 60)
    for rule_idx, checker in enumerate(ALL_RULE_CHECKERS):
        rule_num = rule_idx + 1
        # Extract rule name from first report if available
        rule_name = reports[0].rules[rule_idx].rule_name if reports else f"Rule {rule_num}"
        passed_for_rule = sum(
            1 for rpt in reports if rpt.rules[rule_idx].passed
        )
        rate = 100.0 * passed_for_rule / len(reports) if reports else 0.0
        lines.append(f"  Rule {rule_num} ({rule_name:12s}): {passed_for_rule}/{len(reports)} ({rate:.0f}%)")

    lines.append("")

    # List failing simulations per rule
    lines.append("-" * 60)
    lines.append("FAILING SIMULATIONS PER RULE")
    lines.append("-" * 60)
    for rule_idx in range(len(ALL_RULE_CHECKERS)):
        rule_num = rule_idx + 1
        rule_name = reports[0].rules[rule_idx].rule_name if reports else f"Rule {rule_num}"
        failing = [
            rpt.sim_id for rpt in reports if not rpt.rules[rule_idx].passed
        ]
        if failing:
            lines.append(f"  Rule {rule_num} ({rule_name}): {len(failing)} failing")
            for sid in failing[:10]:  # Show first 10
                lines.append(f"    - {sid}")
            if len(failing) > 10:
                lines.append(f"    ... and {len(failing) - 10} more")
        else:
            lines.append(f"  Rule {rule_num} ({rule_name}): ALL PASS")

    lines.append("")
    return "\n".join(lines)


# ===========================================================================
# Pytest test class
# ===========================================================================
class TestSSOTFullCompliance:
    """
    Pytest test class that checks all 9 SSOT rules against every simulation
    in the pipeline.
    """

    @pytest.fixture(scope="class")
    def all_sims(self) -> List[SimulationBase]:
        return get_all_simulations()

    @pytest.fixture(scope="class")
    def all_reports(self, all_sims) -> List[SimComplianceReport]:
        return [check_simulation(sim) for sim in all_sims]

    # -----------------------------------------------------------------------
    # Individual rule tests
    # -----------------------------------------------------------------------

    def test_rule_1_formulas(self, all_sims):
        """Rule 1: Every simulation provides >=1 Formula with derivation, terms, category."""
        failures = []
        for sim in all_sims:
            result = check_rule_1_formulas(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 1 (Formulas) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_2_parameters(self, all_sims):
        """Rule 2: Every simulation provides >=1 Parameter with units, description, bounds."""
        failures = []
        for sim in all_sims:
            result = check_rule_2_parameters(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 2 (Parameters) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_3_sections(self, all_sims):
        """Rule 3: Every simulation provides SectionContent with >=1 paragraph >50 chars."""
        failures = []
        for sim in all_sims:
            result = check_rule_3_sections(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 3 (Sections) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_4_certificates(self, all_sims):
        """Rule 4: Every simulation provides >=1 certificate with id/assertion/condition/status."""
        failures = []
        for sim in all_sims:
            result = check_rule_4_certificates(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 4 (Certificates) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_5_validation(self, all_sims):
        """Rule 5: Every simulation provides >=1 validation check with name/passed/log_level."""
        failures = []
        for sim in all_sims:
            result = check_rule_5_validation(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 5 (Validation) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_6_references(self, all_sims):
        """Rule 6: Every simulation provides >=1 reference with id/authors/title/year/url|doi."""
        failures = []
        for sim in all_sims:
            result = check_rule_6_references(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 6 (References) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_7_learning(self, all_sims):
        """Rule 7: Every simulation provides >=1 learning material with topic/url/relevance."""
        failures = []
        for sim in all_sims:
            result = check_rule_7_learning(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 7 (Learning) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_8_inputs(self, all_sims):
        """Rule 8: Every non-seed simulation has >=1 required_inputs entry."""
        failures = []
        for sim in all_sims:
            result = check_rule_8_inputs(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 8 (PM Inputs) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    def test_rule_9_gate_checks(self, all_sims):
        """Rule 9: Every simulation's get_gate_checks() returns a list."""
        failures = []
        for sim in all_sims:
            result = check_rule_9_gate_checks(sim)
            if not result.passed:
                failures.append(f"{sim.metadata.id}: {result.details}")

        if failures:
            msg = f"Rule 9 (Gate Checks) failed for {len(failures)} simulation(s):\n"
            msg += "\n".join(f"  - {f}" for f in failures)
            pytest.fail(msg)

    # -----------------------------------------------------------------------
    # Aggregate test
    # -----------------------------------------------------------------------

    def test_aggregate_compliance_percentage(self, all_reports):
        """Report aggregate compliance percentage (informational, always passes)."""
        total_rules = sum(r.total_count for r in all_reports)
        total_passed = sum(r.passed_count for r in all_reports)
        pct = 100.0 * total_passed / total_rules if total_rules else 0.0

        import warnings
        warnings.warn(
            f"\nSSOT Full Compliance: {pct:.1f}% "
            f"({total_passed}/{total_rules} checks across {len(all_reports)} simulations). "
            f"Run standalone for full report: python tests/test_ssot_full_compliance.py\n"
        )

    def test_simulation_count_sanity(self, all_sims):
        """Sanity check: pipeline should register a non-trivial number of simulations."""
        assert len(all_sims) >= 10, (
            f"Only {len(all_sims)} simulations found in pipeline, expected >= 10. "
            f"Check SimulationRunner.phases for missing imports."
        )


# ===========================================================================
# Standalone main()
# ===========================================================================
def _run_gemini_review(reports: List[SimComplianceReport], fail_only: bool = True):
    """Run Gemini peer review on simulations that fail compliance checks.

    Requires GEMINI_API_KEY or GOOGLE_API_KEY environment variable.
    When fail_only=True (default), only reviews failing simulations.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("\n[GEMINI] No API key found (GEMINI_API_KEY or GOOGLE_API_KEY).")
        print("[GEMINI] Skipping Gemini peer review. Set one to enable.")
        return

    try:
        scripts_dir = PROJECT_ROOT / "scripts" / "validation"
        sys.path.insert(0, str(scripts_dir.parent.parent))
        from scripts.validation.gemini_peer_review import (
            GeminiClient, SimulationAnalyzer, get_theory_context,
            review_simulation_file, review_paper_sections,
        )
    except ImportError as e:
        print(f"\n[GEMINI] Could not import gemini_peer_review module: {e}")
        return

    # Select simulations to review
    if fail_only:
        target_ids = {r.sim_id for r in reports if not r.all_passed}
    else:
        target_ids = {r.sim_id for r in reports}

    if not target_ids:
        print("\n[GEMINI] All simulations pass compliance — no review needed.")
        return

    print(f"\n{'=' * 72}")
    print(f"  GEMINI PEER REVIEW — {len(target_ids)} simulation(s)")
    print(f"{'=' * 72}")

    client = GeminiClient(api_key)
    analyzer = SimulationAnalyzer()
    theory_context = get_theory_context()

    all_files = analyzer.get_all_simulation_files()
    review_files = []
    for fpath in all_files:
        try:
            text = fpath.read_text(encoding='utf-8')
            for tid in target_ids:
                if tid in text:
                    review_files.append(fpath)
                    break
        except Exception:
            pass

    print(f"  Matched {len(review_files)} files to review.\n")

    import json
    all_reviews = []
    for i, fpath in enumerate(review_files, 1):
        try:
            review, report = review_simulation_file(
                client, analyzer, fpath, theory_context, auto_fix=True
            )
            all_reviews.append(review)

            # Save .review.md next to file
            report_path = fpath.with_suffix('.review.md')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)

            score = review.get("overall_score", 0)
            print(f"  [{i}/{len(review_files)}] {fpath.name}: {score:.1f}/10 -> {report_path.name}")

            import time
            if i < len(review_files):
                time.sleep(1)

        except Exception as e:
            print(f"  [{i}/{len(review_files)}] {fpath.name}: ERROR - {e}")

    # Save aggregate
    if all_reviews:
        from datetime import datetime
        output = {
            "timestamp": datetime.now().isoformat(),
            "source": "ssot_compliance_checker",
            "files_reviewed": len(all_reviews),
            "file_reviews": all_reviews,
        }
        scores = [r.get("overall_score", 0) for r in all_reviews if "overall_score" in r]
        if scores:
            output["aggregate"] = {
                "mean_score": sum(scores) / len(scores),
                "min_score": min(scores),
                "max_score": max(scores),
                "below_7": sum(1 for s in scores if s < 7),
            }
        out_path = PROJECT_ROOT / "AutoGenerated" / "gemini_peer_review_results.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n  Results saved to: {out_path}")


def main():
    """Run the full SSOT compliance checker and print a detailed report."""
    import argparse

    parser = argparse.ArgumentParser(
        description="SSOT Full Compliance Checker - validates all simulations against 9 schema rules"
    )
    parser.add_argument(
        "--rule", "-r", type=int, default=None, choices=range(1, 10),
        help="Check only a specific rule (1-9)"
    )
    parser.add_argument(
        "--sim", "-s", type=str, default=None,
        help="Check only a specific simulation by ID (substring match)"
    )
    parser.add_argument(
        "--fail-only", "-f", action="store_true",
        help="Show only failing simulations"
    )
    parser.add_argument(
        "--gemini", action="store_true",
        help="Run Gemini AI peer review on failing simulations (requires GEMINI_API_KEY)"
    )
    parser.add_argument(
        "--gemini-all", action="store_true",
        help="Run Gemini AI peer review on ALL simulations (requires GEMINI_API_KEY)"
    )
    args = parser.parse_args()

    print("SSOT Full Compliance Checker v23.3")
    print("Loading simulations from pipeline...")

    all_sims = get_all_simulations()
    print(f"Found {len(all_sims)} simulations in {len(set(type(s).__name__ for s in all_sims))} classes\n")

    # Filter by simulation ID if requested
    if args.sim:
        filtered = [s for s in all_sims if args.sim.lower() in s.metadata.id.lower()]
        if not filtered:
            print(f"No simulation matching '{args.sim}' found.")
            print("Available simulations:")
            for s in all_sims:
                print(f"  - {s.metadata.id}")
            sys.exit(1)
        all_sims = filtered
        print(f"Filtered to {len(all_sims)} simulation(s) matching '{args.sim}'")

    # Run all checks
    reports: List[SimComplianceReport] = []
    for sim in all_sims:
        report = check_simulation(sim)

        # If filtering by rule, keep only that rule's results
        if args.rule:
            report.rules = [r for r in report.rules if r.rule_number == args.rule]

        reports.append(report)

    # Filter to failures only if requested
    if args.fail_only:
        reports = [r for r in reports if not r.all_passed]

    # Print report
    print(generate_full_report(reports))

    # Gemini peer review (optional)
    if args.gemini:
        _run_gemini_review(reports, fail_only=True)
    elif args.gemini_all:
        _run_gemini_review(reports, fail_only=False)

    # Exit code: number of failing simulations
    failing = sum(1 for r in reports if not r.all_passed)
    sys.exit(failing)


if __name__ == "__main__":
    main()
