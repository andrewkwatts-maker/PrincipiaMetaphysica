/* Pure helpers for the "reasonable alternative" glow on the paths graph.
 * Usable in the browser (window.PMPathsGlow) and in node (module.exports). */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PMPathsGlow = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function isReasonable(node) {
    var a = node && node.attrs;
    return !!(a && a.reasonable && !a.on_active_path);
  }

  // The CSS class a node group gets: the gold path never glows as an alternative.
  function glowClass(node) {
    return isReasonable(node) ? ' pp-reasonable' : '';
  }

  function fmt(x) {
    return typeof x === 'number' ? (Math.round(x * 100) / 100).toString() : 'n/a';
  }

  // [label, value] rows for the inspector; empty when the node is not a reasonable alternative.
  function inspectorRows(node, ranking) {
    if (!isReasonable(node)) return [];
    var a = node.attrs;
    return [['Rank', a.rank === null || a.rank === undefined ? 'n/a' : String(a.rank)],
      ['\u0394\u03c7\u00b2 against the selected path', fmt(a.delta_chi2)],
      ['Why it is reasonable', (ranking && ranking.reasonable_rule) || 'not stated']];
  }

  // Path ids of option nodes marked reasonable, for the path list.
  function reasonableOptionKeys(nodes) {
    var out = {};
    (nodes || []).forEach(function (n) {
      if (n.type === 'option' && isReasonable(n) && n.attrs.fork) out[n.attrs.fork + '--' + n.label] = true;
    });
    return out;
  }

  return { isReasonable: isReasonable, glowClass: glowClass, inspectorRows: inspectorRows,
    reasonableOptionKeys: reasonableOptionKeys };
});
