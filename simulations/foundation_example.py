"""
Example script demonstrating the foundation schema system.

This script shows how to:
1. Create foundation entries programmatically
2. Add formulas to foundations
3. Validate entries
4. Save to theory_output.json
5. Generate templates
"""

from foundation_schema import (
    FoundationEntry,
    FormulaEntry,
    CATEGORY_GEOMETRY,
    CATEGORY_QUANTUM,
    CATEGORY_GRAVITY,
    CATEGORY_TOPOLOGY,
    BADGE_ESTABLISHED,
    BADGE_NOVEL,
    load_foundations_from_theory_output,
    save_foundations_to_theory_output,
    validate_all_foundations,
    generate_html_template,
    generate_json_template,
)


def create_riemannian_geometry_foundation():
    """Create a foundation entry for Riemannian Geometry."""

    # Create related formulas
    metric_tensor = FormulaEntry(
        id="metric-tensor",
        label="Metric Tensor",
        plain_text="ds² = g_μν dx^μ dx^ν",
        latex=r"ds^2 = g_{\mu\nu} dx^\mu dx^\nu",
        validated=True,
        description="Line element in Riemannian geometry"
    )

    christoffel = FormulaEntry(
        id="christoffel-symbol",
        label="Christoffel Symbol",
        plain_text="Γ^λ_μν = ½ g^λρ (∂_μ g_νρ + ∂_ν g_μρ - ∂_ρ g_μν)",
        latex=r"\Gamma^\lambda_{\mu\nu} = \frac{1}{2} g^{\lambda\rho} (\partial_\mu g_{\nu\rho} + \partial_\nu g_{\mu\rho} - \partial_\rho g_{\mu\nu})",
        validated=True,
        description="Connection coefficients for covariant derivative"
    )

    riemann_tensor = FormulaEntry(
        id="riemann-tensor",
        label="Riemann Curvature Tensor",
        plain_text="R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ",
        latex=r"R^\rho_{\sigma\mu\nu} = \partial_\mu \Gamma^\rho_{\nu\sigma} - \partial_\nu \Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda} \Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda} \Gamma^\lambda_{\mu\sigma}",
        validated=True,
        description="Fundamental measure of spacetime curvature"
    )

    # Create foundation
    foundation = FoundationEntry(
        id="riemannian-geometry",
        title="Riemannian Geometry",
        category=CATEGORY_GEOMETRY,
        year_established=1854,
        badge_type=BADGE_ESTABLISHED,
        main_equation="ds² = g_μν dx^μ dx^ν",
        main_equation_latex=r"ds^2 = g_{\mu\nu} dx^\mu dx^\nu",
        summary="Riemannian geometry studies smooth manifolds equipped with a Riemannian metric, providing the mathematical framework for understanding curved spaces. It forms the geometric foundation for general relativity.",
        key_properties=[
            "Metric tensor defines inner product on tangent space",
            "Curvature characterized by Riemann tensor",
            "Geodesics as paths of parallel transport",
            "Covariant derivative preserves geometric structure",
            "Local vs global geometric properties"
        ],
        pm_connection="The Pneuma field in Principia Metaphysica exists on a Riemannian manifold with signature (3,1), inheriting the geometric structure of spacetime. The TCS topology induces additional curvature beyond standard GR, manifesting as dark energy and providing a geometric mechanism for consciousness-matter coupling.",
        formulas=[metric_tensor, christoffel, riemann_tensor],
        references=[
            "Riemann, B. (1854). Über die Hypothesen, welche der Geometrie zu Grunde liegen.",
            "Lee, J. M. (2018). Introduction to Riemannian Manifolds. Springer.",
            "do Carmo, M. P. (1992). Riemannian Geometry. Birkhäuser."
        ],
        tags=["geometry", "manifolds", "curvature", "general-relativity"]
    )

    return foundation


def create_quantum_field_theory_foundation():
    """Create a foundation entry for Quantum Field Theory."""

    # Create formulas
    lagrangian = FormulaEntry(
        id="qft-lagrangian",
        label="QFT Lagrangian Density",
        plain_text="L = ψ̄(iγ^μ D_μ - m)ψ - ¼ F_μν F^μν",
        latex=r"\mathcal{L} = \bar{\psi}(i\gamma^\mu D_\mu - m)\psi - \frac{1}{4} F_{\mu\nu} F^{\mu\nu}",
        validated=True,
        description="Dirac fermion coupled to gauge field"
    )

    propagator = FormulaEntry(
        id="fermion-propagator",
        label="Fermion Propagator",
        plain_text="S_F(p) = i/(γ^μ p_μ - m + iε)",
        latex=r"S_F(p) = \frac{i}{\gamma^\mu p_\mu - m + i\epsilon}",
        validated=True,
        description="Feynman propagator for fermion field"
    )

    foundation = FoundationEntry(
        id="quantum-field-theory",
        title="Quantum Field Theory",
        category=CATEGORY_QUANTUM,
        year_established=1948,
        badge_type=BADGE_ESTABLISHED,
        main_equation="⟨0|T{φ(x₁)φ(x₂)...φ(xₙ)}|0⟩",
        main_equation_latex=r"\langle 0 | T\{\phi(x_1)\phi(x_2)\cdots\phi(x_n)\} | 0 \rangle",
        summary="Quantum Field Theory combines quantum mechanics and special relativity by treating fields as fundamental quantum objects. It provides the framework for the Standard Model of particle physics.",
        key_properties=[
            "Fields are operator-valued distributions",
            "Particle creation and annihilation",
            "Feynman path integral formulation",
            "Renormalization of infinities",
            "Gauge invariance and symmetries",
            "S-matrix and scattering amplitudes"
        ],
        pm_connection="The Pneuma Lagrangian extends QFT by incorporating topological field configurations and consciousness coupling terms. The TCS cycles provide a geometric quantization mechanism that naturally explains fermion generations and gauge group structure.",
        formulas=[lagrangian, propagator],
        references=[
            "Weinberg, S. (1995). The Quantum Theory of Fields, Vol. 1. Cambridge University Press.",
            "Peskin, M. E., & Schroeder, D. V. (1995). An Introduction to Quantum Field Theory. Westview Press.",
            "Schwartz, M. D. (2014). Quantum Field Theory and the Standard Model. Cambridge University Press."
        ],
        tags=["quantum", "field-theory", "standard-model", "particle-physics"]
    )

    return foundation


def create_pm_novel_foundation():
    """Create a novel PM foundation entry."""

    tcs_formula = FormulaEntry(
        id="tcs-cycle-condition",
        label="TCS Cycle Condition",
        plain_text="R_μν = Λ g_μν + 8πG T_μν^(pneuma)",
        latex=r"R_{\mu\nu} = \Lambda g_{\mu\nu} + 8\pi G T_{\mu\nu}^{(\text{pneuma})}",
        validated=True,
        description="Modified Einstein equation with Pneuma stress-energy"
    )

    consciousness_coupling = FormulaEntry(
        id="consciousness-coupling",
        label="Consciousness Coupling",
        plain_text="S_c = ∫ d⁴x √(-g) κ Ψ̄ γ^μ ∂_μ Φ Ψ",
        latex=r"S_c = \int d^4x \sqrt{-g} \, \kappa \bar{\Psi} \gamma^\mu \partial_\mu \Phi \Psi",
        validated=True,
        description="Coupling between consciousness field and Pneuma"
    )

    foundation = FoundationEntry(
        id="tcs-topology",
        title="Topological Cycle Separation (TCS)",
        category=CATEGORY_TOPOLOGY,
        year_established=2024,
        badge_type=BADGE_NOVEL,
        main_equation="K = |H₁(M₄; ℤ)| = 3 (generations)",
        main_equation_latex=r"K = |H_1(M_4; \mathbb{Z})| = 3 \text{ (generations)}",
        summary="TCS theory proposes that spacetime topology contains non-trivial 1-cycles that separate into K=3 distinct sectors, providing a geometric origin for the three fermion generations. Each cycle corresponds to a topological defect in the Pneuma field.",
        key_properties=[
            "Non-trivial first homology: H₁(M₄; ℤ) ≅ ℤ³",
            "Three topologically distinct cycles (K=3)",
            "Geometric selection rule suppressing proton decay",
            "Dark energy from topological tension",
            "Consciousness coupling through cycle orientation",
            "Natural gauge group structure from cycle symmetries"
        ],
        pm_connection="TCS topology is the central innovation of Principia Metaphysica. It provides geometric explanations for: (1) three fermion generations, (2) gauge group SU(3)×SU(2)×U(1), (3) proton stability, (4) dark energy, and (5) consciousness-matter interaction. The topological structure emerges naturally from the Pneuma Lagrangian.",
        formulas=[tcs_formula, consciousness_coupling],
        references=[
            "Principia Metaphysica (2024). Section 3: Pneuma Lagrangian and TCS Topology.",
            "Hatcher, A. (2002). Algebraic Topology. Cambridge University Press. (Mathematical foundation)",
            "Nakahara, M. (2003). Geometry, Topology and Physics. Taylor & Francis. (Physics applications)"
        ],
        tags=["topology", "pm-novel", "tcs", "fermion-generations", "dark-energy", "consciousness"]
    )

    return foundation


def main():
    """Main demonstration function."""

    print("=" * 80)
    print("Foundation Schema System - Example Usage")
    print("=" * 80)
    print()

    # Create foundations
    print("Creating foundation entries...")
    foundations_to_add = [
        create_riemannian_geometry_foundation(),
        create_quantum_field_theory_foundation(),
        create_pm_novel_foundation(),
    ]

    print(f"Created {len(foundations_to_add)} new foundations:")
    for f in foundations_to_add:
        print(f"  - {f.title} ({f.category}, {f.year_established})")
    print()

    # Validate all
    print("Validating foundations...")
    report = validate_all_foundations(foundations_to_add)
    print(f"Validation: {report['valid']}/{report['total']} passed")

    if report['invalid'] > 0:
        print("ERRORS FOUND:")
        for error_info in report['errors']:
            print(f"\n{error_info['title']}:")
            for error in error_info['errors']:
                print(f"  - {error}")
        return

    print("All foundations are valid!")
    print()

    # Load existing foundations
    print("Loading existing foundations from theory_output.json...")
    existing = load_foundations_from_theory_output('theory_output.json')
    print(f"Found {len(existing)} existing foundations")

    # Merge (avoid duplicates by ID)
    existing_ids = {f.id for f in existing}
    for foundation in foundations_to_add:
        if foundation.id not in existing_ids:
            existing.append(foundation)
            print(f"  + Added: {foundation.id}")
        else:
            print(f"  = Exists: {foundation.id}")
    print()

    # Save
    print("Saving foundations to theory_output.json...")
    success = save_foundations_to_theory_output(existing, 'theory_output.json', merge=True)

    if success:
        print(f"Successfully saved {len(existing)} foundations!")
    else:
        print("Error saving foundations")
        return

    print()

    # Generate example HTML
    print("Generating example HTML template...")
    pm_foundation = create_pm_novel_foundation()
    html = generate_html_template(pm_foundation)

    html_file = 'output/tcs-topology-foundation.html'
    import os
    os.makedirs('output', exist_ok=True)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML template written to: {html_file}")
    print()

    # Generate example JSON
    print("Generating example JSON template...")
    json_str = generate_json_template(pm_foundation)

    json_file = 'output/tcs-topology-foundation.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(f"JSON template written to: {json_file}")
    print()

    print("=" * 80)
    print("Example completed successfully!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. View foundations: python simulations/foundation_manager.py list")
    print("  2. Validate: python simulations/foundation_manager.py validate")
    print("  3. Generate report: python simulations/foundation_manager.py report")
    print("  4. Export HTML: python simulations/foundation_manager.py export-html")
    print()


if __name__ == "__main__":
    main()
