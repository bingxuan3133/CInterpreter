__author__ = 'admin'

import unittest
from VirtualMachine import *
from ByteCodeGenerator import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_VMStep(self):
        bytecode = []
        bytecode.append(ByteCodeGenerator.dumpRegisterHex(None, [7]))  # hacked bytecode to display r7 value
        bytecode.append(ByteCodeGenerator.dumpRegisterHex(None, [7]))  #
        bytecode.append(ByteCodeGenerator.halt(None))

        vm = VirtualMachine()
        cbytecodes = vm.convertToCArray(bytecode)
        cCharArray_t = c_char * 300
        cCharArray = cCharArray_t(0)
        cPtr = c_char_p
        cPtr = cCharArray
        vm.dumpBytecodes(bytecode)

        vm.dumpBytecode(bytecode[0])
        vm.dumpBytecode(bytecode[1])
        vm.dumpBytecode(bytecode[2])

if __name__ == '__main__':
    unittest.main()
