#include "Disassembler.h"
#include "Instruction.h"
#include <stdio.h>

void (*disassemble[256])(char*, int)  = { [LDR_IMM] = disassembleLdrImm,
                                          [LDR_MEM] = disassembleLdrMem,
                                          [STR_MEM] = disassembleStrMem,
                                          [MOV_REG] = disassembleMovReg
                                          };
wer


/**
 *  This function disassemble multiple bytecodes into readable assembly code
 *  Input:    *strBuffer    address of string buffer that is provided by user to store assembly code into
 *            *bytecode     address of bytecode that is going to be disassembled into assembly code
 */
int disassembleBytecodes(char *strBuffer, int *bytecode) {
  int operand = (*bytecode)>>8 & 0x00FFFFFF;
  while(*bytecode != 0xFFFFFFFF) {
    while(*strBuffer != 0)  // Find \0 to write
      strBuffer++;
    disassemble[(char)*bytecode](strBuffer, operand);
    while(*strBuffer != 0)  // Find \0 to write
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
  int source = getBits(operand, 5, 3);
  sprintf(strBuffer, "mov r%d r%d", destination, source);
}