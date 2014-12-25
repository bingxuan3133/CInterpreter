__author__ = 'admin'

from ctypes import *

import os
from ctypes import *

print("path", os.path.abspath(__file__))

bytecodeArray_t = c_uint * 10
bytecodeArray = bytecodeArray_t()
bytecodeArray[0] = 0x0
bytecodeArray[1] = 0x100
bytecodeArray[2] = 0x320fc
bytecodeArray[3] = 0x641fc
bytecodeArray[4] = 0x0
bytecodeArray[5] = 0x100
bytecodeArray[6] = 0x10fa
bytecodeArray[7] = 0x0
bytecodeArray[8] = 0x100
bytecodeArray[9] = 0xffffffff


bytecodesPtr = c_char_p()
bytecodesPtr.value = addressof(bytecodeArray)

#vmdll = WinDLL('VirtualMachine')
vmdll = cdll.LoadLibrary('../VirtualMachine.dll')
vmdll.runVM(bytecodesPtr)

f = open('myFirstByteCode', 'rb')
#vmdll.runVMFromStream('myFirstByteCode.txt')
