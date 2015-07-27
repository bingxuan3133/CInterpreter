#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

unsigned int programCounter = 0;
Register reg[MAX_REG];

unsigned int getProgramCounter() {
  return programCounter;
}

void clearProgramCounter() {
  programCounter = 0;
}

int getBytecode(FILE *file) {
  int bytecode = 0;
  bytecode |= fgetc(file);
  bytecode |= fgetc(file) << 8;
  bytecode |= fgetc(file) << 16;
  bytecode |= fgetc(file) << 24;
  return bytecode;
}

void VMLoad(char* filepath, int *bytecode) {
  // FILE *file;
  // char fileNameBuffer[100];
  // sprintf(fileNameBuffer, "%s", filepath);
  // file = fopen(filepath, "r+");
  // int i;
  
  // *bytecode = getBytecode(file);
  // while(*bytecode != 0xFFFFFFFF) {
    // bytecode++;
    // *bytecode = getBytecode(file);
  // }
  
  // fclose(file);
}

void VMRun(int *bytecode) {
  unsigned char opcode = bytecode[programCounter];
  while(bytecode[programCounter] != halt()) {
    execute(bytecode[programCounter]);
    programCounter++;
  }
}

void VMStep(int *bytecode) {
  unsigned char opcode = bytecode[programCounter];
  if(bytecode[programCounter] != halt()) {
    execute(bytecode[programCounter]);
    programCounter++;
  }
}

Exception* __declspec(dllexport) _VMLoad(char *filepath, int *bytecode) {
  // Exception* exception;
  // Try {
    // VMLoad(filepath, bytecode);
    // return NULL;
  // } Catch (exception) {
    // return exception;
  // }
}

Exception* __declspec(dllexport) _VMRun(int *bytecode) {
  Exception* exception;
  Try {
    VMRun(bytecode);
    return NULL;
  } Catch (exception) {
    return exception;
  }
}

Exception* __declspec(dllexport) _VMStep(int *bytecode) {
  Exception* exception;
  Try {
    VMStep(bytecode);
    return NULL;
  } Catch (exception) {
    return exception;
  }
}