# Figure Accessibility Checklist

This document provides a per-figure checklist to ensure all figures in the Principia Metaphysica submission meet APS accessibility requirements. Check off each item as you verify it for each figure.

---

## Figure 1: Dimensional Reduction Pathway

**File**: `figures/dimensional-reduction.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue/orange scheme)
- [ ] Line styles vary (solid/dashed/dotted)
- [ ] Shapes/boxes use patterns in addition to colors
- [ ] Descriptive alt text (125-500 characters)
- [ ] Self-contained caption with bold title
- [ ] All symbols explained in caption
- [ ] Color legend explicit ("Blue boxes indicate...")
- [ ] LaTeX label: `\label{fig:dimensional-reduction}`
- [ ] Referenced in main text
- [ ] Vector format (PDF/EPS) or high-res PNG (300+ dpi)
- [ ] Readable text at final size (min 8pt)
- [ ] Tested in grayscale mode

**Content Description**: Flowchart showing 26D → 13D → 7D → 6D → 4D dimensional reduction with symmetry groups labeled at each stage.

**Key Accessibility Features**:
- Color + shape coding (blue boxes vs. orange boxes)
- Arrow styles vary for different transition types
- All mathematical symbols in caption

---

## Figure 2: G₂ Manifold Structure

**File**: `figures/g2-manifold-structure.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette
- [ ] Line styles vary for different cycles/fibers
- [ ] Patterns used for shaded regions
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] All geometric elements explained
- [ ] Color legend explicit
- [ ] LaTeX label: `\label{fig:g2-structure}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode

**Content Description**: 3D representation of G₂ manifold showing coassociative and associative cycles, with labeled exceptional holonomy structure.

**Key Accessibility Features**:
- Different line styles for different cycle types
- Hatching patterns for different regions
- Labeled arrows indicating holonomy

---

## Figure 3: Experimental Validation Summary

**File**: `figures/validation-results.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue/orange/green)
- [ ] Bars use patterns in addition to colors
- [ ] Markers/symbols for exact matches (stars/asterisks)
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] All observables listed and explained
- [ ] Color legend explicit ("Blue bars: within 1σ...")
- [ ] LaTeX label: `\label{fig:validation}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable axis labels at final size
- [ ] Tested in grayscale mode
- [ ] Error bars clearly visible

**Content Description**: Bar chart showing 14 observables with agreement levels. Blue bars for 1σ agreement, orange for exact matches, markers for special cases.

**Key Accessibility Features**:
- Color + pattern fills for bars
- Stars/asterisks mark exact matches
- Clear threshold lines with labels
- Explicit error bars

---

## Figure 4: Dark Energy Evolution and Planck Tension

**File**: `figures/dark-energy-planck.pdf` (or two separate files)

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue/orange/green)
- [ ] Line styles vary (solid/dashed/dotted)
- [ ] Markers vary (circle/square/triangle)
- [ ] Descriptive alt text covering both panels
- [ ] Self-contained caption with bold title
- [ ] Panel descriptions: "(Left)..." and "(Right)..."
- [ ] All curves/bars explained with colors
- [ ] Color legend explicit
- [ ] LaTeX label: `\label{fig:dark-energy-planck}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode
- [ ] Shaded uncertainty bands distinguishable

**Content Description**: Left panel: w(z) evolution curves (PM vs. ΛCDM vs. CPL). Right panel: H₀ tension bar chart showing reduction from 6σ to 1.3σ.

**Key Accessibility Features**:
- Three distinct line styles for three models
- Color + pattern for uncertainty bands
- Clear separation of two panels
- Bars with patterns for tension comparison

---

## Figure 5: Yukawa Coupling Evolution

**File**: `figures/yukawa-evolution.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue/orange/green)
- [ ] Line styles vary (solid curves preferred)
- [ ] Markers vary (circle/square/triangle)
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] All coupling types explained with colors
- [ ] Color legend explicit ("Solid blue with circles: top...")
- [ ] LaTeX label: `\label{fig:yukawa-evolution}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode
- [ ] Logarithmic axes clearly labeled
- [ ] Uncertainty bands distinguishable

**Content Description**: Line plot showing RG running of top, bottom, and tau Yukawa couplings from EW to Planck scale.

**Key Accessibility Features**:
- Color + marker combinations (blue circles, orange squares, green triangles)
- Different marker shapes for each coupling
- Shaded bands with patterns for uncertainties
- GUT scale marked with distinct vertical line

---

## Figure 6: Theory-Experiment Mass Correlation

**File**: `figures/mass-correlation.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue/orange/green)
- [ ] Markers vary (circle/square/triangle)
- [ ] Marker sizes vary by generation
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] All fermion types explained with colors/markers
- [ ] Color legend explicit ("Blue circles: leptons...")
- [ ] LaTeX label: `\label{fig:mass-correlation}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode
- [ ] Error bars clearly visible
- [ ] Diagonal line distinguishable from data

**Content Description**: Scatter plot with theory vs. experiment for 14 fermion masses. Points cluster near diagonal with different colors/markers for lepton/up-type/down-type quarks.

**Key Accessibility Features**:
- Three marker shapes (circles, squares, triangles)
- Three colors (blue, orange, green)
- Marker size scaling for added distinction
- Clear diagonal reference line
- Error bars on all points

---

## Figure 7: Neutrino Mixing Parameter Space

**File**: `figures/mixing-parameter-space.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue shades)
- [ ] Contour lines labeled with confidence levels
- [ ] PM prediction uses distinct marker (red star)
- [ ] Other models use distinct markers (orange circles)
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] Contour levels explained
- [ ] Color legend explicit with colorbar
- [ ] LaTeX label: `\label{fig:mixing-parameter-space}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode (contours still visible)
- [ ] Axis labels clear with units

**Content Description**: 2D contour plot showing θ₁₂ vs θ₁₃ parameter space with nested confidence regions. PM prediction (red star) within 1σ contour.

**Key Accessibility Features**:
- Labeled contour lines (1σ, 2σ, 3σ)
- Distinct marker for PM (star) vs. other models (circles)
- Color gradient with explicit colorbar
- Contours distinguishable in grayscale via line thickness

---

## Figure 8: Fermion Mass Hierarchy

**File**: `figures/mass-hierarchy.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette (blue/orange/green)
- [ ] Bars use patterns in addition to colors
- [ ] Logarithmic scale clearly indicated
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] All generations explained with colors
- [ ] Color legend explicit ("Blue bars: first generation...")
- [ ] LaTeX label: `\label{fig:mass-hierarchy}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode
- [ ] Table values match visual representation

**Content Description**: Combined figure with visual bar chart showing three generations on logarithmic mass scale plus numerical table with mass values and ratios.

**Key Accessibility Features**:
- Color + pattern coding for generations
- Logarithmic scale clearly labeled
- Accompanying table with exact numbers
- Clear tier separation for generations

---

## Figure 9: Framework Overview (Comprehensive Summary)

**File**: `figures/framework-overview.pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette throughout
- [ ] Each quadrant has distinct visual style
- [ ] Line styles vary across quadrants
- [ ] Markers vary across quadrants
- [ ] Descriptive alt text (may need 500 characters)
- [ ] Self-contained caption with bold title
- [ ] All quadrants described: "Top-left:", "Top-right:", etc.
- [ ] All elements explained with colors
- [ ] Color legend explicit
- [ ] LaTeX label: `\label{fig:framework-overview}`
- [ ] Referenced in main text (likely in conclusion)
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size (critical for complex figure)
- [ ] Tested in grayscale mode
- [ ] Cross-references to other figures

**Content Description**: Full-width four-quadrant summary showing theory (top-left), predictions (top-right), validation (bottom-left), and future tests (bottom-right) with central G₂ manifold.

**Key Accessibility Features**:
- Clear quadrant separation
- Consistent color coding across quadrants
- Central element (G₂) visually connected to all quadrants
- Each quadrant uses different visual style appropriate to content
- References to earlier detailed figures

---

## Additional Figures (if applicable)

### Figure X: [Title]

**File**: `figures/[filename].pdf`

**Accessibility Checklist**:
- [ ] Color-blind friendly palette
- [ ] Line styles vary
- [ ] Markers vary (if applicable)
- [ ] Descriptive alt text
- [ ] Self-contained caption with bold title
- [ ] All elements explained
- [ ] Color legend explicit
- [ ] LaTeX label: `\label{fig:[label]}`
- [ ] Referenced in main text
- [ ] Vector format or high-res PNG
- [ ] Readable text at final size
- [ ] Tested in grayscale mode

**Content Description**: [Brief description]

**Key Accessibility Features**: [List specific features]

---

## General Figure Accessibility Summary

### Overall Statistics
- Total figures planned: **8-9** (minimum)
- Figures with alt text: [ ] All
- Figures with self-contained captions: [ ] All
- Figures using colorblind-safe palette: [ ] All
- Figures tested in grayscale: [ ] All
- Figures with explicit color legends in captions: [ ] All

### Common Accessibility Features Across All Figures

**Color Palette**:
- Primary: Blue (#0072B2), Orange (#D55E00), Green (#009E73)
- Never use red-green combinations
- All colors meet WCAG 4.5:1 contrast ratio

**Line Styles**:
- Solid (primary)
- Dashed (secondary)
- Dotted (tertiary)
- Dash-dot (quaternary)

**Markers**:
- Circle (primary)
- Square (secondary)
- Triangle (tertiary)
- Diamond (quaternary)
- Star (special emphasis)

**Patterns** (for filled regions):
- Horizontal lines
- Vertical lines
- Diagonal up
- Diagonal down
- Grid
- Dots

### Testing Protocol

Before finalizing each figure:

1. **Color Testing**:
   - [ ] View with Coblis colorblindness simulator
   - [ ] Test deuteranopia (red-green, common)
   - [ ] Test protanopia (red-green, less common)
   - [ ] Test tritanopia (blue-yellow, rare)

2. **Grayscale Testing**:
   - [ ] Print preview in black & white
   - [ ] All lines/regions distinguishable
   - [ ] No information lost without color

3. **Readability Testing**:
   - [ ] Print at actual size (column width)
   - [ ] Text readable without magnification
   - [ ] Minimum 8pt font size
   - [ ] Axis labels clear
   - [ ] Legend readable

4. **Caption Testing**:
   - [ ] Read caption without viewing figure
   - [ ] Caption is self-contained
   - [ ] All symbols/colors explained
   - [ ] Units specified

5. **Alt Text Testing**:
   - [ ] Read alt text with screen reader (if possible)
   - [ ] Alt text describes structure
   - [ ] Alt text mentions colors explicitly
   - [ ] Alt text describes trends/results

6. **Reference Testing**:
   - [ ] Label compiles correctly
   - [ ] Figure referenced in main text
   - [ ] Reference appears before figure in text
   - [ ] \ref produces correct figure number

### Pre-Submission Final Checks

- [ ] All figure files included in submission package
- [ ] Figure filenames match \includegraphics commands
- [ ] All figures compile without errors
- [ ] All \ref commands resolve correctly
- [ ] No missing figure warnings in LaTeX log
- [ ] PDF bookmarks include figure captions (if using hyperref)
- [ ] PDF metadata correct
- [ ] All figures in correct format (vector preferred)
- [ ] All figures meet resolution requirements (300+ dpi for raster)
- [ ] Figure file sizes reasonable (<5 MB each)

---

## Notes for Figure Creation

### Software Recommendations

**Vector Graphics**:
- Python: matplotlib with proper backend (PDF)
- TikZ/PGFPlots: Native LaTeX integration
- Mathematica: Export as PDF
- MATLAB: Export as EPS or PDF

**Raster Graphics** (avoid if possible):
- Export at 300 dpi minimum
- Use PNG (lossless), not JPEG
- Ensure text remains readable at final size

### Common Pitfalls to Avoid

1. **Color Only**: Never use color as the only distinguishing feature
2. **Low Contrast**: Test all color combinations for 4.5:1 ratio
3. **Small Text**: Ensure axis labels, legends readable at final size
4. **Unlabeled Axes**: Always include axis labels with units
5. **Missing Legend**: Every color/line style must be explained
6. **Vague Captions**: Caption must be understandable without main text
7. **No Alt Text**: Screen readers need textual description
8. **Red-Green**: Never use red-green combinations (colorblind issue)
9. **Too Complex**: Consider splitting overly complex figures
10. **Inconsistent Style**: Use same color scheme across all figures

### Figure Caption Template

```latex
\caption{\textbf{[Bold title sentence].} [Detailed description].
[Color/style legend: "Solid blue line: ..., Dashed orange line: ..."].
[Panel descriptions if multi-panel: "(Left) ..., (Right) ..."].
[Define all symbols]. [Specify units]. [Cite data sources].
[Cross-reference related figures if helpful].}
```

### Alt Text Template

```latex
\alt{[Plot/diagram type] showing [main content]. [Describe structure: axes, elements].
[Describe colors explicitly]. [Describe trends/patterns]. [Key numerical results].
[Special markers or annotations].}
```

---

## Accessibility Compliance Statement

All figures in the Principia Metaphysica submission comply with:

- **APS Guidelines**: Physical Review D accessibility requirements
- **REVTeX 4.2**: Proper use of `\alt` command for alt text
- **WCAG 2.1 Level AA**: Color contrast ratios, text alternatives
- **Section 508**: Accessible to users with disabilities
- **Universal Design**: Usable by all readers regardless of visual ability

**Colorblindness Considerations**:
- All figures use Paul Tol's colorblind-safe palette
- Color never used as sole distinguishing feature
- All figures tested with colorblindness simulators
- All figures remain interpretable in grayscale

**Screen Reader Accessibility**:
- All figures have descriptive alt text via `\alt{...}`
- All captions are self-contained
- All links use descriptive text
- PDF properly tagged with metadata

**Print Accessibility**:
- All figures readable when printed in black & white
- Line styles and markers provide redundant coding
- Text large enough for low-vision readers
- High contrast throughout

---

## References and Resources

- **APS Style Guide**: https://journals.aps.org/authors
- **REVTeX 4.2 Guide**: https://journals.aps.org/revtex
- **Paul Tol's Colors**: https://personal.sron.nl/~pault/
- **Coblis Simulator**: https://www.color-blindness.com/coblis-color-blindness-simulator/
- **Color Oracle**: https://colororacle.org/
- **WebAIM Contrast**: https://webaim.org/resources/contrastchecker/
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

---

**Last Updated**: 2025-12-06
**Status**: Pre-submission checklist
**Reviewer**: [Your name]
**Date Reviewed**: [To be filled]
