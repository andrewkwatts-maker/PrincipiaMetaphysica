/**
 * PM Paper Renderer
 * =================
 *
 * Dynamically renders the complete Principia Metaphysica paper from theory_output.json.
 * Loads sections, renders formulas, populates parameters, and triggers MathJax.
 *
 * Features:
 * - Loads all sections from theory_output.json
 * - Renders title, abstract, and sections dynamically
 * - Replaces inline formulas with data-formula-id references
 * - Uses PM.get() for parameter values
 * - Coordinates MathJax typesetting
 * - Supports loading section HTML files
 *
 * Usage:
 *   import { renderPaper } from './pm-paper-renderer.js';
 *   await renderPaper('paper-container');
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 * Version: 1.0.0
 */

(function() {
    'use strict';

    // ========================================================================
    // STATE MANAGEMENT
    // ========================================================================

    const PaperRenderer = {
        _data: null,
        _loaded: false,
        _loading: null,
        _sectionsCache: new Map(),
        _debug: false
    };

    // ========================================================================
    // MAIN RENDERING FUNCTIONS
    // ========================================================================

    /**
     * Render the complete paper into a container
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Rendering options
     * @returns {Promise<boolean>} - True if rendered successfully
     */
    async function renderPaper(containerId, options = {}) {
        const {
            loadSections = true,
            loadFormulas = true,
            loadParameters = true,
            renderAbstract = true,
            renderTOC = true,
            debug = false
        } = options;

        PaperRenderer._debug = debug;

        // 1. Load theory_output.json
        const loaded = await loadTheoryData();
        if (!loaded) {
            console.error('PMPaperRenderer: Failed to load theory_output.json');
            return false;
        }

        // 2. Get container
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`PMPaperRenderer: Container not found: ${containerId}`);
            return false;
        }

        // 3. Clear container
        container.innerHTML = '';
        container.classList.add('pm-paper-container');

        // 4. Render paper components
        try {
            // Title and metadata
            if (PaperRenderer._data.metadata) {
                renderTitle(container, PaperRenderer._data.metadata);
            }

            // Abstract
            if (renderAbstract && PaperRenderer._data.sections?.['1']?.abstract) {
                renderAbstractSection(container, PaperRenderer._data.sections['1'].abstract);
            }

            // Table of Contents
            if (renderTOC) {
                renderTableOfContents(container, PaperRenderer._data.sections);
            }

            // Main sections
            if (loadSections && PaperRenderer._data.sections) {
                await renderAllSections(container, PaperRenderer._data.sections, { loadFormulas, loadParameters });
            }

            // Trigger MathJax
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
                console.log('PMPaperRenderer: Triggering MathJax...');
                await MathJax.typesetPromise([container]);
            }

            console.log('%cPMPaperRenderer: Paper rendered successfully', 'color: green; font-weight: bold');
            return true;

        } catch (error) {
            console.error('PMPaperRenderer: Error during rendering:', error);
            return false;
        }
    }

    /**
     * Load theory_output.json data
     * @private
     */
    async function loadTheoryData() {
        if (PaperRenderer._loaded) return true;
        if (PaperRenderer._loading) return PaperRenderer._loading;

        PaperRenderer._loading = (async () => {
            const pathPrefixes = [
                '',
                'AUTO_GENERATED/',
                '../',
                '../AUTO_GENERATED/',
                '../../',
                '../../AUTO_GENERATED/'
            ];

            for (const prefix of pathPrefixes) {
                try {
                    const path = prefix + 'theory_output.json';
                    const response = await fetch(path);
                    if (response.ok) {
                        PaperRenderer._data = await response.json();
                        PaperRenderer._loaded = true;
                        console.log(`PMPaperRenderer: Loaded theory_output.json from ${path}`);
                        return true;
                    }
                } catch (e) {
                    if (PaperRenderer._debug) {
                        console.debug(`PMPaperRenderer: Failed to load from ${prefix}theory_output.json`);
                    }
                }
            }

            console.error('PMPaperRenderer: Could not load theory_output.json');
            return false;
        })();

        return PaperRenderer._loading;
    }

    // ========================================================================
    // COMPONENT RENDERERS
    // ========================================================================

    /**
     * Render paper title and metadata
     * @private
     */
    function renderTitle(container, metadata) {
        const titleSection = document.createElement('div');
        titleSection.className = 'paper-title-section';
        titleSection.innerHTML = `
            <h1 class="paper-title">${metadata.title || 'Principia Metaphysica'}</h1>
            ${metadata.subtitle ? `<h2 class="paper-subtitle">${metadata.subtitle}</h2>` : ''}
            ${metadata.author ? `<div class="paper-author">${metadata.author}</div>` : ''}
            ${metadata.date ? `<div class="paper-date">${metadata.date}</div>` : ''}
            ${metadata.version ? `<div class="paper-version">Version ${metadata.version}</div>` : ''}
        `;
        container.appendChild(titleSection);
    }

    /**
     * Render abstract section
     * @private
     */
    function renderAbstractSection(container, abstractText) {
        const abstractDiv = document.createElement('div');
        abstractDiv.className = 'paper-abstract';
        abstractDiv.innerHTML = `
            <h2>Abstract</h2>
            <p>${abstractText}</p>
        `;
        container.appendChild(abstractDiv);
    }

    /**
     * Render table of contents
     * @private
     */
    function renderTableOfContents(container, sections) {
        if (!sections || Object.keys(sections).length === 0) return;

        const tocDiv = document.createElement('div');
        tocDiv.className = 'paper-toc';
        tocDiv.innerHTML = '<h2>Table of Contents</h2>';

        const tocList = document.createElement('ol');
        tocList.className = 'toc-list';

        // Sort sections by order or ID
        const sortedSections = Object.values(sections).sort((a, b) => {
            const orderA = a.order || parseInt(a.id) || 0;
            const orderB = b.order || parseInt(b.id) || 0;
            return orderA - orderB;
        });

        for (const section of sortedSections) {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="#section-${section.id}" class="toc-link">
                    <span class="toc-number">${section.id}</span>
                    <span class="toc-title">${section.title}</span>
                </a>
            `;
            tocList.appendChild(li);

            // Subsections (if any)
            if (section.subsections && section.subsections.length > 0) {
                const subList = document.createElement('ol');
                subList.className = 'toc-sublist';
                for (const subsection of section.subsections) {
                    const subLi = document.createElement('li');
                    subLi.innerHTML = `
                        <a href="#section-${subsection.id}" class="toc-link">
                            <span class="toc-number">${subsection.id}</span>
                            <span class="toc-title">${subsection.title}</span>
                        </a>
                    `;
                    subList.appendChild(subLi);
                }
                li.appendChild(subList);
            }
        }

        tocDiv.appendChild(tocList);
        container.appendChild(tocDiv);
    }

    /**
     * Render all sections
     * @private
     */
    async function renderAllSections(container, sections, options) {
        if (!sections || Object.keys(sections).length === 0) return;

        const sectionsDiv = document.createElement('div');
        sectionsDiv.className = 'paper-sections';

        // Sort sections by order
        const sortedSections = Object.values(sections).sort((a, b) => {
            const orderA = a.order || parseInt(a.id) || 0;
            const orderB = b.order || parseInt(b.id) || 0;
            return orderA - orderB;
        });

        for (const section of sortedSections) {
            const sectionEl = await renderSection(section, options);
            if (sectionEl) {
                sectionsDiv.appendChild(sectionEl);
            }
        }

        container.appendChild(sectionsDiv);
    }

    /**
     * Render a single section with subsections
     * @param {Object} section - Section data from theory_output.json
     * @param {Object} options - Rendering options
     * @returns {Promise<HTMLElement>} - Rendered section element
     */
    async function renderSection(section, options = {}) {
        const { loadFormulas = true, loadParameters = true } = options;

        const sectionDiv = document.createElement('section');
        sectionDiv.id = `section-${section.id}`;
        sectionDiv.className = 'paper-section';
        sectionDiv.setAttribute('data-section-id', section.id);

        // Section header
        const header = document.createElement('div');
        header.className = 'section-header';
        header.innerHTML = `
            <h2 class="section-title">
                <span class="section-number">${section.id}</span>
                ${section.title}
            </h2>
        `;
        sectionDiv.appendChild(header);

        // Section abstract (if available)
        if (section.abstract) {
            const abstractDiv = document.createElement('div');
            abstractDiv.className = 'section-abstract';
            abstractDiv.innerHTML = `<p>${section.abstract}</p>`;
            sectionDiv.appendChild(abstractDiv);
        }

        // Try to load section HTML file if specified
        if (section.sectionFile) {
            const content = await loadSectionFile(section.sectionFile);
            if (content) {
                const contentDiv = document.createElement('div');
                contentDiv.className = 'section-content';
                contentDiv.innerHTML = content;
                sectionDiv.appendChild(contentDiv);

                // Process formulas and parameters in the loaded content
                if (loadFormulas) {
                    processFormulas(contentDiv);
                }
                if (loadParameters) {
                    processParameters(contentDiv);
                }
            }
        }

        // Render content blocks (if any)
        if (section.contentBlocks && section.contentBlocks.length > 0) {
            const blocksDiv = renderContentBlocks(section.contentBlocks);
            sectionDiv.appendChild(blocksDiv);
        }

        // Key takeaways (if available)
        if (section.keyTakeaways && section.keyTakeaways.length > 0) {
            const takeawaysDiv = document.createElement('div');
            takeawaysDiv.className = 'section-takeaways';
            takeawaysDiv.innerHTML = `
                <h3>Key Takeaways</h3>
                <ul>
                    ${section.keyTakeaways.map(item => `<li>${item}</li>`).join('')}
                </ul>
            `;
            sectionDiv.appendChild(takeawaysDiv);
        }

        return sectionDiv;
    }

    /**
     * Load section HTML file
     * @private
     */
    async function loadSectionFile(filePath) {
        // Check cache first
        if (PaperRenderer._sectionsCache.has(filePath)) {
            return PaperRenderer._sectionsCache.get(filePath);
        }

        const pathPrefixes = ['', '../', '../../'];

        for (const prefix of pathPrefixes) {
            try {
                const fullPath = prefix + filePath;
                const response = await fetch(fullPath);
                if (response.ok) {
                    const html = await response.text();

                    // Extract content from the <body> tag
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const body = doc.querySelector('body');

                    if (body) {
                        const content = body.innerHTML;
                        PaperRenderer._sectionsCache.set(filePath, content);
                        return content;
                    }
                }
            } catch (e) {
                if (PaperRenderer._debug) {
                    console.debug(`PMPaperRenderer: Failed to load ${filePath} from ${prefix}`);
                }
            }
        }

        console.warn(`PMPaperRenderer: Could not load section file: ${filePath}`);
        return null;
    }

    /**
     * Render content blocks
     * @private
     */
    function renderContentBlocks(blocks) {
        const container = document.createElement('div');
        container.className = 'content-blocks';

        for (const block of blocks) {
            const blockEl = renderContentBlock(block);
            if (blockEl) {
                container.appendChild(blockEl);
            }
        }

        return container;
    }

    /**
     * Render a single content block
     * @private
     */
    function renderContentBlock(block) {
        const blockDiv = document.createElement('div');
        blockDiv.className = `content-block content-block-${block.type}`;

        switch (block.type) {
            case 'paragraph':
                blockDiv.innerHTML = `<p>${block.content}</p>`;
                break;

            case 'heading':
                const level = block.level || 3;
                blockDiv.innerHTML = `<h${level}>${block.content}</h${level}>`;
                break;

            case 'formula':
                blockDiv.innerHTML = `
                    <div class="formula-block" data-formula-id="${block.formulaId}">
                        ${block.content || ''}
                    </div>
                `;
                break;

            case 'equation':
                blockDiv.innerHTML = `
                    <div class="equation-block">
                        ${block.latex ? `$$${block.latex}$$` : block.content}
                    </div>
                `;
                break;

            case 'list':
                const listType = block.ordered ? 'ol' : 'ul';
                const items = block.items.map(item => `<li>${item}</li>`).join('');
                blockDiv.innerHTML = `<${listType}>${items}</${listType}>`;
                break;

            case 'code':
                blockDiv.innerHTML = `<pre><code>${escapeHtml(block.content)}</code></pre>`;
                break;

            case 'quote':
                blockDiv.innerHTML = `<blockquote>${block.content}</blockquote>`;
                break;

            default:
                blockDiv.innerHTML = block.content || '';
        }

        return blockDiv;
    }

    // ========================================================================
    // FORMULA AND PARAMETER PROCESSING
    // ========================================================================

    /**
     * Process formulas in a container
     * Replaces inline formula references with proper data-formula-id elements
     * @private
     */
    function processFormulas(container) {
        // Find all elements with data-formula-id that are empty
        const formulaElements = container.querySelectorAll('[data-formula-id]');

        formulaElements.forEach(el => {
            const formulaId = el.getAttribute('data-formula-id');

            // Skip if already has content
            if (el.innerHTML.trim() && !el.classList.contains('pm-formula-auto')) {
                return;
            }

            // Try to get formula from PM
            if (window.PM && typeof window.PM.formula === 'function') {
                const formula = window.PM.formula(formulaId);
                if (formula) {
                    el.innerHTML = formula.html || formula.latex || formula.plainText || '';
                    el.classList.add('pm-formula-loaded');

                    // Add tooltip with description
                    if (formula.description) {
                        el.setAttribute('title', formula.description);
                    }
                }
            }
        });
    }

    /**
     * Process parameters in a container
     * Replaces data-pm-value elements with actual values
     * @private
     */
    function processParameters(container) {
        // Process data-pm-value elements
        const pmValueElements = container.querySelectorAll('[data-pm-value]');

        pmValueElements.forEach(el => {
            const path = el.getAttribute('data-pm-value');
            const format = el.getAttribute('data-format');

            if (window.PM && typeof window.PM.get === 'function') {
                const value = window.PM.get(path);
                if (value !== null && value !== undefined) {
                    el.textContent = formatValue(value, format);
                    el.classList.add('pm-loaded');
                    el.classList.remove('pm-loading', 'pm-error');
                }
            }
        });

        // Process data-category + data-param elements
        const categoryElements = container.querySelectorAll('[data-category][data-param]');

        categoryElements.forEach(el => {
            const category = el.getAttribute('data-category');
            const param = el.getAttribute('data-param');
            const format = el.getAttribute('data-format');

            if (window.PM && typeof window.PM.get === 'function') {
                // Try multiple paths
                const paths = [
                    `simulations.${param}`,
                    `simulations.${category}.${param}`,
                    `parameters.${category}.${param}`,
                    `${category}.${param}`
                ];

                for (const path of paths) {
                    let value = window.PM.get(path);

                    // Auto-extract .value property if present
                    if (value !== null && value !== undefined && typeof value === 'object' && 'value' in value) {
                        value = value.value;
                    }

                    if (value !== null && value !== undefined) {
                        el.textContent = formatValue(value, format);
                        el.classList.add('pm-loaded');
                        el.classList.remove('pm-loading', 'pm-error');
                        break;
                    }
                }
            }
        });
    }

    /**
     * Render a formula by ID
     * @param {string} formulaId - Formula ID
     * @returns {string|null} - HTML/LaTeX string
     */
    function renderFormula(formulaId) {
        if (!window.PM || typeof window.PM.formula !== 'function') {
            console.error('PMPaperRenderer: PM.formula() not available');
            return null;
        }

        const formula = window.PM.formula(formulaId);
        if (!formula) {
            console.warn(`PMPaperRenderer: Formula not found: ${formulaId}`);
            return null;
        }

        return formula.html || formula.latex || formula.plainText || null;
    }

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================

    /**
     * Format a value for display
     * @private
     */
    function formatValue(value, format) {
        if (value === null || value === undefined) return '?';

        if (typeof value === 'number') {
            if (format) {
                if (format.startsWith('scientific:')) {
                    const decimals = parseInt(format.split(':')[1]) || 2;
                    return value.toExponential(decimals);
                }
                if (format.startsWith('fixed:')) {
                    const decimals = parseInt(format.split(':')[1]) || 2;
                    return value.toFixed(decimals);
                }
                if (format === 'percent') {
                    return (value * 100).toFixed(1) + '%';
                }
                if (format === 'integer') {
                    return Math.round(value).toString();
                }
            }

            // Auto-format based on magnitude
            if (Math.abs(value) >= 1e10 || (Math.abs(value) < 0.001 && value !== 0)) {
                return value.toExponential(2);
            } else if (Number.isInteger(value)) {
                return value.toString();
            } else {
                return value.toFixed(3);
            }
        }

        if (typeof value === 'boolean') {
            return value ? 'Yes' : 'No';
        }

        return String(value);
    }

    /**
     * Escape HTML special characters
     * @private
     */
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Trigger MathJax typesetting on a specific element
     * @param {HTMLElement} element - Element to typeset
     */
    function typesetMathJax(element) {
        if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
            MathJax.typesetPromise([element]).catch(err => {
                console.warn('PMPaperRenderer: MathJax typesetting failed:', err);
            });
        } else if (typeof MathJax !== 'undefined' && MathJax.Hub) {
            MathJax.Hub.Queue(['Typeset', MathJax.Hub, element]);
        }
    }

    // ========================================================================
    // PUBLIC API
    // ========================================================================

    const API = {
        renderPaper,
        renderSection,
        renderFormula,
        processFormulas,
        processParameters,
        typesetMathJax,
        get data() { return PaperRenderer._data; },
        get loaded() { return PaperRenderer._loaded; }
    };

    // Export globally
    window.PMPaperRenderer = API;

    // Export for ES modules
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = API;
    }

    console.log('PMPaperRenderer: Ready (v1.0.0)');

})();
