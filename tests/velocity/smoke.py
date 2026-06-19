"""Velocity smoke test via the shipped SDK: user -> create(first_message) -> get -> list."""
from _env import client

c = client()

print("== user ==")
try:
    u = c.atoms.user.get_user_details()
    print("user ok:", getattr(u, "data", u))
except Exception as e:
    print("user FAILED:", type(e).__name__, str(e)[:200])
    print("user namespace methods:", [m for m in dir(c.atoms.user) if not m.startswith("_")])

print("== create agent with first_message ==")
r = c.atoms.agents.create_agent(name="sdk-smoke-2026-06-18", first_message="Banana phone greeting")
aid = getattr(r, "data", None)
print("created agent id:", aid)

print("== get agent back -> firstMessage ==")
g = c.atoms.agents.get_agent(id=aid)
data = getattr(g, "data", None)
fm = getattr(data, "first_message", None) or getattr(data, "firstMessage", None)
print("firstMessage on agent:", repr(fm), "(bug #2 if empty)")

print("== list agents ==")
lst = c.atoms.agents.list_agents()
ad = getattr(lst, "data", None)
agents = getattr(ad, "agents", ad)
count = len(agents) if agents is not None and hasattr(agents, "__len__") else "?"
print("list ok, count:", count)
