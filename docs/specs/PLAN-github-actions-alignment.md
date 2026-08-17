# GitHub Actions Alignment Implementation Plan

Status: Approved

## Specification

- `docs/specs/SPEC-github-actions-alignment.md`

## Affected Files

- `.github/dependabot.yml`
- `.github/workflows/ci-publish.yml` (renamed and split)
- `.github/workflows/ci.yml`
- `.github/workflows/publish.yml`
- `README.md`
- `docs/specs/SPEC-github-actions-alignment.md`
- `docs/specs/PLAN-github-actions-alignment.md`

## Implementation Performed

1. Split the combined CI/publish workflow into the shared two-file layout.
2. Preserved lint and tests as publication prerequisites.
3. Standardized names, concurrency, immutable pins, checkout handling, caching,
   step names, and formatting.
4. Added grouped weekly Dependabot updates and updated README guidance.
5. Added this completed-work spec and plan.

## Validation Run

- YAML parsing and shared structural assertions for all aligned repositories.
- `git diff --check`.

## Validation Skipped

- Full tests, hosted Actions, and live Forgejo publication/download were skipped
  because they exceed the `super-agent` validation boundary or require external
  runtime state.

## Review And QA

- Formal QA: skipped as required by `super-agent`.
- Independent code review: skipped as required by `super-agent`.

## Documentation

- README and completed-work artifacts document the delivered conventions.

## Delivery State

- All accepted files are staged after final reconciliation, committed together,
  and pushed to `origin/main` as explicitly requested.
- The invoking checkout is used; no linked worktree or artifact cleanup applies.

## Residual Risk

- Hosted execution and live Forgejo behavior remain unverified.
