# AGENTS

## Active Spec
- `docs/specs/fan-temperature-moving-average.md`

## Branch
- `spec/fan-temperature-moving-average`

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
