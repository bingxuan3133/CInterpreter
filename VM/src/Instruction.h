#ifndef Instruction_H
#define Instruction_H

// Registers
#define REG_0  0
#define REG_1  1
#define REG_2  2
#define REG_3  3
#define REG_4  4
#define REG_5  5
#define REG_6  6
#define REG_7  7
#define REG_8  8
#define REG_9  9
#define REG_10  10
#define REG_11  11
#define REG_12  12
#define REG_13  13
#define REG_14  14
#define REG_15  15

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
#define halt() \
                HALT
#define dumpr(reg) \
                DUMPR | (reg)<<8
#define dumprHex(reg) \
                DUMPR_HEX | (reg)<<8
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
#define _div(resultRegQ, resultRegR, reg1, reg2) \
                DIV | (resultRegQ)<<8 | (resultRegR)<<(8+MAX_REG_BIT) | (reg1)<<(8+2*MAX_REG_BIT) | (reg2)<<(8+3*MAX_REG_BIT)
#define and(resultReg, reg1, reg2) \
                AND | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define or(resultReg, reg1, reg2) \
                OR | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define xor(resultReg, reg1, reg2) \
                XOR | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
// floating point
#define fldrImm(reg) \
                FLDR_IMM | (reg)<<8 
#define fldr(reg, refReg, imm) \
                FLDR | (reg)<<8 | (refReg)<<(8+MAX_REG_BIT) | (imm)<<(8+2*MAX_REG_BIT)
#define fstr(reg, refReg, imm) \
                FSTR | (reg)<<8 | (refReg)<<(8+MAX_REG_BIT) | (imm)<<(8+2*MAX_REG_BIT)
#define fadd(resultReg, reg1, reg2) \
                FADD | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define fsub(resultReg, reg1, reg2) \
                FSUB | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define fmul(resultRegH, resultRegL, reg1, reg2) \
                FMUL | (resultRegH)<<8 | (resultRegL)<<(8+MAX_REG_BIT) | (reg1)<<(8+2*MAX_REG_BIT) | (reg2)<<(8+3*MAX_REG_BIT)
#define fdiv(resultRegQ, reg1, reg2) \
                FDIV | (resultRegQ)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define bra(refAddress) \
                BRA | (refAddress)<<8
#define bit(reg, refAddress) \
                BRA_IF_TRUE | (reg)<<8 | (refAddress)<<(8+MAX_REG_BIT)
// compare
#define cmpe \
                CMPE | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define cmplt \
                CMPLT | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define cmplte \
                CMPLTE | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define cmpgt \
                CMPGT | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
#define cmpgte \
                CMPGTE | (resultReg)<<8 | (reg1)<<(8+MAX_REG_BIT) | (reg2)<<(8+2*MAX_REG_BIT)
//

typedef enum {
  DUMPR = 0x00,
  DUMPR_HEX = 0x01,
  LDR_IMM = 0x02,
  MOV_REG = 0x03,
  LDR_MEM_SAFE = 0x04,
  LDR_MEM = 0x05,
  STR_MEM_SAFE = 0x06,
  STR_MEM = 0x07,
  LDMS = 0x08,
  LDM = 0x09,
  STMS = 0x0a,
  STM = 0x0b,
  ADD = 0x0c,
  SUB = 0x0d,
  MUL = 0x0e,
  DIV = 0x0f,
  AND = 0x10,
  OR = 0x11,
  XOR = 0x12,
  FLDR_IMM = 0x13,
  FLDR ,
  FSTR ,
  FADD ,
  FSUB ,
  FMUL ,
  FDIV,
  BRA ,
  BRA_IF_TRUE ,
  CMPE,
  CMPLT,
  CMPLTE,
  CMPGT,
  CMPGTE,
  HALT = 0xff,
} Instruction;

#define MAX_INSTRUCTION BRA_IF_TRUE

// main function
void execute(int bytecode);

// debug helper
void dumpRegister(int bytecode);
void dumpRegisterHex(int bytecode);

// load store
void loadRegisterWithImmediate(int bytecode);
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

// floating point
void floadRegisterWithImmediate(int bytecode);
void floadRegisterFromMemory(int bytecode);
void fstoreRegisterIntoMemory(int bytecode);
void faddRegisters(int bytecode);
void fsubtractRegisters(int bytecode);
void fmultiplyRegisters(int bytecode);
void fdivideRegisters(int bytecode);
void fandRegisters(int bytecode);
void forRegisters(int bytecode);
void fxorRegisters(int bytecode);

// branch
void branch(int bytecode);
void branchIfTrue(int bytecode);

// compare
void compareIfEqual(int bytecode);
void compareIfLesserThan(int bytecode);
void compareIfLesserThanOrEqual(int bytecode);
void compareIfGreaterThan(int bytecode);
void compareIfGreaterThanOrEqual(int bytecode);

// helper functions
int getRd(int bytecode);
int getBits(int data, unsigned char start, unsigned char length);
int getR1(int bytecode);
int getR2(int bytecode);
int getRlist(int bytecode);

#endif // Instruction_H