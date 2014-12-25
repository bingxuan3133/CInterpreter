#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

void (*instruction[256])(int)  = {[DUMPR] = dumpRegister,
                                  [DUMPR_HEX] = dumpRegisterHex,
                                  [LDR_IMM] = loadRegisterWithLiteral,
                                  [LDR_MEM] = loadRegisterFromMemory,
                                  [STR_MEM] = storeRegisterIntoMemory,
                                  [MOV_REG] = moveRegister,
                                  [LDR_MEM_SAFE] = loadRegisterFromMemorySafe,
                                  [STR_MEM_SAFE] = storeRegisterIntoMemorySafe,
                                  [LDM] = loadMultipleRegistersFromMemory,
                                  [STM] = storeMultipleRegistersIntoMemory,
                                  [LDMS] = loadMultipleRegistersFromMemorySafe,
                                  [STMS] = storeMultipleRegistersIntoMemorySafe,
                                  [ADD] = addRegisters,
                                  [SUB] = subtractRegisters,
                                  [MUL] = multiplyRegisters,
                                  [DIV] = divideRegisters,
                                  [AND] = andRegisters,
                                  [OR] = orRegisters,
                                  [XOR] = xorRegisters
                                  };

//

int getBytecode(FILE *file) {
  int bytecode = 0;
  bytecode |= fgetc(file);
  bytecode |= fgetc(file) << 8;
  bytecode |= fgetc(file) << 16;
  bytecode |= fgetc(file) << 24;
  return bytecode;
}

void __declspec(dllexport) runVM(int *bytecode) {
  while(*bytecode != 0xFFFFFFFF) {
    instruction[(unsigned char)*bytecode](*bytecode);
    bytecode++;
  }
}

void __declspec(dllexport) runVMFromStream(FILE *file) {
  unsigned int bytecode = getBytecode(file);
  while(bytecode != 0xFFFFFFFF) {
    instruction[(unsigned char)bytecode](bytecode);
    bytecode = getBytecode(file);
  }
}

