"""SessionContext.caller — inbound caller identity surfaced to a crew (PRO-3560).

The SDK must parse the new `caller` block when the orchestrator sends it, read back
`None` when it doesn't (older orchestrators / webcall), and tolerate extra fields.
"""

from smallestai.atoms.crew.events import CallerContext, SessionContext


def test_caller_context_parsed_on_inbound_telephony():
    sc = SessionContext.model_validate(
        {
            "initial_variables": {},
            "conversation_type": "telephonyInbound",
            "caller": {
                "user_number": "+15551234567",
                "agent_number": "+15559876543",
                "direction": "inbound",
                "call_id": "CALL-1",
            },
        }
    )
    assert isinstance(sc.caller, CallerContext)
    assert sc.caller.user_number == "+15551234567"
    assert sc.caller.agent_number == "+15559876543"
    assert sc.caller.direction == "inbound"
    assert sc.caller.call_id == "CALL-1"


def test_caller_is_none_when_absent():
    # Older orchestrators / webcall send no caller block — reading it must be safe.
    sc = SessionContext.model_validate({"initial_variables": {}, "conversation_type": "webcall"})
    assert sc.caller is None


def test_caller_tolerates_extra_fields_and_partial_population():
    sc = SessionContext.model_validate(
        {
            "initial_variables": {},
            "conversation_type": "telephonyInbound",
            "caller": {"user_number": "+1", "sip_headers": {"X-Foo": "bar"}},
        }
    )
    assert sc.caller.user_number == "+1"
    assert sc.caller.agent_number is None  # partial is fine
    assert sc.caller.model_dump().get("sip_headers") == {"X-Foo": "bar"}  # extra allowed
