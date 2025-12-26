#!/usr/bin/env python3
"""
Principia Metaphysica - Reference Extraction & Parameter Linkage
=================================================================

This script:
1. Extracts all references from formulas into a central references.json
2. Adds inputParams and outputParams to all formulas
3. Ensures bi-directional linking between all entities
4. Generates the split JSON files for the AUTO_GENERATED folder

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
from dataclasses import dataclass, field, asdict

# Paths
AUTO_GEN_DIR = Path("AUTO_GENERATED")
JSON_DIR = AUTO_GEN_DIR / "json"

@dataclass
class Reference:
    """Academic reference structure."""
    id: str
    title: str
    authors: str
    year: int
    arxiv: str = ""
    doi: str = ""
    journal: str = ""
    description: str = ""
    cited_by_formulas: List[str] = field(default_factory=list)
    cited_by_params: List[str] = field(default_factory=list)

@dataclass
class ParameterRef:
    """Parameter reference in a formula."""
    id: str
    symbol: str
    name: str
    role: str  # 'input' or 'output'
    units: str = ""
    value: Optional[float] = None

class ReferenceExtractor:
    """Extracts and consolidates all references from theory data."""

    def __init__(self):
        self.references: Dict[str, Reference] = {}
        self.formula_refs: Dict[str, List[str]] = defaultdict(list)

    def extract_from_formula(self, formula_id: str, formula_data: Dict) -> List[str]:
        """Extract references from a formula."""
        ref_ids = []
        for ref_data in formula_data.get('references', []):
            ref_id = ref_data.get('id', '')
            if not ref_id:
                continue

            ref_ids.append(ref_id)

            if ref_id not in self.references:
                self.references[ref_id] = Reference(
                    id=ref_id,
                    title=ref_data.get('title', ''),
                    authors=ref_data.get('authors', ''),
                    year=ref_data.get('year', 0),
                    arxiv=ref_data.get('arxiv', ''),
                    doi=ref_data.get('doi', ''),
                    description=ref_data.get('description', '')
                )

            # Track which formulas cite this reference
            if formula_id not in self.references[ref_id].cited_by_formulas:
                self.references[ref_id].cited_by_formulas.append(formula_id)

        self.formula_refs[formula_id] = ref_ids
        return ref_ids

    def to_json(self) -> Dict:
        """Export references to JSON format."""
        return {
            ref_id: {
                "id": ref.id,
                "title": ref.title,
                "authors": ref.authors,
                "year": ref.year,
                "arxiv": ref.arxiv,
                "doi": ref.doi,
                "description": ref.description,
                "citedByFormulas": ref.cited_by_formulas,
                "citedByParams": ref.cited_by_params
            }
            for ref_id, ref in self.references.items()
        }

class FormulaParamLinker:
    """Links formulas to their input and output parameters."""

    # Common physics symbols that map to parameters (using category.param format)
    SYMBOL_TO_PARAM = {
        # Scales
        'M_GUT': 'gauge.M_GUT',
        'M_Pl': 'dimensions.M_PLANCK',
        'M_*': 'dimensions.M_BULK',
        'M_KK': 'kk_spectrum.m1_TeV',

        # Topology
        'χ_eff': 'topology.CHI_EFF',
        'chi_eff': 'topology.CHI_EFF',
        'b₂': 'topology.B2',
        'b₃': 'topology.B3',
        'b_2': 'topology.B2',
        'b_3': 'topology.B3',
        'n_gen': 'topology.n_gen',

        # Cosmology
        'w₀': 'dark_energy.w0',
        'w_0': 'dark_energy.w0',
        'w_a': 'dark_energy.wa',
        'α_T': 'dark_energy.alpha_T',
        'alpha_T': 'dark_energy.alpha_T',
        'D_eff': 'dark_energy.d_eff',
        'φ_M': 'pneuma.VEV',
        'phi_M': 'pneuma.VEV',

        # Neutrino
        'θ₁₂': 'pmns.theta_12',
        'θ₂₃': 'pmns.theta_23',
        'θ₁₃': 'pmns.theta_13',
        'theta_12': 'pmns.theta_12',
        'theta_23': 'pmns.theta_23',
        'theta_13': 'pmns.theta_13',
        'δ_CP': 'pmns.delta_CP',
        'delta_CP': 'pmns.delta_CP',
        'm₁': 'neutrino.m1',
        'm₂': 'neutrino.m2',
        'm₃': 'neutrino.m3',
        'm_1': 'neutrino.m1',
        'm_2': 'neutrino.m2',
        'm_3': 'neutrino.m3',

        # Gauge
        'α_GUT': 'gauge.ALPHA_GUT',
        'alpha_GUT': 'gauge.ALPHA_GUT',
        'sin²θ_W': 'gauge.WEAK_MIXING_ANGLE',
        'α_s': 'gauge.alpha_s',
        'alpha_s': 'gauge.alpha_s',

        # Proton decay
        'τ_p': 'proton_decay.tau_p_years',
        'tau_p': 'proton_decay.tau_p_years',
        'S': 'proton_decay.suppression',

        # Higgs
        'm_H': 'higgs.m_H',
        'v': 'pneuma.VEV',
        'v_EW': 'pneuma.VEV',
        'λ_H': 'higgs.lambda_H',
        'lambda_H': 'higgs.lambda_H',

        # Breaking chains
        'SO(10)': 'so10-breaking',
        'G₄₂₂': 'pati-salam',
        'G_422': 'pati-salam',

        # Actions
        'S_26D': 'action-26d',
        'ℒ': 'lagrangian',
        'L': 'lagrangian',

        # Potentials and fields

        # Densities

        # Entropy

        # Cosmology

        # Higgs

        # Running couplings

        # Yukawa

        # Thermal/KMS

        # Topological
    }

    def __init__(self, data: Dict):
        self.data = data
        self.param_index = self._build_param_index()

    def _build_param_index(self) -> Dict[str, Dict]:
        """Build index of all parameters."""
        index = {}

        # From parameters section
        params = self.data.get('parameters', {})
        for category, cat_params in params.items():
            if isinstance(cat_params, dict):
                for pid, param in cat_params.items():
                    if isinstance(param, dict):
                        index[pid] = {
                            'id': pid,
                            'category': category,
                            'data': param
                        }

        # From simulations (output params)
        simulations = self.data.get('simulations', {})
        for sim_name, sim_data in simulations.items():
            if isinstance(sim_data, dict):
                for key, value in sim_data.items():
                    param_id = f"{sim_name}.{key}"
                    index[param_id] = {
                        'id': param_id,
                        'category': 'simulation_output',
                        'simulation': sim_name,
                        'key': key,
                        'value': value if not isinstance(value, dict) else value.get('value')
                    }

        return index

    def _extract_symbols_from_html(self, html: str) -> Set[str]:
        """Extract mathematical symbols from HTML formula."""
        symbols = set()

        # Remove HTML tags but preserve content
        text = re.sub(r'<[^>]+>', '', html)

        # Extract common patterns:
        # Greek letters followed by subscripts
        patterns = [
            r'([αβγδεζηθικλμνξοπρστυφχψω]_?[a-zA-Z0-9₀₁₂₃₄₅₆₇₈₉]+)',
            r'([ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]_?[a-zA-Z0-9₀₁₂₃₄₅₆₇₈₉]+)',
            # Latin letters with subscripts
            r'([a-zA-Z]_[a-zA-Z0-9₀₁₂₃₄₅₆₇₈₉]+)',
            # Special symbols
            r'(M_(?:GUT|Pl|KK|\*))',
            r'(chi_eff)',
            r'(b_[23])',
            r'(n_gen)',
            r'(D_eff)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html)
            symbols.update(matches)

        return symbols

    def _extract_symbols_from_latex(self, latex: str) -> Set[str]:
        """Extract symbols from LaTeX formula."""
        symbols = set()

        # Remove LaTeX commands but keep content
        # Extract subscripted variables like M_{GUT}, \alpha_{GUT}
        subscript_pattern = r'([a-zA-Z]+)_\{?([a-zA-Z0-9]+)\}?'
        matches = re.findall(subscript_pattern, latex)
        for base, sub in matches:
            # Construct symbol like 'M_GUT', 'alpha_GUT'
            symbols.add(f'{base}_{sub}')

        # Greek letters in LaTeX
        greek_pattern = r'\\(alpha|beta|gamma|delta|epsilon|theta|lambda|phi|chi|tau|omega|rho|mu|kappa|Psi)(?:_\{?([a-zA-Z0-9]+)\}?)?'
        matches = re.findall(greek_pattern, latex)
        for letter, subscript in matches:
            if subscript:
                symbols.add(f'{letter}_{subscript}')
            else:
                symbols.add(letter)

        # Single uppercase letters (common physics symbols)
        single_letter_pattern = r'\b([VWHSABP])\b(?!\\)'
        matches = re.findall(single_letter_pattern, latex)
        symbols.update(matches)

        return symbols

    def extract_params_from_formula(self, formula_id: str, formula: Dict) -> Dict[str, List[str]]:
        """Extract input and output parameters from a formula."""
        input_params = set()
        output_params = set()

        # 0. Preserve existing params from formula definition (Single Source of Truth)
        existing_input = formula.get('inputParams', [])
        existing_output = formula.get('outputParams', [])
        if existing_input or existing_output:
            # Use what's already defined in config.py
            input_params.update(existing_input)
            output_params.update(existing_output)

        # 1. Extract from terms (these are typically inputs)
        for term_key, term_data in formula.get('terms', {}).items():
            # Clean the term key
            clean_key = term_key.strip()

            # Check if it maps to a known parameter
            if clean_key in self.SYMBOL_TO_PARAM:
                input_params.add(self.SYMBOL_TO_PARAM[clean_key])
            else:
                # Try to find in param index by matching term names
                for pid in self.param_index:
                    param = self.param_index[pid]
                    if 'data' in param:
                        symbol = param['data'].get('symbol', '')
                        if symbol and clean_key in symbol:
                            input_params.add(pid)
                            break

        # 2. Parse HTML field to extract symbols
        html = formula.get('html', '')
        if html:
            html_symbols = self._extract_symbols_from_html(html)
            for symbol in html_symbols:
                # Normalize symbol (remove unicode subscripts, etc.)
                normalized = symbol.replace('₀', '_0').replace('₁', '_1').replace('₂', '_2').replace('₃', '_3')
                if normalized in self.SYMBOL_TO_PARAM:
                    input_params.add(self.SYMBOL_TO_PARAM[normalized])

        # 3. Parse LaTeX field
        latex = formula.get('latex', '')
        if latex:
            latex_symbols = self._extract_symbols_from_latex(latex)
            for symbol in latex_symbols:
                if symbol in self.SYMBOL_TO_PARAM:
                    input_params.add(self.SYMBOL_TO_PARAM[symbol])

        # 4. The computed value is typically the output
        if formula.get('computedValue') is not None:
            # The formula ID itself is often the output
            output_params.add(formula_id)

        # 5. Check simulation file for additional outputs
        sim_file = formula.get('simulationFile', '')
        if sim_file:
            sim_name = Path(sim_file).stem
            # Look for params from this simulation
            for pid in self.param_index:
                if pid.startswith(sim_name + '.'):
                    output_params.add(pid)

        # 6. Infer outputs from formula category and structure
        category = formula.get('category', '')
        if category == 'PREDICTIONS':
            # Prediction formulas output their own parameters
            output_params.add(formula_id)

        # 7. For DERIVED formulas, the left-hand side is usually the output
        # Look for = or → patterns in HTML to identify LHS
        html = formula.get('html', '')
        if category in ['DERIVED', 'THEORY'] and ('=' in html or '→' in html):
            # Try to extract LHS symbol
            if '=' in html:
                lhs = html.split('=')[0].strip()
                # Remove HTML tags
                lhs_clean = re.sub(r'<[^>]+>', '', lhs)
                # Check if LHS is a known symbol
                for symbol, param_id in self.SYMBOL_TO_PARAM.items():
                    if symbol in lhs_clean:
                        output_params.add(param_id)
                        break

        # 8. If formula has relatedFormulas, they might be outputs
        related = formula.get('relatedFormulas', [])
        for related_id in related:
            if related_id in self.data.get('formulas', {}).get('formulas', {}):
                # Don't add related formulas as outputs - too noisy
                pass

        # 9. Ensure formulas with simulation files have at least the formula_id as output
        if sim_file and not output_params:
            output_params.add(formula_id)

        # 10. Final fallback: if still no params detected, but formula is DERIVED/ESTABLISHED,
        # add the formula_id as output (it computes something, even if abstract)
        if not input_params and not output_params:
            if category in ['DERIVED', 'PREDICTIONS']:
                output_params.add(formula_id)

        return {
            'inputParams': sorted(list(input_params)),
            'outputParams': sorted(list(output_params))
        }

class BiDirectionalLinker:
    """Ensures all references are bi-directional."""

    def __init__(self, data: Dict):
        self.data = data

    def link_related_formulas(self) -> int:
        """Ensure related formulas point back to each other."""
        formulas = self.data.get('formulas', {}).get('formulas', {})
        additions = 0

        for fid, formula in formulas.items():
            related = formula.get('relatedFormulas', [])
            for related_id in related:
                if related_id in formulas:
                    related_formula = formulas[related_id]
                    related_refs = related_formula.get('relatedFormulas', [])
                    if fid not in related_refs:
                        if 'relatedFormulas' not in related_formula:
                            related_formula['relatedFormulas'] = []
                        related_formula['relatedFormulas'].append(fid)
                        additions += 1

        return additions

    def link_params_to_formulas(self) -> int:
        """Add usedInFormulas to parameters."""
        formulas = self.data.get('formulas', {}).get('formulas', {})
        params = self.data.get('parameters', {})
        additions = 0

        # Build reverse index
        param_to_formulas = defaultdict(list)

        for fid, formula in formulas.items():
            for param_id in formula.get('inputParams', []) + formula.get('outputParams', []):
                param_to_formulas[param_id].append(fid)

        # Update parameters
        for category, cat_params in params.items():
            if isinstance(cat_params, dict):
                for pid, param in cat_params.items():
                    if isinstance(param, dict):
                        if pid in param_to_formulas:
                            param['usedInFormulas'] = param_to_formulas[pid]
                            additions += 1

        return additions

def split_output_files(data: Dict):
    """Generate separate JSON files from theory_output.json."""
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    # Formulas
    formulas_file = JSON_DIR / "formulas.json"
    formulas_data = data.get('formulas', {})
    with open(formulas_file, 'w', encoding='utf-8') as f:
        json.dump(formulas_data, f, indent=2)
    print(f"  Created: {formulas_file}")

    # Parameters
    params_file = JSON_DIR / "parameters.json"
    params_data = data.get('parameters', {})
    with open(params_file, 'w', encoding='utf-8') as f:
        json.dump(params_data, f, indent=2)
    print(f"  Created: {params_file}")

    # Sections
    sections_file = JSON_DIR / "sections.json"
    sections_data = data.get('sections', {})
    with open(sections_file, 'w', encoding='utf-8') as f:
        json.dump(sections_data, f, indent=2)
    print(f"  Created: {sections_file}")

    # Simulations
    sims_file = JSON_DIR / "simulations.json"
    sims_data = data.get('simulations', {})
    with open(sims_file, 'w', encoding='utf-8') as f:
        json.dump(sims_data, f, indent=2)
    print(f"  Created: {sims_file}")

    # Statistics
    stats_file = JSON_DIR / "statistics.json"
    stats_data = data.get('statistics', {})
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, indent=2)
    print(f"  Created: {stats_file}")

def main():
    print("=" * 70)
    print("PRINCIPIA METAPHYSICA - EXTRACT & LINK")
    print("=" * 70)

    # Load theory output
    theory_file = "theory_output.json"
    print(f"\nLoading {theory_file}...")

    with open(theory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    formulas = data.get('formulas', {}).get('formulas', {})
    print(f"  Found {len(formulas)} formulas")

    # 1. Extract references
    print("\n1. Extracting references...")
    ref_extractor = ReferenceExtractor()
    for fid, formula in formulas.items():
        ref_extractor.extract_from_formula(fid, formula)
    print(f"   Found {len(ref_extractor.references)} unique references")

    # Save references
    refs_file = JSON_DIR / "references.json"
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    with open(refs_file, 'w', encoding='utf-8') as f:
        json.dump(ref_extractor.to_json(), f, indent=2)
    print(f"   Saved: {refs_file}")

    # 2. Link input/output params
    print("\n2. Linking formula parameters...")
    linker = FormulaParamLinker(data)
    params_added = 0
    formulas_with_params = 0
    formulas_without_params = []

    for fid, formula in formulas.items():
        params = linker.extract_params_from_formula(fid, formula)
        if params['inputParams'] or params['outputParams']:
            formula['inputParams'] = params['inputParams']
            formula['outputParams'] = params['outputParams']
            params_added += 1
            formulas_with_params += 1
        else:
            formulas_without_params.append(fid)

    print(f"   Formulas with params: {formulas_with_params}/{len(formulas)}")
    print(f"   Formulas still missing params: {len(formulas_without_params)}")

    if formulas_without_params:
        print(f"   Missing params for: {', '.join(sorted(formulas_without_params)[:10])}")
        if len(formulas_without_params) > 10:
            print(f"   ... and {len(formulas_without_params) - 10} more")

    # 3. Bi-directional linking
    print("\n3. Creating bi-directional links...")
    bi_linker = BiDirectionalLinker(data)

    additions = bi_linker.link_related_formulas()
    print(f"   Added {additions} reverse formula links")

    additions = bi_linker.link_params_to_formulas()
    print(f"   Added {additions} param-to-formula links")

    # 4. Save updated theory_output.json
    print("\n4. Saving updated theory_output.json...")
    with open(theory_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"   Saved: {theory_file}")

    # 5. Copy to AUTO_GENERATED
    print("\n5. Copying to AUTO_GENERATED folder...")
    AUTO_GEN_DIR.mkdir(parents=True, exist_ok=True)
    auto_gen_file = AUTO_GEN_DIR / "theory_output.json"
    with open(auto_gen_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"   Saved: {auto_gen_file}")

    # 6. Generate split files
    print("\n6. Generating split JSON files...")
    split_output_files(data)

    print("\n" + "=" * 70)
    print("EXTRACTION & LINKING COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    main()
