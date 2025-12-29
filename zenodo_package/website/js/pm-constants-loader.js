/**
 * Principia Metaphysica - Constants Loader (Dynamic)
 * ====================================================
 *
 * Dynamically loads ALL constants from theory_output.json.
 * NO HARDCODED VALUES - Single source of truth from Python simulations.
 *
 * Usage:
 *   <span class="pm-value" data-category="simulations" data-param="proton_decay.tau_p_years"></span>
 *   <span data-pm-value="simulations.proton_decay.tau_p_years"></span>
 *
 * Also populates:
 *   window.PM - Flat access to all simulation data
 *   window.PM_FORMULAS - Access to CoreFormulas
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 * Version: 2.2.0 - Enhanced path resolution with case-insensitive lookups and auto-refresh
 */

(function() {
    'use strict';

    // ========================================================================
    // PM - Dynamically populated from theory_output.json
    // ========================================================================

    const PM = {
        _loaded: false,
        _loading: null,
        _data: null,
        _error: null,

        // Fundamental dimensions (always available, from theory)
        dimensions: {
            D_BULK: 26,
            D_AFTER_SP2R: 13,
            D_G2: 7,
            D_SPIN8: 8,         // Octonions dimension (Spin(8) triality)
            D_OBSERVABLE: 4,
            D_COMMON: 4
        },

        // Key electroweak parameters (fallback if not in JSON)
        electroweak: {
            v_higgs: 246.22,    // Higgs VEV in GeV
            v_EW: 246.22,       // Electroweak VEV (alias)
            m_Z: 91.1876,       // Z boson mass in GeV
            m_W: 80.377         // W boson mass in GeV
        },

        // Mapping table for legacy/alternate parameter names
        _parameterAliases: {
            // Note: dimensions.X paths are handled by built-in fallback, not aliases
            // Only map dimension aliases that need special handling
            'dimensions.d_g2': 'dimensions.D_G2',  // Case normalization
            'dimensions.d_spin8': 'parameters.dimensions.D_SPIN8',

            // Topology parameters (case and naming variations)
            'parameters.topology.b2': 'parameters.topology.B2',
            'parameters.topology.b3': 'parameters.topology.B3',
            'parameters.topology.h11': 'parameters.topology.HODGE_H11',
            'parameters.topology.h21': 'parameters.topology.HODGE_H21',
            'parameters.topology.h31': 'parameters.topology.HODGE_H31',
            'parameters.topology.nu': 'parameters.topology.n_gen',

            // Gauge parameters - M_PS is in breaking_chain
            'parameters.gauge.m_ps': 'simulations.breaking_chain.m_ps',

            // Validation -> Framework Statistics mapping (use framework_statistics for accurate counts)
            'validation.total_predictions': 'framework_statistics.total_sm_parameters',
            'validation.total_parameters': 'framework_statistics.total_sm_parameters',
            'validation.exact_matches': 'framework_statistics.exact_matches',
            'validation.predictions_within_1sigma': 'framework_statistics.within_1_sigma',
            'validation.predictions_within_2sigma': 'framework_statistics.within_2_sigma',
            'validation.success_rate': 'framework_statistics.success_rate_1sigma',
            'validation.calibrated_parameters': 'framework_statistics.calibrated_parameters',

            // PMNS angles (in parameters.pmns, not simulations)
            'pmns_matrix.theta_23': 'parameters.pmns.theta_23',
            'pmns_matrix.theta_12': 'parameters.pmns.theta_12',
            'pmns_matrix.theta_13': 'parameters.pmns.theta_13',
            'pmns_matrix.delta_cp': 'parameters.pmns.delta_CP',

            // Common parameter shortcuts
            'topology.b3': 'parameters.topology.B3',
            'topology.b2': 'parameters.topology.B2',
            'topology.chi_eff': 'parameters.topology.CHI_EFF',
            'topology.n_gen': 'parameters.topology.n_gen',

            // KK spectrum
            'kk_spectrum.m1_central': 'simulations.kk_graviton.m_KK_TeV',
            'kk_spectrum.m1_TeV': 'simulations.kk_graviton.m_KK_TeV',

            // Proton decay
            'proton_decay.tau_p_years': 'simulations.proton_decay.tau_p_years',
            'proton_decay.alpha_GUT_inv': 'simulations.proton_decay.alpha_gut_inv',

            // Higgs
            'higgs_mass.m_h_GeV': 'simulations.higgs_mass.m_h_GeV',
            'v11_final_observables.higgs_mass.m_h_gev': 'simulations.higgs_mass.m_h_GeV',

            // Dark energy
            'dark_energy.w0': 'parameters.dark_energy.w0',
            'dark_energy.w0_PM': 'parameters.dark_energy.w0',

            // Beginner's guide aliases
            'v11_final_observables.proton_lifetime.tau_p_years': 'simulations.proton_decay.tau_p_years',
            'kk_spectrum.m1_central': 'simulations.kk_graviton.m_KK_TeV',
            'kk_spectrum.hl_lhc_significance': 'simulations.kk_graviton.hl_lhc_discovery',

            // Validation -> Framework Statistics (comprehensive mapping)
            'validation.predictions_within_1sigma': 'framework_statistics.within_1_sigma',
            'validation.within_1_sigma': 'framework_statistics.within_1_sigma',
            'validation.predictions_within_2sigma': 'framework_statistics.within_2_sigma',
            'validation.total_sm_parameters': 'framework_statistics.total_sm_parameters',
            'validation.total_predictions': 'framework_statistics.total_sm_parameters',
            'validation.exact_matches': 'framework_statistics.exact_matches',

            // Neutrino masses
            'neutrino_mass.delta_m_sq': 'simulations.neutrino_masses.delta_m21_sq',
            'neutrino_masses.delta_m21_sq': 'simulations.neutrino_masses.delta_m21_sq',
            'neutrino_masses.delta_m3l_sq': 'simulations.neutrino_masses.delta_m3l_sq',

            // Proton decay and GUT
            'proton_decay.m_gut': 'parameters.gauge.M_GUT',

            // KK graviton
            'kk_graviton.mass_tev': 'simulations.kk_graviton.m_KK_TeV',

            // VEV / Higgs
            'v12_6_geometric_derivations.vev_pneuma.v_ew': 'parameters.electroweak.v_higgs',
            'electroweak.v_higgs': 'parameters.electroweak.v_higgs',
        },

        /**
         * Get a value by path (e.g., "simulations.proton_decay.tau_p_years")
         * Handles case-insensitive lookups and parameter aliases
         */
        get(path) {
            if (!path) return null;

            // Check parameter aliases first (case-insensitive)
            const normalizedPath = path.toLowerCase();
            for (const [alias, realPath] of Object.entries(this._parameterAliases)) {
                if (normalizedPath === alias.toLowerCase()) {
                    path = realPath;
                    break;
                }
            }

            const parts = path.split('.');

            // Check built-in dimensions first (backward compatibility)
            if (parts[0] === 'dimensions' && parts.length === 2) {
                const dimKey = parts[1].toUpperCase();
                if (this.dimensions[dimKey] !== undefined) {
                    return this.dimensions[dimKey];
                }
            }

            // Check built-in electroweak fallbacks
            if ((parts[0] === 'electroweak' || (parts[0] === 'parameters' && parts[1] === 'electroweak')) && parts.length >= 2) {
                const ewKey = parts[parts.length - 1].toLowerCase();
                // Handle "parameters.electroweak.v_higgs.value" -> "v_higgs"
                if (ewKey === 'value' && parts.length > 2) {
                    const actualKey = parts[parts.length - 2].toLowerCase();
                    if (this.electroweak[actualKey] !== undefined) {
                        return this.electroweak[actualKey];
                    }
                }
                if (this.electroweak[ewKey] !== undefined) {
                    return this.electroweak[ewKey];
                }
            }

            if (!this._data) return null;

            // Try exact path first
            let value = this._tryPath(this._data, parts);
            if (value !== null && value !== undefined) {
                // Auto-extract .value from parameter objects
                return this._extractValue(value);
            }

            // Try case-insensitive lookup
            value = this._tryPathCaseInsensitive(this._data, parts);
            if (value !== null && value !== undefined) {
                // Auto-extract .value from parameter objects
                return this._extractValue(value);
            }

            return null;
        },

        /**
         * Extract primitive value from parameter objects
         * Objects with {value: X, units: Y} structure are common in parameters
         */
        _extractValue(value) {
            if (value === null || value === undefined) return value;

            // If it's a primitive, return as-is
            if (typeof value !== 'object') return value;

            // If it's an array, return as-is
            if (Array.isArray(value)) return value;

            // If it has a 'value' property and doesn't look like a formula/complex object
            // (formulas have 'html' or 'latex' properties)
            if ('value' in value && !('html' in value) && !('latex' in value)) {
                return value.value;
            }

            // Return object as-is for complex structures
            return value;
        },

        /**
         * Try to get a value by exact path
         */
        _tryPath(obj, parts) {
            let value = obj;
            for (const part of parts) {
                if (value && typeof value === 'object' && part in value) {
                    value = value[part];
                } else {
                    return null;
                }
            }
            return value;
        },

        /**
         * Try to get a value by case-insensitive path
         */
        _tryPathCaseInsensitive(obj, parts) {
            let value = obj;
            for (const part of parts) {
                if (!value || typeof value !== 'object') {
                    return null;
                }

                // Try exact match first
                if (part in value) {
                    value = value[part];
                    continue;
                }

                // Try case-insensitive match
                const lowerPart = part.toLowerCase();
                let found = false;
                for (const key of Object.keys(value)) {
                    if (key.toLowerCase() === lowerPart) {
                        value = value[key];
                        found = true;
                        break;
                    }
                }

                if (!found) {
                    return null;
                }
            }
            return value;
        },

        /**
         * Get simulation data by path (e.g., "proton_decay.tau_p_years")
         */
        simulation(path) {
            return this.get('simulations.' + path);
        },

        /**
         * Get formula by ID
         */
        formula(id) {
            return this._data?.formulas?.formulas?.[id] ?? null;
        },

        /**
         * Get all formulas
         */
        get formulas() {
            return this._data?.formulas?.formulas ?? {};
        },

        /**
         * Get statistics
         */
        get statistics() {
            return this._data?.statistics ?? {};
        },

        /**
         * Get validation summary
         */
        get validationSummary() {
            return this._data?.validation_summary ?? [];
        },

        /**
         * Check if all validations passed
         */
        get allPassed() {
            return this._data?.all_passed ?? false;
        },

        /**
         * Get version
         */
        get version() {
            return this._data?.version ?? 'unknown';
        }
    };

    // ========================================================================
    // LOADING FROM theory_output.json
    // ========================================================================

    // ========================================================================
    // COMPONENT-BASED CACHING SYSTEM
    // ========================================================================

    const CACHE_PREFIX = 'pm_';
    const CACHE_VERSION = '16.2';

    // Cache configuration per component (TTL in seconds)
    const CACHE_CONFIG = {
        parameters: { ttl: 3600, storage: 'localStorage' },    // 1 hour
        formulas: { ttl: 3600, storage: 'localStorage' },      // 1 hour
        sections: { ttl: 1800, storage: 'localStorage' },      // 30 minutes
        simulations: { ttl: 300, storage: 'sessionStorage' },  // 5 minutes
        statistics: { ttl: 300, storage: 'sessionStorage' },   // 5 minutes
        metadata: { ttl: 60, storage: 'sessionStorage' }       // 1 minute
    };

    /**
     * Get cached component data
     */
    function getCachedComponent(component) {
        const config = CACHE_CONFIG[component] || { ttl: 300, storage: 'sessionStorage' };
        const storage = config.storage === 'localStorage' ? localStorage : sessionStorage;
        const key = `${CACHE_PREFIX}${component}`;

        try {
            const cached = storage.getItem(key);
            if (!cached) return null;

            const { data, timestamp, version } = JSON.parse(cached);

            // Check version and TTL
            if (version !== CACHE_VERSION) return null;
            if (Date.now() - timestamp > config.ttl * 1000) return null;

            return data;
        } catch (e) {
            return null;
        }
    }

    /**
     * Cache component data
     */
    function cacheComponent(component, data) {
        const config = CACHE_CONFIG[component] || { ttl: 300, storage: 'sessionStorage' };
        const storage = config.storage === 'localStorage' ? localStorage : sessionStorage;
        const key = `${CACHE_PREFIX}${component}`;

        try {
            storage.setItem(key, JSON.stringify({
                data,
                timestamp: Date.now(),
                version: CACHE_VERSION
            }));
        } catch (e) {
            console.warn(`[PM Cache] Could not cache ${component}:`, e.message);
        }
    }

    /**
     * Determine base path for loading files
     */
    function getBasePath() {
        const path = window.location.pathname;
        if (path.includes('/foundations/') || path.includes('/sections/') ||
            path.includes('/docs/') || path.includes('/diagrams/') ||
            path.includes('/components/') || path.includes('/tests/')) {
            return '../AutoGenerated/';
        }
        return 'AutoGenerated/';
    }

    /**
     * Load a single component file with caching
     */
    async function loadComponent(component, basePath) {
        // Check cache first
        const cached = getCachedComponent(component);
        if (cached) {
            console.log(`[PM] ${component}: loaded from cache`);
            return cached;
        }

        // Try to load from file
        const paths = [
            `/AutoGenerated/${component}.json`,       // Absolute path (for live site)
            `${basePath}${component}.json`,
            `./${basePath}${component}.json`,
            `../${basePath}${component}.json`,
            `../../AutoGenerated/${component}.json`
        ];

        for (const path of paths) {
            try {
                const response = await fetch(path);
                if (response.ok) {
                    const data = await response.json();
                    cacheComponent(component, data);
                    console.log(`[PM] ${component}: loaded from ${path}`);
                    return data;
                }
            } catch (e) {
                continue;
            }
        }

        return null;
    }

    async function loadConstants() {
        if (PM._loaded) return true;
        if (PM._loading) return PM._loading;

        PM._loading = (async () => {
            const basePath = getBasePath();
            console.log(`[PM] Loading components from ${basePath}`);

            // ================================================================
            // STRATEGY 1: Load split component files in parallel (preferred)
            // ================================================================
            try {
                const [parameters, simulations, formulas, statistics, metadata] = await Promise.all([
                    loadComponent('parameters', basePath),
                    loadComponent('simulations', basePath),
                    loadComponent('formulas', basePath),
                    loadComponent('statistics', basePath),
                    loadComponent('metadata', basePath)
                ]);

                // If we got at least parameters or simulations, use split files
                if (parameters || simulations) {
                    PM._data = {
                        version: metadata?.version || '16.0',
                        parameters: parameters?.parameters || {},
                        simulations: simulations?.simulations || {},
                        formulas: formulas || { formulas: {}, count: 0 },
                        statistics: statistics?.statistics || {},
                        framework_statistics: statistics?.framework_statistics || {},
                        validation_summary: metadata?.validation_summary || [],
                        all_passed: metadata?.all_passed ?? true
                    };

                    PM._loaded = true;

                    // Create flat access to simulations
                    if (PM._data.simulations) {
                        for (const [key, value] of Object.entries(PM._data.simulations)) {
                            PM[key] = value;
                        }
                    }

                    console.log(`%cPM: Loaded from split components`, 'color: green; font-weight: bold');
                    console.log(`  Version: ${PM._data.version}`);
                    console.log(`  Parameters: ${Object.keys(PM._data.parameters).length} categories`);
                    console.log(`  Simulations: ${Object.keys(PM._data.simulations).length}`);
                    console.log(`  Formulas: ${PM._data.formulas?.count || Object.keys(PM._data.formulas?.formulas || {}).length}`);

                    // Expose globally
                    window.PM_DATA = PM._data;
                    window.PM_FORMULAS = PM._data.formulas?.formulas || {};

                    updateDOM();
                    setTimeout(() => {
                        if (typeof signalMathJax === 'function') signalMathJax();
                    }, 100);

                    return true;
                }
            } catch (e) {
                console.warn('[PM] Split component loading failed, trying unified file:', e.message);
            }

            // ================================================================
            // STRATEGY 2: Fallback to unified theory_output.json
            // ================================================================
            const unifiedPaths = [
                '/AutoGenerated/theory_output.json',  // Absolute path (for live site)
                `${basePath}theory_output.json`,
                'AutoGenerated/theory_output.json',
                './AutoGenerated/theory_output.json',
                '../AutoGenerated/theory_output.json',
                'theory_output.json',
                '../theory_output.json'
            ];

            for (const path of unifiedPaths) {
                try {
                    const response = await fetch(path);
                    if (response.ok) {
                        const data = await response.json();
                        PM._data = data;
                        PM._loaded = true;

                        // Create flat access to simulations
                        if (data.simulations) {
                            for (const [key, value] of Object.entries(data.simulations)) {
                                PM[key] = value;
                            }
                        }

                        console.log(`%cPM: Loaded from unified ${path}`, 'color: green; font-weight: bold');

                        window.PM_DATA = data;
                        window.PM_FORMULAS = data.formulas?.formulas || {};

                        updateDOM();
                        setTimeout(() => {
                            if (typeof signalMathJax === 'function') signalMathJax();
                        }, 100);

                        return true;
                    }
                } catch (e) {
                    continue;
                }
            }

            // ================================================================
            // FAILURE: Could not load data
            // ================================================================
            PM._error = 'Could not load data files';
            console.error('%cPM: Failed to load data!', 'color: red; font-weight: bold');
            console.error('  Run: python run_all_simulations.py');
            console.error('  Then: python simulations/Constants/split_theory_output.py');

            updateDOM();
            return false;
        })();

        return PM._loading;
    }

    // ========================================================================
    // DOM MANIPULATION
    // ========================================================================

    function formatValue(value, format) {
        if (value === null || value === undefined) return '?';

        // Safety net: extract .value from objects that slipped through
        if (typeof value === 'object' && !Array.isArray(value)) {
            if ('value' in value && !('html' in value) && !('latex' in value)) {
                value = value.value;
            } else {
                // For complex objects without a value property, return a sensible default
                console.warn('formatValue received object:', value);
                return '?';
            }
        }

        if (typeof value === 'number') {
            // Handle format specifications
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

    function updateDOM() {
        const stats = {
            pmValue: { loaded: 0, failed: 0 },
            category: { loaded: 0, failed: 0 },
            formula: { loaded: 0, failed: 0 },
            stat: { loaded: 0, failed: 0 }
        };

        // ====================================================================
        // 1. Handle data-pm-value="path.to.value" format
        // ====================================================================
        const pmValueElements = document.querySelectorAll('[data-pm-value]');
        pmValueElements.forEach(el => {
            const path = el.getAttribute('data-pm-value');
            const format = el.getAttribute('data-format');
            const value = PM.get(path);

            if (value !== null && value !== undefined) {
                el.textContent = formatValue(value, format);
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.removeAttribute('title');

                // Mark element to prevent MathJax from processing it
                el.classList.add('mathjax-ignore');

                stats.pmValue.loaded++;
            } else if (!PM._loaded) {
                el.textContent = '...';
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.textContent = '?';
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                el.setAttribute('title', `ERROR: Path not found in theory_output.json: "${path}"`);
                if (window.PM_DEBUG) {
                    console.error(`PM: Path not found: ${path}`);
                }
                stats.pmValue.failed++;
            }
        });

        // ====================================================================
        // 2. Handle data-category + data-param format
        // ====================================================================
        const categoryElements = document.querySelectorAll('[data-category][data-param]');
        categoryElements.forEach(el => {
            const category = el.getAttribute('data-category');
            const param = el.getAttribute('data-param');
            const format = el.getAttribute('data-format');
            const field = el.getAttribute('data-field'); // Optional sub-field

            let value = null;
            const triedPaths = [];

            // Strategy 1: Try simulations.category.param (most common)
            if (category === 'simulations') {
                const path1 = `simulations.${param}`;
                triedPaths.push(path1);
                value = PM.get(path1);
            } else {
                const path2 = `simulations.${category}.${param}`;
                triedPaths.push(path2);
                value = PM.get(path2);
            }

            // Strategy 2: Try parameters.category.param (for parameter section)
            if (value === null || value === undefined) {
                const path3 = `parameters.${category}.${param}`;
                triedPaths.push(path3);
                value = PM.get(path3);
            }

            // Strategy 3: Try top-level category.param
            if (value === null || value === undefined) {
                const path4 = `${category}.${param}`;
                triedPaths.push(path4);
                value = PM.get(path4);
            }

            // Strategy 4: Try direct simulation access via flat PM object
            if ((value === null || value === undefined) && PM[category]) {
                triedPaths.push(`PM.${category}.${param}`);
                const parts = param.split('.');
                value = PM[category];
                for (const part of parts) {
                    if (value && typeof value === 'object' && part in value) {
                        value = value[part];
                    } else {
                        value = null;
                        break;
                    }
                }
            }

            // Extract nested field if specified (e.g., data-field="value" or "experimental_value")
            if ((value !== null && value !== undefined) && field) {
                if (typeof value === 'object' && field in value) {
                    value = value[field];
                } else {
                    console.warn(`PM: Field "${field}" not found in ${category}.${param}`, value);
                    value = null;
                }
            }

            // Auto-extract .value property if present (common pattern)
            if (value !== null && value !== undefined && !field) {
                if (typeof value === 'object' && 'value' in value && !('html' in value) && !('latex' in value)) {
                    value = value.value;
                }
            }

            if (value !== null && value !== undefined) {
                el.textContent = formatValue(value, format);
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.removeAttribute('title');
                stats.category.loaded++;
            } else if (!PM._loaded) {
                el.textContent = '...';
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.textContent = '?';
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                const errorMsg = `ERROR: Not found in theory_output.json\nCategory: "${category}"\nParam: "${param}"${field ? `\nField: "${field}"` : ''}\nTried paths: ${triedPaths.join(', ')}`;
                el.setAttribute('title', errorMsg);
                if (window.PM_DEBUG) {
                    console.error(`PM: Not found - category="${category}" param="${param}"${field ? ` field="${field}"` : ''}\nTried: ${triedPaths.join(', ')}`);
                }
                stats.category.failed++;
            }
        });

        // ====================================================================
        // 3. Handle data-formula-id displays
        // ====================================================================
        const formulaElements = document.querySelectorAll('[data-formula-id]');
        formulaElements.forEach(el => {
            const formulaId = el.getAttribute('data-formula-id');
            const formula = PM.formula(formulaId);

            if (formula) {
                // If element is empty, populate with formula HTML
                if (!el.innerHTML.trim() || el.classList.contains('pm-formula-auto')) {
                    el.innerHTML = formula.html || formula.latex || '';
                    el.classList.add('pm-formula-auto');
                }
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.setAttribute('title', formula.description || '');
                stats.formula.loaded++;
            } else if (!PM._loaded) {
                if (!el.innerHTML.trim()) {
                    el.textContent = '...';
                }
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                const errorMsg = `ERROR: Formula not found in theory_output.json: "${formulaId}"`;
                el.setAttribute('title', errorMsg);
                if (!el.innerHTML.trim()) {
                    el.textContent = '?';
                }
                if (window.PM_DEBUG) {
                    console.error(`PM: Formula not found: ${formulaId}`);
                }
                stats.formula.failed++;
            }
        });

        // ====================================================================
        // 4. Handle data-stat-id displays (from PM_STATS or statistics)
        // ====================================================================
        const statElements = document.querySelectorAll('[data-stat-id]');
        statElements.forEach(el => {
            const statId = el.getAttribute('data-stat-id');
            const format = el.getAttribute('data-format');
            let value = null;
            const triedSources = [];

            // Strategy 1: Try PM_STATS if available (computed stats)
            if (typeof window.PM_STATS !== 'undefined') {
                triedSources.push('PM_STATS');
                value = window.PM_STATS[statId];
                if (value === undefined && typeof window.PM_STATS.get === 'function') {
                    value = window.PM_STATS.get(statId);
                }
            }

            // Strategy 2: Try statistics section in theory_output.json
            if (value === null || value === undefined) {
                triedSources.push('statistics');
                value = PM.statistics?.[statId];
            }

            // Strategy 3: Try dotted path in full data (e.g., "simulations.proton_decay.tau_p_years")
            if ((value === null || value === undefined) && statId.includes('.')) {
                triedSources.push('dotted path');
                value = PM.get(statId);
            }

            // Strategy 4: Try validation_summary array
            if (value === null || value === undefined) {
                triedSources.push('validation_summary');
                const validationItem = PM.validationSummary.find(item => item.name === statId || item.id === statId);
                if (validationItem) {
                    value = validationItem.value ?? validationItem;
                }
            }

            if (value !== null && value !== undefined) {
                el.textContent = formatValue(value, format);
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.removeAttribute('title');
                stats.stat.loaded++;
            } else if (!PM._loaded) {
                el.textContent = '...';
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.textContent = '?';
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                const errorMsg = `ERROR: Stat not found in theory_output.json: "${statId}"\nTried sources: ${triedSources.join(', ')}`;
                el.setAttribute('title', errorMsg);
                if (window.PM_DEBUG) {
                    console.error(`PM: Stat not found: ${statId} (tried: ${triedSources.join(', ')})`);
                }
                stats.stat.failed++;
            }
        });

        // ====================================================================
        // Summary Report
        // ====================================================================
        if (PM._loaded) {
            const total = stats.pmValue.loaded + stats.category.loaded + stats.formula.loaded + stats.stat.loaded;
            const failed = stats.pmValue.failed + stats.category.failed + stats.formula.failed + stats.stat.failed;

            if (total > 0 || failed > 0) {
                console.log(`%cPM: Updated ${total} elements`, 'color: green; font-weight: bold');
                if (stats.pmValue.loaded > 0) console.log(`  data-pm-value: ${stats.pmValue.loaded} loaded`);
                if (stats.category.loaded > 0) console.log(`  data-category: ${stats.category.loaded} loaded`);
                if (stats.formula.loaded > 0) console.log(`  data-formula-id: ${stats.formula.loaded} loaded`);
                if (stats.stat.loaded > 0) console.log(`  data-stat-id: ${stats.stat.loaded} loaded`);

                if (failed > 0) {
                    console.warn(`%cPM: ${failed} elements failed to load (hover over "?" for details)`, 'color: orange; font-weight: bold');
                    if (stats.pmValue.failed > 0) console.warn(`  data-pm-value: ${stats.pmValue.failed} failed`);
                    if (stats.category.failed > 0) console.warn(`  data-category: ${stats.category.failed} failed`);
                    if (stats.formula.failed > 0) console.warn(`  data-formula-id: ${stats.formula.failed} failed`);
                    if (stats.stat.failed > 0) console.warn(`  data-stat-id: ${stats.stat.failed} failed`);
                    console.warn('  Set window.PM_DEBUG = true for detailed error logs');
                }
            }
        }
    }

    // ========================================================================
    // MATHJAX INTEGRATION
    // ========================================================================

    function signalMathJax() {
        // Signal MathJax to typeset after PM values are loaded
        if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
            console.log('PM: Signaling MathJax to typeset...');
            MathJax.typesetPromise().catch((err) => {
                console.warn('PM: MathJax typeset error:', err);
            });
        } else if (typeof MathJax !== 'undefined' && MathJax.Hub) {
            // MathJax v2
            MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
        }
    }

    // ========================================================================
    // PUBLIC API
    // ========================================================================

    PM.load = loadConstants;
    PM.refresh = loadConstants;
    PM.updateDOM = updateDOM;
    PM.formatValue = formatValue;
    PM.signalMathJax = signalMathJax;

    // Export globally
    window.PM = PM;

    console.log('PM: Constants loader ready (v2.2.0 - Enhanced path resolution)');

    // ========================================================================
    // MUTATION OBSERVER - Re-process when new elements are added
    // ========================================================================

    function initMutationObserver() {
        if (!window.MutationObserver) return;

        const observer = new MutationObserver(function(mutations) {
            let needsUpdate = false;
            for (const mutation of mutations) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Check if any added nodes have pm-value attributes
                    for (const node of mutation.addedNodes) {
                        if (node.nodeType === 1) { // Element node
                            if (node.hasAttribute && (
                                node.hasAttribute('data-pm-value') ||
                                node.hasAttribute('data-category') ||
                                node.hasAttribute('data-formula-id') ||
                                node.hasAttribute('data-stat-id') ||
                                node.querySelector('[data-pm-value], [data-category], [data-formula-id], [data-stat-id]')
                            )) {
                                needsUpdate = true;
                                break;
                            }
                        }
                    }
                }
                if (needsUpdate) break;
            }

            if (needsUpdate && PM._loaded) {
                // Debounce updates
                clearTimeout(observer._timeout);
                observer._timeout = setTimeout(updateDOM, 50);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        console.log('PM: MutationObserver initialized - will auto-update dynamic content');
    }

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            loadConstants();
            initMutationObserver();
        });
    } else {
        loadConstants();
        initMutationObserver();
    }

    // Refresh on visibility change
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && PM._loaded) {
            setTimeout(updateDOM, 100);
        }
    });

})();
