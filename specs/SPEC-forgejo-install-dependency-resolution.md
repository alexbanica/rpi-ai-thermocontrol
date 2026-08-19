# Forgejo install dependency resolution

Status: Approved

## Purpose

Ensure the published `rpi-ai-thermocontrol` wheel can be installed anonymously
from Forgejo together with its public Python dependencies.

## Requested behavior

The public installation command must retrieve `rpi-ai-thermocontrol` from the
Forgejo package index and allow pip to retrieve dependencies unavailable there,
including `PyYAML`, from public PyPI. Release verification must exercise that
same dependency-resolving installation path instead of downloading the project
wheel with dependencies disabled.

## Scope

- Correct the public Forgejo installation command in `README.md`.
- Strengthen the post-publication smoke check in
  `.github/workflows/publish.yml`.

## Out of scope

- Publishing third-party dependencies to Forgejo.
- Changing package dependencies or versions.
- Changing Forgejo credentials, visibility, or upload behavior.
- Adding automated workflow tests, which the repository test policy forbids.

## Inputs and constraints

- Forgejo remains the primary index for `rpi-ai-thermocontrol`.
- Public PyPI is an additional index for dependencies absent from Forgejo.
- Anonymous verification must select the published project wheel and must not
  reuse pip's download cache.

## Deterministic behavior delivered

The documented command supplies both the Forgejo package index and public PyPI.
The release smoke check installs the exact published version into an isolated
target directory, requires a wheel for `rpi-ai-thermocontrol`, resolves its
dependencies, disables pip's cache, and retains the existing five-attempt
Forgejo availability retry behavior.

## Assumptions

`rpi-ai-thermocontrol` is published only in the configured Forgejo index, while
its third-party dependencies are available from public PyPI. The GitHub-hosted
runner can reach both indexes during release verification.

## Impact

Operators no longer receive `No matching distribution found for PyYAML` solely
because the Forgejo-only install command replaced pip's public PyPI index. A
release fails its smoke check when the project wheel is downloadable but its
declared dependencies cannot be resolved and installed.

## Validation performed

- Parsed `.github/workflows/publish.yml` as YAML.
- Checked the workflow command structure and relevant pip options statically.
- Ran `git diff --check`.

## Validation skipped

- Live installation from Forgejo and public PyPI.
- Hosted GitHub Actions execution and package publication.
- Automated tests, code review, and QA.

## Documentation changes

`README.md` now documents the dependency index and why it is required.
