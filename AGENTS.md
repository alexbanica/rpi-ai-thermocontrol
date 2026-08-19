# AGENTS

## Domain-only test policy

- Automated tests of any kind, including unit, integration, contract, snapshot,
  workflow, and configuration tests, may be created or maintained only for
  deterministic domain source logic in this project.
- Do not create or maintain tests for anything outside domain source logic,
  including application orchestration, infrastructure and adapters,
  presentation, UI and controllers, Docker or container files, GitHub Actions
  or other CI/CD workflows, deployment and configuration, packaging and release
  scripts, tooling, or other operational code.
- Validate non-domain changes with appropriate static, syntax, lint, type,
  structural, build, dry-run, smoke, runtime, or operator checks instead of
  automated tests.
- If this project has no domain source logic, automated testing and test-first
  work are not applicable.
- This policy supersedes any more general testing or validation wording
  elsewhere in this file.

## Active Spec
- `docs/specs/forgejo-python-package-publishing.md`

## Branch
- `spec/forgejo-python-package-publishing`

## Architecture Rules
- DDD/onion split:
- `thermocontrol/domain`: entities and domain service contracts for temperature and fan control.
- `thermocontrol/application`: use-case orchestration for reading temperature and toggling fan state.
- `thermocontrol/infrastructure`: YAML parsing, platform temperature readers, and GPIO fan adapters.
- `thermocontrol/presentation`: runtime controller and module entrypoint.
- `thermocontrol/shared`: constants and shared values only.
- Dependencies point inward: presentation and infrastructure may depend on application/domain contracts, but domain must not depend on infrastructure, presentation, GPIO, hwmon, YAML, or process-runtime details.
- Interfaces are named with `Interface` suffix.
- Abstract classes are prefixed with `Abstract`.
- Implementations of abstract classes remove the `Abstract` prefix and keep the remaining name.
- Service implementations match interface names without suffix.
- Legacy module paths were removed intentionally.

## Project-Specific Architecture
- `thermocontrol/domain/entities`: fan and temperature state entities.
- `thermocontrol/domain/services`: domain-facing contracts.
- `thermocontrol/application/services`: deterministic fan-control use cases.
- `thermocontrol/infrastructure/parsers`: configuration and raw hardware data parsing.
- `thermocontrol/infrastructure/services`: concrete GPIO, hwmon, and runtime adapters.
- `thermocontrol/presentation/controllers`: process/runtime coordination.
- `resources/config.yml` is the default runtime configuration.
- `tests/` contains unit coverage for service and parser behavior.

## Packaging Rules
- `setup.py` remains for package install metadata.
- `requirements.txt` + `requirements.dev.txt` + `requirements/*.txt` are dependency install flows.

## HTTP/OpenAPI
- No HTTP controllers in this project.
- No swagger/openapi or `.http` artifacts are required for this spec.
