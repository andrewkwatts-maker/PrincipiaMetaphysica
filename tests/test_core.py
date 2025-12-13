"""
Unit Tests for Core Module
==========================

Tests for the SOLID-compliant core architecture.

Run with: python -m pytest tests/test_core.py -v

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.constants import (
    DimensionalStructure,
    TopologyParameters,
    EnergyScales,
    GaugeParameters,
    NeutrinoConfig,
    DarkEnergyConfig,
    ProtonDecayConfig,
    get_dimensions,
    get_topology,
    get_energy_scales,
    get_gauge,
    get_neutrino,
    get_dark_energy,
    get_proton_decay,
)
from core.config_provider import ConfigProvider, get_config, reset_config
from core.simulation_base import SimulationBase, SimulationResult, SimulationRegistry
from core.validation import (
    PhysicsValidator,
    ExperimentalComparator,
    validate_n_gen,
    validate_chi_eff,
    validate_m_gut,
    validate_proton_lifetime,
)


class TestDimensionalStructure:
    """Tests for DimensionalStructure dataclass"""

    def test_default_values(self):
        """Test default dimensional values"""
        dims = DimensionalStructure()
        assert dims.D_BULK == 26
        assert dims.D_AFTER_SP2R == 13
        assert dims.D_INTERNAL == 7
        assert dims.D_EFFECTIVE == 6
        assert dims.D_OBSERVABLE == 4

    def test_signature_tuples(self):
        """Test spacetime signature tuples"""
        dims = DimensionalStructure()
        assert dims.SIGNATURE_BULK == (24, 2)
        assert dims.SIGNATURE_AFTER_SP2R == (12, 1)
        assert dims.SIGNATURE_EFFECTIVE == (5, 1)
        assert dims.SIGNATURE_OBSERVABLE == (3, 1)

    def test_pneuma_dimension_full(self):
        """Test Pneuma spinor dimension calculation"""
        dims = DimensionalStructure()
        # 2^(26/2) = 2^13 = 8192
        assert dims.pneuma_dimension_full() == 8192

    def test_pneuma_dimension_reduced(self):
        """Test reduced Pneuma dimension after gauging"""
        dims = DimensionalStructure()
        # 8192 / 2^6 / 2 = 8192 / 64 / 2 = 64
        assert dims.pneuma_dimension_reduced() == 64

    def test_immutability(self):
        """Test that dataclass is frozen (immutable)"""
        dims = DimensionalStructure()
        with pytest.raises(Exception):  # FrozenInstanceError
            dims.D_BULK = 27


class TestTopologyParameters:
    """Tests for TopologyParameters dataclass"""

    def test_betti_numbers(self):
        """Test Betti number values"""
        topo = TopologyParameters()
        assert topo.b2 == 4
        assert topo.b3 == 24

    def test_euler_characteristic(self):
        """Test chi_eff value"""
        topo = TopologyParameters()
        assert topo.chi_eff == 144

    def test_generation_count(self):
        """Test n_gen = chi_eff / 48"""
        topo = TopologyParameters()
        assert topo.n_gen == 3
        assert topo.chi_eff // 48 == 3

    def test_torsion_class(self):
        """Test T_omega value"""
        topo = TopologyParameters()
        assert abs(topo.T_OMEGA - (-0.884)) < 1e-10


class TestEnergyScales:
    """Tests for EnergyScales dataclass"""

    def test_planck_mass(self):
        """Test Planck mass values"""
        energy = EnergyScales()
        assert abs(energy.M_PLANCK_REDUCED - 2.435e18) < 1e15
        assert abs(energy.M_PLANCK_FULL - 1.221e19) < 1e16
        assert energy.M_PLANCK == energy.M_PLANCK_REDUCED

    def test_gut_scale(self):
        """Test GUT scale"""
        energy = EnergyScales()
        assert abs(energy.M_GUT - 2.118e16) < 1e14

    def test_electroweak_scale(self):
        """Test electroweak VEV"""
        energy = EnergyScales()
        assert abs(energy.V_EW - 173.97) < 1

    def test_higgs_mass(self):
        """Test Higgs mass"""
        energy = EnergyScales()
        assert abs(energy.M_HIGGS - 125.10) < 0.1


class TestGaugeParameters:
    """Tests for GaugeParameters dataclass"""

    def test_gut_coupling(self):
        """Test alpha_GUT values"""
        gauge = GaugeParameters()
        assert abs(gauge.ALPHA_GUT_INV - 23.54) < 0.1
        assert abs(gauge.ALPHA_GUT - 1/23.54) < 1e-4

    def test_so10_group_theory(self):
        """Test SO(10) group theory constants"""
        gauge = GaugeParameters()
        assert gauge.C_A_SO10_ADJOINT == 9
        assert gauge.DIM_ADJOINT == 45
        assert gauge.DIM_SPINOR == 16

    def test_xy_boson_charges(self):
        """Test X,Y gauge boson charges"""
        gauge = GaugeParameters()
        assert abs(gauge.CHARGE_X - 4/3) < 1e-10
        assert abs(gauge.CHARGE_Y - 1/3) < 1e-10


class TestNeutrinoConfig:
    """Tests for NeutrinoConfig dataclass"""

    def test_pmns_angles(self):
        """Test PMNS mixing angles"""
        nu = NeutrinoConfig()
        assert abs(nu.theta_23 - 45.0) < 0.1  # Maximal mixing
        assert abs(nu.theta_12 - 33.59) < 0.1
        assert abs(nu.theta_13 - 8.57) < 0.1

    def test_alpha_equality(self):
        """Test alpha_4 = alpha_5 (maximal mixing)"""
        nu = NeutrinoConfig()
        assert abs(nu.alpha_4 - nu.alpha_5) < 1e-10
        assert abs(nu.alpha_4 - 0.576152) < 1e-6

    def test_hierarchy(self):
        """Test hierarchy prediction"""
        nu = NeutrinoConfig()
        assert nu.HIERARCHY == "Normal"


class TestDarkEnergyConfig:
    """Tests for DarkEnergyConfig dataclass"""

    def test_equation_of_state(self):
        """Test w0 and wa values"""
        de = DarkEnergyConfig()
        assert abs(de.w0 - (-0.8528)) < 0.001
        assert abs(de.wa - (-0.75)) < 0.01

    def test_effective_dimension(self):
        """Test d_eff value"""
        de = DarkEnergyConfig()
        assert abs(de.d_eff - 12.576) < 0.001

    def test_w0_from_d_eff(self):
        """Test w0 calculation from d_eff"""
        w0 = DarkEnergyConfig.w0_from_d_eff(12.576)
        assert abs(w0 - (-0.8527)) < 0.001


class TestConfigProvider:
    """Tests for ConfigProvider"""

    def setup_method(self):
        """Reset singleton before each test"""
        reset_config()

    def test_singleton_pattern(self):
        """Test that get_config returns same instance"""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2

    def test_all_domains_accessible(self):
        """Test that all domain configs are accessible"""
        config = get_config()
        assert config.dimensions is not None
        assert config.topology is not None
        assert config.energy is not None
        assert config.gauge is not None
        assert config.neutrino is not None
        assert config.dark_energy is not None
        assert config.proton_decay is not None

    def test_convenience_properties(self):
        """Test convenience properties"""
        config = get_config()
        assert config.D_BULK == 26
        assert config.n_gen == 3
        assert config.chi_eff == 144
        assert abs(config.M_GUT - 2.118e16) < 1e14


class TestSimulationResult:
    """Tests for SimulationResult"""

    def test_basic_creation(self):
        """Test creating a simulation result"""
        result = SimulationResult(
            name="test_sim",
            version="1.0",
            data={"value": 42}
        )
        assert result.name == "test_sim"
        assert result.version == "1.0"
        assert result.data["value"] == 42
        assert result.status == "completed"

    def test_to_dict(self):
        """Test converting to dictionary"""
        result = SimulationResult(
            name="test_sim",
            version="1.0",
            data={"value": 42, "array": [1, 2, 3]}
        )
        d = result.to_dict()
        assert d["name"] == "test_sim"
        assert d["data"]["value"] == 42
        assert d["data"]["array"] == [1, 2, 3]


class TestSimulationRegistry:
    """Tests for SimulationRegistry"""

    def setup_method(self):
        """Clear registry before each test"""
        SimulationRegistry.clear()

    def test_register_simulation(self):
        """Test registering a simulation"""
        class TestSim(SimulationBase):
            name = "test_sim"
            version = "1.0"

            def run(self, verbose=True, **kwargs):
                return SimulationResult(name=self.name, version=self.version)

        SimulationRegistry.register(TestSim)
        assert "test_sim" in SimulationRegistry.list_all()

    def test_get_simulation(self):
        """Test retrieving a registered simulation"""
        class TestSim(SimulationBase):
            name = "test_sim"
            version = "1.0"

            def run(self, verbose=True, **kwargs):
                return SimulationResult(name=self.name, version=self.version)

        SimulationRegistry.register(TestSim)
        sim_class = SimulationRegistry.get("test_sim")
        assert sim_class is TestSim


class TestPhysicsValidator:
    """Tests for PhysicsValidator"""

    def test_validate_mass_positive(self):
        """Test mass validation with positive value"""
        result = PhysicsValidator.validate_mass(125.0, "m_h")
        assert result.valid is True

    def test_validate_mass_negative(self):
        """Test mass validation with negative value"""
        result = PhysicsValidator.validate_mass(-1.0, "m_h")
        assert result.valid is False

    def test_validate_angle_valid(self):
        """Test angle validation with valid value"""
        result = PhysicsValidator.validate_angle(45.0, "theta_23")
        assert result.valid is True

    def test_validate_angle_invalid(self):
        """Test angle validation with invalid value"""
        result = PhysicsValidator.validate_angle(400.0, "theta")
        assert result.valid is False

    def test_validate_probability_valid(self):
        """Test probability validation"""
        result = PhysicsValidator.validate_probability(0.76, "prob_NH")
        assert result.valid is True

    def test_validate_probability_invalid(self):
        """Test probability validation with invalid value"""
        result = PhysicsValidator.validate_probability(1.5, "prob")
        assert result.valid is False


class TestExperimentalComparator:
    """Tests for ExperimentalComparator"""

    def test_sigma_deviation_excellent(self):
        """Test sigma deviation for excellent agreement"""
        sigma, result = ExperimentalComparator.sigma_deviation(
            predicted=45.0,
            experimental=45.0,
            uncertainty=1.5
        )
        assert sigma < 0.1
        assert result.valid is True

    def test_sigma_deviation_poor(self):
        """Test sigma deviation for poor agreement"""
        sigma, result = ExperimentalComparator.sigma_deviation(
            predicted=50.0,
            experimental=45.0,
            uncertainty=1.0
        )
        assert sigma > 3
        assert result.valid is False

    def test_percent_error_excellent(self):
        """Test percent error for excellent match"""
        error, result = ExperimentalComparator.percent_error(
            predicted=125.10,
            experimental=125.10
        )
        assert error < 0.01
        assert result.valid is True


class TestValidationFunctions:
    """Tests for pre-defined validation functions"""

    def test_validate_n_gen_correct(self):
        """Test n_gen validation with correct value"""
        result = validate_n_gen(3)
        assert result.valid is True

    def test_validate_n_gen_incorrect(self):
        """Test n_gen validation with incorrect value"""
        result = validate_n_gen(4)
        assert result.valid is False

    def test_validate_chi_eff_correct(self):
        """Test chi_eff validation with correct value"""
        result = validate_chi_eff(144)
        assert result.valid is True

    def test_validate_m_gut_valid(self):
        """Test M_GUT validation within tolerance"""
        result = validate_m_gut(2.1e16)
        assert result.valid is True

    def test_validate_proton_lifetime_above_bound(self):
        """Test proton lifetime above Super-K bound"""
        result = validate_proton_lifetime(3.9e34)
        assert result.valid is True

    def test_validate_proton_lifetime_below_bound(self):
        """Test proton lifetime below Super-K bound"""
        result = validate_proton_lifetime(1.0e34)
        assert result.valid is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
