from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.tree.Tree import TerminalNodeImpl
from parse_tools.KqlLexer import KqlLexer
from parse_tools.KqlParser import KqlParser
from parser.listener import Listener
import json
class KqlTraverse:
    
    def parse(self, text):
        lexer = KqlLexer(text)
        stream = CommonTokenStream(lexer)
        self.parser = KqlParser(stream)
        tree = self.parser.top()
        
        if self.parser.getNumberOfSyntaxErrors() > 0:
            raise SyntaxError("syntax errors")

        return tree
    
    
    def print_tree(self, tree):
        print(tree.toStringTree(recog=self.parser))
        
    def traverse(self, tree):
        listener = Listener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener
        
    def get_json_tree(self, listener):
        return json.dumps(listener.json_tree)