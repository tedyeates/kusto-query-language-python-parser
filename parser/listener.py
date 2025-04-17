import sys
from antlr4 import *
from ..parse_tools.KqlParser import KqlParser
from ..parse_tools.KqlListener import KqlListener
from enum import Enum

class Mode(Enum):
    JSON_TREE = 0
    SEARCH = 1
class Listener(KqlListener):
    def __init__(self, mode: Mode, **kwargs):
        self.result = {}
        self.json_tree = {}
        self.mode = mode
        
        if self.mode == Mode.SEARCH:
            self.search_type = kwargs.pop('search_type', None)
            self.search_results = []
            
            
    def package_node(self, ctx):
        return {
            "type": KqlParser.ruleNames[ctx.getRuleIndex()],
            "text": ctx.getText(),
            "body": [self.result[child] for child in ctx.getChildren()],
        }
        
    def create_json_tree(self, ctx):
        child_count = ctx.getChildCount()
        
        if child_count <= 0:
            self.result[ctx] = {
                "type": KqlParser.ruleNames[ctx.getRuleIndex()],
                "text": ctx.getText()
            }
            
            return
    
        self.result[ctx] = self.package_node(ctx)
        
        if ctx.getRuleIndex() == KqlParser.RULE_top:
            self.json_tree = self.result[ctx]

    def create_json_terminal(self, node):
        token = node.getSymbol()
        self.result[node] = {
            "type": token.type,
            "text": token.text
        }
    
    
    def matches_search(self, ctx) -> bool:
        if not self.search_type: return False
        
        return KqlParser.ruleNames[ctx.getRuleIndex()] == self.search_type
    
    def search(self, ctx):
        if self.matches_search(ctx):
            self.search_results.append(ctx)
            
        
    def visitTerminal(self, node):
        options = {
            Mode.JSON_TREE: self.create_json_terminal
        }
        
        if self.mode not in options: return
        
        options[self.mode](node)
    
    
    def exitEveryRule(self, ctx:ParserRuleContext):
        options = {
            Mode.JSON_TREE: self.create_json_tree,
            Mode.SEARCH: self.search
        }
        
        if self.mode not in options: return
        
        options[self.mode](ctx)
