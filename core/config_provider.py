"""
Configuration Provider
======================

SOLID Principles Applied:
- Dependency Inversion: Provides abstraction layer for configuration access
- Single Responsibility: Only handles configuration aggregation

This module provides a unified interface for accessing all configuration
parameters, bridging the new SOLID architecture with the legacy config.py.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass
from typing import Optional

from .constants import (
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


@dataclass
class ConfigProvider:
    """
    Unified configuration provider.

    Dependency Inversion: Simulations depend on this abstraction,
    not directly on config modules.

    Aggregates all domain configurations into a single injectable object.

    Example Usage:
        config = get_config()
        m_gut = config.energy.M_GUT
        n_gen = config.topology.n_gen
        alpha_gut = config.gauge.ALPHA_GUT
    """

    dimensions: DimensionalStructure
    topology: TopologyParameters
    energy: EnergyScales
    gauge: GaugeParameters
    neutrino: NeutrinoConfig
    dark_energy: DarkEnergyConfig
    proton_decay: ProtonDecayConfig

    # Version info
    VERSION: str = "12.7"

    @classmethod
    def default(cls) -> 'ConfigProvider':
        """Create a ConfigProvider with default values"""
        return cls(
            dimensions=get_dimensions(),
            topology=get_topology(),
            energy=get_energy_scales(),
            gauge=get_gauge(),
            neutrino=get_neutrino(),
            dark_energy=get_dark_energy(),
            proton_decay=get_proton_decay(),
        )

    # Convenience properties for backward compatibility

    @property
    def D_BULK(self) -> int:
        return self.dimensions.D_BULK

    @property
    def D_AFTER_SP2R(self) -> int:
        return self.dimensions.D_AFTER_SP2R

    @property
    def D_INTERNAL(self) -> int:
        return self.dimensions.D_INTERNAL

    @property
    def D_EFFECTIVE(self) -> int:
        return self.dimensions.D_EFFECTIVE

    @property
    def n_gen(self) -> int:
        return self.topology.n_gen

    @property
    def chi_eff(self) -> int:
        return self.topology.chi_eff

    @property
    def b2(self) -> int:
        return self.topology.b2

    @property
    def b3(self) -> int:
        return self.topology.b3

    @property
    def T_omega(self) -> float:
        return self.topology.T_OMEGA

    @property
    def M_GUT(self) -> float:
        return self.energy.M_GUT

    @property
    def M_PLANCK(self) -> float:
        return self.energy.M_PLANCK

    @property
    def M_PLANCK_REDUCED(self) -> float:
        return self.energy.M_PLANCK_REDUCED

    @property
    def V_EW(self) -> float:
        return self.energy.V_EW

    @property
    def ALPHA_GUT(self) -> float:
        return self.gauge.ALPHA_GUT

    @property
    def ALPHA_GUT_INV(self) -> float:
        return self.gauge.ALPHA_GUT_INV

    @property
    def theta_23(self) -> float:
        return self.neutrino.theta_23

    @property
    def theta_12(self) -> float:
        return self.neutrino.theta_12

    @property
    def theta_13(self) -> float:
        return self.neutrino.theta_13

    @property
    def delta_cp(self) -> float:
        return self.neutrino.delta_cp

    @property
    def shadow_kuf(self) -> float:
        return self.neutrino.shadow_kuf

    @property
    def shadow_chet(self) -> float:
        return self.neutrino.shadow_chet

    @property
    def w0(self) -> float:
        return self.dark_energy.w0

    @property
    def wa(self) -> float:
        return self.dark_energy.wa


# Singleton instance
_config_instance: Optional[ConfigProvider] = None


def get_config() -> ConfigProvider:
    """
    Get the singleton ConfigProvider instance.

    Returns:
        ConfigProvider with all default configurations
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigProvider.default()
    return _config_instance


def reset_config():
    """Reset the singleton (for testing)"""
    global _config_instance
    _config_instance = None
