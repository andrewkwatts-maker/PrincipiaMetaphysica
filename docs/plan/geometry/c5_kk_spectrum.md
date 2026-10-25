# C5: exact scalar-Laplacian KK spectrum on T^7/Gamma (Joyce Ex.3, Z2^3, (b2,b3)=(12,43))
Code: metaphysica-kkspec/src/metaphysica/simulations/PM/geometry/kk_spectrum.py (uncommitted); tests/test_kk_spectrum.py.
Method: modes e^{2 pi i k.x}; g=(eps,s): x->eps*x+s/2 gives trace sum over eps-fixed k of (-1)^{k.s}; mult = (1/8) sum_g trace. Integer arithmetic only. Gamma = canonical_point() elements (same as Joyce's alpha, beta, gamma).
First 8 levels, at the symmetric point R_1..R_7 equal (a choice); q = |k|^2, eigenvalue 4 pi^2 q/R^2:
 q | mult T^7 | mult T^7/Gamma | m_n/m_1 (symmetric point)
 1 | 14 | 4 | 1
 2 | 84 | 13 | 1.4142
 3 | 280 | 38 | 1.7321
 4 | 574 | 77 | 2
 5 | 840 | 114 | 2.2361
 6 | 1288 | 166 | 2.4495
 7 | 2368 | 296 | 2.6458
 8 | 3444 | 441 | 2.8284
Zero mode: 1 (checked, raises otherwise). Level 1 hand-checked: only k=+-e_1..e_4 survive (e_5..e_7 are killed by the half-shifts), 4 of 14.
Radius-independent: Gamma and its shifts; multiplicity per |k|-vector class (generic_classes: e.g. e_1..e_4 give 1, e_5..e_7 give 0); which classes exist or are absent; zero mode = 1.
Radius-dependent (moduli): how classes merge into levels, the level order, all ratios m_n/m_1 = sqrt(q_n/q_1). Equal-radii ratios are sqrt(n), a symmetric-point choice, not predictions. No number here is tied to experiment.
Symmetry note: the only coordinate permutation preserving Gamma (with shifts) is the identity, so radii cannot be permuted freely on T^7/Gamma; permuting radii together with Gamma is a covariance (tested).
Engine assumption: config/parameters/shared_dimensions.py sets M_KK_1=5.02 TeV, M_KK_2=10.04, M_KK_3=15.06 (linear n*M_KK, circle-like tower), M_KK_CENTRAL=5 TeV; G56 uses M_KK=M_Pl/(b3 k_gimel^2). Not consistent with this spectrum: the flat T^7/Gamma tower is sqrt(q) with ratios 1, 1.414, 1.732 at the symmetric point, not 1, 2, 3; for generic radii the ratios are free. The absolute scale is a modulus (R) not fixed by the lattice; the 5 TeV value is an input, not derived here.
Tests: 8 collected, 8 passed (pytest tests/test_kk_spectrum.py, 2.3 s).
