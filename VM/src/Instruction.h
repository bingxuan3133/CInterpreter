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
  MOV_REG,
  LDR_MEM_SAFE,
  STR_MEM_SAFE,
  LDMS,
  STMS,
  MUL,
  DIV,
  AND,
  OR,
  XOR,
  LDM = 0xf7,
  STM = 0xf9,
  ADD = 0xfa,
  SUB = 0xfb,
  LDR_IMM = 0xfc,
  LDR_MEM = 0xfe, 
  STR_MEM = 0xff,
} Instruction;

#define MAX_REG 8

// Registers
#define REG_0  0
#define REG_1  1
#define REG_2  2
#define REG_3  3
#define REG_4  4
#define REG_5  5
#define REG_6  6
#define REG_7  7

// Registers in bit
#define R0  1
#define R1  2
#define R2  4
#define R3  8
#define R4  16
#define R5  32
#define R6  64
#define R7  128

// Register Attribute
#define DATA  0
#define BASE  1
#define LIMIT 2

// Shift / Rotate Operations
#define NOP     0 // No operation (put as #immediate)
#define LSR     0 // Logical shift left
#define LSL     1 // Logical shift right
#define ASR     2 // Arithmetic shift right
#define RR      3 // Rotate right

// LDM STM direction
#define DEC 0
#define INC 1

// Update
#define NO_UPDATE 0
#define UPDATE    1

// Bytecode Macros
#define ldrImm(reg, imm) \
                LDR_IMM | (reg)<<8 | (imm)<<11
#define ldrMem(reg, refReg, imm) \
                LDR_MEM | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define strMem(reg, refReg, imm) \
                STR_MEM | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define movReg(dest, destAttrib, sour, shift, imm) \
                MOV_REG | (dest)<<8 | (destAttrib)<<11 | (sour)<<13 | (shift)<<16 | (imm)<<18
#define ldrMemSafe(reg, refReg, imm) \
                LDR_MEM_SAFE | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define strMemSafe(reg, refReg, imm) \
                STR_MEM_SAFE | (reg)<<8 | (refReg)<<11 | (imm)<<14
#define ldm(refReg, registers, direction, update) \
                LDM | (refReg)<<8 | (registers)<<11 | (direction)<<19 | (update)<<20
#define stm(refReg, registers, direction, update) \
                STM | (refReg)<<8 | (registers)<<11 | (direction)<<19 | (update)<<20
#define ldms(refReg, registers, direction, update) \
                LDMS | (refReg)<<8 | (registers)<<11 | (direction)<<19 | (update)<<20
#define stms(refReg, registers, direction, update) \
                STMS | (refReg)<<8 | (registers)<<11 | (direction)<<19 | (update)<<20
#define add(resultReg, reg1, reg2) \
                ADD | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
#define sub(resultReg, reg1, reg2) \
                SUB | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
#define mul(resultReg, reg1, reg2) \
                MUL | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
#define div(resultReg, reg1, reg2) \
                DIV | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
#define and(resultReg, reg1, reg2) \
                AND | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
#define or(resultReg, reg1, reg2) \
                OR | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
#define xor(resultReg, reg1, reg2) \
                XOR | (resultReg)<<8 | (reg1)<<11 | (reg2)<<14
// load store
void loadRegisterWithLiteral(int bytecode);
void loadRegisterFromMemory(int bytecode);
void storeRegisterIntoMemory(int bytecode);
void moveRegister(int bytecode);
void loadRegisterFromMemorySafe(int bytecode);
void storeRegisterIntoMemorySafe(int bytecode);
void loadMultipleRegistersFromMemory(int bytecode);
void storeMultipleRegistersIntoMemory(int bytecode);
void loadMultipleRegistersFromMemorySafe(int bytecode);
void storeMultipleRegistersIntoMemorySafe(int bytecode);
// arithmetic
void addRegisters(int bytecode);
void subtractRegisters(int bytecode);
void multiplyRegisters(int bytecode);
void divideRegisters(int bytecode);
void andRegisters(int bytecode);
void orRegisters(int bytecode);
void xorRegisters(int bytecode);

int getBits(int data, unsigned char start, unsigned char length);

#endif // Instruction_H