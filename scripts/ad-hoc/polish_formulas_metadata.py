"""
Script to polish formula metadata for rich rendering.
This script updates HIGGS_MASS, DARK_ENERGY_W0, and CP_PHASE_GEOMETRIC formulas.
"""

import re

def polish_higgs_mass_in_file(filepath):
    """Polish HIGGS_MASS formula metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find HIGGS_MASS formula and replace just the terms
    old_terms = r'''        terms=\{
            "m_h": FormulaTerm\("Higgs Mass", "LHC measured value"\),
            "Re\(T\)": FormulaTerm\("Volume Modulus", "= 7\.086, fixed by m_h constraint"\),
        \},'''

    new_terms = '''        terms={
            "m_h": FormulaTerm(
                name="Higgs Boson Mass",
                description="Mass of the Standard Model Higgs boson measured at LHC",
                symbol="m_h",
                value="125.10 GeV",
                units="GeV",
                oom=2.10,
                contribution="Experimental input that constrains moduli",
                link="sections/gauge-unification.html"
            ),
            "Re(T)": FormulaTerm(
                name="Volume Modulus (Real Part)",
                description="Real part of Kähler modulus T controlling G₂ volume",
                symbol="Re(T)",
                value="7.086",
                units="dimensionless",
                contribution="Derived value from m_h constraint",
                link="foundations/moduli-stabilization.html"
            ),
        },
        info_title="Higgs Mass Constrains Moduli",
        info_meaning="Unlike most entries, the Higgs mass is NOT a prediction of PM—it is an experimental INPUT. The measured value m_h = 125.10 GeV from the LHC is used as a constraint to determine the volume modulus Re(T) = 7.086. This modulus then feeds into other predictions like fermion masses and coupling constants.",
        info_grid=[
            FormulaInfoItem(title="LHC Measurement", content="125.10 ± 0.14 GeV"),
            FormulaInfoItem(title="Role in PM", content="INPUT (not prediction)"),
            FormulaInfoItem(title="Constrains", content="Re(T) = 7.086"),
            FormulaInfoItem(title="Discovery", content="ATLAS & CMS (2012)"),
        ],
        expansion_title="m_h = 125.10\\\\,\\\\text{GeV} \\\\quad \\\\Rightarrow \\\\quad \\\\text{Re}(T) = 7.086",
        sub_components=[
            FormulaSubComponent(symbol="m_h", name="Higgs Mass", description="Measured at LHC: 125.10 ± 0.14 GeV", badge="ESTABLISHED", badge_type="established"),
            FormulaSubComponent(symbol="Re(T)", name="Volume Modulus", description="Derived from m_h via scalar potential minimum", badge="CONSTRAINED", badge_type="theory"),
        ],
        derivation_chain=[
            FormulaDerivationStep(title="LHC Discovery (2012)", badge="EXPERIMENTAL", badge_type="established"),
            FormulaDerivationStep(title="Scalar Potential Minimization", link="foundations/moduli-stabilization.html", badge="THEORY", badge_type="theory"),
        ],
        discussion="The Higgs mass m_h = 125.10 GeV is a phenomenological INPUT to PM, not a prediction. This experimental value from the LHC discovery serves as a crucial constraint on the theory's free parameters, fixing the volume modulus Re(T) = 7.086.",'''

    content = re.sub(old_terms, new_terms, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Polished HIGGS_MASS formula metadata")

if __name__ == "__main__":
    filepath = r"h:\Github\PrincipiaMetaphysica\config.py"
    print("Polishing formula metadata in config.py...")
    polish_higgs_mass_in_file(filepath)
    print("Done!")
