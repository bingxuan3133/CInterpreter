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
        self.defaultContext = DefaultContext(self.manager)
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.flowControlContext]

        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.addContext('Default', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parseStatement_call_buildScope_when_declaration(self):
        lexer = LexerStateMachine('int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatement(0)
        mockScopeBuilder.buildScope.assert_called_once_with(token[0])

    def test_parseStatements_should_call_buildScope_properly(self):
        lexer = LexerStateMachine('int x; { int y;};', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        scopeBuilder = ScopeBuilder()
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatements(0)
        calls = [call(token[0]), call(token[1]), call(token[1].data[0])]
        mockScopeBuilder.buildScope.assert_has_calls(calls, any_order=False)
        calls = [call()]
        mockScopeBuilder.destroyScope.assert_has_calls(calls)
        self.assertEqual(1, mockScopeBuilder.destroyScope.call_count)

    def test_parseStatements_complex_nested_brace_should_call_buildScope_properly(self):
        lexer = LexerStateMachine('int x; {int y; {int z; {int a;} int b; }};', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        scopeBuilder = ScopeBuilder()
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatements(0)
        calls = [call(token[0]), call(token[1]), call(token[1].data[0]), call(token[1].data[1]), call(token[1].data[1].data[0])]
        calls2 = [call(token[1].data[1].data[1]), call(token[1].data[1].data[1].data[0])]
        calls3 = [call(token[1].data[1].data[2])]
        calls.extend(calls2)
        calls.extend(calls3)
        mockScopeBuilder.buildScope.assert_has_calls(calls, any_order=False)
        calls = [call(), call(), call()]
        mockScopeBuilder.destroyScope.assert_has_calls(calls, any_order=False)
        self.assertEqual(3, mockScopeBuilder.destroyScope.call_count)

    def test_buildScope_should_raise_when_redeclaration(self):
        lexer = LexerStateMachine('int x; int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Redeclaration of 'x'" + '\n' +
                             'nt x; int x;' + '\n' +
                             '          ^', e.msg)

if __name__ == '__main__':
    unittest.main()
