"""Convenience wrappers over the waves text-to-speech endpoints.

`client.waves` exposes several `synthesize_*` methods (per model / transport).
For the common case — "turn this text into an audio file" — start here:

    from smallestai import SmallestAI
    from smallestai.waves.helpers import synthesize_to_file, synthesize_bytes

    client = SmallestAI(api_key="...")
    synthesize_to_file(client, "Hello from Smallest.", voice_id="kanik", path="hello.wav")
    audio = synthesize_bytes(client, "Hello again.", voice_id="kanik")

Both wrap `client.waves.synthesize_tts` (which streams audio chunks) and accept
any of its keyword options via `**kwargs` (e.g. `sample_rate`, `speed`,
`language`). Sync client only.
"""

import typing

# The current default TTS model. NB: the tts endpoint uses the underscore form
# (`lightning_v3.1`); the get-voices endpoint uses the hyphen form. See waves CLI.
DEFAULT_TTS_MODEL = "lightning_v3.1"


def _synthesize_stream(
    client: typing.Any,
    text: str,
    *,
    voice_id: str,
    model: str,
    output_format: str,
    kwargs: typing.Dict[str, typing.Any],
) -> typing.Iterator[bytes]:
    return client.waves.synthesize_tts(
        text=text, voice_id=voice_id, model=model, output_format=output_format, **kwargs
    )


def synthesize_bytes(
    client: typing.Any,
    text: str,
    *,
    voice_id: str,
    model: str = DEFAULT_TTS_MODEL,
    output_format: str = "wav",
    **kwargs: typing.Any,
) -> bytes:
    """Synthesize `text` and return the full audio as bytes (buffers the stream)."""
    return b"".join(
        _synthesize_stream(
            client, text, voice_id=voice_id, model=model, output_format=output_format, kwargs=kwargs
        )
    )


def synthesize_to_file(
    client: typing.Any,
    text: str,
    *,
    voice_id: str,
    path: str,
    model: str = DEFAULT_TTS_MODEL,
    output_format: str = "wav",
    **kwargs: typing.Any,
) -> int:
    """Synthesize `text` and stream it to `path`. Returns the number of bytes written."""
    written = 0
    with open(path, "wb") as fh:
        for chunk in _synthesize_stream(
            client, text, voice_id=voice_id, model=model, output_format=output_format, kwargs=kwargs
        ):
            fh.write(chunk)
            written += len(chunk)
    return written
