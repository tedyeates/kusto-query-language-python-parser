import sys
from antlr4 import *
from parse_tools.KqlParser import KqlParser
from parse_tools.KqlListener import KqlListener

class Listener(KqlListener):
    def __init__(self):
        self.result = {}
    
    def exitEveryRule(self, ctx:ParserRuleContext):
        print(KqlParser.ruleNames[ctx.getRuleIndex()])