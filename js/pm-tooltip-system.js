/**
 * Principia Metaphysica - Tooltip System
 * =======================================
 *
 * Automatically populates .pm-value elements with theory constants
 * and enables hover tooltips showing formula, derivation, uncertainty.
 *
 * Usage in HTML:
 * <span class="pm-value"
 *       data-category="proton_decay"
 *       data-param="tau_p_median"
 *       data-format="scientific:2"></span>
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

(function() {
    'use strict';

    // Wait for DOM and PM constants to load
    if (typeof PM === 'undefined') {
        console.error('PM constants not loaded! Include theory-constants-enhanced.js before pm-tooltip-system.js');
        return;
    }

    /**
     * Format a value according to specified format
     */
    function formatValue(value, format) {
        if (!format) {
            return value.toString();
        }

        const [type, precision] = format.split(':');
        const prec = parseInt(precision) || 2;

        switch(type) {
            case 'scientific':
                return value.toExponential(prec);
            case 'fixed':
                return value.toFixed(prec);
            case 'percent':
                return (value * 100).toFixed(prec) + '%';
            case 'display':
                return value; // Use pre-formatted display string
            default:
                return value.toString();
        }
    }

    /**
     * Populate all .pm-value elements with their values
     */
    function setupPMValues() {
        const elements = document.querySelectorAll('.pm-value');

        elements.forEach(el => {
            const category = el.dataset.category;
            const param = el.dataset.param;
            const format = el.dataset.format;

            if (!category || !param) {
                console.warn('Missing data-category or data-param on element:', el);
                return;
            }

            if (!PM[category]) {
                console.warn(`Category "${category}" not found in PM constants`);
                return;
            }

            const obj = PM[category][param];
            if (!obj) {
                console.warn(`Parameter "${param}" not found in PM.${category}`);
                return;
            }

            // Use display string if available, otherwise format value
            let displayValue;
            if (format === 'display' && obj.display) {
                displayValue = obj.display;
            } else {
                displayValue = formatValue(obj.value, format);
            }

            // Set the text content
            el.textContent = displayValue;

            // Add unit if specified and not already in display
            if (obj.unit && !el.dataset.noUnit && format !== 'display') {
                el.textContent += ' ' + obj.unit;
            }

            // Store object reference for tooltip
            el._pmObject = obj;
        });

        console.log(`[PM] Populated ${elements.length} constant values`);
    }

    /**
     * Create and show tooltip
     */
    function showTooltip(event, obj) {
        // Remove any existing tooltips
        removeTooltip();

        const tooltip = document.createElement('div');
        tooltip.className = 'pm-tooltip-popup';
        tooltip.innerHTML = PM.getTooltip(obj);

        // Position tooltip near cursor
        tooltip.style.position = 'absolute';
        tooltip.style.left = event.pageX + 10 + 'px';
        tooltip.style.top = event.pageY + 10 + 'px';
        tooltip.style.zIndex = '10000';

        document.body.appendChild(tooltip);
    }

    /**
     * Remove tooltip
     */
    function removeTooltip() {
        const existing = document.querySelector('.pm-tooltip-popup');
        if (existing) {
            existing.remove();
        }
    }

    /**
     * Setup hover listeners
     */
    function setupHoverListeners() {
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('pm-value') && e.target._pmObject) {
                showTooltip(e, e.target._pmObject);
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('pm-value')) {
                removeTooltip();
            }
        });

        // Update tooltip position on mouse move
        document.addEventListener('mousemove', (e) => {
            const tooltip = document.querySelector('.pm-tooltip-popup');
            if (tooltip) {
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY + 10 + 'px';
            }
        });
    }

    /**
     * Modified PM.getTooltip to work with object directly
     */
    PM.getTooltip = (obj) => {
        let tooltip = `<div class="pm-tooltip-content">`;

        // Value and unit
        tooltip += `<div class="pm-tooltip-value"><strong>${obj.display || obj.value}</strong>`;
        if (obj.unit) {
            tooltip += ` ${obj.unit}`;
        }
        tooltip += `</div>`;

        // Description
        if (obj.description) {
            tooltip += `<div class="pm-tooltip-desc">${obj.description}</div>`;
        }

        // Formula
        if (obj.formula) {
            tooltip += `<div class="pm-tooltip-formula"><em>Formula:</em> ${obj.formula}</div>`;
        }

        // Derivation
        if (obj.derivation) {
            tooltip += `<div class="pm-tooltip-derivation"><em>Derivation:</em> ${obj.derivation}</div>`;
        }

        // Uncertainty
        if (obj.uncertainty !== undefined || obj.uncertainty_oom !== undefined) {
            const unc = obj.uncertainty_oom !== undefined
                ? `±${obj.uncertainty_oom.toFixed(2)} OOM`
                : obj.uncertainty_lower && obj.uncertainty_upper
                    ? `${obj.confidence_level || '68%'} CI: [${obj.uncertainty_lower.toExponential(2)}-${obj.uncertainty_upper.toExponential(2)}]`
                    : `±${obj.uncertainty}`;
            tooltip += `<div class="pm-tooltip-uncertainty"><em>Uncertainty:</em> ${unc}</div>`;
        }

        // Experimental comparison
        if (obj.experimental_value !== undefined) {
            tooltip += `<div class="pm-tooltip-experiment">`;
            tooltip += `<em>Experiment:</em> ${obj.experimental_value}`;
            if (obj.experimental_uncertainty) {
                tooltip += ` ± ${obj.experimental_uncertainty}`;
            }
            if (obj.experimental_source) {
                tooltip += ` (${obj.experimental_source})`;
            }
            tooltip += `</div>`;
        }

        // Agreement
        if (obj.agreement_sigma !== undefined || obj.agreement || obj.agreement_text) {
            const sigma = obj.agreement_sigma || 0;
            const color = sigma < 1 ? '#4caf50' : sigma < 3 ? '#ff9800' : '#f44336';
            tooltip += `<div class="pm-tooltip-agreement" style="color:${color}">`;
            tooltip += `<em>Agreement:</em> ${obj.agreement_text || obj.agreement || `${sigma.toFixed(2)}σ`}`;
            tooltip += `</div>`;
        }

        // Testability
        if (obj.testable) {
            tooltip += `<div class="pm-tooltip-testable"><em>Testable:</em> ${obj.testable}</div>`;
        }

        // Source
        if (obj.source) {
            tooltip += `<div class="pm-tooltip-source"><em>Source:</em> <code>${obj.source}</code></div>`;
        }

        // References
        if (obj.references && obj.references.length > 0) {
            tooltip += `<div class="pm-tooltip-refs"><em>References:</em> ${obj.references.join(', ')}</div>`;
        }

        tooltip += `</div>`;
        return tooltip;
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setupPMValues();
            setupHoverListeners();
        });
    } else {
        setupPMValues();
        setupHoverListeners();
    }

    console.log('[PM] Tooltip system initialized');

})();
