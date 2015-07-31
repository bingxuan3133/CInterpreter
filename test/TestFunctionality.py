__author__ = 'admin'

import unittest
import os
from LexerStateMachine import *
from ctypes import *
from Parser import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *
from GeneratorAPI import *
from VirtualMachine import *

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
        self.expressionContext.addInfixOperator('==', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addOperator(')', 0)
        self.flowControlContext.addWhileControl('while', 0)
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

        self.generator = GeneratorAPI(self.context, self.manager)
        self.byteCodeGenerator = ByteCodeGenerator(self.context, self.manager)
        self.informationInjector = InformationInjector()

    def test_call_directly_to_dll_VMStep(self):
        lexer = LexerStateMachine('int x = 5;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        byteCodes =self.generator.generateCode(token)
        byteCodes.insert(0, self.byteCodeGenerator.dumpRegisterHex([7]))  # hacked bytecode to display r7 value
        byteCodes.insert(2, self.byteCodeGenerator.dumpRegisterHex([7]))  #

        vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')

        byteCodes.append(0xffffffff)  # to halt the VM
        byteCodesSize = len(byteCodes)
        cByteCodes_t = c_uint * byteCodesSize
        cByteCodes = cByteCodes_t(*byteCodes)

        vmdll.restype = POINTER(C_Exception)

        exception = vmdll._VMStep(cByteCodes)
        exception = vmdll._VMStep(cByteCodes)
        exception = vmdll._VMStep(cByteCodes)
        exception = vmdll._VMStep(cByteCodes)

    def test_call_directly_to_dll_VMRun(self):
        lexer = LexerStateMachine('int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        byteCodes =self.generator.generateCode(token)
        vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')

        byteCodes.append(0xffffffff)  # to halt the VM
        bytecodesSize = len(byteCodes)
        cByteCodes_t = c_uint * bytecodesSize
        cByteCodes = cByteCodes_t(*byteCodes)
        vmdll._VMRun(cByteCodes)

    def test_VMStep(self):
        lexer = LexerStateMachine('int x = 5;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        byteCodes =self.generator.generateCode(token)
        byteCodes.insert(0, self.byteCodeGenerator.dumpRegisterHex([7]))  # hacked bytecode to display r7 value
        byteCodes.insert(2, self.byteCodeGenerator.dumpRegisterHex([7]))  #
        byteCodes.append(self.byteCodeGenerator.halt())

        vm = VirtualMachine()
        cbytecodes = vm.convertToCArray(byteCodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)

    def test_VMStep_should_raise_RuntimeError_given_invalid_bytecode(self):
        bytecodes = [0xfff12314]

        vm = VirtualMachine()

        try:
            cbytecodes = vm.convertToCArray(bytecodes)
            vm.VMStep(cbytecodes)
        except RuntimeError as e:
            self.assertEqual('ERROR: invalid bytecode (0xfff12314, pc = 2).', e.args)
            #self.assertEqual('ERROR: invalid bytecode (0xfff12314, pc = 2).', e.errMsg)

    def xtest_call_directly_to_dll_VMRun(self):
        lexer = LexerStateMachine('int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        byteCodes =self.generator.generateCode(token)
        vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')

        byteCodes.append(0xffffffff)  # to halt the VM
        byteCodesSize = len(byteCodes)
        cByteCodes_t = c_uint * byteCodesSize
        cByteCodes = cByteCodes_t(*byteCodes)
        vmdll._VMRun(cByteCodes)

    def test_VMStep_while_loop(self):
        lexer = LexerStateMachine('while( x == 2) {x = 100;\n y = 1000;\n z=2000;} ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        self.byteCodeGenerator.variablesInThisAST['x'] = 4
        self.byteCodeGenerator.variablesInThisAST['y'] = 8
        self.byteCodeGenerator.variablesInThisAST['z'] = 12
        bytecodes = self.generator.generateCode(token)

        vm = VirtualMachine()
        cbytecodes = vm.convertToCArray(bytecodes)

        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)
        vm.VMStep(cbytecodes)

if __name__ == '__main__':
    unittest.main()
