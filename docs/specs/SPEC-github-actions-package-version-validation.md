# GitHub Actions package-version validation

Status: Approved

## Purpose

Restore tag-release validation so it reads the package version from `setup.py`
before comparing it with the release tag.

## Requested behavior

The `Publish Forgejo Package` job must set `PACKAGE_VERSION` to the parsed
`setup.py` version, or fail with an explicit parsing error when no version is
present. It must then retain the existing exact-tag/version comparison.

## Scope

- Correct the inline version-extraction command in `.github/workflows/ci-publish.yml`.

## Out of scope

- Changing package version, tag format, publishing credentials, build behavior,
  or Forgejo publication.

## Deterministic behavior delivered

The extraction command prints the matched version when one exists. It raises the
existing explicit error only when parsing fails, rather than exiting successfully
before printing.

## Validation performed

- Inspected failed Actions job `95444742430`: failure occurred in `Validate tag
  and package version` before build or upload.
- Reproduced the empty extracted version from the original command and verified
  the corrected command returns `2.0.0`.
- Ran `git diff --check`.

## Validation skipped

- Hosted Actions rerun and Forgejo upload/download validation.

## Documentation changes

This completed-work specification records the workflow repair.
