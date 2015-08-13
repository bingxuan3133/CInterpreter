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
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.contexts = [self.declarationContext, self.expressionContext, self.flowControlContext]

        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.addContext('Default', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_parseStatement_call_buildScope_when_declaration(self):
        lexer = LexerStateMachine('int x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatement(0)
        mockScopeBuilder.buildScope.assert_called_once_with(token[0])

    def test_parseStatements_should_call_buildScope_properly(self):
        lexer = LexerStateMachine('int x; { int y;};', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        mockScopeBuilder = MagicMock(wraps=ScopeBuilder())
        scopeBuilder = ScopeBuilder()
        parser.scopeBuilder = mockScopeBuilder
        token = parser.parseStatements(0)
        calls = [call(token[0]), call(token[1]), call(token[1].data[0])]
        mockScopeBuilder.buildScope.assert_has_calls(calls, any_order=False)
        calls = [call()]
        mockScopeBuilder.destroyCurrentScope.assert_has_calls(calls)
        self.assertEqual(1, mockScopeBuilder.destroyCurrentScope.call_count)

    def test_parseStatements_complex_nested_brace_should_call_buildScope_properly(self):
        lexer = LexerStateMachine('int x; {int y; {int z; {int a;} int b; }};', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
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
        mockScopeBuilder.destroyCurrentScope.assert_has_calls(calls, any_order=False)
        self.assertEqual(3, mockScopeBuilder.destroyCurrentScope.call_count)

    def test_buildScope_should_raise_given_redeclaration_of_x(self):
        lexer = LexerStateMachine('int x; int x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Redeclaration of 'x'" + '\n' +
                             'nt x; int x;' + '\n' +
                             '          ^', e.msg)

    def test_buildScope_should_raise_given_redeclaration_of_x_3xpointer(self):
        lexer = LexerStateMachine('int x; int ***x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Error[1][11]:Redeclaration of 'x'" + '\n' +
                             'nt x; int ***x;' + '\n' +
                             '             ^', e.msg)

    def test_buildScope_should_raise_given_redeclaration_of_x_in_single_statement(self):
        lexer = LexerStateMachine('int x, x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Redeclaration of 'x'"+ '\n' +
                               'int x, x;'+ '\n' +
                               '       ^',e.msg)

    def test_redeclaration_of_x_given_second_x_is_pointer_in_single_statement(self):
        lexer = LexerStateMachine('int x, *x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Redeclaration of 'x'"+ '\n' +
                             'int x, *x;'+ '\n' +
                             '        ^',e.msg)

    def test_buildScope_should_not_raise_given_redeclaration_of_x(self):
        lexer = LexerStateMachine('int x', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting ; before (systemToken)" + '\n' +
                             'int x' + '\n' +
                             '     ^', e.msg)
        try:
            lexer = LexerStateMachine('int x;', self.context)
            parser.lexer = lexer
            parser.parseStatement(0)
        except SyntaxError as e:
            print(e.msg)
            self.fail('Should not raise')

if __name__ == '__main__':
    unittest.main()
