import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Context import *
from DefaultContext import *
from ExpressionContext import *
from FlowControlContext import *
from Parser import *
from ContextManager import *

class MyTestCase(unittest.TestCase):
    def test_default_context(self):
        manager = ContextManager()
        context = Context(manager)
        defaultContext = DefaultContext(manager)
        flowControlContext = FlowControlContext(manager)
        expressionContext = ExpressionContext(manager)

        manager.addContext('Default', defaultContext)
        manager.addContext('FlowControl', flowControlContext)
        manager.addContext('Expression', expressionContext)
        defaultContext.addKeyword('if')
        defaultContext.addKeyword('while')
        manager.setCurrentContexts([defaultContext])
        lexer = LexerStateMachine('if', context)
        parser = Parser(lexer, manager)
        manager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            pass
        lexer = LexerStateMachine('123 if', context)
        parser = Parser(lexer, manager)
        manager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            pass

if __name__ == '__main__':
    unittest.main()
