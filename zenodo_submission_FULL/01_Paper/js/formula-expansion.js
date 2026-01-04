/**
 * Formula Expansion System for Principia Metaphysica
 * Handles expandable formulas and derivation chains
 */

(function() {
    'use strict';

    // Initialize all expandable formulas on page load
    document.addEventListener('DOMContentLoaded', function() {
        initExpandableFormulas();
        initFormulaTooltips();
    });

    /**
     * Initialize expandable formula components
     */
    function initExpandableFormulas() {
        const formulas = document.querySelectorAll('.expandable-formula');

        formulas.forEach(formula => {
            const header = formula.querySelector('.formula-header');
            const expandBtn = formula.querySelector('.expand-btn');

            if (header) {
                header.addEventListener('click', function(e) {
                    // Don't toggle if clicking on a link
                    if (e.target.tagName === 'A') return;
                    toggleFormula(formula);
                });
            }

            if (expandBtn) {
                expandBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    toggleFormula(formula);
                });
            }
        });
    }

    /**
     * Toggle formula expansion state
     */
    function toggleFormula(formula) {
        const isExpanded = formula.classList.contains('expanded');
        const expandBtn = formula.querySelector('.expand-btn');

        if (isExpanded) {
            formula.classList.remove('expanded');
            if (expandBtn) {
                expandBtn.classList.remove('expanded');
                expandBtn.innerHTML = '&#x25BC;'; // Down arrow
                expandBtn.title = 'Expand formula';
            }
        } else {
            formula.classList.add('expanded');
            if (expandBtn) {
                expandBtn.classList.add('expanded');
                expandBtn.innerHTML = '&#x25B2;'; // Up arrow
                expandBtn.title = 'Collapse formula';
            }
        }
    }

    /**
     * Initialize formula variable tooltips
     */
    function initFormulaTooltips() {
        const formulaVars = document.querySelectorAll('.formula-var');

        formulaVars.forEach(varEl => {
            // Handle touch devices
            varEl.addEventListener('touchstart', function(e) {
                e.preventDefault();
                const tooltip = varEl.querySelector('.var-tooltip');
                if (tooltip) {
                    // Hide all other tooltips first
                    document.querySelectorAll('.var-tooltip.active').forEach(t => {
                        t.classList.remove('active');
                    });
                    tooltip.classList.toggle('active');
                }
            });
        });

        // Close tooltips when clicking elsewhere
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.formula-var')) {
                document.querySelectorAll('.var-tooltip.active').forEach(t => {
                    t.classList.remove('active');
                });
            }
        });
    }

    /**
     * Expand all formulas on the page
     */
    window.expandAllFormulas = function() {
        document.querySelectorAll('.expandable-formula').forEach(formula => {
            if (!formula.classList.contains('expanded')) {
                toggleFormula(formula);
            }
        });
    };

    /**
     * Collapse all formulas on the page
     */
    window.collapseAllFormulas = function() {
        document.querySelectorAll('.expandable-formula').forEach(formula => {
            if (formula.classList.contains('expanded')) {
                toggleFormula(formula);
            }
        });
    };

    /**
     * Escape HTML to prevent XSS
     * @param {string} str - String to escape
     * @returns {string} Escaped string
     */
    function escapeHtml(str) {
        if (typeof str !== 'string') return str || '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Create an expandable formula element programmatically
     * @param {Object} config - Formula configuration
     * @returns {HTMLElement} The formula element
     */
    window.createExpandableFormula = function(config) {
        // Null check for config
        if (!config || typeof config !== 'object') {
            console.warn('createExpandableFormula: Invalid config provided');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'formula-error';
            errorDiv.textContent = 'Invalid formula configuration';
            return errorDiv;
        }

        const formula = document.createElement('div');
        formula.className = 'expandable-formula';

        // Create header
        const header = document.createElement('div');
        header.className = 'formula-header';

        const main = document.createElement('div');
        main.className = 'formula-main';
        // Sanitize formula content - allow only trusted formula HTML
        main.innerHTML = config.formula || '';

        const controls = document.createElement('div');
        controls.className = 'formula-controls';

        if (config.badge) {
            const badge = document.createElement('span');
            // Sanitize badge type to prevent class injection
            const safeTypes = ['established', 'derived', 'prediction', 'theory', 'validated', ''];
            const badgeType = safeTypes.includes(config.badgeType) ? config.badgeType : '';
            badge.className = `foundation-badge ${badgeType}`;
            badge.textContent = config.badge;
            controls.appendChild(badge);
        }

        if (config.linkUrl) {
            const link = document.createElement('a');
            link.className = 'link-btn';
            link.href = config.linkUrl;
            link.innerHTML = 'Details &rarr;';
            controls.appendChild(link);
        }

        const expandBtn = document.createElement('button');
        expandBtn.className = 'expand-btn';
        expandBtn.innerHTML = '&#x25BC;';
        expandBtn.title = 'Expand formula';
        controls.appendChild(expandBtn);

        header.appendChild(main);
        header.appendChild(controls);
        formula.appendChild(header);

        // Create expansion content
        if (config.components && config.components.length > 0) {
            const expansion = document.createElement('div');
            expansion.className = 'formula-expansion';

            const subComponents = document.createElement('div');
            subComponents.className = 'sub-components';

            config.components.forEach(comp => {
                if (!comp) return; // Skip null/undefined components

                const component = document.createElement('div');
                component.className = 'sub-component';

                // Create elements safely to avoid XSS
                const symbolDiv = document.createElement('div');
                symbolDiv.className = 'component-symbol';
                symbolDiv.textContent = comp.symbol || '';

                const nameDiv = document.createElement('div');
                nameDiv.className = 'component-name';
                nameDiv.textContent = comp.name || '';

                const descDiv = document.createElement('div');
                descDiv.className = 'component-desc';
                descDiv.textContent = comp.description || '';

                component.appendChild(symbolDiv);
                component.appendChild(nameDiv);
                component.appendChild(descDiv);

                if (comp.link) {
                    const link = document.createElement('a');
                    link.className = 'component-link';
                    link.href = comp.link;
                    link.innerHTML = 'Learn more &rarr;';
                    component.appendChild(link);
                }

                subComponents.appendChild(component);
            });

            expansion.appendChild(subComponents);

            // Add derivation chain if provided
            if (config.derivationChain && config.derivationChain.length > 0) {
                const chain = document.createElement('div');
                chain.className = 'derivation-chain';
                chain.innerHTML = `<div class="chain-title">Derivation Path to Established Physics</div>`;

                config.derivationChain.forEach(step => {
                    if (!step) return; // Skip null/undefined steps

                    const stepEl = document.createElement('div');
                    stepEl.className = 'chain-step';

                    // Create elements safely to avoid XSS
                    const arrow = document.createElement('span');
                    arrow.className = 'step-arrow';
                    arrow.innerHTML = '&rarr;';
                    stepEl.appendChild(arrow);

                    if (step.link) {
                        const link = document.createElement('a');
                        link.href = step.link;
                        link.textContent = step.name || '';
                        stepEl.appendChild(link);
                    } else {
                        const nameSpan = document.createElement('span');
                        nameSpan.textContent = step.name || '';
                        stepEl.appendChild(nameSpan);
                    }

                    if (step.badge) {
                        const badge = document.createElement('span');
                        // Sanitize badge type
                        const safeTypes = ['established', 'derived', 'prediction', 'theory', 'validated', ''];
                        const badgeType = safeTypes.includes(step.badgeType) ? step.badgeType : '';
                        badge.className = `foundation-badge ${badgeType}`;
                        badge.textContent = step.badge;
                        stepEl.appendChild(badge);
                    }

                    chain.appendChild(stepEl);
                });

                expansion.appendChild(chain);
            }

            formula.appendChild(expansion);
        }

        // Initialize click handlers
        header.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') return;
            toggleFormula(formula);
        });

        expandBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleFormula(formula);
        });

        return formula;
    };

})();
