# Releasing `smallestai`

The PyPI package is **`smallestai`**. Releases are driven from **this repo**.

## How a release happens (today)

`.github/workflows/ci.yml` runs on every push to `main` and has a `publish` job that:

1. Reads the version from `pyproject.toml` (`[tool.poetry] version`).
2. If no git tag `v<version>` exists yet → builds the package and `poetry publish`es to
   PyPI using the repo secret **`PYPI_API_TOKEN`**, then creates the `v<version>` tag.
3. If the tag already exists → no-op.

**So a release = bump the version in `pyproject.toml` + merge to `main`.** Nothing
else publishes. (There is also `release.yml` for a manual `workflow_dispatch` if you
prefer to trigger explicitly.)

### To cut a release
1. Add a `## <version> - YYYY-MM-DD` entry to `changelog.md` / `CHANGELOG.md`.
2. Bump `[tool.poetry] version` in `pyproject.toml`.
3. Merge to `main` → CI publishes + tags.

### Prerequisite
Repo secret **`PYPI_API_TOKEN`** (PyPI API token, upload scope) must be set
(Settings → Secrets and variables → Actions). It is.

## After the Fern repo-target migration (Workstream A)

Once `fern/apis/unified/generators.yml` `github.repository` points at
`smallest-inc/smallest-python-sdk`, Fern will open **regen PRs** here (mode:
`pull-request`). The flow becomes: Fern opens a PR (generated code + version bump) →
review → merge → `ci.yml` publishes. **This repo's `ci.yml` stays the single
publisher.**

⚠️ **Avoid double-publish:** the generator currently also has `output.location: pypi`,
which makes *Fern itself* publish during `fern generate`. Pick **one** publisher.
Recommended: drop `output.location: pypi` from the python-sdk generator (use
`github` output only) so the canonical repo's `ci.yml` owns publishing. Tracked in
the Workstream A escalation.
