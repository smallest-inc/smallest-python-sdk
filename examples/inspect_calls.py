"""
Inspect calls: list, details, transcript, recording — smallestai 5.4.0.

Read-only helpers for after a call happened. Handy for verifying a transfer:
a transfer leg that shows status `no_answer` / `timeout` fired correctly but the
destination did not pick up (not an SDK problem).

Run:
    pip install "smallestai>=5.4.0"
    export SMALLEST_API_KEY=sk_...
    python examples/inspect_calls.py            # lists recent calls
    python examples/inspect_calls.py CALL-...   # details + transcript for one call
"""
import os
import sys

from smallestai import SmallestAI


def main() -> None:
    client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])

    if len(sys.argv) > 1:
        call_id = sys.argv[1]
        call = client.atoms.calls.get(id=call_id).data
        print(f"call {call_id}")
        print("  status     :", getattr(call, "status", None))
        print("  type       :", getattr(call, "type", None))
        print("  duration   :", getattr(call, "duration", None))
        print("  from -> to :", getattr(call, "from_", None), "->", getattr(call, "to", None))
        print("  recording  :", getattr(call, "recording_url", None))
        print("  transcript :")
        for turn in getattr(call, "transcript", None) or []:
            print(f"    {getattr(turn, 'role', '?')}: {getattr(turn, 'content', '')}")
        return

    # No id given -> list recent calls.
    logs = client.atoms.calls.list(limit=10).data.logs or []
    print(f"{len(logs)} recent call(s):")
    for item in logs:
        print(
            f"  {getattr(item, 'call_id', '?')}  "
            f"{(getattr(item, 'type', '') or '').replace('telephony_', ''):9} "
            f"{getattr(item, 'status', ''):10} "
            f"{getattr(item, 'from_', '')} -> {getattr(item, 'to', '')}"
        )
    print("\nPass a CALL-... id to see its transcript + recording.")


if __name__ == "__main__":
    main()
