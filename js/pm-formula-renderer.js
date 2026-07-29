/**
 * PM Formula Renderer
 * ===================
 *
 * Rich UX formula rendering system for Principia Metaphysica.
 * Supports interactive formulas with tooltips, info panels, expandable sections,
 * and full rendering modes for both inline (sections.html) and standalone (formulas.html) views.
 *
 * Usage:
 *   PMFormulaRenderer.renderInteractive(formulaId, containerId, options)
 *   PMFormulaRenderer.renderInfoPanel(formulaId, containerId)
 *   PMFormulaRenderer.renderExpandable(formulaId, containerId)
 *   PMFormulaRenderer.renderPlainText(formulaId, containerId)
 *   PMFormulaRenderer.renderFull(formulaId, containerId, options)
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

(function(window) {
    'use strict';

    // State management
    const state = {
        loadingFormulas: new Set(),
        failedFormulas: new Set(),
        eventListeners: new WeakMap() // Track listeners for cleanup
    };

    const PMFormulaRenderer = {
        /**
         * Get formula data from multiple sources with fallback strategy
         * @param {string} formulaId - Formula identifier
         * @returns {Object|null} - Formula data object or null if not found
         * @private
         */
        getFormula(formulaId) {
            // Validate formulaId - check for null, undefined, empty string, and string "undefined"/"null"
            if (!formulaId || formulaId === 'undefined' || formulaId === 'null') {
                console.warn('PMFormulaRenderer: Invalid or empty formula ID provided:', formulaId);
                return null;
            }

            // Strategy 1: Try PM.formulas first (from pm-constants-loader.js)
            if (window.PM && window.PM.formulas && window.PM.formulas[formulaId]) {
                return window.PM.formulas[formulaId];
            }

            // Strategy 2: Try PM_FORMULAS global (exported by pm-constants-loader.js)
            if (window.PM_FORMULAS && window.PM_FORMULAS[formulaId]) {
                return window.PM_FORMULAS[formulaId];
            }

            // Strategy 3: Try PM._data.formulas.formulas (direct access)
            if (window.PM && window.PM._data && window.PM._data.formulas && window.PM._data.formulas.formulas) {
                const formula = window.PM._data.formulas.formulas[formulaId];
                if (formula) return formula;
            }

            // Strategy 4: Try FORMULA_REGISTRY (legacy support)
            if (window.FORMULA_REGISTRY) {
                for (const category of ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS']) {
                    const formulas = window.FORMULA_REGISTRY[category];
                    if (formulas && formulas[formulaId]) {
                        return { ...formulas[formulaId], category };
                    }
                }
            }

            // Strategy 5: Try window.findFormula if available (legacy support)
            if (typeof window.findFormula === 'function') {
                const result = window.findFormula(formulaId);
                if (result) {
                    return { ...result.formula, category: result.category };
                }
            }

            // Cache failure to avoid repeated lookups
            if (!state.failedFormulas.has(formulaId)) {
                console.warn(`PMFormulaRenderer: Formula not found: ${formulaId}`);
                state.failedFormulas.add(formulaId);
            }

            return null;
        },

        /**
         * Parse HTML formula into hoverable variables with tooltips
         * @param {string} formulaHtml - Formula HTML string
         * @param {Object} terms - Map of term symbols to their metadata
         * @returns {string} - HTML with hoverable term elements
         * @private
         */
        parseToHoverable(formulaHtml, terms) {
            if (!formulaHtml) {
                console.warn('PMFormulaRenderer: Empty formula HTML provided');
                return '';
            }

            if (!terms || typeof terms !== 'object' || Object.keys(terms).length === 0) {
                return formulaHtml;
            }

            let html = formulaHtml;

            // Sort terms by length (longest first) to avoid partial replacements
            const sortedTerms = Object.entries(terms)
                .sort((a, b) => b[0].length - a[0].length);

            for (const [term, info] of sortedTerms) {
                const tooltip = this.createTooltip(info.name, info.description, info.units, info.contribution, info.link);

                // Escape special regex characters
                const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

                // Replace term with hoverable link (only if not already wrapped)
                // Safari-compatible: avoid lookbehind by using split/join approach
                const link = info.link || '#';
                const replacement = `<a class="formula-var" href="${link}" style="text-decoration: none; color: inherit;">${term}${tooltip}</a>`;

                // Skip if already wrapped (check for formula-var before term)
                if (!html.includes(`class="formula-var">${term}`)) {
                    // Use simple regex without lookbehind for Safari compatibility
                    const regex = new RegExp(`${escapedTerm}(?![^<]*</a>)`, 'g');
                    html = html.replace(regex, replacement);
                }
            }

            return html;
        },

        /**
         * Create tooltip HTML
         */
        createTooltip(name, description, units, contribution, link) {
            let tooltip = '<div class="var-tooltip">';
            tooltip += `<div class="var-name">${name}</div>`;

            if (description) {
                tooltip += `<div class="var-description">${description}</div>`;
            }

            if (units) {
                tooltip += `<div class="var-units">${units}</div>`;
            }

            if (contribution) {
                tooltip += `<div class="var-contribution">${contribution}</div>`;
            }

            if (link) {
                tooltip += `<div style="margin-top: 0.5rem; color: var(--accent-secondary); font-size: 0.8rem;">Click to learn more →</div>`;
            }

            tooltip += '</div>';
            return tooltip;
        },

        /**
         * Render interactive formula display with hoverable variables
         * @param {string} formulaId - Formula ID
         * @param {string|HTMLElement} container - Container ID or element
         * @param {Object} options - Rendering options
         *   - showHint: Show "Hover for details" hint (default: true)
         *   - large: Use large font size (default: false)
         */
        renderInteractive(formulaId, container, options = {}) {
            const formula = this.getFormula(formulaId);
            if (!formula) {
                this.renderError(container, `Formula not found: ${formulaId}`, { formulaId });
                return;
            }

            const {
                showHint = true,
                large = false
            } = options;

            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`Container not found: ${container}`);
                return;
            }

            const hoverableHtml = this.parseToHoverable(formula.html, formula.terms);

            let html = '<div class="interactive-formula">';

            if (showHint) {
                html += '<span class="formula-hint">Hover for details</span>';
            }

            html += `<div class="formula-display${large ? ' large' : ''}">`;
            html += hoverableHtml;
            html += '</div>';
            html += '</div>';

            containerEl.innerHTML = html;
            this.setupTooltipHandlers(containerEl);
        },

        /**
         * Render formula info panel
         * Shows title, meaning, info grid (dimensions, gauge group), and use cases
         */
        renderInfoPanel(formulaId, container) {
            const formula = this.getFormula(formulaId);
            if (!formula) {
                this.renderError(container, `Formula not found: ${formulaId}`, { formulaId });
                return;
            }

            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`Container not found: ${container}`);
                return;
            }

            let html = '<div class="formula-info">';

            // Title
            if (formula.label || formula.description) {
                html += `<div class="formula-title">${formula.label || formula.description}</div>`;
            }

            // Meaning
            if (formula.description && formula.label !== formula.description) {
                html += `<div class="formula-meaning">${formula.description}</div>`;
            }

            // Info grid (metadata)
            if (formula.infoGrid && formula.infoGrid.length > 0) {
                html += '<div class="formula-info-grid">';
                for (const item of formula.infoGrid) {
                    const link = item.link || '#';
                    html += `
                        <div class="formula-info-item">
                            <a href="${link}" style="text-decoration: none; color: inherit;">
                                <h5>${item.title}</h5>
                                <p>${item.content}</p>
                            </a>
                        </div>
                    `;
                }
                html += '</div>';
            }

            // Use cases ("What Emerges")
            if (formula.useCases && formula.useCases.length > 0) {
                html += '<div class="use-cases">';
                html += '<h5>What Emerges</h5>';
                html += '<ul>';
                for (const useCase of formula.useCases) {
                    const link = useCase.link || '#';
                    html += `
                        <li>
                            <a href="${link}" style="color: var(--text-secondary);">${useCase.text}</a>
                        </li>
                    `;
                }
                html += '</ul>';
                html += '</div>';
            }

            html += '</div>';

            containerEl.innerHTML = html;
        },

        /**
         * Render expandable section
         * Collapsible header with sub-components grid and derivation chain
         */
        renderExpandable(formulaId, container, options = {}) {
            const formula = this.getFormula(formulaId);
            if (!formula) {
                this.renderError(container, `Formula not found: ${formulaId}`, { formulaId });
                return;
            }

            const {
                headerText = 'Dimensional Reduction',
                expanded = false
            } = options;

            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`Container not found: ${container}`);
                return;
            }

            const expandedClass = expanded ? ' expanded' : '';

            let html = `<div class="expandable-formula${expandedClass}">`;

            // Header
            html += '<div class="formula-header" style="cursor: pointer;">';
            html += '<div class="formula-main">';
            html += `<span style="color: var(--text-muted); font-size: 0.85rem; margin-right: 0.5rem;">▼ ${headerText}:</span>`;
            html += formula.plainText || formula.label;
            html += '</div>';
            html += '<div class="formula-controls">';
            html += `<button class="expand-btn" title="Expand to see details">${expanded ? '▲' : '▼'}</button>`;
            html += '</div>';
            html += '</div>';

            // Expansion content
            html += '<div class="formula-expansion">';

            // Sub-components
            if (formula.subComponents && formula.subComponents.length > 0) {
                html += '<div class="sub-components">';
                for (const component of formula.subComponents) {
                    const link = component.link || '#';
                    html += `
                        <a class="sub-component" href="${link}" style="text-decoration: none;">
                            <div class="component-symbol">${component.symbol}</div>
                            <div class="component-name">${component.name}</div>
                            <div class="component-description">${component.description}</div>
                            ${component.badge ? `<span class="foundation-badge ${component.badgeClass || 'established'}">${component.badge}</span>` : ''}
                        </a>
                    `;
                }
                html += '</div>';
            }

            // Derivation chain
            if (formula.derivation && (formula.derivation.establishedPhysics || formula.derivation.parentFormulas)) {
                html += '<div class="derivation-chain">';
                html += '<div class="chain-title">Derivation Path to Established Physics</div>';

                // Parent formulas
                if (formula.derivation.parentFormulas && formula.derivation.parentFormulas.length > 0) {
                    for (const parentId of formula.derivation.parentFormulas) {
                        const parent = this.getFormula(parentId);
                        if (parent) {
                            html += `
                                <div class="chain-step">
                                    <span class="step-arrow">→</span>
                                    <a href="#${parentId}">${parent.label || parentId}</a>
                                    <span class="foundation-badge derived">PM Derived</span>
                                </div>
                            `;
                        }
                    }
                }

                // Established physics roots
                if (formula.derivation.establishedPhysics && formula.derivation.establishedPhysics.length > 0) {
                    for (const estId of formula.derivation.establishedPhysics) {
                        const est = this.getFormula(estId);
                        if (est) {
                            html += `
                                <div class="chain-step">
                                    <span class="step-arrow">→</span>
                                    <a href="foundations/${estId}.html">${est.label || estId}</a>
                                    <span class="foundation-badge established">Established</span>
                                </div>
                            `;
                        }
                    }
                }

                html += '</div>';
            }

            html += '</div>'; // formula-expansion
            html += '</div>'; // expandable-formula

            containerEl.innerHTML = html;

            // Setup expand/collapse handler
            const header = containerEl.querySelector('.formula-header');
            const expandBtn = containerEl.querySelector('.expand-btn');
            const expandableDiv = containerEl.querySelector('.expandable-formula');

            if (header && expandBtn && expandableDiv) {
                const toggleExpand = () => {
                    expandableDiv.classList.toggle('expanded');
                    expandBtn.textContent = expandableDiv.classList.contains('expanded') ? '▲' : '▼';
                };
                header.addEventListener('click', toggleExpand);
                expandBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleExpand();
                });
            }
        },

        /**
         * Render plain text version of formula
         * Good for AI processing and accessibility
         */
        renderPlainText(formulaId, container) {
            const formula = this.getFormula(formulaId);
            if (!formula) {
                this.renderError(container, `Formula not found: ${formulaId}`, { formulaId });
                return;
            }

            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`Container not found: ${container}`);
                return;
            }

            const plainText = formula.plainText || formula.latex || formula.html.replace(/<[^>]*>/g, '');

            let html = '<div class="formula-plain-text" style="';
            html += 'font-family: \'Courier New\', monospace; ';
            html += 'background: rgba(0, 0, 0, 0.3); ';
            html += 'padding: 1rem; ';
            html += 'border-radius: 8px; ';
            html += 'border-left: 4px solid var(--accent-primary); ';
            html += 'overflow-x: auto; ';
            html += 'white-space: pre-wrap; ';
            html += 'word-break: break-all;';
            html += '">';

            if (formula.label) {
                html += `<div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem;">${formula.label}</div>`;
            }

            html += `<code>${plainText}</code>`;
            html += '</div>';

            containerEl.innerHTML = html;
        },

        /**
         * Render full formula display
         * Combines interactive, info panel, and optionally expandable sections
         */
        renderFull(formulaId, container, options = {}) {
            const formula = this.getFormula(formulaId);
            if (!formula) {
                this.renderError(container, `Formula not found: ${formulaId}`, { formulaId });
                return;
            }

            const {
                showInteractive = true,
                showInfoPanel = true,
                showExpandable = false,
                showPlainText = true,
                interactiveOptions = {},
                expandableOptions = {}
            } = options;

            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`Container not found: ${container}`);
                return;
            }

            // Clear container
            containerEl.innerHTML = '';

            // Create sections
            if (showInteractive) {
                const interactiveDiv = document.createElement('div');
                containerEl.appendChild(interactiveDiv);
                this.renderInteractive(formulaId, interactiveDiv, { large: true, ...interactiveOptions });
            }

            if (showInfoPanel) {
                const infoDiv = document.createElement('div');
                containerEl.appendChild(infoDiv);
                this.renderInfoPanel(formulaId, infoDiv);
            }

            if (showExpandable) {
                const expandableDiv = document.createElement('div');
                expandableDiv.style.marginTop = '1.5rem';
                containerEl.appendChild(expandableDiv);
                this.renderExpandable(formulaId, expandableDiv, expandableOptions);
            }

            if (showPlainText) {
                const plainTextDiv = document.createElement('div');
                plainTextDiv.style.marginTop = '1.5rem';
                containerEl.appendChild(plainTextDiv);
                this.renderPlainText(formulaId, plainTextDiv);
            }
        },

        /**
         * Render loading state
         * @param {string|HTMLElement} container - Container element or selector
         * @param {string} message - Loading message
         * @private
         */
        renderLoading(container, message = 'Loading formula...') {
            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`PMFormulaRenderer: Container not found: ${container}`);
                return;
            }

            containerEl.innerHTML = `
                <div class="pm-loading" style="
                    background: rgba(96, 165, 250, 0.1);
                    border: 1px solid rgba(96, 165, 250, 0.3);
                    border-radius: 8px;
                    padding: 1rem;
                    color: #60a5fa;
                    text-align: center;
                    animation: pulse 1.5s ease-in-out infinite;
                ">
                    <span class="loading-spinner" style="display: inline-block; margin-right: 0.5rem;">⏳</span>
                    ${message}
                </div>
            `;
        },

        /**
         * Render error message with helpful diagnostic information
         * @param {string|HTMLElement} container - Container element or selector
         * @param {string} message - Error message
         * @param {Object} details - Additional error details
         * @private
         */
        renderError(container, message, details = {}) {
            const containerEl = typeof container === 'string'
                ? document.getElementById(container) || document.querySelector(container)
                : container;

            if (!containerEl) {
                console.error(`PMFormulaRenderer: Container not found: ${container}`);
                return;
            }

            let errorHtml = `
                <div class="pm-error" style="
                    background: rgba(244, 67, 54, 0.1);
                    border: 1px solid rgba(244, 67, 54, 0.3);
                    border-left: 4px solid #f44336;
                    border-radius: 8px;
                    padding: 1rem;
                    color: #f44336;
                ">
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">
                        <span style="margin-right: 0.5rem;">⚠️</span>
                        Error
                    </div>
                    <div style="color: #d32f2f;">${message}</div>
            `;

            // Add troubleshooting hints
            if (details.formulaId) {
                errorHtml += `
                    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(244, 67, 54, 0.2); color: #666; font-size: 0.9rem;">
                        <strong>Troubleshooting:</strong>
                        <ul style="margin: 0.5rem 0 0 1.5rem; padding: 0;">
                            <li>Ensure <code>pm-constants-loader.js</code> is loaded</li>
                            <li>Check that <code>AutoGenerated/formulas.json</code> exists</li>
                            <li>Verify formula ID: <code>${details.formulaId}</code></li>
                            <li>Check browser console for more details</li>
                        </ul>
                    </div>
                `;
            }

            errorHtml += '</div>';
            containerEl.innerHTML = errorHtml;
            containerEl.classList.add('pm-error-state');
        },

        /**
         * Setup tooltip handlers for mobile touch support with proper cleanup
         * @param {HTMLElement} containerEl - Container element
         * @private
         */
        setupTooltipHandlers(containerEl) {
            if (!containerEl) return;

            // Clean up any existing listeners for this container
            this.cleanupTooltipHandlers(containerEl);

            const formulaVars = containerEl.querySelectorAll('.formula-var');
            const handlers = [];

            formulaVars.forEach(el => {
                // Touch start handler - show tooltip
                const touchHandler = (e) => {
                    e.preventDefault();
                    // Remove touched from all other elements
                    formulaVars.forEach(other => other.classList.remove('touched'));
                    // Add touched to this element
                    el.classList.add('touched');
                };

                el.addEventListener('touchstart', touchHandler, { passive: false });

                // Store handler for cleanup
                handlers.push({ element: el, event: 'touchstart', handler: touchHandler });
            });

            // Touch outside to dismiss
            const dismissHandler = (e) => {
                if (!containerEl.contains(e.target)) {
                    formulaVars.forEach(el => el.classList.remove('touched'));
                }
            };

            document.addEventListener('touchstart', dismissHandler, { passive: true });
            handlers.push({ element: document, event: 'touchstart', handler: dismissHandler });

            // Store handlers in WeakMap for cleanup
            state.eventListeners.set(containerEl, handlers);
        },

        /**
         * Clean up tooltip handlers to prevent memory leaks
         * @param {HTMLElement} containerEl - Container element
         * @private
         */
        cleanupTooltipHandlers(containerEl) {
            if (!containerEl) return;

            const handlers = state.eventListeners.get(containerEl);
            if (handlers) {
                handlers.forEach(({ element, event, handler }) => {
                    element.removeEventListener(event, handler);
                });
                state.eventListeners.delete(containerEl);
            }
        },

        /**
         * Normalize a LaTeX string for cross-check comparison.
         * Strategy: strip whitespace and lowercase. This is intentionally lossy
         * - we just want to surface the obvious Sprint 2 disagreements
         * (e.g. n_gen = chi_eff/(4 b_3) vs the buggy chi_eff/(4*b_3*) form,
         * the dark-force leakage discrepancy, etc).
         * @param {string} s - LaTeX source
         * @returns {string} - normalized string
         */
        normalizeLatex(s) {
            if (!s || typeof s !== 'string') return '';
            return s.replace(/\s+/g, '').toLowerCase();
        },

        /**
         * Detect mismatch between Arithma and EML LaTeX renderings.
         * @param {Object} formula - formula record
         * @returns {boolean} - true if both views exist AND disagree
         */
        isMismatch(formula) {
            if (!formula) return false;
            const arithma = formula.arithma_latex || '';
            const eml = formula.eml_latex || formula.emlLatex || '';
            if (!arithma || !eml) return false;
            return this.normalizeLatex(arithma) !== this.normalizeLatex(eml);
        },

        /**
         * Format a numeric value for the "Value" panel.
         * Uses scientific notation for very large/small numbers and respects
         * sensible precision. Returns an HTML snippet (number + units + rel).
         * @param {Object} formula - formula record
         * @returns {string} - HTML
         */
        formatValueBlock(formula) {
            if (!formula) return '';
            const raw = formula.value;
            const computed = formula.computedValue;
            const v = (raw !== undefined && raw !== null) ? raw : computed;

            if (v === undefined || v === null) {
                return '<div class="pm-tv-panel__empty">No evaluated value</div>';
            }

            let numStr;
            if (typeof v === 'number') {
                const absv = Math.abs(v);
                if (absv === 0) {
                    numStr = '0';
                } else if (absv < 1e-3 || absv >= 1e5) {
                    numStr = v.toExponential(6);
                } else {
                    numStr = v.toPrecision(8);
                }
            } else {
                numStr = String(v);
            }

            const units = formula.units || '';
            const rel = formula.rel_tolerance || formula.relTolerance ||
                        (formula.uncertainty != null ? `±${formula.uncertainty}` : '');

            let html = `<span class="pm-tv-value__number">${this.escapeHtml(numStr)}</span>`;
            if (units) {
                const formattedUnits = String(units)
                    .replace(/\^(-?\d+)/g, '<sup>$1</sup>')
                    .replace(/\*\*/g, '');
                html += `<span class="pm-tv-value__units">${formattedUnits}</span>`;
            }
            if (rel) {
                html += `<span class="pm-tv-value__rel">rel = ${this.escapeHtml(String(rel))}</span>`;
            }
            return html;
        },

        /**
         * Escape HTML for safe insertion.
         */
        escapeHtml(s) {
            if (s === null || s === undefined) return '';
            return String(s)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        },

        /**
         * Pick the best EML LaTeX source available on a formula.
         * Preference: cached eml_latex -> eml_tree_compact.x -> eml_tree_str
         */
        getEmlLatex(formula) {
            if (!formula) return '';
            if (formula.eml_latex) return formula.eml_latex;
            if (formula.emlLatex) return formula.emlLatex;
            const compact = formula.eml_tree_compact;
            if (compact && typeof compact === 'object') {
                if (compact.x) return compact.x;
                if (compact.latex) return compact.latex;
            }
            return '';
        },

        /**
         * Render the three-column triple-view (Arithma / EML / Value).
         *
         * Layout:
         *   +---------------+---------------+----------------+
         *   | Arithma LaTeX | EML LaTeX     | Value (float)  |
         *   +---------------+---------------+----------------+
         *
         * Graceful degradation:
         *   - arithma_latex missing -> 2 columns (EML + Value)
         *   - both LaTeX missing    -> 1 column (Value only)
         *
         * @param {Object} formula - formula record from formulas.json
         * @param {Object} options
         *   - graphHref: URL the "Trace to b3" button should point to (default '#')
         *   - showActions: render the action row (default true)
         * @returns {string} - HTML string
         */
        renderTripleView(formula, options = {}) {
            if (!formula) return '';
            const { graphHref = '#', showActions = true } = options;

            const arithma = formula.arithma_latex || '';
            const eml = this.getEmlLatex(formula);
            const hasArithma = !!arithma;
            const hasEml = !!eml;
            const mismatch = this.isMismatch(formula);

            // Determine grid mode
            let gridMode = '';
            if (!hasArithma && hasEml) gridMode = 'pm-triple-view--no-arithma';
            if (!hasArithma && !hasEml) gridMode = 'pm-triple-view--value-only';

            const formulaId = formula.id || formula.label || 'unknown';
            const status = formula.triple_status || (hasArithma && hasEml ? 'TRIPLE' : 'PARTIAL');
            const statusClass = mismatch
                ? 'pm-triple-status__badge--mismatch'
                : (status === 'TRIPLE' ? 'pm-triple-status__badge--triple' :
                   (status === 'PARTIAL' ? 'pm-triple-status__badge--missing' : ''));

            const b3Rooted = !!(formula.b3_rooted || formula.b3Rooted ||
                                (formula.derivation && formula.derivation.b3_rooted));

            // Status banner
            let bannerHtml = `<div class="pm-triple-status">
                <span class="pm-triple-status__item">
                    <strong>Formula:</strong> <code>${this.escapeHtml(formulaId)}</code>
                </span>
                <span class="pm-triple-status__item">
                    b<sub>3</sub>-rooted:
                    ${b3Rooted
                        ? '<span class="pm-triple-status__check">&#x2713;</span>'
                        : '<span class="pm-triple-status__cross">&#x2717;</span>'}
                </span>
                <span class="pm-triple-status__item">
                    status:
                    <span class="pm-triple-status__badge ${statusClass}">${this.escapeHtml(status)}</span>
                </span>
                ${mismatch ? '<span class="pm-triple-status__badge pm-triple-status__badge--mismatch" title="Arithma LaTeX and EML LaTeX disagree after normalization">MISMATCH</span>' : ''}
            </div>`;

            // Build the three panels
            const arithmaPanel = `
                <div class="pm-tv-panel pm-tv-panel--arithma">
                    <div class="pm-tv-panel__label">
                        <span>Arithma</span>
                        <span class="pm-tv-tag">LaTeX</span>
                    </div>
                    <div class="pm-tv-panel__body">
                        ${hasArithma ? `\\(${arithma}\\)` : '<div class="pm-tv-panel__empty">No Arithma rendering</div>'}
                    </div>
                </div>`;

            const emlPanel = `
                <div class="pm-tv-panel pm-tv-panel--eml">
                    <div class="pm-tv-panel__label">
                        <span>EML</span>
                        <span class="pm-tv-tag">LaTeX</span>
                    </div>
                    <div class="pm-tv-panel__body">
                        ${hasEml ? `\\(${eml}\\)` : '<div class="pm-tv-panel__empty">No EML rendering</div>'}
                    </div>
                </div>`;

            const valuePanel = `
                <div class="pm-tv-panel pm-tv-panel--value">
                    <div class="pm-tv-panel__label">
                        <span>Value</span>
                        <span class="pm-tv-tag">float</span>
                    </div>
                    <div class="pm-tv-panel__body">
                        ${this.formatValueBlock(formula)}
                    </div>
                </div>`;

            // Assemble grid
            let gridContent;
            if (!hasArithma && !hasEml) {
                gridContent = valuePanel;
            } else if (!hasArithma) {
                gridContent = emlPanel + valuePanel;
            } else {
                gridContent = arithmaPanel + emlPanel + valuePanel;
            }

            const tripleViewHtml = `
                ${bannerHtml}
                <div class="pm-triple-view ${gridMode}" data-formula-id="${this.escapeHtml(formulaId)}">
                    ${gridContent}
                </div>`;

            // Action row
            let actionsHtml = '';
            if (showActions) {
                const safeId = this.escapeHtml(formulaId);
                const safeGraph = this.escapeHtml(graphHref);
                actionsHtml = `
                    <div class="pm-card-actions">
                        <a class="pm-card-actions__btn pm-card-actions__btn--primary"
                           href="${safeGraph}"
                           data-pm-trace="${safeId}"
                           title="Open the dependency graph for this formula">
                            &#x21B3; Trace to b<sub>3</sub>
                        </a>
                        <button type="button" class="pm-card-actions__btn" data-pm-show-json="${safeId}">
                            Show JSON
                        </button>
                        <button type="button" class="pm-card-actions__btn" data-pm-show-alts="${safeId}">
                            Show alternatives
                        </button>
                    </div>
                    <pre class="pm-card-reveal" data-pm-reveal-json="${safeId}"></pre>
                    <div class="pm-card-reveal" data-pm-reveal-alts="${safeId}"></div>`;
            }

            return tripleViewHtml + actionsHtml;
        },

        /**
         * Wire up the action-row buttons for a container.
         * Idempotent - safe to call repeatedly after re-renders.
         * @param {HTMLElement|Document} root - element to scan for buttons
         * @param {Object} formulaIndex - { [id]: formulaRecord }
         */
        bindTripleViewActions(root, formulaIndex) {
            if (!root) root = document;
            if (!formulaIndex) formulaIndex = window.PM_FORMULAS || {};

            // Show JSON
            root.querySelectorAll('[data-pm-show-json]').forEach(btn => {
                if (btn.dataset.pmBound === '1') return;
                btn.dataset.pmBound = '1';
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    const id = btn.getAttribute('data-pm-show-json');
                    const target = root.querySelector(`[data-pm-reveal-json="${CSS.escape(id)}"]`);
                    if (!target) return;
                    if (target.classList.contains('open')) {
                        target.classList.remove('open');
                        return;
                    }
                    const f = formulaIndex[id] ||
                              (typeof window.findFormulaById === 'function' && window.findFormulaById(id));
                    target.textContent = JSON.stringify(f || { error: 'Not found', id }, null, 2);
                    target.classList.add('open');
                });
            });

            // Show alternatives (collapsed details: arithma_compact, eml_tree_str)
            root.querySelectorAll('[data-pm-show-alts]').forEach(btn => {
                if (btn.dataset.pmBound === '1') return;
                btn.dataset.pmBound = '1';
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    const id = btn.getAttribute('data-pm-show-alts');
                    const target = root.querySelector(`[data-pm-reveal-alts="${CSS.escape(id)}"]`);
                    if (!target) return;
                    if (target.classList.contains('open')) {
                        target.classList.remove('open');
                        return;
                    }
                    const f = formulaIndex[id] || {};
                    const lines = [];
                    if (f.arithma_compact) lines.push(`arithma_compact:\n${JSON.stringify(f.arithma_compact, null, 2)}`);
                    if (f.eml_tree_str) lines.push(`eml_tree_str:\n${f.eml_tree_str}`);
                    if (f.eml_tree_compact) lines.push(`eml_tree_compact:\n${JSON.stringify(f.eml_tree_compact, null, 2)}`);
                    if (f.plainText || f.plain_text) lines.push(`plain_text:\n${f.plainText || f.plain_text}`);
                    target.textContent = lines.length
                        ? lines.join('\n\n')
                        : 'No alternative representations on record.';
                    target.classList.add('open');
                });
            });

            // Trace to b3 - delegate to graph viewer if present, otherwise no-op
            root.querySelectorAll('[data-pm-trace]').forEach(btn => {
                if (btn.dataset.pmBound === '1') return;
                btn.dataset.pmBound = '1';
                btn.addEventListener('click', (e) => {
                    const id = btn.getAttribute('data-pm-trace');
                    if (typeof window.PMTraceToB3 === 'function') {
                        e.preventDefault();
                        window.PMTraceToB3(id);
                    }
                    // else: fall through to default href (S3.7 will wire up the page)
                });
            });
        },

        /**
         * Batch render formulas
         * Useful for rendering multiple formulas at once
         */
        renderBatch(formulas, options = {}) {
            const {
                containerSelector = '.formula-container',
                renderMode = 'interactive' // 'interactive', 'full', 'plain'
            } = options;

            const containers = document.querySelectorAll(containerSelector);

            formulas.forEach((formulaId, index) => {
                if (containers[index]) {
                    switch (renderMode) {
                        case 'full':
                            this.renderFull(formulaId, containers[index], options);
                            break;
                        case 'plain':
                            this.renderPlainText(formulaId, containers[index]);
                            break;
                        case 'interactive':
                        default:
                            this.renderInteractive(formulaId, containers[index], options);
                            break;
                    }
                }
            });
        }
    };

    // Export to global scope
    window.PMFormulaRenderer = PMFormulaRenderer;

    // Also export as module if in module context
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = PMFormulaRenderer;
    }

    console.log('[PM] Formula Renderer initialized');

})(typeof window !== 'undefined' ? window : global);
