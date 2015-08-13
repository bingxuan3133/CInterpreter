#ifndef VirtualMachine_H
#define VirtualMachine_H
#include <stdio.h>
#include "Exception.h"

// Register Mode (supports only 2 to 16 registers mode)
#define MAX_REG 8      // 2 to 16
#define MAX_REG_BIT 3   // 1 to 4

typedef struct Register Register;

struct Register {
  int data;
  int base;
  int limit;
};

typedef struct DoubleRegister DoubleRegister;

struct DoubleRegister {
  double data;
  int base;
  int limit;
};

typedef struct Status Status;

struct Status {
  int B; // Boolean Flag
};

extern int *memoryStack;
extern Status statusReg;
extern Register reg[MAX_REG];
extern DoubleRegister dReg[MAX_REG];

// Export Functions
void __declspec(dllexport) VMinit(int memorySize, char *buffer);
void VMConfig(int memorySize);
int* __declspec(dllexport) VMLoad(int *bytecode, int size);
int*  __declspec(dllexport) VMLoadAppend(int *bytecode, int size);
void __declspec(dllexport) VMLoadFree();
Exception* __declspec(dllexport) VMRun();
Exception* __declspec(dllexport) VMStep();

void _VMRun();
void _VMStep();

int getVMBytecode(int pc);
void loadVMBytecode(int *bytecode);
void clearRegisters();
void clearProgramCounter();
void moveProgramCounter(int relativeAddress);
unsigned int getProgramCounter();
void clearStatus();
void setStatusBit(char bit);
void clearStatusBit(char bit);
int getBytecode(FILE *file);


#endif // VirtualMachine_H