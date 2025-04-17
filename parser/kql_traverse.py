from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.tree.Tree import TerminalNodeImpl
from ..parse_tools.KqlLexer import KqlLexer
from ..parse_tools.KqlParser import KqlParser
from .listener import Listener, Mode
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
        listener = Listener(Mode.JSON_TREE)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener

        
    def get_json_tree(self, listener):
        return json.dumps(listener.json_tree)
    
    
    def get_function_name(self, ctx):
        return ctx.getChild(0).getText()
    
    
    def get_argument_names(self, ctx):
        arguments = []
        index = 0
        for child in ctx.getChildren():
            if index > 0 and index % 2 == 0:
                arguments.append(child.getText())
                
            index += 1
            
        return arguments
        
    def find_functions(self, tree):
        listener = Listener(
            Mode.SEARCH, search_type="namedFunctionCallExpression"
        )
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        
        functions = []
        for result in listener.search_results:
            functions.append({
                "name": self.get_function_name(result),
                "arguments": self.get_argument_names(result)
            })
            
        return functions
    
    def find(self, tree, search_type):
        listener = Listener(
            Mode.SEARCH, search_type=search_type
        )
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
            
        results = []
        for result in listener.search_results:
            results.append(result.getText())
            
        return results