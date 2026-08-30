import json

from antlr4 import InputStream

from kusto_query_language_parser.parser.kql_traverse import KqlTraverse


def test_get_json_tree_rooted_at_top():
    parser = KqlTraverse()
    tree = parser.parse(InputStream('StormEvents | where State == "OR"'))
    listener = parser.traverse(tree)
    payload = json.loads(parser.get_json_tree(listener))
    assert payload["type"] == "top"
    assert payload["text"] == 'StormEvents|whereState=="OR"<EOF>'
    assert isinstance(payload["body"], list)


def test_traverse_returns_listener_with_json_tree():
    parser = KqlTraverse()
    tree = parser.parse(InputStream("StormEvents | summarize count() by State"))
    listener = parser.traverse(tree)
    assert listener.json_tree is not None
    assert listener.json_tree["type"] == "top"


def test_json_tree_has_statement_hierarchy():
    parser = KqlTraverse()
    tree = parser.parse(InputStream("StormEvents | project State"))
    payload = json.loads(parser.get_json_tree(parser.traverse(tree)))
    top_body = payload["body"]
    assert top_body
    assert top_body[0]["type"] == "query"
    statement = top_body[0]["body"][0]
    assert statement["type"] == "statement"
    assert statement["text"] == "StormEvents|projectState"