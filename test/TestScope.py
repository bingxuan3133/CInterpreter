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
        lexer = Lexer('int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token1 = parser.parse(0)

        lexer = Lexer('int y ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token2 = parser.parse(0)

        closeBrace = self.context.createToken('}')
        scope = Scope(closeBrace)

        scope.buildScope(token1)
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

        scope.buildScope(token2)
        self.assertEqual(2, len(scope.list))
        self.assertEqual('int', scope.list[1].id)
        self.assertEqual('(identifier)', scope.list[1].data[0].id)
        self.assertEqual('y', scope.list[1].data[0].data[0])

    def test_buildScope_with_bracers(self):
        token1 = self.context.createToken('int')
        token2 = self.context.createToken('x')
        token3 = self.context.createToken('{')
        token4 = self.context.createToken('int')
        token5 = self.context.createToken('y')
        token6 = self.context.createToken('}')

        token1.data = []
        token1.data.append(token2)
        token4.data = []
        token4.data.append(token5)

        closeBrace = self.context.createToken('}')
        scope = Scope(closeBrace)

        scope.buildScope(token1)
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

        scope.buildScope(token3)
        self.assertEqual(2, len(scope.list))
        self.assertEqual(0, len(scope.list[1]))
        self.assertEqual([], scope.list[1])

        scope.buildScope(token4)
        self.assertEqual(2, len(scope.list))
        self.assertEqual(1, len(scope.list[1]))
        self.assertEqual('int', scope.list[1][0].id)
        self.assertEqual('(identifier)', scope.list[1][0].data[0].id)
        self.assertEqual('y', scope.list[1][0].data[0].data[0])

        scope.buildScope(token6)
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

    def test_scanForInterestedTokens(self):
        lexer = Lexer('int x ; { int y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        openBrace = self.context.createToken('{')
        scope = Scope(closeBrace)

        tokenLists = scope.scanForInterestedTokens(token)

        self.assertEqual('int', tokenLists[0].id)
        self.assertEqual('x', tokenLists[0].data[0].data[0])
        self.assertEqual('{', tokenLists[1].id)
        self.assertEqual('int', tokenLists[2].id)
        self.assertEqual('y', tokenLists[2].data[0].data[0])
        self.assertEqual('}', tokenLists[3].id)

        scope.buildScope(tokenLists[0])
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

        scope.buildScope(tokenLists[1])
        self.assertEqual(2, len(scope.list))
        self.assertEqual(0, len(scope.list[1]))
        self.assertEqual([], scope.list[1])

        scope.buildScope(tokenLists[2])
        self.assertEqual(2, len(scope.list))
        self.assertEqual(1, len(scope.list[1]))
        self.assertEqual('int', scope.list[1][0].id)
        self.assertEqual('(identifier)', scope.list[1][0].data[0].id)
        self.assertEqual('y', scope.list[1][0].data[0].data[0])

        scope.buildScope(tokenLists[3])
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

    def test_scanForInterestedTokens_will_ignore_expressions(self):
        lexer = Lexer('int x ; x = 2 + 3 ; { x = 5 + 6 ; int y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        openBrace = self.context.createToken('{')
        scope = Scope(closeBrace)

        tokenLists = scope.scanForInterestedTokens(token)

        self.assertEqual('int', tokenLists[0].id)
        self.assertEqual('x', tokenLists[0].data[0].data[0])
        self.assertEqual('{', tokenLists[1].id)
        self.assertEqual('int', tokenLists[2].id)
        self.assertEqual('y', tokenLists[2].data[0].data[0])
        self.assertEqual('}', tokenLists[3].id)

        scope.buildScope(tokenLists[0])
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

        scope.buildScope(tokenLists[1])
        self.assertEqual(2, len(scope.list))
        self.assertEqual(0, len(scope.list[1]))
        self.assertEqual([], scope.list[1])

        scope.buildScope(tokenLists[2])
        self.assertEqual(2, len(scope.list))
        self.assertEqual(1, len(scope.list[1]))
        self.assertEqual('int', scope.list[1][0].id)
        self.assertEqual('(identifier)', scope.list[1][0].data[0].id)
        self.assertEqual('y', scope.list[1][0].data[0].data[0])

        scope.buildScope(tokenLists[3])
        self.assertEqual(1, len(scope.list))
        self.assertEqual('int', scope.list[0].id)
        self.assertEqual('(identifier)', scope.list[0].data[0].id)
        self.assertEqual('x', scope.list[0].data[0].data[0])

if __name__ == '__main__':
    unittest.main()
