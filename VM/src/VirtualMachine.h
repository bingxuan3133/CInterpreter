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

extern Register reg[MAX_REG];

extern void (*instruction[256])(int);

unsigned int getProgramCounter();
void clearProgramCounter();
int getBytecode(FILE *file);
void VMLoad(char* filepath, int *bytecode);
void VMRun(int *bytecode);
void VMStep(int *bytecode);

// Proxy Functions
Exception* __declspec(dllexport) _VMLoad(char* filepath, int *bytecode);
Exception* __declspec(dllexport) _VMRun(int *bytecode);
Exception* __declspec(dllexport) _VMStep(int *bytecode);

#endif // VirtualMachine_H