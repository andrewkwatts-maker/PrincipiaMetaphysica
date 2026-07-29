/**
 * Math Mode Manager + Speculation Toggle
 * =======================================
 * Global state for switching between Normal Math and EML Math display modes,
 * and for showing/hiding speculative content blocks.
 *
 * Usage:
 *   import { getMathMode, setMathMode, initMathMode,
 *            getSpeculationMode, setSpeculationMode, initSpeculationMode } from './math-mode.js';
 *
 * Math mode: persisted in localStorage, applied as data-math-mode="normal|eml" on <html>.
 * Speculation: persisted in localStorage, applied as data-speculation="show" on <html>.
 *   Default is OFF (no attribute) — speculation blocks hidden by CSS.
 *
 * Events:
 *   'pm-math-mode-changed'    → { mode, previous }
 *   'pm-speculation-changed'  → { show: boolean }
 */

const STORAGE_KEY = 'pm-math-mode';
const VALID_MODES = ['normal', 'eml'];
const DEFAULT_MODE = 'normal';

// ── Speculation toggle ──────────────────────────────────────────────────────

const SPECULATION_KEY = 'pm-speculation';

/** Returns true if speculation content should be visible. */
export function getSpeculationMode() {
    return localStorage.getItem(SPECULATION_KEY) === 'show';
}

/** Show or hide speculation blocks. Persists choice. */
export function setSpeculationMode(show) {
    if (show) {
        localStorage.setItem(SPECULATION_KEY, 'show');
        document.documentElement.setAttribute('data-speculation', 'show');
    } else {
        localStorage.removeItem(SPECULATION_KEY);
        document.documentElement.removeAttribute('data-speculation');
    }
    window.dispatchEvent(new CustomEvent('pm-speculation-changed', {
        detail: { show },
        bubbles: false,
    }));
}

/** Apply stored speculation preference to DOM on page load. */
export function initSpeculationMode() {
    if (getSpeculationMode()) {
        document.documentElement.setAttribute('data-speculation', 'show');
    } else {
        document.documentElement.removeAttribute('data-speculation');
    }
}

/** Toggle speculation visibility. */
export function toggleSpeculationMode() {
    setSpeculationMode(!getSpeculationMode());
}

/**
 * Get the current math display mode.
 * @returns {'normal' | 'eml'}
 */
export function getMathMode() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return VALID_MODES.includes(stored) ? stored : DEFAULT_MODE;
}

/**
 * Set the math display mode and persist it.
 * Applies data-math-mode attribute to <html> and dispatches event.
 * @param {'normal' | 'eml'} mode
 */
export function setMathMode(mode) {
    if (!VALID_MODES.includes(mode)) {
        console.warn(`[MathMode] Invalid mode "${mode}". Use "normal" or "eml".`);
        return;
    }
    const previous = getMathMode();
    if (mode === previous) return;

    localStorage.setItem(STORAGE_KEY, mode);
    applyMathModeToDOM(mode);

    window.dispatchEvent(new CustomEvent('pm-math-mode-changed', {
        detail: { mode, previous },
        bubbles: false,
    }));
}

/**
 * Apply the current mode to the DOM without dispatching an event.
 * Called during page init to avoid triggering re-render on load.
 */
export function initMathMode() {
    applyMathModeToDOM(getMathMode());
}

/**
 * Toggle between normal and eml modes.
 */
export function toggleMathMode() {
    setMathMode(getMathMode() === 'normal' ? 'eml' : 'normal');
}

/**
 * Apply data-math-mode attribute to <html> element.
 * @param {string} mode
 */
function applyMathModeToDOM(mode) {
    document.documentElement.setAttribute('data-math-mode', mode);
}
