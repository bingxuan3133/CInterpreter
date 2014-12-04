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

class TestByteCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.expressionContext = ExpressionContext(self.manager)

        self.contexts = [self.expressionContext, self.defaultContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addInfixOperator('/', 100)


        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)
        self.byteCodeGenerator = ByteCodeGenerator(self.context, self.manager)



    def test_generateByteCode_will_return_the_byteCode_in_a_list(self):
        lexer = Lexer('2 + 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.initGeneration(token)
        dataList = token.generateByteCode()
        self.assertEqual('0xff000002', dataList[0])
        self.assertEqual('0xff010003', dataList[1])
        self.assertEqual('0xfc020001', dataList[2])


    def test_generateByteCode_will_return_the_byteCode_in_a_list_for_a_multiply_expression(self):
        lexer = Lexer('3 * 4 + 2 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.initGeneration(token)
        dataList = token.generateByteCode()
        self.assertEqual('0xff000003', dataList[0])
        self.assertEqual('0xff010004', dataList[1])
        self.assertEqual('0xfa020001', dataList[2])
        self.assertEqual('0xff000002', dataList[3])
        self.assertEqual('0xfc010200', dataList[4])

    def test_generateByteCode_will_modify_the_byteCode_to_store_value_in_different_register(self):
        lexer = Lexer('3 * 4 + 2 - 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.initGeneration(token)
        dataList = token.generateByteCode()
        self.assertEqual('0xff000003', dataList[0])
        self.assertEqual('0xff010004', dataList[1])
        self.assertEqual('0xfa020001', dataList[2])
        self.assertEqual('0xff000002', dataList[3])
        self.assertEqual('0xfc010200', dataList[4])
        self.assertEqual('0xff02000a', dataList[5])
        self.assertEqual('0xfb000102', dataList[6])

    def test_generateByteCode_will_return_the_byteCode_in_a_list_with_alonger_expression(self):
        lexer = Lexer('3 * 4 + 2 - 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.initGeneration(token)
        dataList = token.generateByteCode()
        self.assertEqual('0xff000003', dataList[0])
        self.assertEqual('0xff010004', dataList[1])
        self.assertEqual('0xfa020001', dataList[2])
        self.assertEqual('0xff000002', dataList[3])
        self.assertEqual('0xfc010200', dataList[4])
        self.assertEqual('0xff02000a', dataList[5])
        self.assertEqual('0xfb000102', dataList[6])



if __name__ == '__main__':
    unittest.main()
