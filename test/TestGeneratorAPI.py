__author__ = 'Jing'

import unittest
from FlowControlContext import *
from DeclarationContext import *
from DefaultContext import *
from ExpressionContext import *
from Parser import *
from GeneratorAPI import *
from ByteCodeGenerator import *


class TestGeneratorAPI(unittest.TestCase):
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
        self.generatorAPI = GeneratorAPI(self.context, self.manager)

    def test_generateByteCode_will_accept_an_AST_and_generate_code(self):
        lexer = LexerStateMachine('3 * 4 + 2 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)

        byteCodes = self.generatorAPI.generateCode(token)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 3]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.multiplyRegister([0, 0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 2]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.addRegister([0, 0, 5]), byteCodes[4])

    def test_generaByteCode_will_generate_byte_code_for_a_list_of_tokens(self):
        lexer = LexerStateMachine('x = 3;\
                                y = 4;\
                                  z=10;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.variablesInThisAST['y'] = 8
        self.byteCodeGenerator.variablesInThisAST['z'] = 12

        byteCodes = self.generatorAPI.generateCode(token)
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 4]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 3]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.assignRegister([5, 0]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 8]), byteCodes[3])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 4]), byteCodes[4])
        self.assertEqual(self.byteCodeGenerator.assignRegister([5, 0]), byteCodes[5])
        self.assertEqual(self.byteCodeGenerator.loadRegister([0, 7, 12]), byteCodes[6])
        self.assertEqual(self.byteCodeGenerator.loadValue([5, 10]), byteCodes[7])
        self.assertEqual(self.byteCodeGenerator.assignRegister([5, 0]), byteCodes[8])


if __name__ == '__main__':
    unittest.main()
