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

class TestByteCodeGenerator(unittest.TestCase):
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

    def test_generateByteCode_will_generate_code_for_push_the_working_register_into_the_stack(self):
        lexer = Lexer(' x = 5 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        token.leftValue = 1
        token.rightValue = 1
        self.byteCodeGenerator.injectRegisterRequired(token)
        self.byteCodeGenerator.oracle.workingRegisterCounter = 5
        self.byteCodeGenerator.oracle.registerLeft = 1
        self.byteCodeGenerator.oracle.registerStatus = [1, 1, 1, 1, 1, 0]
        self.byteCodeGenerator.registersInThisAST['x'] =4

        self.byteCodeGenerator.initGeneration()
        dataList = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple(7, 0b000010), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadRegister(4, 7, 4), dataList[1])
        self.assertEqual(self.byteCodeGenerator.loadValue(5, 5), dataList[2])
        self.assertEqual(self.byteCodeGenerator.assignRegister(5, 4), dataList[3])
        self.assertEqual(self.byteCodeGenerator.loadMultiple(7, 0b000010), dataList[4])

    def test_generateByteCode_will_push_the_register_at_the_second_token(self):
        lexer = Lexer(' x = 5 + 10 + 20', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.injectRegisterRequired(token)
        token.maxRequiredRegister = 2
        token.data[1].minRequiredRegister = 3 # hard code this to make sure the program will push the working register
        self.byteCodeGenerator.oracle.workingRegisterCounter = 4
        self.byteCodeGenerator.oracle.registerLeft = 2
        self.byteCodeGenerator.oracle.registerStatus = [1, 1, 1, 1, 0, 0]
        self.byteCodeGenerator.registersInThisAST['x'] =4

        self.byteCodeGenerator.initGeneration()
        dataList = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple(7, 0b000100), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(3, 5), dataList[1])
        self.assertEqual(self.byteCodeGenerator.loadValue(5, 10), dataList[2])
        self.assertEqual(self.byteCodeGenerator.addRegister(3, 5), dataList[3])
        self.assertEqual(self.byteCodeGenerator.loadValue(5, 20), dataList[4])
        self.assertEqual(self.byteCodeGenerator.addRegister(5, 3), dataList[5])
        self.assertEqual(self.byteCodeGenerator.loadMultiple(7, 0b000100), dataList[6])
        self.assertEqual(self.byteCodeGenerator.loadRegister(4, 7, 4), dataList[7])
        self.assertEqual(self.byteCodeGenerator.assignRegister(4, 5), dataList[8])

    def test_generateByteCode_will_push_the_register_when_the_registers_available_is_not_enough_for_maxRequiredRegister(self):
        lexer = Lexer(' x = 8 * 9 * 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.injectRegisterRequired(token)
        self.byteCodeGenerator.oracle.workingRegisterCounter = 4
        self.byteCodeGenerator.oracle.registerLeft = 2
        self.byteCodeGenerator.oracle.registerStatus = [1, 1, 1, 1, 0, 0]
        self.byteCodeGenerator.registersInThisAST['x'] =4

        self.byteCodeGenerator.initGeneration()
        dataList = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple(7, 0b001100), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(2, 8), dataList[1])
        self.assertEqual(self.byteCodeGenerator.loadValue(5, 9), dataList[2])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister(2, 5), dataList[3])
        self.assertEqual(self.byteCodeGenerator.loadValue(5, 10), dataList[4])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister(2, 5), dataList[5])
        self.assertEqual(self.byteCodeGenerator.loadRegister(5, 7, 4), dataList[6])
        self.assertEqual(self.byteCodeGenerator.assignRegister(5, 2), dataList[7])
        self.assertEqual(self.byteCodeGenerator.loadMultiple(7, 0b001100), dataList[8])

class TestHelperFunction(unittest.TestCase):
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

    def test_injectRegisterRequired_will_give_registerRequiredAtThatLevel_to_a_tree(self):
        lexer = Lexer('{ x = y + 8 * 16 / 180 - 20 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        if token[0].id == '{':
            token = token[0].data[0]
        self.byteCodeGenerator.injectRegisterRequired(token)

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
        self.byteCodeGenerator.injectRegisterRequired(token)

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

"""
#These Test Code Might be useful in future(Do not Remove, admin:Jing Wen)
def xtest_generateByteCode_will_return_the_byteCode_in_a_list(self):
        lexer = Lexer('2 + 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.byteCodeGenerator.initGeneration(token)
        dataList = token.generateByteCode()
        self.assertEqual('0xff000002', dataList[0])
        self.assertEqual('0xff010003', dataList[1])
        self.assertEqual('0xfc020001', dataList[2])


    def xtest_generateByteCode_will_return_the_byteCode_in_a_list_for_a_multiply_expression(self):
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

    def xtest_generateByteCode_will_modify_the_byteCode_to_store_value_in_different_register(self):
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

    def xtest_generateByteCode_will_return_the_byteCode_in_a_list_with_alonger_expression(self):
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


    def test_generateByteCode_will_understand_declaration_and_generate_reservation_byteCode(self):
        lexer = Lexer('int x', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.byteCodeGenerator.initGeneration()
        dataList = token[0].generateByteCode()
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 4), dataList[0])

    def test_generateByteCode_will_generate_multiple_byteCode_for_a_multiple_declaration(self):
        lexer = Lexer('int x , y , z', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.byteCodeGenerator.initGeneration()
        dataList = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 12), dataList[0])

    def test_generateByteCode_will_generate_code_to_initialize_the_(self):
        lexer = Lexer('int x = 2', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        dataList = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 4), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 2), dataList[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[2])

    def test_generateByteCode_will_generate_code_for_multiple_initialization(self):
        lexer = Lexer('int x = 3 , y = 5 , z = 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        dataList = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 12), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), dataList[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 5), dataList[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), dataList[4])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 10), dataList[5])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 12), dataList[6])


    def test_generateByteCode_will_generate_code_initialization_and_assignment(self):
        lexer = Lexer('{ int x = 3 ; \
                      int y = 15 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        dataList = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), dataList[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 15), dataList[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), dataList[4])

    def xtest_generateByteCode_will_generate_for_expression_with_add_command(self):
        lexer = Lexer('{ int x = 3 ;\
                      int y = 15 ; \
                      x = y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        dataList = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), dataList[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 15), dataList[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), dataList[4])


    def test_generateByteCode_will_generate_for_an_arithmetic_statements(self):
        lexer = Lexer('{ int x = 20 ;\
                      int y = 35 ; \
                      x = 5 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        dataList = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 20), dataList[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 35), dataList[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), dataList[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister(0, 7, 4), dataList[5])
        self.assertEqual(self.byteCodeGenerator.loadValue(1, 5), dataList[6])
        self.assertEqual(self.byteCodeGenerator.storeValue(1, 0), dataList[7])

    def test_generateByteCode_will_generate_byteCodes_for_an_add_expression(self):
        lexer = Lexer('{ int x = 3 ;\
                      int y = 15 ; \
                      x = y + 8 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        dataList = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), dataList[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), dataList[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 15), dataList[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), dataList[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister(0, 7, 8), dataList[5])
        self.assertEqual(self.byteCodeGenerator.loadValue(1, 8), dataList[6])
        self.assertEqual(self.byteCodeGenerator.addRegisters(1, 0), dataList[7])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), dataList[8])

"""
