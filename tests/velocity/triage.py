"""Live re-triage of the SDK_ASKS items against the Velocity rig using the
shipped 4.4.7 SDK. Each check prints: <id> | <verdict> | <detail>.

verdict: FIXED (no longer a bug), BUG (reproduces), N/A (needs richer flow).
owner:   sdk / platform / spec / cli
"""
import io
import os
import warnings
import contextlib
from _env import client

c = client()
R = []


def rec(id_, verdict, owner, detail):
    R.append((id_, verdict, owner, detail))
    print(f"{id_:>4} | {verdict:<7} | {owner:<8} | {detail}")


def agent_id_helper():
    r = c.atoms.agents.create_a_new_agent(name="triage-base-2026-06-18")
    return getattr(r, "data", None)


# --- #3 env-var: does only SMALLEST_API_KEY authenticate (no api_key arg)? ---
try:
    from smallestai import SmallestAI
    from smallestai.environment import SmallestAIEnvironment
    base = os.environ["SMALLEST_BASE_URL"].rstrip("/")
    env = SmallestAIEnvironment(atoms=f"{base}/atoms/v1", waves=base, waves_ws=base.replace("https", "wss"))
    saved = {k: os.environ.pop(k, None) for k in ("SMALLEST_AI_TOKEN",)}
    os.environ["SMALLEST_API_KEY"] = os.environ["SMALLEST_API_KEY"]
    c2 = SmallestAI(environment=env)  # no api_key arg -> must read SMALLEST_API_KEY
    c2.atoms.user.get_user_details()
    rec("#3", "FIXED", "sdk", "SmallestAI() reads SMALLEST_API_KEY (no api_key arg needed)")
    for k, v in saved.items():
        if v is not None:
            os.environ[k] = v
except Exception as e:
    rec("#3", "BUG", "sdk", f"{type(e).__name__}: {str(e)[:90]}")

# --- #2 first_message persisted on create ---
try:
    r = c.atoms.agents.create_a_new_agent(name="triage-fm-2026-06-18", first_message="Banana phone")
    aid = getattr(r, "data", None)
    g = c.atoms.agents.get_agent_by_id(id=aid)
    d = getattr(g, "data", None)
    fm = getattr(d, "first_message", None) or getattr(d, "firstMessage", None)
    rec("#2", "FIXED" if fm == "Banana phone" else "BUG", "platform", f"firstMessage={fm!r} after create")
except Exception as e:
    rec("#2", "ERR", "platform", f"{type(e).__name__}: {str(e)[:90]}")

# --- #7 calls namespace has get / list ---
try:
    methods = [m for m in dir(c.atoms.calls) if not m.startswith("_")]
    has = [m for m in methods if "get" in m or "list" in m]
    rec("#7", "FIXED" if has else "BUG", "sdk", f"calls methods: {methods}")
except Exception as e:
    rec("#7", "ERR", "sdk", str(e)[:90])

# --- #18 get_agent_by_id("") ---
try:
    g = c.atoms.agents.get_agent_by_id(id="")
    d = getattr(g, "data", None)
    is_list = hasattr(d, "agents")
    rec("#18", "BUG" if is_list else "FIXED", "sdk/platform", f"empty id -> {'list payload' if is_list else type(d).__name__}")
except Exception as e:
    rec("#18", "FIXED", "sdk", f"raises {type(e).__name__} (good)")

# --- #19 get_agent_by_id('nonexistent') status ---
try:
    c.atoms.agents.get_agent_by_id(id="nonexistent")
    rec("#19", "BUG", "platform", "no error for malformed id")
except Exception as e:
    code = getattr(e, "status_code", "?")
    rec("#19", "BUG" if code == 500 else "FIXED", "platform", f"status={code} for malformed id")

# --- #21 duplicate name -> 409 ---
try:
    a = getattr(c.atoms.agents.create_a_new_agent(name="triage-dup-2026-06-18"), "data", None)
    try:
        b = getattr(c.atoms.agents.create_a_new_agent(name="triage-dup-2026-06-18"), "data", None)
        rec("#21", "BUG", "platform", f"dup name allowed (a={a} b={b})")
    except Exception as e:
        rec("#21", "FIXED", "platform", f"dup rejected: {getattr(e,'status_code','?')}")
except Exception as e:
    rec("#21", "ERR", "platform", str(e)[:90])

# --- #22 update_workflow_configuration still public ---
rec("#22", "BUG" if hasattr(c.atoms.agents, "update_workflow_configuration") else "FIXED",
    "sdk", "update_workflow_configuration on public surface" if hasattr(c.atoms.agents, "update_workflow_configuration") else "hidden")

# --- #24 pydantic serialization warning on list ---
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        c.atoms.agents.get_all_agents()
        ser = [str(x.message)[:60] for x in w if "Serializ" in str(x.message) or "Unexpected" in str(x.message)]
    rec("#24", "BUG" if ser else "FIXED", "spec", f"{len(ser)} serialization warning(s)")
except Exception as e:
    rec("#24", "ERR", "spec", str(e)[:90])

# --- #25 data shape: create (str) vs get (object) ---
try:
    cr = c.atoms.agents.create_a_new_agent(name="triage-shape-2026-06-18")
    create_t = type(getattr(cr, "data", None)).__name__
    gt = type(getattr(c.atoms.agents.get_agent_by_id(id=getattr(cr, "data", None)), "data", None)).__name__
    rec("#25", "BUG" if create_t != gt else "FIXED", "spec", f"create.data={create_t} vs get.data={gt}")
except Exception as e:
    rec("#25", "ERR", "spec", str(e)[:90])

# --- #1 / #12 / #12a / #15 crew + helpers surface (import-level) ---
try:
    from smallestai.atoms.crew.clients.openai import OpenAIClient
    raised = False
    try:
        os.environ.pop("OPENAI_API_KEY", None)
        OpenAIClient(api_key=None)
    except ValueError:
        raised = True
    except Exception:
        raised = False
    rec("#1", "FIXED" if raised else "BUG", "sdk", "OpenAIClient(api_key=None) raises" if raised else "no raise (warns + proceeds)")
    rec("#12", "FIXED" if hasattr(OpenAIClient, "electron") else "BUG", "sdk", "electron() factory present" if hasattr(OpenAIClient, "electron") else "no electron() factory")
except Exception as e:
    rec("#1", "ERR", "sdk", f"import crew openai failed: {str(e)[:80]}")

try:
    import smallestai.atoms.helpers as h
    names = [n for n in dir(h) if not n.startswith("_")]
    rec("#15", "BUG" if "Call" in names and "CallAnalytics" not in names else "FIXED", "sdk", f"helpers: {names}")
except Exception as e:
    rec("#15/#17", "BUG", "sdk", f"helpers import failed: {str(e)[:80]}")

print("\n=== SUMMARY ===")
for v in ("BUG", "FIXED", "N/A", "ERR"):
    ids = [i for i, vv, _, _ in R if vv == v]
    if ids:
        print(f"{v}: {', '.join(ids)}")
