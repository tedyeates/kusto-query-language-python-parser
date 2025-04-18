from antlr4 import FileStream
from kusto__query_language_parser.parser.kql_traverse import KqlTraverse

if __name__ == '__main__':
    input_stream = FileStream('input.txt')
    parser = KqlTraverse()
    tree = parser.parse(input_stream)
    parser.print_tree(tree)
    listener = parser.traverse(tree)
    json_tree = parser.get_json_tree(listener)
    
    functions = parser.find_functions(tree)
    function = parser.find(tree, "nameReferenceWithDataScope")
    
    print(json_tree)
    print(functions)
    print(function)