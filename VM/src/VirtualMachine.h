#ifndef VirtualMachine_H
#define VirtualMachine_H
#include <stdio.h>
extern void (*instruction[256])(int);

#endif // VirtualMachine_H

int getBytecode(FILE *file);
void __declspec(dllexport) VMLoad(char* filepath, int *bytecode);
void __declspec(dllexport) VMRun(int *bytecode);
void __declspec(dllexport) VMStep(int *bytecode);