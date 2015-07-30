#ifndef Disassembler_H
#define Disassembler_H

extern void (*disassemble[256])(char*, int);

int disassembleBytecodes(char *strBuffer, int *bytecode);
int disassembleBytecode(char *strBuffer, int bytecode);
void dumpBytecode(int bytecode);

void disassembleDumpr(char *strBuffer, int bytecode);
void disassembleDumprHex(char *strBuffer, int bytecode);
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

void disassembleSubImm(char *strBuffer, int bytecode);
void disassembleAdd(char *strBuffer, int bytecode);
void disassembleSub(char *strBuffer, int bytecode);
void disassembleMul(char *strBuffer, int bytecode);
void disassembleDiv(char *strBuffer, int bytecode);
void disassembleAnd(char *strBuffer, int bytecode);
void disassembleOr(char *strBuffer, int bytecode);
void disassembleXor(char *strBuffer, int bytecode);

#endif // Disassembler_H
