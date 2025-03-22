from antlr4 import FileStream
from parser.kql_traverse import KqlTraverse

if __name__ == '__main__':
    input_stream = FileStream('input.txt')
    parser = KqlTraverse()
    tree = parser.parse(input_stream)
    parser.print_tree(tree)