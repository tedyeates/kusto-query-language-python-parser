import pytest
from antlr4 import InputStream

from kusto_query_language_parser.parser.kql_traverse import KqlTraverse

MUST_PARSE = [
    "StormEvents | summarize DailyActiveUsers = dcount(DeviceId) by DateUtc | order by DateUtc asc;",
    "StormEvents | summarize count() by State",
    "let f = (x: long) { x + 1 }; f(41)",
    "let f = (T: (a: int)) { T | project a }; f(StormEvents)",
    "StormEvents | graph-match (a) where a.Damage > 0",
    "StormEvents | graph-match (a) where a.Damage > 0 project a.Damage",
    "StormEvents | graph-to-table nodes",
    "StormEvents | graph-to-table nodes as N",
]

MUST_REJECT = [
    "StormEvents | summarize by",
    "let x = ; x",
    "StormEvents | project | where",
    "let f = (x: long) { x + 1 }; f(41",
    "StormEvents | |",
    "summarize count( by State",
    "StormEvents | where",
]


@pytest.mark.parametrize("query", MUST_PARSE)
def test_must_parse(query):
    parser = KqlTraverse()
    tree = parser.parse(InputStream(query))
    assert tree is not None
    assert parser.parser.getNumberOfSyntaxErrors() == 0


@pytest.mark.parametrize("query", MUST_REJECT)
def test_must_reject(query):
    parser = KqlTraverse()
    with pytest.raises(SyntaxError):
        parser.parse(InputStream(query))


def test_order_by():
    parser = KqlTraverse()
    query = (
        "StormEvents | project State, EventType, DamageProperty "
        "| where DamageProperty > 100 "
        "| summarize DailyActiveUsers = dcount(DeviceId) by DateUtc "
        "| order by DateUtc asc;"
    )
    tree = parser.parse(InputStream(query))
    assert tree is not None
    assert parser.parser.getNumberOfSyntaxErrors() == 0


def test_issue_2():
    parser = KqlTraverse()
    query = (
        "let a = GetAppLaunches(StartTime = startofday(ago(30d)), EndTime = startofday(now()));"
        "a | summarize DailyActiveUsers = dcount(DeviceId) by DateUtc "
        "| order by DateUtc asc;"
    )
    tree = parser.parse(InputStream(query))
    assert tree is not None
    assert parser.parser.getNumberOfSyntaxErrors() == 0