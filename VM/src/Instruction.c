#include "Instruction.h"
#include <stdio.h>

Register reg[8];

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
 *  Input:  operand
 */
void loadRegisterWithLiteral(int operand) {
  int regIndex = getBits(operand, 2, 3);
  int value = getBits(operand, 23, 21);
  if(getBits(value, 23, 1)) // value is - signed
    value = 0xFFE00000 | value;
  reg[regIndex].data = value;
}

/**
 *  This function load register with value in the reference
 *  Input:  operand
 */
void loadRegisterWithReference(int operand) {
  int *ref;
  int registerToBeLoaded = getBits(operand, 2, 3);
  int referenceRegister = getBits(operand, 5, 3);
  int relativeAddress = getBits(operand, 23, 18);
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  reg[registerToBeLoaded].data = *ref;
}

/**
 *  This function store register into a reference
 *  Input:  operand
 */
void storeRegisterIntoReference(int operand) {
  int *ref;
  int registerToBeStored = getBits(operand, 2, 3);
  int referenceRegister = getBits(operand, 5, 3);
  int relativeAddress = getBits(operand, 23, 18);
  ref = (int *)(reg[referenceRegister].data + relativeAddress);
  *ref = reg[registerToBeStored].data;
}

/**
 *  This function move value of a register into another register
 *  Input:  operand
 */
void moveRegister(int operand) {
  int destination = getBits(operand, 2, 3);
  int source = getBits(operand, 5, 3);
  reg[destination].data = reg[source].data;
}