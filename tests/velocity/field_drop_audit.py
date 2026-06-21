"""Field-drop audit: find fields the live API returns but the SDK models don't type.

This catches the *spec-vs-reality* bug class that wire tests miss (wire tests use the
spec's example fixtures, so a field the spec omits passes the wire test but shows up
here against real data). Examples this would have caught: agent_templates `_id`/`id`,
live-transcript `metrics` as a list, the agent model's missing config fields.

Mechanism: pydantic models use extra="allow", so any field the API sends that the model
doesn't declare lands in `model_extra`. We walk each response model recursively and
report those keys. `__v` (mongo version) and a small noise set are ignored.

    SMALLEST_API_KEY=... [SMALLEST_BASE_URL=...] python tests/velocity/field_drop_audit.py
"""
from _env import client
from smallestai.atoms.helpers import as_page

_NOISE = {"__v"}  # mongo internals, not real SDK gaps

c = client()


def extras(model, path):
    found = []
    if model is None:
        return found
    me = getattr(model, "model_extra", None) or {}
    for k in me:
        if k not in _NOISE:
            found.append(f"{path}.{k}")
    for fname in (type(model).model_fields if hasattr(type(model), "model_fields") else {}):
        v = getattr(model, fname, None)
        if hasattr(v, "model_extra"):
            found += extras(v, f"{path}.{fname}")
        elif isinstance(v, list) and v and hasattr(v[0], "model_extra"):
            found += extras(v[0], f"{path}.{fname}[0]")
    return found


def _first_agent():
    return c.atoms.agents.get_agent(id=as_page(c.atoms.agents.list_agents()).items[0].id).data


CHECKS = {
    "user": lambda: c.atoms.user.get_user_details().data,
    "agent": _first_agent,
    "agent_template": lambda: as_page(c.atoms.agent_templates.list_agent_templates()).items[0],
    "knowledge_base": lambda: as_page(c.atoms.knowledge_base.list()).items[0],
    "phone_number": lambda: as_page(c.atoms.phone_numbers.list()).items[0],
    "call": lambda: as_page(c.atoms.calls.list()).items[0],
}


def main():
    print("== field-drop audit (API returns but SDK doesn't type) ==")
    total = 0
    for name, fn in CHECKS.items():
        try:
            drops = extras(fn(), name)
            total += len(drops)
            print(f"  {name}: {('DROPS(%d) -> ' % len(drops)) + ', '.join(drops) if drops else 'clean'}")
        except Exception as e:
            print(f"  {name}: skip ({type(e).__name__}: {str(e)[:60]})")
    print(f"\n== {total} untyped fields across sampled resources ==")


if __name__ == "__main__":
    main()
