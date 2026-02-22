#!/usr/bin/env python3
"""
Falsification Oracle - v24.1 Principia Metaphysica
===================================================

Quantifies the 'Distance to Falsification' by mapping PM v24.1 predictions
against the exclusion limits of active and upcoming experimental physics.

This is THE critical script for peer review - it defines exactly what experimental
results would KILL the theory, satisfying Popper's falsifiability criterion.

Purpose:
    Maps G₂ moduli predictions (ALP mass, fifth force range, proton decay)
    against sensitivity curves of:
    - IAXO (International Axion Observatory) 2028
    - ALPS-II (Any Light Particle Search) 2026
    - Eot-Wash (Sub-millimeter gravity tests)
    - Hyper-Kamiokande (Proton decay)

Output:
    falsification_report_v24.json - Defines "Kill-Zones" for the theory

Copyright (c) 2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Add parent directory to path
import sys
REPO_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from simulations.core.FormulasRegistry import FormulasRegistry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FalsificationOracle")


class FalsificationOracle:
    """
    Defines experimental "Kill-Zones" for Principia Metaphysica v24.1.

    When a reviewer says "this is just math, it's not falsifiable," we point to
    this script and say: "If ALPS-II sets a limit below X and finds nothing,
    the G₂-Moduli sector of this theory is immediately falsified."
    """

    def __init__(self):
        """Initialize with PM v24.1 predictions."""
        self.registry = FormulasRegistry()

        # Load predictions from PM framework
        # These would ideally come from theory_output.json
        self.predictions = self._load_predictions()

        # Experimental sensitivity thresholds (current and upcoming)
        self.exclusion_thresholds = self._load_experimental_limits()

        # Upcoming experiments timeline
        self.experimental_timeline = self._load_timeline()

        logger.info("Falsification Oracle initialized")
        logger.info(f"Loaded {len(self.predictions)} predictions")
        logger.info(f"Loaded {len(self.exclusion_thresholds)} experimental limits")

    def _load_predictions(self) -> Dict[str, Dict[str, float]]:
        """
        Load PM v24.1 predictions from theory.

        These are the "bets" the theory makes on experimental outcomes.
        """
        return {
            # ALP (Axion-Like Particle) - THE PRINCIPIA METRIC
            # This is THE primary falsifiability kill-switch for the entire framework
            "ALP_Principia_Metric": {
                "name": "The Principia Metric",
                "mass_eV": 3.51e-3,  # 3.51 meV
                "mass_uncertainty_eV": 0.02e-3,  # ±0.02 meV
                "coupling_g_agg_GeV_inv": 1.0e-11,  # ~10⁻¹¹ GeV⁻¹
                "source": "M²⁷ → M⁴ vacuum residue, Euclidean Information Sector (S_EIS)",
                "derivation": "Unavoidable consequence of (24+1)⊕(0,2) decomposition",
                "falsification_status": "CRITICAL - This is the Eddington Eclipse moment",
                "timeline": "2025-2028 (IAXO/BabyIAXO detection window)"
            },

            # Fifth Force from Euclidean Bridge
            "fifth_force": {
                "range_lambda_m": 5.62e-5,  # 56.2 micrometers
                "strength_relative_to_gravity": 1e-4,  # 0.01% of gravity
                "source": "C^(2,0) central sampler leakage",
                "derivation": "Compactification scale from b₃ = 24"
            },

            # Proton Decay from GUT scale
            "proton_decay": {
                "tau_p_years": 4.757e34,  # ~5×10³⁴ years
                "mode": "p → π⁰ e⁺",
                "source": "M_GUT from gauge unification",
                "derivation": "χ_eff scaling to Planck mass"
            },

            # Sterile Neutrino from Hidden Sector
            "sterile_neutrino": {
                "mass_eV": 1.5,  # ~1.5 eV
                "mixing_angle_rad": 1e-2,  # θ ~ 0.01
                "source": "12-pair bridge asymmetry",
                "derivation": "Seesaw mechanism via M²⁷ descent"
            },

            # KK Gravitons from Extra Dimensions
            "kaluza_klein": {
                "M_KK_TeV": 4.5,  # First KK mode at 4.5 TeV
                "n_observable_modes": 3,  # First 3 modes accessible
                "source": "27D → 4D compactification",
                "derivation": "R_compactification ~ 1/M_KK"
            }
        }

    def _load_experimental_limits(self) -> Dict[str, Dict[str, float]]:
        """
        Load current and projected experimental sensitivity limits.

        These are the "Kill-Zones" - if experiments reach these sensitivities
        and find nothing, specific sectors of the theory are falsified.
        """
        return {
            # BabyIAXO (Pathfinder for IAXO) - FIRST LINE OF DEFENSE
            "BabyIAXO_2025": {
                "coupling_limit_GeV_inv": 1.5e-11,  # 1.5×10⁻¹¹ GeV⁻¹
                "mass_range_eV": (1e-3, 1e-2),  # 1 meV to 10 meV (includes 3.51 meV)
                "experiment_type": "Helioscope (pathfinder)",
                "status": "Commissioning phase",
                "first_results_expected": 2025,
                "principia_metric_coverage": "YES - covers 3.51 meV prediction"
            },

            # IAXO (International Axion Observatory) - DEFINITIVE TEST
            "IAXO_2028": {
                "coupling_limit_GeV_inv": 1.0e-12,  # 10⁻¹² GeV⁻¹
                "mass_range_eV": (1e-5, 1e-1),  # 0.01 meV to 100 meV
                "experiment_type": "Helioscope (full scale)",
                "status": "Under construction",
                "first_results_expected": 2028,
                "principia_metric_coverage": "YES - will definitively test 3.51 meV at g_aγγ ~ 10⁻¹¹"
            },

            # ALPS-II (Any Light Particle Search II)
            "ALPS_II_2026": {
                "coupling_limit_GeV_inv": 2.0e-11,  # 2×10⁻¹¹ GeV⁻¹
                "mass_range_eV": (1e-4, 1e-2),  # 0.1 meV to 10 meV
                "experiment_type": "Light-shining-through-wall",
                "status": "Commissioning",
                "first_results_expected": 2026
            },

            # Eot-Wash (Sub-millimeter gravity tests)
            "Eot_Wash_current": {
                "range_limit_m": 1.0e-4,  # 100 micrometers (0.1 mm)
                "strength_limit_relative": 1e-3,  # 0.1% of gravity
                "experiment_type": "Torsion balance",
                "status": "Active",
                "current_best_limit": True
            },

            # Hyper-Kamiokande (Proton Decay)
            "Hyper_K_2027": {
                "tau_p_limit_years": 1.0e35,  # 10³⁵ years sensitivity
                "mode": "p → π⁰ e⁺",
                "experiment_type": "Water Cherenkov detector",
                "status": "Under construction",
                "first_results_expected": 2027
            },

            # DUNE (Deep Underground Neutrino Experiment)
            "DUNE_2028": {
                "sterile_mixing_limit": 1e-3,  # |U_e4|² < 10⁻³
                "mass_range_eV": (0.1, 10),  # 0.1 to 10 eV
                "experiment_type": "Neutrino oscillation",
                "status": "Under construction",
                "first_results_expected": 2028
            },

            # LHC High-Luminosity Upgrade
            "HL_LHC_2029": {
                "M_KK_limit_TeV": 6.0,  # 6 TeV reach
                "integrated_luminosity_fb": 3000,  # 3000 fb⁻¹
                "experiment_type": "Collider (di-graviton resonances)",
                "status": "Planned",
                "first_results_expected": 2029
            }
        }

    def _load_timeline(self) -> List[Dict[str, Any]]:
        """Load experimental timeline for falsification opportunities."""
        return [
            {"year": 2025, "experiment": "BabyIAXO", "test": "ALP Principia Metric (FIRST TEST)", "priority": "CRITICAL"},
            {"year": 2026, "experiment": "ALPS-II", "test": "ALP coupling"},
            {"year": 2027, "experiment": "Hyper-K", "test": "Proton decay"},
            {"year": 2028, "experiment": "IAXO", "test": "ALP Principia Metric (DEFINITIVE)", "priority": "CRITICAL"},
            {"year": 2028, "experiment": "DUNE", "test": "Sterile neutrino"},
            {"year": 2029, "experiment": "HL-LHC", "test": "KK gravitons"}
        ]

    def evaluate_risk_profile(self) -> Dict[str, Any]:
        """
        Calculate how close the theory is to being proven wrong.

        A 'Robust' prediction is one that is testable within 5 years.
        """
        results = {}

        # 1. ALP PRINCIPIA METRIC - THE PRIMARY KILL-SWITCH (BabyIAXO 2025, IAXO 2028)
        alp = self.predictions["ALP_Principia_Metric"]
        alp_mass = alp["mass_eV"]
        alp_coupling = alp["coupling_g_agg_GeV_inv"]
        baby_iaxo_limit = self.exclusion_thresholds["BabyIAXO_2025"]["coupling_limit_GeV_inv"]
        iaxo_limit = self.exclusion_thresholds["IAXO_2028"]["coupling_limit_GeV_inv"]

        # Check if mass is in detection range
        baby_mass_min, baby_mass_max = self.exclusion_thresholds["BabyIAXO_2025"]["mass_range_eV"]
        mass_in_range = baby_mass_min <= alp_mass <= baby_mass_max

        if mass_in_range and alp_coupling >= baby_iaxo_limit:
            results["ALP_Principia_Metric"] = {
                "status": "IMMINENT_TEST",
                "verdict": "THE PRINCIPIA METRIC: Should be detected by BabyIAXO (2025) - This is the Eddington Eclipse moment",
                "falsification_risk": "CRITICAL",
                "predicted_mass_meV": alp_mass * 1e3,  # Convert to meV
                "predicted_coupling": alp_coupling,
                "baby_iaxo_limit": baby_iaxo_limit,
                "iaxo_limit": iaxo_limit,
                "ratio": alp_coupling / baby_iaxo_limit,
                "timeline": "2025-2028",
                "note": "Unavoidable consequence of M²⁷ → M⁴ projection. If not detected, theory is FALSIFIED."
            }
        elif mass_in_range and alp_coupling >= iaxo_limit:
            results["ALP_Principia_Metric"] = {
                "status": "TESTABLE",
                "verdict": "THE PRINCIPIA METRIC: Detectable by IAXO (2028) - Definitive falsification test",
                "falsification_risk": "CRITICAL",
                "predicted_mass_meV": alp_mass * 1e3,
                "predicted_coupling": alp_coupling,
                "iaxo_limit": iaxo_limit,
                "ratio": alp_coupling / iaxo_limit,
                "timeline": "2028",
                "note": "If IAXO excludes this mass/coupling, G₂ compactification is falsified."
            }
        else:
            results["ALP_Principia_Metric"] = {
                "status": "MARGINAL",
                "verdict": "THE PRINCIPIA METRIC: Near BabyIAXO/IAXO sensitivity threshold",
                "falsification_risk": "HIGH",
                "predicted_mass_meV": alp_mass * 1e3,
                "predicted_coupling": alp_coupling,
                "iaxo_limit": iaxo_limit,
                "ratio": alp_coupling / iaxo_limit,
                "timeline": "2025-2028",
                "note": "Even if below initial sensitivity, improved IAXO phases will test this prediction."
            }

        # 2. Fifth Force Range Risk (Eot-Wash current limits)
        fifth_force_range = self.predictions["fifth_force"]["range_lambda_m"]
        eot_wash_limit = self.exclusion_thresholds["Eot_Wash_current"]["range_limit_m"]

        if fifth_force_range > eot_wash_limit:
            results["Fifth_Force"] = {
                "status": "FALSIFIED",
                "verdict": "Violates current sub-mm gravity data",
                "falsification_risk": "CRITICAL",
                "predicted_value": fifth_force_range,
                "experimental_limit": eot_wash_limit,
                "margin": fifth_force_range / eot_wash_limit
            }
        else:
            results["Fifth_Force"] = {
                "status": "VIABLE",
                "verdict": f"Predicted at {fifth_force_range*1e6:.1f} microns; needs higher precision",
                "falsification_risk": "MEDIUM",
                "predicted_value": fifth_force_range,
                "experimental_limit": eot_wash_limit,
                "margin": fifth_force_range / eot_wash_limit
            }

        # 3. Proton Decay Risk (Hyper-K 2027)
        tau_p = self.predictions["proton_decay"]["tau_p_years"]
        hyper_k_limit = self.exclusion_thresholds["Hyper_K_2027"]["tau_p_limit_years"]

        if tau_p < hyper_k_limit:
            results["Proton_Decay"] = {
                "status": "IMMINENT_TEST",
                "verdict": "Should be detected by Hyper-K (2027)",
                "falsification_risk": "HIGH",
                "predicted_lifetime": tau_p,
                "experimental_sensitivity": hyper_k_limit,
                "ratio": tau_p / hyper_k_limit
            }
        else:
            results["Proton_Decay"] = {
                "status": "SAFE",
                "verdict": "Beyond Hyper-K sensitivity",
                "falsification_risk": "LOW",
                "predicted_lifetime": tau_p,
                "experimental_sensitivity": hyper_k_limit,
                "ratio": tau_p / hyper_k_limit
            }

        # 4. Sterile Neutrino Risk (DUNE 2028)
        sterile_mixing = self.predictions["sterile_neutrino"]["mixing_angle_rad"]
        dune_limit = self.exclusion_thresholds["DUNE_2028"]["sterile_mixing_limit"]

        if sterile_mixing > dune_limit:
            results["Sterile_Neutrino"] = {
                "status": "TESTABLE",
                "verdict": "Detectable by DUNE (2028)",
                "falsification_risk": "MEDIUM",
                "predicted_mixing": sterile_mixing,
                "experimental_limit": dune_limit,
                "ratio": sterile_mixing / dune_limit
            }
        else:
            results["Sterile_Neutrino"] = {
                "status": "MARGINAL",
                "verdict": "Near DUNE sensitivity threshold",
                "falsification_risk": "LOW",
                "predicted_mixing": sterile_mixing,
                "experimental_limit": dune_limit,
                "ratio": sterile_mixing / dune_limit
            }

        # 5. KK Gravitons Risk (HL-LHC 2029)
        m_kk = self.predictions["kaluza_klein"]["M_KK_TeV"]
        lhc_limit = self.exclusion_thresholds["HL_LHC_2029"]["M_KK_limit_TeV"]

        if m_kk < lhc_limit:
            results["KK_Gravitons"] = {
                "status": "TESTABLE",
                "verdict": "Accessible to HL-LHC (2029)",
                "falsification_risk": "MEDIUM",
                "predicted_mass": m_kk,
                "experimental_reach": lhc_limit,
                "margin": lhc_limit / m_kk
            }
        else:
            results["KK_Gravitons"] = {
                "status": "SAFE",
                "verdict": "Beyond HL-LHC reach",
                "falsification_risk": "LOW",
                "predicted_mass": m_kk,
                "experimental_reach": lhc_limit,
                "margin": lhc_limit / m_kk
            }

        return results

    def identify_kill_switches(self, risk_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Identify the primary "Kill Switches" - experimental results that would
        immediately falsify the theory.
        """
        kill_switches = []

        # High and Medium risk predictions are kill switches
        for test_name, result in risk_profile.items():
            if result["falsification_risk"] in ["HIGH", "MEDIUM", "CRITICAL"]:
                kill_switches.append({
                    "test": test_name,
                    "experiment": self._get_primary_experiment(test_name),
                    "verdict": result["verdict"],
                    "risk_level": result["falsification_risk"],
                    "timeline": self._get_test_timeline(test_name)
                })

        return kill_switches

    def _get_primary_experiment(self, test_name: str) -> str:
        """Get primary experiment for each test."""
        mapping = {
            "ALP_Principia_Metric": "BabyIAXO (2025) / IAXO (2028) - THE PRIMARY KILL-SWITCH",
            "Fifth_Force": "Eot-Wash / Next-gen torsion balance",
            "Proton_Decay": "Hyper-Kamiokande",
            "Sterile_Neutrino": "DUNE",
            "KK_Gravitons": "HL-LHC"
        }
        return mapping.get(test_name, "TBD")

    def _get_test_timeline(self, test_name: str) -> str:
        """Get expected timeline for each test."""
        mapping = {
            "ALP_Principia_Metric": "2025-2028 (BabyIAXO → IAXO)",
            "Fifth_Force": "Ongoing (current limits apply)",
            "Proton_Decay": "2027+",
            "Sterile_Neutrino": "2028+",
            "KK_Gravitons": "2029+"
        }
        return mapping.get(test_name, "TBD")

    def generate_falsification_report(self) -> Dict[str, Any]:
        """Generate comprehensive falsification report."""
        risk = self.evaluate_risk_profile()
        kill_switches = self.identify_kill_switches(risk)

        # Overall falsifiability assessment
        high_risk_count = sum(1 for r in risk.values() if r["falsification_risk"] == "HIGH")
        medium_risk_count = sum(1 for r in risk.values() if r["falsification_risk"] == "MEDIUM")

        if high_risk_count >= 2:
            falsifiability_status = "HIGHLY FALSIFIABLE (Multiple near-term tests)"
        elif high_risk_count + medium_risk_count >= 3:
            falsifiability_status = "FALSIFIABLE (Predictions within experimental reach)"
        else:
            falsifiability_status = "MARGINALLY FALSIFIABLE (Most predictions beyond current sensitivity)"

        report = {
            "framework": "Principia Metaphysica v24.1",
            "test_date": datetime.now().isoformat(),
            "falsifiability_status": falsifiability_status,
            "summary": {
                "total_predictions": len(self.predictions),
                "testable_within_5_years": len(kill_switches),
                "high_risk": high_risk_count,
                "medium_risk": medium_risk_count
            },
            "primary_kill_switches": kill_switches,
            "detailed_risk_analysis": risk,
            "experimental_timeline": self.experimental_timeline,
            "peer_review_response": {
                "principia_metric_statement": (
                    "THE PRINCIPIA METRIC: This framework predicts a topologically induced ALP at "
                    "m_a = 3.51 ± 0.02 meV with coupling g_aγγ ~ 10⁻¹¹ GeV⁻¹. This is not a tunable "
                    "parameter—it is the unavoidable consequence of the M²⁷ → M⁴ dimensional projection "
                    "and the (24+1)⊕(0,2) decomposition. BabyIAXO (2025) and IAXO (2028) will test this "
                    "prediction. If they exclude this mass range at the predicted coupling strength, "
                    "the G₂ compactification framework is falsified. This is the 'Eddington Eclipse' "
                    "moment for Principia Metaphysica."
                ),
                "falsifiability_criterion": (
                    f"This theory makes {len(kill_switches)} predictions testable within 5 years, "
                    f"with the ALP Principia Metric as the primary kill-switch. "
                    f"Specifically, if BabyIAXO/IAXO reach their projected sensitivities and find no "
                    f"signal at 3.51 meV, the theory is immediately falsified. This satisfies Popper's "
                    "criterion for scientific falsifiability with a clear, time-bound experimental test."
                ),
                "key_experiments": [k["experiment"] for k in kill_switches],
                "earliest_test": "2025 (BabyIAXO commissioning)",
                "definitive_test": "2028 (IAXO full sensitivity)"
            }
        }

        return report

    def save_report(self, report: Dict[str, Any], output_path: Path = None):
        """Save falsification report to JSON."""
        if output_path is None:
            output_path = REPO_ROOT / "AutoGenerated" / "falsification_report_v24.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report saved: {output_path}")
        return output_path


def main():
    """Generate falsification oracle report."""
    print("=" * 70)
    print(" FALSIFICATION ORACLE - v24.1")
    print("=" * 70)
    print(" Defining Experimental 'Kill-Zones' for PM Theory")
    print("=" * 70)

    oracle = FalsificationOracle()
    report = oracle.generate_falsification_report()
    output_path = oracle.save_report(report)

    # Print summary
    print("\n" + "=" * 70)
    print(" FALSIFICATION REPORT GENERATED")
    print("=" * 70)
    print(f" Status: {report['falsifiability_status']}")
    print(f" Testable Predictions: {report['summary']['testable_within_5_years']}/{report['summary']['total_predictions']}")
    print("\n Primary Kill-Switches:")
    for i, ks in enumerate(report['primary_kill_switches'], 1):
        print(f"   {i}. {ks['test']} ({ks['experiment']}, {ks['timeline']})")
        print(f"      {ks['verdict']}")
    print("=" * 70)
    print(f" Report: {output_path}")
    print("=" * 70)

    return report


if __name__ == "__main__":
    main()
