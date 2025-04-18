# Kusto Query Language Parser
A parser for parsing KQL queries, including printing parse tree as json and search capabilities.
Feel free to request features or make suggestions for improvements

## Install
### Quick Install
`pip install kusto-query-language-parser`

### Use from Source
Clone repo into your project then run `pip install antlr4-python3-runtime==4.8.0`

## Usage
Check the examples section for example code and an example KQL query for testing

### Parse Code
You will need to `pip install antlr4-python3-runtime==4.8.0` for creating a file stream or input stream
This will give you an antlr parse tree; the parser also add some further helper functions

```python
from antlr4 import FileStream, InputStream
from kusto__query_language_parser.parser.kql_traverse import KqlTraverse

# parse from file
input_stream = FileStream('input.txt')

# OR parse from text
input_stream = InputStream('_GetWatchlist("Test")')

parser = KqlTraverse()
tree = parser.parse(input_stream)
```

### Get JSON Tree
Traversing an Antlr parse tree can be tedious, the parser provides an alternate visualization of the tree in JSON

```python
# After obtaining the tree above
listener = parser.traverse(tree)
json_tree = parser.get_json_tree(listener)
```

### Searching
You can also search for functions which also returns the arguments along with function name
Any expression can also be searched, you can view the JSON tree to see what expressions are available

```python
    functions = parser.find_functions(tree)
    # e.g. [{'name': '_GetWatchlist', 'arguments': ["'test'"]}]
    
    references = parser.find(tree, "nameReferenceWithDataScope")
    # e.g. ['StartTime', 'State']
```