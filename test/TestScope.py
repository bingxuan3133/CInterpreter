__author__ = 'admin'

import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Scope import *
from Parser import *
from ContextManager import *
from Context import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestScope(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.declarationContext.addIntDeclaration('int', 0)
        self.expressionContext = ExpressionContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.expressionContext.addOperator(';', 0)
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addInfixOperator('+', 70)
        self.expressionContext.addInfixOperator('-', 70)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.contexts = [self.declarationContext, self.expressionContext, self.flowControlContext, self.defaultContext]
        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_buildScope(self):
        lexer = LexerStateMachine('int x ;\
                                   int y ;\
                                   int z ;', self.context)
        scopeBuilder = ScopeBuilder()
        parser = Parser(lexer, self.manager, scopeBuilder)
        self.manager.setParser(parser)

        token = parser.parseStatements(0)

        self.assertEqual(['x'], scopeBuilder.scopeHistory[0])
        self.assertEqual(['x', 'y'], scopeBuilder.scopeHistory[1])
        self.assertEqual(['x', 'y', 'z'], scopeBuilder.scopeHistory[2])

    def test_buildScope_will_only_care_declaration_but_not_expression(self):
        lexer = LexerStateMachine('int x ;\
                                   x = 2 + 3 ;', self.context)
        scopeBuilder = ScopeBuilder()
        parser = Parser(lexer, self.manager, scopeBuilder)
        self.manager.setParser(parser)

        token = parser.parseStatements(0)

        self.assertEqual(['x'], scopeBuilder.scopeHistory[0])
        self.assertEqual(['x'], scopeBuilder.scopeHistory[1])

    def test_buildScope_to_deal_with_curly_brace(self):
        lexer = LexerStateMachine('int x ; { int y ; }', self.context)
        scopeBuilder = ScopeBuilder()
        parser = Parser(lexer, self.manager, scopeBuilder)
        self.manager.setParser(parser)

        token = parser.parseStatements(0)

        self.assertEqual(['x'], scopeBuilder.scopeHistory[0])
        self.assertEqual(['x', []], scopeBuilder.scopeHistory[1])
        self.assertEqual(['x', ['y']], scopeBuilder.scopeHistory[2])
        self.assertEqual(['x'], scopeBuilder.scopeHistory[3])

    def test_buildScope_to_deal_with_curly_braces(self):
        lexer = LexerStateMachine('{ int x ;\
                                   { int y ; }\
                                   }', self.context)
        scopeBuilder = ScopeBuilder()
        parser = Parser(lexer, self.manager, scopeBuilder)
        self.manager.setParser(parser)

        token = parser.parseStatements(0)

        self.assertEqual([[]], scopeBuilder.scopeHistory[0])
        self.assertEqual([['x']], scopeBuilder.scopeHistory[1])
        self.assertEqual([['x', []]], scopeBuilder.scopeHistory[2])
        self.assertEqual([['x', ['y']]], scopeBuilder.scopeHistory[3])
        self.assertEqual([['x']], scopeBuilder.scopeHistory[4])
        self.assertEqual([], scopeBuilder.scopeHistory[5])
        pass

    def test_buildScope_can_deal_with_3_nested_curly_braces(self):
        lexer = LexerStateMachine('{ int a ; int b ; { int x ; { int y ; } int z ; } }', self.context)
        scopeBuilder = ScopeBuilder()
        parser = Parser(lexer, self.manager, scopeBuilder)
        self.manager.setParser(parser)

        token = parser.parseStatements(0)

        self.assertEqual([[]], scopeBuilder.scopeHistory[0])
        self.assertEqual([['a']], scopeBuilder.scopeHistory[1])
        self.assertEqual([['a', 'b']], scopeBuilder.scopeHistory[2])
        self.assertEqual([['a', 'b', []]], scopeBuilder.scopeHistory[3])
        self.assertEqual([['a', 'b', ['x']]], scopeBuilder.scopeHistory[4])
        self.assertEqual([['a', 'b', ['x', []]]], scopeBuilder.scopeHistory[5])
        self.assertEqual([['a', 'b', ['x', ['y']]]], scopeBuilder.scopeHistory[6])
        self.assertEqual([['a', 'b', ['x']]], scopeBuilder.scopeHistory[7])
        self.assertEqual([['a', 'b', ['x', 'z']]], scopeBuilder.scopeHistory[8])
        self.assertEqual([['a', 'b']], scopeBuilder.scopeHistory[9])
        self.assertEqual([], scopeBuilder.scopeHistory[10])

    def test_findLocal(self):
        lexer = LexerStateMachine('int x ; x = 2 + 3 ; { x = 5 + 6 ; int y ; }', self.context)
        scopeBuilder = ScopeBuilder()
        parser = Parser(lexer, self.manager, scopeBuilder)
        self.manager.setParser(parser)

        token = parser.parseStatements(0)

        self.assertEqual(['x'], scopeBuilder.scopeHistory[0])
        self.assertEqual(['x'], scopeBuilder.scopeHistory[1])
        self.assertEqual([['x', []]], scopeBuilder.scopeHistory[2])
        self.assertEqual([['x', ['y']]], scopeBuilder.scopeHistory[3])
        self.assertEqual([['x']], scopeBuilder.scopeHistory[4])
        self.assertEqual([], scopeBuilder.scopeHistory[5])

if __name__ == '__main__':
    unittest.main()
