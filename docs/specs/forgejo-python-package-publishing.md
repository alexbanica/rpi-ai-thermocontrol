# Spec: Forgejo Python Package Publishing

Status: Approved

## Purpose

Add a GitHub Actions release and continuous-integration contract that validates
pull requests and changes merged to the default branch, then publishes trusted
version tags as publicly readable Python packages in the Forgejo package
registry.

## Problem

The repository currently has no GitHub Actions workflows. Pull requests and
default-branch updates therefore have no automated lint or test result, and a
pushed release tag does not build or publish `rpi-ai-thermocontrol` to Forgejo.
Publishing also needs deterministic version, authentication, provenance, and
public-read checks so a tag cannot silently produce the wrong package version or
an inaccessible package.

## Scope

- Run lint and unit tests for pull requests targeting the repository's default
  branch.
- Run lint and unit tests after changes are pushed or merged to the default
  branch.
- Run the same lint and unit-test gates for a supported release tag before any
  package publication.
- Build both a source distribution and a wheel from the tagged revision.
- Publish the distributions to the Forgejo `public` organization PyPI registry.
- Verify after publication that the exact released version is anonymously
  downloadable from the public Forgejo PyPI index.
- Document the release tag contract, GitHub secrets, public install command,
  immutable-version behavior, and required GitHub branch/tag protections.

## Out of Scope

- Publishing to pypi.org, TestPyPI, GitHub Packages, or another registry.
- Publishing from a branch push, pull request, manual dispatch, schedule, or
  GitHub release event.
- Automatically creating Git tags or GitHub releases.
- Automatically changing the package version stored in package metadata.
- Publishing a prerelease, development release, or tag with a `v` prefix.
- Changing application runtime behavior, dependencies, architecture, or
  hardware integration.
- Migrating package metadata away from the repository's required `setup.py`
  flow.
- Configuring Forgejo instance visibility, organization membership, or GitHub
  branch/tag rules through repository code.
- Retrospectively publishing tags that existed before the workflow was present.

## Definitions

- **Default branch:** `main`, which is the current branch referenced by
  `origin/HEAD`. The request's reference to `master` means this repository's
  actual default branch; no `master` branch is introduced.
- **Pull-request validation:** Validation of a `pull_request` whose base branch
  is `main`.
- **Merged-change validation:** Validation of a push to `main`, including the
  push produced when a pull request is merged.
- **Supported release tag:** A pushed, unprefixed stable version tag containing
  exactly three numeric components in `MAJOR.MINOR.PATCH` form, such as
  `2.0.0`.
- **Package version:** The canonical version declared by the package metadata at
  the tagged revision.
- **Public package:** A package owned by the Forgejo `public` organization and
  retrievable from its PyPI-compatible simple index without credentials.
- **Validation gates:** Separate, stable lint and unit-test results that must
  both succeed for their triggering revision.

## Inputs and Constraints

- The source repository remains GitHub
  `alexbanica/rpi-ai-thermocontrol`, and GitHub Actions is the workflow runtime.
- The default branch is `main`.
- The package name remains `rpi-ai-thermocontrol`.
- The package metadata remains sourced from `setup.py`; it currently declares
  version `2.0.0` and Python `>=3.9`.
- The lint command is `ruff check .`.
- The unit-test command is `pytest`.
- Validation must exercise Python 3.9, the minimum version declared by the
  package.
- The Forgejo upload endpoint is
  `https://forgejo.alexlab.nl/api/packages/public/pypi`.
- The anonymous package index is
  `https://forgejo.alexlab.nl/api/packages/public/pypi/simple`.
- Publishing authentication is supplied only to the publish operation through
  GitHub Actions secrets:
  - `FORGEJO_PACKAGE_USERNAME`: the Forgejo user or service-account name.
  - `FORGEJO_PACKAGE_TOKEN`: a token authorized to write packages owned by the
    public organization and restricted to public resources with the minimum
    practical package-write permission.
- Credentials, authenticated URLs, and token values must never be committed,
  printed, embedded in built artifacts, or made available to pull-request
  validation.
- TLS verification must remain enabled for every Forgejo request. No insecure
  certificate, hostname, or transport bypass is allowed.
- GitHub workflow permissions must be read-only unless a narrower step
  demonstrably requires more. Forgejo publication uses the Forgejo credentials,
  not GitHub package-write permission.
- Forgejo package versions are immutable. An existing package name and version
  must not be overwritten or skipped as success.

## Deterministic Behavior

### Pull Requests

1. Opening, updating, or reopening a pull request targeting `main` runs both
   validation gates.
2. Lint succeeds only when `ruff check .` exits successfully.
3. Unit tests succeed only when `pytest` exits successfully.
4. A failure or cancellation in either gate makes the workflow unsuccessful.
5. No package is built for publication, no Forgejo credentials are exposed, and
   no Forgejo package is published from a pull-request event.

### Pushes and Merges to the Default Branch

1. Every push to `main`, including a pull-request merge result, runs both
   validation gates against the resulting commit.
2. Success and failure use the same commands and criteria as pull-request
   validation.
3. A normal push to `main` never publishes a package unless the same commit is
   separately pushed as a supported release tag.

### Release Tags

1. Pushing a supported release tag runs both validation gates against the exact
   tagged revision.
2. The tag's target commit must be contained in `main`. A tag targeting an
   unmerged commit must fail without publishing.
3. The tag text must exactly equal the package version declared by the tagged
   revision. Version normalization, automatic rewriting, a leading `v`, and
   tag-to-metadata mismatch are not accepted.
4. Package build and publication may begin only after both validation gates
   succeed.
5. The release build produces one source distribution and one wheel for
   `rpi-ai-thermocontrol` from the tagged revision.
6. Both distributions must pass package metadata and archive checks before
   upload.
7. The checked distributions are uploaded with authenticated TLS to the fixed
   Forgejo `public` organization endpoint.
8. Missing credentials, invalid credentials, unavailable Forgejo service,
   certificate failure, version collision, build failure, or upload failure
   makes the release unsuccessful; none may be reported as success.
9. After upload, the exact package version must be downloadable from the public
   Forgejo simple index without authentication and without resolving its runtime
   dependencies. Failure of this anonymous check makes the release
   unsuccessful.
10. Tags that do not match the supported release-tag format do not invoke the
    release workflow and do not publish a package.

## Invariants

- No release can publish unless lint and unit tests passed for the same tagged
  revision.
- Pull-request code cannot access Forgejo publish credentials.
- Branch-only activity cannot publish a package.
- The Git tag, package metadata version, uploaded version, and anonymously
  downloaded verification version are identical.
- The published package comes from the immutable tagged Git revision rather
  than a later branch head.
- A duplicate version fails instead of replacing an existing package.
- The public verification is credential-free and therefore tests public read
  access rather than authenticated maintainer access.
- Application behavior and package contents are unchanged by this spec. If the
  existing package cannot build or install correctly, that is a blocker that
  requires an explicitly approved spec amendment rather than an inferred
  packaging change.

## Assumptions

- The `public` Forgejo organization is public, its package registry is enabled,
  and the Forgejo instance permits anonymous reads of public packages.
- The publishing user is a member of the `public` organization with sufficient
  package-write access.
- GitHub-hosted runners can resolve and reach `forgejo.alexlab.nl` over trusted
  HTTPS.
- Stable releases intentionally use unprefixed tags such as the existing
  `1.0.0` tag.
- Maintainers update the version in `setup.py` before creating the matching
  release tag.
- GitHub branch protection or a ruleset will require the stable lint and test
  checks before merging to `main`; workflow code exposes the checks but cannot
  itself configure repository protection.
- A GitHub tag ruleset or equivalent maintainer policy prevents untrusted users
  from creating or moving release tags.

## Regression Impact

Potential regressions include CI installing incomplete dependencies, checks
running against the wrong event or branch, tag builds using a branch head,
publishing before validation finishes, accepting a mismatched tag and package
version, leaking publish credentials to pull requests or logs, weakening TLS,
overwriting an immutable version, or claiming public availability after only an
authenticated check.

Regression safety requires event-filter validation, local execution of the exact
lint and test commands, workflow syntax inspection, tag/version mismatch and
non-main-tag failure checks, distribution build and metadata inspection, secret
scope review, and a first-release live publish/download round trip.

## Validation Plan

- Run `ruff check .` using Python 3.9-compatible dependencies.
- Run the complete `pytest` suite using Python 3.9-compatible dependencies.
- Validate the GitHub Actions workflow syntax and inspect its effective event
  filters for pull requests to `main`, pushes to `main`, and supported release
  tags.
- Build the source distribution and wheel from the repository package metadata.
- Check both built distributions with the standard Python package upload
  validation tool.
- Inspect distribution metadata to confirm the package name, declared Python
  requirement, and version.
- Exercise release guard logic for a matching tag, a tag/version mismatch, and a
  tag whose commit is not contained in `main` without publishing.
- Confirm publish credentials exist only in the tag-only publish operation and
  that workflow/job permissions are least privilege.
- Run `git diff --check`.
- For the first new release tag, observe successful GitHub Actions lint, test,
  build, upload, and anonymous exact-version download evidence. Until this live
  round trip succeeds, delivery remains DRAFT.

## Documentation Needs

- Add a release section to `README.md` documenting:
  - the `MAJOR.MINOR.PATCH` tag format and exact metadata-version match;
  - the `main` ancestry requirement;
  - required GitHub Actions secret names without secret values;
  - the fixed Forgejo public upload and install endpoints;
  - an anonymous exact-version `pip` installation example;
  - immutable-version and duplicate-publish failure behavior;
  - the first-release live-validation boundary.
- Document the required GitHub branch protection or ruleset for the lint and
  unit-test checks and the trusted-maintainer tag policy as operator-owned setup.

## External Contract References

- Forgejo PyPI registry upload and install contract:
  <https://forgejo.org/docs/latest/user/packages/pypi/>
- Forgejo package ownership and public-read rules:
  <https://forgejo.org/docs/latest/user/packages/>
- GitHub Actions branch and tag filters:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- Python distribution build and upload flow:
  <https://packaging.python.org/en/latest/flow/>
