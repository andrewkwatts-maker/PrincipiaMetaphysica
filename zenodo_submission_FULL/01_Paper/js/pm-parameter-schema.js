/**
 * Principia Metaphysica - Standardized Parameter Schema
 * ======================================================
 *
 * Defines the standard schema for all simulation outputs and parameters.
 * Each parameter includes metadata for rendering, validation, and documentation.
 *
 * Usage:
 *   const param = PM_PARAMS.get('higgs_mass');
 *   console.log(param.value, param.display, param.agreement_sigma);
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

const PM_PARAMETER_SCHEMA = {
    // Schema version
    version: '1.0.0',

    // Parameter categories
    categories: {
        FUNDAMENTAL: 'fundamental',
        DERIVED: 'derived',
        PREDICTED: 'predicted',
        CALIBRATED: 'calibrated',
        EXPERIMENTAL: 'experimental'
    },

    // Status indicators
    status: {
        EXACT_MATCH: 'exact_match',
        WITHIN_1_SIGMA: 'within_1sigma',
        WITHIN_2_SIGMA: 'within_2sigma',
        WITHIN_3_SIGMA: 'within_3sigma',
        TENSION: 'tension',
        UNTESTED: 'untested'
    }
};

/**
 * Standard parameter definition structure
 */
class PMParameter {
    constructor(config) {
        // Required fields
        this.id = config.id;
        this.value = config.value;

        // Display information
        this.title = config.title || config.id;
        this.shortDescription = config.shortDescription || '';
        this.longDescription = config.longDescription || '';
        this.display = config.display || this.formatValue(config.value);
        this.unit = config.unit || '';
        this.symbol = config.symbol || '';

        // Formula reference
        this.formula = config.formula || null;
        this.formulaHtml = config.formulaHtml || null;
        this.formulaLatex = config.formulaLatex || null;
        this.formulaPlainText = config.formulaPlainText || null;

        // Derivation chain
        this.derivedFrom = config.derivedFrom || [];
        this.derivationSteps = config.derivationSteps || [];
        this.derivationFile = config.derivationFile || null;

        // Experimental comparison
        this.experimentalValue = config.experimentalValue || null;
        this.experimentalUncertainty = config.experimentalUncertainty || null;
        this.experimentalSource = config.experimentalSource || null;
        this.experimentalYear = config.experimentalYear || null;

        // Agreement metrics
        this.agreementSigma = config.agreementSigma || null;
        this.agreementOOM = config.agreementOOM || null;
        this.agreementStatus = this.calculateAgreementStatus();

        // Uncertainty
        this.uncertainty = config.uncertainty || null;
        this.uncertaintyLower = config.uncertaintyLower || null;
        this.uncertaintyUpper = config.uncertaintyUpper || null;
        this.confidenceLevel = config.confidenceLevel || '68%';

        // Category and status
        this.category = config.category || PM_PARAMETER_SCHEMA.categories.DERIVED;
        this.status = config.status || 'derived';
        this.v12_8_status = config.v12_8_status || null;

        // Testability
        this.testable = config.testable || false;
        this.testableBy = config.testableBy || null;
        this.testableYear = config.testableYear || null;

        // References and links
        this.references = config.references || [];
        this.paperSection = config.paperSection || null;
        this.simulationFile = config.simulationFile || null;

        // Terms breakdown (for formulas)
        this.terms = config.terms || {};

        // Related parameters
        this.relatedParams = config.relatedParams || [];
    }

    formatValue(value) {
        if (value === null || value === undefined) return 'N/A';
        if (typeof value === 'number') {
            if (Math.abs(value) >= 1e6 || (Math.abs(value) < 1e-3 && value !== 0)) {
                return value.toExponential(2);
            }
            return value.toPrecision(4);
        }
        return String(value);
    }

    calculateAgreementStatus() {
        if (this.agreementSigma === null) {
            return PM_PARAMETER_SCHEMA.status.UNTESTED;
        }
        const sigma = Math.abs(this.agreementSigma);
        if (sigma === 0) return PM_PARAMETER_SCHEMA.status.EXACT_MATCH;
        if (sigma <= 1) return PM_PARAMETER_SCHEMA.status.WITHIN_1_SIGMA;
        if (sigma <= 2) return PM_PARAMETER_SCHEMA.status.WITHIN_2_SIGMA;
        if (sigma <= 3) return PM_PARAMETER_SCHEMA.status.WITHIN_3_SIGMA;
        return PM_PARAMETER_SCHEMA.status.TENSION;
    }

    getStatusColor() {
        switch (this.agreementStatus) {
            case PM_PARAMETER_SCHEMA.status.EXACT_MATCH:
                return '#4caf50';  // Green
            case PM_PARAMETER_SCHEMA.status.WITHIN_1_SIGMA:
                return '#8bc34a';  // Light green
            case PM_PARAMETER_SCHEMA.status.WITHIN_2_SIGMA:
                return '#ff9800';  // Orange
            case PM_PARAMETER_SCHEMA.status.WITHIN_3_SIGMA:
                return '#ff5722';  // Deep orange
            case PM_PARAMETER_SCHEMA.status.TENSION:
                return '#f44336';  // Red
            default:
                return '#9e9e9e';  // Grey
        }
    }

    getStatusLabel() {
        switch (this.agreementStatus) {
            case PM_PARAMETER_SCHEMA.status.EXACT_MATCH:
                return 'Exact Match';
            case PM_PARAMETER_SCHEMA.status.WITHIN_1_SIGMA:
                return `${this.agreementSigma.toFixed(2)}σ`;
            case PM_PARAMETER_SCHEMA.status.WITHIN_2_SIGMA:
                return `${this.agreementSigma.toFixed(2)}σ`;
            case PM_PARAMETER_SCHEMA.status.WITHIN_3_SIGMA:
                return `${this.agreementSigma.toFixed(2)}σ`;
            case PM_PARAMETER_SCHEMA.status.TENSION:
                return `${this.agreementSigma.toFixed(2)}σ (tension)`;
            default:
                return 'Untested';
        }
    }

    toJSON() {
        return {
            id: this.id,
            value: this.value,
            title: this.title,
            shortDescription: this.shortDescription,
            longDescription: this.longDescription,
            display: this.display,
            unit: this.unit,
            symbol: this.symbol,
            formula: this.formula,
            formulaHtml: this.formulaHtml,
            experimentalValue: this.experimentalValue,
            experimentalUncertainty: this.experimentalUncertainty,
            experimentalSource: this.experimentalSource,
            agreementSigma: this.agreementSigma,
            agreementStatus: this.agreementStatus,
            category: this.category,
            testable: this.testable,
            testableBy: this.testableBy,
            references: this.references,
            simulationFile: this.simulationFile
        };
    }
}

/**
 * Parameter Registry - Single source of truth for all PM parameters
 */
class PMParameterRegistry {
    constructor() {
        this.parameters = new Map();
        this.categories = new Map();
        this.bySimulation = new Map();
    }

    register(param) {
        const p = param instanceof PMParameter ? param : new PMParameter(param);
        this.parameters.set(p.id, p);

        // Index by category
        if (!this.categories.has(p.category)) {
            this.categories.set(p.category, []);
        }
        this.categories.get(p.category).push(p.id);

        // Index by simulation file
        if (p.simulationFile) {
            if (!this.bySimulation.has(p.simulationFile)) {
                this.bySimulation.set(p.simulationFile, []);
            }
            this.bySimulation.get(p.simulationFile).push(p.id);
        }

        return p;
    }

    get(id) {
        return this.parameters.get(id);
    }

    getByCategory(category) {
        const ids = this.categories.get(category) || [];
        return ids.map(id => this.parameters.get(id));
    }

    getBySimulation(simFile) {
        const ids = this.bySimulation.get(simFile) || [];
        return ids.map(id => this.parameters.get(id));
    }

    getStatistics() {
        const params = Array.from(this.parameters.values());
        const withExperimental = params.filter(p => p.experimentalValue !== null);
        const sigmas = withExperimental
            .filter(p => p.agreementSigma !== null)
            .map(p => Math.abs(p.agreementSigma));

        return {
            total: params.length,
            withExperimental: withExperimental.length,
            exactMatches: params.filter(p => p.agreementStatus === PM_PARAMETER_SCHEMA.status.EXACT_MATCH).length,
            within1Sigma: params.filter(p => p.agreementSigma !== null && Math.abs(p.agreementSigma) <= 1).length,
            within2Sigma: params.filter(p => p.agreementSigma !== null && Math.abs(p.agreementSigma) <= 2).length,
            meanSigma: sigmas.length > 0 ? (sigmas.reduce((a, b) => a + b, 0) / sigmas.length).toFixed(2) : 'N/A',
            testable: params.filter(p => p.testable).length,
            geometric: params.filter(p => p.category === PM_PARAMETER_SCHEMA.categories.DERIVED).length,
            calibrated: params.filter(p => p.category === PM_PARAMETER_SCHEMA.categories.CALIBRATED).length
        };
    }

    // Load from simulation output JSON
    loadFromSimulationOutput(data) {
        if (!data || !data.simulations) return;

        for (const [simName, simData] of Object.entries(data.simulations)) {
            if (typeof simData !== 'object') continue;

            // Create parameter entries from simulation output
            for (const [key, value] of Object.entries(simData)) {
                if (typeof value === 'object' && value !== null && value.hasOwnProperty('value')) {
                    // Already structured as parameter
                    this.register({
                        id: `${simName}.${key}`,
                        simulationFile: simName,
                        ...value
                    });
                } else if (typeof value === 'number' || typeof value === 'string') {
                    // Simple value - wrap in parameter
                    this.register({
                        id: `${simName}.${key}`,
                        value: value,
                        title: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                        simulationFile: simName,
                        category: PM_PARAMETER_SCHEMA.categories.DERIVED
                    });
                }
            }
        }
    }

    // Export all parameters to JSON for the website
    exportForWebsite() {
        const output = {};
        for (const [id, param] of this.parameters) {
            output[id] = param.toJSON();
        }
        return output;
    }
}

// Global registry instance
const PM_PARAMS = new PMParameterRegistry();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PM_PARAMETER_SCHEMA, PMParameter, PMParameterRegistry, PM_PARAMS };
}
