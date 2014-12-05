#ifndef VirtualMachine_H
#define VirtualMachine_H

extern int reg[8];

int getBits(int data, unsigned char start, unsigned char length);
void loadRegisterWithLiteral(int operand);
void loadRegisterWithReference(int operand);

#endif // VirtualMachine_H