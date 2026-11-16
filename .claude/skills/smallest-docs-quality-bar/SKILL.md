---
name: Smallest docs quality bar
description: >-
  Extra rigor for Smallest docs and SDK-adjacent prose: unslop customer copy,
  prove claims, technical-writing structure. Use with the docs edit protocol;
  does not replace probe/API gates.
---
# Smallest docs quality bar

Patterns adapted from Lauren Tan’s pstack (`/unslop`, `/technical-writing`, prove-it) for Smallest — keep our probe protocol as the truth gate.

## When

After (or interleaved with) the docs edit protocol, before asking for human review. Also when rewriting README / changelog / PR body for docs or SDK regen PRs.

## Rules

1. **Prove it** — every shippable API claim still needs `PROVEN` live probe or `waves-platform` file:line (docs-edit protocol). Do not “feel” correct.
2. **Unslop** — delete AI tells: filler intros, “robust/seamless/leverage”, fake certainty, internal notes, mechanism dumps customers don’t need. Prefer outcome language.
3. **Technical writing** — task-first; one idea per paragraph; Diátaxis-ish (howto vs reference vs explanation); short sentences; no newly coined product brands (Atoms/Waves rule from docs-edit).
4. **Smallest change** — prefer deleting wrong prose over adding hedging layers.
5. **Interrogate before merge** — re-read the diff as a hostile integrator: broken links, contradicting tables, default retention claims that disagree across files.

Do **not** vendor the full pstack plugin into this repo. Install pstack in Cursor locally (`/add-plugin pstack`) if you want `/poteto-mode` personally; this skill is the portable subset for Claude Code / org clones.
