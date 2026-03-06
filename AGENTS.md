# AGENTS

## Active Spec
- `docs/specs/fan-toggle-temperature-logging.md`

## Branch
- `spec/fan-toggle-temperature-logging`

## Architecture Rules
- DDD/onion split:
- `thermocontrol/domain`
- `thermocontrol/application`
- `thermocontrol/infrastructure`
- `thermocontrol/presentation`
- `thermocontrol/shared`
- Interfaces are named with `Interface` suffix.
- Service implementations match interface names without suffix.
- Legacy module paths were removed intentionally.

## Packaging Rules
- `setup.py` remains for package install metadata.
- `requirements.txt` + `requirements.dev.txt` + `requirements/*.txt` are dependency install flows.

## HTTP/OpenAPI
- No HTTP controllers in this project.
- No swagger/openapi or `.http` artifacts are required for this spec.
