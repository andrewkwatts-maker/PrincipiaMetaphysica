/**
 * PM Paper Formula Renderer
 * =========================
 *
 * Renders formulas in professional scientific paper format.
 * Designed for print-ready academic presentation.
 *
 * Features:
 * - Black text on white background
 * - Formula numbering (e.g., Eq. 4.13)
 * - Clear description and derivation chain
 * - Input/output parameter listing
 * - Reference citations
 *
 * Usage:
 *   const renderer = new PMPaperFormulaRenderer();
 *   const html = renderer.render(formulaData);
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

(function() {
    'use strict';

    class PMPaperFormulaRenderer {
        constructor(options = {}) {
            this.options = {
                showDerivation: true,
                showParameters: true,
                showReferences: true,
                numberPrefix: 'Eq.',
                ...options
            };
        }

        /**
         * Render a formula in paper format
         * @param {Object} formula - Formula data object
         * @returns {string} HTML string
         */
        render(formula) {
            if (!formula) return '';

            const number = formula.number || formula.id || '';
            const title = formula.title || formula.name || formula.label || '';
            const description = formula.description || formula.shortDescription || '';
            const latex = formula.latex || formula.latexDisplay || '';

            return `
                <div class="paper-formula" id="formula-${this.sanitizeId(formula.id)}">
                    ${this.renderHeader(number, title)}
                    ${this.renderEquation(latex, number)}
                    ${description ? this.renderDescription(description) : ''}
                    ${this.options.showParameters ? this.renderParameters(formula) : ''}
                    ${this.options.showDerivation ? this.renderDerivation(formula) : ''}
                    ${this.options.showReferences ? this.renderReferences(formula) : ''}
                </div>
            `;
        }

        /**
         * Render formula header with number and title
         */
        renderHeader(number, title) {
            if (!title) return '';
            return `
                <div class="paper-formula-header">
                    ${number ? `<span class="formula-number">${this.options.numberPrefix} ${number}:</span>` : ''}
                    <span class="formula-title">${this.escapeHtml(title)}</span>
                </div>
            `;
        }

        /**
         * Render the main equation display
         */
        renderEquation(latex, number) {
            if (!latex) return '';

            // For MathJax display mode
            const displayLatex = latex.includes('\\[') || latex.includes('$$')
                ? latex
                : `\\[${latex}\\]`;

            return `
                <div class="paper-equation-block">
                    <div class="paper-equation">
                        ${displayLatex}
                    </div>
                    ${number ? `<span class="equation-number">(${number})</span>` : ''}
                </div>
            `;
        }

        /**
         * Render description text
         */
        renderDescription(description) {
            return `
                <div class="paper-formula-description">
                    <p>${this.escapeHtml(description)}</p>
                </div>
            `;
        }

        /**
         * Render input/output parameters
         */
        renderParameters(formula) {
            const inputs = formula.inputParams || formula.input_params || [];
            const outputs = formula.outputParams || formula.output_params || [];
            const components = formula.components || formula.terms || [];

            if (inputs.length === 0 && outputs.length === 0 && components.length === 0) {
                return '';
            }

            let html = '<div class="paper-formula-params">';

            // Component terms (what each symbol means)
            if (components.length > 0) {
                html += `
                    <div class="paper-params-section">
                        <strong>where:</strong>
                        <ul class="paper-params-list terms-list">
                            ${components.map(c => `
                                <li>
                                    <span class="param-symbol">${this.escapeHtml(c.symbol || c.name || '')}</span>
                                    ${c.description ? ` — ${this.escapeHtml(c.description)}` : ''}
                                    ${c.value !== undefined ? ` = ${this.formatValue(c.value)}` : ''}
                                    ${c.units ? ` ${this.escapeHtml(c.units)}` : ''}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                `;
            }

            // Input parameters
            if (inputs.length > 0) {
                html += `
                    <div class="paper-params-section">
                        <strong>Inputs:</strong>
                        <span class="paper-params-inline">
                            ${inputs.map(p => this.formatParamRef(p)).join(', ')}
                        </span>
                    </div>
                `;
            }

            // Output parameters
            if (outputs.length > 0) {
                html += `
                    <div class="paper-params-section">
                        <strong>Outputs:</strong>
                        <span class="paper-params-inline">
                            ${outputs.map(p => this.formatParamRef(p)).join(', ')}
                        </span>
                    </div>
                `;
            }

            html += '</div>';
            return html;
        }

        /**
         * Format a parameter reference
         */
        formatParamRef(param) {
            if (typeof param === 'string') {
                // Just the parameter path like "topology.b3"
                const name = param.split('.').pop();
                return `<code class="param-ref">${this.escapeHtml(name)}</code>`;
            }
            // Object with value
            const name = param.symbol || param.name || (param.constant || '').split('.').pop();
            const val = param.value !== undefined ? ` = ${this.formatValue(param.value)}` : '';
            const units = param.units ? ` ${this.escapeHtml(param.units)}` : '';
            return `<code class="param-ref">${this.escapeHtml(name)}${val}${units}</code>`;
        }

        /**
         * Render derivation chain
         */
        renderDerivation(formula) {
            const derivation = formula.derivationChain || formula.derivation?.steps || [];
            const parentFormulas = formula.derivation?.parentFormulas || [];

            if (derivation.length === 0 && parentFormulas.length === 0) {
                return '';
            }

            let html = '<div class="paper-derivation">';
            html += '<strong>Derivation:</strong>';

            if (derivation.length > 0) {
                html += '<ol class="derivation-steps">';
                derivation.forEach(step => {
                    if (typeof step === 'string') {
                        html += `<li>${this.escapeHtml(step)}</li>`;
                    } else {
                        // Step object with name, badge, link
                        const badge = step.badge ? ` <span class="derivation-badge ${this.getBadgeClass(step.badge)}">${this.escapeHtml(step.badge)}</span>` : '';
                        const text = step.link
                            ? `<a href="${this.escapeHtml(step.link)}">${this.escapeHtml(step.name || step.step || '')}</a>`
                            : this.escapeHtml(step.name || step.step || '');
                        html += `<li>${text}${badge}</li>`;
                    }
                });
                html += '</ol>';
            }

            if (parentFormulas.length > 0) {
                html += `
                    <div class="parent-formulas">
                        <em>Derived from:</em> ${parentFormulas.map(p =>
                            `<a href="#formula-${this.sanitizeId(p)}">${this.escapeHtml(p)}</a>`
                        ).join(', ')}
                    </div>
                `;
            }

            html += '</div>';
            return html;
        }

        /**
         * Render references
         */
        renderReferences(formula) {
            const refs = formula.references || formula.foundationRefs || [];

            if (refs.length === 0) return '';

            return `
                <div class="paper-references">
                    <strong>References:</strong>
                    <ul class="reference-list">
                        ${refs.map(ref => {
                            if (typeof ref === 'string') {
                                return `<li>${this.escapeHtml(ref)}</li>`;
                            }
                            // Reference object with title, url, authors, year
                            const link = ref.url
                                ? `<a href="${this.escapeHtml(ref.url)}" target="_blank">${this.escapeHtml(ref.title || ref.name)}</a>`
                                : this.escapeHtml(ref.title || ref.name);
                            const authors = ref.authors ? `${this.escapeHtml(ref.authors)}. ` : '';
                            const year = ref.year ? ` (${ref.year})` : '';
                            return `<li>${authors}${link}${year}</li>`;
                        }).join('')}
                    </ul>
                </div>
            `;
        }

        /**
         * Get CSS class for badge type
         */
        getBadgeClass(badge) {
            const lower = (badge || '').toLowerCase();
            if (lower.includes('established')) return 'badge-established';
            if (lower.includes('mathematics')) return 'badge-mathematics';
            if (lower.includes('derived')) return 'badge-derived';
            if (lower.includes('prediction')) return 'badge-prediction';
            if (lower.includes('pm')) return 'badge-pm';
            return 'badge-default';
        }

        /**
         * Format numeric value
         */
        formatValue(value) {
            if (value === null || value === undefined) return 'N/A';
            if (typeof value === 'number') {
                const abs = Math.abs(value);
                if (abs >= 1e6 || (abs < 1e-3 && abs !== 0)) {
                    return value.toExponential(3);
                }
                if (Number.isInteger(value)) return value.toString();
                return value.toPrecision(4);
            }
            return String(value);
        }

        /**
         * Sanitize ID for use in HTML
         */
        sanitizeId(id) {
            return (id || '').replace(/[^a-zA-Z0-9-_]/g, '-');
        }

        /**
         * Escape HTML entities
         */
        escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        /**
         * Get CSS styles for paper format
         */
        static getStyles() {
            return `
                /* Paper Formula Styles - Professional Scientific Format */
                .paper-formula {
                    margin: 1.5rem 0;
                    padding: 1rem 0;
                    border-bottom: 1px solid #e0e0e0;
                    color: #000;
                    font-family: 'Times New Roman', Times, serif;
                    font-size: 11pt;
                    line-height: 1.6;
                }

                .paper-formula:last-child {
                    border-bottom: none;
                }

                .paper-formula-header {
                    margin-bottom: 0.75rem;
                }

                .paper-formula-header .formula-number {
                    font-weight: bold;
                    color: #333;
                }

                .paper-formula-header .formula-title {
                    font-style: italic;
                    margin-left: 0.5rem;
                }

                .paper-equation-block {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin: 1rem 0;
                    padding: 0.5rem 1rem;
                    background: #fafafa;
                    border-left: 3px solid #333;
                }

                .paper-equation {
                    flex: 1;
                    text-align: center;
                    color: #000;
                    font-size: 1.1em;
                }

                .paper-equation .MathJax {
                    color: #000 !important;
                }

                .equation-number {
                    font-weight: bold;
                    color: #333;
                    margin-left: 1rem;
                    white-space: nowrap;
                }

                .paper-formula-description {
                    margin: 0.75rem 0;
                    color: #333;
                    text-align: justify;
                }

                .paper-formula-params {
                    margin: 1rem 0;
                    padding-left: 1rem;
                    font-size: 10pt;
                }

                .paper-params-section {
                    margin: 0.5rem 0;
                }

                .paper-params-section strong {
                    color: #333;
                }

                .paper-params-list {
                    margin: 0.25rem 0 0.25rem 1.5rem;
                    padding: 0;
                }

                .paper-params-list li {
                    margin: 0.25rem 0;
                }

                .paper-params-list .param-symbol {
                    font-family: serif;
                    font-style: italic;
                    color: #000;
                }

                .paper-params-inline {
                    display: inline;
                }

                .param-ref {
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                    background: #f0f0f0;
                    padding: 0.1rem 0.3rem;
                    border-radius: 2px;
                }

                .paper-derivation {
                    margin: 1rem 0;
                    padding-left: 1rem;
                    font-size: 10pt;
                }

                .derivation-steps {
                    margin: 0.5rem 0 0.5rem 1.5rem;
                    padding: 0;
                }

                .derivation-steps li {
                    margin: 0.25rem 0;
                }

                .derivation-badge {
                    display: inline-block;
                    font-size: 0.75em;
                    padding: 0.1rem 0.4rem;
                    border-radius: 3px;
                    margin-left: 0.5rem;
                    font-weight: 500;
                    text-transform: uppercase;
                }

                .badge-established {
                    background: #4caf50;
                    color: white;
                }

                .badge-mathematics {
                    background: #2196f3;
                    color: white;
                }

                .badge-derived {
                    background: #9c27b0;
                    color: white;
                }

                .badge-prediction {
                    background: #ff9800;
                    color: white;
                }

                .badge-pm {
                    background: #8b7fff;
                    color: white;
                }

                .badge-default {
                    background: #757575;
                    color: white;
                }

                .parent-formulas {
                    margin-top: 0.5rem;
                    font-style: italic;
                }

                .parent-formulas a {
                    color: #1a73e8;
                    text-decoration: none;
                }

                .parent-formulas a:hover {
                    text-decoration: underline;
                }

                .paper-references {
                    margin: 1rem 0;
                    padding-left: 1rem;
                    font-size: 9pt;
                }

                .reference-list {
                    margin: 0.25rem 0 0 1.5rem;
                    padding: 0;
                }

                .reference-list li {
                    margin: 0.15rem 0;
                }

                .reference-list a {
                    color: #1a73e8;
                    text-decoration: none;
                }

                .reference-list a:hover {
                    text-decoration: underline;
                }

                /* Print styles */
                @media print {
                    .paper-formula {
                        page-break-inside: avoid;
                    }

                    .paper-equation-block {
                        background: white;
                        border-left-color: #000;
                    }

                    .derivation-badge {
                        border: 1px solid currentColor;
                    }
                }
            `;
        }
    }

    // Export
    window.PMPaperFormulaRenderer = PMPaperFormulaRenderer;

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = PMPaperFormulaRenderer;
    }
})();
