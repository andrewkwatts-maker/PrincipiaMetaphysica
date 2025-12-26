#!/usr/bin/env python3
"""
Add learning resources to remaining formulas in config.py.
Based on LEARNING_RESOURCES_FORMULAS_1-27.md and LEARNING_RESOURCES_REPORT.md.

This script adds 2-3 learning resources per formula that currently lacks them.
"""

import re
from typing import Dict, List


def get_learning_resources(formula_id: str) -> List[Dict]:
    """Return learning resources for a given formula ID."""

    resources_map = {
        "racetrack-superpotential": [
            {"title": "KKLT After 20 Years - Quevedo & Valenzuela", "url": "https://arxiv.org/abs/2212.06886", "type": "article", "level": "advanced", "description": "Modern perspective on moduli stabilization and racetrack superpotentials"},
            {"title": "Racetrack Superpotentials - Burgess et al.", "url": "https://arxiv.org/abs/hep-th/0209204", "type": "article", "level": "advanced", "description": "Detailed analysis with examples"},
            {"title": "Introduction to Supergravity - Perimeter", "url": "https://www.perimeterinstitute.ca/video-library", "type": "video", "duration": "3 hours", "level": "intermediate", "description": "SUSY breaking and moduli stabilization"}
        ],
        "pneuma-vev": [
            {"title": "Moduli Stabilization in String Theory", "url": "https://arxiv.org/abs/hep-th/0502058", "type": "article", "level": "advanced", "description": "Review of VEVs and stabilization techniques"},
            {"title": "String Theory and M-Theory - Becker et al.", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Chapters 3-4 on compactification and moduli"}
        ],
        "reduction-cascade": [
            {"title": "Kaluza-Klein Theory - PBS Space Time", "url": "https://www.youtube.com/c/pbsspacetime", "type": "video", "duration": "15 min", "level": "beginner", "description": "Introduction to compactification"},
            {"title": "TASI Lectures on Extra Dimensions - Csaki", "url": "https://arxiv.org/abs/hep-ph/0404096", "type": "article", "level": "intermediate", "description": "KK reduction with examples"},
            {"title": "Gravity and Strings - Ortín", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Chapters 8-9 on KK reduction"}
        ],
        "primordial-spinor-13d": [
            {"title": "Clifford Algebras and Spinors - Lounesto", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Chapters 4-6 on spin groups and spinors"},
            {"title": "Spinors and Space-Time - Penrose & Rindler", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Classic reference for spinors"},
            {"title": "Clifford Algebras - Perimeter Institute", "url": "https://www.perimeterinstitute.ca/video-library", "type": "video", "duration": "2 hours", "level": "intermediate", "description": "Geometric algebra and spinors"}
        ],
        "tcs-topology": [
            {"title": "Introduction to G₂ Geometry - Karigiannis", "url": "https://arxiv.org/abs/0807.3858", "type": "article", "level": "intermediate", "description": "Comprehensive G₂ manifolds intro"},
            {"title": "Twisted Connected Sums - Corti et al.", "url": "https://arxiv.org/abs/1510.07068", "type": "article", "level": "advanced", "description": "TCS construction with b₂=4, b₃=24"},
            {"title": "Riemannian Holonomy Groups - Joyce", "url": "https://global.oup.com/academic/product/", "type": "textbook", "level": "graduate", "description": "Definitive G₂ reference, chapters 10-13"}
        ],
        "bekenstein-hawking": [
            {"title": "Bekenstein-Hawking Formula - Wikipedia", "url": "https://en.wikipedia.org/wiki/Bekenstein%E2%80%93Hawking_formula", "type": "article", "level": "beginner", "description": "Overview of black hole entropy"},
            {"title": "Quantum Fields in Curved Space - Birrell & Davies", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Chapters 3-4 on Hawking radiation"},
            {"title": "Black Hole Entropy - Susskind", "url": "https://theoreticalminimum.com/courses", "type": "video", "duration": "90 min", "level": "intermediate", "description": "Statistical mechanics of black holes"}
        ],
        "neutrino-mass-21": [
            {"title": "NuFIT 6.0 - Neutrino Fits", "url": "http://www.nu-fit.org/", "type": "interactive", "level": "intermediate", "description": "Best-fit values for mass splittings"},
            {"title": "Fundamentals of Neutrino Physics - Giunti & Kim", "url": "https://global.oup.com/academic/product/", "type": "textbook", "level": "graduate", "description": "Chapters 3-5 on masses and mixing"},
            {"title": "Neutrino Physics - Fermilab", "url": "https://www.youtube.com/user/fermilab", "type": "video", "duration": "15 min", "level": "beginner", "description": "Intro to neutrino masses"}
        ],
        "neutrino-mass-31": [
            {"title": "NuFIT 6.0 Global Fits", "url": "http://www.nu-fit.org/", "type": "interactive", "level": "intermediate", "description": "Δm²₃₁ = 2.515×10⁻³ eV² constraints"},
            {"title": "Neutrino Mass Models - de Gouvêa", "url": "https://arxiv.org/abs/1411.0308", "type": "article", "level": "advanced", "description": "Comprehensive mass generation review"},
            {"title": "CERN Neutrino Platform", "url": "https://indico.cern.ch/category/5864/", "type": "video", "duration": "90 min", "level": "intermediate", "description": "Mass hierarchy lectures"}
        ],
        "dark-energy-wa": [
            {"title": "Equation of State (Cosmology) - Wikipedia", "url": "https://en.wikipedia.org/wiki/Equation_of_state_(cosmology)", "type": "article", "level": "beginner", "description": "w = P/ρ parameter evolution"},
            {"title": "DESI 2024 Results", "url": "https://data.desi.lbl.gov/", "type": "interactive", "level": "intermediate", "description": "Latest w₀ and w_a measurements"},
            {"title": "Dark Energy - Copeland et al.", "url": "https://arxiv.org/abs/hep-th/0603057", "type": "article", "level": "advanced", "description": "Comprehensive dark energy review"}
        ],
        "thermal-time": [
            {"title": "Thermal Time Hypothesis - Connes & Rovelli", "url": "https://arxiv.org/abs/gr-qc/9406019", "type": "article", "level": "advanced", "description": "Original thermal time paper"},
            {"title": "Operator Algebras - Bratteli & Robinson", "url": "https://www.springer.com/gp/book/", "type": "textbook", "level": "advanced", "description": "Vol 2, Ch 5: Tomita-Takesaki theory"},
            {"title": "Rovelli Thermal Time Lecture", "url": "https://www.youtube.com/results?search_query=rovelli+thermal+time", "type": "video", "duration": "60 min", "level": "intermediate", "description": "Modular flow and thermodynamics"}
        ],
        "gw-dispersion": [
            {"title": "Gravitational Waves Vol 1 - Maggiore", "url": "https://global.oup.com/academic/product/", "type": "textbook", "level": "graduate", "description": "Chapters 1-3 on GW fundamentals and dispersion"},
            {"title": "Testing GR with GWs - Yunes & Siemens", "url": "https://arxiv.org/abs/1304.3473", "type": "article", "level": "advanced", "description": "Modified dispersion relations"},
            {"title": "LIGO Educational Resources", "url": "https://www.ligo.org/science/outreach.php", "type": "interactive", "level": "beginner", "description": "GW detection and analysis"}
        ],
        "gw-dispersion-coeff": [
            {"title": "GW Dispersion in Extra Dimensions", "url": "https://arxiv.org/abs/1008.1783", "type": "article", "level": "advanced", "description": "Relevant to PM predictions"},
            {"title": "TASI Lectures on GWs - Holz", "url": "https://arxiv.org/abs/1809.06348", "type": "article", "level": "intermediate", "description": "Theory and detection"}
        ],
        "gw-dispersion-alt": [
            {"title": "Modified GW Propagation", "url": "https://arxiv.org/abs/gr-qc/", "type": "article", "level": "advanced", "description": "Alternative dispersion formulations"},
            {"title": "LISA Mission", "url": "https://www.lisamission.org/", "type": "interactive", "level": "intermediate", "description": "Future GW observatory"}
        ],
        "higgs-vev": [
            {"title": "Higgs Boson Explained - CERN", "url": "https://home.cern/resources/video", "type": "video", "duration": "20 min", "level": "beginner", "description": "Higgs mechanism and mass generation"},
            {"title": "Standard Model in a Nutshell - Goldberg", "url": "https://press.princeton.edu/books/", "type": "textbook", "level": "intermediate", "description": "Chapter 7 on Higgs mechanism"},
            {"title": "QFT and the Standard Model - Schwartz", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Chapters 28-29 on Higgs VEV"}
        ],
        "higgs-mass": [
            {"title": "Higgs Boson - Wikipedia", "url": "https://en.wikipedia.org/wiki/Higgs_boson", "type": "article", "level": "beginner", "description": "125.1 GeV mass measurement"},
            {"title": "MIT 8.701 Standard Model", "url": "https://ocw.mit.edu/", "type": "video", "duration": "Full semester", "level": "graduate", "description": "Lectures 10-12 on SSB and Higgs"}
        ],
        "higgs-potential": [
            {"title": "Spontaneous Symmetry Breaking - Scholarpedia", "url": "http://www.scholarpedia.org/article/Spontaneous_symmetry_breaking", "type": "article", "level": "intermediate", "description": "Mexican hat potential and SSB"},
            {"title": "Falstad Higgs Potential", "url": "https://www.falstad.com/", "type": "interactive", "level": "beginner", "description": "3D visualization"}
        ],
        "higgs-quartic": [
            {"title": "Higgs Mechanism - Wikipedia", "url": "https://en.wikipedia.org/wiki/Higgs_mechanism", "type": "article", "level": "intermediate", "description": "Quartic coupling overview"},
            {"title": "Electroweak SSB - TASI Lectures", "url": "https://physicslearning.colorado.edu/tasi/", "type": "article", "level": "advanced", "description": "Higgs potential and coupling running"}
        ],
        "top-quark-mass": [
            {"title": "Particle Data Group - Top Quark", "url": "https://pdg.lbl.gov/", "type": "interactive", "level": "intermediate", "description": "172.69 ± 0.30 GeV"},
            {"title": "Understanding Fermion Masses - Antusch & King", "url": "https://arxiv.org/abs/hep-ph/0402121", "type": "article", "level": "advanced", "description": "Yukawa couplings and hierarchies"}
        ],
        "bottom-quark-mass": [
            {"title": "PDG 2024 - Bottom Quark", "url": "https://pdg.lbl.gov/", "type": "interactive", "level": "intermediate", "description": "m_b(m_b) = 4.18 ± 0.03 GeV"},
            {"title": "Yukawa Textures from String Theory", "url": "https://arxiv.org/abs/1105.3424", "type": "article", "level": "advanced", "description": "Geometric origin of masses"}
        ],
        "tau-lepton-mass": [
            {"title": "PDG - Tau Lepton", "url": "https://pdg.lbl.gov/", "type": "interactive", "level": "intermediate", "description": "m_τ = 1.77686 ± 0.00012 GeV"},
            {"title": "Lepton Masses and Mixing", "url": "https://arxiv.org/abs/hep-ph/", "type": "article", "level": "intermediate", "description": "Charged lepton spectrum"}
        ],
        "proton-branching": [
            {"title": "Proton Decay - Wikipedia", "url": "https://en.wikipedia.org/wiki/Proton_decay", "type": "article", "level": "beginner", "description": "Decay channels and branching ratios"},
            {"title": "Super-Kamiokande Results", "url": "http://www-sk.icrr.u-tokyo.ac.jp/sk/", "type": "interactive", "level": "intermediate", "description": "Latest bounds on p→e⁺π⁰"},
            {"title": "Standard Model and Beyond - Langacker", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Chapters 12-13 on proton decay"}
        ],
        "so10-breaking": [
            {"title": "SO(10) GUT - Wikipedia", "url": "https://en.wikipedia.org/wiki/SO(10)", "type": "article", "level": "beginner", "description": "SO(10) breaking patterns"},
            {"title": "SO(10) Grand Unification - Babu & Mohapatra", "url": "https://arxiv.org/abs/1411.5762", "type": "article", "level": "advanced", "description": "Comprehensive SO(10) review"},
            {"title": "Modern Particle Physics - Thomson", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "intermediate", "description": "Chapter 17 on GUTs"}
        ],
        "gut-coupling": [
            {"title": "Grand Unification - Langacker", "url": "https://arxiv.org/abs/0901.0241", "type": "article", "level": "advanced", "description": "GUT coupling unification"},
            {"title": "Renormalization Group - Scholarpedia", "url": "http://www.scholarpedia.org/article/Renormalization_group", "type": "article", "level": "intermediate", "description": "RG flow and coupling evolution"}
        ],
        "weak-mixing-angle": [
            {"title": "Weinberg Angle - Wikipedia", "url": "https://en.wikipedia.org/wiki/Weinberg_angle", "type": "article", "level": "beginner", "description": "Weak mixing angle overview"},
            {"title": "PDG - Electroweak Parameters", "url": "https://pdg.lbl.gov/", "type": "interactive", "level": "intermediate", "description": "sin²θ_W(M_Z) = 0.23122 ± 0.00004"},
            {"title": "Gauge Theories - Aitchison & Hey", "url": "https://www.routledge.com/", "type": "textbook", "level": "graduate", "description": "Electroweak unification"}
        ],
        "strong-coupling": [
            {"title": "QCD Coupling - PDG", "url": "https://pdg.lbl.gov/", "type": "interactive", "level": "intermediate", "description": "α_s(M_Z) = 0.1180 ± 0.0010"},
            {"title": "Introduction to QFT - Peskin & Schroeder", "url": "https://www.routledge.com/", "type": "textbook", "level": "graduate", "description": "Chapters 15-16 on QCD"}
        ],
        "effective-dimension": [
            {"title": "Thermal Time and Dimensions", "url": "https://arxiv.org/abs/gr-qc/9406019", "type": "article", "level": "advanced", "description": "Effective dimensionality"},
            {"title": "Maximum Entropy Principle", "url": "https://en.wikipedia.org/wiki/Principle_of_maximum_entropy", "type": "article", "level": "intermediate", "description": "MEP and dark energy"}
        ],
        "effective-euler": [
            {"title": "G₂ and M-Theory - Acharya", "url": "https://arxiv.org/abs/hep-th/0409048", "type": "article", "level": "advanced", "description": "χ_eff to physics"},
            {"title": "Betti Numbers - Wikipedia", "url": "https://en.wikipedia.org/wiki/Betti_number", "type": "article", "level": "beginner", "description": "Topological invariants"}
        ],
        "effective-torsion": [
            {"title": "G₂ Torsion - Karigiannis", "url": "https://arxiv.org/abs/0807.3858", "type": "article", "level": "advanced", "description": "Intrinsic torsion"},
            {"title": "Torsion Tensor - Wikipedia", "url": "https://en.wikipedia.org/wiki/Torsion_tensor", "type": "article", "level": "intermediate", "description": "Torsion overview"}
        ],
        "flux-quantization": [
            {"title": "Flux Compactifications", "url": "https://arxiv.org/abs/hep-th/0603057", "type": "article", "level": "advanced", "description": "Flux quantization review"},
            {"title": "TASI String Compactifications - Ibanez & Uranga", "url": "https://arxiv.org/abs/hep-th/0609213", "type": "article", "level": "graduate", "description": "Flux in CY and G₂"}
        ],
        "friedmann-constraint": [
            {"title": "Friedmann Equations - Wikipedia", "url": "https://en.wikipedia.org/wiki/Friedmann_equations", "type": "article", "level": "beginner", "description": "Cosmological dynamics"},
            {"title": "Modern Cosmology - Dodelson", "url": "https://www.elsevier.com/", "type": "textbook", "level": "graduate", "description": "Chapters 1-3 on Friedmann"},
            {"title": "Introduction to Cosmology - Ryden", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "undergraduate", "description": "Accessible intro"}
        ],
        "cp-phase-geometric": [
            {"title": "CP Violation in Neutrinos", "url": "https://en.wikipedia.org/wiki/CP_violation", "type": "article", "level": "beginner", "description": "PMNS CP violation"},
            {"title": "NuFIT 6.0 CP Phase", "url": "http://www.nu-fit.org/", "type": "interactive", "level": "intermediate", "description": "δ_CP = 232° ± 30°"}
        ],
        "dirac-pneuma": [
            {"title": "Dirac in Curved Spacetime", "url": "https://en.wikipedia.org/wiki/Dirac_equation_in_curved_spacetime", "type": "article", "level": "intermediate", "description": "Dirac on curved backgrounds"},
            {"title": "Spinors in Physics - Hladik", "url": "https://www.springer.com/", "type": "textbook", "level": "graduate", "description": "Spinors in higher dimensions"}
        ],
        "pneuma-stress-energy": [
            {"title": "Stress-Energy Tensor", "url": "https://en.wikipedia.org/wiki/Stress%E2%80%93energy_tensor", "type": "article", "level": "beginner", "description": "Energy-momentum in GR"},
            {"title": "QFT in Curved Space - Birrell & Davies", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Stress-energy for quantum fields"}
        ],
        "ghost-coefficient": [
            {"title": "Conformal Field Theory - Di Francesco et al.", "url": "https://www.springer.com/", "type": "textbook", "level": "graduate", "description": "Chapters 5-7 on Virasoro and ghosts"},
            {"title": "Intro to CFT - Qualls", "url": "https://arxiv.org/abs/1511.04074", "type": "article", "level": "intermediate", "description": "Central charge and ghost systems"}
        ],
        "kappa-gut-coefficient": [
            {"title": "Gauge Kinetic Functions", "url": "https://arxiv.org/abs/hep-th/", "type": "article", "level": "advanced", "description": "Coupling normalization"},
            {"title": "String Theory Vol 1 - Polchinski", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "Effective field theories"}
        ],
        "effective-torsion-spinor": [
            {"title": "Spin(7) and G₂", "url": "https://arxiv.org/abs/math/", "type": "article", "level": "advanced", "description": "Holonomy relationships"},
            {"title": "Special Holonomy - Acharya", "url": "https://www.youtube.com/", "type": "video", "duration": "60 min", "level": "graduate", "description": "G₂ and spinor stabilization"}
        ],
        "pati-salam-chain": [
            {"title": "Pati-Salam Model - Wikipedia", "url": "https://en.wikipedia.org/wiki/Pati%E2%80%93Salam_model", "type": "article", "level": "beginner", "description": "SU(4)×SU(2)_L×SU(2)_R"},
            {"title": "GUT Theories - Mohapatra & Pal", "url": "https://arxiv.org/abs/hep-ph/0506032", "type": "article", "level": "advanced", "description": "Pati-Salam intermediate scale"}
        ],
        "rg-running-couplings": [
            {"title": "Renormalization Group", "url": "http://www.scholarpedia.org/article/Renormalization_group", "type": "article", "level": "intermediate", "description": "RG flow and beta functions"},
            {"title": "TASI RG Lectures", "url": "https://arxiv.org/abs/hep-ph/", "type": "article", "level": "graduate", "description": "Coupling evolution"}
        ],
        "mirror-dm-ratio": [
            {"title": "Mirror Matter - Wikipedia", "url": "https://en.wikipedia.org/wiki/Mirror_matter", "type": "article", "level": "beginner", "description": "Mirror symmetry and DM"},
            {"title": "Hidden Sector DM", "url": "https://arxiv.org/abs/hep-ph/", "type": "article", "level": "intermediate", "description": "Mirror/shadow dark matter"}
        ],
        "mirror-temp-ratio": [
            {"title": "Thermal History of Hidden Sectors", "url": "https://arxiv.org/abs/astro-ph/", "type": "article", "level": "intermediate", "description": "Temperature evolution"},
            {"title": "Early Universe - Kolb & Turner", "url": "https://www.routledge.com/", "type": "textbook", "level": "graduate", "description": "Chapters 3-4 on thermodynamics"}
        ],
        "vacuum-minimization": [
            {"title": "Scalar Potential Minimization", "url": "https://en.wikipedia.org/wiki/Potential_energy", "type": "article", "level": "beginner", "description": "Finding vacuum states"},
            {"title": "SUSY and String Theory - Dine", "url": "https://www.cambridge.org/core/books/", "type": "textbook", "level": "graduate", "description": "F-term and D-term potentials"}
        ],
    }

    return resources_map.get(formula_id, [])


def format_learning_resource(resource: Dict) -> str:
    """Format a learning resource dict as Python code."""
    lines = ['            LearningResource(\n']
    lines.append(f'                title="{resource["title"]}",\n')
    lines.append(f'                url="{resource["url"]}",\n')
    lines.append(f'                type="{resource["type"]}",\n')
    if "duration" in resource:
        lines.append(f'                duration="{resource["duration"]}",\n')
    lines.append(f'                level="{resource["level"]}",\n')
    lines.append(f'                description="{resource["description"]}"\n')
    lines.append('            )')
    return ''.join(lines)


def main():
    """Main function to add learning resources to config.py."""

    config_path = r"h:\Github\PrincipiaMetaphysica\config.py"

    print("Reading config.py...")
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match formula definitions
    # Looking for: FORMULA_NAME = Formula(\n    id="formula-id",...\n    )\n
    pattern = r'(    (\w+) = Formula\(\s+id="([^"]+)".*?)(    \))'

    added_count = 0
    skipped_count = 0

    def add_resources(match):
        nonlocal added_count, skipped_count

        full_match = match.group(0)
        formula_var = match.group(2)
        formula_id = match.group(3)

        # Check if already has learning_resources
        if 'learning_resources=' in full_match:
            skipped_count += 1
            return full_match

        # Get resources for this formula
        resources = get_learning_resources(formula_id)

        if not resources:
            skipped_count += 1
            return full_match

        # Build the learning_resources section
        lr_lines = [',\n        learning_resources=[\n']
        for i, resource in enumerate(resources):
            lr_lines.append(format_learning_resource(resource))
            if i < len(resources) - 1:
                lr_lines.append(',\n')
        lr_lines.append('\n        ]\n')

        # Insert before closing )
        parts = full_match.rsplit('    )', 1)
        new_formula = parts[0] + ''.join(lr_lines) + '    )'

        added_count += 1
        print(f'✓ Added learning resources to {formula_id}')

        return new_formula

    # Apply the transformation
    new_content = re.sub(pattern, add_resources, content, flags=re.DOTALL)

    # Write back
    print(f"\nWriting updated config.py...")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'\n' + '='*60)
    print(f'✓ Successfully added learning resources to {added_count} formulas')
    print(f'✓ Skipped {skipped_count} formulas (already have resources or none defined)')
    print('='*60)


if __name__ == "__main__":
    main()
