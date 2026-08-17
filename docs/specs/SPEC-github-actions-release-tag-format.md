# GitHub Actions release tag format

Status: Approved

## Purpose

Make the release tag the authoritative Forgejo package version, following the
existing `rpi-groove-ir-receiver` release model.

## Requested behavior

The release workflow accepts only Git tags `MAJOR.MINOR.PATCH` and
`MAJOR.MINOR.PATCH-betaN`, where `N` is a positive integer. A stable tag maps
directly to the package version. A beta tag maps to its PEP 440 package version:
`1.0.0-beta1` maps to `1.0.0b1`.

The workflow must build with that derived version without requiring a committed
`setup.py` version to match the tag or requiring the tagged commit to be on
`main`.

## Scope

- Update `.github/workflows/ci-publish.yml` tag triggering, validation, and
  anonymous wheel verification.
- Make `setup.py` accept an ephemeral `RELEASE_VERSION` value for release
  builds while retaining `1.0.0` as its ordinary local-build default.

## Out of scope

- Changing build artifacts, credentials, Forgejo visibility, or publication
  targets.

## Deterministic behavior delivered

GitHub Actions runs the release workflow for numeric-looking tags and
fail-closes unless the tag exactly matches one supported form. The workflow
derives the corresponding PEP 440 package version, passes it to the release
build as `RELEASE_VERSION`, and uses it for anonymous-install verification.
The verification downloads only the published wheel, matching the receiver's
release path and avoiding a later source-distribution metadata build that lacks
the ephemeral `RELEASE_VERSION` value.

## Assumptions

Beta package metadata uses standard PEP 440 `bN` notation, as required by
Python build and package tooling. Non-release local builds use the default
`setup.py` version unless `RELEASE_VERSION` is explicitly set.

## Impact

`1.0.1` builds and publishes package version `1.0.1` without a source-version
edit. `1.0.1-beta1` builds and publishes `1.0.1b1`. Unsupported tags fail
before building or uploading artifacts.

## Validation performed

- Local Bash simulations for stable and beta tag mappings, plus invalid-tag
  rejection.
- Local `setup.py --version` checks for the default and an injected release
  version.
- Built a local `1.0.1` wheel with `RELEASE_VERSION` and verified its embedded
  metadata reports `Version: 1.0.1`.
- Confirmed pip supports wheel-only download selection.
- `git diff --check`.

## Validation skipped

- Hosted Actions rerun and live Forgejo package publication/download with the
  tag-authoritative release version and wheel-only verification.

## Documentation changes

This completed-work specification records the accepted release-tag contract.
