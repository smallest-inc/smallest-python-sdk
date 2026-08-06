"""Typed entry point for streaming speech-to-text (Pulse live WebSocket).

The generated ``client.speech.speech_to_text.stream()`` accepts session config only
through ``request_options["additional_query_parameters"]``, because the Pulse live
endpoint reads every knob (``model``, ``language``, ``sample_rate``, keyword boosting,
redaction, VAD, ...) from the WebSocket handshake query string. That works, but it is
untyped and undiscoverable.

``stream_speech_to_text`` gives all of those a typed keyword argument and forwards to
the generated method, so it survives a Fern regen (this module is .fernignore'd). The
typed params mirror the Speech-to-Text API reference; anything not named here still
passes through ``additional_query_parameters``.

Example (sync), with keyword boosting::

    from smallestai import SmallestAI
    from smallestai.speech.helpers import stream_speech_to_text

    client = SmallestAI()
    with stream_speech_to_text(
        client, language="en", sample_rate=16000,
        keywords=["Smallest", "Atoms", "Waves"],   # keyword boosting
        punctuate=True, numerals=True,
    ) as socket:
        socket.send_audio_chunk_out(pcm_bytes)
        socket.send_finalize_signal({"type": "finalize"})
        for event in socket:
            print(event)

The same call works with an ``AsyncSmallestAI`` client; it returns whatever the
underlying ``stream()`` returns (a sync or async context manager).

Booleans are sent to the server as the strings ``"true"`` / ``"false"``, and list
params (``keywords``, ``redact_pii``, ``redact_pci``) are sent comma-joined, matching
what the endpoint expects.
"""

import typing

__all__ = ["stream_speech_to_text", "build_stt_stream_query"]

# Sent to the server as "true" / "false" (the controller compares === "true").
_BOOLEAN_KNOBS = frozenset(
    {
        "word_timestamps",
        "sentence_timestamps",
        "diarize",
        "punctuate",
        "capitalize",
        "itn_normalize",
        "numerals",
        "finalize_on_words",
        "full_transcript",
        "vad",
        "vad_events",
    }
)

# Sent comma-joined when given a list/tuple (a plain string passes through as-is).
_LIST_KNOBS = frozenset({"keywords", "redact_pii", "redact_pci"})


def _coerce(key: str, value: typing.Any) -> typing.Any:
    if key in _BOOLEAN_KNOBS and isinstance(value, bool):
        return "true" if value else "false"
    if key in _LIST_KNOBS and isinstance(value, (list, tuple)):
        return ",".join(str(v) for v in value)
    return value


def build_stt_stream_query(
    *,
    language: str,
    model: str = "pulse",
    sample_rate: int = 16000,
    encoding: str = "linear16",
    format: typing.Optional[str] = None,
    # transcript formatting / output
    word_timestamps: typing.Optional[bool] = None,
    sentence_timestamps: typing.Optional[bool] = None,
    diarize: typing.Optional[bool] = None,
    punctuate: typing.Optional[bool] = None,
    capitalize: typing.Optional[bool] = None,
    itn_normalize: typing.Optional[bool] = None,
    numerals: typing.Optional[bool] = None,
    full_transcript: typing.Optional[bool] = None,
    max_words: typing.Optional[int] = None,
    # turn-taking / endpointing
    finalize_on_words: typing.Optional[bool] = None,
    eou_timeout_ms: typing.Optional[int] = None,
    # voice-activity detection
    vad: typing.Optional[bool] = None,
    vad_events: typing.Optional[bool] = None,
    vad_threshold: typing.Optional[float] = None,
    vad_min_speech_ms: typing.Optional[int] = None,
    # redaction
    redact_pii: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    redact_pci: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    # keyword boosting
    keywords: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    # escape hatch for anything not named above
    additional_query_parameters: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Dict[str, typing.Any]:
    """Build the handshake query dict for the Pulse live STT endpoint.

    Split out so it can be unit-tested and reused without opening a socket. Only
    ``language`` is required; every other param is omitted from the query when left as
    ``None``, so the server applies its own default.
    """
    params: typing.Dict[str, typing.Any] = {
        "model": model,
        "language": language,
        "sample_rate": sample_rate,
        "encoding": encoding,
    }
    optional = {
        "format": format,
        "word_timestamps": word_timestamps,
        "sentence_timestamps": sentence_timestamps,
        "diarize": diarize,
        "punctuate": punctuate,
        "capitalize": capitalize,
        "itn_normalize": itn_normalize,
        "numerals": numerals,
        "full_transcript": full_transcript,
        "max_words": max_words,
        "finalize_on_words": finalize_on_words,
        "eou_timeout_ms": eou_timeout_ms,
        "vad": vad,
        "vad_events": vad_events,
        "vad_threshold": vad_threshold,
        "vad_min_speech_ms": vad_min_speech_ms,
        "redact_pii": redact_pii,
        "redact_pci": redact_pci,
        "keywords": keywords,
    }
    for key, value in optional.items():
        if value is None:
            continue
        params[key] = _coerce(key, value)
    if additional_query_parameters:
        params.update(additional_query_parameters)
    return params


def stream_speech_to_text(
    client: typing.Any,
    *,
    language: str,
    model: str = "pulse",
    sample_rate: int = 16000,
    encoding: str = "linear16",
    format: typing.Optional[str] = None,
    word_timestamps: typing.Optional[bool] = None,
    sentence_timestamps: typing.Optional[bool] = None,
    diarize: typing.Optional[bool] = None,
    punctuate: typing.Optional[bool] = None,
    capitalize: typing.Optional[bool] = None,
    itn_normalize: typing.Optional[bool] = None,
    numerals: typing.Optional[bool] = None,
    full_transcript: typing.Optional[bool] = None,
    max_words: typing.Optional[int] = None,
    finalize_on_words: typing.Optional[bool] = None,
    eou_timeout_ms: typing.Optional[int] = None,
    vad: typing.Optional[bool] = None,
    vad_events: typing.Optional[bool] = None,
    vad_threshold: typing.Optional[float] = None,
    vad_min_speech_ms: typing.Optional[int] = None,
    redact_pii: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    redact_pci: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    keywords: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    additional_query_parameters: typing.Optional[typing.Dict[str, typing.Any]] = None,
    request_options: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Any:
    """Open a streaming STT session with typed handshake params.

    Delegates to ``client.speech.speech_to_text.stream(...)`` and returns its context
    manager unchanged, so use it with ``with`` (sync client) or ``async with`` (async
    client). Only ``language`` is required; the rest have Pulse-live defaults or are
    omitted when ``None``.

    Anything passed via ``additional_query_parameters`` or an existing
    ``request_options["additional_query_parameters"]`` overrides the typed values.
    """
    query = build_stt_stream_query(
        language=language,
        model=model,
        sample_rate=sample_rate,
        encoding=encoding,
        format=format,
        word_timestamps=word_timestamps,
        sentence_timestamps=sentence_timestamps,
        diarize=diarize,
        punctuate=punctuate,
        capitalize=capitalize,
        itn_normalize=itn_normalize,
        numerals=numerals,
        full_transcript=full_transcript,
        max_words=max_words,
        finalize_on_words=finalize_on_words,
        eou_timeout_ms=eou_timeout_ms,
        vad=vad,
        vad_events=vad_events,
        vad_threshold=vad_threshold,
        vad_min_speech_ms=vad_min_speech_ms,
        redact_pii=redact_pii,
        redact_pci=redact_pci,
        keywords=keywords,
        additional_query_parameters=additional_query_parameters,
    )
    resolved: typing.Dict[str, typing.Any] = dict(request_options or {})
    caller_overrides = resolved.get("additional_query_parameters") or {}
    resolved["additional_query_parameters"] = {**query, **caller_overrides}
    return client.speech.speech_to_text.stream(request_options=resolved)
