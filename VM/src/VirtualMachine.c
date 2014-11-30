#include "VirtualMachine.h"
#include "Stack.h"

int reg[8];

int getBits(int data, unsigned char start, unsigned char length) {
  int result;
  result = data >> (start - length + 1);
  result = result & (0xFFFFFFFF >> (32 - length));
  return result;
}

void loadRegisterLiteral(int operand) {
  int regIndex = getBits(operand, 23, 3);
  int value = getBits(operand, 20, 21);
  if(getBits(value, 20, 1)) // value is - signed
    value = 0xFFE00000 | value;
  reg[regIndex] = value;
}

void add() {
  int result;
  int value2 = pop();
  int value1 = pop();
  
  result = value1 + value2;
  push(result);
}

void subtract() {
  int result;
  int value2 = pop();
  int value1 = pop();
  
  result = value1 - value2;
  push(result);
}

void multiply() {
  int result;
  int value2 = pop();
  int value1 = pop();
  
  result = value1 * value2;
  push(result);
}

void divide() {
  int result;
  int value2 = pop();
  int value1 = pop();
  
  result = value1 / value2;
  push(result);
}