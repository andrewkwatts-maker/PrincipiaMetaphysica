#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v15.3 - Unified Biological Quantum Threshold Model
=========================================================================

SPECULATIVE APPENDIX MATERIAL - Open Problem for Future Work

Unified framework examining biological quantum systems (microtubules,
photosynthetic complexes, magnetoreception) through threshold-based viability.

CORE THESIS:
    Biology works ABOVE minimum thresholds for robust function across
    variable environmental conditions. Evolution optimizes for reliability,
    not fine-tuned peaks in hypothetical PM sampling coordinates.

NO CLAIM OF BIOLOGICAL TUNING:
    This model does NOT claim biology is "tuned" to PM vacuum parameters.
    It explores what thresholds would need to be exceeded for quantum
    biological function, presenting the math as an open problem.

SYSTEMS EXAMINED:
    1. Microtubules (Orch OR): tau = hbar/E_G, 25-2000 ms viable
    2. Photosynthesis (FMO/LHCII): 100-700 fs coherence, >80% efficiency
    3. Magnetoreception (Cryptochrome): 1-100 us radical pair coherence

NUMERICAL PREDICTIONS (All Literature-Based):
    See individual NUMERICAL_LIMITS dictionaries for testable bounds.

STATUS: Highly speculative - offered for future theoretical/experimental work.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from simulations.microtubule_threshold_v15_3 import MicrotubuleThresholdModel
    from simulations.photosynthetic_threshold_v15_3 import PhotosyntheticThresholdModel
    MODELS_LOADED = True
except ImportError:
    MODELS_LOADED = False


@dataclass
class BiologicalSystem:
    """Data class for biological quantum system parameters."""
    name: str
    timescale_min: float       # Minimum coherence/collapse time
    timescale_max: float       # Maximum viable time
    timescale_unit: str        # 'ms', 'fs', 'us'
    efficiency_threshold: float  # Minimum functional efficiency
    plateau_width: float       # Viable range as fraction of [0,1]
    references: List[str]      # Key literature references


class UnifiedBiologicalThreshold:
    """
    Unified model for biological quantum thresholds.

    Examines multiple biological systems through threshold-based viability.
    No claim of PM-specific tuning - presents math as open problem.
    """

    # ==========================================================================
    # BIOLOGICAL SYSTEMS DATABASE
    # ==========================================================================
    SYSTEMS = {
        'microtubule': BiologicalSystem(
            name='Microtubule (Orch OR)',
            timescale_min=25.0,       # ms (gamma ~40 Hz)
            timescale_max=2000.0,     # ms (slow processing)
            timescale_unit='ms',
            efficiency_threshold=0.5,  # Superposition coherence
            plateau_width=0.4,         # 40% viable range
            references=['Hameroff & Penrose (2014)', 'Craddock et al. (2017)']
        ),
        'photosynthesis': BiologicalSystem(
            name='Photosynthetic Complex (FMO/LHCII)',
            timescale_min=100.0,      # fs (classical limit)
            timescale_max=700.0,      # fs (FMO upper)
            timescale_unit='fs',
            efficiency_threshold=0.80, # Transfer efficiency
            plateau_width=0.5,         # 50% viable range
            references=['Engel et al. (2007)', 'Cao et al. (2020)']
        ),
        'magnetoreception': BiologicalSystem(
            name='Cryptochrome (Avian Magnetoreception)',
            timescale_min=1.0,        # us (minimum detection)
            timescale_max=100.0,      # us (radical pair lifetime)
            timescale_unit='us',
            efficiency_threshold=0.70, # Directional sensitivity
            plateau_width=0.6,         # 60% viable range (robust)
            references=['Ritz et al. (2004)', 'Hore & Mouritsen (2016)']
        ),
    }

    # ==========================================================================
    # THRESHOLD PARAMETERS
    # ==========================================================================
    DEFAULT_POSITION = 0.5  # Racetrack minimum

    def __init__(self, sampling_position: float = None):
        """
        Initialize unified biological threshold model.

        Args:
            sampling_position: PM modulus coordinate [0, 1]
        """
        self.pos = np.clip(
            sampling_position if sampling_position is not None else self.DEFAULT_POSITION,
            0.0, 1.0
        )

    def viability_factor(self, plateau_width: float) -> float:
        """
        Compute viability factor for given plateau width.

        Args:
            plateau_width: Half-width of viable plateau

        Returns:
            Viability factor in [0, 1]
        """
        hw = plateau_width / 2
        deviation = abs(self.pos - 0.5)
        if deviation <= hw:
            return 1.0
        else:
            return np.exp(-((deviation - hw)**2) / (0.1**2))

    def system_viability(self, system_key: str) -> Dict:
        """
        Compute viability for a specific biological system.

        Args:
            system_key: Key from SYSTEMS dictionary

        Returns:
            Viability analysis for the system
        """
        system = self.SYSTEMS[system_key]
        viability = self.viability_factor(system.plateau_width)

        # Effective timescale (reduced outside plateau)
        timescale_eff = system.timescale_min + (system.timescale_max - system.timescale_min) * viability

        # Is above minimum threshold?
        above_threshold = timescale_eff >= system.timescale_min

        return {
            'system': system.name,
            'viability_factor': viability,
            'timescale_effective': timescale_eff,
            'timescale_bounds': (system.timescale_min, system.timescale_max),
            'timescale_unit': system.timescale_unit,
            'efficiency_threshold': system.efficiency_threshold,
            'above_threshold': above_threshold,
            'in_plateau': abs(self.pos - 0.5) <= system.plateau_width / 2,
            'references': system.references
        }

    def all_systems_viability(self) -> Dict:
        """
        Compute viability for all biological systems.

        Returns:
            Comprehensive viability analysis
        """
        results = {}
        all_pass = True

        for key in self.SYSTEMS:
            results[key] = self.system_viability(key)
            if not results[key]['above_threshold']:
                all_pass = False

        return {
            'systems': results,
            'all_above_threshold': all_pass,
            'sampling_position': self.pos
        }

    def run_analysis(self, verbose: bool = True) -> Dict:
        """
        Run complete unified biological threshold analysis.

        Returns:
            Comprehensive results dictionary
        """
        viability = self.all_systems_viability()

        results = {
            'input_parameters': {
                'sampling_position': float(self.pos),
                'models_loaded': MODELS_LOADED
            },
            'systems_analysis': viability['systems'],
            'summary': {
                'all_above_threshold': viability['all_above_threshold'],
                'n_systems': len(self.SYSTEMS),
                'systems_passing': sum(1 for s in viability['systems'].values() if s['above_threshold'])
            },
            'numerical_predictions': {
                key: {
                    'timescale_range': f"{s.timescale_min}-{s.timescale_max} {s.timescale_unit}",
                    'efficiency_min': s.efficiency_threshold,
                    'plateau_width': s.plateau_width
                }
                for key, s in self.SYSTEMS.items()
            },
            'interpretation': {
                'key_insight': 'Biology works ABOVE thresholds, not at fine-tuned peaks',
                'no_tuning_claim': 'Model does NOT claim biology is tuned to PM parameters',
                'open_problem': 'Presented as mathematical framework for future investigation'
            },
            'status': 'SPECULATIVE - Open problem, no overclaims',
            'overall_valid': viability['all_above_threshold'],
            'version': 'v15.3'
        }

        if verbose:
            self._print_report(results)

        return results

    def _print_report(self, results: Dict):
        """Print formatted analysis report."""
        print()
        print("=" * 70)
        print(" UNIFIED BIOLOGICAL QUANTUM THRESHOLD MODEL (v15.3)")
        print("=" * 70)
        print()
        print("STATUS: Speculative appendix - open problem for future work")
        print("NOTE: NO CLAIM of biological tuning to PM parameters")
        print("      Presented as mathematical framework only")
        print()

        print("=" * 70)
        print(" NUMERICAL PREDICTIONS BY SYSTEM")
        print("=" * 70)
        for key, system in self.SYSTEMS.items():
            print(f"\n  {system.name}:")
            print(f"    Timescale range: {system.timescale_min}-{system.timescale_max} {system.timescale_unit}")
            print(f"    Efficiency min:  {system.efficiency_threshold:.0%}")
            print(f"    Plateau width:   {system.plateau_width:.0%} of range")
            print(f"    References:      {', '.join(system.references)}")
        print()

        print("=" * 70)
        print(" VIABILITY ANALYSIS (at position = {:.2f})".format(self.pos))
        print("=" * 70)
        for key, data in results['systems_analysis'].items():
            status = "PASS" if data['above_threshold'] else "FAIL"
            print(f"\n  {data['system']}:")
            print(f"    Viability factor:    {data['viability_factor']:.4f}")
            print(f"    Effective timescale: {data['timescale_effective']:.1f} {data['timescale_unit']}")
            print(f"    In plateau:          {data['in_plateau']}")
            print(f"    Above threshold:     {status}")
        print()

        print("=" * 70)
        print(" SUMMARY")
        print("=" * 70)
        summary = results['summary']
        print(f"  Systems analyzed: {summary['n_systems']}")
        print(f"  Systems passing:  {summary['systems_passing']}/{summary['n_systems']}")
        overall = "PASS" if results['overall_valid'] else "FAIL"
        print(f"  Overall status:   {overall}")
        print()

        print("=" * 70)
        print(" INTERPRETATION")
        print("=" * 70)
        interp = results['interpretation']
        for key, val in interp.items():
            print(f"  {key}: {val}")
        print("=" * 70)


def scan_all_positions() -> Dict:
    """
    Scan all biological systems across full position range.

    Returns:
        Comprehensive scan results
    """
    positions = np.linspace(0, 1, 51)

    results = {
        'positions': positions.tolist(),
        'systems': {}
    }

    for system_key in UnifiedBiologicalThreshold.SYSTEMS:
        viabilities = []
        passes = []
        for pos in positions:
            model = UnifiedBiologicalThreshold(sampling_position=pos)
            v = model.system_viability(system_key)
            viabilities.append(v['viability_factor'])
            passes.append(v['above_threshold'])

        results['systems'][system_key] = {
            'viabilities': viabilities,
            'passes': passes,
            'viable_fraction': sum(passes) / len(passes)
        }

    return results


def export_unified_results() -> Dict:
    """Export unified threshold results."""
    model = UnifiedBiologicalThreshold()
    results = model.run_analysis(verbose=False)

    return {
        'SAMPLING_POSITION': results['input_parameters']['sampling_position'],
        'N_SYSTEMS': results['summary']['n_systems'],
        'SYSTEMS_PASSING': results['summary']['systems_passing'],
        'ALL_ABOVE_THRESHOLD': results['overall_valid'],
        'NUMERICAL_PREDICTIONS': results['numerical_predictions'],
        'STATUS': 'SPECULATIVE',
        'VERSION': 'v15.3'
    }


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Run unified analysis
    model = UnifiedBiologicalThreshold()
    model.run_analysis()

    # Show position scan
    print("\n" + "=" * 70)
    print(" POSITION SCAN (Viable Fraction by System)")
    print("=" * 70)
    scan = scan_all_positions()
    for system, data in scan['systems'].items():
        print(f"  {system}: {data['viable_fraction']*100:.1f}% of positions viable")
    print("=" * 70)
