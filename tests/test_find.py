import pytest
from antlr4 import InputStream

from kusto_query_language_parser.parser.kql_traverse import KqlTraverse


@pytest.fixture
def parser():
    return KqlTraverse()


def parse(parser, query):
    return parser.parse(InputStream(query))


def test_find_functions_single_expression(parser):
    tree = parse(parser, '_GetWatchlist("Test")')
    assert parser.find_functions(tree) == [{"name": "_GetWatchlist", "arguments": ['"Test"']}]


def test_find_functions_multiple(parser):
    tree = parse(parser, "StormEvents | extend d = dcount(DeviceId) | project sum = sum(Damage)")
    functions = parser.find_functions(tree)
    assert functions == [
        {"name": "dcount", "arguments": ["DeviceId"]},
        {"name": "sum", "arguments": ["Damage"]},
    ]


def test_find_functions_in_let_function(parser):
    tree = parse(parser, "let AddOne = (x: long) { x + 1 }; AddOne(41)")
    assert parser.find_functions(tree) == [{"name": "AddOne", "arguments": ["41"]}]


def test_find_name_reference_with_data_scope(parser):
    tree = parse(parser, 'StormEvents | where State == "OR" | project State, EventType')
    references = parser.find(tree, "nameReferenceWithDataScope")
    assert references == ["StormEvents", "State", "State", "EventType"]


def test_find_returns_empty_list_for_unknown_rule(parser):
    tree = parse(parser, "StormEvents | where State == \"OR\"")
    assert parser.find(tree, "definitelyNotARule") == []