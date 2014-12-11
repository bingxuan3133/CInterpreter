#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"

void (*instruction[256])(int)  = {[LDR_IMM] = loadRegisterWithLiteral,
                                  [LDR_MEM] = loadRegisterFromMemory,
                                  [STR_MEM] = storeRegisterIntoMemory,
                                  [MOV_REG] = moveRegister,
                                  [LDR_MEM_SAFE] = loadRegisterFromMemorySafe,
                                  [STR_MEM_SAFE] = storeRegisterIntoMemorySafe
                                  };