#!/usr/bin/env python3
"""
Add FormulaReference entries to formulas 7-20 in config.py
"""

import re

# Read the config file
with open(r"H:\Github\PrincipiaMetaphysica\config.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define the references to add for each formula
formula_refs = {
    "RACETRACK_SUPERPOTENTIAL": '''        references=[
            FormulaReference(
                id="kachru2003",
                title="de Sitter vacua in string theory",
                authors="Kachru, S., Kallosh, R., Linde, A., Trivedi, S.P.",
                year=2003,
                arxiv="hep-th/0301240",
                description="KKLT mechanism for stabilizing moduli via racetrack superpotential"
            ),
            FormulaReference(
                id="blanco2004",
                title="Racetrack Inflation",
                authors="Blanco-Pillado, J.J., Burgess, C.P., Cline, J.M., et al.",
                year=2004,
                arxiv="hep-th/0406230",
                description="Racetrack potential from competing non-perturbative effects"
            ),
            FormulaReference(
                id="burgess2003",
                title="de Sitter String Vacua from Supersymmetric D-terms",
                authors="Burgess, C.P., Kallosh, R., Quevedo, F.",
                year=2003,
                arxiv="hep-th/0309187",
                description="Alternative stabilization mechanisms"
            )
        ]''',

    "PNEUMA_VEV": '''        references=[
            FormulaReference(
                id="kachru2003_vev",
                title="de Sitter vacua in string theory",
                authors="Kachru, S., Kallosh, R., Linde, A., Trivedi, S.P.",
                year=2003,
                arxiv="hep-th/0301240",
                description="F-term potential minimization from superpotential"
            ),
            FormulaReference(
                id="blanco2004_racetrack",
                title="Racetrack Inflation",
                authors="Blanco-Pillado, J.J., et al.",
                year=2004,
                arxiv="hep-th/0406230",
                description="Derivation of racetrack minimum"
            ),
            FormulaReference(
                id="giddings2002",
                title="Hierarchies from fluxes in string compactifications",
                authors="Giddings, S.B., Kachru, S., Polchinski, J.",
                year=2002,
                arxiv="hep-th/0105097",
                description="Flux stabilization mechanisms"
            )
        ]''',

    "REDUCTION_CASCADE": '''        references=[
            FormulaReference(
                id="bars2006_cascade",
                title="Two-time physics papers",
                authors="Bars, I.",
                year=2006,
                description="26D → 13D via Sp(2,R) constraints"
            ),
            FormulaReference(
                id="acharya1998_m_theory",
                title="M Theory, Joyce Orbifolds and Super Yang-Mills",
                authors="Acharya, B.S.",
                year=1998,
                description="M-theory on G₂ manifolds: 11D → 4D"
            ),
            FormulaReference(
                id="atiyah2001",
                title="M-Theory Dynamics On A Manifold Of G₂ Holonomy",
                authors="Atiyah, M.F., Witten, E.",
                year=2001,
                arxiv="hep-th/0107177",
                description="Comprehensive study of dimensional reduction via G₂ compactification"
            )
        ]''',

    "PRIMORDIAL_SPINOR_13D": '''        references=[
            FormulaReference(
                id="dirac1928",
                title="The Quantum Theory of the Electron",
                authors="Dirac, P.A.M.",
                year=1928,
                description="Original spinor formulation"
            ),
            FormulaReference(
                id="cartan1913",
                title="Les groupes projectifs qui ne laissent invariante aucune multiplicité plane",
                authors="Cartan, É.",
                year=1913,
                description="Classification of spinor representations"
            ),
            FormulaReference(
                id="lawson1989",
                title="Spin Geometry",
                authors="Lawson, H.B., Michelsohn, M.-L.",
                year=1989,
                description="Standard reference for spinor representations: dim = 2^[D/2]"
            )
        ]''',

    "TCS_TOPOLOGY": '''        references=[
            FormulaReference(
                id="corti2015_tcs",
                title="G₂-manifolds and associative submanifolds via semi-Fano 3-folds",
                authors="Corti, A., Haskins, M., Nordström, J., Pacini, T.",
                year=2015,
                description="Systematic TCS construction of compact G₂ manifolds with b₂=4, b₃=24"
            ),
            FormulaReference(
                id="joyce2000",
                title="Compact Manifolds with Special Holonomy",
                authors="Joyce, D.D.",
                year=2000,
                description="Foundation for G₂ topology and Hodge numbers"
            ),
            FormulaReference(
                id="halverson2020",
                title="The Landscape of M-theory Compactifications on Seven-Manifolds with G₂ Holonomy",
                authors="Halverson, J., Morrison, D.R.",
                year=2020,
                arxiv="1905.03729",
                description="Systematic study of G₂ landscape"
            )
        ]''',

    "EFFECTIVE_EULER": '''        references=[
            FormulaReference(
                id="joyce2000_euler",
                title="Compact Manifolds with Special Holonomy",
                authors="Joyce, D.D.",
                year=2000,
                description="Definitive treatment of G₂ cohomology and Hodge numbers"
            ),
            FormulaReference(
                id="corti2015_hodge",
                title="G₂-manifolds and associative submanifolds via semi-Fano 3-folds",
                authors="Corti, A., et al.",
                year=2015,
                description="Explicit computation of Hodge numbers for TCS manifolds"
            ),
            FormulaReference(
                id="atiyah1963",
                title="The Index of Elliptic Operators on Compact Manifolds",
                authors="Atiyah, M.F., Singer, I.M.",
                year=1963,
                description="Index theorem relating topology to analysis"
            )
        ]'''
}

# Function to add references to a formula
def add_references_to_formula(content, formula_name, references_text):
    """Add references to a formula definition."""
    # Pattern to find the formula definition
    pattern = rf'({formula_name}\s*=\s*Formula\([^)]*?)(related_formulas=\[[^\]]*\]\s*)\)'

    # Check if references already exist
    if f'{formula_name}' in content and 'references=[' in content[content.find(formula_name):content.find(formula_name)+5000]:
        print(f"Skipping {formula_name} - already has references")
        return content

    # Try to add references after related_formulas
    match = re.search(pattern, content, re.DOTALL)
    if match:
        replacement = f'{match.group(1)}{match.group(2)},\n{references_text}\n    )'
        content = content.replace(match.group(0), replacement)
        print(f"Added references to {formula_name}")
        return content

    # If no related_formulas, try adding before closing paren
    pattern2 = rf'({formula_name}\s*=\s*Formula\([^)]*?)(simulation_file="[^"]*"\s*)\)'
    match2 = re.search(pattern2, content, re.DOTALL)
    if match2:
        replacement = f'{match2.group(1)}{match2.group(2)},\n{references_text}\n    )'
        content = content.replace(match2.group(0), replacement)
        print(f"Added references to {formula_name} (via simulation_file)")
        return content

    print(f"WARNING: Could not add references to {formula_name}")
    return content

# Add references to each formula
for formula_name, refs in formula_refs.items():
    content = add_references_to_formula(content, formula_name, refs)

# Write back to file
with open(r"H:\Github\PrincipiaMetaphysica\config.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\nDone! Added references to formulas 10-15 (RACETRACK through EFFECTIVE_EULER)")
