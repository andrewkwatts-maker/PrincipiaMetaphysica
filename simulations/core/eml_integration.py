"""
EML Math Integration Utilities
================================

Provides helper functions for implementing EML Math computation paths
in Principia Metaphysica simulations.

The EML Sheffer operator: eml(x, y) = exp(x) - ln(y)
All 36 elementary functions are generated from this single operator.

Usage in simulation run_eml() methods:
    from simulations.core.eml_integration import (
        eml_scalar, eml_compute, eml_pi, eml_add, eml_mul, eml_div,
        eml_sub, eml_neg, eml_sqrt, eml_pow, eml_exp, eml_ln,
        eml_sin, eml_cos, eml_agree, eml_tree_str
    )

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from __future__ import annotations

import math
from typing import Union

try:
    from eml_math import EMLPoint, EMLPair, EMLState, EMLNDVector
    from eml_math import operators as ops
    from eml_math import (
        MetricTensor, Octonion, EMLMultivector,
        FourMomentum, MinkowskiFourVector,
        e8_lattice_points, leech_lattice_points,
        PLANCK_D,
    )
    EML_AVAILABLE = True
except ImportError:
    EML_AVAILABLE = False


# ── Type alias ────────────────────────────────────────────────────────────────

_Num = Union[float, int]


# ── Availability guard ────────────────────────────────────────────────────────

def require_eml() -> None:
    """Raise ImportError with install instructions if eml_math is not available."""
    if not EML_AVAILABLE:
        raise ImportError(
            "eml_math is not installed. Install with: pip install eml-math"
        )


# ── Core scalar helpers ───────────────────────────────────────────────────────

def eml_scalar(v: _Num) -> "EMLPoint":
    """
    Wrap a scalar value as an EMLPoint literal node.

    EMLPoint(log(|v|), 1.0): tension() = exp(log(|v|)) - ln(1) = |v|.
    For v < 0: returns ops.neg(EMLPoint(log(-v), 1.0)) so tension() = v.
    For v == 0: returns EMLPoint(-1e300, 1.0) (tension ≈ 0).
    """
    require_eml()
    fv = float(v)
    if fv == 0.0:
        return EMLPoint(-1e300, 1.0)
    elif fv > 0:
        return EMLPoint(math.log(fv), 1.0)
    else:
        return ops.neg(EMLPoint(math.log(-fv), 1.0))


def eml_lit(v: _Num) -> "EMLPoint":
    """
    Wrap a value as a literal EMLPoint constant (same as eml_scalar).
    Alias for clarity in formula trees.
    """
    return eml_scalar(v)


def eml_compute(expr: "EMLPoint") -> float:
    """Evaluate an EML expression tree to a float via .tension()."""
    require_eml()
    return float(expr.tension())


# ── EML constant factories ────────────────────────────────────────────────────

def eml_pi() -> "EMLPoint":
    """π as an EMLPoint literal."""
    require_eml()
    return eml_scalar(math.pi)


def eml_e() -> "EMLPoint":
    """Euler's number e as EMLPoint. Value: ops.exp(1)."""
    require_eml()
    return ops.exp(eml_scalar(1.0))


def eml_two_pi() -> "EMLPoint":
    """2π as EMLPoint tree."""
    require_eml()
    return ops.mul(eml_scalar(2.0), eml_pi())


def eml_four_pi() -> "EMLPoint":
    """4π as EMLPoint tree."""
    require_eml()
    return ops.mul(eml_scalar(4.0), eml_pi())


# ── Arithmetic operator wrappers ──────────────────────────────────────────────

def eml_add(a: Union[_Num, "EMLPoint"], b: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """a + b via EML operator tree."""
    require_eml()
    return ops.add(_ensure_eml(a), _ensure_eml(b))


def eml_sub(a: Union[_Num, "EMLPoint"], b: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """a - b via EML operator tree."""
    require_eml()
    return ops.sub(_ensure_eml(a), _ensure_eml(b))


def eml_mul(a: Union[_Num, "EMLPoint"], b: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """a × b via EML operator tree."""
    require_eml()
    return ops.mul(_ensure_eml(a), _ensure_eml(b))


def eml_div(a: Union[_Num, "EMLPoint"], b: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """a / b via EML operator tree."""
    require_eml()
    return ops.div(_ensure_eml(a), _ensure_eml(b))


def eml_neg(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """-x via EML operator tree."""
    require_eml()
    return ops.neg(_ensure_eml(x))


def eml_inv(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """1/x via EML operator tree."""
    require_eml()
    return ops.inv(_ensure_eml(x))


def eml_sqrt(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """√x via EML operator tree."""
    require_eml()
    return ops.sqrt(_ensure_eml(x))


def eml_sqr(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """x² via EML operator tree."""
    require_eml()
    return ops.sqr(_ensure_eml(x))


def eml_pow(base: Union[_Num, "EMLPoint"], exp: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """
    base^exp = exp(exp_val × ln(base)) via EML operator tree.

    Handles 0 < base < 1 case: ops.mul drops signs, so when ln(base) < 0
    we negate both sides: exp(-(exp_val × |ln(base)|)).
    """
    require_eml()
    b_pt = _ensure_eml(base)
    e_pt = _ensure_eml(exp)
    ln_b = ops.ln(b_pt)
    if float(ln_b.tension()) >= 0:
        return ops.exp(ops.mul(e_pt, ln_b))
    else:
        return ops.exp(ops.neg(ops.mul(e_pt, ops.neg(ln_b))))


def eml_exp(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """e^x via EML operator tree."""
    require_eml()
    return ops.exp(_ensure_eml(x))


def eml_ln(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """ln(x) via EML operator tree."""
    require_eml()
    return ops.ln(_ensure_eml(x))


def eml_sin(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """sin(x) via EML operator tree."""
    require_eml()
    return ops.sin(_ensure_eml(x))


def eml_cos(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """cos(x) via EML operator tree."""
    require_eml()
    return ops.cos(_ensure_eml(x))


def eml_tan(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """tan(x) via EML operator tree."""
    require_eml()
    return ops.tan(_ensure_eml(x))


def eml_sinh(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """sinh(x) via EML operator tree."""
    require_eml()
    return ops.sinh(_ensure_eml(x))


def eml_cosh(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """cosh(x) via EML operator tree."""
    require_eml()
    return ops.cosh(_ensure_eml(x))


def eml_tanh(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """tanh(x) via EML operator tree."""
    require_eml()
    return ops.tanh(_ensure_eml(x))


def eml_arcsin(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """arcsin(x) via EML operator tree."""
    require_eml()
    return ops.arcsin(_ensure_eml(x))


def eml_arccos(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """arccos(x) via EML operator tree."""
    require_eml()
    return ops.arccos(_ensure_eml(x))


def eml_arctan(x: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """arctan(x) via EML operator tree."""
    require_eml()
    return ops.arctan(_ensure_eml(x))


def eml_avg(a: Union[_Num, "EMLPoint"], b: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """Arithmetic mean (a+b)/2 via EML operator tree."""
    require_eml()
    return ops.avg(_ensure_eml(a), _ensure_eml(b))


def eml_hypot(a: Union[_Num, "EMLPoint"], b: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """√(a²+b²) via EML operator tree."""
    require_eml()
    return ops.hypot(_ensure_eml(a), _ensure_eml(b))


# ── Compound physics helpers ──────────────────────────────────────────────────

def eml_ratio(numerator: _Num, denominator: _Num) -> float:
    """Compute numerator/denominator via EML div and return float."""
    require_eml()
    return eml_compute(eml_div(eml_scalar(numerator), eml_scalar(denominator)))


def eml_product(*factors: _Num) -> float:
    """Compute product of all factors via EML mul chain and return float."""
    require_eml()
    if not factors:
        return 1.0
    result = eml_scalar(factors[0])
    for f in factors[1:]:
        result = eml_mul(result, eml_scalar(f))
    return eml_compute(result)


def eml_sum_of_squares(*values: _Num) -> float:
    """Compute Σ(vᵢ²) via EML and return float."""
    require_eml()
    result = eml_scalar(0.0)
    for v in values:
        result = eml_add(result, eml_sqr(eml_scalar(v)))
    return eml_compute(result)


def eml_normalize_angle(theta_deg: _Num) -> float:
    """Convert degrees to radians via EML: θ_rad = θ_deg × π / 180."""
    require_eml()
    return eml_compute(
        eml_div(eml_mul(eml_scalar(theta_deg), eml_pi()), eml_scalar(180.0))
    )


# ── G₂ geometry helpers ───────────────────────────────────────────────────────

def eml_g2_metric() -> "MetricTensor":
    """Return the G₂-holonomy metric tensor from eml_math."""
    require_eml()
    return MetricTensor.g2_holonomy()


def eml_e8_points(n: int = 240, scale: float = 1.0) -> list:
    """Return E₈ root lattice points (240 minimal vectors) as EMLNDVectors."""
    require_eml()
    return e8_lattice_points(n_points=n, scale=scale)


def eml_leech_points(n: int = 24, scale: float = 1.0) -> list:
    """Return Leech lattice (24D) sample points as EMLNDVectors."""
    require_eml()
    return leech_lattice_points(n_points=n, scale=scale)


def eml_octonion_norm(components: list) -> float:
    """Compute the norm of an octonion with given real components via EML."""
    require_eml()
    pts = [eml_scalar(c) for c in components]
    o = Octonion(pts)
    return float(o.norm())


def eml_g2_chi_eff(b3: int = 24) -> float:
    """
    Compute χ_eff = 4 × b₃ × n_gen = 4 × 24 × 3 = 288 from EML topology.
    n_gen = χ_eff / (4 × b₃) → χ_eff = 144 for standard PM (6 × 24).
    """
    require_eml()
    six = eml_scalar(6.0)
    b3_pt = eml_scalar(float(b3))
    return eml_compute(eml_mul(six, b3_pt))


def eml_n_gen(chi_eff: float, b3: int = 24) -> float:
    """n_gen = χ_eff / (4 × b₃) via EML."""
    require_eml()
    return eml_compute(
        eml_div(eml_scalar(chi_eff), eml_mul(eml_scalar(4.0), eml_scalar(float(b3))))
    )


# ── Agreement checking ────────────────────────────────────────────────────────

def eml_agree(normal_val: float, eml_val: float, rtol: float = 1e-6) -> bool:
    """
    Check that normal_val and eml_val agree within relative tolerance.

    Uses: |normal - eml| / max(|normal|, 1e-300) < rtol
    Integer / zero special cases handled.
    """
    if normal_val == eml_val:
        return True
    if normal_val == 0.0:
        return abs(eml_val) < rtol
    rel_diff = abs(normal_val - eml_val) / max(abs(normal_val), 1e-300)
    return rel_diff < rtol


def eml_deviation(normal_val: float, eml_val: float) -> float:
    """Return the relative deviation |normal - eml| / |normal|."""
    if normal_val == 0.0:
        return abs(eml_val)
    return abs(normal_val - eml_val) / max(abs(normal_val), 1e-300)


# ── Tree string representation ────────────────────────────────────────────────

def eml_tree_str(expr: "EMLPoint") -> str:
    """
    Return a compact string representation of an EML expression tree.
    Falls back to repr() if the EMLPoint has no __str__ override.
    """
    try:
        return str(expr)
    except Exception:
        return repr(expr)


# ── Formula LaTeX helpers ─────────────────────────────────────────────────────

def eml_latex_div(num_latex: str, den_latex: str) -> str:
    """Format a/b as EML LaTeX: ops.div(num, den)."""
    return rf"\operatorname{{ops.div}}\!\left({num_latex},\, {den_latex}\right)"


def eml_latex_mul(a_latex: str, b_latex: str) -> str:
    """Format a×b as EML LaTeX: ops.mul(a, b)."""
    return rf"\operatorname{{ops.mul}}\!\left({a_latex},\, {b_latex}\right)"


def eml_latex_add(a_latex: str, b_latex: str) -> str:
    """Format a+b as EML LaTeX: ops.add(a, b)."""
    return rf"\operatorname{{ops.add}}\!\left({a_latex},\, {b_latex}\right)"


def eml_latex_sqrt(x_latex: str) -> str:
    """Format √x as EML LaTeX: ops.sqrt(x)."""
    return rf"\operatorname{{ops.sqrt}}\!\left({x_latex}\right)"


def eml_latex_pow(base_latex: str, exp_latex: str) -> str:
    """Format base^exp as EML LaTeX: ops.pow(base, exp)."""
    return rf"\operatorname{{ops.pow}}\!\left({base_latex},\, {exp_latex}\right)"


# ── Internal helper ───────────────────────────────────────────────────────────

def _ensure_eml(v: Union[_Num, "EMLPoint"]) -> "EMLPoint":
    """Coerce a float/int to EMLPoint literal if needed."""
    if EML_AVAILABLE and isinstance(v, EMLPoint):
        return v
    return eml_scalar(float(v))
