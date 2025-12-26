# Learning Resources Additions for config.py

This document contains the learning_resources fields to add to each formula in the CoreFormulas class.

## Summary

Based on `LEARNING_RESOURCES_FORMULAS_1-27.md`, the following formulas need learning resources added:

### Formulas Already Updated (✓)
1. **GENERATION_NUMBER** - Already has learning resources
2. **GUT_SCALE** - Already has learning resources

### Formulas To Update

#### 3. DARK_ENERGY_W0

Add after `related_formulas` and before `references`:

```python
        learning_resources=[
            LearningResource(
                title="Dark Energy Explained - PBS Space Time",
                url="https://www.youtube.com/c/pbsspacetime",
                type="video",
                level="beginner",
                duration="15-20 min",
                description="Introduction to dark energy and cosmic acceleration (search 'dark energy')"
            ),
            LearningResource(
                title="Dark Energy - Edmund Copeland, M. Sami, Shinji Tsujikawa",
                url="https://arxiv.org/abs/hep-th/0603057",
                type="article",
                level="intermediate",
                duration="~4 hours reading",
                description="Comprehensive review of dark energy models and equation of state w(z)"
            ),
            LearningResource(
                title="Modern Cosmology - Scott Dodelson & Fabian Schmidt",
                url="https://www.sciencedirect.com/book/9780128159484/modern-cosmology",
                type="textbook",
                level="advanced",
                description="Standard modern cosmology textbook (Chapters 6-8 on dark energy, equation of state, observational tests)"
            ),
        ],
```

#### 4. PROTON_LIFETIME

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="Proton Decay - Wikipedia",
                url="https://en.wikipedia.org/wiki/Proton_decay",
                type="article",
                level="beginner",
                description="Phenomenon, experimental bounds, and theoretical predictions from GUT theories"
            ),
            LearningResource(
                title="Proton Decay in GUT Theories - Review",
                url="https://arxiv.org/abs/hep-ph/0001293",
                type="article",
                level="intermediate",
                duration="~2 hours reading",
                description="Theoretical framework for proton decay in grand unified theories"
            ),
            LearningResource(
                title="The Standard Model and Beyond - Paul Langacker",
                url="https://www.routledge.com/The-Standard-Model-and-Beyond/Langacker/p/book/9781420079067",
                type="textbook",
                level="advanced",
                description="Comprehensive treatment of proton decay in GUTs (Chapters 12-13 on proton decay, dimension-6 operators)"
            ),
        ],
```

#### 5. THETA23_MAXIMAL

Add after `related_formulas` and before `references`:

```python
        learning_resources=[
            LearningResource(
                title="Neutrino Oscillations Explained - Fermilab",
                url="https://www.youtube.com/user/fermilab",
                type="video",
                level="beginner",
                duration="10-15 min",
                description="Introduction to neutrino masses and mixing including atmospheric angle"
            ),
            LearningResource(
                title="TASI Lectures on Neutrino Physics - André de Gouvêa",
                url="https://arxiv.org/abs/hep-ph/0411274",
                type="article",
                level="intermediate",
                duration="~4 hours reading",
                description="Comprehensive lecture notes on neutrino masses and mixing including PMNS matrix"
            ),
            LearningResource(
                title="Fundamentals of Neutrino Physics and Astrophysics - Giunti & Kim",
                url="https://global.oup.com/academic/product/fundamentals-of-neutrino-physics-and-astrophysics-9780198508717",
                type="textbook",
                level="advanced",
                description="Standard reference for neutrino physics (Chapters 6-8 on PMNS matrix, mass hierarchy, oscillations)"
            ),
        ],
```

#### 6. KK_GRAVITON

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="Extra Dimensions Explained - PBS Space Time",
                url="https://www.youtube.com/c/pbsspacetime",
                type="video",
                level="beginner",
                duration="15-20 min",
                description="Introduction to compactified dimensions and Kaluza-Klein theory"
            ),
            LearningResource(
                title="Extra Dimensions in Particle Physics - Review",
                url="https://arxiv.org/abs/hep-ph/0404175",
                type="article",
                level="intermediate",
                duration="~3 hours reading",
                description="Phenomenology of extra dimensions and KK graviton signals"
            ),
            LearningResource(
                title="Gravity and Strings - Tomás Ortín",
                url="https://www.cambridge.org/core/books/gravity-and-strings/",
                type="textbook",
                level="advanced",
                description="Modern treatment of dimensional reduction (Chapters 8-9 on Kaluza-Klein reduction, compactification)"
            ),
        ],
```

#### 7. MASTER_ACTION_26D

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="String Theory Explained - PBS Space Time",
                url="https://www.youtube.com/c/pbsspacetime",
                type="video",
                level="beginner",
                duration="15-20 min",
                description="Accessible introduction to string theory basics, critical dimension, and extra dimensions (search 'String Theory')"
            ),
            LearningResource(
                title="Lectures on String Theory - David Tong",
                url="http://www.damtp.cam.ac.uk/user/tong/string.html",
                type="article",
                level="intermediate",
                duration="~10 hours reading",
                description="Excellent freely available lecture notes with clear explanations of 26D bosonic string"
            ),
            LearningResource(
                title="String Theory Vol. 1 - Polchinski",
                url="https://doi.org/10.1017/CBO9780511816079",
                type="textbook",
                level="advanced",
                description="Standard graduate-level reference for string theory (Chapters 2-3 on Virasoro algebra, BRST quantization)"
            ),
        ],
```

#### 8. VIRASORO_ANOMALY

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="Virasoro Algebra - Wikipedia",
                url="https://en.wikipedia.org/wiki/Virasoro_algebra",
                type="article",
                level="beginner",
                description="Overview of central extension and highest-weight representations"
            ),
            LearningResource(
                title="Introduction to Conformal Field Theory - Joshua Qualls",
                url="https://arxiv.org/abs/1511.04074",
                type="article",
                level="intermediate",
                duration="~3 hours reading",
                description="Modern lecture notes on CFT with emphasis on Virasoro algebra and central charge"
            ),
            LearningResource(
                title="Conformal Field Theory - Di Francesco, Mathieu, Sénéchal",
                url="https://link.springer.com/book/10.1007/978-1-4612-2256-9",
                type="textbook",
                level="advanced",
                description="Comprehensive reference for conformal field theory and Virasoro algebra (Chapters 5-7 on central charge, representations)"
            ),
        ],
```

#### 9. SP2R_CONSTRAINTS

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="Symplectic Group - Wikipedia",
                url="https://en.wikipedia.org/wiki/Symplectic_group",
                type="article",
                level="beginner",
                description="Sp(2,R) as special case of symplectic groups"
            ),
            LearningResource(
                title="Survey of Two-Time Physics - Itzhak Bars",
                url="https://arxiv.org/abs/hep-th/0008164",
                type="article",
                level="intermediate",
                duration="~2 hours reading",
                description="Overview of 2T-physics and Sp(2,R) gauge symmetry by the original developer"
            ),
            LearningResource(
                title="Gauge Symmetry and Supersymmetry of Multiple M2-Branes - Bars",
                url="https://arxiv.org/abs/0904.3986",
                type="article",
                level="advanced",
                description="Applications of Sp(2,R) to M-theory and two-time physics framework"
            ),
        ],
```

#### 10. TCS_TOPOLOGY (if exists in CoreFormulas)

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="Betti Numbers - Wikipedia",
                url="https://en.wikipedia.org/wiki/Betti_number",
                type="article",
                level="beginner",
                description="Topological invariants (b₂, b₃) used in TCS construction"
            ),
            LearningResource(
                title="Twisted Connected Sums and G₂ Manifolds - Corti et al.",
                url="https://arxiv.org/abs/1510.07068",
                type="article",
                level="intermediate",
                duration="~5 hours reading",
                description="Construction of TCS G₂ manifolds with specific topology including χ_eff = 144"
            ),
            LearningResource(
                title="Introduction to G₂ Geometry - Spiro Karigiannis",
                url="https://arxiv.org/abs/0807.3858",
                type="article",
                level="advanced",
                description="Comprehensive mathematical treatment of G₂ manifolds and their topological invariants"
            ),
        ],
```

#### 11. THERMAL_TIME (if exists)

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="KMS State - Wikipedia",
                url="https://en.wikipedia.org/wiki/KMS_state",
                type="article",
                level="beginner",
                description="Kubo-Martin-Schwinger thermal equilibrium condition"
            ),
            LearningResource(
                title="Thermal Time and the Tolman-Ehrenfest Effect - Connes & Rovelli",
                url="https://arxiv.org/abs/gr-qc/9406019",
                type="article",
                level="intermediate",
                duration="~2 hours reading",
                description="Original paper on thermal time hypothesis proposing emergent time from statistical flow"
            ),
            LearningResource(
                title="Operator Algebras and Quantum Statistical Mechanics - Bratteli & Robinson",
                url="https://link.springer.com/book/10.1007/978-3-662-02520-8",
                type="textbook",
                level="advanced",
                description="Definitive mathematical reference (Vol. 2, Ch. 5 on Tomita-Takesaki theory, KMS states)"
            ),
        ],
```

#### 12. CLIFFORD_26D (if exists)

Add after `related_formulas`:

```python
        learning_resources=[
            LearningResource(
                title="Clifford Algebra - Wikipedia",
                url="https://en.wikipedia.org/wiki/Clifford_algebra",
                type="article",
                level="beginner",
                description="Mathematical structure and classification of Clifford algebras"
            ),
            LearningResource(
                title="Clifford Algebras and Spin Representations - Lecture Notes",
                url="https://arxiv.org/",
                type="article",
                level="intermediate",
                duration="~3 hours reading",
                description="Pedagogical introductions to Clifford algebras and spinor representations (search arXiv for 'Clifford algebra lectures')"
            ),
            LearningResource(
                title="Clifford Algebras and Spinors - Pertti Lounesto",
                url="https://www.cambridge.org/core/books/clifford-algebras-and-spinors/",
                type="textbook",
                level="advanced",
                description="Comprehensive mathematical treatment (Chapters 4-6 on Spin groups, spinor representations, dimension 8192 = 2^13)"
            ),
        ],
```

## Additional Formulas from Learning Resources Document

The following formulas are mentioned in the learning resources document but may need to be checked:

- **SO10_BREAKING**: Gauge theory resources
- **GUT_COUPLING**: Renormalization group resources
- **WEAK_MIXING_ANGLE**: Gauge unification resources
- **THETA12_SOLAR**: Neutrino physics resources
- **SEESAW_MECHANISM**: Already has resources (line 1736 in config.py)
- **NORMAL_HIERARCHY**: Neutrino physics resources

## Implementation Instructions

For each formula above:

1. Locate the formula definition in `config.py`
2. Find the `related_formulas=` line
3. Check if there's already a `references=` field
4. If `references=` exists, add `learning_resources=` BEFORE it
5. If `references=` doesn't exist, add `learning_resources=` AFTER `related_formulas=` and before the closing parenthesis

## Verification

After adding all resources, verify by:

1. Running `python config.py` to check for syntax errors
2. Searching for `learning_resources=` to count how many formulas now have resources
3. Exporting formulas with `CoreFormulas.export_formulas()` and checking the JSON output
4. Ensuring all LearningResource objects have:
   - title (required)
   - url (required)
   - type (video, article, textbook, interactive)
   - level (beginner, intermediate, advanced)
   - duration (optional, for videos/articles)
   - description (optional but recommended)

## Statistics

- Total formulas in learning resources document: 55
- Formulas already with learning resources: 2 (GENERATION_NUMBER, GUT_SCALE)
- Formulas to be updated: ~10-15 core formulas (from user request)
- Target coverage: All major theory formulas (sections 2-7)
