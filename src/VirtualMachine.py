__author__ = 'admin'

from ctypes import *

class C_Exception(Structure):
    _fields_ = [("errMsg", c_char_p), ("errCode", c_uint), ("pc", c_uint), ("bc", c_int)]

class VirtualMachine:
    def __init__(self):
        self.vmdll = cdll.LoadLibrary('../VM/build/release/out/c/VirtualMachine.dll')
        pass

    def convertToCArray(self, bytecodeList):
        size = len(bytecodeList)
        cBytecodeList_t = c_int * size
        cBytecodeList = cBytecodeList_t(*bytecodeList)
        return cBytecodeList

    def VMStep(self, cBytecodeList):  # proxy function to interact with real VM
        vmstep = self.vmdll._VMStep
        #vmstep.argtypes = [POINTER(c_int)]
        vmstep.restype = POINTER(C_Exception)
        exception = vmstep(cBytecodeList)
        if bool(exception):
            raise RuntimeError(exception.contents.errMsg)

    def VMRun(self, cBytecodeList):  # proxy function to interact with real VM
        vmrun = self.vmdll._VMRun
        #vmstep.argtypes = [POINTER(c_int)]
        vmrun.restype = POINTER(C_Exception)
        exception = vmrun(cBytecodeList)
        if bool(exception):
            raise RuntimeError(exception.contents.errMsg)

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

