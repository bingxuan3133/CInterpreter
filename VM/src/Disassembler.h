#ifndef Disassembler_H
#define Disassembler_H

extern void (*disassemble[256])(char*, int);

int disassembleBytecode(char *strBuffer, int *bytecode);
void disassembleLdrImm(char *strBuffer, int bytecode);
void disassembleLdrMem(char *strBuffer, int bytecode);
void disassembleStrMem(char *strBuffer, int bytecode);
void disassembleMovReg(char *strBuffer, int bytecode);
void disassembleLdrMemSafe(char *strBuffer, int bytecode);
void disassembleStrMemSafe(char *strBuffer, int bytecode);
void disassembleLdm(char *strBuffer, int bytecode);
void disassembleStm(char *strBuffer, int bytecode);
void disassembleLdms(char *strBuffer, int bytecode);
void disassembleStms(char *strBuffer, int bytecode);

#endif // Disassembler_H
