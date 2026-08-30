# AGENTS.md

## Project Config

repo: tedyeates/kusto-query-language-python-parser
issue_tracker: github
cli: gh
test_command: .venv/bin/pytest
type_check_command: .venv/bin/mypy .
build_command:
setup_command: python -m venv .venv && .venv/bin/pip install -r requirements.txt

## Triage Labels

| Role | Label |
|------|-------|
| ready-for-agent | ready-for-agent |
| ready-for-human | ready-for-human |
| ready-for-production | ready-for-production |
| spec | spec |
| needs-triage | needs-triage |
| needs-info | needs-info |
| wontfix | wontfix |
| impl-failed | impl-failed |

## Corrections

(read the corrections log before starting work; append on error)

see docs/corrections-log.md
