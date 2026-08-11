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

/**
 * Sync every <details class="speculation-block"> on the page to the
 * requested open/closed state. The panel summary chip stays visible in
 * both states (so readers always see where speculation lives); only the
 * expanded body toggles. Users can still click individual summaries to
 * expand/collapse a single panel afterwards.
 *
 * Reaches into declared shadow roots (pm-section shadow DOMs) so section
 * content behaves the same as light-DOM content.
 */
function _applySpeculationToAllPanels(open) {
    const walk = (root) => {
        if (!root || !root.querySelectorAll) return;
        root.querySelectorAll('.speculation-block').forEach(el => {
            if (el.tagName === 'DETAILS') {
                if (open) el.setAttribute('open', '');
                else el.removeAttribute('open');
            }
        });
        // Also descend into any shadow roots that carry speculation panels
        // (pm-section is the primary case).
        root.querySelectorAll('*').forEach(el => {
            if (el.shadowRoot) walk(el.shadowRoot);
        });
    };
    walk(document);
}

export function setSpeculationMode(show) {
    if (show) {
        localStorage.setItem(SPECULATION_KEY, 'show');
        document.documentElement.setAttribute('data-speculation', 'show');
    } else {
        localStorage.removeItem(SPECULATION_KEY);
        document.documentElement.removeAttribute('data-speculation');
    }
    _applySpeculationToAllPanels(!!show);
    window.dispatchEvent(new CustomEvent('pm-speculation-changed', {
        detail: { show },
        bubbles: false,
    }));
}

export function initSpeculationMode() {
    const show = getSpeculationMode();
    if (show) {
        document.documentElement.setAttribute('data-speculation', 'show');
    } else {
        document.documentElement.removeAttribute('data-speculation');
    }
    // Apply to any panels already in the DOM (later-injected panels
    // are handled by pm-section-renderer and by an observer here).
    _applySpeculationToAllPanels(show);
    _startObserver();
}

export function toggleSpeculationMode() {
    setSpeculationMode(!getSpeculationMode());
}

// ── Observer: sync newly-injected speculation panels to current state ──
let _observerStarted = false;
function _startObserver() {
    if (_observerStarted || typeof window === 'undefined') return;
    _observerStarted = true;
    const mo = new MutationObserver(mutations => {
        const show = getSpeculationMode();
        for (const m of mutations) {
            if (m.type !== 'childList') continue;
            for (const node of m.addedNodes) {
                if (node.nodeType !== 1) continue;
                const isPanel = node.classList?.contains('speculation-block') && node.tagName === 'DETAILS';
                const hasPanels = node.querySelectorAll?.('details.speculation-block').length > 0;
                if (isPanel || hasPanels) {
                    _applySpeculationToAllPanels(show);
                    return;
                }
            }
        }
    });
    mo.observe(document.documentElement, { childList: true, subtree: true });
}

// ── Legacy no-ops (kept so old inline scripts don't ReferenceError) ──────────
export function getMathMode() { return 'per-card'; }
export function setMathMode() {}
export function initMathMode() {}
export function toggleMathMode() {}
