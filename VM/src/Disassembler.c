#include "VirtualMachine.h"
#include "Disassembler.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>
#include <string.h>

void (*disassemble[256])(char*, int)  = { [DUMPR] = disassembleDumpr,
                                          [DUMPR_HEX] = disassembleDumprHex,
                                          [LDR_IMM] = disassembleLdrImm,
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
                                          [XOR] = disassembleXor,
                                          [FLDR_IMM] = disassembleFldrImm,
                                          [FLDR] = disassembleFldr,
                                          [FSTR] = disassembleFstr,
                                          [FADD] = disassembleFadd,
                                          [FSUB] = disassembleFsub,
                                          [FMUL] = disassembleFmul,
                                          [FDIV] = disassembleFdiv,
                                          [BRA] = disassembleBra,
                                          [BRA_IF_TRUE] = disassembleBit,
                                          [CMPE] = disassembleCmpe,
                                          [CMPLT] = disassembleCmplt,
                                          [CMPLTE] = disassembleCmplte,
                                          [CMPGT] = disassembleCmpgt,
                                          [CMPGTE] = disassembleCmpgte,
                                          [HALT] = disassembleHalt
                                          };
//

/**
 *  This function disassemble multiple bytecodes into readable assembly code
 *  Input:    *strBuffer    address of string buffer that is provided by user to store assembly code into
 *            *bytecode     address of bytecode that is going to be disassembled into assembly code
 *  Return:   1   bytecode can be disassembled
 *            0   bytecode cannot be disassembled
 */
int __declspec(dllexport) disassembleBytecodes(char *strBuffer, int *bytecode) {
  while((unsigned char)bytecode[getProgramCounter()] != halt()) {
    disassembleBytecode(strBuffer, bytecode[getProgramCounter()]);
    while(*strBuffer != '\0')  // Find \0 to write and add newline
      strBuffer++;
    sprintf(strBuffer, "\n");
    moveProgramCounter(1);
    while(*strBuffer != '\0')  // Find \0 to write
      strBuffer++;
  }
  disassembleHalt(strBuffer, bytecode[getProgramCounter()]);
}

/**
 *  This function disassemble bytecode into readable assembly code
 *  Input:    *strBuffer    address of string buffer that is provided by user to store assembly code into
 *            bytecode      bytecode that is going to be disassembled into assembly code
 *  Return:   1   bytecode can be disassembled
 *            0   bytecode cannot be disassembled
 */
int __declspec(dllexport) disassembleBytecode(char *strBuffer, int bytecode) {
  unsigned char opcode = bytecode;
  if(opcode == halt()) {
    disassembleHalt(strBuffer, bytecode);
  } else if(opcode > MAX_INSTRUCTION) {
    disassembleDefault(strBuffer, bytecode);
  } else {
    disassemble[opcode](strBuffer, bytecode);
  }
}

/**
 *  Simpler version of disassembleBytecodes
 */
void dumpBytecodes(int *bytecode) {
  char dumpBuffer[1000] = {0};
  disassembleBytecodes(dumpBuffer, bytecode);
  printf("%s", dumpBuffer);
}

/**
 *  Simpler version of disassembleBytecode
 */
void dumpBytecode(int bytecode) {
  char dumpBuffer[500] = {0};
  unsigned char opcode = bytecode;
  disassembleBytecode(dumpBuffer, bytecode);
  printf("%s", dumpBuffer);
}

void disassembleHalt(char *strBuffer, int bytecode) {
  sprintf(strBuffer, "halt");
}

void disassembleDefault(char *strBuffer, int bytecode) {
  sprintf(strBuffer, "Invalid Bytecode! (0x%08x)", bytecode);
}

// Disassemble Functions
void disassembleDumpr(char *strBuffer, int bytecode) {
  int regIndex = getRd(bytecode);
  sprintf(strBuffer, "dumpr r%d", regIndex);
}

void disassembleDumprHex(char *strBuffer, int bytecode) {
  int regIndex = getRd(bytecode);
  sprintf(strBuffer, "dumprhex r%d", regIndex);
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

// void disassembleSubImm(char *strBuffer, int bytecode) {
  // int regIndex = getRd(bytecode);
  // int value = bytecode >> (8 + MAX_REG_BIT);
  // sprintf(strBuffer, "sub r%d #%d", regIndex, value);
// }

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
  int resultHighReg = getRd(bytecode);
  int resultLowReg = getR1(bytecode);
  int reg1 = getR2(bytecode);
  int reg2 = getR3(bytecode);
  sprintf(strBuffer, "mul r%d:r%d r%d r%d", resultHighReg, resultLowReg, reg1, reg2);
}
void disassembleDiv(char *strBuffer, int bytecode) {
  int resultQuotientReg = getRd(bytecode);
  int resultRemainderReg = getR1(bytecode);
  int reg1 = getR2(bytecode);
  int reg2 = getR3(bytecode);
  sprintf(strBuffer, "div r%d:r%d r%d r%d", resultQuotientReg, resultRemainderReg, reg1, reg2);
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

// floating point

void disassembleFldrImm(char *strBuffer, int bytecode) {
  int regIndex = getRd(bytecode);
  int pc = getProgramCounter();
  long long high_unint32 = (unsigned long long)getVMBytecode(pc + 2)<<32;
  long long low_unint32 = (unsigned long long)getVMBytecode(pc + 1);
  double value = high_unint32 + low_unint32;
  moveProgramCounter(2);
  sprintf(strBuffer, "fldr r%d #%f", regIndex, value);
}

void disassembleFldr(char *strBuffer, int bytecode) {
  int dRegisterToBeLoaded = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  sprintf(strBuffer, "fldr d%d [r%d + #%d]", dRegisterToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleFstr(char *strBuffer, int bytecode) {
  int *ref;
  int dRegisterToBeStored = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  sprintf(strBuffer, "fstr d%d [r%d + #%d]", dRegisterToBeStored, referenceRegister, relativeAddress);
}

void disassembleFadd(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "fadd d%d d%d d%d", resultReg, reg1, reg2);
}
void disassembleFsub(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "fsub d%d d%d d%d", resultReg, reg1, reg2);
}
void disassembleFmul(char *strBuffer, int bytecode) {
  int resultHighReg = getRd(bytecode);
  int resultLowReg = getR1(bytecode);
  int reg1 = getR2(bytecode);
  int reg2 = getR3(bytecode);
  sprintf(strBuffer, "fmul d%d:d%d d%d d%d", resultHighReg, resultLowReg, reg1, reg2);
}
void disassembleFdiv(char *strBuffer, int bytecode) {
  int resultQuotientReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "fdiv d%d d%d d%d", resultQuotientReg, reg1, reg2);
}

// branch

void disassembleBra(char *strBuffer, int bytecode) {
  int relativeAddress = bytecode >> 8;
  sprintf(strBuffer, "bra #%d", relativeAddress);
}

void disassembleBit(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int relativeAddress = bytecode >> (8 + MAX_REG_BIT);
  sprintf(strBuffer, "bit r%d #%d", resultReg, relativeAddress);
}

// compare

void disassembleCmpe(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "cmpe r%d r%d r%d", resultReg, reg1, reg2);
}

void disassembleCmplt(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "cmplt r%d r%d r%d", resultReg, reg1, reg2);
}

void disassembleCmplte(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "cmplte r%d r%d r%d", resultReg, reg1, reg2);
}

void disassembleCmpgt(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "cmpgt r%d r%d r%d", resultReg, reg1, reg2);
}

void disassembleCmpgte(char *strBuffer, int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  sprintf(strBuffer, "cmpgte r%d r%d r%d", resultReg, reg1, reg2);
}
