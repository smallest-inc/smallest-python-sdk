"""Live integration sweep across the Atoms SDK surface.

Run against the rig (SMALLEST_BASE_URL set) or prod. Each block is independent
and prints PASS/FAIL so one failure doesn't hide the rest. Creates a few test
resources (named *-itest-*) and cleans up the agents it makes.

    SMALLEST_API_KEY=... [SMALLEST_BASE_URL=...] python tests/velocity/integration.py
"""
from _env import client
from smallestai.atoms.helpers import as_page, require_id

c = client()
results = []


def check(name, fn):
    try:
        detail = fn()
        results.append((name, "PASS", detail))
        print(f"  PASS  {name}  {detail or ''}")
    except Exception as e:
        results.append((name, "FAIL", f"{type(e).__name__}: {str(e)[:100]}"))
        print(f"  FAIL  {name}  {type(e).__name__}: {str(e)[:100]}")


made_agents = []


def _create():
    aid = c.atoms.agents.create_agent(name="sdk-itest-agent", first_message="Hi from itest").data
    made_agents.append(aid)
    return f"id={aid}"


def _get():
    aid = made_agents[-1]
    a = c.atoms.agents.get_agent(id=aid).data
    fm = getattr(a, "first_message", None)
    assert fm == "Hi from itest", f"firstMessage not persisted: {fm!r}"
    return f"firstMessage={fm!r}"


def _list():
    pg = as_page(c.atoms.agents.list_agents())
    return f"{len(pg.items)} agents (total={pg.total_count})"


def _update():
    aid = made_agents[-1]
    c.atoms.agents.update_agent(id=aid, description="updated by itest")
    return "updated"


def _duplicate():
    aid = made_agents[-1]
    org = c.atoms.user.get_user_details().data.organization_id
    dup = c.atoms.agents.duplicate_agent(id=aid, target_organization_id=org)
    if getattr(dup, "data", None):
        made_agents.append(dup.data if isinstance(dup.data, str) else getattr(dup.data, "_id", None))
    return "duplicated"


def _templates():
    pg = as_page(c.atoms.agent_templates.list_agent_templates())
    return f"{len(pg.items)} templates"


def _kb_list():
    return f"{len(as_page(c.atoms.knowledge_base.get_all_knowledge_bases()).items)} KBs"


def _phone_list():
    pg = as_page(c.atoms.phone_numbers.get_acquired_phone_numbers())
    return f"{len(pg.items)} numbers"


def _calls_list():
    pg = as_page(c.atoms.calls.list())
    return f"{len(pg.items)} calls"


def _guard():
    try:
        require_id("")
        raise AssertionError("require_id did not raise")
    except ValueError:
        return "require_id('') raises"


def _bad_id():
    try:
        c.atoms.agents.get_agent(id="nonexistent")
        return "WARN: no error for malformed id"
    except Exception as e:
        return f"malformed id -> {type(e).__name__} (expected)"


print("== Atoms SDK integration sweep ==")
check("user.get_user_details", lambda: c.atoms.user.get_user_details().data.user_email)
check("agents.create_agent", _create)
check("agents.get_agent (#2 firstMessage)", _get)
check("agents.list_agents (+as_page)", _list)
check("agents.update_agent", _update)
check("agents.duplicate_agent", _duplicate)
check("agent_templates.list_agent_templates", _templates)
check("knowledge_base.list", _kb_list)
check("phone_numbers.list", _phone_list)
check("calls.list", _calls_list)
check("helpers.require_id (#18)", _guard)
check("get_agent malformed id (#19)", _bad_id)

# cleanup
for aid in made_agents:
    try:
        if aid:
            c.atoms.agents.archive_agent(id=aid)
    except Exception:
        pass

passed = sum(1 for _, v, _ in results if v == "PASS")
print(f"\n== {passed}/{len(results)} passed ==")
