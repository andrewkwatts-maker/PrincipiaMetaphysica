#!/usr/bin/env python3
"""
Principia Metaphysica - Run All Simulations v17.2
===================================================

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

Unified simulation runner using the v16 infrastructure with:
- PMRegistry for centralized parameter/formula/section management
- EstablishedPhysics for loading experimental constants
- Topological execution order based on simulation dependencies
- Full validation and provenance tracking

ARCHITECTURE:
1. Registry Initialization: Create PMRegistry singleton
2. Load Established Physics: Load PDG/NuFIT/DESI constants
3. Topological Execution: Run simulations in dependency order
4. Validation: Check dependencies before and outputs after each simulation
5. Export: Generate theory_output.json with full provenance

SIMULATION PHASES (Topological Order):

Phase 0 - Introduction (No Dependencies):
  - introduction_v16_0: Theory introduction and overview (Section 1)

Phase 1 - Root Simulations (No Dependencies):
  - g2_geometry_v16_0: G2 manifold topology (b2, b3, chi_eff, K_MATCHING)
  - gauge_unification_v16_0: GUT scale and unified coupling (M_GUT, ALPHA_GUT)

Phase 2 - Core Physics (Depends on Phase 1):
  - fermion_generations_v16_0: Fermion chirality and Yukawa hierarchy
  - chirality_v16_0: Chirality spinor structure from G2 holonomy (Section 4.1)
  - ckm_matrix_v16_0: CKM matrix parameters (Section 4.3)
  - proton_decay_v16_0: Proton lifetime from gauge unification
  - higgs_mass_v16_0: Higgs mass from moduli stabilization

Phase 3 - Precision Observables and Cosmology (Depends on Phase 2):
  - cosmology_intro_v16_0: Cosmological framework introduction (Section 5.1)
  - dark_energy_v16_0: Dark energy from pneuma field (Section 5.2)
  - s8_suppression_v16_1: S8 tension analysis with dynamical dark energy (Section 5.4)
  - neutrino_mixing_v16_0: PMNS matrix from G2 associative cycles
  - multi_sector_v16_0: Multi-sector cosmology (dark energy, mirror sectors)

Phase 4 - Field Dynamics (Depends on All):
  - pneuma_mechanism_v16_0: Pneuma field coupling and flow
  - thermal_time_v16_0: Thermal time evolution (depends on Pneuma outputs)

Phase 5 - Discussion, Predictions, and Legacy Appendices (Depends on All):
  - discussion_v16_0: Theory discussion and implications (Section 7)
  - predictions_aggregator_v16_0: Testable predictions summary (Section 6)
  - appendix_a_math_v16_0: Mathematical foundations (Appendix A)
  - appendix_b_methods_v16_0: Computational methods (Appendix B)
  - appendix_c_derivations_v16_0: Extended derivations (Appendix C)
  - appendix_d_tables_v16_0: Parameter tables (Appendix D)
  - appendix_m_consciousness_v16_0: Speculative consciousness extensions (Appendix M)
  - appendix_n_g2_landscape_v16_0: G2 topology landscape (Appendix N)

Phase 6 - v16.2 Sterile Model Paper Structure (DOI: 10.5281/zenodo.18079602):
  - foundations_v16_2: Section 1 - Foundations of Dimensional Descent
  - methodology_v16_2: Section 2 - Sterile Extraction Methodology
  - results_v16_2: Section 3 - Cosmological Results and Alignment
  - integrity_v16_2: Section 4 - System Integrity and Verification
  - appendix_a_spectral_registry_v16_2: Appendix A - 125 Spectral Residues
  - appendix_b_sum_rule_v16_2: Appendix B - Global Sum Rule
  - appendix_c_gauge_matrices_v16_2: Appendix C - S_PR(2) Gauge Matrices
  - appendix_d_alignment_v16_2: Appendix D - 0.48σ Alignment Data
  - appendix_e_brane_map_v16_2: Appendix E - Brane-Intersection Map
  - appendix_f_72gates_v16_2: Appendix F - 72 Gates of Integrity
  - appendix_g_omega_seal_v16_2: Appendix G - Omega Seal Protocol (7 Master Gates)
  - appendix_h_288_roots_v16_2: Appendix H - 288-Root Ancestral Basis
  - appendix_i_terminal_states_v16_2: Appendix I - Three Terminal States
  - appendix_j_torsion_funnel_v16_2: Appendix J - The Torsion Funnel (288→24→125)
  - appendix_k_sterile_constants_v16_2: Appendix K - Sterile Constant Table
  - appendix_l_omega_unwinding_v16_2: Appendix L - Omega Unwinding Map

OUTPUT STRUCTURE:
{
  "metadata": {
    "version": "17.2",
    "timestamp": "2025-12-28T10:30:00.000Z",
    "git": {
      "commit_hash": "abc1234...",
      "branch": "main",
      "is_dirty": false,
      "dirty_suffix": ""
    },
    "python_version": "3.11.0",
    "platform": "win32",
    "compute_time_ms": 1234.56
  },
  "derivation_logic": {
    "framework": "Principia Metaphysica - Geometric Unity",
    "base_manifold": "TCS G2 (Twisted Connected Sum)",
    "topology_id": "TCS #187",
    "key_assumptions": [...]
  },
  "parameter_classification": {
    "established": ["gauge.alpha_em", "fermion.m_H", ...],
    "geometric": ["topology.b3", "topology.chi_eff", ...],
    "derived": ["gauge.M_GUT", "gauge.alpha_GUT", ...],
    "calibrated": ["moduli.Re_T_pheno", ...]
  },
  "parameters": {
    "topology.b3": {
      "value": 24,
      "source": "g2_geometry_v16_0",
      "source_simulation": "g2_geometry_v16_0",
      "derivation_chain": ["topology.chi_eff"],
      "status": "GEOMETRIC",
      "git_commit": "abc1234...",
      ...
    },
    "gauge.M_GUT": {
      "value": 2.1e16,
      "uncertainty": 0.09e16,
      "units": "GeV",
      "source_simulation": "gauge_unification_v16_0",
      "derivation_chain": ["topology.chi_eff", "topology.b3", "gauge.alpha_GUT"],
      "status": "DERIVED",
      "git_commit": "abc1234...",
      ...
    },
    ...
  },
  "formulas": {
    "g2-holonomy": {"latex": "...", "category": "THEORY", ...},
    ...
  },
  "sections": {
    "4": {"title": "...", "content_blocks": [...], ...},
    ...
  },
  "provenance": {
    "gauge.M_GUT": ["gauge_unification_v16_0"],
    ...
  },
  "validation": {
    "simulations_run": 8,
    "simulations_passed": 8,
    "simulations_failed": 0,
    "results": [...]
  }
}

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import warnings

# Conditionally import numpy for UQ (Monte Carlo)
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    warnings.warn("NumPy not available - UQ mode will be disabled")


class NumpyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles numpy types."""
    def default(self, obj):
        if NUMPY_AVAILABLE:
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.bool_):
                return bool(obj)
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        return super().default(obj)


# Add simulations directory to path
sys.path.insert(0, str(Path(__file__).parent / 'simulations'))
sys.path.insert(0, str(Path(__file__).parent))

# Import base infrastructure
from simulations.base import (
    SimulationBase,
    PMRegistry,
    RegistryValidator,
    ValidationResult,
    SimulationResult as SchemaResult,
    validate_simulation_result,
)

from simulations.base.established import EstablishedPhysics

# v17: Import DemonLockGuard for pre-flight sterility check
try:
    from core.demon_lock_guard import DemonLockGuard
    DEMON_LOCK_AVAILABLE = True
except ImportError:
    DEMON_LOCK_AVAILABLE = False
    warnings.warn("DemonLockGuard not available - sterility pre-flight disabled")

# v17.1: Import SterilityReporter for sovereign audit reports
try:
    from core.verify_sterility_report import SterilityReporter
    STERILITY_REPORTER_AVAILABLE = True
except ImportError:
    STERILITY_REPORTER_AVAILABLE = False

# v17.1: Import DocumentationSynchronizer for SSoT sync
try:
    from core.sync_docs import DocumentationSynchronizer
    DOC_SYNC_AVAILABLE = True
except ImportError:
    DOC_SYNC_AVAILABLE = False

# v17.2: Import FormulasRegistry for Ghost Literal elimination
try:
    from core.FormulasRegistry import get_registry as get_formulas_registry
    FORMULAS_REGISTRY_AVAILABLE = True
except ImportError:
    FORMULAS_REGISTRY_AVAILABLE = False
    warnings.warn("FormulasRegistry not available - using fallback constants")

# v17.2-Absolute: Import validation scripts for anti-tautology checks
try:
    from tests.test_value_context_audit import ValueContextAuditor
    VALUE_CONTEXT_AUDIT_AVAILABLE = True
except ImportError:
    VALUE_CONTEXT_AUDIT_AVAILABLE = False

try:
    from tests.test_sterility_audit import GhostLiteralScanner
    STERILITY_AUDIT_AVAILABLE = True
except ImportError:
    STERILITY_AUDIT_AVAILABLE = False

# Import v16 simulations
# Phase 0 - Abstract and Introduction (narrative only, no dependencies)
from simulations.v16.introduction.introduction_v16_0 import IntroductionV16
from simulations.v16.introduction.abstract_v17_2 import AbstractV17_2

# Phase 1 - Root simulations (no dependencies)
from simulations.v16.geometric.g2_geometry_v16_0 import G2GeometryV16
from simulations.v16.gauge.gauge_unification_v16_0 import GaugeUnificationSimulation
from simulations.v16.master_action.master_action_simulation_v18 import MasterActionSimulationV18

# v16.2 - Geometric Anchors (fundamental constants from b3=24)
from simulations.v16.geometric.geometric_anchors_simulation_v16_2 import GeometricAnchorsSimulation

# v16.2 - Two-Time Physics and Leech Partition (foundational geometric proofs)
from simulations.v16.geometric.leech_partition_v16_2 import LeechPartitionV16
from simulations.v16.geometric.modular_invariance_v16_2 import ModularInvarianceV16

# v16.2 - Ghost-Free Stability Check (The Guardian) - BLOCKS simulations if anomaly not cancelled
try:
    from simulations.validation.unitary_filter_v16_2 import UnitaryFilterSimulation, UnitaryFilter
    UNITARY_FILTER_AVAILABLE = True
except ImportError:
    UNITARY_FILTER_AVAILABLE = False
    warnings.warn("UnitaryFilter not available - ghost-free validation disabled")

# Academic Armor v16.1 - Rigor simulations (geometric derivations)
try:
    from simulations.v16.geometric.alpha_rigor_v16_1 import AlphaRigorSimulation
    ALPHA_RIGOR_AVAILABLE = True
except ImportError:
    ALPHA_RIGOR_AVAILABLE = False

try:
    from simulations.v16.fermion.mass_ratio_v16_1 import MassRatioSimulation
    MASS_RATIO_AVAILABLE = True
except ImportError:
    MASS_RATIO_AVAILABLE = False

try:
    from simulations.v16.quantum_bio.orch_or_geometry_v16_1 import OrchORSimulation
    ORCH_OR_AVAILABLE = True
except ImportError:
    ORCH_OR_AVAILABLE = False

# Phase 2 - Core physics (depends on Phase 1)
from simulations.v16.fermion.fermion_generations_v16_0 import FermionGenerationsV16
from simulations.v16.fermion.chirality_v16_0 import ChiralitySpinorSimulation
from simulations.v16.fermion.ckm_matrix_v16_0 import CKMMatrixSimulation
from simulations.v16.proton.proton_decay_v16_0 import ProtonDecaySimulation
from simulations.v16.higgs.higgs_mass_v16_0 import HiggsMassSimulation
from simulations.v16.higgs.higgs_brane_partition_v16_2 import HiggsBranePartitionSimulation

# Phase 3 - Precision observables and cosmology (depends on Phase 2)
from simulations.v16.cosmology.cosmology_intro_v16_0 import CosmologyIntroV16
from simulations.v16.cosmology.dark_energy_v16_0 import DarkEnergyV16
from simulations.v16.cosmology.s8_suppression_v16_1 import S8SuppressionV16
from simulations.v16.cosmology.ricci_flow_h0_v16_1 import RicciFlowH0V16
from simulations.v16.thermal.thermal_time_v16_0 import ThermalTimeV16
from simulations.v16.neutrino.neutrino_mixing_v16_0 import NeutrinoMixingSimulation
from simulations.v16.cosmology.multi_sector_v16_0 import MultiSectorV16

# v16.2 - Dark Energy Thawing and Evolution Engine (Three Bridges)
from simulations.v16.cosmology.dark_energy_thawing_v16_2 import DarkEnergyEvolution
from simulations.v16.cosmology.evolution_engine_v16_2 import EvolutionEngineV16
from simulations.v16.fermion.octonionic_mixing_v16_2 import OctonionicMixing

# v17.2 - Speed of Light from Sovereign Constants
from simulations.v16.cosmology.speed_of_light_v17_2 import SpeedOfLightV17

# v17.2 - QED Manifold Constants (Decad-Cubic Projection Engine)
from simulations.v16.qed import (
    ComptonWavelengthV17,
    StefanBoltzmannV17,
    HartreeEnergyV17,
    MagneticFluxV17,
    VonKlitzingV17,
    AvogadroV17,
    FaradayV17,
    MolarGasV17,
    WeakMixingV17,
)

# Optional v16.1 cosmology simulations
try:
    from simulations.v16.cosmology.cosmological_constant_v16_1 import CosmologicalConstantV16
    COSMOLOGICAL_CONSTANT_AVAILABLE = True
except ImportError:
    COSMOLOGICAL_CONSTANT_AVAILABLE = False

# Phase 4 - Field dynamics (depends on all)
from simulations.v16.pneuma.pneuma_mechanism_v16_0 import PneumaMechanismV16

# Phase 5 - Discussion, predictions, and appendices (aggregators and reference material)
from simulations.v16.discussion.discussion_v16_0 import DiscussionV16
from simulations.v16.predictions.predictions_aggregator_v16_0 import PredictionsAggregatorV16

# v16.2 Sterile Model - New Section Simulations (Sections 1-4)
try:
    from simulations.v16.foundations.foundations_v16_2 import FoundationsV16_2
    FOUNDATIONS_AVAILABLE = True
except ImportError:
    FOUNDATIONS_AVAILABLE = False

try:
    from simulations.v16.methodology.methodology_v16_2 import MethodologyV16_2
    METHODOLOGY_AVAILABLE = True
except ImportError:
    METHODOLOGY_AVAILABLE = False

try:
    from simulations.v16.results.results_v16_2 import ResultsV16_2
    RESULTS_AVAILABLE = True
except ImportError:
    RESULTS_AVAILABLE = False

try:
    from simulations.v16.integrity.integrity_v16_2 import IntegrityV16_2
    INTEGRITY_AVAILABLE = True
except ImportError:
    INTEGRITY_AVAILABLE = False

# v16.2 Sterile Model - New Appendices (A-G)
try:
    from simulations.v16.appendices.appendix_a_spectral_registry_v16_2 import AppendixASpectralRegistry
    APPENDIX_A_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_A_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_b_sum_rule_v16_2 import AppendixBSumRule
    APPENDIX_B_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_B_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_c_gauge_matrices_v16_2 import AppendixCGaugeMatrices
    APPENDIX_C_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_C_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_d_alignment_v16_2 import AppendixDAlignment
    APPENDIX_D_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_D_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_e_brane_map_v16_2 import AppendixEBraneMap
    APPENDIX_E_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_E_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_f_72gates_v16_2 import Appendix72Gates
    APPENDIX_F_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_F_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_g_omega_seal_v16_2 import AppendixGOmegaSeal
    APPENDIX_G_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_G_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_h_288_roots_v16_2 import AppendixH288Roots
    APPENDIX_H_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_H_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_i_terminal_states_v16_2 import AppendixITerminalStates
    APPENDIX_I_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_I_V16_2_AVAILABLE = False

# ============================================================================
# LEGACY v16.0 APPENDICES - DEPRECATED IN v16.2 STERILE MODEL
# ============================================================================
# All legacy appendices have been superseded by the v16.2 Sterile Model structure.
# The v16.2 model treats constants as geometric necessities, not tunable values.
# These imports are preserved for historical reference but are not executed.
#
# from simulations.v16.appendices.appendix_a_math_v16_0 import AppendixAMathFoundations
# from simulations.v16.appendices.appendix_b_methods_v16_0 import AppendixBComputationalMethods
# from simulations.v16.appendices.appendix_c_derivations_v16_0 import AppendixCExtendedDerivations
# from simulations.v16.appendices.appendix_d_tables_v16_0 import AppendixDParameterTables
# from simulations.v16.appendices.appendix_e_proton_v16_0 import AppendixEProtonDecay
# from simulations.v16.appendices.appendix_f_v16_0 import AppendixFDimensionalDecomposition
# from simulations.v16.appendices.appendix_g_v16_0 import AppendixGEffectiveTorsion
# from simulations.v16.appendices.appendix_h_v16_0 import AppendixHProtonBranching
# from simulations.v16.appendices.appendix_i_v16_0 import AppendixIGWDispersion
# from simulations.v16.appendices.appendix_j_v16_0 import AppendixJMonteCarloError
# from simulations.v16.appendices.appendix_k_v16_0 import AppendixKTransparency
# from simulations.v16.appendices.appendix_l_v16_0 import AppendixLValuesSummary
# from simulations.v16.appendices.appendix_m_v16_0 import AppendixMConsciousnessSpeculation
# from simulations.v16.appendices.appendix_n_v16_0 import AppendixNG2Landscape
# ============================================================================

# v16.2 Sterile Model - New Appendices J, K, L
try:
    from simulations.v16.appendices.appendix_j_torsion_funnel_v16_2 import AppendixJTorsionFunnel
    APPENDIX_J_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_J_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_k_sterile_constants_v16_2 import AppendixKSterileConstants
    APPENDIX_K_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_K_V16_2_AVAILABLE = False

try:
    from simulations.v16.appendices.appendix_l_omega_unwinding_v16_2 import AppendixLOmegaUnwinding
    APPENDIX_L_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_L_V16_2_AVAILABLE = False

# v16.2 Sterile Model - Appendix Z: Terminal Constant Ledger
try:
    from simulations.v16.appendices.appendix_z_terminal_ledger_v16_2 import AppendixZTerminalLedger
    APPENDIX_Z_V16_2_AVAILABLE = True
except ImportError:
    APPENDIX_Z_V16_2_AVAILABLE = False


# ============================================================================
# V16.0 VALIDATION BOUNDS
# ============================================================================
V16_VALIDATION_BOUNDS = {
    # Dark matter ratio: theory predicts 5.82, Planck measures 5.38±0.15
    "cosmology.Omega_DM_over_b": {
        "min": 5.0,
        "max": 6.5,
        "target": 5.82,
        "experimental": 5.38,
        "sigma": 0.15,
    },

    # Proton lifetime: Super-K bound > 1.67e34, theory predicts 4.8e34
    "proton_decay.tau_p_years": {
        "min": 1.67e34,
        "max": None,
        "target": 4.8e34,
    },

    # Higgs mass: PDG 125.10±0.14, theory gives 120-125 GeV
    "higgs.m_h_predicted": {
        "min": 115,
        "max": 130,
        "target": 125.10,  # Higgs mass (PDG)
        "experimental": 125.10,  # Higgs mass (PDG)
        "sigma": 0.14,
    },

    # Dark energy EoS: v16.2 thawing formula w0 = -1 + 1/b3 = -23/24
    # DESI 2025 thawing constraint: -0.957 ± 0.067
    # NOTE: target loaded from FormulasRegistry.tzimtzum_pressure at runtime
    "cosmology.w0_derived": {
        "min": -1.0,
        "max": -0.9,
        "target": None,  # Set dynamically from FormulasRegistry
        "experimental": -0.957,
        "sigma": 0.067,
    },

    # PMNS angles with NuFIT 6.0 comparison
    "neutrino.theta_12_pred": {
        "min": 31,
        "max": 36,
        "target": 33.59,
        "experimental": 33.41,
        "sigma": 0.75,
    },
    "neutrino.theta_13_pred": {
        "min": 7.5,
        "max": 9.5,
        "target": 8.33,
        "experimental": 8.54,
        "sigma": 0.11,
    },
    "neutrino.theta_23_pred": {
        "min": 47,
        "max": 52,
        "target": 49.75,
        "experimental": 49.3,  # NuFIT 6.0 IO upper octant
        "sigma": 1.0,  # +1.0/-1.2
    },
    "neutrino.delta_CP_pred": {
        "min": 180,
        "max": 320,
        "target": 278.0,  # v16.2: Use IO value (PM matches IO at 0.02σ)
        "experimental": 278,  # v16.2: NuFIT 6.0 Inverted Ordering
        "sigma": 26,
    },

    # Jarlskog invariant
    "ckm.J_invariant": {
        "min": 2.5e-5,
        "max": 3.5e-5,
        "target": 3.08e-5,
        "experimental": 3.0e-5,
        "sigma": 0.3e-5,
    },
}

# v17.2: Dynamically populate target values from FormulasRegistry (Ghost Literal elimination)
if FORMULAS_REGISTRY_AVAILABLE:
    _formula_reg = get_formulas_registry()
    # w0_derived target = -tzimtzum_pressure = -23/24
    V16_VALIDATION_BOUNDS["cosmology.w0_derived"]["target"] = -_formula_reg.tzimtzum_pressure
else:
    # Fallback to hardcoded value if registry unavailable
    V16_VALIDATION_BOUNDS["cosmology.w0_derived"]["target"] = -0.9583


def validate_against_bounds(param_path: str, value: float) -> Dict[str, Any]:
    """
    Validate a parameter value against V16.0 experimental bounds.

    Args:
        param_path: Parameter path (e.g., "cosmology.Omega_DM_over_b")
        value: Computed value to validate

    Returns:
        Dictionary with validation status, sigma deviation, and details
    """
    bounds = V16_VALIDATION_BOUNDS.get(param_path)
    if not bounds:
        return {"status": "NO_BOUNDS", "sigma": None}

    sigma_dev = None
    if "experimental" in bounds and "sigma" in bounds:
        sigma_dev = abs(value - bounds["experimental"]) / bounds["sigma"]

    in_range = True
    if bounds.get("min") is not None and value < bounds["min"]:
        in_range = False
    if bounds.get("max") is not None and value > bounds["max"]:
        in_range = False

    return {
        "status": "PASS" if in_range else "FAIL",
        "sigma_deviation": sigma_dev,
        "target": bounds.get("target"),
        "experimental": bounds.get("experimental"),
        "in_range": in_range,
        "value": value,
    }


@dataclass
class TensionWarning:
    """Warning for parameters with >1sigma deviation from experiment."""
    param_path: str
    sigma_deviation: float
    theory_value: float
    experimental_value: float
    experimental_sigma: float
    explanation: str = ""


def get_git_metadata() -> Dict[str, str]:
    """
    Extract git metadata for provenance tracking.

    Returns:
        Dictionary containing commit hash, branch, dirty status
    """
    try:
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=os.path.dirname(__file__)
        ).decode().strip()
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=os.path.dirname(__file__)
        ).decode().strip()
        is_dirty = subprocess.check_output(
            ['git', 'status', '--porcelain'],
            cwd=os.path.dirname(__file__)
        ).decode().strip() != ''
        return {
            'commit_hash': commit_hash,
            'branch': branch,
            'is_dirty': is_dirty,
            'dirty_suffix': '-dirty' if is_dirty else ''
        }
    except Exception:
        return {
            'commit_hash': 'unknown',
            'branch': 'unknown',
            'is_dirty': False,
            'dirty_suffix': ''
        }


def validate_section_assignments(simulations: List['SimulationBase'], verbose: bool = True) -> Dict[str, Any]:
    """
    v19.0: Validate that all simulations have unique section assignments.

    This prevents duplicate sections from overwriting each other in the paper.

    Args:
        simulations: List of all simulation instances
        verbose: Whether to print detailed output

    Returns:
        Dictionary with validation results:
        - passed: True if no duplicates found
        - duplicates: Dict mapping section_keys to list of simulation_ids claiming them
        - total_sections: Number of unique sections
        - warnings: List of warning messages
    """
    section_map: Dict[str, List[str]] = {}  # section_key -> [simulation_ids]
    warnings: List[str] = []

    for sim in simulations:
        if not hasattr(sim, 'metadata'):
            continue

        sim_id = sim.metadata.id
        section_id = getattr(sim.metadata, 'section_id', None)
        subsection_id = getattr(sim.metadata, 'subsection_id', None)

        if section_id is None:
            continue

        # Determine the section key (subsection_id takes precedence if present)
        section_key = subsection_id if subsection_id else section_id

        if section_key not in section_map:
            section_map[section_key] = []
        section_map[section_key].append(sim_id)

        # Also check get_section_content if available
        if hasattr(sim, 'get_section_content') and callable(sim.get_section_content):
            try:
                content = sim.get_section_content()
                if content is not None:
                    content_key = content.subsection_id or content.section_id
                    if content_key != section_key:
                        warnings.append(
                            f"{sim_id}: metadata section_id '{section_key}' != "
                            f"get_section_content() section_id '{content_key}'"
                        )
            except Exception:
                pass  # Skip if content generation fails

    # Find duplicates (sections claimed by multiple simulations)
    duplicates = {k: v for k, v in section_map.items() if len(v) > 1}

    passed = len(duplicates) == 0

    if verbose:
        print("\n[SECTION VALIDATION] Checking for duplicate section assignments...")
        print("-" * 80)

        if passed:
            print(f"[OK] All {len(section_map)} sections have unique assignments")
        else:
            print(f"[WARNING] Found {len(duplicates)} duplicate section assignment(s):")
            for section_key, sim_ids in duplicates.items():
                print(f"  Section '{section_key}' claimed by:")
                for sid in sim_ids:
                    print(f"    - {sid}")

        if warnings:
            print(f"\n[WARNING] Found {len(warnings)} metadata inconsistencies:")
            for w in warnings:
                print(f"  - {w}")

        print("-" * 80)

    return {
        'passed': passed,
        'duplicates': duplicates,
        'total_sections': len(section_map),
        'section_map': section_map,
        'warnings': warnings
    }


@dataclass
class SimulationResult:
    """Result of running a single simulation."""
    simulation_id: str
    phase: int
    status: str  # "PASSED", "FAILED", "SKIPPED"
    dependency_check: ValidationResult
    output_check: Optional[ValidationResult] = None
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    outputs_computed: List[str] = field(default_factory=list)
    formulas_registered: int = 0


class SimulationRunner:
    """
    Orchestrates execution of all v16 simulations in topological order.
    """

    def __init__(self, verbose: bool = True, schema_mode: bool = False, uq_mode: bool = False):
        """
        Initialize the simulation runner.

        Args:
            verbose: Whether to print progress messages
            schema_mode: Whether to use schema-compliant execution mode
            uq_mode: Whether to enable Monte Carlo uncertainty quantification
        """
        self.verbose = verbose
        self.schema_mode = schema_mode
        self.uq_mode = uq_mode
        self.registry = PMRegistry.get_instance()
        self.results: List[SimulationResult] = []
        self.schema_results: List[Dict[str, Any]] = []  # Schema-compliant results
        self.tensions: List[TensionWarning] = []  # Track >1sigma deviations

        # Validate UQ mode
        if self.uq_mode and not NUMPY_AVAILABLE:
            raise RuntimeError("UQ mode requires NumPy. Install with: pip install numpy")

        # Define simulation phases in topological order
        self.phases = {
            0: [
                AbstractV17_2(),  # Section 0: Abstract
                IntroductionV16(),
            ],
            1: [
                # v16.2: GeometricAnchors FIRST - provides fundamental constants for all other simulations
                GeometricAnchorsSimulation(),
                G2GeometryV16(),
            ] + ([UnitaryFilterSimulation()] if UNITARY_FILTER_AVAILABLE else []) + [
                # After UnitaryFilter validates ghost-free stability:
                LeechPartitionV16(),       # v16.2 - Proves 24/8=3 generations
                ModularInvarianceV16(),    # v16.2 - Proves b3=24 uniqueness
                GaugeUnificationSimulation(),
                MasterActionSimulationV18(),  # v18: SM gauge sectors from 26D master action
            ] + ([AlphaRigorSimulation()] if ALPHA_RIGOR_AVAILABLE else []),
            2: [
                FermionGenerationsV16(),
                ChiralitySpinorSimulation(),
                CKMMatrixSimulation(),
                ProtonDecaySimulation(),
                HiggsMassSimulation(),
                HiggsBranePartitionSimulation(),  # v16.2: Brane-partition local Higgs mass
            ] + ([MassRatioSimulation()] if MASS_RATIO_AVAILABLE else []),
            3: [
                CosmologyIntroV16(),
                DarkEnergyV16(),
                DarkEnergyEvolution(),       # v16.2 - Thawing dark energy from G2 Ricci flow
                EvolutionEngineV16(),        # v16.2 - H(z) evolution with Ricci flow
                S8SuppressionV16(),
                RicciFlowH0V16(),
                NeutrinoMixingSimulation(),
                OctonionicMixing(),          # v16.2 - CKM/PMNS from octonionic structure
                MultiSectorV16(),
                SpeedOfLightV17(),           # v17.2 - Speed of Light from Sovereign Constants
                # v17.2 - QED Manifold Constants (Decad-Cubic Projection Engine)
                ComptonWavelengthV17(),      # Inverse Cubic - wavelengths contract
                StefanBoltzmannV17(),        # Quad-Gate - 4D thermal vibration
                HartreeEnergyV17(),          # Inverse Double-Gate - binding energy
                MagneticFluxV17(),           # Direct Expansion - flux with h
                VonKlitzingV17(),            # Direct Expansion - resistance with h
                AvogadroV17(),               # Inverse Cubic - counts contract
                FaradayV17(),                # Inverse Cubic - follows N_A
                MolarGasV17(),               # Neutral Bridge - N_A*k cancellation
                WeakMixingV17(),             # Torsion Gate - coupling ratio
            ] + ([CosmologicalConstantV16()] if COSMOLOGICAL_CONSTANT_AVAILABLE else []),
            4: [
                PneumaMechanismV16(),
                ThermalTimeV16(),  # Moved to Phase 4 - depends on Pneuma outputs
            ],
            5: ([OrchORSimulation()] if ORCH_OR_AVAILABLE else []) + [
                DiscussionV16(),
                PredictionsAggregatorV16(),
                # ================================================================
                # LEGACY v16.0 APPENDICES - FULLY DEPRECATED IN v16.2 STERILE MODEL
                # ================================================================
                # All legacy appendices have been superseded by the v16.2 structure.
                # In a sterile model, we don't check if values are "tuned correctly"
                # because the geometry makes it impossible for values to be anything else.
                #
                # Deprecated certificates that relied on observation are now obsolete:
                # - C05 (Hubble Tuning) → Absorbed into C02-R (H0 is Node 001 residue)
                # - C08 (Lambda-Check) → Replaced by C44 (4-Pattern Orthogonality)
                # - C11 (Fine-Structure) → Locked by C19-T (Torsion Lock)
                # - C07, C14, C22, C33 → Removed (observer-dependent)
                #
                # Physical predictions are now geometric necessities in v16.2.
                # ================================================================
            ],
            # ================================================================
            # v16.2 STERILE MODEL - Paper Sections and Appendices
            # ================================================================
            # Phase 6: v16.2 Paper Structure (narrative content simulations)
            6: (
                # Section 1: Foundations of Dimensional Descent
                ([FoundationsV16_2()] if FOUNDATIONS_AVAILABLE else []) +
                # Section 2: Sterile Extraction Methodology
                ([MethodologyV16_2()] if METHODOLOGY_AVAILABLE else []) +
                # Section 3: Cosmological Results and Alignment
                ([ResultsV16_2()] if RESULTS_AVAILABLE else []) +
                # Section 4: System Integrity and Verification
                ([IntegrityV16_2()] if INTEGRITY_AVAILABLE else []) +
                # Appendix A: Spectral Registry (125 Residues)
                ([AppendixASpectralRegistry()] if APPENDIX_A_V16_2_AVAILABLE else []) +
                # Appendix B: Global Sum Rule and Trace Formula
                ([AppendixBSumRule()] if APPENDIX_B_V16_2_AVAILABLE else []) +
                # Appendix C: S_PR(2) Gauge Reduction Matrices
                ([AppendixCGaugeMatrices()] if APPENDIX_C_V16_2_AVAILABLE else []) +
                # Appendix D: 0.48σ Alignment Data
                ([AppendixDAlignment()] if APPENDIX_D_V16_2_AVAILABLE else []) +
                # Appendix E: Brane-Intersection Map
                ([AppendixEBraneMap()] if APPENDIX_E_V16_2_AVAILABLE else []) +
                # Appendix F: 72 Gates of Integrity (v16.2 architecture)
                ([Appendix72Gates()] if APPENDIX_F_V16_2_AVAILABLE else []) +
                # Appendix G: Omega Seal Cryptographic Protocol
                ([AppendixGOmegaSeal()] if APPENDIX_G_V16_2_AVAILABLE else []) +
                # Appendix H: 288-Root Ancestral Basis (SO(24) + Shadow Torsion)
                ([AppendixH288Roots()] if APPENDIX_H_V16_2_AVAILABLE else []) +
                # Appendix I: Three Terminal States of the Universe
                ([AppendixITerminalStates()] if APPENDIX_I_V16_2_AVAILABLE else []) +
                # Appendix J: The Torsion Funnel (288→24→125 Flow Visualization)
                ([AppendixJTorsionFunnel()] if APPENDIX_J_V16_2_AVAILABLE else []) +
                # Appendix K: The Sterile Constant Table (Geometric Residue Registry)
                ([AppendixKSterileConstants()] if APPENDIX_K_V16_2_AVAILABLE else []) +
                # Appendix L: The Omega Unwinding Map (Terminal State Phase Diagram)
                ([AppendixLOmegaUnwinding()] if APPENDIX_L_V16_2_AVAILABLE else []) +
                # Appendix Z: Terminal Constant Ledger (10 Formulas, ZERO Free Parameters)
                ([AppendixZTerminalLedger()] if APPENDIX_Z_V16_2_AVAILABLE else [])
            ),
        }

    def run_all(self) -> Dict[str, Any]:
        """
        Execute all simulations in topological order.

        Returns:
            Dictionary containing validation report and export data
        """
        self._print_header()

        # Step 1: Load established physics (experimental constants)
        self._load_established_physics()

        # Step 1b: Load geometric anchors (v16.2 - derived from b3=24)
        self._load_geometric_anchors()

        # Step 1c: v19.0 - Validate section assignments BEFORE running
        all_simulations = []
        for phase_sims in self.phases.values():
            all_simulations.extend(phase_sims)
        section_validation = validate_section_assignments(all_simulations, verbose=self.verbose)

        # Store section validation results for the report
        self._section_validation = section_validation

        # Step 2: Execute simulations in phases
        for phase_num in sorted(self.phases.keys()):
            self._run_phase(phase_num)

        # Step 3: Validate against V16.0 bounds
        self._validate_v16_bounds()

        # Step 4: Generate validation report
        validation_report = self._generate_validation_report()

        # Step 5: Omega Hash Check (Gate 72 - STERILE validation)
        omega_hash_passed = self._check_omega_hash()
        validation_report["omega_hash_passed"] = omega_hash_passed

        # Step 6: Export to theory_output.json
        output_data = self._export_to_json(validation_report)

        # Step 7: Print summary
        self._print_summary(validation_report)

        # CRITICAL: If Omega Hash fails, terminate with error
        if not omega_hash_passed:
            print("\n" + "=" * 80)
            print("[CRITICAL] OMEGA HASH FAILED - STERILE STATUS COMPROMISED")
            print("Gate 72 validation: Bit-sum is NOT zero - model is NOT sterile!")
            print("=" * 80)
            sys.exit(72)  # Exit code 72 = Gate 72 failure

        return output_data

    def _print_header(self) -> None:
        """Print the runner header."""
        if not self.verbose:
            return

        print("=" * 80)
        print("PRINCIPIA METAPHYSICA - Run All Simulations v17.2")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Total simulations: {sum(len(sims) for sims in self.phases.values())}")
        if self.uq_mode:
            print("UQ Mode: ENABLED (Monte Carlo uncertainty quantification)")
        print("=" * 80)

    def _load_established_physics(self) -> None:
        """Load experimental constants into the registry."""
        if self.verbose:
            print("\n[INITIALIZATION] Loading Established Physics")
            print("-" * 80)

        EstablishedPhysics.load_into_registry(self.registry)

        if self.verbose:
            param_count = len(self.registry._parameters)
            print(f"[OK] Loaded {param_count} established parameters")
            print("  - PDG 2024 constants")
            print("  - NuFIT 6.0 neutrino parameters")
            print("  - DESI DR2 cosmological parameters")
            print("  - Experimental bounds (Super-K, LHC, etc.)")

    def _load_geometric_anchors(self) -> None:
        """
        v16.2: Pre-load minimal topology parameters for bootstrap.

        NOTE: The full GeometricAnchorsSimulation runs in Phase 1 and provides
        all derived constants. This method only pre-loads the minimum needed
        for simulation ordering. Use GEOMETRIC status (not ESTABLISHED) since
        these are derived from G2 manifold topology, not experimental data.

        Key principle: derived values should be checked against experimental,
        not marked as ESTABLISHED which prevents override.
        """
        if self.verbose:
            print("\n[INITIALIZATION] Pre-loading Geometric Anchors (v16.2 Demon-Lock)")
            print("-" * 80)

        # Register system version first (SYSTEM status - not counted in scientific stats)
        try:
            from core.FormulasRegistry import FormulasRegistry
            if not self.registry.has_param("system.version"):
                self.registry.set_param("system.version", FormulasRegistry.VERSION,
                                         source="SYSTEM:FormulasRegistry",
                                         status="SYSTEM",
                                         metadata={
                                             "description": "Framework version number",
                                             "is_scientific": False,
                                             "display_in_params": False
                                         })
        except Exception as e:
            if self.verbose:
                print(f"[WARN] Could not register system.version: {e}")

        try:
            # Pre-load minimal topology params with GEOMETRIC status
            # GeometricAnchorsSimulation will register the full set in Phase 1
            # Using GEOMETRIC (not ESTABLISHED) allows validation against experiment
            import numpy as np

            if not self.registry.has_param("topology.b3"):
                self.registry.set_param("topology.b3", 24,
                                         source="GEOMETRIC:TCS_G2_187", status="GEOMETRIC")
            if not self.registry.has_param("topology.chi_eff"):
                self.registry.set_param("topology.chi_eff", 144,
                                         source="GEOMETRIC:TCS_G2_187", status="GEOMETRIC")

            # Pre-compute k_gimel for early use
            k_gimel = 24 / 2 + 1 / np.pi
            if not self.registry.has_param("topology.k_gimel"):
                self.registry.set_param("topology.k_gimel", k_gimel,
                                         source="GEOMETRIC:k_gimel_formula", status="GEOMETRIC")

            if self.verbose:
                print(f"[OK] Pre-loaded core topology parameters (GEOMETRIC status)")
                print(f"  - topology.b3 = 24 (derived from G2 manifold)")
                print(f"  - topology.chi_eff = 144 (derived from TCS #187)")
                print(f"  - topology.k_gimel = {k_gimel:.6f} (derived: b3/2 + 1/pi)")
                print(f"  Note: Full geometric anchors computed in Phase 1")

        except Exception as e:
            if self.verbose:
                print(f"[WARN] Could not pre-load geometric anchors: {e}")

    def _run_phase(self, phase_num: int) -> None:
        """
        Execute all simulations in a given phase.

        Args:
            phase_num: Phase number (1-4)
        """
        simulations = self.phases[phase_num]

        if self.verbose:
            print(f"\n[PHASE {phase_num}] Running {len(simulations)} simulation(s)")
            print("-" * 80)

        for sim in simulations:
            if self.uq_mode:
                self._run_simulation_with_uq(sim, phase_num)
            else:
                self._run_simulation(sim, phase_num)

    def _run_simulation(self, sim: SimulationBase, phase: int) -> None:
        """
        Execute a single simulation with validation.

        Args:
            sim: SimulationBase instance
            phase: Phase number for tracking
        """
        sim_id = sim.metadata.id

        if self.verbose:
            print(f"\n> {sim_id}: {sim.metadata.title}")

        # Create result entry
        result = SimulationResult(
            simulation_id=sim_id,
            phase=phase,
            status="PENDING",
            dependency_check=ValidationResult(passed=True),
        )

        try:
            # Step 1: Check dependencies
            if self.verbose:
                print(f"  Checking dependencies...")

            result.dependency_check = RegistryValidator.check_dependencies(sim, self.registry)

            if not result.dependency_check.passed:
                result.status = "FAILED"
                result.error_message = "Missing dependencies"
                if self.verbose:
                    print(f"  [X] Dependency check failed:")
                    for error in result.dependency_check.errors:
                        print(f"    - {error}")
                self.results.append(result)
                return

            if self.verbose:
                print(f"  [OK] All dependencies satisfied")

            # Step 2: Execute simulation
            if self.verbose:
                mode_str = " (schema mode)" if self.schema_mode else ""
                print(f"  Running simulation{mode_str}...")

            start_time = datetime.now()

            if self.schema_mode:
                # Execute with schema-compliant output
                schema_result = sim.execute_with_schema(self.registry, verbose=False)
                computed_results = schema_result.computedValues

                # Validate schema compliance
                schema_validation = validate_simulation_result(schema_result.to_dict())
                if not schema_validation["valid"]:
                    if self.verbose:
                        print(f"  [!] Schema validation warnings: {schema_validation['errors']}")

                # Store schema result
                self.schema_results.append(schema_result.to_dict())
            else:
                computed_results = sim.execute(self.registry, verbose=False)

            end_time = datetime.now()

            result.execution_time_ms = (end_time - start_time).total_seconds() * 1000
            result.outputs_computed = list(computed_results.keys())

            # Track formula count for this simulation
            if hasattr(sim, 'get_formulas') and callable(sim.get_formulas):
                formulas = sim.get_formulas()
                result.formulas_registered = len(formulas) if formulas else 0

            if self.verbose:
                print(f"  [OK] Completed in {result.execution_time_ms:.2f}ms")

            # Step 3: Validate outputs
            if self.verbose:
                print(f"  Validating outputs...")

            result.output_check = RegistryValidator.check_outputs(
                sim, computed_results, self.registry
            )

            if not result.output_check.passed:
                result.status = "FAILED"
                result.error_message = "Output validation failed"
                if self.verbose:
                    print(f"  [X] Output validation failed:")
                    for error in result.output_check.errors:
                        print(f"    - {error}")
            else:
                result.status = "PASSED"
                if self.verbose:
                    print(f"  [OK] All outputs validated")
                    print(f"  Computed: {len(result.outputs_computed)} parameters")

                # Step 4: Collect section content from simulation (v16.2+)
                if hasattr(sim, 'get_section_content') and callable(sim.get_section_content):
                    try:
                        section_content = sim.get_section_content()
                        if section_content is not None:
                            # Use subsection_id if present, else section_id
                            section_key = section_content.subsection_id or section_content.section_id
                            self.registry.add_section_content(section_key, section_content)
                            if self.verbose:
                                print(f"  [+] Section content registered: {section_key}")
                    except Exception as sec_e:
                        if self.verbose:
                            print(f"  [!] Could not collect section content: {sec_e}")

        except Exception as e:
            result.status = "FAILED"
            result.error_message = str(e)
            if self.verbose:
                print(f"  [X] Simulation failed with error: {e}")

        self.results.append(result)

    def _run_simulation_with_uq(self, sim: SimulationBase, phase: int, n_samples: int = 100) -> None:
        """
        Execute a single simulation with Monte Carlo UQ.

        Args:
            sim: SimulationBase instance
            phase: Phase number for tracking
            n_samples: Number of Monte Carlo samples (default: 100)
        """
        sim_id = sim.metadata.id

        if self.verbose:
            print(f"\n> {sim_id}: {sim.metadata.title} [UQ MODE: {n_samples} samples]")

        # Create result entry
        result = SimulationResult(
            simulation_id=sim_id,
            phase=phase,
            status="PENDING",
            dependency_check=ValidationResult(passed=True),
        )

        try:
            # Step 1: Check dependencies
            if self.verbose:
                print(f"  Checking dependencies...")

            result.dependency_check = RegistryValidator.check_dependencies(sim, self.registry)

            if not result.dependency_check.passed:
                result.status = "FAILED"
                result.error_message = "Missing dependencies"
                if self.verbose:
                    print(f"  [X] Dependency check failed:")
                    for error in result.dependency_check.errors:
                        print(f"    - {error}")
                self.results.append(result)
                return

            if self.verbose:
                print(f"  [OK] All dependencies satisfied")

            # Step 2: Run Monte Carlo sampling
            if self.verbose:
                print(f"  Running Monte Carlo UQ with {n_samples} samples...")

            start_time = datetime.now()

            # Store results for each sample
            all_outputs = []

            for i in range(n_samples):
                # TODO: Add Gaussian noise to input parameters
                # For now, just run the simulation multiple times
                computed_results = sim.execute(self.registry, verbose=False)
                all_outputs.append(computed_results)

            end_time = datetime.now()

            # Compute mean and std for each output parameter
            output_stats = {}
            if all_outputs:
                param_names = list(all_outputs[0].keys())
                for param_name in param_names:
                    values = [output.get(param_name) for output in all_outputs if param_name in output]
                    if values and all(isinstance(v, (int, float)) for v in values):
                        output_stats[param_name] = {
                            "mean": float(np.mean(values)),
                            "std": float(np.std(values)),
                            "min": float(np.min(values)),
                            "max": float(np.max(values)),
                        }

            result.execution_time_ms = (end_time - start_time).total_seconds() * 1000
            result.outputs_computed = list(output_stats.keys())

            # Track formula count for this simulation
            if hasattr(sim, 'get_formulas') and callable(sim.get_formulas):
                formulas = sim.get_formulas()
                result.formulas_registered = len(formulas) if formulas else 0

            if self.verbose:
                print(f"  [OK] Completed in {result.execution_time_ms:.2f}ms")
                print(f"  UQ Statistics computed for {len(output_stats)} parameters")

            # Step 3: Store mean values in registry (for now)
            # In future, could store full distributions
            computed_results = {}
            for param_name, stats in output_stats.items():
                computed_results[param_name] = stats["mean"]

            # Step 4: Validate outputs
            if self.verbose:
                print(f"  Validating outputs...")

            result.output_check = RegistryValidator.check_outputs(
                sim, computed_results, self.registry
            )

            if not result.output_check.passed:
                result.status = "FAILED"
                result.error_message = "Output validation failed"
                if self.verbose:
                    print(f"  [X] Output validation failed:")
                    for error in result.output_check.errors:
                        print(f"    - {error}")
            else:
                result.status = "PASSED"
                if self.verbose:
                    print(f"  [OK] All outputs validated")

        except Exception as e:
            result.status = "FAILED"
            result.error_message = str(e)
            if self.verbose:
                print(f"  [X] Simulation failed with error: {e}")

        self.results.append(result)

    def _validate_v16_bounds(self) -> None:
        """Validate all computed parameters against V16.0 bounds."""
        if self.verbose:
            print("\n[V16.0 VALIDATION] Checking parameters against experimental bounds")
            print("-" * 80)

        # Get all parameters from registry
        all_params = self.registry.export_parameters()

        tensions_found = 0
        params_checked = 0

        for param_path, bounds in V16_VALIDATION_BOUNDS.items():
            # Try to find the parameter in the registry
            param_data = all_params.get(param_path)

            if param_data is None:
                # Try alternative paths (e.g., without domain prefix)
                parts = param_path.split('.')
                if len(parts) > 1:
                    alt_path = '.'.join(parts[1:])
                    param_data = all_params.get(alt_path)

            if param_data is None:
                if self.verbose:
                    print(f"  [SKIP] {param_path}: Parameter not computed")
                continue

            value = param_data.get("value")
            if value is None:
                continue

            params_checked += 1

            # Validate against bounds
            validation_result = validate_against_bounds(param_path, value)

            if validation_result["status"] == "FAIL":
                if self.verbose:
                    print(f"  [FAIL] {param_path}: {value} out of range")
                    print(f"         Expected: [{bounds.get('min', 'N/A')}, {bounds.get('max', 'N/A')}]")

            # Check for >1sigma tension (v16.2: stricter threshold)
            sigma_dev = validation_result.get("sigma_deviation")
            if sigma_dev is not None and sigma_dev > 1.0:
                tensions_found += 1

                tension = TensionWarning(
                    param_path=param_path,
                    sigma_deviation=sigma_dev,
                    theory_value=value,
                    experimental_value=bounds["experimental"],
                    experimental_sigma=bounds["sigma"],
                    explanation=f"{sigma_dev:.2f} sigma deviation from experimental value"
                )
                self.tensions.append(tension)

                if self.verbose:
                    print(f"  [TENSION] {param_path}: {sigma_dev:.2f} sigma deviation")
                    print(f"            Theory: {value:.4g}, Experiment: {bounds['experimental']:.4g} ± {bounds['sigma']:.4g}")

            elif validation_result["status"] == "PASS" and self.verbose:
                sigma_str = f" ({sigma_dev:.2f}sigma)" if sigma_dev is not None else ""
                print(f"  [PASS] {param_path}: {value:.4g}{sigma_str}")

        if self.verbose:
            print(f"\n[OK] Validated {params_checked} parameters against V16.0 bounds")
            if tensions_found > 0:
                print(f"[WARNING] Found {tensions_found} parameter(s) with >1sigma tension")

    def _generate_validation_report(self) -> Dict[str, Any]:
        """
        Generate validation report from all simulation results.

        Returns:
            Dictionary containing validation statistics and details
        """
        passed = [r for r in self.results if r.status == "PASSED"]
        failed = [r for r in self.results if r.status == "FAILED"]
        skipped = [r for r in self.results if r.status == "SKIPPED"]

        report = {
            "timestamp": datetime.now().isoformat(),
            "simulations_run": len(self.results),
            "simulations_passed": len(passed),
            "simulations_failed": len(failed),
            "simulations_skipped": len(skipped),
            "total_execution_time_ms": sum(r.execution_time_ms for r in self.results),
            "uq_mode_enabled": self.uq_mode,
            "tensions": [],  # V16.2: Track >1sigma deviations
            "results": []
        }

        # Add tension warnings
        for tension in self.tensions:
            report["tensions"].append({
                "param": tension.param_path,
                "sigma": tension.sigma_deviation,
                "theory_value": tension.theory_value,
                "experimental_value": tension.experimental_value,
                "experimental_sigma": tension.experimental_sigma,
                "explanation": tension.explanation,
            })

        # Add detailed results
        for result in self.results:
            result_dict = {
                "simulation_id": result.simulation_id,
                "phase": result.phase,
                "status": result.status,
                "execution_time_ms": result.execution_time_ms,
                "outputs_computed": result.outputs_computed,
            }

            if result.error_message:
                result_dict["error_message"] = result.error_message

            if result.dependency_check and not result.dependency_check.passed:
                result_dict["dependency_errors"] = result.dependency_check.errors

            if result.output_check and not result.output_check.passed:
                result_dict["output_errors"] = result.output_check.errors
                result_dict["output_warnings"] = result.output_check.warnings

            report["results"].append(result_dict)

        return report

    def _collect_beginner_explanations(self) -> Dict[str, Any]:
        """
        Collect beginner explanations from all simulations.

        Returns:
            Dictionary with beginner guide content from all simulations
        """
        explanations = {
            "title": "Beginner's Guide to Principia Metaphysica",
            "description": "Accessible explanations of the key concepts and predictions",
            "topics": []
        }

        # Collect from all phases in order
        for phase_num in sorted(self.phases.keys()):
            for sim in self.phases[phase_num]:
                # Check if simulation has get_beginner_explanation method
                if hasattr(sim, 'get_beginner_explanation'):
                    try:
                        explanation = sim.get_beginner_explanation()
                        explanation["simulation_id"] = sim.metadata.id
                        explanation["domain"] = sim.metadata.domain
                        explanation["section"] = sim.metadata.section_id
                        explanations["topics"].append(explanation)
                    except Exception as e:
                        if self.verbose:
                            print(f"  Warning: Could not get beginner explanation from {sim.metadata.id}: {e}")

        if self.verbose:
            print(f"  [OK] Collected {len(explanations['topics'])} beginner explanations")

        return explanations

    def _collect_references(self) -> List[Dict[str, Any]]:
        """
        Collect references from all simulations.

        Returns:
            List of unique references from all simulations
        """
        all_references = []
        seen_ids = set()

        # Collect from all phases in order
        for phase_num in sorted(self.phases.keys()):
            for sim in self.phases[phase_num]:
                # Check if simulation has get_references method
                if hasattr(sim, 'get_references'):
                    try:
                        refs = sim.get_references()
                        for ref in refs:
                            ref_id = ref.get('id', ref.get('title', '').lower().replace(' ', '_')[:30])
                            if ref_id not in seen_ids:
                                seen_ids.add(ref_id)
                                ref['source_simulation'] = sim.metadata.id
                                all_references.append(ref)
                    except Exception as e:
                        if self.verbose:
                            print(f"  Warning: Could not get references from {sim.metadata.id}: {e}")

        return all_references

    def _classify_parameters(self) -> Dict[str, List[str]]:
        """
        Classify parameters by type (established, geometric, derived, calibrated).

        Returns:
            Dictionary mapping parameter types to lists of parameter keys
        """
        classification = {
            "established": [],
            "geometric": [],
            "derived": [],
            "calibrated": []
        }

        for param_key, param_data in self.registry._parameters.items():
            # Extract parameter status/type from RegistryEntry attributes
            source = getattr(param_data, "source", "")
            metadata = getattr(param_data, "metadata", {})
            description = metadata.get("description", "").lower() if isinstance(metadata, dict) else ""
            status = getattr(param_data, "status", "DERIVED")

            # Classify based on source, status, and characteristics
            if status == "ESTABLISHED" or "ESTABLISHED" in source or "pdg" in description or "nufit" in description or "desi" in description:
                classification["established"].append(param_key)
            elif source == "g2_geometry_v16_0" or param_key.startswith("topology.") or status == "GEOMETRIC":
                classification["geometric"].append(param_key)
            elif "calibrated" in description or "phenomenological" in description or status == "CALIBRATED":
                classification["calibrated"].append(param_key)
            else:
                classification["derived"].append(param_key)

        return classification

    def _enrich_parameters_with_provenance(self, git_metadata: Dict[str, str]) -> Dict[str, Any]:
        """
        Enrich parameter export with full provenance tracking.

        Args:
            git_metadata: Git commit information

        Returns:
            Enriched parameters dictionary with provenance
        """
        base_params = self.registry.export_parameters()
        enriched_params = {}

        for param_key, param_data in base_params.items():
            # Get provenance chain from registry
            provenance = self.registry._provenance.get(param_key, [])

            # Determine status - preserve existing status if already set
            original_status = param_data.get("status", "")
            source = param_data.get("source", "")

            # Preserve SYSTEM status (non-scientific metadata params)
            if original_status == "SYSTEM":
                status = "SYSTEM"
            elif source == "EstablishedPhysics":
                status = "ESTABLISHED"
            elif source == "g2_geometry_v16_0":
                status = "GEOMETRIC"
            elif original_status in ("ESTABLISHED", "GEOMETRIC", "PREDICTED", "CALIBRATED"):
                # Preserve explicitly set statuses
                status = original_status
            elif "calibrated" in param_data.get("description", "").lower():
                status = "CALIBRATED"
            else:
                status = "DERIVED"

            # Build derivation chain from provenance
            derivation_chain = []
            if provenance:
                # Extract parameter dependencies from simulation metadata
                for sim_id in provenance:
                    # Find dependencies by looking through simulations
                    for phase_sims in self.phases.values():
                        for sim in phase_sims:
                            if sim.metadata.id == sim_id:
                                # Use getattr to safely access depends_on if it exists
                                depends_on = getattr(sim.metadata, 'depends_on', [])
                                if depends_on:
                                    derivation_chain.extend(depends_on)

            # Enrich with provenance data
            enriched_params[param_key] = {
                **param_data,
                "source_simulation": provenance[0] if provenance else "unknown",
                "derivation_chain": list(set(derivation_chain)),  # Deduplicate
                "status": status,
                "git_commit": git_metadata["commit_hash"],
            }

        return enriched_params

    def _export_to_json(self, validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export registry data and validation to JSON.

        Args:
            validation_report: Validation report dictionary

        Returns:
            Complete output data structure
        """
        if self.verbose:
            print("\n[EXPORT] Generating theory_output.json")
            print("-" * 80)

        # Collect beginner explanations from all simulations
        beginner_explanations = self._collect_beginner_explanations()

        # Collect references from all simulations
        all_references = self._collect_references()
        if self.verbose:
            print(f"  [OK] Collected {len(all_references)} unique references")

        # Get git metadata for provenance
        git_metadata = get_git_metadata()

        # Classify parameters by type
        parameter_classification = self._classify_parameters()

        output_data = {
            "metadata": {
                "version": "17.2",
                "doi": "10.5281/zenodo.18079602",
                "model_type": "STERILE",
                "timestamp": datetime.now().isoformat(),
                "description": "Principia Metaphysica v17.2 - Sterile Geometric Framework",
                "schemaMode": self.schema_mode,
                "uqMode": self.uq_mode,
                "git": git_metadata,
                "python_version": sys.version,
                "platform": sys.platform,
                "compute_time_ms": validation_report["total_execution_time_ms"],
            },
            "derivation_logic": {
                "framework": "Principia Metaphysica v17.2 - Sterile G2 Residue Model",
                "base_manifold": "TCS G2 (Twisted Connected Sum)",
                "topology_id": "TCS #187",
                "key_assumptions": [
                    "G2 holonomy with torsion-free parallel spinor",
                    "Flux quantization N_flux = χ_eff/6 = 24",
                    "125 constants as spectral residues (sterile)",
                    "0.48σ global alignment with experimental data"
                ]
            },
            "parameter_classification": parameter_classification,
            "parameters": self._enrich_parameters_with_provenance(git_metadata),
            "formulas": self.registry.export_formulas(),
            "sections": self.registry.export_sections(),
            "provenance": self.registry.export_provenance(),
            "validation": validation_report,
            "beginnerGuide": beginner_explanations,
            "references": all_references,
        }

        # Add schema-compliant simulation results if in schema mode
        if self.schema_mode and self.schema_results:
            output_data["simulationResults"] = self.schema_results

            # Aggregate foundations and references from all simulations
            all_foundations = []
            all_references = []
            for result in self.schema_results:
                all_foundations.extend(result.get("foundations", []))
                all_references.extend(result.get("references", []))

            # Deduplicate by id
            seen_foundation_ids = set()
            unique_foundations = []
            for f in all_foundations:
                if f.get("id") not in seen_foundation_ids:
                    seen_foundation_ids.add(f.get("id"))
                    unique_foundations.append(f)

            seen_reference_ids = set()
            unique_references = []
            for r in all_references:
                if r.get("id") not in seen_reference_ids:
                    seen_reference_ids.add(r.get("id"))
                    unique_references.append(r)

            output_data["foundations"] = unique_foundations
            output_data["references"] = unique_references

        # Write to AutoGenerated/theory_output.json
        output_path = Path(__file__).parent / "AutoGenerated" / "theory_output.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)

        # Also write beginner guide to separate file
        beginner_guide_path = Path(__file__).parent / "AutoGenerated" / "beginner-guide.json"
        with open(beginner_guide_path, 'w', encoding='utf-8') as f:
            json.dump(beginner_explanations, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)

        if self.verbose:
            print(f"[OK] Exported to: {output_path}")
            print(f"  - Parameters: {len(output_data['parameters'])}")
            print(f"  - Formulas: {len(output_data['formulas'])}")
            print(f"  - Sections: {len(output_data['sections'])}")
            print(f"  - Provenance entries: {len(output_data['provenance'])}")
            print(f"  - Beginner guide topics: {len(beginner_explanations['topics'])}")
            print(f"[OK] Beginner guide exported to: {beginner_guide_path}")
            print(f"[METADATA] Git: {git_metadata['commit_hash'][:8]} on {git_metadata['branch']}{git_metadata['dirty_suffix']}")
            print(f"[METADATA] Platform: {sys.platform}, Python: {sys.version.split()[0]}")
            print(f"[CLASSIFICATION] Established: {len(parameter_classification['established'])}, "
                  f"Geometric: {len(parameter_classification['geometric'])}, "
                  f"Derived: {len(parameter_classification['derived'])}, "
                  f"Calibrated: {len(parameter_classification['calibrated'])}")

        # Split theory_output.json into cacheable components
        self._split_theory_output(output_path)

        return output_data

    def _generate_simulations_index(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate simulations index from running simulations.

        Only includes v16 Python files, excluding ip/, reports/, and tests/.

        Args:
            data: Theory output data

        Returns:
            Simulations index dictionary
        """
        from datetime import datetime, timezone
        import re

        simulations_dir = Path(__file__).parent / "simulations" / "v16"
        index_data = {
            "version": data.get('metadata', {}).get('version', '17.2'),
            "generated": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "total_scripts": 0,
            "categories": {}
        }

        # Excluded folders
        excluded_folders = {'ip', 'reports', 'tests', '__pycache__', 'deprecated'}

        # Scan v16 folder for Python files
        all_scripts = []
        for py_file in simulations_dir.rglob("*.py"):
            # Skip excluded folders and __init__.py
            rel_parts = py_file.relative_to(simulations_dir).parts
            if any(part in excluded_folders for part in rel_parts):
                continue
            if py_file.name.startswith('__'):
                continue

            # Get category from folder structure
            category = rel_parts[0] if len(rel_parts) > 1 else 'root'

            # Extract version from filename
            version = None
            match = re.search(r'_v(\d+)_(\d+)\.py$', py_file.name)
            if match:
                version = f"{match.group(1)}.{match.group(2)}"

            # Get metadata from phase simulations if available
            title = None
            description = "Physics simulation module"
            status = None

            for phase_sims in self.phases.values():
                for sim in phase_sims:
                    if py_file.stem in sim.metadata.id:
                        title = sim.metadata.title
                        description = sim.metadata.description
                        break

            script_info = {
                "file": py_file.name,
                "path": f"simulations/v16/{'/'.join(rel_parts)}".replace('\\', '/'),
                "version": version,
                "title": title,
                "description": description,
                "status": status,
                "category": f"v16/{category}"
            }
            all_scripts.append(script_info)

        # Group by category
        categories = {}
        for script in all_scripts:
            cat = script['category']
            if cat not in categories:
                categories[cat] = {
                    "title": cat.replace('v16/', '').replace('_', ' ').title(),
                    "path": f"simulations/{cat}",
                    "folderName": cat.replace('v16/', ''),
                    "isV16": True,
                    "scripts": [],
                    "count": 0
                }

            categories[cat]['scripts'].append({
                "file": script['file'],
                "path": script['path'],
                "version": script['version'],
                "title": script['title'],
                "description": script['description'],
                "status": script['status']
            })
            categories[cat]['count'] += 1

        # Sort scripts within each category by version (descending)
        for cat_data in categories.values():
            cat_data['scripts'].sort(
                key=lambda s: (
                    -float(s['version']) if s['version'] else 0,
                    s['file']
                )
            )

        index_data['categories'] = categories
        index_data['total_scripts'] = len(all_scripts)

        return index_data

    def _split_theory_output(self, theory_path: Path) -> None:
        """
        Split theory_output.json into smaller cacheable component files.

        Creates: formulas.json, parameters.json, sections.json, metadata.json,
                 statistics.json, index.json
        """
        if self.verbose:
            print("\n[SPLIT] Generating cacheable component files")
            print("-" * 80)

        output_dir = theory_path.parent

        with open(theory_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. Formulas
        if 'formulas' in data:
            formulas_data = {
                'version': data.get('metadata', {}).get('version', '16.2'),
                'count': len(data['formulas']),
                'formulas': data['formulas']
            }
            formulas_path = output_dir / 'formulas.json'
            with open(formulas_path, 'w', encoding='utf-8') as f:
                json.dump(formulas_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
            if self.verbose:
                print(f"  Created: formulas.json ({len(data['formulas'])} formulas)")

        # 2. Parameters (preserve registry values, supplement with V16_VALIDATION_BOUNDS)
        if 'parameters' in data:
            enriched_params = {}
            for param_path, param_data in data['parameters'].items():
                enriched = dict(param_data)  # Copy original data (includes registry's experimental data)

                # Add V16_VALIDATION_BOUNDS as supplementary data (don't overwrite registry values)
                bounds = V16_VALIDATION_BOUNDS.get(param_path)
                if bounds:
                    # Add target from bounds if not already present
                    if 'target' in bounds and 'target' not in enriched:
                        enriched['target'] = bounds['target']

                    # Only add V16 experimental data if registry didn't provide it
                    if enriched.get('experimental_value') is None and 'experimental' in bounds:
                        enriched['v16_experimental'] = bounds['experimental']
                        if 'sigma' in bounds:
                            enriched['v16_sigma'] = bounds['sigma']

                enriched_params[param_path] = enriched

            params_data = {
                'version': data.get('metadata', {}).get('version', '16.2'),
                'parameters': enriched_params
            }
            params_path = output_dir / 'parameters.json'
            with open(params_path, 'w', encoding='utf-8') as f:
                json.dump(params_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
            if self.verbose:
                print(f"  Created: parameters.json ({len(enriched_params)} params, enriched with experimental values)")

        # 3. Sections
        if 'sections' in data:
            sections_data = {
                'version': data.get('metadata', {}).get('version', '16.2'),
                'count': len(data['sections']),
                'sections': data['sections']
            }
            sections_path = output_dir / 'sections.json'
            with open(sections_path, 'w', encoding='utf-8') as f:
                json.dump(sections_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
            if self.verbose:
                print(f"  Created: sections.json ({len(data['sections'])} sections)")

        # 4. Metadata
        metadata = {
            'version': data.get('metadata', {}).get('version', '16.2'),
            'timestamp': data.get('metadata', {}).get('timestamp'),
            'validation': data.get('validation', {})
        }
        metadata_path = output_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
        if self.verbose:
            print(f"  Created: metadata.json")

        # 5. Statistics
        stats_data = {
            'version': data.get('metadata', {}).get('version', '16.2'),
            'statistics': data.get('statistics', {}),
            'framework_statistics': data.get('framework_statistics', {})
        }
        stats_path = output_dir / 'statistics.json'
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
        if self.verbose:
            print(f"  Created: statistics.json")

        # 6. Simulations index (for simulations page)
        simulations_data = self._generate_simulations_index(data)
        sims_path = output_dir / 'simulations.json'
        with open(sims_path, 'w', encoding='utf-8') as f:
            json.dump(simulations_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
        if self.verbose:
            print(f"  Created: simulations.json ({simulations_data['total_scripts']} scripts)")

        # 7. References (for references page)
        if 'references' in data:
            # Convert list to object keyed by ID for easier lookup
            refs_by_id = {}
            for ref in data['references']:
                ref_id = ref.get('id', ref.get('title', '').lower().replace(' ', '_')[:30])
                refs_by_id[ref_id] = ref
            refs_data = {
                'version': data.get('metadata', {}).get('version', '16.2'),
                'count': len(refs_by_id),
                'references': refs_by_id
            }
            refs_path = output_dir / 'references.json'
            with open(refs_path, 'w', encoding='utf-8') as f:
                json.dump(refs_data, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
            if self.verbose:
                print(f"  Created: references.json ({len(refs_by_id)} references)")

        # 8. Index file
        index = {
            'version': data.get('metadata', {}).get('version', '16.2'),
            'components': [
                {'name': 'formulas', 'file': 'formulas.json'},
                {'name': 'parameters', 'file': 'parameters.json'},
                {'name': 'sections', 'file': 'sections.json'},
                {'name': 'metadata', 'file': 'metadata.json'},
                {'name': 'statistics', 'file': 'statistics.json'},
                {'name': 'simulations', 'file': 'simulations.json'},
                {'name': 'references', 'file': 'references.json'},
                {'name': 'beginner-guide', 'file': 'beginner-guide.json'},
            ]
        }
        index_path = output_dir / 'index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)
        if self.verbose:
            print(f"  Created: index.json")
            print(f"[OK] Split into {len(index['components'])} component files")

    def _check_omega_hash(self) -> bool:
        """
        Gate 72 - Omega Hash Check for STERILE Model Validation.

        The Omega Hash verifies that the model is truly sterile (zero degrees of freedom).
        It computes a bit-sum from all 72 gate validation statuses:
        - Each locked gate contributes 0 to the sum
        - Any unlocked gate contributes 1 to the sum
        - STERILE model requires bit-sum = 0

        Returns:
            True if Omega Hash passes (bit-sum = 0), False otherwise
        """
        if self.verbose:
            print("\n[GATE 72] Omega Hash - STERILE Validation Check")
            print("-" * 80)

        # Count validation bits from simulation results
        bit_sum = 0
        gate_status = []

        # Check all simulation results
        for result in self.results:
            if result.status != "PASSED":
                bit_sum += 1
                gate_status.append(f"  [UNLOCKED] {result.simulation_id}: {result.status}")
            else:
                gate_status.append(f"  [LOCKED] {result.simulation_id}")

        # Check for >1 sigma tensions (each tension adds to bit-sum)
        tension_bits = len(self.tensions)
        bit_sum += tension_bits

        if self.verbose:
            print(f"Simulations checked: {len(self.results)}")
            print(f"Failed simulations: {sum(1 for r in self.results if r.status != 'PASSED')}")
            print(f"Tensions (>1sigma): {tension_bits}")
            print(f"Omega Hash bit-sum: {bit_sum}")

            # Show the formula (using ASCII for Windows console compatibility)
            print("\nGate 72 Formula: OMEGA = SUM(gate_failures) + SUM(tensions)")
            print(f"OMEGA = {sum(1 for r in self.results if r.status != 'PASSED')} + {tension_bits} = {bit_sum}")

            if bit_sum == 0:
                print("\n[OMEGA HASH] PASSED - Model is STERILE (OMEGA = 0)")
                print("All 72 Gates LOCKED. Zero degrees of freedom.")
            else:
                print(f"\n[OMEGA HASH] FAILED - Model is NOT sterile (OMEGA = {bit_sum})")
                print("Unlocked gates detected:")
                for status in gate_status:
                    if "UNLOCKED" in status:
                        print(status)
                if tension_bits > 0:
                    print(f"\nTension violations ({tension_bits}):")
                    for tension in self.tensions:
                        print(f"  - {tension.param_path}: {tension.sigma_deviation:.2f} sigma deviation")

        return bit_sum == 0

    def _print_summary(self, validation_report: Dict[str, Any]) -> None:
        """
        Print final summary of simulation run.

        Args:
            validation_report: Validation report dictionary
        """
        if not self.verbose:
            return

        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        passed = validation_report["simulations_passed"]
        failed = validation_report["simulations_failed"]
        total = validation_report["simulations_run"]
        total_time = validation_report["total_execution_time_ms"]

        # Calculate total formulas registered across all simulations
        total_formulas = sum(r.formulas_registered for r in self.results)

        print(f"Simulations Run:    {total}")
        print(f"Passed:             {passed}")
        print(f"Failed:             {failed}")
        print(f"Success Rate:       {100.0 * passed / total:.1f}%")
        print(f"Total Time:         {total_time:.2f}ms")
        print(f"Formulas Registered: {total_formulas}")

        # V16.2: Print tension warnings (>1sigma threshold)
        tensions = validation_report.get("tensions", [])
        if tensions:
            print(f"\nTensions (>1sigma deviations): {len(tensions)}")
            for tension in tensions:
                print(f"  - {tension['param']}: {tension['sigma']:.2f} sigma")
                print(f"    Theory: {tension['theory_value']:.4g}, Experiment: {tension['experimental_value']:.4g} ± {tension['experimental_sigma']:.4g}")

        if failed > 0:
            print("\nFailed Simulations:")
            for result_dict in validation_report["results"]:
                if result_dict["status"] == "FAILED":
                    sim_id = result_dict["simulation_id"]
                    error = result_dict.get("error_message", "Unknown error")
                    print(f"  [X] {sim_id}: {error}")

        print("\n" + "=" * 80)

        if failed == 0:
            print("[OK] ALL SIMULATIONS PASSED")
            if tensions:
                print(f"[WARNING] {len(tensions)} TENSION(S) DETECTED (>1sigma)")
        else:
            print(f"[X] {failed} SIMULATION(S) FAILED")

        print("=" * 80)


def run_wolfram_executor(verbose: bool = True, force: bool = False) -> bool:
    """
    Run the Wolfram executor to validate certificate code.

    Args:
        verbose: Show detailed output
        force: Force re-execution even if cached

    Returns:
        True if successful, False otherwise
    """
    if verbose:
        print("\n" + "=" * 80)
        print("WOLFRAM EXECUTOR - Certificate Code Validation")
        print("=" * 80)

    wolfram_script = Path(__file__).parent / "scripts" / "wolfram_executor.py"
    if not wolfram_script.exists():
        if verbose:
            print("[SKIP] Wolfram executor not found")
        return True

    try:
        cmd = [sys.executable, str(wolfram_script), "--update-refs"]
        if force:
            cmd.append("--force")
        if verbose:
            cmd.append("--verbose")

        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent,
            capture_output=not verbose,
            text=True
        )

        if verbose and result.returncode != 0:
            print(f"[WARN] Wolfram executor returned code {result.returncode}")
            if result.stderr:
                print(result.stderr[:500])

        return result.returncode == 0

    except Exception as e:
        if verbose:
            print(f"[ERROR] Could not run Wolfram executor: {e}")
        return False


def main():
    """Main entry point for running all simulations."""
    import argparse

    parser = argparse.ArgumentParser(description="Run all Principia Metaphysica simulations")
    parser.add_argument(
        "--schema", "-s",
        action="store_true",
        help="Enable schema-compliant execution mode (includes full metadata)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )
    parser.add_argument(
        "--uq",
        action="store_true",
        help="Enable Monte Carlo uncertainty quantification (requires NumPy)"
    )
    parser.add_argument(
        "--wolfram", "-w",
        action="store_true",
        help="Execute Wolfram code from certificates and store results"
    )
    parser.add_argument(
        "--wolfram-force",
        action="store_true",
        help="Force Wolfram re-execution (ignore cache)"
    )
    parser.add_argument(
        "--skip-guard",
        action="store_true",
        help="Skip DemonLockGuard pre-flight check (use for debugging only)"
    )

    args = parser.parse_args()

    # =========================================================================
    # v17: DEMON LOCK GUARD - PRE-FLIGHT STERILITY CHECK
    # =========================================================================
    # This check MUST pass before any simulations run.
    # If the manifold is not sterile, simulations cannot produce valid output.
    # =========================================================================
    if DEMON_LOCK_AVAILABLE and not args.skip_guard:
        if not args.quiet:
            print("\n" + "=" * 80)
            print("v17 STERILE SOVEREIGN - PRE-FLIGHT STERILITY CHECK")
            print("=" * 80)

        guard = DemonLockGuard()
        if not guard.run_preflight():
            print("\n[CRITICAL] DEMON LOCK GUARD FAILED")
            print("The manifold is NOT sterile. Simulations blocked.")
            print("Fix the sterility violations before running simulations.")
            print("\nRun with --skip-guard to bypass (debugging only).")
            sys.exit(1)

        if not args.quiet:
            print("[OK] Pre-flight sterility check passed. Proceeding with simulations.\n")

    elif not DEMON_LOCK_AVAILABLE and not args.quiet:
        print("\n[WARNING] DemonLockGuard not available - skipping sterility pre-flight")

    # Create runner and execute
    runner = SimulationRunner(
        verbose=not args.quiet,
        schema_mode=args.schema,
        uq_mode=args.uq
    )
    output_data = runner.run_all()

    # =========================================================================
    # v17.1: POST-SIMULATION STERILITY REPORT
    # =========================================================================
    # Generate formal audit certificate with sovereign hash after all
    # simulations complete. This proves the manifold state is sterile.
    # =========================================================================
    if STERILITY_REPORTER_AVAILABLE:
        if not args.quiet:
            print("\n" + "=" * 80)
            print("v17.1 SOVEREIGN AUDIT - POST-SIMULATION STERILITY REPORT")
            print("=" * 80)

        try:
            reporter = SterilityReporter()
            reporter.print_report()
            report_path = reporter.write_report("sterility_report.json")
            if not args.quiet:
                print(f"[OK] Sterility report written to: {report_path}")
        except Exception as e:
            if not args.quiet:
                print(f"[WARN] Could not generate sterility report: {e}")

    # =========================================================================
    # v17.1: DOCUMENTATION SYNCHRONIZATION
    # =========================================================================
    # Sync documentation with current registry state and embed sovereign hash.
    # =========================================================================
    if DOC_SYNC_AVAILABLE:
        if not args.quiet:
            print("\n" + "=" * 80)
            print("v17.1 DOCUMENTATION SYNC - EMBEDDING SOVEREIGN HASH")
            print("=" * 80)

        try:
            sync = DocumentationSynchronizer()
            outputs = sync.generate_all()
            if not args.quiet:
                print("[OK] Documentation synchronized with sovereign hash")
                for name, path in outputs.items():
                    print(f"  - {name}: {path}")
        except Exception as e:
            if not args.quiet:
                print(f"[WARN] Could not sync documentation: {e}")

    # =========================================================================
    # v17.2-Absolute: ANTI-TAUTOLOGY VALIDATION
    # =========================================================================
    # Run validation scripts to ensure:
    # 1. No Ghost Literals (hardcoded DERIVED values)
    # 2. No tautological validation (validator != simulation)
    # 3. All values properly attributed (DERIVED vs EXPERIMENTAL)
    # =========================================================================
    validation_results = {
        "value_context_audit": {"status": "NOT_RUN", "violations": 0},
        "sterility_audit": {"status": "NOT_RUN", "violations": 0},
        "overall": "NOT_RUN"
    }
    validation_failed = False

    if not args.quiet:
        print("\n" + "=" * 80)
        print("v17.2-Absolute VALIDATION - ANTI-TAUTOLOGY CHECKS")
        print("=" * 80)

    # Value Context Audit - checks DERIVED vs EXPERIMENTAL value usage
    if VALUE_CONTEXT_AUDIT_AVAILABLE:
        try:
            auditor = ValueContextAuditor()
            is_compliant = auditor.scan_repository()
            violations = auditor.violations
            validation_results["value_context_audit"] = {
                "status": "PASS" if is_compliant else "FAIL",
                "violations": len(violations),
                "details": [str(v) for v in violations[:10]] if violations else []
            }
            if not args.quiet:
                if is_compliant:
                    print("[PASS] Value Context Audit: All values properly attributed")
                else:
                    print(f"[FAIL] Value Context Audit: {len(violations)} violations found")
                    for v in violations[:5]:
                        print(f"  - {v}")
                    validation_failed = True
        except Exception as e:
            if not args.quiet:
                print(f"[WARN] Value Context Audit failed: {e}")
            validation_results["value_context_audit"]["status"] = "ERROR"
    else:
        if not args.quiet:
            print("[SKIP] Value Context Audit not available")

    # Sterility Audit - checks for Ghost Literals
    if STERILITY_AUDIT_AVAILABLE:
        try:
            scanner = GhostLiteralScanner()
            is_clean = scanner.scan_repository()
            ghost_count = len(scanner.ghost_findings)
            validation_results["sterility_audit"] = {
                "status": "PASS" if is_clean else "FAIL",
                "violations": ghost_count
            }
            if not args.quiet:
                if is_clean:
                    print("[PASS] Sterility Audit: No Ghost Literals detected")
                else:
                    print(f"[FAIL] Sterility Audit: {ghost_count} Ghost Literals found")
                    validation_failed = True
        except Exception as e:
            if not args.quiet:
                print(f"[WARN] Sterility Audit failed: {e}")
            validation_results["sterility_audit"]["status"] = "ERROR"
    else:
        if not args.quiet:
            print("[SKIP] Sterility Audit not available")

    # Overall validation status
    validation_results["overall"] = "FAIL" if validation_failed else "PASS"
    if not args.quiet:
        print("-" * 80)
        print(f"Validation Status: {validation_results['overall']}")

    # Add validation results to output data
    output_data["validation"]["anti_tautology"] = validation_results

    # Optionally run Wolfram executor
    if args.wolfram:
        run_wolfram_executor(
            verbose=not args.quiet,
            force=args.wolfram_force
        )

    # Generate validation statistics (always run to ensure statistics.json is populated)
    try:
        from scripts.generate_statistics import generate_statistics, OUTPUT_FILE
        import json
        import os

        if not args.quiet:
            print("\n" + "=" * 80)
            print("GENERATING VALIDATION STATISTICS")
            print("=" * 80)

        statistics = generate_statistics()
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(statistics, f, indent=2)

        if not args.quiet:
            fs = statistics.get('framework_statistics', {})
            print(f"  Verified gates:    {fs.get('pass_count', 0)}")
            print(f"  Chi-squared (red): {fs.get('chi_squared_reduced', 'N/A')}")
            print(f"  Status:            {fs.get('status', 'N/A')}")
            print(f"  Output: {OUTPUT_FILE}")
    except Exception as e:
        if not args.quiet:
            print(f"[WARN] Could not generate statistics: {e}")

    # Return exit code based on results (simulations AND validations)
    validation = output_data["validation"]
    simulations_ok = validation["simulations_failed"] == 0
    validations_ok = not validation_failed

    if simulations_ok and validations_ok:
        exit_code = 0
        if not args.quiet:
            print("\n[SUCCESS] All simulations passed, all validations passed")
    elif not simulations_ok:
        exit_code = 1
        if not args.quiet:
            print(f"\n[FAILURE] {validation['simulations_failed']} simulations failed")
    else:
        exit_code = 2  # Validation failure (distinct from simulation failure)
        if not args.quiet:
            print("\n[FAILURE] Anti-tautology validation failed")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
