#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v15.3 - Photosynthetic Quantum Coherence Threshold Model
===============================================================================

SPECULATIVE APPENDIX MATERIAL - Open Problem for Future Work

This simulation explores a hypothetical coupling between PM's G2 moduli sampling
and vibronic quantum coherence in photosynthetic light-harvesting complexes
(FMO in bacteria, LHCII in plants/algae).

KEY INSIGHT: Biology works ABOVE minimum coherence thresholds for robust function.
Evolution optimizes for reliable operation in variable environments, not razor peaks.

CORE ASSUMPTIONS (Literature-Based):
    1. Coherence times: 300-700 fs at physiological temperature (FMO/LHCII)
    2. Energy transfer efficiency: 95-99% (near-unity via ENAQT)
    3. Vibronic (mixed electronic-vibrational) quantum effects
    4. Noise-assisted transport (ENAQT regime) robust across conditions

NUMERICAL PREDICTIONS (Testable Limits):
    - coherence_min: 100 fs (below = classical transport dominates)
    - coherence_max: 700 fs (observed upper in FMO at room temp)
    - efficiency_threshold: 0.80 (below = evolutionary disadvantage)
    - viable_plateau: |phi - 0.5| < 0.25 (50% of sampling range)

STATUS: Highly speculative - no direct evidence connects extra-D moduli
        to photosynthetic quantum effects. Offered as open problem.

REFERENCES:
    - Engel et al. (2007) Nature - FMO coherence discovery
    - Cao et al. (2020) Science Advances - Quantum biology review
    - PM racetrack stabilization (v15.0)

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os
from typing import Dict, Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import FluxQuantization
    B3 = FluxQuantization.B3
    CONFIG_LOADED = True
except ImportError:
    B3 = 24
    CONFIG_LOADED = False


class PhotosyntheticThresholdModel:
    """
    Rigorous threshold-based model for photosynthetic coherence coupling to PM vacuum.

    Core principle: Biology requires passing thresholds for function.
    Photosynthetic quantum effects are viable across a broad parameter range.
    """

    # ==========================================================================
    # NUMERICAL PREDICTIONS - Testable Limits
    # ==========================================================================
    NUMERICAL_LIMITS = {
        # Coherence time bounds (from quantum biology literature)
        'coherence_min_fs': 100.0,       # Below: classical dominates
        'coherence_fmo_fs': 500.0,       # FMO typical at room temp
        'coherence_max_fs': 700.0,       # Observed upper bound

        # Energy transfer efficiency bounds
        'efficiency_threshold': 0.80,    # Minimum for evolutionary advantage
        'efficiency_fmo': 0.95,          # FMO observed
        'efficiency_lhcii': 0.99,        # LHCII near-unity

        # Temperature regime
        'temp_physiological_K': 300.0,   # Room temperature operation
        'temp_min_viable_K': 270.0,      # Lower functional limit
        'temp_max_viable_K': 320.0,      # Upper functional limit

        # Plateau parameters
        'plateau_halfwidth': 0.25,       # Viable zone +/- 0.25
        'coherence_mod_depth': 0.20,     # Max coherence variation
    }

    # ==========================================================================
    # THRESHOLD PARAMETERS (Recommended Starting Point)
    # ==========================================================================
    THRESHOLD_PARAMS = {
        'coherence_base_fs': 500.0,      # Nominal FMO value
        'efficiency_base': 0.95,         # Nominal efficiency
        'sampling_position': 0.5,        # Racetrack minimum
        'plateau_halfwidth': 0.25,       # Viable zone
        'coherence_mod_depth': 0.20,     # Modulation depth
    }

    def __init__(self,
                 coherence_base_fs: float = None,
                 efficiency_base: float = None,
                 sampling_position: float = None,
                 plateau_halfwidth: float = None,
                 coherence_mod_depth: float = None):
        """
        Initialize photosynthetic threshold model.

        Args:
            coherence_base_fs: Base coherence time in femtoseconds
            efficiency_base: Base energy transfer efficiency [0, 1]
            sampling_position: PM modulus coordinate [0, 1]
            plateau_halfwidth: Half-width of viable plateau
            coherence_mod_depth: Maximum coherence modulation
        """
        self.coh_base = coherence_base_fs if coherence_base_fs is not None else self.THRESHOLD_PARAMS['coherence_base_fs']
        self.eff_base = efficiency_base if efficiency_base is not None else self.THRESHOLD_PARAMS['efficiency_base']
        self.pos = np.clip(
            sampling_position if sampling_position is not None else self.THRESHOLD_PARAMS['sampling_position'],
            0.0, 1.0
        )
        self.hw = plateau_halfwidth if plateau_halfwidth is not None else self.THRESHOLD_PARAMS['plateau_halfwidth']
        self.depth = coherence_mod_depth if coherence_mod_depth is not None else self.THRESHOLD_PARAMS['coherence_mod_depth']

    # ==========================================================================
    # CORE PHYSICS
    # ==========================================================================

    def viability_factor(self) -> float:
        """
        Compute viability factor f(phi) - broad plateau for robust function.

        f(phi) = 1.0                             for |phi - 0.5| <= hw
               = exp(-(|phi-0.5| - hw)^2/0.15^2)  otherwise

        Returns:
            Viability factor in [0, 1]
        """
        deviation = abs(self.pos - 0.5)
        if deviation <= self.hw:
            return 1.0  # Full viability within plateau
        else:
            # Gentle falloff outside plateau
            return np.exp(-((deviation - self.hw)**2) / (0.15**2))

    def effective_coherence_time(self) -> float:
        """
        Effective vibronic coherence time modulated by vacuum position.

        T_coh_eff = T_coh_base * (1 - depth * (1 - f(phi)))

        In viable plateau: full coherence
        At sector edges: reduced by up to depth fraction

        Returns:
            Coherence time in femtoseconds
        """
        f = self.viability_factor()
        return self.coh_base * (1.0 - self.depth * (1.0 - f))

    def effective_efficiency(self) -> float:
        """
        Effective energy transfer efficiency.

        eta_eff = eta_base + (1 - eta_base) * f(phi)

        Maximum efficiency (near 1.0) at plateau center.

        Returns:
            Efficiency in [0, 1]
        """
        f = self.viability_factor()
        # Efficiency boosted toward 1.0 in viable region
        return self.eff_base + (1.0 - self.eff_base) * f

    def enaqt_quality(self) -> float:
        """
        ENAQT (Environment-Assisted Quantum Transport) quality factor.

        Measures how well the system operates in the noise-assisted regime.
        Q = sqrt(coherence_ratio * efficiency_ratio)

        Returns:
            Quality factor in [0, 1]
        """
        coh_ratio = self.effective_coherence_time() / self.coh_base
        eff_ratio = self.effective_efficiency() / 1.0  # Normalized to unity
        return np.sqrt(coh_ratio * eff_ratio)

    # ==========================================================================
    # THRESHOLD VALIDATION
    # ==========================================================================

    def is_above_threshold(self) -> Tuple[bool, Dict]:
        """
        Check if system passes minimum thresholds for photosynthetic function.

        Returns:
            (passes_threshold, details)
        """
        coh_eff = self.effective_coherence_time()
        eff = self.effective_efficiency()

        limits = self.NUMERICAL_LIMITS

        # Check individual thresholds
        coh_above_min = coh_eff >= limits['coherence_min_fs']
        coh_in_range = limits['coherence_min_fs'] <= coh_eff <= limits['coherence_max_fs']
        eff_above_threshold = eff >= limits['efficiency_threshold']
        in_plateau = abs(self.pos - 0.5) <= self.hw

        passes = coh_above_min and eff_above_threshold

        details = {
            'coherence_fs': coh_eff,
            'coherence_above_min': coh_above_min,
            'coherence_in_range': coh_in_range,
            'coherence_bounds': (limits['coherence_min_fs'], limits['coherence_max_fs']),
            'efficiency': eff,
            'efficiency_above_threshold': eff_above_threshold,
            'efficiency_threshold': limits['efficiency_threshold'],
            'position': self.pos,
            'in_plateau': in_plateau,
            'plateau_bounds': (0.5 - self.hw, 0.5 + self.hw),
            'enaqt_quality': self.enaqt_quality(),
            'passes_all': passes
        }

        return passes, details

    # ==========================================================================
    # ANALYSIS
    # ==========================================================================

    def run_analysis(self, verbose: bool = True) -> Dict:
        """
        Run complete photosynthetic threshold analysis.

        Returns:
            Comprehensive results dictionary
        """
        # Core quantities
        coh_eff = self.effective_coherence_time()
        eff = self.effective_efficiency()
        viability = self.viability_factor()
        enaqt = self.enaqt_quality()

        # Threshold check
        passes, threshold_details = self.is_above_threshold()

        results = {
            'input_parameters': {
                'coherence_base_fs': float(self.coh_base),
                'efficiency_base': float(self.eff_base),
                'sampling_position': float(self.pos),
                'plateau_halfwidth': float(self.hw),
                'coherence_mod_depth': float(self.depth),
                'config_loaded': CONFIG_LOADED
            },
            'physical_quantities': {
                'effective_coherence_fs': float(coh_eff),
                'effective_efficiency': float(eff),
                'enaqt_quality': float(enaqt)
            },
            'viability': {
                'viability_factor': float(viability),
                'in_plateau': threshold_details['in_plateau'],
                'plateau_bounds': threshold_details['plateau_bounds']
            },
            'threshold_validation': {
                'passes_all_thresholds': passes,
                'coherence_above_min': threshold_details['coherence_above_min'],
                'coherence_bounds_fs': threshold_details['coherence_bounds'],
                'efficiency_above_threshold': threshold_details['efficiency_above_threshold'],
                'efficiency_threshold': threshold_details['efficiency_threshold']
            },
            'numerical_predictions': self.NUMERICAL_LIMITS.copy(),
            'interpretation': {
                'key_insight': 'Photosynthesis works ABOVE coherence threshold across broad range',
                'enaqt_regime': 'Noise-assisted transport robust to environmental variation',
                'testable': 'Disrupting vibronic mixing -> efficiency drop below threshold'
            },
            'status': 'SPECULATIVE - Open problem for future work',
            'overall_valid': passes,
            'version': 'v15.3'
        }

        if verbose:
            self._print_report(results)

        return results

    def _print_report(self, results: Dict):
        """Print formatted analysis report."""
        print()
        print("=" * 70)
        print(" PHOTOSYNTHETIC QUANTUM COHERENCE THRESHOLD MODEL (v15.3)")
        print("=" * 70)
        print()
        print("STATUS: Speculative appendix - open problem for future work")
        print("KEY INSIGHT: Photosynthesis works ABOVE thresholds, broadly robust")
        print()

        print("=" * 70)
        print(" NUMERICAL PREDICTIONS (Testable Limits)")
        print("=" * 70)
        limits = results['numerical_predictions']
        print(f"  coherence_min:        {limits['coherence_min_fs']:.0f} fs (classical limit)")
        print(f"  coherence_fmo:        {limits['coherence_fmo_fs']:.0f} fs (FMO typical)")
        print(f"  coherence_max:        {limits['coherence_max_fs']:.0f} fs (observed upper)")
        print(f"  efficiency_threshold: {limits['efficiency_threshold']:.2f} (evolutionary min)")
        print(f"  efficiency_fmo:       {limits['efficiency_fmo']:.2f} (FMO observed)")
        print(f"  plateau_width:        +/- {limits['plateau_halfwidth']:.2f} (viable zone)")
        print()

        print("=" * 70)
        print(" INPUT PARAMETERS")
        print("=" * 70)
        inp = results['input_parameters']
        print(f"  coherence_base:       {inp['coherence_base_fs']:.0f} fs")
        print(f"  efficiency_base:      {inp['efficiency_base']:.2f}")
        print(f"  sampling_position:    {inp['sampling_position']:.2f}")
        print(f"  plateau_halfwidth:    {inp['plateau_halfwidth']:.2f}")
        print()

        print("=" * 70)
        print(" COMPUTED QUANTITIES")
        print("=" * 70)
        phys = results['physical_quantities']
        print(f"  effective_coherence:  {phys['effective_coherence_fs']:.1f} fs")
        print(f"  effective_efficiency: {phys['effective_efficiency']:.4f}")
        print(f"  ENAQT quality:        {phys['enaqt_quality']:.4f}")
        print()

        print("=" * 70)
        print(" VIABILITY (Broad Plateau)")
        print("=" * 70)
        viab = results['viability']
        print(f"  Viability factor:     {viab['viability_factor']:.4f}")
        print(f"  In plateau:           {viab['in_plateau']}")
        print(f"  Plateau bounds:       [{viab['plateau_bounds'][0]:.2f}, {viab['plateau_bounds'][1]:.2f}]")
        print()

        print("=" * 70)
        print(" THRESHOLD VALIDATION")
        print("=" * 70)
        val = results['threshold_validation']
        status_coh = "PASS" if val['coherence_above_min'] else "FAIL"
        status_eff = "PASS" if val['efficiency_above_threshold'] else "FAIL"
        print(f"  coherence >= {val['coherence_bounds_fs'][0]:.0f} fs: {status_coh}")
        print(f"  efficiency >= {val['efficiency_threshold']:.2f}: {status_eff}")
        print()
        overall = "PASSES" if results['overall_valid'] else "FAILS"
        print(f"  Overall: {overall} threshold requirements")
        print()

        print("=" * 70)
        print(" INTERPRETATION")
        print("=" * 70)
        interp = results['interpretation']
        print(f"  {interp['key_insight']}")
        print(f"  {interp['enaqt_regime']}")
        print(f"  Testable: {interp['testable']}")
        print("=" * 70)


def scan_threshold_viability() -> Dict:
    """
    Scan viability across positions.

    Returns:
        Scan results with threshold regions
    """
    positions = np.linspace(0, 1, 101)

    coherences = []
    efficiencies = []
    passes_list = []

    for pos in positions:
        model = PhotosyntheticThresholdModel(sampling_position=pos)
        coherences.append(model.effective_coherence_time())
        efficiencies.append(model.effective_efficiency())
        p, _ = model.is_above_threshold()
        passes_list.append(p)

    return {
        'positions': positions.tolist(),
        'coherences_fs': coherences,
        'efficiencies': efficiencies,
        'passes_threshold': passes_list,
        'viable_fraction': sum(passes_list) / len(passes_list)
    }


def export_photosynthetic_results() -> Dict:
    """Export photosynthetic threshold results for integration."""
    model = PhotosyntheticThresholdModel()
    results = model.run_analysis(verbose=False)

    return {
        'COHERENCE_FS': results['physical_quantities']['effective_coherence_fs'],
        'EFFICIENCY': results['physical_quantities']['effective_efficiency'],
        'ENAQT_QUALITY': results['physical_quantities']['enaqt_quality'],
        'VIABILITY_FACTOR': results['viability']['viability_factor'],
        'IN_PLATEAU': results['viability']['in_plateau'],
        'PASSES_THRESHOLD': results['overall_valid'],
        'NUMERICAL_LIMITS': results['numerical_predictions'],
        'STATUS': 'SPECULATIVE',
        'VERSION': 'v15.3'
    }


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Run threshold analysis
    model = PhotosyntheticThresholdModel()
    model.run_analysis()

    # Show scan results
    print("\n" + "=" * 70)
    print(" THRESHOLD VIABILITY SCAN")
    print("=" * 70)
    scan = scan_threshold_viability()
    print(f"  Viable fraction: {scan['viable_fraction']*100:.1f}% of positions")
    print(f"  Peak coherence: {max(scan['coherences_fs']):.1f} fs")
    print(f"  Peak efficiency: {max(scan['efficiencies']):.4f}")
    print("=" * 70)
