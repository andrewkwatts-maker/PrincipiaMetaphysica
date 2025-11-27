"""
cross_references.py - Cross-Reference Map for HTML Pages and Python Modules
Principia Metaphysica v6.1+

This module provides a mapping between HTML content and Python implementations.
Use this to quickly find where specific predictions or calculations are implemented.

Usage:
    from cross_references import find_implementation, list_all_references

    # Find where a prediction is implemented
    find_implementation("dark energy w_0")

    # List all cross-references
    list_all_references()
"""

# ==============================================================================
# CROSS-REFERENCE DICTIONARY
# ==============================================================================

CROSS_REFERENCES = {
    # Core Predictions
    "dark_energy_w0": {
        "html_pages": ["index.html", "beginners-guide.html", "sections/cosmology.html"],
        "python_modules": ["config.py::PhenomenologyParameters", "SimulateTheory.py::derive_all_parameters"],
        "config_parameter": "PhenomenologyParameters.w0_value()",
        "equation_number": "Eq. 2.1",
        "description": "Dark energy equation of state at z=0: w_0 = -11/13"
    },

    "dark_energy_wa": {
        "html_pages": ["index.html", "sections/cosmology.html"],
        "python_modules": ["config.py::PhenomenologyParameters", "SimulateTheory.py::derive_all_parameters"],
        "config_parameter": "PhenomenologyParameters.WA_EVOLUTION",
        "equation_number": "Eq. 2.2",
        "description": "Dark energy evolution parameter: w_a = -0.75"
    },

    "generations": {
        "html_pages": ["index.html", "beginners-guide.html"],
        "python_modules": ["config.py::FundamentalConstants", "SimulateTheory.py::derive_all_parameters"],
        "config_parameter": "FundamentalConstants.fermion_generations()",
        "equation_number": "Eq. 1.8",
        "description": "Fermion generations from χ/48 = 3"
    },

    "proton_decay": {
        "html_pages": ["index.html", "computational-appendices.html"],
        "python_modules": [
            "config.py::PhenomenologyParameters",
            "validation_modules.py::propagate_error_proton_decay",
            "proton_decay_corrected.py",
            "proton_decay_dimensional.py",
            "proton_decay_rg.py"
        ],
        "config_parameter": "PhenomenologyParameters.TAU_PROTON",
        "equation_number": "Eq. 3.4",
        "description": "Proton lifetime τ_p = 3.5×10^34 years"
    },

    # Dimensional Structure
    "dimensions_26D": {
        "html_pages": ["index.html", "beginners-guide.html"],
        "python_modules": ["config.py::FundamentalConstants"],
        "config_parameter": "FundamentalConstants.D_BULK",
        "equation_number": "Eq. 1.1",
        "description": "26D bulk spacetime from Virasoro anomaly"
    },

    "dimensions_13D": {
        "html_pages": ["index.html", "beginners-guide.html"],
        "python_modules": ["config.py::FundamentalConstants"],
        "config_parameter": "FundamentalConstants.D_INTERNAL",
        "equation_number": "Eq. 1.2",
        "description": "13D effective dimension after Sp(2,R) gauge fixing"
    },

    "brane_hierarchy": {
        "html_pages": ["index.html", "beginners-guide.html"],
        "python_modules": ["config.py::FundamentalConstants"],
        "config_parameter": "FundamentalConstants.N_BRANES, SPATIAL_DIMS, TIME_DIMS",
        "equation_number": "Eq. 1.3",
        "description": "4 branes × 3 spatial + 1 time = 13D"
    },

    # Multi-Time Physics
    "gw_dispersion": {
        "html_pages": ["index.html", "computational-appendices.html"],
        "python_modules": [
            "config.py::MultiTimeParameters",
            "gw_dispersion.py",
            "SimulateTheory.py::derive_all_parameters"
        ],
        "config_parameter": "MultiTimeParameters.XI_QUADRATIC, eta_linear()",
        "equation_number": "Eq. 4.2",
        "description": "GW dispersion relation with ξ and η coefficients"
    },

    "orthogonal_time": {
        "html_pages": ["index.html", "philosophical-implications.html"],
        "python_modules": ["config.py::MultiTimeParameters"],
        "config_parameter": "MultiTimeParameters.DELTA_T_ORTHO",
        "equation_number": "Eq. 4.1",
        "description": "Orthogonal time delay Δt_ortho ~ 10^-18 s"
    },

    # Moduli Stabilization
    "swampland_constraint": {
        "html_pages": ["index.html", "computational-appendices.html"],
        "python_modules": ["config.py::ModuliParameters", "SimulateTheory.py::derive_all_parameters"],
        "config_parameter": "ModuliParameters.a_swampland(), SWAMPLAND_BOUND",
        "equation_number": "Eq. 5.3",
        "description": "Swampland constraint: a = √2 > √(2/3)"
    },

    "moduli_potential": {
        "html_pages": ["computational-appendices.html"],
        "python_modules": ["moduli_simulation.py", "config.py::ModuliParameters"],
        "config_parameter": "ModuliParameters (all)",
        "equation_number": "Eq. 5.1",
        "description": "KKLT moduli potential V(φ)"
    },

    # v6.1 New Predictions
    "kaluza_klein_modes": {
        "html_pages": ["index.html"],
        "python_modules": ["config.py::V61Predictions"],
        "config_parameter": "V61Predictions.M_KK_CENTRAL, M_KK_MIN, M_KK_MAX",
        "equation_number": "Eq. 6.1",
        "description": "KK mode mass m_KK = 5 ± 2 TeV (LHC-testable)"
    },

    "chsh_violation": {
        "html_pages": ["index.html"],
        "python_modules": ["config.py::V61Predictions", "validation_modules.py::simulate_retrocausal_chsh"],
        "config_parameter": "V61Predictions.CHSH_DELTA_ORTHO, CHSH_PREDICTED",
        "equation_number": "Eq. 6.3",
        "description": "CHSH inequality with retrocausal correction"
    },

    "mirror_sector": {
        "html_pages": ["index.html"],
        "python_modules": ["config.py::V61Predictions"],
        "config_parameter": "V61Predictions.DELTA_N_EFF_CENTRAL",
        "equation_number": "Eq. 6.4",
        "description": "Mirror sector dark radiation ΔN_eff ~ 0.12"
    },

    # Modified Gravity
    "f_r_t_tau": {
        "html_pages": ["sections/cosmology.html"],
        "python_modules": ["config.py::FRTTauParameters", "SimulateTheory.py::derive_all_parameters"],
        "config_parameter": "FRTTauParameters (all coefficients)",
        "equation_number": "Eq. 2.5",
        "description": "F(R,T,τ) modified gravity with quantum corrections"
    },

    "thermal_time": {
        "html_pages": ["sections/cosmology.html", "philosophical-implications.html"],
        "python_modules": ["config.py::ThermalTimeParameters"],
        "config_parameter": "ThermalTimeParameters.ALPHA_T_CANONICAL",
        "equation_number": "Eq. 2.3",
        "description": "Thermal time hypothesis: α_T = 2.7"
    },

    # Landscape/Multiverse
    "landscape_entropy": {
        "html_pages": ["computational-appendices.html"],
        "python_modules": [
            "config.py::LandscapeParameters",
            "validation_modules.py::count_landscape_vacua"
        ],
        "config_parameter": "LandscapeParameters.landscape_entropy()",
        "equation_number": "Eq. 7.2",
        "description": "Landscape entropy S ~ 1151"
    },

    "cmb_bubbles": {
        "html_pages": ["computational-appendices.html"],
        "python_modules": [
            "config.py::CMBBubbleParameters",
            "validation_modules.py::simulate_cmb_bubble_statistics"
        ],
        "config_parameter": "CMBBubbleParameters (all)",
        "equation_number": "Eq. 7.5",
        "description": "CMB bubble collision statistics"
    },

    # Neutrinos
    "neutrino_hierarchy": {
        "html_pages": ["index.html"],
        "python_modules": ["config.py::NeutrinoParameters"],
        "config_parameter": "NeutrinoParameters.HIERARCHY_PREDICTION",
        "equation_number": "Eq. 3.6",
        "description": "Normal hierarchy prediction (PRIMARY FALSIFICATION TEST)"
    },

    # Gauge Unification
    "gut_scale": {
        "html_pages": ["computational-appendices.html"],
        "python_modules": ["config.py::GaugeUnificationParameters"],
        "config_parameter": "GaugeUnificationParameters.M_GUT",
        "equation_number": "Eq. 3.1",
        "description": "GUT scale M_GUT ~ 1.8×10^16 GeV"
    }
}


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def find_implementation(search_term):
    """
    Find Python implementations for a given topic.

    Args:
        search_term: Topic to search for (e.g., "dark energy", "proton decay")

    Returns:
        List of matching cross-references
    """
    search_lower = search_term.lower()
    matches = []

    for key, ref in CROSS_REFERENCES.items():
        if search_lower in key.lower() or search_lower in ref["description"].lower():
            matches.append({
                "key": key,
                "reference": ref
            })

    return matches


def list_all_references():
    """
    Print all cross-references in a readable format.
    """
    print("=" * 80)
    print("CROSS-REFERENCE MAP: HTML Pages ↔ Python Modules")
    print("=" * 80)
    print()

    for key, ref in CROSS_REFERENCES.items():
        print(f"{key.upper().replace('_', ' ')}")
        print(f"  Description: {ref['description']}")
        print(f"  Equation: {ref['equation_number']}")
        print(f"  HTML Pages: {', '.join(ref['html_pages'])}")
        print(f"  Python Modules: {', '.join(ref['python_modules'])}")
        print(f"  Config Parameter: {ref['config_parameter']}")
        print()


def get_module_for_equation(equation_number):
    """
    Find which Python module implements a specific equation.

    Args:
        equation_number: Equation identifier (e.g., "Eq. 2.1")

    Returns:
        Cross-reference dict or None
    """
    for key, ref in CROSS_REFERENCES.items():
        if ref["equation_number"] == equation_number:
            return ref
    return None


def get_equations_in_module(module_name):
    """
    Find all equations implemented in a specific Python module.

    Args:
        module_name: Name of Python module (e.g., "config.py")

    Returns:
        List of cross-references
    """
    equations = []
    for key, ref in CROSS_REFERENCES.items():
        for module in ref["python_modules"]:
            if module_name in module:
                equations.append({
                    "key": key,
                    "equation": ref["equation_number"],
                    "description": ref["description"]
                })
                break
    return equations


# ==============================================================================
# COMMAND-LINE INTERFACE
# ==============================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            list_all_references()

        elif command == "find" and len(sys.argv) > 2:
            search_term = " ".join(sys.argv[2:])
            matches = find_implementation(search_term)

            if matches:
                print(f"Found {len(matches)} match(es) for '{search_term}':")
                print()
                for match in matches:
                    ref = match["reference"]
                    print(f"{match['key'].upper().replace('_', ' ')}")
                    print(f"  {ref['description']}")
                    print(f"  Python: {', '.join(ref['python_modules'])}")
                    print()
            else:
                print(f"No matches found for '{search_term}'")

        elif command == "equation" and len(sys.argv) > 2:
            eq_num = sys.argv[2]
            ref = get_module_for_equation(eq_num)

            if ref:
                print(f"Equation {eq_num}:")
                print(f"  {ref['description']}")
                print(f"  Python: {', '.join(ref['python_modules'])}")
            else:
                print(f"Equation {eq_num} not found in cross-reference map")

        elif command == "module" and len(sys.argv) > 2:
            module = sys.argv[2]
            equations = get_equations_in_module(module)

            if equations:
                print(f"Equations in {module}:")
                for eq in equations:
                    print(f"  {eq['equation']}: {eq['description']}")
            else:
                print(f"No equations found for module {module}")

        else:
            print("Usage:")
            print("  python cross_references.py list")
            print("  python cross_references.py find <search term>")
            print("  python cross_references.py equation <Eq. X.Y>")
            print("  python cross_references.py module <module.py>")

    else:
        print(__doc__)
        print("\nQuick Examples:")
        print("  python cross_references.py find dark energy")
        print("  python cross_references.py equation 'Eq. 2.1'")
        print("  python cross_references.py module config.py")
        print("  python cross_references.py list")
