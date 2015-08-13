#include "unity.h"
#include "VirtualMachine.h"
#include "Instruction.h"
#include "Disassembler.h"
#include "Exception.h"
#include "Print.h"

void setUp(void) {
  VMinit(10, NULL);
}

void tearDown(void) {

}
/*
void xtest_explore_function_pointer_array(void) {
  instruction[LDR_IMM](ldrImm(0, 2));
  TEST_ASSERT_EQUAL(2, reg[0].data);
}

void xtest_read_binary_file(void) {
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
*/

void test_VMinit(void) {
  VMinit(100, NULL);
  TEST_ASSERT_EQUAL((int)(memoryStack+100), reg[7].data);
  VMinit(100, NULL);
  TEST_ASSERT_EQUAL(100, reg[7].limit);
}

void test_VMRun(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  printf("start\n");
  bytecodes[0] = dumprHex(REG_0);
  bytecodes[1] = dumprHex(REG_1);
  bytecodes[2] = ldrImm(REG_0, 0x50);
  bytecodes[3] = ldrImm(REG_1, 0x100);
  bytecodes[4] = dumprHex(REG_0);
  bytecodes[5] = dumprHex(REG_1);
  bytecodes[6] = add(REG_0, REG_1, REG_0);
  bytecodes[7] = dumprHex(REG_0);
  bytecodes[8] = dumprHex(REG_1);
  bytecodes[9] = 0xffffffff;
  VMLoad(bytecodes, 10);
  VMRun();
  printf("stop\n");
}

void test_VMStep_test(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = halt();
  VMLoad(bytecodes, 1);
  VMStep(bytecodes);
}

void test_VMStep(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = ldrImm(REG_0, 0x50);
  bytecodes[1] = ldrImm(REG_0, 0x100);
  VMLoad(bytecodes, 2);
  VMStep();
  TEST_ASSERT_EQUAL_HEX(0x50, reg[REG_0].data);
  VMStep();
  TEST_ASSERT_EQUAL_HEX(0x100, reg[REG_0].data);
}

void test_Proxy_VMStep(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = ldrMemSafe(REG_0, REG_0, 0x01); // <-- invalid memory access
  Exception *exception;
  VMLoad(bytecodes, 1);
  exception = VMStep();
  TEST_ASSERT_NOT_NULL(exception);
  TEST_ASSERT_EQUAL(INVALID_MEMORY_ACCESS, exception->errCode);
  TEST_ASSERT_EQUAL(ldrMemSafe(REG_0, REG_0, 0x01), exception->bc);
  TEST_ASSERT_EQUAL(0, exception->pc);
  freeException(exception);
}

void test_Proxy_VMRun(void) {
  int bytecodes[11] = {0};
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
  bytecodes[9] = ldrMemSafe(REG_0, REG_1, 0x00); // <-- invalid memory access
  bytecodes[10] = halt();
  Exception *exception;
  
  VMLoad(bytecodes, 11);
  exception = VMRun(bytecodes);
  TEST_ASSERT_NOT_NULL(exception);
  TEST_ASSERT_EQUAL(INVALID_MEMORY_ACCESS, exception->errCode);
  TEST_ASSERT_EQUAL(9, exception->pc);
  TEST_ASSERT_EQUAL_HEX(ldrMemSafe(REG_0, REG_1, 0x00), exception->bc);
  freeException(exception);
}

void test_Proxy_VMRun_should_return_INVALID_BYTECODE_exception(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = 0x01230123;  // invalid bytecode
  bytecodes[1] = halt();
  Exception *exception;
  
  VMLoad(bytecodes, 2);
  exception = VMRun(bytecodes);
  TEST_ASSERT_NOT_NULL(exception);
  TEST_ASSERT_EQUAL_STRING("ERROR: invalid bytecode (0x01230123, pc = 0).", exception->errMsg);
  TEST_ASSERT_EQUAL(INVALID_BYTECODE, exception->errCode);
  TEST_ASSERT_EQUAL(0, exception->pc);
  TEST_ASSERT_EQUAL_HEX(0x01230123, exception->bc);
  freeException(exception);
}

// void test_VMStep_test2(void) {
  // int bytecodes[10] = {1793, 8194, 1793, 16141, 538628, 11522, 1286, 4294967295, 0xffffffff};
  // char strBuffer[300] = {0};
  // Exception *exception;
  
  // exception = VMRun(bytecodes);
  // freeException(exception);
// }
