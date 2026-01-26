"""
SSOT Compliance Validator v23.3
================================
Scans ALL simulation Python files for parameter lookups (get_latex, get_latex_term,
get_latex_sum, get_latex_frac, param_id references) and validates each code name
against the FormulasRegistry LATEX_REGISTRY and HEBREW_SYMBOL_REGISTRY.

Reports unregistered names with file path, line number, and context.

## How the SSOT System Works

The FormulasRegistry (core/FormulasRegistry.py) is the Single Source of Truth for
all PM parameter names, LaTeX symbols, and Hebrew gematria values.

### Key Registries:
- LATEX_REGISTRY: Maps canonical code names → LaTeX symbol strings (131+ entries)
- HEBREW_SYMBOL_REGISTRY: Maps canonical code names → {symbol, gematria, value, ...}
- SYMBOL_MAP: Maps Greek/Latin symbol keys → canonical property names

### Strict Mode (v23+):
- get_latex(param_name) raises KeyError if param_name is not in LATEX_REGISTRY
  or HEBREW_SYMBOL_REGISTRY. No legacy fallback.
- Legacy names (b3, chi_eff, visible_sector, etc.) are REJECTED.
- Use canonical names only: elder_kads, mephorash_chi, sophian_modulus, etc.

### Legacy → Canonical Name Mapping:
    b3                  → elder_kads        (Betti number b₃ = 24)
    chi_eff             → mephorash_chi     (Euler characteristic χ_eff = 72)
    chi_eff_total       → mephorash_chi     (total χ_eff = 144)
    visible_sector      → sophian_modulus   (visible dimensions = 125)
    sterile_sector      → barbelo_modulus   (sterile sector = 163)
    roots_total         → nitzotzin_roots   (root count = 288)
    shadow_sector       → demiurgic_Yetts   (shadow = 13)
    watts_constant      → monad_unity       (observer unity = 1.0)
    reid_invariant      → nitsot_par        (mirror parity = 1/144)
    odowd_bulk_pressure → barbelo_modulus   (bulk pressure = 163)
    christ_constant     → logos_joint       (logos potential = 153)
    decad               → residual_key      (core flux residual = 10)
    horos               → pleroma_boundary  (boundary = 30)

### Formula LaTeX Template System:
Formulas can use <<param_name>> placeholders in LaTeX strings:
    r"\\sum_{n=1}^{<<sophian_modulus>>} \\omega_n"
→   r"\\sum_{n=1}^{\\text{ק}_{\\text{כה}}} \\omega_n"

Use FormulasRegistry.render_formula(template) to substitute.

### How to Fix Violations:
1. Replace legacy name in get_latex("old_name") with canonical name
2. Replace legacy name in param_id "topology.old_name" with canonical name
3. Replace legacy name in get_latex_term("old_name") with canonical name
4. For new parameters, add entry to LATEX_REGISTRY in FormulasRegistry.py
5. Sync changes across all 3 package copies:
   - core/FormulasRegistry.py (root)
   - Principia_Metaphysica-Demon_Lock_FULL/core/FormulasRegistry.py
   - Principia_Metaphysica-Demon_Lock/core/FormulasRegistry.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any
from dataclasses import dataclass, field

import pytest

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.core.FormulasRegistry import FormulasRegistry


# ===========================================================================
# Legacy names that MUST NOT appear in get_latex/param_id calls
# ===========================================================================
LEGACY_NAMES = {
    "b3": "elder_kads",
    "chi_eff": "mephorash_chi",
    "chi_eff_total": "mephorash_chi",
    "visible_sector": "sophian_modulus",
    "sterile_sector": "barbelo_modulus",
    "roots_total": "nitzotzin_roots",
    "shadow_sector": "demiurgic_Yetts",
    "watts_constant": "monad_unity",
    "reid_invariant": "nitsot_par",
    "odowd_bulk_pressure": "barbelo_modulus",
    "christ_constant": "logos_joint",
    "total_local_pairs": None,  # no direct replacement
    "total_effective_pairs": None,  # no direct replacement
    "decad": "residual_key",
    "horos": "pleroma_boundary",
}


@dataclass
class Violation:
    """A single SSOT compliance violation."""
    file_path: str
    line_number: int
    line_text: str
    param_name: str
    call_type: str  # 'get_latex', 'get_latex_term', 'get_latex_sum', 'get_latex_frac', 'param_id', 'render_formula'
    is_legacy: bool
    canonical_name: str = ""  # suggested replacement for legacy names

    def __str__(self) -> str:
        fix = f" → use '{self.canonical_name}'" if self.canonical_name else ""
        return (
            f"  {self.file_path}:{self.line_number}\n"
            f"    [{self.call_type}] '{self.param_name}'"
            f" {'(LEGACY)' if self.is_legacy else '(UNREGISTERED)'}{fix}\n"
            f"    {self.line_text.strip()}"
        )


# ===========================================================================
# Regex patterns to find param lookups in Python source
# ===========================================================================
# get_latex("param_name") or get_latex('param_name')
RE_GET_LATEX = re.compile(
    r'''get_latex\(\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']\s*\)'''
)

# get_latex_term("param_name") or get_latex_term('param_name', ...)
RE_GET_LATEX_TERM = re.compile(
    r'''get_latex_term\(\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']'''
)

# get_latex_sum(..., "upper_param", ...) — extract the 3rd arg (upper bound param)
RE_GET_LATEX_SUM = re.compile(
    r'''get_latex_sum\(\s*["'][^"']*["']\s*,\s*["'][^"']*["']\s*,\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']'''
)

# get_latex_frac("num_param", "den_param")
RE_GET_LATEX_FRAC = re.compile(
    r'''get_latex_frac\(\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']\s*,\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']'''
)

# param_id references like "topology.b3" or 'gauge.alpha_inverse'
RE_PARAM_ID = re.compile(
    r'''["'](topology|gauge|cosmology|geometry|constants|physics|dimensions|higgs|qed|fermion|neutrino|dark_energy|prediction|pneuma|gravity|thermal|proton|moduli|quantum_bio|dark_matter|validation)\.([a-zA-Z_][a-zA-Z0-9_]*)["']'''
)

# <<param_name>> placeholders in render_formula templates
RE_TEMPLATE_PLACEHOLDER = re.compile(r'<<([a-zA-Z_][a-zA-Z0-9_]*)>>')


def get_registered_params() -> Set[str]:
    """Get the set of all valid param names from FormulasRegistry."""
    valid = set()
    valid.update(FormulasRegistry.LATEX_REGISTRY.keys())
    valid.update(FormulasRegistry.HEBREW_SYMBOL_REGISTRY.keys())
    # Also include SYMBOL_MAP property names (they should all be in LATEX_REGISTRY)
    for _sym, prop_name in FormulasRegistry.SYMBOL_MAP.items():
        valid.add(prop_name)
    return valid


def scan_file(file_path: str, registered_params: Set[str]) -> List[Violation]:
    """Scan a single Python file for param lookup violations."""
    violations = []

    # Skip self — example text contains legacy names intentionally
    basename = os.path.basename(file_path)
    if basename in ('test_ssot_compliance.py', 'validate_ssot_compliance.py'):
        return violations

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return violations

    for line_num, line in enumerate(lines, start=1):
        # Skip comments-only lines
        stripped = line.strip()
        if stripped.startswith('#'):
            continue

        # 1. get_latex("param_name")
        for match in RE_GET_LATEX.finditer(line):
            param = match.group(1)
            _check_param(param, 'get_latex', file_path, line_num, line,
                         registered_params, violations)

        # 2. get_latex_term("param_name")
        for match in RE_GET_LATEX_TERM.finditer(line):
            param = match.group(1)
            _check_param(param, 'get_latex_term', file_path, line_num, line,
                         registered_params, violations)

        # 3. get_latex_sum(..., "upper_param", ...)
        for match in RE_GET_LATEX_SUM.finditer(line):
            param = match.group(1)
            _check_param(param, 'get_latex_sum', file_path, line_num, line,
                         registered_params, violations)

        # 4. get_latex_frac("num", "den")
        for match in RE_GET_LATEX_FRAC.finditer(line):
            for param in [match.group(1), match.group(2)]:
                _check_param(param, 'get_latex_frac', file_path, line_num, line,
                             registered_params, violations)

        # 5. param_id "category.param_name"
        for match in RE_PARAM_ID.finditer(line):
            param = match.group(2)
            _check_param(param, 'param_id', file_path, line_num, line,
                         registered_params, violations)

        # 6. <<param_name>> template placeholders
        for match in RE_TEMPLATE_PLACEHOLDER.finditer(line):
            param = match.group(1)
            _check_param(param, 'render_formula', file_path, line_num, line,
                         registered_params, violations)

    return violations


def _check_param(param: str, call_type: str, file_path: str, line_num: int,
                 line: str, registered_params: Set[str],
                 violations: List[Violation]) -> None:
    """Check a single param name against the registry."""
    # Skip known non-param patterns (loop variables, math vars)
    if param in ('n', 'i', 'j', 'k', 'x', 'y', 'z', 'r', 't', 'idx',
                 'key', 'value', 'name', 'path', 'self', 'cls'):
        return

    is_legacy = param in LEGACY_NAMES
    is_registered = param in registered_params

    if is_legacy:
        canonical = LEGACY_NAMES[param] or "(no direct replacement)"
        violations.append(Violation(
            file_path=file_path,
            line_number=line_num,
            line_text=line,
            param_name=param,
            call_type=call_type,
            is_legacy=True,
            canonical_name=canonical,
        ))
    elif not is_registered:
        violations.append(Violation(
            file_path=file_path,
            line_number=line_num,
            line_text=line,
            param_name=param,
            call_type=call_type,
            is_legacy=False,
        ))


def scan_directory(directory: str, registered_params: Set[str]) -> List[Violation]:
    """Scan all Python files in a directory recursively."""
    all_violations = []
    dir_path = Path(directory)

    if not dir_path.exists():
        return all_violations

    for py_file in sorted(dir_path.rglob("*.py")):
        # Skip __pycache__ and .pyc files
        if '__pycache__' in str(py_file):
            continue
        violations = scan_file(str(py_file), registered_params)
        all_violations.extend(violations)

    return all_violations


def generate_report(violations: List[Violation]) -> str:
    """Generate a human-readable compliance report."""
    if not violations:
        return "[PASS] All param lookups use registered canonical code names.\n"

    # Group by file
    by_file: Dict[str, List[Violation]] = {}
    for v in violations:
        by_file.setdefault(v.file_path, []).append(v)

    legacy_count = sum(1 for v in violations if v.is_legacy)
    unregistered_count = sum(1 for v in violations if not v.is_legacy)

    lines = [
        "=" * 80,
        "SSOT COMPLIANCE REPORT",
        "=" * 80,
        f"Total violations: {len(violations)}",
        f"  Legacy names:     {legacy_count}",
        f"  Unregistered:     {unregistered_count}",
        f"  Files affected:   {len(by_file)}",
        "",
    ]

    for file_path, file_violations in sorted(by_file.items()):
        rel = os.path.relpath(file_path)
        lines.append(f"--- {rel} ({len(file_violations)} violations) ---")
        for v in file_violations:
            fix = f" → use '{v.canonical_name}'" if v.canonical_name else ""
            tag = "LEGACY" if v.is_legacy else "UNREGISTERED"
            lines.append(
                f"  L{v.line_number}: [{v.call_type}] '{v.param_name}' ({tag}){fix}"
            )
            lines.append(f"         {v.line_text.strip()[:120]}")
        lines.append("")

    # Add fix instructions
    lines.extend([
        "=" * 80,
        "HOW TO FIX",
        "=" * 80,
        "",
        "LEGACY NAMES: Replace with canonical name in the SSOT mapping above.",
        "  Example: get_latex('b3') → get_latex('elder_kads')",
        "  Example: 'topology.b3'  → 'topology.elder_kads'",
        "",
        "UNREGISTERED NAMES: Either:",
        "  1. Add the param to LATEX_REGISTRY in core/FormulasRegistry.py",
        "  2. Or use an existing canonical name from LATEX_REGISTRY",
        "",
        "After fixing, sync FormulasRegistry.py to all 3 packages:",
        "  - core/FormulasRegistry.py (root)",
        "  - Principia_Metaphysica-Demon_Lock_FULL/core/FormulasRegistry.py",
        "  - Principia_Metaphysica-Demon_Lock/core/FormulasRegistry.py",
        "",
        "Run: pytest tests/test_ssot_compliance.py -v  to verify compliance.",
    ])

    return "\n".join(lines)


# ===========================================================================
# Pytest Tests
# ===========================================================================

class TestSSOTComplianceSimulations:
    """Validate all simulation files use registered canonical param names."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.registered = get_registered_params()
        self.project_root = Path(__file__).parent.parent

    def _get_sim_dirs(self) -> List[Path]:
        """Get all simulation directories to scan."""
        dirs = []
        # Root simulations
        root_sim = self.project_root / "simulations"
        if root_sim.exists():
            dirs.append(root_sim)
        # FULL package simulations
        full_sim = self.project_root / "Principia_Metaphysica-Demon_Lock_FULL" / "simulations"
        if full_sim.exists():
            dirs.append(full_sim)
        # Demon_Lock package simulations
        dl_sim = self.project_root / "Principia_Metaphysica-Demon_Lock" / "simulations"
        if dl_sim.exists():
            dirs.append(dl_sim)
        return dirs

    def test_no_legacy_names_in_get_latex(self):
        """No simulation file uses legacy names in get_latex() calls."""
        all_violations = []
        for sim_dir in self._get_sim_dirs():
            violations = scan_directory(str(sim_dir), self.registered)
            legacy = [v for v in violations if v.is_legacy and v.call_type == 'get_latex']
            all_violations.extend(legacy)

        if all_violations:
            report = generate_report(all_violations)
            pytest.fail(f"Legacy names found in get_latex() calls:\n{report}")

    def test_no_legacy_names_in_param_ids(self):
        """No simulation file uses legacy names in param_id references."""
        all_violations = []
        for sim_dir in self._get_sim_dirs():
            violations = scan_directory(str(sim_dir), self.registered)
            legacy = [v for v in violations if v.is_legacy and v.call_type == 'param_id']
            all_violations.extend(legacy)

        if all_violations:
            report = generate_report(all_violations)
            pytest.fail(f"Legacy names found in param_id references:\n{report}")

    def test_no_legacy_names_in_latex_term(self):
        """No simulation file uses legacy names in get_latex_term() calls."""
        all_violations = []
        for sim_dir in self._get_sim_dirs():
            violations = scan_directory(str(sim_dir), self.registered)
            legacy = [v for v in violations if v.is_legacy and v.call_type == 'get_latex_term']
            all_violations.extend(legacy)

        if all_violations:
            report = generate_report(all_violations)
            pytest.fail(f"Legacy names found in get_latex_term() calls:\n{report}")

    def test_no_unregistered_get_latex_calls(self):
        """All get_latex() calls reference registered param names."""
        all_violations = []
        for sim_dir in self._get_sim_dirs():
            violations = scan_directory(str(sim_dir), self.registered)
            unregistered = [v for v in violations
                           if not v.is_legacy and v.call_type == 'get_latex']
            all_violations.extend(unregistered)

        if all_violations:
            report = generate_report(all_violations)
            pytest.fail(f"Unregistered params in get_latex() calls:\n{report}")

    def test_no_unregistered_template_placeholders(self):
        """All <<param_name>> placeholders in formulas resolve to registered params."""
        all_violations = []
        for sim_dir in self._get_sim_dirs():
            violations = scan_directory(str(sim_dir), self.registered)
            unregistered = [v for v in violations
                           if v.call_type == 'render_formula']
            all_violations.extend(unregistered)

        if all_violations:
            report = generate_report(all_violations)
            pytest.fail(f"Unresolved <<param>> placeholders:\n{report}")

    def test_full_scan_summary(self):
        """Generate full compliance scan (informational — passes with warnings)."""
        all_violations = []
        for sim_dir in self._get_sim_dirs():
            violations = scan_directory(str(sim_dir), self.registered)
            all_violations.extend(violations)

        if all_violations:
            report = generate_report(all_violations)
            # Log as warning, don't fail
            import warnings
            warnings.warn(
                f"\nSSOT Compliance: {len(all_violations)} total violations found.\n"
                f"Run standalone for full report: python tests/test_ssot_compliance.py\n"
            )


class TestSSOTComplianceCoreFiles:
    """Validate core Python files use registered param names."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.registered = get_registered_params()
        self.project_root = Path(__file__).parent.parent

    def test_core_files_no_legacy_get_latex(self):
        """Core Python files don't use legacy names in get_latex()."""
        core_dir = self.project_root / "core"
        if not core_dir.exists():
            pytest.skip("core/ directory not found")

        violations = scan_directory(str(core_dir), self.registered)
        legacy = [v for v in violations if v.is_legacy and v.call_type == 'get_latex']

        if legacy:
            report = generate_report(legacy)
            pytest.fail(f"Legacy names in core/ get_latex() calls:\n{report}")

    def test_config_no_legacy_param_ids(self):
        """config.py doesn't use legacy names in param_id references."""
        for pkg in ['', 'Principia_Metaphysica-Demon_Lock_FULL',
                     'Principia_Metaphysica-Demon_Lock']:
            config_path = self.project_root / pkg / "config.py"
            if config_path.exists():
                violations = scan_file(str(config_path), self.registered)
                legacy = [v for v in violations if v.is_legacy and v.call_type == 'param_id']
                if legacy:
                    report = generate_report(legacy)
                    pytest.fail(f"Legacy param_ids in {config_path}:\n{report}")


class TestSSOTRegistryIntegrity:
    """Validate the registry itself is self-consistent."""

    def test_registered_param_count(self):
        """Registry has expected minimum param count."""
        registered = get_registered_params()
        assert len(registered) >= 100, (
            f"Only {len(registered)} registered params, expected >= 100"
        )

    def test_legacy_names_not_registered(self):
        """Legacy names are NOT in the registry (they were removed)."""
        registered = get_registered_params()
        for legacy_name in LEGACY_NAMES:
            assert legacy_name not in registered, (
                f"Legacy name '{legacy_name}' should not be in registered params"
            )

    def test_canonical_names_are_registered(self):
        """All canonical replacement names ARE in the registry."""
        registered = get_registered_params()
        for legacy, canonical in LEGACY_NAMES.items():
            if canonical and canonical != "(no direct replacement)":
                assert canonical in registered, (
                    f"Canonical name '{canonical}' (replacement for '{legacy}') "
                    f"is not registered"
                )


# ===========================================================================
# Standalone runner
# ===========================================================================

def main():
    """Run full SSOT compliance scan and print report."""
    import argparse

    parser = argparse.ArgumentParser(
        description="SSOT Compliance Validator - scans simulation files for param lookup violations"
    )
    parser.add_argument('--dir', '-d', type=str, default=None,
                        help='Directory to scan (default: all simulation dirs)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all violations with context')
    parser.add_argument('--legacy-only', action='store_true',
                        help='Only report legacy name usage')
    args = parser.parse_args()

    registered = get_registered_params()
    project_root = Path(__file__).parent.parent

    print("SSOT Compliance Validator v23.3")
    print(f"Registered params: {len(registered)}")
    print()

    # Determine directories to scan
    if args.dir:
        scan_dirs = [Path(args.dir)]
    else:
        scan_dirs = []
        for subdir in ['simulations', 'core']:
            # Root
            d = project_root / subdir
            if d.exists():
                scan_dirs.append(d)
            # FULL
            d = project_root / "Principia_Metaphysica-Demon_Lock_FULL" / subdir
            if d.exists():
                scan_dirs.append(d)
            # Demon_Lock
            d = project_root / "Principia_Metaphysica-Demon_Lock" / subdir
            if d.exists():
                scan_dirs.append(d)

        # Also scan config.py files
        for pkg in ['', 'Principia_Metaphysica-Demon_Lock_FULL',
                     'Principia_Metaphysica-Demon_Lock']:
            config = project_root / pkg / "config.py"
            if config.exists():
                scan_dirs.append(config)

    all_violations = []
    for scan_path in scan_dirs:
        if scan_path.is_file():
            violations = scan_file(str(scan_path), registered)
        else:
            violations = scan_directory(str(scan_path), registered)
        all_violations.extend(violations)

    if args.legacy_only:
        all_violations = [v for v in all_violations if v.is_legacy]

    report = generate_report(all_violations)
    print(report)

    # Exit code: 0 if clean, 1 if violations found
    sys.exit(0 if not all_violations else 1)


if __name__ == "__main__":
    main()
