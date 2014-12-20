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
                                          [STM] = disassembleStm,
                                          [LDMS] = disassembleLdms,
                                          [STMS] = disassembleStms,
                                          [ADD] = disassembleAdd,
                                          [SUB] = disassembleSub,
                                          [MUL] = disassembleMul,
                                          [DIV] = disassembleDiv,
                                          [AND] = disassembleAnd,
                                          [OR] = disassembleOr,
                                          [XOR] = disassembleXor
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
    disassemble[(unsigned char)(*bytecode)](strBuffer, *bytecode);
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
  disassemble[(unsigned char)*bytecode](strBuffer, *bytecode);
}

void disassembleLdrImm(char *strBuffer, int bytecode) {
  int regIndex = getRd(bytecode);
  int value = bytecode>>(8 + MAX_REG_BIT);
  sprintf(strBuffer, "ldr r%d #%d", regIndex, value);
}

void disassembleLdrMem(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeLoaded = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  sprintf(strBuffer, "ldr r%d [r%d + #%d]", registerToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleStrMem(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeStored = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  sprintf(strBuffer, "str r%d [r%d + #%d]", registerToBeStored, referenceRegister, relativeAddress);
}

void disassembleMovReg(char *strBuffer, int bytecode) {
  int destination = getRd(bytecode);
  int source = getR1(bytecode);
  int destAttrib = getBits(bytecode, (9 + 2 * MAX_REG_BIT), 2);
  int shift = getBits(bytecode, (11 + 2 * MAX_REG_BIT), 2);
  int imm = getBits(bytecode, (16 + 2 * MAX_REG_BIT), 5); // number of shift 0 ~ 31
  char attribString[6];
  char shiftString[15];

  if(imm == NOP) sprintf(shiftString, "NOP");
  else if(shift == LSR) sprintf(shiftString, "LSR %d", imm);
  else if(shift == LSL) sprintf(shiftString, "LSL %d", imm);
  else if(shift == ASR) sprintf(shiftString, "ASR %d", imm);
  else if(shift == RR) sprintf(shiftString, "RR %d", imm);
  
  if(destAttrib == DATA) sprintf(attribString, "");
  else if(destAttrib == BASE) sprintf(attribString, ".base");
  else if(destAttrib == LIMIT) sprintf(attribString, ".limit");
  
  sprintf(strBuffer, "mov r%d%s r%d %s", destination, attribString, source, shiftString);
}

void disassembleLdrMemSafe(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeLoaded = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  sprintf(strBuffer, "ldrs r%d [r%d + #%d]", registerToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleStrMemSafe(char *strBuffer, int bytecode) {
  int *ref;
  int registerToBeStored = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  sprintf(strBuffer, "strs r%d [r%d + #%d]", registerToBeStored, referenceRegister, relativeAddress);
}

void disassembleLdm(char *strBuffer, int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeLoaded = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  
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
  int referenceRegister = getRd(bytecode);
  int registersToBeStored = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  
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

void disassembleLdms(char *strBuffer, int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeLoaded = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  
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

  sprintf(strBuffer, "ldms%c r%d%c [%s]", directionChar, referenceRegister, updateChar, regList);
}

void disassembleStms(char *strBuffer, int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeStored = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  
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
  sprintf(strBuffer, "stms%c r%d%c [%s]", directionChar, referenceRegister, updateChar, regList);
}

void disassembleAdd(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "add r%d r%d r%d", resultReg, reg1, reg2);
}

void disassembleSub(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "sub r%d r%d r%d", resultReg, reg1, reg2);
}
void disassembleMul(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "mul r%d r%d r%d", resultReg, reg1, reg2);
}
void disassembleDiv(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "div r%d r%d r%d", resultReg, reg1, reg2);
}
void disassembleAnd(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "and r%d r%d r%d", resultReg, reg1, reg2);
}
void disassembleOr(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "or r%d r%d r%d", resultReg, reg1, reg2);
}
void disassembleXor(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "xor r%d r%d r%d", resultReg, reg1, reg2);
}