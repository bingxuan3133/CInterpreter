#ifndef VirtualMachine_H
#define VirtualMachine_H
#include <stdio.h>
extern void (*instruction[256])(int);

#endif // VirtualMachine_H

int getBytecode(FILE *file);