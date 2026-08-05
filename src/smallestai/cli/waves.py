"""`smallestai waves …` — text-to-speech, speech-to-text, and voices.

Thin CLI over the published `client.waves` surface, matching the style of
`smallestai calls`/`agents`. Auth resolves the same way (SMALLEST_API_KEY or
`smallestai auth login`).
"""

import json as _json
import typing

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client

console = Console()


def _data(resp):
    """Unwrap `.data` from an SDK response (or return the object itself)."""
    return getattr(resp, "data", resp)


def initialise_waves_app(auth_client: AuthClient):
    waves_app = typer.Typer(name="waves", help="Text-to-speech, speech-to-text, and voices.")

    @waves_app.command("voices")
    def voices(
        model: str = typer.Option("lightning-v3.1", "--model", help="Voice model"),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """List available voices for a model."""
        resp = make_client(auth_client).waves.get_voices(model=model)
        data = _data(resp)
        items = getattr(data, "voices", None) or (data if isinstance(data, list) else [])
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(items, default=str))
            return
        table = Table("Voice ID", "Name", "Gender", "Languages", title=f"Voices ({len(items)})")
        for v in items:
            tags = getattr(v, "tags", None) or {}
            if hasattr(tags, "dict"):
                tags = tags.dict()
            langs = tags.get("language") if isinstance(tags, dict) else None
            table.add_row(
                str(getattr(v, "voice_id", None) or getattr(v, "id", None) or "—"),
                str(getattr(v, "display_name", None) or getattr(v, "name", None) or "—"),
                str((tags.get("gender") if isinstance(tags, dict) else None) or "—"),
                ", ".join(langs) if isinstance(langs, list) else str(langs or "—"),
            )
        console.print(table)

    @waves_app.command("clones")
    def clones(
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """List your cloned voices."""
        resp = make_client(auth_client).waves.list_voice_clones()
        data = _data(resp)
        items = getattr(data, "voices", None) or (data if isinstance(data, list) else [])
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(items, default=str))
            return
        table = Table("Voice ID", "Name", "Status", title=f"Cloned voices ({len(items)})")
        for v in items:
            table.add_row(
                str(getattr(v, "voice_id", None) or getattr(v, "id", None) or "—"),
                str(getattr(v, "display_name", None) or getattr(v, "name", None) or "—"),
                str(getattr(v, "status", None) or "—"),
            )
        console.print(table)

    @waves_app.command("tts")
    def tts(
        text: str = typer.Argument(..., help="Text to synthesize"),
        voice_id: str = typer.Option(..., "--voice-id", help="Voice id (see `waves voices`)"),
        out: str = typer.Option("out.wav", "--out", "-o", help="Output audio file"),
        model: str = typer.Option("lightning_v3.1", "--model", help="TTS model"),
        output_format: str = typer.Option(
            "wav", "--format", help="Audio format: wav | mp3 | pcm | ulaw | alaw"
        ),
        sample_rate: int = typer.Option(None, "--sample-rate", help="Sample rate (Hz)"),
        speed: float = typer.Option(None, "--speed", help="Speech speed multiplier"),
    ):
        """Synthesize speech and write it to a file."""
        kw: typing.Dict[str, typing.Any] = {
            "text": text,
            "voice_id": voice_id,
            "model": model,
            "output_format": output_format,
        }
        if sample_rate is not None:
            kw["sample_rate"] = sample_rate
        if speed is not None:
            kw["speed"] = speed
        written = 0
        with open(out, "wb") as fh:
            for chunk in make_client(auth_client).waves.synthesize_tts(**kw):
                fh.write(chunk)
                written += len(chunk)
        console.print(f"[green]Wrote {written} bytes to {out}[/green]")

    @waves_app.command("stt")
    def stt(
        file: str = typer.Argument(..., help="Audio file to transcribe"),
        model: str = typer.Option("pulse", "--model", help="STT model: pulse | pulse-pro"),
        language: str = typer.Option("en", "--language", "--lang", help="Language code"),
        diarize: bool = typer.Option(False, "--diarize", help="Speaker diarization"),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """Transcribe an audio file."""
        with open(file, "rb") as fh:
            audio = fh.read()
        kw: typing.Dict[str, typing.Any] = {"model": model, "language": language, "request": audio}
        if diarize:
            kw["diarize"] = True
        resp = make_client(auth_client).waves.speech_to_text.transcribe(**kw)
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(resp, default=str))
            return
        text = (
            getattr(resp, "transcription", None)
            or getattr(resp, "text", None)
            or getattr(resp, "transcript", None)
        )
        console.print(text if text is not None else resp)

    return waves_app
