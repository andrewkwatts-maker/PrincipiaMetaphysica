"""
Legacy Bridge Module
====================

Provides backward compatibility with the existing config.py structure.

This module allows gradual migration from the monolithic config.py
to the new SOLID-compliant architecture.

Existing code can continue to use:
    from config import FundamentalConstants, PhenomenologyParameters, ...

While new code uses:
    from core import get_config

Both will return consistent values.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from typing import Dict, Any
import numpy as np

from .constants import (
    get_dimensions,
    get_topology,
    get_energy_scales,
    get_gauge,
    get_neutrino,
    get_dark_energy,
    get_proton_decay,
)


class FundamentalConstantsProxy:
    """
    Proxy class that maps legacy FundamentalConstants access
    to the new DimensionalStructure and TopologyParameters.
    """

    def __init__(self):
        self._dim = get_dimensions()
        self._topo = get_topology()

    @property
    def D_BULK(self) -> int:
        return self._dim.D_BULK

    @property
    def D_AFTER_SP2R(self) -> int:
        return self._dim.D_AFTER_SP2R

    @property
    def D_INTERNAL(self) -> int:
        return self._dim.D_INTERNAL

    @property
    def D_EFFECTIVE(self) -> int:
        return self._dim.D_EFFECTIVE

    @property
    def D_COMMON(self) -> int:
        return self._dim.D_OBSERVABLE

    @property
    def D_SHARED_EXTRAS(self) -> int:
        return 2

    @property
    def D_OBSERVABLE_BRANE(self) -> int:
        return self._dim.D_OBSERVABLE_BRANE

    @property
    def D_SHADOW_BRANE(self) -> int:
        return self._dim.D_SHADOW_BRANE

    @property
    def N_BRANES(self) -> int:
        return self._dim.N_BRANES

    @property
    def N_SHADOW_BRANES(self) -> int:
        return self._dim.N_SHADOW_BRANES

    @property
    def SIGNATURE_INITIAL(self):
        return self._dim.SIGNATURE_BULK

    @property
    def SIGNATURE_BULK(self):
        return self._dim.SIGNATURE_AFTER_SP2R

    @property
    def SIGNATURE_EFFECTIVE(self):
        return self._dim.SIGNATURE_EFFECTIVE

    @property
    def INTERNAL_MANIFOLD(self) -> str:
        return self._dim.INTERNAL_MANIFOLD

    @property
    def D_OBSERVED(self) -> int:
        return self._dim.D_OBSERVABLE

    @property
    def SPATIAL_DIMS(self) -> int:
        return 3

    @property
    def TIME_DIMS(self) -> int:
        return 1

    @property
    def HODGE_H11(self) -> int:
        return self._topo.h11

    @property
    def HODGE_H21(self) -> int:
        return self._topo.h21

    @property
    def HODGE_H31(self) -> int:
        return self._topo.h31

    @property
    def FLUX_REDUCTION(self) -> int:
        return self._topo.FLUX_REDUCTION

    @property
    def GAUGING_DOFS(self) -> int:
        return self._dim.GAUGING_DOFS

    @property
    def MIRRORING_FACTOR(self) -> int:
        return self._dim.MIRRORING_FACTOR

    @property
    def SM_GLUONS(self) -> int:
        return 8

    @property
    def SM_WEAK(self) -> int:
        return 3

    @property
    def SM_PHOTON(self) -> int:
        return 1

    @property
    def SM_BOSONS(self) -> int:
        return 12

    @staticmethod
    def euler_characteristic():
        topo = get_topology()
        chi_base = 2 * (1 - topo.h11 + topo.h21 - topo.h31)
        return 2 * chi_base

    @staticmethod
    def euler_characteristic_effective():
        return get_topology().chi_eff

    @staticmethod
    def fermion_generations():
        return get_topology().n_gen

    @staticmethod
    def pneuma_dimension_full():
        return get_dimensions().pneuma_dimension_full()

    @staticmethod
    def pneuma_dimension_reduced():
        return get_dimensions().pneuma_dimension_reduced()


class PhenomenologyParametersProxy:
    """
    Proxy class for PhenomenologyParameters.
    """

    def __init__(self):
        self._energy = get_energy_scales()
        self._de = get_dark_energy()
        self._proton = get_proton_decay()

    @property
    def M_PLANCK_REDUCED(self) -> float:
        return self._energy.M_PLANCK_REDUCED

    @property
    def M_PLANCK_FULL(self) -> float:
        return self._energy.M_PLANCK_FULL

    @property
    def M_PLANCK(self) -> float:
        return self._energy.M_PLANCK_REDUCED

    @property
    def M_STAR(self) -> float:
        return self._energy.M_STAR

    @property
    def TAU_PROTON(self) -> float:
        return self._proton.tau_p_median

    @property
    def TAU_PROTON_LOWER_68(self) -> float:
        return self._proton.tau_p_lower_68

    @property
    def TAU_PROTON_UPPER_68(self) -> float:
        return self._proton.tau_p_upper_68

    @property
    def TAU_PROTON_UNCERTAINTY_OOM(self) -> float:
        return self._proton.tau_p_uncertainty_oom

    @property
    def TAU_PROTON_SUPER_K_BOUND(self) -> float:
        return self._proton.SUPER_K_BOUND

    @property
    def W0_DESI_DR2(self) -> float:
        return self._de.w0_DESI

    @property
    def W0_DESI_ERROR(self) -> float:
        return self._de.w0_DESI_error

    @property
    def WA_EVOLUTION(self) -> float:
        return self._de.wa_DESI

    @property
    def WA_ERROR(self) -> float:
        return self._de.wa_DESI_error

    @property
    def OMEGA_LAMBDA(self) -> float:
        return self._de.OMEGA_LAMBDA

    @property
    def OMEGA_MATTER(self) -> float:
        return self._de.OMEGA_MATTER

    @property
    def OMEGA_BARYON(self) -> float:
        return self._de.OMEGA_BARYON

    @property
    def H0(self) -> float:
        return self._de.H0

    @property
    def ALPHA_EM(self) -> float:
        return 1 / 137.035999084

    @staticmethod
    def w0_value():
        return get_dark_energy().w0


class GaugeUnificationParametersProxy:
    """
    Proxy class for GaugeUnificationParameters.
    """

    def __init__(self):
        self._energy = get_energy_scales()
        self._gauge = get_gauge()

    @property
    def M_GUT(self) -> float:
        return self._energy.M_GUT

    @property
    def M_GUT_ERROR(self) -> float:
        return self._energy.M_GUT_ERROR

    @property
    def ALPHA_GUT(self) -> float:
        return self._gauge.ALPHA_GUT

    @property
    def ALPHA_GUT_INV(self) -> float:
        return self._gauge.ALPHA_GUT_INV

    @property
    def C_A_SO10_ADJOINT(self) -> int:
        return self._gauge.C_A_SO10_ADJOINT

    @property
    def DIM_ADJOINT(self) -> int:
        return self._gauge.DIM_ADJOINT

    @property
    def DIM_SPINOR(self) -> int:
        return self._gauge.DIM_SPINOR

    @property
    def BETA_PREFACTOR(self) -> float:
        return self._gauge.BETA_PREFACTOR

    @property
    def M_RH_NEUTRINO_SCALE(self) -> float:
        return self._energy.M_RH_NEUTRINO


class NeutrinoParametersProxy:
    """
    Proxy class for NeutrinoParameters.
    """

    def __init__(self):
        self._nu = get_neutrino()

    @property
    def THETA_23(self) -> float:
        return self._nu.theta_23

    @property
    def THETA_23_ERROR(self) -> float:
        return self._nu.theta_23_error

    @property
    def THETA_23_NUFIT(self) -> float:
        return self._nu.theta_23_nufit

    @property
    def THETA_12(self) -> float:
        return self._nu.theta_12

    @property
    def THETA_12_ERROR(self) -> float:
        return self._nu.theta_12_error

    @property
    def THETA_12_NUFIT(self) -> float:
        return self._nu.theta_12_nufit

    @property
    def THETA_13(self) -> float:
        return self._nu.theta_13

    @property
    def THETA_13_ERROR(self) -> float:
        return self._nu.theta_13_error

    @property
    def THETA_13_NUFIT(self) -> float:
        return self._nu.theta_13_nufit

    @property
    def DELTA_CP(self) -> float:
        return self._nu.delta_cp

    @property
    def DELTA_CP_ERROR(self) -> float:
        return self._nu.delta_cp_error

    @property
    def DELTA_CP_NUFIT(self) -> float:
        return self._nu.delta_cp_nufit

    @property
    def DELTA_M_SQUARED_21(self) -> float:
        return self._nu.DELTA_M21_SQ

    @property
    def DELTA_M_SQUARED_31(self) -> float:
        return self._nu.DELTA_M31_SQ

    @property
    def HIERARCHY_PREDICTION(self) -> str:
        return self._nu.HIERARCHY

    @property
    def M_RH_NEUTRINO(self) -> float:
        return get_energy_scales().M_RH_NEUTRINO


class FittedParametersProxy:
    """
    Proxy class for FittedParameters.
    """

    def __init__(self):
        self._nu = get_neutrino()

    @property
    def SHADOW_KUF(self) -> float:
        return self._nu.shadow_kuf

    @property
    def SHADOW_CHET(self) -> float:
        return self._nu.shadow_chet


class TorsionClassProxy:
    """
    Proxy class for TorsionClass.
    """

    def __init__(self):
        self._topo = get_topology()

    @property
    def T_OMEGA(self) -> float:
        return self._topo.T_OMEGA

    @staticmethod
    def derive_M_GUT():
        """Legacy method - returns M_GUT from energy scales"""
        return get_energy_scales().M_GUT


# Create singleton proxies for backward compatibility
FundamentalConstants = FundamentalConstantsProxy()
PhenomenologyParameters = PhenomenologyParametersProxy()
GaugeUnificationParameters = GaugeUnificationParametersProxy()
NeutrinoParameters = NeutrinoParametersProxy()
FittedParameters = FittedParametersProxy()
TorsionClass = TorsionClassProxy()


def get_legacy_config() -> Dict[str, Any]:
    """
    Get all configuration as a flat dictionary for legacy code.
    """
    return {
        'VERSION': '12.7',
        'D_BULK': FundamentalConstants.D_BULK,
        'D_AFTER_SP2R': FundamentalConstants.D_AFTER_SP2R,
        'D_INTERNAL': FundamentalConstants.D_INTERNAL,
        'D_EFFECTIVE': FundamentalConstants.D_EFFECTIVE,
        'chi_eff': get_topology().chi_eff,
        'n_gen': get_topology().n_gen,
        'b2': get_topology().b2,
        'b3': get_topology().b3,
        'T_omega': get_topology().T_OMEGA,
        'M_GUT': get_energy_scales().M_GUT,
        'M_PLANCK_REDUCED': get_energy_scales().M_PLANCK_REDUCED,
        'ALPHA_GUT_INV': get_gauge().ALPHA_GUT_INV,
        'theta_23': get_neutrino().theta_23,
        'theta_12': get_neutrino().theta_12,
        'theta_13': get_neutrino().theta_13,
        'delta_cp': get_neutrino().delta_cp,
        'shadow_kuf': get_neutrino().shadow_kuf,
        'shadow_chet': get_neutrino().shadow_chet,
        'w0': get_dark_energy().w0,
        'wa': get_dark_energy().wa,
        'tau_p_median': get_proton_decay().tau_p_median,
    }
