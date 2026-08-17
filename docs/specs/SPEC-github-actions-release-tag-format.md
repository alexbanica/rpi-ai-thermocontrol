# GitHub Actions release tag format

Status: Approved

## Purpose

Repair Forgejo package publication for numeric stable and beta release tags.

## Requested behavior

The release workflow accepts only Git tags `MAJOR.MINOR.PATCH` and
`MAJOR.MINOR.PATCH-betaN`, where `N` is a positive integer. A stable tag maps
directly to the package version. A beta tag maps to its PEP 440 package version:
`1.0.0-beta1` maps to `1.0.0b1`.

## Scope

- Update `.github/workflows/ci-publish.yml` tag triggering, validation, and
  anonymous-install verification.
- Align `setup.py` package metadata with the existing `1.0.0` release tag.

## Out of scope

- Changing build artifacts, credentials, Forgejo visibility, or publication
  targets.

## Deterministic behavior delivered

GitHub Actions runs the release-validation job for any pushed tag. The job
fail-closes unless the tag exactly matches one supported form, derives the
corresponding PEP 440 package version, and requires that version to match
`setup.py`. The anonymous install check uses that derived package version.

## Assumptions

Beta package metadata uses standard PEP 440 `bN` notation, as required by
Python build and package tooling.

## Impact

`1.0.0` publishes only when `setup.py` is `1.0.0`; `1.0.0-beta1` publishes
only when `setup.py` is `1.0.0b1`. Unsupported tags run validation and fail
before building or uploading artifacts.

The current package metadata is set to `1.0.0`, allowing the existing `1.0.0`
tag to pass the exact-version check.

## Validation performed

- Local Bash simulations for stable and beta tag mappings, plus invalid-tag
  rejection.
- `git diff --check`.

## Validation skipped

- Hosted Actions rerun and live Forgejo package publication/download.

## Documentation changes

This completed-work specification records the accepted release-tag contract.
