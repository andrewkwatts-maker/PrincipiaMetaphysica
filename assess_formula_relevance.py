"""
Formula Relevance Assessment for v8.4 Framework

Analyzes all 259 formulas and categorizes them as:
- KEEP: Essential formulas actively used in v8.4
- UPDATE: Formulas that need correction to match v8.4
- REMOVE: Deprecated formulas from earlier versions

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
from pathlib import Path
from collections import defaultdict

# Load simulation output to know what's currently used
with open('theory_output.json', 'r') as f:
    simulation = json.load(f)

# Load orphaned formula analysis
with open('orphaned_formulas_analysis.json', 'r', encoding='utf-8') as f:
    formula_data = json.load(f)

class FormulaRelevanceAssessor:
    def __init__(self, simulation_data, formula_data):
        self.simulation = simulation_data
        self.formulas = formula_data
        self.assessments = {
            'KEEP': [],
            'UPDATE': [],
            'REMOVE': [],
            'REVIEW': []
        }

    def assess_all(self):
        """Assess relevance of all unique formulas"""
        unique_formulas = self.formulas.get('unique_formulas', [])

        for formula in unique_formulas:
            assessment = self.assess_formula(formula)
            self.assessments[assessment['action']].append(assessment)

        return self.assessments

    def assess_formula(self, formula):
        """Assess a single formula against v8.4 framework"""
        text = formula.get('text', '').lower()
        category = formula.get('category', 'other')
        file = formula.get('file', '')

        # Default assessment
        assessment = {
            'formula': formula['text'][:100],
            'category': category,
            'file': file,
            'action': 'REVIEW',
            'reason': 'Needs manual review',
            'simulation_backed': False
        }

        # === KEEP: Essential v8.4 Formulas ===

        # Proton decay (from simulation)
        if 'proton' in text or 'tau_p' in text or 'm_gut' in text:
            if self._check_simulation_backed('proton_decay'):
                assessment['action'] = 'KEEP'
                assessment['reason'] = 'Proton decay actively simulated in v8.4'
                assessment['simulation_backed'] = True
                assessment['pm_values'] = ['tau_p_central', 'M_GUT', 'alpha_GUT_inv']

        # PMNS matrix (from simulation)
        elif 'pmns' in text or 'theta_12' in text or 'theta_23' in text or 'theta_13' in text or 'delta_cp' in text:
            if self._check_simulation_backed('pmns_matrix'):
                assessment['action'] = 'KEEP'
                assessment['reason'] = 'PMNS mixing angles from pmns_full_matrix.py simulation'
                assessment['simulation_backed'] = True
                assessment['pm_values'] = ['theta_23', 'theta_12', 'theta_13', 'delta_cp']

        # Dark energy w(z) evolution (from simulation)
        elif 'w(z)' in text or 'w_0' in text or 'w_a' in text or 'dark energy' in text:
            if self._check_simulation_backed('dark_energy'):
                assessment['action'] = 'KEEP'
                assessment['reason'] = 'Dark energy evolution from wz_evolution_desi_dr2.py'
                assessment['simulation_backed'] = True
                assessment['pm_values'] = ['w0_PM', 'wa_PM_effective', 'functional_test_sigma_preference']

        # KK spectrum (from simulation)
        elif 'kk' in text or 'kaluza' in text or 'm_kk' in text:
            if self._check_simulation_backed('kk_spectrum'):
                assessment['action'] = 'KEEP'
                assessment['reason'] = 'KK spectrum from kk_spectrum_full.py simulation'
                assessment['simulation_backed'] = True
                assessment['pm_values'] = ['m1', 'm2', 'm3', 'BR_gg', 'BR_qq']

        # Neutrino mass ordering (from simulation)
        elif 'mass ordering' in text or 'inverted' in text or 'normal hierarchy' in text:
            if self._check_simulation_backed('neutrino_mass_ordering'):
                assessment['action'] = 'KEEP'
                assessment['reason'] = 'Mass ordering from neutrino_mass_ordering.py (IH 85.5%)'
                assessment['simulation_backed'] = True
                assessment['pm_values'] = ['prob_IH_mean', 'ordering_predicted']

        # Generation count (topology)
        elif 'generation' in text or 'chi_eff' in text or '144' in formula['text'] or 'n_gen' in text:
            assessment['action'] = 'KEEP'
            assessment['reason'] = 'Generation formula from G₂ topology: n_gen = χ_eff/48 = 3'
            assessment['simulation_backed'] = True
            assessment['pm_values'] = ['chi_eff', 'n_gen']

        # Dimensional framework (shared dimensions)
        elif 'd_eff' in text or 'alpha_4' in text or 'alpha_5' in text or '12.589' in formula['text']:
            assessment['action'] = 'KEEP'
            assessment['reason'] = 'Shared dimensions from TCS G₂ construction'
            assessment['simulation_backed'] = True
            assessment['pm_values'] = ['d_eff', 'alpha_4', 'alpha_5', 'w0_from_d_eff']

        # Einstein field equations
        elif 'einstein' in text or 'r_μν' in text or 'ricci' in text:
            assessment['action'] = 'KEEP'
            assessment['reason'] = 'Fundamental gravitational equations (always relevant)'
            assessment['simulation_backed'] = False

        # Clifford algebra (Pneuma spinors)
        elif 'clifford' in text or 'gamma' in text or 'γμ' in text:
            assessment['action'] = 'KEEP'
            assessment['reason'] = 'Clifford algebra for 26D→13D fermion sector'
            assessment['simulation_backed'] = False

        # Thermal time (Tomita-Takesaki)
        elif 'thermal time' in text or 'kms' in text or 't = αt' in text or 'entropy' in text and 's[ρ]' in text:
            assessment['action'] = 'KEEP'
            assessment['reason'] = 'Thermal time hypothesis (framework foundation)'
            assessment['simulation_backed'] = False

        # === UPDATE: Formulas needing correction ===

        # Old generation count (chi_raw = -300)
        elif '-300' in formula['text'] or 'chi_raw' in text:
            assessment['action'] = 'UPDATE'
            assessment['reason'] = 'Replace chi_raw = -300 with chi_eff = 144 (flux-dressed)'
            assessment['simulation_backed'] = True
            assessment['correction'] = 'Use PM.topology.chi_eff (144, not -300)'

        # Old proton decay uncertainty (0.8 OOM)
        elif '0.8' in formula['text'] and 'oom' in text:
            assessment['action'] = 'UPDATE'
            assessment['reason'] = 'Update proton decay uncertainty to 0.177 OOM (v8.4 improvement)'
            assessment['simulation_backed'] = True
            assessment['correction'] = 'Use PM.proton_decay.tau_p_uncertainty_oom (0.177)'

        # Old branching ratios (placeholder values)
        elif 'br(e+pi0)' in text or 'br(k+nu)' in text:
            if '50%' in formula['text'] or '28%' in formula['text']:
                assessment['action'] = 'UPDATE'
                assessment['reason'] = 'Update proton decay BRs to v8.4 CKM rotation values'
                assessment['simulation_backed'] = True
                assessment['correction'] = 'BR(e⁺π⁰) = 64.2%, BR(K⁺ν̄) = 35.6%'

        # === REMOVE: Deprecated formulas ===

        # Old vacuum structure (14D×2 approach)
        elif '14d' in text or '×2' in formula['text']:
            assessment['action'] = 'REMOVE'
            assessment['reason'] = 'Deprecated 14D×2 structure (now using 26D→13D shadow)'

        # Old CY₄ construction (replaced with G₂)
        elif 'cy4' in text or 'calabi-yau' in text and '4-fold' in text:
            assessment['action'] = 'REMOVE'
            assessment['reason'] = 'Deprecated CY₄ construction (replaced by TCS G₂)'

        # === REVIEW: Needs decision ===

        # CMB bubble collisions (testable but not yet simulated)
        elif 'coleman' in text or 'de luccia' in text or 'bubble' in text:
            assessment['action'] = 'REVIEW'
            assessment['reason'] = 'CMB bubble predictions (testable but not core to v8.4)'
            assessment['simulation_backed'] = False

        # Landscape entropy (context-dependent)
        elif 'landscape' in text or '10^500' in text:
            assessment['action'] = 'REVIEW'
            assessment['reason'] = 'String landscape (context-dependent relevance)'
            assessment['simulation_backed'] = False

        return assessment

    def _check_simulation_backed(self, simulation_key):
        """Check if simulation category exists in theory_output.json"""
        return simulation_key in self.simulation

    def generate_report(self):
        """Generate comprehensive assessment report"""
        print("=" * 80)
        print("FORMULA RELEVANCE ASSESSMENT FOR v8.4")
        print("=" * 80)
        print()

        total = sum(len(v) for v in self.assessments.values())

        print(f"Total formulas assessed: {total}")
        print(f"  KEEP (v8.4 relevant): {len(self.assessments['KEEP'])} ({len(self.assessments['KEEP'])/total*100:.1f}%)")
        print(f"  UPDATE (needs correction): {len(self.assessments['UPDATE'])} ({len(self.assessments['UPDATE'])/total*100:.1f}%)")
        print(f"  REMOVE (deprecated): {len(self.assessments['REMOVE'])} ({len(self.assessments['REMOVE'])/total*100:.1f}%)")
        print(f"  REVIEW (manual decision): {len(self.assessments['REVIEW'])} ({len(self.assessments['REVIEW'])/total*100:.1f}%)")
        print()

        print("=" * 80)
        print("KEEP: Essential v8.4 Formulas")
        print("=" * 80)
        for i, item in enumerate(self.assessments['KEEP'][:20], 1):
            print(f"{i:2d}. [{item['category']:15s}] {item['formula'][:60]}")
            print(f"    Reason: {item['reason']}")
            if item.get('pm_values'):
                print(f"    PM values: {', '.join(item['pm_values'])}")
            print()

        if len(self.assessments['KEEP']) > 20:
            print(f"... and {len(self.assessments['KEEP']) - 20} more")
            print()

        print("=" * 80)
        print("UPDATE: Formulas Needing Correction")
        print("=" * 80)
        for i, item in enumerate(self.assessments['UPDATE'], 1):
            print(f"{i:2d}. [{item['category']:15s}] {item['formula'][:60]}")
            print(f"    Reason: {item['reason']}")
            if item.get('correction'):
                print(f"    Correction: {item['correction']}")
            print()

        print("=" * 80)
        print("REMOVE: Deprecated Formulas")
        print("=" * 80)
        for i, item in enumerate(self.assessments['REMOVE'], 1):
            print(f"{i:2d}. [{item['category']:15s}] {item['formula'][:60]}")
            print(f"    Reason: {item['reason']}")
            print()

        print("=" * 80)
        print("REVIEW: Manual Decision Needed")
        print("=" * 80)
        for i, item in enumerate(self.assessments['REVIEW'][:10], 1):
            print(f"{i:2d}. [{item['category']:15s}] {item['formula'][:60]}")
            print(f"    Reason: {item['reason']}")
            print()

        if len(self.assessments['REVIEW']) > 10:
            print(f"... and {len(self.assessments['REVIEW']) - 10} more")
            print()

        # Save detailed results
        results = {
            'summary': {
                'total': total,
                'keep': len(self.assessments['KEEP']),
                'update': len(self.assessments['UPDATE']),
                'remove': len(self.assessments['REMOVE']),
                'review': len(self.assessments['REVIEW'])
            },
            'assessments': self.assessments
        }

        with open('formula_relevance_assessment.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("✅ Detailed results saved to: formula_relevance_assessment.json")
        print()


def main():
    assessor = FormulaRelevanceAssessor(simulation, formula_data)
    assessor.assess_all()
    assessor.generate_report()


if __name__ == '__main__':
    main()
