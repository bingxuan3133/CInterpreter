__author__ = 'admin'

import unittest
from unittest.mock import MagicMock
from unittest.mock import call

from ContextManager import *
from DefaultContext import *
from ExpressionContext import *
from DeclarationContext import *
from Parser import *
from FlowControlContext import *

class TestParseStatementToMockBuildScope(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.flowControlContext]

        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addInfixOperator('/', 100)
        self.expressionContext.addInfixOperator('==', 20)
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addOperator(';')
        self.declarationContext.addInt('int', 0)
        self.flowControlContext.addIfControl('if', 0)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addGroupOperator(')', 0)

        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parseStatement_call_buildScope_when_declaration(self):
        lexer = LexerStateMachine('int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatement(0)
        mockScopeBuilder.buildScope.assert_called_once_with(token[0])

    def test_parseStatement_should_call_buildScope_properly(self):
        lexer = LexerStateMachine('int x; { int y;};', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        scopeBuilder = ScopeBuilder()
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatements(0)
        print(token)
        print(mockScopeBuilder.mock_calls)
        calls = [call(token[0]), call(token[1]), call(token[1].data[0]), call(parser.closingBrace)]
        mockScopeBuilder.buildScope.assert_has_calls(calls, any_order=False)


if __name__ == '__main__':
    unittest.main()
