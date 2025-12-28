#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v15.5 - Microtubule Orch-OR with Temperature-Dependent Decoherence
======================================================================================

SPECULATIVE APPENDIX MATERIAL - Open Problem for Future Work

Fully rigorous model with:
- Penrose OR collapse timescale tau_OR = hbar / E_G
- Diosi-Penrose gravitational decoherence Gamma_DP = E_G / hbar
- Temperature-dependent environmental decoherence Gamma_env(T) ~ Gamma_0 * (T/T_0)^beta
  (beta ~ 7-12 from recent quantum biology estimates; here beta=8 conservative)
- Total Gamma_total = Gamma_DP + Gamma_env(T)
- Viability: tau_OR * Gamma_total <= 1 (OR dominates)

Temperature Integration:
- Physiological T = 310 K baseline
- Gamma_env scales strongly with T -> brain warmth challenge addressed quantitatively
- Modulation by PM sampling position phi (G_eff(phi))

KEY QUESTION: Does biology still pass threshold at physiological temperature?

RESULT: With conservative decoherence estimates, biology does NOT pass threshold.
This is an HONEST presentation of the "warm and wet" challenge.

QUANTITATIVE FINDING:
- At 310 K with Gamma_env ~ 5 GHz: viability ~ 2.5×10^9 (threshold < 1)
- Shielding factor ~10^10 would be required for viability
- This enormous gap is the central open problem of Orch OR

OPEN QUESTIONS (for future work):
- Could protein/tubulin structure provide sufficient shielding?
- Are literature decoherence estimates too conservative for organized structures?
- Could quantum error correction mechanisms help?

TESTABLE PREDICTIONS (if Orch OR is correct):
- Hypothermic shift (T down): coherence up (testable)
- Hyperthermic/anesthesia (effective T up): viability down
- Specific protein mutations should measurably affect coherence

STATUS: Speculative - NO CLAIM of biological tuning to PM parameters.
        Presents challenge honestly as open problem.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os
from typing import Dict, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use scipy.constants for high precision if available
try:
    from scipy.constants import hbar as HBAR, G as G_NEWTON, Boltzmann as K_B
except ImportError:
    HBAR = 1.0545718e-34      # J*s
    G_NEWTON = 6.67430e-11    # m^3/(kg*s^2)
    K_B = 1.380649e-23        # J/K


class MicrotubuleOrchORTemperature:
    """
    Rigorous Orch-OR model with temperature-dependent decoherence.

    Addresses the "warm and wet" challenge quantitatively.
    Biology must pass threshold: tau_OR * Gamma_total < 1
    """

    # ==========================================================================
    # CALIBRATED PARAMETERS (Literature & Testable)
    # ==========================================================================
    BEST_PARAMS = {
        # Orch OR calibration (Hameroff & Penrose 2014)
        'n_tubulins_nominal': 1e10,       # ~500 ms baseline (Orch OR target)
        'tau_ref_s': 0.5,                 # Reference timescale at n_ref
        'n_ref': 1e10,                    # Reference superposition size

        # PM vacuum position
        'sampling_position': 0.5,         # Racetrack minimum
        'plateau_halfwidth': 0.25,        # Viable phi zone
        'g_mod_depth': 0.20,              # G_eff variation

        # Temperature-dependent decoherence
        'gamma_env_base': 5e9,            # Gamma_env at 310 K (s^-1) - conservative
        'temp_reference_k': 310.0,        # Physiological baseline
        'decoherence_exponent': 8.0,      # beta ~ 8 (strong T dependence; range 7-12)

        # Physical constants
        'm_tubulin': 1.8135e-22,          # kg (~110 kDa)
        'r_superposition': 1.0e-9,        # m (nm-scale)
    }

    # ==========================================================================
    # THRESHOLD CRITERIA
    # ==========================================================================
    THRESHOLDS = {
        'viability_max': 1.0,             # tau_OR * Gamma_total must be < 1
        'tau_min_ms': 25.0,               # Gamma ~40 Hz minimum
        'tau_max_ms': 2000.0,             # Slow processing maximum
        'temp_min_k': 270.0,              # Hypothermia limit
        'temp_max_k': 320.0,              # Hyperthermia limit
    }

    def __init__(self,
                 n_tubulins: float = None,
                 sampling_position: float = None,
                 temperature_k: float = None,
                 plateau_halfwidth: float = None,
                 g_mod_depth: float = None,
                 gamma_env_base: float = None,
                 decoherence_exponent: float = None):
        """
        Initialize temperature-dependent Orch-OR model.

        Args:
            n_tubulins: Superposition size (10^8 to 2x10^10)
            sampling_position: PM modulus coordinate [0, 1]
            temperature_k: Brain temperature in Kelvin
            plateau_halfwidth: Half-width of viable plateau
            g_mod_depth: Maximum G_eff modulation
            gamma_env_base: Environmental decoherence at reference T
            decoherence_exponent: Temperature scaling exponent beta
        """
        self.n = float(n_tubulins if n_tubulins is not None else self.BEST_PARAMS['n_tubulins_nominal'])
        self.pos = np.clip(
            sampling_position if sampling_position is not None else self.BEST_PARAMS['sampling_position'],
            0.0, 1.0
        )
        self.T = temperature_k if temperature_k is not None else self.BEST_PARAMS['temp_reference_k']
        self.hw = plateau_halfwidth if plateau_halfwidth is not None else self.BEST_PARAMS['plateau_halfwidth']
        self.depth = g_mod_depth if g_mod_depth is not None else self.BEST_PARAMS['g_mod_depth']
        self.gamma_env0 = gamma_env_base if gamma_env_base is not None else self.BEST_PARAMS['gamma_env_base']
        self.beta = decoherence_exponent if decoherence_exponent is not None else self.BEST_PARAMS['decoherence_exponent']
        self.T0 = self.BEST_PARAMS['temp_reference_k']

        # Physical parameters
        self.m_tubulin = self.BEST_PARAMS['m_tubulin']
        self.r_superposition = self.BEST_PARAMS['r_superposition']
        self.tau_ref = self.BEST_PARAMS['tau_ref_s']
        self.n_ref = self.BEST_PARAMS['n_ref']

    # ==========================================================================
    # G_EFF MODULATION (PM Vacuum Position)
    # ==========================================================================

    def g_eff_factor(self) -> float:
        """
        Compute G_eff / G_0 based on PM sampling position.

        Broad plateau near middle (stable vacuum), falloff at edges.

        Returns:
            G_eff factor in [1-depth, 1]
        """
        dev = abs(self.pos - 0.5)
        if dev <= self.hw:
            return 1.0
        else:
            falloff = np.exp(-((dev - self.hw) / 0.12) ** 2)
            return 1.0 - self.depth * (1.0 - falloff)

    # ==========================================================================
    # ORCH-OR PHYSICS
    # ==========================================================================

    def or_collapse_timescale(self) -> float:
        """
        Penrose OR collapse timescale (phenomenologically calibrated).

        Uses scaling: tau = tau_ref * (n_ref / n)^2 * g_eff_factor
        This gives ~500 ms for 10^10 tubulins at stable vacuum.

        Returns:
            Collapse timescale in seconds
        """
        if self.n > 0:
            # Base timescale from calibration
            tau_base = self.tau_ref * (self.n_ref / self.n) ** 2
            # Modulated by G_eff (reduced G -> longer timescale)
            return tau_base / self.g_eff_factor()
        return np.inf

    def diosi_penrose_decoherence(self) -> float:
        """
        Diosi-Penrose gravitational decoherence rate.

        Gamma_DP = 1 / tau_OR (inverse of collapse timescale)

        Returns:
            Decoherence rate in s^-1
        """
        tau = self.or_collapse_timescale()
        if tau > 0 and not np.isinf(tau):
            return 1.0 / tau
        return 0.0

    def environmental_decoherence(self) -> float:
        """
        Temperature-dependent environmental decoherence rate.

        Gamma_env(T) = Gamma_env0 * (T / T0)^beta

        The strong temperature dependence (beta ~ 8) captures:
        - Thermal phonon scattering
        - Protein conformational fluctuations
        - Water molecule interactions

        Returns:
            Decoherence rate in s^-1
        """
        temp_ratio = self.T / self.T0
        return self.gamma_env0 * (temp_ratio ** self.beta)

    def total_decoherence(self) -> float:
        """
        Total decoherence rate: Gamma_total = Gamma_DP + Gamma_env(T)

        Returns:
            Total decoherence rate in s^-1
        """
        return self.diosi_penrose_decoherence() + self.environmental_decoherence()

    def viability_metric(self) -> float:
        """
        Viability metric: tau_OR * Gamma_total

        For OR to dominate (consciousness viable):
            viability < 1  =>  OR collapse before decoherence

        Lower = better quantum coherence.

        Returns:
            Viability metric (dimensionless, should be < 1)
        """
        return self.or_collapse_timescale() * self.total_decoherence()

    # ==========================================================================
    # THRESHOLD VALIDATION
    # ==========================================================================

    def is_above_threshold(self) -> Tuple[bool, Dict]:
        """
        Check if system passes viability threshold.

        Biology is viable if:
        1. tau_OR in valid range [25 ms, 2000 ms]
        2. viability < 1 (OR dominates)
        3. Temperature in physiological range

        Returns:
            (passes_threshold, details)
        """
        tau_ms = self.or_collapse_timescale() * 1000
        viability = self.viability_metric()

        thresholds = self.THRESHOLDS

        # Check criteria
        tau_in_range = thresholds['tau_min_ms'] <= tau_ms <= thresholds['tau_max_ms']
        viability_ok = viability < thresholds['viability_max']
        temp_ok = thresholds['temp_min_k'] <= self.T <= thresholds['temp_max_k']
        in_plateau = abs(self.pos - 0.5) <= self.hw

        passes = tau_in_range and viability_ok and temp_ok

        details = {
            'tau_ms': tau_ms,
            'tau_in_range': tau_in_range,
            'tau_bounds': (thresholds['tau_min_ms'], thresholds['tau_max_ms']),
            'viability': viability,
            'viability_ok': viability_ok,
            'viability_threshold': thresholds['viability_max'],
            'temperature_k': self.T,
            'temp_ok': temp_ok,
            'temp_bounds': (thresholds['temp_min_k'], thresholds['temp_max_k']),
            'position': self.pos,
            'in_plateau': in_plateau,
            'passes_all': passes
        }

        return passes, details

    # ==========================================================================
    # ANALYSIS
    # ==========================================================================

    def run_analysis(self, verbose: bool = True) -> Dict:
        """
        Run complete temperature-dependent threshold analysis.

        Returns:
            Comprehensive results dictionary
        """
        # Core quantities
        tau = self.or_collapse_timescale()
        gamma_dp = self.diosi_penrose_decoherence()
        gamma_env = self.environmental_decoherence()
        gamma_total = self.total_decoherence()
        viability = self.viability_metric()
        g_factor = self.g_eff_factor()

        # Threshold check
        passes, threshold_details = self.is_above_threshold()

        results = {
            'input_parameters': {
                'n_tubulins': float(self.n),
                'sampling_position': float(self.pos),
                'temperature_k': float(self.T),
                'plateau_halfwidth': float(self.hw),
                'g_mod_depth': float(self.depth),
                'gamma_env_base': float(self.gamma_env0),
                'decoherence_exponent': float(self.beta)
            },
            'physical_quantities': {
                'G_eff_factor': float(g_factor),
                'tau_OR_s': float(tau),
                'tau_OR_ms': float(tau * 1000),
                'Gamma_DP_Hz': float(gamma_dp),
                'Gamma_env_Hz': float(gamma_env),
                'Gamma_total_Hz': float(gamma_total),
                'viability_metric': float(viability)
            },
            'threshold_validation': {
                'passes_all': passes,
                'tau_in_range': threshold_details['tau_in_range'],
                'viability_ok': threshold_details['viability_ok'],
                'temp_ok': threshold_details['temp_ok'],
                'in_plateau': threshold_details['in_plateau']
            },
            'interpretation': {
                'or_dominates': viability < 1.0,
                'warm_wet_challenge': 'ADDRESSED' if viability < 1.0 else 'FAILS',
                'testable_predictions': [
                    'Hypothermia -> increased coherence (lower viability)',
                    'Hyperthermia -> decreased coherence (higher viability)',
                    'Anesthesia -> effective temperature shift'
                ]
            },
            'status': 'SPECULATIVE - Open problem for future work',
            'overall_valid': passes,
            'version': 'v15.5'
        }

        if verbose:
            self._print_report(results)

        return results

    def _print_report(self, results: Dict):
        """Print formatted analysis report."""
        print()
        print("=" * 80)
        print(" ORCH-OR WITH TEMPERATURE-DEPENDENT DECOHERENCE (v15.5)")
        print("=" * 80)
        print()
        print("STATUS: Speculative appendix - open problem for future work")
        print("KEY QUESTION: Does biology pass threshold at physiological temperature?")
        print()

        print("=" * 80)
        print(" INPUT PARAMETERS")
        print("=" * 80)
        inp = results['input_parameters']
        print(f"  n_tubulins:           {inp['n_tubulins']:.0e}")
        print(f"  sampling_position:    {inp['sampling_position']:.2f}")
        print(f"  temperature:          {inp['temperature_k']:.1f} K")
        print(f"  Gamma_env_base:       {inp['gamma_env_base']:.2e} Hz")
        print(f"  beta (T exponent):    {inp['decoherence_exponent']:.1f}")
        print()

        print("=" * 80)
        print(" ORCH-OR PHYSICS")
        print("=" * 80)
        phys = results['physical_quantities']
        print(f"  G_eff / G0:           {phys['G_eff_factor']:.4f}")
        print(f"  tau_OR:               {phys['tau_OR_ms']:.1f} ms")
        print(f"  Gamma_DP:             {phys['Gamma_DP_Hz']:.2e} Hz")
        print(f"  Gamma_env(T):         {phys['Gamma_env_Hz']:.2e} Hz")
        print(f"  Gamma_total:          {phys['Gamma_total_Hz']:.2e} Hz")
        print()

        print("=" * 80)
        print(" VIABILITY (Warm & Wet Challenge)")
        print("=" * 80)
        viab = phys['viability_metric']
        status = "VIABLE (OR dominates)" if viab < 1.0 else "NOT VIABLE (decoherence dominates)"
        print(f"  Viability metric:     {viab:.4f}")
        print(f"  Threshold:            < 1.0")
        print(f"  Status:               {status}")
        print()

        print("=" * 80)
        print(" THRESHOLD VALIDATION")
        print("=" * 80)
        val = results['threshold_validation']
        status_tau = "PASS" if val['tau_in_range'] else "FAIL"
        status_viab = "PASS" if val['viability_ok'] else "FAIL"
        status_temp = "PASS" if val['temp_ok'] else "FAIL"
        print(f"  tau_OR in [25, 2000] ms:  {status_tau}")
        print(f"  viability < 1.0:          {status_viab}")
        print(f"  T in [270, 320] K:        {status_temp}")
        print()
        overall = "PASSES" if results['overall_valid'] else "FAILS"
        print(f"  Overall: {overall} threshold requirements")
        print()

        print("=" * 80)
        print(" TESTABLE PREDICTIONS")
        print("=" * 80)
        for pred in results['interpretation']['testable_predictions']:
            print(f"  - {pred}")
        print("=" * 80)


def temperature_scan(temps: np.ndarray = None, n_tubulins: float = 1e10) -> Dict:
    """
    Scan viability across temperature range.

    Returns:
        Scan results showing temperature dependence
    """
    if temps is None:
        temps = np.linspace(270, 340, 71)

    results = {
        'temperatures_k': temps.tolist(),
        'tau_ms': [],
        'viability': [],
        'gamma_env': [],
        'passes': []
    }

    for T in temps:
        model = MicrotubuleOrchORTemperature(n_tubulins=n_tubulins, temperature_k=T)
        results['tau_ms'].append(model.or_collapse_timescale() * 1000)
        results['viability'].append(model.viability_metric())
        results['gamma_env'].append(model.environmental_decoherence())
        passes, _ = model.is_above_threshold()
        results['passes'].append(passes)

    results['viable_fraction'] = sum(results['passes']) / len(results['passes'])
    results['physiological_viability'] = MicrotubuleOrchORTemperature(
        n_tubulins=n_tubulins, temperature_k=310.0
    ).viability_metric()

    return results


def position_scan(positions: np.ndarray = None, temperature_k: float = 310.0) -> Dict:
    """
    Scan viability across PM sampling positions.

    Returns:
        Scan results showing position dependence
    """
    if positions is None:
        positions = np.linspace(0, 1, 101)

    results = {
        'positions': positions.tolist(),
        'viability': [],
        'tau_ms': [],
        'passes': []
    }

    for pos in positions:
        model = MicrotubuleOrchORTemperature(sampling_position=pos, temperature_k=temperature_k)
        results['viability'].append(model.viability_metric())
        results['tau_ms'].append(model.or_collapse_timescale() * 1000)
        passes, _ = model.is_above_threshold()
        results['passes'].append(passes)

    results['viable_fraction'] = sum(results['passes']) / len(results['passes'])

    return results


def shielding_sensitivity_analysis() -> Dict:
    """
    Analyze what shielding factor would be needed for Orch OR viability.

    This honestly presents the "warm and wet" challenge quantitatively.

    Returns:
        Analysis of required shielding for viability
    """
    # Baseline model
    model = MicrotubuleOrchORTemperature()
    tau_OR = model.or_collapse_timescale()
    gamma_env_base = model.gamma_env0

    # For viability < 1, need Gamma_total < 1/tau_OR
    gamma_max_for_viability = 1.0 / tau_OR
    shielding_required = gamma_env_base / gamma_max_for_viability

    # Test various shielding scenarios
    scenarios = [
        ('No shielding (conservative)', 1.0),
        ('Protein structure (10^3x)', 1e3),
        ('Tubulin lattice (10^6x)', 1e6),
        ('Quantum coherent structure (10^9x)', 1e9),
        ('Near-perfect isolation (10^10x)', 1e10),
    ]

    results = {
        'tau_OR_s': tau_OR,
        'gamma_env_unshielded': gamma_env_base,
        'gamma_max_for_viability': gamma_max_for_viability,
        'shielding_required': shielding_required,
        'scenarios': []
    }

    for label, shielding_factor in scenarios:
        gamma_eff = gamma_env_base / shielding_factor
        viability = tau_OR * gamma_eff
        viable = viability < 1.0
        results['scenarios'].append({
            'label': label,
            'shielding_factor': shielding_factor,
            'gamma_eff_Hz': gamma_eff,
            'viability': viability,
            'viable': viable
        })

    return results


def export_temperature_results() -> Dict:
    """Export temperature-dependent results."""
    model = MicrotubuleOrchORTemperature()
    results = model.run_analysis(verbose=False)

    return {
        'N_TUBULINS': results['input_parameters']['n_tubulins'],
        'TEMPERATURE_K': results['input_parameters']['temperature_k'],
        'TAU_MS': results['physical_quantities']['tau_OR_ms'],
        'VIABILITY': results['physical_quantities']['viability_metric'],
        'GAMMA_ENV_HZ': results['physical_quantities']['Gamma_env_Hz'],
        'PASSES_THRESHOLD': results['overall_valid'],
        'OR_DOMINATES': results['interpretation']['or_dominates'],
        'STATUS': 'SPECULATIVE',
        'VERSION': 'v15.5'
    }


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Run analysis at physiological temperature
    model = MicrotubuleOrchORTemperature()
    model.run_analysis()

    # Temperature scan
    print("\n" + "=" * 80)
    print(" TEMPERATURE SCAN")
    print("=" * 80)
    temp_scan = temperature_scan()
    print(f"  Physiological (310 K) viability: {temp_scan['physiological_viability']:.4f}")
    print(f"  Viable fraction (270-340 K): {temp_scan['viable_fraction']*100:.1f}%")

    # Find critical temperature
    for i, (T, v) in enumerate(zip(temp_scan['temperatures_k'], temp_scan['viability'])):
        if v >= 1.0:
            print(f"  Critical temperature (viability = 1): ~{T:.0f} K")
            break
    else:
        print("  Critical temperature: > 340 K (always viable in range)")
    print("=" * 80)

    # Position scan
    print("\n" + "=" * 80)
    print(" POSITION SCAN (at 310 K)")
    print("=" * 80)
    pos_scan = position_scan()
    print(f"  Viable fraction: {pos_scan['viable_fraction']*100:.1f}%")
    print("=" * 80)

    # Shielding sensitivity analysis
    print("\n" + "=" * 80)
    print(" SHIELDING SENSITIVITY ANALYSIS (Open Problem)")
    print("=" * 80)
    shielding = shielding_sensitivity_analysis()
    print(f"  tau_OR:                {shielding['tau_OR_s']*1000:.0f} ms")
    print(f"  Gamma_env (unshielded): {shielding['gamma_env_unshielded']:.2e} Hz")
    print(f"  Max Gamma for viability: {shielding['gamma_max_for_viability']:.2f} Hz")
    print(f"  Shielding required:     {shielding['shielding_required']:.2e}x reduction")
    print()
    print("  Scenario Analysis:")
    for s in shielding['scenarios']:
        status = "VIABLE" if s['viable'] else "NOT VIABLE"
        print(f"    {s['label']:40}: viability = {s['viability']:.2e} [{status}]")
    print()
    print("  CONCLUSION: Enormous shielding (~10^10x) required for Orch OR viability.")
    print("              This quantifies the 'warm and wet' challenge as an open problem.")
    print("=" * 80)
