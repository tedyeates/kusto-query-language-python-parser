import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from parsetools.ExprLexer import ExprLexer
from parsetools.ExprParser import ExprParser
class Parser:
    def parse(self, text):
        lexer = ExprLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ExprParser(stream)
        tree = parser.start_()
        
        print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    input_stream = FileStream('input.txt')
    parser = Parser()
    parser.parse(input_stream)