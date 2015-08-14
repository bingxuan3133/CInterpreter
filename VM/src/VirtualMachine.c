#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include "Print.h"
#include <stdio.h>
#include <malloc.h>

int *VMbytecode;
int VMbytecodeSize;
int *memoryStack;
unsigned int programCounter = 0;
Register reg[MAX_REG];
DoubleRegister dReg[MAX_REG];
Status statusReg;

void __declspec(dllexport) VMinit(int memorySize, char *buffer) {
  free(memoryStack);
  pythonBuffer = buffer;
  VMbytecode = NULL;
  clearRegisters();
  clearProgramCounter();
  clearStatus();
  VMConfig(memorySize);
}

// Export Functions
Exception* __declspec(dllexport) VMRun() {
  Exception* exception;
  Try {
    _VMRun();
    return NULL;
  } Catch (exception) {
    return exception;
  }
}

Exception* __declspec(dllexport) VMStep() {
  Exception* exception;
  Try {
    _VMStep();
    return NULL;
  } Catch (exception) {
    return exception;
  }
}

int* __declspec(dllexport) VMLoad(int *bytecode, int size) {
  VMbytecode = malloc(size*sizeof(int));
  VMbytecodeSize = size;
  int i;
  for(i = 0; i < size; i++) {
    VMbytecode[i] = bytecode[i];
  }
  return VMbytecode;
}

int* __declspec(dllexport) VMLoadAppend(int *bytecode, int size) {
  int *oldVMbytecode = VMbytecode;
  int oldSize = VMbytecodeSize;
  VMbytecode = malloc((VMbytecodeSize + size)*sizeof(int));
  VMbytecodeSize = size;
  int i;
  for(i = 0; i < oldSize; i++) {
    VMbytecode[i] = oldVMbytecode[i];
  }
  for(i = 0; i < size; i++) {
    VMbytecode[i + oldSize] = bytecode[i];
  }
  free(oldVMbytecode);
  return VMbytecode;
}

int __declspec(dllexport) VMgetBytecode(int *bytecode) {
  return *bytecode;
}

void __declspec(dllexport) VMLoadFree() {
  free(VMbytecode);
}


void VMConfig(int memorySize) {  // memorySize = number of 4 bytes
  memoryStack = malloc(memorySize*4);
  reg[MAX_REG - 1].data = (int)(memoryStack + memorySize);
  reg[MAX_REG - 1].base = (int)memoryStack;
  reg[MAX_REG - 1].limit = memorySize;
}

// Inner Functions
void _VMRun() {
  while((unsigned char)VMbytecode[programCounter] != halt()) {
    execute(VMbytecode[programCounter]);
    programCounter++;
  }
}

void _VMStep() {
  if((unsigned char)VMbytecode[programCounter] != halt()) {
    execute(VMbytecode[programCounter]);
    programCounter++;
  }
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
