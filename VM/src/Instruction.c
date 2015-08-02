#include "VirtualMachine.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

// Instruction Entry
void (*instruction[256])(int)  = {[DUMPR] = dumpRegister,
                                  [DUMPR_HEX] = dumpRegisterHex,
                                  [LDR_IMM] = loadRegisterWithImmediate,
                                  [LDR_MEM] = loadRegisterFromMemory,
                                  [STR_MEM] = storeRegisterIntoMemory,
                                  [MOV_REG] = moveRegister,
                                  [LDR_MEM_SAFE] = loadRegisterFromMemorySafe,
                                  [STR_MEM_SAFE] = storeRegisterIntoMemorySafe,
                                  [LDM] = loadMultipleRegistersFromMemory,
                                  [STM] = storeMultipleRegistersIntoMemory,
                                  [LDMS] = loadMultipleRegistersFromMemorySafe,
                                  [STMS] = storeMultipleRegistersIntoMemorySafe,
                                  [ADD] = addRegisters,
                                  [SUB] = subtractRegisters,
                                  // [SUB_IMM] = subtractRegisterWithImmediate,
                                  [MUL] = multiplyRegisters,
                                  [DIV] = divideRegisters,
                                  [AND] = andRegisters,
                                  [OR] = orRegisters,
                                  [XOR] = xorRegisters
                                  };
//

//========================
//    Helper Functions
//========================

//-----------------------
//    Bytecode Format
//-----------------------

//  COMMAND | Rd | R1 | imm
//  ldr Rd, [R1 + imm]

//  COMMAND | Rd | R1 | R2
//  add Rd, R1, R2

//  COMMAND | Rd | R1 | R2 | R3
//  mul Rhigh, Rlow, R1, R2

//  COMMAND | Rd | R1 | Rd.attribute
//  mov Rd, R1, R2

//  COMMAND | Rd | Rlist
//  ldm Rd, [Rlist]

/**
 *  This is a helper function to get a specific range of bits from a 32-bit data
 *  Input:  data    original 32-bit data
 *          start   the start bit index of the returning bits (MSB)
 *          length  the length of returning bits
 *  Return: result  returning bits
 */
int getBits(int data, unsigned char start, unsigned char length) {
  int result;
  result = data >> (start - length + 1);
  result = result & (0xFFFFFFFF >> (32 - length));
  return result;
}

/**
 *  This is a helper function to get the destination register
 *  Input:  
 */
int getRd(int bytecode) {
  return getBits(bytecode, 7 + MAX_REG_BIT, MAX_REG_BIT);
}

/**
 *  This is a helper function to get the destination register
 *  Input:  
 */
int getR1(int bytecode) {
  return getBits(bytecode, 7 + (2 * MAX_REG_BIT), MAX_REG_BIT);
}

/**
 *  This is a helper function to get the destination register
 *  Input:  
 */
int getR2(int bytecode) {
  return getBits(bytecode, 7 + (3 * MAX_REG_BIT), MAX_REG_BIT);
}

/**
 *  This is a helper function to get the destination register
 *  Input:  
 */
int getR3(int bytecode) {
  return getBits(bytecode, 7 + (4 * MAX_REG_BIT), MAX_REG_BIT);
}

/**
 *  This is a helper function to get the register list (used in ldm and stm)
 *  Input:  
 */
int getRlist(int bytecode) {
  return getBits(bytecode, 7 + MAX_REG_BIT + MAX_REG, MAX_REG);
}

//======================
//    Main Function
//======================

void execute(int bytecode) {
  unsigned char opcode = bytecode;
  Exception *exception;
  if(opcode > MAX_INSTRUCTION) {
    sprintf(errBuffer, "ERROR: invalid bytecode (0x%08x, pc = %d).", bytecode, getProgramCounter());
    exception = createException(errBuffer, INVALID_BYTECODE, bytecode);
    Throw(exception);
  } else {
    instruction[opcode](bytecode);
  }
}

//======================
//    Instructions
//======================

//----------------------
//    Register-associated
//----------------------

void dumpRegister(int bytecode) {
  int regIndex = getRd(bytecode);
  printf("r%d: %d\n", regIndex, reg[regIndex].data);
}

void dumpRegisterHex(int bytecode) {
  int regIndex = getRd(bytecode);
  printf("r%d: 0x%x\n", regIndex, reg[regIndex].data);
}

/**
 *  This function load register with a immediate value
 *  Input:  bytecode
 */
void loadRegisterWithImmediate(int bytecode) {
  int regIndex = getRd(bytecode);
  reg[regIndex].data = bytecode >> (8 + MAX_REG_BIT);
}

/**
 *  This function load register with data from memory
 *  Input:  bytecode
 */
void loadRegisterFromMemory(int bytecode) {
  int *ref;
  int registerToBeLoaded = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  reg[registerToBeLoaded].data = *ref;
}

/**
 *  This function store register data into memory
 *  Input:  bytecode
 */
void storeRegisterIntoMemory(int bytecode) {
  int *ref;
  int registerToBeStored = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  *ref = reg[registerToBeStored].data;
}

/**
 *  This function move of register data into another register (data, base, or limit)
 *  Input:  bytecode
 */
void moveRegister(int bytecode) {
  int destination = getRd(bytecode);
  int source = getR1(bytecode);
  int destAttrib = getBits(bytecode, (9 + 2 * MAX_REG_BIT), 2);
  int shift = getBits(bytecode, (11 + 2 * MAX_REG_BIT), 2);
  int imm = getBits(bytecode, (16 + 2 * MAX_REG_BIT), 5); // number of shift 0 ~ 31
  int data = reg[source].data;
  
  // Shift / Rotate Operations
  if(imm == NOP)
    ;
  if(shift == LSR) {
    data = (unsigned int)data >> imm;
  } else if(shift == LSL) {
    data = (unsigned int)data << imm;
  } else if(shift == ASR) {
    data = (int)data >> imm;
  } else if(shift == RR) {
    data = (data & 0xFFFFFFFF >> (32 - imm)) << (32 - imm); // Get shifted out bits
    data = (data) | ((unsigned int)(reg[source].data) >> imm); // Put shifted in bits
  }
  // Assign
  if(destAttrib == DATA)
    reg[destination].data = data;
  else if(destAttrib == BASE)
    reg[destination].base = data;
  else if(destAttrib == LIMIT)
    reg[destination].limit = data;
  else // Treat as DATA
    reg[destination].data = data;
}

/**
 *  This function load register with data from safe memory
 *  Input:  bytecode
 */
void loadRegisterFromMemorySafe(int bytecode) {
  int *ref;
  int registerToBeLoaded = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  Exception *exception;
  if(base <= (int)ref &&  base + limit >= (int)ref + 4) { // Safe area
    reg[registerToBeLoaded].data = *ref;
  } else {
    sprintf(errBuffer, "ERROR: r%d (%p-%p) has invalid access to memory location (%p).", registerToBeLoaded, base, base+limit, ref);
    exception = createException(errBuffer, INVALID_MEMORY_ACCESS, bytecode);
    Throw(exception);
  }
}

/**
 *  This function store register data into safe memory
 *  Input:  bytecode
 */
void storeRegisterIntoMemorySafe(int bytecode) {
  int *ref;
  int registerToBeStored = getRd(bytecode);
  int referenceRegister = getR1(bytecode);
  int relativeAddress = bytecode >> (8 + 2 * MAX_REG_BIT);
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  Exception *exception;
  if(base <= (int)ref && base + limit >= (int)ref + 4) { // Safe area
    *ref = reg[registerToBeStored].data;
  } else {
    sprintf(errBuffer, "ERROR: r%d (%p-%p) has invalid access to memory location (%p).", registerToBeStored, base, base+limit, ref);
    exception = createException(errBuffer, INVALID_MEMORY_ACCESS, bytecode);
    Throw(exception);
  }
}

/**
 *  This function load multiple registers with data from memory
 *  Input:  bytecode
 */
void loadMultipleRegistersFromMemory(int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeLoaded = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  int *ref = (int *)reg[referenceRegister].data;
  int i;
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeLoaded >> i)) {
      reg[i].data = *ref;
      if(direction == INC) {
        ref++;
      } else { // direction == DEC
        ref--;
      }
    }
  }
  if(update == UPDATE)
    reg[referenceRegister].data = (int)ref;
}

/**
 *  This function store multiple registers into memory
 *  Input:  bytecode
 */
void storeMultipleRegistersIntoMemory(int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeStored = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  int *ref = (int *)reg[referenceRegister].data;
  int i;
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeStored >> i)) {
      *ref = reg[i].data;
      if(direction == INC) {
        ref++;
      } else { // direction == DEC
        ref--;
      }
    }
  }
  if(update == UPDATE)
    reg[referenceRegister].data = (int)ref;
}

/**
 *  This function load multiple registers with data from safe memory
 *  Input:  bytecode
 */
void loadMultipleRegistersFromMemorySafe(int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeLoaded = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  int *ref = (int *)reg[referenceRegister].data;
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  int i;
  Exception *exception;
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeLoaded >> i)) {
      if(base <= (int)ref &&  base + limit >= (int)ref + 4) { // Safe area
        reg[i].data = *ref;
      } else {
        sprintf(errBuffer, "ERROR: r%d (%p-%p) has invalid access when loading r%d from memory location (%p).", referenceRegister, base, base+limit, i, ref);
        exception = createException(errBuffer, INVALID_MEMORY_ACCESS, bytecode);
        Throw(exception);
      }
      if(direction == INC) {
        ref++;
      } else { // direction == DEC
        ref--;
      }
    }
  }
  if(update == UPDATE)
    reg[referenceRegister].data = (int)ref;
}

/**
 *  This function store multiple registers into safe memory
 *  Input:  bytecode
 */
void storeMultipleRegistersIntoMemorySafe(int bytecode) {
  int referenceRegister = getRd(bytecode);
  int registersToBeStored = getRlist(bytecode);
  int direction = getBits(bytecode, 8 + MAX_REG + MAX_REG_BIT, 1);
  int update = getBits(bytecode, 9 + MAX_REG + MAX_REG_BIT, 1);
  int *ref = (int *)reg[referenceRegister].data;
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  int i;
  Exception *exception;
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeStored >> i)) {
        if(base <= (int)ref && base + limit >= (int)ref + 4) { // Safe area
          *ref = reg[i].data;
        } else {
          sprintf(errBuffer, "ERROR: r%d (%p-%p) has invalid access when storing r%d into memory location (%p).", referenceRegister, base, base+limit, i, ref);
          exception = createException(errBuffer, INVALID_MEMORY_ACCESS, bytecode);
          Throw(exception);
        }
      if(direction == INC) {
        ref++;
      } else { // direction == DEC
        ref--;
      }
    }
  }
  if(update == UPDATE)
    reg[referenceRegister].data = (int)ref;
}

//----------------------
//    Arithmetic
//----------------------

void addRegisters(int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  reg[resultReg].data = reg[reg1].data + reg[reg2].data;
}

void subtractRegisters(int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  reg[resultReg].data = reg[reg1].data - reg[reg2].data;
}

// void subtractRegisterWithImmediate(int bytecode) {
  // int regIndex = getRd(bytecode);
  // unsigned int value = bytecode >> (8 + MAX_REG_BIT);
  
  // reg[regIndex].data = reg[regIndex].data - value;
// }

void multiplyRegisters(int bytecode) {
  unsigned long long result;
  int resultHighReg = getRd(bytecode);
  int resultLowReg = getR1(bytecode);
  int reg1 = getR2(bytecode);
  int reg2 = getR3(bytecode);
  result = (unsigned long long)reg[reg1].data * reg[reg2].data;
  reg[resultHighReg].data = result>>32;
  reg[resultLowReg].data = result;
}

void divideRegisters(int bytecode) {
  int resultQuotientReg = getRd(bytecode);
  int resultRemainderReg = getR1(bytecode);
  int reg1 = getR2(bytecode);
  int reg2 = getR3(bytecode);
  int quotient = reg[reg1].data / reg[reg2].data;
  int remainder = reg[reg1].data % reg[reg2].data;
  reg[resultQuotientReg].data = quotient;
  reg[resultRemainderReg].data = remainder;
}

void andRegisters(int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  reg[resultReg].data = reg[reg1].data & reg[reg2].data;
}

void orRegisters(int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  reg[resultReg].data = reg[reg1].data | reg[reg2].data;
}

void xorRegisters(int bytecode) {
  int resultReg = getRd(bytecode);
  int reg1 = getR1(bytecode);
  int reg2 = getR2(bytecode);
  reg[resultReg].data = reg[reg1].data ^ reg[reg2].data;
}

//----------------------
//    Branch
//----------------------

void branch(int bytecode) {
  int resultReg = getRd(bytecode);
  int relativeAddress = bytecode >> 8;
  moveProgramCounter(relativeAddress);
}

void branchIfTrue(int bytecode) {
  int resultReg = getRd(bytecode);
  int relativeAddress = bytecode >> 8;
  if(statusReg.B) {
    moveProgramCounter(relativeAddress);
  }
}
