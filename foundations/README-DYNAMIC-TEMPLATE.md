# Foundation Page Dynamic Template System

This document explains the new dynamic template system for foundation pages in Principia Metaphysica.

## Overview

The template system allows foundation pages to load their content dynamically from `theory_output.json`, making it easier to:
- Create new foundation pages quickly
- Update content centrally in one place
- Ensure consistency across all foundation pages
- Reduce code duplication

## Components

### 1. JavaScript Loader: `js/pm-foundation-page.js`

The core loader class `PMFoundationPageLoader` handles:
- Extracting foundation ID from URL (query parameter or filename)
- Fetching `theory_output.json`
- Finding the matching foundation entry
- Rendering all page sections dynamically

**Auto-initialization**: Pages with the attribute `data-pm-foundation-auto-load` on the `<body>` tag will automatically load on DOM ready.

### 2. Template File: `foundations/foundation-template.html`

A complete HTML template with placeholder sections that are populated by the JavaScript loader. This can be copied to create new foundation pages.

### 3. Data Structure: `theory_output.json` foundations section

Foundation data is stored as an array in `theory_output.json`:

```json
{
  "foundations": [
    {
      "id": "boltzmann-entropy",
      "name": "Boltzmann Entropy",
      "description": "...",
      "equation": "S = k<sub>B</sub> ln &Omega;",
      "status": "established",
      "year": "1877",
      "attribution": "Formulated by Ludwig Boltzmann in 1877",
      "gradient": "linear-gradient(...)",
      "borderColor": "rgba(...)",
      "properties": { ... },
      "pmConnection": { ... },
      "formulas": [ ... ],
      "usedInSections": [ ... ]
    }
  ]
}
```

## Creating a New Foundation Page

### Option 1: Using URL Query Parameter

1. Copy `foundation-template.html` to a new file (e.g., `my-foundation.html`)
2. Add foundation data to `theory_output.json` with a unique ID
3. Access via: `my-foundation.html?id=your-foundation-id`

### Option 2: Using Filename

1. Copy `foundation-template.html` to `your-foundation-id.html`
2. Add foundation data to `theory_output.json` with `id: "your-foundation-id"`
3. Access via: `your-foundation-id.html`
4. The loader will automatically extract the ID from the filename

### Option 3: Hybrid Approach (Recommended for existing pages)

Keep some static content (like complex visualizations) and load the rest dynamically:

1. Copy an existing page or start from template
2. Add `data-pm-foundation-auto-load` to `<body>` tag
3. Include sections with IDs:
   - `foundation-hero` - Hero section
   - `key-properties` - Key properties/components
   - `formula-list` - Expandable formulas
   - `pm-connection` - PM connections
   - `pm-usage` - Usage in PM sections
4. Add static content between dynamic sections as needed

See `boltzmann-entropy-dynamic.html` for an example.

## Foundation Data Structure

### Required Fields

```json
{
  "id": "unique-identifier",          // Must match filename or query param
  "name": "Display Name",
  "description": "Brief description",
  "equation": "Main equation (HTML)"
}
```

### Optional Fields

```json
{
  "status": "established",            // Badge type: established, theoretical, conjectural
  "year": "1877",                     // Year discovered/formulated
  "attribution": "Formulated by...",  // Attribution text
  "gradient": "linear-gradient(...)", // Hero background gradient
  "borderColor": "rgba(...)"          // Hero border color
}
```

### Properties Section

Explains what the equation means and its components:

```json
{
  "properties": {
    "meaning": "Human-readable explanation",
    "components": [
      {
        "symbol": "S",
        "name": "Entropy",
        "description": "What it represents"
      }
    ]
  }
}
```

### PM Connection Section

How the foundation relates to Principia Metaphysica:

```json
{
  "pmConnection": {
    "description": "Overview text",
    "applications": [
      {
        "title": "Application Name",
        "description": "What it does",
        "equation": "Optional equation",
        "note": "Optional note",
        "details": "Optional details",
        "list": ["Item 1", "Item 2"]  // Alternative to details
      }
    ]
  }
}
```

### Formulas Section

Expandable formula details:

```json
{
  "formulas": [
    {
      "equation": "The formula (HTML)",
      "status": "established",
      "components": [
        {
          "symbol": "x",
          "name": "Variable Name",
          "description": "What it means",
          "link": "https://...",
          "linkText": "Learn more",
          "badge": "Optional badge text",
          "badgeType": "established"  // or other types
        }
      ],
      "derivationChain": [
        {
          "text": "Step description",
          "badge": "Badge text",
          "type": "established"
        }
      ]
    }
  ]
}
```

### Used in Sections

Links to PM theory sections that use this foundation:

```json
{
  "usedInSections": [
    {
      "title": "Section Title",
      "description": "Brief description",
      "link": "section-filename.html"
    }
  ]
}
```

## Adding Foundation Data to theory_output.json

### Using the Python Script

A helper script `add_foundations_to_theory.py` is provided:

```python
python add_foundations_to_theory.py
```

This script:
- Loads existing `theory_output.json`
- Merges new foundation data
- Avoids duplicates by ID
- Updates existing entries if ID matches

To add new foundations, edit the `create_foundations_data()` function in the script.

### Manual Editing

1. Open `theory_output.json`
2. Find or create the `"foundations"` array
3. Add your foundation object to the array
4. Save with UTF-8 encoding

## Styling

All foundation pages share common styles defined inline in the template. These include:

- `.equation-hero` - Hero section with equation
- `.main-equation` - Large equation display
- `.subsection` - Content sections
- `.equation-box` - Boxed equations
- `.highlight-box` - Highlighted content boxes
- `.resource-card` - Resource/section cards
- `.resource-link` - Links to resources

Custom colors can be set per foundation using the `gradient` and `borderColor` fields.

## Examples

### Example 1: Boltzmann Entropy (Dynamic)

File: `boltzmann-entropy-dynamic.html`
- Loads core content from JSON
- Keeps static SVG diagram
- Demonstrates hybrid approach

### Example 2: Pure Template

File: `foundation-template.html`
- Minimal HTML, all content from JSON
- Best for simple foundations without complex visualizations
- Can be used as-is with query parameter

## Migration Guide

To convert an existing foundation page to use the dynamic loader:

1. **Extract data**: Copy content to JSON structure in `theory_output.json`
2. **Add loader script**: Include `<script src="../js/pm-foundation-page.js"></script>`
3. **Add auto-load attribute**: `<body data-pm-foundation-auto-load>`
4. **Replace sections**: Replace static content with placeholder divs with IDs
5. **Keep unique content**: Leave complex visualizations, diagrams, etc. as static HTML
6. **Test**: Load the page and verify content renders correctly

## Troubleshooting

### Foundation Not Loading

1. Check browser console for errors
2. Verify foundation ID in JSON matches filename or query param
3. Ensure `theory_output.json` is accessible and valid JSON
4. Check that `data-pm-foundation-auto-load` attribute is present

### Missing Sections

1. Check that section IDs in HTML match expected IDs in loader
2. Verify JSON data includes all required fields
3. Check that section data is properly nested in JSON

### Styling Issues

1. Ensure all required CSS files are loaded
2. Check that custom gradients/colors in JSON are valid CSS
3. Verify HTML entities in equations are properly escaped

## Future Enhancements

Potential improvements to the template system:

1. **Diagram generation**: Dynamic SVG generation from JSON data
2. **Formula validation**: Client-side validation of formula syntax
3. **Search integration**: Foundation search from theory_output.json
4. **Automated migration**: Script to convert existing HTML to JSON
5. **Preview mode**: Live preview of JSON changes
6. **Multi-language support**: i18n for foundation descriptions

## Best Practices

1. **Use semantic IDs**: Foundation IDs should be lowercase-with-hyphens
2. **HTML in JSON**: Use HTML entities (`&times;`, `&Omega;`, etc.) in equations
3. **Gradients**: Use rgba colors with alpha for consistent theming
4. **Descriptions**: Keep descriptions concise (1-2 sentences for listing)
5. **Attribution**: Include year and source for established physics
6. **Testing**: Always test page load before committing JSON changes
7. **Validation**: Validate JSON syntax with a linter

## Credits

- Template system: Andrew Keith Watts
- Based on existing foundation page structure
- Integrated with PM theory output system

---

Last updated: 2025-12-26
