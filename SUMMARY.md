# Campaign caller-ID migration

## Built

- Added keyword-only `from_numbers: Optional[List[str]]` to `Campaign.create`, serialized as `fromNumbers`.
- Preserved legacy positional and keyword `phone_ids`, including positional description/retry arguments. Legacy use emits `DeprecationWarning` with the replacement and migration URL; the docstring and usage example explain the migration.
- Added mocked HTTP regression tests and an Unreleased entry in `changelog.md`.

## Decisions and review

The live API reference was fetched read-only on 2026-10-24:
https://docs.smallest.ai/api-reference/voice-agents/campaigns/create
It explicitly allows both fields and ignores `phoneNumberIds` when `fromNumbers` is present. Both are therefore sent when supplied; precedence remains with the server.

Entries must be strings starting with `+`, which also excludes empty strings. Full E.164 validation and number ownership/resolution remain server-side. An empty list is transmitted for server validation. Supplying neither argument raises `ValueError` before HTTP.

The hand-written helper has no standalone request model or update operation. Its request model is the payload dictionary in `src/smallestai/atoms/helpers/campaign.py`. The generated sync/async campaign clients also build request dictionaries directly and remain unchanged to keep this helper fix surgical. No conflicting pair-handling convention or phone validation routine was found in the adjacent helpers.

Reviewed the complete tracked diff and new test file: only the campaign helper, changelog, tests, and this requested summary are changed. Authentication, timeout forwarding, response parsing, and HTTP error propagation are retained. There are no storage or authorization changes.

## Verification

Passed:

- `PYTHONPATH=src python -m pytest tests/custom/test_campaign_helper.py tests/custom/test_helpers_rest.py tests/custom/test_helpers_request_timeout.py -q` — 32 passed.
- `python -m ruff check src/smallestai/atoms/helpers/campaign.py tests/custom/test_campaign_helper.py`.
- `PYTHONPATH=src python -m compileall -q src/smallestai/atoms/helpers/campaign.py tests/custom/test_campaign_helper.py`.
- `git diff --check`.

The initial pytest invocation without `PYTHONPATH=src` imported a stale installed SDK and failed the new tests; the corrected checkout-based run passed. Tests mock HTTP and exercise successful payload/response handling, legacy compatibility, caller-location warnings, both fields, invalid inputs, and HTTP failure propagation. The global test harness started and stopped local WireMock containers; the new tests made no network requests.

## Skipped

No remote push, repository/PR creation, publication, or external writes were performed, as required by the headless-run constraints. Live campaign creation was not attempted because it would write to an external service. Full-suite tests, package build, remote CI/security checks, and live PR review were not run. No commit was created.

## Prepared PR description

Title: Add current caller-ID numbers to the campaign helper

Campaign creation through `Campaign.create` only accepted deprecated phone-number product IDs. Add `from_numbers`, serialized as `fromNumbers`, to support the current telephony API. Preserve `phone_ids` compatibility with a deprecation warning and migration link. Validate caller-ID entries locally for a leading `+`, leaving full E.164 and ownership validation to the server. When both fields are supplied, send both and let the API give `fromNumbers` precedence.

Validation: 32 focused mocked-HTTP/helper tests passed; focused Ruff, compilation, and diff whitespace checks passed. Live API writes and remote CI were not exercised.

Follow-ups outside this PR:

- Generated sync/async campaign clients (`CampaignsClient` / `AsyncCampaignsClient`, including raw clients) still expose `phone_number_ids` and send `phoneNumberIds`; migrate these separately, preferably in the generator definition.
- Generated agent create/update methods still send `telephonyProductId` in `src/smallestai/atoms/agents/raw_client.py`.
- Generated outbound call methods still send `fromProductId` in `src/smallestai/atoms/calls/raw_client.py`.

## Exact next steps for a human

1. Review `git diff` and the new `tests/custom/test_campaign_helper.py`; review this summary separately as the requested local handoff artifact.
2. Re-run the verification commands above with `PYTHONPATH=src` for checkout-based imports.
3. Create a branch and commit the intended files. Use the prepared title/description when opening a PR after pushing under human authorization.
4. Inspect the live PR diff, description, unresolved review threads, and CI/security checks. Address failures or feedback, rerun relevant verification, push fixes, and recheck before merging.
5. Schedule the listed generated-client telephony migrations separately.
