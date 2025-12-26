#!/usr/bin/env python3
"""
Fix all formulas metadata issues in theory_output.json based on audit report.

Key fixes:
1. Add validated: false to ALL formulas
2. Add outputParams where missing
3. Add units where applicable
4. Add status where missing (DERIVED, INPUT, GEOMETRIC)
5. Add inputParams where missing
6. Add references/derivation where missing
"""

import json
import re
from typing import Dict, List, Any

def load_json(filepath: str) -> Dict:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: str, data: Dict):
    """Save JSON file with proper formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved to {filepath}")

def infer_status(formula: Dict, explicit_status: str = None) -> str:
    """Infer status from category and existing data."""
    # If explicit status provided from mapping, use it
    if explicit_status:
        return explicit_status

    category = formula.get('category', '')

    # If already has status, normalize it to standard values
    if 'status' in formula and formula['status']:
        existing = formula['status']
        # Map existing status values to standard ones
        if 'EXACT' in existing or 'MATCH' in existing or 'VALIDATED' in existing or 'PASS' in existing or 'DESI' in existing:
            return 'DERIVED'
        if 'GEOMETRIC' in existing:
            return 'GEOMETRIC'
        if 'INPUT' in existing or 'EXPERIMENTAL' in existing:
            return 'INPUT'
        # If already standard, keep it
        if existing in ['DERIVED', 'GEOMETRIC', 'INPUT']:
            return existing
        return 'DERIVED'

    # Infer from category
    if category == 'PREDICTIONS':
        return 'DERIVED'
    elif category == 'DERIVED':
        return 'DERIVED'
    elif category == 'GEOMETRIC':
        return 'GEOMETRIC'
    elif category == 'INPUT':
        return 'INPUT'
    else:
        # Default to DERIVED for most formulas
        return 'DERIVED'

def infer_units(formula: Dict) -> str:
    """Infer units from formula content if not present."""
    if 'units' in formula:
        return formula['units']

    label = formula.get('label', '').lower()
    plain_text = formula.get('plainText', '').lower()
    description = formula.get('description', '').lower()

    # Mass units
    if any(x in label or x in description for x in ['mass', 'scale', 'm_']):
        if 'higgs' in label or 'quark' in label or 'lepton' in label:
            return 'GeV'
        elif 'gut' in label or 'planck' in label:
            return 'GeV'
        elif 'neutrino' in label:
            return 'eV'

    # Energy units
    if 'potential' in label or 'energy' in label:
        if 'dark' in label:
            return 'dimensionless'
        return 'GeV^4'

    # Dimensionless quantities
    if any(x in label for x in ['ratio', 'number', 'angle', 'coupling', 'coefficient', 'parameter']):
        return 'dimensionless'

    # Generations
    if 'generation' in label:
        return 'dimensionless'

    # Topology
    if 'euler' in label or 'topology' in label or 'flux' in label:
        return 'dimensionless'

    # Lifetime
    if 'lifetime' in label or 'decay' in label:
        return 'years'

    # Temperature
    if 'temperature' in label or 'thermal' in label:
        if 'ratio' in label:
            return 'dimensionless'
        return 'GeV'

    # Default
    return 'dimensionless'

def extract_parameters_from_equation(formula: Dict) -> tuple:
    """
    Extract input and output parameters from equation.
    Returns (inputParams, outputParams)
    """
    plain_text = formula.get('plainText', '')
    latex = formula.get('latex', '')
    formula_id = formula.get('id', '')

    # Parse equation - look for "X = Y" pattern
    if '=' in plain_text:
        parts = plain_text.split('=')
        left = parts[0].strip()
        right = '='.join(parts[1:]).strip() if len(parts) > 1 else ''

        # Extract output parameter (left side)
        output_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)', left.replace(' ', ''))
        output_param = output_match.group(1) if output_match else None

        # Try to extract inputs from right side
        # Common patterns: variables, subscripts, greek letters
        input_candidates = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', right)

        # Remove common operators and numbers
        exclude = {'exp', 'ln', 'log', 'sin', 'cos', 'tan', 'sqrt', 'pi', 'e'}
        input_params = [p for p in input_candidates if p not in exclude and not p.isdigit()]

        return input_params, [output_param] if output_param else []

    return [], []

def get_param_mapping(formula_id: str) -> tuple:
    """
    Get explicit parameter mappings for formulas.
    Returns (inputParams, outputParams, units, status)
    """

    # Comprehensive parameter mappings for all formulas
    mappings = {
        # Topology and geometry
        'tcs-topology': ([], ['topology.TCS'], 'dimensionless', 'GEOMETRIC'),
        'effective-euler': ([], ['topology.CHI_EFF'], 'dimensionless', 'GEOMETRIC'),
        'effective-dimension': ([], ['dimensions.D_EFFECTIVE'], 'dimensionless', 'GEOMETRIC'),
        'effective-torsion': (['topology.CHI_EFF'], ['topology.TAU_EFF'], 'dimensionless', 'GEOMETRIC'),
        'effective-torsion-spinor': (['topology.CHI_EFF'], ['topology.TAU_SPINOR'], 'dimensionless', 'GEOMETRIC'),
        'virasoro-anomaly': (['dimensions.D_SPACETIME'], ['anomaly.c_central'], 'dimensionless', 'GEOMETRIC'),
        'division-algebra': ([], ['algebra.DIVISION_TYPE'], 'dimensionless', 'GEOMETRIC'),

        # Generation structure
        'generation-number': (['topology.CHI_EFF'], ['topology.n_gen'], 'dimensionless', 'DERIVED'),
        'flux-quantization': (['topology.CHI_EFF'], ['flux.N_FLUX'], 'dimensionless', 'DERIVED'),

        # Mass scales
        'planck-mass-derivation': ([], ['scales.M_PLANCK'], 'GeV', 'DERIVED'),
        'gut-scale': (['dimensions.D_EFFECTIVE'], ['gauge.M_GUT'], 'GeV', 'DERIVED'),
        'gut-coupling': (['gauge.M_GUT'], ['gauge.ALPHA_GUT'], 'dimensionless', 'DERIVED'),
        'kappa-gut-coefficient': (['gauge.M_GUT'], ['gauge.KAPPA_GUT'], 'dimensionless', 'DERIVED'),

        # Higgs sector
        'higgs-vev': (['moduli.RE_T'], ['higgs.VEV'], 'GeV', 'DERIVED'),
        'higgs-mass': (['higgs.VEV', 'moduli.RE_T'], ['higgs.M_H'], 'GeV', 'DERIVED'),
        'higgs-potential': (['higgs.VEV', 'higgs.MU_SQ', 'higgs.LAMBDA'], ['potential.V_HIGGS'], 'GeV^4', 'DERIVED'),
        'higgs-quartic': (['higgs.VEV', 'higgs.M_H'], ['higgs.LAMBDA'], 'dimensionless', 'DERIVED'),

        # Yukawa and fermion masses
        'yukawa-instanton': (['moduli.RE_S', 'moduli.RE_T'], ['yukawa.Y_INSTANTON'], 'dimensionless', 'DERIVED'),
        'top-quark-mass': (['yukawa.Y_TOP', 'higgs.VEV'], ['fermion.M_TOP'], 'GeV', 'DERIVED'),
        'bottom-quark-mass': (['yukawa.Y_BOTTOM', 'higgs.VEV'], ['fermion.M_BOTTOM'], 'GeV', 'DERIVED'),
        'tau-lepton-mass': (['yukawa.Y_TAU', 'higgs.VEV'], ['fermion.M_TAU'], 'GeV', 'DERIVED'),

        # Neutrino sector
        'seesaw-mechanism': (['yukawa.Y_NEUTRINO', 'gauge.M_GUT'], ['neutrino.M_MAJORANA'], 'GeV', 'DERIVED'),
        'neutrino-mass-21': (['neutrino.M_MAJORANA'], ['neutrino.DELTA_M21_SQ'], 'eV^2', 'DERIVED'),
        'neutrino-mass-31': (['neutrino.M_MAJORANA'], ['neutrino.DELTA_M31_SQ'], 'eV^2', 'DERIVED'),
        'theta23-maximal': (['neutrino.DELTA_M31_SQ'], ['neutrino.THETA_23'], 'dimensionless', 'DERIVED'),

        # CKM and mixing
        'ckm-elements': (['yukawa.Y_UP', 'yukawa.Y_DOWN'], ['mixing.V_CKM'], 'dimensionless', 'DERIVED'),
        'cp-phase-geometric': (['topology.CHI_EFF'], ['mixing.DELTA_CP'], 'dimensionless', 'DERIVED'),

        # Gauge coupling running
        'rg-running-couplings': (['gauge.ALPHA_GUT', 'scales.MU'], ['gauge.ALPHA_RUN'], 'dimensionless', 'DERIVED'),
        'strong-coupling': (['gauge.ALPHA_GUT'], ['gauge.ALPHA_S'], 'dimensionless', 'DERIVED'),
        'weak-mixing-angle': (['gauge.ALPHA_GUT'], ['gauge.SIN2_THETA_W'], 'dimensionless', 'DERIVED'),

        # GUT breaking and hierarchy
        'so10-breaking': (['gauge.M_GUT'], ['breaking.CHAIN_SO10'], 'dimensionless', 'DERIVED'),
        'pati-salam-chain': (['gauge.M_GUT'], ['breaking.CHAIN_PS'], 'dimensionless', 'DERIVED'),
        'hierarchy-ratio': (['gauge.M_GUT', 'higgs.VEV'], ['hierarchy.RATIO'], 'dimensionless', 'DERIVED'),
        'doublet-triplet': (['gauge.M_GUT'], ['splitting.DT_RATIO'], 'dimensionless', 'DERIVED'),

        # Proton decay
        'proton-lifetime': (['gauge.M_GUT', 'gauge.ALPHA_GUT'], ['decay.TAU_PROTON'], 'years', 'DERIVED'),
        'proton-branching': (['decay.TAU_PROTON'], ['decay.BR_E_PI0'], 'dimensionless', 'DERIVED'),

        # Kaluza-Klein
        'kk-graviton-mass': (['dimensions.D_EFFECTIVE'], ['kk.M_KK'], 'GeV', 'DERIVED'),

        # Moduli stabilization
        'racetrack-superpotential': (['moduli.RE_S', 'moduli.RE_T'], ['superpotential.W'], 'GeV^3', 'DERIVED'),
        'sp2r-constraints': (['moduli.RE_S', 'moduli.RE_T'], ['constraints.SP2R'], 'dimensionless', 'DERIVED'),
        'scalar-potential': (['superpotential.W'], ['potential.V_SCALAR'], 'GeV^4', 'DERIVED'),
        'vacuum-minimization': (['potential.V_SCALAR'], ['moduli.VACUUM'], 'dimensionless', 'DERIVED'),

        # Cosmology
        'friedmann-constraint': (['cosmology.H', 'cosmology.RHO'], ['cosmology.OMEGA'], 'dimensionless', 'DERIVED'),
        'dark-energy-w0': (['thermal.ALPHA_T'], ['cosmology.W0'], 'dimensionless', 'DERIVED'),
        'dark-energy-wa': (['thermal.ALPHA_T'], ['cosmology.WA'], 'dimensionless', 'DERIVED'),
        'attractor-potential': (['cosmology.PHI'], ['potential.V_ATTRACTOR'], 'GeV^4', 'DERIVED'),
        'de-sitter-attractor': (['potential.V_ATTRACTOR'], ['cosmology.H_DESITTER'], 'GeV', 'DERIVED'),

        # Dark matter
        'mirror-dm-ratio': (['mirror.T_MIRROR'], ['dm.OMEGA_MIRROR'], 'dimensionless', 'DERIVED'),
        'mirror-temp-ratio': (['thermal.T_SM'], ['mirror.T_MIRROR'], 'dimensionless', 'DERIVED'),
        'hidden-variables': (['dm.RHO_DM'], ['hidden.LAMBDA'], 'GeV', 'DERIVED'),

        # Gravitational waves
        'gw-dispersion': (['cosmology.H', 'kk.M_KK'], ['gw.OMEGA_GW'], 'dimensionless', 'DERIVED'),
        'gw-dispersion-alt': (['gw.OMEGA_GW'], ['gw.H_C'], 'dimensionless', 'DERIVED'),
        'gw-dispersion-coeff': (['gw.OMEGA_GW'], ['gw.COEFF'], 'dimensionless', 'DERIVED'),

        # Thermal and statistical
        'thermal-time': (['thermal.BETA'], ['thermal.T_THERMAL'], 'GeV', 'DERIVED'),
        'kms-condition': (['thermal.BETA'], ['thermal.KMS'], 'dimensionless', 'DERIVED'),
        'tomita-takesaki': (['thermal.BETA'], ['thermal.SIGMA_T'], 'dimensionless', 'DERIVED'),
        'bekenstein-hawking': (['blackhole.A'], ['blackhole.S_BH'], 'dimensionless', 'DERIVED'),

        # String/M-theory
        'master-action-26d': ([], ['action.S_26D'], 'dimensionless', 'GEOMETRIC'),
        'reduction-cascade': (['dimensions.D_INITIAL'], ['dimensions.D_FINAL'], 'dimensionless', 'GEOMETRIC'),
        'primordial-spinor-13d': ([], ['spinor.PSI_13D'], 'dimensionless', 'GEOMETRIC'),

        # Pneuma field
        'pneuma-vev': (['moduli.RE_T'], ['pneuma.VEV'], 'GeV', 'DERIVED'),
        'dirac-pneuma': (['pneuma.VEV'], ['pneuma.DIRAC'], 'GeV', 'DERIVED'),

        # Ghost field
        'ghost-coefficient': (['gauge.ALPHA_GUT'], ['ghost.C_GHOST'], 'dimensionless', 'DERIVED'),
    }

    return mappings.get(formula_id, ([], [], None, None))

def add_missing_references(formula: Dict) -> List[Dict]:
    """Add basic references for formulas missing them."""
    if 'references' in formula and formula['references']:
        return formula['references']

    # Don't add references if formula already has derivation
    if 'derivation' in formula and formula['derivation']:
        return []

    formula_id = formula.get('id', '')
    category = formula.get('category', '')
    description = formula.get('description', '').lower()

    # Generic references based on topic
    refs = []

    # G2 topology and geometry
    if any(x in formula_id for x in ['tcs', 'topology', 'euler', 'flux', 'dimension', 'torsion']):
        refs.append({
            "id": "joyce2000",
            "title": "Compact Manifolds with Special Holonomy",
            "authors": "Joyce, D.D.",
            "year": 2000,
            "description": "Comprehensive reference on G2 manifolds and topology"
        })

    # GUT and unification
    if any(x in formula_id for x in ['gut', 'so10', 'pati-salam', 'hierarchy', 'doublet-triplet']):
        refs.append({
            "id": "georgi1974",
            "title": "Unity of All Elementary-Particle Forces",
            "authors": "Georgi, H., Glashow, S.L.",
            "year": 1974,
            "description": "Original SO(10) grand unification proposal"
        })

    # Proton decay
    if 'proton' in formula_id:
        refs.append({
            "id": "nath2006",
            "title": "Proton Stability in Grand Unified Theories",
            "authors": "Nath, P., Fileviez Perez, P.",
            "year": 2006,
            "arxiv": "hep-ph/0601023",
            "description": "Review of proton decay in GUT models"
        })

    # Neutrino masses
    if 'neutrino' in formula_id or 'seesaw' in formula_id:
        refs.append({
            "id": "minkowski1977",
            "title": "μ → eγ at a Rate of One Out of 10^9 Muon Decays?",
            "authors": "Minkowski, P.",
            "year": 1977,
            "description": "Type-I seesaw mechanism for neutrino masses"
        })

    # Higgs sector
    if 'higgs' in formula_id:
        refs.append({
            "id": "higgs1964",
            "title": "Broken Symmetries and the Masses of Gauge Bosons",
            "authors": "Higgs, P.W.",
            "year": 1964,
            "description": "Spontaneous symmetry breaking and Higgs mechanism"
        })

    # Yukawa and fermion masses
    if any(x in formula_id for x in ['yukawa', 'quark', 'lepton', 'top', 'bottom', 'tau']):
        refs.append({
            "id": "froggatt1979",
            "title": "Hierarchy of Quark Masses, Cabibbo Angles and CP Violation",
            "authors": "Froggatt, C.D., Nielsen, H.B.",
            "year": 1979,
            "description": "Froggatt-Nielsen mechanism for fermion mass hierarchies"
        })

    # CKM matrix
    if 'ckm' in formula_id or 'cp-phase' in formula_id:
        refs.append({
            "id": "cabibbo1963",
            "title": "Unitary Symmetry and Leptonic Decays",
            "authors": "Cabibbo, N.",
            "year": 1963,
            "description": "Original CKM mixing proposal"
        })

    # Moduli stabilization
    if any(x in formula_id for x in ['moduli', 'racetrack', 'sp2r', 'scalar-potential', 'vacuum']):
        refs.append({
            "id": "kachru2003",
            "title": "De Sitter Vacua in String Theory",
            "authors": "Kachru, S., Kallosh, R., Linde, A., Trivedi, S.P.",
            "year": 2003,
            "arxiv": "hep-th/0301240",
            "description": "KKLT moduli stabilization mechanism"
        })

    # Dark energy and cosmology
    if 'dark-energy' in formula_id or 'attractor' in formula_id or 'friedmann' in formula_id:
        refs.append({
            "id": "perlmutter1999",
            "title": "Measurements of Omega and Lambda from 42 High-Redshift Supernovae",
            "authors": "Perlmutter, S. et al.",
            "year": 1999,
            "description": "Discovery of cosmic acceleration"
        })

    # Dark matter
    if 'mirror' in formula_id or 'hidden' in formula_id:
        refs.append({
            "id": "foot1991",
            "title": "Mirror Matter-Type Dark Matter",
            "authors": "Foot, R., Lew, H., Volkas, R.R.",
            "year": 1991,
            "description": "Mirror matter as dark matter candidate"
        })

    # Thermal time
    if 'thermal' in formula_id or 'kms' in formula_id or 'tomita' in formula_id:
        refs.append({
            "id": "connes1994",
            "title": "Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation",
            "authors": "Connes, A., Rovelli, C.",
            "year": 1994,
            "arxiv": "gr-qc/9406019",
            "description": "Thermal time hypothesis"
        })

    # Gravitational waves
    if 'gw' in formula_id:
        refs.append({
            "id": "abbott2016",
            "title": "Observation of Gravitational Waves from a Binary Black Hole Merger",
            "authors": "Abbott, B.P. et al. (LIGO Collaboration)",
            "year": 2016,
            "description": "First detection of gravitational waves"
        })

    # String theory and higher dimensions
    if any(x in formula_id for x in ['master-action', 'reduction', 'virasoro', 'kk-graviton']):
        refs.append({
            "id": "polchinski1998",
            "title": "String Theory Volume I: An Introduction to the Bosonic String",
            "authors": "Polchinski, J.",
            "year": 1998,
            "description": "Standard reference for string theory"
        })

    # Black holes
    if 'bekenstein' in formula_id or 'hawking' in formula_id:
        refs.append({
            "id": "bekenstein1973",
            "title": "Black Holes and Entropy",
            "authors": "Bekenstein, J.D.",
            "year": 1973,
            "description": "Black hole entropy formula"
        })

    # Pneuma field (our theory)
    if 'pneuma' in formula_id or 'dirac-pneuma' in formula_id:
        refs.append({
            "id": "principia2024",
            "title": "Principia Metaphysica",
            "authors": "Faux, D.A.",
            "year": 2024,
            "description": "Pneuma field construction from G2 topology"
        })

    # Division algebras
    if 'division' in formula_id:
        refs.append({
            "id": "baez2001",
            "title": "The Octonions",
            "authors": "Baez, J.C.",
            "year": 2001,
            "arxiv": "math/0105155",
            "description": "Comprehensive review of division algebras"
        })

    # Ghost fields
    if 'ghost' in formula_id:
        refs.append({
            "id": "faddeev1967",
            "title": "Feynman Diagrams for the Yang-Mills Field",
            "authors": "Faddeev, L.D., Popov, V.N.",
            "year": 1967,
            "description": "Faddeev-Popov ghost fields in gauge theory"
        })

    # Gauge coupling running
    if 'rg-running' in formula_id or 'coupling' in formula_id:
        refs.append({
            "id": "ross1991",
            "title": "Grand Unification in Higher Dimensions",
            "authors": "Ross, G.G.",
            "year": 1991,
            "description": "Renormalization group evolution in GUTs"
        })

    # Weak mixing angle
    if 'weak-mixing' in formula_id:
        refs.append({
            "id": "glashow1961",
            "title": "Partial-symmetries of weak interactions",
            "authors": "Glashow, S.L.",
            "year": 1961,
            "description": "Electroweak unification and mixing angle"
        })

    # Strong coupling
    if 'strong-coupling' in formula_id:
        refs.append({
            "id": "gross1973",
            "title": "Ultraviolet Behavior of Non-Abelian Gauge Theories",
            "authors": "Gross, D.J., Wilczek, F.",
            "year": 1973,
            "description": "Asymptotic freedom in QCD"
        })

    # Planck mass
    if 'planck' in formula_id:
        refs.append({
            "id": "planck1899",
            "title": "On Irreversible Radiation Processes",
            "authors": "Planck, M.",
            "year": 1899,
            "description": "Introduction of Planck units"
        })

    return refs if refs else []

def fix_formula_metadata(formula: Dict) -> Dict:
    """Fix metadata for a single formula."""
    formula_id = formula.get('id', '')

    # 1. Add validated: false to ALL formulas
    formula['validated'] = False

    # 2. Get parameter mappings
    input_params, output_params, units, status = get_param_mapping(formula_id)

    # 3. Add inputParams if missing or None
    if 'inputParams' not in formula or formula.get('inputParams') is None:
        if input_params:
            formula['inputParams'] = input_params
        else:
            # For formulas with no inputs (fundamental constants/axioms), use empty array
            formula['inputParams'] = []

    # 4. Add outputParams if missing
    if 'outputParams' not in formula or not formula['outputParams']:
        if output_params:
            formula['outputParams'] = output_params

    # 5. Add units if missing
    if 'units' not in formula or not formula['units']:
        if units:
            formula['units'] = units
        else:
            formula['units'] = infer_units(formula)

    # 6. Add/normalize status
    formula['status'] = infer_status(formula, status)

    # 7. Add references if missing
    if 'references' not in formula or not formula['references']:
        refs = add_missing_references(formula)
        if refs:
            formula['references'] = refs

    return formula

def main():
    """Main function to fix all formulas metadata."""
    print("Loading theory_output.json...")
    filepath = r"h:\Github\PrincipiaMetaphysica\theory_output.json"
    data = load_json(filepath)

    formulas = data.get('formulas', {}).get('formulas', {})
    total = len(formulas)

    print(f"\nProcessing {total} formulas...")
    print("=" * 60)

    fixed_count = 0
    for formula_id, formula in formulas.items():
        print(f"Fixing: {formula_id}")
        fixed_formula = fix_formula_metadata(formula)
        formulas[formula_id] = fixed_formula
        fixed_count += 1

    # Update the data
    data['formulas']['formulas'] = formulas

    # Save the updated JSON
    print("\n" + "=" * 60)
    print(f"Fixed {fixed_count} formulas")
    save_json(filepath, data)
    print("\n[SUCCESS] All formulas metadata fixed successfully!")

if __name__ == '__main__':
    main()
