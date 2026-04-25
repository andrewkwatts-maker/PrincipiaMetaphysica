/**
 * Math Mode Manager
 * =================
 * Global state for switching between Normal Math and EML Math display modes.
 *
 * Usage:
 *   import { getMathMode, setMathMode, initMathMode } from './math-mode.js';
 *
 * The mode is persisted in localStorage and applied as a data attribute on
 * <html data-math-mode="normal|eml"> so CSS can switch formula/text blocks.
 *
 * Event: 'pm-math-mode-changed' dispatched on window whenever mode changes.
 *   event.detail = { mode: 'normal' | 'eml', previous: 'normal' | 'eml' }
 */

const STORAGE_KEY = 'pm-math-mode';
const VALID_MODES = ['normal', 'eml'];
const DEFAULT_MODE = 'normal';

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
