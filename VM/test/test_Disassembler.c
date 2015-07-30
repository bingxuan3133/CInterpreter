#include "unity.h"
#include "Disassembler.h"
#include "Exception.h"
#include "VirtualMachine.h"
#include "Instruction.h"
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
  bytecode[3] = ldrMem(12, 3, 8);

	disassembleBytecode(&buffer[0], bytecode[0]);
  printf("%s\n", buffer);
	disassembleBytecode(&buffer[20], bytecode[1]);
  printf("%s\n", &buffer[20]);
	disassembleBytecode(&buffer[40], bytecode[2]);
  printf("%s\n", &buffer[40]);
  disassembleBytecode(&buffer[60], bytecode[3]);
  printf("%s\n", &buffer[60]);
}

void test_disassembleBytecodes_should_disassemble_an_array_of_bytecode(void) {
  char buffer[500] = {0};
  int bytecode[20] = {0};
  bytecode[0] = ldrImm(REG_4, -128);
  bytecode[1] = ldrMem(REG_0, REG_1, 8);
  bytecode[2] = strMem(REG_0, REG_1, 8);
  bytecode[3] = ldrMemSafe(REG_0, REG_1, 8);
  bytecode[4] = strMemSafe(REG_0, REG_1, 8);
  bytecode[5] = movReg(REG_0, DATA, REG_4, NOP, NOP);
  bytecode[6] = movReg(REG_0, DATA, REG_4, LSL, 4);
  bytecode[7] = movReg(REG_0, DATA, REG_4, LSR, 2);
  bytecode[8] = movReg(REG_0, DATA, REG_4, ASR, 6);
  bytecode[9] = movReg(REG_0, DATA, REG_4, RR, 5);
  bytecode[10] = ldm(REG_7, R4|R5|R6, INC, UPDATE);
  bytecode[11] = ldm(REG_7, R0|R5|R6, DEC, NO_UPDATE);
  bytecode[12] = stm(REG_7, R1|R2|R5|R6, DEC, UPDATE);
  bytecode[13] = stm(REG_7, R3|R4|R5|R6, INC, NO_UPDATE);
  bytecode[14] = ldms(REG_7, R3|R4|R5|R6, INC, NO_UPDATE);
  bytecode[15] = stms(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, NO_UPDATE);
  bytecode[16] = 0xFFFFFFFF; // Indicates end of bytecodes

  disassembleBytecodes(&buffer[0], &bytecode[0]);
  printf("%s\n", &buffer[0]);
}

void test_disassemble_arithmetic(void) {
  char buffer[500] = {0};
  int bytecode[20] = {0};
  bytecode[0] = add(REG_0, REG_0, REG_1);
  bytecode[1] = sub(REG_0, REG_0, REG_1);
  bytecode[2] = mul(REG_1, REG_0, REG_0, REG_1);
  bytecode[3] = div(REG_0, REG_1, REG_0, REG_1);
  bytecode[4] = and(REG_0, REG_0, REG_1);
  bytecode[5] = or(REG_0, REG_0, REG_1);
  bytecode[6] = xor(REG_0, REG_0, REG_1);
  bytecode[7] = 0xFFFFFFFF;

  disassembleBytecodes(&buffer[0], &bytecode[0]);
  printf("%s\n", &buffer[0]);
}
