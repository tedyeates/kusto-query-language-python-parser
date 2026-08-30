# Building & Deploying to PyPI

The package is published manually with `build` + `twine` (both already in `.venv`).
There is no release CI; every step below runs locally.

## Checklist before a release

1. The fix/change is merged to `main` — never release from a feature branch.
2. Version in `pyproject.toml` is bumped (e.g. `0.1.0` → `0.1.1`). PyPI rejects
   re-uploads of an existing version, so the version must never repeat.
3. Runtime dependencies are declared under `[project] dependencies` (not just
   `[build-system]`) — otherwise `pip install` gives users a broken package.
   Current runtime dependency: `antlr4-python3-runtime==4.13.2`, which must match
   the ANTLR version used to generate `parse_tools/` (see [grammar.md](grammar.md)).

## Build

```bash
rm -rf dist && .venv/bin/python -m build
```

Produces both artifacts in `dist/`:

- `kusto_query_language_parser-<version>-py3-none-any.whl`
- `kusto_query_language_parser-<version>.tar.gz`

Always `rm -rf dist` first — stale artifacts from a previous version cause
confusing upload failures or, worse, shipping old code.

## Verify locally (as a PyPI user would see it)

Install the wheel into a throwaway venv and run the example and tests:

```bash
python3.14 -m venv /tmp/venv-test
/tmp/venv-test/bin/pip install dist/*.whl
/tmp/venv-test/bin/python examples/example.py
.venv/bin/pytest
```

This catches packaging bugs that don't show up in the dev venv (e.g. missing
dependency declarations, stale artifacts).

## Upload

```bash
.venv/bin/twine upload dist/*
```

- Username: `__token__` (twine's token prompt handles this automatically).
- Password: an API token from pypi.org → Account settings → API tokens
  (starts with `pypi-`).
- The warning `This environment is not supported for trusted publishing` is
  benign — trusted publishing is a CI-only (GitHub Actions OIDC) feature and
  token auth is fully supported for local uploads.

## After publishing

Optionally tag the release so the repo matches PyPI:

```bash
git tag v<version> && git push --tags
```

Check the result at https://pypi.org/project/kusto-query_language_parser/
