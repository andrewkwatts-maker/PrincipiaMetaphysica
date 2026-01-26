"""
LaTeX Registry Unit Test Suite v23.3
====================================
Validates the FormulasRegistry LaTeX SSoT system:
- All LATEX_REGISTRY entries produce valid LaTeX
- Bi-directional coverage: PM Params ↔ LaTeX symbols
- No legacy/old parameter names accepted
- render_formula() template substitution
- All 72 gates covered
- Balanced braces and non-empty strings

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
import sys
from pathlib import Path

import pytest

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.core.FormulasRegistry import FormulasRegistry


# ===========================================================================
# Known legacy/old parameter names that MUST NOT resolve
# ===========================================================================
LEGACY_NAMES = [
    "b3", "chi_eff", "chi_eff_total", "visible_sector", "sterile_sector",
    "roots_total", "shadow_sector", "christ_constant", "horos", "decad",
    "watts_constant", "reid_invariant", "odowd_bulk_pressure",
    "total_local_pairs", "total_effective_pairs",
]


class TestLatexRegistryCompleteness:
    """Tests for LATEX_REGISTRY structural completeness."""

    def test_all_latex_entries_non_empty(self):
        """Every LATEX_REGISTRY entry produces a non-empty string."""
        for key, latex in FormulasRegistry.LATEX_REGISTRY.items():
            assert latex and latex.strip(), (
                f"LATEX_REGISTRY['{key}'] is empty or whitespace-only"
            )

    def test_all_latex_entries_balanced_braces(self):
        """Every LaTeX string has balanced {{ }} braces."""
        for key, latex in FormulasRegistry.LATEX_REGISTRY.items():
            opens = latex.count("{")
            closes = latex.count("}")
            assert opens == closes, (
                f"LATEX_REGISTRY['{key}'] has unbalanced braces: "
                f"{opens} open vs {closes} close in '{latex}'"
            )

    def test_no_legacy_names_in_registry_keys(self):
        """LATEX_REGISTRY keys must be latest code names, not old_names."""
        for legacy_name in LEGACY_NAMES:
            assert legacy_name not in FormulasRegistry.LATEX_REGISTRY, (
                f"Legacy name '{legacy_name}' found as LATEX_REGISTRY key. "
                f"Use the canonical code name instead."
            )

    def test_hebrew_registry_fully_covered(self):
        """Every HEBREW_SYMBOL_REGISTRY entry has a LATEX_REGISTRY entry."""
        missing = []
        for key in FormulasRegistry.HEBREW_SYMBOL_REGISTRY:
            if key not in FormulasRegistry.LATEX_REGISTRY:
                missing.append(key)
        assert not missing, (
            f"HEBREW_SYMBOL_REGISTRY entries missing from LATEX_REGISTRY: {missing}"
        )

    def test_symbol_map_fully_covered(self):
        """Every SYMBOL_MAP property name has a LATEX_REGISTRY entry."""
        missing = []
        for _sym, prop_name in FormulasRegistry.SYMBOL_MAP.items():
            if prop_name not in FormulasRegistry.LATEX_REGISTRY:
                missing.append(prop_name)
        assert not missing, (
            f"SYMBOL_MAP properties missing from LATEX_REGISTRY: {missing}"
        )

    def test_latex_keys_have_properties(self):
        """Every LATEX_REGISTRY key (except spectral symbols) is a valid @property."""
        SPECTRAL_OPERATORS = {
            "spectral_residue", "spectral_weight", "g2_invariant",
            "sterile_tolerance",
        }
        missing = []
        registry = FormulasRegistry()
        for key in FormulasRegistry.LATEX_REGISTRY:
            if key in SPECTRAL_OPERATORS:
                continue
            if not hasattr(registry, key):
                missing.append(key)
        assert not missing, (
            f"LATEX_REGISTRY keys with no @property on FormulasRegistry: {missing}"
        )

    def test_all_gates_have_latex(self):
        """All 72 gate properties (G01-G72) have LATEX_REGISTRY entries."""
        missing_gates = []
        for sym, prop_name in FormulasRegistry.SYMBOL_MAP.items():
            if sym.startswith("G") and sym[1:].isdigit():
                if prop_name not in FormulasRegistry.LATEX_REGISTRY:
                    missing_gates.append(f"{sym} → {prop_name}")
        assert not missing_gates, (
            f"Gate properties missing from LATEX_REGISTRY: {missing_gates}"
        )

    def test_latex_no_duplicate_symbols(self):
        """No two different params map to the same LaTeX string."""
        seen = {}
        duplicates = []
        for key, latex in FormulasRegistry.LATEX_REGISTRY.items():
            if latex in seen:
                duplicates.append(f"'{key}' and '{seen[latex]}' both → '{latex}'")
            else:
                seen[latex] = key
        assert not duplicates, (
            f"Duplicate LaTeX symbols found: {duplicates}"
        )

    def test_minimum_entry_count(self):
        """LATEX_REGISTRY has at least 100 entries (gates + core params)."""
        count = len(FormulasRegistry.LATEX_REGISTRY)
        assert count >= 100, (
            f"LATEX_REGISTRY has only {count} entries, expected >= 100"
        )


class TestGetLatexStrict:
    """Tests for strict get_latex() behavior (no legacy fallback)."""

    def test_get_latex_raises_on_unknown(self):
        """get_latex() raises KeyError for unknown parameter names."""
        with pytest.raises(KeyError, match="Unknown parameter"):
            FormulasRegistry.get_latex("nonexistent_parameter_xyz")

    def test_get_latex_raises_on_legacy_names(self):
        """get_latex() raises KeyError for old/legacy names."""
        for legacy_name in LEGACY_NAMES:
            with pytest.raises(KeyError, match="Unknown parameter"):
                FormulasRegistry.get_latex(legacy_name)

    def test_get_latex_returns_correct_topological_symbols(self):
        """Spot-check key topological symbols."""
        checks = {
            "elder_kads":      r"\mathcal{E}_{\text{כד}}",
            "mephorash_chi":   r"\chi_{\text{עב}}",
            "sophian_modulus":  r"\text{ק}_{\text{כה}}",
            "barbelo_modulus":  r"\text{ק}_{\text{סג}}",
            "nitzotzin_roots":  r"\mathcal{N}_{\text{רפח}}",
            "logos_joint":     r"\Lambda_{\nu}",
        }
        for param, expected in checks.items():
            result = FormulasRegistry.get_latex(param)
            assert result == expected, (
                f"get_latex('{param}') returned '{result}', expected '{expected}'"
            )

    def test_get_latex_returns_correct_gate_symbols(self):
        """Gate symbols follow G_{{NN}} pattern."""
        assert FormulasRegistry.get_latex("gate_01_initial_action") == r"G_{01}"
        assert FormulasRegistry.get_latex("gate_36_fine_structure_alignment") == r"G_{36}"
        assert FormulasRegistry.get_latex("gate_72_absolute_closure") == r"G_{72}"

    def test_get_latex_returns_correct_physics_symbols(self):
        """Physics constants have correct LaTeX."""
        assert FormulasRegistry.get_latex("alpha_inverse") == r"\alpha^{-1}"
        assert FormulasRegistry.get_latex("higgs_vev") == r"v_{\text{EW}}"
        assert FormulasRegistry.get_latex("fermi_constant") == r"G_F"
        assert FormulasRegistry.get_latex("h0_local") == r"H_0"


class TestGetLatexTerm:
    """Tests for get_latex_term() metadata generation."""

    def test_returns_dict_with_required_fields(self):
        """get_latex_term() returns dict with symbol, param_id, description."""
        term = FormulasRegistry.get_latex_term("sophian_modulus")
        assert "symbol" in term
        assert "param_id" in term
        assert "description" in term

    def test_hebrew_entry_has_value(self):
        """HEBREW_SYMBOL_REGISTRY entries include numeric value."""
        term = FormulasRegistry.get_latex_term("sophian_modulus")
        assert term.get("value") == 125

    def test_param_id_uses_prefix(self):
        """param_id uses the provided prefix."""
        term = FormulasRegistry.get_latex_term("elder_kads", param_id_prefix="geometry")
        assert term["param_id"] == "geometry.elder_kads"

    def test_non_hebrew_entry_has_fallback_description(self):
        """Non-Hebrew entries get a formatted description."""
        term = FormulasRegistry.get_latex_term("alpha_inverse")
        assert "description" in term
        assert term["description"]  # non-empty


class TestRenderFormula:
    """Tests for render_formula() template substitution."""

    def test_basic_substitution(self):
        """Substitutes single placeholder correctly."""
        result = FormulasRegistry.render_formula(
            r"\sum_{n=1}^{<<sophian_modulus>>} x_n"
        )
        assert r"\text{ק}_{\text{כה}}" in result
        assert "<<" not in result

    def test_multiple_substitutions(self):
        """Substitutes multiple placeholders in one template."""
        result = FormulasRegistry.render_formula(
            r"\frac{<<elder_kads>>}{8} = <<n_gen>>"
        )
        assert r"\mathcal{E}_{\text{כד}}" in result
        assert r"n_{\text{gen}}" in result
        assert "<<" not in result

    def test_gate_substitution(self):
        """Gate placeholders resolve correctly."""
        result = FormulasRegistry.render_formula(r"<<gate_01_initial_action>> = 0.566")
        assert result == r"G_{01} = 0.566"

    def test_raises_on_unknown_placeholder(self):
        """Raises KeyError for unknown <<param>> placeholders."""
        with pytest.raises(KeyError):
            FormulasRegistry.render_formula(r"<<totally_fake_param>> = 42")

    def test_no_unresolved_placeholders(self):
        """After render, no <<...>> remain in output."""
        template = r"<<elder_kads>> + <<logos_joint>> = <<nitzotzin_roots>>"
        result = FormulasRegistry.render_formula(template)
        assert "<<" not in result
        assert ">>" not in result

    def test_passthrough_latex_without_placeholders(self):
        """Templates without <<>> pass through unchanged."""
        template = r"\alpha^{-1} \approx 137.036"
        result = FormulasRegistry.render_formula(template)
        assert result == template


class TestValidateLatexCoverage:
    """Tests for validate_latex_coverage() bi-directional check."""

    def test_bidirectional_validation_passes(self):
        """validate_latex_coverage() returns passed=True with no gaps."""
        result = FormulasRegistry.validate_latex_coverage()
        assert result["passed"], (
            f"Validation failed:\n"
            f"  latex_without_property: {result.get('latex_without_property', [])}\n"
            f"  hebrew_without_latex: {result.get('hebrew_without_latex', [])}\n"
            f"  symbol_map_without_latex: {result.get('symbol_map_without_latex', [])}\n"
            f"  invalid_latex: {result.get('invalid_latex', [])}\n"
            f"  duplicate_latex: {result.get('duplicate_latex', [])}"
        )

    def test_returns_entry_counts(self):
        """Validation result includes count metadata."""
        result = FormulasRegistry.validate_latex_coverage()
        assert result["total_latex_entries"] >= 100
        assert result["total_hebrew_entries"] >= 15
        assert result["total_symbol_map_entries"] >= 70


class TestValidateFormulaLatex:
    """Tests for validate_formula_latex() individual formula checks."""

    def test_valid_formula(self):
        """Valid LaTeX passes validation."""
        result = FormulasRegistry.validate_formula_latex(
            r"\sum_{n=1}^{125} \omega_n \mathcal{R}_n^2 = \Phi_{G_2}"
        )
        assert result["valid"]
        assert not result["errors"]

    def test_empty_formula_fails(self):
        """Empty LaTeX fails validation."""
        result = FormulasRegistry.validate_formula_latex("")
        assert not result["valid"]

    def test_unbalanced_braces_fails(self):
        """Unbalanced braces fail validation."""
        result = FormulasRegistry.validate_formula_latex(r"\frac{a}{b")
        assert not result["valid"]
        assert any("braces" in e.lower() for e in result["errors"])

    def test_formula_with_valid_placeholders(self):
        """Formula with valid <<param>> placeholders passes."""
        result = FormulasRegistry.validate_formula_latex(
            r"\sum_{n=1}^{<<sophian_modulus>>} x_n"
        )
        assert result["valid"]

    def test_formula_with_invalid_placeholder_fails(self):
        """Formula with unknown <<param>> fails."""
        result = FormulasRegistry.validate_formula_latex(
            r"\sum_{n=1}^{<<fake_param>>} x_n"
        )
        assert not result["valid"]


class TestBuilderMethods:
    """Tests for get_latex_sum() and get_latex_frac() builders."""

    def test_get_latex_sum(self):
        """get_latex_sum() builds correct sum expression."""
        result = FormulasRegistry.get_latex_sum(
            "n", "1", "sophian_modulus", r"\omega_n \mathcal{R}_n^2"
        )
        expected_upper = FormulasRegistry.get_latex("sophian_modulus")
        assert expected_upper in result
        assert r"\sum_{n=1}" in result

    def test_get_latex_frac(self):
        """get_latex_frac() builds correct fraction."""
        result = FormulasRegistry.get_latex_frac("elder_kads", "n_gen")
        assert r"\frac{" in result
        assert FormulasRegistry.get_latex("elder_kads") in result


class TestFormulaMetadataLatex:
    """Tests for FormulaMetadata.render_latex() and validate_latex()."""

    def _make_formula(self, latex: str) -> "FormulaMetadata":
        """Helper to create a minimal FormulaMetadata for testing."""
        from simulations.base.formulas import FormulaMetadata
        return FormulaMetadata(
            id="test-formula",
            label="(T.1)",
            section_id="test",
            latex=latex,
            plain_text="test",
            category="DERIVED",
            description="Test formula",
        )

    def test_render_latex_substitution(self):
        """FormulaMetadata.render_latex() substitutes <<param>> placeholders."""
        formula = self._make_formula(
            r"\sum_{n=1}^{<<sophian_modulus>>} \omega_n"
        )
        rendered = formula.render_latex()
        assert r"\text{ק}_{\text{כה}}" in rendered
        assert "<<" not in rendered

    def test_render_latex_passthrough(self):
        """Formulas without placeholders pass through unchanged."""
        raw = r"\alpha^{-1} \approx 137.036"
        formula = self._make_formula(raw)
        assert formula.render_latex() == raw

    def test_render_latex_multiple_params(self):
        """Multiple <<param>> placeholders all resolve."""
        formula = self._make_formula(
            r"\frac{<<elder_kads>>}{<<n_gen>>}"
        )
        rendered = formula.render_latex()
        assert r"\mathcal{E}_{\text{כד}}" in rendered
        assert r"n_{\text{gen}}" in rendered

    def test_validate_latex_valid(self):
        """Valid formula passes validation."""
        formula = self._make_formula(r"\sum_{n=1}^{125} x_n = 0")
        result = formula.validate_latex()
        assert result["valid"]
        assert not result["errors"]

    def test_validate_latex_unbalanced(self):
        """Unbalanced braces fail validation."""
        formula = self._make_formula(r"\frac{a}{b")
        result = formula.validate_latex()
        assert not result["valid"]

    def test_validate_latex_unknown_placeholder(self):
        """Unknown <<param>> fails validation."""
        formula = self._make_formula(r"<<nonexistent_xyz>> = 42")
        result = formula.validate_latex()
        assert not result["valid"]


class TestFormulaRegistryLatexValidation:
    """Tests for FormulaRegistry.validate_all_latex() and render_all_latex()."""

    def test_validate_all_latex_returns_structure(self):
        """validate_all_latex() returns dict with required keys."""
        from simulations.base.formulas import FormulaRegistry
        registry = FormulaRegistry()
        result = registry.validate_all_latex()
        assert "passed" in result
        assert "total_formulas" in result
        assert "valid_formulas" in result
        assert "invalid_formulas" in result
        assert "latex_coverage" in result

    def test_validate_all_latex_coverage_passes(self):
        """The latex_coverage bi-directional check passes."""
        from simulations.base.formulas import FormulaRegistry
        registry = FormulaRegistry()
        result = registry.validate_all_latex()
        assert result["latex_coverage"]["passed"], (
            f"LaTeX coverage check failed: {result['latex_coverage']}"
        )

    def test_render_all_latex_returns_dict(self):
        """render_all_latex() returns a dict of formula_id → LaTeX strings."""
        from simulations.base.formulas import FormulaRegistry
        registry = FormulaRegistry()
        rendered = registry.render_all_latex()
        assert isinstance(rendered, dict)
        for fid, latex in rendered.items():
            assert isinstance(latex, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
