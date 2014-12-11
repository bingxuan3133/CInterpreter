#include "unity.h"
#include "Disassembler.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

void setUp(void)
{
}

void tearDown(void)
{
}

void test_dissembleBytecode(void) {
  char buffer[100] = {0};
  int bytecode[10] = {0};
  bytecode[0] = ldrImm(0, 4);
  bytecode[1] = ldrMem(0, 1, 8);
  bytecode[2] = strMem(0, 1, 8);
  bytecode[3] = movReg(0, 4);
  bytecode[4] = 0xFFFFFFFF;
	disassembleBytecode(&buffer[0], &bytecode[0]);
  printf("%s\n", buffer);
	disassembleBytecode(&buffer[20], &bytecode[1]);
  printf("%s\n", &buffer[20]);
	disassembleBytecode(&buffer[40], &bytecode[2]);
  printf("%s\n", &buffer[40]);
	disassembleBytecode(&buffer[60], &bytecode[3]);
  printf("%s\n", &buffer[60]);
}

void test_disassembleBytecodes_should_disassemble_an_array_of_bytecode(void) {
  char buffer[100] = {0};
  int bytecode[10] = {0};
  bytecode[0] = ldrImm(0, 4);
  bytecode[1] = ldrMem(0, 1, 8);
  bytecode[2] = strMem(0, 1, 8);
  bytecode[3] = movReg(0, 4);
  bytecode[4] = 0xFFFFFFFF; // Indicates end of bytecodes

  disassembleBytecodes(&buffer[0], &bytecode[0]);
  printf("%s\n", &buffer[0]);
}
