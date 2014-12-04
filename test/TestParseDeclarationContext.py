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

class TestDeclarationContext(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.declarationContext.addIntDeclaration('int', 0)
        self.expressionContext.addOperator(',', 0)


        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)



    def test_int_x(self):
        lexer = Lexer('int x', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('int', token.id)
        self.assertEqual('x', token.data[0].data[0])

    def test_int_x_equal_to_2(self):
        lexer = Lexer('int x = 2', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('int', token.id)
        self.assertEqual('x', token.data[0].data[0])
        self.assertEqual('=', token.data[1].id)
        self.assertEqual('x', token.data[1].data[0].data[0])
        self.assertEqual(2, token.data[1].data[1].data[0])

    def test_int_x_y_and_z(self):
        lexer = Lexer('int x , y , z ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('int', token[1].id)
        self.assertEqual('y', token[1].data[0].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('z', token[2].data[0].data[0])
if __name__ == '__main__':
    unittest.main()
