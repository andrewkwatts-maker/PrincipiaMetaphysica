#!/usr/bin/env python3
"""
Script to add FormulaReference entries to formulas F21-F40 in config.py
Based on FORMULA_REFERENCES_F21_F40.md
"""

# Read the config.py file
with open("H:\\Github\\PrincipiaMetaphysica\\config.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define replacements as (old_text, new_text) pairs
replacements = [
    # F21: FLUX_QUANTIZATION
    (
        '        computed_value=24,\n        related_formulas=["tcs-topology", "effective-torsion"]\n    )\n\n    EFFECTIVE_TORSION',
        '''        computed_value=24,
        related_formulas=["tcs-topology", "effective-torsion"],
        references=[
            FormulaReference("acharya2002", "M theory, Joyce Orbifolds and Super Yang-Mills", "Acharya, B.S.", 2002, arxiv="hep-th/9812205"),
            FormulaReference("acharya2001", "Chiral Fermions from Manifolds of G₂ Holonomy", "Acharya, B.S. & Witten, E.", 2001, arxiv="hep-th/0109152"),
            FormulaReference("gukov2000", "CFT's from Calabi-Yau four-folds", "Gukov, S., Vafa, C., & Witten, E.", 2000, arxiv="hep-th/9906070"),
        ]
    )

    EFFECTIVE_TORSION'''
    ),

    # F22: EFFECTIVE_TORSION
    (
        '        computed_value=-1.0,\n        related_formulas=["flux-quantization", "tcs-topology"]\n    )\n\n    MIRROR_DM_RATIO',
        '''        computed_value=-1.0,
        related_formulas=["flux-quantization", "tcs-topology"],
        references=[
            FormulaReference("fernandez1982", "Riemannian manifolds with structure group G₂", "Fernández, M. & Gray, A.", 1982, doi="10.1007/BF01760975"),
            FormulaReference("karigiannis2009", "Flows of G₂-structures, I", "Karigiannis, S.", 2009, arxiv="math/0702077"),
            FormulaReference("acharya2004", "Freund-Rubin Revisited", "Acharya, B.S. et al.", 2004, arxiv="hep-th/0308046"),
        ]
    )

    MIRROR_DM_RATIO'''
    ),

    # F23: MIRROR_DM_RATIO
    (
        '        sigma_deviation=0.7,\n        related_formulas=["mirror-temp-ratio"]\n    )\n\n    # =',
        '''        sigma_deviation=0.7,
        related_formulas=["mirror-temp-ratio"],
        references=[
            FormulaReference("foot1991", "A model with fundamental improper spacetime symmetries", "Foot, R., Lew, H., & Volkas, R.R.", 1991, doi="10.1016/0370-2693(91)91013-L"),
            FormulaReference("foot2004", "Experimental implications of mirror matter-type dark matter", "Foot, R.", 2004, arxiv="astro-ph/0309330"),
            FormulaReference("planck2020", "Planck 2018 results. VI. Cosmological parameters", "Planck Collaboration", 2020, arxiv="1807.06209"),
        ]
    )

    # ='''
    ),

    # F26: SO10_BREAKING
    (
        '        section="5",\n        related_formulas=["gut-scale", "gut-coupling"]\n    )\n\n    GUT_COUPLING',
        '''        section="5",
        related_formulas=["gut-scale", "gut-coupling"],
        references=[
            FormulaReference("fritzsch1975", "Unified Interactions of Leptons and Hadrons", "Fritzsch, H. & Minkowski, P.", 1975, doi="10.1016/0003-4916(75)90211-0"),
            FormulaReference("mohapatra1980", "Neutrino Mass and Spontaneous Parity Nonconservation", "Mohapatra, R.N. & Senjanović, G.", 1980, doi="10.1103/PhysRevLett.44.912"),
            FormulaReference("langacker1981", "Grand Unified Theories and Proton Decay", "Langacker, P.", 1981, doi="10.1016/0370-1573(81)90059-4"),
        ]
    )

    GUT_COUPLING'''
    ),

    # F27: GUT_COUPLING
    (
        '        simulation_file="simulations/gauge_unification_precision_v12_4.py",\n        related_formulas=["gut-scale", "tcs-topology"]\n    )\n\n    WEAK_MIXING_ANGLE',
        '''        simulation_file="simulations/gauge_unification_precision_v12_4.py",
        related_formulas=["gut-scale", "tcs-topology"],
        references=[
            FormulaReference("georgi1974", "Hierarchy of Interactions in Unified Gauge Theories", "Georgi, H., Quinn, H.R., & Weinberg, S.", 1974, doi="10.1103/PhysRevLett.33.451"),
            FormulaReference("dimopoulos1981", "Supersymmetry and the Scale of Unification", "Dimopoulos, S., Raby, S., & Wilczek, F.", 1981, doi="10.1103/PhysRevD.24.1681"),
            FormulaReference("amaldi1991", "Comparison of grand unified theories with electroweak and strong coupling constants", "Amaldi, U., de Boer, W., & Fürstenau, H.", 1991, doi="10.1016/0370-2693(91)91641-8"),
        ]
    )

    WEAK_MIXING_ANGLE'''
    ),

    # F28: WEAK_MIXING_ANGLE
    (
        '        simulation_file="simulations/gauge_unification_precision_v12_4.py",\n        related_formulas=["gut-coupling", "gut-scale"]\n    )\n\n    HIGGS_VEV',
        '''        simulation_file="simulations/gauge_unification_precision_v12_4.py",
        related_formulas=["gut-coupling", "gut-scale"],
        references=[
            FormulaReference("weinberg1967", "A Model of Leptons", "Weinberg, S.", 1967, doi="10.1103/PhysRevLett.19.1264"),
            FormulaReference("pdg2024", "Review of Particle Physics", "Particle Data Group", 2024, doi="10.1103/PhysRevD.110.030001"),
            FormulaReference("erler2005", "Weak mixing angle at low energies", "Erler, J. & Ramsey-Musolf, M.J.", 2005, arxiv="hep-ph/0409169"),
        ]
    )

    HIGGS_VEV'''
    ),

    # F29: HIGGS_VEV
    (
        '        units="GeV",\n        related_formulas=["top-quark-mass"]\n    )\n\n    # =',
        '''        units="GeV",
        related_formulas=["top-quark-mass"],
        references=[
            FormulaReference("higgs1964", "Broken Symmetries and the Masses of Gauge Bosons", "Higgs, P.W.", 1964, doi="10.1103/PhysRevLett.13.508"),
            FormulaReference("atlas_cms2015", "Combined Measurement of the Higgs Boson Mass", "ATLAS & CMS Collaborations", 2015, arxiv="1503.07589"),
        ]
    )

    # ='''
    ),

    # F31: TOP_QUARK_MASS
    (
        '        sigma_deviation=0.06,\n        related_formulas=["higgs-vev"]\n    )\n\n    STRONG_COUPLING',
        '''        sigma_deviation=0.06,
        related_formulas=["higgs-vev"],
        references=[
            FormulaReference("cdf_d0_2014", "Combination of CDF and D0 results on the mass of the top quark", "CDF & D0 Collaborations", 2014, arxiv="1407.2682"),
            FormulaReference("pdg2024_top", "Review of Particle Physics (top quark)", "Particle Data Group", 2024, doi="10.1103/PhysRevD.110.030001"),
            FormulaReference("froggatt1979", "Hierarchy of Quark Masses, Cabibbo Angles and CP Violation", "Froggatt, C.D. & Nielsen, H.B.", 1979, doi="10.1016/0550-3213(79)90316-X"),
        ]
    )

    STRONG_COUPLING'''
    ),

    # F32: STRONG_COUPLING
    (
        '        simulation_file="simulations/gauge_unification_precision_v12_4.py",\n        related_formulas=["gut-coupling"]\n    )\n\n    NEUTRINO_MASS_21',
        '''        simulation_file="simulations/gauge_unification_precision_v12_4.py",
        related_formulas=["gut-coupling"],
        references=[
            FormulaReference("gross1973", "Ultraviolet Behavior of Non-Abelian Gauge Theories", "Gross, D.J. & Wilczek, F.", 1973, doi="10.1103/PhysRevLett.30.1343"),
            FormulaReference("politzer1973", "Reliable Perturbative Results for Strong Interactions?", "Politzer, H.D.", 1973, doi="10.1103/PhysRevLett.30.1346"),
            FormulaReference("pdg2024_alpha_s", "Review of Particle Physics (QCD)", "Particle Data Group", 2024, doi="10.1103/PhysRevD.110.030001"),
        ]
    )

    NEUTRINO_MASS_21'''
    ),

    # F33: NEUTRINO_MASS_21
    (
        '        simulation_file="simulations/pmns_full_matrix.py",\n        related_formulas=["neutrino-mass-31", "theta23-maximal"]\n    )\n\n    NEUTRINO_MASS_31',
        '''        simulation_file="simulations/pmns_full_matrix.py",
        related_formulas=["neutrino-mass-31", "theta23-maximal"],
        references=[
            FormulaReference("fukuda1998_sk", "Evidence for oscillation of atmospheric neutrinos", "Fukuda, Y., et al. (Super-Kamiokande)", 1998, arxiv="hep-ex/9807003"),
            FormulaReference("ahmad2002_sno", "Direct Evidence for Neutrino Flavor Transformation", "Ahmad, Q.R., et al. (SNO)", 2002, arxiv="nucl-ex/0204008"),
            FormulaReference("nufit2024", "NuFIT 6.0 (2024)", "Esteban, I., et al.", 2024),
        ]
    )

    NEUTRINO_MASS_31'''
    ),

    # F34: NEUTRINO_MASS_31
    (
        '        simulation_file="simulations/pmns_full_matrix.py",\n        related_formulas=["neutrino-mass-21", "theta23-maximal"]\n    )\n\n    CP_PHASE_GEOMETRIC',
        '''        simulation_file="simulations/pmns_full_matrix.py",
        related_formulas=["neutrino-mass-21", "theta23-maximal"],
        references=[
            FormulaReference("fukuda1998_atm", "Evidence for oscillation of atmospheric neutrinos", "Fukuda, Y., et al. (Super-Kamiokande)", 1998, arxiv="hep-ex/9807003"),
            FormulaReference("t2k2020", "Constraint on the matter-antimatter symmetry-violating phase", "Abe, K., et al. (T2K)", 2020, arxiv="1910.03887"),
            FormulaReference("nufit2024_dm31", "NuFIT 6.0 (2024) - global fit", "Esteban, I., et al.", 2024),
        ]
    )

    CP_PHASE_GEOMETRIC'''
    ),

    # F35: CP_PHASE_GEOMETRIC
    (
        '        simulation_file="simulations/pmns_theta13_delta_geometric_v14_1.py",\n        related_formulas=["tcs-topology"]\n    )\n\n    # =',
        '''        simulation_file="simulations/pmns_theta13_delta_geometric_v14_1.py",
        related_formulas=["tcs-topology"],
        references=[
            FormulaReference("kobayashi1973", "CP-Violation in the Renormalizable Theory of Weak Interaction", "Kobayashi, M. & Maskawa, T.", 1973, doi="10.1143/PTP.49.652"),
            FormulaReference("t2k2020_cp", "Constraint on the matter-antimatter symmetry-violating phase", "Abe, K., et al. (T2K)", 2020, arxiv="1910.03887"),
            FormulaReference("nufit2024_cp", "NuFIT 6.0 (2024) - CP phase", "Esteban, I., et al.", 2024),
        ]
    )

    # ='''
    ),

    # F39: EFFECTIVE_DIMENSION
    (
        '        computed_value=12.576,\n        related_formulas=["dark-energy-w0"]\n    )\n\n    DARK_ENERGY_WA',
        '''        computed_value=12.576,
        related_formulas=["dark-energy-w0"],
        references=[
            FormulaReference("virasoro1970", "Subsidiary Conditions and Ghosts in Dual-Resonance Models", "Virasoro, M.A.", 1970, doi="10.1103/PhysRevD.1.2933"),
            FormulaReference("goddard1973", "Quantum dynamics of a massless relativistic string", "Goddard, P., et al.", 1973, doi="10.1016/0550-3213(73)90223-X"),
            FormulaReference("polchinski1998", "String Theory, Vol. 1: An Introduction to the Bosonic String", "Polchinski, J.", 1998),
        ]
    )

    DARK_ENERGY_WA'''
    ),

    # F40: DARK_ENERGY_WA
    (
        '        simulation_file="simulations/thermal_time_v12_8.py",\n        related_formulas=["dark-energy-w0", "effective-dimension"]\n    )\n\n    THERMAL_TIME',
        '''        simulation_file="simulations/thermal_time_v12_8.py",
        related_formulas=["dark-energy-w0", "effective-dimension"],
        references=[
            FormulaReference("chevallier2001", "Accelerating Universes with Scaling Dark Matter", "Chevallier, M. & Polarski, D.", 2001, arxiv="gr-qc/0009008"),
            FormulaReference("linder2003", "Exploring the Expansion History of the Universe", "Linder, E.V.", 2003, arxiv="astro-ph/0208512"),
            FormulaReference("desi2024", "DESI 2024 VI: Cosmological Constraints from BAO", "DESI Collaboration", 2024, arxiv="2404.03002"),
        ]
    )

    THERMAL_TIME'''
    ),

    # F24: HIERARCHY_RATIO
    (
        '        notes="Natural explanation for 10¹⁶ hierarchy without fine-tuning",\n        related_formulas=["higgs-vev", "tcs-topology"]\n    )\n\n    DIVISION_ALGEBRA',
        '''        notes="Natural explanation for 10¹⁶ hierarchy without fine-tuning",
        related_formulas=["higgs-vev", "tcs-topology"],
        references=[
            FormulaReference("arkani-hamed1998", "The Hierarchy problem and new dimensions at a millimeter", "Arkani-Hamed, N., Dimopoulos, S., & Dvali, G.", 1998, arxiv="hep-ph/9803315"),
            FormulaReference("randall1999", "A Large Mass Hierarchy from a Small Extra Dimension", "Randall, L. & Sundrum, R.", 1999, arxiv="hep-ph/9905221"),
            FormulaReference("kklt2003", "de Sitter Vacua in String Theory", "Kachru, S., Kallosh, R., Linde, A., & Trivedi, S.P.", 2003, arxiv="hep-th/0301240"),
        ]
    )

    DIVISION_ALGEBRA'''
    ),

    # F25: PLANCK_MASS_DERIVATION
    (
        '        related_formulas=["gut-scale", "tcs-topology"]\n    )\n\n    DOUBLET_TRIPLET = Formula(',
        '''        related_formulas=["gut-scale", "tcs-topology"],
        references=[
            FormulaReference("kaluza1921", "Zum Unitätsproblem der Physik", "Kaluza, T.", 1921),
            FormulaReference("klein1926", "Quantentheorie und fünfdimensionale Relativitätstheorie", "Klein, O.", 1926, doi="10.1007/BF01397481"),
            FormulaReference("witten1981", "Search for a Realistic Kaluza-Klein Theory", "Witten, E.", 1981, doi="10.1016/0550-3213(81)90021-3"),
        ]
    )

    DOUBLET_TRIPLET = Formula('''
    ),

    # F30: DOUBLET_TRIPLET
    (
        '        notes="Topological protection against proton decay from Higgs",\n        related_formulas=["proton-lifetime", "so10-breaking"]\n    )\n\n    DIRAC_PNEUMA',
        '''        notes="Topological protection against proton decay from Higgs",
        related_formulas=["proton-lifetime", "so10-breaking"],
        references=[
            FormulaReference("atiyah1963", "The Index of Elliptic Operators on Compact Manifolds", "Atiyah, M.F. & Singer, I.M.", 1963, doi="10.1090/S0002-9904-1963-10957-X"),
            FormulaReference("witten1985", "Symmetry Breaking Patterns in Superstring Models", "Witten, E.", 1985, doi="10.1016/0550-3213(85)90603-0"),
            FormulaReference("kawamura2001", "Triplet-doublet splitting, proton stability and extra dimension", "Kawamura, Y.", 2001, arxiv="hep-ph/0012125"),
        ]
    )

    DIRAC_PNEUMA'''
    ),

    # F36: SEESAW_MECHANISM
    (
        '        related_formulas=["neutrino-mass-21", "neutrino-mass-31"]\n    )\n\n    CKM_ELEMENTS',
        '''        related_formulas=["neutrino-mass-21", "neutrino-mass-31"],
        references=[
            FormulaReference("minkowski1977", "μ → eγ at a Rate of One Out of 10⁹ Muon Decays?", "Minkowski, P.", 1977, doi="10.1016/0370-2693(77)90435-X"),
            FormulaReference("gell-mann1979", "Complex Spinors and Unified Theories", "Gell-Mann, M., Ramond, P., & Slansky, R.", 1979, arxiv="1306.4669"),
            FormulaReference("mohapatra1980_seesaw", "Neutrino Mass and Spontaneous Parity Nonconservation", "Mohapatra, R.N. & Senjanović, G.", 1980, doi="10.1103/PhysRevLett.44.912"),
        ]
    )

    CKM_ELEMENTS'''
    ),

    # F37: CKM_ELEMENTS
    (
        '        notes="Derived from G₂ wavefunction overlaps",\n        related_formulas=["theta23-maximal"]\n    )\n\n    YUKAWA_INSTANTON',
        '''        notes="Derived from G₂ wavefunction overlaps",
        related_formulas=["theta23-maximal"],
        references=[
            FormulaReference("cabibbo1963", "Unitary Symmetry and Leptonic Decays", "Cabibbo, N.", 1963, doi="10.1103/PhysRevLett.10.531"),
            FormulaReference("kobayashi1973_ckm", "CP-Violation in the Renormalizable Theory of Weak Interaction", "Kobayashi, M. & Maskawa, T.", 1973, doi="10.1143/PTP.49.652"),
            FormulaReference("pdg2024_ckm", "Review of Particle Physics (CKM matrix)", "Particle Data Group", 2024, doi="10.1103/PhysRevD.110.030001"),
        ]
    )

    YUKAWA_INSTANTON'''
    ),

    # F38: YUKAWA_INSTANTON
    (
        '        notes="Explains fermion mass hierarchies geometrically",\n        related_formulas=["top-quark-mass"]\n    )\n\n    ATTRACTOR_POTENTIAL',
        '''        notes="Explains fermion mass hierarchies geometrically",
        related_formulas=["top-quark-mass"],
        references=[
            FormulaReference("witten1996", "Strong Coupling Expansion Of Calabi-Yau Compactification", "Witten, E.", 1996, arxiv="hep-th/9602070"),
            FormulaReference("blumenhagen2005", "Toward realistic intersecting D-brane models", "Blumenhagen, R., Cvetic, M., Langacker, P., & Shiu, G.", 2005, arxiv="hep-th/0502005"),
            FormulaReference("donagi2008", "Model Building with F-Theory", "Donagi, R. & Wijnholt, M.", 2008, arxiv="0802.2969"),
        ]
    )

    ATTRACTOR_POTENTIAL'''
    ),
]

# Apply all replacements
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Replaced: {old[:50]}...")
    else:
        print(f"✗ NOT FOUND: {old[:50]}...")

# Write back
with open("H:\\Github\\PrincipiaMetaphysica\\config.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\n✓ Script completed - check config.py")
