"""
Dynamical Lambda Relaxation via Sampler Entropy v24.3
=====================================================

Derives the cosmological constant through dynamical relaxation of the
effective potential V_eff via exponential entropy suppression:

    V_eff = V_bare * exp(-S_Pneuma)

where V_bare = V_racetrack + V_torsion and S_Pneuma is the total Pneuma
entropy from bridge thermodynamics, OR collapse events, and sampler
diffusion on S^{2,0}.

MOTIVATION:
    The previous cosmological_constant.py (v16.1) was classified UNFOUNDED
    because it used observed H0 circularly to derive Lambda. The racetrack
    stabilization gives V_min ~ 3.7e-5 M_Pl^4 -- 117 orders too large.

    This module attempts to bridge the gap via exp(-S_Pneuma) suppression,
    analogous to instanton-mediated tunneling where V ~ V_0 * exp(-S_inst).

HONEST STATUS:
    The mechanism is PLAUSIBLE but NOT YET DERIVED. The key issue is that
    S_Pneuma must equal ~280 for exp(-S) ~ 10^-122, but our naive estimate
    gives S ~ 530. The factor-of-2 discrepancy in the exponent corresponds
    to a 108-order-of-magnitude error in the suppression factor. A rigorous
    derivation of S_Pneuma from first principles has not been completed.

TORSION FUNNEL CALIBRATION (v24.3, 2026-03-20):
    Sprint 3 added compute_V_eff_with_torsion_funnel() which attempts to
    close the 108-order gap by subtracting a "torsion funnel integral" from
    S_naive. The integral must equal ~250 for Lambda to match observation.
    Eight candidate G2 formulas were evaluated; NONE independently produce 250.
    Gemini 2.5 Flash debate (3 rounds) classified this as FITTED.
    The mechanism remains PLAUSIBLE; the specific entropy value is FITTED.

INDEPENDENT ASSESSMENT (Claude Opus 4.6 + Gemini 2.5 Flash, 2026-03-16)
========================================================================

Gemini Debate (3 rounds):

Round 1 (Physical viability):
    Gemini identified two critical flaws:
    (A) ENTROPY INCONSISTENCY: The naive estimate S ~ 14*T_min ~ 530 gives
        exp(-530) ~ 10^-230, NOT 10^-122. This is a direct numerical
        contradiction -- a factor-of-2 error in the exponent produces a
        108-order-of-magnitude error in the suppression.
    (B) FINE-TUNING OF rho_sampler: In the original formulation V_eff =
        V_racetrack - (1/b3)*rho_sampler + V_torsion*exp(-S), the dominant
        V_racetrack ~ 3.7e-5 term must be canceled by rho_sampler to 117
        digits. This just moves the fine-tuning problem.

Round 2 (Revised mechanism):
    After reformulating as V_eff = V_bare * exp(-S_Pneuma) (entire potential
    suppressed, not just V_torsion), Gemini assessed:
    (A) V_bare * exp(-S) is "much more physically motivated" -- analogous to
        instanton physics where exp(-S_inst) multiplies the entire amplitude.
    (B) The naive S ~ 530 might be an upper bound. Partial thermalization,
        quantum correlations between bridges, or constraints reducing phase
        space could lower S. But this "has not been done."
    (C) "Your next critical step is to derive S_Pneuma more rigorously."

Round 3 (Classification):
    CLASSIFICATION: PLAUSIBLE
    "The mechanism is physically motivated and offers a compelling path to
    solving the cosmological constant problem. The main missing piece is the
    rigorous derivation of the precise value of S_Pneuma."

    On improvement over previous formula: "Yes, this is a significant
    improvement. The previous formula was essentially a tautology... This
    mechanism starts with V_bare independently calculated from fundamental
    theory, proposes a physically motivated mechanism for suppression, and
    aims to derive S_Pneuma from topology independent of observed Lambda."

INDEPENDENT ASSESSMENT #2 (Torsion Funnel, 2026-03-20)
=======================================================

Gemini Debate (3 rounds):

Round 1 (Is torsion_integral = 250 natural?):
    Gemini confirmed the correction is circular: "The correction of 250
    appears to be circular (fitted to Lambda_obs). It is exactly the value
    needed (530 - 280 = 250) and all candidate G2 formulas fail to produce
    this value."

Round 2 (Mutual information alternative):
    "While the concept of mutual information reducing entropy due to quantum
    correlations is highly plausible and a much more physically grounded
    explanation, the specific value of 250 for that mutual information is
    still being chosen to fit the desired outcome. The numerical value of
    250 remains an input chosen to match the target, rather than an output
    derived from a predictive model."

Round 3 (Classification):
    CLASSIFICATION: FITTED
    "The value 250 is explicitly chosen to match Lambda_obs."

SECTION: 5c (Dynamical Lambda Relaxation)

OUTPUTS:
    - dynamical_lambda.V_racetrack: Racetrack potential at T_min
    - dynamical_lambda.V_torsion: Torsion potential from G2 topology
    - dynamical_lambda.V_bare: Total bare potential
    - dynamical_lambda.S_Pneuma_naive: Naive entropy estimate (overestimate)
    - dynamical_lambda.S_Pneuma_required: Required entropy for Lambda_obs
    - dynamical_lambda.V_eff_naive: V_eff using naive entropy
    - dynamical_lambda.V_eff_target: V_eff using required entropy
    - dynamical_lambda.Lambda_obs: Observed Lambda in M_Pl^4
    - dynamical_lambda.gap_orders_naive: Remaining gap with naive S
    - dynamical_lambda.gap_orders_target: Gap with target S (should be ~0)
    - dynamical_lambda.classification: Honesty classification string

FORMULAS:
    - dynamical-lambda-veff: V_eff = V_bare * exp(-S_Pneuma)
    - dynamical-lambda-vbare: V_bare = V_racetrack(T_min) + V_torsion
    - dynamical-lambda-vtorsion: V_torsion = (chi_eff/b3^3) * M_Pl^4
    - dynamical-lambda-entropy-naive: S_naive = (N_bridges + kappa) * T_min

REFERENCES:
    - Abbott (1985) "A mechanism for reducing the value of the cosmological
      constant" Phys. Lett. B 150, 189-192
    - Bousso, Polchinski (2000) "Quantization of four-form fluxes and
      dynamical neutralization of the cosmological constant" JHEP 0006:006
    - Kachru, Kallosh, Linde, Trivedi (2003) hep-th/0301240
    - Acharya, Gukov (2004) hep-th/0409191

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import sys
import os
import math
import numpy as np
from typing import Dict, Any, List, Optional

# Add parent directories to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(os.path.dirname(_current_dir))
_project_root = os.path.dirname(_simulations_dir)
sys.path.insert(0, _project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
    PMRegistry,
)

from simulations.core.FormulasRegistry import get_registry
_REG = get_registry()


class DynamicalLambdaRelaxation(SimulationBase):
    """
    Dynamical Lambda relaxation via Pneuma entropy suppression (v24.3).

    Computes the effective cosmological constant through exponential
    suppression of the bare potential by the total Pneuma entropy:

        V_eff = V_bare * exp(-S_Pneuma)

    where V_bare combines the racetrack stabilization potential and the
    G2 torsion potential, and S_Pneuma is the late-time Pneuma entropy
    from bridge thermodynamics, OR collapse, and sampler diffusion.

    HONESTY NOTE:
        This mechanism is PLAUSIBLE but has an unresolved factor-of-2
        problem in the entropy exponent. The naive estimate gives
        S ~ 530 (yielding exp(-530) ~ 10^-230), while the observed
        Lambda requires S ~ 280 (yielding exp(-280) ~ 10^-122).
        The mechanism framework is physically motivated (instanton
        analogy), but the precise entropy value is NOT YET DERIVED.

    KEY PARAMETERS (from topology):
        - b3 = 24: G2 Betti number
        - chi_eff = 144: Effective Euler characteristic
        - N_bridges = 12: Number of bridge pairs
        - kappa_sampler = 2: dim(S^{2,0})
    """

    # Topological constants
    B3 = 24                     # G2 Betti number
    CHI_EFF = 144               # Effective Euler characteristic (b3^2/4)
    N_BRIDGES = 12              # Bridge pairs (b3/2)
    KAPPA_SAMPLER = 2           # dim(S^{2,0})

    # Racetrack parameters (from bridge_geometry.py BridgeSystem)
    RACETRACK_A = 1.0           # First instanton prefactor
    RACETRACK_B = -0.5          # Second instanton prefactor
    RACETRACK_a = 2 * math.pi / 24   # 2*pi/b3
    RACETRACK_b = 2 * math.pi / 26   # 2*pi/N_b (N_b=26 = spacelike dims)

    # Observed cosmological constant in Planck units
    # Lambda_obs ~ 2.846e-122 M_Pl^4 (Planck 2018 + DESI)
    LAMBDA_OBS_MPL4 = 2.846e-122

    def __init__(self):
        """Initialize dynamical Lambda relaxation module."""
        self._T_min = None
        self._V_min = None
        self._results = None

    # =========================================================================
    # METADATA
    # =========================================================================

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="dynamical_lambda_v24_2",
            version="24.3",
            domain="cosmology",
            title="Dynamical Lambda Relaxation via Sampler Entropy",
            description=(
                "Derives cosmological constant through dynamical relaxation "
                "of the effective potential via exponential Pneuma entropy "
                "suppression: V_eff = V_bare * exp(-S_Pneuma). Replaces the "
                "UNFOUNDED circular formula in cosmological_constant.py."
            ),
            section_id="5",
            subsection_id="5c",
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return required input parameter paths."""
        return [
            "topology.elder_kads",              # b3 = 24
        ]

    @property
    def output_params(self) -> List[str]:
        """Return output parameter paths."""
        return [
            "dynamical_lambda.V_racetrack",
            "dynamical_lambda.V_torsion",
            "dynamical_lambda.V_bare",
            "dynamical_lambda.S_Pneuma_naive",
            "dynamical_lambda.S_Pneuma_required",
            "dynamical_lambda.V_eff_naive",
            "dynamical_lambda.V_eff_target",
            "dynamical_lambda.Lambda_obs",
            "dynamical_lambda.gap_orders_naive",
            "dynamical_lambda.gap_orders_target",
            "dynamical_lambda.classification",
            "dynamical_lambda.torsion_funnel.S_corrected",
            "dynamical_lambda.torsion_funnel.torsion_integral_needed",
            "dynamical_lambda.torsion_funnel.V_eff_corrected",
            "dynamical_lambda.torsion_funnel.classification",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return formula IDs this simulation provides."""
        return [
            "dynamical-lambda-veff",
            "dynamical-lambda-vbare",
            "dynamical-lambda-vtorsion",
            "dynamical-lambda-entropy-naive",
            "dynamical-lambda-torsion-funnel",
        ]

    # =========================================================================
    # RACETRACK POTENTIAL
    # =========================================================================

    @staticmethod
    def fterm_sugra_potential_single(T_re: float, A: float = 1.0,
                                     B: float = -0.5,
                                     a: float = 2 * math.pi / 24,
                                     b: float = 2 * math.pi / 26) -> float:
        """F-term N=1 SUGRA scalar potential for a single Kahler modulus.

        Implements the full racetrack SUGRA potential:
            W = A exp(-aT) + B exp(-bT)
            K = -3 ln(T + T_bar) = -3 ln(2 Re(T))
            V = e^K [ (T+T_bar)^2/3 |D_T W|^2 - 3|W|^2 ]

        This is the same computation as BridgeSystem.fterm_sugra_potential_single()
        in bridge_geometry.py, duplicated here to avoid circular imports and to
        make this module self-contained.

        Args:
            T_re: Real part of the Kahler modulus (Re(T) > 0)
            A: First instanton prefactor
            B: Second instanton prefactor
            a: First instanton exponent (2*pi/b3)
            b: Second instanton exponent (2*pi/N_b)

        Returns:
            V(T): scalar potential value in M_Pl^4 units
        """
        if T_re <= 0:
            return 1e10

        exp_aT = math.exp(-a * T_re)
        exp_bT = math.exp(-b * T_re)

        W = A * exp_aT + B * exp_bT
        dW = -a * A * exp_aT - b * B * exp_bT

        # Kahler potential K = -3 ln(2T) for real T
        two_T = 2.0 * T_re
        eK = 1.0 / (two_T ** 3)

        # D_T W = dW/dT + (dK/dT) W = dW - (3/(2T)) W
        dK_dT = -3.0 / two_T
        D_T_W = dW + dK_dT * W

        # V = e^K [ (2T)^2/3 |D_T W|^2 - 3|W|^2 ]
        V = eK * ((two_T ** 2 / 3.0) * D_T_W ** 2 - 3.0 * W ** 2)

        return V

    def _find_racetrack_minimum(self) -> tuple:
        """Find the racetrack potential minimum T_min and V_min.

        Uses the same algorithm as BridgeSystem.compute_stabilized_cycle_volumes():
        solve D_T W = 0 by bisection on sign change, then evaluate V(T_min).

        Returns:
            (T_min, V_min) tuple
        """
        if self._T_min is not None:
            return self._T_min, self._V_min

        A = self.RACETRACK_A
        B = self.RACETRACK_B
        a = self.RACETRACK_a
        b = self.RACETRACK_b

        def d_t_w(T_re):
            """Covariant derivative D_T W for real T."""
            if T_re <= 0:
                return -1e10
            exp_aT = math.exp(-a * T_re)
            exp_bT = math.exp(-b * T_re)
            W = A * exp_aT + B * exp_bT
            dW = -a * A * exp_aT - b * B * exp_bT
            return dW - (3.0 / (2.0 * T_re)) * W

        # Scan for sign change in D_T W
        T_lo, T_hi = 0.5, 200.0
        n_scan = 2000
        scan_T = np.linspace(T_lo, T_hi, n_scan)
        sign_change_found = False

        from scipy.optimize import brentq

        for idx in range(n_scan - 1):
            d1 = d_t_w(scan_T[idx])
            d2 = d_t_w(scan_T[idx + 1])
            if d1 * d2 < 0:
                self._T_min = brentq(d_t_w, scan_T[idx], scan_T[idx + 1],
                                     xtol=1e-14)
                sign_change_found = True
                break

        if not sign_change_found:
            # Fallback: minimize |V| with bounded search
            from scipy.optimize import minimize_scalar
            result = minimize_scalar(
                lambda T: self.fterm_sugra_potential_single(T, A, B, a, b),
                bounds=(0.5, 100.0),
                method='bounded',
                options={'xatol': 1e-12}
            )
            self._T_min = result.x

        self._V_min = self.fterm_sugra_potential_single(
            self._T_min, A, B, a, b
        )

        return self._T_min, self._V_min

    # =========================================================================
    # V_EFF COMPUTATION
    # =========================================================================

    def compute_V_torsion(self) -> float:
        """Compute the torsion potential from G2 topology.

        V_torsion = (chi_eff / b3^3) * M_Pl^4

        In Planck units (M_Pl = 1):
            V_torsion = 144 / 24^3 = 144 / 13824 ~ 0.01042

        This represents the residual vacuum energy from the torsion of the
        G2 manifold's associative 3-cycles. The chi_eff factor counts the
        number of independent torsion contributions, while b3^3 provides the
        volume suppression from the compact dimensions.

        Returns:
            V_torsion in M_Pl^4 units
        """
        return self.CHI_EFF / (self.B3 ** 3)

    def compute_V_bare(self) -> dict:
        """Compute the total bare potential before entropy suppression.

        V_bare = V_racetrack(T_min) + V_torsion

        Note: V_racetrack is typically NEGATIVE (AdS minimum), while V_torsion
        is positive. The sign of V_bare depends on which term dominates.

        Returns:
            dict with V_racetrack, V_torsion, V_bare, T_min
        """
        T_min, V_racetrack = self._find_racetrack_minimum()
        V_torsion = self.compute_V_torsion()

        # V_bare is the sum. Note V_racetrack < 0 (AdS), V_torsion > 0
        V_bare = V_racetrack + V_torsion

        return {
            'T_min': T_min,
            'V_racetrack': V_racetrack,
            'V_torsion': V_torsion,
            'V_bare': V_bare,
        }

    def compute_naive_entropy(self, T_min: float) -> float:
        """Compute the naive late-time Pneuma entropy estimate.

        The naive estimate sums contributions from all entropy sources at
        late cosmological times, when the system approaches equilibrium:

            S_naive = N_bridges * ln(states_per_bridge) + sampler_contribution

        For thermal bridges at temperature T_min (Kahler modulus as proxy):
            Each bridge contributes S_vN ~ T_min (von Neumann entropy of
            thermal state with effective temperature ~ 1/T_min)

        Sampler contribution:
            S_sampler ~ kappa_sampler * T_min (from diffusion equilibrium)

        Total: S_naive = (N_bridges + kappa_sampler) * T_min
                       = (12 + 2) * T_min = 14 * T_min

        HONESTY NOTE: This is a ROUGH ESTIMATE. The identification of the
        Kahler modulus T_min with a thermodynamic temperature proxy is
        ASSUMED, not derived. The actual entropy depends on the full
        density matrix of the bridge system at late times.

        Args:
            T_min: Stabilized Kahler modulus from racetrack

        Returns:
            S_naive: Naive entropy estimate (dimensionless)
        """
        return (self.N_BRIDGES + self.KAPPA_SAMPLER) * T_min

    def compute_required_entropy(self, V_bare: float) -> float:
        """Compute the entropy required to match observed Lambda.

        Given V_eff = V_bare * exp(-S), we need:
            S_required = -ln(Lambda_obs / V_bare)

        This is the TARGET value that a rigorous derivation must produce.
        If S_required matches S_naive (or a more refined estimate), the
        mechanism is validated. If not, there is a gap.

        Args:
            V_bare: Total bare potential in M_Pl^4

        Returns:
            S_required: Required entropy for Lambda_obs
        """
        if V_bare <= 0:
            # V_bare is negative (AdS). Cannot match positive Lambda_obs
            # with V_eff = V_bare * exp(-S) since exp(-S) > 0.
            # This indicates a deeper problem: need uplift mechanism.
            # Return NaN to signal this.
            return float('nan')

        if V_bare == 0:
            return float('inf')

        ratio = self.LAMBDA_OBS_MPL4 / V_bare
        if ratio <= 0:
            return float('nan')

        return -math.log(ratio)

    def compute_effective_potential(self, S_Pneuma: float,
                                    V_bare: float) -> float:
        """Compute V_eff = V_bare * exp(-S_Pneuma).

        This is the core equation of the dynamical relaxation mechanism.
        The exponential suppression by the Pneuma entropy reduces the
        bare potential to cosmologically small values.

        Physical motivation (from Gemini debate):
            Analogous to instanton physics where V ~ V_0 * exp(-S_inst).
            If S_Pneuma represents the entropy of the vacuum configuration,
            then exp(-S_Pneuma) is the statistical weight of finding the
            system in that configuration. The entire potential is weighted
            by this probability.

        Args:
            S_Pneuma: Total Pneuma entropy (dimensionless)
            V_bare: Bare potential in M_Pl^4

        Returns:
            V_eff in M_Pl^4 units
        """
        return V_bare * math.exp(-S_Pneuma)

    def compute_lambda_prediction(self) -> dict:
        """Compare V_eff predictions with observed Lambda.

        Computes V_eff using both the naive entropy estimate and the
        required entropy, reporting the gap in orders of magnitude.

        Returns:
            dict with all prediction results and honesty metrics
        """
        # Get bare potential components
        bare = self.compute_V_bare()
        T_min = bare['T_min']
        V_racetrack = bare['V_racetrack']
        V_torsion = bare['V_torsion']
        V_bare = bare['V_bare']

        # Compute entropy estimates
        S_naive = self.compute_naive_entropy(T_min)
        S_required = self.compute_required_entropy(V_bare)

        # Compute V_eff with naive entropy
        if V_bare > 0:
            V_eff_naive = self.compute_effective_potential(S_naive, V_bare)
            V_eff_target = self.compute_effective_potential(S_required, V_bare)
        else:
            # V_bare < 0: mechanism fails for positive Lambda
            V_eff_naive = V_bare  # No suppression helps with wrong sign
            V_eff_target = float('nan')

        # Compute gaps
        def _log_ratio(V_eff):
            if V_eff == 0 or not math.isfinite(V_eff):
                return float('inf')
            ratio = abs(V_eff) / self.LAMBDA_OBS_MPL4
            if ratio <= 0:
                return float('inf')
            return math.log10(ratio)

        log_ratio_naive = _log_ratio(V_eff_naive)
        log_ratio_target = _log_ratio(V_eff_target)

        # Entropy gap: how far is S_naive from S_required?
        if math.isfinite(S_required):
            entropy_gap = S_naive - S_required
            entropy_ratio = S_naive / S_required if S_required > 0 else float('inf')
        else:
            entropy_gap = float('nan')
            entropy_ratio = float('nan')

        # Classification based on gap
        if V_bare <= 0:
            classification = "UNFOUNDED: V_bare < 0 (AdS), cannot match positive Lambda"
        elif abs(log_ratio_naive) < 1:
            classification = "SPECULATIVE: Naive entropy within 1 order (integration timescale not topological)"
        elif abs(log_ratio_naive) < 10:
            classification = "PLAUSIBLE: Naive entropy within 10 orders"
        elif math.isfinite(S_required) and abs(entropy_ratio - 1.0) < 0.1:
            classification = "PLAUSIBLE: Entropy within 10% of required"
        else:
            classification = (
                "PLAUSIBLE-MECHANISM / NUMEROLOGICAL-VALUE: "
                "Mechanism is physically motivated (instanton analogy), "
                f"but naive S={S_naive:.1f} vs required S={S_required:.1f} "
                f"(ratio {entropy_ratio:.2f}x). "
                "The entropy value is NOT YET DERIVED from first principles."
            )

        return {
            # Bare potential components
            'T_min': T_min,
            'V_racetrack': V_racetrack,
            'V_torsion': V_torsion,
            'V_bare': V_bare,

            # Entropy estimates
            'S_Pneuma_naive': S_naive,
            'S_Pneuma_required': S_required,
            'entropy_gap': entropy_gap,
            'entropy_ratio': entropy_ratio,

            # Effective potential predictions
            'V_eff_naive': V_eff_naive,
            'V_eff_target': V_eff_target,
            'Lambda_obs': self.LAMBDA_OBS_MPL4,

            # Gap analysis (orders of magnitude)
            'gap_orders_naive': abs(log_ratio_naive),
            'gap_orders_target': abs(log_ratio_target),
            'improvement_from_bare': (
                abs(math.log10(abs(V_bare) / self.LAMBDA_OBS_MPL4))
                - abs(log_ratio_naive)
                if V_bare != 0 and math.isfinite(log_ratio_naive)
                else float('nan')
            ),

            # Honesty
            'classification': classification,
            'sign_ok': V_bare > 0,
        }

    # =========================================================================
    # TORSION FUNNEL CALIBRATION (v24.3)
    # =========================================================================

    def compute_torsion_funnel_candidates(self, T_min: float) -> dict:
        """Exhaustively evaluate candidate torsion funnel integrals.

        The torsion funnel hypothesis proposes that the naive entropy S ~ 530
        can be reduced by subtracting a "torsion integral" arising from the
        G2 manifold's torsion forms (Hitchin 2001, Joyce 2000). For V_eff to
        match Lambda_obs, the integral must reduce S from ~530 to ~280,
        requiring torsion_integral ~ 250.

        This method evaluates ALL candidate formulas from G2 topology and
        reports whether any naturally produce the required value.

        HONESTY: None of the candidate formulas independently yield 250.
        The closest natural candidates are chi_eff * ln(T_min) ~ 523
        (too large, overshoots) and b3 * ln(T_min) ~ 87 (too small).

        Args:
            T_min: Stabilized Kahler modulus from racetrack

        Returns:
            dict with all candidate values and analysis
        """
        ln_T = math.log(T_min)
        ln_T2 = math.log(T_min ** 2)

        candidates = {
            # (a) Full Euler characteristic times log modulus
            'chi_eff_ln_T': {
                'formula': 'chi_eff * ln(T_min) = 144 * ln(37.85)',
                'value': self.CHI_EFF * ln_T,
                'motivation': 'Integral of |T|^2 over G2 7-manifold with chi_eff torsion classes',
            },
            # (b) Betti number times log modulus
            'b3_ln_T': {
                'formula': 'b3 * ln(T_min) = 24 * ln(37.85)',
                'value': self.B3 * ln_T,
                'motivation': 'One torsion class per harmonic 3-form (b3 classes)',
            },
            # (c) Bridge count times log modulus squared
            'N_bridges_ln_T2': {
                'formula': 'N_bridges * ln(T_min^2) = 12 * 2*ln(37.85)',
                'value': self.N_BRIDGES * ln_T2,
                'motivation': 'Each bridge pair contributes torsion over (2,0) cycle',
            },
            # (d) (chi_eff - b3) times log modulus
            'chi_minus_b3_ln_T': {
                'formula': '(chi_eff - b3) * ln(T_min) = 120 * ln(37.85)',
                'value': (self.CHI_EFF - self.B3) * ln_T,
                'motivation': 'Non-harmonic torsion classes (total minus free part)',
            },
            # (e) b3^2 / ln(T_min)
            'b3_sq_over_ln_T': {
                'formula': 'b3^2 / ln(T_min) = 576 / ln(37.85)',
                'value': self.B3 ** 2 / ln_T,
                'motivation': 'Dual formulation: torsion squared over logarithmic volume',
            },
            # (f) (b3/2)^2 * ln(T_min) [= chi_eff * ln(T_min)]
            'half_b3_sq_ln_T': {
                'formula': '(b3/2)^2 * ln(T_min) = 144 * ln(37.85)',
                'value': (self.B3 / 2) ** 2 * ln_T,
                'motivation': 'Bridge-squared torsion (equivalent to candidate a)',
            },
            # (g) b3 * T_min / ln(T_min) -- ad hoc
            'b3_T_over_ln_T': {
                'formula': 'b3 * T_min / ln(T_min)',
                'value': self.B3 * T_min / ln_T,
                'motivation': 'Ad hoc ratio (no topological origin). NOTE: numerically '
                              'close to target (~0.4% off) but this is a coincidence: '
                              'T_min depends on b3 through the racetrack (a=2*pi/b3), '
                              'creating an implicit circular dependency.',
                'ad_hoc': True,
            },
            # (h) sqrt(chi_eff) * T_min / kappa
            'sqrt_chi_T_over_kappa': {
                'formula': 'sqrt(chi_eff) * T_min / kappa = 12 * T_min / 2',
                'value': math.sqrt(self.CHI_EFF) * T_min / self.KAPPA_SAMPLER,
                'motivation': 'Geometric mean torsion with sampler normalization',
            },
        }

        # Compute target and deviations
        S_naive = self.compute_naive_entropy(T_min)
        S_required = 280.96  # -ln(Lambda_obs / V_bare) ~ 280.96
        target_integral = S_naive - S_required

        for key, cand in candidates.items():
            cand['target'] = target_integral
            cand['deviation'] = cand['value'] - target_integral
            cand['deviation_pct'] = (
                100.0 * (cand['value'] - target_integral) / target_integral
                if target_integral != 0 else float('inf')
            )

        # Find closest candidate (excluding ad hoc ones for "natural match")
        closest_key = min(candidates, key=lambda k: abs(candidates[k]['deviation']))
        closest = candidates[closest_key]

        # For "natural match", exclude ad hoc candidates (no topological origin)
        non_adhoc = {k: v for k, v in candidates.items() if not v.get('ad_hoc', False)}
        closest_natural_key = min(non_adhoc, key=lambda k: abs(non_adhoc[k]['deviation']))
        closest_natural = non_adhoc[closest_natural_key]

        return {
            'candidates': candidates,
            'target_integral': target_integral,
            'S_naive': S_naive,
            'S_required': S_required,
            'closest_candidate': closest_key,
            'closest_value': closest['value'],
            'closest_deviation_pct': closest['deviation_pct'],
            'closest_natural_candidate': closest_natural_key,
            'closest_natural_value': closest_natural['value'],
            'closest_natural_deviation_pct': closest_natural['deviation_pct'],
            # A "natural match" requires a non-ad-hoc candidate within 5%
            'any_natural_match': abs(closest_natural['deviation_pct']) < 5.0,
            'note_on_closest': (
                f'Closest overall is {closest_key} = {closest["value"]:.2f} '
                f'({closest["deviation_pct"]:+.1f}%), but it is ad hoc '
                f'(T_min depends on b3, creating implicit circularity). '
                f'Closest with topological motivation: {closest_natural_key} '
                f'= {closest_natural["value"]:.2f} '
                f'({closest_natural["deviation_pct"]:+.1f}%).'
            ) if closest.get('ad_hoc', False) else None,
        }

    def compute_V_eff_with_torsion_funnel(self) -> dict:
        """Compute V_eff with torsion funnel correction to S_Pneuma.

        S_corrected = S_naive - torsion_integral
        V_eff = V_bare * exp(-S_corrected)

        CRITICAL HONESTY CHECK (Gemini 2.5 Flash debate, 2026-03-20):
        ================================================================
        Round 1: Gemini confirmed that the torsion_integral = 250 is
            circular because it equals EXACTLY 530 - 280 = the value needed
            to match Lambda_obs. All candidate G2 formulas fail to produce 250.

        Round 2: The alternative explanation (mutual information from bridge
            entanglement reducing naive S) is conceptually more sound, but
            the VALUE of 250 is still chosen to match the target, not
            independently derived. "You've shifted from a conceptually vague
            torsion integral to a conceptually sound mutual information,
            which is progress. However, the numerical value of 250 remains
            an input chosen to match the target."

        Round 3: CLASSIFICATION = FITTED
            "The value 250 is explicitly chosen to match Lambda_obs."

        CONCLUSION: The torsion funnel correction is FITTED, not DERIVED.
        We report all candidate formulas transparently and acknowledge that
        none independently produces the required value.

        Returns:
            dict with corrected V_eff and full honesty analysis
        """
        # Get bare potential
        bare = self.compute_V_bare()
        T_min = bare['T_min']
        V_bare = bare['V_bare']

        if V_bare <= 0:
            return {
                'status': 'UNFOUNDED',
                'reason': 'V_bare < 0 (AdS), cannot match positive Lambda',
                'V_bare': V_bare,
            }

        # Compute naive entropy
        S_naive = self.compute_naive_entropy(T_min)

        # Required entropy for Lambda_obs
        S_required = self.compute_required_entropy(V_bare)

        # The torsion integral needed
        torsion_integral_needed = S_naive - S_required

        # Evaluate all candidate formulas
        candidates = self.compute_torsion_funnel_candidates(T_min)

        # ── FITTED correction: use the exact value needed ──
        # We are TRANSPARENT that this is fitted, not derived
        S_corrected = S_required  # = S_naive - torsion_integral_needed

        V_eff_corrected = self.compute_effective_potential(S_corrected, V_bare)

        # Gap with corrected S
        if V_eff_corrected > 0:
            gap_corrected = abs(math.log10(V_eff_corrected / self.LAMBDA_OBS_MPL4))
        else:
            gap_corrected = float('inf')

        return {
            # Core results
            'V_bare': V_bare,
            'T_min': T_min,
            'S_naive': S_naive,
            'S_required': S_required,
            'torsion_integral_needed': torsion_integral_needed,
            'S_corrected': S_corrected,
            'V_eff_corrected': V_eff_corrected,
            'Lambda_obs': self.LAMBDA_OBS_MPL4,
            'gap_orders_corrected': gap_corrected,

            # Candidate analysis
            'candidates': candidates,
            'any_natural_match': candidates['any_natural_match'],
            'closest_candidate': candidates['closest_candidate'],
            'closest_value': candidates['closest_value'],
            'closest_deviation_pct': candidates['closest_deviation_pct'],

            # Honesty
            'classification': 'FITTED',
            'classification_detail': (
                f"The torsion funnel integral = {torsion_integral_needed:.2f} is "
                f"FITTED to match Lambda_obs. No natural G2 formula independently "
                f"produces this value. Closest candidate: "
                f"{candidates['closest_candidate']} = "
                f"{candidates['closest_value']:.2f} "
                f"({candidates['closest_deviation_pct']:+.1f}% off). "
                f"The mechanism (entropy suppression) is PLAUSIBLE; the specific "
                f"entropy value is FITTED."
            ),

            # Gemini debate record
            'gemini_debate': {
                'date': '2026-03-20',
                'model': 'gemini-2.5-flash',
                'rounds': 3,
                'round_1': (
                    'Torsion integral = 250 is circular. All candidate G2 '
                    'formulas fail to produce this value.'
                ),
                'round_2': (
                    'Mutual information from bridge entanglement is conceptually '
                    'sounder but the VALUE of 250 is still chosen to match target. '
                    '"The numerical value of 250 remains an input."'
                ),
                'round_3': 'CLASSIFICATION: FITTED',
            },
        }

    # =========================================================================
    # SAMPLER ENERGY DENSITY
    # =========================================================================

    def _get_sampler_energy_density(self) -> float:
        """Get sampler energy density from SamplerEntropyDynamics.

        Uses the compute_rho_sampler() method from sampler_entropy_dynamics.py.
        Falls back to a default estimate if the module is unavailable.

        Returns:
            rho_sampler in natural units
        """
        try:
            from simulations.PM.field_dynamics.sampler_entropy_dynamics import (
                SamplerEntropyDynamics,
            )
            sed = SamplerEntropyDynamics()
            return sed.compute_rho_sampler()
        except (ImportError, Exception):
            # Fallback: estimate from Gaussian profile on S^{2,0}
            # rho_sampler = (kappa/2) * <(nabla S)^2>
            # For Gaussian with sigma=0.3 on [-1,1]^2: <(nabla S)^2> ~ 1/sigma^2 ~ 11
            # rho_sampler ~ (2/2) * 11 ~ 11
            sigma = 0.3
            return (self.KAPPA_SAMPLER / 2.0) * (1.0 / sigma ** 2)

    # =========================================================================
    # ORIGINAL V_EFF FORMULATION (for reference / comparison)
    # =========================================================================

    def compute_effective_potential_original(self) -> dict:
        """Compute V_eff in the original (flawed) formulation.

        V_eff = V_racetrack - (1/b3)*rho_sampler + V_torsion*exp(-S_Pneuma)

        This formulation was criticized by Gemini for requiring rho_sampler
        to cancel V_racetrack to 117 digits -- just moving the fine-tuning
        problem rather than solving it. Retained for comparison.

        Returns:
            dict with original formulation results
        """
        T_min, V_racetrack = self._find_racetrack_minimum()
        V_torsion = self.compute_V_torsion()
        rho_sampler = self._get_sampler_energy_density()
        S_naive = self.compute_naive_entropy(T_min)

        V_eff_original = (
            V_racetrack
            - (1.0 / self.B3) * rho_sampler
            + V_torsion * math.exp(-S_naive)
        )

        return {
            'formulation': 'original (V_race - rho/b3 + V_tor*exp(-S))',
            'V_racetrack': V_racetrack,
            'rho_sampler_term': (1.0 / self.B3) * rho_sampler,
            'V_torsion_suppressed': V_torsion * math.exp(-S_naive),
            'V_eff': V_eff_original,
            'critique': (
                'Fine-tuning moved to rho_sampler. V_racetrack dominates and '
                'must be canceled by rho_sampler/b3 to 117 digits.'
            ),
        }

    # =========================================================================
    # MAIN EXECUTION
    # =========================================================================

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """Execute the dynamical Lambda relaxation computation.

        Args:
            registry: PMRegistry instance for parameter access

        Returns:
            dict of output parameter values
        """
        # Validate inputs
        self.validate_inputs(registry)

        # Run the main computation
        results = self.compute_lambda_prediction()
        self._results = results

        # Also compute original formulation for comparison
        original = self.compute_effective_potential_original()

        # Compute torsion funnel analysis
        torsion_funnel = self.compute_V_eff_with_torsion_funnel()
        self._torsion_funnel = torsion_funnel

        # Register outputs
        outputs = {
            "dynamical_lambda.V_racetrack": results['V_racetrack'],
            "dynamical_lambda.V_torsion": results['V_torsion'],
            "dynamical_lambda.V_bare": results['V_bare'],
            "dynamical_lambda.S_Pneuma_naive": results['S_Pneuma_naive'],
            "dynamical_lambda.S_Pneuma_required": results['S_Pneuma_required'],
            "dynamical_lambda.V_eff_naive": results['V_eff_naive'],
            "dynamical_lambda.V_eff_target": results['V_eff_target'],
            "dynamical_lambda.Lambda_obs": results['Lambda_obs'],
            "dynamical_lambda.gap_orders_naive": results['gap_orders_naive'],
            "dynamical_lambda.gap_orders_target": results['gap_orders_target'],
            "dynamical_lambda.classification": results['classification'],
            # Torsion funnel outputs
            "dynamical_lambda.torsion_funnel.S_corrected": torsion_funnel.get('S_corrected', float('nan')),
            "dynamical_lambda.torsion_funnel.torsion_integral_needed": torsion_funnel.get('torsion_integral_needed', float('nan')),
            "dynamical_lambda.torsion_funnel.V_eff_corrected": torsion_funnel.get('V_eff_corrected', float('nan')),
            "dynamical_lambda.torsion_funnel.classification": torsion_funnel.get('classification', 'UNFOUNDED'),
        }

        # Register all outputs
        for path, value in outputs.items():
            registry.register_parameter(path, value)

        return outputs

    # =========================================================================
    # SECTION CONTENT
    # =========================================================================

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        content_blocks = [
            ContentBlock(
                type="paragraph",
                content=(
                    "The cosmological constant problem -- why &Lambda; ~ 10<sup>-122</sup> "
                    "M<sub>Pl</sub><sup>4</sup> -- is addressed through dynamical relaxation "
                    "of the effective potential via Pneuma entropy suppression. The previous "
                    "approach (v16.1) used the observed Hubble constant H<sub>0</sub> circularly "
                    "and was classified UNFOUNDED. This module replaces it with a mechanism "
                    "analogous to instanton-mediated tunneling."
                ),
            ),
            ContentBlock(
                type="heading",
                content="Bare Potential",
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The bare potential V<sub>bare</sub> combines the racetrack stabilization "
                    "minimum V<sub>racetrack</sub>(T<sub>min</sub>) from KKLT-type moduli "
                    "stabilization with the G2 torsion potential V<sub>torsion</sub> = "
                    "(&chi;<sub>eff</sub>/b<sub>3</sub><sup>3</sup>) M<sub>Pl</sub><sup>4</sup>. "
                    "The racetrack gives V<sub>racetrack</sub> ~ 10<sup>-5</sup> M<sub>Pl</sub><sup>4</sup> "
                    "(an AdS minimum), while V<sub>torsion</sub> ~ 0.01 M<sub>Pl</sub><sup>4</sup> provides "
                    "an uplift contribution."
                ),
            ),
            ContentBlock(
                type="heading",
                content="Entropy Suppression Mechanism",
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The effective potential is V<sub>eff</sub> = V<sub>bare</sub> &times; "
                    "exp(-S<sub>Pneuma</sub>), where S<sub>Pneuma</sub> is the total late-time "
                    "Pneuma entropy from bridge thermodynamics, OR collapse events, and sampler "
                    "diffusion on S<sup>(2,0)</sup>. This formulation is physically motivated by "
                    "the analogy to instanton physics, where exp(-S<sub>inst</sub>) multiplies "
                    "the entire amplitude (Abbott 1985, Bousso-Polchinski 2000)."
                ),
            ),
            ContentBlock(
                type="heading",
                content="The Factor-of-Two Problem",
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "HONESTY: The naive entropy estimate gives S<sub>naive</sub> ~ "
                    "(N<sub>bridges</sub> + &kappa;<sub>sampler</sub>) &times; T<sub>min</sub> "
                    "= 14 &times; 37.85 ~ 530, yielding exp(-530) ~ 10<sup>-230</sup>. "
                    "This overshoots the required suppression by ~108 orders of magnitude. "
                    "For the mechanism to work, S<sub>Pneuma</sub> must be ~280, giving "
                    "exp(-280) ~ 10<sup>-122</sup>. The factor-of-two discrepancy in the "
                    "exponent could arise from partial thermalization, quantum correlations "
                    "between bridges, or constraints reducing the effective phase space. "
                    "A rigorous derivation of S<sub>Pneuma</sub> from the G2 action principle "
                    "remains an open problem."
                ),
            ),
        ]

        return SectionContent(
            section_id="5",
            subsection_id="5c",
            title="Dynamical Lambda Relaxation via Sampler Entropy",
            content=content_blocks,
            output_params=[
                "dynamical_lambda.V_racetrack",
                "dynamical_lambda.V_torsion",
                "dynamical_lambda.V_bare",
                "dynamical_lambda.S_Pneuma_naive",
                "dynamical_lambda.S_Pneuma_required",
                "dynamical_lambda.V_eff_naive",
                "dynamical_lambda.V_eff_target",
                "dynamical_lambda.Lambda_obs",
                "dynamical_lambda.gap_orders_naive",
                "dynamical_lambda.gap_orders_target",
                "dynamical_lambda.classification",
            ],
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for dynamical Lambda relaxation."""
        return [
            Formula(
                id="dynamical-lambda-veff",
                label="(DL.1)",
                latex=(
                    r"V_{\text{eff}} = V_{\text{bare}} \cdot "
                    r"e^{-S_{\text{Pneuma}}}"
                ),
                plain_text="V_eff = V_bare * exp(-S_Pneuma)",
                category="PLAUSIBLE",
                description=(
                    "Effective cosmological constant from dynamical relaxation. "
                    "The entire bare potential is suppressed by the exponential "
                    "of the Pneuma entropy, analogous to instanton-mediated "
                    "tunneling. PLAUSIBLE mechanism but S_Pneuma value not yet "
                    "derived from first principles."
                ),
                inputParams=[
                    "dynamical_lambda.V_bare",
                    "dynamical_lambda.S_Pneuma_naive",
                ],
                outputParams=[
                    "dynamical_lambda.V_eff_naive",
                ],
                input_params=[
                    "dynamical_lambda.V_bare",
                    "dynamical_lambda.S_Pneuma_naive",
                ],
                output_params=[
                    "dynamical_lambda.V_eff_naive",
                ],
                derivation={
                    "method": "entropy_suppression",
                    "parentFormulas": [
                        "dynamical-lambda-vbare",
                        "sampler-entropy-gradient",
                    ],
                    "steps": [
                        "Compute V_bare from racetrack + torsion",
                        "Compute S_Pneuma from bridge, OR, and sampler entropy",
                        "Apply exponential suppression: V_eff = V_bare * exp(-S)",
                    ],
                    "references": [
                        "Abbott (1985) Phys. Lett. B 150, 189",
                        "Bousso, Polchinski (2000) JHEP 0006:006",
                        "KKLT (2003) hep-th/0301240",
                    ],
                    "honesty": (
                        "PLAUSIBLE: Mechanism is physically motivated but "
                        "S_Pneuma ~ 280 is not derived. Naive estimate gives "
                        "S ~ 530, a factor-of-2 discrepancy in the exponent."
                    ),
                },
                terms={
                    "V_bare": "Bare potential = V_racetrack + V_torsion",
                    "S_Pneuma": "Total Pneuma entropy (bridge + OR + sampler)",
                    "V_eff": "Effective (observed) cosmological constant",
                },
            ),
            Formula(
                id="dynamical-lambda-vbare",
                label="(DL.2)",
                latex=(
                    r"V_{\text{bare}} = V_{\text{racetrack}}(T_{\min}) + "
                    r"V_{\text{torsion}}"
                ),
                plain_text="V_bare = V_racetrack(T_min) + V_torsion",
                category="PLAUSIBLE",
                description=(
                    "Bare potential combining the KKLT racetrack minimum "
                    "(AdS, typically negative) with the G2 torsion uplift. "
                    "V_racetrack is PLAUSIBLE (depends on instanton prefactors "
                    "A, B which are not uniquely fixed by topology). "
                    "V_torsion is DERIVED from chi_eff and b3."
                ),
                inputParams=["topology.elder_kads"],
                outputParams=["dynamical_lambda.V_bare"],
                input_params=["topology.elder_kads"],
                output_params=["dynamical_lambda.V_bare"],
                derivation={
                    "method": "racetrack_plus_torsion",
                    "steps": [
                        "Minimize F-term SUGRA potential to find T_min",
                        "V_racetrack = V_SUGRA(T_min) [AdS minimum]",
                        "V_torsion = (chi_eff/b3^3) * M_Pl^4 [topological]",
                        "V_bare = V_racetrack + V_torsion",
                    ],
                },
                terms={
                    "V_racetrack": "F-term SUGRA racetrack minimum ~ -3.7e-5 M_Pl^4",
                    "V_torsion": "G2 torsion potential ~ 0.01042 M_Pl^4",
                    "T_min": "Stabilized Kahler modulus ~ 37.85",
                },
            ),
            Formula(
                id="dynamical-lambda-vtorsion",
                label="(DL.3)",
                latex=(
                    r"V_{\text{torsion}} = \frac{\chi_{\text{eff}}}{b_3^3} "
                    r"\, M_{\text{Pl}}^4 = \frac{144}{24^3} \, M_{\text{Pl}}^4 "
                    r"\approx 0.01042 \, M_{\text{Pl}}^4"
                ),
                plain_text="V_torsion = (chi_eff / b3^3) * M_Pl^4 = 144/13824 ~ 0.01042",
                category="DERIVED",
                description=(
                    "Torsion potential from G2 manifold topology. chi_eff = 144 "
                    "and b3 = 24 are topological invariants, making this term "
                    "fully DERIVED."
                ),
                inputParams=["topology.elder_kads"],
                outputParams=["dynamical_lambda.V_torsion"],
                input_params=["topology.elder_kads"],
                output_params=["dynamical_lambda.V_torsion"],
                derivation={
                    "method": "topological",
                    "steps": [
                        "chi_eff = b3^2/4 = 576/4 = 144 (Euler characteristic)",
                        "V_torsion = chi_eff / b3^3 = 144/13824",
                    ],
                },
                terms={
                    "chi_eff": "= 144 = b3^2/4, effective Euler characteristic",
                    "b3": "= 24, third Betti number of G2 manifold",
                },
            ),
            Formula(
                id="dynamical-lambda-entropy-naive",
                label="(DL.4)",
                latex=(
                    r"S_{\text{naive}} = (N_{\text{bridges}} + "
                    r"\kappa_{\text{sampler}}) \times T_{\min} = "
                    r"14 \times T_{\min}"
                ),
                plain_text="S_naive = (N_bridges + kappa_sampler) * T_min = 14 * T_min",
                category="PLAUSIBLE",
                description=(
                    "Naive late-time entropy estimate. Each bridge contributes "
                    "S_vN ~ T_min and the sampler contributes kappa * T_min. "
                    "HONESTY: This gives S ~ 530, not the required S ~ 280. "
                    "The factor-of-2 discrepancy is an open problem."
                ),
                inputParams=[
                    "dynamical_lambda.V_bare",
                ],
                outputParams=[
                    "dynamical_lambda.S_Pneuma_naive",
                ],
                input_params=[
                    "dynamical_lambda.V_bare",
                ],
                output_params=[
                    "dynamical_lambda.S_Pneuma_naive",
                ],
                derivation={
                    "method": "thermal_entropy_estimate",
                    "steps": [
                        "Each bridge: S_i ~ T_min (von Neumann of thermal state)",
                        "12 bridges: S_bridge = 12 * T_min",
                        "Sampler: S_sampler ~ kappa * T_min = 2 * T_min",
                        "Total: S_naive = 14 * T_min",
                        "WARNING: This is an OVERESTIMATE giving S ~ 530",
                    ],
                    "honesty": (
                        "S ~ 530 overshoots required S ~ 280 by factor ~2. "
                        "Possible causes: overcounting of states, neglect of "
                        "correlations between bridges, partial thermalization."
                    ),
                },
                terms={
                    "N_bridges": "= 12 = b3/2, bridge pair count",
                    "kappa_sampler": "= 2 = dim(S^{2,0}), sampler diffusion",
                    "T_min": "Stabilized Kahler modulus ~ 37.85",
                },
            ),
            Formula(
                id="dynamical-lambda-torsion-funnel",
                label="(DL.5)",
                latex=(
                    r"S_{\text{corrected}} = S_{\text{naive}} - "
                    r"\mathcal{I}_{\text{torsion}}, \quad "
                    r"\mathcal{I}_{\text{torsion}} \approx 250 \;"
                    r"\text{(FITTED)}"
                ),
                plain_text=(
                    "S_corrected = S_naive - I_torsion, "
                    "I_torsion ~ 250 (FITTED, not derived)"
                ),
                category="FITTED",
                description=(
                    "Torsion funnel correction to the naive entropy. "
                    "Subtracts a torsion integral from S_naive ~ 530 to get "
                    "S_corrected ~ 280, yielding exp(-280) ~ 10^{-122} = Lambda_obs. "
                    "CRITICAL: The torsion integral ~ 250 is FITTED to match "
                    "Lambda_obs. No natural G2 formula independently produces this "
                    "value. Closest candidate: chi_eff * ln(T_min) ~ 523 (109% off). "
                    "Gemini 2.5 Flash debate (3 rounds, 2026-03-20) classified this "
                    "as FITTED."
                ),
                inputParams=[
                    "dynamical_lambda.S_Pneuma_naive",
                ],
                outputParams=[
                    "dynamical_lambda.torsion_funnel.S_corrected",
                ],
                input_params=[
                    "dynamical_lambda.S_Pneuma_naive",
                ],
                output_params=[
                    "dynamical_lambda.torsion_funnel.S_corrected",
                ],
                derivation={
                    "method": "torsion_funnel_correction",
                    "steps": [
                        "S_naive = (N_bridges + kappa) * T_min ~ 530",
                        "S_required = -ln(Lambda_obs / V_bare) ~ 280",
                        "I_torsion = S_naive - S_required ~ 250",
                        "FITTED: I_torsion chosen to match Lambda_obs",
                        "No natural G2 formula gives 250 independently",
                    ],
                    "candidates_evaluated": [
                        "chi_eff * ln(T_min) = 523 (109% off)",
                        "b3 * ln(T_min) = 87 (-65% off)",
                        "(chi_eff - b3) * ln(T_min) = 436 (75% off)",
                        "b3^2 / ln(T_min) = 158 (-37% off)",
                    ],
                    "honesty": (
                        "FITTED: The torsion integral = 250 is chosen to match "
                        "Lambda_obs. This is honestly acknowledged. The entropy "
                        "suppression MECHANISM is plausible (instanton analogy), "
                        "but the specific entropy VALUE is not derived from "
                        "first principles. Gemini 2.5 Flash (2026-03-20) concurs."
                    ),
                    "gemini_debate": {
                        "date": "2026-03-20",
                        "model": "gemini-2.5-flash",
                        "classification": "FITTED",
                        "summary": (
                            "Round 1: torsion_integral=250 is circular. "
                            "Round 2: Mutual information alternative also circular "
                            "in value. Round 3: FITTED."
                        ),
                    },
                },
                terms={
                    "S_naive": "Naive entropy ~ 530 (overestimate)",
                    "I_torsion": "Torsion funnel integral ~ 250 (FITTED)",
                    "S_corrected": "Corrected entropy ~ 280",
                },
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for dynamical Lambda."""
        # Compute results if not already done
        if self._results is None:
            self._results = self.compute_lambda_prediction()

        r = self._results

        return [
            Parameter(
                path="dynamical_lambda.V_racetrack",
                name="Racetrack Potential Minimum",
                units="M_Pl^4",
                status="PLAUSIBLE",
                description=(
                    "F-term SUGRA racetrack potential at stabilized modulus T_min. "
                    "Negative (AdS minimum). Depends on instanton prefactors A, B "
                    "which are PLAUSIBLE, not uniquely fixed by topology."
                ),
                derivation_formula="dynamical-lambda-vbare",
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.V_torsion",
                name="G2 Torsion Potential",
                units="M_Pl^4",
                status="DERIVED",
                description=(
                    "Torsion potential from G2 topology: V = chi_eff/b3^3 = "
                    "144/13824 ~ 0.01042 M_Pl^4. Fully DERIVED from topological "
                    "invariants."
                ),
                derivation_formula="dynamical-lambda-vtorsion",
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.V_bare",
                name="Bare Vacuum Potential",
                units="M_Pl^4",
                status="PLAUSIBLE",
                description=(
                    "Total bare potential before entropy suppression: "
                    "V_bare = V_racetrack + V_torsion."
                ),
                derivation_formula="dynamical-lambda-vbare",
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.S_Pneuma_naive",
                name="Naive Pneuma Entropy",
                units="dimensionless",
                status="PLAUSIBLE",
                description=(
                    "Naive late-time entropy estimate: S = (N_bridges + kappa) * T_min. "
                    "HONESTY: Gives S ~ 530, not required S ~ 280. Factor-of-2 problem "
                    "in the exponent is unresolved."
                ),
                derivation_formula="dynamical-lambda-entropy-naive",
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.S_Pneuma_required",
                name="Required Pneuma Entropy",
                units="dimensionless",
                status="TARGET",
                description=(
                    "Entropy required for V_eff to match Lambda_obs: "
                    "S = -ln(Lambda_obs / V_bare). This is the TARGET, "
                    "not a derivation."
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.V_eff_naive",
                name="Effective Potential (naive S)",
                units="M_Pl^4",
                status="PLAUSIBLE",
                description=(
                    "V_eff = V_bare * exp(-S_naive). Using the naive entropy "
                    "estimate, this overshoots the suppression."
                ),
                derivation_formula="dynamical-lambda-veff",
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.V_eff_target",
                name="Effective Potential (target S)",
                units="M_Pl^4",
                status="TARGET",
                description=(
                    "V_eff = V_bare * exp(-S_required) = Lambda_obs by "
                    "construction. This is what a successful derivation "
                    "of S_Pneuma would produce."
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.Lambda_obs",
                name="Observed Cosmological Constant",
                units="M_Pl^4",
                status="INPUT",
                description=(
                    "Lambda_obs ~ 2.846e-122 M_Pl^4 from Planck 2018 + DESI."
                ),
                experimental_value=self.LAMBDA_OBS_MPL4,
            ),
            Parameter(
                path="dynamical_lambda.gap_orders_naive",
                name="Gap with Naive Entropy",
                units="orders of magnitude",
                status="DIAGNOSTIC",
                description=(
                    "log10(|V_eff_naive / Lambda_obs|). Measures how many "
                    "orders of magnitude the naive prediction is off."
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.gap_orders_target",
                name="Gap with Target Entropy",
                units="orders of magnitude",
                status="DIAGNOSTIC",
                description=(
                    "log10(|V_eff_target / Lambda_obs|). Should be ~0 by "
                    "construction."
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="dynamical_lambda.classification",
                name="Mechanism Classification",
                units="string",
                status="DIAGNOSTIC",
                description=(
                    "Honesty classification of the dynamical Lambda mechanism."
                ),
                no_experimental_value=True,
            ),
        ]


# =========================================================================
# STANDALONE EXECUTION
# =========================================================================

def _run_standalone():
    """Run dynamical Lambda relaxation as standalone script."""
    print("=" * 72)
    print("DYNAMICAL LAMBDA RELAXATION via SAMPLER ENTROPY")
    print("Principia Metaphysica v24.3")
    print("=" * 72)

    sim = DynamicalLambdaRelaxation()
    results = sim.compute_lambda_prediction()

    print()
    print("--- Bare Potential Components ---")
    print(f"  T_min (stabilized modulus):  {results['T_min']:.4f}")
    print(f"  V_racetrack(T_min):          {results['V_racetrack']:.6e} M_Pl^4")
    print(f"  V_torsion (chi_eff/b3^3):    {results['V_torsion']:.6e} M_Pl^4")
    print(f"  V_bare = V_race + V_torsion: {results['V_bare']:.6e} M_Pl^4")

    print()
    print("--- Entropy Estimates ---")
    print(f"  S_Pneuma (naive):    {results['S_Pneuma_naive']:.2f}")
    print(f"  S_Pneuma (required): {results['S_Pneuma_required']:.2f}")
    print(f"  Entropy gap:         {results['entropy_gap']:.2f}")
    print(f"  Entropy ratio:       {results['entropy_ratio']:.3f}x")

    print()
    print("--- Effective Potential ---")
    print(f"  V_eff (naive S):     {results['V_eff_naive']:.6e} M_Pl^4")
    print(f"  V_eff (target S):    {results['V_eff_target']:.6e} M_Pl^4")
    print(f"  Lambda_obs:          {results['Lambda_obs']:.6e} M_Pl^4")

    print()
    print("--- Gap Analysis ---")
    print(f"  Gap (naive S):       {results['gap_orders_naive']:.1f} orders")
    print(f"  Gap (target S):      {results['gap_orders_target']:.1f} orders")
    if math.isfinite(results.get('improvement_from_bare', float('nan'))):
        print(f"  Improvement from bare: {results['improvement_from_bare']:.1f} orders")

    print()
    print(f"--- Classification ---")
    print(f"  {results['classification']}")

    # Torsion funnel analysis
    print()
    print("--- Torsion Funnel Calibration (v24.3) ---")
    tf = sim.compute_V_eff_with_torsion_funnel()
    if tf.get('status') == 'UNFOUNDED':
        print(f"  UNFOUNDED: {tf['reason']}")
    else:
        print(f"  S_naive:                 {tf['S_naive']:.2f}")
        print(f"  S_required:              {tf['S_required']:.2f}")
        print(f"  Torsion integral needed: {tf['torsion_integral_needed']:.2f}")
        print(f"  S_corrected:             {tf['S_corrected']:.2f}")
        print(f"  V_eff (corrected):       {tf['V_eff_corrected']:.6e} M_Pl^4")
        print(f"  Gap (corrected):         {tf['gap_orders_corrected']:.2f} orders")
        print()
        print("  Candidate torsion integrals from G2 topology:")
        for key, cand in tf['candidates']['candidates'].items():
            print(f"    {key}: {cand['value']:.2f} ({cand['deviation_pct']:+.1f}% off)")
        print()
        print(f"  Closest: {tf['closest_candidate']} = {tf['closest_value']:.2f} "
              f"({tf['closest_deviation_pct']:+.1f}% off)")
        print(f"  Natural match found: {tf['any_natural_match']}")
        print()
        print(f"  CLASSIFICATION: {tf['classification']}")
        print(f"  {tf['classification_detail']}")

    # Also show original formulation for comparison
    print()
    print("--- Original Formulation (for comparison) ---")
    original = sim.compute_effective_potential_original()
    print(f"  {original['formulation']}")
    print(f"  V_eff (original):    {original['V_eff']:.6e} M_Pl^4")
    print(f"  Critique: {original['critique']}")

    print()
    print("=" * 72)


if __name__ == "__main__":
    _run_standalone()
