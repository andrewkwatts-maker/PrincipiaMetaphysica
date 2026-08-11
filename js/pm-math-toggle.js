/**
 * Per-card Math-Mode Toggle
 * =========================
 * Handles the Normal-Math / EML-Math switch that appears inside individual
 * formula, parameter, and foundation cards. Uses event delegation on the
 * document so newly-injected cards (dynamic renders) pick up the behaviour
 * automatically — no init call needed per card.
 *
 * Markup convention (see css/pm-common.css for the CSS scope rules):
 *
 *   <div class="math-scope" data-math-mode="normal">
 *     <div class="math-toggle" role="group" aria-label="Math notation">
 *       <button type="button" class="math-toggle-btn" data-mode="normal"
 *               aria-pressed="true">Normal</button>
 *       <button type="button" class="math-toggle-btn" data-mode="eml"
 *               aria-pressed="false">EML</button>
 *     </div>
 *     <div class="math-mode-block" data-mode="normal">…standard…</div>
 *     <div class="math-mode-block" data-mode="eml">…EML…</div>
 *   </div>
 *
 * A single mutation observer syncs button aria-pressed state whenever the
 * scope's data-math-mode attribute changes (including programmatic changes).
 */

const CLICK_HANDLER_KEY = '__pmMathToggleWired__';

function getScopeFor(el) {
    return el.closest('.math-scope, [data-math-mode]');
}

function syncButtons(scope) {
    if (!scope) return;
    const mode = scope.getAttribute('data-math-mode') || 'normal';
    scope.querySelectorAll(':scope > .math-toggle .math-toggle-btn, :scope > * > .math-toggle .math-toggle-btn, :scope .math-toggle > .math-toggle-btn').forEach(btn => {
        // Only sync buttons whose closest scope is *this* scope (avoids
        // grabbing pills from nested cards).
        if (getScopeFor(btn.parentElement) !== scope) return;
        const isActive = btn.dataset.mode === mode;
        btn.setAttribute('aria-pressed', String(isActive));
    });
}

function handleClick(event) {
    const btn = event.target.closest('.math-toggle-btn');
    if (!btn) return;
    const scope = getScopeFor(btn);
    if (!scope) return;
    const mode = btn.dataset.mode;
    if (!mode || (mode !== 'normal' && mode !== 'eml')) return;
    event.preventDefault();
    scope.setAttribute('data-math-mode', mode);
    syncButtons(scope);
    // If MathJax is present and the newly-visible variant hasn't rendered
    // yet (e.g. because it was `display:none` at initial typeset time),
    // ask MathJax to typeset this scope. Safe to call repeatedly.
    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([scope]).catch(() => {});
    }
}

function initExistingScopes(root) {
    (root || document).querySelectorAll('.math-scope, [data-math-mode]').forEach(scope => {
        // Ensure a default mode
        if (!scope.hasAttribute('data-math-mode')) {
            scope.setAttribute('data-math-mode', 'normal');
        }
        syncButtons(scope);
    });
}

function ensureDelegateWired() {
    if (document[CLICK_HANDLER_KEY]) return;
    document[CLICK_HANDLER_KEY] = true;
    document.addEventListener('click', handleClick);
}

// Auto-init on load. Also expose an init function so callers that
// re-render cards after this module ran can force a re-sync.
export function initMathToggles(root) {
    ensureDelegateWired();
    initExistingScopes(root);
}

if (typeof window !== 'undefined') {
    ensureDelegateWired();
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => initExistingScopes());
    } else {
        initExistingScopes();
    }
    // Re-scan whenever new content is injected (formula/param/foundation
    // cards render asynchronously). Debounced with a microtask.
    let scanPending = false;
    const scheduleScan = () => {
        if (scanPending) return;
        scanPending = true;
        queueMicrotask(() => {
            scanPending = false;
            initExistingScopes();
        });
    };
    const observer = new MutationObserver(mutations => {
        for (const m of mutations) {
            if (m.type === 'childList' && m.addedNodes.length) {
                for (const node of m.addedNodes) {
                    if (node.nodeType !== 1) continue;
                    if (node.matches?.('.math-scope, [data-math-mode]') ||
                        node.querySelector?.('.math-scope, [data-math-mode]')) {
                        scheduleScan();
                        return;
                    }
                }
            }
        }
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    // Expose for debugging.
    window.pmInitMathToggles = initMathToggles;
}
