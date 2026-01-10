/**
 * observer-heartbeat.js - Runtime Integrity Hook for Principia Metaphysica
 *
 * v17.2 Observer Coupling (CERT-OBSV-041) Runtime Implementation
 *
 * This module implements the Observer Heartbeat - a runtime parity check
 * that prevents floating-point "rounding debt" from accumulating during
 * simulation execution. If numerical hysteresis is detected, values are
 * snapped back to their G2-residue locked values.
 *
 * Certificate: CERT-OBSV-041 (Observer Coupling & Decidability)
 * Certificate: CERT-HYST-042 (Time-Reversibility & Symplectic Integrity)
 *
 * Generated: 2026-01-01
 * Framework Version: v17.2
 */

const ObserverHeartbeat = {
    // Configuration
    config: {
        epoch_interval: 10000,      // Check every 10k iterations
        tolerance: 1e-12,           // Maximum allowed drift
        strict_mode: true,          // Throw on violation if true
        log_level: 'warn',          // 'silent', 'warn', 'error', 'verbose'
    },

    // Registry of locked G2-residue values
    _lockedResidues: new Map(),

    // Heartbeat statistics
    _stats: {
        checks_performed: 0,
        violations_detected: 0,
        corrections_applied: 0,
        last_check_timestamp: null,
    },

    /**
     * Initialize the Observer Heartbeat with locked residue values.
     *
     * @param {Object} residues - Object mapping parameter names to locked values
     * @param {Object} config - Optional configuration overrides
     */
    initialize(residues, config = {}) {
        // Merge configuration
        this.config = { ...this.config, ...config };

        // Lock the residue values
        for (const [key, value] of Object.entries(residues)) {
            this._lockedResidues.set(key, {
                value: value,
                source: 'G2_RESIDUE',
                locked_at: new Date().toISOString(),
                verification: 'LOCKED',
            });
        }

        this._log('info', `Observer Heartbeat initialized with ${this._lockedResidues.size} locked residues`);
        return this;
    },

    /**
     * Register a single residue value as locked.
     *
     * @param {string} key - Parameter identifier
     * @param {number} value - Locked value
     * @param {string} source - Source certificate or derivation
     */
    lockResidue(key, value, source = 'G2_RESIDUE') {
        this._lockedResidues.set(key, {
            value: value,
            source: source,
            locked_at: new Date().toISOString(),
            verification: 'LOCKED',
        });
    },

    /**
     * Check observer parity for a set of current residue values.
     * Returns 1.0 if parity is maintained, < 1.0 if drift detected.
     *
     * Implements CERT-OBSV-041 validation logic.
     *
     * @param {Object} currentResidues - Current computed values to check
     * @returns {number} Parity value (1.0 = perfect, < 1.0 = drift detected)
     */
    checkObserverParity(currentResidues) {
        this._stats.checks_performed++;
        this._stats.last_check_timestamp = new Date().toISOString();

        let maxDrift = 0;
        const violations = [];

        for (const [key, lockedData] of this._lockedResidues) {
            const currentValue = currentResidues[key];

            if (currentValue === undefined) {
                continue; // Skip if parameter not in current set
            }

            const lockedValue = lockedData.value;
            const drift = Math.abs(currentValue - lockedValue);
            const relativeDrift = lockedValue !== 0
                ? drift / Math.abs(lockedValue)
                : drift;

            if (relativeDrift > this.config.tolerance) {
                violations.push({
                    key: key,
                    locked: lockedValue,
                    current: currentValue,
                    drift: relativeDrift,
                });
                maxDrift = Math.max(maxDrift, relativeDrift);
            }
        }

        if (violations.length > 0) {
            this._stats.violations_detected++;
            this._log('warn', `C41 Warning: Numerical hysteresis detected in ${violations.length} parameter(s)`);

            for (const v of violations) {
                this._log('verbose', `  ${v.key}: locked=${v.locked}, current=${v.current}, drift=${v.drift.toExponential(2)}`);
            }
        }

        // Parity: 1.0 if no drift, decreases with drift
        return maxDrift === 0 ? 1.0 : Math.max(0, 1.0 - maxDrift * 1e10);
    },

    /**
     * Snap current values back to their locked G2-residue values.
     * Called when hysteresis is detected to restore integrity.
     *
     * Implements CERT-HYST-042 symplectic reset.
     *
     * @param {Object} currentResidues - Object to be corrected (mutated in place)
     * @returns {Object} The corrected residues object
     */
    snapToResidue(currentResidues) {
        let corrections = 0;

        for (const [key, lockedData] of this._lockedResidues) {
            if (currentResidues.hasOwnProperty(key)) {
                const currentValue = currentResidues[key];
                const lockedValue = lockedData.value;

                if (currentValue !== lockedValue) {
                    currentResidues[key] = lockedValue;
                    corrections++;
                }
            }
        }

        if (corrections > 0) {
            this._stats.corrections_applied += corrections;
            this._log('info', `Symplectic reset: Snapped ${corrections} parameter(s) to G2-residue values`);
        }

        return currentResidues;
    },

    /**
     * Run a full integrity check and auto-correct if needed.
     * This is the main runtime hook to be called at epoch boundaries.
     *
     * @param {Object} currentResidues - Current computed values
     * @returns {Object} Integrity check result
     */
    runIntegrityCheck(currentResidues) {
        const parity = this.checkObserverParity(currentResidues);

        const result = {
            timestamp: new Date().toISOString(),
            parity: parity,
            passed: parity === 1.0,
            corrected: false,
        };

        if (parity !== 1.0) {
            this._log('warn', 'C41 Warning: Numerical Hysteresis detected. Re-normalizing to G2 Manifold.');
            this.snapToResidue(currentResidues);
            result.corrected = true;

            if (this.config.strict_mode) {
                throw new Error(`Topological Lock Violation: Observer parity check failed (parity=${parity.toFixed(6)})`);
            }
        }

        return result;
    },

    /**
     * Get current heartbeat statistics.
     *
     * @returns {Object} Statistics object
     */
    getStats() {
        return {
            ...this._stats,
            locked_residue_count: this._lockedResidues.size,
            config: { ...this.config },
        };
    },

    /**
     * Create a protected registry proxy that prevents modification of locked values.
     * Any attempt to write to locked parameters will throw a HardLockError.
     *
     * @param {Object} registry - The registry object to protect
     * @returns {Proxy} Protected registry proxy
     */
    createTopologicalGuardrail(registry) {
        const lockedResidues = this._lockedResidues;
        const strictMode = this.config.strict_mode;

        return new Proxy(registry, {
            set: function(obj, prop, value) {
                if (lockedResidues.has(prop)) {
                    const lockedData = lockedResidues.get(prop);
                    const errorMsg = `Topological Lock Violation: Cannot modify ${prop}. ` +
                        `Value is G2-Residue Locked (source: ${lockedData.source}, locked: ${lockedData.locked_at})`;

                    if (strictMode) {
                        throw new Error(errorMsg);
                    } else {
                        console.warn(errorMsg);
                        return true; // Silently reject the write
                    }
                }
                obj[prop] = value;
                return true;
            },

            deleteProperty: function(obj, prop) {
                if (lockedResidues.has(prop)) {
                    throw new Error(`Topological Lock Violation: Cannot delete ${prop}. Value is G2-Residue Locked.`);
                }
                delete obj[prop];
                return true;
            },
        });
    },

    /**
     * Internal logging helper.
     */
    _log(level, message) {
        if (this.config.log_level === 'silent') return;

        const levels = ['verbose', 'info', 'warn', 'error'];
        const configLevel = levels.indexOf(this.config.log_level);
        const msgLevel = levels.indexOf(level);

        if (msgLevel >= configLevel) {
            const prefix = `[ObserverHeartbeat:${level.toUpperCase()}]`;
            switch (level) {
                case 'error':
                    console.error(prefix, message);
                    break;
                case 'warn':
                    console.warn(prefix, message);
                    break;
                default:
                    console.log(prefix, message);
            }
        }
    },
};

// Pre-load with G2 fundamental constants
ObserverHeartbeat.initialize({
    // Topological invariants (LOCKED)
    'topology.b3': 24,
    'topology.chi_eff': 144,
    'topology.k_gimel': 12.31831,
    'topology.c_kaf': 27.2,

    // Dark energy (LOCKED to -23/24)
    'cosmology.w0': -0.9583333333,  // = -23/24

    // Fundamental constants (LOCKED)
    'gauge.alpha_inverse': 137.036,
    'fermion.n_generations': 3,

    // Neutrino mass sum (LOCKED)
    'neutrino.sum_m_nu': 0.0816883,
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ObserverHeartbeat;
}

// Make available globally in browser
if (typeof window !== 'undefined') {
    window.ObserverHeartbeat = ObserverHeartbeat;
}

console.log('[ObserverHeartbeat] v17.2 Runtime integrity hook loaded');
console.log(`  Locked residues: ${ObserverHeartbeat._lockedResidues.size}`);
console.log(`  Tolerance: ${ObserverHeartbeat.config.tolerance}`);
console.log(`  Epoch interval: ${ObserverHeartbeat.config.epoch_interval}`);
