#ifndef Instruction_H
#define Instruction_H

// Register Mode
#define MAX_REG 16      // 2 to 16
#define MAX_REG_BIT 4   // 1 to 4

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
                LDR_IMM | (reg)<<8 | (imm)<<(8+MAX_REG_BIT)
#define ldrMem(reg, refReg, imm) \
                LDR_MEM | (reg)<<8 | (refReg)<<(8+MAX_REG_BIT) | (imm)<<(8+2*MAX_REG_BIT)
#define strMem(reg, refReg, imm) \
                STR_MEM | (reg)<<8 | (refReg)<<(8+MAX_REG_BIT) | (imm)<<(8+2*MAX_REG_BIT)
#define movReg(dest, destAttrib, sour, shift, imm) \
                MOV_REG | (dest)<<8 | (sour)<<(8+MAX_REG_BIT) | (destAttrib)<<(8+2*MAX_REG_BIT) | (shift)<<(10+2*MAX_REG_BIT) | (imm)<<(12+2*MAX_REG_BIT)
#define ldrMemSafe(reg, refReg, imm) \
                LDR_MEM_SAFE | (reg)<<8 | (refReg)<<(8+MAX_REG_BIT) | (imm)<<(8+2*MAX_REG_BIT)
#define strMemSafe(reg, refReg, imm) \
                STR_MEM_SAFE | (reg)<<8 | (refReg)<<(8+MAX_REG_BIT) | (imm)<<(8+2*MAX_REG_BIT)
#define ldm(refReg, registers, direction, update) \
                LDM | (refReg)<<8 | (registers)<<(8+MAX_REG_BIT) | (direction)<<(8+MAX_REG_BIT+MAX_REG) | (update)<<(9+MAX_REG_BIT+MAX_REG)
#define stm(refReg, registers, direction, update) \
                STM | (refReg)<<8 | (registers)<<(8+MAX_REG_BIT) | (direction)<<(8+MAX_REG_BIT+MAX_REG) | (update)<<(9+MAX_REG_BIT+MAX_REG)
#define ldms(refReg, registers, direction, update) \
                LDMS | (refReg)<<8 | (registers)<<(8+MAX_REG_BIT) | (direction)<<(8+MAX_REG_BIT+MAX_REG) | (update)<<(9+MAX_REG_BIT+MAX_REG)
#define stms(refReg, registers, direction, update) \
                STMS | (refReg)<<8 | (registers)<<(8+MAX_REG_BIT) | (direction)<<(8+MAX_REG_BIT+MAX_REG) | (update)<<(9+MAX_REG_BIT+MAX_REG)
#define add(resultReg, reg1, reg2) \
                ADD | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define sub(resultReg, reg1, reg2) \
                SUB | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define mul(resultRegH, resultRegL, reg1, reg2) \
                MUL | (resultRegH)<<8 | (resultRegL)<<(8+MAX_REG_BIT) | (reg1)<<(8+2*MAX_REG_BIT) | (reg2)<<(8+3*MAX_REG_BIT)
#define div(resultRegQ, resultRegR, reg1, reg2) \
                DIV | (resultRegQ)<<8 | (resultRegR)<<(8+MAX_REG_BIT) | (reg1)<<(8+2*MAX_REG_BIT) | (reg2)<<(8+3*MAX_REG_BIT)
#define and(resultReg, reg1, reg2) \
                AND | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define or(resultReg, reg1, reg2) \
                OR | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define xor(resultReg, reg1, reg2) \
                XOR | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)

typedef struct Register Register;

struct Register {
  int data;
  int base;
  int limit;
};

extern Register reg[MAX_REG];

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

// helper functions
int getRd(int bytecode);
int getBits(int data, unsigned char start, unsigned char length);
int getR1(int bytecode);
int getR2(int bytecode);
int getRlist(int bytecode);

#endif // Instruction_H