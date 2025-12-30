/**
 * PM Formula Component
 * ====================
 *
 * Web component for rendering formulas with hoverable terms and plain text fallback.
 * Uses FORMULA_REGISTRY from formula-registry.js as single source of truth.
 *
 * Usage:
 *   <pm-formula formula-id="master-action-26d"></pm-formula>
 *
 * Or with inline formula (for formulas not in registry):
 *   <pm-formula html="..." plain="..." label="..."></pm-formula>
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

// Use global FORMULA_REGISTRY from formula-registry.js
// Note: FORMULA_REGISTRY is declared globally in formula-registry.js, so we reference it directly
// without re-declaring to avoid "Identifier already declared" errors

/**
 * Find a formula by ID across all categories
 */
function findFormula(id) {
    const registry = window.FORMULA_REGISTRY;
    if (!registry) return null;

    for (const category of ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS']) {
        const categoryFormulas = registry[category];
        if (categoryFormulas && categoryFormulas[id]) {
            return {
                formula: categoryFormulas[id],
                category: category
            };
        }
    }
    return null;
}

/**
 * Parse HTML formula into hoverable spans
 * Wraps mathematical terms with formula-var class and tooltips
 */
function parseFormulaToHoverable(formula) {
    if (!formula.terms || Object.keys(formula.terms).length === 0) {
        // No terms defined, return raw HTML
        return formula.html;
    }

    let html = formula.html;

    // Sort terms by length (longest first) to avoid partial replacements
    const sortedTerms = Object.entries(formula.terms)
        .sort((a, b) => b[0].length - a[0].length);

    for (const [term, info] of sortedTerms) {
        const tooltip = `
            <div class="var-tooltip">
                <div class="var-name">${info.name}</div>
                <div class="var-description">${info.description || ''}</div>
                ${info.link ? `<div class="var-link"><a href="${info.link}">Learn more →</a></div>` : ''}
            </div>
        `;

        // Escape special regex characters in term
        const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

        // Replace term with hoverable span (only if not already wrapped)
        const regex = new RegExp(`(?<!class="formula-var">)${escapedTerm}(?!</span>)`, 'g');
        html = html.replace(regex, `<span class="formula-var">${term}${tooltip}</span>`);
    }

    return html;
}

/**
 * Get category badge color
 */
function getCategoryColor(category) {
    const colors = {
        'ESTABLISHED': '#4ade80',  // green
        'THEORY': '#8b7fff',       // purple
        'DERIVED': '#60a5fa',      // blue
        'PREDICTIONS': '#f472b6'   // pink
    };
    return colors[category] || '#888';
}

/**
 * PM Formula Custom Element
 */
class PMFormula extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
        this.setupTouchHandlers();
    }

    setupTouchHandlers() {
        // Add touch support for mobile devices
        const shadowRoot = this.shadowRoot;
        if (!shadowRoot) return;

        // Wait for next frame to ensure DOM is ready
        requestAnimationFrame(() => {
            const formulaVars = shadowRoot.querySelectorAll('.formula-var');

            formulaVars.forEach(el => {
                // Touch start - show tooltip
                el.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    // Remove touched from all other elements
                    formulaVars.forEach(other => other.classList.remove('touched'));
                    // Add touched to this element
                    el.classList.add('touched');
                }, { passive: false });
            });

            // Touch outside to dismiss
            document.addEventListener('touchstart', (e) => {
                if (!shadowRoot.contains(e.target)) {
                    formulaVars.forEach(el => el.classList.remove('touched'));
                }
            }, { passive: true });

            // Click outside shadow root to dismiss (for hybrid devices)
            shadowRoot.addEventListener('click', (e) => {
                if (!e.target.closest('.formula-var')) {
                    formulaVars.forEach(el => el.classList.remove('touched'));
                }
            });
        });
    }

    static get observedAttributes() {
        return ['formula-id', 'data-id', 'html', 'plain', 'label', 'show-label', 'show-derivation'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }

    render() {
        // Support both formula-id and data-id attributes
        const formulaId = this.getAttribute('formula-id') || this.getAttribute('data-id');
        const inlineHtml = this.getAttribute('html');
        const inlinePlain = this.getAttribute('plain');
        const inlineLabel = this.getAttribute('label');
        const showLabel = this.getAttribute('show-label') !== 'false';
        const showDerivation = this.getAttribute('show-derivation') === 'true';

        let formula, category;

        if (formulaId && formulaId !== 'undefined' && formulaId !== 'null') {
            // Try to look up in FORMULA_REGISTRY first
            const result = findFormula(formulaId);
            if (result) {
                formula = result.formula;
                category = result.category;
            }
            // Try PMFormulaLoader if FORMULA_REGISTRY lookup failed
            else if (window.PMFormulaLoader) {
                const pmFormula = window.PMFormulaLoader.get(formulaId);
                if (pmFormula) {
                    formula = pmFormula;
                    category = pmFormula.category || 'DERIVED';
                } else {
                    this.renderError(`Formula not found in database: <code>${formulaId}</code>`);
                    return;
                }
            } else {
                this.renderError(`Formula not found: <code>${formulaId}</code>`);
                return;
            }
        } else if (inlineHtml) {
            // Use inline attributes
            formula = {
                html: inlineHtml,
                plainText: inlinePlain || '',
                label: inlineLabel || '',
                terms: {}
            };
            category = 'INLINE';
        } else {
            this.renderError('No formula ID or inline content specified');
            return;
        }

        // Build hoverable HTML
        const hoverableHtml = parseFormulaToHoverable(formula);

        // Build derivation chain display
        let derivationHtml = '';
        if (showDerivation && formula.derivation) {
            const parents = formula.derivation.parentFormulas || [];
            const established = formula.derivation.establishedPhysics || [];
            derivationHtml = `
                <div class="derivation-chain">
                    <div class="chain-label">Derivation Chain:</div>
                    ${parents.map(p => `<span class="chain-item parent">${p}</span>`).join(' → ')}
                    ${parents.length > 0 && established.length > 0 ? ' → ' : ''}
                    ${established.map(e => `<span class="chain-item established">${e}</span>`).join(', ')}
                </div>
            `;
        }

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin: 1.5rem 0;
                }

                .formula-container {
                    background: rgba(139, 127, 255, 0.08);
                    border: 1px solid rgba(139, 127, 255, 0.2);
                    border-left: 4px solid ${getCategoryColor(category)};
                    border-radius: 8px;
                    padding: 1rem 1.5rem;
                    position: relative;
                }

                .formula-label {
                    font-family: 'Crimson Text', Georgia, serif;
                    font-size: 0.85rem;
                    color: #888;
                    margin-bottom: 0.5rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .category-badge {
                    font-size: 0.7rem;
                    padding: 0.15rem 0.5rem;
                    border-radius: 10px;
                    background: ${getCategoryColor(category)}22;
                    color: ${getCategoryColor(category)};
                    border: 1px solid ${getCategoryColor(category)}44;
                }

                .formula-display {
                    font-family: 'Times New Roman', serif;
                    font-size: 1.3rem;
                    line-height: 1.8;
                    text-align: center;
                    padding: 0.5rem 0;
                    overflow: visible;
                }

                .formula-var {
                    display: inline-block;
                    position: relative;
                    padding: 0.2rem 0.4rem;
                    margin: 0 0.1rem;
                    background: rgba(139, 127, 255, 0.15);
                    border: 1px solid rgba(139, 127, 255, 0.3);
                    border-radius: 4px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }

                .formula-var:hover {
                    background: rgba(139, 127, 255, 0.3);
                    transform: translateY(-1px);
                    box-shadow: 0 2px 8px rgba(139, 127, 255, 0.2);
                }

                .var-tooltip {
                    position: absolute;
                    bottom: 100%;
                    left: 50%;
                    transform: translateX(-50%) translateY(-8px);
                    width: 250px;
                    background: #1a1a2e;
                    border: 1px solid rgba(139, 127, 255, 0.4);
                    border-radius: 8px;
                    padding: 0.8rem;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
                    z-index: 1000;
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.2s ease;
                    text-align: left;
                }

                .formula-var:hover .var-tooltip {
                    opacity: 1;
                    visibility: visible;
                    transform: translateX(-50%) translateY(-12px);
                }

                .var-tooltip::after {
                    content: '';
                    position: absolute;
                    top: 100%;
                    left: 50%;
                    transform: translateX(-50%);
                    border: 6px solid transparent;
                    border-top-color: rgba(139, 127, 255, 0.4);
                }

                .var-name {
                    font-size: 1rem;
                    color: #8b7fff;
                    font-weight: 600;
                    margin-bottom: 0.3rem;
                }

                .var-description {
                    font-size: 0.85rem;
                    color: #ccc;
                    line-height: 1.4;
                }

                .var-link a {
                    color: #60a5fa;
                    text-decoration: none;
                    font-size: 0.8rem;
                }

                .plain-text {
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    color: #888;
                    text-align: center;
                    padding: 0.5rem 0;
                    border-top: 1px dashed rgba(139, 127, 255, 0.2);
                    margin-top: 0.5rem;
                }

                .plain-text::before {
                    content: 'Plain text: ';
                    color: #666;
                    font-size: 0.75rem;
                }

                .derivation-chain {
                    font-size: 0.8rem;
                    color: #888;
                    margin-top: 0.75rem;
                    padding-top: 0.75rem;
                    border-top: 1px dashed rgba(139, 127, 255, 0.2);
                }

                .chain-label {
                    color: #666;
                    margin-bottom: 0.3rem;
                }

                .chain-item {
                    display: inline-block;
                    padding: 0.1rem 0.4rem;
                    border-radius: 4px;
                    font-size: 0.75rem;
                }

                .chain-item.parent {
                    background: rgba(96, 165, 250, 0.2);
                    color: #60a5fa;
                }

                .chain-item.established {
                    background: rgba(74, 222, 128, 0.2);
                    color: #4ade80;
                }

                /* Mobile touch support */
                @media (hover: none) and (pointer: coarse) {
                    .formula-var:hover {
                        background: rgba(139, 127, 255, 0.15);
                        transform: none;
                        box-shadow: none;
                    }
                    .formula-var:hover .var-tooltip {
                        opacity: 0;
                        visibility: hidden;
                    }
                    .formula-var.touched {
                        background: rgba(139, 127, 255, 0.3);
                        transform: translateY(-1px);
                        box-shadow: 0 2px 8px rgba(139, 127, 255, 0.2);
                    }
                    .formula-var.touched .var-tooltip {
                        opacity: 1 !important;
                        visibility: visible !important;
                        transform: translateX(-50%) translateY(-12px);
                        pointer-events: auto;
                    }
                }

                /* Small screens - tooltip below */
                @media (max-width: 600px) {
                    .var-tooltip {
                        bottom: auto;
                        top: 100%;
                        transform: translateX(-50%) translateY(8px);
                        width: calc(100vw - 4rem);
                        max-width: 300px;
                        left: 50%;
                    }
                    .formula-var:hover .var-tooltip,
                    .formula-var.touched .var-tooltip {
                        transform: translateX(-50%) translateY(12px);
                    }
                    .var-tooltip::after {
                        top: auto;
                        bottom: 100%;
                        border-top-color: transparent;
                        border-bottom-color: rgba(139, 127, 255, 0.4);
                    }
                    .formula-display {
                        font-size: 1.1rem;
                        overflow-x: auto;
                    }
                }
            </style>

            <div class="formula-container">
                ${showLabel && formula.label ? `
                    <div class="formula-label">
                        <span>${formula.label}</span>
                        ${category !== 'INLINE' ? `<span class="category-badge">${category}</span>` : ''}
                    </div>
                ` : ''}

                <div class="formula-display">
                    ${hoverableHtml}
                </div>

                ${formula.plainText ? `
                    <div class="plain-text">${formula.plainText}</div>
                ` : ''}

                ${derivationHtml}
            </div>
        `;
    }

    /**
     * Render an error message
     * @param {string} message - Error message to display
     */
    renderError(message) {
        this.shadowRoot.innerHTML = `
            <style>
                .formula-error {
                    background: rgba(244, 67, 54, 0.1);
                    border: 1px solid rgba(244, 67, 54, 0.3);
                    border-left: 4px solid #f44336;
                    border-radius: 6px;
                    padding: 0.75rem 1rem;
                    color: #d32f2f;
                    font-family: 'Source Sans Pro', sans-serif;
                    font-size: 0.9rem;
                }
                .formula-error strong {
                    display: block;
                    margin-bottom: 0.25rem;
                    color: #f44336;
                }
                .formula-error code {
                    background: rgba(0, 0, 0, 0.1);
                    padding: 0.15rem 0.4rem;
                    border-radius: 3px;
                    font-family: 'Source Code Pro', monospace;
                    font-size: 0.85em;
                }
            </style>
            <div class="formula-error">
                <strong>⚠️ Formula Error</strong>
                ${message}
            </div>
        `;
    }
}

// Register the custom element
if (typeof window !== 'undefined' && window.customElements) {
    if (!customElements.get('pm-formula')) {
        customElements.define('pm-formula', PMFormula);
    }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PMFormula, findFormula, parseFormulaToHoverable };
}
