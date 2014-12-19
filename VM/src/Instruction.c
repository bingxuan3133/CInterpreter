#include "Instruction.h"
#include <stdio.h>
#include "Exception.h"

Register reg[MAX_REG];
char errBuffer[100] = {0};

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
 *  This function load register with a literal value
 *  Input:  bytecode
 */
void loadRegisterWithLiteral(int bytecode) {
  int regIndex = getBits(bytecode, 10, 3);
  reg[regIndex].data = bytecode >> 11;
}

/**
 *  This function load register with data from memory
 *  Input:  bytecode
 */
void loadRegisterFromMemory(int bytecode) {
  int *ref;
  int registerToBeLoaded = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = bytecode >> 14;
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  reg[registerToBeLoaded].data = *ref;
}

/**
 *  This function store register data into memory
 *  Input:  bytecode
 */
void storeRegisterIntoMemory(int bytecode) {
  int *ref;
  int registerToBeStored = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = bytecode >> 14;
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  *ref = reg[registerToBeStored].data;
}

/**
 *  This function move of register data into another register (data, base, or limit)
 *  Input:  bytecode
 */
void moveRegister(int bytecode) {
  int destination = getBits(bytecode, 10, 3);
  int attrib = getBits(bytecode, 12, 2);
  int source = getBits(bytecode, 15, 3);
  int shift = getBits(bytecode, 17, 2);
  int imm = getBits(bytecode, 22, 5); // number of shift 0 ~ 31
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
    printf("data%x\n", data);
    data = (data & 0xFFFFFFFF >> (32 - imm)) << (32 - imm); // Get shifted out bits
    printf("data%x\n", data);
    data = (data) | ((unsigned int)(reg[source].data) >> imm); // Put shifted in bits
    printf("data%x\n", data);
  }
  // Assign
  if(attrib == DATA)
    reg[destination].data = data;
  else if(attrib == BASE)
    reg[destination].base = data;
  else if(attrib == LIMIT)
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
  int registerToBeLoaded = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = bytecode >> 14;
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  if(base <= (int)ref &&  base + limit >= (int)ref + 4) { // Safe area
    reg[registerToBeLoaded].data = *ref;
  } else {
    sprintf(errBuffer, "ERROR: r%d (%p - %p) has invalid access to address %p.", registerToBeLoaded, base, base+limit-1, ref);
    exception = createException(errBuffer, INVALID_MEMORY_ACCESS);
    Throw(exception);
  }
}

/**
 *  This function store register data into safe memory
 *  Input:  bytecode
 */
void storeRegisterIntoMemorySafe(int bytecode) {
  int *ref;
  int registerToBeStored = getBits(bytecode, 10, 3);
  int referenceRegister = getBits(bytecode, 13, 3);
  int relativeAddress = bytecode >> 14;
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  if(base <= (int)ref && base + limit >= (int)ref + 4) { // Safe area
    *ref = reg[registerToBeStored].data;
  } else {
    sprintf(errBuffer, "ERROR: r%d (%p - %p) has invalid access to address %p.", registerToBeStored, base, base+limit-1, ref);
    exception = createException(errBuffer, INVALID_MEMORY_ACCESS);
    Throw(exception);
  }
}

/**
 *  This function load multiple registers with data from memory
 *  Input:  bytecode
 */
void loadMultipleRegistersFromMemory(int bytecode) {
  int referenceRegister = getBits(bytecode, 10, 3);
  int registersToBeLoaded = getBits(bytecode, 18, 8);
  int direction = getBits(bytecode, 19, 1);
  int update = getBits(bytecode, 20, 1);
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
  int referenceRegister = getBits(bytecode, 10, 3);
  int registersToBeStored = getBits(bytecode, 18, 8);
  int direction = getBits(bytecode, 19, 1);
  int update = getBits(bytecode, 20, 1);
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
  int referenceRegister = getBits(bytecode, 10, 3);
  int registersToBeLoaded = getBits(bytecode, 18, 8);
  int direction = getBits(bytecode, 19, 1);
  int update = getBits(bytecode, 20, 1);
  int *ref = (int *)reg[referenceRegister].data;
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  int i;
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeLoaded >> i)) {
      if(base <= (int)ref &&  base + limit >= (int)ref + 4) { // Safe area
        reg[i].data = *ref;
      } else {
        sprintf(errBuffer, "ERROR: r%d (%p - %p) has invalid access when loading r%d from address %p.", referenceRegister, base, base+limit-1, i, ref);
        exception = createException(errBuffer, INVALID_MEMORY_ACCESS);
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
  int referenceRegister = getBits(bytecode, 10, 3);
  int registersToBeStored = getBits(bytecode, 18, 8);
  int direction = getBits(bytecode, 19, 1);
  int update = getBits(bytecode, 20, 1);
  int *ref = (int *)reg[referenceRegister].data;
  int base = reg[referenceRegister].base;
  int limit = reg[referenceRegister].limit;
  int i;
  for(i = 0; i < MAX_REG; i++) {
    if(0x01 & (registersToBeStored >> i)) {
        if(base <= (int)ref && base + limit >= (int)ref + 4) { // Safe area
          *ref = reg[i].data;
        } else {
          sprintf(errBuffer, "ERROR: r%d (%p - %p) has invalid access when storing r%d into address %p.", referenceRegister, base, base+limit-1, i, ref);
          exception = createException(errBuffer, INVALID_MEMORY_ACCESS);
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

void addRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data + reg[reg2].data;
}

void subtractRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data - reg[reg2].data;
}

void multiplyRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data * reg[reg2].data;
}

void divideRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data / reg[reg2].data;
}

void andRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data & reg[reg2].data;
}

void orRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data | reg[reg2].data;
}

void xorRegisters(int bytecode) {
  int resultReg = getBits(bytecode, 10, 3);
  int reg1 = getBits(bytecode, 13, 3);
  int reg2 = getBits(bytecode, 16, 3);
  reg[resultReg].data = reg[reg1].data ^ reg[reg2].data;
}