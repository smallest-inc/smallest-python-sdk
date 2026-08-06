"""
Configure a transfer_call tool on a single-prompt agent from code — smallestai 5.4.0.

Uses `AgentTools`, which drives the branch/revision versioning flow
(draft -> publish -> make-live) so the tool actually takes effect on live calls.
Writing the legacy workflow doc does NOT take effect under the branch model.

Transfer types:
  - cold_transfer: a direct connect. The caller is bridged straight to the
    destination, no debrief. No hold music / whisper / three-way (nothing to fill).
  - warm_transfer: the agent debriefs the destination before bridging. This is the
    window where on_hold_music (and whisper / three-way) apply.

So: if you want the caller to hear music during the transfer, use warm_transfer.
Setting on_hold_music on a cold transfer is silently ignored.

Run:
    pip install "smallestai>=5.4.0"
    export SMALLEST_API_KEY=sk_...
    python examples/transfer_call.py
"""
import os

from smallestai import SmallestAI
from smallestai.agents.helpers import AgentTools


def main() -> None:
    api_key = os.environ["SMALLEST_API_KEY"]
    client = SmallestAI(api_key=api_key)

    # 1. A single-prompt agent. Its prompt should tell the LLM WHEN to transfer,
    #    otherwise the tool never fires.
    agent_id = client.agents.agents.create_agent(
        name="Front desk (transfer demo)",
        workflow_type="single_prompt",
        first_message="Hi, thanks for calling. How can I help?",
    ).data
    print("created agent:", agent_id)

    tools = AgentTools(api_key=api_key)

    # 2a. Cold transfer — direct connect to a human or number.
    tools.add_transfer_call(
        agent_id,
        number="+15551234567",
        transfer_type="cold_transfer",
    )

    # 2b. Warm transfer — agent debriefs the destination; hold music plays to the
    #     caller during the handover. Uncomment to use instead of the cold one above.
    # tools.add_transfer_call(
    #     agent_id,
    #     number="+15551234567",
    #     transfer_type="warm_transfer",
    #     on_hold_music="relaxing_sound",  # ringtone | relaxing_sound | uplifting_beats | none
    # )

    # 3. Read back the live tools.
    for tool in tools.get_tools(agent_id):
        print("tool:", tool.type, tool.name, getattr(tool, "transfer_number", ""))

    print(
        "\nThe agent now transfers when the caller asks. Attach a phone number and "
        "place a call to try it (see `smallestai agent-crew deploy` / the cookbook)."
    )

    # 4. Clean up the demo tool if you want:
    # tools.remove_tool(agent_id, "transfer_call")


if __name__ == "__main__":
    main()
