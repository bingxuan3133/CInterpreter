#ifndef Disassembler_H
#define Disassembler_H

extern void (*disassemble[256])(char*, int);

int __declspec(dllexport) disassembleBytecodes(char *strBuffer, int *bytecode);
int __declspec(dllexport) disassembleBytecode(char *strBuffer, int bytecode);
void dumpBytecode(int bytecode);
void dumpBytecodes(int *bytecode);

void disassembleDefault(char *strBuffer, int bytecode);
void disassembleHalt(char *strBuffer, int bytecode);

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

// void disassembleSubImm(char *strBuffer, int bytecode);
void disassembleAdd(char *strBuffer, int bytecode);
void disassembleSub(char *strBuffer, int bytecode);
void disassembleMul(char *strBuffer, int bytecode);
void disassembleDiv(char *strBuffer, int bytecode);
void disassembleAnd(char *strBuffer, int bytecode);
void disassembleOr(char *strBuffer, int bytecode);
void disassembleXor(char *strBuffer, int bytecode);
void disassembleBra(char *strBuffer, int bytecode);
void disassembleBit(char *strBuffer, int bytecode);

void disassembleFLdrImm(char *strBuffer, int bytecode);
void disassembleFldr(char *strBuffer, int bytecode);
void disassembleFstr(char *strBuffer, int bytecode);
void disassembleFadd(char *strBuffer, int bytecode);
void disassembleFsub(char *strBuffer, int bytecode);
void disassembleFmul(char *strBuffer, int bytecode);
void disassembleFdiv(char *strBuffer, int bytecode);

#endif // Disassembler_H
