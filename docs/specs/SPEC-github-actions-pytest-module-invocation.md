# GitHub Actions pytest module invocation

Status: Approved

## Purpose

Restore the GitHub Actions test job by making the repository package importable
when tests execute on the configured Python 3.9 runner.

## Requested behavior

The `Tests` job in `.github/workflows/ci-publish.yml` invokes pytest through the
Python interpreter: `python -m pytest`.

## Scope

- Update only the test-command invocation in the CI workflow.
- Preserve the Python 3.9 runtime, dependency installation, and existing test
  collection behavior.

## Out of scope

- Application, test, dependency, packaging, lint, and publishing behavior.
- Hosted CI execution, commits, and pushes.

## Inputs and constraints

The workflow installs development dependencies but does not install the local
package. The test command must therefore run in a way that includes the
repository checkout on Python's module search path.

## Deterministic behavior delivered

Using `python -m pytest` executes the existing pytest suite in the configured
interpreter and includes the checkout directory on `sys.path`, allowing imports
from `thermocontrol` during collection.

## Assumptions and impact

This relies on Python's standard module execution behavior. It changes no test
selection, test code, package contents, or production runtime behavior.

## Validation performed

- Inspected failed GitHub Actions job `95397699898`; it reported three
  `ModuleNotFoundError: No module named 'thermocontrol'` collection errors.
- Parsed the workflow and verified the replacement command is valid Python
  module syntax.

## Validation skipped

The local checkout has no pytest installation, and dependency installation plus
the complete suite were skipped because `$super-agent` limits validation to
commands expected to finish within ten seconds. Hosted Actions rerun is not
performed by this invocation.

## Documentation changes

This completed-work specification records the scoped CI repair.
