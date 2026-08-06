"""Convenience wrappers over the waves text-to-speech endpoints.

`client.waves` exposes several `synthesize_*` methods (per model / transport).
For the common case — "turn this text into an audio file" — start here:

    from smallestai import SmallestAI
    from smallestai.speech.helpers import synthesize_to_file, synthesize_bytes

    client = SmallestAI(api_key="...")
    synthesize_to_file(client, "Hello from Smallest.", voice_id="kanik", path="hello.wav")
    audio = synthesize_bytes(client, "Hello again.", voice_id="kanik")

Both wrap `client.speech.synthesize_tts` (which streams audio chunks) and accept
any of its keyword options via `**kwargs` (e.g. `sample_rate`, `speed`,
`language`). Sync client only.

Content expiry (Enterprise): pass `expire_content=True` to opt a request's
free-text content into deletion after 7 days (billing/usage unaffected). The
opt-in is silently ignored on non-Enterprise plans, so to confirm it took effect
use `synthesize_with_expiry`, which also returns the `x-content-expiry` outcome.
"""

import typing

# The current default TTS model. NB: the tts endpoint uses the underscore form
# (`lightning_v3.1`); the get-voices endpoint uses the hyphen form. See waves CLI.
DEFAULT_TTS_MODEL = "lightning_v3.1"

# Enterprise content-expiry opt-in (request) and its outcome (response).
EXPIRE_CONTENT_HEADER = "x-expire-content"
CONTENT_EXPIRY_HEADER = "x-content-expiry"


def _kwargs_with_expiry(kwargs: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Return a copy of kwargs with the x-expire-content header set on
    request_options (merging any headers the caller already passed)."""
    kwargs = dict(kwargs)
    request_options = dict(kwargs.get("request_options") or {})
    headers = dict(request_options.get("additional_headers") or {})
    headers[EXPIRE_CONTENT_HEADER] = "true"
    request_options["additional_headers"] = headers
    kwargs["request_options"] = request_options
    return kwargs


def _synthesize_stream(
    client: typing.Any,
    text: str,
    *,
    voice_id: str,
    model: str,
    output_format: str,
    expire_content: bool,
    kwargs: typing.Dict[str, typing.Any],
) -> typing.Iterator[bytes]:
    if expire_content:
        kwargs = _kwargs_with_expiry(kwargs)
    return client.speech.synthesize_tts(
        text=text, voice_id=voice_id, model=model, output_format=output_format, **kwargs
    )


def synthesize_bytes(
    client: typing.Any,
    text: str,
    *,
    voice_id: str,
    model: str = DEFAULT_TTS_MODEL,
    output_format: str = "wav",
    expire_content: bool = False,
    **kwargs: typing.Any,
) -> bytes:
    """Synthesize `text` and return the full audio as bytes (buffers the stream)."""
    return b"".join(
        _synthesize_stream(
            client,
            text,
            voice_id=voice_id,
            model=model,
            output_format=output_format,
            expire_content=expire_content,
            kwargs=kwargs,
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
    expire_content: bool = False,
    **kwargs: typing.Any,
) -> int:
    """Synthesize `text` and stream it to `path`. Returns the number of bytes written."""
    written = 0
    with open(path, "wb") as fh:
        for chunk in _synthesize_stream(
            client,
            text,
            voice_id=voice_id,
            model=model,
            output_format=output_format,
            expire_content=expire_content,
            kwargs=kwargs,
        ):
            fh.write(chunk)
            written += len(chunk)
    return written


def synthesize_with_expiry(
    client: typing.Any,
    text: str,
    *,
    voice_id: str,
    model: str = DEFAULT_TTS_MODEL,
    output_format: str = "wav",
    **kwargs: typing.Any,
) -> typing.Tuple[bytes, typing.Optional[str]]:
    """Synthesize with the Enterprise content-expiry opt-in and report the outcome.

    Returns ``(audio_bytes, outcome)`` where ``outcome`` is the value of the
    ``x-content-expiry`` response header: ``"not-entitled"`` means the plan does
    not include content expiry (content is retained), a truthy value means it was
    applied, and ``None`` means the header was absent. Use this when you need to
    confirm the opt-in took effect (a non-Enterprise request still succeeds — the
    header is simply ignored)."""
    kwargs = _kwargs_with_expiry(kwargs)
    # Streaming raw responses are exposed as a context manager yielding an
    # object with `.data` (the byte stream) and `.headers`.
    with client.speech.with_raw_response.synthesize_tts(
        text=text, voice_id=voice_id, model=model, output_format=output_format, **kwargs
    ) as raw:
        audio = b"".join(raw.data)
        outcome = raw.headers.get(CONTENT_EXPIRY_HEADER) if raw.headers is not None else None
    return audio, outcome
