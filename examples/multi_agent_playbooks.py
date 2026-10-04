"""Author a multi-agent (Playbooks) agent with the smallestai SDK.

A multi-agent agent is an intent router plus a set of specialist "playbooks". The
router classifies each turn and routes to the matching playbook (falling back to
`router.fallback_playbook_id`), and may re-route mid-call. The platform runs the
LLM turn; you author the specialist prompts and their tool references.

The SDK is the source of truth: you define the config in Python, publish it, and
the dashboard renders it. Writing the config flips the agent's workflow type to
`multi_agents` and writes the versioned `playbooks` config section through the same
draft -> publish pipeline the dashboard uses.

    pip install smallestai
    export SMALLEST_API_KEY=sk_...
    python examples/multi_agent_playbooks.py

Note: multi-agent (Playbooks) is gated behind a rollout allowlist. On an account
without access, `create_agent` raises `MultiAgentNotEntitledError`.
"""

import os

from smallestai import SmallestAI
from smallestai.atoms.helpers import (
    IntentRouter,
    MultiAgent,
    MultiAgentNotEntitledError,
    Playbook,
    PlaybooksConfig,
    Verification,
)

client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])
ma = MultiAgent(client)

# 1. Define the router + specialist playbooks.
config = PlaybooksConfig(
    router=IntentRouter(
        fallback_playbook_id="general",
        classifier_model="gpt-4o-mini",
        allow_mid_call_reroute=True,
    ),
    # Persona/style injected into EVERY specialist prompt, defined once.
    conversation_guide="You are Aria, a warm, concise support agent. Mirror the caller's language.",
    # Tools visible on every turn regardless of the active playbook.
    global_tool_refs=["tool_lookup_account"],
    # Reusable identity checks referenced by playbooks via verification_ids.
    verifications=[
        Verification(id="v_identity", name="Identity check", tool_refs=["tool_verify_dob"], max_retries=2),
    ],
    playbooks=[
        Playbook(
            id="card_fraud",
            name="Card fraud",
            intent_name="card_fraud",
            intent_description="Caller reports a lost/stolen card or suspected fraud.",
            prompt="You handle card-fraud reports. Confirm the card, then freeze it.",
            tool_refs=["tool_freeze_card"],
            verification_ids=["v_identity"],
        ),
        Playbook(
            id="general",
            name="General",
            intent_name="general",
            intent_description="Anything that is not a more specific intent.",
            prompt="You handle general support questions.",
        ),
    ],
)

# 2. Create a new multi-agent agent carrying this config, published + live.
try:
    agent_id = ma.create_agent(name="Support bot", config=config)
except MultiAgentNotEntitledError:
    print("This account is not on the multi-agent allowlist.")
    raise

print("created multi-agent agent:", agent_id)

# 3. Round-trip: read the published config back (typed).
back = ma.read_config(agent_id)
assert back is not None
print("playbooks:", [p.id for p in back.playbooks], "fallback:", back.router.fallback_playbook_id)

# 4. Edit it later: change a prompt and publish again (same draft -> publish flow).
config.playbooks[0].prompt = "You handle card-fraud reports. Verify identity first, then freeze the card."
ma.publish_config(agent_id, config, label="tighten fraud flow")
print("republished.")
