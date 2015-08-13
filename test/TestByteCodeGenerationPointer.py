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

class TestPointerByteCodeGeneration(unittest.TestCase):
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
"""
    def test_generateByteCode_will_make_code_for_pointer_initialization(self):
        lexer = LexerStateMachine('char *ptr;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)

        self.informationInjector.injectRegisterRequired(token)
        self.byteCodeGenerator.initGeneration()
        byteCodes = token.generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)
        self.assertEqual(self.byteCodeGenerator.loadValue([0, 4]),byteCodes[0])
        """




if __name__ == '__main__':
    unittest.main()
