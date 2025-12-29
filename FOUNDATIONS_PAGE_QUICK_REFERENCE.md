# Foundations Page - Quick Reference

## Page Location
**File:** `h:\Github\PrincipiaMetaphysica\Pages\foundations.html`
**URL:** `/Pages/foundations.html`

## Purpose
Display ONLY established physics that Principia Metaphysica builds upon. This includes:
- Historical foundational equations
- Fundamental constants (CODATA)
- Experimental particle masses (PDG)
- Neutrino parameters (NuFIT)
- Cosmological parameters (Planck)

## Data Source
**File:** `h:\Github\PrincipiaMetaphysica\simulations\base\foundations_registry.json`

**Structure:**
```json
{
  "foundations": [...],              // 22 historical equations
  "fundamental_constants": [...],    // 4 CODATA constants
  "experimental_masses": [...],      // 6 PDG particle masses
  "neutrino_parameters": [...],      // 5 NuFIT parameters
  "cosmological_parameters": [...],  // 4 Planck parameters
  "metadata": {...}
}
```

## Adding New Foundations

### 1. Add to Appropriate Section in JSON

For a new fundamental constant:
```json
{
  "id": "boltzmann-constant",
  "title": "Boltzmann Constant",
  "category": "fundamental_constants",
  "year": 2019,
  "author": "CODATA 2022",
  "latex": "k_B = 1.380649 \\times 10^{-23} \\text{ J/K (exact)}",
  "description": "Relates thermal energy to temperature.",
  "source": "CODATA 2022",
  "references": ["https://physics.nist.gov/cuu/Constants/"]
}
```

For a new foundational equation:
```json
{
  "id": "schrodinger-equation",
  "title": "Schrödinger Equation",
  "category": "quantum_mechanics",
  "year": 1926,
  "author": "Erwin Schrödinger",
  "latex": "i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi",
  "description": "The fundamental equation of quantum mechanics describing wave function evolution.",
  "prerequisites": [],
  "references": []
}
```

### 2. Required Fields
- `id` - Unique identifier (kebab-case)
- `title` - Display name
- `category` - Physics domain (see categories below)
- `year` - Discovery/measurement year
- `author` - Discoverer or data source
- `latex` - LaTeX equation (use double backslashes)
- `description` - Physical significance

### 3. Optional Fields
- `source` - Data source citation (e.g., "PDG 2024")
- `references` - Array of URLs
- `prerequisites` - Array of prerequisite IDs

## Categories

### Existing Categories
- `general_relativity` - Purple
- `quantum_mechanics` - Blue
- `quantum_field_theory` - Blue
- `differential_geometry` - Pink
- `mathematics` - Pink
- `particle_physics` - Green
- `neutrino_physics` - Green
- `cosmology` - Yellow
- `statistical_mechanics` - Yellow
- `black_hole_physics` - Yellow
- `grand_unification` - Red
- `higher_dimensional_physics` - Red
- `fundamental_constants` - Gold
- `particle_masses` - Violet

### Adding New Category
1. Add to `metadata.categories` array in JSON
2. Add color styling in `foundations.html`:
```css
.category-badge.your_category_name {
    background: rgba(R, G, B, 0.2);
    color: #hexcolor;
    border: 1px solid rgba(R, G, B, 0.3);
}
```

## Data Sources

### Authoritative References
1. **CODATA 2022** - https://physics.nist.gov/cuu/Constants/
   - Fundamental physical constants
   - Regularly updated by international committee

2. **PDG 2024** - https://pdg.lbl.gov/
   - Particle Data Group
   - Comprehensive particle physics reference
   - Annual updates

3. **NuFIT 6.0** - http://www.nu-fit.org/
   - Global neutrino oscillation fits
   - Combines all neutrino experiments

4. **Planck 2018** - https://www.cosmos.esa.int/web/planck
   - Cosmic Microwave Background measurements
   - Cosmological parameters

### When to Add New Source
1. Add URL to appropriate foundation entry
2. Update `metadata.data_sources` array
3. Ensure source is peer-reviewed and authoritative

## Styling Guidelines

### Card Layout
```
┌─────────────────────────────────────┐
│ Title                    [Category]  │
│ Author (Year)                        │
├─────────────────────────────────────┤
│                                      │
│         LaTeX Equation               │
│                                      │
├─────────────────────────────────────┤
│ Description text explaining the      │
│ physical significance...             │
├─────────────────────────────────────┤
│ Source: CODATA 2022 📖               │
└─────────────────────────────────────┘
```

### Color Scheme
- Background: Dark (#0a0a0f)
- Cards: Glass morphism with blur
- Accent: Purple gradient (#8b7fff → #ff7eb6)
- Text: Light gray (#e0e0e0)

## Features

### 1. Dynamic Filtering
- By physics domain (dropdown)
- By search text (real-time)

### 2. Sorting
- Chronological by default (oldest first)
- Shows historical progression of physics

### 3. LaTeX Rendering
- MathJax 3.x
- Automatic typesetting on load and filter

### 4. Responsive Design
- Desktop: Multi-column grid
- Mobile: Single column stack

### 5. Source Attribution
- Every entry cites authoritative source
- Direct links to references
- Maintains academic rigor

## Maintenance Checklist

### Annual Updates
- [ ] Update PDG values (yearly in August)
- [ ] Check NuFIT for new releases (1-2 per year)
- [ ] Review CODATA updates (every ~4 years)
- [ ] Monitor Planck/CMB updates (as released)

### Adding Data
- [ ] Verify source is authoritative
- [ ] Include proper citation
- [ ] Add reference URL if available
- [ ] Test LaTeX renders correctly
- [ ] Check category badge color
- [ ] Validate JSON syntax

### Code Updates
- [ ] Keep MathJax updated
- [ ] Test mobile responsiveness
- [ ] Verify filter functionality
- [ ] Check search performance
- [ ] Validate accessibility

## Common Issues

### LaTeX Not Rendering
- Check double backslashes in JSON
- Verify MathJax script loads
- Look for console errors

### Wrong Category Color
- Add missing category style in CSS
- Check spelling of category name

### Broken References
- Verify URL is still valid
- Update to new official source if moved

### Search Not Working
- Check searchable fields include new data
- Verify filter function updated

## File Dependencies

### Required Files
- `foundations.html` - Main page
- `foundations_registry.json` - Data source
- `pm-header.js` - Header injection
- `auth-guard.js` - Authentication
- `pm-common.css` - Base styles
- MathJax CDN - LaTeX rendering

### Optional Files
- `pm-scientific-typography.css` - Typography
- `pm-ux-consistency.css` - Consistency
- `mobile-responsive.css` - Mobile support

## Best Practices

1. **Always cite sources** - Every value needs attribution
2. **Use authoritative data** - No Wikipedia, prefer primary sources
3. **Include uncertainties** - Show error bars when available
4. **Keep descriptions concise** - 1-2 sentences max
5. **Link to originals** - Let users verify independently
6. **Maintain chronology** - Sort by year shows physics evolution
7. **Separate PM content** - This page is ONLY established physics

## Quick Commands

### Validate JSON
```bash
python -m json.tool simulations/base/foundations_registry.json
```

### Test MathJax Locally
Open `foundations.html` in browser, check console for errors

### Count Entries
Total = foundations + constants + masses + neutrino + cosmological
Current: 22 + 4 + 6 + 5 + 4 = 41 entries

## Contact
For questions about this page, contact: AndrewKWatts@Gmail.com
