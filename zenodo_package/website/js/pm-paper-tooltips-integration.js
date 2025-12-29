/**
 * PM Paper Tooltips - Integration Helpers
 * ========================================
 *
 * Enhances existing paper elements with tooltip-friendly classes and attributes.
 * Run after paper is rendered to add interactivity to existing content.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

(function() {
    'use strict';

    /**
     * Enhance the paper with tooltip-friendly elements
     */
    function enhancePaperForTooltips() {
        console.log('[PMTooltipsIntegration] Enhancing paper elements...');

        // Add equation reference links
        enhanceEquationReferences();

        // Mark parameter values
        enhanceParameterValues();

        // Add acronym classes
        enhanceAcronyms();

        // Add variable tooltips to formula terms
        enhanceFormulaVariables();

        console.log('[PMTooltipsIntegration] Enhancement complete');
    }

    /**
     * Convert equation references in text to clickable links
     */
    function enhanceEquationReferences() {
        // Find all text nodes in paper sections
        const paperSections = document.querySelectorAll('.paper-section, .paper-abstract, .section-abstract, .equation-discussion');

        paperSections.forEach(section => {
            const walker = document.createTreeWalker(
                section,
                NodeFilter.SHOW_TEXT,
                {
                    acceptNode: (node) => {
                        // Skip if parent is already a link or code
                        const parent = node.parentElement;
                        if (!parent || ['A', 'CODE', 'PRE', 'SCRIPT', 'STYLE'].includes(parent.tagName)) {
                            return NodeFilter.FILTER_REJECT;
                        }
                        // Check if text contains equation reference
                        if (/\b(?:Eq\.|equation|Equation)\s*\([0-9]+\.[0-9]+\)/i.test(node.textContent)) {
                            return NodeFilter.FILTER_ACCEPT;
                        }
                        return NodeFilter.FILTER_REJECT;
                    }
                }
            );

            const textNodes = [];
            let node;
            while (node = walker.nextNode()) {
                textNodes.push(node);
            }

            // Process each text node
            textNodes.forEach(textNode => {
                const text = textNode.textContent;
                const regex = /\b((?:Eq\.|equation|Equation)\s*\(([0-9]+\.[0-9]+)\))/gi;

                if (regex.test(text)) {
                    const fragment = document.createDocumentFragment();
                    let lastIndex = 0;
                    regex.lastIndex = 0;

                    let match;
                    while ((match = regex.exec(text)) !== null) {
                        // Add text before match
                        if (match.index > lastIndex) {
                            fragment.appendChild(document.createTextNode(text.substring(lastIndex, match.index)));
                        }

                        // Create link
                        const link = document.createElement('a');
                        link.href = `#eq-${match[2]}`;
                        link.className = 'equation-ref';
                        link.textContent = match[1];
                        link.title = `Jump to Equation ${match[2]}`;
                        fragment.appendChild(link);

                        lastIndex = match.index + match[0].length;
                    }

                    // Add remaining text
                    if (lastIndex < text.length) {
                        fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
                    }

                    // Replace text node with fragment
                    textNode.parentNode.replaceChild(fragment, textNode);
                }
            });
        });

        console.log('[PMTooltipsIntegration] Enhanced equation references');
    }

    /**
     * Add helper classes to parameter value elements
     */
    function enhanceParameterValues() {
        // Find all elements with data-pm-value
        const paramElements = document.querySelectorAll('[data-pm-value], [data-category][data-param]');

        paramElements.forEach(el => {
            if (!el.classList.contains('pm-value')) {
                el.classList.add('pm-value');
            }
        });

        console.log(`[PMTooltipsIntegration] Enhanced ${paramElements.length} parameter elements`);
    }

    /**
     * Identify and mark common acronyms
     */
    function enhanceAcronyms() {
        const acronyms = [
            'SM', 'GUT', 'SUSY', 'CKM', 'PMNS', 'QCD', 'QED', 'VEV', 'EW', 'KK',
            'PDG', 'LHC', 'HL-LHC', 'TeV', 'GeV', 'MeV', 'MSSM', 'SU', 'SO'
        ];

        const acronymPattern = new RegExp(`\\b(${acronyms.join('|')})\\b`, 'g');

        // Find text in paragraphs (avoid headers and code)
        const textContainers = document.querySelectorAll('p, li, td, .section-abstract, .equation-discussion');

        textContainers.forEach(container => {
            const walker = document.createTreeWalker(
                container,
                NodeFilter.SHOW_TEXT,
                {
                    acceptNode: (node) => {
                        const parent = node.parentElement;
                        if (!parent || ['A', 'CODE', 'PRE', 'SCRIPT', 'STYLE', 'ABBR'].includes(parent.tagName)) {
                            return NodeFilter.FILTER_REJECT;
                        }
                        if (acronymPattern.test(node.textContent)) {
                            return NodeFilter.FILTER_ACCEPT;
                        }
                        return NodeFilter.FILTER_REJECT;
                    }
                }
            );

            const textNodes = [];
            let node;
            while (node = walker.nextNode()) {
                textNodes.push(node);
            }

            textNodes.forEach(textNode => {
                const text = textNode.textContent;

                if (acronymPattern.test(text)) {
                    const fragment = document.createDocumentFragment();
                    let lastIndex = 0;
                    acronymPattern.lastIndex = 0;

                    let match;
                    while ((match = acronymPattern.exec(text)) !== null) {
                        // Add text before match
                        if (match.index > lastIndex) {
                            fragment.appendChild(document.createTextNode(text.substring(lastIndex, match.index)));
                        }

                        // Create abbr element
                        const abbr = document.createElement('abbr');
                        abbr.className = 'acronym';
                        abbr.textContent = match[1];
                        fragment.appendChild(abbr);

                        lastIndex = match.index + match[0].length;
                    }

                    // Add remaining text
                    if (lastIndex < text.length) {
                        fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
                    }

                    // Replace text node
                    textNode.parentNode.replaceChild(fragment, textNode);
                }
            });
        });

        console.log('[PMTooltipsIntegration] Enhanced acronyms');
    }

    /**
     * Add interactive variable tooltips to formula term definitions
     */
    function enhanceFormulaVariables() {
        // Find all term definition lists
        const termLists = document.querySelectorAll('.equation-terms, .pm-formula-terms');

        termLists.forEach(termList => {
            // Find all <i> tags (variables)
            const variables = termList.querySelectorAll('i');

            variables.forEach(varEl => {
                if (!varEl.classList.contains('tooltip-enabled')) {
                    varEl.classList.add('tooltip-enabled');
                    varEl.style.cursor = 'help';
                }
            });
        });

        console.log('[PMTooltipsIntegration] Enhanced formula variables');
    }

    /**
     * Auto-run when document is ready or immediately if already loaded
     */
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                // Wait a bit for paper to render
                setTimeout(enhancePaperForTooltips, 500);
            });
        } else {
            // Already loaded, wait for paper renderer
            setTimeout(enhancePaperForTooltips, 500);
        }
    }

    // Export API
    window.PMTooltipsIntegration = {
        enhance: enhancePaperForTooltips,
        enhanceEquationReferences,
        enhanceParameterValues,
        enhanceAcronyms,
        enhanceFormulaVariables
    };

    // Auto-initialize
    init();

    console.log('PMTooltipsIntegration: Loaded');

})();
