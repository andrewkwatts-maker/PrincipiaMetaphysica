# Centralized Content Management System

**Created:** 2025-12-05
**Version:** 1.0
**Status:** Operational, ready for migration

## Overview

The Principia Metaphysica now has a centralized content management system that ensures all numerical values, section content, and topic structure come from a single source of truth. This eliminates inconsistencies between the paper and website, enables validation of completeness, and provides full traceability from content to simulation output.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SINGLE SOURCE OF TRUTH                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  config.py → simulations → theory_output.json                  │
│       ↓                                                         │
│  sections_content.py (content structure)                       │
│       ↓                                                         │
│  generate_enhanced_constants.py (export to JS)                 │
│       ↓                                                         │
│  theory-constants-enhanced.js (PM.sections + PM.*)             │
│       ↓                                                         │
│  HTML pages (load content + populate values dynamically)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. sections_content.py (350 lines)
**Purpose:** Single source of truth for all section/page content

**Features:**
- `SECTIONS` dictionary with recursive topic structure
- Full metadata: title, subtitle, content, pages, values
- Unlimited topic nesting
- Helper functions: `get_section()`, `get_pages_for_section()`, `get_required_values()`, `get_topic_by_id()`

**Structure:**
```python
SECTIONS = {
    "geometric_framework": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/sections/geometric-framework.html",
                "section": "",
                "order": 1,
                "include": ["title", "content", "topics", "values"],
                "hover_details": True,
                "template_type": "Section Page"
            }
        ],
        "title": "Section 1: Geometric Framework",
        "subtitle": "26D → 13D → 4D Dimensional Reduction",
        "content": "...",
        "values": ["D_bulk", "D_after_sp2r", "chi_eff", "n_gen"],
        "topics": [
            {
                "id": "dimensional_reduction",
                "title": "Dimensional Reduction Pathway",
                "values": ["D_bulk", "D_after_sp2r"],
                "topics": [  # Recursive!
                    {
                        "id": "sp2r_projection",
                        "title": "Sp(2,R) Gauge Fixing",
                        "template_type": "mechanism_card"
                    }
                ]
            }
        ]
    }
}
```

**Currently Implemented:**
- ✅ `abstract` (2 pages: index.html, paper.html)
- ✅ `geometric_framework` (2 pages, 3 topics with recursive sub-topics)
- ⚠️ Other sections (placeholders ready for implementation)

### 2. validate_magic_numbers.py (250 lines)
**Purpose:** Find hardcoded numerical values that should use PM references

**Detects:**
- Scientific notation: `2.1×10¹⁶`, `1.23e16`
- Decimal values: `w₀ = -0.8528`, `χ_eff = 144`
- Tensions: `6σ`, `0.38σ`
- OOM uncertainties: `0.177 OOM`
- M_GUT values
- Percentages (predictions)

**Pattern Matching:**
```python
MAGIC_NUMBER_PATTERNS = [
    (r'(?<!data-param=")w₀\s*=\s*[−-]?(0\.\d+)', 'w0_value',
     'Use PM.dark_energy.w0_PM'),
    (r'(?<!data-param=")χ_eff\s*=\s*(\d+)', 'chi_value',
     'Use PM.topology.chi_eff'),
    # ... more patterns
]
```

**Usage:**
```bash
python validate_magic_numbers.py
```

**Output:**
- `MAGIC_NUMBERS_REPORT.txt` - Human-readable report
- `MAGIC_NUMBERS_REPORT.json` - Machine-readable for agents

**Current Results:**
- 20 files scanned
- 712 potential issues found
- Top files: beginners-guide.html (48), predictions.html (124 topics)

### 3. validate_topic_implementation.py (300 lines)
**Purpose:** Validate pages implement topics defined in sections_content.py

**Checks:**
- Missing topic sections in HTML files
- Orphaned content not defined in sections_content.py
- Inconsistent topic structure between pages
- Required PM values exist

**Validation Statuses:**
- `complete`: All expected topics present
- `partial`: Some topics present (>50%)
- `incomplete`: Few topics present (<50%)
- `not_in_sections_content`: Page not yet defined

**Usage:**
```bash
python validate_topic_implementation.py
```

**Output:**
- `TOPIC_VALIDATION_REPORT.txt` - Status by page
- `TOPIC_MIGRATION_PLAN.json` - Migration strategy

**Current Results:**
```
Total pages: 20
  Complete: 0
  Incomplete: 2 (paper.html, geometric-framework.html)
  Not Defined: 18

Priority 1 (Incomplete): 2 pages
  - principia-metaphysica-paper.html (missing: dimensional_reduction, euler_characteristic)
  - sections/geometric-framework.html (missing: dimensional_reduction, euler_characteristic, so10_emergence)

Priority 3 (Not Defined): 18 pages
  - index.html (67 topics found)
  - predictions.html (124 topics found)
  - cosmology.html (54 topics found)
  - ... etc
```

### 4. theory-constants-enhanced.js (Updated)
**New Section:** `PM.sections`

**Structure:**
```javascript
PM.sections = {
  "meta": {
    "description": "Section content metadata for paper and website",
    "version": "1.0",
    "last_updated": "2025-12-05"
  },
  "abstract": {
    "title": "Abstract",
    "subtitle": "A 26D Two-Time Framework...",
    "content": "...",
    "pages": [...],
    "values": [],
    "required_values": []
  },
  "geometric_framework": {
    "title": "Section 1: Geometric Framework",
    "subtitle": "26D → 13D → 4D Dimensional Reduction",
    "content": "...",
    "pages": [
      {
        "file": "https://www.metaphysicæ.com/sections/geometric-framework.html",
        "include": ["title", "content", "topics", "values"]
      }
    ],
    "values": ["D_bulk", "D_after_sp2r", "chi_eff", "n_gen"],
    "required_values": ["dimensions.D_bulk", "dimensions.D_after_sp2r", ...]
  }
}
```

**Usage in HTML:**
```html
<script src="../theory-constants-enhanced.js"></script>
<script>
  // Load section content
  const section = PM.sections.geometric_framework;
  document.getElementById('section-title').textContent = section.title;
  document.getElementById('section-content').textContent = section.content;

  // Populate values
  section.required_values.forEach(valueId => {
    const [category, param] = valueId.split('.');
    const value = PM[category][param];
    // ... populate into page
  });
</script>
```

### 5. tests/test-dynamic-content.html
**Purpose:** Demonstrate dynamic content loading

**5 Tests:**
1. **Load Section Metadata** - ✅ Shows all sections with counts
2. **Render Section Content** - ✅ Loads title/subtitle/content dynamically
3. **Populate Values from PM** - ✅ Shows required_values with status
4. **Render Topics Recursively** - ⚠️ Requires full implementation
5. **Validate Required Values** - ✅ Checks all values exist

**Features:**
- Frosted glass cards
- Color-coded status (green = found, yellow = missing)
- Live validation
- Ready for expansion to full page rendering

**Open in Browser:**
```
file:///h:/Github/PrincipiaMetaphysica/tests/test-dynamic-content.html
```

## Current Status

### ✅ Completed
- [x] Created sections_content.py with recursive topic structure
- [x] Created validate_magic_numbers.py to find hardcoded values
- [x] Updated generate_enhanced_constants.py to merge section metadata
- [x] Ran validation scripts and analyzed findings
- [x] Created content loading prototype (test-dynamic-content.html)
- [x] Created validation script for topic implementation status
- [x] Generated migration plan
- [x] Committed all changes to repository

### 📊 Validation Results

**Magic Numbers:**
- 712 potential hardcoded values found across 20 files
- All logged in MAGIC_NUMBERS_REPORT.json with PM reference suggestions

**Topic Implementation:**
- 2 pages partially implemented (geometric_framework defined)
- 18 pages need sections_content.py definitions
- Migration plan created with priorities

**PM Constants:**
- 70 total constants across 14 categories
- `PM.sections` category added with metadata
- All sections linked to required PM values

## Migration Plan

### Phase 1: Define All Sections (Priority 3)
**Goal:** Add all sections to sections_content.py

**Tasks:**
1. Define cosmology section with topics
2. Define gauge_unification section with topics
3. Define fermion_sector section with topics
4. Define predictions section with topics
5. Define thermal_time section with topics
6. Define pneuma_lagrangian section with topics
7. Define conclusion section with topics
8. Define all other sections

**Estimate:** 5-8 hours (can deploy agents in parallel)

### Phase 2: Fix Incomplete Pages (Priority 1)
**Goal:** Add missing topics to pages that have sections defined

**Tasks:**
1. **principia-metaphysica-paper.html**
   - Add `id="dimensional_reduction"` section
   - Add `id="euler_characteristic"` section
2. **sections/geometric-framework.html**
   - Add `id="dimensional_reduction"` section
   - Add `id="euler_characteristic"` section
   - Add `id="so10_emergence"` section

**Estimate:** 2-4 hours

### Phase 3: Replace Hardcoded Values (Ongoing)
**Goal:** Replace 712 hardcoded values with PM references

**Strategy:**
- Use MAGIC_NUMBERS_REPORT.json as task list
- Deploy agents to process files in parallel
- Verify with validate_magic_numbers.py

**Estimate:** 3-5 hours (agents can run in parallel)

### Phase 4: Enable Full Dynamic Rendering (Future)
**Goal:** Expand test-dynamic-content.html to full page generator

**Tasks:**
1. Implement topic rendering from recursive structure
2. Auto-generate panels from metadata
3. Create page templates for different template_type values
4. Update all HTML pages to load from PM.sections

**Estimate:** 8-12 hours

## Usage Examples

### Adding a New Section

1. **Define in sections_content.py:**
```python
SECTIONS['cosmology'] = {
    'pages': [
        {
            'file': 'https://www.metaphysicæ.com/sections/cosmology.html',
            'include': ['title', 'content', 'topics', 'values']
        }
    ],
    'title': 'Section 6: Cosmological Dynamics',
    'subtitle': 'Dark Energy and the MEP Attractor',
    'content': '...',
    'values': ['w0_from_d_eff', 'w0_DESI_central', 'planck_tension_resolved'],
    'topics': [
        {
            'id': 'dark_energy_derivation',
            'title': 'Dark Energy from Effective Dimensions',
            'values': ['d_eff', 'w0_from_d_eff']
        }
    ]
}
```

2. **Regenerate constants:**
```bash
python generate_enhanced_constants.py
```

3. **Validate:**
```bash
python validate_topic_implementation.py
```

4. **Update HTML page:**
```html
<div id="dark_energy_derivation">
  <h3>Dark Energy from Effective Dimensions</h3>
  <p>w₀ = <span class="pm-value" data-category="dark_energy" data-param="w0_from_d_eff"></span></p>
</div>
```

### Finding Hardcoded Values

```bash
# Run scanner
python validate_magic_numbers.py

# Check report
cat MAGIC_NUMBERS_REPORT.txt

# Use JSON for agent processing
cat MAGIC_NUMBERS_REPORT.json
```

### Checking Topic Implementation

```bash
# Run validator
python validate_topic_implementation.py

# Check report
cat TOPIC_VALIDATION_REPORT.txt

# Check migration plan
cat TOPIC_MIGRATION_PLAN.json
```

## Benefits

✅ **Single Source of Truth**
- All content defined once in sections_content.py
- No duplication between paper and website

✅ **Automatic Consistency**
- Changes propagate to all pages automatically
- No manual syncing required

✅ **Full Validation**
- Ensures all topics implemented
- Ensures all required values exist
- Finds hardcoded values

✅ **Complete Traceability**
- Content → sections_content.py
- Values → theory_output.json → simulations → config.py
- Topics → recursive structure with metadata

✅ **Easy Maintenance**
- Update content in one place
- Regenerate with one command
- Validate with scripts

✅ **No Orphaned Content**
- Validation catches content not in sections_content.py
- Migration plan identifies undefined pages

## Files Created/Modified

### New Files
- `sections_content.py` - Content structure definition
- `validate_magic_numbers.py` - Hardcoded value scanner
- `validate_topic_implementation.py` - Topic validator
- `tests/test-dynamic-content.html` - Dynamic loading prototype
- `MAGIC_NUMBERS_REPORT.txt` - Human-readable scan results
- `MAGIC_NUMBERS_REPORT.json` - Machine-readable scan results
- `TOPIC_VALIDATION_REPORT.txt` - Topic validation results
- `TOPIC_MIGRATION_PLAN.json` - Migration strategy

### Modified Files
- `generate_enhanced_constants.py` - Added sections metadata export
- `theory-constants-enhanced.js` - Added PM.sections (70 constants total)

## Next Steps

1. **Define remaining sections** in sections_content.py
   - Use TOPIC_MIGRATION_PLAN.json to prioritize
   - 18 pages need definitions

2. **Fix incomplete pages**
   - Add missing topic sections to paper.html and geometric-framework.html
   - 2 pages, 5 topics total

3. **Replace hardcoded values**
   - Use MAGIC_NUMBERS_REPORT.json as task list
   - Deploy agents to process files in parallel
   - 712 values to update

4. **Expand dynamic rendering**
   - Build on test-dynamic-content.html prototype
   - Create full page generator
   - Update all HTML pages

## Support

For questions or issues:
- Review validation reports in repository root
- Check test-dynamic-content.html for examples
- Run validators to check current status

---

**Copyright (c) 2025 Andrew Keith Watts. All rights reserved.**

Developed with assistance from Claude (Anthropic), Grok (xAI), and Gemini (Google).
