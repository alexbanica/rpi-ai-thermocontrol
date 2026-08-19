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
- Existing tests outside the domain layer are legacy coverage; their presence
  does not authorize additions or maintenance outside the domain-only boundary.
- Validate non-domain changes with appropriate static, syntax, lint, type,
  structural, build, dry-run, smoke, runtime, or operator checks instead of
  automated tests.
- If this project has no domain source logic, automated testing and test-first
  work are not applicable.
- This policy supersedes more general testing or validation wording elsewhere
  in repository or workspace instructions.

## Architecture

The repository uses a DDD/onion split:

- `thermocontrol/domain/entities`: runtime configuration state.
- `thermocontrol/domain/services`: domain-facing contracts for configuration,
  temperature input, and fan output.
- `thermocontrol/application/services`: fan-control use-case orchestration.
- `thermocontrol/infrastructure/parsers`: YAML configuration parsing.
- `thermocontrol/infrastructure/services`: concrete hwmon temperature and GPIO
  fan adapters, including graceful-shutdown `pinctrl` handling.
- `thermocontrol/presentation/controllers`: dependency wiring, logging, and
  process coordination.
- `thermocontrol/shared`: constants and shared values only.

Dependencies point inward. Domain code must not depend on infrastructure,
presentation, GPIO, hwmon, YAML, subprocesses, or process-runtime details.

## Naming and compatibility rules

- Interfaces use the `Interface` suffix.
- Abstract classes use the `Abstract` prefix.
- Concrete implementations remove `Abstract` and retain the remaining name.
- Service implementations match their interface name without the `Interface`
  suffix.
- Legacy module paths were removed intentionally; do not restore compatibility
  aliases without an approved behavior change.
- Python 3.9 is the lint, test, and package-build baseline.

## Runtime contracts

- `python -m thermocontrol` is the module entrypoint.
- Runtime configuration is read from `resources/` in this order:
  `config.yaml`, `config.yml`, `config.local.yaml`, and `config.local.yml`.
  Each discovered file is parsed in sequence; later values replace earlier
  values, and omitted keys in that later file reset to code defaults.
- `resources/config.yml` is the repository default configuration.
- Temperature input is read from
  `/sys/class/hwmon/<configured name>/temp1_input`; configured names are tried
  in comma-separated order.
- Fan decisions use a sliding window of valid readings. The fan remains off
  until the window is full, uses `average >= threshold` to enable, and is
  requested off immediately when all temperature reads fail.
- Graceful shutdown drives the fan low, closes GPIO Zero and its pin factory,
  then runs `pinctrl <gpio> op dl`. Missing `pinctrl` or command failure is
  logged and does not block shutdown.
- Persistent fan-off state is not guaranteed after abrupt termination, reboot,
  or external GPIO reconfiguration. Do not claim physical fail-safe behavior
  without live hardware validation.
- Logs go to stderr and `/var/log/rpi-ai-thermocontrol.log`; file logs rotate at
  midnight with five backups.
- There are no HTTP controllers, OpenAPI contracts, or `.http` artifacts.

## Packaging and release

- `setup.py` remains the package metadata and build entrypoint.
- `requirements.txt`, `requirements.dev.txt`, and `requirements/*.txt` are the
  dependency installation flows.
- The package supports Python 3.9 or newer; CI and release workflows currently
  exercise Python 3.9.
- CI checks are `Lint` and `Tests` from `.github/workflows/ci.yml`.
- `.github/workflows/publish.yml` accepts exact unprefixed `X.Y.Z` and
  `X.Y.Z-betaN` tags. Beta tags map to PEP 440 `X.Y.ZbN` package versions.
- Publishing uses the Forgejo public PyPI endpoint. Anonymous installation uses
  Forgejo as the primary index and public PyPI as the additional dependency
  index.
- The publish workflow does not enforce `main` ancestry. Release-tag trust and
  branch/check protection remain operator-owned controls.
- GitHub Actions changes must be validated structurally and syntactically, not
  with automated workflow tests.

## Documentation and validation boundaries

- Keep `README.md` aligned with actual configuration lookup, runtime behavior,
  platform requirements, graceful-shutdown limitations, and release workflow.
- Automated test-first work is not applicable to documentation, infrastructure,
  presentation, CI/CD, packaging, configuration, or operational changes.
- Use `ruff check .`, Python compilation, build checks, YAML parsing, workflow
  inspection, `git diff --check`, and targeted smoke or operator validation as
  appropriate to the changed non-domain scope.
- Do not claim Raspberry Pi GPIO behavior, fan state, permissions, hosted CI,
  or Forgejo publication as validated without observing the corresponding live
  environment.
