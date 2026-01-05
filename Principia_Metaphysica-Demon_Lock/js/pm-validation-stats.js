/**
 * Principia Metaphysica - Validation Statistics (Dynamic Loader)
 * ===============================================================
 *
 * Dynamically loads ALL statistics from theory_output.json.
 * NO HARDCODED VALUES - Single source of truth from Python simulations.
 *
 * Usage:
 *   <span class="pm-stat" data-stat-id="total_parameters"></span>
 *   <span data-stat-id="success_rate_1sigma"></span>
 *   <span data-stat-id="simulations.proton_decay.tau_p_years"></span>
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 * Version: 2.0.0 - Dynamic loader (no hardcoded values)
 */

(function() {
    'use strict';

    // ========================================================================
    // PM_STATS - Dynamically populated from theory_output.json
    // ========================================================================

    const PM_STATS = {
        // State
        _loaded: false,
        _loading: null,
        _data: null,
        _error: null,

        // ====================================================================
        // DYNAMIC GETTERS - Compute from loaded data
        // ====================================================================

        get total_parameters() {
            return this._data?.statistics?.total_parameters ??
                   this._data?.formulas?.count ??
                   '...';
        },

        get geometric_count() {
            // Count formulas with category != CALIBRATED
            if (!this._data?.formulas?.formulas) return '...';
            const formulas = Object.values(this._data.formulas.formulas);
            return formulas.filter(f => f.category !== 'CALIBRATED').length;
        },

        get derived_count() {
            if (!this._data?.formulas?.formulas) return '...';
            const formulas = Object.values(this._data.formulas.formulas);
            return formulas.filter(f => f.category === 'DERIVED').length;
        },

        get calibrated_count() {
            if (!this._data?.formulas?.formulas) return '...';
            const formulas = Object.values(this._data.formulas.formulas);
            return formulas.filter(f => f.category === 'CALIBRATED').length;
        },

        get exact_count() {
            if (!this._data?.formulas?.formulas) return '...';
            const formulas = Object.values(this._data.formulas.formulas);
            return formulas.filter(f => f.sigmaDeviation === 0).length;
        },

        get total_validations() {
            return this._data?.validation_summary?.length ?? '...';
        },

        get validations_passed() {
            if (!this._data?.validation_summary) return '...';
            return this._data.validation_summary.filter(v => v[1] === 'PASS').length;
        },

        get validations_failed() {
            if (!this._data?.validation_summary) return '...';
            return this._data.validation_summary.filter(v => v[1] === 'FAIL').length;
        },

        get testable_predictions() {
            return this._data?.formulas?.count ?? '...';
        },

        get within_1sigma() {
            return this._data?.statistics?.within_1sigma ?? '...';
        },

        get within_2sigma() {
            return this._data?.statistics?.within_2sigma ?? '...';
        },

        get within_3sigma() {
            return this._data?.statistics?.within_3sigma ?? '...';
        },

        get exact_matches() {
            return this._data?.statistics?.exact_matches ?? '...';
        },

        get mean_sigma() {
            const val = this._data?.statistics?.mean_sigma;
            return val !== undefined ? val.toFixed(2) : '...';
        },

        get max_sigma() {
            const sigmas = this._data?.statistics?.sigmas;
            if (!sigmas || sigmas.length === 0) return '...';
            return Math.max(...sigmas).toFixed(2);
        },

        // ====================================================================
        // COMPUTED PERCENTAGES
        // ====================================================================

        get success_rate_1sigma() {
            const w = this.within_1sigma;
            const t = this.testable_predictions;
            if (w === '...' || t === '...') return '...';
            return (100 * w / t).toFixed(1);
        },

        get success_rate_2sigma() {
            const w = this.within_2sigma;
            const t = this.testable_predictions;
            if (w === '...' || t === '...') return '...';
            return (100 * w / t).toFixed(1);
        },

        get success_rate_3sigma() {
            const w = this.within_3sigma;
            const t = this.testable_predictions;
            if (w === '...' || t === '...') return '...';
            return (100 * w / t).toFixed(1);
        },

        get validation_success_rate() {
            const p = this.validations_passed;
            const t = this.total_validations;
            if (p === '...' || t === '...') return '...';
            return (100 * p / t).toFixed(1);
        },

        get geometric_percentage() {
            const g = this.geometric_count;
            const t = this.total_parameters;
            if (g === '...' || t === '...') return '...';
            return (100 * g / t).toFixed(1);
        },

        // ====================================================================
        // FORMATTED SUMMARIES
        // ====================================================================

        get geometric_fraction() {
            return `${this.geometric_count}/${this.total_parameters}`;
        },

        get validation_summary() {
            return `${this.within_1sigma}/${this.testable_predictions}`;
        },

        get validation_summary_percent() {
            return `${this.within_1sigma}/${this.testable_predictions} (${this.success_rate_1sigma}%)`;
        },

        get summary_short() {
            return `${this.within_1sigma}/${this.testable_predictions} within 1σ, ${this.exact_matches} exact`;
        },

        // ====================================================================
        // SIMULATION DATA ACCESS
        // ====================================================================

        getSimulation(path) {
            if (!this._data?.simulations) return null;
            const parts = path.split('.');
            let value = this._data.simulations;
            for (const part of parts) {
                if (value && typeof value === 'object' && part in value) {
                    value = value[part];
                } else {
                    return null;
                }
            }
            return value;
        },

        // ====================================================================
        // DEEP PATH ACCESS (for data-stat-id="simulations.proton_decay.tau_p_years")
        // ====================================================================

        get(path) {
            // First check if it's a direct property
            if (path in this && typeof this[path] !== 'function') {
                return this[path];
            }

            // Then try as a path in _data
            if (!this._data) return '...';

            const parts = path.split('.');
            let value = this._data;
            for (const part of parts) {
                if (value && typeof value === 'object' && part in value) {
                    value = value[part];
                } else {
                    return null;
                }
            }
            return value;
        }
    };

    // ========================================================================
    // LOADING FROM theory_output.json
    // ========================================================================

    async function loadStats() {
        if (PM_STATS._loaded) return true;
        if (PM_STATS._loading) return PM_STATS._loading;

        PM_STATS._loading = (async () => {
            const pathPrefixes = [
                '',           // Same directory
                '../',        // Parent directory
                '../../',     // Two levels up
            ];

            for (const prefix of pathPrefixes) {
                try {
                    const testPath = prefix + 'theory_output.json';
                    const response = await fetch(testPath);
                    if (response.ok) {
                        const data = await response.json();
                        PM_STATS._data = data;
                        PM_STATS._loaded = true;
                        console.log(`PM_STATS: Loaded from ${testPath}`);
                        console.log(`  Version: ${data.version || 'unknown'}`);
                        console.log(`  Validations: ${data.validation_summary?.length || 0}`);
                        console.log(`  Formulas: ${data.formulas?.count || 0}`);
                        updateDOM();
                        return true;
                    }
                } catch (e) {
                    continue;
                }
            }

            PM_STATS._error = 'theory_output.json not found';
            console.error('PM_STATS: Failed to load theory_output.json');
            console.error('  Run: python run_all_simulations.py --export');
            updateDOM(); // Will show '...' placeholders
            return false;
        })();

        return PM_STATS._loading;
    }

    // ========================================================================
    // DOM MANIPULATION
    // ========================================================================

    function updateDOM() {
        const elements = document.querySelectorAll('.pm-stat, [data-stat-id]');
        let updated = 0;

        elements.forEach(el => {
            const statId = el.dataset.statId || el.getAttribute('data-stat-id');
            if (!statId) return;

            // Try to get the value
            let value = PM_STATS.get(statId);

            if (value !== null && value !== undefined) {
                // Format numbers nicely
                if (typeof value === 'number') {
                    if (Math.abs(value) >= 1e10 || (Math.abs(value) < 0.01 && value !== 0)) {
                        value = value.toExponential(2);
                    } else if (Number.isInteger(value)) {
                        value = value.toString();
                    } else {
                        value = value.toFixed(2);
                    }
                }
                el.textContent = value;
                el.classList.add('pm-stat-loaded');
                el.classList.remove('pm-stat-error');
                updated++;
            } else if (!PM_STATS._loaded) {
                el.textContent = '...';
                el.classList.add('pm-stat-loading');
            } else {
                el.textContent = '?';
                el.classList.add('pm-stat-error');
                console.warn(`PM_STATS: Unknown stat ID: ${statId}`);
            }
        });

        if (updated > 0) {
            console.log(`PM_STATS: Updated ${updated} DOM element(s)`);
        }
    }

    // ========================================================================
    // PUBLIC API
    // ========================================================================

    PM_STATS.update = loadStats;
    PM_STATS.refresh = loadStats;
    PM_STATS.updateDOM = updateDOM;

    // Export globally
    window.PM_STATS = PM_STATS;

    console.log('PM_STATS: Module loaded (v2.0.0 - dynamic loader)');

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadStats);
    } else {
        loadStats();
    }

    // Refresh on visibility change
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && PM_STATS._loaded) {
            setTimeout(updateDOM, 100);
        }
    });

})();
