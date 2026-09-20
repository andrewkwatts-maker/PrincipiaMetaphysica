/**
 * Site-wide Layperson / Full toggle
 * =================================
 * A second reading axis, orthogonal to the Normal-Math / EML-Math switch in
 * pm-math-toggle.js. That one chooses NOTATION per card; this one chooses
 * READING LEVEL for the whole page, so a visitor sets it once rather than per
 * card. All four combinations render.
 *
 * Markup convention, deliberately parallel to the math toggle so the two are
 * learned once:
 *
 *   <div class="reading-toggle" role="group" aria-label="Reading level">
 *     <button type="button" class="reading-toggle-btn" data-level="layperson"
 *             aria-pressed="false">Layperson</button>
 *     <button type="button" class="reading-toggle-btn" data-level="full"
 *             aria-pressed="true">Full</button>
 *   </div>
 *
 *   <div class="reading-block" data-level="layperson">plain statement</div>
 *   <div class="reading-block" data-level="full">the derivation</div>
 *
 * The level lives on <html data-reading-level>, so CSS hides the blocks that do
 * not match and nothing needs re-rendering. Event delegation on the document
 * means dynamically injected cards pick the behaviour up with no init call.
 *
 * WHY BOTH REGISTERS ARE REQUIRED, not merely offered
 * ---------------------------------------------------
 * A derivation whose plain statement cannot be written without hand-waving is a
 * derivation that does not exist. The plain register is therefore an audit
 * instrument as much as a courtesy, and a missing one is a finding rather than
 * a formatting gap. The build enforces presence; this file only renders.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const STORAGE_KEY = 'pm-reading-level';
const LEVELS = ['layperson', 'full'];
const DEFAULT_LEVEL = 'full';
const WIRED_KEY = '__pmLaypersonToggleWired__';

function normalise(level) {
    return LEVELS.indexOf(level) === -1 ? DEFAULT_LEVEL : level;
}

function storedLevel() {
    try {
        return normalise(window.localStorage.getItem(STORAGE_KEY));
    } catch (err) {
        // Private mode, or storage disabled. The toggle still works for the
        // session; it simply does not persist.
        return DEFAULT_LEVEL;
    }
}

function persist(level) {
    try {
        window.localStorage.setItem(STORAGE_KEY, level);
    } catch (err) {
        /* not fatal - see storedLevel */
    }
}

function syncButtons(level) {
    document.querySelectorAll('.reading-toggle-btn').forEach((btn) => {
        btn.setAttribute('aria-pressed', String(btn.dataset.level === level));
    });
}

/**
 * Apply a reading level to the document.
 *
 * Exported so a page can set it programmatically (for example a deep link that
 * should open in plain language) without faking a click.
 */
export function setReadingLevel(level, options) {
    const next = normalise(level);
    const root = document.documentElement;
    if (root.getAttribute('data-reading-level') !== next) {
        root.setAttribute('data-reading-level', next);
    }
    syncButtons(next);
    if (!options || options.persist !== false) {
        persist(next);
    }
    document.dispatchEvent(new CustomEvent('pm:reading-level', {
        detail: { level: next },
    }));
    return next;
}

export function getReadingLevel() {
    return normalise(document.documentElement.getAttribute('data-reading-level'));
}

function handleClick(event) {
    const btn = event.target.closest('.reading-toggle-btn');
    if (!btn) return;
    const level = btn.dataset.level;
    if (LEVELS.indexOf(level) === -1) return;
    event.preventDefault();
    setReadingLevel(level);
}

function handleKeydown(event) {
    // Left/Right move between the two pills, matching the ARIA group pattern.
    const btn = event.target.closest('.reading-toggle-btn');
    if (!btn) return;
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    const group = btn.closest('.reading-toggle');
    if (!group) return;
    const pills = Array.from(group.querySelectorAll('.reading-toggle-btn'));
    const idx = pills.indexOf(btn);
    if (idx === -1) return;
    const delta = event.key === 'ArrowRight' ? 1 : -1;
    const target = pills[(idx + delta + pills.length) % pills.length];
    event.preventDefault();
    target.focus();
    setReadingLevel(target.dataset.level);
}

export function initLaypersonToggle() {
    if (document[WIRED_KEY]) {
        // Already wired; just re-sync, since new pills may have been injected.
        syncButtons(getReadingLevel());
        return;
    }
    document[WIRED_KEY] = true;
    document.addEventListener('click', handleClick);
    document.addEventListener('keydown', handleKeydown);
    setReadingLevel(storedLevel(), { persist: false });
}

if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLaypersonToggle);
    } else {
        initLaypersonToggle();
    }
}

export default { initLaypersonToggle, setReadingLevel, getReadingLevel };
