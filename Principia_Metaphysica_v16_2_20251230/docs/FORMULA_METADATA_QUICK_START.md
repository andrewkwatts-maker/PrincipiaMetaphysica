# Formula Metadata Display - Quick Start Guide

## What You Get

Every formula in the Principia Metaphysica paper now displays with scientific rigor:

### Always Visible
- ✅ **LaTeX Equation** - Beautiful math rendering
- ✅ **Equation Number** - "(2.3)" style labels
- ✅ **Plain Text** - Copy-friendly Unicode
- ✅ **Parameter Definitions** - "where χ is the Euler characteristic..."
- ✅ **Description** - What the formula computes

### Expandable Panel (Click "Show metadata")
- 📥 **Input Parameters** - What goes into the calculation
- 📤 **Output Parameters** - What comes out
- 🔬 **Derivation Steps** - How we got here
- 📚 **References** - Academic citations
- 📊 **Category** - ESTABLISHED / THEORY / DERIVED / PREDICTION
- 🎯 **Values** - Theory vs Experiment comparison
- 📝 **Notes** - Additional context

### Interactive Features
- 🖱️ **Hover** over "Eq. (2.3)" → See preview tooltip
- 🖱️ **Click** equation reference → Jump to formula
- 🖱️ **Click** parameter chip → (Future: jump to definition)

## Example Formula Display

```
┌─────────────────────────────────────────────────────────┐
│  n_gen = χ_eff / 48                         (2.3)      │
│  ───────────────────                                    │
│  n_gen = χ_eff / 48  [Plain text fallback]            │
│                                                          │
│  where n_gen is the number of generations,              │
│  χ_eff is the effective Euler characteristic            │
│                                                          │
│  Number of fermion generations from index theorem       │
│                                                          │
│  ▸ Show formula metadata and derivation                 │
└─────────────────────────────────────────────────────────┘

[Expanded view shows:]
┌─────────────────────────────────────────────────────────┐
│  ▾ Hide formula metadata and derivation                 │
│                                                          │
│  📥 INPUT PARAMETERS                                     │
│  ┌──────────────────┐                                   │
│  │ topology.chi_eff │                                   │
│  └──────────────────┘                                   │
│                                                          │
│  📤 OUTPUT PARAMETERS                                    │
│  ┌──────────────┐                                       │
│  │ topology.n_gen │                                     │
│  └──────────────┘                                       │
│                                                          │
│  🔬 DERIVATION                                          │
│  1. Atiyah-Singer index theorem for chiral fermions     │
│  2. Index = (1/48) ∫ ch(F) ∧ Â(TM)                     │
│  3. For G2 with minimal flux: Index = χ_eff / 48       │
│  4. Substitute χ_eff = 144                              │
│  5. n_gen = 144 / 48 = 3 generations                   │
│                                                          │
│  📚 REFERENCES                                          │
│  › Atiyah & Singer (1968) "Index of Elliptic Operators"│
│  › Witten (1996) "Five-Brane Effective Action"         │
│                                                          │
│  📊 CATEGORY                                            │
│  ┌───────────────────────────────────────────┐         │
│  │ THEORY                                     │         │
│  │ Core theoretical prediction of PM          │         │
│  └───────────────────────────────────────────┘         │
│                                                          │
│  🎯 VALUES                                              │
│  Theory:      3 (dimensionless)                         │
│  Experiment:  3 (dimensionless)                         │
│  Deviation:   0.00σ    ← Excellent match!              │
│                                                          │
│  📝 NOTES                                               │
│  Exact agreement with observation - one of the most     │
│  precise predictions of the theory.                      │
└─────────────────────────────────────────────────────────┘
```

## Color Coding

| Element | Color | Meaning |
|---------|-------|---------|
| **Input Params** | 🔵 Blue | Data that goes into formula |
| **Output Params** | 🟠 Orange | Results computed by formula |
| **Derivation** | 🟢 Green | How we derived the formula |
| **References** | 🟣 Purple | Academic citations |
| **Category: THEORY** | 🟣 Purple | Core PM prediction |
| **Category: ESTABLISHED** | 🟢 Green | Known from literature |
| **Category: DERIVED** | 🔵 Blue | Derived from fundamentals |
| **Category: PREDICTION** | 🟡 Yellow | Novel testable prediction |
| **σ < 1** | 🟢 Green | Excellent agreement |
| **1 < σ < 2** | 🟡 Yellow | Good agreement |
| **σ > 2** | 🟠 Orange | Needs investigation |

## Equation References

When you write in sections:

```
"The three-generation formula Eq. (2.3) derives from
the Euler characteristic equation (2.2)."
```

The system automatically:
1. ✅ Makes "Eq. (2.3)" and "(2.2)" clickable
2. ✅ Shows preview tooltip on hover
3. ✅ Jumps to equation on click

## Adding Metadata to Formulas

In `AutoGenerated/formulas.json`:

```json
{
  "your-formula-id": {
    "id": "your-formula-id",
    "label": "(X.Y) Formula Name",
    "latex": "E = mc^2",
    "plain_text": "E = mc²",
    "category": "THEORY",
    "description": "What this formula computes",

    "input_params": ["param1", "param2"],
    "output_params": ["result"],

    "derivation": {
      "steps": [
        "Step 1: Start with principle X",
        "Step 2: Apply transformation Y",
        "Step 3: Result is Z"
      ],
      "references": [
        "Author (Year) arXiv:xxxx.xxxxx",
        "Book Title, Chapter N"
      ]
    },

    "terms": {
      "E": {
        "description": "the total energy",
        "symbol": "E"
      },
      "m": {
        "description": "the mass",
        "symbol": "m"
      },
      "c": {
        "description": "the speed of light",
        "symbol": "c"
      }
    },

    "computed_value": 1.234e-5,
    "experimental_value": 1.236e-5,
    "sigma_deviation": 0.5,
    "units": "eV",

    "notes": "Additional scientific context here."
  }
}
```

## Math Typography Best Practices

### Variables
- Use italic: `$n$` → *n*
- With text subscripts: `$n_{\text{gen}}$` → *n*<sub>gen</sub>

### Units
- Always upright: `$\text{GeV}$` → GeV
- Space before unit: `$137\,\text{GeV}$` → 137 GeV

### Functions
- Upright: `$\sin$`, `$\log$`, `$\exp$`
- Not: `$sin$` (wrong - italic)

### Operators
- Use proper spacing: `$a + b$` not `$a+b$`
- Fractions: `$\frac{a}{b}$` for display
- Inline: `$a/b$` for text

### Greek Letters
- Lowercase: `$\alpha$`, `$\beta$`, `$\chi$`
- Uppercase: `$\Gamma$`, `$\Delta$`, `$\Omega$`

## Testing Your Formulas

1. Add formula to `formulas.json`
2. Open `test-formula-metadata.html`
3. Update test data with your formula
4. Check:
   - ✅ LaTeX renders correctly
   - ✅ Plain text is readable
   - ✅ Terms are defined
   - ✅ Metadata panel expands
   - ✅ Colors are appropriate
   - ✅ Values display correctly

## Browser Compatibility

✅ **Supported:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

⚠️ **Partial Support:**
- IE 11 (basic display, no animations)
- Mobile browsers (optimized layout)

## Accessibility

- **Screen Readers**: Use plain text fallback
- **Keyboard**: Tab through interactive elements
- **High Contrast**: Color schemes tested
- **Print**: Auto-expand all metadata

## Performance

- **Lazy Loading**: Formulas load on demand
- **Caching**: MathJax results cached
- **Responsive**: Smooth on mobile
- **Print**: Optimized for PDF export

## Troubleshooting

### Formula doesn't show metadata?
- Check `formulaId` matches in both places
- Verify `formulas.json` is loaded
- Open browser console for errors

### Tooltip doesn't appear?
- Check equation has proper `(X.Y)` format
- Verify equation anchor exists: `#eq-X.Y`
- Look for JavaScript errors

### Metadata panel won't expand?
- Check formula has metadata fields
- Verify CSS file is loaded
- Test in different browser

### MathJax not rendering?
- Wait for MathJax to load
- Check network for CDN access
- Verify proper `$$` delimiters

## Need Help?

See full documentation: `FORMULA_METADATA_ENHANCEMENT.md`

---

**Quick tip:** Start with the test file `test-formula-metadata.html` to see examples!
