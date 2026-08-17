# Plan: Forgejo Python Package Publishing

Status: Approved

## Approved Spec

- `docs/specs/forgejo-python-package-publishing.md`
- Status: Approved

## Objective

Implement the approved GitHub Actions contract so pull requests to `main`,
pushes and merges to `main`, and trusted stable release tags run deterministic
lint and test gates, while matching tags publish checked Python distributions to
the anonymously readable Forgejo `public` package registry.

## No-Research Constraint

Implementation must use only the approved spec, applicable agent instructions,
this plan, the exact files listed or directly implied here, current branch and
worktree state, and minimal local syntax patterns. It must not reopen product,
architecture, scope, registry, action-version, or plan research. Any material
conflict or missing behavior discovered during implementation requires stopping
for a spec or plan amendment.

## Planning Evidence and Decisions

- The invoking checkout was clean before planning and is currently `main` at
  `2213043b398079182d713a23a960253a7f375da3` with only the approved spec and
  this proposed plan as task artifacts.
- `origin/main` was fetched during planning and resolves to the same commit.
- `spec/forgejo-python-package-publishing` did not exist locally or on `origin`
  when checked during planning.
- The repository has no `.github` workflow directory.
- `setup.py` declares package `rpi-ai-thermocontrol`, version `2.0.0`, and Python
  `>=3.9`; release tags therefore remain operator-created and must match this
  metadata exactly.
- `requirements.dev.txt` already defines the lint and test tools through `ruff`
  and `pytest`; build and upload tools are release-job-only dependencies and do
  not require a dependency-file change.
- The implementation uses `actions/checkout@v7` and
  `actions/setup-python@v7`, the current official major versions verified during
  planning, with only `contents: read` GitHub permissions.
- `pytest`, `ruff`, and `actionlint` were not installed in the planning host, so
  no local baseline suite or workflow lint was claimed during planning.
- The change is a narrow CI/release configuration and documentation change.
  Architecture-agent review is not justified.

## Expected Files

- `.github/workflows/ci-publish.yml` (new)
- `README.md`
- `AGENTS.md`
- `docs/specs/forgejo-python-package-publishing.md` (approved artifact)
- `docs/specs/PLAN-forgejo-python-package-publishing.md` (this plan)

No application, test, runtime configuration, package metadata, dependency, or
hardware-adapter file is expected to change. If the current package cannot be
built or checked without such a change, stop for an approved artifact amendment.

## Branch and Worktree Policy

1. Begin implementation only after the clean-context gate is satisfied.
2. Fetch `origin/main` and verify it still resolves to exact expected base
   `2213043b398079182d713a23a960253a7f375da3`. If it moved, stop rather than
   silently select a different base.
3. Verify the planned branch `spec/forgejo-python-package-publishing` remains
   absent locally and on `origin`; any conflict requires stopping.
4. Use task slug `forgejo-python-package-publishing` and isolated worktree path
   `/home/alexbanica/.herdr/worktrees/rpi-ai-thermocontrol/forgejo-python-package-publishing`.
5. Create `/home/alexbanica/.herdr/worktrees/rpi-ai-thermocontrol` when absent,
   verify the repository name and task slug, and create or reuse the planned
   worktree detached at the exact expected base. A reused worktree must belong to
   this repository, point at the expected base, and be clean.
6. Keep the invoking checkout on `main`. After worktree creation, the main agent
   copies the approved spec and plan from the invoking checkout to their exact
   relative paths in the detached worktree and verifies byte-for-byte content.
   Workers do not transfer or edit these artifacts.
7. Workers must not create or manage worktrees or branches, commit, push, stage,
   or alter the invoking checkout.
8. Remain detached during development. Create
   `spec/forgejo-python-package-publishing` in the worktree only after the change
   reaches its locally validated DRAFT state.
9. After the implementation commit is pushed and verified, remove the duplicate
   untracked spec and plan copies from the invoking checkout only if they are
   still byte-identical to the committed versions. Preserve and report either
   file if it has been modified.

## Test-First Applicability

Test-first production coverage is not applicable. The change is workflow
configuration, documentation, and active-artifact metadata only; it changes no
business or domain logic and adds no executable application behavior suitable
for project unit tests. Existing tests must remain unchanged. The workflow
contract instead receives static workflow linting, temporary-repository guard
simulation, package-build checks, and the full existing test suite.

No test-focused subagent is planned. Maximum test-focused concurrency is `0`.

## Workflow Contract Implementation

Create one workflow at `.github/workflows/ci-publish.yml` with these boundaries:

1. Name the workflow `CI and Forgejo Publish` and define stable job/check names
   `Lint`, `Tests`, and `Publish Forgejo Package`.
2. Trigger pull-request validation only for pull requests targeting `main`.
3. Configure the push event with both `main` and exact stable numeric tag filter
   `[0-9]+.[0-9]+.[0-9]+`; branch pushes and tag pushes are separate accepted
   alternatives.
4. Run lint and test jobs on `ubuntu-latest` with Python `3.9`,
   `actions/checkout@v7`, `actions/setup-python@v7`, and repository contents
   read permission only.
5. Install the existing developer requirements, run `ruff check .` in the lint
   job, and run `pytest` in the test job. Neither job receives Forgejo secrets.
6. Run the publish job only for a tag ref and only after both validation jobs
   succeed. Use non-cancelling per-tag concurrency so a newer run cannot cancel
   an in-flight publication.
7. Check out the exact tag with sufficient Git history, fetch `main`, and fail if
   the tag target is not an ancestor of `origin/main`.
8. Fail unless the tag is an exact unprefixed `MAJOR.MINOR.PATCH` value and is
   identical to the canonical package version built from `setup.py`.
9. Install `build` and `twine` only in the publish job, run `python -m build` to
   create exactly one source distribution and one wheel, and run
   `python -m twine check` on both files.
10. Upload with `python -m twine upload --repository-url
    https://forgejo.alexlab.nl/api/packages/public/pypi dist/*`. Supply
    `TWINE_USERNAME` and `TWINE_PASSWORD` only on this step from
    `FORGEJO_PACKAGE_USERNAME` and `FORGEJO_PACKAGE_TOKEN` respectively. Do not
    use skip-existing or an insecure TLS option.
11. After upload, remove credentials from the environment and use a bounded
    retry to run an unauthenticated, dependency-free exact-version download from
    `https://forgejo.alexlab.nl/api/packages/public/pypi/simple`. Exhausting the
    retry fails the job.
12. Avoid `pull_request_target`, interpolating untrusted values into privileged
    execution, credential-bearing URLs, secret echoing, and third-party actions.

## Documentation and Agent Metadata

1. Add a focused `README.md` release section containing the approved tag format,
   metadata-version match, `main` ancestry rule, GitHub secret names, Forgejo
   upload/index endpoints, credential-free exact-version install example,
   immutable duplicate behavior, and first live release DRAFT boundary.
2. Document operator-owned GitHub setup: require the stable `Lint` and `Tests`
   checks before merging to `main`, restrict matching release tags to trusted
   maintainers, and configure the two Forgejo secrets.
3. Do not claim that repository code configures branch protection, tag rules,
   organization visibility, token permissions, or Forgejo instance settings.
4. Update only the `AGENTS.md` active-spec and branch entries to this approved
   work. Preserve all architecture, packaging, and HTTP/OpenAPI rules.

## Dependency-Aware Execution Graph

### W0 - Main-Agent Worktree and Artifact Setup

- Type: integration setup.
- Owner: main agent only.
- Files: approved spec and plan copies only.
- Dependencies: clean-context, base, branch, path, and worktree checks.
- Acceptance: detached clean worktree at the exact base containing byte-identical
  approved artifacts; invoking checkout otherwise unchanged.
- Validation: `git worktree list --porcelain`, `git status --short --branch`,
  `git rev-parse HEAD`, and byte comparison.
- Subagent: none.

### D1 - CI and Release Workflow

- Type: development, configuration-only.
- Owner: `.github/workflows/ci-publish.yml` exclusively.
- Dependencies: W0.
- Acceptance: every Workflow Contract Implementation item is represented with
  no secret exposure or package publication from non-tag events.
- Validation: focused file inspection and local static syntax parsing; full
  actionlint and behavioral checks are owned by QA.
- Subagent: one clean-context `developer`, scoped for at most five minutes.

### D2 - Release Documentation and Active Metadata

- Type: development, documentation-only.
- Owner: `README.md` and only the active-spec/branch entries in `AGENTS.md`.
- Dependencies: W0. It may run concurrently with D1 because ownership does not
  overlap and exact workflow/check names are fixed by this plan.
- Acceptance: every Documentation and Agent Metadata requirement is documented
  literally, without secret values or unsupported operational claims.
- Validation: focused diff and exact endpoint/check-name comparison to the
  approved spec and plan.
- Subagent: one clean-context `developer`, scoped for at most five minutes.

### I1 - Main-Agent Integration

- Type: integration.
- Owner: whole accepted change set; no new behavior.
- Dependencies: D1 and D2.
- Acceptance: worker changes are non-overlapping, expected paths only, and the
  workflow, documentation, spec, plan, and agent metadata agree exactly.
- Validation: full unstaged diff, changed-path classification, and
  `git diff --check`.
- Subagent: none.

### R1 - Independent Review

- Type: code review.
- Owner: read-only review of the complete diff.
- Dependencies: I1.
- Acceptance: reviewer checks spec/plan conformance, event coverage, job
  dependencies, tag ancestry and version guards, package immutability, public
  verification, secret isolation, TLS, documentation accuracy, and missing
  validation. Findings are concrete and prioritized; no files are edited.
- Validation: reviewer report reconciled by the main agent.
- Subagent: one clean-context `code-reviewer`, scoped for at most five minutes.

### F1 - Conditional Review or QA Fix

- Type: development, only if a confirmed in-scope finding exists.
- Owner: the smallest file boundary implicated by one or more related findings.
- Dependencies: R1 or QA finding.
- Acceptance: finding is resolved without scope expansion or weakening the
  approved contract.
- Validation: focused regression check followed by affected full QA checks.
- Subagent: a new clean-context `developer`, scoped for at most five minutes;
  split unrelated findings into non-overlapping follow-ups.

### Q1 - Main-Agent QA and Acceptance

- Type: QA and final integration.
- Owner: main agent only.
- Dependencies: R1 and any F1 work.
- Acceptance: all locally executable validation passes; non-executable live
  checks are reported accurately; every path is reconciled before delivery.
- Validation: commands and traces in the next section.
- Subagent: none.

Maximum planned concurrency is `0` test-focused agents, `2` developer agents,
and `1` code-review agent. D1 and D2 are the only concurrent units. The main
agent serializes artifact transfer, integration, review-fix routing, staging,
branch creation, commit, push, and duplicate-artifact cleanup. If any subagent
reaches five minutes, interrupt it, preserve and inspect usable work, record its
status, and split remaining ownership into smaller clean-context units rather
than retrying the same assignment.

## Validation and Main-Agent QA

Use temporary environments and caches under `/tmp`; do not add generated build,
virtual-environment, or tool files to the repository.

1. Create a temporary virtual environment and install
   `requirements.dev.txt`, `build`, and `twine` with the pip cache redirected to
   `/tmp`.
2. Run `python -m pytest`.
3. Run `python -m ruff check .`.
4. Download official `actionlint` v1.7.12 for Linux amd64 into `/tmp`, verify its
   published SHA-256
   `8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8`,
   and run it against `.github/workflows/ci-publish.yml`.
5. Build into a temporary output directory with `python -m build`, run
   `python -m twine check` on both distributions, assert exactly one wheel and
   one source archive exist, and inspect both metadata records for package name
   `rpi-ai-thermocontrol`, version `2.0.0`, and Python requirement `>=3.9`.
6. In a temporary Git repository under `/tmp`, exercise the workflow's guard
   logic for a matching `2.0.0` tag on `main`, a `1.0.0` tag/version mismatch,
   and a `2.0.0` tag on a commit not contained in `main`. Only the first case may
   pass.
7. Manually trace these events against job conditions and dependencies:
   pull-request update targeting `main`; push/merge to `main`; matching tag on
   `main`; malformed tag; matching tag outside `main`; failed lint; failed
   tests; missing credentials; duplicate version; anonymous verification
   failure.
8. Inspect workflow permissions and every secret reference, confirming secrets
   occur only on the authenticated upload step and are absent from pull-request,
   lint, test, and anonymous verification execution.
9. Run `python3 -m compileall thermocontrol tests` without leaving accepted
   generated files.
10. Run `git diff --check`.
11. Reconcile every modified, added, deleted, renamed, and untracked path with
    the approved expected-file list before staging.

The local host currently provides Python 3.12 rather than Python 3.9. The
workflow must explicitly use Python 3.9, but actual GitHub-hosted Python 3.9
execution cannot be claimed until a pull request, `main` push, or release tag
runs the workflow. Do not push a release tag or publish to Forgejo as part of
implementation. The first live tag and anonymous package round trip are
operator-owned. Their absence makes implementation delivery DRAFT even when all
local checks pass.

## Review and Fix Flow

1. The main agent inspects both developer diffs before integration.
2. R1 reviews the integrated diff without editing.
3. The main agent confirms or rejects each finding using the approved artifacts
   and current diff.
4. Route confirmed fixes to a new developer as F1 with exact file ownership.
5. Repeat focused review only for materially changed areas, then run full QA.
6. The main agent performs final acceptance and owns the final delivery state.

## Commit and Push Policy

1. After review, QA, documentation, and final acceptance, create and switch the
   detached worktree to branch `spec/forgejo-python-package-publishing`.
2. Reconcile the complete worktree with `git status`, preserve unrelated user
   changes, and stage every accepted in-scope modified, added, deleted, renamed,
   and untracked path, including the approved spec and plan.
3. Inspect `git diff --cached --check`, `git diff --cached --name-status`, and
   the full staged diff before committing.
4. Because GitHub-hosted Python 3.9 execution and a real Forgejo publish remain
   unverified, commit with `feature: DRAFT add Forgejo package publishing
   workflow`.
5. Push `spec/forgejo-python-package-publishing` to `origin`, configure its
   upstream, and verify the local branch is not ahead of the upstream.
6. Inspect final worktree status and do not report completion while any accepted
   in-scope change remains outside the commit.
7. Do not create a pull request, change GitHub repository settings, create or
   push a release tag, or publish a package unless the user separately requests
   those actions.

## Completion Report Requirements

Report the implemented CI and release behavior, review and QA issues found,
findings resolved, every validation run and not run, the missing live GitHub and
Forgejo evidence, documentation updates, changed-path reconciliation, commit and
push state, DRAFT status, skipped or operator-owned steps, Definition of Done
status, and final main-agent acceptance.
