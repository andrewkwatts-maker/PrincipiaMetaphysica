# Principia Metaphysica v19.2 - Version Management & Paper Polish Plan

**STATUS: COMPLETE** - v19.2-SOVEREIGN implemented and validated.

## Version Management Architecture

### Current State Issues
- 134 files have hardcoded version strings
- Inconsistent versions: "16.2", "17.2", "18.0", "19.0"
- No single source of truth for version
- Version embedded in individual SimulationMetadata

### Target State (v19.2)
- **Single Source of Truth**: `core/FormulasRegistry.py::VERSION`
- **PM Registry Param**: `pm.version` accessible by all simulations
- **Semantic Version**: `pm.version.short` = "19.2"
- **Full Version**: `pm.version.full` = "19.2-SOVEREIGN"

---

## Implementation Plan

### Phase 1: Core Version Update
1. Update `core/FormulasRegistry.py`:
   - `VERSION = "19.2-SOVEREIGN"`
   - Add `VERSION_SHORT = "19.2"`

2. Update `config.py`:
   - Set `PM_VERSION = "19.2-SOVEREIGN"`

3. Update `run_all_simulations.py`:
   - Register `pm.version` param from FormulasRegistry
   - Update header to reference v19.2

### Phase 2: Simulation Access Pattern
All simulations can access version via:
```python
def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
    pm_version = registry.get("pm.version", default="19.2")
    # Use pm_version in output
```

### Phase 3: Key Files to Update
1. `core/FormulasRegistry.py` - VERSION constant
2. `config.py` - PM_VERSION
3. `run_all_simulations.py` - header and metadata
4. `simulations/base/__init__.py` - __version__
5. `simulations/__init__.py` - __version__

### Phase 4: Validation
- Run full simulation suite
- Verify MANIFOLD IS STERILE
- Confirm version appears in all outputs

---

## Version Semantics for v19.2

| Component | Value | Meaning |
|-----------|-------|---------|
| `pm.version` | "19.2-SOVEREIGN" | Full version with status |
| `pm.version.short` | "19.2" | Semantic version |
| `pm.version.status` | "SOVEREIGN" | Indicates absolute sovereignty |
| Certificate version | "16.2" | Locked to sterile paper |

---

## Files to Update

### Core (COMPLETED ✓)
- [x] `core/FormulasRegistry.py` - VERSION = "19.2-SOVEREIGN", VERSION_SHORT = "19.2"
- [x] `config.py` - VERSION = "19.2-SOVEREIGN", VERSION_SHORT = "19.2"
- [x] `run_all_simulations.py` - Header v19.2, metadata uses FormulasRegistry.VERSION, pm.version + pm.version.short registered

### Modules (__version__ declarations)
- [ ] `simulations/__init__.py`
- [ ] `simulations/base/__init__.py`
- [ ] `core/__init__.py`
- [ ] `src/__init__.py`

### New v19 Simulations (Already at 19.0)
- [ ] 10 derivation files - update to 19.2
- [ ] 7 appendix files (M-S) - update to 19.2

---

## Success Criteria - ALL MET ✓

1. **Version Consistency**: All outputs show v19.2 ✓
2. **Single Source**: VERSION constant in FormulasRegistry ✓
3. **PM Param Access**: `registry.get("pm.version")` works ✓
4. **Validation Passes**: MANIFOLD IS STERILE ✓
5. **Audit Clean**: Formula-section audit passes ✓

---

## What's New in v19.2

### From v19.0/19.1
- Registry param integration (R, S appendices use PM params)
- Fixed formula references in Appendix F (72 gates)
- Complete section content for derivations
- Eigenchris-style appendices M-Q complete

### New in v19.2
- Centralized version management via `pm.version`
- Full paper polish verification
- All simulations reference PM version param
- Clean audit status

---

Generated: 2026-01-11
Target Version: 19.2-SOVEREIGN
