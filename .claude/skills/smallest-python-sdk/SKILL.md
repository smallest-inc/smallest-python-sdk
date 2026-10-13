---
name: Smallest Python SDK
description: >-
  Use for any change in smallest-python-sdk: Fern regeneration, Replay
  conflicts, hand-written crew/CLI layers, releases. Prefer regenerated client
  over inventing API surface.
---
# Smallest Python SDK

## Source of truth

1. **Generated client** comes from Fern in `smallest-inc/smallest-ai-documentation` (`fern/apis/unified/generators.yml` → this repo, `mode: pull-request`).
2. Trigger is **manual**: from the docs repo run  
   `gh workflow run python-sdk.yml -R smallest-inc/smallest-ai-documentation`  
   Nothing auto-opens an SDK PR when waves-platform / api-spec issues fire.
3. Hand-written layers (crew, CLI, helpers) may exist **above** the generated client — do not fight Fern on generated paths; resolve Replay conflicts carefully.

## When docs/public API change

1. Confirm docs OpenAPI / Fern inputs reflect the GA surface (link related docs `api-spec` issue if any).
2. Dispatch `python-sdk.yml`; wait for Fern bot PR.
3. If PR closed for **Replay** conflicts: rebase/regenerate, keep intentional hand-written files, do not silently drop public methods.
4. Merge Fern PR; let `ci.yml` publish. Verify version / changelog honesty.
5. **Never invent** request/response fields in README examples that the regenerated client does not expose — probe or read generated code.

## Quality bar

- Prefer smallest diff; prove regen with real import/call smoke when credentials allow (`SMALLEST_API_KEY`).
- Unslop README/changelog; no fake “fully updated” claims if only hand-written paths changed.
- Customer prose naming: capabilities / model names — no new Atoms/Waves product intros if you touch shared wording.

## Stale detection (quick)

- No open Fern “SDK regeneration” PR after a docs OpenAPI bump → missing dispatch.
- Closed-unmerged Fern PRs → Replay / conflict debt.
- `.fern/metadata.json` / package version far behind docs Fern CLI pin → investigate.

## Related

Docs protocol (claims about the live API) lives in the documentation repo skills — do not duplicate probe tables here; link the docs PR/issue instead.
