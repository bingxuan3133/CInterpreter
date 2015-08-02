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

from DeclarationContext import *
from FlowControlContext import *
from RegisterAllocator import *
from InformationInjector import *
from ByteCodeGenerator import *

import struct
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

        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext,self.context]
        self.expressionContext.addInfixOperator('=', 20)

        self.expressionContext.addInfixOperator('==', 10)
        self.expressionContext.addInfixOperator('<', 10)
        self.expressionContext.addInfixOperator('<=', 10)
        self.expressionContext.addInfixOperator('>', 10)
        self.expressionContext.addInfixOperator('>=', 10)
        self.expressionContext.addInfixOperator('&&', 5)

        self.expressionContext.addInfixOperator('|',40)
        self.expressionContext.addInfixOperator('%',40)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addInfixOperator('/', 100)
        self.expressionContext.addGroupOperator('(',0)
        self.expressionContext.addOperator(')',0)
        self.declarationContext.addInt('int', 0)
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

    def test_generateByteCode_will_understand_declaration_and_generate_reservation_byteCode(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        self.informationInjector.injectRegisterRequired(token[0])
        self.byteCodeGenerator.initGeneration()
        byteCodes = token[0].generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 4]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.subRegister([7, 7, 0]), byteCodes[1])

    def test_generateByteCode_will_generate_multiple_byteCode_for_a_multiple_declaration(self):
        lexer = LexerStateMachine('int x , y , z ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.byteCodeGenerator.initGeneration()
        token[0].generateByteCode()
        token[1].generateByteCode()
        byteCodes = token[2].generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 12]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.subRegister([7, 7, 0]), byteCodes[1])

    def test_generateByteCode_will_generate_code_in_the_list_form(self):
        """
                    =(max=2,min=2)
            /                       \
            x(max=1,min=1)       5 (max=1,min=1)
        """

        lexer = LexerStateMachine(' x = 5 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)

        self.byteCodeGenerator.variablesInThisAST['x'] =4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]), byteCodes[2])

    def test_generateByteCode_will_generate_code_to_initialize_the_(self):
        lexer = LexerStateMachine('int x = 2;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.byteCodeGenerator.initGeneration()
        self.informationInjector.injectRegisterRequired(token[0])
        token[0].generateByteCode()
        self.informationInjector.injectRegisterRequired(token[1])
        byteCodes = token[1].generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 4]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.subRegister([7, 7, 0]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]), byteCodes[4])


    def test_generateByteCode_will_generate_code_for_multiple_initialization(self):
        lexer = LexerStateMachine('int x = 3 , y = 5 , z = 10 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.byteCodeGenerator.initGeneration()
        for subTree in token:
            self.informationInjector.injectRegisterRequired(subTree)
            byteCodes = subTree.generateByteCode()
            self.byteCodeGenerator.mapping.reset()

        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 12]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.subRegister([7, 7, 0]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 8]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 12]), byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]), byteCodes[10])

    def test_generateByteCode_will_return_the_byteCode_in_a_list_for_a_multiply_expression(self):
        lexer = LexerStateMachine('3 * 4 + 2 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 3]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]), byteCodes[4])

    def test_generateByteCode_will_return_the_byteCode_in_a_list_with_a_longer_expression(self):
        lexer = LexerStateMachine('3 * 4 + 2 - 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.byteCodeGenerator.mapping.registerFromLeft = 5
        self.byteCodeGenerator.mapping.registerLeft = 1
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.informationInjector.injectRegisterRequired(token)

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b011100]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([2, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([2, 2, 5]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.addRegister([2, 2, 5]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.subRegister([5, 2, 5]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b011100]), byteCodes[8])


    def test_generateByteCode_will_push_the_register_two_times(self):
        """
                    =(max=4,min=2)
            /                       \
            x(max=1,min=1)       * (max=3,min=2)<- min is hardcoded to 6, max is hardcoded to 6 so that the push will works
                            /                       \
                        * (max=2,min=2)        10 (max=1,min=1)
                    /                     \
            8 (max=1,min=1)               9 (max=1,min=1)
        """
        lexer = LexerStateMachine(' x = 8 * 9 * 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        token.minRequiredRegister = 4
        token.data[1].minRequiredRegister = 6
        token.data[1].maxRequiredRegister = 6
        self.byteCodeGenerator.mapping.registerLeft = 1
        self.byteCodeGenerator.mapping.registerFromLeft = 5
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b011100]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b000011]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 8]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 9]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([2, 0, 5]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b000011]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.storeRegister([2, 5]), byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b011100]), byteCodes[10])



    """
#These Test Code Might be useful in future(Do not Remove, admin:Jing Wen)


    def test_generateByteCode_will_generate_code_initialization_and_assignment(self):
        lexer = LexerStateMachine('{ int x = 3 ; \
                      int y = 15 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        byteCodes = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 15), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), byteCodes[4])

    def xtest_generateByteCode_will_generate_for_expression_with_add_command(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                      int y = 15 ; \
                      x = y ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        byteCodes = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 15), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), byteCodes[4])


    def test_generateByteCode_will_generate_for_an_arithmetic_statements(self):
        lexer = LexerStateMachine('{ int x = 20 ;\
                      int y = 35 ; \
                      x = 5 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        byteCodes = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 20), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 35), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister(0, 7, 4), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue(1, 5), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.storeValue(1, 0), byteCodes[7])

    def test_generateByteCode_will_generate_byteCodes_for_an_add_expression(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                      int y = 15 ; \
                      x = y + 8 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        byteCodes = self.byteCodeGenerator.generateByteCode(token)
        self.assertEqual(self.byteCodeGenerator.subRegister(7, 8), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 3), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue(0, 15), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 8), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister(0, 7, 8), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue(1, 8), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.addRegisters(1, 0), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.storeValue(0, 7, 4), byteCodes[8])

"""

    def test_generateByteCode_will_generate_code_for_push_the_working_register_into_the_stack(self):

        """
                    =(max=2,min=2)
            /                       \
            x(max=1,min=1)       5 (max=1,min=1)
        """

        lexer = LexerStateMachine(' x = 5 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.mapping.registerFromLeft = 5
        self.byteCodeGenerator.mapping.registerLeft = 1
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b010000]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadRegister([4, 7, 4]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 4]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b010000]), byteCodes[4])

    def test_generateByteCode_will_push_the_register_at_the_second_token(self):
        """
                    =(max=4,min=2)
            /                       \
            x(max=1,min=1)       + (max=3,min=2)
                            /                       \
                        + (max=2,min=2)        20 (max=1,min=1)
                    /                     \
            5 (max=1,min=1)               10 (max=1,min=1)
        """
        lexer = LexerStateMachine(' x = 5 + 10 + 20', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.mapping.registerFromLeft = 5
        self.byteCodeGenerator.mapping.registerLeft = 1
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b011100]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([2, 5]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.addRegister([2, 2, 5]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 20]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.addRegister([2, 2, 5]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.storeRegister([2, 5]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b011100]), byteCodes[8])

    def test_generateByteCode_will_push_the_register_when_the_registers_available_is_not_enough_at_the_begining(self):
        """
                    =(max=4,min=2) <- min is hardcoded to 4
            /                       \
            x(max=1,min=1)       * (max=3,min=2)
                            /                       \
                        * (max=2,min=2)        10 (max=1,min=1)
                    /                     \
            8 (max=1,min=1)               9 (max=1,min=1)
        """
        lexer = LexerStateMachine(' x = 8 * 9 * 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.mapping.registerFromLeft = 5
        self.byteCodeGenerator.mapping.registerLeft = 1
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b011100]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([2, 8]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 9]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([2, 2, 5]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([2, 2, 5]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.storeRegister([2, 5]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b011100]), byteCodes[8])

    def test_generateByteCode_will_push_the_register_two_times_with_multiply(self):
        """
                    =(max=4,min=2)
            /                       \
            x(max=1,min=1)       * (max=3,min=2)<- min is hardcoded to 6, max is hardcoded to 6 so that the push will works
                            /                       \
                        * (max=2,min=2)        10 (max=1,min=1)
                    /                     \
            8 (max=1,min=1)               9 (max=1,min=1)
        """
        lexer = LexerStateMachine(' x = 8 * 9 * 10', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        token.minRequiredRegister = 4
        token.data[1].minRequiredRegister = 6
        token.data[1].maxRequiredRegister = 6
        self.byteCodeGenerator.mapping.registerLeft = 1
        self.byteCodeGenerator.mapping.registerFromLeft = 5
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b011100]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.storeMultiple([7, 0b000011]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 8]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 9]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([2, 0, 5]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b000011]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.storeRegister([2, 5]), byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.loadMultiple([7, 0b011100]), byteCodes[10])

    def test_generateByteCode_will_make_byteCode_for_comparison(self):
        lexer = LexerStateMachine(' x == 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[2])

    def test_generateByteCode_will_create_byteCode_for_comparison_with_expression_on_right_side(self):
        lexer = LexerStateMachine(' x == 3 - 12', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 3]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 12]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.subRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[4])

    def test_generateByteCode_will_create_byteCode_for_comparison_with_expression_on_right_side_and_left_side(self):
        lexer = LexerStateMachine(' x * 3== 3 / 12', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7,4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([1, 3]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 12]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.divideRegister([5, 1, 5]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[6])

    def test_generateByteCode_will_make_byteCode_for_identifier_comparison(self):
        lexer = LexerStateMachine(' x == y', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.variablesInThisAST['y'] = 8

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 8]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[2])

    def test_generateByteCode_will_make_byteCode_for_less_than_expression(self):
        lexer = LexerStateMachine(' x < 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareIsLessThan([0, 0, 5]), byteCodes[2])

    def test_generateByteCode_will_make_byteCode_for_less_than_or_equal_expression(self):
        lexer = LexerStateMachine(' x <=  3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareIsLessThanOrEqual([0, 0, 5]), byteCodes[2])

    def test_generateByteCode_will_make_byteCode_for_greater_Than_expression(self):
        lexer = LexerStateMachine(' x >  3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareIsGreaterThan([0, 0, 5]), byteCodes[2])

    def test_generateByteCode_will_make_byteCode_for_greater_Than_or_equal_expression(self):
        lexer = LexerStateMachine(' y >=  300', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['y'] = 16

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 16]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 300]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareIsGreaterThanOrEqual([0, 0, 5]), byteCodes[2])

    def test_generateByteCode_will_produce_byteCode_for_a_complex_comparison_expression(self):
        lexer = LexerStateMachine(' y >=  300 && x == 100', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 25
        self.byteCodeGenerator.variablesInThisAST['y'] = 16

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 16]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 300]),byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareIsGreaterThanOrEqual([0, 0, 5]),byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadRegister([1, 7, 25]),byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 100]),byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.compareRegister([5, 1, 5]),byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.orRegister([0, 0, 5]),byteCodes[6])



    def test_generateByteCode_will_make_byteCode_for_this_simple_equation(self):
        lexer = LexerStateMachine(' x = 2 + 3 * 4 / 5', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 3]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.divideRegister([0, 0, 5]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.storeRegister([0, 5]), byteCodes[8])

    def test_generateByteCode_will_make_byteCode_for_this_simple_equation_with_braces(self):
        lexer = LexerStateMachine(' x = 2 + 3 * (4 / 5)', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.divideRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.storeRegister([0, 5]), byteCodes[8])


    def test_generateByteCode_will_make_byteCode_for_the_expression_that_contain_braces_in_the_middle_of_the_expression(self):
        lexer = LexerStateMachine(' x = 123 * (456 + 145) / (150- 200)', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 456]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 145]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 123]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]),byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadValue([1, 150]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 200]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.subRegister([5, 1, 5]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.divideRegister([0, 0, 5]), byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]), byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.storeRegister([0, 5]), byteCodes[10])
        
    def test_generateByteCode_for_this_long_expression(self):
        lexer = LexerStateMachine('2+((((3|4)%5)*(6/7))-8)', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 3]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.orRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.modulusRegister([0, 0, 5]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadValue([1, 6]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 7]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.divideRegister([5, 1, 5]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 8]), byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.subRegister([0, 0, 5]), byteCodes[10])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[11])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]), byteCodes[12])

    def test_generateByteCode_for_the_equation_that_contain_floating_point(self):
        lexer = LexerStateMachine('x = 2.3 + 27.5', self.context)
        float1 = struct.pack('!f', 2.3)
        float2 = struct.pack('!f', 27.5)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.variablesInThisAST['x'] = 8
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadFloatingPoint([0, float1[0],float1[1]]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadFloatingPoint([1, float1[2],float1[3]]),byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.loadFloatingPoint([5, float2[0],float2[1]]),byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadFloatingPoint([4, float2[2],float2[3]]),byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.addFloatingRegister([1,2,3,4]),byteCodes[4])


if __name__ == '__main__':
    unittest.main()
