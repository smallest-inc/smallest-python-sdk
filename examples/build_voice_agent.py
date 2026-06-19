"""
Build a voice agent with smallestai 5.0.0 — full lifecycle, end to end.

Walks the real one-shot flow you'd use in an app:
  create agent -> inspect -> (optional) knowledge base -> draft a new version
  -> publish with activate=True -> watch it go LIVE -> list -> clean up.

Run:
    pip install .
    export SMALLEST_API_KEY=sk_...            # app.smallest.ai key, or the dev key
    # optional non-prod target (needs VPN for the dev rig):
    # export SMALLEST_BASE_URL=https://abhishek-sdk-atoms.dev.smallest.ai
    python examples/build_voice_agent.py

Note: this builds + activates the agent via the API. Actually placing a phone
call additionally needs a phone number attached and the agent runtime running —
see the cookbook / `smallestai agent-crew deploy`. This script proves the
create-configure-publish-activate path that every voice agent starts from.
"""
import os
import time

from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms.helpers import as_page


def _id_of(obj):
    """Resource id — agents expose `_id`, versions expose `id`."""
    return getattr(obj, "id", None) or getattr(obj, "_id", None)


def make_client() -> SmallestAI:
    api_key = os.environ["SMALLEST_API_KEY"]
    base = os.environ.get("SMALLEST_BASE_URL")
    if base:
        base = base.rstrip("/")
        env = SmallestAIEnvironment(
            atoms=f"{base}/atoms/v1",
            waves=base,
            waves_ws=base.replace("https", "wss").replace("http", "ws"),
        )
        return SmallestAI(api_key=api_key, environment=env)
    return SmallestAI(api_key=api_key)


def main() -> None:
    c = make_client()
    created_ids = []

    print("1. whoami")
    print("   ", c.atoms.user.get_user_details().data.user_email)

    print("2. create agent")
    agent_id = c.atoms.agents.create_agent(
        name=f"mario-pizza-{int(time.time())}",
        first_message="Hi, thanks for calling Mario's Pizza! What can I get started for you?",
        global_prompt="You are a friendly assistant for Mario's Pizza. Take orders, "
        "answer menu questions, and confirm the delivery address.",
    ).data
    created_ids.append(agent_id)
    print("    agent id:", agent_id)

    print("3. read it back")
    agent = c.atoms.agents.get_agent(id=agent_id).data
    print("    name        :", agent.name)
    print("    firstMessage :", repr(agent.first_message))

    print("4. (optional) knowledge base for the menu")
    try:
        kb = c.atoms.knowledge_base.create_a_knowledge_base(
            name="mario-menu", description="Pizza menu + prices"
        )
        print("    KB created:", getattr(kb, "data", kb))
    except Exception as e:
        print("    KB skipped:", type(e).__name__, str(e)[:80])

    print("5. draft a new version from the active one")
    versions = as_page(c.atoms.agent_versioning_versions.list_published_versions(id=agent_id))
    active = next((v for v in versions.items if getattr(v, "is_active", False)), None) or versions.items[0]
    src_version_id = _id_of(active)
    print("    source version:", src_version_id)
    draft = c.atoms.agent_versioning_drafts.create_a_draft(id=agent_id, source_version_id=src_version_id)
    draft_id = getattr(draft.data, "draft_id", None) or _id_of(draft.data)
    print("    draft id:", draft_id)

    print("6. publish the draft with activate=True (go live)")
    published = c.atoms.agent_versioning_drafts.publish_a_draft(
        id=agent_id, draft_id=draft_id, label="v2-live", activate=True
    )
    new_version_id = _id_of(published.data)
    print("    published version:", new_version_id, "— waiting for it to go live...")

    print("7. poll until the new version is active")
    live = False
    for i in range(10):
        time.sleep(4)
        vs = as_page(c.atoms.agent_versioning_versions.list_published_versions(id=agent_id))
        v = next((x for x in vs.items if _id_of(x) == new_version_id), None)
        sc = getattr(v, "security_check", None)
        status = getattr(sc, "status", None) if sc else None
        is_active = getattr(v, "is_active", None) if v else None
        print(f"    t+{(i + 1) * 4}s: securityCheck={status} isActive={is_active}")
        if is_active:
            live = True
            break
    print("    -> LIVE" if live else "    -> not active yet (security check may still be running)")

    print("8. list agents in the org")
    print("    total:", len(as_page(c.atoms.agents.list_agents()).items))

    print("9. cleanup (archive the demo agent)")
    for aid in created_ids:
        try:
            c.atoms.agents.archive_agent(id=aid)
            print("    archived:", aid)
        except Exception as e:
            print("    archive skipped:", type(e).__name__, str(e)[:60])

    print("\nDONE — built, configured, and activated a voice agent end to end.")
    print("Next (telephony): attach a phone number + run the agent runtime to take real calls.")


if __name__ == "__main__":
    main()
