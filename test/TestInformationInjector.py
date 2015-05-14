__author__ = 'JingWen'

import unittest
import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)
from Parser import *
from Context import *
from ContextManager import *
from DefaultContext import *
from ExpressionContext import *
from ByteCodeGenerator import *
from DeclarationContext import *
from FlowControlContext import *
from RegisterAllocator import *
from InformationInjector import *
from InformationInjector import *

class TestInformationInjector(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.declarationContext = DeclarationContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.expressionContext = ExpressionContext(self.manager)
        self.expressionContext.addOperator(',', 0)

        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addInfixOperator('/', 100)
        self.declarationContext.addIntDeclaration('int', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)


        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)
        self.byteCodeGenerator = ByteCodeGenerator(self.context, self.manager)
        self.informationInjector = InformationInjector()

    def test_injectRegisterRequired_will_give_registerRequiredAtThatLevel_to_a_tree(self):
        lexer = Lexer('{ x = y + 8 * 16 / 180 - 20 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        if token[0].id == '{':
            token = token[0].data[0]
        self.informationInjector.injectRegisterRequired(token)

        self.assertEqual(1, token.data[0].registerRequiredAtThatLevel)
        self.assertEqual(2, token.registerRequiredAtThatLevel)
        self.assertEqual(-2, token.data[1].registerRequiredAtThatLevel)
        self.assertEqual(1, token.data[1].data[1].registerRequiredAtThatLevel)
        self.assertEqual(2, token.data[1].data[0].registerRequiredAtThatLevel)
        self.assertEqual(1, token.data[1].data[0].data[0].registerRequiredAtThatLevel)
        self.assertEqual(-2, token.data[1].data[0].data[1].registerRequiredAtThatLevel)
        self.assertEqual(-2, token.data[1].data[0].data[1].data[0].registerRequiredAtThatLevel)
        self.assertEqual(1, token.data[1].data[0].data[1].data[1].registerRequiredAtThatLevel)
        self.assertEqual(1, token.data[1].data[0].data[1].data[0].data[0].registerRequiredAtThatLevel)
        self.assertEqual(1, token.data[1].data[0].data[1].data[0].data[1].registerRequiredAtThatLevel)

    def test_injectRegisterRequired_will_give_min_and_max_register_to_each_of_the_token(self):
        lexer = Lexer('{ x = y + 8 * 16 / 180 - 20 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        if token[0].id == '{':
            token = token[0].data[0]
        self.informationInjector.injectRegisterRequired(token)

        self.assertEqual(1, token.data[0].maxRequiredRegister)
        self.assertEqual(1, token.data[0].minRequiredRegister)
        self.assertEqual(6, token.maxRequiredRegister)
        self.assertEqual(2, token.minRequiredRegister)
        self.assertEqual(5, token.data[1].maxRequiredRegister)
        self.assertEqual(2, token.data[1].minRequiredRegister)
        self.assertEqual(1, token.data[1].data[1].maxRequiredRegister)
        self.assertEqual(1, token.data[1].data[1].minRequiredRegister)
        self.assertEqual(4, token.data[1].data[0].maxRequiredRegister)
        self.assertEqual(2, token.data[1].data[0].minRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[0].maxRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[0].minRequiredRegister)
        self.assertEqual(3, token.data[1].data[0].data[1].maxRequiredRegister)
        self.assertEqual(2, token.data[1].data[0].data[1].minRequiredRegister)
        self.assertEqual(2, token.data[1].data[0].data[1].data[0].maxRequiredRegister)
        self.assertEqual(2, token.data[1].data[0].data[1].data[0].minRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[1].data[1].maxRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[1].data[1].minRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[1].data[0].data[0].maxRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[1].data[0].data[0].minRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[1].data[0].data[1].maxRequiredRegister)
        self.assertEqual(1, token.data[1].data[0].data[1].data[0].data[1].minRequiredRegister)



if __name__ == '__main__':
    unittest.main()
