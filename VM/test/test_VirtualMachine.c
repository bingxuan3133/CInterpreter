#include "unity.h"
#include "VirtualMachine.h"
#include "Instruction.h"
#include "Disassembler.h"
#include "Exception.h"

void setUp(void) {
  int i;
  for(i = 0; i < MAX_REG; i ++) {
    reg[i].data = 0;
    reg[i].base = 0;
    reg[i].limit = 0;
  }
}

void tearDown(void)
{
}

void test_explore_function_pointer_array(void) {
  instruction[LDR_IMM](ldrImm(0, 2));
  TEST_ASSERT_EQUAL(2, reg[0].data);
}

void test_read_binary_file(void) {
  FILE *myfile;
  myfile = fopen("../myFirstByteCode", "r+");
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = getBytecode(myfile);
  bytecodes[1] = getBytecode(myfile);
  bytecodes[2] = getBytecode(myfile);
  bytecodes[3] = getBytecode(myfile);
  bytecodes[4] = getBytecode(myfile);
  bytecodes[5] = 0xffffffff;
  
  // printf("%x\n", bytecodes[0]);
  // printf("%x\n", bytecodes[1]);
  // printf("%x\n", bytecodes[2]);
  // printf("%x\n", bytecodes[3]);
  // printf("%x\n", bytecodes[4]);
  // printf("%x\n", getBytecode(myfile));
  // printf("%x\n", getBytecode(myfile));
  // printf("%x\n", getBytecode(myfile));
  
  disassembleBytecodes(&strBuffer[0], &bytecodes[0]);
  printf("%s\n", strBuffer);
}

void test_run_VirtualMachine(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = dumpr(REG_0);
  bytecodes[1] = dumpr(REG_1);
  bytecodes[2] = ldrImm(REG_0, 0x50);
  bytecodes[3] = ldrImm(REG_1, 0x100);
  bytecodes[4] = dumpr(REG_0);
  bytecodes[5] = dumpr(REG_1);
  bytecodes[6] = add(REG_0, REG_1, REG_0);
  bytecodes[7] = dumpr(REG_0);
  bytecodes[8] = dumpr(REG_1);
  bytecodes[9] = 0xffffffff;
  
  VMRun(bytecodes);
}

void test_run_VirtualMachine_testcode(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = 10229;
  bytecodes[1] = 0xffffffff;

  VMRun(bytecodes);
}

void test_stepVM(void) {
  int programCounter = 0;
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = ldrImm(REG_0, 0x50);
  bytecodes[1] = ldrImm(REG_0, 0x100);

  VMStep(bytecodes[0]);
  TEST_ASSERT_EQUAL_HEX(0x50, reg[REG_0].data);
  VMStep(bytecodes[1]);
  TEST_ASSERT_EQUAL_HEX(0x100, reg[REG_0].data);
}

void test_stepVM_will_reset(void) {
  int programCounter = 0;
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = ldrImm(REG_0, 0x50);
  bytecodes[1] = ldrImm(REG_0, 0x100);

  VMStep(bytecodes[0]);
  TEST_ASSERT_EQUAL_HEX(0x50, reg[REG_0].data);
  VMStep(bytecodes[1]);
  TEST_ASSERT_EQUAL_HEX(0x100, reg[REG_0].data);
}

void xtest_VMLoad(void) {
  int bytecodes[10] = {0};
  VMLoad("../myFirstByteCode", bytecodes);
  
  TEST_ASSERT_EQUAL_HEX(bytecodes[0], stm(REG_7, R3, DEC, NO_UPDATE));
  TEST_ASSERT_EQUAL_HEX(bytecodes[1], ldrMem(REG_12, REG_3, 8));
  TEST_ASSERT_EQUAL_HEX(bytecodes[2], ldrImm(REG_13, 2));
  TEST_ASSERT_EQUAL_HEX(bytecodes[3], 0xffffffff);
}