/**
 * PM Paper Parameter Processor
 * =============================
 *
 * Enhances paper rendering by processing inline parameter references
 * and converting them to interactive pm-param-paper components.
 *
 * Usage:
 *   - Automatically loaded by paper.html
 *   - Processes {{param:key}} references in text
 *   - Converts to <pm-param-paper key="..."> components
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

(function() {
    'use strict';

    /**
     * Process inline parameter references in a container
     * Converts {{param:gauge.M_GUT}} to interactive parameter display
     * @param {HTMLElement} container - Container to process
     */
    function processInlineParameterReferences(container) {
        if (!container) {
            console.warn('PMPaperParamProcessor: No container provided');
            return;
        }

        // Find all text nodes
        const walker = document.createTreeWalker(
            container,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            // Skip if parent is script, style, or already processed
            const parent = node.parentElement;
            if (parent && !['SCRIPT', 'STYLE', 'CODE', 'PRE', 'PM-PARAM-PAPER'].includes(parent.tagName)) {
                textNodes.push(node);
            }
        }

        let replacementsCount = 0;

        // Process each text node
        for (const textNode of textNodes) {
            const text = textNode.textContent;

            // Match patterns like {{param:gauge.M_GUT}} or {{param:constants.M_PLANCK}}
            const pattern = /\{\{param:([^}]+)\}\}/gi;

            if (pattern.test(text)) {
                // Create a temporary container to build the replacement HTML
                const tempDiv = document.createElement('div');
                let lastIndex = 0;
                let match;
                pattern.lastIndex = 0; // Reset regex

                while ((match = pattern.exec(text)) !== null) {
                    const paramKey = match[1];
                    const fullMatch = match[0];

                    // Add text before match
                    if (match.index > lastIndex) {
                        tempDiv.appendChild(document.createTextNode(text.substring(lastIndex, match.index)));
                    }

                    // Create pm-param-paper component
                    const paramEl = document.createElement('pm-param-paper');
                    paramEl.setAttribute('key', paramKey);
                    paramEl.setAttribute('inline', 'true');
                    tempDiv.appendChild(paramEl);

                    replacementsCount++;
                    lastIndex = match.index + fullMatch.length;
                }

                // Add remaining text
                if (lastIndex < text.length) {
                    tempDiv.appendChild(document.createTextNode(text.substring(lastIndex)));
                }

                // Replace the text node with the new content
                if (tempDiv.childNodes.length > 0) {
                    const parent = textNode.parentNode;
                    while (tempDiv.firstChild) {
                        parent.insertBefore(tempDiv.firstChild, textNode);
                    }
                    parent.removeChild(textNode);
                }
            }
        }

        if (replacementsCount > 0) {
            console.log(`PMPaperParamProcessor: Processed ${replacementsCount} parameter reference(s)`);
        }
    }

    /**
     * Auto-process on DOM content loaded
     */
    function autoProcess() {
        // Process the main paper container
        const paperContainer = document.querySelector('.pm-paper-container, #paper-content');
        if (paperContainer) {
            processInlineParameterReferences(paperContainer);
        }
    }

    // Export API
    window.PMPaperParamProcessor = {
        process: processInlineParameterReferences,
        autoProcess
    };

    // Auto-run on DOM content loaded (after paper renderer)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            // Delay to ensure paper is rendered first
            setTimeout(autoProcess, 500);
        });
    } else {
        // DOM already loaded
        setTimeout(autoProcess, 500);
    }

    console.log('PMPaperParamProcessor: Ready');

})();
