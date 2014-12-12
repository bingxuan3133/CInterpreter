#ifndef Disassembler_H
#define Disassembler_H

extern void (*disassemble[256])(char*, int);

int disassembleBytecode(char *strBuffer, int *bytecode);
void disassembleLdrImm(char *strBuffer, int operand);
void disassembleLdrMem(char *strBuffer, int operand);
void disassembleStrMem(char *strBuffer, int operand);
void disassembleMovReg(char *strBuffer, int operand);
void disassembleLdrMemSafe(char *strBuffer, int operand);
void disassembleStrMemSafe(char *strBuffer, int operand);

#endif // Disassembler_H
