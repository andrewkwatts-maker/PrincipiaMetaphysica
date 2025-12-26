# Dynamic Section Loading System

## Overview

The Principia Metaphysica website now supports dynamic section loading from a single source of truth: `theory_output.json`. This eliminates duplication and ensures consistency between the paper and website.

## Architecture

```
config.py → section_registry.py → run_all_simulations.py → theory_output.json → website
```

### Components

1. **section_registry.py** - Defines all section metadata using `SectionMetadata` dataclass
2. **run_all_simulations.py** - Exports sections to `theory_output.json`
3. **js/pm-section-renderer.js** - Custom element that renders sections from JSON
4. **theory_output.json** - Single source of truth for all section content

## Section Metadata Structure

Each section includes:

- **id**: Section number (e.g., "1", "2", "3")
- **title**: Section title
- **abstract**: Brief section summary
- **beginnerSummary**: Simplified explanation for non-experts
- **keyTakeaways**: List of 3-5 main points
- **sectionFile**: Path to full HTML file (e.g., "sections/introduction.html")
- **prevSection/nextSection**: Navigation links
- **contentBlocks**: Structured content (text, formulas, tables, etc.)

## Usage

### 1. Basic Section Rendering

```html
<pm-section section-id="1"></pm-section>
```

### 2. Display Levels

```html
<!-- Summary only (title + abstract) -->
<pm-section section-id="1" level="summary"></pm-section>

<!-- Standard display (includes key takeaways) -->
<pm-section section-id="1" level="display"></pm-section>

<!-- Full (includes beginner summary and all content) -->
<pm-section section-id="1" level="full"></pm-section>
```

### 3. Testing

Open `test-section-loader.html` in a browser to test the dynamic loading system:

```bash
# Start a local server (required for fetch() to work)
python -m http.server 8000

# Open in browser
http://localhost:8000/test-section-loader.html
```

## Adding New Sections

### Step 1: Add to section_registry.py

```python
"7": SectionMetadata(
    id="7",
    title="New Section Title",
    section_type="section",
    abstract="Brief description...",
    section_file="sections/new-section.html",
    beginner_summary="Simplified explanation...",
    key_takeaways=[
        "First key point",
        "Second key point",
        "Third key point"
    ],
    prev_section="6",
    next_section="8",
),
```

### Step 2: Regenerate theory_output.json

```bash
python run_all_simulations.py --export
```

### Step 3: Use in HTML

```html
<pm-section section-id="7" level="full"></pm-section>
```

## Content Blocks (Advanced)

For richer section content, use `ContentBlock` in section_registry.py:

```python
from config import SectionMetadata, ContentBlock

section = SectionMetadata(
    id="2",
    title="Geometric Framework",
    content_blocks=[
        ContentBlock(
            type="text",
            text="The framework begins with 26D spacetime..."
        ),
        ContentBlock(
            type="formula",
            formula_id="generation-number",
            show_derivation=True
        ),
        ContentBlock(
            type="callout",
            callout_type="info",
            title="Key Insight",
            children=[
                ContentBlock(
                    type="text",
                    text="This topology uniquely determines..."
                )
            ]
        )
    ]
)
```

### Supported Block Types

- **text**: Markdown/HTML text
- **formula**: Reference to formula in formula registry
- **param**: Reference to parameter
- **figure**: Image with caption
- **table**: Data table
- **callout**: Highlighted box (info, warning, derivation, example)
- **grid**: Multi-column layout
- **panel**: Grouped content

## Integration with Existing Pages

### Option 1: Replace Static Sections

Replace existing section HTML with dynamic loading:

```html
<!-- Before -->
<section id="introduction">
    <h2>1. Introduction</h2>
    <p>The Principia Metaphysica framework...</p>
</section>

<!-- After -->
<pm-section section-id="1" level="full"></pm-section>
```

### Option 2: Hybrid Approach

Keep detailed sections in separate HTML files, use dynamic loading for abstracts/summaries:

```html
<!-- Table of Contents with dynamic summaries -->
<nav>
    <pm-section section-id="1" level="summary"></pm-section>
    <pm-section section-id="2" level="summary"></pm-section>
    <pm-section section-id="3" level="summary"></pm-section>
</nav>

<!-- Full content -->
<iframe src="sections/introduction.html"></iframe>
```

## Benefits

1. **Single Source of Truth**: All section metadata lives in `section_registry.py`
2. **Consistency**: Paper and website automatically stay in sync
3. **Maintainability**: Update content in one place
4. **Flexibility**: Three display levels (summary, display, full)
5. **Extensibility**: Easy to add new sections or content types

## Troubleshooting

### Sections not loading

1. Check browser console for errors
2. Verify `theory_output.json` has `sections` key:
   ```bash
   python -c "import json; print('sections' in json.load(open('theory_output.json')))"
   ```
3. Ensure you're using a web server (not file:// protocol)
4. Check network tab to see if JSON is loading

### Section appears empty

1. Verify section ID exists in registry
2. Check `section_file` path is correct
3. Ensure `abstract` and `key_takeaways` are populated

### Styling issues

The `pm-section` component uses Shadow DOM with encapsulated styles. To customize:

1. Edit styles in `js/pm-section-renderer.js` (getStyles() method)
2. Or use CSS custom properties:
   ```css
   pm-section {
       --accent-color: #8b7fff;
       --bg-color: rgba(255, 255, 255, 0.05);
   }
   ```

## Next Steps

1. **Migrate existing sections**: Convert static HTML sections to use dynamic loading
2. **Add content blocks**: Enrich sections with structured content
3. **Create section templates**: Build reusable section layouts
4. **Implement search**: Add full-text search across all sections
5. **Add versioning**: Track section changes over time

## Files

- `section_registry.py` - Section metadata definitions
- `js/pm-section-renderer.js` - Rendering component
- `test-section-loader.html` - Test/demo page
- `theory_output.json` - Exported JSON (auto-generated)
- `run_all_simulations.py` - Export script

## Reference

- SectionMetadata class: `config.py` lines 414-479
- ContentBlock class: `config.py` lines 322-389
- PMSectionRenderer: `js/pm-section-renderer.js`
