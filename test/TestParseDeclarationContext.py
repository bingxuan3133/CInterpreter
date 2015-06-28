__author__ = 'JingWen'

import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Parser import *
from Context import *
from ContextManager import *
from DeclarationContext import *
from DefaultContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestDeclarationContext(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.declarationContext.addIntDeclaration('int', 0)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_int_x_without_semicolon(self):
        lexer = LexerStateMachine('int x', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_int_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_int_y_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int x, int y ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_coma_but_left_empty_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int x, ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_x(self):
        lexer = LexerStateMachine('int x x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Expecting ; before (identifier)", e.msg)

    def test_int_x(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_int_x_equal_to_2(self):
        lexer = LexerStateMachine('int x = 2 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(2, token[1].data[1].data[0])

    def test_int_x_y_and_z(self):
        lexer = LexerStateMachine('int x , y , z ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('int', token[1].id)
        self.assertEqual('y', token[1].data[0].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('z', token[2].data[0].data[0])

    def test_int_x_y_and_z_with_some_initialization(self):
        lexer = LexerStateMachine('int x = 3 , y , z = 2 + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(3, token[1].data[1].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('y', token[2].data[0].data[0])
        self.assertEqual('int', token[3].id)
        self.assertEqual('z', token[3].data[0].data[0])
        self.assertEqual('=', token[4].id)
        self.assertEqual('z', token[4].data[0].data[0])
        self.assertEqual('+', token[4].data[1].id)
        self.assertEqual(2, token[4].data[1].data[0].data[0])
        self.assertEqual(3, token[4].data[1].data[1].data[0])

    def test_int_x_y_z_with_initialization(self):
        lexer = LexerStateMachine('int x = 3 , y = 2 + 3 , z = y + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(3, token[1].data[1].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('y', token[2].data[0].data[0])
        self.assertEqual('=', token[3].id)
        self.assertEqual('y', token[3].data[0].data[0])
        self.assertEqual('+', token[3].data[1].id)
        self.assertEqual(2, token[3].data[1].data[0].data[0])
        self.assertEqual(3, token[3].data[1].data[1].data[0])
        self.assertEqual('int', token[4].id)
        self.assertEqual('z', token[4].data[0].data[0])
        self.assertEqual('=', token[5].id)
        self.assertEqual('z', token[5].data[0].data[0])
        self.assertEqual('+', token[5].data[1].id)
        self.assertEqual('y', token[5].data[1].data[0].data[0])
        self.assertEqual(3, token[5].data[1].data[1].data[0])

    def test_expression_with_separate_initialization(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                      int y = 15 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
        self.assertEqual('int', token[0].data[2].id)
        self.assertEqual('y', token[0].data[2].data[0].data[0])
        self.assertEqual('=', token[0].data[3].id)
        self.assertEqual('y', token[0].data[3].data[0].data[0])
        self.assertEqual(15, token[0].data[3].data[1].data[0])

    def test_nested_bracers(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                         { int y = 5 ; }\
                         { int z = 15 ; } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
        self.assertEqual('{', token[0].data[2].id)
        self.assertEqual('int', token[0].data[2].data[0].id)
        self.assertEqual('y', token[0].data[2].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[2].data[1].id)
        self.assertEqual('y', token[0].data[2].data[1].data[0].data[0])
        self.assertEqual(5, token[0].data[2].data[1].data[1].data[0])
        self.assertEqual('{', token[0].data[3].id)
        self.assertEqual('int', token[0].data[3].data[0].id)
        self.assertEqual('z', token[0].data[3].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[3].data[1].id)
        self.assertEqual('z', token[0].data[3].data[1].data[0].data[0])
        self.assertEqual(15, token[0].data[3].data[1].data[1].data[0])

    def test_declaration_expression_declaration(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                                     x = 5 + 10 ;\
                                     int z = 15 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
        self.assertEqual('=', token[0].data[2].id)
        self.assertEqual('x', token[0].data[2].data[0].data[0])
        self.assertEqual('+', token[0].data[2].data[1].id)
        self.assertEqual(5, token[0].data[2].data[1].data[0].data[0])
        self.assertEqual(10, token[0].data[2].data[1].data[1].data[0])
        self.assertEqual('int', token[0].data[3].id)
        self.assertEqual('z', token[0].data[3].data[0].data[0])
        self.assertEqual('=', token[0].data[4].id)
        self.assertEqual('z', token[0].data[4].data[0].data[0])
        self.assertEqual(15, token[0].data[4].data[1].data[0])

"""
    def test_int_int_will_raiseException(self):
        lexer = Lexer('int int x = 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
"""

class TestPointerDeclaration(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.declarationContext.addIntDeclaration('int', 0)
        self.declarationContext.addPointerDeclaration('*', 120)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

"""
    def test_int_pointer(self):
        lexer = Lexer('int * ptr ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('*', token[0].data[0].id)
        self.assertEqual('ptr', token[0].data[0].data[0].data[0])


    def test_int_pointer_equal_3(self):
        lexer = Lexer('int * ptr = 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('*', token[0].data[0].id)
        self.assertEqual('ptr', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[1].data[0].id)
        self.assertEqual('ptr', token[1].data[0].data[0])
        self.assertEqual('3', token[1].data[0].data[1])
"""

if __name__ == '__main__':
    unittest.main()
