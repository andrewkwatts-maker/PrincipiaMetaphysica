/*
 * The one MathJax configuration for every page (loaded before the pinned
 * mathjax@3.2.2 script). tools/texcheck/check.js evaluates this same file, so
 * the render gate and the site cannot drift. Keep it plain data: no page
 * specific code, and no reference to `document`.
 */
window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true,
        processEnvironments: true,
        tags: 'ams',
        macros: {
            shadow: '\\text{shadow}',
            kgimel: 'k_{\\gimel}',
            // Force displaystyle for fractions in display mode.
            dfrac: ['\\displaystyle\\frac{#1}{#2}', 2],
            // Feynman slash: a solidus overlaid on the symbol (MathJax has no \slashed).
            slashed: ['{\\rlap{\\,/}#1}', 1]
        }
    },
    options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
        ignoreHtmlClass: 'pm-value|pm-loaded|pm-loading|pm-error|mathjax-ignore'
    },
    chtml: {
        scale: 1.0,
        minScale: 0.5,
        matchFontHeight: true,
        displayAlign: 'center',
        displayIndent: '0'
    }
};
