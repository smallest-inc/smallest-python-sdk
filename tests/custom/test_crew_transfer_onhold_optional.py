"""SDKAgentTransferConversationEvent.on_hold_music must be optional.

Regression: the field was declared Optional[...] but without a default, so pydantic
treated it as required — every crew transfer had to pass on_hold_music (even as None)
or the event construction raised a ValidationError. It now defaults to None.
"""

import pytest

from smallestai.atoms.crew.events import SDKAgentTransferConversationEvent, TransferOption


def _transfer_option():
    return TransferOption(type="cold_transfer")


def test_on_hold_music_is_optional():
    ev = SDKAgentTransferConversationEvent(
        transfer_call_number="+15551234567",
        transfer_options=_transfer_option(),
    )
    assert ev.on_hold_music is None
    assert ev.transfer_call_number == "+15551234567"


def test_on_hold_music_still_settable():
    ev = SDKAgentTransferConversationEvent(
        transfer_call_number="+15551234567",
        transfer_options=_transfer_option(),
        on_hold_music="relaxing_sound",
    )
    assert ev.on_hold_music == "relaxing_sound"


@pytest.mark.parametrize("music", ["ringtone", "relaxing_sound", "uplifting_beats", "none"])
def test_on_hold_music_accepts_all_options(music):
    ev = SDKAgentTransferConversationEvent(
        transfer_call_number="+1",
        transfer_options=_transfer_option(),
        on_hold_music=music,
    )
    assert ev.on_hold_music == music
