/**
 * PM Visualization Manifest v16.2
 * ===============================
 *
 * Maps high-fidelity visualizations to theoretical sections.
 * Provides GetImagePath for local repo references and code display.
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

const PM_VISUALIZATION_MANIFEST = {
    version: "16.2",
    manuscript_id: "PM-v16.2-FINAL",

    /**
     * Get the local image path for a visualization
     * @param {string} vizId - Visualization identifier
     * @returns {string} Local path to the image file
     */
    getImagePath: function(vizId) {
        const viz = this.visualizations[vizId];
        if (!viz) {
            console.warn(`Visualization not found: ${vizId}`);
            return null;
        }
        return `../images/${viz.image}`;
    },

    /**
     * Get the simulation script path that generates a visualization
     * @param {string} vizId - Visualization identifier
     * @returns {string} Path to the simulation script
     */
    getSimulationPath: function(vizId) {
        const viz = this.visualizations[vizId];
        if (!viz || !viz.simulation) {
            console.warn(`No simulation found for: ${vizId}`);
            return null;
        }
        return `../simulations/${viz.simulation}`;
    },

    /**
     * Get all visualizations for a specific section
     * @param {string} sectionId - Section identifier (e.g., "1.4", "2.1")
     * @returns {Array} Array of visualization objects
     */
    getVisualizationsForSection: function(sectionId) {
        return Object.values(this.visualizations).filter(v => v.section === sectionId);
    },

    // Section-to-visualization injections for the paper
    injections: [
        {
            section: "1.4",
            title: "Dimensional Descent",
            anchor_text: "transition from the 26D bosonic string vacuum to the 11D M-theory limit",
            visualization: "dimensional_projection_stack",
            caption: "Figure 1: The recursive folding of the 26D Leech Lattice into the 11D Supergravity limit via G2 compactification."
        },
        {
            section: "2.1",
            title: "The G2 Holonomy",
            anchor_text: "associative 3-form calibration and the co-associative 4-form residue",
            visualization: "g2_manifold_holonomy",
            caption: "Figure 2: Geometric representation of the G2 manifold, highlighting the associative cycles (b3=24) that determine gauge coupling residues."
        },
        {
            section: "4.2",
            title: "Renormalization Group Flow",
            anchor_text: "running of the fine structure constant from the Planck scale to MZ",
            visualization: "rg_flow_convergence",
            caption: "Figure 3: 3-Loop RG evolution of alpha^-1 showing the transition from the bare G2 residue to the CODATA laboratory value."
        },
        {
            section: "5.3",
            title: "Neutrino Mass Hierarchy",
            anchor_text: "sum of neutrino masses constrained by the octonionic volume suppression",
            visualization: "neutrino_mass_landscape",
            caption: "Figure 4: Normal Hierarchy octonionic scaling from v16.2 (IO experimental values, theta_g golden angle constraint)."
        },
        {
            section: "6.1",
            title: "CKM Unitarity Triangles",
            anchor_text: "Jarlskog invariant as a geometric area within the symplectic boundary",
            visualization: "ckm_unitary_triangle",
            caption: "Figure 5: The CKM Unitary Triangle showing the v16.2 CP phase from doubled golden angle (2*theta_g = 63.44 deg)."
        },
        {
            section: "7.4",
            title: "Dark Energy Thawing",
            anchor_text: "thawing equation of state w(z) aligned with DESI 2025 cusp data",
            visualization: "de_cusp_z2_anchor",
            caption: "Figure 6: w0-wa parameter space showing PM-v16.2 thawing prediction (w0=-0.9583, wa=-0.204) at 0.02 sigma from DESI 2025."
        },
        {
            section: "8.2",
            title: "Structure Formation",
            anchor_text: "S8 clustering suppression induced by torsional metric pressure",
            visualization: "matter_power_spectrum_damping",
            caption: "Figure 7: The matter power spectrum comparing Lambda-CDM clustering with the PM-v16.2 torsional damping result (S8=0.766)."
        },
        {
            section: "9.1",
            title: "Cosmic Microwave Background",
            anchor_text: "acoustic peak shifts in the high-ell regime",
            visualization: "cmb_acoustic_peaks",
            caption: "Figure 8: CMB Power Spectrum showing v16.2 alignment with Planck 2018/2025 TT-TE-EE datasets."
        }
    ],

    // Visualization registry with metadata
    visualizations: {
        // === KEEP: Core Geometric Foundation ===
        "g2_manifold_holonomy": {
            id: "g2_manifold_holonomy",
            image: "g2-manifold.png",
            title: "G2 Holonomy Manifold",
            section: "2.1",
            simulation: "v16/geometric/g2_geometry_v16_0.py",
            description: "The 7-dimensional G2 manifold with b3=24 associative 3-cycles",
            status: "KEEP",
            v16_2_notes: "Core foundation - unchanged from v16.1"
        },

        "dimensional_projection_stack": {
            id: "dimensional_projection_stack",
            image: "dimensional-reduction-pathway.svg",
            title: "Dimensional Projection Stack",
            section: "1.4",
            simulation: "derivations/g2_geometry_derivations.py",
            description: "26D to 4D compactification pathway via G2",
            status: "KEEP",
            v16_2_notes: "Shows complete dimensional descent"
        },

        "ckm_unitary_triangle": {
            id: "ckm_unitary_triangle",
            image: "octonionic-triality-ckm-pmns.png",
            title: "CKM Unitarity Triangle",
            section: "6.1",
            simulation: "v16/fermion/ckm_matrix_v16_0.py",
            description: "CKM matrix from octonionic triality with CP phase",
            status: "KEEP",
            v16_2_notes: "Updated CP phase = 2*theta_g (doubled golden angle)"
        },

        // === NEW: v16.2 Dark Energy Thawing ===
        "de_cusp_z2_anchor": {
            id: "de_cusp_z2_anchor",
            image: "ricci-flow-hubble-evolution.png",
            title: "Dark Energy Thawing Cusp",
            section: "7.4",
            simulation: "v16/cosmology/dark_energy_thawing_v16_2.py",
            description: "w0-wa parameter space with Ricci flow z=2.0 anchor",
            status: "NEW",
            v16_2_notes: "Essential for DESI 2025 alignment. w0=-0.9583 from b3=24 thawing correction."
        },

        "ricci_flow_evolution": {
            id: "ricci_flow_evolution",
            image: "ricci-flow-hubble-evolution.png",
            title: "Ricci Flow Cosmological Evolution",
            section: "7.4",
            simulation: "v16/cosmology/dark_energy_thawing_v16_2.py",
            description: "Hubble evolution with Ricci flow correction at z=2.0",
            status: "NEW",
            v16_2_notes: "Shows H(z) transition at Ricci flow anchor"
        },

        // === KEEP: Validated Visualizations ===
        "cmb_acoustic_peaks": {
            id: "cmb_acoustic_peaks",
            image: "cmb-power-spectrum.png",
            title: "CMB Power Spectrum",
            section: "9.1",
            simulation: "v16/cosmology/cosmology_intro_v16_0.py",
            description: "CMB TT power spectrum with Planck comparison",
            status: "KEEP",
            v16_2_notes: "Aligned with Planck 2018/2025 data"
        },

        "rg_flow_convergence": {
            id: "rg_flow_convergence",
            image: "gauge-fixing-time.png",
            title: "RG Flow Convergence",
            section: "4.2",
            simulation: "renormalization_group_runner_fixed.py",
            description: "3-loop RG running of gauge couplings",
            status: "KEEP",
            v16_2_notes: "Uses Radau method for numerical stability"
        },

        "neutrino_mass_landscape": {
            id: "neutrino_mass_landscape",
            image: "parameter-space.png",
            title: "Neutrino Mass Landscape",
            section: "5.3",
            simulation: "v16/neutrino/neutrino_mixing_v16_0.py",
            description: "Normal hierarchy mass landscape with octonionic scaling",
            status: "KEEP",
            v16_2_notes: "Updated to Normal Hierarchy (IO experimental values)"
        },

        "matter_power_spectrum_damping": {
            id: "matter_power_spectrum_damping",
            image: "cosmology-evolution-diagram.png",
            title: "Matter Power Spectrum Damping",
            section: "8.2",
            simulation: "v16/cosmology/s8_suppression_v16_1.py",
            description: "S8 suppression from torsional damping",
            status: "KEEP",
            v16_2_notes: "S8=0.766 within 0.6 sigma of KiDS-1000"
        },

        // === DELETE: Obsolete v16.1 Visualizations ===
        "static_gut_unification_v16_1": {
            id: "static_gut_unification_v16_1",
            image: null,
            title: "Static GUT Unification (OBSOLETE)",
            section: null,
            simulation: null,
            description: "Tree-level gauge meeting point - invalid in 3-loop framework",
            status: "DELETE",
            v16_2_notes: "Replaced by RG Flow Convergence with logarithmic running"
        },

        "inverted_hierarchy_density_v16_1": {
            id: "inverted_hierarchy_density_v16_1",
            image: null,
            title: "Inverted Hierarchy Density (OBSOLETE)",
            section: null,
            simulation: null,
            description: "Inverted hierarchy probability map - invalid after IO switch",
            status: "DELETE",
            v16_2_notes: "Replaced by Normal Hierarchy octonionic scaling"
        }
    },

    // Appendix visualization references
    appendices: {
        "appendix_g": {
            title: "Non-Linear Ricci Flow and Redshift Anchors",
            visualization: "de_cusp_z2_anchor",
            figure_ref: "Figure 6"
        },
        "appendix_h": {
            title: "Symplectic Parity and CP-Phase Rotation",
            visualization: "ckm_unitary_triangle",
            figure_ref: "Figure 5"
        }
    }
};

// Helper function to inject visualization into a DOM element
function injectVisualization(vizId, containerId) {
    const viz = PM_VISUALIZATION_MANIFEST.visualizations[vizId];
    if (!viz || viz.status === "DELETE") {
        console.warn(`Cannot inject visualization: ${vizId}`);
        return false;
    }

    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`Container not found: ${containerId}`);
        return false;
    }

    const imgPath = PM_VISUALIZATION_MANIFEST.getImagePath(vizId);
    const simPath = PM_VISUALIZATION_MANIFEST.getSimulationPath(vizId);

    container.innerHTML = `
        <figure class="pm-visualization">
            <img src="${imgPath}" alt="${viz.title}" loading="lazy">
            <figcaption>
                <strong>${viz.title}</strong>
                <span class="viz-section">Section ${viz.section}</span>
                ${simPath ? `<a href="${simPath}" class="viz-code-link" title="View simulation code">View Code</a>` : ''}
            </figcaption>
        </figure>
    `;

    return true;
}

// Export for use
if (typeof window !== 'undefined') {
    window.PM_VISUALIZATION_MANIFEST = PM_VISUALIZATION_MANIFEST;
    window.injectVisualization = injectVisualization;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PM_VISUALIZATION_MANIFEST, injectVisualization };
}
