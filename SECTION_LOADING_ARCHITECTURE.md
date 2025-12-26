# Section Loading Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Single Source of Truth                       │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  config.py       │  Defines SectionMetadata and ContentBlock classes
│  (base classes)  │  Used by section_registry.py
└────────┬─────────┘
         │
         v
┌──────────────────────────────┐
│  section_registry.py         │  Contains SECTION_REGISTRY dict
│  ════════════════════════    │
│  SECTION_REGISTRY = {        │  Metadata for all 6 sections:
│    "1": SectionMetadata(     │  - id, title, abstract
│      id="1",                  │  - beginnerSummary, keyTakeaways
│      title="Introduction",   │  - sectionFile, navigation links
│      abstract="...",          │  - contentBlocks (optional)
│      keyTakeaways=[...],     │
│      ...                      │
│    ),                         │
│    "2": ...,                  │
│    ...                        │
│  }                            │
│                               │
│  get_section_dict() ->        │  Exports to JSON-compatible dict
└────────────┬──────────────────┘
             │
             v
┌─────────────────────────────────┐
│  run_all_simulations.py         │  Main export script
│  ═══════════════════════════    │
│  from section_registry import   │  Imports section registry
│      get_section_dict           │
│                                  │
│  results = {                     │  Builds output JSON
│    'version': '14.1',            │
│    'simulations': {...},         │  Simulation results
│    'formulas': {...},            │  Formula registry
│    'parameters': {...},          │  Parameter values
│    'sections': get_section_dict() ← Sections from registry
│  }                               │
│                                  │
│  export_to_json(results)         │  Writes to file
└─────────────┬───────────────────┘
              │
              v
┌──────────────────────────────────────────────────────┐
│  theory_output.json                                  │  Generated file
│  ══════════════════                                  │
│  {                                                   │
│    "version": "14.1",                                │
│    "sections": {                                     │
│      "1": {                                          │
│        "id": "1",                                    │
│        "title": "Introduction",                      │
│        "abstract": "The Principia Metaphysica...",   │
│        "beginnerSummary": "This theory starts...",   │
│        "keyTakeaways": [                             │
│          "The framework begins with 26D...",         │
│          "Dimensional reduction via Sp(2,R)...",     │
│          ...                                         │
│        ],                                            │
│        "sectionFile": "sections/introduction.html",  │
│        "nextSection": "2"                            │
│      },                                              │
│      "2": {...},                                     │
│      ...                                             │
│    }                                                 │
│  }                                                   │
└──────────────────────┬───────────────────────────────┘
                       │
                       │ HTTP fetch()
                       v
┌────────────────────────────────────────────────────┐
│  js/pm-section-renderer.js                         │  Web Component
│  ══════════════════════════                        │
│  class PMSectionRenderer extends HTMLElement {     │
│                                                     │
│    async loadSectionData(sectionId) {              │  Loads from JSON
│      const response = await fetch(               │
│        'theory_output.json'                        │
│      );                                            │
│      const data = await response.json();           │
│      return data.sections[sectionId];              │
│    }                                               │
│                                                     │
│    renderHTML(section, level) {                    │  Renders to DOM
│      // Builds HTML from section data              │
│      // - Abstract                                 │
│      // - Beginner summary (if level='full')       │
│      // - Key takeaways                            │
│      // - Content blocks                           │
│      // - Navigation                               │
│    }                                               │
│  }                                                 │
│                                                     │
│  customElements.define('pm-section', ...)          │
└────────────────────┬───────────────────────────────┘
                     │
                     │ Custom element
                     v
┌─────────────────────────────────────────────────────┐
│  HTML Pages                                         │
│  ═══════════                                        │
│                                                      │
│  <!-- Simple usage -->                              │
│  <pm-section section-id="1"></pm-section>          │
│                                                      │
│  <!-- With display level -->                        │
│  <pm-section                                        │
│    section-id="2"                                   │
│    level="full">                                    │
│  </pm-section>                                      │
│                                                      │
│  <!-- Summary only -->                              │
│  <pm-section                                        │
│    section-id="3"                                   │
│    level="summary">                                 │
│  </pm-section>                                      │
└─────────────────────────────────────────────────────┘
```

## Component Details

### 1. Section Metadata Definition (section_registry.py)

**Purpose**: Define section content in Python
**Output**: Python dict with SectionMetadata instances

Example:
```python
"1": SectionMetadata(
    id="1",
    title="Introduction",
    abstract="Brief summary...",
    key_takeaways=["Point 1", "Point 2", ...],
    beginner_summary="Simplified explanation...",
    section_file="sections/introduction.html",
    next_section="2"
)
```

### 2. Export Pipeline (run_all_simulations.py)

**Purpose**: Convert Python metadata to JSON
**Command**: `python run_all_simulations.py --export`
**Output**: `theory_output.json` with sections

Key code:
```python
from section_registry import get_section_dict
results['sections'] = get_section_dict()
export_to_json(results, "theory_output.json")
```

### 3. Web Component (pm-section-renderer.js)

**Purpose**: Dynamically render sections in browser
**Technology**: Custom HTML Element (Web Components)
**Attributes**:
  - `section-id`: Which section to load (e.g., "1", "2")
  - `level`: Display depth ("summary", "display", "full")
  - `format`: Output format ("html" or "latex")

Key methods:
- `loadSectionData()`: Fetches from theory_output.json
- `renderHTML()`: Builds DOM from section data
- `renderContentBlock()`: Handles text, formulas, tables, etc.

### 4. Display Levels

| Level     | Shows                                           |
|-----------|-------------------------------------------------|
| summary   | Title + Abstract only                           |
| display   | Title + Abstract + Key Takeaways (default)      |
| full      | All of above + Beginner Summary + Content Blocks|

## Benefits of This Architecture

1. **Single Source of Truth**
   - Section metadata lives in ONE place (section_registry.py)
   - No duplication between paper and website
   - Easy to maintain and update

2. **Type Safety**
   - Python dataclasses provide structure
   - Validated at export time
   - Clear schema for sections

3. **Flexibility**
   - Three display levels for different contexts
   - Can add new sections without touching HTML
   - Content blocks support rich media

4. **Modularity**
   - Each component has single responsibility
   - Easy to test and debug
   - Can swap implementations

5. **Future-Proof**
   - Easy to add versioning
   - Can support LaTeX export
   - Extensible content block system

## Example Workflow

### Adding a new section:

1. **Edit section_registry.py**:
   ```python
   "7": SectionMetadata(
       id="7",
       title="New Section",
       abstract="...",
       ...
   )
   ```

2. **Regenerate JSON**:
   ```bash
   python run_all_simulations.py --export
   ```

3. **Use in HTML**:
   ```html
   <pm-section section-id="7" level="full"></pm-section>
   ```

That's it! No manual HTML editing required.

## Testing

Use `test-section-loader.html` to verify:

```bash
# Start server
python -m http.server 8000

# Open browser
http://localhost:8000/test-section-loader.html
```

The test page shows:
- Dynamic section switching
- All three display levels
- Summary view of all sections
- Error handling

## Files Created/Modified

### New Files:
- `section_registry.py` - Section metadata registry
- `test-section-loader.html` - Test page
- `DYNAMIC_SECTION_LOADING.md` - User guide
- `SECTION_LOADING_ARCHITECTURE.md` - This file

### Modified Files:
- `run_all_simulations.py` - Added section export
- `theory_output.json` - Now includes sections

### Existing Files (used):
- `config.py` - SectionMetadata and ContentBlock classes
- `js/pm-section-renderer.js` - Already existed, ready to use

## Next Steps

1. **Migrate existing content**: Move static section HTML to section_registry.py
2. **Add content blocks**: Enrich sections with structured content (formulas, tables, callouts)
3. **Update main paper**: Replace static sections with `<pm-section>` tags
4. **Add search**: Index section content for full-text search
5. **Add analytics**: Track which sections are viewed most
