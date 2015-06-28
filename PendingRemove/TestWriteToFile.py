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
from writeToFile import *
from InformationInjector import *

class MyTestCase(unittest.TestCase):
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
        self.writeFile = writeToFile(self.byteCodeGenerator)
        self.informationInjector = InformationInjector()
    def xtest_generateByteCode_will_generate_code_for_push_the_working_register_into_the_stack(self):

        """
                    =(max=2,min=2)
            /                       \
            x(max=1,min=1)       5 (max=1,min=1)
        """

        lexer = LexerStateMachine(' x = 5 ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        token.leftValue = 1
        token.rightValue = 1
        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.oracle.workingRegisterCounter = 5
        self.byteCodeGenerator.oracle.registerLeft = 1
        self.byteCodeGenerator.oracle.registerStatus = [1, 1, 1, 1, 1, 0]
        self.byteCodeGenerator.registersInThisAST['x'] = 4

        self.byteCodeGenerator.initGeneration()
        token.generateByteCode()
        self.writeFile.writeAllToFile()



if __name__ == '__main__':
    unittest.main()
