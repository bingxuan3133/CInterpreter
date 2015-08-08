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
        cBytecodeList_t = c_uint * size
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

    def dumpBytecodes(self, cBytecodeList):  # proxy function to interact with real VM
        self.vmdll.dumpBytecodes(cBytecodeList)

    def disassembleBytecodes(self, cBuffer, cBytecodeList):  # proxy function to interact with real VM
        getBytecode = self.vmdll.disassembleBytecode
        getBytecode.restype = c_char_p
        getBytecode(cBuffer, cBytecodeList)
        pass


