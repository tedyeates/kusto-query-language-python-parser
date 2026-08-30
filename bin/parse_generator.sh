#!/usr/bin/env bash
set -euo pipefail

export ANTLR4_TOOLS_ANTLR_VERSION="${ANTLR4_TOOLS_ANTLR_VERSION:-4.13.2}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ANTLR4="antlr4"
if [[ -x "$REPO_ROOT/.venv/bin/antlr4" ]]; then
  ANTLR4="$REPO_ROOT/.venv/bin/antlr4"
fi

PACKAGE_DIR="$REPO_ROOT/src/kusto_query_language_parser"

cd "$PACKAGE_DIR/grammar"

"$ANTLR4" -Dlanguage=Python3 -o ../parse_tools Kql.g4 -listener -visitor