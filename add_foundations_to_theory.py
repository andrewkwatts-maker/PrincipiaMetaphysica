#!/usr/bin/env python3
"""
Add foundations section to theory_output.json

This script adds a structured foundations section based on the existing foundation pages.
"""

import json
import os

def create_foundations_data():
    """Create the foundations data structure as a list"""
    return [
        {
            "id": "boltzmann-entropy",
            "name": "Boltzmann Entropy",
            "description": "The fundamental bridge between microscopic statistical mechanics and macroscopic thermodynamics, connecting the number of microstates to entropy.",
            "equation": "S = k<sub>B</sub> ln &Omega;",
            "status": "established",
            "year": "1877",
            "attribution": "Formulated by Ludwig Boltzmann in 1877 | Engraved on his tombstone",
            "gradient": "linear-gradient(135deg, rgba(255, 126, 182, 0.15), rgba(255, 179, 71, 0.1))",
            "borderColor": "rgba(255, 126, 182, 0.3)",
            "properties": {
                "meaning": "Entropy is the logarithm of the number of ways a system can be arranged.",
                "components": [
                    {
                        "symbol": "S",
                        "name": "Entropy",
                        "description": "The <strong>macroscopic measure</strong> of disorder or information content. Higher entropy means more disorder and more ways the system can be arranged."
                    },
                    {
                        "symbol": "&Omega;",
                        "name": "Microstates",
                        "description": "The <strong>number of microscopic configurations</strong> that produce the same macroscopic state. More microstates = higher entropy."
                    },
                    {
                        "symbol": "k<sub>B</sub>",
                        "name": "Boltzmann Constant",
                        "description": "The <strong>fundamental bridge</strong> between energy and temperature: k<sub>B</sub> = 1.38 &times; 10<sup>-23</sup> J/K. Connects microscopic and macroscopic scales."
                    }
                ]
            },
            "pmConnection": {
                "description": "Boltzmann entropy plays a crucial role in Principia Metaphysica's dimensional framework:",
                "applications": [
                    {
                        "title": "Thermal Time Hypothesis",
                        "description": "In PM, the flow of time is related to entropy increase:",
                        "equation": "t &prop; S = k<sub>B</sub> ln &Omega;",
                        "note": "Time emerges from statistical correlations",
                        "details": "This connects to Carlo Rovelli's thermal time hypothesis: time is the direction of increasing entropy in the statistical state."
                    },
                    {
                        "title": "Entropy in Higher Dimensions",
                        "description": "Boltzmann's formula generalizes to the 26D bulk and 13D shadow spaces:",
                        "list": [
                            "<strong>26D bulk entropy:</strong> S<sub>26</sub> = k<sub>B</sub> ln &Omega;<sub>26</sub>, counting microstates in (24,2) signature spacetime",
                            "<strong>13D shadow entropy:</strong> S<sub>13</sub> = k<sub>B</sub> ln &Omega;<sub>13</sub>, after Sp(2,R) gauge fixing",
                            "<strong>Dimensional reduction:</strong> Entropy is preserved through compactification: S<sub>26</sub> = S<sub>13</sub> + S<sub>compact</sub>",
                            "<strong>Holographic entropy:</strong> Connection to black hole entropy S<sub>BH</sub> = A/(4&ell;<sub>P</sub><sup>2</sup>)"
                        ]
                    },
                    {
                        "title": "Black Hole Entropy",
                        "description": "The Bekenstein-Hawking entropy formula connects Boltzmann's formula to gravity:",
                        "equation": "S<sub>BH</sub> = k<sub>B</sub>A/(4&ell;<sub>P</sub><sup>2</sup>) = k<sub>B</sub> ln &Omega;<sub>horizon</sub>",
                        "note": "Black hole area measures the number of horizon microstates",
                        "details": "This suggests entropy is fundamentally geometric in higher-dimensional theories. PM explores how black hole microstates may arise from compactified dimensions in the 26D &rarr; 4D reduction."
                    }
                ]
            },
            "formulas": [
                {
                    "equation": "S = k<sub>B</sub> ln &Omega;",
                    "status": "established",
                    "components": [
                        {
                            "symbol": "S",
                            "name": "Entropy",
                            "description": "Thermodynamic state function measuring disorder, information content, and irreversibility.<br>Units: Joules per Kelvin (J/K) or J K<sup>-1</sup><br>Always increases in isolated systems (Second Law of Thermodynamics).",
                            "link": "https://en.wikipedia.org/wiki/Entropy",
                            "linkText": "Wikipedia: Entropy"
                        },
                        {
                            "symbol": "k<sub>B</sub>",
                            "name": "Boltzmann Constant",
                            "description": "k<sub>B</sub> = 1.380649 &times; 10<sup>-23</sup> J/K (exact as of 2019 SI redefinition)<br>Relates temperature to energy: &lang;E&rang; = k<sub>B</sub>T<br>Also appears in ideal gas law: PV = Nk<sub>B</sub>T",
                            "badge": "Fundamental Constant"
                        },
                        {
                            "symbol": "&Omega;",
                            "name": "Number of Microstates",
                            "description": "The number of distinct microscopic configurations consistent with a macroscopic state.<br>Dimensionless integer, typically enormous (&Omega; ~ 10<sup>10<sup>23</sup></sup>)<br>Depends on system's energy, volume, and particle number.",
                            "link": "https://en.wikipedia.org/wiki/Microstate_(statistical_mechanics)",
                            "linkText": "Wikipedia: Microstate"
                        }
                    ],
                    "derivationChain": [
                        {
                            "text": "Combinatorics & Probability Theory",
                            "badge": "Mathematics",
                            "type": "established"
                        },
                        {
                            "text": "Statistical Mechanics (Boltzmann, 1877)",
                            "badge": "Physics",
                            "type": "established"
                        },
                        {
                            "text": "Ergodic Hypothesis (time average = ensemble average)",
                            "badge": "Statistical Principle",
                            "type": "established"
                        },
                        {
                            "text": "Shannon Information Theory (1948)",
                            "badge": "Information Theory",
                            "type": "established"
                        }
                    ]
                }
            ],
            "usedInSections": [
                {
                    "title": "Thermal Time",
                    "description": "Entropy and time emergence",
                    "link": "thermal-time.html"
                },
                {
                    "title": "Cosmology",
                    "description": "Thermodynamic arrow of time",
                    "link": "cosmology.html"
                }
            ]
        },
        {
            "id": "einstein-field-equations",
            "name": "Einstein Field Equations",
            "description": "The fundamental equations of general relativity, describing how matter and energy curve spacetime.",
            "equation": "G<sub>&mu;&nu;</sub> + &Lambda;g<sub>&mu;&nu;</sub> = (8&pi;G/c<sup>4</sup>)T<sub>&mu;&nu;</sub>",
            "status": "established",
            "year": "1915",
            "attribution": "Formulated by Albert Einstein in 1915",
            "gradient": "linear-gradient(135deg, rgba(79, 172, 254, 0.15), rgba(139, 127, 255, 0.1))",
            "borderColor": "rgba(79, 172, 254, 0.3)",
            "properties": {
                "meaning": "Spacetime curvature is proportional to the stress-energy of matter and fields.",
                "components": [
                    {
                        "symbol": "G<sub>&mu;&nu;</sub>",
                        "name": "Einstein Tensor",
                        "description": "Describes the <strong>curvature of spacetime</strong>. Combines Ricci curvature and scalar curvature."
                    },
                    {
                        "symbol": "T<sub>&mu;&nu;</sub>",
                        "name": "Stress-Energy Tensor",
                        "description": "Describes the <strong>distribution of matter and energy</strong>. Source of gravitational field."
                    },
                    {
                        "symbol": "&Lambda;",
                        "name": "Cosmological Constant",
                        "description": "Represents <strong>dark energy</strong> or vacuum energy density. Drives accelerated expansion of universe."
                    }
                ]
            },
            "pmConnection": {
                "description": "Einstein's equations are the foundation for PM's geometric approach to physics:",
                "applications": [
                    {
                        "title": "Higher-Dimensional Gravity",
                        "description": "PM extends Einstein's equations to 26 dimensions:",
                        "equation": "G<sub>MN</sub><sup>(26)</sup> = (8&pi;G/c<sup>4</sup>)T<sub>MN</sub><sup>(26)</sup>",
                        "note": "Capital indices M,N run over all 26 dimensions",
                        "details": "After dimensional reduction and gauge fixing, the 4D effective theory recovers standard Einstein gravity plus corrections from extra dimensions."
                    },
                    {
                        "title": "Pneuma Stress-Energy",
                        "description": "The Pneuma field contributes to the stress-energy tensor:",
                        "list": [
                            "Pneuma spinor energy density creates effective dark matter",
                            "Pneuma condensate pressure contributes to cosmological constant",
                            "Geometric curvature from compactified dimensions modifies 4D gravity"
                        ]
                    }
                ]
            },
            "usedInSections": [
                {
                    "title": "Cosmology",
                    "description": "4D effective Einstein equations",
                    "link": "cosmology.html"
                },
                {
                    "title": "Dimensional Reduction",
                    "description": "26D to 4D reduction",
                    "link": "dimensional-reduction.html"
                }
            ]
        }
    ]

def add_foundations_to_theory_output():
    """Add foundations section to theory_output.json"""
    theory_path = r'h:\Github\PrincipiaMetaphysica\theory_output.json'

    # Load existing theory_output.json
    print(f"Loading {theory_path}...")
    with open(theory_path, 'r', encoding='utf-8') as f:
        theory_data = json.load(f)

    # Get existing foundations or create new list
    existing_foundations = theory_data.get('foundations', [])
    new_foundations = create_foundations_data()

    # Merge - keep existing and add new ones (avoid duplicates by ID)
    existing_ids = {f.get('id') for f in existing_foundations}
    for new_f in new_foundations:
        if new_f['id'] not in existing_ids:
            existing_foundations.append(new_f)
            print(f"  Added: {new_f['id']}")
        else:
            # Update existing entry
            for i, existing_f in enumerate(existing_foundations):
                if existing_f.get('id') == new_f['id']:
                    existing_foundations[i] = new_f
                    print(f"  Updated: {new_f['id']}")
                    break

    theory_data['foundations'] = existing_foundations

    # Save updated theory_output.json
    print(f"\nSaving updated {theory_path}...")
    with open(theory_path, 'w', encoding='utf-8') as f:
        json.dump(theory_data, f, indent=2, ensure_ascii=False)

    print("Successfully updated foundations section in theory_output.json!")
    print(f"Total foundation entries: {len(theory_data['foundations'])}")
    for foundation in theory_data['foundations']:
        print(f"  - {foundation.get('id', 'unknown')}: {foundation.get('name', 'no name')}")

if __name__ == '__main__':
    add_foundations_to_theory_output()
