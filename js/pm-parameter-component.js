/**
 * Principia Metaphysica - Parameter Display Component
 * ====================================================
 *
 * Custom web component for rendering parameters with hover details,
 * formulas, experimental comparisons, and derivation chains.
 *
 * Usage:
 *   <pm-param id="higgs_mass"></pm-param>
 *   <pm-param id="higgs_mass" show="value"></pm-param>
 *   <pm-param id="higgs_mass" show="agreement"></pm-param>
 *   <pm-param id="higgs_mass" mode="full"></pm-param>
 *
 * Attributes:
 *   - id: Parameter ID from PM_PARAMS registry
 *   - show: What to display (value|agreement|formula|full)
 *   - mode: Display mode (inline|block|card)
 *   - hover: Enable hover tooltip (true|false)
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

class PMParameterComponent extends HTMLElement {
    static get observedAttributes() {
        return ['id', 'show', 'mode', 'hover'];
    }

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }

    getParameter() {
        const id = this.getAttribute('id');
        if (!id) return null;

        // Try PM_PARAMS registry first
        if (typeof PM_PARAMS !== 'undefined' && PM_PARAMS.get) {
            return PM_PARAMS.get(id);
        }

        // Fallback to PM object (theory-constants-enhanced.js)
        if (typeof PM !== 'undefined') {
            const parts = id.split('.');
            let obj = PM;
            for (const part of parts) {
                if (obj && typeof obj === 'object') {
                    obj = obj[part];
                } else {
                    return null;
                }
            }
            return obj;
        }

        return null;
    }

    render() {
        const param = this.getParameter();
        const show = this.getAttribute('show') || 'value';
        const mode = this.getAttribute('mode') || 'inline';
        const hoverEnabled = this.getAttribute('hover') !== 'false';

        const styles = this.getStyles();
        let content = '';

        if (!param) {
            content = `<span class="pm-param-missing">[${this.getAttribute('id') || 'missing'}]</span>`;
        } else if (mode === 'card') {
            content = this.renderCard(param);
        } else if (mode === 'full') {
            content = this.renderFull(param);
        } else {
            content = this.renderInline(param, show, hoverEnabled);
        }

        this.shadowRoot.innerHTML = `
            <style>${styles}</style>
            ${content}
        `;

        // Add event listeners for hover
        if (hoverEnabled && param) {
            this.setupHover();
        }
    }

    renderInline(param, show, hoverEnabled) {
        const value = this.formatValue(param);
        const unit = param.unit || '';
        const statusColor = this.getStatusColor(param);

        let displayContent = '';

        switch (show) {
            case 'agreement':
                const sigma = param.agreementSigma || param.agreement_sigma;
                displayContent = sigma !== null && sigma !== undefined
                    ? `<span class="pm-sigma" style="color: ${statusColor}">${sigma.toFixed(2)}σ</span>`
                    : '<span class="pm-sigma">N/A</span>';
                break;
            case 'formula':
                displayContent = param.formulaHtml || param.formula || value;
                break;
            case 'full':
                displayContent = `<span class="pm-value">${value}</span>
                    ${unit ? `<span class="pm-unit">${unit}</span>` : ''}
                    ${param.agreementSigma ? `<span class="pm-sigma" style="color: ${statusColor}">(${param.agreementSigma.toFixed(2)}σ)</span>` : ''}`;
                break;
            default:
                displayContent = `<span class="pm-value">${value}</span>${unit ? `<span class="pm-unit"> ${unit}</span>` : ''}`;
        }

        return `
            <span class="pm-param-inline ${hoverEnabled ? 'pm-hoverable' : ''}" data-param-id="${param.id || this.getAttribute('id')}">
                ${displayContent}
                ${hoverEnabled ? this.renderTooltip(param) : ''}
            </span>
        `;
    }

    renderCard(param) {
        const value = this.formatValue(param);
        const statusColor = this.getStatusColor(param);
        const statusLabel = this.getStatusLabel(param);

        return `
            <div class="pm-param-card">
                <div class="pm-card-header">
                    <span class="pm-card-title">${param.title || param.id}</span>
                    ${param.symbol ? `<span class="pm-card-symbol">${param.symbol}</span>` : ''}
                </div>
                <div class="pm-card-value">
                    <span class="pm-value-large">${value}</span>
                    ${param.unit ? `<span class="pm-unit">${param.unit}</span>` : ''}
                </div>
                ${param.shortDescription ? `<div class="pm-card-desc">${param.shortDescription}</div>` : ''}
                ${param.experimentalValue !== null && param.experimentalValue !== undefined ? `
                    <div class="pm-card-exp">
                        <span class="pm-exp-label">Experimental:</span>
                        <span class="pm-exp-value">${param.experimentalValue}${param.experimentalUncertainty ? ` ± ${param.experimentalUncertainty}` : ''}</span>
                        ${param.experimentalSource ? `<span class="pm-exp-source">(${param.experimentalSource})</span>` : ''}
                    </div>
                ` : ''}
                ${param.agreementSigma !== null && param.agreementSigma !== undefined ? `
                    <div class="pm-card-agreement" style="border-left: 3px solid ${statusColor}">
                        <span class="pm-agreement-label">Agreement:</span>
                        <span class="pm-agreement-value" style="color: ${statusColor}">${statusLabel}</span>
                    </div>
                ` : ''}
                ${param.formula ? `
                    <div class="pm-card-formula">
                        <span class="pm-formula-label">Formula:</span>
                        <span class="pm-formula-content">${param.formulaHtml || param.formula}</span>
                    </div>
                ` : ''}
                ${param.simulationFile ? `
                    <div class="pm-card-source">
                        <span class="pm-source-label">Source:</span>
                        <code class="pm-source-file">${param.simulationFile}</code>
                    </div>
                ` : ''}
            </div>
        `;
    }

    renderFull(param) {
        return `
            <div class="pm-param-full">
                ${this.renderCard(param)}
                ${param.longDescription ? `
                    <div class="pm-full-desc">
                        <h4>Description</h4>
                        <p>${param.longDescription}</p>
                    </div>
                ` : ''}
                ${param.derivationSteps && param.derivationSteps.length > 0 ? `
                    <div class="pm-full-derivation">
                        <h4>Derivation</h4>
                        <ol>
                            ${param.derivationSteps.map(step => `<li>${step}</li>`).join('')}
                        </ol>
                    </div>
                ` : ''}
                ${param.terms && Object.keys(param.terms).length > 0 ? `
                    <div class="pm-full-terms">
                        <h4>Terms</h4>
                        <dl>
                            ${Object.entries(param.terms).map(([sym, def]) => `
                                <dt>${sym}</dt>
                                <dd>${typeof def === 'object' ? def.description || def.name : def}</dd>
                            `).join('')}
                        </dl>
                    </div>
                ` : ''}
                ${param.references && param.references.length > 0 ? `
                    <div class="pm-full-refs">
                        <h4>References</h4>
                        <ul>
                            ${param.references.map(ref => `<li>${ref}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }

    renderTooltip(param) {
        const statusColor = this.getStatusColor(param);

        return `
            <div class="pm-tooltip">
                <div class="pm-tooltip-header">
                    <strong>${param.title || param.id}</strong>
                    ${param.symbol ? `<span class="pm-tooltip-symbol">${param.symbol}</span>` : ''}
                </div>
                ${param.shortDescription ? `<div class="pm-tooltip-desc">${param.shortDescription}</div>` : ''}
                ${param.formula ? `<div class="pm-tooltip-formula"><em>Formula:</em> ${param.formulaHtml || param.formula}</div>` : ''}
                ${param.experimentalValue !== null && param.experimentalValue !== undefined ? `
                    <div class="pm-tooltip-exp">
                        <em>Exp:</em> ${param.experimentalValue}${param.experimentalUncertainty ? ` ± ${param.experimentalUncertainty}` : ''}
                        ${param.experimentalSource ? `(${param.experimentalSource})` : ''}
                    </div>
                ` : ''}
                ${param.agreementSigma !== null && param.agreementSigma !== undefined ? `
                    <div class="pm-tooltip-sigma" style="color: ${statusColor}">
                        ${param.agreementSigma.toFixed(2)}σ from experiment
                    </div>
                ` : ''}
                ${param.testable ? `
                    <div class="pm-tooltip-testable">
                        <em>Testable:</em> ${param.testableBy || 'Yes'}
                        ${param.testableYear ? `(${param.testableYear})` : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }

    formatValue(param) {
        const value = param.value !== undefined ? param.value : param;
        const display = param.display;

        if (display) return display;

        if (value === null || value === undefined) return 'N/A';
        if (typeof value === 'number') {
            if (Math.abs(value) >= 1e6 || (Math.abs(value) < 1e-3 && value !== 0)) {
                return value.toExponential(2);
            }
            if (Number.isInteger(value)) return value.toString();
            return value.toPrecision(4);
        }
        return String(value);
    }

    getStatusColor(param) {
        const sigma = param.agreementSigma || param.agreement_sigma;
        if (sigma === null || sigma === undefined) return '#9e9e9e';
        const absSigma = Math.abs(sigma);
        if (absSigma === 0) return '#4caf50';
        if (absSigma <= 1) return '#8bc34a';
        if (absSigma <= 2) return '#ff9800';
        if (absSigma <= 3) return '#ff5722';
        return '#f44336';
    }

    getStatusLabel(param) {
        const sigma = param.agreementSigma || param.agreement_sigma;
        if (sigma === null || sigma === undefined) return 'Untested';
        if (sigma === 0) return 'Exact Match';
        return `${sigma.toFixed(2)}σ`;
    }

    setupHover() {
        const wrapper = this.shadowRoot.querySelector('.pm-hoverable');
        const tooltip = this.shadowRoot.querySelector('.pm-tooltip');

        if (!wrapper || !tooltip) return;

        wrapper.addEventListener('mouseenter', () => {
            tooltip.classList.add('pm-tooltip-visible');
        });

        wrapper.addEventListener('mouseleave', () => {
            tooltip.classList.remove('pm-tooltip-visible');
        });
    }

    getStyles() {
        return `
            :host {
                display: inline;
            }

            .pm-param-inline {
                position: relative;
                display: inline;
            }

            .pm-hoverable {
                cursor: help;
                border-bottom: 1px dotted currentColor;
            }

            .pm-value {
                font-weight: 600;
                color: var(--pm-value-color, #8b7fff);
            }

            .pm-unit {
                font-size: 0.9em;
                color: var(--pm-unit-color, #888);
                margin-left: 0.2em;
            }

            .pm-sigma {
                font-size: 0.85em;
                margin-left: 0.3em;
            }

            .pm-param-missing {
                color: #f44336;
                font-style: italic;
            }

            /* Tooltip styles */
            .pm-tooltip {
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, rgba(20, 20, 35, 0.98), rgba(30, 30, 50, 0.95));
                border: 1px solid rgba(139, 127, 255, 0.3);
                border-radius: 8px;
                padding: 12px 16px;
                min-width: 280px;
                max-width: 400px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                z-index: 1000;
                font-size: 0.9rem;
                line-height: 1.5;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.2s, visibility 0.2s;
                pointer-events: none;
            }

            .pm-tooltip-visible {
                opacity: 1;
                visibility: visible;
            }

            .pm-tooltip-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
                color: #fff;
            }

            .pm-tooltip-symbol {
                color: #8b7fff;
                font-family: serif;
            }

            .pm-tooltip-desc {
                color: #aaa;
                margin-bottom: 8px;
            }

            .pm-tooltip-formula {
                background: rgba(0, 0, 0, 0.3);
                padding: 6px 10px;
                border-radius: 4px;
                margin: 8px 0;
                font-family: serif;
                color: #ddd;
            }

            .pm-tooltip-exp, .pm-tooltip-sigma, .pm-tooltip-testable {
                margin-top: 6px;
                color: #ccc;
            }

            /* Card styles */
            .pm-param-card {
                background: linear-gradient(135deg, rgba(139, 127, 255, 0.08), rgba(255, 126, 182, 0.05));
                border: 1px solid rgba(139, 127, 255, 0.2);
                border-radius: 12px;
                padding: 16px 20px;
                margin: 12px 0;
            }

            .pm-card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }

            .pm-card-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: var(--pm-title-color, #8b7fff);
            }

            .pm-card-symbol {
                font-family: serif;
                font-size: 1.2rem;
                color: #888;
            }

            .pm-card-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 8px;
            }

            .pm-card-desc {
                color: #aaa;
                font-size: 0.95rem;
                margin-bottom: 12px;
            }

            .pm-card-exp, .pm-card-agreement, .pm-card-formula, .pm-card-source {
                padding: 8px 12px;
                margin-top: 8px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                font-size: 0.9rem;
            }

            .pm-card-agreement {
                padding-left: 15px;
            }

            .pm-exp-label, .pm-agreement-label, .pm-formula-label, .pm-source-label {
                color: #888;
                margin-right: 8px;
            }

            .pm-exp-source {
                color: #666;
                font-size: 0.85em;
            }

            .pm-source-file {
                font-family: monospace;
                background: rgba(139, 127, 255, 0.1);
                padding: 2px 6px;
                border-radius: 3px;
            }

            /* Full mode styles */
            .pm-param-full {
                padding: 16px;
            }

            .pm-full-desc, .pm-full-derivation, .pm-full-terms, .pm-full-refs {
                margin-top: 16px;
                padding-top: 16px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }

            .pm-full-desc h4, .pm-full-derivation h4, .pm-full-terms h4, .pm-full-refs h4 {
                color: #8b7fff;
                font-size: 1rem;
                margin-bottom: 8px;
            }

            .pm-full-derivation ol {
                padding-left: 24px;
                color: #ccc;
            }

            .pm-full-derivation li {
                margin-bottom: 6px;
            }

            .pm-full-terms dl {
                display: grid;
                grid-template-columns: auto 1fr;
                gap: 8px 16px;
            }

            .pm-full-terms dt {
                color: #8b7fff;
                font-family: serif;
            }

            .pm-full-terms dd {
                color: #aaa;
                margin: 0;
            }

            /* Responsive scaling */
            @media (max-width: 768px) {
                .pm-tooltip {
                    min-width: 200px;
                    max-width: 90vw;
                    font-size: 0.85rem;
                }

                .pm-param-card {
                    padding: 12px 14px;
                }

                .pm-card-value {
                    font-size: 1.3rem;
                }
            }
        `;
    }
}

// Register the custom element
customElements.define('pm-param', PMParameterComponent);

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PMParameterComponent;
}
