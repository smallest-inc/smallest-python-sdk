# CLAUDE.md — smallest-python-sdk

Agents working in this repo **must** read `.claude/skills/smallest-python-sdk/SKILL.md` by default.

- Prefer Fern regeneration from `smallest-ai-documentation` (`python-sdk.yml` workflow_dispatch) over hand-editing generated clients.
- After public API / docs OpenAPI changes: check for an open Fern regen PR; if missing, say so and dispatch from the docs repo.
- Do not invent SDK methods or payload fields that the regenerated client does not expose.
- Hand-written crew/CLI layers: keep diffs small; resolve Replay conflicts without deleting intentional customizations blindly.
