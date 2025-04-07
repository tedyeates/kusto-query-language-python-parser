import sys
from antlr4 import *
from parse_tools.KqlParser import KqlParser
from parse_tools.KqlListener import KqlListener

class Listener(KqlListener):
    def __init__(self):
        self.result = {}
        self.json_tree = {}
        
    def visitTerminal(self, node):
        token = node.getSymbol()
        self.result[node] = {
            "type": token.type,
            "text": token.text
        }
    
    def exitEveryRule(self, ctx:ParserRuleContext):
        child_count = ctx.getChildCount()
        
        if child_count <= 0:
            self.result[ctx] = {
                "type": KqlParser.ruleNames[ctx.getRuleIndex()],
                "text": ctx.getText()
            }
            
            return
        
    
        self.result[ctx] = {
            "type": KqlParser.ruleNames[ctx.getRuleIndex()],
            "text": ctx.getText(),
            "body": [self.result[child] for child in ctx.getChildren()],
        }
        
        if ctx.getRuleIndex() == KqlParser.RULE_top:
            self.json_tree = self.result[ctx]
