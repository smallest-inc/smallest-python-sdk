#!/usr/bin/env python3
"""Pre-release verification harness for smallestai.

One command, four layers, one pass/fail coverage report. This is the standing
release gate: it turns "did we miss anything?" into a number.

  1. WIRE COVERAGE   (static) — every generated endpoint has a wire test
  2. LIVE READ SWEEP (live)   — every no-arg read endpoint is reachable + parses
  3. FIELD-DROP AUDIT(live)   — fields the API returns but the SDK doesn't type
                                (the spec-vs-reality class wire tests miss)
  4. HELPER COVERAGE (static) — every hand-written helper has a unit test

Live layers need SMALLEST_API_KEY (+ optional SMALLEST_BASE_URL); skipped if absent.
Hard gates (1, 2, 4) fail the build; the field-drop audit (3) reports gaps as warnings
(tracked as spec work, not a build break).

    python scripts/verify.py        # or: make verify
"""
import inspect
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "smallestai"
WIRE = ROOT / "tests" / "wire"
CUSTOM = ROOT / "tests" / "custom"

GREEN, RED, YEL, DIM, END = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
failures = []
warnings = []


def hdr(t):
    print(f"\n{'='*64}\n  {t}\n{'='*64}")


# ---------------------------------------------------------------- layer 1
def public_methods(client_py):
    txt = client_py.read_text()
    names = re.findall(r"^    def ([a-z][a-zA-Z0-9_]*)\(", txt, re.M)
    return [n for n in names if n != "with_raw_response"]


def check_wire_coverage():
    hdr("1. WIRE COVERAGE — every endpoint has a wire test")
    wire_files = list(WIRE.glob("test_*.py"))

    def wire_count_for(ns):
        key = ns.replace("_", "")
        for wf in wire_files:
            if key in wf.stem.lower().replace("_", ""):
                return len(re.findall(r"def test_", wf.read_text()))
        return 0

    tot_m = tot_w = 0
    for ns_dir in sorted((SRC / "atoms").glob("*/")):
        cf = ns_dir / "client.py"
        if not cf.exists():
            continue
        ns = ns_dir.name
        m = len(public_methods(cf))
        w = wire_count_for(ns)
        tot_m += m
        tot_w += w
        if w < m:
            failures.append(f"wire: {ns} has {w} wire tests for {m} methods")
            print(f"  {RED}FAIL{END} {ns:<26} methods={m} wiretests={w}")
        else:
            print(f"  {GREEN}ok{END}   {ns:<26} methods={m} wiretests={w}")
    print(f"  {DIM}totals: {tot_m} methods, {tot_w} wire tests{END}")


# ---------------------------------------------------------------- layer 1b
def check_wire_imports():
    """Import every `from smallestai... import X` in the wire tests.

    mypy CANNOT catch a missing lazy __init__ export (the generated __getattr__ is typed
    `-> Any`), so a type stripped by exclude_types_from_init_exports passes mypy but fails
    at import/collection time. This check catches that class without needing Docker/WireMock.
    """
    import importlib

    hdr("1b. WIRE-TEST IMPORTS — every `from smallestai import ...` resolves")
    pat = re.compile(r"^from (smallestai[\w.]*) import (.+)$")
    n = bad = 0
    for f in sorted(WIRE.glob("test_*.py")):
        for line in f.read_text().splitlines()[:10]:
            mt = pat.match(line.strip())
            if not mt:
                continue
            mod, names = mt.group(1), mt.group(2)
            for name in [x.strip() for x in names.split(",") if x.strip()]:
                n += 1
                try:
                    getattr(importlib.import_module(mod), name)
                except Exception as e:
                    bad += 1
                    failures.append(f"wire-import: {f.name}: from {mod} import {name} -> {type(e).__name__}")
                    print(f"  {RED}FAIL{END} {f.name}: from {mod} import {name}")
    if not bad:
        print(f"  {GREEN}ok{END}   all {n} wire-test imports resolve")


# ---------------------------------------------------------------- live client
def live_client():
    key = os.environ.get("SMALLEST_API_KEY")
    if not key:
        return None
    from smallestai import SmallestAI
    base = os.environ.get("SMALLEST_BASE_URL")
    if base:
        from smallestai.environment import SmallestAIEnvironment
        base = base.rstrip("/")
        ws = base.replace("https://", "wss://").replace("http://", "ws://")
        env = SmallestAIEnvironment(atoms=f"{base}/atoms/v1", waves=base, waves_ws=ws)
        return SmallestAI(api_key=key, environment=env)
    return SmallestAI(api_key=key)


def read_methods(client):
    """Yield (label, bound_method) for every no-required-arg read endpoint."""
    READ = re.compile(r"^(list|get_all|retrieve_all|search|get_acquired)")
    EXTRA = {"get_user_details", "get_account_details"}
    for ns_name in dir(client.atoms):
        if ns_name.startswith("_"):
            continue
        ns = getattr(client.atoms, ns_name)
        if "Client" not in type(ns).__name__:
            continue
        for m_name in dir(ns):
            if m_name.startswith("_") or m_name == "with_raw_response":
                continue
            m = getattr(ns, m_name)
            if not callable(m):
                continue
            if not (READ.match(m_name) or m_name in EXTRA):
                continue
            try:
                req = [p for p in inspect.signature(m).parameters.values()
                       if p.default is p.empty and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
            except (TypeError, ValueError):
                req = []
            if req:
                continue
            yield f"{ns_name}.{m_name}", m


# ---------------------------------------------------------------- layer 2
def check_live_sweep(client):
    hdr("2. LIVE READ SWEEP — every no-arg read endpoint")
    from smallestai.atoms.helpers import as_page
    items_by_label = {}
    n = ok = 0
    for label, method in read_methods(client):
        n += 1
        try:
            resp = method()
            try:
                pg = as_page(resp)
                items_by_label[label] = pg.items
                detail = f"{len(pg.items)} items"
            except Exception:
                detail = "ok (non-list)"
            ok += 1
            print(f"  {GREEN}PASS{END} {label:<46} {DIM}{detail}{END}")
        except Exception as e:
            failures.append(f"live: {label} -> {type(e).__name__}: {str(e)[:80]}")
            print(f"  {RED}FAIL{END} {label:<46} {type(e).__name__}: {str(e)[:60]}")
    print(f"  {DIM}{ok}/{n} read endpoints reachable{END}")
    return items_by_label


# ---------------------------------------------------------------- layer 3
def _extras(model, path, noise={"__v"}):
    found = []
    if model is None:
        return found
    # aliases of declared fields: the unchecked-construct path can leave the raw alias
    # key in model_extra even when the field is populated — not a real drop.
    aliases = {getattr(f, "alias", None)
               for f in (type(model).model_fields.values() if hasattr(type(model), "model_fields") else [])}
    for k in (getattr(model, "model_extra", None) or {}):
        if k not in noise and k not in aliases:
            found.append(f"{path}.{k}")
    for fname in (type(model).model_fields if hasattr(type(model), "model_fields") else {}):
        v = getattr(model, fname, None)
        if hasattr(v, "model_extra"):
            found += _extras(v, f"{path}.{fname}")
        elif isinstance(v, list) and v and hasattr(v[0], "model_extra"):
            found += _extras(v[0], f"{path}.{fname}[0]")
    return found


def check_field_drop(items_by_label):
    hdr("3. FIELD-DROP AUDIT — API returns but SDK doesn't type (spec gaps)")
    total = 0
    for label, items in sorted(items_by_label.items()):
        if not items:
            continue
        drops = _extras(items[0], label.split(".")[0])
        if drops:
            total += len(drops)
            warnings.append(f"field-drop: {label} -> {len(drops)} untyped")
            shown = ['.'.join(d.split('.')[1:]) for d in drops[:6]]
            print(f"  {YEL}GAP{END}  {label:<46} {len(drops)} untyped: {DIM}{', '.join(shown)}{'…' if len(drops)>6 else ''}{END}")
        else:
            print(f"  {GREEN}ok{END}   {label:<46} all fields typed")
    print(f"  {DIM}{total} untyped fields total (tracked as 5.1.x spec completeness){END}")


# ---------------------------------------------------------------- layer 4
def check_helper_coverage():
    hdr("4. HELPER COVERAGE — every hand-written helper has a test")
    init = (SRC / "atoms" / "helpers" / "__init__.py").read_text()
    names = re.findall(r"\"([A-Za-z_]+)\"", init.split("__all__")[-1]) if "__all__" in init else []
    test_blob = "\n".join(p.read_text() for p in CUSTOM.glob("test_*.py"))
    for name in names:
        if re.search(rf"\b{name}\b", test_blob):
            print(f"  {GREEN}ok{END}   {name}")
        else:
            failures.append(f"helper: {name} has no test in tests/custom")
            print(f"  {RED}FAIL{END} {name} — no test references it")


# ---------------------------------------------------------------- main
def main():
    print(f"{DIM}smallestai pre-release verification — {ROOT.name}{END}")
    check_wire_coverage()
    check_wire_imports()
    client = live_client()
    if client is None:
        hdr("2-3. LIVE LAYERS — SKIPPED (set SMALLEST_API_KEY to run)")
        warnings.append("live layers skipped (no SMALLEST_API_KEY)")
    else:
        items = check_live_sweep(client)
        check_field_drop(items)
    check_helper_coverage()

    hdr("REPORT")
    for w in warnings:
        print(f"  {YEL}WARN{END} {w}")
    if failures:
        for f in failures:
            print(f"  {RED}FAIL{END} {f}")
        print(f"\n  {RED}VERIFY FAILED — {len(failures)} hard failure(s){END}")
        sys.exit(1)
    print(f"\n  {GREEN}VERIFY PASSED{END}  ({len(warnings)} warning(s), 0 hard failures)")


if __name__ == "__main__":
    main()
