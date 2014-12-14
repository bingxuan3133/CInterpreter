#include "Disassembler.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>
#include <string.h>

void (*disassemble[256])(char*, int)  = { [LDR_IMM] = disassembleLdrImm,
                                          [LDR_MEM] = disassembleLdrMem,
                                          [STR_MEM] = disassembleStrMem,
                                          [MOV_REG] = disassembleMovReg,
                                          [LDR_MEM_SAFE] = disassembleLdrMemSafe,
                                          [STR_MEM_SAFE] = disassembleStrMemSafe,
                                          [LDM] = disassembleLdm,
                                          [STM] = disassembleStm
                                          };
//

/**
 *  This function disassemble multiple bytecodes into readable assembly code
 *  Input:    *strBuffer    address of string buffer that is provided by user to store assembly code into
 *            *bytecode     address of bytecode that is going to be disassembled into assembly code
 */
int disassembleBytecodes(char *strBuffer, int *bytecode) {
  while(*bytecode != 0xFFFFFFFF) {
    while(*strBuffer != '\0')  // Find \0 to write
      strBuffer++;
    disassemble[(char)*bytecode](strBuffer, *bytecode);
    while(*strBuffer != '\0')  // Find \0 to write
      strBuffer++;
    bytecode++;
    if(*bytecode != 0xFFFFFFFF)   // remove \n for last line
      sprintf(strBuffer, "\n");   // add \n for each disassembled bytecode
  }
}

/**
 *  This function disassemble bytecode into readable assembly code
 *  Input:    *strBuffer    address of string buffer that is provided by user to store assembly code into
 *            *bytecode     address of bytecode that is going to be disassembled into assembly code
 */
int disassembleBytecode(char *strBuffer, int *bytecode) {
  disassemble[(char)*bytecode](strBuffer, *bytecode);
}

void disassembleLdrImm(char *strBuffer, int bytecode) {
  int regIndex = getBits(bytecode, 10, 3);
  int value = bytecode>>11;
  sprintf(strBuffer, "ldr r%d #%d", regIndex, value);
}

void disassembleLdrMem(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeLoaded = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = getBits(bytecode, 31, 18);
  sprintf(strBuffer, "ldr r%d [r%d + #%d]", registerToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleStrMem(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeStored = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = getBits(bytecode, 31, 18);
  sprintf(strBuffer, "str r%d [r%d + #%d]", registerToBeStored, referenceRegister, relativeAddress);
}

void disassembleMovReg(char *strBuffer, int bytecode) {
  int destination = getBits(bytecode, 10, 3);
  int attrib = getBits(bytecode, 12, 2);
  int source = getBits(bytecode, 15, 3);
  int shift = getBits(bytecode, 17, 2);
  int imm = getBits(bytecode, 22, 5); // number of shift 0 ~ 3

  char attribString[6];
  char shiftString[15];

  if(imm == NOP) sprintf(shiftString, "NOP");
  else if(shift == LSR) sprintf(shiftString, "LSR %d", imm);
  else if(shift == LSL) sprintf(shiftString, "LSL %d", imm);
  else if(shift == ASR) sprintf(shiftString, "ASR %d", imm);
  else if(shift == RR) sprintf(shiftString, "RR %d", imm);
  
  if(attrib == DATA) sprintf(attribString, "");
  else if(attrib == BASE) sprintf(attribString, ".base");
  else if(attrib == LIMIT) sprintf(attribString, ".limit");
  
  sprintf(strBuffer, "mov r%d%s r%d %s", destination, attribString, source, shiftString);
}

void disassembleLdrMemSafe(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeLoaded = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = getBits(bytecode, 31, 18);
  sprintf(strBuffer, "ldrs r%d [r%d + #%d]", registerToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleStrMemSafe(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeStored = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = getBits(bytecode, 31, 18);
  sprintf(strBuffer, "strs r%d [r%d + #%d]", registerToBeStored, referenceRegister, relativeAddress);
}

void disassembleLdm(char *strBuffer, int bytecode) {
  int referenceRegister = getBits(bytecode, 10, 3);
  int registersToBeLoaded = getBits(bytecode, 18, 8);
  int direction = getBits(bytecode, 19, 1);
  int update = getBits(bytecode, 20, 1);
  
  char regList[32] = {0};
  char directionChar;
  char updateChar;
  
  int i;
  
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeLoaded >> i)) {
      sprintf(regList, "%sr%d ", regList, i); // Keep append register at behind
    }
  }
  
  if(direction == INC) directionChar = 'i';
  else directionChar = 'd';
  
  if(update == UPDATE) updateChar = '!';
  else updateChar = ' ';

  sprintf(strBuffer, "ldm%c r%d%c [%s]", directionChar, referenceRegister, updateChar, regList);
}

void disassembleStm(char *strBuffer, int bytecode) {
  int referenceRegister = getBits(bytecode, 10, 3);
  int registersToBeStored = getBits(bytecode, 18, 8);
  int direction = getBits(bytecode, 19, 1);
  int update = getBits(bytecode, 20, 1);
  
  char regList[32] = {0};
  char directionChar;
  char updateChar;
  
  int i;
  
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeStored >> i)) {
      sprintf(regList, "%sr%d ", regList, i); // Keep append register at behind
    }
  }
  
  if(direction == INC) directionChar = 'i';
  else directionChar = 'd';
  
  if(update == UPDATE) updateChar = '!';
  else updateChar = ' ';
  sprintf(strBuffer, "stm%c r%d%c [%s]", directionChar, referenceRegister, updateChar, regList);
}