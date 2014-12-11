#ifndef Instruction_H
#define Instruction_H

typedef struct Register Register;

struct Register {
  int data;
  int base;
  int limit;
};

extern Register reg[8];

typedef enum {
  LDR_IMM, LDR_MEM, STR_MEM, MOV_REG, LDR_MEM_SAFE, STR_MEM_SAFE
} Instruction;

#define ldrImm(register, immediate)                     LDR_IMM | (register)<<8 | (immediate)<<11
#define ldrMem(register, referenceRegister, immediate)  LDR_MEM | (register)<<8 | (referenceRegister)<<11 | (immediate)<<14
#define strMem(register, referenceRegister, immediate)  STR_MEM | (register)<<8 | (referenceRegister)<<11 | (immediate)<<14
#define movReg(destinationRegister, sourceRegister)     MOV_REG | (destinationRegister)<<8 | (sourceRegister)<<11
#define ldrMemSafe(register, referenceRegister, immediate)  LDR_MEM_SAFE | (register)<<8 | (referenceRegister)<<11 | (immediate)<<14
#define strMemSafe(register, referenceRegister, immediate)  STR_MEM_SAFE | (register)<<8 | (referenceRegister)<<11 | (immediate)<<14

void loadRegisterWithLiteral(int bytecode);
void loadRegisterFromMemory(int bytecode);
void storeRegisterIntoMemory(int bytecode);
void moveRegister(int bytecode);
void loadRegisterFromMemorySafe(int bytecode);
void storeRegisterIntoMemorySafe(int bytecode);

int getBits(int data, unsigned char start, unsigned char length);

#endif // Instruction_H