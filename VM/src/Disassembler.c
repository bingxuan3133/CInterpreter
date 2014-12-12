#include "Disassembler.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

void (*disassemble[256])(char*, int)  = { [LDR_IMM] = disassembleLdrImm,
                                          [LDR_MEM] = disassembleLdrMem,
                                          [STR_MEM] = disassembleStrMem,
                                          [MOV_REG] = disassembleMovReg,
                                          [LDR_MEM_SAFE] = disassembleLdrMemSafe,
                                          [STR_MEM_SAFE] = disassembleStrMemSafe
                                          };
//

/**
 *  This function disassemble multiple bytecodes into readable assembly code
 *  Input:    *strBuffer    address of string buffer that is provided by user to store assembly code into
 *            *bytecode     address of bytecode that is going to be disassembled into assembly code
 */
int disassembleBytecodes(char *strBuffer, int *bytecode) {
  int operand;
  while(*bytecode != 0xFFFFFFFF) {
  operand = (*bytecode)>>8 & 0x00FFFFFF;
    while(*strBuffer != '\0')  // Find \0 to write
      strBuffer++;
    disassemble[(char)*bytecode](strBuffer, operand);
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
  int operand = (*bytecode)>>8 & 0x00FFFFFF;
  disassemble[(char)*bytecode](strBuffer, operand);
}

void disassembleLdrImm(char *strBuffer, int operand) {
  int regIndex = getBits(operand, 2, 3);
  int value = getBits(operand, 23, 21);
  if(getBits(value, 23, 1))   // value is - signed
    value = 0xFFE00000 | value;
  sprintf(strBuffer, "ldr r%d #%d", regIndex, value);
}

void disassembleLdrMem(char *strBuffer, int operand) {
  int *ref;
  int registerToBeLoaded = getBits(operand, 2, 3);
  int referenceRegister = getBits(operand, 5, 3);
  int relativeAddress = getBits(operand, 23, 18);
  sprintf(strBuffer, "ldr r%d [r%d + #%d]", registerToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleStrMem(char *strBuffer, int operand) {
  int *ref;
  int registerToBeStored = getBits(operand, 2, 3);
  int referenceRegister = getBits(operand, 5, 3);
  int relativeAddress = getBits(operand, 23, 18);
  sprintf(strBuffer, "str r%d [r%d + #%d]", registerToBeStored, referenceRegister, relativeAddress);
}

void disassembleMovReg(char *strBuffer, int operand) {
  int destination = getBits(operand, 2, 3);
  int attrib = getBits(operand, 4, 2);
  int source = getBits(operand, 7, 3);
  int shift = getBits(operand, 9, 2);
  int imm = getBits(operand, 14, 5); // number of shift 0 ~ 3

  char attribString[6];
  char shiftString[15];
  printf("%x\n", operand);
  printf("%d %d %d %d %d\n", destination, attrib, source, shift, imm);
  
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

void disassembleLdrMemSafe(char *strBuffer, int operand) {
  int *ref;
  int registerToBeLoaded = getBits(operand, 2, 3);
  int referenceRegister = getBits(operand, 5, 3);
  int relativeAddress = getBits(operand, 23, 18);
  sprintf(strBuffer, "ldrs r%d [r%d + #%d]", registerToBeLoaded, referenceRegister, relativeAddress);
}

void disassembleStrMemSafe(char *strBuffer, int operand) {
  int *ref;
  int registerToBeStored = getBits(operand, 2, 3);
  int referenceRegister = getBits(operand, 5, 3);
  int relativeAddress = getBits(operand, 23, 18);
  sprintf(strBuffer, "strs r%d [r%d + #%d]", registerToBeStored, referenceRegister, relativeAddress);
}