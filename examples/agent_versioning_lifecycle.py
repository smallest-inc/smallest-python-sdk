"""Build a voice agent and iterate on it safely, with the smallestai SDK.

The 90% path is one call: create_agent(...) stands up a fully-configured, LIVE
agent. You do NOT need the versioning API to create or run an agent.

Versioning (branches / drafts / revisions) is the layer for CHANGING an agent's
config safely after it exists: edits are staged as a draft, published as an
immutable revision (with a security scan), and can be staged on a branch or
rolled back. Under the branch model, runtime-config edits go through this flow;
`update_agent` only changes metadata (name, description, inbound toggle, ...).

    pip install smallestai
    export SMALLEST_API_KEY=sk_...
    python examples/agent_versioning_lifecycle.py
"""
import os

from smallestai import SmallestAI
from smallestai.agents.helpers.versioning import DraftConflictError, Versioning

client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])

# 1. CREATE — one call, fully configured, live immediately. No versioning needed.
agent_id = client.agents.agents.create_agent(
    name="receptionist",
    global_prompt="You are a friendly receptionist. Book appointments and answer questions.",
    first_message="Hi, how can I help?",
    language={"switching": {"isEnabled": False}},
).data
print("agent (live):", agent_id)

# You can place calls right now — the agent is serving the config above.
# client.agents.calls.start_an_outbound_call(agent_id=agent_id, to_phone="+15551234567")

# ------------------------------------------------------------------------------
# 2. EDIT the config later — this is where versioning comes in.
# ------------------------------------------------------------------------------
v = Versioning(client)

# Find the live Main branch (id + isDefault live on the inner .branch).
branches = v.branches.list(id=agent_id).data.branches
main_id = next(b for b in branches if b.branch.is_default).branch.id

# Quick edit: change the config and publish in one call (draft -> publish -> live,
# security scan handled). This is the simple "update my agent" path.
revision = v.edit_and_publish(
    agent_id, main_id,
    global_prompt="You are a warm, concise receptionist. Confirm details before booking.",
    label="tone tweak",
)
print("published revision:", revision.id, "status:", revision.status)

# Test the branch before/after going live.
test = v.branches.test_call(id=agent_id, branch_id=main_id, mode="webcall")
print("test call id:", test.data.call_id)

# ------------------------------------------------------------------------------
# 3. ADVANCED — stage a big change on a fork, promote it, roll back.
# ------------------------------------------------------------------------------
# Fork Main so real traffic keeps hitting the live config while you experiment.
staging_id = v.branches.create_branch(id=agent_id, source_branch_id=main_id, name="staging").data.id
v.edit_and_publish(agent_id, staging_id, global_prompt="New experimental prompt.", label="experiment")
v.branches.make_live(id=agent_id, branch_id=staging_id)   # staging live, Main flips to not-live

# Roll back: restore an older revision as a new head revision on the live branch.
older = v.revisions.list(id=agent_id, branch_id=staging_id).data.revisions[-1].id
v.revisions.restore(id=agent_id, branch_id=staging_id, revision_id=older)

# ------------------------------------------------------------------------------
# 4. Safe concurrent edits — optimistic concurrency.
# ------------------------------------------------------------------------------
draft = v.branches.get_draft(id=agent_id, branch_id=main_id).data
try:
    v.edit_and_publish(
        agent_id, main_id,
        expected_revision=draft.latest.draft_revision,   # only apply if nobody edited since
        global_prompt="Applied only if no conflicting edit landed first.",
    )
except DraftConflictError as e:
    print(f"conflict: based on r{e.expected_revision}, latest is r{e.latest_revision}")
    for d in e.diffs:
        print("  changed section:", d["section"])
    # Rebase on e.latest_revision, or retry without expected_revision to force-overwrite.
