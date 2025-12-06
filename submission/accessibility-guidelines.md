# APS Accessibility Requirements Checklist

## Overview

This document provides a comprehensive checklist for ensuring the Principia Metaphysica submission meets APS Physical Review D accessibility requirements. All figures, captions, links, and content must be accessible to readers with visual impairments and color-vision deficiencies.

---

## Color-Blind Friendly Figures

### Color Palette Requirements
- [ ] Use color-blind friendly palettes (blue/orange, not red/green)
- [ ] All figures use Paul Tol's colorblind-safe color schemes
- [ ] Primary colors: Blue (#0072B2), Orange (#D55E00), Green (#009E73)
- [ ] Avoid red-green combinations completely
- [ ] Test figures with colorblindness simulators

### Visual Differentiation
- [ ] Line styles vary (solid, dashed, dotted) in addition to colors
- [ ] Markers vary (circle, square, triangle, diamond) in addition to colors
- [ ] Pattern fills vary (horizontal, vertical, diagonal hatching) for areas
- [ ] Text labels supplement color coding where possible
- [ ] Minimum contrast ratio 4.5:1 for all color pairs

### Specific Figure Types
- [ ] **Diagrams**: Use patterns + colors + labels
- [ ] **Plots**: Vary line style + marker + color
- [ ] **Bar charts**: Use patterns + colors + value labels
- [ ] **Contour plots**: Use line labels + varying thickness + color

---

## Figure Captions

### Content Requirements
- [ ] All figures have descriptive captions
- [ ] Captions are self-contained (readable without main text)
- [ ] Captions explain all symbols, line types, and colors explicitly
- [ ] Captions define all abbreviations used in figure
- [ ] Captions specify units for all quantities
- [ ] Captions indicate data sources (experimental, theoretical, simulated)

### Format Requirements
- [ ] Captions use `\caption{...}` in LaTeX
- [ ] Bold figure title at start: `\textbf{Title.} Description...`
- [ ] Legend explanations: "Solid blue line: ..., Dashed orange line: ..."
- [ ] Panel descriptions for multi-panel figures: "(Left) ..., (Right) ..."
- [ ] Mathematical symbols use proper LaTeX: $G_2$, not G2
- [ ] Citations in captions use `\cite{...}` when referencing data sources

### Length Guidelines
- [ ] Minimum 2-3 sentences per figure
- [ ] Complex figures may need paragraph-length captions
- [ ] Simple diagrams need at least 1 descriptive sentence
- [ ] Multi-panel figures need description of each panel

---

## Alt Text for Figures

### Implementation
- [ ] Each figure has alt text via `\alt{...}` command (REVTeX 4.2+)
- [ ] Alt text placed immediately before or after `\includegraphics`
- [ ] Fallback: Use figure description in `\caption` if `\alt` unavailable
- [ ] Alt text length: 125-200 characters recommended, up to 500 if needed

### Content Guidelines
- [ ] Alt text describes visual content, not just repeats caption
- [ ] Describe structure: "Three-panel diagram showing..."
- [ ] Describe trends: "Blue line increases logarithmically while orange line remains constant"
- [ ] Describe relationships: "Arrows indicate dimensional reduction from 26D to 4D"
- [ ] Include key numbers: "Agreement within 1-sigma for 10 of 14 observables"
- [ ] Avoid: "Figure showing...", "Image of..." (screen readers announce it's a figure)

### Examples
```latex
% Good alt text
\alt{Bar chart with 14 blue bars showing prediction accuracy. Ten bars reach the 1-sigma threshold line marked in green. Three bars marked with asterisks indicate exact matches.}

% Bad alt text
\alt{A figure showing validation results.}
```

---

## Link Accessibility

### Descriptive Link Text
- [ ] All links use descriptive text (not "click here" or "here")
- [ ] Link text indicates destination or purpose
- [ ] URLs are meaningful when read aloud by screen readers

### Specific Link Types
- [ ] **GitHub links**: Use "GitHub repository" or "source code repository"
  ```latex
  \href{https://github.com/andrewkwatts-maker/PrincipiaMetaphysica}{GitHub repository}
  ```
- [ ] **arXiv links**: Use "arXiv:1234.5678" as link text
  ```latex
  \href{https://arxiv.org/abs/1234.5678}{arXiv:1234.5678}
  ```
- [ ] **DOI links**: Embed in proper citation, not bare URL
  ```latex
  \cite{AuthorYear} % with DOI in .bib file
  ```
- [ ] **Website links**: Use site name or page title
  ```latex
  \href{https://pdg.lbl.gov}{Particle Data Group}
  ```

### URL Formatting
- [ ] Long URLs use `\url{...}` command for proper line breaking
- [ ] DOIs use `\doi{...}` command if available
- [ ] Hyperref package configured with `breaklinks=true`
- [ ] All URLs tested (no broken links)

---

## Language and Terminology

### American English
- [ ] American English throughout ("color" not "colour")
- [ ] American spellings: "fiber" not "fibre", "flavor" not "flavour"
- [ ] Units: Use standard physics notation (GeV, not Gev or gev)

### Consistency
- [ ] Consistent terminology for key concepts throughout
- [ ] G₂ notation: Use "G$_2$" in math mode, "G₂" in Unicode if supported
- [ ] Dimension notation: 26D, 13D, 7D, 4D (consistent format)
- [ ] Parameter names: Always use same symbol ($\theta_{23}$, not sometimes $\theta_2$)

### Acronyms and Abbreviations
- [ ] Define all acronyms on first use: "Standard Model (SM)"
- [ ] Use `\gls{...}` if using glossaries package
- [ ] Common physics acronyms (SM, QCD, QED) defined once in introduction
- [ ] Framework-specific terms (TCS, PM) defined in abstract or introduction

### Special Characters
- [ ] Subscripts/superscripts in math mode: $G_2$, not G₂ in equations
- [ ] Greek letters in math mode: $\theta$, $\phi$, $\alpha$
- [ ] Operators properly spaced: $\sin$, $\log$, $\exp$ (use `\sin`, not sin)
- [ ] Vectors use bold or arrow notation consistently: $\mathbf{v}$ or $\vec{v}$

---

## Equation Accessibility

### Labels and References
- [ ] All equations have descriptive labels: `\label{eq:generation-count}`
- [ ] Labels indicate equation purpose, not just numbering
- [ ] Referenced in text: "as shown in Eq.~\eqref{eq:generation-count}"
- [ ] Important equations numbered; intermediate steps may be unnumbered

### Formatting
- [ ] Complex equations broken into multiple lines when appropriate
- [ ] Use `align` environment for multi-line equations
- [ ] Use `split` within `equation` for numbered multi-line equations
- [ ] Alignment points chosen for readability (usually at = or + signs)

### Variable Definitions
- [ ] Variables defined in text near first use
- [ ] Units specified for dimensional quantities
- [ ] Ranges specified for dimensionless quantities
- [ ] Subscripts and superscripts explained

### Example
```latex
The generation count is determined by
\begin{equation}
n_{\text{gen}} = \frac{1}{2}|\chi(M_7)| = \frac{1}{2} \times 6 = 3,
\label{eq:generation-count}
\end{equation}
where $\chi(M_7)$ is the Euler characteristic of the G$_2$ manifold and $n_{\text{gen}}$ is the number of fermion generations.
```

---

## Table Accessibility

### Captions
- [ ] Tables have descriptive captions above table
- [ ] Caption format: `\caption{\textbf{Title.} Description}`
- [ ] Caption explains all columns and abbreviations
- [ ] Caption specifies data sources and uncertainties

### Structure
- [ ] Column headers clearly labeled using `\tablehead{...}` in REVTeX
- [ ] Units specified in headers or caption, not in each cell
- [ ] Use `\tablenum{...}` for numbers with uncertainties in REVTeX
- [ ] Avoid merged cells when possible (harder for screen readers)
- [ ] Use `\colhead{...}` for column headers in REVTeX

### Formatting
- [ ] Consistent decimal places within columns
- [ ] Alignment: Numbers right-aligned, text left-aligned
- [ ] Use `\phantom{0}` for alignment if needed
- [ ] Horizontal rules: Only `\hline` at top, bottom, and below headers
- [ ] No vertical rules (APS style)

### Example
```latex
\begin{table}[htbp]
\caption{\textbf{SM fermion mass predictions.} All masses in GeV. Theoretical values from TCS G$_2$ manifold \#187. Experimental values from PDG 2024.}
\label{tab:fermion-masses}
\begin{ruledtabular}
\begin{tabular}{lcc}
\tablehead{
\colhead{Particle} &
\colhead{Theoretical (GeV)} &
\colhead{Experimental (GeV)}
}
Electron & \tablenum{0.000511} & \tablenum{0.000511(0)} \\
Muon & \tablenum{0.1057} & \tablenum{0.1057(0)} \\
\end{tabular}
\end{ruledtabular}
\end{table}
```

---

## PDF Metadata

### Required Fields
- [ ] PDF title matches paper title
- [ ] PDF author(s) listed correctly
- [ ] PDF subject: "High Energy Physics - Phenomenology"
- [ ] PDF keywords: Include main framework terms
- [ ] PDF language set to "en-US"

### Hyperref Configuration
```latex
\usepackage[
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue,
  breaklinks=true,
  pdfauthor={Andrew Keith Watts},
  pdftitle={Principia Metaphysica: A Unified Framework from G2 Holonomy},
  pdfsubject={High Energy Physics - Phenomenology},
  pdfkeywords={G2 manifolds, M-theory, grand unification, extra dimensions, cosmology},
  pdflang={en-US}
]{hyperref}
```

---

## Additional Accessibility Features

### Document Structure
- [ ] Proper section hierarchy (don't skip levels)
- [ ] Section titles descriptive and meaningful
- [ ] Use `\section`, `\subsection`, `\subsubsection` properly
- [ ] No "orphan" sections (single subsection under section)

### Mathematical Content
- [ ] Screen-reader friendly: Avoid images of equations
- [ ] Use LaTeX math mode for all equations
- [ ] Define custom commands for repeated expressions
- [ ] Use `\text{...}` for text within equations

### References
- [ ] All citations have complete bibliography entries
- [ ] DOIs included in bibliography when available
- [ ] arXiv IDs included for preprints
- [ ] Journal references use standard abbreviations

### Fonts and Readability
- [ ] Font size at least 10pt (APS standard: 10-12pt)
- [ ] Sufficient line spacing (1.5 or double for drafts)
- [ ] Margins adequate for notes (APS handles in production)
- [ ] No light gray text on white background

---

## Testing and Validation

### Pre-Submission Checks
- [ ] Compile PDF with hyperref and check all links work
- [ ] View PDF metadata (File > Properties in Adobe Reader)
- [ ] Test color figures in grayscale (Print preview in B&W)
- [ ] Use colorblindness simulator on all figures
- [ ] Check all `\ref` and `\eqref` resolve correctly
- [ ] Verify all `\cite` commands have bibliography entries

### Accessibility Tools
- [ ] Use PAVE (PDF Accessibility Validation Engine) if available
- [ ] Adobe Acrobat accessibility checker
- [ ] Online colorblind simulators: Coblis, Color Oracle
- [ ] Screen reader testing (NVDA, JAWS) if possible

### Manual Review
- [ ] Read all alt text and captions without viewing figures
- [ ] Verify captions are self-contained
- [ ] Check link text makes sense out of context
- [ ] Confirm all acronyms defined before use
- [ ] Review equation labels for clarity

---

## Common Pitfalls to Avoid

### Figures
- [ ] **Don't**: Use red-green color combinations
- [ ] **Don't**: Rely on color alone to distinguish lines/regions
- [ ] **Don't**: Use low-contrast color pairs (yellow on white, etc.)
- [ ] **Don't**: Make captions that just repeat figure title
- [ ] **Don't**: Forget to explain symbols in multi-panel figures

### Links
- [ ] **Don't**: Use "click here" or "here" as link text
- [ ] **Don't**: Put bare URLs in text (use `\url{...}` or descriptive links)
- [ ] **Don't**: Have link text that doesn't indicate destination
- [ ] **Don't**: Break URLs manually (use `\url{...}` for automatic breaking)

### Equations
- [ ] **Don't**: Use images for equations (always use LaTeX)
- [ ] **Don't**: Leave variables undefined
- [ ] **Don't**: Use inconsistent notation for same quantity
- [ ] **Don't**: Number every trivial rearrangement

### Tables
- [ ] **Don't**: Use color alone to indicate important values
- [ ] **Don't**: Omit units from headers
- [ ] **Don't**: Use unclear abbreviations without definition
- [ ] **Don't**: Make overly complex merged-cell structures

---

## APS-Specific Requirements

### REVTeX 4.2
- [ ] Use `\documentclass[reprint,aps,prd]{revtex4-2}`
- [ ] Use `\alt{...}` command for figure alt text
- [ ] Use `\tablehead`, `\colhead`, `\tablenum` for tables
- [ ] Follow APS style guide for citations and references

### Physical Review D Specifics
- [ ] Maximum 20 pages for Letters (rarely applicable)
- [ ] No page limit for Regular Articles
- [ ] Figures: EPS, PDF, or PNG (vector preferred)
- [ ] Resolution: 300 dpi minimum for raster images
- [ ] Width: Single column (3.4") or double column (7")

### Submission Requirements
- [ ] All figure files included separately
- [ ] Figure file names match those in `\includegraphics{...}`
- [ ] Bibliography: BibTeX .bib file included
- [ ] Supplemental material clearly marked if included
- [ ] Cover letter mentions accessibility features if notable

---

## Summary

This checklist ensures the Principia Metaphysica paper meets all APS accessibility requirements:

1. **Visual accessibility**: Colorblind-friendly palettes, varied line styles
2. **Screen reader accessibility**: Alt text, descriptive links, proper structure
3. **Reading accessibility**: Self-contained captions, defined terms
4. **Navigation accessibility**: Proper labels, working hyperlinks
5. **Format accessibility**: LaTeX equations, structured tables, PDF metadata

**Before submission**: Review each section of this checklist and mark all items as complete. Pay special attention to figures (most common accessibility issues) and links.

**Resources**:
- APS Editorial Style Guide: https://journals.aps.org/authors
- REVTeX 4.2 Documentation: https://journals.aps.org/revtex
- Paul Tol's Color Schemes: https://personal.sron.nl/~pault/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
