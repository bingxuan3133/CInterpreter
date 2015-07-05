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
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        scopeBuilder = ScopeBuilder()

        token = parser.parseStatement(0)
        scopeBuilder.buildScope(token[0])
        self.assertEqual(['x'], scopeBuilder.scope.list)
        token = parser.parseStatement(0)  # for ;
        token = parser.parseStatement(0)
        scopeBuilder.buildScope(token[0])
        self.assertEqual(['x', 'y'], scopeBuilder.scope.list)
        token = parser.parseStatement(0)  # for ;
        token = parser.parseStatement(0)
        scopeBuilder.buildScope(token[0])
        self.assertEqual(['x', 'y', 'z'], scopeBuilder.scope.list)

    def test_buildScope_xx1(self):
        lexer = LexerStateMachine('int x ;\
                                   x = 2 + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        scopeBuilder = ScopeBuilder()

        scopeBuilder.buildScope(token[0])
        self.assertEqual(['x'], scopeBuilder.scope.list)
        scopeBuilder.buildScope(token[1])
        self.assertEqual(['x'], scopeBuilder.scope.list)

    def test_buildScope_xx2(self):
        lexer = LexerStateMachine('{ int x ;\
                                   { int y ;}\
                                   }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        scopeBuilder = ScopeBuilder()

        scopeBuilder.buildScope(token[0])
        self.assertEqual([[]], scopeBuilder.scope.list)
        scopeBuilder.buildScope(token[0].data[0])
        self.assertEqual([['x']], scopeBuilder.scope.list)
        scopeBuilder.buildScope(token[0].data[1])
        self.assertEqual([['x', []]], scopeBuilder.scope.list)
        scopeBuilder.buildScope(token[0].data[1].data[0])
        self.assertEqual([['x', ['y']]], scopeBuilder.scope.list)
        parser.lexer.peep('}')
        self.assertEqual([], scopeBuilder.scope.list)
        self.assertEqual([['x']], scopeBuilder.scope.list)

    def test_buildScope_can_deal_with_identifiers(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token1 = parser.parse(0)

        lexer = LexerStateMachine('int y ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token2 = parser.parse(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        scopeBuilder.buildScope(token1)
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

        scopeBuilder.buildScope(token2)
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[1].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[1].data[0].id)
        self.assertEqual('y', scopeBuilder.scope.list[1].data[0].data[0])

    def test_buildScope_can_build_identifiers_with_braces(self):
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
        scopeBuilder = ScopeBuilder(closeBrace)

        scopeBuilder.buildScope(token1)
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

        scopeBuilder.buildScope(token3)
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual(0, len(scopeBuilder.scope.list[1]))
        self.assertEqual([], scopeBuilder.scope.list[1])

        scopeBuilder.buildScope(token4)
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual(1, len(scopeBuilder.scope.list[1]))
        self.assertEqual('int', scopeBuilder.scope.list[1][0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[1][0].data[0].id)
        self.assertEqual('y', scopeBuilder.scope.list[1][0].data[0].data[0])

        scopeBuilder.buildScope(token6)
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

    def test_scanForInterestedTokens_will_scan_for_identifiers_and_opening_curly_braces_and_buildScope(self):
        lexer = LexerStateMachine('int x ; { int y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        self.assertEqual('int', tokenLists[0].id)
        self.assertEqual('x', tokenLists[0].data[0].data[0])
        self.assertEqual('{', tokenLists[1].id)
        self.assertEqual('int', tokenLists[2].id)
        self.assertEqual('y', tokenLists[2].data[0].data[0])
        self.assertEqual('}', tokenLists[3].id)

    def test_buildScope_1(self):
        lexer = LexerStateMachine('int x ; { int y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        scopeBuilder.buildScope(tokenLists[0])
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

        scopeBuilder.buildScope(tokenLists[1])
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual(0, len(scopeBuilder.scope.list[1]))
        self.assertEqual([], scopeBuilder.scope.list[1])

        scopeBuilder.buildScope(tokenLists[2])
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual(1, len(scopeBuilder.scope.list[1]))
        self.assertEqual('int', scopeBuilder.scope.list[1][0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[1][0].data[0].id)
        self.assertEqual('y', scopeBuilder.scope.list[1][0].data[0].data[0])

        scopeBuilder.buildScope(tokenLists[3])
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

    def test_scanForInterestedTokens_will_ignore_expressions(self):
        lexer = LexerStateMachine('int x ; x = 2 + 3 ; { x = 5 + 6 ; int y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        self.assertEqual('int', tokenLists[0].id)
        self.assertEqual('x', tokenLists[0].data[0].data[0])
        self.assertEqual('{', tokenLists[1].id)
        self.assertEqual('int', tokenLists[2].id)
        self.assertEqual('y', tokenLists[2].data[0].data[0])
        self.assertEqual('}', tokenLists[3].id)

    def test_buildScope_2(self):
        lexer = LexerStateMachine('int x ; x = 2 + 3 ; { x = 5 + 6 ; int y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        scopeBuilder.buildScope(tokenLists[0])
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

        scopeBuilder.buildScope(tokenLists[1])
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual(0, len(scopeBuilder.scope.list[1]))
        self.assertEqual([], scopeBuilder.scope.list[1])

        scopeBuilder.buildScope(tokenLists[2])
        self.assertEqual(2, len(scopeBuilder.scope.list))
        self.assertEqual(1, len(scopeBuilder.scope.list[1]))
        self.assertEqual('int', scopeBuilder.scope.list[1][0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[1][0].data[0].id)
        self.assertEqual('y', scopeBuilder.scope.list[1][0].data[0].data[0])

        scopeBuilder.buildScope(tokenLists[3])
        self.assertEqual(1, len(scopeBuilder.scope.list))
        self.assertEqual('int', scopeBuilder.scope.list[0].id)
        self.assertEqual('(identifier)', scopeBuilder.scope.list[0].data[0].id)
        self.assertEqual('x', scopeBuilder.scope.list[0].data[0].data[0])

    def test_findLocal_with_2_variables(self):
        lexer = LexerStateMachine('{ int x ; { int y ; } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        scopeBuilder.buildScope(tokenLists[0])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[1])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('x', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[2])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[3])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('y', returnedToken.data[0].data[0])

    def test_scanForInterestedTokens_and_buildScope_with_many_variables(self):
        lexer = LexerStateMachine('{ int a ; int b ; { int x ; { int y ; } int z ; } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        # scopeBuilder.list = []

        # scopeBuilder.list = [ [] ]
        scopeBuilder.buildScope(tokenLists[0])
        self.assertEqual(list(), scopeBuilder.scope.list[0])

        # scopeBuilder.list = [ [a] ]
        scopeBuilder.buildScope(tokenLists[1])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])

        # scopeBuilder.list = [ [a, b] ]
        scopeBuilder.buildScope(tokenLists[2])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])

        # scopeBuilder.list = [ [a, b, [] ] ]
        scopeBuilder.buildScope(tokenLists[3])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])
        self.assertEqual(list(), scopeBuilder.scope.list[0][2])

        # scopeBuilder.list = [ [a, b, [x] ] ]
        scopeBuilder.buildScope(tokenLists[4])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])
        self.assertEqual('x', scopeBuilder.scope.list[0][2][0].data[0].data[0])

        # scopeBuilder.list = [ [a, b, [x, [] ] ] ]
        scopeBuilder.buildScope(tokenLists[5])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])
        self.assertEqual('x', scopeBuilder.scope.list[0][2][0].data[0].data[0])
        self.assertEqual(list(), scopeBuilder.scope.list[0][2][1])

        # scopeBuilder.list = [ [a, b, [x, [y] ] ] ]
        scopeBuilder.buildScope(tokenLists[6])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])
        self.assertEqual('x', scopeBuilder.scope.list[0][2][0].data[0].data[0])
        self.assertEqual('y', scopeBuilder.scope.list[0][2][1][0].data[0].data[0])

        # scopeBuilder.list = [ [a, b, [x] ] ]
        scopeBuilder.buildScope(tokenLists[7])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])
        self.assertEqual('x', scopeBuilder.scope.list[0][2][0].data[0].data[0])

        # scopeBuilder.list = [ [a, b, [x, z] ] ]
        scopeBuilder.buildScope(tokenLists[8])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])
        self.assertEqual('x', scopeBuilder.scope.list[0][2][0].data[0].data[0])
        self.assertEqual('z', scopeBuilder.scope.list[0][2][1].data[0].data[0])

        # scopeBuilder.list = [ [a, b] ]
        scopeBuilder.buildScope(tokenLists[9])
        self.assertEqual('a', scopeBuilder.scope.list[0][0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.scope.list[0][1].data[0].data[0])

        # scopeBuilder.list = [ ]
        scopeBuilder.buildScope(tokenLists[10])
        self.assertEqual(list(), scopeBuilder.scope.list)

    def test_findLocal_with_many_variables(self):
        lexer = LexerStateMachine('{ int a ; int b ; { int x ; { int y ; } int z ; } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        scopeBuilder.buildScope(tokenLists[0])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[1])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('a', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[2])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('a', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('b', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[3])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[4])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('x', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[5])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[6])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('y', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[7])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('x', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[8])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('x', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('z', returnedToken.data[0].data[0])

        scopeBuilder.buildScope(tokenLists[9])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('a', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual('int', returnedToken.id)
        self.assertEqual('(identifier)', returnedToken.data[0].id)
        self.assertEqual('b', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

        scopeBuilder.buildScope(tokenLists[10])
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('z')
        self.assertEqual(None, returnedToken)

    def test_findGlobal_with_many_variables(self):
        lexer = LexerStateMachine('{ int a ; int b ; { int x ; { int y ; { int z ; } } } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)

        closeBrace = self.context.createToken('}')
        scopeBuilder = ScopeBuilder(closeBrace)

        tokenLists = scopeBuilder.scanForInterestedTokens(token)

        scopeBuilder.buildScope(tokenLists[0])
        scopeBuilder.buildScope(tokenLists[1])
        scopeBuilder.buildScope(tokenLists[2])
        scopeBuilder.buildScope(tokenLists[3])
        scopeBuilder.buildScope(tokenLists[4])
        scopeBuilder.buildScope(tokenLists[5])
        scopeBuilder.buildScope(tokenLists[6])

        # scopeBuilder.list = [ [a, b, [x, [y, [z] ] ] ]
        #                      currentScope ^  ^ not yet built
        self.assertEqual('y', scopeBuilder.currentScope.list[0].data[0].data[0])
        self.assertEqual('x', scopeBuilder.currentScope.parentScope.list[0].data[0].data[0])
        self.assertEqual('a', scopeBuilder.currentScope.parentScope.parentScope.list[0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.currentScope.parentScope.parentScope.list[1].data[0].data[0])

        returnedToken = scopeBuilder.findLocal('y')
        self.assertEqual('y', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findLocal('x')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('a')
        self.assertEqual(None, returnedToken)
        returnedToken = scopeBuilder.findLocal('b')
        self.assertEqual(None, returnedToken)

        returnedToken = scopeBuilder.findGlobal('y')
        self.assertEqual('y', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findGlobal('x')
        self.assertEqual('x', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findGlobal('a')
        self.assertEqual('a', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findGlobal('b')
        self.assertEqual('b', returnedToken.data[0].data[0])
        returnedToken = scopeBuilder.findGlobal('z')
        self.assertEqual(None, returnedToken)

        # scopeBuilder.list = [ [a, b, [x, [y, [z] ] ] ]
        #                      currentScope ^  ^ not yet built
        self.assertEqual('y', scopeBuilder.currentScope.list[0].data[0].data[0])
        self.assertEqual('x', scopeBuilder.currentScope.parentScope.list[0].data[0].data[0])
        self.assertEqual('a', scopeBuilder.currentScope.parentScope.parentScope.list[0].data[0].data[0])
        self.assertEqual('b', scopeBuilder.currentScope.parentScope.parentScope.list[1].data[0].data[0])

if __name__ == '__main__':
    unittest.main()
