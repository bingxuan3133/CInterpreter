#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

void (*instruction[256])(int)  = {[DUMPR] = dumpRegister,
                                  [DUMPR_HEX] = dumpRegisterHex,
                                  [LDR_IMM] = loadRegisterWithImmediate,
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
                                  [SUB_IMM] = subtractRegisters,
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

void __declspec(dllexport) VMLoad(char* filepath, int *bytecode) {
  FILE *file;
  char fileNameBuffer[100];
  sprintf(fileNameBuffer, "%s", filepath);
  file = fopen(filepath, "r+");
  int i;
  
  *bytecode = getBytecode(file);
  while(*bytecode != 0xFFFFFFFF) {
    bytecode++;
    *bytecode = getBytecode(file);
  }
  
  fclose(file);
}

void __declspec(dllexport) VMRun(int *bytecode) {
  while(*bytecode != 0xFFFFFFFF) {
    instruction[(unsigned char)*bytecode](*bytecode);
    bytecode++;
  }
}

/**
 *  pc = Program Counter
 *
 */
void __declspec(dllexport) VMStep(int bytecode) {
  if(bytecode != 0xFFFFFFFF) {
    instruction[(unsigned char)bytecode](bytecode);
  }
}