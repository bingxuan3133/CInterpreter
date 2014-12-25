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
  myfile = fopen("myFirstByteCode", "r+");
  int bytecodes[10] = {0};
  char strBuffer[200] = {0};
  bytecodes[0] = getBytecode(myfile);
  bytecodes[1] = getBytecode(myfile);
  bytecodes[2] = getBytecode(myfile);
  bytecodes[3] = 0xffffffff;
  
  disassembleBytecodes(&strBuffer[0], &bytecodes[0]);
  printf("%s\n", strBuffer);
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
  printf("%x\n", fgetc(myfile));
}

void test_run_VirtualMachine(void) {
  int bytecodes[10] = {0};
  char strBuffer[300] = {0};
  bytecodes[0] = dumpr(REG_0);
  bytecodes[1] = dumpr(REG_1);
  bytecodes[2] = ldrImm(REG_0, 50);
  bytecodes[3] = ldrImm(REG_1, 100);
  bytecodes[4] = dumpr(REG_0);
  bytecodes[5] = dumpr(REG_1);
  bytecodes[6] = add(REG_0, REG_1, REG_0);
  bytecodes[7] = dumpr(REG_0);
  bytecodes[8] = dumpr(REG_1);
  bytecodes[9] = 0xffffffff;
  
  runVM(bytecodes);
}