__author__ = 'admin'

from ctypes import *

class C_Exception(Structure):
    _fields_ = [("errMsg", c_char_p), ("errCode", c_uint), ("pc", c_uint), ("bc", c_int)]

class VirtualMachine:
    def __init__(self):
        self.vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')
        cCharArray100_t = c_char * 1024
        cBuffer = cCharArray100_t(0)
        self.cPtr = c_char_p(None)
        self.cPtr = cBuffer
        self.vmdll.VMinit(100, self.cPtr)  # replace cPtr with None if printing in VM is desired

    def convertToCArray(self, bytecodeList):
        size = len(bytecodeList)
        cBytecodeList_t = c_int * size
        cBytecodeList = cBytecodeList_t(*bytecodeList)
        return cBytecodeList

    def VMLoad(self, mixedList):  # proxy function to interact with real VM
        self.vmdll.VMLoad.restype = POINTER(c_int)
        bytecodeList = []
        for item in mixedList:
            if isinstance(item, str):
                print(item)
            else:
                print(format(item, '08x') + '   ' + self.disassembleBytecode(item))
                bytecodeList.append(item)
        cBytecodeList = self.convertToCArray(bytecodeList)
        bytecodeAddress = self.vmdll.VMLoad(cBytecodeList, len(cBytecodeList))
        return bytecodeAddress

    def VMLoadAppend(self, mixedList):  # proxy function to interact with real VM
        self.vmdll.VMLoad.restype = POINTER(c_int)
        bytecodeList = []
        for item in mixedList:
            if isinstance(item, str):
                print(item)
            else:
                print(format(item, '08x') + '   ' + self.disassembleBytecode(item))
                bytecodeList.append(item)
        cBytecodeList = self.convertToCArray(bytecodeList)
        bytecodeAddress = self.vmdll.VMLoadAppend(cBytecodeList, len(cBytecodeList))
        return bytecodeAddress

    def VMStep(self):  # proxy function to interact with real VM
        #vmstep.argtypes = [POINTER(c_int)]
        self.vmdll.VMStep.restype = POINTER(C_Exception)
        self.vmdll.VMgetBytecode.restype = c_int
        exception = self.vmdll.VMStep()
        bytecode = self.vmdll.VMgetBytecode()
        print(format(bytecode, '08x') + '   ' + self.disassembleBytecode(bytecode))
        if bool(exception):
            raise RuntimeError(exception.contents.errMsg.decode('ASCII'))

    def VMRun(self):  # proxy function to interact with real VM
        #vmstep.argtypes = [POINTER(c_int)]
        self.vmdll.VMRun.restype = POINTER(C_Exception)
        exception = self.vmdll.VMRun()
        if bool(exception):
            raise RuntimeError(exception.contents.errMsg.decode('ASCII'))

    def dumpBytecodes(self, bytecodeList):  # proxy function to interact with real VM
        for bytecode in bytecodeList:
            self.dumpBytecode(bytecode)

    def dumpBytecode(self, bytecode):  # proxy function to interact with real VM
        cCharArray100_t = c_char * 100
        cBuffer = cCharArray100_t(0)
        cPtr = c_char_p(None)
        cPtr = cBuffer
        self.vmdll.disassembleBytecode(cPtr, c_int(bytecode))
        print(cPtr.value.decode('ascii'))

    def disassembleBytecode(self, bytecode):  # proxy function to interact with real VM
        cCharArray100_t = c_char * 100
        cBuffer = cCharArray100_t(0)
        cPtr = c_char_p(None)
        cPtr = cBuffer
        self.vmdll.disassembleBytecode(cPtr, c_int(bytecode))
        return cPtr.value.decode('ascii')
