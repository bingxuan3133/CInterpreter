__author__ = 'Jing'

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

class TestFlowControlByteCodeGeneration(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.declarationContext = DeclarationContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)

        self.expressionContext = ExpressionContext(self.manager)
        self.expressionContext.addOperator(',', 0)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]
        #self.defaultContext.addKeyword('while')
        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)
        self.byteCodeGenerator = ByteCodeGenerator(self.context, self.manager)
        self.informationInjector = InformationInjector()

    def test_generateByteCode_will_make_code_for_if(self):
        lexer = LexerStateMachine('if(x==2 ) { }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 16

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 16]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.branch([0]), byteCodes[4])

    def test_generateByteCode_will_make_code_for_if_with_statements(self):
        lexer = LexerStateMachine('if(x==2 ) { x = 123 + 4567 * 90 /121;\n y = x +1234;\n x = y *x;}', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 16
        self.byteCodeGenerator.variablesInThisAST['y'] = 20

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 16]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[2])

        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.branch([19]), byteCodes[4])

        self.assertEqual(self.byteCodeGenerator.loadValue([0, 4567]),byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 90]),byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 121]), byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.divideRegister([0,0,5]),byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 123]), byteCodes[10])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]),byteCodes[11])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 16]),byteCodes[12])
        self.assertEqual(self.byteCodeGenerator.storeRegister([0, 5]), byteCodes[13])

        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 16]),byteCodes[14])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 1234]),byteCodes[15])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]),byteCodes[16])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 20]),byteCodes[17])
        self.assertEqual(self.byteCodeGenerator.storeRegister([0, 5]),byteCodes[18])

        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 20]),byteCodes[19])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 16]),byteCodes[20])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[21])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 16]),byteCodes[22])
        self.assertEqual(self.byteCodeGenerator.storeRegister([0, 5]),byteCodes[23])

    def test_generateByteCode_will_make_code_for_if_with_else_that_attacted_statements(self):
        lexer = LexerStateMachine('if ( x == 100) \n{x = 1000;}\n else \n {x = 2000;} ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5,100]),byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]),byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]),byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.branch([3]),byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]),byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5,1000]),byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]),byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2000]),byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[10])


    def test_byteCodeGenerator_will_generate_code_for_the_while_loop_that_contain_no_statements(self):
        lexer = LexerStateMachine('while (x+ (3 - 4 ) * 100 == 200 / 100 * (310 -400) + 120) { } ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 3]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]),byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.subRegister([0, 0, 5]),byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 100]),byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]),byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 4]),byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]),byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadValue([1, 200]),byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 100]),byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.divideRegister([1, 1, 5]),byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.loadValue([2, 310]),byteCodes[10])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 400]),byteCodes[11])
        self.assertEqual(self.byteCodeGenerator.subRegister([5, 2, 5]),byteCodes[12])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([1, 1, 5]),byteCodes[13])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 120]),byteCodes[14])
        self.assertEqual(self.byteCodeGenerator.addRegister([5, 1, 5]),byteCodes[15])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]),byteCodes[16])
        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]),byteCodes[17])
        self.assertEqual(self.byteCodeGenerator.branch([0]),byteCodes[18])

    def test_byteCodeGenerator_will_generate_code_for_while_loop_with_statements(self):
        lexer = LexerStateMachine('while (x == 2) { x = 100;\n y = 1000;\n z=2000;} ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.variablesInThisAST['y'] = 8
        self.byteCodeGenerator.variablesInThisAST['z'] = 12

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadRegister([0,7,4]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]),byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]),byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]),byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.branch([10]),byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]),byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 100]),byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 8]),byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 1000]),byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[10])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 12]),byteCodes[11])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2000]),byteCodes[12])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[13])
        self.assertEqual(self.byteCodeGenerator.branch([-10]),byteCodes[14])

    def test_generateByteCode_will_generate_code_for_do_while_loop(self):
        lexer = LexerStateMachine('do{ }while(x == 321); ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.variablesInThisAST['y'] = 8
        self.byteCodeGenerator.variablesInThisAST['z'] = 12

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 321]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.branch([-5]), byteCodes[4])

    def test_generateByteCode_will_generate_code_for_do_while_loop_with_statements_inside(self):
        lexer = LexerStateMachine('do{x = 1500;\
                                    y = 2500;\
                                    z = 5500;\
                                    }while(x == 321); ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.variablesInThisAST['y'] = 8
        self.byteCodeGenerator.variablesInThisAST['z'] = 12

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]),byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 1500]),byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 8]),byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2500]),byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 12]),byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 5500]),byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.storeRegister([5, 0]),byteCodes[8])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[9])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 321]), byteCodes[10])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 0, 5]), byteCodes[11])
        self.assertEqual(self.byteCodeGenerator.branchIfTrue([1, 0]), byteCodes[12])
        self.assertEqual(self.byteCodeGenerator.branch([-14]), byteCodes[13])

if __name__ == '__main__':
    unittest.main()
