# Environment-selected configuration overlay

Status: Approved

## Purpose

Allow an operator to select an additional YAML configuration file at runtime
without replacing the repository's built-in configuration files or requiring a
modified checkout.

## Problem

The runtime currently reads only the known configuration files under
`resources/`. An operator cannot point the service at a configuration file in
another location. Treating such a file as a complete replacement would also
force the operator to repeat every setting from the repository default, even
when only one value needs to differ.

## Scope

- Define `THERMOCONTROL_CONFIG_PATH` as the environment variable that selects
  one additional YAML configuration file.
- Apply the selected file as a partial overlay after the existing built-in
  configuration sequence.
- Report and reject an explicitly selected file that cannot be loaded or
  parsed.
- Document the environment variable, precedence, merge behavior, path
  handling, and startup-failure behavior.

## Out of scope

- Changing the names, order, or existing semantics of the built-in files under
  `resources/`.
- Supporting more than one environment-selected file.
- Adding environment variables for individual configuration values.
- Adding command-line configuration arguments, file watching, or runtime
  configuration reloads.
- Changing configuration keys, value validation, or code defaults.

## Definitions

- **Built-in configuration sequence:** The existing ordered lookup of
  `resources/config.yaml`, `resources/config.yml`,
  `resources/config.local.yaml`, and `resources/config.local.yml`.
- **Selected file:** The single file identified by the non-empty value of
  `THERMOCONTROL_CONFIG_PATH`.
- **Partial overlay:** Applying only configuration fields present in the
  selected file. A field omitted from that file retains the value established
  by the built-in configuration sequence or, when no built-in file established
  it, its code default.

## Inputs and constraints

- `THERMOCONTROL_CONFIG_PATH` is optional.
- An unset or empty `THERMOCONTROL_CONFIG_PATH` means that no selected file is
  requested and preserves current runtime behavior.
- A non-empty value is interpreted as one filesystem path. An absolute path is
  used directly; a relative path is resolved using the process working
  directory.
- The selected file uses the same YAML configuration structure, supported
  keys, and value validation as the built-in configuration files.
- The selected YAML document must be empty or a mapping. An empty document is a
  valid no-op overlay. A non-mapping document is invalid configuration.

## Deterministic behavior

1. The runtime processes the built-in configuration sequence with its existing
   behavior.
2. If `THERMOCONTROL_CONFIG_PATH` is unset or empty, configuration loading ends
   after the built-in sequence.
3. If `THERMOCONTROL_CONFIG_PATH` contains a non-empty value, the runtime loads
   that selected file after every built-in file, giving it highest
   configuration precedence.
4. Fields present in the selected file replace the corresponding values in the
   configuration state produced by the built-in sequence.
5. Fields absent from the selected file do not reset or otherwise change the
   already established values. This preservation applies at every supported
   nested level; for example, specifying only
   `thermocontrol.ai_module.temperature_threshold` preserves all other
   `thermocontrol` and `ai_module` values.
6. An empty selected YAML document succeeds without changing configuration.
7. If the environment variable is non-empty but its path does not identify a
   readable regular file, YAML parsing fails, the document root is not a
   mapping, or existing value validation fails, startup fails through the
   runtime's existing error path and logs the cause. The service does not start
   with a silently ignored or partially accepted selected file.
8. Loading a selected file is logged consistently with configuration-file
   loading, without logging file contents.

## Assumptions

- Highest precedence is required so deployment-specific configuration can
  override both repository defaults and local built-in overrides.
- An explicitly selected but unusable file represents operator error and must
  fail closed.
- Existing built-in file behavior remains compatibility-sensitive even though
  an omitted key in a later built-in file currently resets that value to its
  code default; only the selected file receives partial-overlay semantics.
- Environment access and path selection are runtime/infrastructure concerns and
  must not create an outward dependency from the domain layer.

## Regression impact

- Runs that do not set `THERMOCONTROL_CONFIG_PATH` must retain the current file
  lookup, precedence, defaults, and startup behavior.
- The existing `GPIOZERO_PIN_FACTORY` runtime environment behavior is
  unaffected.
- Temperature decisions, GPIO behavior, graceful shutdown, logging targets,
  packaging, and release behavior are unaffected after configuration has been
  resolved.
- Existing invalid-value checks apply equally to values supplied by the
  selected file.

## Validation plan

This change affects presentation/infrastructure configuration loading rather
than deterministic domain source logic. Under the repository's domain-only test
policy, no automated tests will be added or maintained for it, including the
legacy infrastructure parser tests.

Validation will cover:

- Python 3.9-compatible compilation and linting.
- Static inspection of environment-variable selection, load order, and
  preservation of existing behavior when the variable is absent or empty.
- Targeted manual smoke checks using temporary YAML files for a one-field
  nested overlay, an empty overlay, relative and absolute paths, missing and
  unreadable paths, malformed YAML, a non-mapping document, and an invalid
  configured value.
- Confirmation that the selected file is processed after all built-in files and
  that omitted selected-file fields preserve previously loaded values.
- `git diff --check` and relevant package build checks.

No Raspberry Pi GPIO behavior, hosted CI, or deployed service behavior may be
claimed as validated without the corresponding live environment.

## Documentation needs

Update `README.md` to document:

- `THERMOCONTROL_CONFIG_PATH` and examples using absolute and relative paths.
- The selected file's highest precedence.
- Partial-overlay behavior, including nested omitted-field preservation.
- Unset and empty-variable behavior.
- Fail-fast behavior for an explicitly selected unusable or invalid file.
