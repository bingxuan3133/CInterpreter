__author__ = 'JingWen'

import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Parser import *
from Context import *
from ContextManager import *
from DeclarationContext import *

class TestDeclarationContext(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.declarationContext = DeclarationContext(self.manager)
        self.contexts = [self.declarationContext]
        self.declarationContext.addIntDeclaration('int', 0)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.setCurrentContexts(self.contexts)


    def test_int_x(self):
        lexer = Lexer('int x', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('int', token.id)
        self.assertEqual('x', token.data[0].data[0])


if __name__ == '__main__':
    unittest.main()
