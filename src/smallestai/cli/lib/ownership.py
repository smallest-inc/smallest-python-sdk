"""Crew-vs-platform config ownership: the single source of truth for the CLI.

A crew build takes over ONLY the LLM turn. Everything else about the call stays on
the platform agent config and is read fresh each call. This module holds that boundary
as data so `init` and `doctor` can surface it consistently.

See AGENT_SDK_OWNERSHIP.md for the full matrix and rationale.
"""

from __future__ import annotations

from typing import List, Tuple

from rich.console import Console
from rich.table import Table

# (concern, where it is configured)
CREW_OWNS: List[Tuple[str, str]] = [
    ("System prompt / LLM messages", "crew code"),
    ("Function tools (@function_tool, incl. transfer_call)", "crew code"),
    ("end_call / speak() / mute / unmute", "crew code"),
]

# (concern, platform field)
PLATFORM_OWNS: List[Tuple[str, str]] = [
    ("PII redaction", "redactionConfig.isEnabled"),
    ("Voice / TTS (provider, speed, ...)", "synthesizer*"),
    ("STT provider + language + switching", "transcriberType, defaultLanguage"),
    ("First message", "firstMessage"),
    ("Interruption / VAD / smart-turn", "allowInterruptions, smartTurnConfig"),
    ("Voicemail detection / denoising", "voiceMailDetectionConfig, denoisingConfig"),
    ("Session / idle timeouts", "sessionTimeoutConfig, llmIdleTimeoutConfig"),
    ("Background sound / pronunciation", "backgroundSound, pronunciationDicts"),
]

# Editing these on the dashboard for a crew agent does nothing (safe no-ops).
DASHBOARD_NO_OPS: List[str] = [
    "The Tools panel (including its transfer_call toggle)",
    "The single-prompt prompt field",
    "The model dropdown (the crew serves its own LLM)",
]

SUMMARY = (
    "A crew build owns ONLY the LLM turn (prompt, messages, @function_tools, end_call, "
    "speak, mute). Everything else - voice, STT, PII redaction, first message, timeouts - "
    "is platform config: set it in the agent settings (dashboard or API), it takes effect "
    "on the next call, no redeploy. The dashboard Tools panel and prompt field are ignored "
    "for a crew agent."
)


def render_ownership(console: Console) -> None:
    """Print the crew-vs-platform ownership tables + no-ops to the console."""
    crew = Table(title="Your crew code owns (the LLM turn)", title_style="bold cyan", show_edge=True)
    crew.add_column("Concern")
    crew.add_column("Configured in")
    for concern, where in CREW_OWNS:
        crew.add_row(concern, where)

    plat = Table(title="The platform owns (set in agent settings, no redeploy)", title_style="bold magenta")
    plat.add_column("Concern")
    plat.add_column("Field")
    for concern, field in PLATFORM_OWNS:
        plat.add_row(concern, field)

    console.print(crew)
    console.print(plat)
    console.print("[dim]Ignored for a crew agent (safe to leave alone on the dashboard):[/dim]")
    for item in DASHBOARD_NO_OPS:
        console.print(f"  [dim]- {item}[/dim]")
