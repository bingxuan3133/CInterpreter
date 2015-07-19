__author__ = 'admin'

import unittest
#from Context import *
from LexerStateMachine import *
import os
from ctypes import *
from Parser import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *
from InformationInjector import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addShort('short', 0)
        self.declarationContext.addLong('long', 0)
        self.declarationContext.addSignedAndUnsigned('signed', 0)
        self.declarationContext.addSignedAndUnsigned('unsigned', 0)
        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

        self.byteCodeGenerator = ByteCodeGenerator(self.context, self.manager)
        self.informationInjector = InformationInjector()

    def test_something(self):
        lexer = LexerStateMachine('int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        self.informationInjector.injectRegisterRequired(token[0])
        self.byteCodeGenerator.initGeneration()
        byteCodes = token[0].generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)

        vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')

        byteCodes.append(0xffffffff)  # to halt the VM
        byteCodesSize = len(byteCodes)
        cByteCodes_t = c_uint * byteCodesSize
        cByteCodes = cByteCodes_t(*byteCodes)
        vmdll.VMRun(cByteCodes)

    def test_VMStep(self):
        lexer = LexerStateMachine('int x = 5;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        self.informationInjector.injectRegisterRequired(token[0])
        self.byteCodeGenerator.initGeneration()
        byteCodes = token[0].generateByteCode()
        byteCodes = self.byteCodeGenerator.injectPrologue(byteCodes)

        vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')

        byteCodes.append(0xffffffff)  # to halt the VM
        byteCodesSize = len(byteCodes)
        print(byteCodes)
        cByteCodes_t = c_uint * byteCodesSize
        cByteCodes = cByteCodes_t(*byteCodes)
        programCounter = c_uint(0)

        vmdll.VMStep(cByteCodes[0])
        vmdll.VMStep(cByteCodes[1])

if __name__ == '__main__':
    unittest.main()
