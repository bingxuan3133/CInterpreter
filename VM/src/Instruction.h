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

// Registers
#define R0  0
#define R1  1
#define R2  2
#define R3  3
#define R4  4
#define R5  5
#define R6  6
#define R7  7

// Register Attribute
#define DATA 0
#define BASE 1
#define LIMIT 2

// Shift / Rotate Operations
#define NOP     0
#define LSR     0
#define LSL     1
#define ASR     2
#define RR      3

#define ldrImm(reg, imm)                            LDR_IMM | (reg)<<8 | (imm)<<11
#define ldrMem(reg, refReg, imm)                    LDR_MEM | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define strMem(reg, refReg, imm)                    STR_MEM | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define movReg(dest, destAttrib, sour, shift, imm)  MOV_REG | (dest)<<8 | (destAttrib)<<11 | (sour)<<13 | (shift)<<16 | (imm)<<18
#define ldrMemSafe(reg, refReg, imm)                LDR_MEM_SAFE | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define strMemSafe(reg, refReg, imm)                STR_MEM_SAFE | (reg)<<8 | (refReg)<<11 | (imm)<<14

void loadRegisterWithLiteral(int bytecode);
void loadRegisterFromMemory(int bytecode);
void storeRegisterIntoMemory(int bytecode);
void moveRegister(int bytecode);
void loadRegisterFromMemorySafe(int bytecode);
void storeRegisterIntoMemorySafe(int bytecode);

int getBits(int data, unsigned char start, unsigned char length);

#endif // Instruction_H