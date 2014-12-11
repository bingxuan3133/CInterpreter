#include "Instruction.h"
#include <stdio.h>
#include "Exception.h"

Register reg[8];
char buffer[100] = {0};

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
 *  This function load register with value from memory
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
 *  This function store register into memory
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
 *  This function move value of a register into another register
 *  Input:  bytecode
 */
void moveRegister(int bytecode) {
  int destination = getBits(bytecode, 10, 3);
  int source = getBits(bytecode, 13, 3);
  reg[destination].data = reg[source].data;
}

/**
 *  This function load register with value from memory
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
  if(base <= (int)ref && limit >= (int)ref) { // Safe area
    reg[registerToBeLoaded].data = *ref;
  } else {
    sprintf(buffer, "r%d (.base = %p .limit = %p) has invalid access to address %p.", registerToBeLoaded, base, limit, ref);
    exception = createException(buffer, INVALID_MEMORY_ACCESS);
    Throw(exception);
  }
}

/**
 *  This function store register value into memory
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
  if(base <= (int)ref && limit >= (int)ref) { // Safe area
    *ref = reg[registerToBeStored].data;
  } else {
    sprintf(buffer, "r%d (.base = %p .limit = %p) has invalid access to address %p.", registerToBeStored, base, limit, ref);
    exception = createException(buffer, INVALID_MEMORY_ACCESS);
    Throw(exception);
  }
}