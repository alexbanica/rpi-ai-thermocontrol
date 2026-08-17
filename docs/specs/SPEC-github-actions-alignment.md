# GitHub Actions Alignment

Status: Approved

## Purpose

Align this Python project's automation with the shared workspace conventions
while preserving its package validation and Forgejo publication contract.

## Requested Behavior

- Separate CI and publication into `.github/workflows/ci.yml` and
  `.github/workflows/publish.yml`.
- Use the common `CI` and `Publish` workflow names.
- Apply least-privilege permissions, immutable external-action pins,
  non-persisted checkout credentials, dependency caching, and per-workflow/per-ref
  concurrency.
- Preserve stable and beta release validation and quality gates.
- Enable grouped weekly Dependabot updates for GitHub Actions.

## Scope

- GitHub Actions and Dependabot configuration.
- README automation and release-tag documentation.
- Completed-work spec and plan artifacts.

## Out Of Scope

- Python application, tests, package metadata, dependency, or runtime behavior.
- Forgejo endpoint, credential names, artifact construction, and anonymous
  verification behavior.
- Central cross-repository reusable workflows.

## Deterministic Behavior Delivered

- `ci.yml` runs the existing Python 3.9 lint and test gates for `main` pull
  requests and pushes, canceling superseded runs for the same workflow/ref.
- `publish.yml` runs the same gates for supported stable and beta tags before
  building, validating, uploading, and anonymously downloading the package.
- Publish runs never cancel an in-progress release for the same ref.
- Checkout is pinned to `v7.0.1`, setup-python to `v7.0.0`, checkout credentials
  are not persisted, and pip caches are keyed by both requirement files.
- Both workflows use read-only contents permission.
- Dependabot groups GitHub Actions updates weekly.

## Assumptions And Impact

- Splitting the former combined workflow changes workflow presentation but
  preserves the prior lint/test-before-publish dependency.
- GitHub-hosted runners satisfy the Node 24 runner requirement of the selected
  action releases.

## Validation Performed

- Parsed both workflows and Dependabot configuration as YAML.
- Structurally verified triggers, names, permissions, concurrency, immutable
  action pins, checkout credential handling, and pip caching.
- Ran `git diff --check`.

## Validation Skipped

- Full tests, hosted GitHub Actions, and live Forgejo publication/download were
  not run.
- Formal QA and independent review were skipped by `super-agent`.

## Documentation Changes

- Updated README workflow names and stable/beta release mapping.
