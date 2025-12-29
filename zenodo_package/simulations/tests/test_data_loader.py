"""
Comprehensive Unit Tests for ExperimentalDataLoader

Tests all aspects of the experimental data loading system:
- Loader instantiation and initialization
- Loading DESI 2025 constraints
- Loading NuFIT 6.0 parameters
- Loading PDG 2024 values
- Error handling for missing files
- Integration with PMRegistry
- Data validation and caching

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.experimental_data_loader import (
    ExperimentalDataLoader,
    ExperimentalValue,
    get_loader,
    get_desi_w0,
    get_desi_wa,
    get_nufit_theta12,
    get_pdg_higgs_mass
)
from base.registry import PMRegistry


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data files."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_desi_data():
    """Sample DESI data structure."""
    return {
        "metadata": {
            "source": "DESI Collaboration",
            "arxiv": "2411.12022",
            "retrieved": "2025-01-15"
        },
        "cosmological_parameters": {
            "w0": {
                "value": -0.727,
                "uncertainty_plus": 0.067,
                "uncertainty_minus": 0.067,
                "units": "dimensionless",
                "description": "Dark energy equation of state"
            },
            "wa": {
                "value": -0.99,
                "uncertainty_plus": 0.32,
                "uncertainty_minus": 0.32,
                "units": "dimensionless",
                "description": "Dark energy evolution parameter"
            },
            "H0": {
                "value": 68.52,
                "uncertainty": 0.62,
                "units": "km/s/Mpc",
                "description": "Hubble constant"
            }
        }
    }


@pytest.fixture
def sample_nufit_data():
    """Sample NuFIT data structure."""
    return {
        "metadata": {
            "source": "NuFIT Collaboration",
            "version": "6.0",
            "date": "2024-09"
        },
        "normal_ordering": {
            "theta_12": {
                "value": 33.41,
                "uncertainty_plus": 0.75,
                "uncertainty_minus": 0.75,
                "units": "degrees",
                "description": "Solar mixing angle"
            },
            "theta_23": {
                "value": 42.1,
                "uncertainty_plus": 1.5,
                "uncertainty_minus": 1.3,
                "units": "degrees",
                "description": "Atmospheric mixing angle"
            },
            "delta_CP": {
                "value": 230.0,
                "uncertainty_plus": 25.0,
                "uncertainty_minus": 25.0,
                "units": "degrees",
                "description": "CP violation phase"
            }
        },
        "inverted_ordering": {
            "theta_12": {
                "value": 33.41,
                "uncertainty_plus": 0.75,
                "uncertainty_minus": 0.75,
                "units": "degrees",
                "description": "Solar mixing angle"
            }
        },
        "mass_ordering_preference": {
            "preferred": "NO",
            "chi2_difference": 9.3,
            "sigma_preference": 3.0
        }
    }


@pytest.fixture
def sample_pdg_data():
    """Sample PDG data structure."""
    return {
        "metadata": {
            "source": "Particle Data Group",
            "year": 2024
        },
        "gauge_bosons": {
            "m_W": {
                "value": 80.377,
                "uncertainty": 0.012,
                "units": "GeV",
                "description": "W boson mass"
            },
            "m_Z": {
                "value": 91.1876,
                "uncertainty": 0.0021,
                "units": "GeV",
                "description": "Z boson mass"
            },
            "m_higgs": {
                "value": 125.25,
                "uncertainty": 0.17,
                "units": "GeV",
                "description": "Higgs boson mass"
            }
        },
        "leptons": {
            "m_electron": {
                "value": 0.51099895000e-3,
                "uncertainty": 0.00000000015e-3,
                "units": "GeV",
                "description": "Electron mass"
            },
            "m_muon": {
                "value": 0.1056583755,
                "uncertainty": 0.0000000023,
                "units": "GeV",
                "description": "Muon mass"
            }
        },
        "quarks": {
            "m_top": {
                "value": 172.57,
                "uncertainty": 0.29,
                "units": "GeV",
                "description": "Top quark mass"
            }
        }
    }


@pytest.fixture
def temp_loader(temp_data_dir, sample_desi_data, sample_nufit_data, sample_pdg_data):
    """Create a loader with temporary test data files."""
    # Create data files
    (temp_data_dir / "desi_2025_constraints.json").write_text(
        json.dumps(sample_desi_data, indent=2)
    )
    (temp_data_dir / "nufit_6_0_parameters.json").write_text(
        json.dumps(sample_nufit_data, indent=2)
    )
    (temp_data_dir / "pdg_2024_values.json").write_text(
        json.dumps(sample_pdg_data, indent=2)
    )

    return ExperimentalDataLoader(data_dir=temp_data_dir)


@pytest.fixture
def registry():
    """Provide a fresh PMRegistry instance."""
    PMRegistry.reset_instance()
    reg = PMRegistry.get_instance()
    yield reg
    PMRegistry.reset_instance()


# =============================================================================
# Test 1: Loader Instantiation
# =============================================================================

class TestLoaderInstantiation:
    """Test ExperimentalDataLoader instantiation and initialization."""

    def test_loader_creates_successfully(self, temp_loader):
        """Test that loader instantiates without errors."""
        assert isinstance(temp_loader, ExperimentalDataLoader)

    def test_loader_with_custom_data_dir(self, temp_data_dir, sample_desi_data):
        """Test loader with custom data directory."""
        # Create minimal data file
        (temp_data_dir / "desi_2025_constraints.json").write_text(
            json.dumps(sample_desi_data)
        )
        (temp_data_dir / "nufit_6_0_parameters.json").write_text("{}")
        (temp_data_dir / "pdg_2024_values.json").write_text("{}")

        loader = ExperimentalDataLoader(data_dir=temp_data_dir)
        assert loader.DATA_DIR == temp_data_dir

    def test_loader_warns_on_missing_files(self, temp_data_dir):
        """Test that loader warns when data files are missing."""
        # Create directory with no files
        with pytest.warns(UserWarning, match="Missing experimental data file"):
            ExperimentalDataLoader(data_dir=temp_data_dir)

    def test_default_data_dir_location(self):
        """Test that default data directory is correctly determined."""
        # Note: This will fail if actual data files don't exist, which is expected
        loader_class = ExperimentalDataLoader
        expected_dir = Path(__file__).parent.parent / "data" / "experimental"

        # The class variable should point to the right place
        assert "experimental" in str(loader_class.DATA_DIR)


# =============================================================================
# Test 2: Loading DESI 2025 Constraints
# =============================================================================

class TestDESILoading:
    """Test loading DESI 2025 cosmological constraints."""

    def test_get_desi_data(self, temp_loader, sample_desi_data):
        """Test getting full DESI data dictionary."""
        data = temp_loader.get_desi_data()
        assert data == sample_desi_data

    def test_get_desi_w0(self, temp_loader):
        """Test getting DESI w0 parameter."""
        w0 = temp_loader.get_desi("w0")

        assert isinstance(w0, ExperimentalValue)
        assert w0.value == -0.727
        assert w0.uncertainty == 0.067
        assert w0.units == "dimensionless"
        assert "DESI 2025" in w0.source

    def test_get_desi_wa(self, temp_loader):
        """Test getting DESI wa parameter."""
        wa = temp_loader.get_desi("wa")

        assert wa.value == -0.99
        assert wa.uncertainty == 0.32

    def test_get_desi_h0(self, temp_loader):
        """Test getting DESI H0 parameter."""
        h0 = temp_loader.get_desi("H0")

        assert h0.value == 68.52
        assert h0.uncertainty == 0.62
        assert h0.units == "km/s/Mpc"

    def test_get_desi_nonexistent_param_raises(self, temp_loader):
        """Test that getting non-existent DESI parameter raises KeyError."""
        with pytest.raises(KeyError, match="DESI parameter 'nonexistent' not found"):
            temp_loader.get_desi("nonexistent")

    def test_desi_data_caching(self, temp_loader):
        """Test that DESI data is cached after first load."""
        # First call loads from file
        data1 = temp_loader.get_desi_data()

        # Second call uses cache
        data2 = temp_loader.get_desi_data()

        # Should be the same object (cached)
        assert data1 is data2

    def test_desi_convenience_methods(self, temp_loader):
        """Test convenience methods for DESI parameters."""
        w0 = temp_loader.get_desi_w0()
        wa = temp_loader.get_desi_wa()

        assert w0.value == -0.727
        assert wa.value == -0.99

    def test_desi_asymmetric_uncertainties(self, temp_loader):
        """Test handling of asymmetric uncertainties (uses plus uncertainty)."""
        w0 = temp_loader.get_desi("w0")

        # Should use uncertainty_plus
        assert w0.uncertainty == 0.067

    def test_desi_symmetric_uncertainty_fallback(self, temp_loader):
        """Test fallback to 'uncertainty' field if plus/minus not available."""
        h0 = temp_loader.get_desi("H0")

        # This uses 'uncertainty' field directly
        assert h0.uncertainty == 0.62


# =============================================================================
# Test 3: Loading NuFIT 6.0 Parameters
# =============================================================================

class TestNuFITLoading:
    """Test loading NuFIT 6.0 neutrino parameters."""

    def test_get_nufit_data(self, temp_loader, sample_nufit_data):
        """Test getting full NuFIT data dictionary."""
        data = temp_loader.get_nufit_data()
        assert data == sample_nufit_data

    def test_get_nufit_theta12_normal_ordering(self, temp_loader):
        """Test getting theta_12 with normal ordering."""
        theta12 = temp_loader.get_nufit("theta_12", "normal_ordering")

        assert isinstance(theta12, ExperimentalValue)
        assert theta12.value == 33.41
        assert theta12.uncertainty == 0.75  # Average of plus and minus
        assert theta12.units == "degrees"
        assert "NuFIT 6.0" in theta12.source

    def test_get_nufit_theta23_normal_ordering(self, temp_loader):
        """Test getting theta_23 with normal ordering."""
        theta23 = temp_loader.get_nufit("theta_23", "normal_ordering")

        assert theta23.value == 42.1
        # Average of asymmetric uncertainties: (1.5 + 1.3) / 2 = 1.4
        assert theta23.uncertainty == 1.4

    def test_get_nufit_delta_cp(self, temp_loader):
        """Test getting delta_CP parameter."""
        delta_cp = temp_loader.get_nufit("delta_CP", "normal_ordering")

        assert delta_cp.value == 230.0
        assert delta_cp.uncertainty == 25.0

    def test_get_nufit_inverted_ordering(self, temp_loader):
        """Test getting parameters with inverted ordering."""
        theta12_inv = temp_loader.get_nufit("theta_12", "inverted_ordering")

        assert theta12_inv.value == 33.41

    def test_get_nufit_invalid_ordering_raises(self, temp_loader):
        """Test that invalid ordering raises KeyError."""
        with pytest.raises(KeyError, match="Ordering 'invalid_ordering' not found"):
            temp_loader.get_nufit("theta_12", "invalid_ordering")

    def test_get_nufit_nonexistent_param_raises(self, temp_loader):
        """Test that getting non-existent parameter raises KeyError."""
        with pytest.raises(KeyError, match="NuFIT parameter 'nonexistent' not found"):
            temp_loader.get_nufit("nonexistent", "normal_ordering")

    def test_get_mass_ordering_preference(self, temp_loader):
        """Test getting mass ordering preference."""
        mo = temp_loader.get_mass_ordering_preference()

        assert mo["preferred"] == "NO"
        assert mo["chi2_difference"] == 9.3
        assert mo["sigma_preference"] == 3.0

    def test_nufit_data_caching(self, temp_loader):
        """Test that NuFIT data is cached after first load."""
        data1 = temp_loader.get_nufit_data()
        data2 = temp_loader.get_nufit_data()

        assert data1 is data2


# =============================================================================
# Test 4: Loading PDG 2024 Values
# =============================================================================

class TestPDGLoading:
    """Test loading PDG 2024 particle physics values."""

    def test_get_pdg_data(self, temp_loader, sample_pdg_data):
        """Test getting full PDG data dictionary."""
        data = temp_loader.get_pdg_data()
        assert data == sample_pdg_data

    def test_get_pdg_higgs_mass(self, temp_loader):
        """Test getting Higgs mass from PDG."""
        m_h = temp_loader.get_pdg("gauge_bosons", "m_higgs")

        assert isinstance(m_h, ExperimentalValue)
        assert m_h.value == 125.25
        assert m_h.uncertainty == 0.17
        assert m_h.units == "GeV"
        assert m_h.source == "PDG 2024"

    def test_get_pdg_w_mass(self, temp_loader):
        """Test getting W boson mass."""
        m_w = temp_loader.get_pdg("gauge_bosons", "m_W")

        assert m_w.value == 80.377
        assert m_w.uncertainty == 0.012

    def test_get_pdg_electron_mass(self, temp_loader):
        """Test getting electron mass."""
        m_e = temp_loader.get_pdg("leptons", "m_electron")

        assert m_e.value == 0.51099895000e-3
        assert m_e.units == "GeV"

    def test_get_pdg_top_mass(self, temp_loader):
        """Test getting top quark mass."""
        m_t = temp_loader.get_pdg("quarks", "m_top")

        assert m_t.value == 172.57
        assert m_t.uncertainty == 0.29

    def test_get_pdg_invalid_category_raises(self, temp_loader):
        """Test that invalid category raises KeyError."""
        with pytest.raises(KeyError, match="PDG category 'invalid' not found"):
            temp_loader.get_pdg("invalid", "m_something")

    def test_get_pdg_invalid_param_raises(self, temp_loader):
        """Test that invalid parameter in valid category raises KeyError."""
        with pytest.raises(KeyError, match="PDG parameter 'nonexistent' not found"):
            temp_loader.get_pdg("gauge_bosons", "nonexistent")

    def test_get_pdg_mass_convenience_leptons(self, temp_loader):
        """Test get_pdg_mass convenience method for leptons."""
        m_e = temp_loader.get_pdg_mass("electron")
        m_mu = temp_loader.get_pdg_mass("muon")

        assert m_e.value == 0.51099895000e-3
        assert m_mu.value == 0.1056583755

    def test_get_pdg_mass_convenience_quarks(self, temp_loader):
        """Test get_pdg_mass convenience method for quarks."""
        m_t = temp_loader.get_pdg_mass("top")
        assert m_t.value == 172.57

    def test_get_pdg_mass_convenience_bosons(self, temp_loader):
        """Test get_pdg_mass convenience method for bosons."""
        m_h = temp_loader.get_pdg_mass("higgs")
        assert m_h.value == 125.25

    def test_get_pdg_mass_invalid_particle_raises(self, temp_loader):
        """Test that invalid particle name raises KeyError."""
        with pytest.raises(KeyError, match="Unknown particle 'invalid'"):
            temp_loader.get_pdg_mass("invalid")

    def test_pdg_data_caching(self, temp_loader):
        """Test that PDG data is cached after first load."""
        data1 = temp_loader.get_pdg_data()
        data2 = temp_loader.get_pdg_data()

        assert data1 is data2


# =============================================================================
# Test 5: Error Handling for Missing Files
# =============================================================================

class TestErrorHandling:
    """Test error handling for various failure modes."""

    def test_missing_desi_file_raises_on_access(self, temp_data_dir):
        """Test that accessing DESI data with missing file raises error."""
        # Create loader with missing DESI file
        (temp_data_dir / "nufit_6_0_parameters.json").write_text("{}")
        (temp_data_dir / "pdg_2024_values.json").write_text("{}")

        with pytest.warns(UserWarning):
            loader = ExperimentalDataLoader(data_dir=temp_data_dir)

        with pytest.raises(FileNotFoundError):
            loader.get_desi_data()

    def test_missing_nufit_file_raises_on_access(self, temp_data_dir):
        """Test that accessing NuFIT data with missing file raises error."""
        (temp_data_dir / "desi_2025_constraints.json").write_text("{}")
        (temp_data_dir / "pdg_2024_values.json").write_text("{}")

        with pytest.warns(UserWarning):
            loader = ExperimentalDataLoader(data_dir=temp_data_dir)

        with pytest.raises(FileNotFoundError):
            loader.get_nufit_data()

    def test_missing_pdg_file_raises_on_access(self, temp_data_dir):
        """Test that accessing PDG data with missing file raises error."""
        (temp_data_dir / "desi_2025_constraints.json").write_text("{}")
        (temp_data_dir / "nufit_6_0_parameters.json").write_text("{}")

        with pytest.warns(UserWarning):
            loader = ExperimentalDataLoader(data_dir=temp_data_dir)

        with pytest.raises(FileNotFoundError):
            loader.get_pdg_data()

    def test_malformed_json_raises_error(self, temp_data_dir):
        """Test that malformed JSON raises appropriate error."""
        (temp_data_dir / "desi_2025_constraints.json").write_text("not valid json {")
        (temp_data_dir / "nufit_6_0_parameters.json").write_text("{}")
        (temp_data_dir / "pdg_2024_values.json").write_text("{}")

        # Files exist, so no warning on instantiation
        loader = ExperimentalDataLoader(data_dir=temp_data_dir)

        # But loading malformed JSON should raise error
        with pytest.raises(json.JSONDecodeError):
            loader.get_desi_data()

    def test_empty_json_file_handled(self, temp_data_dir):
        """Test that empty JSON files are handled gracefully."""
        (temp_data_dir / "desi_2025_constraints.json").write_text("{}")
        (temp_data_dir / "nufit_6_0_parameters.json").write_text("{}")
        (temp_data_dir / "pdg_2024_values.json").write_text("{}")

        # Files exist, so no warning
        loader = ExperimentalDataLoader(data_dir=temp_data_dir)

        # Should load but return empty dict
        data = loader.get_desi_data()
        assert data == {}


# =============================================================================
# Test 6: Registry Integration
# =============================================================================

class TestRegistryIntegration:
    """Test integration with PMRegistry."""

    def test_load_desi_into_registry(self, temp_loader, registry):
        """Test loading DESI parameters into registry."""
        temp_loader._load_desi_into_registry(registry)

        # Check w0 was loaded
        assert registry.has_param("desi.w0")
        assert registry.get_param("desi.w0") == -0.727

        # Check metadata
        entry = registry.get_entry("desi.w0")
        assert entry.status == "ESTABLISHED"
        assert entry.source == "ESTABLISHED:DESI_2025"
        assert entry.uncertainty == 0.067

    def test_load_nufit_into_registry(self, temp_loader, registry):
        """Test loading NuFIT parameters into registry."""
        temp_loader._load_nufit_into_registry(registry)

        # Check theta_12 was loaded
        assert registry.has_param("nufit.theta_12")
        assert registry.get_param("nufit.theta_12") == 33.41

        # Check metadata
        entry = registry.get_entry("nufit.theta_12")
        assert entry.status == "ESTABLISHED"
        assert entry.source == "ESTABLISHED:NuFIT6.0"

    def test_load_pdg_into_registry(self, temp_loader, registry):
        """Test loading PDG parameters into registry."""
        temp_loader._load_pdg_into_registry(registry)

        # Check Higgs mass was loaded
        assert registry.has_param("pdg.m_higgs")
        assert registry.get_param("pdg.m_higgs") == 125.25

        # Check metadata
        entry = registry.get_entry("pdg.m_higgs")
        assert entry.status == "ESTABLISHED"
        assert entry.source == "ESTABLISHED:PDG2024"
        assert entry.uncertainty == 0.17

    def test_load_all_into_registry(self, temp_loader, registry):
        """Test loading all experimental data into registry."""
        temp_loader.load_all_into_registry(registry)

        # Check parameters from all sources
        assert registry.has_param("desi.w0")
        assert registry.has_param("nufit.theta_12")
        assert registry.has_param("pdg.m_higgs")

        # All should be ESTABLISHED
        assert registry.get_entry("desi.w0").status == "ESTABLISHED"
        assert registry.get_entry("nufit.theta_12").status == "ESTABLISHED"
        assert registry.get_entry("pdg.m_higgs").status == "ESTABLISHED"

    def test_registry_integration_with_mass_ordering(self, temp_loader, registry):
        """Test that mass ordering preference is loaded into registry."""
        temp_loader._load_nufit_into_registry(registry)

        assert registry.has_param("nufit.mass_ordering_chi2_diff")
        entry = registry.get_entry("nufit.mass_ordering_chi2_diff")
        assert entry.value == 9.3
        assert entry.metadata["preferred"] == "NO"
        assert entry.metadata["sigma"] == 3.0

    def test_registry_cannot_override_established_params(self, temp_loader, registry):
        """Test that established params from loader cannot be overridden."""
        temp_loader.load_all_into_registry(registry)

        # Try to override with non-ESTABLISHED source
        with pytest.raises(ValueError, match="Cannot override ESTABLISHED param"):
            registry.set_param(
                "desi.w0",
                -0.8,
                source="simulation_v1",
                status="DERIVED"
            )


# =============================================================================
# Test 7: Singleton Pattern for get_loader
# =============================================================================

class TestGetLoaderSingleton:
    """Test the get_loader() singleton function."""

    def test_get_loader_returns_singleton(self):
        """Test that get_loader() returns singleton instance."""
        # Reset the global singleton
        import data.experimental_data_loader as loader_module
        loader_module._loader = None

        loader1 = get_loader()
        loader2 = get_loader()

        assert loader1 is loader2

    def test_get_loader_uses_default_data_dir(self):
        """Test that get_loader() uses default data directory."""
        import data.experimental_data_loader as loader_module
        loader_module._loader = None

        loader = get_loader()
        assert "experimental" in str(loader.DATA_DIR)


# =============================================================================
# Test 8: Convenience Functions
# =============================================================================

class TestConvenienceFunctions:
    """Test top-level convenience functions."""

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "data" / "experimental" / "desi_2025_constraints.json").exists(),
        reason="Requires actual data files"
    )
    def test_get_desi_w0_function(self):
        """Test get_desi_w0() convenience function."""
        w0 = get_desi_w0()
        assert isinstance(w0, ExperimentalValue)
        assert w0.value == -0.727

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "data" / "experimental" / "desi_2025_constraints.json").exists(),
        reason="Requires actual data files"
    )
    def test_get_desi_wa_function(self):
        """Test get_desi_wa() convenience function."""
        wa = get_desi_wa()
        assert isinstance(wa, ExperimentalValue)

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "data" / "experimental" / "nufit_6_0_parameters.json").exists(),
        reason="Requires actual data files"
    )
    def test_get_nufit_theta12_function(self):
        """Test get_nufit_theta12() convenience function."""
        theta12 = get_nufit_theta12()
        assert isinstance(theta12, ExperimentalValue)

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "data" / "experimental" / "pdg_2024_values.json").exists(),
        reason="Requires actual data files"
    )
    def test_get_pdg_higgs_mass_function(self):
        """Test get_pdg_higgs_mass() convenience function."""
        m_h = get_pdg_higgs_mass()
        assert isinstance(m_h, ExperimentalValue)


# =============================================================================
# Test 9: ExperimentalValue Dataclass
# =============================================================================

class TestExperimentalValue:
    """Test ExperimentalValue dataclass."""

    def test_experimental_value_creation(self):
        """Test creating ExperimentalValue."""
        val = ExperimentalValue(
            value=125.25,
            uncertainty=0.17,
            units="GeV",
            source="PDG 2024",
            description="Higgs mass"
        )

        assert val.value == 125.25
        assert val.uncertainty == 0.17
        assert val.units == "GeV"
        assert val.source == "PDG 2024"
        assert val.description == "Higgs mass"

    def test_experimental_value_default_description(self):
        """Test that description defaults to empty string."""
        val = ExperimentalValue(
            value=1.0,
            uncertainty=0.1,
            units="",
            source="test"
        )

        assert val.description == ""


# =============================================================================
# Test 10: Integration Tests
# =============================================================================

class TestIntegrationScenarios:
    """Integration tests for complete workflows."""

    def test_complete_workflow_desi(self, temp_loader, registry):
        """Test complete workflow: load DESI data and validate prediction."""
        # Load experimental data
        temp_loader.load_all_into_registry(registry)

        # Make a prediction
        registry.set_param(
            "theory.w0",
            -0.725,
            source="cosmology_sim_v1",
            status="PREDICTED"
        )

        # Validate
        result = registry.validate_prediction("theory.w0", "desi.w0")

        assert result["status"] == "EXCELLENT"
        assert result["experimental"] == -0.727
        assert result["predicted"] == -0.725

    def test_complete_workflow_nufit(self, temp_loader, registry):
        """Test complete workflow with NuFIT data."""
        temp_loader.load_all_into_registry(registry)

        # Make prediction for mixing angle
        registry.set_param(
            "theory.theta_12",
            33.5,
            source="neutrino_sim_v1",
            status="PREDICTED"
        )

        # Validate
        result = registry.validate_prediction("theory.theta_12", "nufit.theta_12")

        assert result["experimental"] == 33.41
        assert result["predicted"] == 33.5

    def test_complete_workflow_pdg(self, temp_loader, registry):
        """Test complete workflow with PDG data."""
        temp_loader.load_all_into_registry(registry)

        # Make prediction for Higgs mass
        registry.set_param(
            "theory.m_higgs",
            125.3,
            source="higgs_sim_v1",
            status="PREDICTED"
        )

        # Validate
        result = registry.validate_prediction("theory.m_higgs", "pdg.m_higgs")

        assert result["experimental"] == 125.25
        assert result["uncertainty"] == 0.17

    def test_accuracy_report_with_real_data(self, temp_loader, registry):
        """Test generating accuracy report with loaded experimental data."""
        # Load all experimental data
        temp_loader.load_all_into_registry(registry)

        # Make several predictions
        registry.set_param("pred.w0", -0.725, source="sim", status="PREDICTED")
        registry.set_param("pred.theta_12", 33.5, source="sim", status="PREDICTED")
        registry.set_param("pred.m_higgs", 125.3, source="sim", status="PREDICTED")

        # Validate all
        registry.validate_prediction("pred.w0", "desi.w0")
        registry.validate_prediction("pred.theta_12", "nufit.theta_12")
        registry.validate_prediction("pred.m_higgs", "pdg.m_higgs")

        # Get report
        report = registry.get_accuracy_report()

        assert report["summary"]["total_validated"] == 3
        assert all(cat in report for cat in ["excellent", "good", "acceptable", "tension"])


# =============================================================================
# Parametrized Tests
# =============================================================================

class TestParametrizedDataAccess:
    """Parametrized tests for data access patterns."""

    @pytest.mark.parametrize("param_name,expected_value", [
        ("w0", -0.727),
        ("wa", -0.99),
        ("H0", 68.52),
    ])
    def test_desi_parameter_access(self, temp_loader, param_name, expected_value):
        """Test accessing various DESI parameters."""
        val = temp_loader.get_desi(param_name)
        assert val.value == expected_value

    @pytest.mark.parametrize("param_name,ordering", [
        ("theta_12", "normal_ordering"),
        ("theta_23", "normal_ordering"),
        ("delta_CP", "normal_ordering"),
        ("theta_12", "inverted_ordering"),
    ])
    def test_nufit_parameter_access(self, temp_loader, param_name, ordering):
        """Test accessing various NuFIT parameters."""
        val = temp_loader.get_nufit(param_name, ordering)
        assert isinstance(val, ExperimentalValue)
        assert val.value > 0

    @pytest.mark.parametrize("category,param_name", [
        ("gauge_bosons", "m_W"),
        ("gauge_bosons", "m_Z"),
        ("gauge_bosons", "m_higgs"),
        ("leptons", "m_electron"),
        ("leptons", "m_muon"),
        ("quarks", "m_top"),
    ])
    def test_pdg_parameter_access(self, temp_loader, category, param_name):
        """Test accessing various PDG parameters."""
        val = temp_loader.get_pdg(category, param_name)
        assert isinstance(val, ExperimentalValue)
        assert val.value > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
