# Grammar & Parser Regeneration

## Source of truth

The KQL grammar is **not** maintained in this repo. It is sourced from Microsoft's
[`Kusto-Query-Language`](https://github.com/microsoft/Kusto-Query-Language) repository:

| File | Upstream URL |
|------|--------------|
| `grammar/Kql.g4` | https://github.com/microsoft/Kusto-Query-Language/blob/master/grammar/Kql.g4 |
| `grammar/KqlTokens.g4` | https://github.com/microsoft/Kusto-Query-Language/blob/master/grammar/KqlTokens.g4 |

Local copies live at `src/kusto_query_language_parser/grammar/`.


## Generated code

The parser is generated from the grammar by ANTLR. Generated output goes into the
importable package `src/kusto_query_language_parser/parse_tools/`:

- `KqlLexer.py`
- `KqlParser.py`
- `KqlListener.py`
- `KqlVisitor.py`
- `Kql.tokens` / `KqlLexer.tokens`
- `Kql.interp` / `KqlLexer.interp` (ANTLR 4.13+)

These files are **checked in and must never be hand-edited**. Any fix flows through the
grammar → regenerate pipeline.

## Prerequisites

- Java 11+ (the `antlr4` tool is Java-based)
- ANTLR tool. Two options:
  - `pip install antlr4-tools` — installs `antlr4` and `antlr4-parse` launchers, which
    auto-download Java and the latest ANTLR jar.
  - Or download `antlr-4.13.2-complete.jar` from https://www.antlr.org/download.html and
    invoke `java -jar antlr-4.13.2-complete.jar ...` directly.

The Python runtime must match the ANTLR version used to generate. This repo pins
`antlr4-python3-runtime==4.13.2` (see `requirements.txt` / `pyproject.toml`). Older pins
(`4.8.0`) are incompatible with Python 3.13+ because they import `typing.io`.

## Regenerating

The grammar uses `import KqlTokens;`, so `KqlTokens.g4` must sit alongside `Kql.g4` when
generating (it does, under `grammar/`).

### Windows

```
bin\parse_generator.bat
```

### Linux / macOS

```
bin/parse_generator.sh
```

The script sets `ANTLR4_TOOLS_ANTLR_VERSION` (default `4.13.2`) and prefers the repo's
`.venv/bin/antlr4` launcher when present, so `pip install antlr4-tools` into the venv is
enough.

Or run antlr directly from the repo root:

```
antlr4 -Dlanguage=Python3 -o src/kusto_query_language_parser/parse_tools \
    src/kusto_query_language_parser/grammar/Kql.g4 -listener -visitor
```

## After regenerating

1. Run the test suite: `.venv/bin/pytest`
2. Run type checking: `.venv/bin/mypy .`
3. Commit the regenerated `parse_tools/` output alongside the grammar changes.
