"""
Comprehensive Unit Tests for PMRegistry

Tests all aspects of the PMRegistry singleton:
- Singleton pattern enforcement
- Parameter management with provenance
- Sigma deviation computation
- Prediction validation
- Status categories (ESTABLISHED, DERIVED, PREDICTED)
- Uncertainty propagation
- Integration with experimental data

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import pytest
import warnings
from datetime import datetime
from typing import Dict, Any

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from base.registry import PMRegistry, RegistryEntry, FormulaEntry, SectionEntry


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(autouse=True)
def reset_registry():
    """Reset the registry before each test to ensure test isolation."""
    PMRegistry.reset_instance()
    yield
    PMRegistry.reset_instance()


@pytest.fixture
def registry():
    """Provide a fresh PMRegistry instance."""
    return PMRegistry.get_instance()


@pytest.fixture
def sample_established_params(registry):
    """Populate registry with sample established parameters."""
    registry.set_param(
        "pdg.m_higgs",
        125.25,
        source="ESTABLISHED:PDG2024",
        uncertainty=0.17,
        status="ESTABLISHED"
    )
    registry.set_param(
        "pdg.alpha_em",
        0.007297353,
        source="ESTABLISHED:PDG2024",
        uncertainty=0.000000006,
        status="ESTABLISHED"
    )
    registry.set_param(
        "desi.w0",
        -0.727,
        source="ESTABLISHED:DESI_2025",
        uncertainty=0.067,
        status="ESTABLISHED"
    )
    return registry


@pytest.fixture
def sample_derived_params(registry):
    """Populate registry with sample derived parameters."""
    registry.set_param(
        "gauge.M_GUT",
        2.1e16,
        source="gauge_unification_v16_0",
        uncertainty=0.1e16,
        status="DERIVED"
    )
    registry.set_param(
        "gauge.ALPHA_GUT",
        0.0408,
        source="gauge_unification_v16_0",
        uncertainty=0.0005,
        status="DERIVED"
    )
    return registry


# =============================================================================
# Test 1: Singleton Pattern
# =============================================================================

class TestSingletonPattern:
    """Test that PMRegistry implements singleton pattern correctly."""

    def test_get_instance_returns_same_object(self):
        """Test that multiple calls to get_instance return the same object."""
        instance1 = PMRegistry.get_instance()
        instance2 = PMRegistry.get_instance()
        assert instance1 is instance2

    def test_direct_instantiation_returns_singleton(self):
        """Test that direct instantiation also returns singleton."""
        instance1 = PMRegistry.get_instance()
        instance2 = PMRegistry()
        assert instance1 is instance2

    def test_singleton_persists_data(self, registry):
        """Test that data persists across multiple get_instance calls."""
        registry.set_param("test.param", 42, source="test")

        # Get instance again
        registry2 = PMRegistry.get_instance()
        assert registry2.get_param("test.param") == 42

    def test_reset_instance_clears_data(self, registry):
        """Test that reset_instance clears all data."""
        registry.set_param("test.param", 42, source="test")
        assert registry.has_param("test.param")

        PMRegistry.reset_instance()
        registry2 = PMRegistry.get_instance()
        assert not registry2.has_param("test.param")


# =============================================================================
# Test 2: Parameter Get/Set with Provenance
# =============================================================================

class TestParameterManagement:
    """Test parameter storage, retrieval, and provenance tracking."""

    def test_set_and_get_param_basic(self, registry):
        """Test basic parameter set and get."""
        registry.set_param("test.param", 123.45, source="test_simulation")
        value = registry.get_param("test.param")
        assert value == 123.45

    def test_get_nonexistent_param_raises_keyerror(self, registry):
        """Test that getting non-existent parameter raises KeyError."""
        with pytest.raises(KeyError, match="Parameter 'nonexistent' not found"):
            registry.get_param("nonexistent")

    def test_has_param(self, registry):
        """Test has_param method."""
        assert not registry.has_param("test.param")
        registry.set_param("test.param", 42, source="test")
        assert registry.has_param("test.param")

    def test_get_entry_returns_full_metadata(self, registry):
        """Test get_entry returns complete RegistryEntry."""
        registry.set_param(
            "test.param",
            100.0,
            source="test_sim",
            uncertainty=5.0,
            status="DERIVED",
            metadata={"note": "test"}
        )

        entry = registry.get_entry("test.param")
        assert isinstance(entry, RegistryEntry)
        assert entry.value == 100.0
        assert entry.source == "test_sim"
        assert entry.uncertainty == 5.0
        assert entry.status == "DERIVED"
        assert entry.metadata["note"] == "test"

    def test_get_entry_nonexistent_returns_none(self, registry):
        """Test get_entry returns None for non-existent parameter."""
        entry = registry.get_entry("nonexistent")
        assert entry is None

    def test_provenance_tracking(self, registry):
        """Test that provenance is tracked correctly."""
        registry.set_param("test.param", 1.0, source="sim_v1")
        provenance = registry.export_provenance()
        assert "test.param" in provenance
        assert "sim_v1" in provenance["test.param"]

    def test_provenance_tracks_multiple_sources(self, registry):
        """Test provenance when parameter is set multiple times."""
        registry.set_param("test.param", 1.0, source="sim_v1")

        # Suppress warning for this test
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            registry.set_param("test.param", 1.1, source="sim_v2")

        provenance = registry.export_provenance()
        assert len(provenance["test.param"]) == 2
        assert "sim_v1" in provenance["test.param"]
        assert "sim_v2" in provenance["test.param"]

    def test_get_alias_method(self, registry):
        """Test that 'get' is an alias for 'get_param'."""
        registry.set_param("test.param", 42, source="test")
        assert registry.get("test.param") == 42


# =============================================================================
# Test 3: Status Categories
# =============================================================================

class TestStatusCategories:
    """Test different status categories and their enforcement."""

    @pytest.mark.parametrize("status", [
        "ESTABLISHED",
        "GEOMETRIC",
        "DERIVED",
        "PREDICTED",
        "CALIBRATED"
    ])
    def test_valid_status_categories(self, registry, status):
        """Test all valid status categories can be set."""
        registry.set_param(
            "test.param",
            1.0,
            source="test",
            status=status
        )
        entry = registry.get_entry("test.param")
        assert entry.status == status

    def test_established_params_cannot_be_overwritten(self, registry):
        """Test that ESTABLISHED parameters cannot be overridden by non-ESTABLISHED sources."""
        registry.set_param(
            "pdg.m_higgs",
            125.25,
            source="ESTABLISHED:PDG2024",
            status="ESTABLISHED"
        )

        with pytest.raises(ValueError, match="Cannot override ESTABLISHED param"):
            registry.set_param(
                "pdg.m_higgs",
                125.0,
                source="simulation_v1",
                status="DERIVED"
            )

    def test_established_params_can_be_updated_by_established_source(self, registry):
        """Test that ESTABLISHED parameters can be updated by another ESTABLISHED source."""
        registry.set_param(
            "pdg.m_higgs",
            125.25,
            source="ESTABLISHED:PDG2024",
            status="ESTABLISHED"
        )

        # This should work (though may warn)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            registry.set_param(
                "pdg.m_higgs",
                125.26,
                source="ESTABLISHED:PDG2025",
                status="ESTABLISHED"
            )

        assert registry.get_param("pdg.m_higgs") == 125.26

    def test_derived_params_in_validation(self, registry):
        """Test that DERIVED params without provenance show up in validation."""
        # Manually add param without using set_param to bypass provenance
        entry = RegistryEntry(
            value=1.0,
            source="unknown",
            status="DERIVED"
        )
        registry._parameters["orphan.param"] = entry

        issues = registry.validate_all()
        assert any("orphan.param" in issue for issue in issues)


# =============================================================================
# Test 4: Uncertainty Propagation
# =============================================================================

class TestUncertaintyPropagation:
    """Test uncertainty storage and propagation."""

    def test_uncertainty_stored_correctly(self, registry):
        """Test that uncertainty is stored and retrieved."""
        registry.set_param(
            "test.param",
            100.0,
            source="test",
            uncertainty=2.5
        )
        entry = registry.get_entry("test.param")
        assert entry.uncertainty == 2.5

    def test_none_uncertainty_handled(self, registry):
        """Test that None uncertainty is handled gracefully."""
        registry.set_param("test.param", 100.0, source="test")
        entry = registry.get_entry("test.param")
        assert entry.uncertainty is None

    def test_uncertainty_in_export(self, registry):
        """Test that uncertainty appears in exported data."""
        registry.set_param(
            "test.param",
            100.0,
            source="test",
            uncertainty=5.0
        )

        exported = registry.export_parameters()
        assert exported["test.param"]["uncertainty"] == 5.0


# =============================================================================
# Test 5: Sigma Deviation Computation
# =============================================================================

class TestSigmaDeviation:
    """Test compute_sigma_deviation method."""

    def test_sigma_deviation_excellent(self, registry):
        """Test sigma < 1.0 returns EXCELLENT status."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            uncertainty=10.0,
            status="ESTABLISHED"
        )

        result = registry.compute_sigma_deviation(105.0, "exp.param")

        assert result["predicted"] == 105.0
        assert result["experimental"] == 100.0
        assert result["uncertainty"] == 10.0
        assert result["sigma"] == 0.5
        assert result["status"] == "EXCELLENT"

    def test_sigma_deviation_good(self, registry):
        """Test 1.0 <= sigma < 2.0 returns GOOD status."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            uncertainty=10.0,
            status="ESTABLISHED"
        )

        result = registry.compute_sigma_deviation(115.0, "exp.param")

        assert result["sigma"] == 1.5
        assert result["status"] == "GOOD"

    def test_sigma_deviation_acceptable(self, registry):
        """Test 2.0 <= sigma < 3.0 returns ACCEPTABLE status."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            uncertainty=10.0,
            status="ESTABLISHED"
        )

        result = registry.compute_sigma_deviation(125.0, "exp.param")

        assert result["sigma"] == 2.5
        assert result["status"] == "ACCEPTABLE"

    def test_sigma_deviation_tension(self, registry):
        """Test sigma >= 3.0 returns TENSION status."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            uncertainty=10.0,
            status="ESTABLISHED"
        )

        result = registry.compute_sigma_deviation(135.0, "exp.param")

        assert result["sigma"] == 3.5
        assert result["status"] == "TENSION"

    def test_sigma_deviation_missing_data(self, registry):
        """Test handling of missing experimental data."""
        result = registry.compute_sigma_deviation(100.0, "nonexistent.param")

        assert result["predicted"] == 100.0
        assert result["experimental"] is None
        assert result["uncertainty"] is None
        assert result["sigma"] is None
        assert result["status"] == "MISSING_DATA"

    def test_sigma_deviation_no_uncertainty(self, registry):
        """Test handling of zero/None uncertainty."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            status="ESTABLISHED"
        )

        result = registry.compute_sigma_deviation(105.0, "exp.param")

        assert result["sigma"] is None
        assert result["status"] == "NO_UNCERTAINTY"

    def test_sigma_deviation_negative_difference(self, registry):
        """Test that sigma uses absolute deviation."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            uncertainty=10.0,
            status="ESTABLISHED"
        )

        result = registry.compute_sigma_deviation(85.0, "exp.param")

        assert result["sigma"] == 1.5  # abs(-15) / 10 = 1.5
        assert result["status"] == "GOOD"


# =============================================================================
# Test 6: Validate Prediction Method
# =============================================================================

class TestValidatePrediction:
    """Test validate_prediction method."""

    def test_validate_prediction_stores_in_metadata(self, registry):
        """Test that validation result is stored in parameter metadata."""
        # Set up experimental value
        registry.set_param(
            "exp.w0",
            -0.727,
            source="ESTABLISHED:DESI",
            uncertainty=0.067,
            status="ESTABLISHED"
        )

        # Set up prediction
        registry.set_param(
            "theory.w0",
            -0.720,
            source="cosmology_sim_v1",
            status="PREDICTED"
        )

        # Validate
        result = registry.validate_prediction("theory.w0", "exp.w0")

        # Check result returned
        assert result["status"] == "EXCELLENT"

        # Check stored in metadata
        entry = registry.get_entry("theory.w0")
        assert "validation" in entry.metadata
        assert entry.metadata["validation"]["status"] == "EXCELLENT"

    def test_validate_prediction_custom_metadata_key(self, registry):
        """Test using custom metadata key for validation."""
        registry.set_param(
            "exp.param",
            100.0,
            source="ESTABLISHED:TEST",
            uncertainty=5.0,
            status="ESTABLISHED"
        )

        registry.set_param(
            "theory.param",
            102.0,
            source="test_sim",
            status="PREDICTED"
        )

        result = registry.validate_prediction(
            "theory.param",
            "exp.param",
            metadata_key="accuracy_check"
        )

        entry = registry.get_entry("theory.param")
        assert "accuracy_check" in entry.metadata
        assert entry.metadata["accuracy_check"]["sigma"] == 0.4

    def test_validate_prediction_missing_prediction_raises(self, registry):
        """Test that validating non-existent prediction raises KeyError."""
        with pytest.raises(KeyError, match="Prediction 'nonexistent' not in registry"):
            registry.validate_prediction("nonexistent", "exp.param")


# =============================================================================
# Test 7: Accuracy Report
# =============================================================================

class TestAccuracyReport:
    """Test get_accuracy_report method."""

    def test_accuracy_report_categorizes_predictions(self, registry):
        """Test that accuracy report correctly categorizes predictions."""
        # Set up experimental values
        registry.set_param("exp.p1", 100.0, source="ESTABLISHED:TEST", uncertainty=10.0, status="ESTABLISHED")
        registry.set_param("exp.p2", 200.0, source="ESTABLISHED:TEST", uncertainty=10.0, status="ESTABLISHED")
        registry.set_param("exp.p3", 300.0, source="ESTABLISHED:TEST", uncertainty=10.0, status="ESTABLISHED")
        registry.set_param("exp.p4", 400.0, source="ESTABLISHED:TEST", uncertainty=10.0, status="ESTABLISHED")

        # Set up predictions with different sigma levels
        registry.set_param("pred.p1", 105.0, source="sim", status="PREDICTED")  # 0.5σ - EXCELLENT
        registry.set_param("pred.p2", 215.0, source="sim", status="PREDICTED")  # 1.5σ - GOOD
        registry.set_param("pred.p3", 325.0, source="sim", status="PREDICTED")  # 2.5σ - ACCEPTABLE
        registry.set_param("pred.p4", 440.0, source="sim", status="PREDICTED")  # 4.0σ - TENSION
        registry.set_param("pred.p5", 999.0, source="sim", status="PREDICTED")  # No validation

        # Validate predictions
        registry.validate_prediction("pred.p1", "exp.p1")
        registry.validate_prediction("pred.p2", "exp.p2")
        registry.validate_prediction("pred.p3", "exp.p3")
        registry.validate_prediction("pred.p4", "exp.p4")

        # Get report
        report = registry.get_accuracy_report()

        assert len(report["excellent"]) == 1
        assert len(report["good"]) == 1
        assert len(report["acceptable"]) == 1
        assert len(report["tension"]) == 1
        assert len(report["unvalidated"]) == 1

        assert report["summary"]["total_validated"] == 4
        assert report["summary"]["excellent_count"] == 1
        assert report["summary"]["tension_count"] == 1

    def test_accuracy_report_only_includes_derived_predicted(self, registry):
        """Test that report only includes DERIVED and PREDICTED parameters."""
        registry.set_param("exp.param", 100.0, source="ESTABLISHED:TEST", uncertainty=5.0, status="ESTABLISHED")
        registry.set_param("geom.param", 50.0, source="GEOMETRIC:TEST", status="GEOMETRIC")
        registry.set_param("pred.param", 102.0, source="sim", status="PREDICTED")

        registry.validate_prediction("pred.param", "exp.param")

        report = registry.get_accuracy_report()

        # Only pred.param should be in report
        assert report["summary"]["total_validated"] == 1
        assert "geom.param" not in report["unvalidated"]


# =============================================================================
# Test 8: Mismatch Detection and Logging
# =============================================================================

class TestMismatchDetection:
    """Test parameter mismatch warning and logging."""

    def test_mismatch_warning_on_significant_difference(self, registry):
        """Test that significant value changes trigger warnings."""
        registry.set_param("test.param", 100.0, source="sim_v1")

        with pytest.warns(UserWarning, match="Parameter mismatch"):
            registry.set_param("test.param", 110.0, source="sim_v2")

    def test_mismatch_logged(self, registry):
        """Test that mismatches are logged."""
        registry.set_param("test.param", 100.0, source="sim_v1")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            registry.set_param("test.param", 110.0, source="sim_v2")

        mismatches = registry.get_mismatches()
        assert len(mismatches) == 1
        assert mismatches[0]["path"] == "test.param"
        assert mismatches[0]["old_value"] == 100.0
        assert mismatches[0]["new_value"] == 110.0

    def test_no_warning_for_small_difference(self, registry):
        """Test that small differences (< 1%) don't trigger warnings."""
        registry.set_param("test.param", 100.0, source="sim_v1")

        # 0.5% difference - should not warn
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Turn warnings into errors
            try:
                registry.set_param("test.param", 100.5, source="sim_v2")
            except UserWarning:
                pytest.fail("Should not warn for < 1% difference")

    def test_mismatch_for_non_numeric_values(self, registry):
        """Test mismatch detection for non-numeric values."""
        registry.set_param("test.param", "value1", source="sim_v1")

        with pytest.warns(UserWarning):
            registry.set_param("test.param", "value2", source="sim_v2")


# =============================================================================
# Test 9: Export Methods
# =============================================================================

class TestExportMethods:
    """Test data export functionality."""

    def test_export_parameters(self, registry):
        """Test exporting all parameters."""
        registry.set_param(
            "test.param1",
            100.0,
            source="sim1",
            uncertainty=5.0,
            status="DERIVED"
        )
        registry.set_param(
            "test.param2",
            200.0,
            source="sim2",
            status="PREDICTED"
        )

        exported = registry.export_parameters()

        assert "test.param1" in exported
        assert "test.param2" in exported
        assert exported["test.param1"]["value"] == 100.0
        assert exported["test.param1"]["uncertainty"] == 5.0
        assert exported["test.param1"]["status"] == "DERIVED"

    def test_export_parameters_includes_timestamp(self, registry):
        """Test that exported parameters include timestamps."""
        registry.set_param("test.param", 42, source="test")

        exported = registry.export_parameters()

        assert "timestamp" in exported["test.param"]
        # Verify it's a valid ISO format timestamp
        datetime.fromisoformat(exported["test.param"]["timestamp"])

    def test_export_provenance(self, registry):
        """Test exporting provenance data."""
        registry.set_param("test.param", 1.0, source="sim_v1")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            registry.set_param("test.param", 1.1, source="sim_v2")

        provenance = registry.export_provenance()

        assert "test.param" in provenance
        assert provenance["test.param"] == ["sim_v1", "sim_v2"]


# =============================================================================
# Test 10: Integration with Experimental Data
# =============================================================================

class TestExperimentalDataIntegration:
    """Test integration scenarios with experimental data loaders."""

    def test_loading_desi_parameters(self, registry):
        """Test loading DESI-style parameters."""
        # Simulate what data_loader would do
        registry.set_param(
            "desi.w0",
            -0.727,
            source="ESTABLISHED:DESI_2025",
            uncertainty=0.067,
            status="ESTABLISHED",
            metadata={
                "units": "dimensionless",
                "description": "Dark energy equation of state",
                "source_file": "desi_2025_constraints.json"
            }
        )

        entry = registry.get_entry("desi.w0")
        assert entry.value == -0.727
        assert entry.status == "ESTABLISHED"
        assert entry.metadata["units"] == "dimensionless"

    def test_loading_nufit_parameters(self, registry):
        """Test loading NuFIT-style parameters."""
        registry.set_param(
            "nufit.theta_12",
            33.41,
            source="ESTABLISHED:NuFIT6.0",
            uncertainty=0.75,
            status="ESTABLISHED",
            metadata={
                "units": "degrees",
                "description": "Solar mixing angle",
                "ordering": "normal"
            }
        )

        entry = registry.get_entry("nufit.theta_12")
        assert entry.source == "ESTABLISHED:NuFIT6.0"
        assert entry.metadata["ordering"] == "normal"

    def test_loading_pdg_parameters(self, registry):
        """Test loading PDG-style parameters."""
        registry.set_param(
            "pdg.m_higgs",
            125.25,
            source="ESTABLISHED:PDG2024",
            uncertainty=0.17,
            status="ESTABLISHED",
            metadata={
                "units": "GeV",
                "description": "Higgs boson mass"
            }
        )

        entry = registry.get_entry("pdg.m_higgs")
        assert entry.value == 125.25
        assert entry.uncertainty == 0.17

    def test_prediction_validation_workflow(self, registry):
        """Test complete workflow: load experimental data, make prediction, validate."""
        # Step 1: Load experimental data (DESI w0)
        registry.set_param(
            "desi.w0",
            -0.727,
            source="ESTABLISHED:DESI_2025",
            uncertainty=0.067,
            status="ESTABLISHED"
        )

        # Step 2: Theory makes a prediction
        registry.set_param(
            "theory.w0_prediction",
            -0.725,
            source="cosmology_sim_v16_0",
            uncertainty=0.010,
            status="PREDICTED"
        )

        # Step 3: Validate prediction
        result = registry.validate_prediction("theory.w0_prediction", "desi.w0")

        # Step 4: Check results
        assert result["status"] == "EXCELLENT"
        assert result["sigma"] < 1.0

        # Step 5: Generate accuracy report
        report = registry.get_accuracy_report()
        assert len(report["excellent"]) == 1
        assert report["excellent"][0]["path"] == "theory.w0_prediction"


# =============================================================================
# Test 11: Edge Cases and Error Handling
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_registry_exports(self, registry):
        """Test exporting from empty registry."""
        params = registry.export_parameters()
        formulas = registry.export_formulas()
        sections = registry.export_sections()
        provenance = registry.export_provenance()

        assert params == {}
        assert formulas == {}
        assert sections == {}
        assert provenance == {}

    def test_parameter_path_with_dots(self, registry):
        """Test parameter paths with multiple dots."""
        registry.set_param("section.subsection.param.name", 42, source="test")
        value = registry.get_param("section.subsection.param.name")
        assert value == 42

    def test_zero_value_parameters(self, registry):
        """Test that zero values are handled correctly."""
        registry.set_param("test.zero", 0.0, source="test", uncertainty=0.1)

        value = registry.get_param("test.zero")
        assert value == 0.0

        # Test sigma computation with zero experimental value
        result = registry.compute_sigma_deviation(0.05, "test.zero")
        assert result["sigma"] == 0.5

    def test_negative_values(self, registry):
        """Test that negative values work correctly."""
        registry.set_param("test.negative", -100.0, source="test", uncertainty=5.0)

        # Test sigma computation
        result = registry.compute_sigma_deviation(-105.0, "test.negative")
        assert result["sigma"] == 1.0

    def test_very_large_values(self, registry):
        """Test handling of very large values."""
        registry.set_param("test.large", 1e50, source="test", uncertainty=1e48)
        value = registry.get_param("test.large")
        assert value == 1e50

    def test_very_small_values(self, registry):
        """Test handling of very small values."""
        registry.set_param("test.small", 1e-50, source="test", uncertainty=1e-52)
        value = registry.get_param("test.small")
        assert value == 1e-50

    def test_metadata_is_optional(self, registry):
        """Test that metadata parameter is optional."""
        registry.set_param("test.param", 42, source="test")
        entry = registry.get_entry("test.param")
        assert entry.metadata == {}

    def test_complex_metadata(self, registry):
        """Test storing complex metadata structures."""
        metadata = {
            "nested": {
                "value": 42,
                "list": [1, 2, 3]
            },
            "array": [{"a": 1}, {"b": 2}]
        }

        registry.set_param("test.param", 100, source="test", metadata=metadata)
        entry = registry.get_entry("test.param")
        assert entry.metadata["nested"]["value"] == 42
        assert entry.metadata["array"][0]["a"] == 1


# =============================================================================
# Parametrized Tests
# =============================================================================

class TestParametrizedScenarios:
    """Parametrized tests for various scenarios."""

    @pytest.mark.parametrize("pred,exp,unc,expected_status", [
        (100.0, 100.0, 10.0, "EXCELLENT"),  # Perfect match
        (105.0, 100.0, 10.0, "EXCELLENT"),  # 0.5σ
        (109.9, 100.0, 10.0, "EXCELLENT"),  # 0.99σ
        (110.0, 100.0, 10.0, "GOOD"),       # 1.0σ
        (115.0, 100.0, 10.0, "GOOD"),       # 1.5σ
        (119.9, 100.0, 10.0, "GOOD"),       # 1.99σ
        (120.0, 100.0, 10.0, "ACCEPTABLE"), # 2.0σ
        (125.0, 100.0, 10.0, "ACCEPTABLE"), # 2.5σ
        (129.9, 100.0, 10.0, "ACCEPTABLE"), # 2.99σ
        (130.0, 100.0, 10.0, "TENSION"),    # 3.0σ
        (150.0, 100.0, 10.0, "TENSION"),    # 5.0σ
    ])
    def test_sigma_status_boundaries(self, registry, pred, exp, unc, expected_status):
        """Test sigma status boundaries."""
        registry.set_param("exp.param", exp, source="ESTABLISHED:TEST", uncertainty=unc, status="ESTABLISHED")
        result = registry.compute_sigma_deviation(pred, "exp.param")
        assert result["status"] == expected_status

    @pytest.mark.parametrize("value,source,status", [
        (1.0, "sim1", "DERIVED"),
        (2.0, "ESTABLISHED:PDG", "ESTABLISHED"),
        (3.0, "geom", "GEOMETRIC"),
        (4.0, "pred", "PREDICTED"),
        (5.0, "calib", "CALIBRATED"),
    ])
    def test_different_status_types(self, registry, value, source, status):
        """Test setting parameters with different status types."""
        registry.set_param("test.param", value, source=source, status=status)
        entry = registry.get_entry("test.param")
        assert entry.status == status
        assert entry.value == value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
