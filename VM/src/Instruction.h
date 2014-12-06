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
  LDR_IMM, LDR_MEM, STR_MEM, MOV_REG
} Instruction;

#define ldrImm(register, immediate)                     LDR_IMM | (register)<<8 | (immediate)<<11
#define ldrMem(register, referenceRegister, immediate)  LDR_MEM | (register)<<8 | (referenceRegister)<<11 | (immediate)<<14
#define strMem(register, referenceRegister, immediate)  STR_MEM | (register)<<8 | (referenceRegister)<<11 | (immediate)<<14
#define movReg(destinationRegister, sourceRegister)     MOV_REG | (destinationRegister)<<8 | (sourceRegister)<<11

void loadRegisterWithLiteral(int operand);
void loadRegisterWithReference(int operand);
void storeRegisterIntoReference(int operand);
void moveRegister(int operand);

int getBits(int data, unsigned char start, unsigned char length);

#endif // Instruction_H
