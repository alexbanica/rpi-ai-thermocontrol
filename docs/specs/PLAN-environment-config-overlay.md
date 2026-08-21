# Environment-selected configuration overlay implementation plan

Status: Approved

## Approved specification

- `docs/specs/SPEC-environment-config-overlay.md`
- Status required at implementation start: `Approved`

Implementation must deliver only the behavior defined by that specification.
If the current code, refreshed base, or implementation evidence contradicts the
approved behavior or this plan, stop and request an artifact amendment rather
than broadening or reinterpreting the work.

## Delivery configuration

- Repository: `rpi-ai-thermocontrol`
- Delivery branch: `feature/environment-config-overlay`
- Expected base: a successfully refreshed `origin/main` fetched during the
  implementation run
- Implementation mode: isolated linked worktree
- Task slug: `environment-config-overlay`
- Worktree path:
  `~/.herdr/worktrees/rpi-ai-thermocontrol/environment-config-overlay`
- Delivery default: commit and push every accepted in-scope change, including
  the exact approved specification and plan
- Suggested commit subject: `feature: add environment config overlay`

The implementation command must run in a fresh session, after context is
cleared, or after the user explicitly confirms same-context implementation.

## Context and worktree preparation

The main agent must perform all branch and worktree management. Workers must not
create or manage worktrees or branches, commit, or push.

1. Load only applicable instructions, these approved artifacts, current branch
   and worktree state, the files listed in this plan, and minimal local edit
   patterns. Do not repeat product, architecture, scope, or plan research.
2. Confirm the invoking checkout and classify its complete `git status`,
   preserving unrelated user changes.
3. Record the exact paths, contents, index state, and state relative to the
   invoking checkout's `HEAD` for:
   - `docs/specs/SPEC-environment-config-overlay.md`
   - `docs/specs/PLAN-environment-config-overlay.md`
4. Create the repository-specific directory under
   `~/.herdr/worktrees/rpi-ai-thermocontrol/` if absent, and verify the resolved
   repository name and task path.
5. Successfully fetch `origin/main` during the implementation run. Do not
   update or switch the invoking checkout's local `main`.
6. Create the planned worktree detached at the refreshed `origin/main`. A
   reusable worktree must first be clean and detached, then moved to that same
   refreshed commit.
7. Verify the worktree `HEAD` exactly equals refreshed `origin/main` and that
   its path and repository identity match this plan before making edits.
8. Transfer the exact approved spec and plan into the worktree and verify their
   contents match the recorded source copies. Retain the invoking-checkout
   copies as recovery material until remote delivery is verified.

Any base mismatch, dirty reusable worktree, attached branch, conflicting branch
name, artifact mismatch, changed source artifact, or unsafe path state is a hard
stop.

## Affected files and ownership

- `thermocontrol/shared/constants.py`: declare the runtime environment-variable
  name as a shared value without introducing environment access into domain
  code.
- `thermocontrol/infrastructure/parsers/yaml_config_parser.py`: support an
  explicitly selected absolute or relative file and partial-overlay parsing
  that preserves omitted fields while retaining current built-in parsing
  semantics.
- `thermocontrol/presentation/controllers/runtime_controller.py`: read the
  optional environment variable, preserve absent/empty behavior, and request
  the selected overlay after the complete built-in sequence.
- `README.md`: document the environment variable, path resolution, precedence,
  merge rules, error behavior, and examples.
- `docs/specs/SPEC-environment-config-overlay.md`: approved behavior artifact.
- `docs/specs/PLAN-environment-config-overlay.md`: approved execution artifact.

No domain files, tests, packaging metadata, dependency files, CI workflows, or
repository default configuration are expected to change. If one proves
necessary, stop for plan amendment.

## Test-first applicability

Automated test-first work is not applicable. The behavior belongs to
presentation and infrastructure configuration loading, and the project policy
forbids creating or maintaining automated tests outside deterministic domain
source logic. Existing legacy parser tests must not be edited. Validation uses
lint, compilation, package build, static inspection, and deterministic manual
smoke commands instead.

## Dependency-aware execution graph

### D1 - Selected-file partial overlay

- Type: development
- Boundary: infrastructure parsing of one explicitly requested file, including
  readable regular-file enforcement, YAML mapping validation, no-op empty YAML,
  existing value validation, and preservation of every omitted supported field
- Owned file:
  `thermocontrol/infrastructure/parsers/yaml_config_parser.py`
- Dependencies: approved artifacts transferred; worktree verified at exact base
- Assignment: one clean-context `developer` subagent, scoped only to the owned
  file and approved selected-file parsing behavior, for at most 5 minutes of
  active work
- Acceptance criteria:
  - Existing built-in sequence behavior remains unchanged.
  - Selected-file parsing uses the same supported keys and validation.
  - Empty YAML is a successful no-op.
  - Missing, non-file, unreadable, malformed, non-mapping, and invalid-value
    inputs raise rather than being silently skipped.
  - Omitted top-level and nested fields preserve their pre-overlay values.
- Validation: targeted compilation and developer-reported manual calls that
  exercise parser behavior without adding tests

### D2 - Runtime environment selection and precedence

- Type: development
- Boundary: environment-variable constant and presentation wiring that invokes
  the selected overlay after all built-in files
- Owned files:
  - `thermocontrol/shared/constants.py`
  - `thermocontrol/presentation/controllers/runtime_controller.py`
- Dependencies: D1 complete, so runtime wiring targets the finalized parser
  boundary
- Assignment: one clean-context `developer` subagent, scoped only to the owned
  files and approved runtime selection behavior, for at most 5 minutes of active
  work
- Acceptance criteria:
  - The exact variable name is `THERMOCONTROL_CONFIG_PATH`.
  - Unset and empty values perform no selected-file load.
  - A non-empty value is processed once, after the complete existing built-in
    sequence.
  - Relative paths retain process-working-directory semantics; absolute paths
    are accepted.
  - Selected-file failures reach the existing startup error path and prevent
    service startup.
  - Domain code does not access the environment or depend outward.
- Validation: targeted compilation plus static call-order and error-flow
  inspection

### D3 - Operator documentation

- Type: development/documentation
- Boundary: configuration and run guidance for the approved environment overlay
- Owned file: `README.md`
- Dependencies: D1 and D2 complete, so documentation reflects the final
  implemented interface
- Assignment: one clean-context `developer` subagent, scoped only to the owned
  file and approved documentation needs, for at most 5 minutes of active work
- Acceptance criteria:
  - Documents the exact variable name and both absolute and relative examples.
  - States that the selected file loads last and has highest precedence.
  - Explains nested partial-overlay preservation with an example.
  - States unset/empty behavior and fail-fast invalid-path/configuration
    behavior.
  - Does not claim live Raspberry Pi or deployed-runtime validation.
- Validation: main-agent comparison against the approved spec and implemented
  interface

### R1 - Independent implementation review

- Type: review
- Boundary: complete in-scope diff against the approved specification and plan
- Owned files: read-only review of every affected file and both artifacts
- Dependencies: D1, D2, and D3 complete; main agent has integrated the diff
- Assignment: one clean-context `code-reviewer` subagent for at most 5 minutes
  of active review; it must not implement fixes
- Acceptance criteria:
  - Reports spec and plan mismatches, precedence or merge defects, error-path
    gaps, architecture violations, missing documentation, regression risks, and
    prohibited test changes.
  - Distinguishes blocking findings from residual risks.
- Validation: main agent verifies every finding against code and artifacts

### F1 - Review and QA fixes, only if required

- Type: development
- Boundary: one narrowly scoped, verified R1 or main-agent QA finding at a time
- Owned files: only the file or non-overlapping file set explicitly assigned for
  that finding
- Dependencies: relevant finding accepted by the main agent
- Assignment: a new clean-context `developer` subagent per non-overlapping fix,
  each for at most 5 minutes; do not return fixes to the review agent
- Acceptance criteria: the assigned finding is resolved without widening the
  approved scope or overwriting another unit
- Validation: rerun the finding-specific check and all affected final checks

## Concurrency and integration

- Maximum planned test-writer concurrency: 0; prohibited non-domain test work
  is not assigned.
- Maximum planned developer concurrency: 1. D1, D2, and D3 are intentionally
  serialized because D2 depends on D1's parser boundary and D3 must document
  the integrated interface.
- Maximum planned code-reviewer concurrency: 1.
- The main agent supervises the graph and the 5-minute active-work limit. At the
  limit it must interrupt the subagent, record completed and partial work,
  changed files, validation, blockers, and remaining work, inspect and preserve
  usable changes, then split the remainder into smaller non-overlapping units
  before assigning a clean-context replacement.
- `yaml_config_parser.py` is the parser integration point; only D1 may edit it.
  `runtime_controller.py` and `constants.py` are owned only by D2. `README.md`
  is owned only by D3. The main agent alone reconciles cross-unit behavior,
  stages accepted work, and resolves integration issues.

## Main-agent QA and validation

After development and independent review, the main agent owns QA and must:

1. Reconcile every modified, added, deleted, renamed, and untracked path and
   classify it as accepted in scope or preserved unrelated work.
2. Inspect the complete diff and confirm no domain, test, packaging,
   dependency, workflow, or default-config changes occurred.
3. Run `ruff check .`.
4. Run Python compilation with the available Python 3.9 baseline; if Python 3.9
   is unavailable, record that limitation and run the closest available Python
   compilation without claiming baseline validation.
5. Build the package using the repository's `setup.py` build entrypoint in an
   isolated temporary output location, without retaining generated artifacts in
   the repository.
6. Run targeted manual smoke checks using temporary files and direct parser or
   controller-boundary invocations, without adding automated test files:
   - variable unset and empty;
   - absolute and relative selected paths;
   - a one-field nested overlay preserving every omitted configured value;
   - an empty YAML overlay;
   - missing path and directory path;
   - unreadable file where permissions permit a meaningful check;
   - malformed YAML and non-mapping YAML;
   - invalid `temperature_average_read_count`.
7. Confirm by inspection and smoke evidence that the selected overlay is
   applied after all four built-in candidates and that built-in behavior is
   unchanged when no selected file is requested.
8. Run `git diff --check` before staging and against the staged change.
9. Do not run or modify automated tests for this non-domain change. Existing CI
   may still execute legacy tests, but that does not authorize maintaining them.
10. Record any unavailable Python 3.9 environment, unreadable-file limitation,
    Raspberry Pi runtime, GPIO, deployed process, hosted CI, or Forgejo checks as
    unvalidated. Mark delivery DRAFT if an unvalidated risk prevents the
    Definition of Done.

## Commit, push, and cleanup

After development reaches the Definition of Done or an explicitly reported
DRAFT boundary, the main agent must:

1. Create `feature/environment-config-overlay` in the implementation worktree
   at its verified base. Do not create the branch earlier.
2. Reconcile final `git status`, preserve unrelated changes, and stage every
   accepted in-scope path, including the exact approved artifacts.
3. Inspect the staged path list and staged diff, confirming no accepted path is
   omitted and no unrelated path is included.
4. Commit the complete accepted set using the repository convention and include
   `DRAFT` in the subject when required validation, review, QA, or documentation
   remains skipped, blocked, incomplete, or failing.
5. Inspect post-commit status and ensure no accepted in-scope change remains
   outside the commit.
6. Push the exact delivery branch to `origin`, configure its upstream as
   needed, and verify the local branch is not ahead of its upstream.
7. Verify the remote-tracking branch resolves to the delivery commit and that
   the pushed commit contains the exact approved spec and plan contents.
8. Detach the implementation worktree at the pushed delivery commit and verify
   `feature/environment-config-overlay` is no longer attached to any worktree.
   Keep the linked worktree registered.
9. Only after successful push, artifact verification, and detachment, compare
   the invoking-checkout artifact paths and index entries with their recorded
   post-planning state. If unchanged, restore only those exact paths and index
   entries to the invoking checkout's `HEAD` state, removing newly generated
   artifacts or planning-only changes while preserving any version already in
   that checkout's `HEAD`.
10. If remote verification, detachment, artifact verification, or safe cleanup
    fails, stop, preserve the remaining copies, and report DRAFT. Never clean
    unrelated paths or overwrite artifact content changed after transfer.

## Completion report requirements

Report the implemented specification, review and QA issues, resolved findings,
validation run and not run, remaining risks, documentation changes, exact
commit and push status, upstream synchronization, implementation-worktree
detachment, invoking-checkout artifact cleanup, skipped or blocked Definition
of Done items, final versus DRAFT delivery, and final main-agent acceptance.
