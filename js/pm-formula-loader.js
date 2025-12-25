/**
 * PM Formula Loader
 * =================
 *
 * Loads formulas from AUTO_GENERATED/json/formulas.json (or theory_output.json).
 * This provides a single source of truth from Python config.py to JavaScript.
 *
 * The loader caches formulas, provides lookup by ID, and automatically renders
 * formulas into the DOM.
 *
 * Usage:
 *   // Auto-loads on page load and renders all formulas
 *   await PMFormulaLoader.load();
 *
 *   // Get formula data
 *   const formula = PMFormulaLoader.get('generation-number');
 *
 *   // Render formulas in HTML:
 *   <div data-formula-id="generation-number"></div>
 *   <pm-formula data-id="generation-number"></pm-formula>
 *
 *   // Manual rendering
 *   PMFormulaLoader.render(element, 'generation-number', { showLabel: true });
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

class PMFormulaLoader {
    static _formulas = null;
    static _loaded = false;
    static _loading = null;
    static _version = null;

    /**
     * Load formulas from theory_output.json
     * @param {string} path - Path to theory_output.json (default: auto-detect)
     * @returns {Promise<boolean>} - True if loaded successfully
     */
    static async load(path = null) {
        if (this._loaded) return true;
        if (this._loading) return this._loading;

        this._loading = (async () => {
            try {
                const pathPrefixes = [
                    '',                          // Root directory
                    'AUTO_GENERATED/',           // AUTO_GENERATED folder
                    '../',                       // Parent directory (from subdirs)
                    '../AUTO_GENERATED/',        // From subdirectory
                    '../../',                    // Two levels up
                    '../../AUTO_GENERATED/',     // From nested subdirectory
                ];

                const triedPaths = [];

                // ================================================================
                // STRATEGY 1: Try to load unified theory_output.json
                // ================================================================
                if (!path) {
                    for (const prefix of pathPrefixes) {
                        const testPath = prefix + 'theory_output.json';
                        triedPaths.push(testPath);
                        try {
                            const response = await fetch(testPath);
                            if (response.ok) {
                                path = testPath;
                                break;
                            }
                        } catch (e) {
                            if (window.PM_DEBUG) {
                                console.debug(`  - Failed to load ${testPath}: ${e.message}`);
                            }
                            continue;
                        }
                    }
                }

                // If we found theory_output.json, load it
                if (path) {
                    const response = await fetch(path);
                    if (response.ok) {
                        const data = await response.json();

                        if (data.formulas && data.formulas.formulas) {
                            this._formulas = data.formulas.formulas;
                            this._version = data.formulas.version || data.version || 'unknown';
                            this._loaded = true;

                            console.log(`%cPMFormulaLoader: Successfully loaded from ${path}`, 'color: green; font-weight: bold');
                            console.log(`  Formulas: ${Object.keys(this._formulas).length} (v${this._version})`);

                            // Expose globally for debugging
                            window.PM_FORMULAS = this._formulas;

                            // Merge with global FORMULA_REGISTRY if exists
                            if (window.FORMULA_REGISTRY) {
                                this._mergeWithRegistry();
                            }

                            // Render any formulas in the DOM
                            this.renderAll();

                            return true;
                        }
                    }
                }

                // ================================================================
                // STRATEGY 2: Try to load AUTO_GENERATED/json/formulas.json
                // ================================================================
                console.log('%cPMFormulaLoader: theory_output.json not found, trying formulas.json...', 'color: orange');

                for (const prefix of pathPrefixes) {
                    try {
                        const formulasPath = prefix + 'AUTO_GENERATED/json/formulas.json';
                        triedPaths.push(formulasPath);

                        const response = await fetch(formulasPath);
                        if (response.ok) {
                            const formulasData = await response.json();

                            // Handle both formats:
                            // 1. Direct formulas object: { "formula-id": {...}, ... }
                            // 2. Wrapped format: { formulas: {...}, version: "...", count: N }
                            let formulas;
                            if (formulasData.formulas && typeof formulasData.formulas === 'object') {
                                formulas = formulasData.formulas;
                                this._version = formulasData.version || 'unknown';
                            } else {
                                formulas = formulasData;
                                this._version = 'individual-file';
                            }

                            this._formulas = formulas;
                            this._loaded = true;

                            console.log(`%cPMFormulaLoader: Successfully loaded from ${formulasPath}`, 'color: green; font-weight: bold');
                            console.log(`  Formulas: ${Object.keys(this._formulas).length} (v${this._version})`);

                            // Expose globally for debugging
                            window.PM_FORMULAS = this._formulas;

                            // Merge with global FORMULA_REGISTRY if exists
                            if (window.FORMULA_REGISTRY) {
                                this._mergeWithRegistry();
                            }

                            // Render any formulas in the DOM
                            this.renderAll();

                            return true;
                        }
                    } catch (e) {
                        if (window.PM_DEBUG) {
                            console.debug(`  - Failed to load ${prefix}AUTO_GENERATED/json/formulas.json: ${e.message}`);
                        }
                        continue;
                    }
                }

                // ================================================================
                // FAILURE: Could not load formulas
                // ================================================================
                console.error('%cPMFormulaLoader: Failed to load formulas!', 'color: red; font-weight: bold');
                console.error('  Tried paths:', triedPaths);
                console.error('  ');
                console.error('  SOLUTIONS:');
                console.error('  1. Run: python run_all_simulations.py --export');
                console.error('  2. Check that theory_output.json or AUTO_GENERATED/json/formulas.json exists');
                console.error('  3. If using file:// protocol, you may need to run a local web server');
                console.error('     Try: python -m http.server 8000');
                console.error('  ');
                console.error('  Set window.PM_DEBUG = true for verbose logging');

                return false;
            } catch (error) {
                console.error('%cPMFormulaLoader: Error during loading:', 'color: red; font-weight: bold', error);
                return false;
            }
        })();

        return this._loading;
    }

    /**
     * Merge loaded formulas with existing FORMULA_REGISTRY
     */
    static _mergeWithRegistry() {
        if (!this._formulas || !window.FORMULA_REGISTRY) return;

        for (const [id, formula] of Object.entries(this._formulas)) {
            const category = formula.category || 'DERIVED';

            // Create category if doesn't exist
            if (!window.FORMULA_REGISTRY[category]) {
                window.FORMULA_REGISTRY[category] = {};
            }

            // Add/update formula in registry
            window.FORMULA_REGISTRY[category][id] = {
                id: formula.id,
                html: formula.html,
                latex: formula.latex,
                plainText: formula.plainText,
                label: formula.label,
                category: category,
                description: formula.description,
                attribution: formula.attribution || 'Principia Metaphysica',
                status: formula.status,
                section: formula.section,
                terms: formula.terms || {},
                derivation: formula.derivation,
                computedValue: formula.computedValue,
                units: formula.units,
                experimentalValue: formula.experimentalValue,
                sigmaDeviation: formula.sigmaDeviation,
                simulationFile: formula.simulationFile,
                relatedFormulas: formula.relatedFormulas,
                notes: formula.notes,
                testability: formula.testability
            };
        }

        console.log('PMFormulaLoader: Merged with FORMULA_REGISTRY');
    }

    /**
     * Get a formula by ID
     * @param {string} id - Formula ID
     * @returns {Object|null} - Formula object or null
     */
    static get(id) {
        if (!this._formulas) return null;
        return this._formulas[id] || null;
    }

    /**
     * Get all formulas
     * @returns {Object} - All formulas keyed by ID
     */
    static getAll() {
        return this._formulas || {};
    }

    /**
     * Get formulas by category
     * @param {string} category - Category name (THEORY, DERIVED, PREDICTIONS)
     * @returns {Array} - Array of formulas in that category
     */
    static getByCategory(category) {
        if (!this._formulas) return [];
        return Object.values(this._formulas).filter(f => f.category === category);
    }

    /**
     * Get formulas by section
     * @param {string} section - Section number (e.g., "2", "4.1")
     * @returns {Array} - Array of formulas in that section
     */
    static getBySection(section) {
        if (!this._formulas) return [];
        return Object.values(this._formulas).filter(f =>
            f.section && f.section.startsWith(section)
        );
    }

    /**
     * Get related formulas for a given formula ID
     * @param {string} id - Formula ID
     * @returns {Array} - Array of related formula objects
     */
    static getRelated(id) {
        const formula = this.get(id);
        if (!formula || !formula.relatedFormulas) return [];
        return formula.relatedFormulas
            .map(relId => this.get(relId))
            .filter(f => f !== null);
    }

    /**
     * Search formulas by description or label
     * @param {string} query - Search query
     * @returns {Array} - Matching formulas
     */
    static search(query) {
        if (!this._formulas) return [];
        const q = query.toLowerCase();
        return Object.values(this._formulas).filter(f =>
            (f.description && f.description.toLowerCase().includes(q)) ||
            (f.label && f.label.toLowerCase().includes(q)) ||
            (f.id && f.id.includes(q))
        );
    }

    /**
     * Get statistics about loaded formulas
     * @returns {Object} - Statistics
     */
    static getStats() {
        if (!this._formulas) return { loaded: false };

        const all = Object.values(this._formulas);
        const categories = {};
        for (const f of all) {
            const cat = f.category || 'UNKNOWN';
            categories[cat] = (categories[cat] || 0) + 1;
        }

        return {
            loaded: true,
            version: this._version,
            total: all.length,
            categories,
            withExperimental: all.filter(f => f.experimentalValue !== undefined).length,
            withSimulations: all.filter(f => f.simulationFile).length
        };
    }

    /**
     * Render a formula into a DOM element
     * @param {HTMLElement} element - Element to render into
     * @param {string} formulaId - Formula ID
     * @param {Object} options - Rendering options
     * @returns {boolean} - True if rendered successfully
     */
    static render(element, formulaId, options = {}) {
        if (!element) {
            console.error('PMFormulaLoader.render: No element provided');
            return false;
        }

        const formula = this.get(formulaId);
        if (!formula) {
            console.error(`PMFormulaLoader.render: Formula not found: ${formulaId}`);
            element.innerHTML = `<div style="color: red; padding: 0.5rem; background: rgba(255,0,0,0.1); border-radius: 4px;">
                <strong>Formula not found:</strong> ${formulaId}
                <br><small>Available formulas: ${Object.keys(this._formulas || {}).slice(0, 5).join(', ')}...</small>
            </div>`;
            return false;
        }

        const {
            showLabel = true,
            showPlainText = false,
            showDerivation = false,
            className = 'pm-formula-rendered'
        } = options;

        // Build the HTML
        let html = `<div class="${className}" data-formula-id="${formulaId}">`;

        // Label
        if (showLabel && formula.label) {
            html += `<div class="formula-label" style="font-size: 0.9rem; color: #888; margin-bottom: 0.5rem;">
                ${formula.label}
            </div>`;
        }

        // Main formula display
        html += `<div class="formula-display" style="font-size: 1.2rem; padding: 0.5rem 0; text-align: center;">
            ${formula.html || formula.latex || formula.plainText || ''}
        </div>`;

        // Plain text fallback
        if (showPlainText && formula.plainText) {
            html += `<div class="formula-plaintext" style="font-family: monospace; font-size: 0.85rem; color: #666; text-align: center; margin-top: 0.5rem;">
                ${formula.plainText}
            </div>`;
        }

        // Derivation info
        if (showDerivation && formula.derivation) {
            html += `<div class="formula-derivation" style="font-size: 0.85rem; color: #888; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px dashed #444;">
                <strong>Derivation:</strong> ${formula.description || 'See documentation'}
            </div>`;
        }

        html += '</div>';
        element.innerHTML = html;

        // Trigger MathJax if available
        this._triggerMathJax(element);

        return true;
    }

    /**
     * Render all elements with data-formula-id or data-id attributes
     */
    static renderAll() {
        if (!this._loaded) {
            console.warn('PMFormulaLoader.renderAll: Formulas not loaded yet');
            return;
        }

        // Ensure DOM is ready before attempting to render
        if (typeof document === 'undefined') {
            console.warn('PMFormulaLoader.renderAll: Document not available');
            return;
        }

        // Find all elements with data-formula-id attribute
        const elementsWithFormulaId = document.querySelectorAll('[data-formula-id]:not(.pm-formula-rendered)');
        let renderedCount = 0;

        elementsWithFormulaId.forEach(element => {
            const formulaId = element.getAttribute('data-formula-id');
            if (formulaId && this.render(element, formulaId)) {
                renderedCount++;
            }
        });

        // Find all pm-formula elements with data-id attribute (if not using web component)
        const pmFormulaElements = document.querySelectorAll('pm-formula[data-id]:not(.pm-formula-rendered)');
        pmFormulaElements.forEach(element => {
            const formulaId = element.getAttribute('data-id');
            if (formulaId && this.render(element, formulaId)) {
                renderedCount++;
            }
        });

        if (renderedCount > 0) {
            console.log(`PMFormulaLoader: Rendered ${renderedCount} formulas`);
        }
    }

    /**
     * Trigger MathJax typesetting on an element
     * @private
     */
    static _triggerMathJax(element) {
        if (typeof window === 'undefined') return;

        // Check for MathJax v3
        if (window.MathJax && window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise([element]).catch(err => {
                console.warn('MathJax typesetting failed:', err);
            });
        }
        // Check for MathJax v2
        else if (window.MathJax && window.MathJax.Hub) {
            window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, element]);
        }
    }
}

// Auto-load on page load
if (typeof window !== 'undefined') {
    window.PMFormulaLoader = PMFormulaLoader;

    // Load when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => PMFormulaLoader.load());
    } else {
        PMFormulaLoader.load();
    }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PMFormulaLoader };
}
