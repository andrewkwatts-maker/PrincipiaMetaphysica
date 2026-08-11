/**
 * Speculation Toggle
 * ==================
 * Global toggle for showing/hiding speculative content blocks.
 *
 * (The former global Normal-Math / EML-Math toggle was retired in favour
 * of per-card toggles — see js/pm-math-toggle.js. Any legacy callers of
 * getMathMode/setMathMode/initMathMode/toggleMathMode still resolve to
 * safe no-ops so nothing hard-fails during the transition.)
 *
 * Speculation: persisted in localStorage, applied as data-speculation="show" on <html>.
 * Default is OFF (no attribute) — speculation blocks hidden by CSS.
 *
 * Events:
 *   'pm-speculation-changed'  → { show: boolean }
 */

const SPECULATION_KEY = 'pm-speculation';

export function getSpeculationMode() {
    return localStorage.getItem(SPECULATION_KEY) === 'show';
}

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

export function initSpeculationMode() {
    if (getSpeculationMode()) {
        document.documentElement.setAttribute('data-speculation', 'show');
    } else {
        document.documentElement.removeAttribute('data-speculation');
    }
}

export function toggleSpeculationMode() {
    setSpeculationMode(!getSpeculationMode());
}

// ── Legacy no-ops (kept so old inline scripts don't ReferenceError) ──────────
export function getMathMode() { return 'per-card'; }
export function setMathMode() {}
export function initMathMode() {}
export function toggleMathMode() {}
