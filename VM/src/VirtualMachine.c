#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>
#include <malloc.h>

int *VMbytecode;
int *memoryStack;
unsigned int programCounter = 0;
Register reg[MAX_REG];
DoubleRegister dReg[MAX_REG];
Status statusReg;

void __declspec(dllexport) VMinit(int memorySize) {
  free(memoryStack);
  VMbytecode = NULL;
  clearRegisters();
  clearProgramCounter();
  clearStatus();
  VMConfig(memorySize);
}

// Export Functions
Exception* __declspec(dllexport) VMRun(int *bytecode) {
  Exception* exception;
  Try {
    _VMRun(bytecode);
    return NULL;
  } Catch (exception) {
    return exception;
  }
}

Exception* __declspec(dllexport) VMStep(int *bytecode) {
  Exception* exception;
  Try {
    _VMStep(bytecode);
    return NULL;
  } Catch (exception) {
    return exception;
  }
}

void VMConfig(int memorySize) {  // memorySize = number of 4 bytes
  memoryStack = malloc(memorySize*4);
  reg[MAX_REG - 1].data = (int)(memoryStack + memorySize);
  reg[MAX_REG - 1].base = (int)memoryStack;
  reg[MAX_REG - 1].limit = memorySize;
}

// Inner Functions
void _VMRun(int *bytecode) {
  VMbytecode = bytecode;
  while((unsigned char)bytecode[programCounter] != halt()) {
    execute(bytecode[programCounter]);
    programCounter++;
  }
}

void _VMStep(int *bytecode) {
  VMbytecode = bytecode;
  if((unsigned char)bytecode[programCounter] != halt()) {
    execute(bytecode[programCounter]);
    programCounter++;
  }
}

void _VMLoad(char* filepath, int *bytecode) {
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

int getVMBytecode(int pc) {
  return VMbytecode[pc];
}

void loadVMBytecode(int *bytecode) {
  VMbytecode = bytecode;
}

// Register
void clearRegisters() {
  int i;
  for(i = 0; i < MAX_REG; i++) {
    reg[i].data = 0;
    reg[i].base = 0;
    reg[i].limit = 0;
    dReg[i].data = 0;
    dReg[i].base = 0;
    dReg[i].limit = 0;
  }
}

// Status Register
void clearStatus() {
  statusReg.B = 0;
}

void setStatusBit(char bit) {
  switch(bit) {
  case 'B':
    statusReg.B = 1;
    break;
  default:
    break;
  }
}

void clearStatusBit(char bit) {
  switch(bit) {
  case 'B':
    statusReg.B = 0;
    break;
  default:
    break;
  }
}

// Program Counter
void clearProgramCounter() {
  programCounter = 0;
}

void moveProgramCounter(int relativeAddress) {
  programCounter = programCounter + relativeAddress;
}

unsigned int getProgramCounter() {
  return programCounter;
}
