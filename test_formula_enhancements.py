#!/usr/bin/env python3
"""
Test script for enhanced Formula dataclass with rich UX rendering support.
"""

from config import (
    Formula,
    FormulaTerm,
    FormulaInfoItem,
    FormulaSubComponent,
    FormulaDerivationStep,
    FormulaCategory
)

def test_enhanced_formula():
    """Test the enhanced Formula dataclass with all rich UX fields."""

    # Create formula terms with contribution field
    term_action = FormulaTerm(
        symbol="S_26D",
        name="S<sub>26D</sub> - Master Action",
        description="The total 26-dimensional action - the ultimate quantity from which ALL physics derives.",
        units="Dimensionless (natural units)",
        contribution="This is the fundamental action from which all physics emerges.",
        link="paper.html#framework"
    )

    # Create info grid items
    info_items = [
        FormulaInfoItem(
            title="Full Bulk",
            content="26D with signature (24,2)",
            link="paper.html#section-2"
        ),
        FormulaInfoItem(
            title="Effective Shadow",
            content="13D with signature (12,1)",
            link="paper.html#section-2"
        ),
        FormulaInfoItem(
            title="Gauge Group",
            content="SO(10) ⊃ G_SM",
            link="paper.html#section-3"
        )
    ]

    # Create sub-components
    sub_comps = [
        FormulaSubComponent(
            symbol="M<sub>*</sub><sup>11</sup>R<sub>13</sub>",
            name="13D Einstein-Hilbert Term",
            description="13D gravity with signature (12,1): M* is the reduced Planck mass in 13D, R_13 is the 13D Ricci scalar.",
            link="foundations/einstein-hilbert-action.html",
            badge="Established",
            badge_type="established"
        ),
        FormulaSubComponent(
            symbol="Γ<sup>M</sup>",
            name="13D Gamma Matrices",
            description="64×64 matrices from Clifford algebra Cl(12,1). M = 0,1,...,12.",
            link="foundations/dirac-equation.html",
            badge="Clifford Algebra",
            badge_type="established"
        )
    ]

    # Create derivation chain
    deriv_chain = [
        FormulaDerivationStep(
            title="Dirac Equation (1928)",
            link="foundations/dirac-equation.html",
            badge="Established",
            badge_type="established"
        ),
        FormulaDerivationStep(
            title="Einstein-Hilbert Action (1915)",
            link="foundations/einstein-hilbert-action.html",
            badge="Established",
            badge_type="established"
        ),
        FormulaDerivationStep(
            title="Kaluza-Klein Theory (1921)",
            link="foundations/kaluza-klein.html",
            badge="Established",
            badge_type="established"
        )
    ]

    # Create enhanced formula
    formula = Formula(
        id="master-action",
        label="(1.1) Master Action",
        html="S<sub>26D</sub> = ∫ d<sup>26</sup>X √|G<sub>(24,2)</sub>| [M<sub>26</sub><sup>24</sup>R<sub>26</sub> + ...]",
        latex=r"S_{26D} = \int d^{26}X \sqrt{|G_{(24,2)}|} [M_{26}^{24}R_{26} + ...]",
        plain_text="S_26D = ∫ d^26X √|G_(24,2)| [M_26^24 R_26 + ...]",
        category=FormulaCategory.THEORY,
        description="The unified 26-dimensional action principle",
        section="2.1",

        # Enhanced UX fields
        html_interactive='<a class="formula-var" href="paper.html#framework">S<sub>26D</sub></a>',
        info_title="Unified 26-dimensional Action Principle",
        info_meaning="This single 26D action with signature (24,2) encodes ALL of physics through dimensional reduction.",
        info_grid=info_items,
        use_cases=[
            "Einstein gravity + cosmological dynamics",
            "Standard Model gauge interactions",
            "Three generations of fermions",
            "Higgs mechanism and electroweak symmetry breaking"
        ],
        expansion_title="S_26D → S_13D → S_4D",
        sub_components=sub_comps,
        derivation_chain=deriv_chain,

        # Regular fields
        terms={"S_26D": term_action},
        status="FOUNDATIONAL"
    )

    # Test serialization
    formula_dict = formula.to_dict()

    # Verify all fields are present
    assert "id" in formula_dict
    assert "htmlInteractive" in formula_dict
    assert "infoTitle" in formula_dict
    assert "infoMeaning" in formula_dict
    assert "infoGrid" in formula_dict
    assert "useCases" in formula_dict
    assert "expansionTitle" in formula_dict
    assert "subComponents" in formula_dict
    assert "derivationChain" in formula_dict

    # Verify nested structures
    assert len(formula_dict["infoGrid"]) == 3
    assert len(formula_dict["useCases"]) == 4
    assert len(formula_dict["subComponents"]) == 2
    assert len(formula_dict["derivationChain"]) == 3

    # Verify term has contribution field
    assert "contribution" in formula_dict["terms"]["S_26D"]

    print("SUCCESS: All enhanced Formula fields work correctly!")
    print(f"\nFormula ID: {formula_dict['id']}")
    print(f"Info Title: {formula_dict['infoTitle']}")
    print(f"Info Grid Items: {len(formula_dict['infoGrid'])}")
    print(f"Use Cases: {len(formula_dict['useCases'])}")
    print(f"Sub-Components: {len(formula_dict['subComponents'])}")
    print(f"Derivation Chain Steps: {len(formula_dict['derivationChain'])}")

    return formula_dict

if __name__ == "__main__":
    test_enhanced_formula()
