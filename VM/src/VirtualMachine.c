#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

void (*instruction[256])(int)  = {[LDR_IMM] = loadRegisterWithLiteral,
                                  [LDR_MEM] = loadRegisterFromMemory,
                                  [STR_MEM] = storeRegisterIntoMemory,
                                  [MOV_REG] = moveRegister,
                                  [LDR_MEM_SAFE] = loadRegisterFromMemorySafe,
                                  [STR_MEM_SAFE] = storeRegisterIntoMemorySafe
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