"""
smallestai 5.0.0 quickstart — exercises the core Atoms surface.

Run against production (default) or a custom stack:

    pip install -e .                       # from the repo root
    export SMALLEST_API_KEY=sk_...         # your key
    # optional: point at a non-prod stack
    # export SMALLEST_BASE_URL=https://abhishek-sdk-atoms.dev.smallest.ai
    python examples/quickstart.py
"""

import os

from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment


def make_client() -> SmallestAI:
    api_key = os.environ["SMALLEST_API_KEY"]  # also auto-read if omitted
    base = os.environ.get("SMALLEST_BASE_URL")
    if base:
        base = base.rstrip("/")
        env = SmallestAIEnvironment(
            atoms=f"{base}/atoms/v1",
            waves=base,
            waves_ws=base.replace("https", "wss").replace("http", "ws"),
        )
        return SmallestAI(api_key=api_key, environment=env)
    return SmallestAI(api_key=api_key)  # production


def main() -> None:
    client = make_client()

    me = client.atoms.user.get_user_details()
    print("authenticated as:", me.data.user_email)

    created = client.atoms.agents.create_agent(
        name="quickstart-demo",
        first_message="Hi! Thanks for calling — how can I help?",
    )
    agent_id = created.data
    print("created agent:", agent_id)

    agent = client.atoms.agents.get_agent(id=agent_id)
    print("first_message persisted as:", repr(agent.data.first_message))

    listing = client.atoms.agents.list_agents()
    agents = getattr(listing.data, "agents", listing.data)
    print("agents in org:", len(agents))

    print("\nOK — create_agent / get_agent / list_agents all working.")


if __name__ == "__main__":
    main()
