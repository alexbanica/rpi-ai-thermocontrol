# Forgejo install dependency resolution plan

Status: Approved

## Spec reference

`specs/SPEC-forgejo-install-dependency-resolution.md`

## Affected files

- `README.md`
- `.github/workflows/publish.yml`
- `specs/SPEC-forgejo-install-dependency-resolution.md`
- `specs/PLAN-forgejo-install-dependency-resolution.md`

## Implementation performed

1. Added public PyPI as the documented extra dependency index while retaining
   Forgejo as the project package index.
2. Explained the separation between the Forgejo-hosted project and its public
   dependencies.
3. Replaced the release workflow's dependency-free wheel download with an exact
   version installation into an isolated target directory.
4. Required a wheel for `rpi-ai-thermocontrol`, disabled pip's cache, and kept
   the existing bounded publication-availability retries.
5. Recorded the delivered behavior in this approved spec and plan.

## Validation run

- YAML parsing for `.github/workflows/publish.yml`.
- Static inspection of the modified pip commands and options.
- `git diff --check`.

## Validation skipped

- Live Forgejo/PyPI installation, hosted Actions, and publication.
- Automated tests because workflow and documentation tests are prohibited by
  the repository's domain-only test policy.

## QA and code review

QA and code review were skipped as required by `$super-agent`.

## Documentation updates

The README public installation example and dependency-index explanation were
updated.

## Staging and delivery status

All accepted in-scope paths are staged. No commit or push is performed because
the user did not request either.

## Residual risk

Live index availability, ARM platform dependency compatibility, and hosted
workflow behavior remain unverified until the corrected installation path runs
against Forgejo and public PyPI.
