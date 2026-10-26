"""Internal-consistency check of every finished fork-option run (2026-10-26).

For each RUNS/<fork>--<option>/ with a DONE.json (and RUNS/active) this checks:
  a. formulas.json: each formula's arithma_compact tree is re-evaluated (b3 leaf
     read from topology.elder_kads, pi, literals) and compared with its published
     `value` (rel 1e-9); a sole numeric output row is compared with that value
     (rel 1e-6, degree rows also accept radians); input_params and term param_ids
     must be published rows and term values must equal the row (rel 1e-3).
  b. Pages/*.html: every <span data-pm-value=K> / <span data-category=C data-param=P>
     that carries static text is compared with the run's parameters.json row,
     to the printed precision (FULL scan, not a sample).
  c. Status: DERIVED/GEOMETRIC/PREDICTED rows whose source text says calibrated or
     fitted; DERIVED-category formulas whose output row is FITTED/CALIBRATED;
     certificate registry vs certificate files, vs recount of evaluation_summary,
     vs the run's rows; assertion_verdicts tally vs its own list.
  d. Cross-path: rows changed against `active` (interactions.changed); an
     ESTABLISHED row must never change.

Usage: python -I path_consistency.py RUNS [OUT.json]
"""
import glob, json, math, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import interactions  # noqa: E402  (sibling script; reused for rows/changed)

TOL_TREE, TOL_ROW, TOL_TERM = 1e-9, 1e-6, 1e-3
FN = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b, "mul": lambda a, b: a * b,
      "div": lambda a, b: a / b, "pow": lambda a, b: a ** b, "neg": lambda a: -a,
      "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "inv": lambda a: 1 / a,
      "sin": math.sin, "cos": math.cos, "abs": abs}
SOFT = ("DERIVED", "GEOMETRIC", "PREDICTED")
SOFTWORDS = re.compile(r"calibrat|fitted|retrofit|tuned to", re.I)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def num(x):
    """float for real numbers and bools, else None."""
    if isinstance(x, bool):
        return float(x)
    return float(x) if isinstance(x, (int, float)) else None


def close(a, b, tol):
    return a == b or math.isclose(a, b, rel_tol=tol, abs_tol=0.0)


def ev(node, env):
    kind = node[0]
    if kind == "num":
        return float(node[1])
    if kind == "var":
        return math.pi if node[1] == "pi" else env[node[1]]
    if kind == "fn":
        return FN[node[1]](*[ev(x, env) for x in node[2:]])
    raise KeyError(kind)


def formula_row(fid, f, P, env):
    """(tag, detail) tags for one formula; tags are counted per run."""
    tags = []
    for pid in f["input_params"]:
        if pid not in P or P[pid].get("value") is None:
            tags.append(("input_missing", "%s <- %s" % (fid, pid)))
    for sym, t in f["terms"].items():
        pid = isinstance(t, dict) and t.get("param_id")
        if pid and pid not in P:
            tags.append(("term_row_missing", "%s <- %s" % (fid, pid)))
        elif pid and num(P[pid]["value"]) is not None and _num_str(t.get("value")) is not None:
            if not close(_num_str(t["value"]), num(P[pid]["value"]), TOL_TERM):
                tags.append(("term_vs_row", "%s %s %s != %s" % (fid, pid, t["value"], P[pid]["value"])))
    tags += value_tags(fid, f, P, env)
    return tags


def _num_str(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def value_tags(fid, f, P, env):
    val = num(f.get("value"))
    if val is None:
        return [("no_value", fid)]
    try:
        got = ev(f["arithma_compact"], env)
    except (KeyError, ZeroDivisionError, ValueError, TypeError, OverflowError) as e:
        return [("unevaluable", "%s %s %s" % (fid, type(e).__name__, e))]
    tags = []
    if not close(got, val, TOL_TREE):
        ruled = f.get("triple_status") == "RULED_DIVERGENCE"
        tags.append(("tree_ruled_divergence" if ruled else "tree_vs_value",
                     "%s tree=%.10g value=%.10g cat=%s" % (fid, got, val, f["category"])))
    out = f["output_params"]
    row = P.get(out[0]) if len(out) == 1 else None
    rv = num(row.get("value")) if row else None
    if rv is not None and not any(close(val * k, rv, TOL_ROW) for k in (1, 180 / math.pi)):
        tags.append(("value_vs_output_row", "%s value=%.10g %s=%.10g status=%s cat=%s" % (
            fid, val, out[0], rv, row["status"], f["category"])))
    return tags


def check_formulas(ad, P):
    F = read(ad / "formulas.json")["formulas"]
    env = {"b3": num(P.get("topology.elder_kads", {}).get("value")) or 0.0}
    res = {}
    for fid, f in F.items():
        for tag, detail in formula_row(fid, f, P, env):
            res.setdefault(tag, []).append(detail)
    res["n_formulas"] = len(F)
    return res


PM = re.compile(r'<span([^>]*)\bdata-pm-value="([^"]+)"([^>]*)>([^<]*)</span>')
CAT = re.compile(r'<span([^>]*)data-category="([^"]+)"[^>]*data-param="([^"]+)"([^>]*)>([^<]*)</span>')


def page_cases(html):
    for m in PM.finditer(html):
        yield m.group(2), m.group(1) + m.group(3), m.group(4).strip()
    for m in CAT.finditer(html):
        yield "%s.%s" % (m.group(2), m.group(3)), m.group(1) + m.group(4), m.group(5).strip()


def page_ok(text, attrs, rv):
    """True/False, or None if the span text is not a plain number."""
    if not re.fullmatch(r"[-+]?[\d,]*\.?\d+", text):
        return None
    shown = float(text.replace(",", ""))
    fmt = re.search(r'data-format="fixed:(\d+)"', attrs)
    dec = int(fmt.group(1)) if fmt else (len(text.split(".")[1]) if "." in text else 0)
    return abs(shown - rv) <= 0.5 * 10 ** -dec * 1.0001 + 1e-9 * abs(rv)


def check_pages(run, P):
    res = {"spans": 0, "with_text": 0, "unresolved_key": 0, "non_numeric": 0, "mismatch": []}
    for f in sorted(glob.glob(str(run / "Pages" / "*.html"))):
        for key, attrs, text in page_cases(Path(f).read_text(encoding="utf-8")):
            res["spans"] += 1
            if not text:
                continue
            res["with_text"] += 1
            rv = num(P[key]["value"]) if key in P else None
            if rv is None:
                res["unresolved_key" if key not in P else "non_numeric"] += 1
                continue
            ok = page_ok(text, attrs, rv)
            if ok is False:
                res["mismatch"].append("%s %s shows %s row=%.10g" % (Path(f).name, key, text, rv))
    return res


def check_status(ad, P):
    res = {"soft_status_with_fit_source": [], "derived_formula_fitted_row": [],
           "cert_mismatch": [], "cert_prose_numbers": []}
    for k, v in P.items():
        if v.get("status") in SOFT and SOFTWORDS.search(str(v.get("source"))):
            res["soft_status_with_fit_source"].append("%s %s %s" % (k, v["status"], v["source"]))
    F = read(ad / "formulas.json")["formulas"]
    for fid, f in F.items():
        out = f["output_params"]
        row = P.get(out[0]) if len(out) == 1 else None
        if f["category"] in SOFT and row and row["status"] in ("FITTED", "CALIBRATED"):
            res["derived_formula_fitted_row"].append("%s %s -> %s %s" % (
                fid, f["category"], out[0], row["status"]))
    res["cert_mismatch"] = check_certs(ad, P) + check_verdicts(ad)
    res["cert_prose_numbers"] = check_cert_prose(ad)
    return res


def check_certs(ad, P):
    g = read(ad / "GATES_CERTIFICATES.json")
    certs, bad, fails = g["certificates"], [], []
    files = {}
    for f in glob.glob(str(ad / "certificates" / "*.json")):
        c = read(f)
        files[c["proof_id"]] = c
    for c in certs:
        if files.get(c["proof_id"]) != c:
            bad.append("%s file differs from registry" % c["proof_id"])
        ev_ = c.get("evaluation") or {}
        for chk in ev_.get("checks", []):
            rv = num(P.get(chk["path"], {}).get("value"))
            if rv is None or not close(rv, num(chk["value"]) or 0.0, TOL_ROW):
                bad.append("%s check %s value %s != row %s" % (
                    c["proof_id"], chk["path"], chk["value"], rv))
            if (c.get("evaluation_status") == "COMPUTED_PASS") != all(
                    x.get("ok") for x in ev_["checks"]):
                bad.append("%s status %s but checks ok=%s" % (
                    c["proof_id"], c["evaluation_status"], [x.get("ok") for x in ev_["checks"]]))
                break
        if c.get("evaluation_status") == "COMPUTED_FAIL":
            fails.append(c["gate_id"])
    s = g["evaluation_summary"]
    n_pass = sum(c.get("evaluation_status") == "COMPUTED_PASS" for c in certs)
    if (n_pass, len(fails)) != (s["computed_pass"], s["computed_fail"]):
        bad.append("evaluation_summary pass/fail %s/%s but recount %s/%s" % (
            s["computed_pass"], s["computed_fail"], n_pass, len(fails)))
    listed = sorted(set(fails) - {s["seal_gate_id"]})
    if listed != sorted(s["failed_gate_ids"]):
        bad.append("failed_gate_ids %s but certificates fail %s" % (s["failed_gate_ids"], listed))
    return bad


PROSE = re.compile(r"[-+]?\d+\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+[eE][-+]?\d+")


def tol_printed(text):
    mant, _, exp = text.lower().partition("e")
    dec = len(mant.split(".")[1]) if "." in mant else 0
    return 0.5 * 10 ** -dec * (10 ** int(exp) if exp else 1) * 1.0001


def check_cert_prose(ad):
    """Decimal numbers in a registry certificate's `result` text that match no
    executed check value, expected anchor or sigma (to printed precision)."""
    out = []
    for c in read(ad / "GATES_CERTIFICATES.json")["certificates"]:
        checks = (c.get("evaluation") or {}).get("checks") or []
        known = [num(x.get(k)) for x in checks for k in ("value", "expected", "sigma")]
        known = [v for v in known if v is not None]
        bad = [t for t in PROSE.findall(str(c.get("result")))
               if checks and not any(abs(float(t) - v) <= tol_printed(t) for v in known)]
        if bad:
            out.append("G%s result %r carries %s not in the executed checks" % (
                c["gate_id"], c["result"][:60], bad))
    return out


def check_verdicts(ad):
    a = read(ad / "assertion_verdicts.json")
    meta, items, bad = a["metadata"], a["assertions"], []
    if meta["total_assertions"] != len(items):
        bad.append("assertion_verdicts total_assertions %s but %d listed"
                   % (meta["total_assertions"], len(items)))
    tally = {}
    for x in items:
        tally[x["verdict"]] = tally.get(x["verdict"], 0) + 1
    for v in sorted(set(tally) | set(meta["verdicts"])):
        if tally.get(v, 0) != meta["verdicts"].get(v, 0):
            bad.append("assertion_verdicts %s tallied %s but listed %d"
                       % (v, meta["verdicts"].get(v, 0), tally.get(v, 0)))
    return bad


def check_cross(P, base_rows):
    mine = {k: v.get("value") for k, v in P.items()}
    ch = interactions.changed(base_rows, mine)
    est = [k for k in ch if k in P and P[k].get("status") == "ESTABLISHED"]
    return {"changed_rows": len(ch), "established_changed": sorted(est)}


def check_run(run, base_rows):
    ad = run / "AutoGenerated"
    P = read(ad / "parameters.json")["parameters"]
    return {"formulas": check_formulas(ad, P), "pages": check_pages(run, P),
            "status": check_status(ad, P), "cross": check_cross(P, base_rows)}


def counts(r):
    """Flat counts, the only part used for ranking."""
    c = {"formula_" + k: len(v) for k, v in r["formulas"].items() if isinstance(v, list)}
    c["pages_mismatch"] = len(r["pages"]["mismatch"])
    c.update({"status_" + k: len(v) for k, v in r["status"].items()})
    c["established_changed"] = len(r["cross"]["established_changed"])
    return c


def main(argv):
    runs = Path(argv[1])
    base = interactions.rows(runs / "active")
    if base is None:
        raise SystemExit("no active baseline in %s" % runs)
    out = {}
    for run in sorted(runs.iterdir()):
        if run.is_dir() and (run.name == "active" or (run / "DONE.json").is_file()):
            if (run / "AutoGenerated" / "parameters.json").is_file():
                out[run.name] = check_run(run, base)
    for name, r in out.items():
        c = counts(r)
        print("%-52s %s" % (name, " ".join("%s=%d" % kv for kv in c.items() if kv[1])))
    worst = sorted(out, key=lambda n: -sum(counts(out[n]).values()))[:5]
    print("worst:", ", ".join(worst))
    if len(argv) > 2:
        Path(argv[2]).write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
