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
        self.defaultContext.addKeyword('int')
        self.expressionContext = ExpressionContext(self.manager)
        self.expressionContext.addOperator(',', 0)

        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)

        self.expressionContext.addInfixOperator('==', 10)
        self.expressionContext.addInfixOperator('<', 10)
        self.expressionContext.addInfixOperator('<=', 10)
        self.expressionContext.addInfixOperator('>', 10)
        self.expressionContext.addInfixOperator('>=', 10)

        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addInfixOperator('/', 100)
        self.declarationContext.addInt('int', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.expressionContext.addOperator('}', 0)
        self.expressionContext.addOperator(')', 0)
        self.flowControlContext.addIfControl('if')


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
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 2]), byteCodes[0])
        self.assertEqual(self.byteCodeGenerator.loadRegister([5, 7, 16]), byteCodes[1])
        self.assertEqual(self.byteCodeGenerator.compareRegister([0, 5]), byteCodes[2])
        self.assertEqual(self.byteCodeGenerator.branchIfFalse(), byteCodes[3])
        self.assertEqual('IF1', byteCodes[4])
        self.assertEqual('IF1', byteCodes[5])

if __name__ == '__main__':
    unittest.main()
