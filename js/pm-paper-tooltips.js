/**
 * PM Paper Tooltips - Advanced Tooltip System
 * ============================================
 *
 * Comprehensive tooltip system for the paper renderer:
 * - Formula variables with term definitions
 * - Parameters with values, units, uncertainty, source
 * - Formula references with previews
 * - Citations with reference details
 * - Acronyms with expansions
 * - Smart positioning (viewport-aware)
 * - Mobile-friendly (tap to show)
 * - Collapsible derivations
 * - Copy to clipboard
 * - LaTeX/plain text toggle
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 * Version: 1.0.0
 */

(function() {
    'use strict';

    // ========================================================================
    // TOOLTIP STATE
    // ========================================================================

    const TooltipState = {
        currentTooltip: null,
        currentTarget: null,
        hideTimeout: null,
        showTimeout: null,
        isMobile: window.matchMedia('(hover: none) and (pointer: coarse)').matches,
        formulasCache: null,
        parametersCache: null
    };

    // Configuration
    const CONFIG = {
        SHOW_DELAY: 200,      // ms before showing tooltip on hover
        HIDE_DELAY: 100,      // ms before hiding tooltip
        OFFSET_X: 12,         // px from cursor
        OFFSET_Y: 12,         // px from cursor
        MAX_WIDTH: 500,       // max tooltip width
        VIEWPORT_MARGIN: 20   // px margin from viewport edge
    };

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    /**
     * Initialize the tooltip system
     */
    function init() {
        console.log('[PMPaperTooltips] Initializing...');

        // Create tooltip container
        createTooltipContainer();

        // Wait for data to load
        if (window.PMPaperRenderer && window.PMPaperRenderer.loaded) {
            setupTooltips();
        } else {
            // Poll for data
            const checkInterval = setInterval(() => {
                if (window.PMPaperRenderer && window.PMPaperRenderer.loaded) {
                    clearInterval(checkInterval);
                    setupTooltips();
                }
            }, 100);

            // Give up after 10 seconds
            setTimeout(() => clearInterval(checkInterval), 10000);
        }

        console.log('[PMPaperTooltips] Initialized');
    }

    /**
     * Create tooltip DOM container
     */
    function createTooltipContainer() {
        let container = document.getElementById('pm-paper-tooltip');
        if (container) return;

        container = document.createElement('div');
        container.id = 'pm-paper-tooltip';
        container.className = 'pm-paper-tooltip';
        container.style.display = 'none';
        document.body.appendChild(container);
    }

    /**
     * Setup all tooltip listeners
     */
    function setupTooltips() {
        // Load data caches
        loadDataCaches();

        // Setup listeners for different tooltip types
        setupFormulaVariableTooltips();
        setupParameterTooltips();
        setupFormulaReferenceTooltips();
        setupCitationTooltips();
        setupAcronymTooltips();

        // Setup interactive features
        setupCollapsibleDerivations();
        setupCopyToClipboard();
        setupLatexToggle();

        console.log('[PMPaperTooltips] All tooltip handlers ready');
    }

    /**
     * Load formula and parameter data into cache
     */
    function loadDataCaches() {
        // Load from PM globals
        if (window.PM_FORMULAS) {
            TooltipState.formulasCache = window.PM_FORMULAS;
        } else if (window.PMPaperRenderer && window.PMPaperRenderer.data) {
            TooltipState.formulasCache = window.PMPaperRenderer.data.formulas?.formulas || {};
        }

        if (window.PM && window.PM._data) {
            TooltipState.parametersCache = window.PM._data.parameters || {};
        } else if (window.PMPaperRenderer && window.PMPaperRenderer.data) {
            TooltipState.parametersCache = window.PMPaperRenderer.data.parameters || {};
        }

        console.log(`[PMPaperTooltips] Cached ${Object.keys(TooltipState.formulasCache || {}).length} formulas, ${Object.keys(TooltipState.parametersCache || {}).length} parameters`);
    }

    // ========================================================================
    // FORMULA VARIABLE TOOLTIPS
    // ========================================================================

    /**
     * Setup tooltips for formula variables (from terms dict)
     */
    function setupFormulaVariableTooltips() {
        // Find all <i> tags within equations that represent variables
        document.addEventListener('mouseover', (e) => {
            const target = e.target;

            // Check if target is within an equation and is an <i> tag or MathJax element
            if (isInEquation(target) && (target.tagName === 'I' || target.classList.contains('MJX-tex'))) {
                const variable = target.textContent.trim();
                const formulaElement = target.closest('[data-formula-id], .equation-wrapper');

                if (formulaElement) {
                    const formulaId = formulaElement.getAttribute('data-formula-id') ||
                                    formulaElement.id?.replace('eq-', '');
                    showVariableTooltip(e, variable, formulaId);
                }
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (isInEquation(e.target)) {
                scheduleHide();
            }
        });
    }

    /**
     * Show tooltip for a formula variable
     */
    function showVariableTooltip(event, variable, formulaId) {
        const formula = TooltipState.formulasCache?.[formulaId];
        if (!formula || !formula.terms) return;

        const termData = formula.terms[variable];
        if (!termData) return;

        const content = `
            <div class="tooltip-header">
                <span class="tooltip-variable">${variable}</span>
            </div>
            <div class="tooltip-body">
                <div class="tooltip-description">${termData.description || termData.name || ''}</div>
                ${termData.value ? `<div class="tooltip-value">Value: <strong>${termData.value}</strong></div>` : ''}
                ${termData.units ? `<div class="tooltip-units">Units: ${termData.units}</div>` : ''}
                ${termData.param_id ? `<div class="tooltip-param-link">Parameter: <code>${termData.param_id}</code></div>` : ''}
                ${termData.link ? `<div class="tooltip-link"><a href="${termData.link}" target="_blank">Learn more →</a></div>` : ''}
            </div>
        `;

        showTooltip(event, content, 'variable');
    }

    // ========================================================================
    // PARAMETER TOOLTIPS
    // ========================================================================

    /**
     * Setup tooltips for parameter references
     */
    function setupParameterTooltips() {
        document.addEventListener('mouseover', (e) => {
            const target = e.target;

            // Check for parameter elements
            if (target.hasAttribute('data-pm-value') ||
                (target.hasAttribute('data-category') && target.hasAttribute('data-param'))) {
                showParameterTooltip(e, target);
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.hasAttribute('data-pm-value') ||
                (e.target.hasAttribute('data-category') && e.target.hasAttribute('data-param'))) {
                scheduleHide();
            }
        });
    }

    /**
     * Show tooltip for a parameter
     */
    function showParameterTooltip(event, element) {
        const path = element.getAttribute('data-pm-value') ||
                    `${element.getAttribute('data-category')}.${element.getAttribute('data-param')}`;

        // Get parameter data
        const paramData = getParameterData(path);
        if (!paramData) return;

        const value = paramData.value !== undefined ? paramData.value : element.textContent;
        const units = paramData.metadata?.units || paramData.units || '';
        const uncertainty = paramData.uncertainty;
        const source = paramData.source || '';
        const description = paramData.metadata?.description || paramData.description || '';

        const content = `
            <div class="tooltip-header">
                <span class="tooltip-param-name">${path.split('.').pop()}</span>
            </div>
            <div class="tooltip-body">
                ${description ? `<div class="tooltip-description">${description}</div>` : ''}
                <div class="tooltip-value-row">
                    <strong>${formatValue(value)}</strong>
                    ${units ? `<span class="tooltip-units">${units}</span>` : ''}
                </div>
                ${uncertainty ? `
                    <div class="tooltip-uncertainty">
                        <span class="tooltip-label">Uncertainty:</span>
                        ±${formatValue(uncertainty)}
                    </div>
                ` : ''}
                ${source ? `
                    <div class="tooltip-source">
                        <span class="tooltip-label">Source:</span>
                        <code>${source}</code>
                    </div>
                ` : ''}
                ${paramData.status ? `
                    <div class="tooltip-status status-${paramData.status.toLowerCase()}">
                        ${paramData.status}
                    </div>
                ` : ''}
            </div>
        `;

        showTooltip(event, content, 'parameter');
    }

    /**
     * Get parameter data from cache
     */
    function getParameterData(path) {
        if (!TooltipState.parametersCache) return null;

        // Try direct path first
        if (TooltipState.parametersCache[path]) {
            return TooltipState.parametersCache[path];
        }

        // Try alternative paths
        const parts = path.split('.');
        let current = TooltipState.parametersCache;
        for (const part of parts) {
            if (current && typeof current === 'object' && part in current) {
                current = current[part];
            } else {
                return null;
            }
        }

        return current;
    }

    // ========================================================================
    // FORMULA REFERENCE TOOLTIPS
    // ========================================================================

    /**
     * Setup tooltips for formula references (Eq. X.X links)
     */
    function setupFormulaReferenceTooltips() {
        document.addEventListener('mouseover', (e) => {
            const target = e.target;

            if (target.classList.contains('equation-ref') ||
                (target.tagName === 'A' && target.href.includes('#eq-'))) {
                showFormulaReferenceTooltip(e, target);
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('equation-ref') ||
                (e.target.tagName === 'A' && e.target.href.includes('#eq-'))) {
                scheduleHide();
            }
        });
    }

    /**
     * Show preview tooltip for formula reference
     */
    function showFormulaReferenceTooltip(event, element) {
        const href = element.getAttribute('href');
        const eqId = href.replace('#eq-', '');

        // Find the formula
        const formulaElement = document.getElementById(`eq-${eqId}`);
        if (!formulaElement) return;

        // Extract formula info
        const latexElement = formulaElement.querySelector('.equation-content');
        const numberElement = formulaElement.querySelector('.equation-number');

        const latex = latexElement ? latexElement.textContent : '';
        const number = numberElement ? numberElement.textContent : eqId;

        const content = `
            <div class="tooltip-header">
                <span class="tooltip-equation-number">Equation ${number}</span>
            </div>
            <div class="tooltip-body">
                <div class="tooltip-equation-preview">
                    ${latex}
                </div>
                <div class="tooltip-action">
                    <small>Click to jump to equation</small>
                </div>
            </div>
        `;

        showTooltip(event, content, 'formula-ref');
    }

    // ========================================================================
    // CITATION TOOLTIPS
    // ========================================================================

    /**
     * Setup tooltips for citations
     */
    function setupCitationTooltips() {
        document.addEventListener('mouseover', (e) => {
            const target = e.target;

            if (target.classList.contains('citation') ||
                target.classList.contains('pm-citation') ||
                (target.tagName === 'CITE')) {
                showCitationTooltip(e, target);
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('citation') ||
                e.target.classList.contains('pm-citation') ||
                (e.target.tagName === 'CITE')) {
                scheduleHide();
            }
        });
    }

    /**
     * Show tooltip for citation
     */
    function showCitationTooltip(event, element) {
        const citationKey = element.getAttribute('data-citation') ||
                          element.getAttribute('data-ref') ||
                          element.textContent.trim();

        // TODO: Load from bibliography data
        const content = `
            <div class="tooltip-header">
                <span class="tooltip-citation-key">${citationKey}</span>
            </div>
            <div class="tooltip-body">
                <div class="tooltip-description">
                    Citation details for ${citationKey}
                </div>
                <div class="tooltip-action">
                    <small>Click to view in references</small>
                </div>
            </div>
        `;

        showTooltip(event, content, 'citation');
    }

    // ========================================================================
    // ACRONYM TOOLTIPS
    // ========================================================================

    /**
     * Setup tooltips for acronyms
     */
    function setupAcronymTooltips() {
        const acronyms = {
            'SM': 'Standard Model',
            'GUT': 'Grand Unified Theory',
            'SUSY': 'Supersymmetry',
            'CKM': 'Cabibbo-Kobayashi-Maskawa',
            'PMNS': 'Pontecorvo-Maki-Nakagawa-Sakata',
            'QCD': 'Quantum Chromodynamics',
            'QED': 'Quantum Electrodynamics',
            'VEV': 'Vacuum Expectation Value',
            'EW': 'Electroweak',
            'KK': 'Kaluza-Klein',
            'PDG': 'Particle Data Group',
            'LHC': 'Large Hadron Collider',
            'HL-LHC': 'High-Luminosity Large Hadron Collider'
        };

        document.addEventListener('mouseover', (e) => {
            const target = e.target;

            if (target.classList.contains('acronym') || target.tagName === 'ABBR') {
                const acronym = target.textContent.trim();
                if (acronyms[acronym]) {
                    showAcronymTooltip(e, acronym, acronyms[acronym]);
                }
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('acronym') || e.target.tagName === 'ABBR') {
                scheduleHide();
            }
        });
    }

    /**
     * Show tooltip for acronym
     */
    function showAcronymTooltip(event, acronym, expansion) {
        const content = `
            <div class="tooltip-header">
                <span class="tooltip-acronym">${acronym}</span>
            </div>
            <div class="tooltip-body">
                <div class="tooltip-expansion">${expansion}</div>
            </div>
        `;

        showTooltip(event, content, 'acronym');
    }

    // ========================================================================
    // INTERACTIVE FEATURES
    // ========================================================================

    /**
     * Setup collapsible derivations
     */
    function setupCollapsibleDerivations() {
        // Already handled by pm-paper-renderer.js expand buttons
        // Just add smooth transitions
        const style = document.createElement('style');
        style.textContent = `
            .pm-formula-details {
                transition: max-height 0.3s ease, opacity 0.3s ease;
                overflow: hidden;
            }
            .pm-formula-card:not(.expanded) .pm-formula-details {
                max-height: 0;
                opacity: 0;
            }
            .pm-formula-card.expanded .pm-formula-details {
                max-height: 1000px;
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Setup copy to clipboard functionality
     */
    function setupCopyToClipboard() {
        // Add copy buttons to equations
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('copy-equation-btn')) {
                const equation = e.target.closest('.equation-wrapper, .pm-formula-card');
                const latex = equation.querySelector('.pm-formula-latex, .equation-content')?.textContent;

                if (latex) {
                    copyToClipboard(latex);
                    showCopyFeedback(e.target);
                }
            }
        });

        // Add copy buttons to formula cards
        const formulaCards = document.querySelectorAll('.pm-formula-card');
        formulaCards.forEach(card => {
            if (!card.querySelector('.copy-equation-btn')) {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-equation-btn';
                copyBtn.innerHTML = '📋 Copy LaTeX';
                copyBtn.title = 'Copy LaTeX to clipboard';

                const header = card.querySelector('.pm-formula-header');
                if (header) {
                    header.appendChild(copyBtn);
                }
            }
        });

        // Add copy buttons to equation wrappers
        const equations = document.querySelectorAll('.equation-wrapper');
        equations.forEach(eq => {
            if (!eq.querySelector('.copy-equation-btn')) {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-equation-btn equation-copy-btn';
                copyBtn.innerHTML = '📋';
                copyBtn.title = 'Copy LaTeX';
                eq.appendChild(copyBtn);
            }
        });
    }

    /**
     * Copy text to clipboard
     */
    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).catch(err => {
                console.error('Failed to copy:', err);
            });
        } else {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
        }
    }

    /**
     * Show feedback when copy succeeds
     */
    function showCopyFeedback(button) {
        const original = button.innerHTML;
        button.innerHTML = '✓ Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.innerHTML = original;
            button.classList.remove('copied');
        }, 2000);
    }

    /**
     * Setup LaTeX/plain text toggle
     */
    function setupLatexToggle() {
        // Add toggle buttons to formula cards
        const formulaCards = document.querySelectorAll('.pm-formula-card');
        formulaCards.forEach(card => {
            const plainText = card.querySelector('.pm-plaintext-code')?.textContent;
            if (!plainText) return;

            if (!card.querySelector('.latex-toggle-btn')) {
                const toggleBtn = document.createElement('button');
                toggleBtn.className = 'latex-toggle-btn';
                toggleBtn.innerHTML = 'Show Plain Text';
                toggleBtn.title = 'Toggle between LaTeX and plain text';

                toggleBtn.addEventListener('click', () => {
                    card.classList.toggle('show-plaintext');
                    toggleBtn.innerHTML = card.classList.contains('show-plaintext') ?
                        'Show LaTeX' : 'Show Plain Text';
                });

                const header = card.querySelector('.pm-formula-header');
                if (header) {
                    header.appendChild(toggleBtn);
                }
            }
        });
    }

    // ========================================================================
    // TOOLTIP DISPLAY & POSITIONING
    // ========================================================================

    /**
     * Show tooltip with smart positioning
     */
    function showTooltip(event, content, type = 'default') {
        clearTimeout(TooltipState.showTimeout);
        clearTimeout(TooltipState.hideTimeout);

        TooltipState.showTimeout = setTimeout(() => {
            const tooltip = document.getElementById('pm-paper-tooltip');
            if (!tooltip) return;

            tooltip.innerHTML = content;
            tooltip.className = `pm-paper-tooltip pm-tooltip-${type}`;
            tooltip.style.display = 'block';

            // Position tooltip
            positionTooltip(tooltip, event);

            // Store current state
            TooltipState.currentTooltip = tooltip;
            TooltipState.currentTarget = event.target;

            // Trigger MathJax if needed
            if (content.includes('$$') || content.includes('\\(')) {
                if (window.MathJax && window.MathJax.typesetPromise) {
                    window.MathJax.typesetPromise([tooltip]).catch(err => {
                        console.warn('MathJax failed in tooltip:', err);
                    });
                }
            }
        }, CONFIG.SHOW_DELAY);
    }

    /**
     * Position tooltip with smart viewport detection
     */
    function positionTooltip(tooltip, event) {
        const viewport = {
            width: window.innerWidth,
            height: window.innerHeight,
            scrollX: window.pageXOffset,
            scrollY: window.pageYOffset
        };

        let x = event.pageX + CONFIG.OFFSET_X;
        let y = event.pageY + CONFIG.OFFSET_Y;

        // Get tooltip dimensions (may not be accurate until rendered)
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';

        // Wait for next frame to get accurate dimensions
        requestAnimationFrame(() => {
            const rect = tooltip.getBoundingClientRect();

            // Check right edge
            if (x + rect.width > viewport.scrollX + viewport.width - CONFIG.VIEWPORT_MARGIN) {
                x = event.pageX - rect.width - CONFIG.OFFSET_X;
            }

            // Check bottom edge
            if (y + rect.height > viewport.scrollY + viewport.height - CONFIG.VIEWPORT_MARGIN) {
                y = event.pageY - rect.height - CONFIG.OFFSET_Y;
            }

            // Check left edge
            if (x < viewport.scrollX + CONFIG.VIEWPORT_MARGIN) {
                x = viewport.scrollX + CONFIG.VIEWPORT_MARGIN;
            }

            // Check top edge
            if (y < viewport.scrollY + CONFIG.VIEWPORT_MARGIN) {
                y = viewport.scrollY + CONFIG.VIEWPORT_MARGIN;
            }

            tooltip.style.left = x + 'px';
            tooltip.style.top = y + 'px';
        });
    }

    /**
     * Schedule tooltip hide
     */
    function scheduleHide() {
        clearTimeout(TooltipState.showTimeout);
        clearTimeout(TooltipState.hideTimeout);

        TooltipState.hideTimeout = setTimeout(() => {
            hideTooltip();
        }, CONFIG.HIDE_DELAY);
    }

    /**
     * Hide tooltip
     */
    function hideTooltip() {
        const tooltip = document.getElementById('pm-paper-tooltip');
        if (tooltip) {
            tooltip.style.display = 'none';
            tooltip.innerHTML = '';
        }

        TooltipState.currentTooltip = null;
        TooltipState.currentTarget = null;
    }

    // ========================================================================
    // MOBILE SUPPORT
    // ========================================================================

    /**
     * Setup mobile tap handlers
     */
    if (TooltipState.isMobile) {
        document.addEventListener('touchstart', (e) => {
            // Check if tapped element should show tooltip
            const target = e.target;

            if (target.hasAttribute('data-pm-value') ||
                target.classList.contains('equation-ref') ||
                target.classList.contains('acronym')) {

                e.preventDefault();

                // If tooltip already showing for this element, hide it
                if (TooltipState.currentTarget === target) {
                    hideTooltip();
                } else {
                    // Show tooltip for new element
                    const syntheticEvent = {
                        target: target,
                        pageX: e.touches[0].pageX,
                        pageY: e.touches[0].pageY
                    };

                    if (target.hasAttribute('data-pm-value')) {
                        showParameterTooltip(syntheticEvent, target);
                    } else if (target.classList.contains('equation-ref')) {
                        showFormulaReferenceTooltip(syntheticEvent, target);
                    } else if (target.classList.contains('acronym') || target.tagName === 'ABBR') {
                        showCitationTooltip(syntheticEvent, target);
                    }
                }
            } else {
                // Tapped elsewhere - hide tooltip
                hideTooltip();
            }
        });
    }

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================

    /**
     * Check if element is within an equation
     */
    function isInEquation(element) {
        return element.closest('.equation-wrapper, .pm-formula-card, .MathJax, .equation-content') !== null;
    }

    /**
     * Format value for display
     */
    function formatValue(value) {
        if (value === null || value === undefined) return '?';
        if (typeof value === 'number') {
            if (Math.abs(value) >= 1e10 || (Math.abs(value) < 0.001 && value !== 0)) {
                return value.toExponential(3);
            } else if (Number.isInteger(value)) {
                return value.toString();
            } else {
                return value.toFixed(4);
            }
        }
        return String(value);
    }

    // ========================================================================
    // PUBLIC API
    // ========================================================================

    const API = {
        init,
        showTooltip,
        hideTooltip,
        scheduleHide,
        config: CONFIG,
        state: TooltipState
    };

    // Export globally
    window.PMPaperTooltips = API;

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    console.log('PMPaperTooltips: Loaded (v1.0.0)');

})();
