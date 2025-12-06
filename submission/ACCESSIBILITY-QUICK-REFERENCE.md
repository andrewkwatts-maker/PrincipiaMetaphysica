# Accessibility Quick Reference Guide

**For**: Principia Metaphysica APS Submission
**Agent**: Agent 5 - Accessibility & Figure Guidelines
**Date**: 2025-12-06

---

## Quick Start (5 Minutes)

### 1. Add to LaTeX Preamble

In your main `.tex` file, add these lines BEFORE `\begin{document}`:

```latex
% Include accessibility features (add near end of preamble)
\input{colorblind-setup.tex}
\input{hyperref-setup.tex}
```

### 2. Use Colorblind-Safe Colors

In your figures, use these colors:

- **Blue**: `cbBlue` - RGB(0,114,178) - Theory, primary data
- **Orange**: `cbOrange` - RGB(213,94,0) - Experiment, secondary data
- **Green**: `cbGreen` - RGB(0,158,115) - Comparisons, tertiary data

**Never use red and green together!**

### 3. Add Alt Text and Caption

For each figure:

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/your-figure.pdf}
\alt{Brief description of visual structure, colors, and key results (200 chars)}
\caption{\textbf{Bold title.} Description. Solid blue: theory, dashed orange: experiment.}
\label{fig:your-label}
\end{figure}
```

### 4. Reference in Text

```latex
As shown in Fig.~\ref{fig:your-label}, the results...
```

**Note the `~` (non-breaking space)!**

---

## Color Palette Quick Reference

### Primary Colors (Use These)

| Name | LaTeX | RGB | When to Use |
|------|-------|-----|-------------|
| Blue | `cbBlue` | (0,114,178) | Primary/theory |
| Orange | `cbOrange` | (213,94,0) | Secondary/experiment |
| Green | `cbGreen` | (0,158,115) | Tertiary/comparison |
| Yellow | `cbYellow` | (240,228,66) | Emphasis |
| Purple | `cbPurple` | (204,121,167) | 4th series |
| Orange-Red | `cbRed` | (230,159,0) | Highlights only |

### Line Styles (Combine with Colors!)

```latex
% In TikZ:
\draw[cbBlue, solid] (0,0) -- (1,1);         % Blue solid line
\draw[cbOrange, dashed] (0,0) -- (1,0.5);    % Orange dashed line
\draw[cbGreen, dotted] (0,0) -- (1,0.3);     % Green dotted line
```

### Markers (Combine with Colors and Lines!)

```latex
% In TikZ:
\draw[cbBlue, markCircle] ...;      % Blue with circles
\draw[cbOrange, markSquare] ...;    % Orange with squares
\draw[cbGreen, markTriangle] ...;   % Green with triangles
```

---

## Figure Caption Template

Copy this structure for every figure:

```latex
\caption{\textbf{[Title in bold].}
[What the figure shows].
[Explicit color legend: "Solid blue line: X, dashed orange line: Y"].
[For multi-panel: "(Left) description, (Right) description"].
[Define all symbols].
[Specify units].
[Cite data source if applicable].}
```

**Example**:

```latex
\caption{\textbf{Yukawa coupling evolution.}
Running of third-generation Yukawa couplings from electroweak to Planck scale.
Solid blue curve with circles: top quark $y_t$.
Dashed orange curve with squares: bottom quark $y_b$.
Dotted green curve with triangles: tau lepton $y_\tau$.
All couplings calculated using two-loop RG equations.
Experimental values from PDG 2024.}
```

---

## Alt Text Template

Copy this structure for alt text:

```latex
\alt{[Type of plot] showing [main content].
[Describe axes and structure].
[Colors explicitly: "Blue bars...", "Orange line..."].
[Trends: "increases", "clusters near"].
[Key numbers if applicable].}
```

**Example**:

```latex
\alt{Line plot showing three curves on logarithmic energy scale from 1 TeV to Planck scale.
Solid blue curve with circular markers shows top Yukawa increasing from 0.99 to 1.15.
Dashed orange curve with square markers shows bottom Yukawa increasing from 0.024 to 0.05.
Dotted green curve with triangular markers shows tau Yukawa increasing from 0.010 to 0.018.
All three curves rise monotonically.}
```

**Length**: Aim for 200-300 characters (up to 500 if needed)

---

## Pre-Flight Checklist (Per Figure)

Before finalizing each figure, check:

- [ ] Uses colorblind-safe colors (blue/orange/green, NOT red/green)
- [ ] Line styles vary (solid/dashed/dotted)
- [ ] Markers vary if multiple data series (circle/square/triangle)
- [ ] Has alt text via `\alt{...}`
- [ ] Has caption with bold title
- [ ] Caption explains all colors explicitly
- [ ] Caption is self-contained (readable without main text)
- [ ] Has descriptive label: `\label{fig:meaningful-name}`
- [ ] Referenced in text: `Fig.~\ref{fig:meaningful-name}`
- [ ] Vector format (PDF/EPS) or high-res PNG (300 dpi)
- [ ] Text readable at final size (min 8pt font)
- [ ] Tested in grayscale (print preview)

---

## Common Mistakes to Avoid

### ❌ DON'T

1. Use red and green together (colorblind issue)
2. Use color alone to distinguish lines (add line styles!)
3. Write "see Figure 1" without `\ref{}`
4. Use "here" or "click here" for links
5. Write vague captions ("Results are shown")
6. Forget alt text
7. Use bare URLs in text
8. Skip the `~` before `\ref{}` (causes bad line breaks)

### ✅ DO

1. Use blue/orange/green color scheme
2. Combine color + line style + markers
3. Write `Fig.~\ref{fig:label}`
4. Use descriptive links ("GitHub repository", "arXiv:1234.5678")
5. Write self-contained captions with color legends
6. Include alt text for every figure
7. Use `\url{}` or `\href{}` for URLs
8. Always use `~` before references

---

## Testing Your Figures

### Test 1: Colorblind Mode

Visit https://www.color-blindness.com/coblis-color-blindness-simulator/

1. Upload your figure
2. Select "Deuteranopia" (most common red-green colorblindness)
3. Check: Can you still distinguish all elements?
4. Repeat for "Protanopia" and "Tritanopia"

**Pass**: All lines/regions remain distinguishable
**Fail**: Regenerate with better color/style combinations

### Test 2: Grayscale

In your PDF viewer:

1. Print Preview → Black & White
2. Check: Can you distinguish all lines?

**Pass**: Line styles make all elements distinguishable
**Fail**: Add more varied line styles (solid/dashed/dotted)

### Test 3: Caption Independence

1. Read caption without looking at figure
2. Ask: Do I understand what the figure shows?
3. Ask: Are all symbols/colors explained?

**Pass**: Caption is self-contained
**Fail**: Add missing definitions to caption

### Test 4: Size

1. Print figure at actual size (3.4" for single column, 7" for double)
2. Check: Can you read all text without magnification?

**Pass**: All text ≥8pt, legible
**Fail**: Increase font sizes in figure

---

## Links and References

### External Links (Use Descriptive Text)

```latex
% GOOD:
See the \href{https://github.com/user/repo}{GitHub repository} for code.
Data from \href{https://pdg.lbl.gov}{Particle Data Group}.
Preprint available: \href{https://arxiv.org/abs/1234.5678}{arXiv:1234.5678}.

% BAD:
See \href{https://github.com/user/repo}{here} for code.  % "here" not descriptive
Click \href{URL}{this link}.                              % "this link" not descriptive
```

### Internal References (Use Helper Commands)

Available commands (from `hyperref-setup.tex`):

```latex
\figref{fig:label}           % produces "Fig. 1"
\eqnref{eq:label}            % produces "Eq. (1)"
\secref{sec:label}           % produces "Sec. II"
\tabref{tab:label}           % produces "Table I"
```

Or use standard LaTeX with non-breaking space:

```latex
Fig.~\ref{fig:label}
Eq.~\eqref{eq:label}
Sec.~\ref{sec:label}
Table~\ref{tab:label}
```

**Always use `~` (tilde) for non-breaking space!**

---

## File Organization

Place your files like this:

```
submission/
├── colorblind-setup.tex          (colors and styles)
├── hyperref-setup.tex            (links and metadata)
├── figure-template.tex           (examples - reference only)
├── principia-metaphysica-submission.tex  (main paper)
├── references.bib                (bibliography)
└── figures/
    ├── dimensional-reduction.pdf
    ├── validation-results.pdf
    ├── dark-energy-planck.pdf
    └── [other figures].pdf
```

---

## Resources

### Must-Use Tools

1. **Colorblind Simulator**: https://www.color-blindness.com/coblis-color-blindness-simulator/
2. **Color Oracle** (desktop app): https://colororacle.org/

### Reference Documents

1. **Full Guidelines**: See `accessibility-guidelines.md`
2. **Figure Checklist**: See `figure-checklist.md`
3. **Figure Templates**: See `figure-template.tex`
4. **Summary Report**: See `accessibility-summary-report.md`

### APS Requirements

- **Author Guide**: https://journals.aps.org/prd/authors
- **REVTeX Guide**: https://journals.aps.org/revtex

---

## Quick Troubleshooting

### "My figure has red and green colors"

**Fix**: Replace with blue and orange from `colorblind-setup.tex`:
- Red → `cbBlue` or `cbRed` (orange-red)
- Green → `cbOrange` or `cbGreen` (bluish-green)

### "I need more than 3 colors"

**Fix**: Combine colors with line styles and markers:
- Blue + solid + circles
- Orange + dashed + squares
- Green + dotted + triangles
- Purple + dash-dot + diamonds
- Yellow + thick-solid + stars

This supports 5+ data series while remaining accessible.

### "Caption is too long"

**Fix**: Long captions are OK! Self-contained descriptions are required.
Typical length: 3-8 sentences for complex figures.

### "Alt text is too long"

**Fix**: Focus on structure and trends, not every detail.
Target: 200-300 characters (up to 500 max).
Use caption for comprehensive details.

### "Hyperref gives errors"

**Fix**: Load hyperref near END of preamble (before cleveref if used).
The `hyperref-setup.tex` file is designed for this.

### "Links aren't blue"

**Fix**: Check `hyperref-setup.tex` is included in preamble.
Verify `colorlinks=true` and `linkcolor=blue` in hyperref options.

### "Math in section title causes bookmark error"

**Fix**: Use `\texorpdfstring{}{}`:
```latex
\section{The \texorpdfstring{$G_2$}{G2} Manifold}
```

---

## Final Pre-Submission Check

Before submitting to APS, verify:

1. [ ] All figures use colorblind-safe colors
2. [ ] All figures tested with colorblind simulator
3. [ ] All figures tested in grayscale
4. [ ] All figures have alt text
5. [ ] All captions self-contained with color legends
6. [ ] All figures referenced in text
7. [ ] All links use descriptive text (no "click here")
8. [ ] PDF metadata correct (check File → Properties)
9. [ ] All hyperlinks work when clicked
10. [ ] Compiled PDF has no errors or warnings

**Use the full checklist** in `figure-checklist.md` for detailed verification.

---

## Need Help?

1. **Full details**: Read `accessibility-guidelines.md`
2. **Figure examples**: See `figure-template.tex`
3. **Per-figure checks**: Use `figure-checklist.md`
4. **Summary info**: Read `accessibility-summary-report.md`
5. **Color definitions**: See `colorblind-setup.tex`
6. **Link setup**: See `hyperref-setup.tex`

---

**Last Updated**: 2025-12-06
**Version**: 1.0
**Status**: Ready for use
