#ifndef VirtualMachine_H
#define VirtualMachine_H
#include <stdio.h>
extern void (*instruction[256])(int);

#endif // VirtualMachine_H

int getBytecode(FILE *file);
void __declspec(dllexport) runVM(int *bytecode);
void __declspec(dllexport) runVMFromStream(FILE *file);